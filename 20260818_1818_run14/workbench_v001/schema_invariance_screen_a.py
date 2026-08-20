from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


RUN_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = RUN_ROOT / "experiment_v001" / "exp-h14-002-screen-a"
ENDPOINT = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen3:4b"
SEED = 14001


TOOLS = [
    {
        "canonical_name": "calculate_delivery_quote",
        "renamed_name": "derive_logistics_charge",
        "description": "Calculate a delivery price in dollars for a parcel sent to a city.",
        "parameters": [
            ("destination_city", "locality", "string", "Destination city name."),
            ("parcel_weight_kg", "load_kg", "number", "Parcel weight in kilograms."),
            ("priority", "urgency", "string", "Service level: standard or express."),
        ],
    },
    {
        "canonical_name": "convert_temperature",
        "renamed_name": "translate_thermal_reading",
        "description": "Convert a numeric temperature between Celsius and Fahrenheit.",
        "parameters": [
            ("value", "magnitude", "number", "Numeric temperature value."),
            ("from_unit", "source_scale", "string", "Input scale: celsius or fahrenheit."),
            ("to_unit", "target_scale", "string", "Output scale: celsius or fahrenheit."),
        ],
    },
    {
        "canonical_name": "lookup_inventory",
        "renamed_name": "inspect_stock_record",
        "description": "Look up available inventory for a product at a warehouse.",
        "parameters": [
            ("product_code", "item_identifier", "string", "Exact product code."),
            ("warehouse", "storage_site", "string", "Warehouse code."),
        ],
    },
    {
        "canonical_name": "schedule_meeting",
        "renamed_name": "reserve_calendar_slot",
        "description": "Schedule a meeting on a day at a starting hour for a duration.",
        "parameters": [
            ("day", "calendar_day", "string", "Calendar date in YYYY-MM-DD format."),
            ("start_hour", "beginning_hour", "integer", "Starting hour from 0 through 23."),
            ("duration_minutes", "span_minutes", "integer", "Meeting duration in minutes."),
        ],
    },
]


TASKS = [
    ("ship-1", "How much to send a 2.5 kg parcel to Berlin with express service?", "calculate_delivery_quote", {"destination_city": "Berlin", "parcel_weight_kg": 2.5, "priority": "express"}),
    ("ship-2", "Price standard delivery of a 7 kg package to Madrid.", "calculate_delivery_quote", {"destination_city": "Madrid", "parcel_weight_kg": 7, "priority": "standard"}),
    ("ship-3", "Quote express shipping to Tokyo for a parcel weighing 1.2 kilograms.", "calculate_delivery_quote", {"destination_city": "Tokyo", "parcel_weight_kg": 1.2, "priority": "express"}),
    ("temp-1", "Convert 32 Fahrenheit to Celsius.", "convert_temperature", {"value": 32, "from_unit": "fahrenheit", "to_unit": "celsius"}),
    ("temp-2", "What is 20 Celsius in Fahrenheit?", "convert_temperature", {"value": 20, "from_unit": "celsius", "to_unit": "fahrenheit"}),
    ("temp-3", "Translate -4 degrees Fahrenheit into Celsius.", "convert_temperature", {"value": -4, "from_unit": "fahrenheit", "to_unit": "celsius"}),
    ("stock-1", "Check product AX-17 at warehouse W2.", "lookup_inventory", {"product_code": "AX-17", "warehouse": "W2"}),
    ("stock-2", "How many units of BETA-9 are available in warehouse NORTH?", "lookup_inventory", {"product_code": "BETA-9", "warehouse": "NORTH"}),
    ("stock-3", "Look up inventory for item Q4 at storage warehouse S1.", "lookup_inventory", {"product_code": "Q4", "warehouse": "S1"}),
    ("meet-1", "Book a 45 minute meeting on 2026-09-03 starting at 14:00.", "schedule_meeting", {"day": "2026-09-03", "start_hour": 14, "duration_minutes": 45}),
    ("meet-2", "Schedule 30 minutes on 2026-10-11 from 9 AM.", "schedule_meeting", {"day": "2026-10-11", "start_hour": 9, "duration_minutes": 30}),
    ("meet-3", "Reserve a 90-minute meeting for 2026-12-01 beginning at hour 16.", "schedule_meeting", {"day": "2026-12-01", "start_hour": 16, "duration_minutes": 90}),
]


def schema_for(tool: dict[str, Any], renamed: bool) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    required: list[str] = []
    for canonical, alternate, value_type, description in tool["parameters"]:
        name = alternate if renamed else canonical
        item: dict[str, Any] = {"type": value_type, "description": description}
        if description.endswith("standard or express."):
            item["enum"] = ["standard", "express"]
        if description.endswith("celsius or fahrenheit."):
            item["enum"] = ["celsius", "fahrenheit"]
        properties[name] = item
        required.append(name)
    return {
        "type": "function",
        "function": {
            "name": tool["renamed_name"] if renamed else tool["canonical_name"],
            "description": tool["description"],
            "parameters": {"type": "object", "properties": properties, "required": required},
        },
    }


def canonicalize(name: str, arguments: dict[str, Any], renamed: bool) -> tuple[str, dict[str, Any]]:
    for tool in TOOLS:
        exposed = tool["renamed_name"] if renamed else tool["canonical_name"]
        if name != exposed:
            continue
        mapped: dict[str, Any] = {}
        for canonical, alternate, _value_type, _description in tool["parameters"]:
            exposed_arg = alternate if renamed else canonical
            if exposed_arg in arguments:
                mapped[canonical] = arguments[exposed_arg]
        return tool["canonical_name"], mapped
    return name, arguments


def equal_value(actual: Any, expected: Any) -> bool:
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return abs(float(actual) - float(expected)) < 1e-9
    return actual == expected


def run_call(task: tuple[str, str, str, dict[str, Any]], renamed: bool) -> dict[str, Any]:
    task_id, user_text, expected_name, expected_args = task
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Select exactly one supplied tool and fill its arguments from the user request. Do not answer in prose."},
            {"role": "user", "content": user_text},
        ],
        "tools": [schema_for(tool, renamed) for tool in TOOLS],
        "stream": False,
        "think": False,
        "options": {"temperature": 0, "seed": SEED, "num_predict": 256},
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return {"task_id": task_id, "variant": "renamed" if renamed else "canonical", "success": False, "error_stage": "transport_or_parse", "error": repr(error)}
    tool_calls = raw.get("message", {}).get("tool_calls") or []
    if len(tool_calls) != 1:
        return {"task_id": task_id, "variant": "renamed" if renamed else "canonical", "success": False, "error_stage": "tool_selection", "tool_call_count": len(tool_calls), "raw": raw}
    function = tool_calls[0].get("function", {})
    name = function.get("name", "")
    arguments = function.get("arguments", {})
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError:
            arguments = {}
    canonical_name, canonical_args = canonicalize(name, arguments, renamed)
    name_ok = canonical_name == expected_name
    args_ok = set(canonical_args) == set(expected_args) and all(equal_value(canonical_args.get(key), value) for key, value in expected_args.items())
    return {
        "task_id": task_id,
        "variant": "renamed" if renamed else "canonical",
        "success": name_ok and args_ok,
        "error_stage": None if name_ok and args_ok else ("tool_selection" if not name_ok else "argument_mapping"),
        "exposed_call": {"name": name, "arguments": arguments},
        "canonical_call": {"name": canonical_name, "arguments": canonical_args},
        "expected_call": {"name": expected_name, "arguments": expected_args},
        "model": raw.get("model"),
        "created_at": raw.get("created_at"),
        "done_reason": raw.get("done_reason"),
    }


def main() -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for task in TASKS:
        for renamed in (False, True):
            record = run_call(task, renamed)
            records.append(record)
            print(json.dumps({key: record.get(key) for key in ("task_id", "variant", "success", "error_stage")}, ensure_ascii=False), flush=True)
    raw_path = OUTPUT_ROOT / "raw.jsonl"
    with raw_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    by_task: dict[str, dict[str, dict[str, Any]]] = {}
    for record in records:
        by_task.setdefault(record["task_id"], {})[record["variant"]] = record
    disagreements = [task_id for task_id, variants in by_task.items() if variants["canonical"]["success"] != variants["renamed"]["success"]]
    metrics = {
        "artifact_kind": "run14_screening_metrics",
        "evidence_fidelity": "SCREENING",
        "model": MODEL,
        "seed": SEED,
        "task_count": len(TASKS),
        "call_count": len(records),
        "canonical_successes": sum(record["success"] for record in records if record["variant"] == "canonical"),
        "renamed_successes": sum(record["success"] for record in records if record["variant"] == "renamed"),
        "paired_disagreement_count": len(disagreements),
        "paired_disagreement_task_ids": disagreements,
        "error_stage_counts": {
            stage: sum(record.get("error_stage") == stage for record in records)
            for stage in ("transport_or_parse", "tool_selection", "argument_mapping")
        },
        "scientific_boundary": "Local qwen3:4b screening only; not representative and not sufficient to kill a method core or paper direction.",
    }
    (OUTPUT_ROOT / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
