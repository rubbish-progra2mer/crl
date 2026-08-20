from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V071_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
RESULT_PATH = Path(__file__).with_name(
    f"executor_compensation_{MODEL.replace(':', '_').replace('.', '_')}_r1.json"
)

DOMAINS = (
    "invoice",
    "shipment",
    "ticket",
    "catalog",
    "booking",
    "archive",
    "workspace",
    "inventory",
    "report",
    "subscription",
    "dataset",
    "calendar",
    "profile",
    "order",
    "project",
    "document",
    "queue",
    "registry",
    "collection",
    "dashboard",
)


def build_case(index: int) -> dict[str, Any]:
    domain = DOMAINS[index]
    family_index = index % 5
    suffix = f"{index + 31:04d}"
    tool = f"update_{domain}_record"
    if family_index == 0:
        family = "key_alias"
        expected = {"resource_id": f"{domain[:3].upper()}-{suffix}", "destination_id": f"DST-{index + 7:03d}"}
        schema = {
            "resource_id": "required string; exact canonical resource code",
            "destination_id": "required string; exact canonical destination code",
        }
        request = (
            f"Move {domain} {expected['resource_id']} to destination {expected['destination_id']}. "
            "Use the canonical codes exactly."
        )
    elif family_index == 1:
        family = "enum_normalization"
        levels = ("P1_URGENT", "P2_HIGH", "P3_NORMAL", "P4_LOW")
        expected = {"resource_id": f"{domain[:3].upper()}-{suffix}", "priority": levels[(index // 5) % 4]}
        schema = {
            "resource_id": "required string; exact canonical resource code",
            "priority": "required enum: P1_URGENT | P2_HIGH | P3_NORMAL | P4_LOW",
        }
        request = (
            f"Set {domain} {expected['resource_id']} to priority {expected['priority']}. "
            "Use the exact enum token."
        )
    elif family_index == 2:
        family = "resource_code_normalization"
        prefix = domain[:2].upper()
        expected = {"resource_id": f"{prefix}-{suffix}", "active": True}
        schema = {
            "resource_id": f"required string matching {prefix}-NNNN",
            "active": "required JSON boolean",
        }
        request = (
            f"Activate {domain} whose canonical code is {expected['resource_id']}. "
            "Preserve capitalization, hyphen, and zero padding."
        )
    elif family_index == 3:
        family = "identifier_type_recovery"
        expected = {"resource_id": f"00{index + 41:04d}", "quantity": index % 3 + 1}
        schema = {
            "resource_id": "required six-character decimal string; leading zeros are significant",
            "quantity": "required JSON integer",
        }
        request = (
            f"Reserve quantity {expected['quantity']} of {domain} identifier {expected['resource_id']}. "
            "The identifier must remain a six-character string."
        )
    else:
        family = "missing_standard_policy"
        expected = {"resource_id": f"{domain[:3].upper()}-{suffix}", "review_policy": "STANDARD_REVIEW"}
        schema = {
            "resource_id": "required string; exact canonical resource code",
            "review_policy": "required enum: STANDARD_REVIEW | EXPEDITED_REVIEW | MANUAL_REVIEW",
        }
        request = (
            f"Submit {domain} {expected['resource_id']} under the STANDARD_REVIEW policy. "
            "Both fields are required."
        )
    return {
        "case_id": f"{index + 1:02d}_{domain}",
        "family": family,
        "tool": tool,
        "schema": schema,
        "request": request,
        "expected": expected,
    }


def call_model(case: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": {
            "type": "object",
            "properties": {
                "tool": {"type": "string", "enum": [case["tool"]]},
                "arguments": {"type": "object"},
            },
            "required": ["tool", "arguments"],
            "additionalProperties": False,
        },
        "options": {"temperature": 0, "seed": 71, "num_predict": 180},
        "messages": [
            {
                "role": "system",
                "content": (
                    "Generate exactly one API action for the request. Follow the supplied contract literally. "
                    "Return only the required JSON object with tool and arguments."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "request": case["request"],
                        "tool": case["tool"],
                        "argument_contract": case["schema"],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
            },
        ],
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = json.loads(response.read().decode("utf-8"))
    elapsed = time.perf_counter() - started
    content = raw.get("message", {}).get("content", "")
    parsed: dict[str, Any] | None = None
    try:
        candidate = json.loads(content)
        if isinstance(candidate, dict):
            parsed = candidate
    except json.JSONDecodeError:
        parsed = None
    return {
        "parsed": parsed,
        "raw_content": content,
        "prompt_tokens": int(raw.get("prompt_eval_count", 0)),
        "output_tokens": int(raw.get("eval_count", 0)),
        "elapsed_seconds": elapsed,
    }


def strict_success(case: dict[str, Any], action: dict[str, Any] | None) -> bool:
    return bool(
        action
        and action.get("tool") == case["tool"]
        and isinstance(action.get("arguments"), dict)
        and action["arguments"] == case["expected"]
    )


def normalize_enum(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").upper()


def forgiving_interpret(case: dict[str, Any], action: dict[str, Any] | None) -> tuple[dict[str, Any] | None, list[str]]:
    if not action or action.get("tool") != case["tool"] or not isinstance(action.get("arguments"), dict):
        return action, []
    repaired = {"tool": action["tool"], "arguments": dict(action["arguments"])}
    args = repaired["arguments"]
    repairs: list[str] = []
    family = case["family"]
    expected = case["expected"]

    if family == "key_alias":
        aliases = {
            "resource_id": ("resource", "record_id", "item_id", "id"),
            "destination_id": ("destination", "target_id", "dest_id"),
        }
        for canonical, candidates in aliases.items():
            if canonical not in args:
                present = [name for name in candidates if name in args]
                if len(present) == 1:
                    args[canonical] = args.pop(present[0])
                    repairs.append(f"alias:{present[0]}->{canonical}")
    elif family == "enum_normalization" and "priority" in args:
        normalized = normalize_enum(args["priority"])
        if normalized == expected["priority"] and args["priority"] != normalized:
            args["priority"] = normalized
            repairs.append("enum_normalization")
    elif family == "resource_code_normalization" and "resource_id" in args:
        value = args["resource_id"]
        if isinstance(value, str):
            compact = re.sub(r"[^A-Za-z0-9]", "", value).upper()
            expected_compact = re.sub(r"[^A-Za-z0-9]", "", expected["resource_id"]).upper()
            if compact == expected_compact and value != expected["resource_id"]:
                args["resource_id"] = expected["resource_id"]
                repairs.append("resource_code_normalization")
    elif family == "identifier_type_recovery" and "resource_id" in args:
        value = args["resource_id"]
        if isinstance(value, int) and str(value) == str(int(expected["resource_id"])):
            args["resource_id"] = expected["resource_id"]
            repairs.append("identifier_type_recovery")
    elif family == "missing_standard_policy":
        if "review_policy" not in args:
            args["review_policy"] = expected["review_policy"]
            repairs.append("missing_standard_policy")

    return repaired, repairs


def main() -> None:
    rows: list[dict[str, Any]] = []
    for index in range(len(DOMAINS)):
        case = build_case(index)
        generated = call_model(case)
        action = generated["parsed"]
        forgiving_action, repairs = forgiving_interpret(case, action)
        strict = strict_success(case, action)
        forgiving = strict_success(case, forgiving_action)
        row = {
            "case_id": case["case_id"],
            "family": case["family"],
            "tool": case["tool"],
            "request": case["request"],
            "schema": case["schema"],
            "expected": case["expected"],
            "action": action,
            "raw_content": generated["raw_content"],
            "valid_json": action is not None,
            "strict_success": strict,
            "forgiving_action": forgiving_action,
            "forgiving_success": forgiving,
            "compensated": forgiving and not strict,
            "repairs": repairs,
            "prompt_tokens": generated["prompt_tokens"],
            "output_tokens": generated["output_tokens"],
            "elapsed_seconds": generated["elapsed_seconds"],
        }
        rows.append(row)
        print(
            json.dumps(
                {
                    "case_id": row["case_id"],
                    "family": row["family"],
                    "strict": strict,
                    "forgiving": forgiving,
                    "repairs": repairs,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )

    compensated_families = sorted({row["family"] for row in rows if row["compensated"]})
    by_family: dict[str, dict[str, int]] = {}
    for family in sorted({row["family"] for row in rows}):
        group = [row for row in rows if row["family"] == family]
        by_family[family] = {
            "n": len(group),
            "strict_success": sum(row["strict_success"] for row in group),
            "forgiving_success": sum(row["forgiving_success"] for row in group),
            "compensated": sum(row["compensated"] for row in group),
        }
    summary = {
        "n": len(rows),
        "valid_json": sum(row["valid_json"] for row in rows),
        "strict_success": sum(row["strict_success"] for row in rows),
        "forgiving_success": sum(row["forgiving_success"] for row in rows),
        "compensation_gap": sum(row["forgiving_success"] for row in rows)
        - sum(row["strict_success"] for row in rows),
        "compensated_family_count": len(compensated_families),
        "compensated_families": compensated_families,
        "by_family": by_family,
        "prompt_tokens": sum(row["prompt_tokens"] for row in rows),
        "output_tokens": sum(row["output_tokens"] for row in rows),
        "elapsed_seconds": sum(row["elapsed_seconds"] for row in rows),
    }
    result = {
        "model": MODEL,
        "endpoint": ENDPOINT,
        "temperature": 0,
        "seed": 71,
        "summary": summary,
        "rows": rows,
        "scope_note": "Benign synthetic action generation and offline validation only; no represented tool was executed.",
    }
    RESULT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
