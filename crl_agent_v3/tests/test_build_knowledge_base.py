from __future__ import annotations

import hashlib
import inspect
import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pymupdf
import pytest

import tools.build_knowledge_base as builder_module
from crl_v3.knowledge import KnowledgeStore
from tools.build_knowledge_base import build_corpus, import_evidence


MANIFEST_FIELDS = {
    "schema_version",
    "corpus_id",
    "corpus_cutoff",
    "scope_sha256",
    "calibration_query_sha256",
    "blind_query_sha256",
    "papers",
}
PAPER_FIELDS = {
    "paper_id",
    "canonical_id",
    "title",
    "authors",
    "year",
    "source",
    "venue",
    "publication_status",
    "version",
    "landing_page_url",
    "fulltext_url",
    "pdf_path",
    "sha256",
    "mechanism_clusters",
    "admission_role",
}
EVIDENCE_FIELDS = {
    "evidence_id",
    "paper_id",
    "fulltext_sha256",
    "evidence_kind",
    "section",
    "page_start",
    "page_end",
    "locator",
    "source_content",
    "codex_note",
    "passage_id",
    "passage_text_sha256",
    "quote_start",
    "quote_end",
}


def _offline_encoder(texts: list[str]) -> np.ndarray:
    rows = []
    for text in texts:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        rows.append([float(digest[0] + 1), float(digest[1] + 1), 1.0])
    return np.asarray(rows, dtype=np.float32)


def _make_pdf(path: Path) -> None:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "1 Introduction", fontsize=16)
    page.insert_text((72, 105), "A planner records reliable evidence before acting.")
    page = document.new_page()
    page.insert_text((72, 72), "2 Method", fontsize=16)
    page.insert_text((72, 105), "Selective verification changes the executed branch.")
    document.save(path)
    document.close()


def _paper_entry(pdf_path: Path, *, paper_id: str = "paper-one") -> dict[str, object]:
    return {
        "paper_id": paper_id,
        "canonical_id": "doi:10.0000/pilot.one",
        "title": "Pilot Mechanism Study",
        "authors": ["Ada Researcher", "Bo Scientist"],
        "year": 2025,
        "source": "official proceedings",
        "venue": "PilotConf 2025",
        "publication_status": "published",
        "version": "proceedings",
        "landing_page_url": "https://example.org/pilot-one",
        "fulltext_url": "https://example.org/pilot-one.pdf",
        "pdf_path": "papers/paper-one.pdf",
        "sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
        "mechanism_clusters": ["planning", "evaluation"],
        "admission_role": ["operator", "failure"],
    }


def _write_manifest(
    path: Path, paper: dict[str, object] | None, **changes: object
) -> None:
    manifest: dict[str, object] = {
        "schema_version": 1,
        "corpus_id": "pilot",
        "corpus_cutoff": "2026-07-19",
        "scope_sha256": "a" * 64,
        "calibration_query_sha256": "b" * 64,
        "blind_query_sha256": "c" * 64,
        "papers": [] if paper is None else [paper],
    }
    manifest.update(changes)
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
        newline="\n",
    )


def _build_fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path, dict[str, object]]:
    knowledge_root = tmp_path / "knowledge"
    papers = knowledge_root / "papers"
    papers.mkdir(parents=True)
    pdf_path = papers / "paper-one.pdf"
    _make_pdf(pdf_path)
    paper = _paper_entry(pdf_path)
    manifest_path = knowledge_root / "pilot" / "manifest.json"
    manifest_path.parent.mkdir()
    _write_manifest(manifest_path, paper)
    database_path = knowledge_root / "knowledge.sqlite"
    index_path = knowledge_root / "passages.npz"
    return manifest_path, knowledge_root, database_path, index_path, paper


def _build(tmp_path: Path) -> tuple[dict[str, object], Path, Path, dict[str, object]]:
    manifest, root, database, index, paper = _build_fixture(tmp_path)
    result = build_corpus(
        manifest,
        root,
        database,
        index,
        encoder=_offline_encoder,
        encoder_id="tests:pilot-builder-v1",
    )
    return result, database, index, paper


def test_build_corpus_creates_database_and_vector_from_frozen_manifest(tmp_path) -> None:
    result, database, index, _ = _build(tmp_path)

    assert result["papers"] == 1
    assert result["passages"] >= 1
    assert result["database_path"] == str(database.resolve())
    assert result["index_path"] == str(index.resolve())
    assert result["encoder_id"] == "tests:pilot-builder-v1"
    assert set(result) == {
        "database_path",
        "index_path",
        "papers",
        "passages",
        "passage_revision",
        "passage_generation_id",
        "vector_model_name",
        "vector_model_revision",
        "encoder_id",
    }
    assert database.is_file() and index.is_file()
    with sqlite3.connect(database) as connection:
        assert connection.execute("PRAGMA quick_check").fetchone()[0] == "ok"
    with np.load(index, allow_pickle=False) as data:
        assert len(data["passage_ids"]) == result["passages"]


def test_build_corpus_uses_parent_inheriting_sibling_directory(
    tmp_path, monkeypatch
) -> None:
    manifest, root, database, index, _ = _build_fixture(tmp_path)
    real_store = builder_module.KnowledgeStore
    observed_database_paths: list[Path] = []

    def recording_store(path: str | Path, *, read_only: bool = True) -> KnowledgeStore:
        observed_database_paths.append(Path(path).resolve())
        return real_store(path, read_only=read_only)

    monkeypatch.setattr(builder_module, "KnowledgeStore", recording_store)

    build_corpus(
        manifest,
        root,
        database,
        index,
        encoder=_offline_encoder,
        encoder_id="tests:pilot-builder-v1",
    )

    assert len(observed_database_paths) == 1
    temporary_root = observed_database_paths[0].parent
    assert temporary_root.parent == database.parent.resolve()
    assert temporary_root.name.startswith(".crl-build-")
    assert temporary_root.name.endswith(".tmp")
    assert not temporary_root.exists()
    assert "TemporaryDirectory" not in inspect.getsource(builder_module.build_corpus)


@pytest.mark.parametrize(
    ("mutation", "match"),
    [
        (lambda paper, root: paper.update(sha256="0" * 64), "hash"),
        (
            lambda paper, root: paper.update(pdf_path=str((root / "papers" / "paper-one.pdf").resolve())),
            "relative",
        ),
        (lambda paper, root: paper.update(pdf_path="../outside.pdf"), "traversal"),
    ],
)
def test_build_corpus_rejects_bad_hash_and_unsafe_paths_without_outputs(
    tmp_path, mutation, match
) -> None:
    manifest, root, database, index, paper = _build_fixture(tmp_path)
    mutation(paper, root)
    _write_manifest(manifest, paper)

    with pytest.raises(ValueError, match=match):
        build_corpus(
            manifest,
            root,
            database,
            index,
            encoder=_offline_encoder,
            encoder_id="tests:pilot-builder-v1",
        )

    assert not database.exists()
    assert not index.exists()


def test_build_corpus_rejects_duplicate_paper_ids_and_empty_corpus(tmp_path) -> None:
    manifest, root, database, index, paper = _build_fixture(tmp_path)
    _write_manifest(manifest, paper, papers=[paper, dict(paper)])
    with pytest.raises(ValueError, match="duplicate paper_id"):
        build_corpus(
            manifest,
            root,
            database,
            index,
            encoder=_offline_encoder,
            encoder_id="tests:pilot-builder-v1",
        )
    assert not database.exists() and not index.exists()

    _write_manifest(manifest, None)
    with pytest.raises(ValueError, match="empty"):
        build_corpus(
            manifest,
            root,
            database,
            index,
            encoder=_offline_encoder,
            encoder_id="tests:pilot-builder-v1",
        )
    assert not database.exists() and not index.exists()


@pytest.mark.parametrize("existing_target", ["database", "index"])
def test_build_corpus_preserves_existing_target_and_creates_no_peer(
    tmp_path, existing_target
) -> None:
    manifest, root, database, index, _ = _build_fixture(tmp_path)
    target = database if existing_target == "database" else index
    peer = index if existing_target == "database" else database
    target.write_bytes(b"existing-target")

    with pytest.raises(FileExistsError):
        build_corpus(
            manifest,
            root,
            database,
            index,
            encoder=_offline_encoder,
            encoder_id="tests:pilot-builder-v1",
        )

    assert target.read_bytes() == b"existing-target"
    assert not peer.exists()


def test_build_corpus_removes_first_publish_if_second_publish_fails(
    tmp_path, monkeypatch
) -> None:
    manifest, root, database, index, _ = _build_fixture(tmp_path)
    unrelated_sibling = root / ".crl-build-unrelated.tmp"
    unrelated_sibling.mkdir()
    (unrelated_sibling / "keep.txt").write_text(
        "unrelated sibling must survive", encoding="utf-8", newline="\n"
    )
    real_replace = builder_module._replace
    publish_calls = 0

    def fail_second_publish(source: Path, target: Path) -> None:
        nonlocal publish_calls
        publish_calls += 1
        if publish_calls == 2:
            raise OSError("injected second publish failure")
        real_replace(source, target)

    monkeypatch.setattr(builder_module, "_replace", fail_second_publish)

    with pytest.raises(OSError, match="second publish"):
        build_corpus(
            manifest,
            root,
            database,
            index,
            encoder=_offline_encoder,
            encoder_id="tests:pilot-builder-v1",
        )

    assert not database.exists()
    assert not index.exists()
    assert (unrelated_sibling / "keep.txt").read_text(encoding="utf-8") == (
        "unrelated sibling must survive"
    )
    assert list(root.glob(".crl-build-*.tmp")) == [unrelated_sibling]


def test_build_corpus_rejects_unknown_manifest_and_paper_fields(tmp_path) -> None:
    manifest, root, database, index, paper = _build_fixture(tmp_path)
    _write_manifest(manifest, paper, unexpected=True)
    with pytest.raises(ValueError, match="manifest fields"):
        build_corpus(
            manifest,
            root,
            database,
            index,
            encoder=_offline_encoder,
            encoder_id="tests:pilot-builder-v1",
        )

    _write_manifest(manifest, paper | {"unexpected": True})
    with pytest.raises(ValueError, match="paper fields"):
        build_corpus(
            manifest,
            root,
            database,
            index,
            encoder=_offline_encoder,
            encoder_id="tests:pilot-builder-v1",
        )

    assert not database.exists() and not index.exists()


def _evidence_from_built_database(
    database: Path, paper: dict[str, object]
) -> dict[str, object]:
    store = KnowledgeStore(database, read_only=False)
    try:
        passage = store.list_passages()[0]
    finally:
        store.close()
    source_content = passage.text[: min(24, len(passage.text))]
    return {
        "evidence_id": "evidence-one",
        "paper_id": paper["paper_id"],
        "fulltext_sha256": paper["sha256"],
        "evidence_kind": "text",
        "section": passage.section,
        "page_start": passage.page_start,
        "page_end": passage.page_end,
        "locator": "first extracted passage",
        "source_content": source_content,
        "codex_note": "Pilot test preserves an exact source span.",
        "passage_id": passage.passage_id,
        "passage_text_sha256": passage.text_sha256,
        "quote_start": 0,
        "quote_end": len(source_content),
    }


def _write_evidence(path: Path, evidence: dict[str, object], **changes: object) -> None:
    payload: dict[str, object] = {"schema_version": 1, "evidence": [evidence]}
    payload.update(changes)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
        newline="\n",
    )


def test_import_evidence_is_idempotent_and_round_trips_every_input_field(tmp_path) -> None:
    _, database, _, paper = _build(tmp_path)
    evidence = _evidence_from_built_database(database, paper)
    evidence_path = tmp_path / "evidence.json"
    _write_evidence(evidence_path, evidence)

    expected = {
        "database_path": str(database.resolve()),
        "evidence_imported": 1,
    }
    assert import_evidence(evidence_path, database) == expected
    assert import_evidence(evidence_path, database) == expected

    store = KnowledgeStore(database, read_only=False)
    try:
        stored = store.get_evidence("evidence-one")
    finally:
        store.close()
    assert stored is not None
    serialized = asdict(stored)
    assert {field: serialized[field] for field in EVIDENCE_FIELDS} == evidence


@pytest.mark.parametrize(
    ("change", "match"),
    [
        ({"paper_id": "missing-paper"}, "paper does not exist"),
        ({"fulltext_sha256": "0" * 64}, "full-text hash"),
        ({"passage_id": "missing-passage"}, "passage does not exist"),
        ({"passage_text_sha256": "0" * 64}, "passage hash"),
    ],
)
def test_import_evidence_rejects_missing_or_stale_source_bindings(
    tmp_path, change, match
) -> None:
    _, database, _, paper = _build(tmp_path)
    evidence = _evidence_from_built_database(database, paper) | change
    evidence_path = tmp_path / "evidence.json"
    _write_evidence(evidence_path, evidence)

    with pytest.raises(ValueError, match=match):
        import_evidence(evidence_path, database)


def test_import_evidence_rejects_same_id_with_different_content(tmp_path) -> None:
    _, database, _, paper = _build(tmp_path)
    evidence = _evidence_from_built_database(database, paper)
    evidence_path = tmp_path / "evidence.json"
    _write_evidence(evidence_path, evidence)
    import_evidence(evidence_path, database)
    _write_evidence(evidence_path, evidence | {"codex_note": "changed"})

    with pytest.raises(ValueError, match="different content"):
        import_evidence(evidence_path, database)


def test_import_evidence_rejects_unknown_fields(tmp_path) -> None:
    _, database, _, paper = _build(tmp_path)
    evidence = _evidence_from_built_database(database, paper)
    evidence_path = tmp_path / "evidence.json"
    _write_evidence(evidence_path, evidence, unexpected=True)
    with pytest.raises(ValueError, match="evidence document fields"):
        import_evidence(evidence_path, database)

    _write_evidence(evidence_path, evidence | {"unexpected": True})
    with pytest.raises(ValueError, match="evidence fields"):
        import_evidence(evidence_path, database)


def test_cli_exposes_only_build_and_import_subcommands() -> None:
    parser = builder_module.build_parser()
    build = parser.parse_args(
        [
            "build-corpus",
            "--manifest",
            "manifest.json",
            "--knowledge-root",
            "knowledge",
            "--database",
            "knowledge.sqlite",
            "--index",
            "passages.npz",
        ]
    )
    assert build.action == "build-corpus"
    imported = parser.parse_args(
        [
            "import-evidence",
            "--evidence",
            "evidence.json",
            "--database",
            "knowledge.sqlite",
        ]
    )
    assert imported.action == "import-evidence"
    with pytest.raises(SystemExit):
        parser.parse_args(["search"])
