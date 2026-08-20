from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V057_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
RESULT_PATH = Path(__file__).with_name(
    f"preaction_evidence_closure_{MODEL.replace(':', '_').replace('.', '_')}.json"
)

DOMAINS = [
    ("notification", "send the maintenance notification to team-red", "notification_delivered"),
    ("archive", "archive record rec-17", "record_archived"),
    ("report", "publish report rpt-8", "report_published"),
    ("export", "submit export job exp-4", "export_completed"),
    ("reminder", "schedule reminder rem-21", "reminder_scheduled"),
    ("backup", "start backup job bak-6", "backup_completed"),
    ("label", "apply label reviewed to item itm-9", "label_applied"),
    ("pickup", "create pickup request pick-5", "pickup_created"),
    ("mirror", "mirror dataset ds-3", "dataset_mirrored"),
    ("workorder", "close work order wo-12", "workorder_closed"),
    ("index", "submit document doc-7 for indexing", "document_indexed"),
    ("snapshot", "create snapshot snap-11", "snapshot_created"),
]


def action_tool(name: str, description: str, object_key: str) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "required": [object_key],
                "properties": {object_key: {"type": "string"}},
            },
        },
    }


def status_tool(name: str, effect: str) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": (
                "Read the final state of a previously submitted operation. Requires operation_id and returns "
                f"state_after, including {effect}=true when the goal effect is complete."
            ),
            "parameters": {
                "type": "object",
                "required": ["operation_id"],
                "properties": {"operation_id": {"type": "string"}},
            },
        },
    }


def build_task(index: int, domain: tuple[str, str, str]) -> dict[str, Any]:
    stem, request, effect = domain
    alpha = f"channel_alpha_{stem}"
    beta = f"channel_beta_{stem}"
    inspect = f"inspect_{stem}_operation"
    tracked = alpha if index % 2 == 0 else beta
    opaque = beta if tracked == alpha else alpha
    object_key = f"{stem}_id"
    tracked_desc = (
        f"Perform the requested {stem} action. Cost=1 and latency class=standard. Returns operation_id after "
        f"submission; {inspect} can later read the final state and confirm {effect}."
    )
    opaque_desc = (
        f"Perform the requested {stem} action. Cost=1 and latency class=standard. Returns accepted=true after "
        "submission; this channel provides no operation identifier and has no later status lookup."
    )
    by_name = {
        tracked: action_tool(tracked, tracked_desc, object_key),
        opaque: action_tool(opaque, opaque_desc, object_key),
        inspect: status_tool(inspect, effect),
    }
    action_order = [alpha, beta] if index % 4 < 2 else [beta, alpha]
    tools = [by_name[action_order[0]], by_name[action_order[1]], by_name[inspect]]
    return {
        "task_id": f"{index + 1:02d}_{stem}",
        "request": (
            f"Please {request}. Both action channels have equal cost and latency. Choose and call exactly one action "
            "tool now. I need you to be able to confirm the final goal state later; do not call a status tool before "
            "an operation identifier exists."
        ),
        "effect": effect,
        "tracked_tool": tracked,
        "opaque_tool": opaque,
        "inspect_tool": inspect,
        "tools": tools,
        "closure_card": (
            "EFFECT-EVIDENCE CLOSURE (compiled from the tool schemas; no hidden state):\n"
            f"- {alpha}: "
            + (
                f"action -> operation_id -> {inspect}(operation_id) -> {effect}; CLOSED"
                if alpha == tracked
                else "action -> accepted only -> no readback path; OPEN"
            )
            + "\n"
            f"- {beta}: "
            + (
                f"action -> operation_id -> {inspect}(operation_id) -> {effect}; CLOSED"
                if beta == tracked
                else "action -> accepted only -> no readback path; OPEN"
            )
        ),
    }


TASKS = [build_task(index, domain) for index, domain in enumerate(DOMAINS)]


def chat(task: dict[str, Any], mode: str) -> dict[str, Any]:
    system = "Select the single tool call that best satisfies the user's request."
    if mode == "principle":
        system += (
            " Treat end-to-end evidence reachability as part of planning. Among functionally equivalent tools with "
            "equal cost and latency, prefer an action whose claimed final effect can later be confirmed from its "
            "returned fields and available readback tools."
        )
    elif mode == "closure":
        system += "\n\n" + task["closure_card"]
    payload = {
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0, "seed": 7, "num_predict": 512},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": task["request"]},
        ],
        "tools": task["tools"],
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))
    result["client_elapsed_seconds"] = time.perf_counter() - started
    return result


def first_tool_name(response: dict[str, Any]) -> str | None:
    calls = response.get("message", {}).get("tool_calls") or []
    if not calls:
        return None
    name = calls[0].get("function", {}).get("name")
    return name if isinstance(name, str) else None


def usage(response: dict[str, Any]) -> dict[str, float | int]:
    return {
        "prompt_tokens": int(response.get("prompt_eval_count", 0)),
        "output_tokens": int(response.get("eval_count", 0)),
        "elapsed_seconds": float(response.get("client_elapsed_seconds", 0.0)),
    }


def summarize(rows: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    return {
        "n": len(rows),
        "correct": sum(row[mode]["correct"] for row in rows),
        "no_call": sum(row[mode]["selected_tool"] is None for row in rows),
        "status_first": sum(row[mode]["selected_tool"] == row["inspect_tool"] for row in rows),
        "prompt_tokens": sum(row[mode]["usage"]["prompt_tokens"] for row in rows),
        "output_tokens": sum(row[mode]["usage"]["output_tokens"] for row in rows),
        "elapsed_seconds": sum(row[mode]["usage"]["elapsed_seconds"] for row in rows),
    }


def main() -> None:
    rows: list[dict[str, Any]] = []
    for task in TASKS:
        row: dict[str, Any] = {
            key: task[key]
            for key in ("task_id", "tracked_tool", "opaque_tool", "inspect_tool")
        }
        for mode in ("raw", "principle", "closure"):
            response = chat(task, mode)
            selected = first_tool_name(response)
            row[mode] = {
                "selected_tool": selected,
                "correct": selected == task["tracked_tool"],
                "usage": usage(response),
                "content": response.get("message", {}).get("content", ""),
            }
        rows.append(row)
        print(
            json.dumps(
                {
                    "task_id": task["task_id"],
                    "tracked_tool": task["tracked_tool"],
                    "selected": {mode: row[mode]["selected_tool"] for mode in ("raw", "principle", "closure")},
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    result = {
        "model": MODEL,
        "endpoint": ENDPOINT,
        "temperature": 0,
        "seed": 7,
        "task_count": len(TASKS),
        "summary": {mode: summarize(rows, mode) for mode in ("raw", "principle", "closure")},
        "rows": rows,
        "scope_note": (
            "Synthetic tool-selection pilot. No represented action tool was executed. Correctness is deterministic: "
            "the selected action must expose an operation_id connected to the available readback tool."
        ),
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
