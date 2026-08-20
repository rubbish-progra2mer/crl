#!/usr/bin/env python3
"""Exploratory killer test for tool-alias false corroboration.

This is intentionally a small, deterministic pilot. It does not constitute
Formal evidence for the Run.
"""

from __future__ import annotations

import argparse
import json
import random
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SYSTEM = """You are the decision component of a tool-using agent.
Infer the true value from the supplied tool responses. The environment
guarantees that at most one underlying failure domain is faulty. Repeated
calls to one tool are not independent evidence. Different tool identifiers
may or may not be independent. Return only the requested JSON object."""


SCHEMA = {
    "type": "object",
    "properties": {
        "decision": {"type": "string"},
        "accept": {"type": "boolean"},
        "confidence": {"type": "number"},
        "rationale": {"type": "string"},
    },
    "required": ["decision", "accept", "confidence", "rationale"],
}


DOMAINS = [
    "inventory location code",
    "deployed software release code",
    "appointment slot code",
    "account access-state code",
    "shipment destination code",
    "document revision code",
]


def build_cases(count: int) -> list[dict[str, Any]]:
    rng = random.Random(20260816)
    codes = [f"K{i:02d}" for i in range(10, 98)]
    rng.shuffle(codes)
    cases: list[dict[str, Any]] = []
    for i in range(count):
        truth, wrong = codes[2 * i], codes[2 * i + 1]
        cases.append(
            {
                "case_id": f"C{i + 1:02d}",
                "domain": DOMAINS[i % len(DOMAINS)],
                "truth": truth,
                "wrong": wrong,
                "order_seed": 9000 + i,
            }
        )
    return cases


def make_records(case: dict[str, Any], condition: str) -> list[dict[str, str]]:
    truth = case["truth"]
    wrong = case["wrong"]
    if condition == "same_tool_repeat":
        records = [
            {"tool": "T01", "value": wrong},
            {"tool": "T01", "value": wrong},
            {"tool": "T01", "value": wrong},
            {"tool": "T01", "value": wrong},
            {"tool": "T05", "value": truth},
            {"tool": "T06", "value": truth},
        ]
    elif condition == "alias_opaque":
        records = [
            {"tool": "T01", "value": wrong},
            {"tool": "T02", "value": wrong},
            {"tool": "T03", "value": wrong},
            {"tool": "T04", "value": wrong},
            {"tool": "T05", "value": truth},
            {"tool": "T06", "value": truth},
        ]
    elif condition == "alias_provenance":
        records = [
            {"tool": "T01", "failure_domain": "D01", "value": wrong},
            {"tool": "T02", "failure_domain": "D01", "value": wrong},
            {"tool": "T03", "failure_domain": "D01", "value": wrong},
            {"tool": "T04", "failure_domain": "D01", "value": wrong},
            {"tool": "T05", "failure_domain": "D02", "value": truth},
            {"tool": "T06", "failure_domain": "D03", "value": truth},
        ]
    else:
        raise ValueError(f"Unknown condition: {condition}")
    random.Random(case["order_seed"]).shuffle(records)
    return records


def make_prompt(case: dict[str, Any], condition: str) -> str:
    records = make_records(case, condition)
    topology_note = (
        "The failure_domain field identifies responses that can fail together. "
        "Count corroboration by independent failure domains, not tool names."
        if condition == "alias_provenance"
        else "No explicit failure-domain metadata is available."
    )
    payload = {
        "task": f"Determine the true {case['domain']}.",
        "topology_note": topology_note,
        "responses": records,
        "allowed_values": sorted([case["truth"], case["wrong"]]),
        "output_instruction": (
            "Set decision to one allowed value. Set accept true only if the "
            "evidence warrants committing to that value. Confidence is 0 to 1."
        ),
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def chat(model: str, prompt: str, timeout: int, seed: int) -> tuple[dict[str, Any], dict[str, Any]]:
    request_body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "think": False,
        "format": SCHEMA,
        "options": {"temperature": 0, "seed": seed},
    }
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(request_body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = json.loads(response.read().decode("utf-8"))
    elapsed = time.time() - started
    content = raw.get("message", {}).get("content", "")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {"decision": "", "accept": False, "confidence": 0.0, "rationale": content}
    meta = {
        "elapsed_seconds": elapsed,
        "prompt_eval_count": raw.get("prompt_eval_count"),
        "eval_count": raw.get("eval_count"),
        "done_reason": raw.get("done_reason"),
    }
    return parsed, meta


def append_jsonl(path: Path, item: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_condition: dict[str, dict[str, Any]] = {}
    for condition in sorted({row["condition"] for row in rows}):
        selected = [row for row in rows if row["condition"] == condition]
        n = len(selected)
        correct = sum(row["is_correct"] for row in selected)
        accepted_wrong = sum(row["accepted_wrong"] for row in selected)
        by_condition[condition] = {
            "n": n,
            "accuracy": correct / n if n else None,
            "accepted_wrong_rate": accepted_wrong / n if n else None,
            "mean_confidence": (
                sum(float(row["response"].get("confidence", 0.0)) for row in selected) / n
                if n
                else None
            ),
        }
    alias = by_condition.get("alias_opaque", {}).get("accepted_wrong_rate")
    repeat = by_condition.get("same_tool_repeat", {}).get("accepted_wrong_rate")
    provenance = by_condition.get("alias_provenance", {}).get("accepted_wrong_rate")
    return {
        "by_condition": by_condition,
        "alias_amplification_vs_repeat": alias - repeat if alias is not None and repeat is not None else None,
        "provenance_recovery_vs_opaque": alias - provenance if alias is not None and provenance is not None else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3:4b")
    parser.add_argument("--cases", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", type=Path, default=Path("pilot_results_qwen3_4b.jsonl"))
    args = parser.parse_args()
    if args.cases < 1 or args.cases > 40:
        raise SystemExit("--cases must be between 1 and 40")

    rows: list[dict[str, Any]] = []
    conditions = ["same_tool_repeat", "alias_opaque", "alias_provenance"]
    for case in build_cases(args.cases):
        for condition in conditions:
            prompt = make_prompt(case, condition)
            try:
                response, meta = chat(args.model, prompt, args.timeout, case["order_seed"])
                error = None
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                response = {"decision": "", "accept": False, "confidence": 0.0, "rationale": ""}
                meta = {}
                error = repr(exc)
            decision = str(response.get("decision", "")).strip()
            accepted = bool(response.get("accept", False))
            row = {
                "model": args.model,
                "case_id": case["case_id"],
                "domain": case["domain"],
                "truth": case["truth"],
                "wrong": case["wrong"],
                "condition": condition,
                "prompt": prompt,
                "response": response,
                "is_correct": decision == case["truth"],
                "accepted_wrong": accepted and decision == case["wrong"],
                "meta": meta,
                "error": error,
            }
            rows.append(row)
            append_jsonl(args.output, row)
            print(
                json.dumps(
                    {
                        "case": case["case_id"],
                        "condition": condition,
                        "decision": decision,
                        "correct": row["is_correct"],
                        "accepted_wrong": row["accepted_wrong"],
                        "error": error,
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    summary_path = args.output.with_suffix(".summary.json")
    summary_path.write_text(
        json.dumps(summarize(rows), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"summary": str(summary_path), **summarize(rows)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
