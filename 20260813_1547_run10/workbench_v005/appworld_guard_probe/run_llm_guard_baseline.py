from __future__ import annotations

import itertools
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "llm_guard_baseline_results.json"
MODELS = ("qwen3:4b", "qwen2.5:7b", "qwen3:8b")
PREDICATES = (
    "contact_present",
    "receiver_resolvable",
    "sufficient_balance",
)
KNOWN_POSITIVE = {
    "contact_present": True,
    "receiver_resolvable": True,
    "sufficient_balance": True,
}
ACTIVE_NEGATIVES = (
    {"contact_present": False, "receiver_resolvable": True, "sufficient_balance": True},
    {"contact_present": True, "receiver_resolvable": False, "sufficient_balance": True},
    {"contact_present": True, "receiver_resolvable": True, "sufficient_balance": False},
)
# Fixed before inference. These are a same-budget passive/random comparison, not
# selected after seeing model outputs.
PASSIVE_NEGATIVES = (
    {"contact_present": False, "receiver_resolvable": False, "sufficient_balance": True},
    {"contact_present": True, "receiver_resolvable": False, "sufficient_balance": False},
    {"contact_present": False, "receiver_resolvable": True, "sufficient_balance": False},
)


def schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "required_predicates": {
                "type": "array",
                "items": {"type": "string", "enum": list(PREDICATES)},
                "uniqueItems": True,
            }
        },
        "required": ["required_predicates"],
        "additionalProperties": False,
    }


def labeled(state: dict[str, bool], success: bool) -> dict[str, Any]:
    return {"state": state, "official_terminal_success": success}


def prompt(condition: str) -> str:
    evidence: list[dict[str, Any]] = [labeled(KNOWN_POSITIVE, True)]
    if condition == "active_paired":
        evidence.extend(labeled(state, False) for state in ACTIVE_NEGATIVES)
    elif condition == "passive_same_budget":
        evidence.extend(labeled(state, False) for state in PASSIVE_NEGATIVES)
    elif condition != "success_only":
        raise ValueError(condition)

    return (
        "A tool-using agent stores the following fixed procedure for reuse.\n"
        "Goal: privately send the requested payment to the person identified by a phone number.\n"
        "Procedure: search the phone contacts for that exact phone number; take the unique contact email; "
        "search Venmo for that exact email; inspect the sender balance; create the requested transaction.\n\n"
        "The runtime can test these Boolean state predicates before deciding whether to reuse the procedure:\n"
        "- contact_present: the exact phone contact exists.\n"
        "- receiver_resolvable: the contact email resolves to the intended Venmo receiver.\n"
        "- sufficient_balance: the sender balance covers the requested amount.\n\n"
        "Observed development evidence (the terminal label comes from an independent evaluator):\n"
        f"{json.dumps(evidence, ensure_ascii=False, indent=2)}\n\n"
        "Infer the least restrictive positive-conjunction guard supported by the procedure and evidence. "
        "Return the predicate names that must be true. Return only the requested JSON."
    )


def call_ollama(model: str, condition: str) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Follow the JSON schema exactly. /no_think"},
            {"role": "user", "content": prompt(condition)},
        ],
        "stream": False,
        "think": False,
        "format": schema(),
        "options": {"temperature": 0, "seed": 20260813, "num_predict": 120},
        "keep_alive": "10m",
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=240) as response:
        raw = json.loads(response.read().decode("utf-8"))
    elapsed = time.perf_counter() - started
    content = raw.get("message", {}).get("content", "")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = None
    return {
        "model": model,
        "condition": condition,
        "parsed": parsed,
        "raw_content": content,
        "elapsed_seconds": round(elapsed, 4),
        "prompt_eval_count": raw.get("prompt_eval_count"),
        "eval_count": raw.get("eval_count"),
        "done_reason": raw.get("done_reason"),
    }


def score(required: list[str] | None) -> dict[str, Any]:
    selected = set(required or [])
    truth = set(PREDICATES)
    false_admissions = 0
    rejected_successes = 0
    for values in itertools.product((False, True), repeat=len(PREDICATES)):
        state = dict(zip(PREDICATES, values, strict=True))
        admitted = all(state[name] for name in selected)
        success = all(state[name] for name in truth)
        false_admissions += int(admitted and not success)
        rejected_successes += int((not admitted) and success)
    return {
        "exact_guard": selected == truth,
        "false_admissions_over_8_states": false_admissions,
        "rejected_successes_over_8_states": rejected_successes,
    }


def main() -> None:
    calls: list[dict[str, Any]] = []
    for model in MODELS:
        for condition in ("success_only", "passive_same_budget", "active_paired"):
            record = call_ollama(model, condition)
            parsed = record.get("parsed")
            required = parsed.get("required_predicates") if isinstance(parsed, dict) else None
            record["score"] = score(required if isinstance(required, list) else None)
            calls.append(record)

    trivial = score(list(PREDICATES))
    output = {
        "artifact_class": "scratch_strong_baseline",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "fixture": "AppWorld dev 37a8675_1 with the same three hand-declared predicates",
        "conditions": {
            "success_only": "procedure text plus one successful source state; no failed intervention labels",
            "passive_same_budget": "one successful source state plus three fixed passive failed states",
            "active_paired": "one successful source state plus three single-predicate paired failures",
        },
        "trivial_all_predicates_required_baseline": {
            "requires_no_labels_or_model": True,
            "required_predicates": list(PREDICATES),
            "score": trivial,
            "interpretation": (
                "The real fixture's catalogue contains only necessary predicates, so requiring the entire "
                "catalogue exactly matches the learned guard. This fixture cannot establish a learning delta."
            ),
        },
        "calls": calls,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
