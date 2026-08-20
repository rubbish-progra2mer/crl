#!/usr/bin/env python3
"""Executable benchmark for cache-conditioned structural planning failures.

The benchmark uses deterministic, mechanically scored action plans. It compares
the same model on the same target task with and without a cached reference plan.
It is an evaluation artifact, not an implementation of Agentic Plan Caching.
"""

from __future__ import annotations

import argparse
import json
import math
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any


SYSTEM = """You are a deterministic tool-plan compiler. Produce the minimal
safe plan for the TARGET task using only supplied action IDs. Include each
required action exactly once, omit forbidden or unnecessary actions, and obey
all order and conditional-branch requirements. Return only the JSON object."""


OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "actions": {"type": "array", "items": {"type": "string"}},
        "commit": {"type": "boolean"},
        "explanation": {"type": "string"},
    },
    "required": ["actions", "commit", "explanation"],
}


DOMAINS = [
    "inventory record",
    "calendar event",
    "access credential",
    "project file",
    "support ticket",
    "analytics dataset",
    "service deployment",
    "notification route",
]


def _case(
    case_id: str,
    category: str,
    domain: str,
    tools: dict[str, str],
    reference_task: str,
    target_task: str,
    cached_plan: list[str],
    expected_plan: list[str],
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "category": category,
        "domain": domain,
        "tools": tools,
        "reference_task": reference_task,
        "target_task": target_task,
        "cached_plan": cached_plan,
        "expected_plan": expected_plan,
        "graph_changed": cached_plan != expected_plan,
    }


def build_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, domain in enumerate(DOMAINS[:6], 1):
        tools = {
            "READ_SOURCE": "Read the source without changing it.",
            "CHECK_TARGET": "Check that the target can accept the new object.",
            "CREATE_TARGET": "Create the corresponding object at the target.",
            "REMOVE_SOURCE": "Permanently remove the source object.",
        }
        cached = ["READ_SOURCE", "CHECK_TARGET", "CREATE_TARGET", "REMOVE_SOURCE"]
        expected = cached[:-1]
        rows.append(
            _case(
                f"R{index:02d}",
                "action_remove",
                domain,
                tools,
                f"Move the {domain} from source A to target B; remove A only after B is created.",
                f"Copy the {domain} from source A to target B and preserve A unchanged; read A, check B, then create B.",
                cached,
                expected,
            )
        )

    for index, domain in enumerate(DOMAINS[:6], 1):
        tools = {
            "READ_SOURCE": "Read the source without changing it.",
            "CHECK_TARGET": "Check that the target can accept the new object.",
            "CREATE_TARGET": "Create the corresponding object at the target.",
            "WRITE_AUDIT": "Write the mandatory audit record after target creation.",
        }
        cached = ["READ_SOURCE", "CHECK_TARGET", "CREATE_TARGET"]
        expected = cached + ["WRITE_AUDIT"]
        rows.append(
            _case(
                f"A{index:02d}",
                "action_add",
                domain,
                tools,
                f"Copy the {domain} from source A to target B after checking B.",
                f"Copy the {domain} from source A to target B after checking B, then write the newly required audit record.",
                cached,
                expected,
            )
        )

    for index, domain in enumerate(DOMAINS[:6], 1):
        tools = {
            "READ_SOURCE": "Read the source contents.",
            "CHECK_POLICY": "Check authorization policy without reading source contents.",
            "CREATE_TARGET": "Create the target from the already authorized source contents.",
            "WRITE_AUDIT": "Write an audit record after target creation.",
        }
        cached = ["READ_SOURCE", "CHECK_POLICY", "CREATE_TARGET", "WRITE_AUDIT"]
        expected = ["CHECK_POLICY", "READ_SOURCE", "CREATE_TARGET", "WRITE_AUDIT"]
        rows.append(
            _case(
                f"O{index:02d}",
                "order_flip",
                domain,
                tools,
                f"Copy the {domain}; the legacy rule requires reading A before checking the policy, then create B and audit.",
                f"Copy the {domain}; the new privacy rule forbids reading A until CHECK_POLICY succeeds. Check policy first, then read, create B, and audit.",
                cached,
                expected,
            )
        )

    for index, domain in enumerate(DOMAINS[:6], 1):
        tools = {
            "READ_STATUS": "Read whether the source is READY or BLOCKED.",
            "IF_READY_CREATE": "If and only if READY, create the target object.",
            "IF_BLOCKED_ABORT": "If and only if BLOCKED, stop without escalation.",
            "IF_BLOCKED_ESCALATE": "If and only if BLOCKED, escalate for human handling.",
        }
        cached = ["READ_STATUS", "IF_READY_CREATE", "IF_BLOCKED_ABORT"]
        expected = ["READ_STATUS", "IF_READY_CREATE", "IF_BLOCKED_ESCALATE"]
        rows.append(
            _case(
                f"B{index:02d}",
                "branch_flip",
                domain,
                tools,
                f"Process the {domain}: create it when READY; when BLOCKED, abort without escalation.",
                f"Process the {domain}: create it when READY; under the revised rule, when BLOCKED escalate instead of aborting.",
                cached,
                expected,
            )
        )

    for index, domain in enumerate(DOMAINS, 1):
        tools = {
            "READ_SOURCE": "Read the source without changing it.",
            "CHECK_TARGET": "Check that the target can accept the new object.",
            "CREATE_TARGET": "Create the corresponding object at the target.",
            "WRITE_AUDIT": "Write the audit record after target creation.",
        }
        plan = ["READ_SOURCE", "CHECK_TARGET", "CREATE_TARGET", "WRITE_AUDIT"]
        rows.append(
            _case(
                f"S{index:02d}",
                "safe_same_graph",
                domain,
                tools,
                f"Read the {domain} at A, verify B, create the copy at B, and record the operation in the audit log.",
                f"For the {domain}, inspect A first; after confirming B can accept it, create B's copy and finally log the action.",
                plan,
                plan,
            )
        )
    return rows


def build_prompt(case: dict[str, Any], mode: str) -> str:
    payload: dict[str, Any] = {
        "available_actions": case["tools"],
        "target_task": case["target_task"],
        "output_rule": "Use only available action IDs and return them in execution order.",
    }
    if mode == "full_replan":
        payload["planning_mode"] = "Plan from the target task without a reference plan."
    elif mode == "cache_adapt":
        payload.update(
            {
                "planning_mode": "Adapt a cached plan template to the target task.",
                "reference_task": case["reference_task"],
                "cached_plan_template": case["cached_plan"],
                "adaptation_instruction": (
                    "Maintain reusable structure when valid, but customize the plan for the target details. "
                    "Remove, add, reorder, or replace actions whenever target constraints require it."
                ),
            }
        )
    else:
        raise ValueError(mode)
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def call_ollama(
    base_url: str,
    model: str,
    prompt: str,
    seed: int,
    timeout: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "think": False,
        "format": OUTPUT_SCHEMA,
        "options": {"temperature": 0, "seed": seed},
    }
    request = urllib.request.Request(
        base_url.rstrip("/") + "/api/chat",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = json.loads(response.read().decode("utf-8"))
    content = raw.get("message", {}).get("content", "")
    parsed = json.loads(content)
    return parsed, {
        "elapsed_seconds": time.time() - started,
        "prompt_eval_count": int(raw.get("prompt_eval_count") or 0),
        "eval_count": int(raw.get("eval_count") or 0),
        "done_reason": raw.get("done_reason"),
    }


def exact_actions(response: dict[str, Any], expected: list[str], allowed: set[str]) -> tuple[bool, list[str]]:
    actions = response.get("actions", [])
    if not isinstance(actions, list):
        return False, []
    normalized = [str(action) for action in actions]
    valid_vocabulary = all(action in allowed for action in normalized)
    return valid_vocabulary and normalized == expected, normalized


def ratio_record(name: str, value: float, split: str, n: int) -> dict[str, Any]:
    if not math.isfinite(value):
        raise ValueError(f"non-finite metric {name}")
    return {"name": name, "value": value, "unit": "ratio", "split": split, "aggregation": "mean", "n": n}


def compute_metrics(rows: list[dict[str, Any]], experiment_id: str, wall_time: float) -> dict[str, Any]:
    grouped: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        grouped[(row["model"], row["case_id"])][row["mode"]] = row

    counterfactual_pairs: list[dict[str, Any]] = []
    safe_pairs: list[dict[str, Any]] = []
    for (model, case_id), pair in grouped.items():
        if set(pair) != {"full_replan", "cache_adapt"}:
            continue
        item = {
            "model": model,
            "case_id": case_id,
            "category": pair["full_replan"]["category"],
            "full_exact": pair["full_replan"]["exact"],
            "cache_exact": pair["cache_adapt"]["exact"],
        }
        if item["category"] == "safe_same_graph":
            safe_pairs.append(item)
        else:
            counterfactual_pairs.append(item)

    def mean(items: list[dict[str, Any]], key: str) -> float:
        return sum(bool(item[key]) for item in items) / len(items)

    induced = [item["full_exact"] and not item["cache_exact"] for item in counterfactual_pairs]
    primary = sum(induced) / len(counterfactual_pairs)
    records = [
        ratio_record("cache_induced_failure_rate", primary, "counterfactual_all_models", len(counterfactual_pairs)),
        ratio_record("full_replan_accuracy", mean(counterfactual_pairs, "full_exact"), "counterfactual_all_models", len(counterfactual_pairs)),
        ratio_record("cache_adapt_accuracy", mean(counterfactual_pairs, "cache_exact"), "counterfactual_all_models", len(counterfactual_pairs)),
        ratio_record("safe_full_replan_accuracy", mean(safe_pairs, "full_exact"), "safe_same_graph_all_models", len(safe_pairs)),
        ratio_record("safe_cache_adapt_accuracy", mean(safe_pairs, "cache_exact"), "safe_same_graph_all_models", len(safe_pairs)),
    ]

    for model in sorted({item["model"] for item in counterfactual_pairs}):
        selected = [item for item in counterfactual_pairs if item["model"] == model]
        value = sum(item["full_exact"] and not item["cache_exact"] for item in selected) / len(selected)
        records.append(ratio_record("cache_induced_failure_rate", value, f"counterfactual_model={model}", len(selected)))

    for category in ["action_remove", "action_add", "order_flip", "branch_flip"]:
        selected = [item for item in counterfactual_pairs if item["category"] == category]
        value = sum(item["full_exact"] and not item["cache_exact"] for item in selected) / len(selected)
        records.append(ratio_record("cache_induced_failure_rate_by_edit", value, f"category={category}", len(selected)))

    api_calls = len(rows)
    tokens = sum(row["meta"]["prompt_eval_count"] + row["meta"]["eval_count"] for row in rows)
    return {
        "schema_version": 1,
        "experiment_id": experiment_id,
        "records": records,
        "resource_usage": {
            "tokens": tokens,
            "api_calls": api_calls,
            "wall_time_seconds": wall_time,
            "gpu_time_seconds": "unknown",
            "estimated_cost": 0.0,
        },
        "errors": [],
        "warnings": [
            "The cache condition is a same-model, prompt-level proxy for template adaptation, not a reproduction of APC's full system.",
            "All tasks are synthetic and English; external validity is not measured in this attempt.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-id", default="cache-structural-counterfactual-001")
    parser.add_argument("--models", nargs="+", default=["qwen3:4b", "qwen3:8b"])
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    args = parser.parse_args()

    started = time.time()
    rows: list[dict[str, Any]] = []
    all_cases = build_cases()
    with args.raw_output.open("x", encoding="utf-8", newline="\n") as raw_handle:
        for model_index, model in enumerate(args.models):
            for case_index, case in enumerate(all_cases):
                for mode_index, mode in enumerate(["full_replan", "cache_adapt"]):
                    prompt = build_prompt(case, mode)
                    seed = 20260816 + model_index * 1000 + case_index * 2 + mode_index
                    try:
                        response, meta = call_ollama(args.base_url, model, prompt, seed, args.timeout)
                        exact, actions = exact_actions(response, case["expected_plan"], set(case["tools"]))
                    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
                        raise RuntimeError(f"model call failed for {model} {case['case_id']} {mode}: {exc!r}") from exc
                    row = {
                        "model": model,
                        "case_id": case["case_id"],
                        "category": case["category"],
                        "graph_changed": case["graph_changed"],
                        "mode": mode,
                        "reference_task": case["reference_task"],
                        "target_task": case["target_task"],
                        "cached_plan": case["cached_plan"],
                        "expected_plan": case["expected_plan"],
                        "prompt": prompt,
                        "response": response,
                        "actions": actions,
                        "exact": exact,
                        "meta": meta,
                    }
                    rows.append(row)
                    raw_handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
                    raw_handle.flush()
                    print(json.dumps({"model": model, "case": case["case_id"], "mode": mode, "exact": exact}, ensure_ascii=False), flush=True)

    metrics = compute_metrics(rows, args.experiment_id, time.time() - started)
    args.metrics_output.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(metrics, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
