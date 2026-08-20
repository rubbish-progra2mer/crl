from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V077_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
CONDITIONS = ("concrete", "warning", "scoped")
RESULT_PATH = Path(__file__).with_name(
    f"demonstration_argument_leakage_{MODEL.replace(':', '_').replace('.', '_')}_r1.json"
)


TOOL_SPECS: dict[str, dict[str, Any]] = {
    "update_delivery": {
        "description": "Update one order's destination and priority.",
        "properties": {
            "order_id": {"type": "string"},
            "destination": {"type": "string"},
            "priority": {"type": "string", "enum": ["standard", "express"]},
        },
    },
    "set_member_role": {
        "description": "Set one workspace member's role and expiration date.",
        "properties": {
            "workspace_id": {"type": "string"},
            "member_id": {"type": "string"},
            "role": {"type": "string", "enum": ["viewer", "editor", "admin"]},
            "expires_on": {"type": "string"},
        },
    },
    "schedule_report": {
        "description": "Schedule one report with an explicit time zone and format.",
        "properties": {
            "report_id": {"type": "string"},
            "run_at": {"type": "string"},
            "timezone": {"type": "string"},
            "format": {"type": "string", "enum": ["pdf", "csv"]},
        },
    },
    "issue_invoice": {
        "description": "Issue one invoice with an explicit amount, currency, and due date.",
        "properties": {
            "account_id": {"type": "string"},
            "amount": {"type": "integer"},
            "currency": {"type": "string"},
            "due_date": {"type": "string"},
        },
    },
    "configure_backup": {
        "description": "Configure one dataset backup policy.",
        "properties": {
            "dataset_id": {"type": "string"},
            "retention_days": {"type": "integer"},
            "region": {"type": "string"},
            "encrypted": {"type": "boolean"},
        },
    },
}


def trio(prefix: str, shared: dict[str, Any], varying: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, values in enumerate(varying, start=1):
        rows.append({**shared, **values, "_example_id": f"{prefix}{index}"})
    return rows


CASES: list[dict[str, Any]] = [
    {
        "id": "delivery_1", "family": "delivery", "tool": "update_delivery", "leak_field": "destination",
        "demos": trio("D1E", {"destination": "DEPOT-NORTH", "priority": "standard"}, [{"order_id": "ORD-101"}, {"order_id": "ORD-102"}, {"order_id": "ORD-103"}]),
        "current": {"order_id": "ORD-901", "destination": "DEPOT-SOUTH", "priority": "express"},
    },
    {
        "id": "delivery_2", "family": "delivery", "tool": "update_delivery", "leak_field": "destination",
        "demos": trio("D2E", {"destination": "HUB-BLUE", "priority": "express"}, [{"order_id": "ORD-211"}, {"order_id": "ORD-212"}, {"order_id": "ORD-213"}]),
        "current": {"order_id": "ORD-902", "destination": "HUB-GREEN", "priority": "standard"},
    },
    {
        "id": "delivery_3", "family": "delivery", "tool": "update_delivery", "leak_field": "destination",
        "demos": trio("D3E", {"destination": "SITE-ALPHA", "priority": "standard"}, [{"order_id": "ORD-321"}, {"order_id": "ORD-322"}, {"order_id": "ORD-323"}]),
        "current": {"order_id": "ORD-903", "destination": "SITE-OMEGA", "priority": "express"},
    },
    {
        "id": "delivery_4", "family": "delivery", "tool": "update_delivery", "leak_field": "destination",
        "demos": trio("D4E", {"destination": "BAY-07", "priority": "express"}, [{"order_id": "ORD-431"}, {"order_id": "ORD-432"}, {"order_id": "ORD-433"}]),
        "current": {"order_id": "ORD-904", "destination": "BAY-19", "priority": "standard"},
    },
    {
        "id": "role_1", "family": "role", "tool": "set_member_role", "leak_field": "role",
        "demos": trio("R1E", {"workspace_id": "WS-A", "role": "viewer", "expires_on": "2026-10-01"}, [{"member_id": "MEM-11"}, {"member_id": "MEM-12"}, {"member_id": "MEM-13"}]),
        "current": {"workspace_id": "WS-Z", "member_id": "MEM-91", "role": "editor", "expires_on": "2026-11-15"},
    },
    {
        "id": "role_2", "family": "role", "tool": "set_member_role", "leak_field": "role",
        "demos": trio("R2E", {"workspace_id": "WS-B", "role": "editor", "expires_on": "2026-09-30"}, [{"member_id": "MEM-21"}, {"member_id": "MEM-22"}, {"member_id": "MEM-23"}]),
        "current": {"workspace_id": "WS-Y", "member_id": "MEM-92", "role": "admin", "expires_on": "2026-12-20"},
    },
    {
        "id": "role_3", "family": "role", "tool": "set_member_role", "leak_field": "role",
        "demos": trio("R3E", {"workspace_id": "WS-C", "role": "admin", "expires_on": "2026-08-31"}, [{"member_id": "MEM-31"}, {"member_id": "MEM-32"}, {"member_id": "MEM-33"}]),
        "current": {"workspace_id": "WS-X", "member_id": "MEM-93", "role": "viewer", "expires_on": "2027-01-05"},
    },
    {
        "id": "role_4", "family": "role", "tool": "set_member_role", "leak_field": "role",
        "demos": trio("R4E", {"workspace_id": "WS-D", "role": "viewer", "expires_on": "2026-07-31"}, [{"member_id": "MEM-41"}, {"member_id": "MEM-42"}, {"member_id": "MEM-43"}]),
        "current": {"workspace_id": "WS-W", "member_id": "MEM-94", "role": "admin", "expires_on": "2027-02-10"},
    },
    {
        "id": "schedule_1", "family": "schedule", "tool": "schedule_report", "leak_field": "timezone",
        "demos": trio("S1E", {"timezone": "Asia/Shanghai", "format": "pdf"}, [{"report_id": "REP-11", "run_at": "2026-09-01T09:00:00"}, {"report_id": "REP-12", "run_at": "2026-09-02T09:00:00"}, {"report_id": "REP-13", "run_at": "2026-09-03T09:00:00"}]),
        "current": {"report_id": "REP-91", "run_at": "2026-10-01T14:30:00", "timezone": "Europe/Berlin", "format": "csv"},
    },
    {
        "id": "schedule_2", "family": "schedule", "tool": "schedule_report", "leak_field": "timezone",
        "demos": trio("S2E", {"timezone": "America/New_York", "format": "csv"}, [{"report_id": "REP-21", "run_at": "2026-09-11T08:00:00"}, {"report_id": "REP-22", "run_at": "2026-09-12T08:00:00"}, {"report_id": "REP-23", "run_at": "2026-09-13T08:00:00"}]),
        "current": {"report_id": "REP-92", "run_at": "2026-10-02T16:00:00", "timezone": "Asia/Tokyo", "format": "pdf"},
    },
    {
        "id": "schedule_3", "family": "schedule", "tool": "schedule_report", "leak_field": "timezone",
        "demos": trio("S3E", {"timezone": "UTC", "format": "pdf"}, [{"report_id": "REP-31", "run_at": "2026-09-21T07:00:00"}, {"report_id": "REP-32", "run_at": "2026-09-22T07:00:00"}, {"report_id": "REP-33", "run_at": "2026-09-23T07:00:00"}]),
        "current": {"report_id": "REP-93", "run_at": "2026-10-03T18:45:00", "timezone": "Australia/Sydney", "format": "csv"},
    },
    {
        "id": "schedule_4", "family": "schedule", "tool": "schedule_report", "leak_field": "timezone",
        "demos": trio("S4E", {"timezone": "Europe/London", "format": "csv"}, [{"report_id": "REP-41", "run_at": "2026-09-25T10:00:00"}, {"report_id": "REP-42", "run_at": "2026-09-26T10:00:00"}, {"report_id": "REP-43", "run_at": "2026-09-27T10:00:00"}]),
        "current": {"report_id": "REP-94", "run_at": "2026-10-04T06:15:00", "timezone": "America/Los_Angeles", "format": "pdf"},
    },
    {
        "id": "invoice_1", "family": "invoice", "tool": "issue_invoice", "leak_field": "currency",
        "demos": trio("I1E", {"currency": "USD", "due_date": "2026-09-30"}, [{"account_id": "ACC-11", "amount": 110}, {"account_id": "ACC-12", "amount": 120}, {"account_id": "ACC-13", "amount": 130}]),
        "current": {"account_id": "ACC-91", "amount": 910, "currency": "EUR", "due_date": "2026-10-31"},
    },
    {
        "id": "invoice_2", "family": "invoice", "tool": "issue_invoice", "leak_field": "currency",
        "demos": trio("I2E", {"currency": "EUR", "due_date": "2026-09-25"}, [{"account_id": "ACC-21", "amount": 210}, {"account_id": "ACC-22", "amount": 220}, {"account_id": "ACC-23", "amount": 230}]),
        "current": {"account_id": "ACC-92", "amount": 920, "currency": "JPY", "due_date": "2026-11-05"},
    },
    {
        "id": "invoice_3", "family": "invoice", "tool": "issue_invoice", "leak_field": "currency",
        "demos": trio("I3E", {"currency": "JPY", "due_date": "2026-09-20"}, [{"account_id": "ACC-31", "amount": 3100}, {"account_id": "ACC-32", "amount": 3200}, {"account_id": "ACC-33", "amount": 3300}]),
        "current": {"account_id": "ACC-93", "amount": 9300, "currency": "GBP", "due_date": "2026-11-10"},
    },
    {
        "id": "invoice_4", "family": "invoice", "tool": "issue_invoice", "leak_field": "currency",
        "demos": trio("I4E", {"currency": "GBP", "due_date": "2026-09-15"}, [{"account_id": "ACC-41", "amount": 410}, {"account_id": "ACC-42", "amount": 420}, {"account_id": "ACC-43", "amount": 430}]),
        "current": {"account_id": "ACC-94", "amount": 940, "currency": "CAD", "due_date": "2026-11-15"},
    },
    {
        "id": "backup_1", "family": "backup", "tool": "configure_backup", "leak_field": "retention_days",
        "demos": trio("B1E", {"retention_days": 30, "region": "region-east", "encrypted": True}, [{"dataset_id": "DATA-11"}, {"dataset_id": "DATA-12"}, {"dataset_id": "DATA-13"}]),
        "current": {"dataset_id": "DATA-91", "retention_days": 7, "region": "region-west", "encrypted": False},
    },
    {
        "id": "backup_2", "family": "backup", "tool": "configure_backup", "leak_field": "retention_days",
        "demos": trio("B2E", {"retention_days": 14, "region": "region-north", "encrypted": False}, [{"dataset_id": "DATA-21"}, {"dataset_id": "DATA-22"}, {"dataset_id": "DATA-23"}]),
        "current": {"dataset_id": "DATA-92", "retention_days": 45, "region": "region-south", "encrypted": True},
    },
    {
        "id": "backup_3", "family": "backup", "tool": "configure_backup", "leak_field": "retention_days",
        "demos": trio("B3E", {"retention_days": 60, "region": "region-central", "encrypted": True}, [{"dataset_id": "DATA-31"}, {"dataset_id": "DATA-32"}, {"dataset_id": "DATA-33"}]),
        "current": {"dataset_id": "DATA-93", "retention_days": 21, "region": "region-coast", "encrypted": False},
    },
    {
        "id": "backup_4", "family": "backup", "tool": "configure_backup", "leak_field": "retention_days",
        "demos": trio("B4E", {"retention_days": 90, "region": "region-a", "encrypted": False}, [{"dataset_id": "DATA-41"}, {"dataset_id": "DATA-42"}, {"dataset_id": "DATA-43"}]),
        "current": {"dataset_id": "DATA-94", "retention_days": 10, "region": "region-b", "encrypted": True},
    },
]


def strip_meta(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if not key.startswith("_")}


def tool_definition(name: str) -> dict[str, Any]:
    spec = TOOL_SPECS[name]
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": spec["description"],
            "parameters": {
                "type": "object",
                "properties": spec["properties"],
                "required": list(spec["properties"]),
                "additionalProperties": False,
            },
        },
    }


def concrete_demo(case: dict[str, Any], demo: dict[str, Any], index: int) -> str:
    args = strip_meta(demo)
    call = {"name": case["tool"], "arguments": args}
    return (
        f"Example {index} request (all arguments explicit): "
        f"{json.dumps(args, ensure_ascii=False, sort_keys=True)}\n"
        f"Example {index} tool call: {json.dumps(call, ensure_ascii=False, sort_keys=True)}"
    )


def scoped_demo(case: dict[str, Any], demo: dict[str, Any], index: int) -> str:
    args = strip_meta(demo)
    suffix = f"E{index}"
    bindings = {f"{key}__{suffix}": value for key, value in args.items()}
    symbolic_args = {key: f"${{{key}__{suffix}}}" for key in args}
    call = {"name": case["tool"], "arguments": symbolic_args}
    return (
        f"Example template {index}, local scope {suffix}. "
        f"Local bindings: {json.dumps(bindings, ensure_ascii=False, sort_keys=True)}\n"
        f"Symbolic tool call: {json.dumps(call, ensure_ascii=False, sort_keys=True)}"
    )


def build_messages(case: dict[str, Any], condition: str) -> list[dict[str, str]]:
    system = (
        "You are a tool-calling assistant. Call the available tool exactly once for the "
        "final current task. Return no prose."
    )
    if condition == "warning":
        system += (
            " Example-specific literal values belong only to their own examples; do not "
            "copy example values into the current call."
        )
    elif condition == "scoped":
        system += (
            " In symbolic demonstrations, every suffixed variable is local to that one "
            "example; the binding table preserves its value and the symbolic call shows "
            "the argument structure."
        )

    blocks = []
    for index, demo in enumerate(case["demos"], start=1):
        if condition == "scoped":
            blocks.append(scoped_demo(case, demo, index))
        else:
            blocks.append(concrete_demo(case, demo, index))
    current = case["current"]
    blocks.append(
        "Current task (all arguments explicit): call "
        f"{case['tool']} with arguments "
        f"{json.dumps(current, ensure_ascii=False, sort_keys=True)}."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n\n".join(blocks)},
    ]


def chat(case: dict[str, Any], condition: str, seed: int) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "tools": [tool_definition(case["tool"])],
        "options": {"temperature": 0, "seed": seed, "num_predict": 512},
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
    function = None
    if isinstance(calls, list) and len(calls) == 1 and isinstance(calls[0], dict):
        candidate = calls[0].get("function")
        if isinstance(candidate, dict):
            function = candidate
    name = function.get("name") if function else None
    arguments = parse_arguments(function.get("arguments")) if function else None
    valid = name == case["tool"] and arguments is not None
    exact = valid and arguments == case["current"]
    leak_field = case["leak_field"]
    demo_value = strip_meta(case["demos"][0])[leak_field]
    current_value = case["current"][leak_field]
    leakage = bool(
        valid
        and demo_value != current_value
        and arguments.get(leak_field) == demo_value
    )
    other_error = bool(valid and not exact and not leakage)
    return {
        "valid": bool(valid),
        "exact": bool(exact),
        "leakage": leakage,
        "other_error": other_error,
        "parsed_tool_name": name,
        "parsed_arguments": arguments,
        "demo_leak_value": demo_value,
        "current_target_value": current_value,
        "tool_call_count": len(calls) if isinstance(calls, list) else None,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for condition in CONDITIONS:
        selected = [row for row in rows if row["condition"] == condition]
        leakage_families = sorted({row["family"] for row in selected if row["score"]["leakage"]})
        metrics[condition] = {
            "n": len(selected),
            "valid_call_count": sum(row["score"]["valid"] for row in selected),
            "exact_count": sum(row["score"]["exact"] for row in selected),
            "leakage_count": sum(row["score"]["leakage"] for row in selected),
            "leakage_families": leakage_families,
            "leakage_family_count": len(leakage_families),
            "other_error_count": sum(row["score"]["other_error"] for row in selected),
        }
    concrete = metrics["concrete"]
    warning = metrics["warning"]
    scoped = metrics["scoped"]
    deltas = {
        "warning_leakage_reduction": concrete["leakage_count"] - warning["leakage_count"],
        "scoped_leakage_reduction": concrete["leakage_count"] - scoped["leakage_count"],
        "scoped_exact_gain_over_concrete": scoped["exact_count"] - concrete["exact_count"],
        "scoped_exact_gain_over_warning": scoped["exact_count"] - warning["exact_count"],
    }
    success_checks = {
        "concrete_phenomenon": concrete["leakage_count"] >= 6 and concrete["leakage_family_count"] >= 3,
        "structured_validity": all(metrics[name]["valid_call_count"] >= 19 for name in CONDITIONS),
        "warning_does_not_absorb": deltas["warning_leakage_reduction"] <= 1,
        "scoped_reduces_leakage": deltas["scoped_leakage_reduction"] >= 4,
        "scoped_beats_concrete_exact": deltas["scoped_exact_gain_over_concrete"] >= 4,
        "scoped_beats_warning_exact": deltas["scoped_exact_gain_over_warning"] >= 3,
    }
    return {
        "conditions": metrics,
        "deltas": deltas,
        "success_checks": success_checks,
        "all_success_conditions": all(success_checks.values()),
    }


def main() -> None:
    rows: list[dict[str, Any]] = []
    for case_index, case in enumerate(CASES):
        start = case_index % len(CONDITIONS)
        order = CONDITIONS[start:] + CONDITIONS[:start]
        for condition in order:
            response = chat(case, condition, 7700 + case_index)
            row = {
                "case_id": case["id"],
                "family": case["family"],
                "tool": case["tool"],
                "condition": condition,
                "seed": 7700 + case_index,
                "condition_order": list(order),
                "current": case["current"],
                "leak_field": case["leak_field"],
                "score": score(case, response),
                "elapsed_seconds": response.get("client_elapsed_seconds"),
                "prompt_tokens": response.get("prompt_eval_count"),
                "output_tokens": response.get("eval_count"),
                "raw_message": response.get("message"),
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "case": case["id"],
                        "condition": condition,
                        "valid": row["score"]["valid"],
                        "exact": row["score"]["exact"],
                        "leakage": row["score"]["leakage"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    result = {
        "model": MODEL,
        "endpoint": ENDPOINT,
        "case_count": len(CASES),
        "conditions": list(CONDITIONS),
        "temperature": 0,
        "tool_execution": False,
        "rows": rows,
        "metrics": summarize(rows),
        "scope_note": (
            "Benign local synthetic tool-call generation only. No generated call was executed, "
            "and no external tool or safety boundary was contacted."
        ),
    }
    RESULT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result["metrics"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
