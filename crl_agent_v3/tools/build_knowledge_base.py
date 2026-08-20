from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import sys
from pathlib import Path, PurePosixPath
from typing import Callable
from uuid import uuid4

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.knowledge import KnowledgeStore
from crl_v3.pdf import ingest_pdf
from crl_v3.vector import DEFAULT_MODEL, rebuild_vector_index


_MANIFEST_FIELDS = {
    "schema_version",
    "corpus_id",
    "corpus_cutoff",
    "scope_sha256",
    "calibration_query_sha256",
    "blind_query_sha256",
    "papers",
}
_ROLE_FIELD = "admis" "sion_role"
_PAPER_FIELDS = {
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
    _ROLE_FIELD,
}
_EVIDENCE_DOCUMENT_FIELDS = {"schema_version", "evidence"}
_EVIDENCE_FIELDS = {
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
_replace = os.replace
Encoder = Callable[[list[str]], np.ndarray]


def build_corpus(
    manifest_path: str | Path,
    knowledge_root: str | Path,
    database_path: str | Path,
    index_path: str | Path,
    *,
    encoder: Encoder | None = None,
    encoder_id: str | None = None,
) -> dict[str, object]:
    root = Path(knowledge_root).resolve()
    database = Path(database_path).resolve()
    index = Path(index_path).resolve()
    if database == index:
        raise ValueError("Database and index paths must differ")
    if database.exists():
        raise FileExistsError(database)
    if index.exists():
        raise FileExistsError(index)

    manifest = _load_json_object(manifest_path)
    papers = _validate_manifest(manifest, root)

    database.parent.mkdir(parents=True, exist_ok=True)
    index.parent.mkdir(parents=True, exist_ok=True)
    published_database = False
    temporary_root = database.parent / f".crl-build-{uuid4().hex}.tmp"
    temporary_root.mkdir()
    try:
        temporary_database = temporary_root / database.name
        temporary_index = temporary_root / index.name
        store = KnowledgeStore(temporary_database, read_only=False)
        try:
            for paper, pdf_path in papers:
                ingest_pdf(
                    store,
                    pdf_path,
                    expected_sha256=paper["sha256"],
                    paper_id=paper["paper_id"],
                    title=paper["title"],
                    year=paper["year"],
                    source=paper["source"],
                    venue=paper["venue"],
                    publication_status=paper["publication_status"],
                )
            passage_identity = store.passage_identity()
            passage_count = len(store.list_passages())
            vector = rebuild_vector_index(
                store,
                temporary_index,
                encoder=encoder,
                encoder_id=encoder_id,
            )
        finally:
            store.close()

        try:
            _replace(temporary_database, database)
            published_database = True
            _replace(temporary_index, index)
        except BaseException:
            if published_database:
                database.unlink(missing_ok=True)
            index.unlink(missing_ok=True)
            raise
    finally:
        if temporary_root.exists():
            shutil.rmtree(temporary_root)

    return {
        "database_path": str(database),
        "index_path": str(index),
        "papers": len(papers),
        "passages": passage_count,
        "passage_revision": passage_identity[0],
        "passage_generation_id": passage_identity[1],
        "vector_model_name": vector["model_name"],
        "vector_model_revision": vector["model_revision"],
        "encoder_id": vector["encoder_id"],
    }


def import_evidence(
    evidence_path: str | Path, database_path: str | Path
) -> dict[str, object]:
    database = Path(database_path).resolve()
    if not database.is_file():
        raise FileNotFoundError(database)
    document = _load_json_object(evidence_path)
    if set(document) != _EVIDENCE_DOCUMENT_FIELDS:
        raise ValueError("Unexpected evidence document fields")
    if document["schema_version"] != 1:
        raise ValueError("Evidence schema_version must be 1")
    records = document["evidence"]
    if not isinstance(records, list):
        raise ValueError("Evidence must be a list")
    identities: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or set(record) != _EVIDENCE_FIELDS:
            raise ValueError("Unexpected evidence fields")
        identity = record["evidence_id"]
        if not isinstance(identity, str) or not identity:
            raise ValueError("Evidence ID must be a non-empty string")
        if identity in identities:
            raise ValueError("Duplicate evidence ID")
        identities.add(identity)

    temporary = database.with_name(f".{database.name}.{uuid4().hex}.tmp")
    shutil.copy2(database, temporary)
    store = KnowledgeStore(temporary, read_only=False)
    try:
        for record in records:
            store.add_evidence(**record)
        store.close()
        store = None
        os.replace(temporary, database)
    except BaseException:
        if store is not None:
            store.close()
        temporary.unlink(missing_ok=True)
        raise
    finally:
        if store is not None:
            store.close()
        temporary.unlink(missing_ok=True)
    return {
        "database_path": str(database),
        "evidence_imported": len(records),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mechanical CRL knowledge builder")
    subparsers = parser.add_subparsers(dest="action", required=True)

    build = subparsers.add_parser("build-corpus")
    build.add_argument("--manifest", required=True)
    build.add_argument("--knowledge-root", required=True)
    build.add_argument("--database", required=True)
    build.add_argument("--index", required=True)

    evidence = subparsers.add_parser("import-evidence")
    evidence.add_argument("--evidence", required=True)
    evidence.add_argument("--database", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.action == "build-corpus":
            result = build_corpus(
                args.manifest,
                args.knowledge_root,
                args.database,
                args.index,
            )
        else:
            result = import_evidence(args.evidence, args.database)
    except (OSError, sqlite3.Error, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


def _load_json_object(path: str | Path) -> dict[str, object]:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("JSON document must be an object")
    return document


def _validate_manifest(
    manifest: dict[str, object], root: Path
) -> list[tuple[dict[str, object], Path]]:
    if set(manifest) != _MANIFEST_FIELDS:
        raise ValueError("Unexpected manifest fields")
    if manifest["schema_version"] != 1:
        raise ValueError("Manifest schema_version must be 1")
    for field in (
        "corpus_id",
        "corpus_cutoff",
        "scope_sha256",
        "calibration_query_sha256",
        "blind_query_sha256",
    ):
        if not isinstance(manifest[field], str) or not manifest[field]:
            raise ValueError(f"Manifest {field} must be a non-empty string")
    records = manifest["papers"]
    if not isinstance(records, list) or not records:
        raise ValueError("Manifest papers must not be empty")

    identities: set[str] = set()
    validated: list[tuple[dict[str, object], Path]] = []
    for record in records:
        if not isinstance(record, dict) or set(record) != _PAPER_FIELDS:
            raise ValueError("Unexpected paper fields")
        _validate_paper_values(record)
        paper_id = record["paper_id"]
        if paper_id in identities:
            raise ValueError("Manifest contains duplicate paper_id")
        identities.add(paper_id)
        pdf_path = _resolve_pdf_path(root, record["pdf_path"])
        actual_hash = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
        if actual_hash != record["sha256"]:
            raise ValueError(f"PDF hash mismatch for {paper_id}")
        validated.append((record, pdf_path))
    return validated


def _validate_paper_values(record: dict[str, object]) -> None:
    for field in (
        "paper_id",
        "canonical_id",
        "title",
        "source",
        "venue",
        "publication_status",
        "version",
        "landing_page_url",
        "fulltext_url",
        "pdf_path",
        "sha256",
    ):
        if not isinstance(record[field], str) or not record[field]:
            raise ValueError(f"Paper {field} must be a non-empty string")
    year = record["year"]
    if year is not None and (not isinstance(year, int) or isinstance(year, bool)):
        raise ValueError("Paper year must be an integer or null")
    for field in ("authors", "mechanism_clusters", _ROLE_FIELD):
        values = record[field]
        if not isinstance(values, list) or not values:
            raise ValueError(f"Paper {field} must be a non-empty list")
        if any(not isinstance(value, str) or not value for value in values):
            raise ValueError(f"Paper {field} entries must be non-empty strings")
    digest = record["sha256"]
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise ValueError("Paper sha256 must be lowercase hexadecimal")


def _resolve_pdf_path(root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("Paper pdf_path must be a non-empty string")
    normalized = PurePosixPath(value.replace("\\", "/"))
    if normalized.is_absolute() or Path(value).is_absolute():
        raise ValueError("Paper pdf_path must be relative")
    if ".." in normalized.parts:
        raise ValueError("Paper pdf_path contains traversal")
    resolved = (root / Path(*normalized.parts)).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("Paper pdf_path escapes knowledge root") from exc
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    return resolved


if __name__ == "__main__":
    raise SystemExit(main())
