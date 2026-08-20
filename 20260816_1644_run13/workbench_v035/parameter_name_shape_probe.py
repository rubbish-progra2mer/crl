from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = "qwen2.5:7b"
ENDPOINT = "http://127.0.0.1:11434/api/chat"
RESULT_PATH = Path(__file__).with_name("parameter_name_shape_probe_qwen2_5_7b.json")
FIELD_NAMES = [
    "decision",
    "action",
    "next_action",
    "outcome",
    "result",
    "status",
    "route",
    "choice",
    "label",
    "category",
    "priority",
    "mode",
    "code",
    "xqv",
]
ENUM_VALUES = [
    "consume_present",
    "request_missing",
    "wait_pending",
    "skip_not_applicable",
    "request_access",
    "retry_error",
]


def tool(field_name: str) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "handle_observation",
            "description": "Choose the next operation for one observation.",
            "parameters": {
                "type": "object",
                "required": ["observation_id", field_name],
                "properties": {
                    "observation_id": {"type": "string"},
                    field_name: {
                        "type": "string",
                        "description": "Return exactly one enum token.",
                        "enum": ENUM_VALUES,
                    },
                },
            },
        },
    }


def chat(field_name: str) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0, "seed": 13, "num_predict": 256},
        "messages": [
            {
                "role": "system",
                "content": "Use status 200 as PRESENT even when data is false. Call the tool once without prose.",
            },
            {
                "role": "user",
                "content": (
                    "Observation id is obs_false and observation is {\"status\":200,\"data\":false}. "
                    "For PRESENT, choose consume_present."
                ),
            },
        ],
        "tools": [tool(field_name)],
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))
    result["client_elapsed_seconds"] = time.perf_counter() - started
    return result


def first_arguments(response: dict[str, Any]) -> dict[str, Any] | None:
    calls = response.get("message", {}).get("tool_calls") or []
    if not calls:
        return None
    value = calls[0].get("function", {}).get("arguments")
    return value if isinstance(value, dict) else None


def main() -> None:
    rows: list[dict[str, Any]] = []
    for field_name in FIELD_NAMES:
        response = chat(field_name)
        arguments = first_arguments(response)
        field_value = arguments.get(field_name) if arguments is not None else None
        nested_value = None
        if isinstance(field_value, dict):
            nested_value = field_value.get(field_name, field_value.get("decision", field_value.get("value")))
        row = {
            "field_name": field_name,
            "arguments": arguments,
            "parse_ok": arguments is not None,
            "id_ok": arguments is not None and arguments.get("observation_id") == "obs_false",
            "shape_ok": isinstance(field_value, str),
            "semantic_ok": field_value == "consume_present" or nested_value == "consume_present",
            "prompt_tokens": int(response.get("prompt_eval_count", 0)),
            "output_tokens": int(response.get("eval_count", 0)),
            "elapsed_seconds": float(response.get("client_elapsed_seconds", 0.0)),
        }
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False))

    result = {
        "model": MODEL,
        "temperature": 0,
        "seed": 13,
        "summary": {
            "n": len(rows),
            "parse_ok": sum(row["parse_ok"] for row in rows),
            "id_ok": sum(row["id_ok"] for row in rows),
            "shape_ok": sum(row["shape_ok"] for row in rows),
            "semantic_ok": sum(row["semantic_ok"] for row in rows),
        },
        "rows": rows,
        "scope_note": "Single-task lexical-isolation probe; field name is the only schema variable.",
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
