from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
TASKS_PATH = ROOT / "probe_tasks.json"
MODEL = os.environ.get("CRL_PROBE_MODEL", "qwen3:4b")
OUTPUT_PATH = ROOT / f"probe_results_{MODEL.replace(':', '_')}.json"
VARIANTS = ("p0", "p1")
CONDITIONS = ("raw_id", "short_ref", "typed_selector")


def opaque_id(label: str, variant: str, kind: str) -> str:
    digest = hashlib.sha256(f"{variant}|{kind}|{label}".encode("utf-8")).hexdigest()
    return f"{kind[:3]}_{digest[:8]}-{digest[8:12]}-{digest[12:16]}-{digest[16:20]}-{digest[20:32]}"


def schema_for(condition: str) -> dict[str, Any]:
    if condition == "raw_id":
        properties = {
            "target_id": {"type": "string"},
            "resource_id": {"type": "string"},
        }
    elif condition == "short_ref":
        properties = {
            "target_ref": {"type": "string", "pattern": "^T[1-5]$"},
            "resource_ref": {"type": "string", "pattern": "^R[1-5]$"},
        }
    else:
        binding = {
            "type": "object",
            "properties": {
                "source_call": {"type": "string"},
                "row": {"type": "integer", "minimum": 1, "maximum": 5},
                "field": {"type": "string", "const": "id"},
            },
            "required": ["source_call", "row", "field"],
            "additionalProperties": False,
        }
        properties = {"target_binding": binding, "resource_binding": binding}
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def rendered_rows(rows: list[dict[str, Any]], variant: str, kind: str, condition: str) -> tuple[list[dict[str, Any]], dict[str, str]]:
    rendered: list[dict[str, Any]] = []
    refs: dict[str, str] = {}
    prefix = "T" if kind == "target" else "R"
    for index, source in enumerate(rows, start=1):
        row = {key: value for key, value in source.items() if key != "label"}
        actual_id = opaque_id(source["label"], variant, kind)
        refs[f"{prefix}{index}"] = actual_id
        if condition == "raw_id":
            row = {"id": actual_id, **row}
        elif condition == "short_ref":
            row = {"ref": f"{prefix}{index}", **row}
        rendered.append(row)
    return rendered, refs


def prompt_for(task: dict[str, Any], variant: str, condition: str) -> tuple[str, dict[str, str]]:
    target_rows, target_refs = rendered_rows(task["targets"], variant, "target", condition)
    resource_rows, resource_refs = rendered_rows(task["resources"], variant, "resource", condition)
    shared = (
        "You are at the final decision step of a tool-using agent. Select exactly one target and one resource "
        "that satisfy every detail in the user instruction. Similar rows are deliberate distractors. "
        "Return only the JSON object requested; do not explain and do not invent values.\n\n"
        f"User instruction: {task['instruction']}\n"
        f"Planned action: {task['action']}\n\n"
        f"Result of call search_target ({task['target_type']} rows, 1-based order):\n{json.dumps(target_rows, ensure_ascii=False, indent=2)}\n\n"
        f"Result of call search_resource ({task['resource_type']} rows, 1-based order):\n{json.dumps(resource_rows, ensure_ascii=False, indent=2)}\n\n"
    )
    if condition == "raw_id":
        instruction = "Copy the exact target id and resource id into target_id and resource_id."
    elif condition == "short_ref":
        instruction = "Return the selected target ref and resource ref in target_ref and resource_ref. The runtime will dereference them."
    else:
        instruction = (
            "Do not copy identifiers. Return target_binding and resource_binding. Each binding must contain "
            "source_call (search_target or search_resource), the selected 1-based row, and field='id'. "
            "The runtime will late-bind the hidden identifier from that exact result cell."
        )
    return shared + instruction, {**target_refs, **resource_refs}


def call_ollama(prompt: str, condition: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Follow the output schema exactly. /no_think"},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "think": False,
        "format": schema_for(condition),
        "options": {"temperature": 0, "seed": 20260813, "num_predict": 180},
        "keep_alive": "10m",
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = json.loads(response.read().decode("utf-8"))
    elapsed = time.perf_counter() - started
    content = raw.get("message", {}).get("content", "")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = None
    meta = {
        "content": content,
        "elapsed_seconds": round(elapsed, 4),
        "total_duration_ns": raw.get("total_duration"),
        "load_duration_ns": raw.get("load_duration"),
        "prompt_eval_count": raw.get("prompt_eval_count"),
        "eval_count": raw.get("eval_count"),
        "done_reason": raw.get("done_reason"),
    }
    return parsed, meta


def resolve(task: dict[str, Any], variant: str, condition: str, parsed: dict[str, Any] | None, refs: dict[str, str]) -> dict[str, Any]:
    expected_target = opaque_id(task["target_label"], variant, "target")
    expected_resource = opaque_id(task["resource_label"], variant, "resource")
    resolved_target = None
    resolved_resource = None
    selected_target_label = None
    selected_resource_label = None
    error = None
    try:
        if not isinstance(parsed, dict):
            raise ValueError("not_json_object")
        if condition == "raw_id":
            resolved_target = parsed["target_id"]
            resolved_resource = parsed["resource_id"]
        elif condition == "short_ref":
            resolved_target = refs[parsed["target_ref"]]
            resolved_resource = refs[parsed["resource_ref"]]
        else:
            target_binding = parsed["target_binding"]
            resource_binding = parsed["resource_binding"]
            if target_binding["source_call"] != "search_target" or target_binding["field"] != "id":
                raise ValueError("invalid_target_scope")
            if resource_binding["source_call"] != "search_resource" or resource_binding["field"] != "id":
                raise ValueError("invalid_resource_scope")
            resolved_target = refs[f"T{int(target_binding['row'])}"]
            resolved_resource = refs[f"R{int(resource_binding['row'])}"]
    except (KeyError, TypeError, ValueError) as exc:
        error = str(exc)
    target_by_id = {opaque_id(row["label"], variant, "target"): row["label"] for row in task["targets"]}
    resource_by_id = {opaque_id(row["label"], variant, "resource"): row["label"] for row in task["resources"]}
    selected_target_label = target_by_id.get(resolved_target)
    selected_resource_label = resource_by_id.get(resolved_resource)
    return {
        "parse_and_bind_ok": error is None,
        "binding_error": error,
        "resolved_target_id": resolved_target,
        "resolved_resource_id": resolved_resource,
        "selected_target_label": selected_target_label,
        "selected_resource_label": selected_resource_label,
        "expected_target_id": expected_target,
        "expected_resource_id": expected_resource,
        "target_correct": resolved_target == expected_target,
        "resource_correct": resolved_resource == expected_resource,
        "joint_correct": resolved_target == expected_target and resolved_resource == expected_resource,
    }


def main() -> None:
    tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))["tasks"]
    records: list[dict[str, Any]] = []
    for task in tasks:
        for variant in VARIANTS:
            for condition in CONDITIONS:
                prompt, refs = prompt_for(task, variant, condition)
                parsed, meta = call_ollama(prompt, condition)
                record = {
                    "task_id": task["task_id"],
                    "variant": variant,
                    "condition": condition,
                    "model": MODEL,
                    "parsed": parsed,
                    "response_meta": meta,
                    "score": resolve(task, variant, condition, parsed, refs),
                }
                records.append(record)
                OUTPUT_PATH.write_text(
                    json.dumps({"schema_version": 1, "model": MODEL, "records": records}, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                    newline="\n",
                )
                print(json.dumps({"task": task["task_id"], "variant": variant, "condition": condition, **record["score"]}, ensure_ascii=False), flush=True)

    summary: dict[str, Any] = {}
    for condition in CONDITIONS:
        subset = [record for record in records if record["condition"] == condition]
        summary[condition] = {
            "n": len(subset),
            "parse_and_bind_rate": sum(record["score"]["parse_and_bind_ok"] for record in subset) / len(subset),
            "target_accuracy": sum(record["score"]["target_correct"] for record in subset) / len(subset),
            "resource_accuracy": sum(record["score"]["resource_correct"] for record in subset) / len(subset),
            "joint_accuracy": sum(record["score"]["joint_correct"] for record in subset) / len(subset),
        }
        stable_pairs = 0
        for task in tasks:
            pair = [record for record in subset if record["task_id"] == task["task_id"]]
            if (
                len(pair) == 2
                and pair[0]["score"]["selected_target_label"] == pair[1]["score"]["selected_target_label"]
                and pair[0]["score"]["selected_resource_label"] == pair[1]["score"]["selected_resource_label"]
            ):
                stable_pairs += 1
        summary[condition]["permutation_outcome_stability"] = stable_pairs / len(tasks)
    document = {"schema_version": 1, "model": MODEL, "conditions": list(CONDITIONS), "summary": summary, "records": records}
    OUTPUT_PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
