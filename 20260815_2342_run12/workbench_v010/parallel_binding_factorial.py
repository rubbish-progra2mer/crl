#!/usr/bin/env python3
"""Paired result-binding factorial for h-012.

The core valid-protocol comparison keeps call ids, call/result semantics, and
the result multiset fixed while reversing only result-block presentation order.
Malformed missing/colliding/swapped-id conditions are diagnostic and never
count as support for the core claim.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any


SYSTEM = """You consume the results of a completed parallel tool-call batch.
Each TOOL_RESULT.call_id identifies the TOOL_CALL it answers. Result blocks may
arrive in any order; when a unique call_id is present, block position has no
binding meaning. Use the call arguments to recover the entity for each result.

Return exactly one JSON object with only entity_a, value_a, entity_b, value_b.
Do not call tools, explain, guess missing associations, or change identifiers."""

SCHEMA = {
    "type": "object",
    "properties": {
        "entity_a": {"type": "string"},
        "value_a": {"type": "string"},
        "entity_b": {"type": "string"},
        "value_b": {"type": "string"},
    },
    "required": ["entity_a", "value_a", "entity_b", "value_b"],
}

CONDITIONS = (
    "unique_anon_aligned",
    "unique_anon_reversed",
    "unique_self_aligned",
    "unique_self_reversed",
    "missing_anon_aligned",
    "missing_anon_reversed",
    "collision_anon_aligned",
    "collision_anon_reversed",
    "swapped_ids_aligned_diagnostic",
    "direct_mapping_control",
)

CORE_CONDITIONS = {
    "unique_anon_aligned",
    "unique_anon_reversed",
    "unique_self_aligned",
    "unique_self_reversed",
}


def build_tasks() -> list[dict[str, Any]]:
    templates = (
        ("inventory", "warehouse", "lot", "inventory_probe"),
        ("medical", "specimen", "assay", "lab_probe"),
        ("network", "endpoint", "route", "network_probe"),
        ("finance", "account", "quote", "ledger_probe"),
    )
    opaque_values = (
        ("K7V2", "Q4M9"),
        ("R8C3", "H2W6"),
        ("N5J1", "B9T4"),
        ("F3P8", "L6X2"),
    )
    tasks: list[dict[str, Any]] = []
    for index, (domain, noun, field, base_tool) in enumerate(templates):
        for surface in ("same_tool", "distinct_tools"):
            marker = "s" if surface == "same_tool" else "d"
            entity_a = f"{domain[:3]}-{marker}-{noun}-17"
            entity_b = f"{domain[:3]}-{marker}-{noun}-42"
            value_a, value_b = opaque_values[index]
            if surface == "same_tool":
                tool_a = base_tool
                tool_b = base_tool
            else:
                tool_a = f"{base_tool}_primary"
                tool_b = f"{base_tool}_secondary"
            tasks.append(
                {
                    "task_id": f"{domain}-{marker}",
                    "domain": domain,
                    "surface": surface,
                    "field": field,
                    "entity_a": entity_a,
                    "entity_b": entity_b,
                    "value_a": value_a,
                    "value_b": value_b,
                    "call_a": f"call-{domain}-{marker}-A",
                    "call_b": f"call-{domain}-{marker}-B",
                    "tool_a": tool_a,
                    "tool_b": tool_b,
                }
            )
    return tasks


def call_blocks(task: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "call_id": task["call_a"],
            "tool_name": task["tool_a"],
            "arguments": {"entity_id": task["entity_a"], "field": task["field"]},
        },
        {
            "call_id": task["call_b"],
            "tool_name": task["tool_b"],
            "arguments": {"entity_id": task["entity_b"], "field": task["field"]},
        },
    ]


def result_blocks(task: dict[str, Any], condition: str) -> list[dict[str, Any]]:
    self_identifying = condition.startswith("unique_self")
    first: dict[str, Any] = {
        "call_id": task["call_a"],
        "tool_name": task["tool_a"],
        "payload": {"value": task["value_a"]},
    }
    second: dict[str, Any] = {
        "call_id": task["call_b"],
        "tool_name": task["tool_b"],
        "payload": {"value": task["value_b"]},
    }
    if self_identifying:
        first["payload"]["entity_id"] = task["entity_a"]
        second["payload"]["entity_id"] = task["entity_b"]
    if condition.startswith("missing_"):
        first.pop("call_id")
        second.pop("call_id")
    elif condition.startswith("collision_"):
        first["call_id"] = "call-collision-0"
        second["call_id"] = "call-collision-0"
    elif condition == "swapped_ids_aligned_diagnostic":
        first["call_id"] = task["call_b"]
        second["call_id"] = task["call_a"]
    if condition.endswith("reversed"):
        return [second, first]
    return [first, second]


def build_messages(task: dict[str, Any], condition: str) -> list[dict[str, str]]:
    if condition == "direct_mapping_control":
        content = {
            "required_output": [task["entity_a"], task["entity_b"]],
            "mapping": {
                task["entity_a"]: task["value_a"],
                task["entity_b"]: task["value_b"],
            },
        }
        return [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": "DIRECT_MAPPING "
                + json.dumps(content, ensure_ascii=False, separators=(",", ":")),
            },
        ]
    calls = call_blocks(task)
    results = result_blocks(task, condition)
    return [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": (
                "The final answer must map both requested entities to their opaque "
                f"{task['field']} values. The values cannot be inferred without the results."
            ),
        },
        {
            "role": "assistant",
            "content": "PARALLEL_TOOL_CALLS "
            + json.dumps(calls, ensure_ascii=False, separators=(",", ":")),
        },
        {
            "role": "user",
            "content": "PARALLEL_TOOL_RESULTS "
            + json.dumps(results, ensure_ascii=False, separators=(",", ":")),
        },
    ]


def model_turn(
    model: str, messages: list[dict[str, str]], timeout: int, seed: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    body = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "format": SCHEMA,
        "options": {"temperature": 0, "seed": seed, "num_predict": 128},
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = json.loads(response.read().decode("utf-8"))
    content = raw.get("message", {}).get("content", "")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {}
        for key in ("entity_a", "value_a", "entity_b", "value_b"):
            match = re.search(rf'"{key}"\s*:\s*"([^"]*)"', content)
            parsed[key] = match.group(1) if match else ""
        parsed["parse_recovered"] = any(parsed.values())
        parsed["raw_content"] = content.strip()
    return parsed, {
        "elapsed_seconds": time.time() - started,
        "prompt_eval_count": raw.get("prompt_eval_count"),
        "eval_count": raw.get("eval_count"),
        "done_reason": raw.get("done_reason"),
    }


def mapping_from_response(response: dict[str, Any]) -> dict[str, str]:
    return {
        str(response.get("entity_a", "")).strip(): str(
            response.get("value_a", "")
        ).strip(),
        str(response.get("entity_b", "")).strip(): str(
            response.get("value_b", "")
        ).strip(),
    }


def protocol_gold(task: dict[str, Any], condition: str) -> dict[str, str] | None:
    if condition in CORE_CONDITIONS or condition == "direct_mapping_control":
        return {
            task["entity_a"]: task["value_a"],
            task["entity_b"]: task["value_b"],
        }
    if condition == "missing_anon_aligned":
        return {
            task["entity_a"]: task["value_a"],
            task["entity_b"]: task["value_b"],
        }
    if condition == "swapped_ids_aligned_diagnostic":
        return {
            task["entity_a"]: task["value_b"],
            task["entity_b"]: task["value_a"],
        }
    return None


def position_mapping(task: dict[str, Any], condition: str) -> dict[str, str]:
    reversed_order = condition.endswith("reversed")
    if reversed_order:
        return {
            task["entity_a"]: task["value_b"],
            task["entity_b"]: task["value_a"],
        }
    return {
        task["entity_a"]: task["value_a"],
        task["entity_b"]: task["value_b"],
    }


def run(model: str, timeout: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    tasks = build_tasks()
    for task_index, task in enumerate(tasks):
        rotation = task_index % len(CONDITIONS)
        ordered_conditions = CONDITIONS[rotation:] + CONDITIONS[:rotation]
        for condition in ordered_conditions:
            messages = build_messages(task, condition)
            error = None
            try:
                response, meta = model_turn(
                    model,
                    messages,
                    timeout,
                    seed=(
                        20260818
                        + sum(ord(ch) for ch in task["task_id"])
                        + sum(ord(ch) for ch in condition)
                    ),
                )
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                response = {
                    "entity_a": "",
                    "value_a": "",
                    "entity_b": "",
                    "value_b": "",
                }
                meta = {}
                error = repr(exc)
            observed = mapping_from_response(response)
            gold = protocol_gold(task, condition)
            positional = position_mapping(task, condition)
            rows.append(
                {
                    "model": model,
                    "task_id": task["task_id"],
                    "domain": task["domain"],
                    "surface": task["surface"],
                    "condition": condition,
                    "core_valid_protocol": condition in CORE_CONDITIONS,
                    "gold_mapping": gold,
                    "position_mapping": positional,
                    "observed_mapping": observed,
                    "mapping_correct": gold is not None and observed == gold,
                    "follows_position": observed == positional,
                    "response": response,
                    "meta": meta,
                    "error": error,
                    "messages": messages,
                }
            )

    row_index = {(row["task_id"], row["condition"]): row for row in rows}
    pair_names = (
        ("unique_anon_aligned", "unique_anon_reversed", "unique_anon"),
        ("unique_self_aligned", "unique_self_reversed", "unique_self"),
        ("missing_anon_aligned", "missing_anon_reversed", "missing_anon"),
        ("collision_anon_aligned", "collision_anon_reversed", "collision_anon"),
    )
    pair_summary: dict[str, dict[str, int]] = {}
    for aligned, reversed_name, label in pair_names:
        pairs = [
            (row_index[(task["task_id"], aligned)], row_index[(task["task_id"], reversed_name)])
            for task in tasks
        ]
        pair_summary[label] = {
            "n_pairs": len(pairs),
            "mapping_changed": sum(
                left["observed_mapping"] != right["observed_mapping"]
                for left, right in pairs
            ),
            "aligned_correct": sum(bool(left["mapping_correct"]) for left, _ in pairs),
            "reversed_correct": sum(bool(right["mapping_correct"]) for _, right in pairs),
            "reversed_follows_position": sum(
                bool(right["follows_position"]) for _, right in pairs
            ),
        }

    condition_summary: dict[str, Any] = {}
    for condition in CONDITIONS:
        cell = [row for row in rows if row["condition"] == condition]
        condition_summary[condition] = {
            "n": len(cell),
            "mapping_correct": sum(bool(row["mapping_correct"]) for row in cell),
            "follows_position": sum(bool(row["follows_position"]) for row in cell),
            "errors": sum(row["error"] is not None for row in cell),
        }
    summary = {
        "model": model,
        "task_count": len(tasks),
        "cells": len(rows),
        "conditions": condition_summary,
        "pairs": pair_summary,
    }
    return rows, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows, summary = run(args.model, args.timeout)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if all(row["error"] is None for row in rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
