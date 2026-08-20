from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Mapping, Sequence
from urllib.error import HTTPError, URLError
from uuid import uuid4

from . import literature as literature_module
from .hypotheses import read_portfolio
from .literature import LiteratureRecord, LiteratureResponseError, NetworkResponseRecord
from .workspace import ResearchWorkspace, _sha256, _validate_utf8_lf


AUDIT_FILES = ("request.json", "candidates.json", "report.md")
ASSESSMENT_FILE = "assessment.md"
COLLISION_KINDS = (
    "DIRECT_EXACT",
    "EMPIRICAL_ABSORPTION",
    "CONSTRUCTIVE_COMPOSITE",
    "ANALOGICAL_REDUCTION",
    "PROBLEM_OCCUPIED_METHOD_OPEN",
    "METHOD_KILLED_PHENOMENON_SURVIVES",
)
_AUDIT_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,63}")
_CANDIDATE_ID = re.compile(r"prior-[0-9a-f]{16}")
_rename_directory = os.rename


@dataclass(frozen=True, slots=True)
class PriorAuditPublication:
    path: str
    assessment_path: str
    audit_id: str
    created_at_utc: str
    degraded: bool
    candidate_count: int
    files: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class PriorAuditSnapshot:
    path: Path
    request: dict[str, object]
    candidates: dict[str, object]
    assessment: str | None = None
    collision_kind: str | None = None
    assessment_warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PriorPdfDownload:
    candidate_id: str
    path: str
    sha256: str
    byte_count: int
    source_url_identity: str


def create_prior_audit(
    workspace: ResearchWorkspace,
    hypothesis_id: str,
    queries: Sequence[str],
    audit_id: str,
    *,
    seed_paper_id: str | None = None,
    per_source_limit: int = 20,
    expansion_limit: int = 100,
    expansion_pages: int = 3,
    timeout: float = 30.0,
    max_retries: int = 2,
    collision_kind: str | None = None,
    now: str | None = None,
) -> PriorAuditPublication:
    workspace.assert_run_writable()
    identifier = validate_audit_id(audit_id)
    normalized_queries = _queries(queries)
    # Backward-compatible Python API only. The CLI does not expose creation-time
    # classification; any supplied label initializes the separate assessment.
    normalized_collision_kind = _collision_kind(collision_kind)
    if per_source_limit <= 0 or expansion_limit <= 0 or expansion_pages <= 0:
        raise ValueError("prior audit limits must be positive")
    if timeout <= 0 or max_retries < 0 or max_retries > 10:
        raise ValueError("prior audit timeout/retry settings are invalid")

    destination = _audit_path(workspace, identifier)
    workspace.assert_write_target(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"AUDIT_ID already exists: {destination}")

    portfolio_document = read_portfolio(workspace, required=True)
    assert portfolio_document is not None
    matches = [
        item
        for item in portfolio_document.portfolio.hypotheses
        if item.hypothesis_id == hypothesis_id
    ]
    if not matches:
        raise KeyError(f"unknown hypothesis id: {hypothesis_id}")
    hypothesis = matches[0]
    created = now or _utc_now()
    _validate_utc(created)

    responses: list[NetworkResponseRecord] = []
    sourced = []
    attempts: list[dict[str, object]] = []
    api_key = os.environ.get("S2_API_KEY")
    for query_index, query in enumerate(normalized_queries, start=1):
        for source, search in (
            ("Semantic Scholar", literature_module.search_semantic_scholar_records),
            ("arXiv", literature_module.search_arxiv_records),
        ):
            try:
                if source == "Semantic Scholar":
                    found = search(
                        query,
                        per_source_limit,
                        response_log=responses,
                        timeout=timeout,
                        max_retries=max_retries,
                        api_key=api_key,
                    )
                else:
                    found = search(
                        query,
                        per_source_limit,
                        response_log=responses,
                        timeout=timeout,
                        max_retries=max_retries,
                    )
                sourced.extend(found)
                attempts.append(
                    {
                        "source": source,
                        "query_index": query_index,
                        "status": "ok",
                        "record_count": len(found),
                    }
                )
            except (
                HTTPError,
                URLError,
                TimeoutError,
                ConnectionError,
                LiteratureResponseError,
            ) as error:
                attempts.append(_failed_attempt(source, query_index, error))

    if seed_paper_id is not None:
        if not seed_paper_id.strip():
            raise ValueError("seed_paper_id must not be empty")
        for relation in ("citations", "references"):
            try:
                found = literature_module.expand_semantic_scholar_records(
                    seed_paper_id,
                    relation,
                    expansion_limit,
                    response_log=responses,
                    max_pages=expansion_pages,
                    timeout=timeout,
                    max_retries=max_retries,
                    api_key=api_key,
                )
                sourced.extend(found)
                attempts.append(
                    {
                        "source": "Semantic Scholar",
                        "relation": relation,
                        "status": "ok",
                        "record_count": len(found),
                    }
                )
            except (
                HTTPError,
                URLError,
                TimeoutError,
                ConnectionError,
                LiteratureResponseError,
            ) as error:
                attempts.append(
                    _failed_attempt("Semantic Scholar", None, error, relation=relation)
                )

    records = literature_module.merge_literature_records(sourced)
    degraded = any(item["status"] == "error" for item in attempts)
    candidate_document: dict[str, object] = {
        "schema_version": 1,
        "artifact_kind": "run_local_non_authoritative_prior_candidates",
        "audit_id": identifier,
        "created_at_utc": created,
        "degraded": degraded,
        "source_attempts": attempts,
        "candidates": [_record_mapping(item) for item in records],
    }
    candidate_bytes = _json_bytes(_redact_secret(candidate_document, api_key))
    report_bytes = _machine_report_bytes(identifier)
    assessment_bytes = _assessment_bytes(identifier, normalized_collision_kind)
    request_document: dict[str, object] = {
        "schema_version": 3,
        "artifact_kind": "run_local_non_authoritative_prior_audit",
        "audit_id": identifier,
        "created_at_utc": created,
        "run_id": workspace.workspace_path.name,
        "version": workspace.version,
        "hypothesis": {
            "hypothesis_id": hypothesis.hypothesis_id,
            "hypothesis_revision": hypothesis.revision,
            "portfolio_path": Path(portfolio_document.path)
            .relative_to(workspace.workspace_path)
            .as_posix(),
            "portfolio_sha256": portfolio_document.sha256,
        },
        "queries": [
            {"query_id": f"q{index:03d}", "text": query}
            for index, query in enumerate(normalized_queries, start=1)
        ],
        "sources": ["Semantic Scholar", "arXiv"],
        "seed_paper_id": seed_paper_id,
        "limits": {
            "per_source_per_query": per_source_limit,
            "expansion_total_per_relation": expansion_limit,
            "expansion_max_pages": expansion_pages,
            "timeout_seconds": timeout,
            "max_retries": max_retries,
        },
        "network_responses": [asdict(item) for item in responses],
        "degraded": degraded,
        "artifact_hashes": {
            "candidates_json_sha256": _sha256(candidate_bytes),
            "report_md_sha256": _sha256(report_bytes),
        },
    }
    request_bytes = _json_bytes(_redact_secret(request_document, api_key))
    files = {
        "request.json": request_bytes,
        "candidates.json": candidate_bytes,
        "report.md": report_bytes,
        ASSESSMENT_FILE: assessment_bytes,
    }
    _publish_snapshot(workspace, destination, files)
    return PriorAuditPublication(
        path=str(destination),
        assessment_path=str(destination / ASSESSMENT_FILE),
        audit_id=identifier,
        created_at_utc=created,
        degraded=degraded,
        candidate_count=len(records),
        files=tuple((name, _sha256(files[name])) for name in AUDIT_FILES),
    )


def load_prior_audit(
    workspace: ResearchWorkspace, audit_id: str
) -> PriorAuditSnapshot:
    identifier = validate_audit_id(audit_id)
    destination = _audit_path(workspace, identifier)
    workspace.assert_write_target(destination)
    if not destination.is_dir():
        raise FileNotFoundError(destination)
    allowed = set(AUDIT_FILES) | {ASSESSMENT_FILE, "downloads"}
    names = {path.name for path in destination.iterdir()}
    if not set(AUDIT_FILES).issubset(names) or names - allowed:
        raise ValueError("prior audit contains unexpected or missing artifacts")
    files = {
        name: workspace.assert_read_target(destination / name).read_bytes()
        for name in AUDIT_FILES
    }
    for name, data in files.items():
        _validate_utf8_lf(data, f"prior audit {name}")
        if not data:
            raise ValueError(f"empty prior audit artifact: {name}")
    request = _canonical_json(files["request.json"], "request.json")
    candidates = _canonical_json(files["candidates.json"], "candidates.json")
    if request.get("audit_id") != identifier or candidates.get("audit_id") != identifier:
        raise ValueError("prior audit identity mismatch")
    hashes = request.get("artifact_hashes")
    if not isinstance(hashes, dict):
        raise ValueError("prior audit artifact hashes are missing")
    if hashes.get("candidates_json_sha256") != _sha256(files["candidates.json"]):
        raise ValueError("prior audit candidates hash mismatch")
    if hashes.get("report_md_sha256") != _sha256(files["report.md"]):
        raise ValueError("prior audit report hash mismatch")
    request_schema = request.get("schema_version", 1)
    historical_collision = request.get("collision_kind")
    if historical_collision is not None:
        historical_collision = _collision_kind(historical_collision)
    if request_schema == 1:
        expected_reports = (
            _legacy_report_bytes(identifier),
            _report_bytes(identifier, historical_collision),
        )
    elif request_schema == 2:
        expected_reports = (_report_bytes(identifier, historical_collision),)
    elif request_schema == 3:
        if historical_collision is not None:
            raise ValueError("schema 3 prior audit stores interpretation outside request.json")
        expected_reports = (_machine_report_bytes(identifier),)
    else:
        raise ValueError(f"unsupported prior audit schema: {request_schema}")
    if files["report.md"] not in expected_reports:
        raise ValueError("prior audit report bytes are not canonical")
    assessment, assessment_collision, assessment_warnings, marker_present = (
        _load_assessment(
            workspace,
            destination,
            identifier,
            required=request_schema == 3,
        )
    )
    collision_kind = (
        assessment_collision if marker_present else historical_collision
    )
    return PriorAuditSnapshot(
        destination,
        request,
        candidates,
        assessment,
        collision_kind,
        assessment_warnings,
    )


def download_prior_candidate_pdf(
    workspace: ResearchWorkspace,
    audit_id: str,
    hypothesis_id: str,
    candidate_id: str,
    *,
    timeout: float = 60.0,
    max_bytes: int = 50 * 1024 * 1024,
) -> PriorPdfDownload:
    workspace.assert_run_writable()
    if _CANDIDATE_ID.fullmatch(candidate_id) is None:
        raise ValueError("invalid prior candidate ID")
    snapshot = load_prior_audit(workspace, audit_id)
    hypothesis = snapshot.request.get("hypothesis")
    if not isinstance(hypothesis, dict) or hypothesis.get("hypothesis_id") != hypothesis_id:
        raise ValueError("prior audit hypothesis identity mismatch")
    candidates = snapshot.candidates.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("prior audit candidates are invalid")
    matches = [
        item
        for item in candidates
        if isinstance(item, dict) and item.get("candidate_id") == candidate_id
    ]
    if len(matches) != 1:
        raise KeyError(f"unknown prior candidate id: {candidate_id}")
    urls = matches[0].get("pdf_urls")
    if not isinstance(urls, list) or not urls or not isinstance(urls[0], str):
        raise ValueError("selected candidate has no PDF URL")

    downloads = workspace.assert_write_target(snapshot.path / "downloads")
    created_directory = not downloads.exists()
    downloads.mkdir(exist_ok=True)
    workspace.assert_write_target(downloads)
    target = workspace.assert_write_target(downloads / f"{candidate_id}.pdf")
    try:
        downloaded = literature_module.download_pdf(
            urls[0], target, timeout=timeout, max_bytes=max_bytes
        )
    except BaseException:
        if created_directory and downloads.is_dir() and not any(downloads.iterdir()):
            downloads.rmdir()
        raise
    return PriorPdfDownload(
        candidate_id=candidate_id,
        path=str(downloaded.path),
        sha256=downloaded.sha256,
        byte_count=downloaded.byte_count,
        source_url_identity=literature_module.normalize_url_identity(urls[0]),
    )


def validate_audit_id(value: str) -> str:
    if not isinstance(value, str) or _AUDIT_ID.fullmatch(value) is None:
        raise ValueError(
            "AUDIT_ID must be 3-64 lowercase letters, digits, dot, underscore, or hyphen"
        )
    return value


def _failed_attempt(
    source: str,
    query_index: int | None,
    error: Exception,
    *,
    relation: str | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "source": source,
        "status": "error",
        "error_type": type(error).__name__,
    }
    if query_index is not None:
        result["query_index"] = query_index
    if relation is not None:
        result["relation"] = relation
    if isinstance(error, HTTPError):
        result["http_status"] = error.code
    return result


def _record_mapping(record: LiteratureRecord) -> dict[str, object]:
    provenance = [asdict(item) for item in record.provenance]
    query_provenance = []
    seen_queries: set[tuple[str, str]] = set()
    for item in record.provenance:
        key = (item.source, item.query)
        if key not in seen_queries:
            seen_queries.add(key)
            query_provenance.append({"source": item.source, "query": item.query})
    return {
        "candidate_id": record.candidate_id,
        "title": record.title,
        "authors": list(record.authors),
        "year": record.year,
        "venue": record.venue,
        "abstract": record.abstract,
        "urls": list(record.urls),
        "landing_page_urls": list(record.landing_page_urls),
        "pdf_urls": list(record.pdf_urls),
        "source_ids": [
            {"kind": kind, "value": value} for kind, value in record.source_ids
        ],
        "query_provenance": query_provenance,
        "source_rank": [
            {"source": item.source, "query": item.query, "rank": item.source_rank}
            for item in record.provenance
        ],
        "provenance": provenance,
    }


def _queries(values: Sequence[str]) -> tuple[str, ...]:
    queries = tuple(value.strip() for value in values if isinstance(value, str) and value.strip())
    if not queries:
        raise ValueError("prior audit requires at least one query")
    return queries


def _redact_secret(value: object, secret: str | None) -> object:
    if not secret:
        return value
    if isinstance(value, str):
        return value.replace(secret, "[REDACTED]")
    if isinstance(value, list):
        return [_redact_secret(item, secret) for item in value]
    if isinstance(value, tuple):
        return [_redact_secret(item, secret) for item in value]
    if isinstance(value, dict):
        return {str(key): _redact_secret(item, secret) for key, item in value.items()}
    return value


def _report_bytes(audit_id: str, collision_kind: str | None = None) -> bytes:
    collision = collision_kind or "未分类；由主研究者按证据填写或保持自由笔记"
    lines = [
        "# 最近先行人工审计框架",
        "",
        f"- 审计标识：`{audit_id}`",
        f"- 碰撞类型：`{collision}`",
        "- 本文件仅提供空白人工分类框架；工具没有生成科研结论。",
        "- `DIRECT_EXACT` 与公平实验得到的 `EMPIRICAL_ABSORPTION` 可具有直接杀伤力；其余类型只记录风险与剩余差异，不自动改变候选状态。",
        "",
        "## 潜在最近先行",
        "",
        "<!-- 由主研究者填写 -->",
        "",
        "## 可能组件重合",
        "",
        "<!-- 由主研究者填写 -->",
        "",
        "## 仍存贡献增量",
        "",
        "<!-- 可从问题/现象、计算、智能体特有约束、评价、经验发现、理论或系统能力记录 surviving delta -->",
        "",
        "## 只做背景",
        "",
        "<!-- 由主研究者填写 -->",
        "",
        "## 身份未解决",
        "",
        "<!-- 由主研究者填写 -->",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def _machine_report_bytes(audit_id: str) -> bytes:
    lines = [
        "# 最近先行检索事实快照",
        "",
        f"- 审计标识：`{audit_id}`",
        "- 本文件是 machine-owned immutable snapshot 的紧凑说明，请勿编辑。",
        "- 查询、来源、网络响应身份与 artifact hashes 见 `request.json`。",
        "- 合并候选及其 provenance 见 `candidates.json`。",
        "- nearest prior、collision、组件重合、surviving contribution delta 与区分实验属于主研究者解释，请在 `assessment.md` 中阅读和修订。",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def _assessment_bytes(audit_id: str, collision_kind: str | None = None) -> bytes:
    collision = collision_kind or "UNCLASSIFIED"
    lines = [
        "# 最近先行科研解释",
        "",
        "> 本文件属于主研究者解释，可在阅读候选、PDF、Evidence 和实验后继续修订；它不进入机器事实快照哈希。",
        "",
        f"- 审计标识：`{audit_id}`",
        f"- 碰撞类型：`{collision}`",
        "",
        "## 重大科研决策（仅在本先行实际参与关闭、方法核/论文方向杀伤或重大升级时填写）",
        "",
        "- KILLED：",
        "- SURVIVES：",
        "- WHY：",
        "",
        "<!-- 普通检索无需填写本区；重大决策的权威结构化记录仍写入 Hypothesis decision history。 -->",
        "",
        "## 真正的 nearest prior",
        "",
        "<!-- 由主研究者填写；引用 candidate / PDF / Evidence 身份。 -->",
        "",
        "## 实质组件重合",
        "",
        "<!-- 由主研究者填写。 -->",
        "",
        "## 仍存贡献增量",
        "",
        "<!-- 可从问题/现象、计算、智能体特有约束、评价、经验发现、理论或系统能力记录。 -->",
        "",
        "## 最危险替代解释",
        "",
        "<!-- 由主研究者填写。 -->",
        "",
        "## 最小区分实验",
        "",
        "<!-- 由主研究者填写。 -->",
        "",
        "## 方法死亡后仍存现象",
        "",
        "<!-- 由主研究者填写。 -->",
        "",
        "## 背景与身份未解决项",
        "",
        "<!-- 由主研究者填写。 -->",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


_ASSESSMENT_COLLISION = re.compile(
    r"(?m)^- 碰撞类型：`([^`\r\n]+)`[ \t]*$"
)


def assessment_collision_kind(text: str) -> str | None:
    """Return a valid researcher label without treating interpretation as a gate."""
    _, collision_kind, _ = parse_prior_assessment(text)
    return collision_kind


def parse_prior_assessment(
    text: str,
    *,
    audit_id: str | None = None,
) -> tuple[bool, str | None, tuple[str, ...]]:
    matches = _ASSESSMENT_COLLISION.findall(text)
    if not matches:
        return False, None, ("assessment collision marker is missing",)
    if len(matches) != 1:
        return False, None, ("assessment collision marker is ambiguous",)
    value = matches[0]
    if value == "UNCLASSIFIED":
        collision_kind = None
    elif value in COLLISION_KINDS:
        collision_kind = value
    else:
        return False, None, (f"assessment collision kind is unknown: {value}",)
    if audit_id is not None and f"- 审计标识：`{audit_id}`" not in text:
        return (
            False,
            None,
            ("assessment audit identity is missing or different",),
        )
    return True, collision_kind, ()


def _load_assessment(
    workspace: ResearchWorkspace,
    destination: Path,
    audit_id: str,
    *,
    required: bool = False,
) -> tuple[str | None, str | None, tuple[str, ...], bool]:
    path = destination / ASSESSMENT_FILE
    if not path.exists() and not path.is_symlink():
        warnings = ("assessment.md is missing",) if required else ()
        return None, None, warnings, False
    try:
        data = workspace.assert_read_target(path).read_bytes()
        _validate_utf8_lf(data, "prior audit assessment.md")
        text = data.decode("utf-8")
    except (OSError, UnicodeError, ValueError) as error:
        return None, None, (f"assessment is unreadable: {error}",), False
    marker_present, collision_kind, warnings = parse_prior_assessment(
        text, audit_id=audit_id
    )
    return text, collision_kind, warnings, marker_present


def _legacy_report_bytes(audit_id: str) -> bytes:
    lines = [
        "# 最近先行人工审计框架",
        "",
        f"- 审计标识：`{audit_id}`",
        "- 本文件仅提供空白人工分类框架；工具没有生成科研结论。",
        "",
        "## 潜在最近先行",
        "",
        "<!-- 由主研究者填写 -->",
        "",
        "## 可能组件重合",
        "",
        "<!-- 由主研究者填写 -->",
        "",
        "## 只做背景",
        "",
        "<!-- 由主研究者填写 -->",
        "",
        "## 身份未解决",
        "",
        "<!-- 由主研究者填写 -->",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def _collision_kind(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or value not in COLLISION_KINDS:
        raise ValueError(
            "collision_kind must be one of: " + ", ".join(COLLISION_KINDS)
        )
    return value


def _publish_snapshot(
    workspace: ResearchWorkspace,
    destination: Path,
    files: Mapping[str, bytes],
) -> None:
    parent = workspace.assert_write_target(destination.parent)
    parent.mkdir(parents=True, exist_ok=True)
    workspace.assert_write_target(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"AUDIT_ID already exists: {destination}")
    temporary = workspace.assert_write_target(
        parent / f".{destination.name}.{uuid4().hex}.tmp"
    )
    temporary.mkdir()
    try:
        for name in files:
            path = workspace.assert_write_target(temporary / name)
            with path.open("xb") as handle:
                handle.write(files[name])
                handle.flush()
                os.fsync(handle.fileno())
        workspace.assert_write_target(destination)
        _rename_directory(temporary, destination)
    finally:
        if temporary.is_dir():
            for path in temporary.iterdir():
                if path.is_file() and not path.is_symlink():
                    path.unlink()
            temporary.rmdir()


def _audit_path(workspace: ResearchWorkspace, audit_id: str) -> Path:
    return (
        workspace.workspace_path
        / f"hypotheses_{workspace.version}"
        / "priors"
        / audit_id
    )


def _json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def _canonical_json(data: bytes, label: str) -> dict[str, object]:
    try:
        value = json.loads(data)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid prior audit JSON: {label}") from error
    if not isinstance(value, dict) or _json_bytes(value) != data:
        raise ValueError(f"prior audit JSON is not canonical: {label}")
    return value


def _validate_utc(value: object) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("prior audit UTC must be ISO-8601 and end in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError("prior audit UTC is invalid") from error
    if parsed.utcoffset() != UTC.utcoffset(parsed):
        raise ValueError("prior audit timestamp must be UTC")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
