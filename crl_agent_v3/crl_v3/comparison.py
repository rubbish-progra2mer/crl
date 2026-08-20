from __future__ import annotations

import json
import math
import os
import re
import shutil
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping
from uuid import uuid4

from crl_v3.experiment import formal_attempt_integrity_execution_sha256
from crl_v3.workspace import ResearchWorkspace, _required_file, _sha256


SCHEMA_VERSION = 2
SUPPORTED_SCHEMA_VERSIONS = frozenset({1, 2})
PARITY_STATUSES = ("matched", "mismatched", "unknown", "not_applicable")
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")
_Z_95 = 1.959963984540054

_DIMENSION_LABELS = {
    "task": "任务",
    "dataset": "数据集",
    "dataset_split": "数据划分",
    "dataset_revision": "数据集修订版",
    "model": "模型",
    "provider": "提供方",
    "model_revision": "模型修订版",
    "model_quantization": "模型量化",
    "prompt_identity": "提示词身份",
    "context": "上下文",
    "information_access": "信息访问",
    "tool_set": "工具集合",
    "tool_permissions": "工具权限",
    "search_budget": "搜索预算",
    "retry_budget": "重试预算",
    "call_budget": "调用预算",
    "token_budget": "令牌预算",
    "wall_budget": "墙钟时间预算",
    "gpu_budget": "图形处理器预算",
    "cost_budget": "费用预算",
    "seed": "随机种子",
    "replicate_count": "重复试验数",
    "evaluator": "评价器",
    "metric_definition": "指标定义",
    "sampling_unit": "抽样单位",
    "implementation_identity": "实现身份",
    "failure_rate": "失败率",
}


@dataclass(frozen=True, slots=True)
class ComparisonPublication:
    path: str
    comparison_id: str
    candidate_attempt_id: str
    baseline_attempt_ids: tuple[str, ...]
    files: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class _Attempt:
    attempt_id: str
    execution_sha256: str
    spec_sha256: str
    metrics_sha256: str | None
    execution: dict[str, Any]
    spec: dict[str, Any]
    metrics: dict[str, Any] | None
    metrics_unavailable_reasons: tuple[str, ...]
    source_prefix: str


def compare_attempts(
    workspace: ResearchWorkspace,
    comparison_id: str,
    candidate_attempt_id: str,
    baseline_attempt_ids: Iterable[str],
) -> ComparisonPublication:
    """Publish a fixed Run-local comparison of closed integrity-capable attempts."""

    workspace.assert_run_writable()
    identifier = _identifier(comparison_id, "comparison ID")
    candidate_id = _identifier(candidate_attempt_id, "candidate attempt ID")
    baseline_ids = tuple(
        _identifier(value, "baseline attempt ID") for value in baseline_attempt_ids
    )
    if not baseline_ids:
        raise ValueError("at least one baseline attempt ID is required")
    if len(set(baseline_ids)) != len(baseline_ids):
        raise ValueError("baseline attempt IDs must be unique")
    if candidate_id in baseline_ids:
        raise ValueError("candidate attempt must not also be a baseline attempt")

    candidate = _load_closed_attempt(workspace, candidate_id)
    baselines = tuple(_load_closed_attempt(workspace, item) for item in baseline_ids)
    payload = _build_payload(workspace, identifier, candidate, baselines)
    report = render_comparison_report(payload)
    json_data = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    report_data = report.encode("utf-8")

    root = workspace.assert_write_target(workspace.experiment_path / "comparisons")
    destination = workspace.assert_write_target(root / identifier)
    if os.path.lexists(destination):
        raise FileExistsError(f"comparison ID already exists: {destination}")
    root.mkdir(parents=True, exist_ok=True)
    workspace.assert_write_target(root)
    staging = workspace.assert_write_target(root / f".{identifier}.{uuid4().hex}.tmp")
    staging.mkdir()
    try:
        (staging / "comparison.json").write_bytes(json_data)
        (staging / "report.md").write_bytes(report_data)
        os.rename(staging, destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)

    return ComparisonPublication(
        path=str(destination),
        comparison_id=identifier,
        candidate_attempt_id=candidate_id,
        baseline_attempt_ids=baseline_ids,
        files=(
            ("comparison.json", _sha256(json_data)),
            ("report.md", _sha256(report_data)),
        ),
    )


def render_comparison_report(payload: Mapping[str, Any]) -> str:
    aggregation_in_identity = payload.get("schema_version") == 2
    lines = [
        f"# Attempt 事实比较：{payload['comparison_id']}",
        "",
        f"- Run：`{payload['run_id']}`",
        f"- 科学版本：`{payload['version']}`",
        f"- 候选 attempt：`{payload['candidate_attempt']['attempt_id']}`",
        "- 基线 attempts："
        + "、".join(
            f"`{item['attempt_id']}`" for item in payload["baseline_attempts"]
        ),
        "- 本报告仅陈列指标与可比性事实；不产生胜负、质量或可发表性结论。",
        "",
        "## 指标事实",
        "",
        (
            "| 基线 attempt | 指标（名称 / 单位 / split / aggregation） | 候选事实值 | "
            "基线事实值 | 候选减基线 | 候选/基线 | replicate 置信区间 |"
            if aggregation_in_identity
            else "| 基线 attempt | 指标（名称 / 单位 / split） | 候选事实值 | "
            "基线事实值 | 候选减基线 | 候选/基线 | replicate 置信区间 |"
        ),
        "|---|---|---:|---:|---:|---:|---|",
    ]
    missing: list[str] = []
    for summary in [payload["candidate_attempt"], *payload["baseline_attempts"]]:
        if summary["metrics_availability"] == "unavailable":
            reasons = "；".join(summary["metrics_unavailable_reasons"])
            missing.append(
                f"`{summary['attempt_id']}` 没有有效指标快照：{reasons}。"
            )
    for pair in payload["metric_facts"]:
        baseline_id = pair["baseline_attempt_id"]
        for fact in pair["comparisons"]:
            key = fact["metric_key"]
            label = f"{key['name']} / {key['unit']} / {key['split']}"
            if "aggregation" in key:
                label += f" / {key['aggregation']}"
            if fact["metric_presence"] != "both":
                missing.append(
                    f"`{baseline_id}` 的 `{label}` 仅见于 {fact['metric_presence']}。"
                )
            ci = fact.get("confidence_interval")
            ci_text = (
                f"[{_number(ci['lower'])}, {_number(ci['upper'])}]；{ci['method']}"
                if isinstance(ci, dict) and ci.get("lower") is not None
                else "未计算"
            )
            if ci is None and fact.get("confidence_interval_reason"):
                missing.append(
                    f"`{baseline_id}` 的 `{label}` 未计算置信区间："
                    f"{fact['confidence_interval_reason']}。"
                )
            lines.append(
                "| "
                + " | ".join(
                    (
                        _md(baseline_id),
                        _md(label),
                        _number(fact.get("candidate_fact_value")),
                        _number(fact.get("baseline_fact_value")),
                        _number(fact.get("difference_candidate_minus_baseline")),
                        _number(fact.get("ratio_candidate_over_baseline")),
                        _md(ci_text),
                    )
                )
                + " |"
            )
    if not any(item["comparisons"] for item in payload["metric_facts"]):
        lines.append("| — | — | — | — | — | — | — |")

    lines.extend(
        [
            "",
            "## Parity mismatch",
            "",
            "| 基线 attempt | 维度 | 候选原值与来源 | 基线原值与来源 |",
            "|---|---|---|---|",
        ]
    )
    mismatches = [
        (ledger["baseline_attempt_id"], item)
        for ledger in payload["parity_ledgers"]
        for item in ledger["dimensions"]
        if item["status"] == "mismatched"
    ]
    if mismatches:
        for baseline_id, item in mismatches:
            lines.append(
                f"| {_md(baseline_id)} | {_md(_DIMENSION_LABELS[item['dimension']])} "
                f"| {_md(_fact_text(item['candidate']))} | {_md(_fact_text(item['baseline']))} |"
            )
    else:
        lines.append("| — | 未记录到事实不匹配 | — | — |")

    for ledger in payload["parity_ledgers"]:
        for item in ledger["dimensions"]:
            if item["status"] == "unknown":
                missing.append(
                    f"`{ledger['baseline_attempt_id']}` 的"
                    f"“{_DIMENSION_LABELS[item['dimension']]}”信息不足。"
                )
    lines.extend(["", "## 缺失信息", ""])
    lines.extend(f"- {item}" for item in dict.fromkeys(missing))
    if not missing:
        lines.append("- 未记录到缺失信息。")

    lines.extend(["", "## 完整 Parity 台账", ""])
    for ledger in payload["parity_ledgers"]:
        lines.extend(
            [
                f"### 候选 vs `{ledger['baseline_attempt_id']}`",
                "",
                "| 维度 | 状态 | 候选原值与来源 | 基线原值与来源 |",
                "|---|---|---|---|",
            ]
        )
        for item in ledger["dimensions"]:
            lines.append(
                f"| {_md(_DIMENSION_LABELS[item['dimension']])} | `{item['status']}` "
                f"| {_md(_fact_text(item['candidate']))} | {_md(_fact_text(item['baseline']))} |"
            )

    lines.extend(
        [
            "",
            "## 人工解释（由主研究者填写）",
            "",
            "<!-- 请主研究者在此解释指标事实、Parity 不匹配、缺失信息及其科学含义。比较器不自动填写本区。 -->",
            "",
        ]
    )
    return "\n".join(lines)


def _load_closed_attempt(workspace: ResearchWorkspace, attempt_id: str) -> _Attempt:
    execution_sha256 = formal_attempt_integrity_execution_sha256(
        workspace, attempt_id
    )
    attempt = workspace.experiment_path / "attempts" / attempt_id
    execution = _json_object(
        _required_file(attempt / "execution.json", within=workspace.workspace_path),
        "execution.json",
    )
    spec_data = _required_file(
        attempt / "spec.json", within=workspace.workspace_path
    )
    spec = _json_object(spec_data, "spec.json")
    metrics_fact = execution["metrics"]
    if metrics_fact["snapshot"] is None:
        metrics_data = None
        metrics = None
        unavailable = tuple(metrics_fact["validation_errors"])
    else:
        metrics_data = _required_file(
            attempt / "metrics.json", within=workspace.workspace_path
        )
        metrics = _json_object(metrics_data, "metrics.json")
        unavailable = ()
    if (
        formal_attempt_integrity_execution_sha256(workspace, attempt_id)
        != execution_sha256
    ):
        raise ValueError(f"attempt changed while comparison facts were read: {attempt_id}")
    return _Attempt(
        attempt_id=attempt_id,
        execution_sha256=execution_sha256,
        spec_sha256=_sha256(spec_data),
        metrics_sha256=_sha256(metrics_data) if metrics_data is not None else None,
        execution=execution,
        spec=spec,
        metrics=metrics,
        metrics_unavailable_reasons=unavailable,
        source_prefix=f"experiment_{workspace.version}/attempts/{attempt_id}",
    )


def _build_payload(
    workspace: ResearchWorkspace,
    comparison_id: str,
    candidate: _Attempt,
    baselines: tuple[_Attempt, ...],
    *,
    schema_version: int = SCHEMA_VERSION,
) -> dict[str, Any]:
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(f"unsupported comparison schema: {schema_version}")
    aggregation_in_identity = schema_version >= 2
    candidate_summary = _attempt_summary(candidate)
    baseline_summaries = [_attempt_summary(item) for item in baselines]
    return {
        "schema_version": schema_version,
        "artifact_kind": "attempt_fact_comparison",
        "comparison_id": comparison_id,
        "run_id": workspace.workspace_path.name,
        "version": workspace.version,
        "candidate_attempt": candidate_summary,
        "baseline_attempts": baseline_summaries,
        "parity_status_values": list(PARITY_STATUSES),
        "parity_ledgers": [
            _parity_ledger(
                candidate,
                baseline,
                aggregation_in_identity=aggregation_in_identity,
            )
            for baseline in baselines
        ],
        "metric_facts": [
            _metric_pair(
                candidate,
                baseline,
                aggregation_in_identity=aggregation_in_identity,
            )
            for baseline in baselines
        ],
        "interpretation": {
            "owner": "primary_researcher",
            "status": "not_recorded",
            "text": None,
        },
        "mechanical_effects": {
            "changes_hypothesis_or_claim_status": False,
            "participates_in_delivery_eligibility": False,
            "selects_best_attempt": False,
        },
    }


def _attempt_summary(attempt: _Attempt) -> dict[str, Any]:
    return {
        "attempt_id": attempt.attempt_id,
        "execution_path": f"{attempt.source_prefix}/execution.json",
        "execution_sha256": attempt.execution_sha256,
        "spec_path": f"{attempt.source_prefix}/spec.json",
        "spec_sha256": attempt.spec_sha256,
        "metrics_path": f"{attempt.source_prefix}/metrics.json",
        "metrics_sha256": attempt.metrics_sha256,
        "metrics_availability": (
            "available" if attempt.metrics is not None else "unavailable"
        ),
        "metrics_unavailable_reasons": list(attempt.metrics_unavailable_reasons),
        "command_exit_code": attempt.execution["command_exit_code"],
        "runner_exit_code": attempt.execution["runner_exit_code"],
        "timed_out": attempt.execution["timed_out"],
    }


def _parity_ledger(
    candidate: _Attempt,
    baseline: _Attempt,
    *,
    aggregation_in_identity: bool,
) -> dict[str, Any]:
    candidate_facts = _parity_facts(
        candidate, aggregation_in_identity=aggregation_in_identity
    )
    baseline_facts = _parity_facts(
        baseline, aggregation_in_identity=aggregation_in_identity
    )
    return {
        "baseline_attempt_id": baseline.attempt_id,
        "dimensions": [
            {
                "dimension": name,
                "status": _parity_status(candidate_facts[name], baseline_facts[name]),
                "candidate": candidate_facts[name],
                "baseline": baseline_facts[name],
            }
            for name in _DIMENSION_LABELS
        ],
    }


def _parity_facts(
    attempt: _Attempt, *, aggregation_in_identity: bool
) -> dict[str, dict[str, Any]]:
    spec_source = f"{attempt.source_prefix}/spec.json#"
    execution_source = f"{attempt.source_prefix}/execution.json#"
    metrics_source = f"{attempt.source_prefix}/metrics.json#"
    declared = attempt.execution["environment_facts"]["declared_facts"]
    limits = attempt.execution["budget_facts"].get("machine_readable_limits") or {}
    actual = attempt.execution["budget_facts"].get("actual") or {}
    records = attempt.metrics["records"] if attempt.metrics is not None else []
    parity = attempt.spec["parity_dimensions"]

    def declared_or_spec(declared_name: str, spec_name: str) -> dict[str, Any]:
        if declared_name in declared:
            return _fact(
                declared[declared_name],
                f"{execution_source}/environment_facts/declared_facts/{declared_name}",
            )
        return _fact(attempt.spec.get(spec_name), f"{spec_source}/{spec_name}")

    return {
        "task": _fact(attempt.spec.get("research_question"), f"{spec_source}/research_question"),
        "dataset": declared_or_spec("dataset", "dataset"),
        "dataset_split": _fact(
            sorted({record["split"] for record in records}) if records else None,
            f"{metrics_source}/records/*/split",
        ),
        "dataset_revision": _fact(
            declared.get("dataset_revision"),
            f"{execution_source}/environment_facts/declared_facts/dataset_revision",
        ),
        "model": declared_or_spec("model", "model"),
        "provider": declared_or_spec("provider", "provider"),
        "model_revision": (
            _fact(
                declared["model_revision"],
                f"{execution_source}/environment_facts/declared_facts/model_revision",
            )
            if "model_revision" in declared
            else _fact(attempt.spec.get("revision"), f"{spec_source}/revision")
        ),
        "model_quantization": _fact(None, None),
        "prompt_identity": _fact(
            declared.get("prompt_revision"),
            f"{execution_source}/environment_facts/declared_facts/prompt_revision",
        ),
        "context": _fact(None, None),
        "information_access": _fact(
            parity.get("information_access"),
            f"{spec_source}/parity_dimensions/information_access",
        ),
        "tool_set": _fact(
            parity.get("tool_capability"),
            f"{spec_source}/parity_dimensions/tool_capability",
        ),
        "tool_permissions": _fact(
            parity.get("tool_capability"),
            f"{spec_source}/parity_dimensions/tool_capability",
        ),
        "search_budget": _fact(None, None),
        "retry_budget": _fact(None, None),
        "call_budget": _budget_fact(
            limits.get("api_calls"),
            actual.get("api_calls"),
            f"{execution_source}/budget_facts",
        ),
        "token_budget": _budget_fact(
            limits.get("tokens"),
            actual.get("tokens"),
            f"{execution_source}/budget_facts",
        ),
        "wall_budget": _budget_fact(
            limits.get("duration_seconds"),
            actual.get("duration_seconds"),
            f"{execution_source}/budget_facts",
        ),
        "gpu_budget": _budget_fact(
            limits.get("gpu_time_seconds"),
            actual.get("gpu_time_seconds"),
            f"{execution_source}/budget_facts",
        ),
        "cost_budget": _budget_fact(
            None,
            _known(attempt.metrics["resource_usage"].get("estimated_cost"))
            if attempt.metrics is not None
            else None,
            f"{metrics_source}/resource_usage/estimated_cost",
        ),
        "seed": _seed_fact(attempt),
        "replicate_count": _replicate_fact(
            attempt, aggregation_in_identity=aggregation_in_identity
        ),
        "evaluator": _fact(
            attempt.spec.get("independent_ground_truth"),
            f"{spec_source}/independent_ground_truth",
        ),
        "metric_definition": _fact(
            sorted(
                {
                    (
                        record["name"],
                        record["unit"],
                        record["split"],
                        record["aggregation"],
                    )
                    for record in records
                }
            )
            if records
            else None,
            f"{metrics_source}/records",
        ),
        "sampling_unit": _fact(
            attempt.spec.get("sampling_unit"), f"{spec_source}/sampling_unit"
        ),
        "implementation_identity": _fact(
            [
                {
                    "path": item["path"],
                    "size_bytes": item["size_bytes"],
                    "sha256": item["sha256"],
                }
                for item in attempt.execution["implementation_files"]
            ],
            f"{execution_source}/implementation_files",
        ),
        "failure_rate": _fact(
            {
                "failed_attempts": int(_attempt_failed(attempt.execution)),
                "attempt_count": 1,
                "rate": float(_attempt_failed(attempt.execution)),
                "command_exit_code": attempt.execution["command_exit_code"],
                "runner_exit_code": attempt.execution["runner_exit_code"],
                "timed_out": attempt.execution["timed_out"],
            },
            f"{execution_source}/command_exit_code,runner_exit_code,timed_out",
        ),
    }


def _metric_pair(
    candidate: _Attempt,
    baseline: _Attempt,
    *,
    aggregation_in_identity: bool,
) -> dict[str, Any]:
    candidate_groups = _metric_groups(
        candidate.metrics["records"] if candidate.metrics is not None else [],
        aggregation_in_identity=aggregation_in_identity,
    )
    baseline_groups = _metric_groups(
        baseline.metrics["records"] if baseline.metrics is not None else [],
        aggregation_in_identity=aggregation_in_identity,
    )
    comparisons = []
    for key in sorted(set(candidate_groups) | set(baseline_groups)):
        candidate_records = candidate_groups.get(key, [])
        baseline_records = baseline_groups.get(key, [])
        metric_key = {"name": key[0], "unit": key[1], "split": key[2]}
        if aggregation_in_identity:
            metric_key["aggregation"] = key[3]
        item: dict[str, Any] = {
            "metric_key": metric_key,
            "metric_presence": (
                "both"
                if candidate_records and baseline_records
                else "candidate_only"
                if candidate_records
                else "baseline_only"
            ),
            "candidate": _record_summary(candidate_records),
            "baseline": _record_summary(baseline_records),
            "candidate_fact_value": None,
            "baseline_fact_value": None,
            "difference_candidate_minus_baseline": None,
            "ratio_candidate_over_baseline": None,
            "confidence_interval": None,
        }
        if candidate_records and baseline_records:
            candidate_value = statistics.fmean(item["candidate"]["values"])
            baseline_value = statistics.fmean(item["baseline"]["values"])
            item["fact_value_basis"] = (
                "single_record_value"
                if len(candidate_records) == len(baseline_records) == 1
                else (
                    "arithmetic_mean_across_same_metric_unit_split_aggregation_records"
                    if aggregation_in_identity
                    else "arithmetic_mean_across_same_metric_unit_split_records"
                )
            )
            item["candidate_fact_value"] = candidate_value
            item["baseline_fact_value"] = baseline_value
            item["difference_candidate_minus_baseline"] = _finite(
                candidate_value - baseline_value
            )
            if baseline_value == 0:
                item["ratio_reason"] = "baseline fact value is zero"
            else:
                item["ratio_candidate_over_baseline"] = _finite(
                    candidate_value / baseline_value
                )
            ci, reason = _replicate_confidence_interval(
                candidate_records, baseline_records
            )
            item["confidence_interval"] = ci
            if reason is not None:
                item["confidence_interval_reason"] = reason
        comparisons.append(item)
    return {"baseline_attempt_id": baseline.attempt_id, "comparisons": comparisons}


def _metric_groups(
    records: list[dict[str, Any]],
    *,
    aggregation_in_identity: bool,
) -> dict[tuple[str, ...], list[dict[str, Any]]]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for record in records:
        key = (record["name"], record["unit"], record["split"])
        if aggregation_in_identity:
            key += (record["aggregation"],)
        groups.setdefault(key, []).append(record)
    return groups


def _record_summary(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not records:
        return None
    values = [record["value"] for record in records]
    summary: dict[str, Any] = {
        "record_count": len(records),
        "values": values,
        "aggregations": [record["aggregation"] for record in records],
        "n": [record["n"] for record in records],
        "seeds": [record.get("seed") for record in records],
        "replicates": [record.get("replicate") for record in records],
        "descriptive_statistics": {
            "count": len(values),
            "mean": statistics.fmean(values),
            "minimum": min(values),
            "maximum": max(values),
            "sample_standard_deviation": (
                statistics.stdev(values) if len(values) >= 2 else None
            ),
        },
    }
    identities = [_replicate_identity(record) for record in records]
    if all(item is not None for item in identities):
        rendered = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in identities]
        summary["duplicate_replicate_identities"] = sorted(
            {item for item in rendered if rendered.count(item) > 1}
        )
    else:
        summary["duplicate_replicate_identities"] = []
    return summary


def _replicate_confidence_interval(
    candidate: list[dict[str, Any]], baseline: list[dict[str, Any]]
) -> tuple[dict[str, Any] | None, str | None]:
    if len(candidate) < 2 or len(baseline) < 2:
        return None, "each side needs at least two raw replicate records"
    candidate_ids = [_replicate_identity(record) for record in candidate]
    baseline_ids = [_replicate_identity(record) for record in baseline]
    if any(item is None for item in candidate_ids + baseline_ids):
        return None, "raw replicate identifiers are missing"
    candidate_keys = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in candidate_ids]
    baseline_keys = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in baseline_ids]
    if len(set(candidate_keys)) != len(candidate_keys) or len(set(baseline_keys)) != len(
        baseline_keys
    ):
        return None, "raw replicate identifiers contain duplicates"

    if set(candidate_keys) == set(baseline_keys):
        candidate_map = {
            key: record["value"] for key, record in zip(candidate_keys, candidate, strict=True)
        }
        baseline_map = {
            key: record["value"] for key, record in zip(baseline_keys, baseline, strict=True)
        }
        differences = [candidate_map[key] - baseline_map[key] for key in sorted(candidate_map)]
        center = statistics.fmean(differences)
        standard_error = statistics.stdev(differences) / math.sqrt(len(differences))
        method = (
            "two-sided 95% normal approximation for paired raw-replicate "
            f"mean difference; n_pairs={len(differences)}; z=1.959963984540054; "
            "normal-approximation coverage may be inaccurate with small samples"
        )
        sample_sizes = {"paired_replicates": len(differences)}
    else:
        candidate_values = [record["value"] for record in candidate]
        baseline_values = [record["value"] for record in baseline]
        center = statistics.fmean(candidate_values) - statistics.fmean(baseline_values)
        standard_error = math.sqrt(
            statistics.variance(candidate_values) / len(candidate_values)
            + statistics.variance(baseline_values) / len(baseline_values)
        )
        method = (
            "two-sided 95% normal approximation for independent raw-replicate "
            "mean difference with unpooled standard error; "
            f"n_candidate={len(candidate_values)}, n_baseline={len(baseline_values)}; "
            "z=1.959963984540054; normal-approximation coverage may be inaccurate "
            "with small samples"
        )
        sample_sizes = {
            "candidate_replicates": len(candidate_values),
            "baseline_replicates": len(baseline_values),
        }
    return (
        {
            "confidence_level": 0.95,
            "estimand": "candidate_mean_minus_baseline_mean",
            "method": method,
            "lower": _finite(center - _Z_95 * standard_error),
            "upper": _finite(center + _Z_95 * standard_error),
            "sample_sizes": sample_sizes,
        },
        None,
    )


def _seed_fact(attempt: _Attempt) -> dict[str, Any]:
    metric_seeds = [
        record["seed"]
        for record in (attempt.metrics["records"] if attempt.metrics is not None else [])
        if "seed" in record
    ]
    return _fact(
        {
            "spec_seeds": attempt.spec["seeds"],
            "execution_seed": attempt.execution["seed"],
            "metric_record_seeds": metric_seeds,
            "duplicate_metric_record_seeds": sorted(
                {item for item in metric_seeds if metric_seeds.count(item) > 1},
                key=str,
            ),
        },
        [
            f"{attempt.source_prefix}/spec.json#/seeds",
            f"{attempt.source_prefix}/execution.json#/seed",
            f"{attempt.source_prefix}/metrics.json#/records/*/seed",
        ],
    )


def _replicate_fact(
    attempt: _Attempt, *, aggregation_in_identity: bool
) -> dict[str, Any]:
    groups = _metric_groups(
        attempt.metrics["records"] if attempt.metrics is not None else [],
        aggregation_in_identity=aggregation_in_identity,
    )
    described = {}
    for key, records in sorted(groups.items()):
        identities = [_replicate_identity(record) for record in records]
        if any(item is not None for item in identities):
            described[" / ".join(key)] = {
                "record_count": len(records),
                "replicate_identities": identities,
            }
    return _fact(
        described or None,
        f"{attempt.source_prefix}/metrics.json#/records/*/replicate",
    )


def _replicate_identity(record: Mapping[str, Any]) -> dict[str, Any] | None:
    if "replicate" not in record:
        return None
    return {"seed": record.get("seed"), "replicate": record["replicate"]}


def _attempt_failed(execution: Mapping[str, Any]) -> bool:
    return bool(
        execution["timed_out"]
        or execution["command_exit_code"] != 0
        or execution["runner_exit_code"] != 0
    )


def _fact(value: Any, sources: str | list[str] | None) -> dict[str, Any]:
    if sources is None:
        source_list: list[str] = []
    elif isinstance(sources, str):
        source_list = [sources]
    else:
        source_list = sources
    return {"value": value, "sources": source_list}


def _budget_fact(limit: Any, actual: Any, source: str) -> dict[str, Any]:
    limit = _known(limit)
    actual = _known(actual)
    return _fact(
        None if limit is None and actual is None else {"limit": limit, "actual": actual},
        source,
    )


def _known(value: Any) -> Any:
    return None if value is None or value == "unknown" else value


def _parity_status(candidate: Mapping[str, Any], baseline: Mapping[str, Any]) -> str:
    candidate_value = candidate["value"]
    baseline_value = baseline["value"]
    if candidate_value is None or baseline_value is None:
        return "unknown"
    candidate_na = _not_applicable(candidate_value)
    baseline_na = _not_applicable(baseline_value)
    if candidate_na or baseline_na:
        return "not_applicable" if candidate_na and baseline_na else "mismatched"
    return "matched" if candidate_value == baseline_value else "mismatched"


def _not_applicable(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() in {
        "not_applicable",
        "not applicable",
        "n/a",
    }


def _json_object(data: bytes, label: str) -> dict[str, Any]:
    value = json.loads(data.decode("utf-8"), parse_constant=_reject_json_constant)
    if not isinstance(value, dict):
        raise ValueError(f"{label} must contain an object")
    return value


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def _identifier(value: str, label: str) -> str:
    text = str(value).strip()
    if _IDENTIFIER.fullmatch(text) is None:
        raise ValueError(f"{label} must be one safe 1-80 character identifier")
    return text


def _finite(value: float) -> float | None:
    return value if math.isfinite(value) else None


def _number(value: Any) -> str:
    if value is None:
        return "—"
    if type(value) in {int, float}:
        return format(value, ".12g")
    return _md(json.dumps(value, ensure_ascii=False, sort_keys=True))


def _fact_text(fact: Mapping[str, Any]) -> str:
    value = json.dumps(fact["value"], ensure_ascii=False, sort_keys=True)
    sources = ", ".join(fact["sources"]) or "无可用来源"
    return f"{value}；来源：{sources}"


def _md(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")
