from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import stat
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

from .cards import card_index_status, parse_card, validate_card
from .knowledge import KnowledgeStore
from .vector import vector_index_status


DEFAULT_SHORT_PASSAGE_CHARS = 20
DEFAULT_EXTREME_PASSAGE_CHARS = 20_000
_CARD_KINDS = ("failure", "operator", "paper")


@dataclass(frozen=True, slots=True)
class AuditFinding:
    severity: str
    code: str
    message: str
    details: dict[str, object]


def audit_knowledge_base(
    knowledge_root: str | Path,
    *,
    project_root: str | Path,
    lock_path: str | Path | None = None,
    short_passage_chars: int = DEFAULT_SHORT_PASSAGE_CHARS,
    extreme_passage_chars: int = DEFAULT_EXTREME_PASSAGE_CHARS,
) -> dict[str, object]:
    """Read one knowledge base and return diagnostics without changing it.

    Severity labels describe individual findings only.  This function deliberately
    does not calculate a readiness, pass/fail, or research-quality verdict.
    """

    if short_passage_chars < 0:
        raise ValueError("short_passage_chars must be non-negative")
    if extreme_passage_chars <= short_passage_chars:
        raise ValueError("extreme_passage_chars must exceed short_passage_chars")
    project = _existing_directory(project_root, "project_root")
    root = _safe_existing_directory(knowledge_root, project, "knowledge_root")
    selected_lock = (
        _safe_existing_file(lock_path, project, "lock")
        if lock_path is not None
        else root / "evaluation" / "PRODUCTION_RETRIEVAL_LOCK.json"
    )

    findings: list[AuditFinding] = []
    counts: dict[str, int | None] = {
        "papers": None,
        "passages": None,
        "evidence": None,
        "cards": None,
    }
    length_distribution: dict[str, int | float | None] = {
        "minimum": None,
        "p25": None,
        "median": None,
        "p75": None,
        "p90": None,
        "p95": None,
        "p99": None,
        "maximum": None,
    }
    passage_anomaly_counts = {
        "blank": 0,
        "very_short": 0,
        "extreme_long": 0,
        "duplicate_groups_within_paper": 0,
        "duplicate_passages_within_paper": 0,
        "coordinate_length_mismatch": 0,
        "text_hash_mismatch": 0,
    }

    database_candidate = root / "knowledge.sqlite"
    database: Path | None
    connection: sqlite3.Connection | None = None
    store: KnowledgeStore | None = None
    try:
        database = _safe_existing_file(
            database_candidate, project, "knowledge.sqlite"
        )
    except FileNotFoundError:
        database = None
        _add(findings, "ERROR", "KNOWLEDGE_DATABASE_MISSING", "knowledge.sqlite 不存在", path=str(database_candidate))
    except ValueError as exc:
        database = None
        _add(
            findings,
            "ERROR",
            "KNOWLEDGE_DATABASE_UNSAFE",
            "knowledge.sqlite 路径包含重解析点或越界",
            path=str(database_candidate),
            error=str(exc),
        )
    if database is not None:
        try:
            connection = _open_read_only_sqlite(database)
            _audit_sqlite(connection, findings)
            for table, label in (("papers", "papers"), ("passages", "passages"), ("evidence", "evidence")):
                try:
                    counts[label] = int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
                except sqlite3.Error as exc:
                    _add(findings, "ERROR", "TABLE_COUNT_UNAVAILABLE", "无法读取表计数", table=table, error=str(exc))
            length_distribution, passage_anomaly_counts = _audit_passages(
                connection,
                findings,
                short_passage_chars=short_passage_chars,
                extreme_passage_chars=extreme_passage_chars,
            )
            _audit_evidence(connection, findings)
        except (OSError, sqlite3.Error) as exc:
            _add(findings, "ERROR", "KNOWLEDGE_DATABASE_UNREADABLE", "无法以只读方式审计 knowledge.sqlite", path=str(database), error=str(exc))
        finally:
            if connection is not None:
                connection.close()

        try:
            store = KnowledgeStore(database, read_only=True)
        except (OSError, sqlite3.Error) as exc:
            _add(findings, "ERROR", "KNOWLEDGE_STORE_UNAVAILABLE", "KnowledgeStore 只读接口不可用", error=str(exc))

    cards_candidate = root / "cards"
    cards_root: Path | None
    try:
        cards_root = _safe_existing_directory(cards_candidate, project, "cards root")
    except FileNotFoundError:
        cards_root = cards_candidate
    except ValueError as exc:
        cards_root = None
        _add(
            findings,
            "ERROR",
            "CARD_ROOT_UNSAFE",
            "cards 路径包含重解析点或越界",
            path=str(cards_candidate),
            error=str(exc),
        )
    if cards_root is None:
        counts["cards"] = None
    else:
        counts["cards"] = _audit_cards(cards_root, root, store, findings)
    _add(findings, "INFO", "KNOWLEDGE_COUNTS", "知识库对象计数", **counts)
    card_index_candidate = root / "cards_fts.sqlite"
    try:
        card_index = _safe_existing_file(
            card_index_candidate, project, "cards_fts.sqlite"
        )
    except FileNotFoundError:
        card_index = card_index_candidate
    except ValueError as exc:
        card_index = None
        _add(
            findings,
            "ERROR",
            "CARD_INDEX_UNSAFE",
            "cards_fts.sqlite 路径包含重解析点或越界",
            path=str(card_index_candidate),
            error=str(exc),
        )
    if cards_root is not None and card_index is not None:
        _audit_card_index(cards_root, card_index, project, findings)
    if store is None:
        _add(findings, "ERROR", "VECTOR_INDEX_NOT_CHECKED", "知识库接口不可用，无法核验向量索引")
    else:
        vector_candidate = root / "passages.npz"
        try:
            vector_path = _safe_existing_file(
                vector_candidate, project, "passages.npz"
            )
        except FileNotFoundError:
            vector_path = vector_candidate
        except ValueError as exc:
            vector_path = None
            _add(
                findings,
                "ERROR",
                "VECTOR_INDEX_UNSAFE",
                "passages.npz 路径包含重解析点或越界",
                path=str(vector_candidate),
                error=str(exc),
            )
        try:
            if vector_path is None:
                vector = None
            else:
                vector = vector_index_status(store, vector_path)
            if vector is None:
                raise ValueError("vector index path is unsafe")
            severity = "INFO" if vector.get("ready") is True else "WARNING"
            _add(
                findings,
                severity,
                "VECTOR_INDEX_DIAGNOSTIC",
                "向量索引与当前 Passage 身份核验结果",
                reason=str(vector.get("reason", "unknown")),
                index_path=str(vector.get("index_path", vector_candidate)),
                metadata={key: value for key, value in vector.items() if key not in {"ready", "reason", "index_path"}},
            )
        except (OSError, RuntimeError, ValueError) as exc:
            if vector_path is None:
                pass
            else:
                _add(findings, "ERROR", "VECTOR_INDEX_CHECK_ERROR", "向量索引核验失败", error=str(exc))
        finally:
            store.close()

    _audit_lock(selected_lock, project, cards_root, findings)
    findings.sort(key=lambda item: (item.severity, item.code, json.dumps(item.details, ensure_ascii=False, sort_keys=True)))
    return {
        "schema_version": 1,
        "audit_kind": "independent_knowledge_base_maintenance_audit",
        "knowledge_root": str(root),
        "project_root": str(project),
        "lock_path": str(selected_lock),
        "thresholds": {
            "short_passage_chars_inclusive": short_passage_chars,
            "extreme_passage_chars_exclusive": extreme_passage_chars,
        },
        "counts": counts,
        "passage_length_distribution": length_distribution,
        "passage_anomaly_counts": passage_anomaly_counts,
        "findings": [asdict(item) for item in findings],
        "limitations": [
            "该输出是派生维护诊断，不是启动门、知识库就绪结论或科研质量评分。",
            "审计只读，不会自动修复、重建或发布任何知识库资产。",
        ],
    }


def _audit_sqlite(connection: sqlite3.Connection, findings: list[AuditFinding]) -> None:
    integrity = [str(row[0]) for row in connection.execute("PRAGMA integrity_check").fetchall()]
    if integrity == ["ok"]:
        _add(findings, "INFO", "SQLITE_INTEGRITY_CHECK", "SQLite integrity_check 返回 ok")
    else:
        for result in integrity:
            _add(findings, "ERROR", "SQLITE_INTEGRITY_ERROR", "SQLite integrity_check 报告异常", result=result)
    foreign_keys = connection.execute("PRAGMA foreign_key_check").fetchall()
    if not foreign_keys:
        _add(findings, "INFO", "SQLITE_FOREIGN_KEY_CHECK", "SQLite foreign_key_check 未发现异常")
    for table, rowid, parent, foreign_key_index in foreign_keys:
        _add(
            findings,
            "ERROR",
            "SQLITE_FOREIGN_KEY_ERROR",
            "SQLite foreign_key_check 报告悬空引用",
            table=str(table),
            rowid=rowid,
            parent=str(parent),
            foreign_key_index=int(foreign_key_index),
        )


def _audit_passages(
    connection: sqlite3.Connection,
    findings: list[AuditFinding],
    *,
    short_passage_chars: int,
    extreme_passage_chars: int,
) -> tuple[dict[str, int | float | None], dict[str, int]]:
    rows = connection.execute(
        "SELECT paper_id, passage_id, page_start, page_end, char_start, char_end, text, text_sha256 "
        "FROM passages ORDER BY paper_id, passage_id"
    ).fetchall()
    lengths = sorted(len(str(row[6])) for row in rows)
    distribution: dict[str, int | float | None] = {
        "minimum": lengths[0] if lengths else None,
        "p25": _percentile(lengths, 0.25),
        "median": _percentile(lengths, 0.50),
        "p75": _percentile(lengths, 0.75),
        "p90": _percentile(lengths, 0.90),
        "p95": _percentile(lengths, 0.95),
        "p99": _percentile(lengths, 0.99),
        "maximum": lengths[-1] if lengths else None,
    }
    _add(findings, "INFO", "PASSAGE_LENGTH_DISTRIBUTION", "Passage 字符长度分布", **distribution)
    anomaly_counts = {
        "blank": 0,
        "very_short": 0,
        "extreme_long": 0,
        "duplicate_groups_within_paper": 0,
        "duplicate_passages_within_paper": 0,
        "coordinate_length_mismatch": 0,
        "text_hash_mismatch": 0,
    }
    duplicates: dict[tuple[str, str], list[tuple[str, int, int]]] = defaultdict(list)
    for paper_id, passage_id, page_start, page_end, char_start, char_end, text, recorded_sha in rows:
        value = str(text)
        locator = {
            "paper_id": str(paper_id),
            "passage_id": str(passage_id),
            "length": len(value),
            "page_start": int(page_start),
            "page_end": int(page_end),
        }
        if not value.strip():
            anomaly_counts["blank"] += 1
            _add(findings, "ERROR", "PASSAGE_BLANK", "Passage 为空白文本", **locator)
        elif len(value) <= short_passage_chars:
            anomaly_counts["very_short"] += 1
            _add(findings, "WARNING", "PASSAGE_VERY_SHORT", "Passage 极短", **locator)
        if len(value) > extreme_passage_chars:
            anomaly_counts["extreme_long"] += 1
            _add(findings, "WARNING", "PASSAGE_EXTREME_LONG", "Passage 长度超过维护审计阈值", **locator)
        if int(char_end) - int(char_start) != len(value):
            anomaly_counts["coordinate_length_mismatch"] += 1
            _add(
                findings,
                "WARNING",
                "PASSAGE_COORDINATE_LENGTH_MISMATCH",
                "Passage 字符坐标跨度与文本长度不一致",
                **locator,
                char_start=int(char_start),
                char_end=int(char_end),
            )
        actual_sha = hashlib.sha256(value.encode("utf-8")).hexdigest()
        if actual_sha != str(recorded_sha):
            anomaly_counts["text_hash_mismatch"] += 1
            _add(findings, "ERROR", "PASSAGE_TEXT_HASH_MISMATCH", "Passage 文本 SHA-256 不一致", **locator, recorded_sha256=str(recorded_sha), actual_sha256=actual_sha)
        duplicates[(str(paper_id), value)].append((str(passage_id), int(page_start), int(page_end)))
    for (paper_id, text), items in duplicates.items():
        if len(items) < 2:
            continue
        anomaly_counts["duplicate_groups_within_paper"] += 1
        anomaly_counts["duplicate_passages_within_paper"] += len(items)
        _add(
            findings,
            "WARNING",
            "PASSAGE_DUPLICATE_WITHIN_PAPER",
            "同一 Paper 内存在完全相同的 Passage 文本",
            paper_id=paper_id,
            length=len(text),
            passages=[
                {"passage_id": passage_id, "page_start": page_start, "page_end": page_end}
                for passage_id, page_start, page_end in items
            ],
        )
    return distribution, anomaly_counts


def _audit_evidence(connection: sqlite3.Connection, findings: list[AuditFinding]) -> None:
    rows = connection.execute(
        """
        SELECT e.evidence_id, e.paper_id, e.fulltext_sha256, e.source_content,
               e.source_content_sha256, e.passage_id, e.passage_text_sha256,
               e.quote_start, e.quote_end,
               p.paper_id, p.fulltext_sha256,
               g.paper_id, g.text, g.text_sha256
        FROM evidence AS e
        LEFT JOIN papers AS p ON p.paper_id = e.paper_id
        LEFT JOIN passages AS g ON g.passage_id = e.passage_id
        ORDER BY e.evidence_id
        """
    ).fetchall()
    for row in rows:
        evidence_id = str(row[0])
        paper_id = str(row[1])
        base = {"evidence_id": evidence_id, "paper_id": paper_id, "passage_id": row[5]}
        if row[9] is None:
            _add(findings, "ERROR", "EVIDENCE_PAPER_MISSING", "Evidence 引用的 Paper 不存在", **base)
        elif str(row[2]) != str(row[10]):
            _add(findings, "ERROR", "EVIDENCE_PAPER_STALE", "Evidence 的全文身份不是当前 Paper 身份", **base, evidence_fulltext_sha256=str(row[2]), current_fulltext_sha256=str(row[10]))
        source = str(row[3])
        actual_source_sha = hashlib.sha256(source.encode("utf-8")).hexdigest()
        if actual_source_sha != str(row[4]):
            _add(findings, "ERROR", "EVIDENCE_SOURCE_HASH_MISMATCH", "Evidence source_content SHA-256 不一致", **base, recorded_sha256=str(row[4]), actual_sha256=actual_source_sha)
        if row[5] is None:
            continue
        if row[11] is None:
            _add(findings, "ERROR", "EVIDENCE_PASSAGE_MISSING", "Evidence 引用的 Passage 不存在", **base)
            continue
        if str(row[11]) != paper_id:
            _add(findings, "ERROR", "EVIDENCE_PASSAGE_WRONG_PAPER", "Evidence Passage 属于另一 Paper", **base, current_passage_paper_id=str(row[11]))
        passage_text = str(row[12])
        if str(row[6]) != str(row[13]):
            _add(findings, "ERROR", "EVIDENCE_PASSAGE_STALE", "Evidence 的 Passage 文本身份已过期", **base, evidence_passage_sha256=str(row[6]), current_passage_sha256=str(row[13]))
        start, end = row[7], row[8]
        if not isinstance(start, int) or not isinstance(end, int) or not (0 <= start <= end <= len(passage_text)):
            _add(findings, "ERROR", "EVIDENCE_QUOTE_RANGE_INVALID", "Evidence 引用范围无效", **base, quote_start=start, quote_end=end, passage_length=len(passage_text))
        elif passage_text[start:end] != source:
            _add(findings, "ERROR", "EVIDENCE_QUOTE_MISMATCH", "Evidence 引文与当前 Passage 切片不一致", **base, quote_start=start, quote_end=end)


def _audit_cards(cards_root: Path, knowledge_root: Path, store: KnowledgeStore | None, findings: list[AuditFinding]) -> int:
    paths: list[Path] = []
    for kind in _CARD_KINDS:
        kind_candidate = cards_root / kind
        try:
            kind_root = _safe_existing_directory(
                kind_candidate, knowledge_root, f"Card directory {kind}"
            )
        except FileNotFoundError:
            continue
        except ValueError as exc:
            _add(
                findings,
                "ERROR",
                "CARD_DIRECTORY_UNSAFE",
                "Card 类型目录包含重解析点或越界",
                path=str(kind_candidate),
                error=str(exc),
            )
            continue
        for candidate in sorted(kind_root.glob("*.md"), key=lambda item: item.name):
            try:
                paths.append(
                    _safe_existing_file(candidate, knowledge_root, "Card Markdown")
                )
            except (FileNotFoundError, ValueError) as exc:
                _add(
                    findings,
                    "ERROR",
                    "CARD_PATH_UNSAFE",
                    "Card Markdown 路径不存在、包含重解析点或越界",
                    path=str(candidate),
                    error=str(exc),
                )
    paths.sort(key=lambda path: path.relative_to(cards_root).as_posix())
    seen: dict[str, str] = {}
    valid_count = 0
    for path in paths:
        relative = path.relative_to(cards_root).as_posix()
        try:
            card = parse_card(path)
        except (OSError, ValueError) as exc:
            _add(findings, "ERROR", "CARD_PARSE_ERROR", "Card 无法解析", path=relative, error=str(exc))
            continue
        prior = seen.get(card.metadata.card_id)
        if prior is not None:
            _add(findings, "ERROR", "CARD_DUPLICATE_ID", "Card ID 重复", card_id=card.metadata.card_id, paths=[prior, relative])
        else:
            seen[card.metadata.card_id] = relative
        if store is None:
            _add(findings, "ERROR", "CARD_VALIDATION_NOT_RUN", "知识库接口不可用，无法完整验证 Card", path=relative)
            continue
        try:
            for source_ref in card.metadata.source_refs:
                _project_relative_file(knowledge_root, source_ref.path)
            validate_card(card, store=store, project_root=knowledge_root)
        except (FileNotFoundError, OSError, sqlite3.Error, ValueError) as exc:
            _add(findings, "ERROR", "CARD_VALIDATION_ERROR", "Card 验证失败", path=relative, card_id=card.metadata.card_id, error=str(exc))
            continue
        valid_count += 1
    _add(findings, "INFO", "CARD_COUNTS", "Card 全量解析与验证计数", discovered=len(paths), valid=valid_count)
    return len(paths)


def _audit_card_index(
    cards_root: Path,
    index_path: Path,
    project_root: Path,
    findings: list[AuditFinding],
) -> None:
    try:
        source_signature = _card_source_signature(
            cards_root, project_root=project_root
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        _add(
            findings,
            "ERROR",
            "CARD_INDEX_SOURCE_UNSAFE",
            "无法安全计算 Card Markdown source signature",
            path=str(cards_root),
            error=str(exc),
        )
        return
    status = card_index_status(cards_root, index_path)
    severity = "INFO" if status.get("ready") is True else "WARNING"
    _add(
        findings,
        severity,
        "CARD_INDEX_DIAGNOSTIC",
        "Card FTS 索引与 Markdown source signature 核验结果",
        reason=str(status.get("reason", "unknown")),
        index_path=str(status.get("index_path", index_path)),
        cards=status.get("cards"),
        actual_source_signature=source_signature,
    )


def _audit_lock(
    lock_path: Path,
    project_root: Path,
    cards_root: Path | None,
    findings: list[AuditFinding],
) -> None:
    try:
        safe_lock = _safe_existing_file(lock_path, project_root, "retrieval lock")
    except FileNotFoundError:
        _add(findings, "WARNING", "RETRIEVAL_LOCK_MISSING", "生产检索锁不存在", path=str(lock_path))
        return
    except ValueError as exc:
        _add(
            findings,
            "ERROR",
            "RETRIEVAL_LOCK_UNSAFE",
            "生产检索锁路径包含重解析点或越界",
            path=str(lock_path),
            error=str(exc),
        )
        return
    try:
        document = _load_json_object(safe_lock)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        _add(findings, "ERROR", "RETRIEVAL_LOCK_INVALID", "生产检索锁无法解析", path=str(lock_path), error=str(exc))
        return
    snapshot = document.get("source_snapshot")
    if not isinstance(snapshot, dict):
        _add(findings, "ERROR", "RETRIEVAL_LOCK_SOURCE_SNAPSHOT_INVALID", "检索锁 source_snapshot 不是对象", path=str(lock_path))
        return
    for name, entry in sorted(snapshot.items()):
        if name == "card_source_signature":
            if cards_root is None:
                _add(
                    findings,
                    "ERROR",
                    "RETRIEVAL_LOCK_CARD_SIGNATURE_UNAVAILABLE",
                    "cards 路径不安全，无法核验检索锁 Card source signature",
                    source=name,
                )
                continue
            try:
                actual = _card_source_signature(
                    cards_root, project_root=project_root
                )
            except (FileNotFoundError, OSError, ValueError) as exc:
                _add(
                    findings,
                    "ERROR",
                    "RETRIEVAL_LOCK_CARD_SIGNATURE_UNAVAILABLE",
                    "无法安全核验检索锁 Card source signature",
                    source=name,
                    error=str(exc),
                )
                continue
            if not isinstance(entry, str) or entry != actual:
                _add(findings, "ERROR", "RETRIEVAL_LOCK_CARD_SIGNATURE_MISMATCH", "检索锁 Card source signature 与当前 Markdown 不一致", source=name, recorded_sha256=entry, actual_sha256=actual)
            else:
                _add(findings, "INFO", "RETRIEVAL_LOCK_CARD_SIGNATURE_MATCH", "检索锁 Card source signature 与当前 Markdown 一致", source=name, actual_sha256=actual)
            continue
        _audit_hash_reference(entry, project_root, findings, code_prefix="RETRIEVAL_LOCK_SOURCE", source=str(name))
    accepted = document.get("accepted_evidence")
    if isinstance(accepted, dict):
        for name, entry in sorted(accepted.items()):
            _audit_hash_reference(entry, project_root, findings, code_prefix="RETRIEVAL_LOCK_ACCEPTED_EVIDENCE", source=str(name))


def _audit_hash_reference(entry: object, project_root: Path, findings: list[AuditFinding], *, code_prefix: str, source: str) -> None:
    if not isinstance(entry, dict) or not isinstance(entry.get("path"), str) or not isinstance(entry.get("sha256"), str):
        _add(findings, "WARNING", f"{code_prefix}_UNLOCATABLE", "检索锁条目没有可定位的 path/SHA-256", source=source)
        return
    try:
        path = _project_relative_file(project_root, str(entry["path"]))
    except (FileNotFoundError, ValueError) as exc:
        _add(findings, "ERROR", f"{code_prefix}_MISSING", "检索锁引用路径不存在或不安全", source=source, path=entry["path"], error=str(exc))
        return
    actual = _file_sha256(path)
    if actual != entry["sha256"]:
        _add(findings, "ERROR", f"{code_prefix}_HASH_MISMATCH", "检索锁记录的字节身份与当前文件不一致", source=source, path=entry["path"], recorded_sha256=entry["sha256"], actual_sha256=actual)
    else:
        _add(findings, "INFO", f"{code_prefix}_HASH_MATCH", "检索锁记录的字节身份与当前文件一致", source=source, path=entry["path"], actual_sha256=actual)


def _open_read_only_sqlite(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True, timeout=5.0)
    connection.execute("PRAGMA query_only=ON")
    connection.execute("PRAGMA foreign_keys=ON")
    return connection


def _percentile(values: list[int], fraction: float) -> int | float | None:
    if not values:
        return None
    position = (len(values) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    if lower == upper:
        return values[lower]
    result = values[lower] + (values[upper] - values[lower]) * (position - lower)
    return int(result) if result.is_integer() else round(result, 3)


def _card_source_signature(
    cards_root: Path, *, project_root: Path | None = None
) -> str:
    if project_root is None:
        safe_cards_root = _existing_directory(cards_root, "cards_root")
        safety_root = safe_cards_root
    else:
        safety_root = project_root
        try:
            safe_cards_root = _safe_existing_directory(
                cards_root, safety_root, "cards_root"
            )
        except FileNotFoundError:
            _reject_reparse_chain(cards_root, safety_root)
            safe_cards_root = cards_root
    digest = hashlib.sha256()
    paths: list[Path] = []
    for kind in _CARD_KINDS:
        try:
            kind_root = _safe_existing_directory(
                safe_cards_root / kind,
                safety_root,
                f"Card directory {kind}",
            )
        except FileNotFoundError:
            continue
        for candidate in kind_root.glob("*.md"):
            paths.append(
                _safe_existing_file(candidate, safety_root, "Card Markdown")
            )
    for path in sorted(
        paths, key=lambda item: item.relative_to(safe_cards_root).as_posix()
    ):
        digest.update(path.relative_to(safe_cards_root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(_file_sha256(path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _load_json_object(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not allowed")
    document = json.loads(raw.decode("utf-8", errors="strict"))
    if not isinstance(document, dict):
        raise ValueError("JSON document must be an object")
    return document


def _project_relative_file(project_root: Path, value: str) -> Path:
    pure = PurePosixPath(value)
    if not value or "\\" in value or pure.is_absolute() or ".." in pure.parts or any(part in {"", "."} for part in pure.parts):
        raise ValueError(f"path must be a safe project-relative POSIX path: {value!r}")
    path = project_root.joinpath(*pure.parts)
    return _safe_existing_file(path, project_root, "project-relative file")


def _safe_existing_file(path: str | Path, root: Path, label: str) -> Path:
    lexical = Path(os.path.abspath(path))
    _require_within(lexical, root, label)
    _reject_reparse_chain(lexical, root)
    if not lexical.is_file():
        raise FileNotFoundError(lexical)
    resolved = lexical.resolve(strict=True)
    _require_within(resolved, root, label)
    return resolved


def _existing_directory(path: str | Path, label: str) -> Path:
    lexical = Path(os.path.abspath(path))
    if _is_reparse_point(lexical):
        raise ValueError(f"{label} must not be a reparse point: {lexical}")
    if not lexical.is_dir():
        raise FileNotFoundError(f"{label} is not an existing directory: {lexical}")
    return lexical.resolve(strict=True)


def _safe_existing_directory(
    path: str | Path, root: Path, label: str
) -> Path:
    lexical = Path(os.path.abspath(path))
    _require_within(lexical, root, label)
    _reject_reparse_chain(lexical, root)
    if not lexical.is_dir():
        raise FileNotFoundError(f"{label} is not an existing directory: {lexical}")
    resolved = lexical.resolve(strict=True)
    _require_within(resolved, root, label)
    return resolved


def _require_within(path: Path, root: Path, label: str) -> None:
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes project_root: {path}") from exc


def _reject_reparse_chain(path: Path, root: Path) -> None:
    relative = path.relative_to(root)
    current = root
    for part in relative.parts:
        current = current / part
        if (current.exists() or current.is_symlink()) and _is_reparse_point(current):
            raise ValueError(f"path uses a reparse point: {current}")


def _is_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = os.lstat(path).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _add(findings: list[AuditFinding], severity: str, code: str, message: str, **details: object) -> None:
    findings.append(AuditFinding(severity=severity, code=code, message=message, details=details))
