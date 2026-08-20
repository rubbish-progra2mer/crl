from __future__ import annotations

import hashlib
import json
from pathlib import Path

from crl_v3.cards import rebuild_card_index
from crl_v3.knowledge import KnowledgeStore, Paper, Passage
from crl_v3.knowledge_audit import audit_knowledge_base
from conftest import make_file_symlink


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _passage(passage_id: str, paper_id: str, text: str, page: int) -> Passage:
    return Passage(
        passage_id=passage_id,
        paper_id=paper_id,
        section="Methods",
        page_start=page,
        page_end=page,
        char_start=0,
        char_end=len(text),
        text=text,
        text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
    )


def _card_body(evidence_id: str) -> str:
    headings = (
        "Intervention target",
        "Before and after computation",
        "Inputs outputs information and timing",
        "Mechanism hypothesis",
        "Predicted observable signature",
        "Preconditions and transfer risks",
        "Source lineage",
        "Evidence ledger",
        "Retrieval vocabulary",
    )
    sections = []
    for index, heading in enumerate(headings):
        content = (
            f"[AUTHOR_FACT] External finding. [[evidence:{evidence_id}]]"
            if index == 0
            else "[CODEX_SYNTHESIS] Fixture content."
        )
        sections.append(f"## {heading}\n\n{content}")
    return "# Audit operator\n\n" + "\n\n".join(sections) + "\n"


def make_audit_fixture(tmp_path: Path) -> tuple[Path, Path, str]:
    project = tmp_path / "product"
    knowledge = project / "knowledge_base"
    papers = knowledge / "papers"
    papers.mkdir(parents=True)
    pdf = papers / "paper-a.pdf"
    pdf.write_bytes(b"external-pdf")
    pdf_sha = _sha256_bytes(pdf.read_bytes())
    store = KnowledgeStore(knowledge / "knowledge.sqlite", read_only=False)
    paper = Paper(
        paper_id="paper-a",
        title="Paper A",
        year=2026,
        source="test",
        venue="Test",
        publication_status="preprint",
        fulltext_path="papers/paper-a.pdf",
        fulltext_sha256=pdf_sha,
    )
    normal = _passage("passage-normal", "paper-a", "prefix external finding suffix", 1)
    duplicate_a = _passage("passage-duplicate-a", "paper-a", "duplicate exact text", 2)
    duplicate_b = _passage("passage-duplicate-b", "paper-a", "duplicate exact text", 3)
    short = _passage("passage-short", "paper-a", "tiny", 4)
    long_text = "x" * 20_001
    extreme = _passage("passage-extreme", "paper-a", long_text, 5)
    store.add_paper(paper, [normal, duplicate_a, duplicate_b, short, extreme])
    quote = "external finding"
    start = normal.text.index(quote)
    store.add_evidence(
        evidence_id="evidence-a",
        paper_id=paper.paper_id,
        fulltext_sha256=paper.fulltext_sha256,
        evidence_kind="text",
        section=normal.section,
        page_start=1,
        page_end=1,
        locator="page 1",
        source_content=quote,
        codex_note="Fixture.",
        passage_id=normal.passage_id,
        passage_text_sha256=normal.text_sha256,
        quote_start=start,
        quote_end=start + len(quote),
    )
    card = knowledge / "cards" / "operator" / "operator-audit.md"
    card.parent.mkdir(parents=True)
    metadata = {
        "schema_version": 1,
        "card_id": "operator-audit",
        "card_kind": "operator",
        "paper_id": "paper-a",
        "evidence_ids": ["evidence-a"],
        "source_refs": [{"path": "papers/paper-a.pdf", "sha256": pdf_sha}],
    }
    card.write_text(
        "<!-- CRL_CARD_META " + json.dumps(metadata, sort_keys=True) + " -->\n" + _card_body("evidence-a"),
        encoding="utf-8",
        newline="\n",
    )
    rebuilt = rebuild_card_index(
        knowledge / "cards",
        knowledge / "cards_fts.sqlite",
        store=store,
        project_root=knowledge,
    )
    store.close()
    scope = knowledge / "CORPUS_SCOPE.md"
    scope.write_text("# Scope\n", encoding="utf-8", newline="\n")
    lock = knowledge / "evaluation" / "PRODUCTION_RETRIEVAL_LOCK.json"
    lock.parent.mkdir()
    lock.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "accepted_attempt": "knowledge_base/evaluation/attempt",
                "source_snapshot": {
                    "scope": {
                        "path": "knowledge_base/CORPUS_SCOPE.md",
                        "sha256": "0" * 64,
                    },
                    "card_source_signature": rebuilt.source_signature,
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return project, knowledge, long_text


def test_audit_reports_lock_drift_duplicate_extreme_short_and_missing_vector_read_only(
    tmp_path: Path,
) -> None:
    project, knowledge, long_text = make_audit_fixture(tmp_path)
    before = {
        path.relative_to(knowledge).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
        for path in knowledge.rglob("*")
        if path.is_file()
    }

    report = audit_knowledge_base(knowledge, project_root=project)

    codes = [finding["code"] for finding in report["findings"]]
    assert report["counts"] == {"papers": 1, "passages": 5, "evidence": 1, "cards": 1}
    assert report["passage_anomaly_counts"] == {
        "blank": 0,
        "very_short": 3,
        "extreme_long": 1,
        "duplicate_groups_within_paper": 1,
        "duplicate_passages_within_paper": 2,
        "coordinate_length_mismatch": 0,
        "text_hash_mismatch": 0,
    }
    assert "SQLITE_INTEGRITY_CHECK" in codes
    assert "SQLITE_FOREIGN_KEY_CHECK" in codes
    assert "PASSAGE_DUPLICATE_WITHIN_PAPER" in codes
    assert "PASSAGE_EXTREME_LONG" in codes
    assert "PASSAGE_VERY_SHORT" in codes
    assert "VECTOR_INDEX_DIAGNOSTIC" in codes
    assert "RETRIEVAL_LOCK_SOURCE_HASH_MISMATCH" in codes
    assert not ({"ready", "pass", "fail", "status"} & set(report))
    extreme = next(item for item in report["findings"] if item["code"] == "PASSAGE_EXTREME_LONG")
    assert extreme["details"] == {
        "paper_id": "paper-a",
        "passage_id": "passage-extreme",
        "length": 20_001,
        "page_start": 5,
        "page_end": 5,
    }
    assert long_text not in json.dumps(report, ensure_ascii=False)
    after = {
        path.relative_to(knowledge).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
        for path in knowledge.rglob("*")
        if path.is_file()
    }
    assert after == before
    assert not list(knowledge.rglob("*-journal"))
    assert not list(knowledge.rglob("*-wal"))
    assert not list(knowledge.rglob("*-shm"))


def test_audit_reports_damaged_lock_without_writing(tmp_path: Path) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)
    lock = knowledge / "evaluation" / "PRODUCTION_RETRIEVAL_LOCK.json"
    lock.write_bytes(b"{broken")
    before = lock.read_bytes()

    report = audit_knowledge_base(knowledge, project_root=project)

    assert any(item["code"] == "RETRIEVAL_LOCK_INVALID" for item in report["findings"])
    assert lock.read_bytes() == before


def test_audit_rejects_default_lock_symlink_before_reading_target(
    tmp_path: Path,
) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)
    lock = knowledge / "evaluation" / "PRODUCTION_RETRIEVAL_LOCK.json"
    lock.unlink()
    target = project / "maintenance" / "redirected-lock.json"
    target.parent.mkdir()
    target.write_bytes(b"{not-json")
    before = target.read_bytes()
    make_file_symlink(lock, target)

    report = audit_knowledge_base(knowledge, project_root=project)

    codes = {item["code"] for item in report["findings"]}
    assert "RETRIEVAL_LOCK_UNSAFE" in codes
    assert "RETRIEVAL_LOCK_INVALID" not in codes
    assert target.read_bytes() == before
