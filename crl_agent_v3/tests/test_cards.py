from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import replace

import pytest

from crl_v3.knowledge import KnowledgeStore, Paper, Passage


def _metadata(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": 1,
        "card_id": "operator-verifier-guided-search",
        "card_kind": "operator",
        "paper_id": "paper-a",
        "evidence_ids": ["evidence-method"],
        "source_refs": [
            {"path": "papers/paper-a.pdf", "sha256": "a" * 64}
        ],
    }
    value.update(overrides)
    return value


def _write_operator_card(
    tmp_path,
    *,
    metadata: dict[str, object] | None = None,
    body: str | None = None,
    file_id: str = "operator-verifier-guided-search",
    parent_kind: str = "operator",
):
    card_path = tmp_path / "cards" / parent_kind / f"{file_id}.md"
    card_path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "<!-- CRL_CARD_META "
        + json.dumps(metadata or _metadata(), sort_keys=True)
        + " -->\n"
        + (body or _operator_body())
    )
    card_path.write_text(text, encoding="utf-8", newline="\n")
    return card_path


def _body_for(kind: str, evidence_id: str) -> str:
    if kind == "operator":
        return _operator_body(evidence_id)
    headings = {
        "paper": (
            "Role in the knowledge base",
            "Problem and setting",
            "Changed computation",
            "Evidence-backed findings",
            "Limitations and failure signals",
            "Lineage and baselines",
            "Evidence ledger",
            "Retrieval vocabulary",
        ),
        "failure": (
            "Observed failure",
            "Conditions and scope",
            "Failed intervention",
            "Evidence and alternative explanations",
            "Warning for future candidates",
            "Possible repair boundary",
            "Evidence ledger",
            "Retrieval vocabulary",
        ),
    }[kind]
    sections = []
    for index, heading in enumerate(headings):
        if index == 0:
            content = f"[AUTHOR_FACT] Bound claim. [[evidence:{evidence_id}]]"
        else:
            content = "[CODEX_SYNTHESIS] Mechanical test content."
        sections.append(f"## {heading}\n\n{content}")
    return f"# {kind.title()} test card\n\n" + "\n\n".join(sections) + "\n"


def _write_card(
    cards_root,
    *,
    kind: str,
    card_id: str,
    evidence_ids: tuple[str, ...],
    source_refs: tuple[tuple[str, str], ...],
    paper_id: str | None,
    body: str | None = None,
):
    path = cards_root / kind / f"{card_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "schema_version": 1,
        "card_id": card_id,
        "card_kind": kind,
        "paper_id": paper_id,
        "evidence_ids": list(evidence_ids),
        "source_refs": [
            {"path": source_path, "sha256": source_sha}
            for source_path, source_sha in source_refs
        ],
    }
    text = (
        "<!-- CRL_CARD_META "
        + json.dumps(metadata, sort_keys=True)
        + " -->\n"
        + (body or _body_for(kind, evidence_ids[0]))
    )
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _setup_store(tmp_path, *, include_second_paper: bool = False):
    project_root = tmp_path / "knowledge_base"
    papers_root = project_root / "papers"
    papers_root.mkdir(parents=True)
    source_a = papers_root / "paper-a.pdf"
    source_a.write_bytes(b"paper-a-pdf-bytes")
    sha_a = hashlib.sha256(source_a.read_bytes()).hexdigest()
    passage_text = "prefix verification changes selection suffix"
    passage_a = Passage(
        passage_id="passage-a",
        paper_id="paper-a",
        section="Methods",
        page_start=2,
        page_end=2,
        char_start=0,
        char_end=len(passage_text),
        text=passage_text,
        text_sha256=hashlib.sha256(passage_text.encode()).hexdigest(),
    )
    paper_a = Paper(
        paper_id="paper-a",
        title="Paper A",
        year=2025,
        source="test",
        venue="Test Venue",
        publication_status="preprint",
        fulltext_path="papers/paper-a.pdf",
        fulltext_sha256=sha_a,
    )
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    store.add_paper(paper_a, [passage_a])
    quote = "verification changes selection"
    quote_start = passage_text.index(quote)
    store.add_evidence(
        evidence_id="evidence-a",
        paper_id="paper-a",
        fulltext_sha256=sha_a,
        evidence_kind="text",
        section="Methods",
        page_start=2,
        page_end=2,
        locator="paragraph 1",
        source_content=quote,
        codex_note="Mechanical fixture evidence.",
        passage_id=passage_a.passage_id,
        passage_text_sha256=passage_a.text_sha256,
        quote_start=quote_start,
        quote_end=quote_start + len(quote),
    )
    result = {
        "store": store,
        "project_root": project_root,
        "source_a": source_a,
        "sha_a": sha_a,
        "paper_a": paper_a,
        "passage_a": passage_a,
    }
    if include_second_paper:
        source_b = papers_root / "paper-b.pdf"
        source_b.write_bytes(b"paper-b-pdf-bytes")
        sha_b = hashlib.sha256(source_b.read_bytes()).hexdigest()
        paper_b = Paper(
            paper_id="paper-b",
            title="Paper B",
            year=2024,
            source="test",
            venue="Test Venue",
            publication_status="preprint",
            fulltext_path="papers/paper-b.pdf",
            fulltext_sha256=sha_b,
        )
        store.add_paper(paper_b, [])
        store.add_evidence(
            evidence_id="evidence-b",
            paper_id="paper-b",
            fulltext_sha256=sha_b,
            evidence_kind="figure",
            section="Results",
            page_start=4,
            page_end=4,
            locator="figure 2",
            source_content="negative result",
            codex_note="Second paper fixture.",
        )
        result.update(source_b=source_b, sha_b=sha_b, paper_b=paper_b)
    return result


def _operator_body(evidence_id: str = "evidence-method") -> str:
    return f"""# Verifier-guided search

## Intervention target

[AUTHOR_FACT] Verification changes the selected plan. [[evidence:{evidence_id}]]

## Before and after computation

[CODEX_SYNTHESIS] Baseline selection becomes verifier-guided selection.

## Inputs outputs information and timing

[CODEX_SYNTHESIS] The intervention consumes candidate plans before execution.

## Mechanism hypothesis

[CODEX_HYPOTHESIS] Rejecting unsupported plans may improve action selection.

## Predicted observable signature

[CODEX_HYPOTHESIS] Plan changes should concentrate on verifier disagreements.

## Preconditions and transfer risks

[CODEX_SYNTHESIS] The verifier must not receive oracle information.

## Source lineage

[CODEX_SYNTHESIS] Record direct sources and related mechanisms here.

## Evidence ledger

[CODEX_SYNTHESIS] {evidence_id} supports the changed computation.

## Retrieval vocabulary

[CODEX_SYNTHESIS] verifier guided search, plan selection.
"""


def test_parse_valid_operator_card(tmp_path) -> None:
    from crl_v3.cards import CardDocument, CardMetadata, SourceRef, parse_card

    cards_root = tmp_path / "cards"
    card_path = cards_root / "operator" / "operator-verifier-guided-search.md"
    card_path.parent.mkdir(parents=True)
    pdf_sha256 = "a" * 64
    metadata = {
        "schema_version": 1,
        "card_id": "operator-verifier-guided-search",
        "card_kind": "operator",
        "paper_id": "paper-a",
        "evidence_ids": ["evidence-method"],
        "source_refs": [
            {"path": "papers/paper-a.pdf", "sha256": pdf_sha256}
        ],
    }
    text = (
        "<!-- CRL_CARD_META "
        + json.dumps(metadata, sort_keys=True)
        + " -->\n"
        + _operator_body()
    )
    card_path.write_text(text, encoding="utf-8", newline="\n")

    card = parse_card(card_path)

    assert isinstance(card, CardDocument)
    assert card.metadata == CardMetadata(
        schema_version=1,
        card_id="operator-verifier-guided-search",
        card_kind="operator",
        paper_id="paper-a",
        evidence_ids=("evidence-method",),
        source_refs=(
            SourceRef(path="papers/paper-a.pdf", sha256=pdf_sha256),
        ),
    )
    assert card.title == "Verifier-guided search"
    assert card.sha256 == hashlib.sha256(card_path.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    ("raw_builder", "message"),
    [
        (lambda raw: b"\xef\xbb\xbf" + raw, "UTF-8 BOM"),
        (lambda raw: raw.replace(b"Verifier", b"\xffVerifier", 1), "invalid UTF-8"),
        (lambda raw: raw.replace(b"\n", b"\r\n"), "CRLF"),
    ],
)
def test_parse_rejects_noncanonical_text_bytes(tmp_path, raw_builder, message) -> None:
    from crl_v3.cards import parse_card

    card_path = _write_operator_card(tmp_path)
    card_path.write_bytes(raw_builder(card_path.read_bytes()))

    with pytest.raises(ValueError, match=message):
        parse_card(card_path)


@pytest.mark.parametrize(
    ("metadata", "message"),
    [
        ({k: v for k, v in _metadata().items() if k != "schema_version"}, "metadata fields"),
        ({**_metadata(), "extra": True}, "metadata fields"),
        (_metadata(schema_version=2), "schema_version"),
        (_metadata(card_id="Bad ID"), "card_id"),
        (_metadata(card_kind="memory"), "card_kind"),
        (_metadata(paper_id=7), "paper_id"),
        (_metadata(evidence_ids=[]), "evidence_ids"),
        (_metadata(evidence_ids=["evidence-method", "evidence-method"]), "duplicate evidence_id"),
        (_metadata(source_refs=[]), "source_refs"),
        (_metadata(source_refs=[{"path": "papers/a.pdf", "sha256": "ABC"}]), "sha256"),
        (_metadata(source_refs=[{"path": "papers/a.pdf", "sha256": "a" * 64, "extra": 1}]), "source_ref fields"),
    ],
)
def test_parse_rejects_invalid_metadata(tmp_path, metadata, message) -> None:
    from crl_v3.cards import parse_card

    card_path = _write_operator_card(tmp_path, metadata=metadata)

    with pytest.raises(ValueError, match=message):
        parse_card(card_path)


@pytest.mark.parametrize(
    ("source_path", "message"),
    [
        ("C:/papers/paper-a.pdf", "relative POSIX"),
        ("../papers/paper-a.pdf", "relative POSIX"),
        ("papers\\paper-a.pdf", "relative POSIX"),
    ],
)
def test_parse_rejects_noncanonical_source_paths(tmp_path, source_path, message) -> None:
    from crl_v3.cards import parse_card

    metadata = _metadata(
        source_refs=[{"path": source_path, "sha256": "a" * 64}]
    )
    card_path = _write_operator_card(tmp_path, metadata=metadata)

    with pytest.raises(ValueError, match=message):
        parse_card(card_path)


def test_parse_rejects_card_id_file_name_mismatch(tmp_path) -> None:
    from crl_v3.cards import parse_card

    card_path = _write_operator_card(tmp_path, file_id="operator-other")

    with pytest.raises(ValueError, match="card_id.*file name"):
        parse_card(card_path)


def test_parse_rejects_kind_directory_mismatch(tmp_path) -> None:
    from crl_v3.cards import parse_card

    card_path = _write_operator_card(tmp_path, parent_kind="failure")

    with pytest.raises(ValueError, match="card_kind.*directory"):
        parse_card(card_path)


def test_parse_rejects_missing_duplicate_headings_and_extra_h1(tmp_path) -> None:
    from crl_v3.cards import parse_card

    missing = _write_operator_card(
        tmp_path / "missing",
        body=_operator_body().replace("## Predicted observable signature\n", ""),
    )
    duplicate = _write_operator_card(
        tmp_path / "duplicate",
        body=_operator_body() + "\n## Intervention target\n\n[CODEX_SYNTHESIS] duplicate\n",
    )
    extra_h1 = _write_operator_card(
        tmp_path / "extra-h1",
        body=_operator_body() + "\n# Another title\n",
    )

    with pytest.raises(ValueError, match="required heading"):
        parse_card(missing)
    with pytest.raises(ValueError, match="required heading"):
        parse_card(duplicate)
    with pytest.raises(ValueError, match="unique H1"):
        parse_card(extra_h1)


def test_parse_rejects_unknown_fact_label(tmp_path) -> None:
    from crl_v3.cards import parse_card

    body = _operator_body().replace("[CODEX_SYNTHESIS]", "[READER_INTERPRETATION]", 1)
    card_path = _write_operator_card(tmp_path, body=body)

    with pytest.raises(ValueError, match="unknown fact label"):
        parse_card(card_path)


def test_parse_rejects_second_metadata_comment(tmp_path) -> None:
    from crl_v3.cards import parse_card

    body = "<!-- CRL_CARD_META {} -->\n" + _operator_body()
    card_path = _write_operator_card(tmp_path, body=body)

    with pytest.raises(ValueError, match="metadata comment.*unique"):
        parse_card(card_path)


def test_validate_card_accepts_current_evidence_and_nullable_paper(tmp_path) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    path = _write_card(
        tmp_path / "cards",
        kind="operator",
        card_id="operator-current-evidence",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
        paper_id=None,
    )

    validate_card(
        parse_card(path),
        store=fixture["store"],
        project_root=fixture["project_root"],
    )
    fixture["store"].close()


@pytest.mark.parametrize(
    ("evidence_ids", "body_evidence", "message"),
    [
        (("missing-evidence",), "missing-evidence", "Evidence.*not found"),
        (("evidence-a",), "undeclared-evidence", "metadata.*Evidence"),
        (("evidence-a", "unused-evidence"), "evidence-a", "unused.*Evidence"),
    ],
)
def test_validate_card_rejects_missing_or_mismatched_evidence_tokens(
    tmp_path, evidence_ids, body_evidence, message
) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    path = _write_card(
        tmp_path / "cards",
        kind="operator",
        card_id="operator-evidence-binding",
        evidence_ids=evidence_ids,
        source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
        paper_id=None,
        body=_body_for("operator", body_evidence),
    )

    with pytest.raises(ValueError, match=message):
        validate_card(
            parse_card(path),
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    fixture["store"].close()


def test_validate_card_requires_inline_evidence_for_author_claim(tmp_path) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    body = _body_for("operator", "evidence-a").replace(
        "[AUTHOR_FACT] Verification changes the selected plan. [[evidence:evidence-a]]",
        "[AUTHOR_FACT] Verification changes the selected plan.",
    )
    body = body.replace(
        "[CODEX_SYNTHESIS] evidence-a supports the changed computation.",
        "[CODEX_SYNTHESIS] evidence-a supports the changed computation. [[evidence:evidence-a]]",
    )
    path = _write_card(
        tmp_path / "cards",
        kind="operator",
        card_id="operator-missing-inline",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
        paper_id=None,
        body=body,
    )

    with pytest.raises(ValueError, match="AUTHOR_FACT.*inline Evidence"):
        validate_card(
            parse_card(path),
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    fixture["store"].close()


def test_validate_card_allows_evidence_later_in_same_paragraph(tmp_path) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    body = _body_for("operator", "evidence-a").replace(
        "[AUTHOR_FACT] Verification changes the selected plan. [[evidence:evidence-a]]",
        "[AUTHOR_FACT] Verification changes the selected plan.\n"
        "The same paragraph binds [[evidence:evidence-a]].",
    )
    path = _write_card(
        tmp_path / "cards",
        kind="operator",
        card_id="operator-multiline-author-fact",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
        paper_id=None,
        body=body,
    )

    validate_card(
        parse_card(path),
        store=fixture["store"],
        project_root=fixture["project_root"],
    )
    fixture["store"].close()


def test_validate_card_rejects_stale_fulltext_evidence(tmp_path) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    path = _write_card(
        tmp_path / "cards",
        kind="operator",
        card_id="operator-stale-fulltext",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
        paper_id=None,
    )
    fixture["store"].add_paper(
        replace(fixture["paper_a"], fulltext_sha256="b" * 64),
        [fixture["passage_a"]],
    )

    with pytest.raises(ValueError, match="stale Evidence.*fulltext"):
        validate_card(
            parse_card(path),
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    fixture["store"].close()


def test_validate_card_rejects_stale_passage_anchor(tmp_path) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    path = _write_card(
        tmp_path / "cards",
        kind="failure",
        card_id="failure-stale-passage",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
        paper_id="paper-a",
    )
    changed = replace(
        fixture["passage_a"],
        text="changed passage text",
        text_sha256=hashlib.sha256(b"changed passage text").hexdigest(),
    )
    fixture["store"].add_paper(fixture["paper_a"], [changed])

    with pytest.raises(ValueError, match="stale Evidence.*passage"):
        validate_card(
            parse_card(path),
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    fixture["store"].close()


@pytest.mark.parametrize("failure", ["missing", "hash", "coverage"])
def test_validate_card_rejects_invalid_source_binding(tmp_path, failure) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    source_path = "papers/paper-a.pdf"
    source_sha = fixture["sha_a"]
    if failure == "missing":
        source_path = "papers/missing.pdf"
    elif failure == "hash":
        source_sha = "f" * 64
    else:
        unrelated = fixture["project_root"] / "papers" / "unrelated.pdf"
        unrelated.write_bytes(b"unrelated")
        source_path = "papers/unrelated.pdf"
        source_sha = hashlib.sha256(unrelated.read_bytes()).hexdigest()
    path = _write_card(
        tmp_path / "cards",
        kind="operator",
        card_id=f"operator-source-{failure}",
        evidence_ids=("evidence-a",),
        source_refs=((source_path, source_sha),),
        paper_id=None,
    )

    expected = {
        "missing": "source file.*not found",
        "hash": "source.*SHA-256",
        "coverage": "Evidence.*fulltext SHA-256",
    }[failure]
    with pytest.raises(ValueError, match=expected):
        validate_card(
            parse_card(path),
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    fixture["store"].close()


def test_validate_paper_card_requires_existing_paper(tmp_path) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    path = _write_card(
        tmp_path / "cards",
        kind="paper",
        card_id="paper-missing",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
        paper_id="paper-missing",
    )

    with pytest.raises(ValueError, match="paper_id.*not found"):
        validate_card(
            parse_card(path),
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    fixture["store"].close()


def test_validate_paper_card_requires_evidence_from_same_paper(tmp_path) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path, include_second_paper=True)
    path = _write_card(
        tmp_path / "cards",
        kind="paper",
        card_id="paper-cross-source",
        evidence_ids=("evidence-b",),
        source_refs=(("papers/paper-b.pdf", fixture["sha_b"]),),
        paper_id="paper-a",
    )

    with pytest.raises(ValueError, match="Paper Card Evidence.*paper_id"):
        validate_card(
            parse_card(path),
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    fixture["store"].close()


def test_load_valid_cards_sorts_known_kind_directories(tmp_path) -> None:
    from crl_v3.cards import load_valid_cards

    fixture = _setup_store(tmp_path)
    cards_root = tmp_path / "cards"
    for kind, card_id in (
        ("paper", "paper-z"),
        ("failure", "failure-a"),
        ("operator", "operator-m"),
    ):
        _write_card(
            cards_root,
            kind=kind,
            card_id=card_id,
            evidence_ids=("evidence-a",),
            source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
            paper_id="paper-a",
        )
    staging = cards_root / "staging" / "ignored.md"
    staging.parent.mkdir(parents=True)
    staging.write_text("not a card", encoding="utf-8")

    cards = load_valid_cards(
        cards_root,
        store=fixture["store"],
        project_root=fixture["project_root"],
    )

    assert [card.metadata.card_id for card in cards] == [
        "failure-a",
        "operator-m",
        "paper-z",
    ]
    fixture["store"].close()


def test_load_valid_cards_rejects_duplicate_card_id(tmp_path) -> None:
    from crl_v3.cards import load_valid_cards

    fixture = _setup_store(tmp_path)
    cards_root = tmp_path / "cards"
    for kind in ("failure", "operator"):
        _write_card(
            cards_root,
            kind=kind,
            card_id="shared-card-id",
            evidence_ids=("evidence-a",),
            source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
            paper_id="paper-a",
        )

    with pytest.raises(ValueError, match="duplicate card_id"):
        load_valid_cards(
            cards_root,
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    fixture["store"].close()


def _write_search_cards(tmp_path, fixture):
    cards_root = tmp_path / "cards"
    failure_body = _body_for("failure", "evidence-a").replace(
        "[CODEX_SYNTHESIS] Mechanical test content.",
        "[CODEX_SYNTHESIS] Correlated errors repeat without independent evidence.",
        1,
    )
    operator_body = _body_for("operator", "evidence-a").replace(
        "[CODEX_SYNTHESIS] Baseline selection becomes verifier-guided selection.",
        "[CODEX_SYNTHESIS] Verifier guided search changes which plan is executed.",
    )
    paper_body = _body_for("paper", "evidence-a").replace(
        "[CODEX_SYNTHESIS] Mechanical test content.",
        "[CODEX_SYNTHESIS] Direct ancestor of interleaved reasoning and tool acting.",
        1,
    )
    paths = {
        "failure": _write_card(
            cards_root,
            kind="failure",
            card_id="failure-correlated-errors",
            evidence_ids=("evidence-a",),
            source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
            paper_id="paper-a",
            body=failure_body,
        ),
        "operator": _write_card(
            cards_root,
            kind="operator",
            card_id="operator-verifier-search",
            evidence_ids=("evidence-a",),
            source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
            paper_id="paper-a",
            body=operator_body,
        ),
        "paper": _write_card(
            cards_root,
            kind="paper",
            card_id="paper-interleaved-reasoning",
            evidence_ids=("evidence-a",),
            source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
            paper_id="paper-a",
            body=paper_body,
        ),
    }
    return cards_root, paths


def test_rebuild_card_index_and_search_each_kind(tmp_path) -> None:
    from crl_v3.cards import (
        CardIndexBuildResult,
        CardSearchHit,
        card_index_status,
        card_source_signature,
        parse_card,
        rebuild_card_index,
        search_cards,
    )

    fixture = _setup_store(tmp_path)
    cards_root, paths = _write_search_cards(tmp_path, fixture)
    index_path = tmp_path / "derived" / "cards_fts.sqlite"

    result = rebuild_card_index(
        cards_root,
        index_path,
        store=fixture["store"],
        project_root=fixture["project_root"],
    )

    assert isinstance(result, CardIndexBuildResult)
    assert result.index_path == index_path
    assert result.card_count == 3
    assert dict(result.kind_counts) == {"failure": 1, "operator": 1, "paper": 1}
    assert len(result.source_signature) == 64
    ignored = cards_root / "staging" / "not-a-card.md"
    ignored.parent.mkdir()
    ignored.write_text("not indexed\n", encoding="utf-8", newline="\n")
    assert card_source_signature(cards_root) == result.source_signature
    assert card_index_status(cards_root, index_path) == {
        "ready": True,
        "reason": "ready",
        "index_path": str(index_path),
        "cards": 3,
    }
    failure_hits = search_cards(
        cards_root, index_path, "correlated errors", kinds=("failure",), limit=5
    )
    assert all(isinstance(hit, CardSearchHit) for hit in failure_hits)
    assert [hit.card_kind for hit in failure_hits] == ["failure"]
    assert failure_hits[0].markdown_sha256 == parse_card(paths["failure"]).sha256
    operator_hits = search_cards(
        cards_root,
        index_path,
        '"verifier guided" selection',
        kinds=("operator",),
        limit=5,
    )
    assert [hit.card_id for hit in operator_hits] == ["operator-verifier-search"]
    paper_hits = search_cards(
        cards_root,
        index_path,
        "direct ancestor",
        kinds=("paper",),
        limit=5,
    )
    assert [hit.card_id for hit in paper_hits] == ["paper-interleaved-reasoning"]
    fixture["store"].close()


def test_card_index_reports_missing_changed_invalid_and_unsupported(tmp_path) -> None:
    from crl_v3.cards import card_index_status, rebuild_card_index, search_cards

    fixture = _setup_store(tmp_path)
    cards_root, paths = _write_search_cards(tmp_path, fixture)
    index_path = tmp_path / "cards_fts.sqlite"
    assert card_index_status(cards_root, index_path)["reason"] == "index_missing"
    rebuild_card_index(
        cards_root,
        index_path,
        store=fixture["store"],
        project_root=fixture["project_root"],
    )
    path = paths["failure"]
    path.write_text(
        path.read_text(encoding="utf-8") + "\n[CODEX_SYNTHESIS] Source changed.\n",
        encoding="utf-8",
        newline="\n",
    )
    assert card_index_status(cards_root, index_path)["reason"] == "card_sources_changed"
    with pytest.raises(ValueError, match="card_sources_changed"):
        search_cards(cards_root, index_path, "errors", kinds=("failure",))
    rebuild_card_index(
        cards_root,
        index_path,
        store=fixture["store"],
        project_root=fixture["project_root"],
    )
    assert card_index_status(cards_root, index_path)["ready"] is True
    with sqlite3.connect(index_path) as connection:
        connection.execute(
            "UPDATE card_index_metadata SET schema_version = 2 WHERE singleton = 1"
        )
        connection.commit()
    assert card_index_status(cards_root, index_path)["reason"] == "unsupported_schema"
    index_path.write_bytes(b"not a sqlite database")
    assert card_index_status(cards_root, index_path)["reason"] == "index_invalid"
    fixture["store"].close()


def test_search_cards_validates_query_kinds_and_limit(tmp_path) -> None:
    from crl_v3.cards import rebuild_card_index, search_cards

    fixture = _setup_store(tmp_path)
    cards_root, _ = _write_search_cards(tmp_path, fixture)
    index_path = tmp_path / "cards_fts.sqlite"
    rebuild_card_index(
        cards_root,
        index_path,
        store=fixture["store"],
        project_root=fixture["project_root"],
    )

    with pytest.raises(ValueError, match="limit"):
        search_cards(cards_root, index_path, "errors", kinds=("failure",), limit=0)
    with pytest.raises(ValueError, match="kinds"):
        search_cards(cards_root, index_path, "errors", kinds=())
    with pytest.raises(ValueError, match="card kind"):
        search_cards(cards_root, index_path, "errors", kinds=("memory",))
    with pytest.raises(ValueError, match="punctuation"):
        search_cards(cards_root, index_path, "，。", kinds=("failure",))
    forward = search_cards(
        cards_root,
        index_path,
        "evidence",
        kinds=("failure", "operator", "paper"),
    )
    reverse = search_cards(
        cards_root,
        index_path,
        "evidence",
        kinds=("paper", "operator", "failure"),
    )
    assert forward == reverse
    fixture["store"].close()


def test_card_and_passage_queries_share_unicode_normalization() -> None:
    from crl_v3.knowledge import normalize_fts_query

    chinese = normalize_fts_query("工具调用 智能体")
    assert chinese.normalized_query == '"工具调用" OR "智能体"'
    assert chinese.english_keyword_hint
    mixed = normalize_fts_query('"tool use" 智能体 verifier')
    assert mixed.normalized_query == '"tool use" OR "智能体" OR "verifier"'
    assert mixed.english_keyword_hint is None
    with pytest.raises(ValueError, match="punctuation"):
        normalize_fts_query("，。！？")


def test_card_index_schema_is_only_documents_fts_and_metadata(tmp_path) -> None:
    import crl_v3.cards as cards_module
    from crl_v3.cards import rebuild_card_index

    fixture = _setup_store(tmp_path)
    cards_root, _ = _write_search_cards(tmp_path, fixture)
    index_path = tmp_path / "cards_fts.sqlite"
    rebuild_card_index(
        cards_root,
        index_path,
        store=fixture["store"],
        project_root=fixture["project_root"],
    )
    with sqlite3.connect(index_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
    assert tables == {
        "card_documents",
        "card_index_metadata",
        "cards_fts",
        "cards_fts_config",
        "cards_fts_content",
        "cards_fts_data",
        "cards_fts_docsize",
        "cards_fts_idx",
    }
    for forbidden in (
        "generate_card",
        "generate_candidate",
        "write_reviewer_report",
        "judge_research_claim",
    ):
        assert not hasattr(cards_module, forbidden)
    fixture["store"].close()


def test_failed_rebuild_does_not_replace_existing_index(tmp_path) -> None:
    from crl_v3.cards import rebuild_card_index

    fixture = _setup_store(tmp_path)
    cards_root, _ = _write_search_cards(tmp_path, fixture)
    index_path = tmp_path / "cards_fts.sqlite"
    rebuild_card_index(
        cards_root,
        index_path,
        store=fixture["store"],
        project_root=fixture["project_root"],
    )
    before = index_path.read_bytes()
    _write_card(
        cards_root,
        kind="operator",
        card_id="operator-invalid-source",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/missing.pdf", fixture["sha_a"]),),
        paper_id=None,
    )

    with pytest.raises(ValueError, match="source file.*not found"):
        rebuild_card_index(
            cards_root,
            index_path,
            store=fixture["store"],
            project_root=fixture["project_root"],
        )
    assert index_path.read_bytes() == before
    assert not list(index_path.parent.glob("*.tmp"))
    fixture["store"].close()


def test_knowledge_store_rejects_internal_run_source_at_ingestion(tmp_path) -> None:
    fixture = _setup_store(tmp_path)
    paper = Paper(
        paper_id="ire-run-fixture",
        title="Internal run evidence fixture",
        year=2026,
        source="crl-internal-run",
        venue="CRL internal run",
        publication_status="internal_run_evidence",
        fulltext_path="corpus/internal_runs/run-fixture-confirmation-raw.jsonl",
        fulltext_sha256="a" * 64,
    )
    with pytest.raises(ValueError, match="Run-derived papers"):
        fixture["store"].add_paper(paper, [])
    fixture["store"].close()


def test_parse_card_rejects_run_identifier_in_shared_card(tmp_path) -> None:
    from crl_v3.cards import parse_card

    path = _write_card(
        tmp_path / "cards",
        kind="failure",
        card_id="failure-contaminated",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/paper-a.pdf", "a" * 64),),
        paper_id=None,
        body=_body_for("failure", "evidence-a").replace(
            "Mechanical test content.", "Derived from run03.", 1
        ),
    )
    with pytest.raises(ValueError, match="Run-derived material"):
        parse_card(path)


def test_external_card_id_has_no_special_internal_prefix_semantics(tmp_path) -> None:
    from crl_v3.cards import parse_card, validate_card

    fixture = _setup_store(tmp_path)
    path = _write_card(
        tmp_path / "cards",
        kind="failure",
        card_id="internal-prefixed-external-card",
        evidence_ids=("evidence-a",),
        source_refs=(("papers/paper-a.pdf", fixture["sha_a"]),),
        paper_id=None,
        body=_body_for("failure", "evidence-a"),
    )

    validate_card(
        parse_card(path),
        store=fixture["store"],
        project_root=fixture["project_root"],
    )
    fixture["store"].close()
