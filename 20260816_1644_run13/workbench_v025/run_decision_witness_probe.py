#!/usr/bin/env python3
"""Run the source-compiled decision-witness probe on PolarityCheck held-out cases."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


COMPILER_SYSTEM = """You compile an operational policy into executable semantic witnesses.
Given ONLY the reference policy, return JSON with exactly four witnesses. Each witness must have:
- id: w1, w2, w3, or w4
- scenario: a concrete situation that supplies all facts needed for a decision
- question: one operational decision question
- options: 2 to 4 mutually exclusive concrete action or status strings
- expected_index: the zero-based index of the option required by the reference policy
- facet: one of polarity, scope, exception, quantity_unit, modality, condition, timing
Probe decision boundaries, exceptions, modality, scope, or quantities actually supported by the policy. Across the set include a case where the rule applies and, when meaningful, one where it does not. Do not ask about wording, quotations, paraphrases, similarity, or another policy. Do not invent an exception that contradicts the policy.
Return only: {\"witnesses\":[...]}"""

EXECUTOR_SYSTEM = """You execute one operational policy on supplied decision witnesses.
For every witness, use ONLY the policy and scenario to select exactly one listed option. Return its zero-based option_index. Do not compare wording and do not repair or reinterpret the policy using outside norms.
Return only: {\"choices\":[{\"id\":\"w1\",\"option_index\":0}, ...]}"""

PAIR_JUDGE_SYSTEM = """You are a strict operational-semantics judge. Compare a reference policy and a candidate policy. Answer SAME only if required, prohibited, and permitted actions, conditions, scope, exceptions, modality, quantities or units, and timing all agree. Otherwise answer DIFFERENT. Do not use wording similarity as the criterion.
Return only: {\"decision\":\"SAME\" or \"DIFFERENT\",\"reason\":\"brief concrete reason\"}"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(temporary, path)


def extract_json(text: str) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        starts = [position for position in (cleaned.find("{"), cleaned.find("[")) if position >= 0]
        if not starts:
            raise
        value, _ = decoder.raw_decode(cleaned[min(starts):])
        return value


def call_ollama(url: str, model: str, system: str, user: str, num_predict: int) -> dict[str, Any]:
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "format": "json",
        "keep_alive": "30m",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {
            "temperature": 0,
            "seed": 20260816,
            "num_ctx": 8192,
            "num_predict": num_predict,
        },
    }
    request = urllib.request.Request(
        url.rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    last_error: Exception | None = None
    for attempt in range(2):
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=240) as response:
                body = json.loads(response.read().decode("utf-8"))
            content = body.get("message", {}).get("content", "")
            parsed = extract_json(content)
            return {
                "ok": True,
                "parsed": parsed,
                "raw": content,
                "wall_seconds": round(time.perf_counter() - started, 4),
                "prompt_eval_count": body.get("prompt_eval_count"),
                "eval_count": body.get("eval_count"),
                "total_duration_ns": body.get("total_duration"),
            }
        except (OSError, ValueError, urllib.error.URLError) as error:
            last_error = error
            if attempt == 0:
                time.sleep(1)
    return {
        "ok": False,
        "error": f"{type(last_error).__name__}: {last_error}",
        "wall_seconds": round(time.perf_counter() - started, 4),
    }


def validate_witnesses(call: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    if not call.get("ok") or not isinstance(call.get("parsed"), dict):
        return [], ["compiler_call_or_json_invalid"]
    raw_witnesses = call["parsed"].get("witnesses")
    if not isinstance(raw_witnesses, list) or len(raw_witnesses) != 4:
        return [], ["witness_count_not_four"]
    witnesses: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    allowed_facets = {"polarity", "scope", "exception", "quantity_unit", "modality", "condition", "timing"}
    for position, witness in enumerate(raw_witnesses):
        prefix = f"witness_{position}"
        if not isinstance(witness, dict):
            errors.append(prefix + "_not_object")
            continue
        witness_id = witness.get("id")
        scenario = witness.get("scenario")
        question = witness.get("question")
        options = witness.get("options")
        expected_index = witness.get("expected_index")
        if isinstance(expected_index, str) and expected_index.strip().isdigit():
            expected_index = int(expected_index.strip())
        facet = witness.get("facet")
        valid = True
        if not isinstance(witness_id, str) or not witness_id or witness_id in seen_ids:
            errors.append(prefix + "_bad_id")
            valid = False
        if isinstance(scenario, (dict, list)):
            scenario = json.dumps(scenario, ensure_ascii=False, sort_keys=True)
        if not isinstance(scenario, str) or not scenario.strip():
            errors.append(prefix + "_bad_scenario")
            valid = False
        if not isinstance(question, str) or not question.strip():
            errors.append(prefix + "_bad_question")
            valid = False
        if not isinstance(options, list) or not 2 <= len(options) <= 4 or not all(isinstance(x, str) and x.strip() for x in options):
            errors.append(prefix + "_bad_options")
            valid = False
        if isinstance(expected_index, bool) or not isinstance(expected_index, int) or not isinstance(options, list) or not 0 <= expected_index < len(options):
            errors.append(prefix + "_bad_expected_index")
            valid = False
        if facet not in allowed_facets:
            errors.append(prefix + "_bad_facet")
            valid = False
        if valid:
            seen_ids.add(witness_id)
            witnesses.append({
                "id": witness_id,
                "scenario": scenario.strip(),
                "question": question.strip(),
                "options": [x.strip() for x in options],
                "expected_index": expected_index,
                "facet": facet,
            })
    if len(witnesses) != 4:
        errors.append("not_all_witnesses_valid")
        return [], errors
    return witnesses, errors


def compiler_user(reference: str) -> str:
    return "REFERENCE POLICY:\n" + reference


def executor_user(policy: str, witnesses: list[dict[str, Any]]) -> str:
    public_witnesses = [
        {key: witness[key] for key in ("id", "scenario", "question", "options")}
        for witness in witnesses
    ]
    return "POLICY:\n" + policy + "\n\nWITNESSES:\n" + json.dumps(public_witnesses, ensure_ascii=False)


def judge_user(reference: str, candidate: str) -> str:
    return "REFERENCE POLICY:\n" + reference + "\n\nCANDIDATE POLICY:\n" + candidate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--url", default="http://127.0.0.1:11434")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    with args.corpus.open("r", encoding="utf-8") as handle:
        corpus = json.load(handle)
    cases = corpus["cases"]
    if args.limit is not None:
        cases = cases[: args.limit]

    if args.output.exists():
        with args.output.open("r", encoding="utf-8") as handle:
            result = json.load(handle)
        if result.get("model") != args.model:
            raise SystemExit("Output model does not match --model")
    else:
        result = {
            "schema_version": 1,
            "experiment": "source-compiled-decision-witness",
            "model": args.model,
            "seed": 20260816,
            "temperature": 0,
            "corpus_path": str(args.corpus.resolve()),
            "created_at_utc": utc_now(),
            "rows": [],
        }
    completed = {row["id"] for row in result["rows"]}

    for index, case in enumerate(cases, start=1):
        if case["id"] in completed:
            continue
        print(f"[{index}/{len(cases)}] {case['id']}", flush=True)
        compile_call = call_ollama(args.url, args.model, COMPILER_SYSTEM, compiler_user(case["root"]), 1200)
        witnesses, validation_errors = validate_witnesses(compile_call)
        root_call: dict[str, Any] | None = None
        candidate_call: dict[str, Any] | None = None
        if witnesses:
            root_call = call_ollama(args.url, args.model, EXECUTOR_SYSTEM, executor_user(case["root"], witnesses), 500)
            candidate_call = call_ollama(args.url, args.model, EXECUTOR_SYSTEM, executor_user(case["mutated"], witnesses), 500)
        judge_call = call_ollama(args.url, args.model, PAIR_JUDGE_SYSTEM, judge_user(case["root"], case["mutated"]), 300)
        result["rows"].append({
            "id": case["id"],
            "mutation_class": case["mutation_class"],
            "gold": "SAME" if case["mutation_class"] == "faithful_control" else "DIFFERENT",
            "compiler": compile_call,
            "compiler_validation_errors": validation_errors,
            "validated_witnesses": witnesses,
            "root_execution": root_call,
            "candidate_execution": candidate_call,
            "direct_pair_judge": judge_call,
        })
        result["updated_at_utc"] = utc_now()
        atomic_write_json(args.output, result)

    print(f"completed={len(result['rows'])} output={args.output}", flush=True)


if __name__ == "__main__":
    main()
