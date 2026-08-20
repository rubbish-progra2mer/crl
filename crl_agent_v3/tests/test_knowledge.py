from __future__ import annotations

import hashlib
import inspect
import sqlite3

import pytest

from crl_v3.knowledge import KnowledgeStore, Paper, Passage


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _paper(paper_id: str, title: str, fulltext: str) -> Paper:
    return Paper(
        paper_id=paper_id,
        title=title,
        year=2025,
        source="arxiv",
        venue="Test Venue",
        publication_status="preprint",
        fulltext_path=f"fulltext/{paper_id}.md",
        fulltext_sha256=_sha256(fulltext),
    )


def _passage(
    passage_id: str,
    paper_id: str,
    section: str,
    page_start: int,
    page_end: int,
    char_start: int,
    char_end: int,
    text: str,
) -> Passage:
    return Passage(
        passage_id=passage_id,
        paper_id=paper_id,
        section=section,
        page_start=page_start,
        page_end=page_end,
        char_start=char_start,
        char_end=char_end,
        text=text,
        text_sha256=_sha256(text),
    )


def _text_evidence_arguments(paper: Paper, passage: Passage) -> dict[str, object]:
    source_content = "plan first and then call tools"
    quote_start = passage.text.index(source_content)
    return {
        "evidence_id": "evidence-text",
        "paper_id": paper.paper_id,
        "fulltext_sha256": paper.fulltext_sha256,
        "evidence_kind": "text",
        "section": "Methods",
        "page_start": 3,
        "page_end": 3,
        "locator": "right column, second paragraph",
        "source_content": source_content,
        "codex_note": "Codex recorded this as the paper's explicit planning order.",
        "passage_id": passage.passage_id,
        "passage_text_sha256": passage.text_sha256,
        "quote_start": quote_start,
        "quote_end": quote_start + len(source_content),
    }


def test_real_fts_search_preserves_provenance_and_hashes(tmp_path) -> None:
    database = tmp_path / "chosen" / "knowledge.sqlite"
    paper_a = _paper("paper-a", "Alpha Study", "alpha full text")
    paper_b = _paper("paper-b", "Beta Study", "beta full text")
    passages_a = [
        _passage("a-1", "paper-a", "Introduction", 1, 1, 0, 29, "oranges improve alpha retrieval"),
        _passage("a-2", "paper-a", "Results", 4, 5, 30, 63, "controlled evidence supports oranges"),
    ]
    passages_b = [
        _passage("b-1", "paper-b", "Methods", 7, 8, 10, 38, "bananas identify beta retrieval"),
        _passage("b-2", "paper-b", "Conclusion", 9, 9, 39, 68, "beta findings exclude oranges"),
    ]

    store = KnowledgeStore(database, read_only=False)
    store.add_paper(paper_a, passages_a)
    store.add_paper(paper_b, passages_b)

    orange_hits = store.search("oranges")
    banana_hits = store.search("bananas")

    assert {hit.passage_id for hit in orange_hits} == {"a-1", "a-2", "b-2"}
    assert [hit.passage_id for hit in banana_hits] == ["b-1"]
    hit = banana_hits[0]
    assert (
        hit.paper_id,
        hit.title,
        hit.section,
        hit.page_start,
        hit.page_end,
        hit.char_start,
        hit.char_end,
        hit.text,
        hit.fulltext_sha256,
        hit.text_sha256,
    ) == (
        "paper-b",
        "Beta Study",
        "Methods",
        7,
        8,
        10,
        38,
        "bananas identify beta retrieval",
        paper_b.fulltext_sha256,
        passages_b[0].text_sha256,
    )
    assert isinstance(hit.rank, float)
    assert store.get_paper("paper-a") == paper_a
    assert store.get_passage("a-2") == passages_a[1]
    assert database.is_file()
    assert list(tmp_path.rglob("*.sqlite")) == [database]
    store.close()


def test_natural_language_fts_matches_any_query_term(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    paper = _paper("paper-a", "Agent Study", "agent full text")
    passages = [
        _passage(
            "a-1",
            "paper-a",
            "Methods",
            2,
            2,
            0,
            36,
            "agents publish structured artifacts",
        ),
        _passage(
            "a-2",
            "paper-a",
            "Results",
            3,
            3,
            37,
            63,
            "peers revise their answers",
        ),
    ]
    store.add_paper(paper, passages)

    hits = store.search("agents revise answers after reading peers")

    assert {hit.passage_id for hit in hits} == {"a-1", "a-2"}
    store.close()


def test_explicit_fts_phrase_stays_exact(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    paper = _paper("paper-a", "Messaging Study", "message full text")
    passages = [
        _passage(
            "a-1",
            "paper-a",
            "Methods",
            1,
            1,
            0,
            28,
            "agents use a shared message pool",
        ),
        _passage(
            "a-2",
            "paper-a",
            "Discussion",
            2,
            2,
            29,
            62,
            "a shared pool stores every message",
        ),
    ]
    store.add_paper(paper, passages)

    hits = store.search('"shared message pool"')

    assert [hit.passage_id for hit in hits] == ["a-1"]
    store.close()


def test_reingest_replaces_passages_and_removes_old_fts_content(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    store = KnowledgeStore(database, read_only=False)
    original = _paper("paper-a", "Original Title", "original full text")
    old_passage = _passage("a-1", "paper-a", "Old", 2, 2, 0, 18, "obsolete_keyword text")

    store.add_paper(original, [old_passage])
    store.add_paper(original, [old_passage])
    assert len(store.search("obsolete_keyword")) == 1

    updated = _paper("paper-a", "Updated Title", "updated full text")
    new_passage = _passage("a-2", "paper-a", "New", 3, 4, 20, 40, "replacement_keyword text")
    store.add_paper(updated, [new_passage])

    assert store.search("obsolete_keyword") == []
    assert [hit.passage_id for hit in store.search("replacement_keyword")] == ["a-2"]
    assert store.get_paper("paper-a") == updated
    assert store.get_passage("a-1") is None
    store.close()


def test_data_survives_close_and_reopen(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    paper = _paper("paper-a", "Persistent Study", "persistent full text")
    passage = _passage("a-1", "paper-a", "Results", 5, 6, 12, 35, "durable_keyword remains")

    store = KnowledgeStore(database, read_only=False)
    store.add_paper(paper, [passage])
    store.close()

    reopened = KnowledgeStore(database, read_only=False)
    assert reopened.get_paper("paper-a") == paper
    assert reopened.get_passage("a-1") == passage
    assert [hit.passage_id for hit in reopened.search("durable_keyword")] == ["a-1"]
    reopened.close()


def test_paper_passages_and_fts_update_are_one_transaction(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    store = KnowledgeStore(database, read_only=False)
    paper_a = _paper("paper-a", "Alpha", "alpha")
    passage_a = _passage("shared-id", "paper-a", "Results", 1, 1, 0, 13, "stable_keyword")
    store.add_paper(paper_a, [passage_a])
    identity_before_failure = store.passage_identity()

    paper_b = _paper("paper-b", "Beta", "beta")
    conflicting = _passage("shared-id", "paper-b", "Results", 2, 2, 0, 15, "partial_keyword")
    with pytest.raises(sqlite3.IntegrityError):
        store.add_paper(paper_b, [conflicting])

    assert store.get_paper("paper-b") is None
    assert store.search("partial_keyword") == []
    assert [hit.passage_id for hit in store.search("stable_keyword")] == ["shared-id"]
    assert store.passage_identity() == identity_before_failure
    store.close()


def test_passage_revision_is_transactional_and_persists_across_restart(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    store = KnowledgeStore(database, read_only=False)
    initial_identity = store.passage_identity()
    assert initial_identity[0] == 0
    assert len(initial_identity[1]) == 32
    assert store.passage_revision() == initial_identity[0]

    paper = _paper("paper-a", "Alpha", "alpha")
    first = _passage("a-1", "paper-a", "Results", 1, 1, 0, 12, "first version")
    store.add_paper(paper, [first])
    first_identity = store.passage_identity()
    assert first_identity[0] == 1
    assert first_identity[1] != initial_identity[1]

    second = _passage("a-2", "paper-a", "Results", 2, 2, 0, 13, "second version")
    store.add_paper(paper, [second])
    second_identity = store.passage_identity()
    assert second_identity[0] == 2
    assert second_identity[1] != first_identity[1]
    assert store.delete_paper("missing-paper") is False
    assert store.passage_identity() == second_identity
    assert store.delete_paper("paper-a") is True
    deleted_identity = store.passage_identity()
    assert deleted_identity[0] == 3
    assert deleted_identity[1] != second_identity[1]
    store.close()

    reopened = KnowledgeStore(database, read_only=False)
    assert reopened.passage_identity() == deleted_identity
    assert reopened.passage_revision() == 3
    assert reopened.get_paper("paper-a") is None
    assert reopened.get_passage("a-2") is None
    reopened.close()


def test_old_knowledge_metadata_schema_migrates_generation_once(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    connection = sqlite3.connect(database)
    connection.execute(
        """
        CREATE TABLE knowledge_metadata (
            singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
            passage_revision INTEGER NOT NULL CHECK(passage_revision >= 0)
        )
        """
    )
    connection.execute(
        "INSERT INTO knowledge_metadata (singleton, passage_revision) VALUES (1, 7)"
    )
    connection.commit()
    connection.close()

    store = KnowledgeStore(database, read_only=False)
    identity = store.passage_identity()
    store.close()

    assert identity[0] == 7
    assert len(identity[1]) == 32
    assert int(identity[1], 16) >= 0
    reopened = KnowledgeStore(database, read_only=False)
    assert reopened.passage_identity() == identity
    reopened.close()

    connection = sqlite3.connect(database)
    columns = [
        row[1]
        for row in connection.execute(
            "PRAGMA table_info(knowledge_metadata)"
        ).fetchall()
    ]
    connection.close()
    assert columns == ["singleton", "passage_revision", "passage_generation_id"]


def test_read_only_store_queries_without_schema_or_metadata_writes(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    store = KnowledgeStore(database, read_only=False)
    paper = _paper("paper-read-only", "Read Only", "frozen full text")
    store.add_paper(paper, [])
    revision = store.passage_revision()
    store.close()
    before_bytes = database.read_bytes()
    before_mtime_ns = database.stat().st_mtime_ns

    read_only = KnowledgeStore(database, read_only=True)
    assert read_only.get_paper(paper.paper_id) == paper
    assert read_only.passage_revision() == revision
    with pytest.raises(PermissionError):
        read_only.add_paper(
            _paper("paper-write-rejected", "Rejected", "other full text"),
            [],
        )
    read_only.close()

    assert database.read_bytes() == before_bytes
    assert database.stat().st_mtime_ns == before_mtime_ns


def test_passage_snapshot_returns_identity_and_passages_from_one_snapshot(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    paper = _paper("paper-a", "Alpha", "alpha")
    passage = _passage("a-1", "paper-a", "Results", 1, 1, 0, 12, "first version")
    store.add_paper(paper, [passage])

    identity, passages = store.passage_snapshot()

    assert identity == store.passage_identity()
    assert passages == [passage]
    store.close()


def test_codex_confirmed_text_and_direct_source_evidence_persist(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    paper = _paper("paper-a", "Agent Planning", "original PDF bytes represented by hash")
    passage = _passage(
        "passage-a",
        paper.paper_id,
        "Methods",
        3,
        3,
        0,
        55,
        "Agents plan first and then call tools before observation.",
    )
    text_arguments = _text_evidence_arguments(paper, passage)

    store = KnowledgeStore(database, read_only=False)
    store.add_paper(paper, [passage])
    identity = store.passage_identity()
    text_evidence = store.add_evidence(**text_arguments)
    direct_evidence = store.add_evidence(
        evidence_id="evidence-table",
        paper_id=paper.paper_id,
        fulltext_sha256=paper.fulltext_sha256,
        evidence_kind="table",
        section="Results",
        page_start=7,
        page_end=8,
        locator="Table 2, rows 3-5",
        source_content="Method A: 71.2; Method B: 68.4",
        codex_note="Codex recorded the reported comparison; reopen the pages to inspect layout.",
    )

    assert passage.text[
        text_evidence.quote_start : text_evidence.quote_end
    ] == text_evidence.source_content
    assert text_evidence.source_content_sha256 == _sha256(
        text_evidence.source_content
    )
    assert text_evidence.codex_note != text_evidence.source_content
    assert text_evidence.fulltext_is_current is True
    assert text_evidence.passage_is_current is True
    assert (
        text_evidence.page_start,
        text_evidence.page_end,
        text_evidence.section,
        text_evidence.locator,
    ) == (3, 3, "Methods", "right column, second paragraph")
    assert direct_evidence.source_content_sha256 == _sha256(
        direct_evidence.source_content
    )
    assert direct_evidence.fulltext_is_current is True
    assert direct_evidence.passage_is_current is None
    assert direct_evidence.passage_id is None
    assert direct_evidence.passage_text_sha256 is None
    assert direct_evidence.quote_start is None
    assert direct_evidence.quote_end is None
    assert store.passage_identity() == identity
    assert [item.evidence_id for item in store.list_evidence(paper.paper_id)] == [
        "evidence-table",
        "evidence-text",
    ]

    assert store.add_evidence(**text_arguments) == text_evidence
    assert len(store.list_evidence(paper.paper_id)) == 2
    with pytest.raises(ValueError, match="different content"):
        store.add_evidence(
            **(text_arguments | {"codex_note": "A conflicting replacement note."})
        )
    assert store.get_evidence("evidence-text") == text_evidence
    store.close()

    reopened = KnowledgeStore(database, read_only=False)
    assert reopened.get_evidence("evidence-text") == text_evidence
    assert reopened.get_evidence("evidence-table") == direct_evidence
    reopened.close()

    connection = sqlite3.connect(database)
    columns = [
        row[1] for row in connection.execute("PRAGMA table_info(evidence)").fetchall()
    ]
    connection.close()
    assert columns == [
        "evidence_id",
        "paper_id",
        "fulltext_sha256",
        "evidence_kind",
        "section",
        "page_start",
        "page_end",
        "locator",
        "source_content",
        "source_content_sha256",
        "codex_note",
        "passage_id",
        "passage_text_sha256",
        "quote_start",
        "quote_end",
    ]


def test_evidence_validation_failures_leave_no_partial_rows(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    paper_a = _paper("paper-a", "Alpha", "alpha PDF")
    paper_b = _paper("paper-b", "Beta", "beta PDF")
    passage_a = _passage(
        "passage-a", "paper-a", "Methods", 3, 3, 0, 45,
        "Agents plan first and then call tools reliably.",
    )
    passage_b = _passage(
        "passage-b", "paper-b", "Methods", 4, 4, 0, 37,
        "A separate paper contains other text.",
    )
    store.add_paper(paper_a, [passage_a])
    store.add_paper(paper_b, [passage_b])
    revision = store.passage_revision()
    valid = _text_evidence_arguments(paper_a, passage_a)

    failures = [
        valid
        | {
            "evidence_id": "missing-paper",
            "paper_id": "missing",
            "fulltext_sha256": "unknown",
            "passage_id": None,
            "passage_text_sha256": None,
            "quote_start": None,
            "quote_end": None,
        },
        valid | {"evidence_id": "wrong-pdf", "fulltext_sha256": "wrong"},
        valid
        | {
            "evidence_id": "wrong-paper",
            "paper_id": paper_b.paper_id,
            "fulltext_sha256": paper_b.fulltext_sha256,
        },
        valid
        | {
            "evidence_id": "wrong-passage-hash",
            "passage_text_sha256": "wrong",
        },
        valid | {"evidence_id": "missing-passage", "passage_id": "missing"},
        valid | {"evidence_id": "bad-range", "quote_start": -1},
        valid
        | {
            "evidence_id": "bad-slice",
            "source_content": "a different source excerpt",
        },
    ]

    for arguments in failures:
        with pytest.raises(ValueError):
            store.add_evidence(**arguments)
        assert store.get_evidence(str(arguments["evidence_id"])) is None

    assert store.list_evidence(paper_a.paper_id) == []
    assert store.list_evidence(paper_b.paper_id) == []
    assert store.passage_revision() == revision
    store.close()


def test_evidence_reports_independent_fulltext_and_passage_freshness(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)

    paper_a = _paper("paper-a", "Alpha", "original alpha PDF")
    passage_a = _passage(
        "passage-a", "paper-a", "Methods", 3, 3, 0, 45,
        "Agents plan first and then call tools reliably.",
    )
    store.add_paper(paper_a, [passage_a])
    store.add_evidence(**_text_evidence_arguments(paper_a, passage_a))
    changed_pdf = _paper("paper-a", "Alpha revised", "different alpha PDF")
    store.add_paper(changed_pdf, [passage_a])

    pdf_stale = store.get_evidence("evidence-text")
    assert pdf_stale is not None
    assert pdf_stale.fulltext_sha256 == paper_a.fulltext_sha256
    assert pdf_stale.fulltext_is_current is False
    assert pdf_stale.passage_is_current is True

    paper_b = _paper("paper-b", "Beta", "stable beta PDF")
    old_passage = _passage(
        "passage-b", "paper-b", "Methods", 3, 3, 0, 45,
        "Agents plan first and then call tools reliably.",
    )
    store.add_paper(paper_b, [old_passage])
    arguments = _text_evidence_arguments(paper_b, old_passage) | {
        "evidence_id": "evidence-beta"
    }
    store.add_evidence(**arguments)
    changed_passage = _passage(
        "passage-b", "paper-b", "Methods", 3, 3, 0, 36,
        "The parser now extracts different text.",
    )
    store.add_paper(paper_b, [changed_passage])

    passage_stale = store.get_evidence("evidence-beta")
    assert passage_stale is not None
    assert passage_stale.fulltext_is_current is True
    assert passage_stale.passage_is_current is False
    assert passage_stale.source_content == arguments["source_content"]
    assert passage_stale.passage_text_sha256 == old_passage.text_sha256
    store.close()


def test_deleting_paper_cascades_to_evidence(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    store = KnowledgeStore(database, read_only=False)
    paper = _paper("paper-a", "Alpha", "alpha PDF")
    store.add_paper(paper, [])
    store.add_evidence(
        evidence_id="evidence-direct",
        paper_id=paper.paper_id,
        fulltext_sha256=paper.fulltext_sha256,
        evidence_kind="figure",
        section="Results",
        page_start=8,
        page_end=8,
        locator="Figure 4",
        source_content="The diagram connects planner output to tool execution.",
        codex_note="Codex recorded the visual mechanism and must reopen Figure 4 to review it.",
    )

    assert store.delete_paper(paper.paper_id) is True
    assert store.get_evidence("evidence-direct") is None
    store.close()

    connection = sqlite3.connect(database)
    count = connection.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
    connection.close()
    assert count == 0


def test_evidence_methods_have_no_retrieval_or_workflow_dependencies() -> None:
    source = "\n".join(
        (
            inspect.getsource(KnowledgeStore.add_evidence),
            inspect.getsource(KnowledgeStore.get_evidence),
            inspect.getsource(KnowledgeStore.list_evidence),
        )
    ).lower()
    for forbidden in (
        "passages_fts",
        "vector",
        "reranker",
        "candidate",
        "reviewer",
        "workflow",
    ):
        assert forbidden not in source


def test_knowledge_module_has_no_legacy_runtime_dependencies() -> None:
    import crl_v3.knowledge as knowledge

    source = inspect.getsource(knowledge).lower()
    for forbidden in ("campaign", "round", "gate", "receipt"):
        assert forbidden not in source
