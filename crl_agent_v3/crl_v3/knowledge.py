from __future__ import annotations

import hashlib
import re
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from uuid import uuid4


_FORBIDDEN_RUN_SOURCE_STATUS = "internal_run_evidence"
_FORBIDDEN_RUN_EVIDENCE_KINDS = {"internal_run", "internal_run_evidence"}
_RUN_DERIVED_TOKEN = re.compile(
    r"(?i)(?:^|[/\\_-])(?:\d{8}_\d{4}_)?run\d{2,}(?:$|[/\\_.-])"
)


@dataclass(frozen=True, slots=True)
class Paper:
    paper_id: str
    title: str
    year: int | None
    source: str
    venue: str
    publication_status: str
    fulltext_path: str
    fulltext_sha256: str


@dataclass(frozen=True, slots=True)
class ResolvedFulltext:
    paper_id: str
    recorded_path: str
    resolved_path: str
    resolution_mode: str
    size_bytes: int
    sha256: str


def resolve_paper_fulltext(
    knowledge_root: str | Path, paper: Paper
) -> ResolvedFulltext:
    """Resolve a paper PDF while keeping legacy database paths unchanged."""

    root = Path(knowledge_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"knowledge root is not a directory: {root}")
    recorded = Path(paper.fulltext_path)
    candidates: list[tuple[Path, str]] = []
    if recorded.is_absolute():
        if recorded.is_file():
            candidates.append((recorded, "recorded_absolute"))
        else:
            papers_root = root / "papers"
            if papers_root.is_dir():
                matches = [
                    item
                    for item in papers_root.iterdir()
                    if item.is_file() and item.name.casefold() == recorded.name.casefold()
                ]
                if len(matches) > 1:
                    raise ValueError(
                        f"multiple legacy PDF candidates for paper {paper.paper_id}"
                    )
                if matches:
                    candidates.append((matches[0], "legacy_filename_fallback"))
    else:
        candidate = (root / recorded).resolve(strict=False)
        try:
            candidate.relative_to(root)
        except ValueError as error:
            raise ValueError(
                f"paper full-text path escapes knowledge root: {paper.paper_id}"
            ) from error
        if candidate.is_file():
            candidates.append((candidate, "knowledge_relative"))

    if not candidates:
        raise ValueError(f"paper full text is missing: {paper.paper_id}")
    if len(candidates) != 1:
        raise ValueError(f"paper full-text resolution is ambiguous: {paper.paper_id}")
    resolved, mode = candidates[0]
    with resolved.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != paper.fulltext_sha256:
        raise ValueError(f"paper full text hash mismatch: {paper.paper_id}")
    return ResolvedFulltext(
        paper_id=paper.paper_id,
        recorded_path=paper.fulltext_path,
        resolved_path=str(resolved.resolve(strict=True)),
        resolution_mode=mode,
        size_bytes=resolved.stat().st_size,
        sha256=digest,
    )


def paper_payload(knowledge_root: str | Path, paper: Paper) -> dict[str, object]:
    payload = asdict(paper)
    resolved = resolve_paper_fulltext(knowledge_root, paper)
    payload.update(
        {
            "recorded_fulltext_path": resolved.recorded_path,
            "fulltext_path": resolved.resolved_path,
            "fulltext_resolution_mode": resolved.resolution_mode,
            "fulltext_size_bytes": resolved.size_bytes,
            "fulltext_is_current": True,
        }
    )
    return payload


@dataclass(frozen=True, slots=True)
class Passage:
    passage_id: str
    paper_id: str
    section: str
    page_start: int
    page_end: int
    char_start: int
    char_end: int
    text: str
    text_sha256: str


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    paper_id: str
    fulltext_sha256: str
    evidence_kind: str
    section: str
    page_start: int
    page_end: int
    locator: str
    source_content: str
    source_content_sha256: str
    codex_note: str
    passage_id: str | None
    passage_text_sha256: str | None
    quote_start: int | None
    quote_end: int | None
    fulltext_is_current: bool
    passage_is_current: bool | None


@dataclass(frozen=True, slots=True)
class SearchHit:
    paper_id: str
    passage_id: str
    title: str
    section: str
    page_start: int
    page_end: int
    char_start: int
    char_end: int
    text: str
    fulltext_sha256: str
    text_sha256: str
    rank: float


@dataclass(frozen=True, slots=True)
class QueryNormalization:
    original_query: str
    normalized_query: str
    english_keyword_hint: str | None


_SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    paper_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER,
    source TEXT NOT NULL,
    venue TEXT NOT NULL,
    publication_status TEXT NOT NULL,
    fulltext_path TEXT NOT NULL,
    fulltext_sha256 TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS passages (
    passage_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    section TEXT NOT NULL,
    page_start INTEGER NOT NULL,
    page_end INTEGER NOT NULL,
    char_start INTEGER NOT NULL,
    char_end INTEGER NOT NULL,
    text TEXT NOT NULL,
    text_sha256 TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS passages_paper_id_idx ON passages(paper_id);

CREATE TABLE IF NOT EXISTS evidence (
    evidence_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    fulltext_sha256 TEXT NOT NULL,
    evidence_kind TEXT NOT NULL,
    section TEXT NOT NULL,
    page_start INTEGER NOT NULL CHECK(page_start >= 1),
    page_end INTEGER NOT NULL CHECK(page_end >= page_start),
    locator TEXT NOT NULL,
    source_content TEXT NOT NULL,
    source_content_sha256 TEXT NOT NULL,
    codex_note TEXT NOT NULL,
    passage_id TEXT,
    passage_text_sha256 TEXT,
    quote_start INTEGER,
    quote_end INTEGER,
    CHECK (
        (
            passage_id IS NULL AND passage_text_sha256 IS NULL
            AND quote_start IS NULL AND quote_end IS NULL
        ) OR (
            passage_id IS NOT NULL AND passage_text_sha256 IS NOT NULL
            AND quote_start IS NOT NULL AND quote_end IS NOT NULL
            AND quote_start >= 0 AND quote_end >= quote_start
        )
    )
);

CREATE INDEX IF NOT EXISTS evidence_paper_id_idx ON evidence(paper_id);

CREATE VIRTUAL TABLE IF NOT EXISTS passages_fts USING fts5(
    passage_id UNINDEXED,
    paper_id UNINDEXED,
    text
);

CREATE TABLE IF NOT EXISTS knowledge_metadata (
    singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
    passage_revision INTEGER NOT NULL CHECK(passage_revision >= 0),
    passage_generation_id TEXT NOT NULL CHECK(passage_generation_id <> '')
);
"""


_EVIDENCE_SELECT = """
SELECT
    e.evidence_id,
    e.paper_id,
    e.fulltext_sha256,
    e.evidence_kind,
    e.section,
    e.page_start,
    e.page_end,
    e.locator,
    e.source_content,
    e.source_content_sha256,
    e.codex_note,
    e.passage_id,
    e.passage_text_sha256,
    e.quote_start,
    e.quote_end,
    p.fulltext_sha256 AS current_fulltext_sha256,
    g.paper_id AS current_passage_paper_id,
    g.text AS current_passage_text,
    g.text_sha256 AS current_passage_text_sha256
FROM evidence AS e
JOIN papers AS p ON p.paper_id = e.paper_id
LEFT JOIN passages AS g ON g.passage_id = e.passage_id
"""


class KnowledgeStore:
    def __init__(
        self,
        database_path: str | Path,
        *,
        read_only: bool = True,
    ) -> None:
        self.database_path = Path(database_path)
        self.read_only = read_only
        if read_only:
            if not self.database_path.is_file():
                raise FileNotFoundError(
                    f"Knowledge database is not a file: {self.database_path}"
                )
            database_uri = f"{self.database_path.resolve().as_uri()}?mode=ro"
            self._connection = sqlite3.connect(
                database_uri,
                uri=True,
                timeout=5.0,
            )
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys=ON")
            self._connection.execute("PRAGMA busy_timeout=5000")
            self._connection.execute("PRAGMA query_only=ON")
            return
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path, timeout=5.0)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys=ON")
        self._connection.execute("PRAGMA busy_timeout=5000")
        self._connection.executescript(_SCHEMA)
        self._initialize_metadata()

    def _initialize_metadata(self) -> None:
        columns = {
            str(row["name"])
            for row in self._connection.execute(
                "PRAGMA table_info(knowledge_metadata)"
            ).fetchall()
        }
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            if "passage_generation_id" not in columns:
                self._connection.execute(
                    "ALTER TABLE knowledge_metadata ADD COLUMN passage_generation_id TEXT"
                )
                self._connection.execute(
                    """
                    UPDATE knowledge_metadata
                    SET passage_generation_id = ?
                    WHERE singleton = 1
                    """,
                    (uuid4().hex,),
                )
            self._connection.execute(
                """
                INSERT OR IGNORE INTO knowledge_metadata (
                    singleton, passage_revision, passage_generation_id
                ) VALUES (1, 0, ?)
                """,
                (uuid4().hex,),
            )
            row = self._connection.execute(
                """
                SELECT passage_generation_id
                FROM knowledge_metadata
                WHERE singleton = 1
                """
            ).fetchone()
            if row is None or not row["passage_generation_id"]:
                raise RuntimeError("Knowledge metadata generation is missing")
        except BaseException:
            self._connection.rollback()
            raise
        else:
            self._connection.commit()

    def add_paper(self, paper: Paper, passages: Iterable[Passage]) -> None:
        self._assert_writable()
        _reject_run_derived_paper(paper)
        items = tuple(passages)
        if any(item.paper_id != paper.paper_id for item in items):
            raise ValueError("Every passage must refer to the supplied paper")

        try:
            self._connection.execute("BEGIN IMMEDIATE")
            self._connection.execute(
                """
                INSERT INTO papers (
                    paper_id, title, year, source, venue, publication_status,
                    fulltext_path, fulltext_sha256
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(paper_id) DO UPDATE SET
                    title=excluded.title,
                    year=excluded.year,
                    source=excluded.source,
                    venue=excluded.venue,
                    publication_status=excluded.publication_status,
                    fulltext_path=excluded.fulltext_path,
                    fulltext_sha256=excluded.fulltext_sha256
                """,
                (
                    paper.paper_id,
                    paper.title,
                    paper.year,
                    paper.source,
                    paper.venue,
                    paper.publication_status,
                    paper.fulltext_path,
                    paper.fulltext_sha256,
                ),
            )
            self._connection.execute(
                "DELETE FROM passages_fts WHERE paper_id = ?", (paper.paper_id,)
            )
            self._connection.execute(
                "DELETE FROM passages WHERE paper_id = ?", (paper.paper_id,)
            )
            for item in items:
                self._connection.execute(
                    """
                    INSERT INTO passages (
                        passage_id, paper_id, section, page_start, page_end,
                        char_start, char_end, text, text_sha256
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item.passage_id,
                        item.paper_id,
                        item.section,
                        item.page_start,
                        item.page_end,
                        item.char_start,
                        item.char_end,
                        item.text,
                        item.text_sha256,
                    ),
                )
                self._connection.execute(
                    """
                    INSERT INTO passages_fts (passage_id, paper_id, text)
                    VALUES (?, ?, ?)
                    """,
                    (item.passage_id, item.paper_id, item.text),
                )
            self._connection.execute(
                """
                UPDATE knowledge_metadata
                SET
                    passage_revision = passage_revision + 1,
                    passage_generation_id = ?
                WHERE singleton = 1
                """,
                (uuid4().hex,),
            )
        except BaseException:
            self._connection.rollback()
            raise
        else:
            self._connection.commit()

    def add_evidence(
        self,
        *,
        evidence_id: str,
        paper_id: str,
        fulltext_sha256: str,
        evidence_kind: str,
        section: str,
        page_start: int,
        page_end: int,
        locator: str,
        source_content: str,
        codex_note: str,
        passage_id: str | None = None,
        passage_text_sha256: str | None = None,
        quote_start: int | None = None,
        quote_end: int | None = None,
    ) -> Evidence:
        self._assert_writable()
        if evidence_kind.casefold() in _FORBIDDEN_RUN_EVIDENCE_KINDS:
            raise ValueError("Run-derived Evidence is forbidden in the shared knowledge base")
        if any(
            _RUN_DERIVED_TOKEN.search(value)
            for value in (evidence_id, locator, codex_note)
        ):
            raise ValueError("Run-derived identifiers are forbidden in shared Evidence")
        if page_start < 1 or page_end < page_start:
            raise ValueError("Evidence pages must be one-based inclusive endpoints")
        anchors = (passage_id, passage_text_sha256, quote_start, quote_end)
        if any(value is None for value in anchors) and not all(
            value is None for value in anchors
        ):
            raise ValueError("Passage anchor fields must be supplied together")

        source_content_sha256 = hashlib.sha256(
            source_content.encode("utf-8")
        ).hexdigest()
        values = (
            evidence_id,
            paper_id,
            fulltext_sha256,
            evidence_kind,
            section,
            page_start,
            page_end,
            locator,
            source_content,
            source_content_sha256,
            codex_note,
            passage_id,
            passage_text_sha256,
            quote_start,
            quote_end,
        )

        try:
            self._connection.execute("BEGIN IMMEDIATE")
            existing = self._connection.execute(
                """
                SELECT
                    evidence_id, paper_id, fulltext_sha256, evidence_kind,
                    section, page_start, page_end, locator, source_content,
                    source_content_sha256, codex_note, passage_id,
                    passage_text_sha256, quote_start, quote_end
                FROM evidence
                WHERE evidence_id = ?
                """,
                (evidence_id,),
            ).fetchone()
            if existing is not None:
                if tuple(existing) != values:
                    raise ValueError("Evidence ID already has different content")
            else:
                paper = self._connection.execute(
                    "SELECT fulltext_sha256 FROM papers WHERE paper_id = ?",
                    (paper_id,),
                ).fetchone()
                if paper is None:
                    raise ValueError("Evidence paper does not exist")
                if paper["fulltext_sha256"] != fulltext_sha256:
                    raise ValueError("Evidence full-text hash does not match paper")

                if passage_id is not None:
                    passage = self._connection.execute(
                        """
                        SELECT paper_id, text, text_sha256
                        FROM passages
                        WHERE passage_id = ?
                        """,
                        (passage_id,),
                    ).fetchone()
                    if passage is None:
                        raise ValueError("Evidence passage does not exist")
                    if passage["paper_id"] != paper_id:
                        raise ValueError("Evidence passage belongs to another paper")
                    if passage["text_sha256"] != passage_text_sha256:
                        raise ValueError("Evidence passage hash does not match")
                    if not (
                        0 <= quote_start <= quote_end <= len(passage["text"])
                    ):
                        raise ValueError("Evidence quote range is invalid")
                    if passage["text"][quote_start:quote_end] != source_content:
                        raise ValueError("Evidence quote does not match passage text")

                self._connection.execute(
                    """
                    INSERT INTO evidence (
                        evidence_id, paper_id, fulltext_sha256, evidence_kind,
                        section, page_start, page_end, locator, source_content,
                        source_content_sha256, codex_note, passage_id,
                        passage_text_sha256, quote_start, quote_end
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    values,
                )
        except BaseException:
            self._connection.rollback()
            raise
        else:
            self._connection.commit()

        evidence = self.get_evidence(evidence_id)
        if evidence is None:
            raise RuntimeError("Stored evidence is missing")
        return evidence

    def search(self, query: str, limit: int = 20) -> list[SearchHit]:
        match_query = normalize_fts_query(query).normalized_query
        if limit <= 0:
            raise ValueError("Search limit must be positive")
        rows = self._connection.execute(
            """
            SELECT
                p.paper_id,
                g.passage_id,
                p.title,
                g.section,
                g.page_start,
                g.page_end,
                g.char_start,
                g.char_end,
                g.text,
                p.fulltext_sha256,
                g.text_sha256,
                bm25(passages_fts) AS rank
            FROM passages_fts
            JOIN passages AS g ON g.passage_id = passages_fts.passage_id
            JOIN papers AS p ON p.paper_id = g.paper_id
            WHERE passages_fts MATCH ?
            ORDER BY rank, g.passage_id
            LIMIT ?
            """,
            (match_query, limit),
        ).fetchall()
        return [
            SearchHit(
                paper_id=row["paper_id"],
                passage_id=row["passage_id"],
                title=row["title"],
                section=row["section"],
                page_start=row["page_start"],
                page_end=row["page_end"],
                char_start=row["char_start"],
                char_end=row["char_end"],
                text=row["text"],
                fulltext_sha256=row["fulltext_sha256"],
                text_sha256=row["text_sha256"],
                rank=float(row["rank"]),
            )
            for row in rows
        ]

    def get_paper(self, paper_id: str) -> Paper | None:
        row = self._connection.execute(
            "SELECT * FROM papers WHERE paper_id = ?", (paper_id,)
        ).fetchone()
        return Paper(**dict(row)) if row is not None else None

    def get_passage(self, passage_id: str) -> Passage | None:
        row = self._connection.execute(
            "SELECT * FROM passages WHERE passage_id = ?", (passage_id,)
        ).fetchone()
        return Passage(**dict(row)) if row is not None else None

    def get_evidence(self, evidence_id: str) -> Evidence | None:
        row = self._connection.execute(
            _EVIDENCE_SELECT + " WHERE e.evidence_id = ?", (evidence_id,)
        ).fetchone()
        return _evidence_from_row(row) if row is not None else None

    def list_evidence(self, paper_id: str) -> list[Evidence]:
        rows = self._connection.execute(
            _EVIDENCE_SELECT
            + " WHERE e.paper_id = ? ORDER BY e.evidence_id",
            (paper_id,),
        ).fetchall()
        return [_evidence_from_row(row) for row in rows]

    def list_passages(self) -> list[Passage]:
        rows = self._connection.execute(
            "SELECT * FROM passages ORDER BY passage_id"
        ).fetchall()
        return [Passage(**dict(row)) for row in rows]

    def passage_revision(self) -> int:
        row = self._connection.execute(
            "SELECT passage_revision FROM knowledge_metadata WHERE singleton = 1"
        ).fetchone()
        if row is None:
            raise RuntimeError("Knowledge metadata is missing")
        return int(row["passage_revision"])

    def passage_identity(self) -> tuple[int, str]:
        row = self._connection.execute(
            """
            SELECT passage_revision, passage_generation_id
            FROM knowledge_metadata
            WHERE singleton = 1
            """
        ).fetchone()
        if row is None or not row["passage_generation_id"]:
            raise RuntimeError("Knowledge metadata is missing")
        return int(row["passage_revision"]), str(row["passage_generation_id"])

    def passage_snapshot(self) -> tuple[tuple[int, str], list[Passage]]:
        try:
            self._connection.execute("BEGIN")
            identity = self.passage_identity()
            rows = self._connection.execute(
                "SELECT * FROM passages ORDER BY passage_id"
            ).fetchall()
        except BaseException:
            self._connection.rollback()
            raise
        else:
            self._connection.commit()
        return identity, [Passage(**dict(row)) for row in rows]

    def delete_paper(self, paper_id: str) -> bool:
        self._assert_writable()
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            exists = self._connection.execute(
                "SELECT 1 FROM papers WHERE paper_id = ?", (paper_id,)
            ).fetchone()
            if exists is None:
                self._connection.rollback()
                return False
            self._connection.execute(
                "DELETE FROM passages_fts WHERE paper_id = ?", (paper_id,)
            )
            self._connection.execute("DELETE FROM papers WHERE paper_id = ?", (paper_id,))
            self._connection.execute(
                """
                UPDATE knowledge_metadata
                SET
                    passage_revision = passage_revision + 1,
                    passage_generation_id = ?
                WHERE singleton = 1
                """,
                (uuid4().hex,),
            )
        except BaseException:
            self._connection.rollback()
            raise
        else:
            self._connection.commit()
        return True

    def close(self) -> None:
        self._connection.close()

    def _assert_writable(self) -> None:
        if self.read_only:
            raise PermissionError("KnowledgeStore is read-only; maintenance must opt in explicitly")


def _reject_run_derived_paper(paper: Paper) -> None:
    if paper.publication_status.casefold() == _FORBIDDEN_RUN_SOURCE_STATUS:
        raise ValueError("Run-derived papers are forbidden in the shared knowledge base")
    if any(
        _RUN_DERIVED_TOKEN.search(value)
        for value in (
            paper.paper_id,
            paper.source,
            paper.fulltext_path,
        )
    ):
        raise ValueError("Run-derived paper identifiers are forbidden in the shared knowledge base")


def normalize_fts_query(query: str) -> QueryNormalization:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("search query must contain searchable text")
    units: list[str] = []
    seen: set[str] = set()
    for match in re.finditer(r'"([^"\r\n]+)"|([^\W]+)', query, flags=re.UNICODE):
        value = match.group(1) or match.group(2)
        value = value.strip()
        if not value:
            continue
        key = value.casefold()
        if key not in seen:
            seen.add(key)
            units.append('"' + value.replace('"', '""') + '"')
    if not units:
        raise ValueError("search query contains only punctuation or separators")
    contains_non_ascii = any(ord(character) > 127 for character in query)
    contains_ascii_term = re.search(r"[A-Za-z]{2,}", query) is not None
    hint = None
    if contains_non_ascii and not contains_ascii_term:
        hint = "论文正文以英文为主；若结果不足，可补充英文技术关键词。"
    return QueryNormalization(query, " OR ".join(units), hint)


def _evidence_from_row(row: sqlite3.Row) -> Evidence:
    passage_is_current: bool | None
    if row["passage_id"] is None:
        passage_is_current = None
    else:
        text = row["current_passage_text"]
        start = row["quote_start"]
        end = row["quote_end"]
        passage_is_current = (
            row["current_passage_paper_id"] == row["paper_id"]
            and row["current_passage_text_sha256"] == row["passage_text_sha256"]
            and text is not None
            and 0 <= start <= end <= len(text)
            and text[start:end] == row["source_content"]
        )
    return Evidence(
        evidence_id=row["evidence_id"],
        paper_id=row["paper_id"],
        fulltext_sha256=row["fulltext_sha256"],
        evidence_kind=row["evidence_kind"],
        section=row["section"],
        page_start=row["page_start"],
        page_end=row["page_end"],
        locator=row["locator"],
        source_content=row["source_content"],
        source_content_sha256=row["source_content_sha256"],
        codex_note=row["codex_note"],
        passage_id=row["passage_id"],
        passage_text_sha256=row["passage_text_sha256"],
        quote_start=row["quote_start"],
        quote_end=row["quote_end"],
        fulltext_is_current=(
            row["current_fulltext_sha256"] == row["fulltext_sha256"]
        ),
        passage_is_current=passage_is_current,
    )
