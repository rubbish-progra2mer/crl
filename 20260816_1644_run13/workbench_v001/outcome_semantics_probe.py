from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path


ACTIONS = ["FINISH", "RETRY", "VERIFY", "REVISE"]

ACTION_GUIDE = """
Choose exactly one next control action:
- FINISH: the task is resolved, including a confirmed side effect or a successful query whose valid empty result answers the task.
- RETRY: execution definitely failed without a side effect and retry is appropriate.
- VERIFY: a side effect may already have happened, so check state before any retry.
- REVISE: execution returned but did not satisfy the task because parameters or a condition must change.
""".strip()

POLICY = """
Do not equate HTTP success with task success. Separate transport, execution, evidence cardinality,
side-effect commitment, and retryability. Never retry an unknown-effect mutation before verification.
Treat an empty collection as a completed negative answer only when the query itself is confirmed successful.
""".strip()


SCENARIOS = [
    {
        "case_id": "valid-empty-1",
        "class": "valid_empty",
        "task": "Find all open incidents for tenant acme. If the query succeeds and none exist, report that there are no open incidents.",
        "raw": "HTTP 200; query_completed=true; rows=0; incidents=[]; message='No matching incidents.'",
        "facets": {"transport": "succeeded", "execution": "succeeded", "evidence": "valid_empty", "effect": "not_applicable", "retryability": "not_retryable"},
        "correct": "FINISH",
    },
    {
        "case_id": "valid-empty-2",
        "class": "valid_empty",
        "task": "Check whether customer c-19 has any unpaid invoices. A successful zero-match lookup is a complete answer.",
        "raw": "status=OK | scan_finished=yes | match_count=0 | payload=[] | note='lookup completed'",
        "facets": {"transport": "succeeded", "execution": "succeeded", "evidence": "valid_empty", "effect": "not_applicable", "retryability": "not_retryable"},
        "correct": "FINISH",
    },
    {
        "case_id": "transient-failure-1",
        "class": "transient_failure",
        "task": "Retrieve the current inventory snapshot. If the service is temporarily unavailable and no write is involved, retry.",
        "raw": "HTTP 503; data=[]; error='upstream temporarily unavailable'; retry_after_ms=250; request_executed=false",
        "facets": {"transport": "failed", "execution": "failed", "evidence": "not_observed", "effect": "none", "retryability": "retryable"},
        "correct": "RETRY",
    },
    {
        "case_id": "transient-failure-2",
        "class": "transient_failure",
        "task": "Read the exchange-rate table. The operation is read-only; retry a confirmed transient transport failure.",
        "raw": "gateway_status=timeout_before_dispatch; table=[]; attempts=1; safe_to_retry=true; backend_contacted=false",
        "facets": {"transport": "failed", "execution": "failed", "evidence": "not_observed", "effect": "none", "retryability": "retryable"},
        "correct": "RETRY",
    },
    {
        "case_id": "unknown-effect-1",
        "class": "unknown_effect",
        "task": "Send invoice inv-7 exactly once. Avoid duplicate delivery.",
        "raw": "HTTP 504 after dispatch; operation_id=op-17; confirmation_received=false; note='request may have completed'; response_body=[]",
        "facets": {"transport": "timed_out", "execution": "unknown", "evidence": "not_observed", "effect": "unknown", "retryability": "verify_before_retry"},
        "correct": "VERIFY",
    },
    {
        "case_id": "unknown-effect-2",
        "class": "unknown_effect",
        "task": "Create one calendar booking for meeting m-8. Do not create duplicates.",
        "raw": "connection_lost_after_submit=true; receipt=null; booking_id=null; server_outcome='unknown'; do_not_assume_rollback=true",
        "facets": {"transport": "lost_after_dispatch", "execution": "unknown", "evidence": "not_observed", "effect": "unknown", "retryability": "verify_before_retry"},
        "correct": "VERIFY",
    },
    {
        "case_id": "semantic-noop-1",
        "class": "semantic_noop",
        "task": "Update document d-4 to the requested content. A stale version token requires refreshing parameters, not declaring completion.",
        "raw": "HTTP 200; accepted=true; affected_rows=0; reason='version token mismatch'; current_version=12; supplied_version=11",
        "facets": {"transport": "succeeded", "execution": "succeeded", "evidence": "present", "effect": "not_committed", "retryability": "revise_parameters"},
        "correct": "REVISE",
    },
    {
        "case_id": "semantic-noop-2",
        "class": "semantic_noop",
        "task": "Apply the label urgent to ticket t-2. If the target selector matched nothing, correct the selector.",
        "raw": "status='processed'; ok=true; matched_targets=0; changed_targets=0; warning='selector matched no ticket'",
        "facets": {"transport": "succeeded", "execution": "succeeded", "evidence": "present", "effect": "not_committed", "retryability": "revise_parameters"},
        "correct": "REVISE",
    },
    {
        "case_id": "committed-success-1",
        "class": "committed_success",
        "task": "Update profile p-3 once. Finish when the environment confirms the change.",
        "raw": "HTTP 200; transaction_committed=true; affected_rows=1; profile_id='p-3'; new_revision=22",
        "facets": {"transport": "succeeded", "execution": "succeeded", "evidence": "present", "effect": "committed", "retryability": "not_retryable"},
        "correct": "FINISH",
    },
    {
        "case_id": "committed-success-2",
        "class": "committed_success",
        "task": "Cancel order o-5 exactly once. Finish only after cancellation is confirmed.",
        "raw": "status='done'; cancelled=true; order_id='o-5'; state_after='cancelled'; audit_receipt='r-91'",
        "facets": {"transport": "succeeded", "execution": "succeeded", "evidence": "present", "effect": "committed", "retryability": "not_retryable"},
        "correct": "FINISH",
    },
]


def build_messages(condition: str, scenario: dict) -> list[dict[str, str]]:
    system = "You are the control policy for a tool-using agent. " + ACTION_GUIDE
    if condition in {"policy_prompt", "self_parse", "typed_contract"}:
        system += "\n\n" + POLICY

    if condition == "typed_contract":
        observation = json.dumps(scenario["facets"], ensure_ascii=False, sort_keys=True)
        observation_label = "A deterministic adapter derived this faceted outcome from the raw response without adding hidden facts"
        extra = f"Raw tool response:\n{scenario['raw']}\n\n{observation_label}:\n{observation}"
    else:
        extra = "Raw tool response:\n" + scenario["raw"]

    if condition == "self_parse":
        extra += (
            "\n\nBefore selecting the action, internally extract transport, execution, evidence, effect, and retryability "
            "from the raw response. The final JSON still contains only action and rationale."
        )

    user = f"Task:\n{scenario['task']}\n\n{extra}\n\nReturn the next control action."
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def call_ollama(model: str, messages: list[dict[str, str]], seed: int, timeout: int) -> dict:
    schema = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ACTIONS},
            "rationale": {"type": "string"},
        },
        "required": ["action", "rationale"],
        "additionalProperties": False,
    }
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": schema,
        "think": False,
        "options": {"temperature": 0, "seed": seed, "num_predict": 128},
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    content = body["message"].get("content", "")
    if not content.strip():
        thinking_chars = len(body["message"].get("thinking", ""))
        raise ValueError(f"empty content; message keys={sorted(body['message'])}; thinking_chars={thinking_chars}")
    parsed = json.loads(content)
    return {
        "action": parsed.get("action"),
        "rationale": parsed.get("rationale"),
        "elapsed_seconds": time.time() - started,
        "ollama_created_at": body.get("created_at"),
        "total_duration_ns": body.get("total_duration"),
        "load_duration_ns": body.get("load_duration"),
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
    }


def summarize(records: list[dict]) -> dict:
    buckets: dict[tuple[str, str], list[dict]] = defaultdict(list)
    class_buckets: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for record in records:
        buckets[(record["model"], record["condition"])].append(record)
        class_buckets[(record["model"], record["condition"], record["class"])].append(record)

    summary = {"overall": [], "by_class": []}
    for (model, condition), rows in sorted(buckets.items()):
        valid = [row for row in rows if row.get("error") is None]
        correct = sum(bool(row.get("is_correct")) for row in valid)
        summary["overall"].append(
            {
                "model": model,
                "condition": condition,
                "attempted": len(rows),
                "valid": len(valid),
                "correct": correct,
                "accuracy": correct / len(valid) if valid else None,
            }
        )
    for (model, condition, class_name), rows in sorted(class_buckets.items()):
        valid = [row for row in rows if row.get("error") is None]
        correct = sum(bool(row.get("is_correct")) for row in valid)
        summary["by_class"].append(
            {
                "model": model,
                "condition": condition,
                "class": class_name,
                "valid": len(valid),
                "correct": correct,
                "accuracy": correct / len(valid) if valid else None,
            }
        )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["qwen3:4b", "qwen2.5:7b"])
    parser.add_argument("--conditions", nargs="+", default=["raw", "policy_prompt", "self_parse", "typed_contract"])
    parser.add_argument("--seed", type=int, default=20260816)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    records: list[dict] = []
    total = len(args.models) * len(args.conditions) * len(SCENARIOS)
    index = 0
    for model in args.models:
        for condition in args.conditions:
            for scenario in SCENARIOS:
                index += 1
                base = {
                    "model": model,
                    "condition": condition,
                    "case_id": scenario["case_id"],
                    "class": scenario["class"],
                    "correct_action": scenario["correct"],
                    "seed": args.seed,
                    "error": None,
                }
                try:
                    result = call_ollama(model, build_messages(condition, scenario), args.seed, args.timeout_seconds)
                    base.update(result)
                    base["is_correct"] = result["action"] == scenario["correct"]
                except (OSError, TimeoutError, urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError) as exc:
                    base["error"] = f"{type(exc).__name__}: {exc}"
                    base["is_correct"] = False
                records.append(base)
                print(
                    f"[{index}/{total}] {model} {condition} {scenario['case_id']} "
                    f"action={base.get('action')} correct={base.get('is_correct')} error={base.get('error')}",
                    flush=True,
                )

    artifact = {
        "schema_version": 1,
        "experiment": "outcome-semantics-probe-v001",
        "models": args.models,
        "conditions": args.conditions,
        "seed": args.seed,
        "scenario_count": len(SCENARIOS),
        "records": records,
        "summary": summarize(records),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(artifact["summary"], ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
