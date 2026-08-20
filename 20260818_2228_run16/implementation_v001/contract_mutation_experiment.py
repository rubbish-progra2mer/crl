from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


RISK_FAMILIES = (
    "same_entity_extra_record",
    "same_entity_unexpected_field",
    "cross_entity_extra_record",
    "extra_delete",
)


def load_jsonl(path: Path, split: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        row["_split"] = split
        row["_contract"] = json.loads(row["answer"])
        row["_info"] = json.loads(row["info"])
        rows.append(row)
    return rows


def snake(value: str) -> str:
    value = value.replace(".", "_")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def lookup(record: dict[str, Any], path: str) -> tuple[bool, Any]:
    if path in record:
        return True, record[path]
    alias = snake(path)
    for key, value in record.items():
        if snake(str(key)) == alias:
            return True, value
    current: Any = record
    for part in path.split("."):
        if not isinstance(current, dict):
            return False, None
        if part in current:
            current = current[part]
            continue
        part_alias = snake(part)
        found = next((key for key in current if snake(str(key)) == part_alias), None)
        if found is None:
            return False, None
        current = current[found]
    return True, current


def predicate(value: Any, condition: Any, present: bool = True) -> bool:
    if not isinstance(condition, dict):
        return value == condition
    for operator, target in condition.items():
        if operator == "eq" and value != target:
            return False
        if operator in {"ne", "neq"} and value == target:
            return False
        if operator == "contains":
            if isinstance(value, (dict, list, tuple)):
                rendered = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            elif isinstance(value, set):
                rendered = json.dumps(sorted(value), ensure_ascii=False, separators=(",", ":"))
            else:
                rendered = str(value)
            if str(target) not in rendered:
                return False
        if operator == "i_contains":
            if isinstance(value, (dict, list, tuple)):
                rendered = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            elif isinstance(value, set):
                rendered = json.dumps(sorted(value), ensure_ascii=False, separators=(",", ":"))
            else:
                rendered = str(value)
            if str(target).casefold() not in rendered.casefold():
                return False
        if operator == "not_contains" and str(target) in str(value):
            return False
        if operator == "starts_with" and not str(value).startswith(str(target)):
            return False
        if operator == "ends_with" and not str(value).endswith(str(target)):
            return False
        if operator == "regex" and re.search(str(target), str(value)) is None:
            return False
        if operator == "in" and value not in target:
            return False
        if operator == "not_in" and value in target:
            return False
        if operator == "gt" and not (value > target):
            return False
        if operator == "gte" and not (value >= target):
            return False
        if operator == "lt" and not (value < target):
            return False
        if operator == "lte" and not (value <= target):
            return False
        if operator == "is_null" and bool(target) != (value is None):
            return False
        if operator == "not_null" and bool(target) != (value is not None):
            return False
        if operator == "exists" and bool(target) != present:
            return False
        if operator == "has_any" and not set(target).intersection(value or []):
            return False
        if operator == "has_all" and not set(target).issubset(set(value or [])):
            return False
    return True


def matches_where(record: dict[str, Any], where: Any) -> bool:
    if not where:
        return True
    if not isinstance(where, dict):
        return False
    for key, condition in where.items():
        if key == "and":
            if not all(matches_where(record, part) for part in condition):
                return False
            continue
        if key == "or":
            if not any(matches_where(record, part) for part in condition):
                return False
            continue
        present, value = lookup(record, key)
        if not predicate(value, condition, present):
            return False
    return True


def matches_changes(diff_row: dict[str, Any], assertion: dict[str, Any]) -> bool:
    expected = assertion.get("expected_changes") or {}
    before = diff_row.get("before") or {}
    after = diff_row.get("after") or {}
    for field, transition in expected.items():
        if not isinstance(transition, dict):
            continue
        if "from" in transition:
            present, value = lookup(before, field)
            if not predicate(value, transition["from"], present):
                return False
        if "to" in transition:
            present, value = lookup(after, field)
            if not predicate(value, transition["to"], present):
                return False
    return True


def row_view(diff_kind: str, row: dict[str, Any]) -> dict[str, Any]:
    if diff_kind == "updates":
        merged = dict(row.get("before") or {})
        merged.update(row.get("after") or {})
        return merged
    return row


def changed_fields(row: dict[str, Any]) -> set[str]:
    before = row.get("before") or {}
    after = row.get("after") or {}
    return {str(key) for key in set(before).union(after) if before.get(key) != after.get(key)}


def ignored_fields(contract: dict[str, Any], entity: str, assertion: dict[str, Any] | None = None) -> set[str]:
    config = contract.get("ignore_fields") or {}
    values = set(config.get("global") or [])
    values.update(config.get(entity) or [])
    if assertion is not None:
        values.update(assertion.get("ignore") or [])
    return {snake(str(value)) for value in values}


def assertion_kind(assertion: dict[str, Any]) -> str:
    return {"added": "inserts", "changed": "updates", "removed": "deletes", "unchanged": "unchanged"}.get(
        str(assertion.get("diff_type")), "unknown"
    )


def conservative_extras(contract: dict[str, Any], diff: dict[str, Any]) -> list[dict[str, str]]:
    """Return only changes not explained by a positive assertion.

    Matching added/deleted records are treated as wholly expected, and broad predicates are
    allowed to explain every matching row. This intentionally under-counts extras.
    """
    extras: list[dict[str, str]] = []
    assertions = contract.get("assertions") or []
    for kind in ("inserts", "updates", "deletes"):
        for index, row in enumerate(diff.get(kind) or []):
            entity = str(row.get("__table__") or "UNKNOWN")
            view = row_view(kind, row)
            matching = [
                item
                for item in assertions
                if assertion_kind(item) == kind
                and str(item.get("entity")) == entity
                and matches_where(view, item.get("where"))
                and (kind != "updates" or matches_changes(row, item))
            ]
            if not matching:
                if kind == "updates":
                    changed = {snake(field) for field in changed_fields(row)}
                    if changed and changed.issubset(ignored_fields(contract, entity)):
                        continue
                extras.append(
                    {
                        "category": f"unasserted_{kind[:-1]}",
                        "signature": f"{kind}:{entity}",
                        "entity": entity,
                        "detail": f"row:{index}",
                    }
                )
                continue
            if kind != "updates":
                continue
            allowed: set[str] = set()
            ignored = ignored_fields(contract, entity)
            for assertion in matching:
                allowed.update(snake(str(field)) for field in (assertion.get("expected_changes") or {}))
                ignored.update(ignored_fields(contract, entity, assertion))
            for field in sorted(changed_fields(row)):
                normalized = snake(field)
                if normalized not in allowed and normalized not in ignored:
                    extras.append(
                        {
                            "category": "unexpected_update_field",
                            "signature": f"field:{entity}:{normalized}",
                            "entity": entity,
                            "detail": field,
                        }
                    )
    return extras


def synthetic_mutants(row: dict[str, Any], service_entities: dict[str, list[str]]) -> list[dict[str, str]]:
    contract = row["_contract"]
    assertions = contract.get("assertions") or []
    entity = str(assertions[0].get("entity")) if assertions else "UNKNOWN"
    alternatives = [item for item in service_entities[row["service"]] if item != entity]
    cross_entity = alternatives[0] if alternatives else f"{entity}_adjacent"
    ignored = sorted(ignored_fields(contract, entity))
    metadata_field = ignored[0] if ignored else "created_at"
    return [
        {"family": "same_entity_extra_record", "signature": f"inserts:{entity}", "risk": "risk"},
        {"family": "same_entity_unexpected_field", "signature": f"field:{entity}:mutation_probe_field", "risk": "risk"},
        {"family": "cross_entity_extra_record", "signature": f"inserts:{cross_entity}", "risk": "risk"},
        {"family": "extra_delete", "signature": f"deletes:{entity}", "risk": "risk"},
        {"family": "ignored_metadata_noise", "signature": f"field:{entity}:{metadata_field}", "risk": "benign"},
    ]


def main() -> int:
    started = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--train-jsonl", required=True)
    parser.add_argument("--test-jsonl", required=True)
    parser.add_argument("--checkpoint-json", required=True)
    parser.add_argument("--experiment-id", default="contract-mutation-screening-v001")
    arguments = parser.parse_args()
    output_dir = Path(arguments.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_jsonl(Path(arguments.train_jsonl), "train") + load_jsonl(Path(arguments.test_jsonl), "test")
    by_prompt = {row["question"]: row for row in rows}
    checkpoint = json.loads(Path(arguments.checkpoint_json).read_text(encoding="utf-8"))
    actual: list[dict[str, Any]] = []
    for result in checkpoint.get("results") or []:
        contract_row = by_prompt.get(result.get("prompt"))
        if contract_row is None:
            continue
        extras = conservative_extras(contract_row["_contract"], result.get("diff") or {})
        actual.append(
            {
                "test_id": contract_row["test_id"],
                "split": contract_row["_split"],
                "service": contract_row["service"],
                "task_horizon": contract_row["task_horizon"],
                "tools_required": contract_row["_info"].get("tools_required") or [],
                "passed": bool(result.get("passed")),
                "score": result.get("score"),
                "prompt": contract_row["question"],
                "extras": extras,
            }
        )

    allow_by_tool: dict[str, set[str]] = defaultdict(set)
    for item in actual:
        if item["split"] != "train" or not item["passed"]:
            continue
        for tool in item["tools_required"]:
            for extra in item["extras"]:
                allow_by_tool[str(tool)].add(extra["signature"])

    for item in actual:
        allowed = set()
        for tool in item["tools_required"]:
            allowed.update(allow_by_tool.get(str(tool), set()))
        item["unexplained_after_envelope"] = [extra for extra in item["extras"] if extra["signature"] not in allowed]

    service_entities: dict[str, list[str]] = {}
    for service in sorted({row["service"] for row in rows}):
        service_entities[service] = sorted(
            {
                str(assertion.get("entity"))
                for row in rows
                if row["service"] == service
                for assertion in row["_contract"].get("assertions") or []
            }
        )

    mutant_results: list[dict[str, Any]] = []
    for row in rows:
        if row["_split"] != "test":
            continue
        tools = [str(item) for item in row["_info"].get("tools_required") or []]
        allowed = set().union(*(allow_by_tool.get(tool, set()) for tool in tools)) if tools else set()
        for mutant in synthetic_mutants(row, service_entities):
            benign = mutant["risk"] == "benign"
            mutant_results.append(
                {
                    "test_id": row["test_id"],
                    "service": row["service"],
                    **mutant,
                    "original_accepts": True,
                    "global_strict_accepts": benign,
                    "endpoint_envelope_accepts": benign or mutant["signature"] in allowed,
                }
            )

    contracts_without_strict = sum("strict" not in row["_contract"] for row in rows)
    passed = [item for item in actual if item["passed"]]
    test_passed = [item for item in passed if item["split"] == "test"]
    passed_with_extras = [item for item in passed if item["extras"]]
    test_with_extras = [item for item in test_passed if item["extras"]]
    test_unexplained = [item for item in test_passed if item["unexplained_after_envelope"]]
    risk_mutants = [item for item in mutant_results if item["risk"] == "risk"]
    benign_mutants = [item for item in mutant_results if item["risk"] == "benign"]

    def rate(numerator: int, denominator: int) -> float:
        return numerator / denominator if denominator else 0.0

    by_extra_signature = Counter(extra["signature"] for item in passed for extra in item["extras"])
    summary = {
        "contract_count": len(rows),
        "assertion_count": sum(len(row["_contract"].get("assertions") or []) for row in rows),
        "contracts_without_explicit_strict": contracts_without_strict,
        "checkpoint_run_count": len(checkpoint.get("results") or []),
        "matched_checkpoint_run_count": len(actual),
        "passed_run_count": len(passed),
        "passed_with_conservative_unasserted_change_count": len(passed_with_extras),
        "passed_with_conservative_unasserted_change_rate": rate(len(passed_with_extras), len(passed)),
        "test_passed_run_count": len(test_passed),
        "test_global_strict_false_reject_count": len(test_with_extras),
        "test_global_strict_false_reject_rate": rate(len(test_with_extras), len(test_passed)),
        "test_endpoint_envelope_false_reject_count": len(test_unexplained),
        "test_endpoint_envelope_false_reject_rate": rate(len(test_unexplained), len(test_passed)),
        "original_risk_mutant_escape_rate": rate(sum(item["original_accepts"] for item in risk_mutants), len(risk_mutants)),
        "global_strict_risk_mutant_escape_rate": rate(sum(item["global_strict_accepts"] for item in risk_mutants), len(risk_mutants)),
        "endpoint_envelope_risk_mutant_escape_rate": rate(sum(item["endpoint_envelope_accepts"] for item in risk_mutants), len(risk_mutants)),
        "global_strict_benign_accept_rate": rate(sum(item["global_strict_accepts"] for item in benign_mutants), len(benign_mutants)),
        "endpoint_envelope_benign_accept_rate": rate(sum(item["endpoint_envelope_accepts"] for item in benign_mutants), len(benign_mutants)),
        "top_unasserted_signatures": by_extra_signature.most_common(20),
    }
    summary["screening"] = {
        "phenomenon_survives": bool(
            contracts_without_strict == len(rows)
            and summary["passed_with_conservative_unasserted_change_rate"] >= 0.05
        ),
        "prototype_hardening_survives": bool(
            summary["test_endpoint_envelope_false_reject_rate"]
            <= summary["test_global_strict_false_reject_rate"] - 0.10
            and summary["endpoint_envelope_risk_mutant_escape_rate"] <= 0.25
            and summary["endpoint_envelope_benign_accept_rate"] == 1.0
        ),
        "scope_note": "公开合同与一个公开检查点的筛选；保守额外变化检测会少报，且原通过运行不等于人工认证安全。",
    }

    records = [
        {"name": "contracts_without_explicit_strict_rate", "value": rate(contracts_without_strict, len(rows)), "unit": "ratio", "aggregation": "mean", "split": "all_contracts", "n": len(rows)},
        {"name": "checkpoint_prompt_match_rate", "value": rate(len(actual), len(checkpoint.get("results") or [])), "unit": "ratio", "aggregation": "mean", "split": "public_checkpoint", "n": len(checkpoint.get("results") or [])},
        {"name": "passed_with_conservative_unasserted_change_rate", "value": summary["passed_with_conservative_unasserted_change_rate"], "unit": "ratio", "aggregation": "mean", "split": "all_passed", "n": len(passed)},
        {"name": "false_reject_rate", "value": summary["test_global_strict_false_reject_rate"], "unit": "ratio", "aggregation": "mean", "split": "global_strict:test_passed", "n": len(test_passed)},
        {"name": "false_reject_rate", "value": summary["test_endpoint_envelope_false_reject_rate"], "unit": "ratio", "aggregation": "mean", "split": "endpoint_envelope:test_passed", "n": len(test_passed)},
        {"name": "risk_mutant_escape_rate", "value": summary["original_risk_mutant_escape_rate"], "unit": "ratio", "aggregation": "mean", "split": "original:test", "n": len(risk_mutants)},
        {"name": "risk_mutant_escape_rate", "value": summary["global_strict_risk_mutant_escape_rate"], "unit": "ratio", "aggregation": "mean", "split": "global_strict:test", "n": len(risk_mutants)},
        {"name": "risk_mutant_escape_rate", "value": summary["endpoint_envelope_risk_mutant_escape_rate"], "unit": "ratio", "aggregation": "mean", "split": "endpoint_envelope:test", "n": len(risk_mutants)},
        {"name": "benign_metadata_accept_rate", "value": summary["endpoint_envelope_benign_accept_rate"], "unit": "ratio", "aggregation": "mean", "split": "endpoint_envelope:test", "n": len(benign_mutants)},
        {"name": "phenomenon_survives_screen", "value": 1.0 if summary["screening"]["phenomenon_survives"] else 0.0, "unit": "boolean", "aggregation": "decision_rule", "split": "overall", "n": len(rows)},
        {"name": "prototype_hardening_survives_screen", "value": 1.0 if summary["screening"]["prototype_hardening_survives"] else 0.0, "unit": "boolean", "aggregation": "decision_rule", "split": "overall", "n": len(rows)},
    ]
    metrics = {
        "schema_version": 1,
        "experiment_id": arguments.experiment_id,
        "records": records,
        "resource_usage": {
            "api_calls": 0,
            "tokens": 0,
            "wall_time_seconds": time.perf_counter() - started,
            "gpu_time_seconds": 0.0,
            "estimated_cost": 0.0,
        },
        "warnings": [
            "actual_passed_is_not_human_safety_label",
            "conservative_extra_detector_under_counts_broad_assertions",
            "single_public_checkpoint_only",
        ],
        "errors": [],
    }
    details = {
        "summary": summary,
        "actual_runs": actual,
        "synthetic_mutants": mutant_results,
        "learned_allow_by_tool": {key: sorted(value) for key, value in sorted(allow_by_tool.items())},
    }
    (output_dir / "results.json").write_text(json.dumps(details, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (output_dir / "metrics-output.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
