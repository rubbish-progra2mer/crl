from __future__ import annotations

import json
import math
import os
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from crl_v3.comparison import _build_payload, _load_closed_attempt, render_comparison_report
from crl_v3.experiment import INTEGRITY_EXECUTION_SCHEMAS, experiment_material_errors
from crl_v3.falsification import list_plans
from crl_v3.prior_audit import load_prior_audit
from crl_v3.workspace import ResearchWorkspace, _required_file, _sha256, safe_relative_path


SCHEMA_VERSION = 1
_META_PREFIX = "<!-- CRL_SEED_SUPPORT_META "
_META_SUFFIX = " -->"
_AUDIT_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,63}")
_ATTEMPT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")
_NUMBER = re.compile(
    r"(?<![A-Za-z0-9_./-])[-+]?(?:\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)(?:\s*%)?(?![A-Za-z0-9_./-])"
)
_META_FIELDS = {
    "schema_version",
    "hypothesis_ids",
    "claim_ids",
    "falsified_claim_dispositions",
    "metric_mappings",
}
_DISPOSITION_FIELDS = {"claim_id", "seed_text"}
_MAPPING_FIELDS = {
    "seed_text",
    "seed_value",
    "source_path",
    "json_pointer",
}
FINAL_MAPPING_ERROR_CODES = frozenset(
    {
        "seed_metric_mapping_text_missing",
        "seed_metric_mapping_source_missing",
        "seed_metric_mapping_pointer_missing",
        "seed_metric_mapping_text_value_mismatch",
        "seed_metric_mapping_value_mismatch",
    }
)
_FINAL_EVIDENCE_FINDING_CODES = FINAL_MAPPING_ERROR_CODES | {
    "seed_support_metadata_missing",
    "seed_support_metadata_ambiguous",
    "seed_support_metadata_invalid",
    "seed_metric_mapping_resolved",
    "seed_numeric_literals_unmapped",
}
_FINAL_EVIDENCE_MAX_METRIC_RECORDS = 64
_FINAL_EVIDENCE_MAX_FINDINGS = 64
_FINAL_EVIDENCE_MAX_TEXT_CHARS = 1024
_FINAL_EVIDENCE_MAX_LIST_ITEMS = 64


def audit_seed_support(
    workspace: ResearchWorkspace,
    supporting_attempt_ids: Iterable[str] = (),
    *,
    max_prior_age_days: float = 30.0,
    as_of_utc: str | None = None,
) -> dict[str, Any]:
    """Return advisory facts without making a novelty, sufficiency, or delivery decision."""

    if not math.isfinite(max_prior_age_days) or max_prior_age_days <= 0:
        raise ValueError("max_prior_age_days must be a positive finite number")
    as_of = _parse_utc(as_of_utc or _utc_now(), "as_of_utc")
    attempt_ids = tuple(_attempt_id(item) for item in supporting_attempt_ids)
    if len(attempt_ids) != len(set(attempt_ids)):
        raise ValueError("supporting attempt IDs must be unique")

    findings: list[dict[str, Any]] = []

    def add(
        kind: str,
        code: str,
        message: str,
        sources: Iterable[str] = (),
        **details: Any,
    ) -> None:
        item: dict[str, Any] = {
            "kind": kind,
            "code": code,
            "message": message,
            "sources": list(sources),
        }
        if details:
            item["details"] = details
        findings.append(item)

    seed_path = workspace.seed_path
    seed_content = ""
    seed_sha256: str | None = None
    try:
        seed = workspace.read_seed()
        seed_content = seed.content
        seed_sha256 = seed.sha256
        add("finding", "seed_snapshot", "已读取当前 Seed 的精确字节身份。", [_relative(workspace, seed_path)])
    except FileNotFoundError:
        add("missing", "seed_missing", "当前科学版本没有 Seed 文件。", [_relative(workspace, seed_path)])

    portfolio = workspace.read_hypotheses(required=False)
    hypotheses: dict[str, Any] = {}
    portfolio_sha256: str | None = None
    if portfolio is None:
        add(
            "missing",
            "portfolio_missing",
            "当前科学版本没有 hypothesis portfolio。",
            [f"hypotheses_{workspace.version}/portfolio.json"],
        )
    else:
        portfolio_sha256 = portfolio.sha256
        hypotheses = {
            item.hypothesis_id: item for item in portfolio.portfolio.hypotheses
        }
        add(
            "finding",
            "portfolio_snapshot",
            f"已读取 {len(hypotheses)} 个 hypothesis 的当前 portfolio 身份。",
            [f"hypotheses_{workspace.version}/portfolio.json"],
        )

    plans = list_plans(workspace)
    claims: dict[str, tuple[str, Any, str]] = {}
    for document in plans:
        path = _relative(workspace, Path(document.path))
        for claim in document.plan.claims:
            if claim.claim_id in claims:
                raise ValueError(f"claim_id appears in multiple plans: {claim.claim_id}")
            claims[claim.claim_id] = (document.plan.hypothesis_id, claim, path)

    metadata, seed_body = _seed_metadata(seed_content, add)
    declared_hypotheses = tuple(metadata.get("hypothesis_ids", ()))
    declared_claims = tuple(metadata.get("claim_ids", ()))
    dispositions = tuple(metadata.get("falsified_claim_dispositions", ()))
    mappings = tuple(metadata.get("metric_mappings", ()))

    if not declared_hypotheses:
        add("missing", "seed_hypothesis_references_missing", "Seed 没有显式 hypothesis 引用。", [_relative(workspace, seed_path)])
    for hypothesis_id in declared_hypotheses:
        if hypothesis_id not in hypotheses:
            add(
                "missing",
                "seed_hypothesis_reference_unknown",
                f"Seed 声明的 hypothesis 不存在：{hypothesis_id}。",
                [_relative(workspace, seed_path), f"hypotheses_{workspace.version}/portfolio.json"],
                hypothesis_id=hypothesis_id,
            )
        else:
            add(
                "finding",
                "seed_hypothesis_reference_resolved",
                f"Seed hypothesis 引用可解析：{hypothesis_id}。",
                [_relative(workspace, seed_path), f"hypotheses_{workspace.version}/portfolio.json"],
                hypothesis_id=hypothesis_id,
            )

    if not declared_claims:
        add("missing", "seed_claim_references_missing", "Seed 没有显式 Claim 引用。", [_relative(workspace, seed_path)])
    for claim_id in declared_claims:
        if claim_id not in claims:
            add(
                "missing",
                "seed_claim_reference_unknown",
                f"Seed 声明的 Claim 不存在：{claim_id}。",
                [_relative(workspace, seed_path)],
                claim_id=claim_id,
            )
        else:
            add(
                "finding",
                "seed_claim_reference_resolved",
                f"Seed Claim 引用可解析：{claim_id}。",
                [_relative(workspace, seed_path), claims[claim_id][2]],
                claim_id=claim_id,
            )

    prior_facts = _audit_priors(
        workspace,
        as_of,
        timedelta(days=max_prior_age_days),
        declared_hypotheses,
        hypotheses,
        portfolio_sha256,
        add,
    )
    attempt_facts, trusted_sources, independent_attempts = _audit_attempts(
        workspace,
        attempt_ids,
        hypotheses,
        claims,
        set(declared_hypotheses),
        set(declared_claims),
        add,
    )
    comparison_facts, comparison_sources = _audit_comparisons(workspace, add)
    trusted_sources.update(comparison_sources)

    if not attempt_ids:
        add("missing", "supporting_attempts_missing", "没有显式选择 supporting attempt。")
    if not independent_attempts:
        add(
            "missing",
            "independent_claim_validation_missing",
            "选中的有效 supporting attempt 中没有 independent_claim_validation 类型。",
            [item for fact in attempt_facts for item in fact.get("sources", [])],
        )
    else:
        add(
            "finding",
            "independent_claim_validation_present",
            "存在显式绑定为 independent_claim_validation 的有效 supporting attempt。",
            [f"experiment_{workspace.version}/attempts/{item}/spec.json" for item in independent_attempts],
            attempt_ids=independent_attempts,
        )

    _audit_falsified_claim_dispositions(
        claims, dispositions, seed_body, workspace, add
    )
    _audit_metric_mappings(
        mappings, seed_body, trusted_sources, workspace, add
    )

    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "seed_support_advisory",
        "advisory_only": True,
        "run_id": workspace.workspace_path.name,
        "version": workspace.version,
        "as_of_utc": as_of.isoformat().replace("+00:00", "Z"),
        "prior_age_policy_days": max_prior_age_days,
        "inputs": {
            "seed": {
                "path": _relative(workspace, seed_path),
                "sha256": seed_sha256,
            },
            "portfolio": {
                "path": f"hypotheses_{workspace.version}/portfolio.json",
                "sha256": portfolio_sha256,
            },
            "supporting_attempt_ids": list(attempt_ids),
        },
        "facts": {
            "declared_hypothesis_ids": list(declared_hypotheses),
            "declared_claim_ids": list(declared_claims),
            "prior_audits": prior_facts,
            "supporting_attempts": attempt_facts,
            "independent_claim_validation_attempt_ids": independent_attempts,
            "comparisons": comparison_facts,
        },
        "findings": findings,
        "mechanical_effects": {
            "makes_novelty_judgment": False,
            "makes_scientific_sufficiency_judgment": False,
            "makes_delivery_judgment": False,
            "changes_claim_or_hypothesis_state": False,
            "changes_reviewer_count_or_authority": False,
            "changes_review_hash_chain": False,
        },
    }
    return payload


def render_seed_support_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_seed_support_markdown(payload: Mapping[str, Any]) -> str:
    inputs = payload["inputs"]
    findings = payload["findings"]
    lines = [
        f"# Seed 支撑事实审计 {payload['version']}",
        "",
        "> ADVISORY_ONLY：仅陈列可核查的机械或显式事实；不判断新颖性、科学充分性或交付结论。",
        "",
        f"- Run：`{payload['run_id']}`",
        f"- 截止时间：`{payload['as_of_utc']}`",
        f"- Seed：`{inputs['seed']['path']}`；SHA-256：`{inputs['seed']['sha256'] or 'missing'}`",
        f"- Portfolio：`{inputs['portfolio']['path']}`；SHA-256：`{inputs['portfolio']['sha256'] or 'missing'}`",
        "- Supporting attempts：" + ("、".join(f"`{item}`" for item in inputs["supporting_attempt_ids"]) or "（无）"),
        "",
        "## 审计记录",
        "",
        "| 类别 | 代码 | 事实 | 来源 |",
        "|---|---|---|---|",
    ]
    for item in findings:
        sources = "<br>".join(f"`{_md(value)}`" for value in item["sources"]) or "—"
        lines.append(
            f"| `{item['kind']}` | `{item['code']}` | {_md(item['message'])} | {sources} |"
        )
    if not findings:
        lines.append("| `finding` | `no_records` | 没有审计记录。 | — |")
    lines.extend(
        [
            "",
            "## 可追踪事实",
            "",
            "```json",
            json.dumps(payload["facts"], ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "",
            "## 机械权限边界",
            "",
            "本材料不改变 Claim 或 hypothesis 状态，不改变三位 Reviewer、同字节哈希链或主研究者裁决权。",
            "",
        ]
    )
    return "\n".join(lines)


def publish_seed_support_audit(
    workspace: ResearchWorkspace, payload: Mapping[str, Any], audit_id: str
) -> dict[str, str]:
    identifier = str(audit_id).strip()
    if _AUDIT_ID.fullmatch(identifier) is None:
        raise ValueError("AUDIT_ID must be 3-64 lowercase safe characters")
    workspace.assert_run_writable()
    root = workspace.assert_write_target(
        workspace.workspace_path / f"audit_{workspace.version}"
    )
    root.mkdir(parents=True, exist_ok=True)
    workspace.assert_write_target(root)
    stem = f"seed_support_{identifier}"
    outputs = {
        "json": (root / f"{stem}.json", render_seed_support_json(payload).encode("utf-8")),
        "markdown": (root / f"{stem}.md", render_seed_support_markdown(payload).encode("utf-8")),
    }
    for path, _ in outputs.values():
        workspace.assert_write_target(path)
        if os.path.lexists(path):
            raise FileExistsError(f"seed support audit already exists: {path}")
    written: list[Path] = []
    try:
        for path, data in outputs.values():
            with path.open("xb") as handle:
                handle.write(data)
            written.append(path)
    except BaseException:
        for path in written:
            path.unlink(missing_ok=True)
        raise
    return {
        name: path.relative_to(workspace.workspace_path).as_posix()
        for name, (path, _) in outputs.items()
    }


def final_evidence_closure(
    workspace: ResearchWorkspace,
    supporting_attempt_ids: Iterable[str],
) -> dict[str, Any]:
    """Return deterministic, bounded final-review facts without judging sufficiency."""

    attempt_ids = tuple(_attempt_id(item) for item in supporting_attempt_ids)
    if not attempt_ids or len(attempt_ids) != len(set(attempt_ids)):
        raise ValueError("final evidence requires unique supporting attempt IDs")

    seed = workspace.read_seed()
    findings: list[dict[str, Any]] = []

    def add(
        kind: str,
        code: str,
        message: str,
        sources: Iterable[str] = (),
        **details: Any,
    ) -> None:
        findings.append(
            {
                "kind": kind,
                "code": code,
                "message": message,
                "sources": list(sources),
                **({"details": details} if details else {}),
            }
        )

    metadata, seed_body = _seed_metadata(seed.content, add)
    trusted_sources: dict[str, Any] = {}
    attempts: list[dict[str, Any]] = []
    for attempt_id in attempt_ids:
        try:
            attempt = _load_closed_attempt(workspace, attempt_id)
        except ValueError as error:
            raise ValueError(
                f"selected Formal attempt cannot provide integrity-bound Spec/metrics: "
                f"{attempt_id}: {error}"
            ) from error
        if attempt.metrics is None:
            raise ValueError(
                f"selected Formal attempt has no verified metrics snapshot: {attempt_id}"
            )
        metric_path = f"{attempt.source_prefix}/metrics.json"
        trusted_sources[metric_path] = attempt.metrics
        attempts.append(_compact_final_attempt(attempt))

    comparison_facts, comparison_sources = _audit_comparisons(workspace, add)
    trusted_sources.update(comparison_sources)
    _audit_metric_mappings(
        tuple(metadata.get("metric_mappings", ())),
        seed_body,
        trusted_sources,
        workspace,
        add,
    )

    evidence_findings = [
        item for item in findings if item["code"] in _FINAL_EVIDENCE_FINDING_CODES
    ]
    blocking = [
        item for item in evidence_findings if item["code"] in FINAL_MAPPING_ERROR_CODES
    ]
    ordered_findings = blocking + [
        item for item in evidence_findings if item["code"] not in FINAL_MAPPING_ERROR_CODES
    ]
    selected_attempts = set(attempt_ids)
    relevant_comparisons = [
        item
        for item in comparison_facts
        if selected_attempts
        & ({item["candidate_attempt_id"]} | set(item["baseline_attempt_ids"]))
    ]
    return {
        "schema_version": 1,
        "artifact_kind": "final_core_evidence_closure",
        "run_id": workspace.workspace_path.name,
        "version": workspace.version,
        "seed": {
            "path": _relative(workspace, workspace.seed_path),
            "sha256": seed.sha256,
        },
        "selected_supporting_attempt_ids": list(attempt_ids),
        "attempts": attempts,
        "related_comparisons": relevant_comparisons,
        "seed_evidence": {
            "explicit_metric_mapping_count": len(
                metadata.get("metric_mappings", ())
            ),
            "mapping_integrity_valid": not blocking,
            "mapping_integrity_error_count": len(blocking),
            "finding_count": len(evidence_findings),
            "findings": [
                _compact_final_finding(item)
                for item in ordered_findings[:_FINAL_EVIDENCE_MAX_FINDINGS]
            ],
            "omitted_finding_count": max(
                0, len(ordered_findings) - _FINAL_EVIDENCE_MAX_FINDINGS
            ),
        },
        "bounds": {
            "metric_records_per_attempt": _FINAL_EVIDENCE_MAX_METRIC_RECORDS,
            "finding_records": _FINAL_EVIDENCE_MAX_FINDINGS,
            "text_characters_per_field": _FINAL_EVIDENCE_MAX_TEXT_CHARS,
            "list_items_per_field": _FINAL_EVIDENCE_MAX_LIST_ITEMS,
            "raw_code_stdout_stderr_included": False,
        },
        "mechanical_effects": {
            "checks_explicit_mapping_truth": True,
            "requires_all_seed_numbers_mapped": False,
            "makes_scientific_sufficiency_judgment": False,
        },
    }


def final_evidence_mapping_errors(closure: Mapping[str, Any]) -> tuple[str, ...]:
    seed_evidence = closure.get("seed_evidence")
    if not isinstance(seed_evidence, Mapping):
        return ("final core evidence closure has no Seed evidence facts",)
    count = seed_evidence.get("mapping_integrity_error_count")
    if type(count) is not int or count < 0:
        return ("final core evidence closure has invalid mapping integrity facts",)
    if count == 0:
        return ()
    representatives = []
    for item in seed_evidence.get("findings", []):
        if isinstance(item, Mapping) and item.get("code") in FINAL_MAPPING_ERROR_CODES:
            representatives.append(str(item.get("code")))
    summary = ", ".join(representatives[:8]) or "unavailable"
    return (
        f"explicit Seed metric mapping failed mechanical validation "
        f"({count} finding(s); representative codes: {summary})",
    )


def _compact_final_attempt(attempt: Any) -> dict[str, Any]:
    spec = attempt.spec
    metrics = attempt.metrics
    records = metrics["records"]
    primary_metric = spec["primary_metric"]
    prioritized = [
        index for index, item in enumerate(records) if item["name"] == primary_metric
    ] + [
        index for index, item in enumerate(records) if item["name"] != primary_metric
    ]
    included_indexes = sorted(
        prioritized[:_FINAL_EVIDENCE_MAX_METRIC_RECORDS]
    )
    ground_truth = spec["independent_ground_truth"]
    return {
        "attempt_id": attempt.attempt_id,
        "execution_schema_version": attempt.execution["schema_version"],
        "execution_sha256": attempt.execution_sha256,
        "spec_path": f"{attempt.source_prefix}/spec.json",
        "spec_sha256": attempt.spec_sha256,
        "metrics_path": f"{attempt.source_prefix}/metrics.json",
        "metrics_sha256": attempt.metrics_sha256,
        "spec": {
            "experiment_id": spec["experiment_id"],
            "hypothesis_id": spec["hypothesis_id"],
            "claim_ids": _compact_final_list(spec["claim_ids"]),
            "purpose": spec["purpose"],
            "research_question": _compact_final_text(spec["research_question"]),
            "primary_metric": _compact_final_text(primary_metric),
            "secondary_metrics": _compact_final_list(spec["secondary_metrics"]),
            "sampling_unit": _compact_final_text(spec["sampling_unit"]),
            "dataset": _compact_final_text(spec["dataset"]),
            "model": _compact_final_text(spec["model"]),
            "provider": _compact_final_text(spec["provider"]),
            "revision": _compact_final_text(spec["revision"]),
            "independent_ground_truth": {
                "description": _compact_final_text(ground_truth["description"]),
                "external_evidence_ids": _compact_final_list(
                    ground_truth["external_evidence_ids"]
                ),
                "external_card_ids": _compact_final_list(
                    ground_truth["external_card_ids"]
                ),
                "external_literature_refs": _compact_final_list(
                    ground_truth["external_literature_refs"]
                ),
                "run_local_fact_refs": _compact_final_list(
                    ground_truth["run_local_fact_refs"]
                ),
            },
            "falsification_rule": _compact_final_text(
                spec["falsification_rule"]
            ),
        },
        "metrics": {
            "experiment_id": metrics["experiment_id"],
            "primary_metric_selection_priority": primary_metric,
            "record_count": len(records),
            "included_record_count": len(included_indexes),
            "omitted_record_count": len(records) - len(included_indexes),
            "records": [
                {
                    "source_index": index,
                    **{
                        name: _compact_final_text(value)
                        if isinstance(value, str)
                        else value
                        for name, value in records[index].items()
                    },
                }
                for index in included_indexes
            ],
            "resource_usage": metrics["resource_usage"],
            "errors": _compact_final_list(metrics["errors"]),
            "warnings": _compact_final_list(metrics["warnings"]),
        },
    }


def _compact_final_finding(item: Mapping[str, Any]) -> dict[str, Any]:
    details = dict(item.get("details", {}))
    numeric_literals = details.get("numeric_literals")
    if isinstance(numeric_literals, list):
        compact = _compact_final_list(numeric_literals)
        details["numeric_literals"] = compact["items"]
        details["numeric_literal_count"] = compact["total_count"]
        details["omitted_numeric_literal_count"] = compact["omitted_count"]
    return {
        "kind": item["kind"],
        "code": item["code"],
        "message": _compact_final_text(str(item["message"])),
        "sources": _compact_final_list(item.get("sources", [])),
        **({"details": details} if details else {}),
    }


def _compact_final_list(values: Iterable[Any]) -> dict[str, Any]:
    items = list(values)
    included = [
        _compact_final_text(item) if isinstance(item, str) else item
        for item in items[:_FINAL_EVIDENCE_MAX_LIST_ITEMS]
    ]
    return {
        "total_count": len(items),
        "items": included,
        "omitted_count": len(items) - len(included),
    }


def _compact_final_text(value: str) -> str:
    if len(value) <= _FINAL_EVIDENCE_MAX_TEXT_CHARS:
        return value
    digest = _sha256(value.encode("utf-8"))
    return (
        value[:_FINAL_EVIDENCE_MAX_TEXT_CHARS]
        + f"…[TRUNCATED original_chars={len(value)} sha256={digest}]"
    )


def _seed_metadata(
    content: str,
    add: Callable[..., None],
) -> tuple[dict[str, Any], str]:
    lines = content.splitlines(keepends=True)
    matches = [line for line in lines if line.startswith(_META_PREFIX) and line.rstrip("\n").endswith(_META_SUFFIX)]
    body = "".join(line for line in lines if line not in matches)
    if not matches:
        add("missing", "seed_support_metadata_missing", "Seed 没有 CRL_SEED_SUPPORT_META 显式事实映射。")
        return {}, body
    if len(matches) != 1:
        add("warning", "seed_support_metadata_ambiguous", "Seed 支撑元数据不是唯一的一行。")
        return {}, body
    raw = matches[0].rstrip("\n")[len(_META_PREFIX) : -len(_META_SUFFIX)]
    try:
        value = json.loads(raw)
        if not isinstance(value, dict) or set(value) != _META_FIELDS:
            raise ValueError("metadata fields do not match schema 1")
        if value["schema_version"] != 1:
            raise ValueError("unsupported metadata schema version")
        value["hypothesis_ids"] = _string_ids(value["hypothesis_ids"], "hypothesis_ids")
        value["claim_ids"] = _string_ids(value["claim_ids"], "claim_ids")
        dispositions = value["falsified_claim_dispositions"]
        if not isinstance(dispositions, list):
            raise ValueError("falsified_claim_dispositions must be an array")
        for item in dispositions:
            if not isinstance(item, dict) or set(item) != _DISPOSITION_FIELDS:
                raise ValueError("falsified claim disposition fields do not match schema 1")
            _required_text(item["claim_id"], "disposition claim_id")
            _required_text(item["seed_text"], "disposition seed_text")
        mappings = value["metric_mappings"]
        if not isinstance(mappings, list):
            raise ValueError("metric_mappings must be an array")
        for item in mappings:
            if not isinstance(item, dict) or set(item) != _MAPPING_FIELDS:
                raise ValueError("metric mapping fields do not match schema 1")
            _required_text(item["seed_text"], "mapping seed_text")
            _required_text(item["source_path"], "mapping source_path")
            _required_text(item["json_pointer"], "mapping json_pointer")
            if type(item["seed_value"]) not in {int, float} or not math.isfinite(item["seed_value"]):
                raise ValueError("mapping seed_value must be a finite number")
        return value, body
    except (json.JSONDecodeError, ValueError) as error:
        add("warning", "seed_support_metadata_invalid", f"Seed 支撑元数据不可核验：{error}。")
        return {}, body


def _audit_priors(
    workspace: ResearchWorkspace,
    as_of: datetime,
    max_age: timedelta,
    declared_hypotheses: tuple[str, ...],
    hypotheses: Mapping[str, Any],
    portfolio_sha256: str | None,
    add: Callable[..., None],
) -> list[dict[str, Any]]:
    root = workspace.workspace_path / f"hypotheses_{workspace.version}" / "priors"
    workspace.assert_write_target(root)
    if not root.exists():
        add("missing", "prior_audits_missing", "当前科学版本没有最近先行审计材料。", [_relative(workspace, root)])
        return []
    if not root.is_dir():
        raise ValueError(f"prior audit root is not a directory: {root}")
    facts: list[dict[str, Any]] = []
    bound_hypotheses: set[str] = set()
    for directory in sorted(root.iterdir(), key=lambda item: item.name):
        if not directory.is_dir():
            add("warning", "prior_audit_entry_unexpected", "最近先行目录含非目录条目。", [_relative(workspace, directory)])
            continue
        try:
            snapshot = load_prior_audit(workspace, directory.name)
            request = snapshot.request
            candidates = snapshot.candidates
            if request.get("run_id") != workspace.workspace_path.name or request.get("version") != workspace.version:
                raise ValueError("prior audit Run/version identity mismatch")
            hypothesis = request.get("hypothesis")
            if not isinstance(hypothesis, dict) or not isinstance(hypothesis.get("hypothesis_id"), str):
                raise ValueError("prior audit hypothesis binding is missing")
            hypothesis_id = hypothesis["hypothesis_id"]
            created = _parse_utc(request.get("created_at_utc"), "prior created_at_utc")
            queries = request.get("queries")
            if not isinstance(queries, list) or not queries or not all(
                isinstance(item, dict) and isinstance(item.get("text"), str) and item["text"].strip()
                for item in queries
            ):
                raise ValueError("prior audit queries are missing")
            candidate_items = candidates.get("candidates")
            if not isinstance(candidate_items, list):
                raise ValueError("prior candidate material is invalid")
            bound_hypotheses.add(hypothesis_id)
            age = as_of - created
            source = _relative(workspace, snapshot.path)
            fact = {
                "audit_id": directory.name,
                "path": source,
                "hypothesis_id": hypothesis_id,
                "created_at_utc": request["created_at_utc"],
                "age_days": age.total_seconds() / 86400,
                "queries": [item["text"] for item in queries],
                "candidate_count": len(candidate_items),
                "degraded": bool(request.get("degraded")),
            }
            facts.append(fact)
            add("finding", "prior_audit_material_present", f"最近先行审计 {directory.name} 含时间、查询和候选材料。", [source], audit_id=directory.name)
            if age < timedelta(0):
                add("warning", "prior_audit_future_timestamp", f"最近先行审计 {directory.name} 的时间晚于审计截止时间。", [f"{source}/request.json"])
            elif age > max_age:
                add("warning", "prior_audit_stale", f"最近先行审计 {directory.name} 超过显式时效窗口。", [f"{source}/request.json"], age_days=fact["age_days"])
            if not candidate_items:
                add("missing", "prior_candidates_missing", f"最近先行审计 {directory.name} 没有候选记录。", [f"{source}/candidates.json"])
            if request.get("degraded") is True:
                add("warning", "prior_audit_degraded", f"最近先行审计 {directory.name} 记录了来源降级。", [f"{source}/request.json"])
            current = hypotheses.get(hypothesis_id)
            if current is None:
                add("warning", "prior_hypothesis_not_current", f"最近先行审计 {directory.name} 绑定的 hypothesis 已不在当前 portfolio。", [f"{source}/request.json"])
            elif hypothesis.get("hypothesis_revision") != current.revision or hypothesis.get("portfolio_sha256") != portfolio_sha256:
                add("warning", "prior_hypothesis_snapshot_stale", f"最近先行审计 {directory.name} 的 hypothesis/portfolio 身份不是当前字节。", [f"{source}/request.json", f"hypotheses_{workspace.version}/portfolio.json"])
        except (FileNotFoundError, OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
            add("warning", "prior_audit_unreadable", f"最近先行审计 {directory.name} 不可核验：{error}。", [_relative(workspace, directory)])
    for hypothesis_id in declared_hypotheses:
        if hypothesis_id not in bound_hypotheses:
            add("missing", "prior_audit_for_hypothesis_missing", f"Seed hypothesis 没有对应最近先行审计：{hypothesis_id}。", [_relative(workspace, root)], hypothesis_id=hypothesis_id)
    return facts


def _audit_attempts(
    workspace: ResearchWorkspace,
    attempt_ids: tuple[str, ...],
    hypotheses: Mapping[str, Any],
    claims: Mapping[str, tuple[str, Any, str]],
    declared_hypotheses: set[str],
    declared_claims: set[str],
    add: Callable[..., None],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    facts: list[dict[str, Any]] = []
    sources: dict[str, Any] = {}
    independent: list[str] = []
    for attempt_id in attempt_ids:
        prefix = f"experiment_{workspace.version}/attempts/{attempt_id}"
        attempt_root = workspace.experiment_path / "attempts" / attempt_id
        errors = experiment_material_errors(workspace, (attempt_id,))
        if errors:
            kind = "missing" if not attempt_root.exists() else "warning"
            add(kind, "supporting_attempt_integrity_warning", f"supporting attempt {attempt_id} 的闭合事实不可核验。", [prefix], errors=list(errors))
            facts.append({"attempt_id": attempt_id, "sources": [prefix], "integrity_errors": list(errors)})
            continue
        execution_data = _required_file(attempt_root / "execution.json", within=workspace.workspace_path)
        execution = json.loads(execution_data.decode("utf-8"))
        schema = execution.get("schema_version")
        if schema not in INTEGRITY_EXECUTION_SCHEMAS:
            add("missing", "supporting_attempt_spec_missing", f"supporting attempt {attempt_id} 的旧 schema 没有 P11 可核验 Spec 绑定。", [f"{prefix}/execution.json"])
            add("missing", "supporting_attempt_claim_binding_missing", f"supporting attempt {attempt_id} 的旧 schema 没有 P11 可核验 Claim 绑定。", [f"{prefix}/execution.json"])
            add("missing", "supporting_attempt_metrics_missing", f"supporting attempt {attempt_id} 的旧 schema 没有 P11 可核验 metrics 绑定。", [f"{prefix}/execution.json"])
            facts.append({"attempt_id": attempt_id, "schema_version": schema, "execution_sha256": _sha256(execution_data), "sources": [f"{prefix}/execution.json"]})
            continue
        spec_data = _required_file(attempt_root / "spec.json", within=workspace.workspace_path)
        metrics_data = _required_file(attempt_root / "metrics.json", within=workspace.workspace_path)
        spec = json.loads(spec_data.decode("utf-8"))
        metrics = json.loads(metrics_data.decode("utf-8"))
        hypothesis_id = spec["hypothesis_id"]
        claim_ids = tuple(spec["claim_ids"])
        if hypothesis_id not in hypotheses:
            add("missing", "supporting_attempt_hypothesis_unknown", f"supporting attempt {attempt_id} 的 Spec hypothesis 不在当前 portfolio。", [f"{prefix}/spec.json"], hypothesis_id=hypothesis_id)
        if declared_hypotheses and hypothesis_id not in declared_hypotheses:
            add("warning", "supporting_attempt_hypothesis_not_declared", f"supporting attempt {attempt_id} 的 Spec hypothesis 未由 Seed 显式声明。", [f"{prefix}/spec.json", _relative(workspace, workspace.seed_path)], hypothesis_id=hypothesis_id)
        for claim_id in claim_ids:
            claim = claims.get(claim_id)
            if claim is None:
                add("missing", "supporting_attempt_claim_unknown", f"supporting attempt {attempt_id} 的 Spec Claim 不在当前 FalsificationPlan。", [f"{prefix}/spec.json"], claim_id=claim_id)
            elif claim[0] != hypothesis_id:
                add("warning", "supporting_attempt_claim_hypothesis_mismatch", f"supporting attempt {attempt_id} 的 Spec Claim 与 hypothesis 身份不一致。", [f"{prefix}/spec.json", claim[2]], claim_id=claim_id)
            if declared_claims and claim_id not in declared_claims:
                add("warning", "supporting_attempt_claim_not_declared", f"supporting attempt {attempt_id} 的 Spec Claim 未由 Seed 显式声明。", [f"{prefix}/spec.json", _relative(workspace, workspace.seed_path)], claim_id=claim_id)
        parity = spec.get("parity_dimensions", {})
        for name, item in parity.items():
            status = item.get("status") if isinstance(item, dict) else None
            if status == "different":
                add("warning", "attempt_spec_parity_different", f"supporting attempt {attempt_id} 的 Spec parity 维度 {name} 显式为 different。", [f"{prefix}/spec.json#/parity_dimensions/{name}"])
            elif status == "unknown":
                add("warning", "attempt_spec_parity_unknown", f"supporting attempt {attempt_id} 的 Spec parity 维度 {name} 显式为 unknown。", [f"{prefix}/spec.json#/parity_dimensions/{name}"])
        if spec.get("purpose") == "independent_claim_validation":
            independent.append(attempt_id)
        metric_path = f"{prefix}/metrics.json"
        sources[metric_path] = metrics
        facts.append(
            {
                "attempt_id": attempt_id,
                "schema_version": schema,
                "execution_sha256": _sha256(execution_data),
                "spec_sha256": _sha256(spec_data),
                "metrics_sha256": _sha256(metrics_data),
                "hypothesis_id": hypothesis_id,
                "claim_ids": list(claim_ids),
                "purpose": spec["purpose"],
                "metric_record_count": len(metrics["records"]),
                "sources": [f"{prefix}/execution.json", f"{prefix}/spec.json", metric_path],
            }
        )
        add("finding", "supporting_attempt_bound", f"supporting attempt {attempt_id} 绑定了可核验的 Spec、Claim 列表与 metrics 快照。", [f"{prefix}/execution.json", f"{prefix}/spec.json", metric_path])
    return facts, sources, independent


def _audit_comparisons(
    workspace: ResearchWorkspace, add: Callable[..., None]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = workspace.experiment_path / "comparisons"
    workspace.assert_write_target(root)
    if not root.exists():
        return [], {}
    if not root.is_dir():
        raise ValueError(f"comparison root is not a directory: {root}")
    facts: list[dict[str, Any]] = []
    sources: dict[str, Any] = {}
    for directory in sorted(root.iterdir(), key=lambda item: item.name):
        source = _relative(workspace, directory)
        try:
            workspace.assert_write_target(directory)
            names = {item.name for item in directory.iterdir()}
            if names != {"comparison.json", "report.md"}:
                raise ValueError("comparison artifacts are incomplete or unexpected")
            json_data = _required_file(directory / "comparison.json", within=workspace.workspace_path)
            report_data = _required_file(directory / "report.md", within=workspace.workspace_path)
            payload = json.loads(json_data.decode("utf-8"))
            if (
                not isinstance(payload, dict)
                or payload.get("schema_version") not in {1, 2}
                or payload.get("artifact_kind") != "attempt_fact_comparison"
                or payload.get("comparison_id") != directory.name
            ):
                raise ValueError("comparison identity mismatch")
            if payload.get("run_id") != workspace.workspace_path.name or payload.get("version") != workspace.version:
                raise ValueError("comparison Run/version identity mismatch")
            candidate = _load_closed_attempt(workspace, payload["candidate_attempt"]["attempt_id"])
            baselines = tuple(_load_closed_attempt(workspace, item["attempt_id"]) for item in payload["baseline_attempts"])
            expected = _build_payload(
                workspace,
                directory.name,
                candidate,
                baselines,
                schema_version=int(payload["schema_version"]),
            )
            if json.dumps(payload, ensure_ascii=False, sort_keys=True) != json.dumps(
                expected, ensure_ascii=False, sort_keys=True
            ):
                raise ValueError("comparison facts do not match current attempt sources")
            if report_data != render_comparison_report(payload).encode("utf-8"):
                raise ValueError("comparison report does not match comparison facts")
            mismatched = []
            unknown = []
            for ledger in payload["parity_ledgers"]:
                for item in ledger["dimensions"]:
                    target = {"baseline_attempt_id": ledger["baseline_attempt_id"], "dimension": item["dimension"]}
                    if item["status"] == "mismatched":
                        mismatched.append(target)
                    elif item["status"] == "unknown":
                        unknown.append(target)
            facts.append({"comparison_id": directory.name, "path": source, "candidate_attempt_id": candidate.attempt_id, "baseline_attempt_ids": [item.attempt_id for item in baselines], "mismatched": mismatched, "unknown": unknown})
            comparison_path = f"{source}/comparison.json"
            sources[comparison_path] = payload
            add("finding", "comparison_snapshot", f"comparison {directory.name} 与其 attempt 来源及 Markdown 报告一致。", [comparison_path, f"{source}/report.md"])
            if mismatched:
                add("warning", "baseline_parity_mismatched", f"comparison {directory.name} 含 baseline parity mismatch。", [comparison_path], dimensions=mismatched)
            if unknown:
                add("warning", "baseline_parity_unknown", f"comparison {directory.name} 含 baseline parity unknown。", [comparison_path], dimensions=unknown)
        except (FileNotFoundError, OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
            add("warning", "comparison_unreadable", f"comparison {directory.name} 不可核验：{error}。", [source])
    return facts, sources


def _audit_falsified_claim_dispositions(
    claims: Mapping[str, tuple[str, Any, str]],
    dispositions: tuple[Mapping[str, Any], ...],
    seed_body: str,
    workspace: ResearchWorkspace,
    add: Callable[..., None],
) -> None:
    by_claim = {item["claim_id"]: item for item in dispositions}
    if len(by_claim) != len(dispositions):
        add("warning", "falsified_claim_disposition_duplicate", "Seed 对同一 falsified Claim 声明了重复处置映射。")
    for claim_id, (_, claim, plan_path) in claims.items():
        if claim.status != "falsified":
            continue
        disposition = by_claim.get(claim_id)
        if disposition is None or disposition["seed_text"] not in seed_body or claim_id not in disposition["seed_text"]:
            add("missing", "falsified_claim_disposition_missing", f"已显式标为 falsified 的 Claim 没有可定位的 Seed 处置引用：{claim_id}。", [plan_path, _relative(workspace, workspace.seed_path)], claim_id=claim_id)
        else:
            add("finding", "falsified_claim_disposition_present", f"已定位 falsified Claim 的 Seed 处置引用：{claim_id}。", [plan_path, _relative(workspace, workspace.seed_path)], claim_id=claim_id, seed_text=disposition["seed_text"])


def _audit_metric_mappings(
    mappings: tuple[Mapping[str, Any], ...],
    seed_body: str,
    trusted_sources: Mapping[str, Any],
    workspace: ResearchWorkspace,
    add: Callable[..., None],
) -> None:
    mapped_spans: list[tuple[int, int]] = []
    for index, mapping in enumerate(mappings):
        source_path = safe_relative_path(mapping["source_path"]).as_posix()
        source = trusted_sources.get(source_path)
        locations = list(_occurrences(seed_body, mapping["seed_text"]))
        if not locations:
            add("missing", "seed_metric_mapping_text_missing", f"数字映射 {index} 的 seed_text 不在 Seed 正文中。", [_relative(workspace, workspace.seed_path)], mapping_index=index)
            continue
        if source is None:
            add("missing", "seed_metric_mapping_source_missing", f"数字映射 {index} 的来源不是已核验 metrics/comparison 快照。", [source_path], mapping_index=index, source_path=source_path, json_pointer=mapping["json_pointer"])
            continue
        try:
            actual = _json_pointer(source, mapping["json_pointer"])
        except (KeyError, IndexError, TypeError, ValueError) as error:
            add("missing", "seed_metric_mapping_pointer_missing", f"数字映射 {index} 的 JSON Pointer 不可解析：{error}。", [f"{source_path}#{mapping['json_pointer']}"], mapping_index=index, source_path=source_path, json_pointer=mapping["json_pointer"])
            continue
        expected = mapping["seed_value"]
        text_numbers = [_number_value(item.group()) for item in _NUMBER.finditer(mapping["seed_text"])]
        if not any(value == expected for value in text_numbers):
            add("warning", "seed_metric_mapping_text_value_mismatch", f"数字映射 {index} 的 seed_text 未包含 seed_value 的同值数字。", [_relative(workspace, workspace.seed_path)], mapping_index=index, seed_value=expected, source_path=source_path, json_pointer=mapping["json_pointer"])
            continue
        if type(actual) not in {int, float} or not math.isfinite(actual) or actual != expected:
            add("warning", "seed_metric_mapping_value_mismatch", f"数字映射 {index} 的 Seed 数值与来源事实不一致。", [f"{source_path}#{mapping['json_pointer']}"], mapping_index=index, seed_value=expected, source_value=actual, source_path=source_path, json_pointer=mapping["json_pointer"])
            continue
        mapped_spans.extend(locations)
        add("finding", "seed_metric_mapping_resolved", f"数字映射 {index} 可追踪到精确实验事实。", [_relative(workspace, workspace.seed_path), f"{source_path}#{mapping['json_pointer']}"], mapping_index=index, seed_value=expected, source_value=actual, source_path=source_path, json_pointer=mapping["json_pointer"])

    visible = _mask_nonprose(seed_body)
    unmapped = []
    for match in _NUMBER.finditer(visible):
        if any(start <= match.start() and match.end() <= end for start, end in mapped_spans):
            continue
        unmapped.append(match.group().strip())
    if unmapped:
        add("warning", "seed_numeric_literals_unmapped", "Seed 正文含未被成功显式映射的可见数字。", [_relative(workspace, workspace.seed_path)], numeric_literals=unmapped)


def _json_pointer(value: Any, pointer: str) -> Any:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("JSON Pointer must begin with /")
    current = value
    for raw in pointer.split("/")[1:]:
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not token.isdigit():
                raise ValueError("array pointer token must be a non-negative integer")
            current = current[int(token)]
        elif isinstance(current, dict):
            current = current[token]
        else:
            raise TypeError("pointer traverses a scalar")
    return current


def _mask_nonprose(value: str) -> str:
    def mask(match: re.Match[str]) -> str:
        return "".join("\n" if character == "\n" else " " for character in match.group())

    value = re.sub(r"```.*?```", mask, value, flags=re.DOTALL)
    value = re.sub(r"`[^`\n]*`", mask, value)
    value = re.sub(r"<!--.*?-->", mask, value, flags=re.DOTALL)
    return value


def _occurrences(text: str, needle: str) -> Iterable[tuple[int, int]]:
    start = 0
    while True:
        index = text.find(needle, start)
        if index < 0:
            return
        yield index, index + len(needle)
        start = index + len(needle)


def _number_value(value: str) -> int | float:
    text = value.strip().removesuffix("%").strip()
    number = float(text)
    return int(number) if number.is_integer() else number


def _string_ids(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    items = [_required_text(item, label) for item in value]
    if len(items) != len(set(items)):
        raise ValueError(f"{label} must not contain duplicates")
    return items


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\r" in value:
        raise ValueError(f"{label} must be non-empty text")
    return value


def _attempt_id(value: str) -> str:
    text = str(value).strip()
    if _ATTEMPT_ID.fullmatch(text) is None:
        raise ValueError(f"attempt ID must be one safe 1-80 character identifier: {value!r}")
    return text


def _parse_utc(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{label} must be ISO-8601 UTC ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError(f"{label} is invalid") from error
    if parsed.utcoffset() != UTC.utcoffset(parsed):
        raise ValueError(f"{label} must be UTC")
    return parsed


def _relative(workspace: ResearchWorkspace, path: Path) -> str:
    try:
        return path.relative_to(workspace.workspace_path).as_posix()
    except ValueError:
        return str(path)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")
