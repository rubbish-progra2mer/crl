from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from crl_v3.knowledge import KnowledgeStore, Paper


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "tools" / "manage_cards.py"


def _setup_cli_workspace(tmp_path):
    project_root = tmp_path / "knowledge_base"
    source = project_root / "papers" / "paper-a.pdf"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"paper-a-cli-pdf")
    source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    knowledge_db = project_root / "knowledge.sqlite"
    store = KnowledgeStore(knowledge_db, read_only=False)
    store.add_paper(
        Paper(
            paper_id="paper-a",
            title="Paper A",
            year=2025,
            source="test",
            venue="Test Venue",
            publication_status="preprint",
            fulltext_path="papers/paper-a.pdf",
            fulltext_sha256=source_sha,
        ),
        [],
    )
    store.add_evidence(
        evidence_id="evidence-a",
        paper_id="paper-a",
        fulltext_sha256=source_sha,
        evidence_kind="figure",
        section="Results",
        page_start=3,
        page_end=3,
        locator="figure 1",
        source_content="correlated error",
        codex_note="CLI fixture evidence.",
    )
    store.close()
    cards_root = project_root / "cards"
    card_path = cards_root / "failure" / "failure-correlated-error.md"
    card_path.parent.mkdir(parents=True)
    metadata = {
        "schema_version": 1,
        "card_id": "failure-correlated-error",
        "card_kind": "failure",
        "paper_id": "paper-a",
        "evidence_ids": ["evidence-a"],
        "source_refs": [
            {"path": "papers/paper-a.pdf", "sha256": source_sha}
        ],
    }
    headings = (
        "Observed failure",
        "Conditions and scope",
        "Failed intervention",
        "Evidence and alternative explanations",
        "Warning for future candidates",
        "Possible repair boundary",
        "Evidence ledger",
        "Retrieval vocabulary",
    )
    sections = []
    for index, heading in enumerate(headings):
        content = (
            "[AUTHOR_FACT] Correlated error is observed. [[evidence:evidence-a]]"
            if index == 0
            else "[CODEX_SYNTHESIS] Correlated error retrieval fixture."
        )
        sections.append(f"## {heading}\n\n{content}")
    text = (
        "<!-- CRL_CARD_META "
        + json.dumps(metadata, sort_keys=True)
        + " -->\n# Correlated error\n\n"
        + "\n\n".join(sections)
        + "\n"
    )
    card_path.write_text(text, encoding="utf-8", newline="\n")
    return project_root, knowledge_db, cards_root, card_path


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )


def test_validate_rebuild_and_search_emit_mechanical_json(tmp_path) -> None:
    project_root, knowledge_db, cards_root, _ = _setup_cli_workspace(tmp_path)
    index_path = project_root / "cards_fts.sqlite"

    validated = _run(
        "validate",
        "--cards-root",
        str(cards_root),
        "--knowledge-db",
        str(knowledge_db),
        "--project-root",
        str(project_root),
    )
    assert validated.returncode == 0, validated.stderr
    validate_json = json.loads(validated.stdout)
    assert validate_json == {
        "action": "validate",
        "card_count": 1,
        "kind_counts": {"failure": 1, "operator": 0, "paper": 0},
    }

    rebuilt = _run(
        "rebuild-index",
        "--cards-root",
        str(cards_root),
        "--knowledge-db",
        str(knowledge_db),
        "--project-root",
        str(project_root),
        "--index",
        str(index_path),
    )
    assert rebuilt.returncode == 0, rebuilt.stderr
    rebuild_json = json.loads(rebuilt.stdout)
    assert set(rebuild_json) == {
        "action",
        "index_path",
        "card_count",
        "source_signature",
    }
    assert rebuild_json["action"] == "rebuild-index"
    assert rebuild_json["index_path"] == str(index_path)
    assert rebuild_json["card_count"] == 1
    assert len(rebuild_json["source_signature"]) == 64

    searched = _run(
        "search",
        "--cards-root",
        str(cards_root),
        "--index",
        str(index_path),
        "--query",
        "correlated error",
        "--kind",
        "failure",
        "--limit",
        "5",
    )
    assert searched.returncode == 0, searched.stderr
    search_json = json.loads(searched.stdout)
    assert set(search_json) == {
        "action",
        "original_query",
        "normalized_query",
        "english_keyword_hint",
        "kinds",
        "hits",
    }
    assert search_json["action"] == "search"
    assert search_json["original_query"] == "correlated error"
    assert search_json["normalized_query"] == '"correlated" OR "error"'
    assert search_json["kinds"] == ["failure"]
    assert [hit["card_kind"] for hit in search_json["hits"]] == ["failure"]
    assert not ({"score", "decision", "candidate", "research_pass"} & set(search_json))


def test_validate_keeps_knowledge_database_bytes_and_mtime_unchanged(
    tmp_path,
) -> None:
    project_root, knowledge_db, cards_root, _ = _setup_cli_workspace(tmp_path)
    before_bytes = knowledge_db.read_bytes()
    before_mtime_ns = knowledge_db.stat().st_mtime_ns

    validated = _run(
        "validate",
        "--cards-root",
        str(cards_root),
        "--knowledge-db",
        str(knowledge_db),
        "--project-root",
        str(project_root),
    )

    assert validated.returncode == 0, validated.stderr
    assert knowledge_db.read_bytes() == before_bytes
    assert knowledge_db.stat().st_mtime_ns == before_mtime_ns
    assert not (knowledge_db.parent / f"{knowledge_db.name}-journal").exists()
    assert not (knowledge_db.parent / f"{knowledge_db.name}-wal").exists()
    assert not (knowledge_db.parent / f"{knowledge_db.name}-shm").exists()


def test_cli_missing_arguments_use_argparse_exit_two() -> None:
    result = _run("validate")

    assert result.returncode == 2
    assert result.stdout == ""
    assert "required" in result.stderr


def test_cli_rejects_invalid_card_with_specific_stderr(tmp_path) -> None:
    project_root, knowledge_db, cards_root, card_path = _setup_cli_workspace(tmp_path)
    card_path.write_bytes(b"\xef\xbb\xbf" + card_path.read_bytes())

    result = _run(
        "validate",
        "--cards-root",
        str(cards_root),
        "--knowledge-db",
        str(knowledge_db),
        "--project-root",
        str(project_root),
    )

    assert result.returncode != 0
    assert result.stdout == ""
    assert "UTF-8 BOM" in result.stderr


def test_cli_missing_knowledge_db_does_not_create_it(tmp_path) -> None:
    project_root = tmp_path / "knowledge_base"
    cards_root = project_root / "cards"
    cards_root.mkdir(parents=True)
    missing_db = project_root / "missing.sqlite"

    result = _run(
        "validate",
        "--cards-root",
        str(cards_root),
        "--knowledge-db",
        str(missing_db),
        "--project-root",
        str(project_root),
    )

    assert result.returncode != 0
    assert "knowledge database" in result.stderr
    assert not missing_db.exists()


def test_cli_help_exposes_only_three_subcommands() -> None:
    result = _run("--help")

    assert result.returncode == 0
    assert "validate" in result.stdout
    assert "rebuild-index" in result.stdout
    assert "search" in result.stdout
    assert "all-prioritized" not in result.stdout


def test_validate_missing_ok_option_is_removed(tmp_path) -> None:
    absent_root = tmp_path / "knowledge_base" / "internal"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "validate",
            "--cards-root",
            str(absent_root / "cards"),
            "--knowledge-db",
            str(absent_root / "knowledge_internal.sqlite"),
            "--project-root",
            str(tmp_path / "knowledge_base"),
            "--missing-ok",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 2
    assert "unrecognized arguments" in completed.stderr


def test_validate_without_missing_ok_still_fails_on_absent_db(tmp_path) -> None:
    absent_root = tmp_path / "knowledge_base" / "internal"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "validate",
            "--cards-root",
            str(absent_root / "cards"),
            "--knowledge-db",
            str(absent_root / "knowledge_internal.sqlite"),
            "--project-root",
            str(tmp_path / "knowledge_base"),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 1
