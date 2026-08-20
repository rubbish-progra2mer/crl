from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "experiment_v001" / "exp-h14-002-screen-b"
API_URL = "http://127.0.0.1:11434/api/chat"


FUNCTIONS = {
    "calculate_delivery_quote": {
        "alias": "derive_logistics_charge",
        "description": "Calculate a delivery price in dollars for a parcel sent to a city.",
        "arguments": {
            "destination_city": ("locality", "string", "Destination city name."),
            "parcel_weight_kg": ("load_kg", "number", "Parcel weight in kilograms."),
            "priority": ("urgency", "string", "Service level: standard or express."),
        },
    },
    "convert_temperature": {
        "alias": "translate_thermal_reading",
        "description": "Convert a numeric temperature between Celsius and Fahrenheit.",
        "arguments": {
            "value": ("magnitude", "number", "Numeric temperature value."),
            "from_unit": ("source_scale", "string", "Input scale: celsius or fahrenheit."),
            "to_unit": ("target_scale", "string", "Output scale: celsius or fahrenheit."),
        },
    },
    "lookup_inventory": {
        "alias": "inspect_stock_record",
        "description": "Look up available inventory for a product at a warehouse.",
        "arguments": {
            "product_code": ("item_identifier", "string", "Exact product code."),
            "warehouse": ("storage_site", "string", "Warehouse code."),
        },
    },
    "schedule_meeting": {
        "alias": "reserve_calendar_slot",
        "description": "Schedule a meeting on a day at a starting hour for a duration.",
        "arguments": {
            "day": ("calendar_day", "string", "Calendar date in YYYY-MM-DD format."),
            "start_hour": ("beginning_hour", "integer", "Starting hour from 0 through 23."),
            "duration_minutes": ("span_minutes", "integer", "Meeting duration in minutes."),
        },
    },
}


CASES = [
    {"id": "ship-1", "prompt": "How much to send a 2.5 kg parcel to Berlin with express service?", "fn": "calculate_delivery_quote", "args": {"destination_city": "Berlin", "parcel_weight_kg": 2.5, "priority": "express"}},
    {"id": "ship-2", "prompt": "Price standard delivery of a 7 kg package to Madrid.", "fn": "calculate_delivery_quote", "args": {"destination_city": "Madrid", "parcel_weight_kg": 7, "priority": "standard"}},
    {"id": "ship-3", "prompt": "Quote express shipping to Tokyo for a parcel weighing 1.2 kilograms.", "fn": "calculate_delivery_quote", "args": {"destination_city": "Tokyo", "parcel_weight_kg": 1.2, "priority": "express"}},
    {"id": "temp-1", "prompt": "Convert 32 Fahrenheit to Celsius.", "fn": "convert_temperature", "args": {"value": 32, "from_unit": "fahrenheit", "to_unit": "celsius"}},
    {"id": "temp-2", "prompt": "What is 20 Celsius in Fahrenheit?", "fn": "convert_temperature", "args": {"value": 20, "from_unit": "celsius", "to_unit": "fahrenheit"}},
    {"id": "temp-3", "prompt": "Translate -4 degrees Fahrenheit into Celsius.", "fn": "convert_temperature", "args": {"value": -4, "from_unit": "fahrenheit", "to_unit": "celsius"}},
    {"id": "stock-1", "prompt": "Check product AX-17 at warehouse W2.", "fn": "lookup_inventory", "args": {"product_code": "AX-17", "warehouse": "W2"}},
    {"id": "stock-2", "prompt": "How many units of BETA-9 are available in warehouse NORTH?", "fn": "lookup_inventory", "args": {"product_code": "BETA-9", "warehouse": "NORTH"}},
    {"id": "stock-3", "prompt": "Look up inventory for item Q4 at storage warehouse S1.", "fn": "lookup_inventory", "args": {"product_code": "Q4", "warehouse": "S1"}},
    {"id": "meet-1", "prompt": "Book a 45 minute meeting on 2026-09-03 starting at 14:00.", "fn": "schedule_meeting", "args": {"day": "2026-09-03", "start_hour": 14, "duration_minutes": 45}},
    {"id": "meet-2", "prompt": "Schedule 30 minutes on 2026-10-11 from 9 AM.", "fn": "schedule_meeting", "args": {"day": "2026-10-11", "start_hour": 9, "duration_minutes": 30}},
    {"id": "meet-3", "prompt": "Reserve a 90-minute meeting for 2026-12-01 beginning at hour 16.", "fn": "schedule_meeting", "args": {"day": "2026-12-01", "start_hour": 16, "duration_minutes": 90}},
]


def make_tools(alias_mode: bool) -> list[dict[str, Any]]:
    definitions = []
    for canonical_name, info in FUNCTIONS.items():
        props = {}
        required = []
        for canonical_arg, (alias_arg, kind, description) in info["arguments"].items():
            exposed_arg = alias_arg if alias_mode else canonical_arg
            spec: dict[str, Any] = {"type": kind, "description": description}
            if canonical_arg == "priority":
                spec["enum"] = ["standard", "express"]
            if canonical_arg in {"from_unit", "to_unit"}:
                spec["enum"] = ["celsius", "fahrenheit"]
            props[exposed_arg] = spec
            required.append(exposed_arg)
        definitions.append({
            "type": "function",
            "function": {
                "name": info["alias"] if alias_mode else canonical_name,
                "description": info["description"],
                "parameters": {"type": "object", "properties": props, "required": required},
            },
        })
    return definitions


def normalize_call(call: dict[str, Any], alias_mode: bool) -> dict[str, Any]:
    fn = call.get("function") or {}
    emitted_name = fn.get("name")
    emitted_args = fn.get("arguments") or {}
    if isinstance(emitted_args, str):
        emitted_args = json.loads(emitted_args)
    for canonical_name, info in FUNCTIONS.items():
        allowed_name = info["alias"] if alias_mode else canonical_name
        if emitted_name != allowed_name:
            continue
        normalized = {}
        for canonical_arg, (alias_arg, _kind, _description) in info["arguments"].items():
            exposed_arg = alias_arg if alias_mode else canonical_arg
            if exposed_arg in emitted_args:
                normalized[canonical_arg] = emitted_args[exposed_arg]
        return {"name": canonical_name, "arguments": normalized}
    return {"name": emitted_name, "arguments": emitted_args}


def same_scalar(left: Any, right: Any) -> bool:
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(float(left) - float(right)) <= 1e-9
    return left == right


def score(case: dict[str, Any], normalized: dict[str, Any]) -> tuple[bool, str | None]:
    if normalized["name"] != case["fn"]:
        return False, "wrong_tool"
    got = normalized["arguments"]
    expected = case["args"]
    if set(got) != set(expected):
        return False, "wrong_arguments"
    if not all(same_scalar(got[key], expected[key]) for key in expected):
        return False, "wrong_arguments"
    return True, None


def execute(case: dict[str, Any], alias_mode: bool) -> dict[str, Any]:
    response = requests.post(
        API_URL,
        timeout=180,
        json={
            "model": "qwen3:4b",
            "messages": [
                {"role": "system", "content": "Call the single appropriate supplied tool immediately. Return a tool call, not a prose answer."},
                {"role": "user", "content": case["prompt"]},
            ],
            "tools": make_tools(alias_mode),
            "stream": False,
            "think": False,
            "options": {"temperature": 0, "seed": 14002, "num_predict": 1024},
        },
    )
    response.raise_for_status()
    body = response.json()
    calls = (body.get("message") or {}).get("tool_calls") or []
    base = {"case_id": case["id"], "variant": "renamed" if alias_mode else "canonical", "done_reason": body.get("done_reason"), "model": body.get("model"), "call_count": len(calls)}
    if len(calls) != 1:
        return {**base, "success": False, "error": "no_single_tool_call", "content": (body.get("message") or {}).get("content")}
    normalized = normalize_call(calls[0], alias_mode)
    success, error = score(case, normalized)
    return {**base, "success": success, "error": error, "normalized_call": normalized, "emitted_call": calls[0]}


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    observations = []
    for case in CASES:
        for alias_mode in (False, True):
            item = execute(case, alias_mode)
            observations.append(item)
            print(json.dumps({"case_id": item["case_id"], "variant": item["variant"], "success": item["success"], "error": item["error"], "done_reason": item["done_reason"]}, ensure_ascii=False), flush=True)
    pairs = {}
    for item in observations:
        pairs.setdefault(item["case_id"], {})[item["variant"]] = item
    inconsistent = [case_id for case_id, pair in pairs.items() if pair["canonical"]["success"] != pair["renamed"]["success"]]
    metrics = {
        "artifact_kind": "run14_independent_screening_metrics",
        "evidence_fidelity": "SCREENING",
        "independent_implementation_count": 2,
        "model": "qwen3:4b",
        "seed": 14002,
        "task_count": len(CASES),
        "call_count": len(observations),
        "canonical_successes": sum(x["success"] for x in observations if x["variant"] == "canonical"),
        "renamed_successes": sum(x["success"] for x in observations if x["variant"] == "renamed"),
        "paired_disagreement_count": len(inconsistent),
        "paired_disagreement_task_ids": inconsistent,
        "zero_or_multiple_call_count": sum(x["error"] == "no_single_tool_call" for x in observations),
        "wrong_tool_count": sum(x["error"] == "wrong_tool" for x in observations),
        "wrong_arguments_count": sum(x["error"] == "wrong_arguments" for x in observations),
        "scientific_boundary": "Second independent local screening implementation; not representative evidence.",
    }
    (OUTPUT_DIR / "observations.json").write_text(json.dumps(observations, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (OUTPUT_DIR / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
