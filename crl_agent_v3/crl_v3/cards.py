from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from uuid import uuid4

from .knowledge import KnowledgeStore, normalize_fts_query


CardKind = Literal["paper", "operator", "failure"]


@dataclass(frozen=True, slots=True)
class SourceRef:
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class CardMetadata:
    schema_version: int
    card_id: str
    card_kind: CardKind
    paper_id: str | None
    evidence_ids: tuple[str, ...]
    source_refs: tuple[SourceRef, ...]


@dataclass(frozen=True, slots=True)
class CardDocument:
    path: Path
    metadata: CardMetadata
    title: str
    body: str
    sha256: str


@dataclass(frozen=True, slots=True)
class CardIndexBuildResult:
    index_path: Path
    card_count: int
    kind_counts: tuple[tuple[str, int], ...]
    source_signature: str


@dataclass(frozen=True, slots=True)
class CardSearchHit:
    card_id: str
    card_kind: CardKind
    relative_path: str
    title: str
    snippet: str
    markdown_sha256: str
    rank: float


_META_PREFIX = "<!-- CRL_CARD_META "
_META_SUFFIX = " -->"
_CARD_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,127}")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_KINDS = ("failure", "operator", "paper")
_FORBIDDEN_RUN_SOURCE_STATUS = "internal_run_evidence"
_RUN_DERIVED_TOKEN = re.compile(
    r"(?i)(?:^|[^A-Za-z0-9])(?:\d{8}_\d{4}_)?run\d{2,}(?:$|[^A-Za-z0-9])"
)
_METADATA_FIELDS = {
    "schema_version",
    "card_id",
    "card_kind",
    "paper_id",
    "evidence_ids",
    "source_refs",
}
_SOURCE_REF_FIELDS = {"path", "sha256"}
_FACT_LABELS = {
    "AUTHOR_FACT",
    "AUTHOR_INTERPRETATION",
    "CODEX_SYNTHESIS",
    "CODEX_HYPOTHESIS",
}
_EVIDENCE_TOKEN = re.compile(r"\[\[evidence:([^\]\s]+)\]\]")
_REQUIRED_HEADINGS = {
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
    "operator": (
        "Intervention target",
        "Before and after computation",
        "Inputs outputs information and timing",
        "Mechanism hypothesis",
        "Predicted observable signature",
        "Preconditions and transfer risks",
        "Source lineage",
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
}
_CARD_INDEX_SCHEMA_VERSION = 1
_CARD_INDEX_SCHEMA = """
CREATE TABLE card_documents (
    card_id TEXT PRIMARY KEY,
    card_kind TEXT NOT NULL,
    relative_path TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    markdown_sha256 TEXT NOT NULL
);
CREATE VIRTUAL TABLE cards_fts USING fts5(
    card_id UNINDEXED,
    card_kind UNINDEXED,
    title,
    body,
    tokenize='unicode61'
);
CREATE TABLE card_index_metadata (
    singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
    schema_version INTEGER NOT NULL,
    source_signature TEXT NOT NULL
);
"""


def parse_card(path: str | Path) -> CardDocument:
    card_path = Path(path)
    raw = card_path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not allowed")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid UTF-8 Card bytes") from exc
    if "\r" in text:
        raise ValueError("CRLF or CR newlines are not allowed")
    if "\n" not in text:
        raise ValueError("Card must contain metadata and Markdown body")
    first_line, body = text.split("\n", 1)
    if not first_line.startswith(_META_PREFIX) or not first_line.endswith(
        _META_SUFFIX
    ):
        raise ValueError("missing or malformed CRL_CARD_META first line")
    try:
        payload = json.loads(first_line[len(_META_PREFIX) : -len(_META_SUFFIX)])
    except json.JSONDecodeError as exc:
        raise ValueError("invalid CRL_CARD_META JSON") from exc
    if _META_PREFIX in body:
        raise ValueError("metadata comment must be unique and appear only on line one")
    if _RUN_DERIVED_TOKEN.search(first_line) or _RUN_DERIVED_TOKEN.search(body):
        raise ValueError("Run-derived material is forbidden in shared Cards")
    if not isinstance(payload, dict) or set(payload) != _METADATA_FIELDS:
        raise ValueError("metadata fields must equal the six-field schema")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise ValueError("schema_version must be integer 1")
    card_id = payload["card_id"]
    if not isinstance(card_id, str) or _CARD_ID.fullmatch(card_id) is None:
        raise ValueError("card_id is invalid")
    card_kind = payload["card_kind"]
    if not isinstance(card_kind, str) or card_kind not in _KINDS:
        raise ValueError("card_kind is invalid")
    paper_id = payload["paper_id"]
    if paper_id is not None and (not isinstance(paper_id, str) or not paper_id):
        raise ValueError("paper_id must be a non-empty string or null")
    evidence_ids = payload["evidence_ids"]
    if (
        not isinstance(evidence_ids, list)
        or not evidence_ids
        or any(not isinstance(item, str) or not item for item in evidence_ids)
    ):
        raise ValueError("evidence_ids must be a non-empty string array")
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("duplicate evidence_id is not allowed")
    source_items = payload["source_refs"]
    if not isinstance(source_items, list) or not source_items:
        raise ValueError("source_refs must be a non-empty array")
    source_refs: list[SourceRef] = []
    for item in source_items:
        if not isinstance(item, dict) or set(item) != _SOURCE_REF_FIELDS:
            raise ValueError("source_ref fields must be path and sha256")
        source_path = item["path"]
        source_sha256 = item["sha256"]
        if not isinstance(source_path, str) or not _is_relative_posix_path(source_path):
            raise ValueError("source_ref path must be a relative POSIX path")
        if not isinstance(source_sha256, str) or _SHA256.fullmatch(source_sha256) is None:
            raise ValueError("source_ref sha256 must be 64 lowercase hex characters")
        source_refs.append(SourceRef(path=source_path, sha256=source_sha256))
    if card_path.stem != card_id:
        raise ValueError("card_id must match the file name stem")
    if card_path.parent.name != card_kind:
        raise ValueError("card_kind must match the parent directory")
    lines = body.splitlines()
    nonempty = [line for line in lines if line.strip()]
    h1_lines = [line for line in lines if line.startswith("# ")]
    if len(h1_lines) != 1 or not nonempty or nonempty[0] != h1_lines[0]:
        raise ValueError("Card body must contain a unique H1 as its first content")
    headings = tuple(line[3:] for line in lines if line.startswith("## "))
    if headings != _REQUIRED_HEADINGS[card_kind]:
        raise ValueError("required heading set and order do not match card_kind")
    for match in re.finditer(
        r"(?m)^(?:[-*]\s+|\d+\.\s+)?\[([A-Z_]+)\]", body
    ):
        if match.group(1) not in _FACT_LABELS:
            raise ValueError(f"unknown fact label: {match.group(1)}")
    metadata = CardMetadata(
        schema_version=payload["schema_version"],
        card_id=card_id,
        card_kind=card_kind,
        paper_id=paper_id,
        evidence_ids=tuple(evidence_ids),
        source_refs=tuple(source_refs),
    )
    title_line = h1_lines[0]
    return CardDocument(
        path=card_path,
        metadata=metadata,
        title=title_line[2:].strip(),
        body=body,
        sha256=hashlib.sha256(raw).hexdigest(),
    )


def _is_relative_posix_path(value: str) -> bool:
    if not value or "\\" in value or value.startswith("/"):
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    parts = value.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def validate_card(
    card: CardDocument,
    *,
    store: KnowledgeStore,
    project_root: str | Path,
) -> None:
    root = Path(project_root).resolve()
    source_hashes: set[str] = set()
    for source_ref in card.metadata.source_refs:
        source_path = root.joinpath(*source_ref.path.split("/")).resolve()
        if not source_path.is_relative_to(root):
            raise ValueError(f"source path escapes project_root: {source_ref.path}")
        if not source_path.is_file():
            raise ValueError(f"source file not found: {source_ref.path}")
        actual_sha256 = _file_sha256(source_path)
        if actual_sha256 != source_ref.sha256:
            raise ValueError(f"source SHA-256 mismatch: {source_ref.path}")
        source_hashes.add(actual_sha256)

    declared_evidence = set(card.metadata.evidence_ids)
    body_evidence = set(_EVIDENCE_TOKEN.findall(card.body))
    undeclared = sorted(body_evidence - declared_evidence)
    if undeclared:
        raise ValueError(f"metadata does not declare Evidence tokens: {undeclared}")
    unused = sorted(declared_evidence - body_evidence)
    if unused:
        raise ValueError(f"unused metadata Evidence ids: {unused}")
    for block in _paragraph_and_list_blocks(card.body):
        content = re.sub(r"^(?:[-*]\s+|\d+\.\s+)", "", block.strip())
        if content.startswith(("[AUTHOR_FACT]", "[AUTHOR_INTERPRETATION]")):
            if _EVIDENCE_TOKEN.search(content) is None:
                label = content.split("]", 1)[0] + "]"
                raise ValueError(f"{label} requires inline Evidence token")

    evidence_items = []
    for evidence_id in card.metadata.evidence_ids:
        evidence = store.get_evidence(evidence_id)
        if evidence is None:
            raise ValueError(f"Evidence not found: {evidence_id}")
        if not evidence.fulltext_is_current:
            raise ValueError(f"stale Evidence fulltext: {evidence_id}")
        if evidence.passage_id is not None and evidence.passage_is_current is not True:
            raise ValueError(f"stale Evidence passage: {evidence_id}")
        if evidence.fulltext_sha256 not in source_hashes:
            raise ValueError(
                f"Evidence fulltext SHA-256 lacks SourceRef coverage: {evidence_id}"
            )
        evidence_items.append(evidence)

    paper_id = card.metadata.paper_id
    if card.metadata.card_kind == "paper" and paper_id is None:
        raise ValueError("Paper Card paper_id must not be null")
    if paper_id is not None and store.get_paper(paper_id) is None:
        raise ValueError(f"paper_id not found: {paper_id}")
    if card.metadata.card_kind == "paper":
        if any(evidence.paper_id != paper_id for evidence in evidence_items):
            raise ValueError("Paper Card Evidence must match metadata paper_id")

    for evidence in evidence_items:
        source_paper = store.get_paper(evidence.paper_id)
        if (
            source_paper is not None
            and source_paper.publication_status == _FORBIDDEN_RUN_SOURCE_STATUS
        ):
            raise ValueError(
                "Run-derived material is forbidden in the shared paper knowledge base"
            )


def load_valid_cards(
    cards_root: str | Path,
    *,
    store: KnowledgeStore,
    project_root: str | Path,
) -> tuple[CardDocument, ...]:
    root = Path(cards_root)
    paths = sorted(
        (
            path
            for kind in _KINDS
            for path in (root / kind).glob("*.md")
            if path.is_file()
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    cards: list[CardDocument] = []
    seen_ids: set[str] = set()
    for path in paths:
        card = parse_card(path)
        if card.metadata.card_id in seen_ids:
            raise ValueError(f"duplicate card_id: {card.metadata.card_id}")
        validate_card(card, store=store, project_root=project_root)
        seen_ids.add(card.metadata.card_id)
        cards.append(card)
    return tuple(cards)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _paragraph_and_list_blocks(body: str) -> tuple[str, ...]:
    blocks: list[str] = []
    for paragraph in re.split(r"\n[ \t]*\n", body):
        if not paragraph.strip():
            continue
        current: list[str] = []
        for line in paragraph.splitlines():
            if re.match(r"^(?:[-*]\s+|\d+\.\s+)", line):
                if current:
                    blocks.append("\n".join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            blocks.append("\n".join(current))
    return tuple(blocks)


def rebuild_card_index(
    cards_root: str | Path,
    index_path: str | Path,
    *,
    store: KnowledgeStore,
    project_root: str | Path,
) -> CardIndexBuildResult:
    root = Path(cards_root)
    destination = Path(index_path)
    cards = load_valid_cards(root, store=store, project_root=project_root)
    snapshot = tuple(
        sorted(
            (
                card.path.relative_to(root).as_posix(),
                card.sha256,
            )
            for card in cards
        )
    )
    signature = _source_signature(snapshot)
    counts = tuple(
        (kind, sum(card.metadata.card_kind == kind for card in cards))
        for kind in _KINDS
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(
        f"{destination.name}.{uuid4().hex}.tmp"
    )
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(temporary)
        connection.executescript(_CARD_INDEX_SCHEMA)
        connection.execute("BEGIN")
        for card in cards:
            relative_path = card.path.relative_to(root).as_posix()
            values = (
                card.metadata.card_id,
                card.metadata.card_kind,
                relative_path,
                card.title,
                card.body,
                card.sha256,
            )
            connection.execute(
                """
                INSERT INTO card_documents (
                    card_id, card_kind, relative_path, title, body, markdown_sha256
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                values,
            )
            connection.execute(
                """
                INSERT INTO cards_fts (card_id, card_kind, title, body)
                VALUES (?, ?, ?, ?)
                """,
                (
                    card.metadata.card_id,
                    card.metadata.card_kind,
                    card.title,
                    card.body,
                ),
            )
        connection.execute(
            """
            INSERT INTO card_index_metadata (
                singleton, schema_version, source_signature
            ) VALUES (1, ?, ?)
            """,
            (_CARD_INDEX_SCHEMA_VERSION, signature),
        )
        connection.commit()
        connection.close()
        connection = None
        os.replace(temporary, destination)
    except BaseException:
        if connection is not None:
            connection.close()
        temporary.unlink(missing_ok=True)
        raise
    return CardIndexBuildResult(
        index_path=destination,
        card_count=len(cards),
        kind_counts=counts,
        source_signature=signature,
    )


def card_index_status(
    cards_root: str | Path, index_path: str | Path
) -> dict[str, object]:
    root = Path(cards_root)
    path = Path(index_path)
    if not path.is_file():
        return {"ready": False, "reason": "index_missing", "index_path": str(path)}
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(path)
        row = connection.execute(
            """
            SELECT schema_version, source_signature
            FROM card_index_metadata
            WHERE singleton = 1
            """
        ).fetchone()
        if row is None:
            return {
                "ready": False,
                "reason": "index_invalid",
                "index_path": str(path),
            }
        if int(row[0]) != _CARD_INDEX_SCHEMA_VERSION:
            return {
                "ready": False,
                "reason": "unsupported_schema",
                "index_path": str(path),
            }
        stored_signature = str(row[1])
        document_count = int(
            connection.execute("SELECT COUNT(*) FROM card_documents").fetchone()[0]
        )
        fts_count = int(
            connection.execute("SELECT COUNT(*) FROM cards_fts").fetchone()[0]
        )
        if document_count != fts_count or _SHA256.fullmatch(stored_signature) is None:
            return {
                "ready": False,
                "reason": "index_invalid",
                "index_path": str(path),
            }
    except (OSError, sqlite3.Error, TypeError, ValueError):
        return {"ready": False, "reason": "index_invalid", "index_path": str(path)}
    finally:
        if connection is not None:
            connection.close()
    current_signature = _source_signature(_card_source_snapshot(root))
    if current_signature != stored_signature:
        return {
            "ready": False,
            "reason": "card_sources_changed",
            "index_path": str(path),
        }
    return {
        "ready": True,
        "reason": "ready",
        "index_path": str(path),
        "cards": document_count,
    }


def card_source_signature(cards_root: str | Path) -> str:
    """Return the exact source signature used by the Card index."""

    return _source_signature(_card_source_snapshot(Path(cards_root)))


def search_cards(
    cards_root: str | Path,
    index_path: str | Path,
    query: str,
    *,
    kinds: tuple[CardKind, ...],
    limit: int = 20,
) -> tuple[CardSearchHit, ...]:
    if limit <= 0:
        raise ValueError("limit must be greater than zero")
    if not kinds:
        raise ValueError("kinds must not be empty")
    if any(kind not in _KINDS for kind in kinds):
        raise ValueError("invalid card kind")
    selected_kinds = tuple(sorted(set(kinds)))
    status = card_index_status(cards_root, index_path)
    if status["ready"] is not True:
        raise ValueError(f"card index is not ready: {status['reason']}")
    match_query = normalize_fts_query(query).normalized_query
    placeholders = ", ".join("?" for _ in selected_kinds)
    sql = f"""
        SELECT d.card_id, d.card_kind, d.relative_path, d.title,
               snippet(cards_fts, 3, '[', ']', ' ... ', 24) AS snippet,
               d.markdown_sha256, bm25(cards_fts) AS rank
        FROM cards_fts
        JOIN card_documents AS d ON d.card_id = cards_fts.card_id
        WHERE cards_fts MATCH ? AND d.card_kind IN ({placeholders})
        ORDER BY rank, d.card_id
        LIMIT ?
    """
    connection = sqlite3.connect(Path(index_path))
    try:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            sql, (match_query, *selected_kinds, limit)
        ).fetchall()
    finally:
        connection.close()
    return tuple(
        CardSearchHit(
            card_id=str(row["card_id"]),
            card_kind=row["card_kind"],
            relative_path=str(row["relative_path"]),
            title=str(row["title"]),
            snippet=str(row["snippet"]),
            markdown_sha256=str(row["markdown_sha256"]),
            rank=float(row["rank"]),
        )
        for row in rows
    )


def _card_source_snapshot(cards_root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (
                path.relative_to(cards_root).as_posix(),
                _file_sha256(path),
            )
            for kind in _KINDS
            for path in (cards_root / kind).glob("*.md")
            if path.is_file()
        )
    )


def _source_signature(snapshot: tuple[tuple[str, str], ...]) -> str:
    digest = hashlib.sha256()
    for relative_path, markdown_sha256 in snapshot:
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(markdown_sha256.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()
