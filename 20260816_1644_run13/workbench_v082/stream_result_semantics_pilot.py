from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V082_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
CONDITIONS = ("raw_stream", "warning", "materialized")
ACTIONS = [
    "RELEASE", "WAIT", "REJECT", "FULFILL", "BACKORDER",
    "RUN", "PAUSE", "ESCALATE", "CLEAR",
]
RESULT_PATH = Path(__file__).with_name(
    f"stream_result_semantics_{MODEL.replace(':', '_').replace('.', '_')}_r1.json"
)


def snapshot_case(case_id: str, family: str, events: list[dict[str, Any]], expected: str) -> dict[str, Any]:
    return {
        "id": case_id,
        "family": family,
        "mode": "SNAPSHOT",
        "contract": "Each payload is the complete current state. Only the payload with the highest seq is current.",
        "initial": None,
        "events": [{"seq": i + 1, "payload": value} for i, value in enumerate(events)],
        "materialized": events[-1],
        "rule": "Choose RELEASE for status APPROVED, REJECT for status REJECTED, otherwise WAIT.",
        "expected": expected,
    }


def delta_case(case_id: str, family: str, initial: dict[str, Any], deltas: list[dict[str, Any]], expected: str) -> dict[str, Any]:
    current = dict(initial)
    events = []
    for index, fields in enumerate(deltas, start=1):
        current.update(fields)
        events.append({"seq": index, "fields": fields})
    return {
        "id": case_id,
        "family": family,
        "mode": "DELTA",
        "contract": "Start from initial. Each event overwrites only its listed fields; unlisted fields retain their latest value.",
        "initial": initial,
        "events": events,
        "materialized": current,
        "rule": "Choose FULFILL when stock is at least reserved; otherwise choose BACKORDER.",
        "expected": expected,
    }


def patch_case(case_id: str, family: str, initial: dict[str, Any], ops: list[dict[str, Any]], expected: str) -> dict[str, Any]:
    current = dict(initial)
    for op in ops:
        if op["op"] == "set":
            current[op["field"]] = op["value"]
        elif op["op"] == "remove":
            current.pop(op["field"], None)
        else:
            raise ValueError(op)
    return {
        "id": case_id,
        "family": family,
        "mode": "PATCH",
        "contract": "Apply operations by increasing seq. set overwrites a field; remove deletes it. Missing confirmed counts as false.",
        "initial": initial,
        "events": [{"seq": i + 1, **op} for i, op in enumerate(ops)],
        "materialized": current,
        "rule": "Choose RUN only when enabled is true, conflict is false, and confirmed is true; otherwise choose PAUSE.",
        "expected": expected,
    }


def retract_case(case_id: str, family: str, events: list[dict[str, Any]], expected: str) -> dict[str, Any]:
    active: dict[str, dict[str, Any]] = {}
    numbered = []
    for index, event in enumerate(events, start=1):
        numbered.append({"seq": index, **event})
        if event["op"] == "assert":
            active[event["fact_id"]] = {"severity": event["severity"], "message": event["message"]}
        elif event["op"] == "retract":
            active.pop(event["fact_id"], None)
        else:
            raise ValueError(event)
    return {
        "id": case_id,
        "family": family,
        "mode": "ASSERT_RETRACT",
        "contract": "assert adds or replaces the fact_id; retract removes that fact_id. Only active facts after the highest seq are current.",
        "initial": {},
        "events": numbered,
        "materialized": {"active_facts": active},
        "rule": "Choose ESCALATE when any active fact has severity CRITICAL; otherwise choose CLEAR.",
        "expected": expected,
    }


CASES: list[dict[str, Any]] = [
    snapshot_case("snap_1", "approval", [{"request": "A1", "status": "APPROVED"}, {"request": "A1", "status": "PENDING"}], "WAIT"),
    snapshot_case("snap_2", "approval", [{"request": "A2", "status": "PENDING"}, {"request": "A2", "status": "APPROVED"}], "RELEASE"),
    snapshot_case("snap_3", "approval", [{"request": "A3", "status": "APPROVED"}, {"request": "A3", "status": "REJECTED"}], "REJECT"),
    snapshot_case("snap_4", "approval", [{"request": "A4", "status": "REJECTED"}, {"request": "A4", "status": "APPROVED"}], "RELEASE"),
    snapshot_case("snap_5", "approval", [{"request": "A5", "status": "APPROVED"}, {"request": "A5", "status": "HELD"}], "WAIT"),
    snapshot_case("snap_6", "approval", [{"request": "A6", "status": "HELD"}, {"request": "A6", "status": "REJECTED"}], "REJECT"),
    delta_case("delta_1", "inventory", {"stock": 12, "reserved": 5}, [{"stock": 4}], "BACKORDER"),
    delta_case("delta_2", "inventory", {"stock": 3, "reserved": 7}, [{"stock": 9}], "FULFILL"),
    delta_case("delta_3", "inventory", {"stock": 10, "reserved": 4}, [{"reserved": 11}], "BACKORDER"),
    delta_case("delta_4", "inventory", {"stock": 6, "reserved": 9}, [{"reserved": 2}], "FULFILL"),
    delta_case("delta_5", "inventory", {"stock": 20, "reserved": 8}, [{"stock": 7}, {"reserved": 9}], "BACKORDER"),
    delta_case("delta_6", "inventory", {"stock": 2, "reserved": 8}, [{"stock": 10}, {"reserved": 6}], "FULFILL"),
    patch_case("patch_1", "schedule", {"enabled": True, "conflict": False, "confirmed": True}, [{"op": "set", "field": "conflict", "value": True}], "PAUSE"),
    patch_case("patch_2", "schedule", {"enabled": True, "conflict": True, "confirmed": True}, [{"op": "set", "field": "conflict", "value": False}], "RUN"),
    patch_case("patch_3", "schedule", {"enabled": True, "conflict": False, "confirmed": True}, [{"op": "remove", "field": "confirmed"}], "PAUSE"),
    patch_case("patch_4", "schedule", {"enabled": False, "conflict": False}, [{"op": "set", "field": "enabled", "value": True}, {"op": "set", "field": "confirmed", "value": True}], "RUN"),
    patch_case("patch_5", "schedule", {"enabled": True, "conflict": False, "confirmed": False}, [{"op": "set", "field": "confirmed", "value": True}, {"op": "set", "field": "enabled", "value": False}], "PAUSE"),
    patch_case("patch_6", "schedule", {"enabled": False, "conflict": True, "confirmed": True}, [{"op": "set", "field": "enabled", "value": True}, {"op": "set", "field": "conflict", "value": False}], "RUN"),
    retract_case("retract_1", "alert", [{"op": "assert", "fact_id": "F1", "severity": "CRITICAL", "message": "temperature high"}, {"op": "retract", "fact_id": "F1"}], "CLEAR"),
    retract_case("retract_2", "alert", [{"op": "assert", "fact_id": "F2", "severity": "INFO", "message": "check complete"}, {"op": "assert", "fact_id": "F3", "severity": "CRITICAL", "message": "pressure high"}], "ESCALATE"),
    retract_case("retract_3", "alert", [{"op": "assert", "fact_id": "F4", "severity": "CRITICAL", "message": "door open"}, {"op": "assert", "fact_id": "F5", "severity": "INFO", "message": "operator present"}, {"op": "retract", "fact_id": "F4"}], "CLEAR"),
    retract_case("retract_4", "alert", [{"op": "assert", "fact_id": "F6", "severity": "CRITICAL", "message": "voltage high"}, {"op": "retract", "fact_id": "F6"}, {"op": "assert", "fact_id": "F7", "severity": "CRITICAL", "message": "coolant low"}], "ESCALATE"),
    retract_case("retract_5", "alert", [{"op": "assert", "fact_id": "F8", "severity": "INFO", "message": "scan started"}, {"op": "assert", "fact_id": "F9", "severity": "CRITICAL", "message": "scan failed"}, {"op": "retract", "fact_id": "F9"}], "CLEAR"),
    retract_case("retract_6", "alert", [{"op": "assert", "fact_id": "F10", "severity": "INFO", "message": "network stable"}, {"op": "retract", "fact_id": "F10"}, {"op": "assert", "fact_id": "F11", "severity": "CRITICAL", "message": "network lost"}], "ESCALATE"),
]


def tool_definition() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "commit_decision",
            "description": "Commit the unique decision for one synthetic case.",
            "parameters": {
                "type": "object",
                "properties": {
                    "case_id": {"type": "string"},
                    "action": {"type": "string", "enum": ACTIONS},
                },
                "required": ["case_id", "action"],
                "additionalProperties": False,
            },
        },
    }


def build_messages(case: dict[str, Any], condition: str) -> list[dict[str, str]]:
    system = "You are a deterministic tool-using assistant. Call commit_decision exactly once. Return no prose."
    if condition == "warning":
        system += " Do not treat all events as simultaneously current facts. Materialize the final state using the declared stream contract before deciding."
    if condition == "materialized":
        body = {
            "case_id": case["id"],
            "current_state": case["materialized"],
            "decision_rule": case["rule"],
        }
    else:
        body = {
            "case_id": case["id"],
            "stream_mode": case["mode"],
            "stream_contract": case["contract"],
            "initial_state": case["initial"],
            "events": case["events"],
            "decision_rule": case["rule"],
        }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(body, ensure_ascii=False, sort_keys=True)},
    ]


def chat(case: dict[str, Any], condition: str, seed: int) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "tools": [tool_definition()],
        "options": {"temperature": 0, "seed": seed, "num_predict": 256},
        "messages": build_messages(case, condition),
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))
    result["client_elapsed_seconds"] = time.perf_counter() - started
    return result


def parse_arguments(raw: Any) -> dict[str, Any] | None:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None
    return None


def score(case: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    message = response.get("message", {})
    calls = message.get("tool_calls", []) if isinstance(message, dict) else []
    function = calls[0].get("function") if isinstance(calls, list) and len(calls) == 1 and isinstance(calls[0], dict) else None
    arguments = parse_arguments(function.get("arguments")) if isinstance(function, dict) else None
    valid = bool(
        isinstance(function, dict)
        and function.get("name") == "commit_decision"
        and isinstance(arguments, dict)
        and arguments.get("case_id") == case["id"]
        and arguments.get("action") in ACTIONS
        and set(arguments) == {"case_id", "action"}
    )
    exact = valid and arguments["action"] == case["expected"]
    return {
        "valid": valid,
        "exact": bool(exact),
        "expected_action": case["expected"],
        "parsed_arguments": arguments,
        "tool_call_count": len(calls) if isinstance(calls, list) else None,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for condition in CONDITIONS:
        selected = [row for row in rows if row["condition"] == condition]
        errors = [row for row in selected if row["score"]["valid"] and not row["score"]["exact"]]
        metrics[condition] = {
            "n": len(selected),
            "valid_call_count": sum(row["score"]["valid"] for row in selected),
            "exact_count": sum(row["score"]["exact"] for row in selected),
            "error_count": len(errors),
            "error_modes": sorted({row["mode"] for row in errors}),
            "error_mode_count": len({row["mode"] for row in errors}),
            "error_families": sorted({row["family"] for row in errors}),
            "error_family_count": len({row["family"] for row in errors}),
        }
    raw = metrics["raw_stream"]
    warning = metrics["warning"]
    materialized = metrics["materialized"]
    deltas = {
        "warning_error_reduction": raw["error_count"] - warning["error_count"],
        "materialized_error_reduction": raw["error_count"] - materialized["error_count"],
        "materialized_exact_gain_over_raw": materialized["exact_count"] - raw["exact_count"],
        "materialized_exact_gain_over_warning": materialized["exact_count"] - warning["exact_count"],
    }
    checks = {
        "raw_phenomenon": raw["error_count"] >= 6 and raw["error_mode_count"] >= 3 and raw["error_family_count"] >= 3,
        "structured_validity": all(metrics[name]["valid_call_count"] >= 23 for name in CONDITIONS),
        "warning_does_not_absorb": deltas["warning_error_reduction"] <= 2,
        "materialized_reduces_errors": deltas["materialized_error_reduction"] >= 5,
        "materialized_beats_raw_exact": deltas["materialized_exact_gain_over_raw"] >= 5,
        "materialized_beats_warning_exact": deltas["materialized_exact_gain_over_warning"] >= 3,
    }
    return {"conditions": metrics, "deltas": deltas, "success_checks": checks, "all_success_conditions": all(checks.values())}


def main() -> None:
    rows: list[dict[str, Any]] = []
    for case_index, case in enumerate(CASES):
        start = case_index % len(CONDITIONS)
        order = CONDITIONS[start:] + CONDITIONS[:start]
        for condition in order:
            response = chat(case, condition, 8200 + case_index)
            row = {
                "case_id": case["id"],
                "family": case["family"],
                "mode": case["mode"],
                "condition": condition,
                "seed": 8200 + case_index,
                "condition_order": list(order),
                "score": score(case, response),
                "elapsed_seconds": response.get("client_elapsed_seconds"),
                "prompt_tokens": response.get("prompt_eval_count"),
                "output_tokens": response.get("eval_count"),
                "raw_message": response.get("message"),
            }
            rows.append(row)
            print(json.dumps({"case": case["id"], "condition": condition, "valid": row["score"]["valid"], "exact": row["score"]["exact"]}, ensure_ascii=False), flush=True)
    result = {
        "model": MODEL,
        "endpoint": ENDPOINT,
        "case_count": len(CASES),
        "conditions": list(CONDITIONS),
        "temperature": 0,
        "tool_execution": False,
        "rows": rows,
        "metrics": summarize(rows),
        "scope_note": "Benign local synthetic decision generation only; generated decisions were not executed and no external tool or safety boundary was contacted.",
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["metrics"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
