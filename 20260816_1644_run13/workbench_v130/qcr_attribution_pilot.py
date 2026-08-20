from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V130_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
OPS = ("op_amber", "op_blue", "op_coral", "op_dusk")
CONDITIONS = ("direct", "target_plan", "qcr_correct", "qcr_shuffled")
SEQUENCES = (
    ("op_amber", "op_blue", "op_coral", "op_dusk"),
    ("op_blue", "op_dusk", "op_amber", "op_coral"),
    ("op_coral", "op_amber", "op_dusk", "op_blue"),
    ("op_dusk", "op_coral", "op_blue", "op_amber"),
)
RESULT_PATH = Path(__file__).with_name(
    f"qcr_attribution_{MODEL.replace(':', '_').replace('.', '_')}_r1.json"
)


SUPPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "workflow_invariant": {
            "type": "array",
            "items": {"type": "string", "enum": list(OPS)},
            "maxItems": 4,
        },
        "bindings_to_reobtain": {"type": "array", "items": {"type": "string"}},
        "applicability_conditions": {"type": "string"},
        "verification_guardrail": {"type": "string"},
    },
    "required": [
        "workflow_invariant",
        "bindings_to_reobtain",
        "applicability_conditions",
        "verification_guardrail",
    ],
    "additionalProperties": False,
}


def actor_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "actions": {
                "type": "array",
                "minItems": 4,
                "maxItems": 4,
                "items": {
                    "type": "object",
                    "properties": {
                        "tool": {"type": "string", "enum": list(OPS)},
                        "record_id": {"type": "string"},
                    },
                    "required": ["tool", "record_id"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["actions"],
        "additionalProperties": False,
    }


def make_source(sequence: tuple[str, ...], source_id: str) -> str:
    rejected = next(op for op in OPS if op != sequence[0])
    lines = [
        f"Historical instruction: complete one workflow cycle for record {source_id}.",
        f"Initial observation: available operations are {', '.join(OPS)}.",
        f"Attempt {rejected}({source_id}) -> REJECTED: wrong phase; state unchanged.",
    ]
    for index, op in enumerate(sequence, start=1):
        status = "COMPLETED" if index == 4 else f"PHASE_{index}_OK"
        lines.append(f"Action {op}({source_id}) -> {status}.")
    lines.append("Verifier: SUCCESS. The four accepted actions above completed the workflow.")
    return "\n".join(lines)


def build_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for repetition in range(2):
        for seq_index, sequence in enumerate(SEQUENCES):
            for kind in ("transfer_needed", "target_sufficient"):
                case_index = len(cases)
                kind_code = "N" if kind == "transfer_needed" else "S"
                target_id = f"TGT-{kind_code}{seq_index}-{repetition}"
                source_id = f"SRC-C{seq_index}-{repetition}"
                shuffled_index = (seq_index + 1 + repetition) % len(SEQUENCES)
                shuffled_id = f"SRC-S{shuffled_index}-{repetition}"
                target_observation = (
                    f"Current record: {target_id}. Available operations: {', '.join(OPS)}. "
                    "A valid workflow uses every operation exactly once. Every call must use "
                    "the current record identifier."
                )
                if kind == "transfer_needed":
                    target_observation += " The current service does not display the required order."
                else:
                    target_observation += (
                        " The current target-side runbook explicitly gives this required order: "
                        + " -> ".join(sequence)
                        + "."
                    )
                cases.append(
                    {
                        "id": f"case_{case_index:02d}_{kind}_p{seq_index}_r{repetition}",
                        "kind": kind,
                        "target_id": target_id,
                        "source_id": source_id,
                        "shuffled_source_id": shuffled_id,
                        "target_query": f"Complete the workflow cycle for current record {target_id}.",
                        "target_observation": target_observation,
                        "expected_sequence": list(sequence),
                        "correct_source": make_source(sequence, source_id),
                        "shuffled_source": make_source(SEQUENCES[shuffled_index], shuffled_id),
                    }
                )
    return cases


CASES = build_cases()


def chat(
    messages: list[dict[str, str]], schema: dict[str, Any], seed: int, num_predict: int
) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": schema,
        "options": {
            "temperature": 0,
            "seed": seed,
            "num_predict": num_predict,
            "num_ctx": 8192,
        },
        "messages": messages,
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


def response_content(response: dict[str, Any]) -> str:
    message = response.get("message")
    content = message.get("content") if isinstance(message, dict) else ""
    return content if isinstance(content, str) else ""


def support_messages(case: dict[str, Any], condition: str) -> list[dict[str, str]]:
    if condition == "target_plan":
        system = (
            "You are a target-conditioned workflow support writer. You have no historical "
            "trajectory. Produce a short four-field preplanning note from the current query and "
            "initial observation only. Do not invent an order that current evidence does not reveal."
        )
        user = (
            f"Target query:\n{case['target_query']}\n\n"
            f"Initial target observation:\n{case['target_observation']}"
        )
    else:
        source_key = "correct_source" if condition == "qcr_correct" else "shuffled_source"
        system = (
            "You are a query-conditioned trajectory reuse support writer. Produce a short note "
            "with the four required fields. Keep the verified accepted workflow, ignore rejected "
            "attempts whose state did not change, never copy the historical record identifier into "
            "the target, and let explicit current target evidence override history. If applicability "
            "cannot be established, state that limitation."
        )
        user = (
            f"Historical trajectory:\n{case[source_key]}\n\n"
            f"Target query:\n{case['target_query']}\n\n"
            f"Initial target observation:\n{case['target_observation']}"
        )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def actor_messages(case: dict[str, Any], support: str | None) -> list[dict[str, str]]:
    system = (
        "You are a deterministic workflow actor. Return exactly four tool calls as JSON. Use each "
        "available operation exactly once. Every call must use the current target record identifier. "
        "The current target observation is authoritative. A support note is advisory; when it "
        "conflicts with an explicit current runbook, follow the current runbook. Do not include a "
        "rejected historical attempt."
    )
    support_text = support if support is not None else "No separate support note is available."
    user = (
        f"Target query:\n{case['target_query']}\n\n"
        f"Initial target observation:\n{case['target_observation']}\n\n"
        f"Advisory support:\n{support_text}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def parse_actions(content: str) -> tuple[bool, list[dict[str, str]] | None]:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return False, None
    if not isinstance(parsed, dict) or set(parsed) != {"actions"}:
        return False, None
    actions = parsed.get("actions")
    if not isinstance(actions, list) or len(actions) != 4:
        return False, None
    normalized: list[dict[str, str]] = []
    for action in actions:
        if not isinstance(action, dict) or set(action) != {"tool", "record_id"}:
            return False, None
        tool = action.get("tool")
        record_id = action.get("record_id")
        if tool not in OPS or not isinstance(record_id, str):
            return False, None
        normalized.append({"tool": tool, "record_id": record_id})
    return True, normalized


def score(case: dict[str, Any], content: str) -> dict[str, Any]:
    valid, actions = parse_actions(content)
    tools = [a["tool"] for a in actions or []]
    bindings = [a["record_id"] for a in actions or []]
    correct_order = bool(valid and tools == case["expected_sequence"])
    correct_binding = bool(valid and all(v == case["target_id"] for v in bindings))
    stale_ids = {case["source_id"], case["shuffled_source_id"]}
    return {
        "valid": valid,
        "correct_order": correct_order,
        "correct_binding": correct_binding,
        "exact": bool(correct_order and correct_binding),
        "stale_source_binding": bool(valid and any(v in stale_ids for v in bindings)),
        "parsed_actions": actions,
        "raw_content": content,
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metrics: dict[str, Any] = {"overall": {}, "by_kind": {}}
    for condition in CONDITIONS:
        selected = [r for r in rows if r["condition"] == condition]
        metrics["overall"][condition] = summarize_rows(selected)
    for kind in ("transfer_needed", "target_sufficient"):
        metrics["by_kind"][kind] = {}
        for condition in CONDITIONS:
            selected = [
                r for r in rows if r["condition"] == condition and r["kind"] == kind
            ]
            metrics["by_kind"][kind][condition] = summarize_rows(selected)

    transfer = metrics["by_kind"]["transfer_needed"]
    sufficient = metrics["by_kind"]["target_sufficient"]
    checks = {
        "all_conditions_valid_at_least_15_of_16": all(
            metrics["overall"][c]["valid_count"] >= 15 for c in CONDITIONS
        ),
        "target_plan_sufficient_exact_at_least_7_of_8": (
            sufficient["target_plan"]["exact_count"] >= 7
        ),
        "qcr_correct_transfer_exact_at_least_7_of_8": (
            transfer["qcr_correct"]["exact_count"] >= 7
        ),
        "correct_minus_target_plan_transfer_at_least_4": (
            transfer["qcr_correct"]["exact_count"]
            - transfer["target_plan"]["exact_count"]
            >= 4
        ),
        "correct_minus_shuffled_transfer_at_least_4": (
            transfer["qcr_correct"]["exact_count"]
            - transfer["qcr_shuffled"]["exact_count"]
            >= 4
        ),
    }
    metrics["transfer_exact_deltas"] = {
        "qcr_correct_minus_target_plan": (
            transfer["qcr_correct"]["exact_count"]
            - transfer["target_plan"]["exact_count"]
        ),
        "qcr_correct_minus_qcr_shuffled": (
            transfer["qcr_correct"]["exact_count"]
            - transfer["qcr_shuffled"]["exact_count"]
        ),
    }
    metrics["continuation_checks"] = checks
    metrics["all_continuation_conditions"] = all(checks.values())
    return metrics


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "n": len(rows),
        "valid_count": sum(r["score"]["valid"] for r in rows),
        "exact_count": sum(r["score"]["exact"] for r in rows),
        "correct_order_count": sum(r["score"]["correct_order"] for r in rows),
        "correct_binding_count": sum(r["score"]["correct_binding"] for r in rows),
        "stale_source_binding_count": sum(
            r["score"]["stale_source_binding"] for r in rows
        ),
    }


def main() -> None:
    rows: list[dict[str, Any]] = []
    for case_index, case in enumerate(CASES):
        shift = case_index % len(CONDITIONS)
        order = CONDITIONS[shift:] + CONDITIONS[:shift]
        for condition in order:
            support_response: dict[str, Any] | None = None
            support_content: str | None = None
            if condition != "direct":
                support_response = chat(
                    support_messages(case, condition),
                    SUPPORT_SCHEMA,
                    130000 + case_index,
                    256,
                )
                support_content = response_content(support_response)
            actor_response = chat(
                actor_messages(case, support_content),
                actor_schema(),
                131000 + case_index,
                256,
            )
            actor_content = response_content(actor_response)
            row = {
                "case_id": case["id"],
                "kind": case["kind"],
                "condition": condition,
                "condition_order": list(order),
                "target_id": case["target_id"],
                "source_id": case["source_id"],
                "shuffled_source_id": case["shuffled_source_id"],
                "expected_sequence": case["expected_sequence"],
                "support_content": support_content,
                "support_prompt_tokens": (
                    support_response.get("prompt_eval_count") if support_response else 0
                ),
                "support_output_tokens": (
                    support_response.get("eval_count") if support_response else 0
                ),
                "support_elapsed_seconds": (
                    support_response.get("client_elapsed_seconds") if support_response else 0
                ),
                "actor_prompt_tokens": actor_response.get("prompt_eval_count"),
                "actor_output_tokens": actor_response.get("eval_count"),
                "actor_elapsed_seconds": actor_response.get("client_elapsed_seconds"),
                "score": score(case, actor_content),
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "case": case["id"],
                        "condition": condition,
                        "exact": row["score"]["exact"],
                        "order": row["score"]["correct_order"],
                        "binding": row["score"]["correct_binding"],
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
        "real_tool_execution": False,
        "external_network": False,
        "security_bypass_content": False,
        "rows": rows,
        "metrics": aggregate(rows),
        "scope_note": (
            "Benign local synthetic workflow planning only. No real tool or business-state "
            "mutation, no external network, and no security-control interaction."
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
