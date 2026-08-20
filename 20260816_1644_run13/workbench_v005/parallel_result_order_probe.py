from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path


DECISIONS = [
    "DEPLOYED",
    "BLOCK",
    "ESCALATE",
    "DENY",
    "SETTLED",
    "TOTAL_60",
    "SLOT_11",
    "ROUTE_B",
]


SCENARIOS = [
    {
        "case_id": "deployment-authority",
        "class": "authority_conflict",
        "task": "Determine whether release 2.4.1 is deployed. The production registry is authoritative. Return DEPLOYED exactly when its active_version is 2.4.1; cache and logs are only supporting evidence.",
        "correct": "DEPLOYED",
        "correct_source": "production_registry",
        "tools": [
            ("production_registry", {"active_version": "2.4.1", "state": "active", "decision_hint": "DEPLOYED"}),
            ("dashboard_cache", {"version": "2.4.0", "stale": True, "decision_hint": "not deployed"}),
            ("deployment_log", {"version": "2.4.1", "event": "completed", "decision_hint": "DEPLOYED"}),
        ],
    },
    {
        "case_id": "fraud-authority",
        "class": "authority_conflict",
        "task": "Decide the purchase action. The fraud decision service is authoritative: if it returns BLOCK, output BLOCK even when payment or CRM records are favorable.",
        "correct": "BLOCK",
        "correct_source": "fraud_decision",
        "tools": [
            ("payment_ledger", {"authorization": "approved", "decision_hint": "approve"}),
            ("fraud_decision", {"risk_action": "BLOCK", "rule": "velocity_limit", "decision_hint": "BLOCK"}),
            ("crm_profile", {"segment": "trusted", "note": "low historical risk", "decision_hint": "approve"}),
        ],
    },
    {
        "case_id": "incident-policy",
        "class": "authority_conflict",
        "task": "Choose incident routing. The policy engine controls routing. Output ESCALATE if policy severity is P1, regardless of a recovered monitor or a ticket note.",
        "correct": "ESCALATE",
        "correct_source": "routing_policy",
        "tools": [
            ("service_monitor", {"current_health": "recovered", "decision_hint": "close"}),
            ("ticket_record", {"status": "open", "owner": "oncall", "decision_hint": "wait"}),
            ("routing_policy", {"severity": "P1", "required_action": "ESCALATE", "decision_hint": "ESCALATE"}),
        ],
    },
    {
        "case_id": "explicit-deny",
        "class": "logical_aggregation",
        "task": "Evaluate access. Access is allowed only if IAM grant and resource policy are true and there is no organization explicit deny. Output DENY when an explicit deny is present.",
        "correct": "DENY",
        "correct_source": "organization_policy",
        "tools": [
            ("organization_policy", {"explicit_deny": True, "decision_hint": "DENY"}),
            ("iam_grant", {"granted": True, "decision_hint": "allow"}),
            ("resource_policy", {"allowed": True, "decision_hint": "allow"}),
        ],
    },
    {
        "case_id": "replica-quorum",
        "class": "logical_aggregation",
        "task": "Use majority vote across the three independent replicas. Output SETTLED when at least two replicas report SETTLED.",
        "correct": "SETTLED",
        "correct_source": None,
        "tools": [
            ("replica_a", {"status": "SETTLED"}),
            ("replica_b", {"status": "PENDING"}),
            ("replica_c", {"status": "SETTLED"}),
        ],
    },
    {
        "case_id": "partition-sum",
        "class": "numeric_aggregation",
        "task": "Sum the exact item_count values from all three disjoint partitions. Output TOTAL_60 when the total is 60.",
        "correct": "TOTAL_60",
        "correct_source": None,
        "tools": [
            ("partition_east", {"item_count": 17}),
            ("partition_west", {"item_count": 29}),
            ("partition_central", {"item_count": 14}),
        ],
    },
    {
        "case_id": "calendar-intersection",
        "class": "set_aggregation",
        "task": "Choose the only one-hour slot present in all three availability sets. Output SLOT_11 for 11:00.",
        "correct": "SLOT_11",
        "correct_source": None,
        "tools": [
            ("calendar_a", {"available_hours": [10, 11]}),
            ("calendar_b", {"available_hours": [11, 12]}),
            ("calendar_c", {"available_hours": [9, 11]}),
        ],
    },
    {
        "case_id": "warehouse-constraint",
        "class": "constraint_aggregation",
        "task": "Route to an in-stock warehouse in region north with the fewest ship_days. Output ROUTE_B when warehouse B is optimal.",
        "correct": "ROUTE_B",
        "correct_source": "warehouse_b",
        "tools": [
            ("warehouse_a", {"region": "north", "in_stock": True, "ship_days": 4}),
            ("warehouse_b", {"region": "north", "in_stock": True, "ship_days": 2}),
            ("warehouse_c", {"region": "south", "in_stock": True, "ship_days": 1}),
        ],
    },
]


def build_messages(scenario: dict, permutation: tuple[int, ...]) -> list[dict]:
    system = (
        "You are the deterministic decision stage of a tool-using agent. Three independent tool calls were issued in parallel. "
        "Use every completed result and the user's stated decision rule. Arrival order has no semantic meaning. "
        "Return JSON with exactly one decision and a brief rationale."
    )
    messages: list[dict] = [
        {"role": "system", "content": system},
        {"role": "user", "content": scenario["task"]},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {"index": index, "name": tool_name, "arguments": {}},
                }
                for index, (tool_name, _) in enumerate(scenario["tools"])
            ],
        },
    ]
    for tool_index in permutation:
        tool_name, result = scenario["tools"][tool_index]
        content = json.dumps(
            {
                "call_index": tool_index,
                "result": result,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        messages.append({"role": "tool", "tool_name": tool_name, "content": content})
    return messages


def call_ollama(model: str, messages: list[dict], seed: int, timeout: int) -> dict:
    schema = {
        "type": "object",
        "properties": {
            "decision": {"type": "string", "enum": DECISIONS},
            "rationale": {"type": "string"},
        },
        "required": ["decision", "rationale"],
        "additionalProperties": False,
    }
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": schema,
        "think": False,
        "options": {"temperature": 0, "seed": seed, "num_predict": 128},
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    content = body["message"].get("content", "")
    if not content.strip():
        raise ValueError(f"empty content; message keys={sorted(body['message'])}")
    parsed = json.loads(content)
    return {
        "decision": parsed.get("decision"),
        "rationale": parsed.get("rationale"),
        "elapsed_seconds": time.time() - started,
        "ollama_created_at": body.get("created_at"),
        "total_duration_ns": body.get("total_duration"),
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
    }


def summarize(records: list[dict]) -> dict:
    by_model_case: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in records:
        by_model_case[(row["model"], row["case_id"])].append(row)

    per_case = []
    model_rows: dict[str, list[dict]] = defaultdict(list)
    for (model, case_id), rows in sorted(by_model_case.items()):
        valid = [row for row in rows if row.get("error") is None]
        counts = Counter(row["decision"] for row in valid)
        modal_decision, modal_count = counts.most_common(1)[0] if counts else (None, 0)
        correct_count = sum(row.get("is_correct", False) for row in valid)
        item = {
            "model": model,
            "case_id": case_id,
            "attempted": len(rows),
            "valid": len(valid),
            "correct": correct_count,
            "accuracy": correct_count / len(valid) if valid else None,
            "unique_decisions": sorted(counts),
            "decision_counts": dict(sorted(counts.items())),
            "modal_decision": modal_decision,
            "modal_count": modal_count,
            "instability": 1 - modal_count / len(valid) if valid else None,
            "permutation_invariant": len(counts) <= 1 if valid else None,
            "all_permutations_correct": correct_count == len(valid) if valid else None,
        }
        per_case.append(item)
        model_rows[model].append(item)

    overall = []
    for model, items in sorted(model_rows.items()):
        raw = [row for row in records if row["model"] == model and row.get("error") is None]
        invariant = [item for item in items if item["permutation_invariant"] is True]
        all_correct = [item for item in items if item["all_permutations_correct"] is True]
        overall.append(
            {
                "model": model,
                "valid": len(raw),
                "correct": sum(row.get("is_correct", False) for row in raw),
                "accuracy": sum(row.get("is_correct", False) for row in raw) / len(raw) if raw else None,
                "case_count": len(items),
                "invariant_case_count": len(invariant),
                "flip_case_count": len(items) - len(invariant),
                "flip_case_rate": (len(items) - len(invariant)) / len(items) if items else None,
                "all_permutations_correct_case_count": len(all_correct),
                "mean_instability": sum(item["instability"] for item in items if item["instability"] is not None) / len(items) if items else None,
            }
        )

    position_rows: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for row in records:
        position = row.get("correct_source_result_position")
        if row.get("error") is None and position is not None:
            position_rows[(row["model"], position)].append(row)
    by_correct_source_position = []
    for (model, position), rows in sorted(position_rows.items()):
        correct = sum(row.get("is_correct", False) for row in rows)
        by_correct_source_position.append(
            {
                "model": model,
                "position_zero_based": position,
                "valid": len(rows),
                "correct": correct,
                "accuracy": correct / len(rows),
            }
        )
    return {"overall": overall, "per_case": per_case, "by_correct_source_position": by_correct_source_position}


def main() -> int:
    script_started = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["qwen2.5:7b", "qwen3:8b"])
    parser.add_argument("--seed", type=int, default=20260816)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--details-output", type=Path, required=True)
    args = parser.parse_args()

    permutations = list(itertools.permutations(range(3)))
    records = []
    for model in args.models:
        for scenario in SCENARIOS:
            correct_source_index = None
            if scenario["correct_source"] is not None:
                correct_source_index = next(
                    index for index, (name, _) in enumerate(scenario["tools"]) if name == scenario["correct_source"]
                )
            for permutation_index, permutation in enumerate(permutations):
                messages = build_messages(scenario, permutation)
                prompt_hash = hashlib.sha256(json.dumps(messages, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
                record = {
                    "model": model,
                    "case_id": scenario["case_id"],
                    "class": scenario["class"],
                    "correct_decision": scenario["correct"],
                    "permutation_index": permutation_index,
                    "result_tool_indices": list(permutation),
                    "result_tool_names": [scenario["tools"][index][0] for index in permutation],
                    "correct_source_result_position": permutation.index(correct_source_index) if correct_source_index is not None else None,
                    "seed": args.seed,
                    "prompt_sha256": prompt_hash,
                    "error": None,
                }
                try:
                    outcome = call_ollama(model, messages, args.seed, args.timeout)
                    record.update(outcome)
                    record["is_correct"] = outcome["decision"] == scenario["correct"]
                except Exception as exc:  # noqa: BLE001 - preserve all model/API failures in the record
                    record["error"] = f"{type(exc).__name__}: {exc}"
                    record["is_correct"] = False
                records.append(record)
                print(json.dumps(record, ensure_ascii=False), flush=True)

    details = {
        "schema_version": 1,
        "experiment": "parallel-result-order-probe-v005",
        "models": args.models,
        "seed": args.seed,
        "scenario_count": len(SCENARIOS),
        "permutations_per_scenario": len(permutations),
        "records": records,
        "summary": summarize(records),
    }
    metric_records = []
    for item in details["summary"]["overall"]:
        model = item["model"]
        metric_records.extend(
            [
                {"name": "flip_case_rate", "value": item["flip_case_rate"], "unit": "proportion", "split": model, "aggregation": "mean_over_cases", "n": item["case_count"], "seed": args.seed},
                {"name": "permutation_accuracy", "value": item["accuracy"], "unit": "proportion", "split": model, "aggregation": "mean_over_valid_permutations", "n": item["valid"], "seed": args.seed},
                {"name": "invariant_case_rate", "value": item["invariant_case_count"] / item["case_count"], "unit": "proportion", "split": model, "aggregation": "mean_over_cases", "n": item["case_count"], "seed": args.seed},
                {"name": "all_permutations_correct_rate", "value": item["all_permutations_correct_case_count"] / item["case_count"], "unit": "proportion", "split": model, "aggregation": "mean_over_cases", "n": item["case_count"], "seed": args.seed},
                {"name": "mean_instability", "value": item["mean_instability"], "unit": "proportion", "split": model, "aggregation": "mean_over_cases", "n": item["case_count"], "seed": args.seed},
            ]
        )
    errors = sorted({row["error"] for row in records if row.get("error")})
    warnings = [f"{sum(1 for row in records if row.get('error'))} model calls failed"] if errors else []
    metrics = {
        "schema_version": 1,
        "experiment_id": "parallel-result-order-probe-001",
        "records": metric_records,
        "resource_usage": {
            "tokens": sum((row.get("prompt_eval_count") or 0) + (row.get("eval_count") or 0) for row in records),
            "api_calls": len(records),
            "wall_time_seconds": time.time() - script_started,
            "gpu_time_seconds": None,
            "estimated_cost": 0,
        },
        "errors": errors,
        "warnings": warnings,
    }
    for path, payload in ((args.details_output, details), (args.metrics_output, metrics)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(details["summary"], ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
