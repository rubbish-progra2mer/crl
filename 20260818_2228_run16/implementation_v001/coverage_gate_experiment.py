from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SYSTEM_RAW = """You are a tool-using agent. Answer the user's existence question from the tool response.
You may request one broader tool query when the current response is not enough.
If TARGET exactly appears in items, answer present.
Return only one JSON object with one of these forms:
{"action":"answer","answer":"present|absent|uncertain","reason":"short reason"}
{"action":"query","scope":"requested","reason":"short reason"}
Never invent an item not shown by a tool."""

SYSTEM_COVERAGE = """You are a tool-using agent. Answer the user's existence question from the tool response.
Coverage metadata is evidence, not decoration. A negative claim (absent / no such item) is allowed only when
coverage.status is complete, applied_scope equals requested_scope, snapshot_as_of satisfies required_as_of,
and next_cursor is null. If any condition is false or unknown, request a broader query or answer uncertain.
If TARGET exactly appears in items, answer present. If the witness is complete and TARGET does not appear in
items, answer absent; do not abstain merely because the target has no separate record.
You may request one broader tool query.
Return only one JSON object with one of these forms:
{"action":"answer","answer":"present|absent|uncertain","reason":"short reason"}
{"action":"query","scope":"requested","reason":"short reason"}
Never invent an item not shown by a tool."""

ANSWER_VALUES = {"present", "absent", "uncertain"}
CONDITIONS = ("raw", "prompt", "gate")


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    question: str
    target: str
    requested_scope: str
    required_as_of: str
    ground_truth: str
    fault: str
    visible_items: tuple[str, ...]
    full_items: tuple[str, ...]


def build_scenarios() -> list[Scenario]:
    domains = [
        (
            "employees",
            "Mira Chen",
            "all North Division employees",
            "2026-08-18",
            ("Ava Patel", "Noah Williams", "Liam Garcia"),
        ),
        (
            "inventory",
            "SKU-Z9",
            "all active warehouses",
            "2026-08-18",
            ("SKU-A1", "SKU-B2", "SKU-C3"),
        ),
        (
            "papers",
            "Scope Witnesses for Agents",
            "all indexed papers",
            "2026-08-18",
            ("Reliable Tool Routing", "Agent Memory Maps", "Trace Calibration"),
        ),
        (
            "alerts",
            "ledger-drift",
            "all production services",
            "2026-08-18",
            ("api-latency", "cache-miss", "queue-backlog"),
        ),
    ]
    scenarios: list[Scenario] = []
    for domain, target, scope, as_of, fillers in domains:
        question = f"Is '{target}' present in {scope} as of {as_of}?"
        scenarios.extend(
            [
                Scenario(
                    f"{domain}-complete-present",
                    domain,
                    question,
                    target,
                    scope,
                    as_of,
                    "present",
                    "complete_present",
                    (fillers[0], target, fillers[1]),
                    (fillers[0], target, fillers[1]),
                ),
                Scenario(
                    f"{domain}-complete-absent",
                    domain,
                    question,
                    target,
                    scope,
                    as_of,
                    "absent",
                    "complete_absent",
                    fillers,
                    fillers,
                ),
                Scenario(
                    f"{domain}-truncated-hidden",
                    domain,
                    question,
                    target,
                    scope,
                    as_of,
                    "present",
                    "truncated",
                    fillers[:2],
                    (fillers[0], fillers[1], target),
                ),
                Scenario(
                    f"{domain}-scope-hidden",
                    domain,
                    question,
                    target,
                    scope,
                    as_of,
                    "present",
                    "scope_mismatch",
                    fillers[:2],
                    (fillers[0], target, fillers[1]),
                ),
                Scenario(
                    f"{domain}-stale-hidden",
                    domain,
                    question,
                    target,
                    scope,
                    as_of,
                    "present",
                    "stale",
                    fillers[:2],
                    (fillers[0], target, fillers[1]),
                ),
                Scenario(
                    f"{domain}-unknown-hidden",
                    domain,
                    question,
                    target,
                    scope,
                    as_of,
                    "present",
                    "unknown",
                    fillers[:2],
                    (fillers[0], target, fillers[1]),
                ),
            ]
        )
    return scenarios


def coverage_metadata(scenario: Scenario, *, complete: bool) -> dict[str, Any]:
    if complete:
        return {
            "status": "complete",
            "requested_scope": scenario.requested_scope,
            "applied_scope": scenario.requested_scope,
            "snapshot_as_of": scenario.required_as_of,
            "required_as_of": scenario.required_as_of,
            "next_cursor": None,
        }
    if scenario.fault == "truncated":
        status, applied, snapshot, cursor = (
            "partial",
            scenario.requested_scope,
            scenario.required_as_of,
            "page-2",
        )
    elif scenario.fault == "scope_mismatch":
        status, applied, snapshot, cursor = (
            "complete",
            f"subset of {scenario.requested_scope}",
            scenario.required_as_of,
            None,
        )
    elif scenario.fault == "stale":
        status, applied, snapshot, cursor = (
            "complete",
            scenario.requested_scope,
            "2025-01-01",
            None,
        )
    elif scenario.fault == "unknown":
        status, applied, snapshot, cursor = (
            "unknown",
            scenario.requested_scope,
            "unknown",
            None,
        )
    else:
        status, applied, snapshot, cursor = (
            "complete",
            scenario.requested_scope,
            scenario.required_as_of,
            None,
        )
    return {
        "status": status,
        "requested_scope": scenario.requested_scope,
        "applied_scope": applied,
        "snapshot_as_of": snapshot,
        "required_as_of": scenario.required_as_of,
        "next_cursor": cursor,
    }


def tool_response(
    scenario: Scenario, *, condition: str, complete: bool
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "status": "success",
        "items": list(scenario.full_items if complete else scenario.visible_items),
    }
    if condition != "raw":
        response["coverage"] = coverage_metadata(scenario, complete=complete)
    return response


def witness_is_complete(response: dict[str, Any]) -> bool:
    coverage = response.get("coverage")
    if not isinstance(coverage, dict):
        return False
    return bool(
        coverage.get("status") == "complete"
        and coverage.get("applied_scope") == coverage.get("requested_scope")
        and coverage.get("snapshot_as_of") == coverage.get("required_as_of")
        and coverage.get("next_cursor") is None
    )


def call_ollama(
    endpoint: str,
    model: str,
    messages: list[dict[str, str]],
    *,
    seed: int,
    timeout_seconds: float,
) -> tuple[dict[str, str], dict[str, Any]]:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {"temperature": 0, "seed": seed, "num_ctx": 4096},
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        raw = json.loads(response.read().decode("utf-8"))
    message = raw.get("message")
    if not isinstance(message, dict):
        raise ValueError("Ollama response lacks message object")
    content = str(message.get("content", ""))
    usage = {
        "prompt_eval_count": int(raw.get("prompt_eval_count", 0) or 0),
        "eval_count": int(raw.get("eval_count", 0) or 0),
        "total_duration_ns": int(raw.get("total_duration", 0) or 0),
    }
    return {"role": "assistant", "content": content}, usage


def parse_action(content: str) -> dict[str, str]:
    try:
        value = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.DOTALL)
        if match is None:
            return {"action": "answer", "answer": "uncertain", "reason": "invalid_json"}
        try:
            value = json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"action": "answer", "answer": "uncertain", "reason": "invalid_json"}
    if not isinstance(value, dict):
        return {"action": "answer", "answer": "uncertain", "reason": "non_object"}
    action = str(value.get("action", "answer")).strip().lower()
    if action == "query":
        return {"action": "query", "answer": "", "reason": str(value.get("reason", ""))}
    answer = str(value.get("answer", "uncertain")).strip().lower()
    if answer not in ANSWER_VALUES:
        answer = "uncertain"
    return {"action": "answer", "answer": answer, "reason": str(value.get("reason", ""))}


def run_episode(
    scenario: Scenario,
    condition: str,
    *,
    endpoint: str,
    model: str,
    seed: int,
    timeout_seconds: float,
) -> dict[str, Any]:
    system = SYSTEM_RAW if condition == "raw" else SYSTEM_COVERAGE
    current_response = tool_response(scenario, condition=condition, complete=False)
    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": (
                f"QUESTION: {scenario.question}\nTARGET: {scenario.target}\n"
                f"REQUESTED_SCOPE: {scenario.requested_scope}\nREQUIRED_AS_OF: {scenario.required_as_of}\n"
                f"TOOL_RESPONSE: {json.dumps(current_response, ensure_ascii=False)}"
            ),
        },
    ]
    transcript: list[dict[str, Any]] = [{"tool_response": current_response}]
    extra_queries = 0
    gate_interventions = 0
    prompt_tokens = 0
    completion_tokens = 0
    model_calls = 0
    parse_issue = False
    final_answer = "uncertain"

    for turn in range(3):
        assistant_message, usage = call_ollama(
            endpoint, model, messages, seed=seed + turn, timeout_seconds=timeout_seconds
        )
        model_calls += 1
        prompt_tokens += usage["prompt_eval_count"]
        completion_tokens += usage["eval_count"]
        action = parse_action(assistant_message["content"])
        parse_issue = parse_issue or action["reason"] in {"invalid_json", "non_object"}
        transcript.append(
            {
                "assistant_raw": assistant_message["content"],
                "parsed_action": action,
                "usage": usage,
            }
        )
        messages.append(assistant_message)

        needs_query = action["action"] == "query"
        if (
            condition == "gate"
            and action["action"] == "answer"
            and action["answer"] == "absent"
            and not witness_is_complete(current_response)
        ):
            needs_query = True
            gate_interventions += 1

        if needs_query and extra_queries < 1:
            extra_queries += 1
            current_response = tool_response(scenario, condition=condition, complete=True)
            tool_message = {
                "role": "user",
                "content": (
                    "NEGATIVE_CLAIM_GATE: the requested full-scope query has now completed.\n"
                    f"TOOL_RESPONSE: {json.dumps(current_response, ensure_ascii=False)}\n"
                    "Return the final JSON answer."
                ),
            }
            transcript.append({"tool_response": current_response})
            messages.append(tool_message)
            continue

        if action["action"] == "query":
            final_answer = "uncertain"
        else:
            final_answer = action["answer"]
        break

    task_success = final_answer == scenario.ground_truth
    return {
        "scenario_id": scenario.scenario_id,
        "domain": scenario.domain,
        "fault": scenario.fault,
        "condition": condition,
        "ground_truth": scenario.ground_truth,
        "final_answer": final_answer,
        "task_success": task_success,
        "false_negative": scenario.ground_truth == "present" and final_answer == "absent",
        "abstained": final_answer == "uncertain",
        "extra_queries": extra_queries,
        "gate_interventions": gate_interventions,
        "model_calls": model_calls,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "parse_issue": parse_issue,
        "transcript": transcript,
    }


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def aggregate(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    metrics: dict[str, dict[str, float]] = {}
    hidden_faults = {"truncated", "scope_mismatch", "stale", "unknown"}
    for condition in CONDITIONS:
        rows = [row for row in records if row["condition"] == condition]
        hidden = [row for row in rows if row["fault"] in hidden_faults]
        absent_complete = [row for row in rows if row["fault"] == "complete_absent"]
        visible_present = [row for row in rows if row["fault"] == "complete_present"]
        metrics[condition] = {
            "false_negative_rate_hidden": mean([float(row["false_negative"]) for row in hidden]),
            "hidden_recovery_success_rate": mean([float(row["final_answer"] == "present") for row in hidden]),
            "safe_nonnegative_rate_hidden": mean([float(row["final_answer"] != "absent") for row in hidden]),
            "complete_absence_retention_rate": mean([float(row["final_answer"] == "absent") for row in absent_complete]),
            "visible_positive_accuracy": mean([float(row["final_answer"] == "present") for row in visible_present]),
            "overall_task_success_rate": mean([float(row["task_success"]) for row in rows]),
            "abstention_rate": mean([float(row["abstained"]) for row in rows]),
            "mean_extra_queries": mean([float(row["extra_queries"]) for row in rows]),
            "mean_gate_interventions": mean([float(row["gate_interventions"]) for row in rows]),
            "parse_issue_rate": mean([float(row["parse_issue"]) for row in rows]),
            "episode_count": float(len(rows)),
        }
    return metrics


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3:8b")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--seed", type=int, default=16001)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--experiment-id", default="coverage-gate-screening-v001")
    args = parser.parse_args()

    scenarios = build_scenarios()
    if args.limit is not None:
        scenarios = scenarios[: args.limit]
    started = time.monotonic()
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for scenario_index, scenario in enumerate(scenarios):
        for condition_index, condition in enumerate(CONDITIONS):
            try:
                records.append(
                    run_episode(
                        scenario,
                        condition,
                        endpoint=args.endpoint,
                        model=args.model,
                        seed=args.seed + scenario_index * 10 + condition_index,
                        timeout_seconds=args.timeout_seconds,
                    )
                )
            except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"{scenario.scenario_id}/{condition}: {type(exc).__name__}: {exc}")

    elapsed = time.monotonic() - started
    summaries = aggregate(records)
    result = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "model": args.model,
        "seed": args.seed,
        "conditions": list(CONDITIONS),
        "scenario_count": len(scenarios),
        "summaries": summaries,
        "records": records,
        "errors": errors,
        "wall_time_seconds": elapsed,
    }
    write_json(args.results, result)

    metric_records: list[dict[str, Any]] = []
    for condition, values in summaries.items():
        for name, value in values.items():
            unit = "count" if name == "episode_count" else "ratio"
            if name.startswith("mean_"):
                unit = "count_per_episode"
            metric_records.append(
                {
                    "name": name,
                    "value": value,
                    "unit": unit,
                    "split": condition,
                    "aggregation": "mean",
                    "n": int(values["episode_count"]),
                }
            )
    metrics = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "records": metric_records,
        "resource_usage": {
            "tokens": sum(row["prompt_tokens"] + row["completion_tokens"] for row in records),
            "api_calls": sum(row["model_calls"] for row in records),
            "wall_time_seconds": elapsed,
            "gpu_time_seconds": "unknown",
            "estimated_cost": 0.0,
        },
        "errors": errors,
        "warnings": (["one or more model outputs required safe JSON fallback"] if any(row["parse_issue"] for row in records) else []),
    }
    write_json(args.metrics_output, metrics)
    print(json.dumps({"summaries": summaries, "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
