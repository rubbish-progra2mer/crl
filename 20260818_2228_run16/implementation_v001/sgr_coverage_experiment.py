from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TASK_IDS = (
    "arxiv_001",
    "census_001",
    "climategov_011",
    "comptox_010",
    "consumerfinance_008",
    "europemc_001",
    "genome_001",
    "nvd_001",
    "reptile_001",
    "wateroffice_001",
    "waterquality_001",
    "wonder_003",
)
CONDITIONS = ("receipt", "postcondition", "gate")
ANSWERS = {"present", "absent", "uncertain"}

SYSTEM_RECEIPT = """You are a tool-using retrieval agent. The signed receipt proves the exact tool output and result_count.
Use the listed items to answer whether TARGET belongs to the complete qualifying answer set. You may request one
broader query if needed. Return only JSON:
{"action":"answer","answer":"present|absent|uncertain","reason":"short"}
or {"action":"query","reason":"short"}. If TARGET is listed, answer present. Never invent an item."""

SYSTEM_POSTCONDITION = """You are a tool-using retrieval agent. The signed receipt proves the exact output, while
coverage proves whether the observation spans the requested qualifying answer set. If TARGET is listed, answer present.
Answer absent only when coverage.status is complete, applied_scope_id equals requested_scope_id, and next_cursor is null.
Otherwise request one broader query or answer uncertain. Return only JSON:
{"action":"answer","answer":"present|absent|uncertain","reason":"short"}
or {"action":"query","reason":"short"}. Never invent an item."""


@dataclass(frozen=True)
class NaturalTask:
    task_id: str
    domain: str
    instruction: str
    criteria: tuple[str, ...]
    keys: tuple[str, ...]
    scope_id: str


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    task: NaturalTask
    target: str
    ground_truth: str
    mode: str


def _parse_json_object(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if not isinstance(value, str):
        return {}
    parsed = json.loads(value)
    return parsed if isinstance(parsed, dict) else {}


def _answer_records(item: dict[str, Any]) -> list[str]:
    answer = str(item.get("oracle_answer", "")).strip()
    cardinality = int(item.get("oracle_output_cardinality", 0) or 0)
    rubric = _parse_json_object(item.get("rubric"))
    normalization = rubric.get("normalization", {})
    if not isinstance(normalization, dict):
        normalization = {}
    separator = str(normalization.get("record_separator", "\n"))
    if separator == "\\n":
        separator = "\n"
    records = [part.strip() for part in answer.split(separator) if part.strip()]
    if cardinality > 0 and len(records) > cardinality:
        records = records[-cardinality:]
    if len(records) < 2 and cardinality > 1:
        records = [part.strip() for part in answer.split(",") if part.strip()]
    return records


def load_tasks(path: Path) -> list[NaturalTask]:
    selected: dict[str, NaturalTask] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        task_id = str(item.get("task_id", ""))
        if task_id not in TASK_IDS:
            continue
        metadata = _parse_json_object(item.get("metadata"))
        criteria_value = metadata.get("State-Gated Retrieval", [])
        criteria = tuple(str(value) for value in criteria_value) if isinstance(criteria_value, list) else ()
        records = _answer_records(item)
        keys: list[str] = []
        for record in records:
            key = record.split("|", 1)[0].strip()
            if key and key not in keys:
                keys.append(key)
        if len(keys) < 2:
            continue
        scope_payload = json.dumps(criteria, ensure_ascii=False, sort_keys=True)
        scope_id = hashlib.sha256(scope_payload.encode("utf-8")).hexdigest()[:16]
        selected[task_id] = NaturalTask(
            task_id=task_id,
            domain=str(item.get("domain", "unknown")),
            instruction=str(item.get("instruction", "")),
            criteria=criteria,
            keys=tuple(keys),
            scope_id=scope_id,
        )
    tasks = [selected[task_id] for task_id in TASK_IDS if task_id in selected]
    if len(tasks) < 8:
        raise ValueError(f"too few parseable SGR tasks: {len(tasks)}")
    return tasks


def build_scenarios(tasks: list[NaturalTask]) -> list[Scenario]:
    scenarios: list[Scenario] = []
    for task in tasks:
        scenarios.extend(
            [
                Scenario(f"{task.task_id}-hidden", task, task.keys[-1], "present", "hidden"),
                Scenario(f"{task.task_id}-visible", task, task.keys[0], "present", "visible"),
                Scenario(
                    f"{task.task_id}-absent",
                    task,
                    f"ABSENT-{task.task_id.upper()}",
                    "absent",
                    "complete_absent",
                ),
            ]
        )
    return scenarios


def response_for(scenario: Scenario, condition: str, *, complete: bool) -> dict[str, Any]:
    keys = list(scenario.task.keys)
    if complete or scenario.mode == "complete_absent":
        visible = keys
        is_complete = True
    elif scenario.mode == "visible":
        visible = keys[: max(1, len(keys) // 2)]
        is_complete = False
    else:
        visible = keys[: max(1, len(keys) - 1)]
        is_complete = False
    canonical = json.dumps(visible, ensure_ascii=False, sort_keys=True).encode("utf-8")
    value: dict[str, Any] = {
        "status": "success",
        "items": visible,
        "receipt": {
            "result_count": len(visible),
            "output_sha256": hashlib.sha256(canonical).hexdigest(),
            "signature_status": "valid",
        },
    }
    if condition != "receipt":
        value["coverage"] = {
            "status": "complete" if is_complete else "partial",
            "requested_scope_id": scenario.task.scope_id,
            "applied_scope_id": scenario.task.scope_id,
            "next_cursor": None if is_complete else "next-page",
        }
    return value


def witness_complete(response: dict[str, Any]) -> bool:
    coverage = response.get("coverage")
    return bool(
        isinstance(coverage, dict)
        and coverage.get("status") == "complete"
        and coverage.get("requested_scope_id") == coverage.get("applied_scope_id")
        and coverage.get("next_cursor") is None
    )


def call_model(
    endpoint: str,
    model: str,
    messages: list[dict[str, str]],
    seed: int,
    timeout: float,
) -> tuple[dict[str, str], dict[str, int]]:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {"temperature": 0, "seed": seed, "num_ctx": 6144},
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = json.loads(response.read().decode("utf-8"))
    message = raw.get("message")
    if not isinstance(message, dict):
        raise ValueError("model response lacks message")
    return (
        {"role": "assistant", "content": str(message.get("content", ""))},
        {
            "prompt": int(raw.get("prompt_eval_count", 0) or 0),
            "completion": int(raw.get("eval_count", 0) or 0),
        },
    )


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
    if str(value.get("action", "answer")).lower() == "query":
        return {"action": "query", "answer": "", "reason": str(value.get("reason", ""))}
    answer = str(value.get("answer", "uncertain")).lower()
    if answer not in ANSWERS:
        answer = "uncertain"
    return {"action": "answer", "answer": answer, "reason": str(value.get("reason", ""))}


def run_episode(
    scenario: Scenario,
    condition: str,
    *,
    endpoint: str,
    model: str,
    seed: int,
    timeout: float,
) -> dict[str, Any]:
    system = SYSTEM_RECEIPT if condition == "receipt" else SYSTEM_POSTCONDITION
    current = response_for(scenario, condition, complete=False)
    criteria = " | ".join(scenario.task.criteria[:4])
    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": (
                f"TASK_ID: {scenario.task.task_id}\nDOMAIN: {scenario.task.domain}\n"
                f"TARGET: {scenario.target}\nQUALIFYING_CRITERIA: {criteria}\n"
                f"TOOL_RESPONSE: {json.dumps(current, ensure_ascii=False)}"
            ),
        },
    ]
    transcript: list[dict[str, Any]] = [{"tool_response": current}]
    extra_queries = 0
    interventions = 0
    prompt_tokens = 0
    completion_tokens = 0
    model_calls = 0
    parse_issue = False
    final = "uncertain"
    for turn in range(3):
        assistant, usage = call_model(endpoint, model, messages, seed + turn, timeout)
        model_calls += 1
        prompt_tokens += usage["prompt"]
        completion_tokens += usage["completion"]
        action = parse_action(assistant["content"])
        parse_issue = parse_issue or action["reason"] in {"invalid_json", "non_object"}
        transcript.append({"assistant_raw": assistant["content"], "parsed_action": action, "usage": usage})
        messages.append(assistant)
        needs_query = action["action"] == "query"
        if (
            condition == "gate"
            and action["action"] == "answer"
            and action["answer"] == "absent"
            and not witness_complete(current)
        ):
            needs_query = True
            interventions += 1
        if needs_query and extra_queries < 1:
            extra_queries += 1
            current = response_for(scenario, condition, complete=True)
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "FULL_SCOPE_QUERY_COMPLETED.\n"
                        f"TOOL_RESPONSE: {json.dumps(current, ensure_ascii=False)}\n"
                        "Return the final JSON answer."
                    ),
                }
            )
            transcript.append({"tool_response": current})
            continue
        final = action["answer"] if action["action"] == "answer" else "uncertain"
        break
    return {
        "scenario_id": scenario.scenario_id,
        "task_id": scenario.task.task_id,
        "domain": scenario.task.domain,
        "mode": scenario.mode,
        "condition": condition,
        "ground_truth": scenario.ground_truth,
        "final_answer": final,
        "task_success": final == scenario.ground_truth,
        "false_negative": scenario.ground_truth == "present" and final == "absent",
        "abstained": final == "uncertain",
        "extra_queries": extra_queries,
        "gate_interventions": interventions,
        "model_calls": model_calls,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "parse_issue": parse_issue,
        "transcript": transcript,
    }


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def aggregate(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for condition in CONDITIONS:
        rows = [row for row in records if row["condition"] == condition]
        hidden = [row for row in rows if row["mode"] == "hidden"]
        absent = [row for row in rows if row["mode"] == "complete_absent"]
        visible = [row for row in rows if row["mode"] == "visible"]
        output[condition] = {
            "false_negative_rate_hidden": mean([float(row["false_negative"]) for row in hidden]),
            "hidden_recovery_success_rate": mean([float(row["final_answer"] == "present") for row in hidden]),
            "complete_absence_retention_rate": mean([float(row["final_answer"] == "absent") for row in absent]),
            "visible_positive_accuracy": mean([float(row["final_answer"] == "present") for row in visible]),
            "overall_task_success_rate": mean([float(row["task_success"]) for row in rows]),
            "abstention_rate": mean([float(row["abstained"]) for row in rows]),
            "mean_extra_queries": mean([float(row["extra_queries"]) for row in rows]),
            "mean_gate_interventions": mean([float(row["gate_interventions"]) for row in rows]),
            "parse_issue_rate": mean([float(row["parse_issue"]) for row in rows]),
            "episode_count": float(len(rows)),
        }
    return output


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--model", default="qwen2.5:7b")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--seed", type=int, default=16002)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--task-limit", type=int)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--experiment-id", default="sgr-coverage-validation-v001")
    args = parser.parse_args()

    tasks = load_tasks(args.dataset)
    if args.task_limit is not None:
        tasks = tasks[: args.task_limit]
    scenarios = build_scenarios(tasks)
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
                        timeout=args.timeout_seconds,
                    )
                )
            except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"{scenario.scenario_id}/{condition}: {type(exc).__name__}: {exc}")
    elapsed = time.monotonic() - started
    summaries = aggregate(records)
    result = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "dataset_sha256": hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
        "task_ids": [task.task_id for task in tasks],
        "model": args.model,
        "seed": args.seed,
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
        "warnings": (["safe JSON fallback occurred"] if any(row["parse_issue"] for row in records) else []),
    }
    write_json(args.metrics_output, metrics)
    print(json.dumps({"summaries": summaries, "errors": errors, "task_ids": result["task_ids"]}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
