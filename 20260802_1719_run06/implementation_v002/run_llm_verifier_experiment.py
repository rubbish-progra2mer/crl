from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

from joint_coverage_kernel import Claim, Observation, evaluate_claim
from run_joint_coverage_experiment import (
    build_claims,
    build_worlds,
    claim_truth,
    collect_exact_scope_trace,
)


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


def observation_to_dict(observation: Observation) -> dict[str, Any]:
    return {
        "observation_id": observation.observation_id,
        "cell": observation.cell.key,
        "cursor": observation.cursor,
        "next_cursor": observation.next_cursor,
        "snapshot_id": observation.snapshot_id,
        "status": observation.status,
        "attested": observation.attested,
        "permission_complete": observation.permission_complete,
        "silently_truncated": observation.silently_truncated,
        "records": [
            {
                "record_id": record.record_id,
                "cell": record.cell.key,
                "matches_target": record.matches_target,
                "compliant": record.compliant,
            }
            for record in observation.records
        ],
    }


def call_verifier(
    model: str,
    claim: Claim,
    observations: list[Observation],
    seed: int,
) -> tuple[str, str, dict[str, Any]]:
    system = (
        "你是独立的工具证据审查器，只输出 JSON：{\"decision\":\"TRUE|FALSE|UNKNOWN\"}。"
        "每个 cell 是实体×时间×归档的不可分联合范围。完整页链必须从 cursor=0 开始，"
        "沿 next_cursor 到 null，所有页 snapshot_id 一致、status=ok、attested=true、"
        "permission_complete=true 且 silently_truncated=false。exists 为真可由范围内见证证明；"
        "exists 为假必须完整覆盖整个主张范围且没有见证；forall 为假可由不满足谓词的反例证明；"
        "forall 为真必须完整覆盖整个主张范围且没有反例。证据不足必须 UNKNOWN。"
    )
    payload = {
        "claim": {
            "claim_id": claim.claim_id,
            "quantifier": claim.quantifier,
            "predicate": claim.predicate,
            "scope": [cell.key for cell in claim.scope],
            "snapshot_id": claim.snapshot_id,
        },
        "observations": [observation_to_dict(item) for item in observations],
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        "stream": False,
        "format": "json",
        "think": False,
        "keep_alive": "30m",
        "options": {"temperature": 0, "seed": seed, "num_predict": 80},
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = json.loads(response.read().decode("utf-8"))
    content = str(raw.get("message", {}).get("content", ""))
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {}
    decision = str(parsed.get("decision", "UNKNOWN")).upper()
    if decision not in {"TRUE", "FALSE", "UNKNOWN"}:
        decision = "UNKNOWN"
    usage = {
        "prompt_eval_count": raw.get("prompt_eval_count") or 0,
        "eval_count": raw.get("eval_count") or 0,
        "total_duration": raw.get("total_duration") or 0,
        "response_model": raw.get("model"),
    }
    return decision, content, usage


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--worlds", type=int, default=3)
    parser.add_argument("--budget", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    worlds = build_worlds([args.seed], args.worlds)
    started = time.time()
    rows = []
    for world_index, world in enumerate(worlds):
        for claim_index, (scope_family, claim) in enumerate(build_claims(world)):
            observations, tool_calls = collect_exact_scope_trace(world, claim, args.budget)
            gate = evaluate_claim(claim, observations)
            decision, raw_content, usage = call_verifier(
                args.model,
                claim,
                observations,
                args.seed + world_index * 100 + claim_index,
            )
            truth = claim_truth(world, claim)
            expected = "TRUE" if truth else "FALSE"
            row = {
                "world_id": world.world_id,
                "connector_profile": world.profile.profile_id,
                "scope_family": scope_family,
                "claim_id": claim.claim_id,
                "quantifier": claim.quantifier,
                "predicate": claim.predicate,
                "truth": truth,
                "expected_decision": expected,
                "tool_budget": args.budget,
                "tool_calls": tool_calls,
                "observation_digests": [item.digest for item in observations],
                "gate_decision": gate.decision,
                "llm_decision": decision,
                "llm_correct": decision == expected,
                "llm_unsafe_commit": decision != "UNKNOWN" and decision != expected,
                "llm_matches_gate": decision == gate.decision,
                "raw_content": raw_content,
                "usage": usage,
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "claim_id": claim.claim_id,
                        "gate": gate.decision,
                        "llm": decision,
                        "unsafe": row["llm_unsafe_commit"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    answered = [row for row in rows if row["llm_decision"] != "UNKNOWN"]
    document = {
        "experiment": "matched_trace_independent_llm_verifier_v002",
        "model": args.model,
        "seed": args.seed,
        "world_count": len(worlds),
        "case_count": len(rows),
        "tool_budget": args.budget,
        "elapsed_seconds": time.time() - started,
        "information_condition": "the LLM verifier and deterministic gate receive byte-identical matched executor traces",
        "summary": {
            "gate_answer_rate": sum(row["gate_decision"] != "UNKNOWN" for row in rows) / len(rows),
            "llm_answer_rate": len(answered) / len(rows),
            "llm_task_accuracy_unknown_is_incorrect": sum(row["llm_correct"] for row in rows) / len(rows),
            "llm_answered_accuracy": (
                sum(row["llm_correct"] for row in answered) / len(answered) if answered else None
            ),
            "llm_unsafe_commit_rate": sum(row["llm_unsafe_commit"] for row in rows) / len(rows),
            "llm_gate_agreement_rate": sum(row["llm_matches_gate"] for row in rows) / len(rows),
            "prompt_tokens": sum(row["usage"]["prompt_eval_count"] for row in rows),
            "generated_tokens": sum(row["usage"]["eval_count"] for row in rows),
        },
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"output": str(args.output), "summary": document["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
