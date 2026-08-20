from __future__ import annotations

import json
import os
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Iterable, Mapping, Sequence
from uuid import uuid4

from crl_v3.hypotheses import (
    HYPOTHESIS_STATUSES,
    HypothesisPortfolio,
    HypothesisRecord,
)
from crl_v3.workspace import ResearchWorkspace


ANALYSIS_SCHEMA_VERSION = 1
DESCRIPTOR_FIELDS = (
    "problem_family",
    "computation_stage",
    "intervention_family",
    "information_source",
    "timing_class",
    "budget_class",
    "evaluation_mode",
)
MISSING_VALUE = "(missing)"
UNKNOWN_CLAIM_PURPOSE = "unknown"
DEFAULT_NEAR_DUPLICATE_THRESHOLD = 0.85
DEFAULT_STALE_DAYS = 30

_ANALYSIS_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,63}")
_TOKEN_PART = re.compile(r"[a-z0-9]+|[\u3400-\u4dbf\u4e00-\u9fff]+")

SEARCH_OPERATION_TEMPLATES = (
    "保留 failure，改变 intervention stage。",
    "保留 operator，移除额外信息。",
    "匹配预算后重新构造。",
    "改用独立 evaluator。",
    "从 sibling lineage 构造反例。",
)


def analyze_portfolio(
    portfolio: HypothesisPortfolio | None,
    *,
    statuses: Iterable[str] = (),
    descriptor_filters: Mapping[str, Iterable[str]] | None = None,
    lineage_roots: Iterable[str] = (),
    near_duplicate_threshold: float = DEFAULT_NEAR_DUPLICATE_THRESHOLD,
    stale_days: int = DEFAULT_STALE_DAYS,
    as_of: str | None = None,
    source_path: str | None = None,
    source_sha256: str | None = None,
    run_id: str | None = None,
    version: str | None = None,
) -> dict[str, object]:
    """Build a deterministic, read-only structural diagnostic for one portfolio."""

    status_filter = tuple(sorted(set(statuses)))
    unknown_statuses = set(status_filter) - set(HYPOTHESIS_STATUSES)
    if unknown_statuses:
        raise ValueError(f"invalid status filters: {sorted(unknown_statuses)}")
    normalized_descriptor_filters = _normalize_descriptor_filters(
        descriptor_filters or {}
    )
    lineage_filter = tuple(sorted(set(lineage_roots)))
    threshold = _similarity_threshold(near_duplicate_threshold)
    if type(stale_days) is not int or stale_days < 0:
        raise ValueError("stale_days must be a non-negative integer")

    if portfolio is None:
        if lineage_filter:
            raise KeyError(
                f"unknown lineage roots in absent portfolio: {list(lineage_filter)}"
            )
        reference_time = _parse_timestamp(as_of, "as_of") if as_of else None
        return _empty_report(
            portfolio_state="absent",
            run_id=run_id,
            version=version,
            status_filter=status_filter,
            descriptor_filters=normalized_descriptor_filters,
            lineage_filter=lineage_filter,
            threshold=threshold,
            stale_days=stale_days,
            reference_time=reference_time,
            source_path=source_path,
            source_sha256=source_sha256,
        )

    all_records = tuple(portfolio.hypotheses)
    by_id = {record.hypothesis_id: record for record in all_records}
    unknown_lineage = set(lineage_filter) - set(by_id)
    if unknown_lineage:
        raise KeyError(f"unknown lineage roots: {sorted(unknown_lineage)}")
    lineage_members = (
        _descendants_including_roots(all_records, lineage_filter)
        if lineage_filter
        else set(by_id)
    )
    records = tuple(
        record
        for record in all_records
        if record.hypothesis_id in lineage_members
        and (not status_filter or record.status in status_filter)
        and _matches_descriptors(record, normalized_descriptor_filters)
    )
    reference_time = (
        _parse_timestamp(as_of, "as_of")
        if as_of
        else _parse_timestamp(portfolio.updated_at_utc, "portfolio updated_at_utc")
    )

    report: dict[str, object] = {
        "schema_version": ANALYSIS_SCHEMA_VERSION,
        "diagnostic_scope": (
            "Run-local structural and text-similarity diagnostic only; it does not "
            "establish novelty, scientific quality, correctness, importance, "
            "publishability, or Delivery eligibility."
        ),
        "source": {
            "portfolio_state": "empty" if not all_records else "present",
            "path": source_path,
            "sha256": source_sha256,
            "run_id": portfolio.run_id,
            "version": portfolio.version,
            "portfolio_revision": portfolio.revision,
            "portfolio_record_count": len(all_records),
        },
        "filters": {
            "statuses": list(status_filter),
            "descriptors": {
                field: list(values)
                for field, values in normalized_descriptor_filters.items()
            },
            "lineage_roots": list(lineage_filter),
        },
        "selected_record_count": len(records),
        "selected_hypothesis_ids": [record.hypothesis_id for record in records],
        "descriptor_distributions": _descriptor_distributions(records),
        "cross_matrices": {
            "problem_family_x_computation_stage": _cross_matrix(
                records,
                "problem_family",
                "computation_stage",
                lambda record: record.descriptors.problem_family,
                lambda record: record.descriptors.computation_stage,
            ),
            "target_failure_x_intervention_family": _cross_matrix(
                records,
                "target_failure",
                "intervention_family",
                lambda record: record.target_failure.summary,
                lambda record: record.descriptors.intervention_family,
            ),
            "information_source_x_budget_class": _cross_matrix(
                records,
                "information_source",
                "budget_class",
                lambda record: record.descriptors.information_source,
                lambda record: record.descriptors.budget_class,
            ),
            "evaluation_mode_x_claim_purpose": _cross_matrix(
                records,
                "evaluation_mode",
                "claim_purpose",
                lambda record: record.descriptors.evaluation_mode,
                lambda record: UNKNOWN_CLAIM_PURPOSE,
            ),
        },
        "lineage": _lineage_diagnostics(
            records, reference_time=reference_time, stale_days=stale_days
        ),
        "identical_structures": _identical_structures(records),
        "near_duplicates": {
            "method": "field-labelled Unicode token Jaccard",
            "threshold": threshold,
            "warning_count": 0,
            "warnings": [],
        },
        "search_operation_templates": list(SEARCH_OPERATION_TEMPLATES),
        "method_notes": [
            "Missing descriptor values are reported as '(missing)' and are not inferred.",
            (
                "HypothesisPortfolio schema 1 does not record claim purpose; the "
                "claim-purpose axis is therefore reported as 'unknown'."
            ),
            (
                "Text similarity uses title, problem, mechanism claim, and changed "
                "computation only. Similarity is diagnostic and is not a novelty claim."
            ),
            (
                "Search operations are abstract templates; this analysis creates no "
                "Claim and adds or changes no portfolio record or status."
            ),
        ],
    }
    warnings = _near_duplicate_warnings(records, threshold)
    report["near_duplicates"] = {
        "method": "field-labelled Unicode token Jaccard",
        "threshold": threshold,
        "warning_count": len(warnings),
        "warnings": warnings,
    }
    return report


def tokenize_text(value: str) -> frozenset[str]:
    """Return explainable case-folded word and Chinese-bigram tokens."""

    if not isinstance(value, str):
        raise ValueError("text to tokenize must be text")
    normalized = unicodedata.normalize("NFKC", value).casefold()
    tokens: set[str] = set()
    for part in _TOKEN_PART.findall(normalized):
        if _is_cjk(part):
            if len(part) == 1:
                tokens.add(f"zh:{part}")
            else:
                tokens.update(
                    f"zh:{part[index:index + 2]}" for index in range(len(part) - 1)
                )
        else:
            tokens.add(f"word:{part}")
    return frozenset(tokens)


def jaccard_similarity(left: Iterable[str], right: Iterable[str]) -> float:
    left_set = frozenset(left)
    right_set = frozenset(right)
    union = left_set | right_set
    if not union:
        return 0.0
    return len(left_set & right_set) / len(union)


def render_analysis_markdown(report: Mapping[str, object]) -> str:
    source = _mapping(report.get("source"), "analysis source")
    filters = _mapping(report.get("filters"), "analysis filters")
    lines = [
        "# 假设组合结构诊断",
        "",
        "> 本报告只呈现结构覆盖与文本相似性诊断；不判断新颖性、科研质量、正确性、重要性、可发表性或交付资格。",
        "",
        f"- 组合状态：`{source.get('portfolio_state')}`",
        f"- Run：`{source.get('run_id') or '(unknown)'}`",
        f"- 版本：`{source.get('version') or '(unknown)'}`",
        f"- 原始记录数：{source.get('portfolio_record_count', 0)}",
        f"- 过滤后记录数：{report.get('selected_record_count', 0)}",
        "",
        "## 过滤条件",
        "",
        f"- status：{_markdown_values(filters.get('statuses'))}",
        f"- descriptor：{_markdown_mapping(filters.get('descriptors'))}",
        f"- lineage roots：{_markdown_values(filters.get('lineage_roots'))}",
        "",
        "## Descriptor 占用分布",
        "",
    ]
    distributions = _mapping(
        report.get("descriptor_distributions"), "descriptor distributions"
    )
    for field, details_value in distributions.items():
        details = _mapping(details_value, f"descriptor distribution {field}")
        lines.append(f"- `{field}`：{_markdown_counts(details.get('counts'))}")

    lines.extend(["", "## 交叉矩阵", ""])
    matrices = _mapping(report.get("cross_matrices"), "cross matrices")
    for name, matrix_value in matrices.items():
        matrix = _mapping(matrix_value, f"cross matrix {name}")
        lines.extend([f"### `{name}`", ""])
        rows = matrix.get("rows")
        columns = matrix.get("columns")
        if not rows or not columns:
            lines.extend(["(无记录)", ""])
            continue
        lines.append(
            "| "
            + str(matrix.get("row_dimension"))
            + " | "
            + " | ".join(str(item) for item in columns)
            + " |"
        )
        lines.append("| --- | " + " | ".join("---:" for _ in columns) + " |")
        counts = _mapping(matrix.get("counts"), f"cross matrix counts {name}")
        for row in rows:
            row_counts = _mapping(counts.get(str(row)), f"cross matrix row {row}")
            lines.append(
                "| "
                + str(row)
                + " | "
                + " | ".join(str(row_counts.get(str(column), 0)) for column in columns)
                + " |"
            )
        lines.append("")

    lineage = _mapping(report.get("lineage"), "lineage")
    lines.extend(
        [
            "## 谱系事实",
            "",
            f"- 最大深度：{lineage.get('max_depth', 0)}",
            f"- 边数：{lineage.get('edge_count', 0)}",
            f"- 有分支的候选数：{lineage.get('branching_hypothesis_count', 0)}",
            f"- 孤立候选：{_markdown_values(lineage.get('isolated_hypothesis_ids'))}",
            f"- 长期无更新候选：{_markdown_values(lineage.get('stale_hypothesis_ids'))}",
            f"- 各候选深度：{_markdown_mapping(lineage.get('depth_by_hypothesis'))}",
            f"- 各候选分支数：{_markdown_mapping(lineage.get('branch_count_by_hypothesis'))}",
            "",
            "## 结构完全相同",
            "",
        ]
    )
    identical = report.get("identical_structures")
    if not identical:
        lines.extend(["(无完整 descriptor 结构重复组)", ""])
    else:
        for group_value in _sequence(identical, "identical structures"):
            group = _mapping(group_value, "identical structure group")
            lines.append(
                f"- {_markdown_values(group.get('hypothesis_ids'))}；descriptor："
                f"{_markdown_mapping(group.get('descriptors'))}"
            )
        lines.append("")

    near = _mapping(report.get("near_duplicates"), "near duplicates")
    lines.extend(
        [
            "## 文本近重复告警",
            "",
            f"- 方法：{near.get('method')}",
            f"- 阈值：{near.get('threshold')}",
        ]
    )
    warnings = near.get("warnings")
    if not warnings:
        lines.append("- 告警：(无)")
    else:
        for warning_value in _sequence(warnings, "near duplicate warnings"):
            warning = _mapping(warning_value, "near duplicate warning")
            lines.append(
                f"- `{warning.get('left_id')}` ↔ `{warning.get('right_id')}`："
                f"Jaccard={warning.get('similarity')}，共享 token 数="
                f"{warning.get('shared_token_count')}"
            )

    lines.extend(["", "## 抽象搜索操作模板", ""])
    for item in _sequence(
        report.get("search_operation_templates"), "search operation templates"
    ):
        lines.append(f"- {item}")
    lines.extend(["", "## 方法说明", ""])
    for item in _sequence(report.get("method_notes"), "method notes"):
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def analysis_json_bytes(report: Mapping[str, object]) -> bytes:
    return (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def save_analysis(
    workspace: ResearchWorkspace,
    analysis_id: str,
    report: Mapping[str, object],
) -> Path:
    """Save JSON and Markdown once under the fixed Run-local analysis directory."""

    workspace.assert_run_writable()
    if not isinstance(analysis_id, str) or _ANALYSIS_ID.fullmatch(analysis_id) is None:
        raise ValueError(
            "ANALYSIS_ID must be 3-64 lowercase letters, digits, dot, underscore, or hyphen"
        )
    parent = workspace.assert_write_target(
        workspace.hypotheses_path.parent / "analysis"
    )
    parent.mkdir(parents=True, exist_ok=True)
    destination = workspace.assert_write_target(parent / analysis_id)
    if destination.exists():
        raise FileExistsError(f"analysis already exists: {analysis_id}")
    temporary = workspace.assert_write_target(
        parent / f".{analysis_id}.{uuid4().hex}.tmp"
    )
    temporary.mkdir()
    try:
        _write_new_file(temporary / "analysis.json", analysis_json_bytes(report))
        _write_new_file(
            temporary / "analysis.md", render_analysis_markdown(report).encode("utf-8")
        )
        os.rename(temporary, destination)
    finally:
        if temporary.exists():
            for child in temporary.iterdir():
                child.unlink()
            temporary.rmdir()
    return destination


def _empty_report(
    *,
    portfolio_state: str,
    run_id: str | None,
    version: str | None,
    status_filter: tuple[str, ...],
    descriptor_filters: Mapping[str, tuple[str, ...]],
    lineage_filter: tuple[str, ...],
    threshold: float,
    stale_days: int,
    reference_time: datetime | None,
    source_path: str | None,
    source_sha256: str | None,
) -> dict[str, object]:
    empty = HypothesisPortfolio(
        schema_version=1,
        run_id=run_id or "unknown",
        version=version or "v000",
        revision=0,
        created_at_utc="1970-01-01T00:00:00Z",
        updated_at_utc="1970-01-01T00:00:00Z",
        hypotheses=(),
    )
    report = analyze_portfolio(
        empty,
        statuses=status_filter,
        descriptor_filters=descriptor_filters,
        lineage_roots=lineage_filter,
        near_duplicate_threshold=threshold,
        stale_days=stale_days,
        as_of=(reference_time or datetime(1970, 1, 1, tzinfo=UTC)).isoformat().replace(
            "+00:00", "Z"
        ),
        source_path=source_path,
        source_sha256=source_sha256,
    )
    report["source"] = {
        "portfolio_state": portfolio_state,
        "path": source_path,
        "sha256": source_sha256,
        "run_id": run_id,
        "version": version,
        "portfolio_revision": None,
        "portfolio_record_count": 0,
    }
    return report


def _normalize_descriptor_filters(
    filters: Mapping[str, Iterable[str]],
) -> dict[str, tuple[str, ...]]:
    unknown = set(filters) - set(DESCRIPTOR_FIELDS)
    if unknown:
        raise ValueError(f"unknown descriptor filters: {sorted(unknown)}")
    normalized: dict[str, tuple[str, ...]] = {}
    for field in DESCRIPTOR_FIELDS:
        if field not in filters:
            continue
        values = tuple(sorted(set(filters[field])))
        if not values or any(not isinstance(value, str) or not value for value in values):
            raise ValueError(f"descriptor filter {field!r} requires non-empty values")
        normalized[field] = values
    return normalized


def _matches_descriptors(
    record: HypothesisRecord, filters: Mapping[str, tuple[str, ...]]
) -> bool:
    for field, allowed in filters.items():
        value = getattr(record.descriptors, field) or MISSING_VALUE
        if value not in allowed:
            return False
    return True


def _descendants_including_roots(
    records: Sequence[HypothesisRecord], roots: Sequence[str]
) -> set[str]:
    children: dict[str, list[str]] = defaultdict(list)
    for record in records:
        for parent in record.parent_ids:
            children[parent].append(record.hypothesis_id)
    selected = set(roots)
    stack = list(reversed(roots))
    while stack:
        current = stack.pop()
        for child in sorted(children.get(current, ())):
            if child not in selected:
                selected.add(child)
                stack.append(child)
    return selected


def _descriptor_distributions(
    records: Sequence[HypothesisRecord],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for field in DESCRIPTOR_FIELDS:
        values = [getattr(record.descriptors, field) or MISSING_VALUE for record in records]
        counts = Counter(values)
        result[field] = {
            "counts": {key: counts[key] for key in sorted(counts)},
            "occupied_value_count": len([key for key in counts if key != MISSING_VALUE]),
            "missing_count": counts.get(MISSING_VALUE, 0),
        }
    return result


def _cross_matrix(
    records: Sequence[HypothesisRecord],
    row_dimension: str,
    column_dimension: str,
    row_value: object,
    column_value: object,
) -> dict[str, object]:
    pairs = [
        (_display_value(row_value(record)), _display_value(column_value(record)))
        for record in records
    ]
    rows = sorted({row for row, _ in pairs})
    columns = sorted({column for _, column in pairs})
    pair_counts = Counter(pairs)
    return {
        "row_dimension": row_dimension,
        "column_dimension": column_dimension,
        "rows": rows,
        "columns": columns,
        "counts": {
            row: {column: pair_counts[(row, column)] for column in columns}
            for row in rows
        },
    }


def _lineage_diagnostics(
    records: Sequence[HypothesisRecord], *, reference_time: datetime, stale_days: int
) -> dict[str, object]:
    selected_ids = {record.hypothesis_id for record in records}
    parents = {
        record.hypothesis_id: tuple(
            parent for parent in record.parent_ids if parent in selected_ids
        )
        for record in records
    }
    children: dict[str, list[str]] = {record.hypothesis_id: [] for record in records}
    for child, parent_ids in parents.items():
        for parent in parent_ids:
            children[parent].append(child)

    depths: dict[str, int] = {}

    def depth(hypothesis_id: str) -> int:
        if hypothesis_id not in depths:
            depths[hypothesis_id] = (
                0
                if not parents[hypothesis_id]
                else 1 + max(depth(parent) for parent in parents[hypothesis_id])
            )
        return depths[hypothesis_id]

    for hypothesis_id in sorted(selected_ids):
        depth(hypothesis_id)
    branch_counts = {
        hypothesis_id: len(children[hypothesis_id])
        for hypothesis_id in sorted(selected_ids)
    }
    isolated = [
        hypothesis_id
        for hypothesis_id in sorted(selected_ids)
        if not parents[hypothesis_id] and not children[hypothesis_id]
    ]
    cutoff = reference_time - timedelta(days=stale_days)
    stale = sorted(
        record.hypothesis_id
        for record in records
        if _parse_timestamp(record.updated_at_utc, "hypothesis updated_at_utc") <= cutoff
    )
    return {
        "reference_time_utc": reference_time.isoformat().replace("+00:00", "Z"),
        "stale_after_days": stale_days,
        "max_depth": max(depths.values(), default=0),
        "depth_by_hypothesis": {key: depths[key] for key in sorted(depths)},
        "edge_count": sum(len(value) for value in parents.values()),
        "branching_hypothesis_count": sum(
            count > 1 for count in branch_counts.values()
        ),
        "branch_count_by_hypothesis": branch_counts,
        "isolated_hypothesis_ids": isolated,
        "stale_hypothesis_ids": stale,
    }


def _identical_structures(records: Sequence[HypothesisRecord]) -> list[dict[str, object]]:
    groups: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for record in records:
        signature = tuple(getattr(record.descriptors, field) for field in DESCRIPTOR_FIELDS)
        if all(signature):
            groups[signature].append(record.hypothesis_id)
    result = []
    for signature, hypothesis_ids in sorted(groups.items()):
        if len(hypothesis_ids) < 2:
            continue
        result.append(
            {
                "hypothesis_ids": sorted(hypothesis_ids),
                "descriptors": dict(zip(DESCRIPTOR_FIELDS, signature, strict=True)),
            }
        )
    return result


def _near_duplicate_warnings(
    records: Sequence[HypothesisRecord], threshold: float
) -> list[dict[str, object]]:
    warnings: list[dict[str, object]] = []
    ordered = sorted(records, key=lambda record: record.hypothesis_id)
    for index, left in enumerate(ordered):
        left_fields, left_tokens = _record_text_tokens(left)
        for right in ordered[index + 1 :]:
            right_fields, right_tokens = _record_text_tokens(right)
            combined = jaccard_similarity(left_tokens, right_tokens)
            if not left_tokens or not right_tokens or combined < threshold:
                continue
            shared = sorted(left_tokens & right_tokens)
            warnings.append(
                {
                    "left_id": left.hypothesis_id,
                    "right_id": right.hypothesis_id,
                    "similarity": round(combined, 6),
                    "shared_token_count": len(shared),
                    "union_token_count": len(left_tokens | right_tokens),
                    "shared_tokens": shared,
                    "field_similarities": {
                        field: round(
                            jaccard_similarity(left_fields[field], right_fields[field]),
                            6,
                        )
                        for field in ("title", "problem", "claim", "changed_computation")
                    },
                }
            )
    return warnings


def _record_text_tokens(
    record: HypothesisRecord,
) -> tuple[dict[str, frozenset[str]], frozenset[str]]:
    changed = " ".join(
        (
            record.changed_computation.baseline,
            record.changed_computation.intervention,
            record.changed_computation.information_available,
            record.changed_computation.timing,
            record.changed_computation.budget_effect,
        )
    )
    texts = {
        "title": record.title,
        "problem": record.problem,
        "claim": record.mechanism_claim,
        "changed_computation": changed,
    }
    fields = {field: tokenize_text(text) for field, text in texts.items()}
    combined = frozenset(
        f"{field}:{token}" for field, tokens in fields.items() for token in tokens
    )
    return fields, combined


def _similarity_threshold(value: float) -> float:
    if type(value) not in (int, float) or not 0.0 <= float(value) <= 1.0:
        raise ValueError("near_duplicate_threshold must be between 0 and 1")
    return float(value)


def _parse_timestamp(value: str | None, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"invalid {label}: {value!r}") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError(f"{label} must be UTC")
    return parsed.astimezone(UTC)


def _display_value(value: object) -> str:
    return value if isinstance(value, str) and value else MISSING_VALUE


def _is_cjk(value: str) -> bool:
    return all("\u3400" <= character <= "\u9fff" for character in value)


def _write_new_file(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return dict(value)


def _sequence(value: object, label: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{label} must be an array")
    return value


def _markdown_values(value: object) -> str:
    if not value:
        return "(无)"
    return ", ".join(f"`{item}`" for item in _sequence(value, "markdown values"))


def _markdown_mapping(value: object) -> str:
    if not value:
        return "(无)"
    mapping = _mapping(value, "markdown mapping")
    return ", ".join(f"`{key}`={mapping[key]}" for key in sorted(mapping))


def _markdown_counts(value: object) -> str:
    if not value:
        return "(无记录)"
    mapping = _mapping(value, "markdown counts")
    return ", ".join(f"`{key}`={mapping[key]}" for key in sorted(mapping))
