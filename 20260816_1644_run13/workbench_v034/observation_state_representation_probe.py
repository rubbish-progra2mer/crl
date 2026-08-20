from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V034_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
RESULT_PATH = Path(__file__).with_name(
    f"observation_state_representation_{MODEL.replace(':', '_').replace('.', '_')}.json"
)

DECISIONS = [
    "consume_present",
    "request_missing",
    "wait_pending",
    "skip_not_applicable",
    "request_access",
    "retry_error",
]

TOOL = {
    "type": "function",
    "function": {
        "name": "handle_observation",
        "description": "Choose the next action for one tool observation.",
        "parameters": {
            "type": "object",
            "required": ["observation_id", "decision"],
            "properties": {
                "observation_id": {"type": "string"},
                "decision": {"type": "string", "enum": DECISIONS},
            },
        },
    },
}

CONTRACTS = {
    "http": (
        "HTTP-A contract: 200 means PRESENT even when data is 0, false, empty string, or null; "
        "404 means ABSENT; 202 means PENDING; 204 means NOT_APPLICABLE; 403 means REDACTED; "
        "500 or 503 means ERROR."
    ),
    "legacy": (
        "Legacy-B contract: code 0 means PRESENT regardless of the payload value; code 10 means ABSENT; "
        "code 20 means PENDING; code 30 means NOT_APPLICABLE; code 40 means REDACTED; code 50 means ERROR."
    ),
    "graphql": (
        "Graph-C contract: state ok means PRESENT whenever the data object contains the named field, including null, "
        "false, 0, or empty string; state missing means ABSENT; queued means PENDING; na means NOT_APPLICABLE; "
        "hidden means REDACTED; failed means ERROR."
    ),
    "record": (
        "Record-D contract: found true means PRESENT regardless of value; when found is false, reason missing means "
        "ABSENT, pending means PENDING, not_applicable means NOT_APPLICABLE, redacted means REDACTED, and error means ERROR."
    ),
}

STATE_TO_DECISION = {
    "PRESENT": "consume_present",
    "ABSENT": "request_missing",
    "PENDING": "wait_pending",
    "NOT_APPLICABLE": "skip_not_applicable",
    "REDACTED": "request_access",
    "ERROR": "retry_error",
}

CASES = [
    ("h_zero", "http", {"status": 200, "data": 0}, "PRESENT", "falsey"),
    ("h_false", "http", {"status": 200, "data": False}, "PRESENT", "falsey"),
    ("h_empty", "http", {"status": 200, "data": ""}, "PRESENT", "falsey"),
    ("h_null", "http", {"status": 200, "data": None}, "PRESENT", "falsey"),
    ("h_missing", "http", {"status": 404, "data": None}, "ABSENT", "control"),
    ("h_pending", "http", {"status": 202, "data": None}, "PENDING", "control"),
    ("h_na", "http", {"status": 204, "data": None}, "NOT_APPLICABLE", "control"),
    ("h_hidden", "http", {"status": 403, "data": None}, "REDACTED", "control"),
    ("h_error", "http", {"status": 503, "data": None}, "ERROR", "control"),
    ("l_zero", "legacy", {"code": 0, "payload": 0}, "PRESENT", "falsey"),
    ("l_false", "legacy", {"code": 0, "payload": False}, "PRESENT", "falsey"),
    ("l_empty", "legacy", {"code": 0, "payload": ""}, "PRESENT", "falsey"),
    ("l_missing", "legacy", {"code": 10, "payload": None}, "ABSENT", "control"),
    ("l_pending", "legacy", {"code": 20, "payload": None}, "PENDING", "control"),
    ("l_hidden", "legacy", {"code": 40, "payload": None}, "REDACTED", "control"),
    ("l_error", "legacy", {"code": 50, "payload": None}, "ERROR", "control"),
    ("g_null", "graphql", {"state": "ok", "data": {"quota": None}}, "PRESENT", "falsey"),
    ("g_false", "graphql", {"state": "ok", "data": {"enabled": False}}, "PRESENT", "falsey"),
    ("g_empty", "graphql", {"state": "ok", "data": {"nickname": ""}}, "PRESENT", "falsey"),
    ("g_missing", "graphql", {"state": "missing", "data": {}}, "ABSENT", "control"),
    ("g_pending", "graphql", {"state": "queued", "data": {}}, "PENDING", "control"),
    ("g_na", "graphql", {"state": "na", "data": {}}, "NOT_APPLICABLE", "control"),
    ("g_hidden", "graphql", {"state": "hidden", "data": {}}, "REDACTED", "control"),
    ("g_error", "graphql", {"state": "failed", "data": {}}, "ERROR", "control"),
    ("r_zero", "record", {"found": True, "value": 0}, "PRESENT", "falsey"),
    ("r_false", "record", {"found": True, "value": False}, "PRESENT", "falsey"),
    ("r_empty", "record", {"found": True, "value": ""}, "PRESENT", "falsey"),
    ("r_missing", "record", {"found": False, "reason": "missing"}, "ABSENT", "control"),
    ("r_pending", "record", {"found": False, "reason": "pending"}, "PENDING", "control"),
    ("r_na", "record", {"found": False, "reason": "not_applicable"}, "NOT_APPLICABLE", "control"),
    ("r_hidden", "record", {"found": False, "reason": "redacted"}, "REDACTED", "control"),
    ("r_error", "record", {"found": False, "reason": "error"}, "ERROR", "control"),
]


def chat(user_content: str) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0, "seed": 11, "num_predict": 1024},
        "messages": [
            {
                "role": "system",
                "content": (
                    "Apply the supplied source contract exactly. A PRESENT falsey value is still present. "
                    "Call handle_observation once and do not answer in prose."
                ),
            },
            {"role": "user", "content": user_content},
        ],
        "tools": [TOOL],
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


def arguments(response: dict[str, Any]) -> dict[str, Any] | None:
    calls = response.get("message", {}).get("tool_calls") or []
    if not calls:
        return None
    value = calls[0].get("function", {}).get("arguments")
    return value if isinstance(value, dict) else None


def usage(response: dict[str, Any]) -> dict[str, float | int]:
    return {
        "prompt_tokens": int(response.get("prompt_eval_count", 0)),
        "output_tokens": int(response.get("eval_count", 0)),
        "elapsed_seconds": float(response.get("client_elapsed_seconds", 0.0)),
    }


def evaluate(case_id: str, state: str, response: dict[str, Any]) -> dict[str, Any]:
    value = arguments(response)
    raw_decision = value.get("decision") if value is not None else None
    normalized_decision = raw_decision
    if isinstance(raw_decision, dict):
        normalized_decision = raw_decision.get("decision", raw_decision.get("value"))
    return {
        "arguments": value,
        "parse_ok": value is not None,
        "id_ok": value is not None and value.get("observation_id") == case_id,
        "decision_format_ok": isinstance(raw_decision, str),
        "decision_ok": normalized_decision == STATE_TO_DECISION[state],
    }


def prompt(case_id: str, contract_name: str, raw: dict[str, Any], state: str, mode: str) -> str:
    if mode == "raw":
        observation = raw
    else:
        observation = {"observation_id": case_id, "state": state, "value": raw.get("data", raw.get("payload", raw.get("value")))}
    return (
        f"Source contract:\n{CONTRACTS[contract_name]}\n\n"
        f"Observation id: {case_id}\n"
        f"Observation ({mode} representation):\n{json.dumps(observation, ensure_ascii=False)}\n\n"
        "Decision policy: PRESENT -> consume_present; ABSENT -> request_missing; PENDING -> wait_pending; "
        "NOT_APPLICABLE -> skip_not_applicable; REDACTED -> request_access; ERROR -> retry_error."
    )


def main() -> None:
    rows: list[dict[str, Any]] = []
    for case_id, contract_name, raw, state, category in CASES:
        row: dict[str, Any] = {
            "case_id": case_id,
            "contract": contract_name,
            "state": state,
            "category": category,
            "raw_observation": raw,
        }
        for mode in ("raw", "tagged"):
            response = chat(prompt(case_id, contract_name, raw, state, mode))
            row[mode] = {"score": evaluate(case_id, state, response), "usage": usage(response)}
        rows.append(row)
        print(json.dumps({"case_id": case_id, "raw": row["raw"]["score"], "tagged": row["tagged"]["score"]}, ensure_ascii=False))

    summary: dict[str, Any] = {}
    for mode in ("raw", "tagged"):
        summary[mode] = {
            "n": len(rows),
            "parse_ok": sum(row[mode]["score"]["parse_ok"] for row in rows),
            "id_ok": sum(row[mode]["score"]["id_ok"] for row in rows),
            "decision_format_ok": sum(row[mode]["score"]["decision_format_ok"] for row in rows),
            "decision_ok": sum(row[mode]["score"]["decision_ok"] for row in rows),
            "falsey_decision_ok": sum(
                row[mode]["score"]["decision_ok"] for row in rows if row["category"] == "falsey"
            ),
            "falsey_n": sum(row["category"] == "falsey" for row in rows),
            "prompt_tokens": sum(row[mode]["usage"]["prompt_tokens"] for row in rows),
            "output_tokens": sum(row[mode]["usage"]["output_tokens"] for row in rows),
            "elapsed_seconds": sum(row[mode]["usage"]["elapsed_seconds"] for row in rows),
        }
    result = {
        "model": MODEL,
        "temperature": 0,
        "seed": 11,
        "summary": summary,
        "rows": rows,
        "scope_note": (
            "Local synthetic representation probe. Raw and tagged conditions expose the same state information; "
            "tagged form precomputes the source-contract interpretation."
        ),
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
