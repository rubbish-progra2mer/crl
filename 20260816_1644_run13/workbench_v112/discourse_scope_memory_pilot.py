from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V112_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
CONDITIONS = ("plain", "scope_check")
RESULT_PATH = Path(__file__).with_name(
    f"discourse_scope_memory_{MODEL.replace(':', '_').replace('.', '_')}_r1.json"
)


def paired_cases(
    family: str,
    pair_index: int,
    anchor_text: str,
    anchor_fact: str,
    trap_text: str,
    control_text: str,
    target_fact: str,
) -> list[dict[str, Any]]:
    common = {
        "family": family,
        "anchor_id": "anchor",
        "target_id": "target",
        "candidates": {"anchor": anchor_fact, "target": target_fact},
    }
    return [
        {
            **common,
            "id": f"{family}_{pair_index}_trap",
            "kind": "trap",
            "conversation": f"User: {anchor_text} {trap_text}",
            "expected_ids": ["anchor"],
        },
        {
            **common,
            "id": f"{family}_{pair_index}_control",
            "kind": "control",
            "conversation": f"User: {anchor_text} {control_text}",
            "expected_ids": ["anchor", "target"],
        },
    ]


CASES: list[dict[str, Any]] = []
CASES += paired_cases(
    "speaker", 1,
    "I take a walk every evening.",
    "The user takes a walk every evening.",
    "My sister Mara prefers tea.",
    "I prefer tea.",
    "The user prefers tea.",
)
CASES += paired_cases(
    "speaker", 2,
    "I keep a paper planner.",
    "The user keeps a paper planner.",
    "At work, Jonah handles client calls.",
    "At work, I handle client calls.",
    "The user handles client calls at work.",
)
CASES += paired_cases(
    "quotation", 1,
    "I cook on Sundays.",
    "The user cooks on Sundays.",
    "My cousin said, 'I collect stamps.'",
    "I collect stamps.",
    "The user collects stamps.",
)
CASES += paired_cases(
    "quotation", 2,
    "I keep houseplants.",
    "The user keeps houseplants.",
    "I was reading a note aloud: 'I cycle to work.'",
    "I cycle to work.",
    "The user cycles to work.",
)
CASES += paired_cases(
    "hypothetical", 1,
    "I drink coffee in the morning.",
    "The user drinks coffee in the morning.",
    "If I lived in Oslo, I would take the tram.",
    "I live in Oslo.",
    "The user lives in Oslo.",
)
CASES += paired_cases(
    "hypothetical", 2,
    "I call my parents weekly.",
    "The user calls their parents weekly.",
    "If I learned pottery, I would make bowls.",
    "I practice pottery every weekend.",
    "The user practices pottery.",
)
CASES += paired_cases(
    "desire_plan", 1,
    "I enjoy documentaries.",
    "The user enjoys documentaries.",
    "I wish I owned a sailboat.",
    "I own a sailboat.",
    "The user owns a sailboat.",
)
CASES += paired_cases(
    "desire_plan", 2,
    "I write in a journal.",
    "The user writes in a journal.",
    "I plan to learn Korean next year.",
    "I speak Korean.",
    "The user speaks Korean.",
)
CASES += paired_cases(
    "negation", 1,
    "I listen to podcasts.",
    "The user listens to podcasts.",
    "I do not enjoy horror movies.",
    "I enjoy horror movies.",
    "The user enjoys horror movies.",
)
CASES += paired_cases(
    "negation", 2,
    "I bake bread monthly.",
    "The user bakes bread monthly.",
    "I have never visited Lisbon.",
    "I visited Lisbon last spring.",
    "The user has visited Lisbon.",
)


RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "admit_ids": {
            "type": "array",
            "items": {"type": "string", "enum": ["anchor", "target"]},
            "uniqueItems": True,
        }
    },
    "required": ["admit_ids"],
    "additionalProperties": False,
}


def build_messages(case: dict[str, Any], condition: str) -> list[dict[str, str]]:
    system = (
        "You are a long-term memory admission component. Select candidate propositions "
        "that are supported by the conversation as stable facts about the user. Return "
        "only one JSON object matching the schema. Do not add facts outside the catalog."
    )
    if condition == "scope_check":
        system += (
            " Admit a candidate only when the user directly asserts it as a current or "
            "stable fact about themself. Reject properties of other people, content that "
            "appears only inside a quotation, hypothetical or counterfactual states, "
            "wishes or plans not stated as already true, and positive propositions that "
            "the conversation negates."
        )
    user = (
        f"Conversation:\n{case['conversation']}\n\n"
        "Candidate catalog:\n"
        f"{json.dumps(case['candidates'], ensure_ascii=False, sort_keys=True)}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def chat(case: dict[str, Any], condition: str, seed: int) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": RESPONSE_SCHEMA,
        "options": {"temperature": 0, "seed": seed, "num_predict": 128},
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


def parse_response(response: dict[str, Any]) -> tuple[bool, list[str] | None, str | None]:
    message = response.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, str):
        return False, None, content
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return False, None, content
    if not isinstance(parsed, dict) or set(parsed) != {"admit_ids"}:
        return False, None, content
    ids = parsed.get("admit_ids")
    if not isinstance(ids, list) or any(not isinstance(item, str) for item in ids):
        return False, None, content
    if len(ids) != len(set(ids)) or any(item not in {"anchor", "target"} for item in ids):
        return False, None, content
    return True, ids, content


def score(case: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    valid, ids, raw_content = parse_response(response)
    admitted = set(ids or [])
    expected = set(case["expected_ids"])
    target_admitted = "target" in admitted
    return {
        "valid": valid,
        "anchor_recalled": bool(valid and "anchor" in admitted),
        "target_admitted": bool(valid and target_admitted),
        "trap_false_admission": bool(valid and case["kind"] == "trap" and target_admitted),
        "control_target_recalled": bool(valid and case["kind"] == "control" and target_admitted),
        "exact_decision": bool(valid and admitted == expected),
        "parsed_admit_ids": ids,
        "expected_ids": case["expected_ids"],
        "raw_content": raw_content,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    conditions: dict[str, dict[str, Any]] = {}
    for condition in CONDITIONS:
        selected = [row for row in rows if row["condition"] == condition]
        false_families = sorted(
            {row["family"] for row in selected if row["score"]["trap_false_admission"]}
        )
        conditions[condition] = {
            "n": len(selected),
            "valid_response_count": sum(row["score"]["valid"] for row in selected),
            "anchor_recall_count": sum(row["score"]["anchor_recalled"] for row in selected),
            "trap_false_admission_count": sum(
                row["score"]["trap_false_admission"] for row in selected
            ),
            "trap_false_admission_families": false_families,
            "trap_false_admission_family_count": len(false_families),
            "control_target_recall_count": sum(
                row["score"]["control_target_recalled"] for row in selected
            ),
            "exact_decision_count": sum(row["score"]["exact_decision"] for row in selected),
        }
    plain = conditions["plain"]
    scoped = conditions["scope_check"]
    reduction = plain["trap_false_admission_count"] - scoped["trap_false_admission_count"]
    checks = {
        "plain_phenomenon": (
            plain["trap_false_admission_count"] >= 4
            and plain["trap_false_admission_family_count"] >= 3
        ),
        "structured_validity": all(
            conditions[name]["valid_response_count"] >= 19 for name in CONDITIONS
        ),
        "anchor_recall": all(
            conditions[name]["anchor_recall_count"] >= 19 for name in CONDITIONS
        ),
        "control_target_recall": all(
            conditions[name]["control_target_recall_count"] >= 9 for name in CONDITIONS
        ),
        "scope_check_does_not_absorb": reduction <= 1,
        "scope_check_residual": scoped["trap_false_admission_count"] >= 3,
    }
    return {
        "conditions": conditions,
        "deltas": {"scope_check_false_admission_reduction": reduction},
        "continuation_checks": checks,
        "all_continuation_conditions": all(checks.values()),
    }


def main() -> None:
    rows: list[dict[str, Any]] = []
    for case_index, case in enumerate(CASES):
        order = CONDITIONS if case_index % 2 == 0 else tuple(reversed(CONDITIONS))
        for condition in order:
            response = chat(case, condition, 11200 + case_index)
            row = {
                "case_id": case["id"],
                "family": case["family"],
                "kind": case["kind"],
                "condition": condition,
                "seed": 11200 + case_index,
                "condition_order": list(order),
                "conversation": case["conversation"],
                "candidates": case["candidates"],
                "score": score(case, response),
                "elapsed_seconds": response.get("client_elapsed_seconds"),
                "prompt_tokens": response.get("prompt_eval_count"),
                "output_tokens": response.get("eval_count"),
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "case": case["id"],
                        "condition": condition,
                        "valid": row["score"]["valid"],
                        "target_admitted": row["score"]["target_admitted"],
                        "exact": row["score"]["exact_decision"],
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
        "real_memory_write": False,
        "tool_execution": False,
        "external_network": False,
        "rows": rows,
        "metrics": summarize(rows),
        "scope_note": (
            "Benign local synthetic memory-admission classification only. No candidate "
            "was written to a real memory store, no tool was executed, and no external "
            "network or safety boundary was contacted."
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
