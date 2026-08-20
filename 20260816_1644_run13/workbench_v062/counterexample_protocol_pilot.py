from __future__ import annotations

import itertools
import json
import os
import random
import re
import time
import urllib.request
from pathlib import Path
from typing import Any, Iterable


MODEL = os.environ.get("CRL_V062_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
ROUNDS = 6
POLICIES_PER_CALL = 8
ACTIONS = ("COMPLETE", "RETRY", "QUERY", "STOP")
AXES = {
    "status": ("success", "transient_error", "permanent_error"),
    "fields": ("complete", "missing"),
    "freshness": ("fresh", "stale"),
    "confirmation": ("confirmed", "unconfirmed"),
    "effect": ("reversible", "irreversible"),
}
AXIS_NAMES = tuple(AXES)
RESULT_PATH = Path(__file__).with_name(
    f"counterexample_protocol_{MODEL.replace(':', '_').replace('.', '_')}.json"
)


def all_states() -> list[dict[str, str]]:
    return [
        dict(zip(AXIS_NAMES, values))
        for values in itertools.product(*(AXES[name] for name in AXIS_NAMES))
    ]


STATES = all_states()


def state_key(state: dict[str, str]) -> str:
    return "|".join(state[name] for name in AXIS_NAMES)


STATE_BY_KEY = {state_key(state): state for state in STATES}


def oracle(state: dict[str, str]) -> str:
    if state["fields"] == "missing":
        return "QUERY"
    if state["freshness"] == "stale":
        return "QUERY"
    if state["status"] == "success":
        return "COMPLETE"
    if state["status"] == "permanent_error":
        return "STOP"
    if state["effect"] == "irreversible" and state["confirmation"] == "unconfirmed":
        return "QUERY"
    return "RETRY"


INITIAL_STATES = [
    {
        "status": "success",
        "fields": "complete",
        "freshness": "fresh",
        "confirmation": "confirmed",
        "effect": "reversible",
    },
    {
        "status": "transient_error",
        "fields": "complete",
        "freshness": "fresh",
        "confirmation": "confirmed",
        "effect": "reversible",
    },
    {
        "status": "permanent_error",
        "fields": "complete",
        "freshness": "fresh",
        "confirmation": "confirmed",
        "effect": "reversible",
    },
    {
        "status": "transient_error",
        "fields": "missing",
        "freshness": "fresh",
        "confirmation": "confirmed",
        "effect": "reversible",
    },
]
INITIAL_SUPPORT = tuple(state_key(state) for state in INITIAL_STATES)


def validate_policy(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    default = raw.get("default")
    rules = raw.get("rules")
    if default not in ACTIONS or not isinstance(rules, list) or len(rules) > 12:
        return None
    clean_rules: list[dict[str, Any]] = []
    for rule in rules:
        if not isinstance(rule, dict) or rule.get("action") not in ACTIONS:
            return None
        when = rule.get("when")
        if not isinstance(when, dict) or not when:
            return None
        clean_when: dict[str, str] = {}
        for key, value in when.items():
            if key not in AXES or value not in AXES[key]:
                return None
            clean_when[key] = value
        clean_rules.append({"when": clean_when, "action": rule["action"]})
    return {
        "name": str(raw.get("name", "unnamed"))[:120],
        "rules": clean_rules,
        "default": default,
    }


def act(policy: dict[str, Any], state: dict[str, str]) -> str:
    for rule in policy["rules"]:
        if all(state[key] == value for key, value in rule["when"].items()):
            return rule["action"]
    return policy["default"]


def profile(policy: dict[str, Any]) -> tuple[str, ...]:
    return tuple(act(policy, state) for state in STATES)


ORACLE_PROFILE = tuple(oracle(state) for state in STATES)


def matches_support(policy: dict[str, Any], support: Iterable[str]) -> bool:
    return all(act(policy, STATE_BY_KEY[key]) == oracle(STATE_BY_KEY[key]) for key in support)


def differs_globally(policy: dict[str, Any]) -> bool:
    return profile(policy) != ORACLE_PROFILE


def unique_policies(policies: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, ...]] = set()
    kept: list[dict[str, Any]] = []
    for policy in policies:
        sig = profile(policy)
        if sig not in seen:
            seen.add(sig)
            kept.append(policy)
    return kept


def parse_json_object(text: str) -> dict[str, Any] | None:
    candidates = [text.strip()]
    fenced = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    candidates.extend(part.strip() for part in fenced)
    first = text.find("{")
    last = text.rfind("}")
    if first >= 0 and last > first:
        candidates.append(text[first : last + 1])
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def prompt_for(support: Iterable[str], purpose: str) -> str:
    observations = [
        {**STATE_BY_KEY[key], "action": oracle(STATE_BY_KEY[key])}
        for key in support
    ]
    return f"""You are generating compact deterministic workflow policies for a benign synthetic study.
Infer multiple plausible policies consistent with every observed state-action pair. Unobserved states are genuinely unspecified to you. Produce diverse simple generalizations; do not explain them.

Policy DSL:
- Output one JSON object with key \"policies\" containing at most {POLICIES_PER_CALL} policies.
- Each policy has name, ordered rules, and default.
- A rule is {{\"when\": {{one or more feature:value tests}}, \"action\": ACTION}}.
- Allowed features and values: {json.dumps(AXES, ensure_ascii=False)}
- Allowed actions: {json.dumps(ACTIONS)}
- First matching rule wins; otherwise default applies.
- Use only allowed feature values and actions. Every policy must match all observations.
- Make the policies behaviorally diverse on unobserved states.

Purpose tag: {purpose}
Observed pairs:
{json.dumps(observations, ensure_ascii=False, indent=2)}
"""


def chat(support: Iterable[str], seed: int, purpose: str) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.7, "seed": seed, "num_predict": 4096},
        "messages": [
            {
                "role": "system",
                "content": "Return only valid JSON following the requested policy DSL.",
            },
            {"role": "user", "content": prompt_for(support, purpose)},
        ],
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


def extract_policies(response: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    content = response.get("message", {}).get("content", "")
    parsed = parse_json_object(content) if isinstance(content, str) else None
    raw_policies = parsed.get("policies", []) if parsed else []
    valid = []
    if isinstance(raw_policies, list):
        for raw in raw_policies:
            policy = validate_policy(raw)
            if policy is not None:
                valid.append(policy)
    return unique_policies(valid), content if isinstance(content, str) else ""


def best_cell(policies: list[dict[str, Any]], support: set[str]) -> tuple[str | None, int]:
    best: tuple[int, str] | None = None
    for state in STATES:
        key = state_key(state)
        if key in support:
            continue
        load = sum(act(policy, state) != oracle(state) for policy in policies)
        candidate = (load, key)
        if load > 0 and (best is None or candidate > best):
            best = candidate
    return (best[1], best[0]) if best else (None, 0)


def policy_killed(policy: dict[str, Any], support: Iterable[str]) -> bool:
    return any(act(policy, STATE_BY_KEY[key]) != oracle(STATE_BY_KEY[key]) for key in support)


def kill_rate(policies: list[dict[str, Any]], support: Iterable[str]) -> float | None:
    if not policies:
        return None
    return sum(policy_killed(policy, support) for policy in policies) / len(policies)


def random_policy(rng: random.Random) -> dict[str, Any]:
    rule_count = rng.randint(1, 5)
    rules = []
    for _ in range(rule_count):
        keys = rng.sample(list(AXIS_NAMES), rng.randint(1, 3))
        when = {key: rng.choice(AXES[key]) for key in keys}
        rules.append({"when": when, "action": rng.choice(ACTIONS)})
    return {"name": "procedural", "rules": rules, "default": rng.choice(ACTIONS)}


def oracle_fallback_rules() -> list[dict[str, Any]]:
    return [
        {"when": dict(state), "action": oracle(state)}
        for state in STATES
    ]


def procedural_bank(
    seed: int,
    size: int = 600,
    exclude_profiles: set[tuple[str, ...]] | None = None,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    excluded = exclude_profiles or set()
    bank: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set(excluded)
    attempts = 0
    while len(bank) < size and attempts < 200000:
        attempts += 1
        override_count = rng.randint(1, 4)
        overrides = []
        for _ in range(override_count):
            keys = rng.sample(list(AXIS_NAMES), rng.randint(1, 3))
            overrides.append(
                {
                    "when": {key: rng.choice(AXES[key]) for key in keys},
                    "action": rng.choice(ACTIONS),
                }
            )
        policy = {
            "name": f"procedural_{seed}_{attempts}",
            "rules": overrides + oracle_fallback_rules(),
            "default": "QUERY",
        }
        sig = profile(policy)
        if (
            sig not in seen
            and matches_support(policy, INITIAL_SUPPORT)
            and differs_globally(policy)
        ):
            bank.append(policy)
            seen.add(sig)
    if len(bank) != size:
        raise RuntimeError(f"procedural bank underfilled: requested={size}, actual={len(bank)}")
    return bank


def hand_mutants() -> list[dict[str, Any]]:
    raw = [
        {"name": "ignore_stale", "rules": [{"when": {"fields": "missing"}, "action": "QUERY"}, {"when": {"status": "success"}, "action": "COMPLETE"}, {"when": {"status": "permanent_error"}, "action": "STOP"}], "default": "RETRY"},
        {"name": "retry_irreversible", "rules": [{"when": {"fields": "missing"}, "action": "QUERY"}, {"when": {"freshness": "stale"}, "action": "QUERY"}, {"when": {"status": "success"}, "action": "COMPLETE"}, {"when": {"status": "permanent_error"}, "action": "STOP"}], "default": "RETRY"},
        {"name": "success_first", "rules": [{"when": {"status": "success"}, "action": "COMPLETE"}, {"when": {"fields": "missing"}, "action": "QUERY"}, {"when": {"freshness": "stale"}, "action": "QUERY"}, {"when": {"status": "permanent_error"}, "action": "STOP"}], "default": "RETRY"},
        {"name": "permanent_first", "rules": [{"when": {"status": "permanent_error"}, "action": "STOP"}, {"when": {"fields": "missing"}, "action": "QUERY"}, {"when": {"freshness": "stale"}, "action": "QUERY"}, {"when": {"status": "success"}, "action": "COMPLETE"}], "default": "RETRY"},
        {"name": "query_unconfirmed", "rules": [{"when": {"fields": "missing"}, "action": "QUERY"}, {"when": {"freshness": "stale"}, "action": "QUERY"}, {"when": {"confirmation": "unconfirmed"}, "action": "QUERY"}, {"when": {"status": "success"}, "action": "COMPLETE"}, {"when": {"status": "permanent_error"}, "action": "STOP"}], "default": "RETRY"},
        {"name": "stop_all_errors", "rules": [{"when": {"fields": "missing"}, "action": "QUERY"}, {"when": {"freshness": "stale"}, "action": "QUERY"}, {"when": {"status": "success"}, "action": "COMPLETE"}], "default": "STOP"},
        {"name": "ignore_missing_on_permanent", "rules": [{"when": {"status": "permanent_error"}, "action": "STOP"}, {"when": {"fields": "missing"}, "action": "QUERY"}, {"when": {"freshness": "stale"}, "action": "QUERY"}, {"when": {"status": "success"}, "action": "COMPLETE"}], "default": "RETRY"},
        {"name": "stale_stop", "rules": [{"when": {"fields": "missing"}, "action": "QUERY"}, {"when": {"freshness": "stale"}, "action": "STOP"}, {"when": {"status": "success"}, "action": "COMPLETE"}, {"when": {"status": "permanent_error"}, "action": "STOP"}], "default": "RETRY"},
    ]
    return unique_policies(policy for item in raw if (policy := validate_policy(item)) is not None)


def greedy_support(policies: list[dict[str, Any]], budget: int) -> list[str]:
    support = set(INITIAL_SUPPORT)
    for _ in range(budget):
        remaining = [policy for policy in policies if not policy_killed(policy, support)]
        key, _ = best_cell(remaining or policies, support)
        if key is None:
            key = sorted(set(STATE_BY_KEY) - support)[0]
        support.add(key)
    return sorted(support)


def random_baseline(bank: list[dict[str, Any]], added_budget: int) -> dict[str, Any]:
    candidates = sorted(set(STATE_BY_KEY) - set(INITIAL_SUPPORT))
    rng = random.Random(620062)
    rates = []
    for _ in range(500):
        added = rng.sample(candidates, added_budget)
        rates.append(float(kill_rate(bank, set(INITIAL_SUPPORT) | set(added)) or 0.0))
    rates.sort()
    return {
        "repetitions": len(rates),
        "median": rates[len(rates) // 2],
        "p10": rates[len(rates) // 10],
        "p90": rates[(9 * len(rates)) // 10],
        "mean": sum(rates) / len(rates),
    }


def generate_independent_holdout() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    policies: list[dict[str, Any]] = []
    meta = []
    for index, seed in enumerate((9101, 9102, 9103, 9104, 9105, 9106)):
        response = chat(INITIAL_SUPPORT, seed, f"independent_holdout_{index + 1}")
        extracted, content = extract_policies(response)
        colliders = [
            policy
            for policy in extracted
            if matches_support(policy, INITIAL_SUPPORT) and differs_globally(policy)
        ]
        policies.extend(colliders)
        meta.append(
            {
                "seed": seed,
                "valid_unique": len(extracted),
                "colliders": len(colliders),
                "elapsed_seconds": response.get("client_elapsed_seconds", 0.0),
                "prompt_tokens": response.get("prompt_eval_count", 0),
                "output_tokens": response.get("eval_count", 0),
                "raw_content": content,
            }
        )
    return unique_policies(policies), meta


def main() -> None:
    support = set(INITIAL_SUPPORT)
    rounds = []
    all_generated: list[dict[str, Any]] = []
    for round_index in range(ROUNDS):
        seed = 6200 + round_index
        response = chat(sorted(support), seed, f"adaptive_round_{round_index + 1}")
        extracted, content = extract_policies(response)
        colliders = [
            policy
            for policy in extracted
            if matches_support(policy, support) and differs_globally(policy)
        ]
        colliders = unique_policies(colliders)
        all_generated.extend(colliders)
        key, load = best_cell(colliders, support)
        row = {
            "round": round_index + 1,
            "seed": seed,
            "support_before": sorted(support),
            "valid_unique": len(extracted),
            "colliders": len(colliders),
            "collision_yield": len(colliders) / len(extracted) if extracted else 0.0,
            "selected_cell": key,
            "selected_oracle_action": oracle(STATE_BY_KEY[key]) if key else None,
            "distinguishing_load": load,
            "elapsed_seconds": response.get("client_elapsed_seconds", 0.0),
            "prompt_tokens": response.get("prompt_eval_count", 0),
            "output_tokens": response.get("eval_count", 0),
            "raw_content": content,
            "collider_policies": colliders,
        }
        rounds.append(row)
        print(json.dumps({key: row[key] for key in ("round", "valid_unique", "colliders", "selected_cell", "distinguishing_load")}, ensure_ascii=False), flush=True)
        if key is None:
            break
        support.add(key)

    procedural_train = procedural_bank(seed=6202026)
    train_profiles = {profile(policy) for policy in procedural_train}
    procedural_test = procedural_bank(seed=6202027, exclude_profiles=train_profiles)
    generated_holdout, holdout_meta = generate_independent_holdout()
    added_budget = len(support) - len(INITIAL_SUPPORT)
    hand_support = greedy_support(hand_mutants(), added_budget)
    programmatic_support = greedy_support(procedural_train, added_budget)
    random_stats = random_baseline(procedural_test, added_budget)
    result = {
        "model": MODEL,
        "endpoint": ENDPOINT,
        "registered_round_budget": ROUNDS,
        "initial_support": list(INITIAL_SUPPORT),
        "final_support": sorted(support),
        "added_budget": added_budget,
        "rounds_completed": len(rounds),
        "rounds_with_added_cell": added_budget,
        "generated_unique_colliders": len(unique_policies(all_generated)),
        "rounds": rounds,
        "independent_generated_holdout": generated_holdout,
        "independent_generated_holdout_meta": holdout_meta,
        "procedural_train_bank_size": len(procedural_train),
        "procedural_test_bank_size": len(procedural_test),
        "hand_mutant_count": len(hand_mutants()),
        "hand_greedy_support": hand_support,
        "programmatic_greedy_support": programmatic_support,
        "metrics": {
            "adaptive_procedural_holdout_kill_rate": kill_rate(procedural_test, support),
            "hand_procedural_holdout_kill_rate": kill_rate(procedural_test, hand_support),
            "programmatic_procedural_holdout_kill_rate": kill_rate(procedural_test, programmatic_support),
            "random_procedural_holdout": random_stats,
            "adaptive_generated_holdout_kill_rate": kill_rate(generated_holdout, support),
            "hand_generated_holdout_kill_rate": kill_rate(generated_holdout, hand_support),
            "programmatic_generated_holdout_kill_rate": kill_rate(generated_holdout, programmatic_support),
        },
        "scope_note": "Local synthetic benign policy programs only. No represented workflow action or external tool was executed.",
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"model": MODEL, "added_budget": added_budget, "metrics": result["metrics"]}, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
