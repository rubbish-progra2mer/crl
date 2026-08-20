from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable
from uuid import uuid4

import numpy as np

from .decision import environment_secrets, redact_secrets, scan_secret_bytes
from .vector import DEFAULT_MODEL, DEFAULT_MODEL_REVISION, _encode
from .workspace import ResearchWorkspace, _is_reparse_point, _sha256


_TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".jsonl", ".py", ".ps1", ".sh",
    ".log", ".csv", ".tsv", ".toml", ".yaml", ".yml",
}
_SENSITIVE_FILE_NAME = re.compile(
    r"(?i)(?:^\.env(?:\..*)?$|^credentials?(?:\.(?:json|ini|yaml|yml|txt))?$|"
    r"^credential[_-]?store(?:\.(?:json|ini|yaml|yml|txt))?$|"
    r"^client[_-]?secret(?:\.(?:json|ini|yaml|yml|txt))?$|"
    r"^token[_-]?dump(?:\.(?:json|log|txt))?$|"
    r"^auth[_-]?cache(?:\.(?:json|log|txt))?$|"
    r"^session[_-]?cache(?:\.(?:json|log|txt))?$|"
    r"^id_rsa(?:\..*)?$|^id_ed25519(?:\..*)?$|\.pem$|\.key$|\.pfx$|\.p12$)"
)
_EXCLUDED_DIR_REASONS = {
    ".crl": "derived_recall_tree",
    ".git": "repository_metadata_tree",
    "__pycache__": "cache_tree",
    ".pytest_cache": "cache_tree",
    ".cache": "cache_tree",
    ".mypy_cache": "cache_tree",
    ".ruff_cache": "cache_tree",
    "build": "build_cache_tree",
    "dist": "build_cache_tree",
    "node_modules": "dependency_tree",
    ".venv": "generated_environment_tree",
    "venv": "generated_environment_tree",
    "env": "generated_environment_tree",
    "external": "third_party_tree",
    "vendor": "third_party_tree",
    "third_party": "third_party_tree",
    "site-packages": "dependency_tree",
    "ground_truth": "ground_truth_tree",
    "hidden_test": "hidden_test_tree",
    "hidden_tests": "hidden_test_tree",
    "reference_solution": "reference_solution_tree",
    "credentials": "credential_store_tree",
    "credential_store": "credential_store_tree",
    "token_dump": "credential_store_tree",
    "auth_cache": "credential_store_tree",
    "session_cache": "credential_store_tree",
    ".ssh": "credential_store_tree",
}
_RESEARCH_OWNED_DIR = re.compile(
    r"^(?:research_workspace|workbench_v\d{3,}|hypotheses_v\d{3,}|"
    r"implementation_v\d{3,}|experiment_v\d{3,}|review_v\d{3,}|"
    r"audit_v\d{3,})(?:/|$)"
)
_ROOT_RESEARCH_FILE = re.compile(
    r"^(?:RUN_(?:CHARTER|STATUS|LEDGER)\.md|(?:NO_DELIVERY(?:_v\d{3,})?|"
    r"DELIVERY(?:_v\d{3,})?|TERMINATED_BY_USER)\.md|(?:problem|research_map|"
    r"nearest_prior|candidate|evidence_packet|selection_context|memory|"
    r"hypothesis_portfolio|failure_attribution|seed|decision)_v\d{3,}\.md)$"
)
_RAW_SEARCH_RESULT = re.compile(
    r"^hypotheses_v\d{3,}/searches/[^/]+/result\.json$"
)
_DUPLICATE_REVIEW_PACKET = re.compile(
    r"^review_v\d{3,}/evaluations/[^/]+/packet\.md$"
)
_RAW_REVIEW_TELEMETRY = re.compile(
    r"^review_v\d{3,}/evaluations/[^/]+/(?:SCI|EMP|ADV)/"
    r"(?:events\.jsonl|raw_output\.json)$"
)
_MAX_FILE_BYTES = 10 * 1024 * 1024
_CHUNK_CHARS = 4000
_RECENT_CONTEXT_LIMIT = 6
_RECENT_CONTEXT_CHARS = 2400
_KEY_RESEARCH_DOCUMENT = re.compile(
    r"^(?:problem|research_map|nearest_prior|candidate|evidence_packet|"
    r"selection_context|memory|hypothesis_portfolio|failure_attribution|seed|"
    r"decision)_v\d{3,}\.md$"
)


def rebuild_recall(
    workspace: ResearchWorkspace, *, semantic: bool = False
) -> dict[str, object]:
    workspace.assert_run_writable()
    recall_root = workspace.assert_write_target(workspace.workspace_path / ".crl" / "recall")
    recall_root.mkdir(parents=True, exist_ok=True)
    index_path = workspace.assert_write_target(recall_root / "index.sqlite")
    manifest_path = workspace.assert_write_target(recall_root / "manifest.json")
    vector_path = workspace.assert_write_target(recall_root / "semantic_vectors.npz")
    removable_paths = [index_path, manifest_path]
    if semantic:
        removable_paths.append(vector_path)
    elif vector_path.exists() and not vector_path.is_file():
        raise ValueError(f"unsafe recall derivative path: {vector_path}")
    for path in removable_paths:
        if path.exists():
            if _is_reparse_point(path) or not path.is_file():
                raise ValueError(f"unsafe recall derivative path: {path}")
            path.unlink()

    indexed: list[dict[str, object]] = []
    excluded: list[dict[str, str]] = []
    chunks: list[tuple[str, int, int, str, str]] = []
    secrets = environment_secrets()
    source_paths, excluded_trees = _run_text_files(workspace.workspace_path)
    excluded.extend(excluded_trees)
    for path in source_paths:
        relative = path.relative_to(workspace.workspace_path).as_posix()
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        reason = _exclusion_reason(relative, path, data, secrets)
        if reason is not None:
            excluded.append({"path": relative, "reason": reason, "sha256": digest})
            continue
        text = data.decode("utf-8")
        file_chunks = list(_text_chunks(text))
        indexed.append(
            {
                "path": relative,
                "size_bytes": len(data),
                "mtime_ns": path.stat().st_mtime_ns,
                "sha256": digest,
                "chunk_count": len(file_chunks),
            }
        )
        chunks.extend(
            (relative, start, end, digest, chunk)
            for start, end, chunk in file_chunks
        )

    connection = sqlite3.connect(index_path)
    try:
        connection.execute(
            "CREATE VIRTUAL TABLE chunks USING fts5("
            "path UNINDEXED, line_start UNINDEXED, line_end UNINDEXED, "
            "source_sha256 UNINDEXED, text, tokenize='unicode61')"
        )
        connection.executemany(
            "INSERT INTO chunks(path,line_start,line_end,source_sha256,text) VALUES(?,?,?,?,?)",
            chunks,
        )
        connection.commit()
    finally:
        connection.close()

    semantic_status = "DEGRADED"
    semantic_reason = "not_requested"
    if semantic and chunks:
        try:
            embeddings = _encode(
                [item[4] for item in chunks],
                None,
                DEFAULT_MODEL,
                DEFAULT_MODEL_REVISION,
            )
            embeddings = _normalized(embeddings)
            temporary = recall_root / f".semantic.{uuid4().hex}.npz"
            np.savez_compressed(
                temporary,
                rowids=np.arange(1, len(chunks) + 1, dtype=np.int64),
                embeddings=embeddings,
                model_name=np.asarray(DEFAULT_MODEL),
                model_revision=np.asarray(DEFAULT_MODEL_REVISION),
                index_sha256=np.asarray(_file_sha256(index_path)),
            )
            os.replace(temporary, vector_path)
            semantic_status = "READY"
            semantic_reason = None
        except (ImportError, OSError, RuntimeError, ValueError) as error:
            semantic_reason = f"encoding_unavailable: {error}"
    elif not semantic and vector_path.is_file():
        semantic_status, semantic_reason = _semantic_artifact_compatibility(
            vector_path, index_path
        )

    manifest = {
        "schema_version": 2,
        "run_id": workspace.workspace_path.name,
        "contract_version": workspace.contract_version,
        "generated_at_utc": _utc_now(),
        "index_sha256": _file_sha256(index_path),
        "indexed_file_count": len(indexed),
        "chunk_count": len(chunks),
        "indexed_files": indexed,
        "excluded_files": excluded,
        "indexed_bytes": sum(int(item["size_bytes"]) for item in indexed),
        "semantic_status": semantic_status,
        "semantic_reason": semantic_reason,
    }
    _atomic_json(manifest_path, manifest)
    return manifest


def search_recall(
    workspace: ResearchWorkspace, query: str, *, limit: int = 12
) -> dict[str, object]:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("recall query must not be empty")
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("recall limit must be between 1 and 100")
    recall_root = workspace.workspace_path / ".crl" / "recall"
    index_path = workspace.assert_read_target(recall_root / "index.sqlite")
    manifest_path = workspace.assert_read_target(recall_root / "manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("index_sha256") != _file_sha256(index_path):
        raise ValueError("recall index identity does not match manifest")

    fts_query = _fts_query(query)
    connection = sqlite3.connect(f"{index_path.resolve().as_uri()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            "SELECT rowid,path,line_start,line_end,source_sha256,text,bm25(chunks) AS score "
            "FROM chunks WHERE chunks MATCH ? ORDER BY score LIMIT ?",
            (fts_query, max(limit * 4, 40)),
        ).fetchall()
        fts_hits = [dict(row) for row in rows]
        semantic_hits, semantic_status, semantic_reason = _safe_semantic_hits(
            workspace,
            connection,
            recall_root / "semantic_vectors.npz",
            index_path,
            query,
            max(limit * 4, 40),
        )
    finally:
        connection.close()

    by_row: dict[int, dict[str, object]] = {}
    scores: defaultdict[int, float] = defaultdict(float)
    ranks: defaultdict[int, dict[str, int]] = defaultdict(dict)
    stale_sources: set[str] = set()
    fts_hits = [
        hit
        for hit in fts_hits
        if _hit_source_is_current(workspace, hit, stale_sources)
    ]
    semantic_hits = [
        hit
        for hit in semantic_hits
        if _hit_source_is_current(workspace, hit, stale_sources)
    ]
    for rank, hit in enumerate(fts_hits, start=1):
        rowid = int(hit["rowid"])
        by_row[rowid] = hit
        ranks[rowid]["fts"] = rank
        scores[rowid] += 1.0 / (60 + rank)
    for rank, hit in enumerate(semantic_hits, start=1):
        rowid = int(hit["rowid"])
        by_row.setdefault(rowid, hit)
        ranks[rowid]["semantic"] = rank
        scores[rowid] += 1.0 / (60 + rank)
    ordered = sorted(scores, key=lambda rowid: (-scores[rowid], rowid))[:limit]
    secrets = environment_secrets()
    hits = []
    for rowid in ordered:
        hit = by_row[rowid]
        text = redact_secrets(str(hit["text"]).encode("utf-8"), secrets).decode(
            "utf-8", errors="replace"
        )
        hits.append(
            {
                "path": hit["path"],
                "line_start": int(hit["line_start"]),
                "line_end": int(hit["line_end"]),
                "source_sha256": hit["source_sha256"],
                "text": text,
                "fts_rank": ranks[rowid].get("fts"),
                "semantic_rank": ranks[rowid].get("semantic"),
                "fused_score": scores[rowid],
            }
        )
    return {
        "query": query,
        "index_sha256": manifest["index_sha256"],
        "semantic_status": semantic_status,
        "semantic_reason": semantic_reason,
        "hits": hits,
        "stale_source_count": len(stale_sources),
        "stale_sources": sorted(stale_sources),
        "authority": "NON_AUTHORITATIVE_DERIVED_RECALL",
    }


def resume_recall(workspace: ResearchWorkspace, *, limit: int = 16) -> dict[str, object]:
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("recall limit must be between 1 and 100")
    queries = (
        "failure failed contradiction falsifier 失败 反证 矛盾",
        "implementation baseline experiment reviewer 实现 基线 实验 评审",
    )
    sections = []
    seen: set[tuple[str, int]] = set()
    semantic_states = []
    for query in queries:
        result = search_recall(workspace, query, limit=limit)
        semantic_states.append(
            {
                "status": result["semantic_status"],
                "reason": result["semantic_reason"],
            }
        )
        selected = []
        for hit in result["hits"]:
            identity = (str(hit["path"]), int(hit["line_start"]))
            if identity not in seen:
                seen.add(identity)
                selected.append(hit)
        sections.append(
            {
                "kind": "fixed_anchor",
                "query": query,
                "semantic_status": result["semantic_status"],
                "semantic_reason": result["semantic_reason"],
                "hits": selected,
            }
        )

    recent_files, context_query, indexed_mtimes = _recent_research_context(workspace)
    recovery_hits = []
    recovery_status = "DEGRADED"
    recovery_reason = "no_recent_key_research_context"
    if context_query:
        result = search_recall(
            workspace,
            context_query,
            limit=min(max(limit * 4, 40), 100),
        )
        recovery_status = str(result["semantic_status"])
        recovery_reason = result["semantic_reason"]
        semantic_states.append(
            {"status": recovery_status, "reason": recovery_reason}
        )
        source_paths = {str(item["path"]) for item in recent_files}
        newest_context_floor = min(int(item["mtime_ns"]) for item in recent_files)
        candidates = []
        recovery_seen: set[tuple[str, int]] = set()
        for order, hit in enumerate(result["hits"]):
            path = str(hit["path"])
            if path in source_paths:
                continue
            identity = (path, int(hit["line_start"]))
            if identity in recovery_seen:
                continue
            recovery_seen.add(identity)
            earlier = indexed_mtimes.get(path, newest_context_floor) < newest_context_floor
            item = dict(hit)
            item["earlier_than_recent_context"] = earlier
            candidates.append((not earlier, order, item))
        for _, _, hit in sorted(candidates)[:limit]:
            recovery_hits.append(hit)
    sections.append(
        {
            "kind": "recent_context_recovery",
            "query": context_query,
            "source_files": recent_files,
            "semantic_status": recovery_status,
            "semantic_reason": recovery_reason,
            "hits": recovery_hits,
        }
    )
    semantic_ready = any(item["status"] == "READY" for item in semantic_states)
    return {
        "authority": "ADVISORY_NON_AUTHORITATIVE",
        "run_id": workspace.workspace_path.name,
        "version": workspace.version,
        "semantic_status": "READY" if semantic_ready else "DEGRADED",
        "semantic_reason": None
        if semantic_ready
        else next(
            (
                item["reason"]
                for item in semantic_states
                if item["reason"] is not None
            ),
            recovery_reason,
        ),
        "sections": sections,
    }


def _recent_research_context(
    workspace: ResearchWorkspace,
) -> tuple[list[dict[str, object]], str | None, dict[str, int]]:
    recall_root = workspace.workspace_path / ".crl" / "recall"
    index_path = workspace.assert_read_target(recall_root / "index.sqlite")
    manifest_path = workspace.assert_read_target(recall_root / "manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("index_sha256") != _file_sha256(index_path):
        raise ValueError("recall index identity does not match manifest")
    indexed = manifest.get("indexed_files")
    if not isinstance(indexed, list):
        raise ValueError("recall manifest indexed_files is invalid")
    indexed_mtimes: dict[str, int] = {}
    candidates = []
    for item in indexed:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path", ""))
        mtime_ns = item.get("mtime_ns")
        if type(mtime_ns) is not int:
            continue
        if not _manifest_source_is_current(workspace, item):
            continue
        indexed_mtimes[path] = mtime_ns
        if _is_key_research_path(path, workspace.version):
            candidates.append((mtime_ns, path, str(item.get("sha256", ""))))
    selected = sorted(candidates, key=lambda item: (-item[0], item[1]))[
        :_RECENT_CONTEXT_LIMIT
    ]
    if not selected:
        return [], None, indexed_mtimes

    recent_files = [
        {"path": path, "mtime_ns": mtime_ns, "source_sha256": digest}
        for mtime_ns, path, digest in selected
    ]
    excerpts = []
    connection = sqlite3.connect(f"{index_path.resolve().as_uri()}?mode=ro", uri=True)
    try:
        for _, path, _ in selected:
            rows = connection.execute(
                "SELECT text FROM chunks WHERE path=? ORDER BY line_start LIMIT 2",
                (path,),
            ).fetchall()
            excerpt = _research_context_excerpt(
                "\n".join(str(row[0]) for row in rows)
            )
            if excerpt:
                excerpts.append(excerpt)
    finally:
        connection.close()
    query = "\n".join(excerpts).strip()[:_RECENT_CONTEXT_CHARS]
    return recent_files, query or None, indexed_mtimes


def _is_key_research_path(path: str, version: str) -> bool:
    pure = Path(path)
    if len(pure.parts) == 1 and _KEY_RESEARCH_DOCUMENT.fullmatch(pure.name):
        return pure.name.endswith(f"_{version}.md")
    return path in {
        f"hypotheses_{version}/portfolio.json",
        f"experiment_{version}/result.md",
    }


def _research_context_excerpt(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    selected = []
    for line in lines:
        if line.startswith("#") or re.search(
            r"(?i)problem|failure|mechanism|hypoth|candidate|claim|baseline|"
            r"experiment|evidence|contradict|uncertain|问题|失败|机制|假设|候选|"
            r"主张|基线|实验|证据|矛盾|不确定",
            line,
        ):
            selected.append(line)
        if len(selected) >= 12:
            break
    if not selected:
        selected = lines[:4]
    return "\n".join(selected)


def research_owned_run_files(root: Path) -> tuple[Path, ...]:
    """Return safe Run-local research files using Recall's traversal exclusions."""
    research, _, _ = inspection_run_files(root)
    return research


def inspection_run_files(
    root: Path,
) -> tuple[tuple[Path, ...], tuple[Path, ...], tuple[dict[str, object], ...]]:
    """Return research files and the wider safe set needed for secret inspection."""
    files, excluded = _walk_run_files(root)
    research = tuple(
        path
        for path in files
        if is_research_owned_path(path.relative_to(root).as_posix())
    )
    research_set = set(research)
    security = tuple(
        path
        for path in files
        if path in research_set or _SENSITIVE_FILE_NAME.search(path.name)
    )
    return research, security, tuple(excluded)


def is_research_owned_path(relative: str) -> bool:
    """Report whether a Run-relative POSIX path is owned by CRL research."""
    return bool(
        _ROOT_RESEARCH_FILE.fullmatch(relative)
        or _RESEARCH_OWNED_DIR.match(relative)
    )


def _run_text_files(root: Path) -> tuple[list[Path], list[dict[str, object]]]:
    files, excluded = _walk_run_files(root)
    sources = [
        path
        for path in files
        if path.suffix.casefold() in _TEXT_SUFFIXES
        or _SENSITIVE_FILE_NAME.search(path.name)
    ]
    return sources, excluded


def _walk_run_files(root: Path) -> tuple[list[Path], list[dict[str, object]]]:
    files_found: list[Path] = []
    excluded: list[dict[str, object]] = []
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        if current_path != root:
            git_marker = current_path / ".git"
            if _is_reparse_point(git_marker):
                raise ValueError(
                    f"Run recall refuses reparse-point repository marker: {git_marker}"
                )
            if git_marker.exists() or git_marker.is_symlink():
                relative = current_path.relative_to(root).as_posix().rstrip("/") + "/"
                excluded.append(
                    {
                        "path": relative,
                        "reason": "nested_repository_tree",
                        "sha256": None,
                    }
                )
                directories[:] = []
                continue
        kept = []
        for name in sorted(directories):
            path = current_path / name
            if _is_reparse_point(path):
                raise ValueError(f"Run recall refuses reparse-point directory: {path}")
            reason = _EXCLUDED_DIR_REASONS.get(name.casefold())
            relative_parts = path.relative_to(root).parts
            if (
                reason is None
                and name.casefold() == "diagnosis"
                and relative_parts
                and re.fullmatch(r"workbench_v\d{3,}", relative_parts[0])
            ):
                reason = "derived_diagnosis_tree"
            if reason is not None:
                relative = path.relative_to(root).as_posix().rstrip("/") + "/"
                excluded.append({"path": relative, "reason": reason, "sha256": None})
                continue
            kept.append(name)
        directories[:] = kept
        for name in sorted(files):
            path = current_path / name
            if _is_reparse_point(path):
                raise ValueError(f"Run recall refuses reparse-point file: {path}")
            files_found.append(path)
    return files_found, excluded


def _exclusion_reason(
    relative: str, path: Path, data: bytes, secrets: tuple[bytes, ...]
) -> str | None:
    if _SENSITIVE_FILE_NAME.search(path.name):
        return "sensitive_filename"
    if _RAW_SEARCH_RESULT.fullmatch(relative):
        return "raw_search_payload"
    if _DUPLICATE_REVIEW_PACKET.fullmatch(relative):
        return "duplicate_review_packet"
    if _RAW_REVIEW_TELEMETRY.fullmatch(relative):
        return "raw_reviewer_telemetry"
    if not is_research_owned_path(relative):
        return "not_research_owned"
    if len(data) > _MAX_FILE_BYTES:
        return "file_too_large"
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return "not_strict_utf8"
    scan = scan_secret_bytes(data, secrets)
    if scan.environment_secret:
        return "environment_secret_match"
    if scan.heuristic_pattern:
        return "credential_pattern_match"
    if relative.startswith(".crl/"):
        return "derived_recall_artifact"
    return None


def _hit_source_is_current(
    workspace: ResearchWorkspace,
    hit: dict[str, object],
    stale_sources: set[str],
) -> bool:
    path = str(hit.get("path", ""))
    digest = str(hit.get("source_sha256", ""))
    try:
        source = workspace.assert_read_target(workspace.workspace_path / Path(path))
        current = _file_sha256(source)
    except (FileNotFoundError, OSError, ValueError):
        stale_sources.add(path)
        return False
    if current != digest:
        stale_sources.add(path)
        return False
    return True


def _manifest_source_is_current(
    workspace: ResearchWorkspace, item: dict[str, object]
) -> bool:
    path = str(item.get("path", ""))
    digest = str(item.get("sha256", ""))
    try:
        source = workspace.assert_read_target(workspace.workspace_path / Path(path))
        return _file_sha256(source) == digest
    except (FileNotFoundError, OSError, ValueError):
        return False


def _text_chunks(text: str) -> Iterable[tuple[int, int, str]]:
    lines = text.splitlines()
    if not lines:
        return
    start = 0
    buffer: list[str] = []
    size = 0
    for index, line in enumerate(lines):
        addition = len(line) + 1
        if buffer and size + addition > _CHUNK_CHARS:
            yield start + 1, index, "\n".join(buffer)
            start = index
            buffer = []
            size = 0
        buffer.append(line)
        size += addition
    if buffer:
        yield start + 1, len(lines), "\n".join(buffer)


def _safe_semantic_hits(
    workspace: ResearchWorkspace,
    connection: sqlite3.Connection,
    vector_path: Path,
    index_path: Path,
    query: str,
    limit: int,
) -> tuple[list[dict[str, object]], str, str | None]:
    try:
        safe_vector_path = workspace.assert_read_target(vector_path)
    except FileNotFoundError:
        return [], "DEGRADED", "semantic_index_missing"
    except (OSError, ValueError):
        return [], "DEGRADED", "semantic_index_unsafe"
    return _semantic_hits(
        connection, safe_vector_path, index_path, query, limit
    )


def _semantic_hits(
    connection: sqlite3.Connection,
    vector_path: Path,
    index_path: Path,
    query: str,
    limit: int,
) -> tuple[list[dict[str, object]], str, str | None]:
    compatibility, reason = _semantic_artifact_compatibility(vector_path, index_path)
    if compatibility != "READY":
        return [], compatibility, reason
    try:
        with np.load(vector_path, allow_pickle=False) as data:
            rowids = np.asarray(data["rowids"], dtype=np.int64)
            embeddings = np.asarray(data["embeddings"], dtype=np.float32)
        query_vector = _normalized(
            _encode([query], None, DEFAULT_MODEL, DEFAULT_MODEL_REVISION)
        )[0]
        scores = embeddings @ query_vector
        order = np.argsort(-scores, kind="stable")[:limit]
        results = []
        for index in order:
            row = connection.execute(
                "SELECT rowid,path,line_start,line_end,source_sha256,text FROM chunks WHERE rowid=?",
                (int(rowids[index]),),
            ).fetchone()
            if row is not None:
                item = dict(row)
                item["semantic_score"] = float(scores[index])
                results.append(item)
        return results, "READY", None
    except (ImportError, OSError, RuntimeError, ValueError, KeyError) as error:
        return [], "DEGRADED", f"semantic_query_failed: {error}"


def _semantic_artifact_compatibility(
    vector_path: Path, index_path: Path
) -> tuple[str, str | None]:
    if not vector_path.is_file():
        return "DEGRADED", "semantic_index_missing"
    try:
        with np.load(vector_path, allow_pickle=False) as data:
            if str(data["index_sha256"].item()) != _file_sha256(index_path):
                return "DEGRADED", "semantic_index_stale"
            if "model_name" not in data.files or "model_revision" not in data.files:
                return "DEGRADED", "semantic_model_identity_missing"
            model_name = str(data["model_name"].item())
            model_revision = str(data["model_revision"].item())
        if (
            model_name != DEFAULT_MODEL
            or model_revision != DEFAULT_MODEL_REVISION
        ):
            return "DEGRADED", "semantic_model_identity_mismatch"
        return "READY", None
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        return "DEGRADED", f"semantic_index_invalid: {error}"


def _fts_query(value: str) -> str:
    tokens = re.findall(r"[^\W_]+", value, flags=re.UNICODE)
    if not tokens:
        raise ValueError("recall query has no searchable tokens")
    return " OR ".join('"' + token.replace('"', '""') + '"' for token in tokens)


def _normalized(values: np.ndarray) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms == 0) or not np.isfinite(matrix).all():
        raise ValueError("semantic encoder returned invalid vectors")
    return matrix / norms


def _atomic_json(path: Path, value: dict[str, object]) -> None:
    data = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    with temporary.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _file_sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
