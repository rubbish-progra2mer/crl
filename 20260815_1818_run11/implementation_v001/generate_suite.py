from __future__ import annotations

import argparse
import copy
import json
import random
from pathlib import Path
from typing import Any, Callable


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def _plain_copy(base: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(base)


def _top_level_record_key(tool_result: dict[str, Any]) -> str | None:
    keys = [key for key, value in tool_result.items() if isinstance(value, list)]
    if len(keys) > 1:
        raise ValueError("tool result has more than one top-level record list")
    return keys[0] if keys else None


def _apply_record_order(tool_result: dict[str, Any], order: list[int]) -> None:
    key = _top_level_record_key(tool_result)
    if key is None:
        if order:
            raise ValueError("cannot apply a record order to a scalar tool result")
        return
    records = tool_result[key]
    if len(records) != len(order):
        raise ValueError("record order length mismatch")
    tool_result[key] = [records[index] for index in order]


def filtered_argmin(index: int, rng: random.Random) -> dict[str, Any]:
    prefix = f"M{index:02d}"
    identifiers = [f"{prefix}-{letter}" for letter in "ABCD"]
    best = rng.randint(4, 12)
    scores = [best, best + rng.randint(4, 9), max(1, best - 2), best + rng.randint(10, 18)]
    eligible = [True, True, False, True]
    base = {
        "items": [
            {
                "item_id": identifier,
                "score": score,
                "eligible": allowed,
                "display_rank": position + 1,
            }
            for position, (identifier, score, allowed) in enumerate(
                zip(identifiers, scores, eligible, strict=True)
            )
        ],
        "debug": {"cached_guess": identifiers[2]},
    }
    relevant = copy.deepcopy(base)
    relevant["items"][0]["item_id"], relevant["items"][1]["item_id"] = (
        relevant["items"][1]["item_id"],
        relevant["items"][0]["item_id"],
    )
    plain = _plain_copy(base)
    for position, item in enumerate(plain["items"]):
        item["display_rank"] = 20 - position
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = identifiers[1]
    return {
        "case_id": f"filtered_argmin_{index:02d}",
        "family": "filtered_argmin",
        "answer_kind": "identifier",
        "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
        "expected": {
            "base": identifiers[0],
            "relevant": identifiers[1],
            "irrelevant_plain": identifiers[0],
            "irrelevant_adversarial": identifiers[0],
        },
        "relation": {
            "kind": "bijection",
            "mapping": {identifiers[0]: identifiers[1], identifiers[1]: identifiers[0]},
        },
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


def latest_confirmed(index: int, rng: random.Random) -> dict[str, Any]:
    del rng
    prefix = f"E{index:02d}"
    identifiers = [f"{prefix}-{letter}" for letter in "ABCD"]
    base = {
        "events": [
            {"event_id": identifiers[0], "timestamp": "2026-08-01T09:00:00Z", "status": "confirmed", "note": "east"},
            {"event_id": identifiers[1], "timestamp": "2026-08-05T09:00:00Z", "status": "cancelled", "note": "north"},
            {"event_id": identifiers[2], "timestamp": "2026-08-03T09:00:00Z", "status": "confirmed", "note": "west"},
            {"event_id": identifiers[3], "timestamp": "2026-08-06T09:00:00Z", "status": "cancelled", "note": "south"},
        ],
        "debug": {"cached_guess": identifiers[0]},
    }
    relevant = copy.deepcopy(base)
    relevant["events"][1]["event_id"], relevant["events"][2]["event_id"] = (
        relevant["events"][2]["event_id"],
        relevant["events"][1]["event_id"],
    )
    plain = _plain_copy(base)
    for position, event in enumerate(plain["events"]):
        event["note"] = f"decorative-{position}"
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = identifiers[3]
    return {
        "case_id": f"latest_confirmed_{index:02d}",
        "family": "latest_confirmed",
        "answer_kind": "identifier",
        "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
        "expected": {
            "base": identifiers[2],
            "relevant": identifiers[1],
            "irrelevant_plain": identifiers[2],
            "irrelevant_adversarial": identifiers[2],
        },
        "relation": {
            "kind": "bijection",
            "mapping": {identifiers[1]: identifiers[2], identifiers[2]: identifiers[1]},
        },
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


def valid_sum(index: int, rng: random.Random) -> dict[str, Any]:
    amounts = [rng.randint(3, 20), rng.randint(5, 25), rng.randint(60, 140), rng.randint(2, 18)]
    delta = rng.randint(2, 9)
    valid = [True, True, False, True]
    total = amounts[0] + amounts[1] + amounts[3]
    base = {
        "rows": [
            {"amount": amount, "valid": keep, "label": f"row-{position}"}
            for position, (amount, keep) in enumerate(zip(amounts, valid, strict=True))
        ],
        "debug": {"cached_guess": str(sum(amounts))},
    }
    relevant = copy.deepcopy(base)
    relevant["rows"][1]["amount"] += delta
    plain = _plain_copy(base)
    for position, row in enumerate(plain["rows"]):
        row["label"] = f"renamed-{position}"
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = str(total + 1000)
    return {
        "case_id": f"valid_sum_{index:02d}",
        "family": "valid_sum",
        "answer_kind": "integer",
        "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
        "expected": {
            "base": str(total),
            "relevant": str(total + delta),
            "irrelevant_plain": str(total),
            "irrelevant_adversarial": str(total),
        },
        "relation": {"kind": "numeric_delta", "delta": delta},
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


def tier_score(index: int, rng: random.Random) -> dict[str, Any]:
    severity = rng.randint(2, 12)
    bonus = rng.randint(8, 20)
    delta = rng.randint(2, 7)
    base_score = severity + bonus
    base = {
        "ticket": {
            "severity": severity,
            "customer_tier": "gold",
            "bonus": bonus,
            "sentiment": "calm",
        },
        "debug": {"cached_guess": str(severity)},
    }
    relevant = copy.deepcopy(base)
    relevant["ticket"]["severity"] += delta
    plain = _plain_copy(base)
    plain["ticket"]["sentiment"] = "angry"
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = str(base_score + 99)
    return {
        "case_id": f"tier_score_{index:02d}",
        "family": "tier_score",
        "answer_kind": "integer",
        "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
        "expected": {
            "base": str(base_score),
            "relevant": str(base_score + delta),
            "irrelevant_plain": str(base_score),
            "irrelevant_adversarial": str(base_score),
        },
        "relation": {"kind": "numeric_delta", "delta": delta},
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


def count_open(index: int, rng: random.Random) -> dict[str, Any]:
    del rng
    statuses = ["open", "closed", "open", "closed", "closed"]
    base = {
        "records": [
            {"record_id": f"C{index:02d}-{position}", "status": status, "label": f"label-{position}"}
            for position, status in enumerate(statuses)
        ],
        "debug": {"cached_guess": "5"},
    }
    relevant = copy.deepcopy(base)
    relevant["records"][1]["status"] = "open"
    plain = _plain_copy(base)
    for position, record in enumerate(plain["records"]):
        record["label"] = f"changed-{position}"
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = "0"
    return {
        "case_id": f"count_open_{index:02d}",
        "family": "count_open",
        "answer_kind": "integer",
        "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
        "expected": {
            "base": "2",
            "relevant": "3",
            "irrelevant_plain": "2",
            "irrelevant_adversarial": "2",
        },
        "relation": {"kind": "numeric_delta", "delta": 1},
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


BUILDERS: dict[str, Callable[[int, random.Random], dict[str, Any]]] = {
    "filtered_argmin": filtered_argmin,
    "latest_confirmed": latest_confirmed,
    "valid_sum": valid_sum,
    "tier_score": tier_score,
    "count_open": count_open,
}


def generate_cases(spec: dict[str, Any]) -> list[dict[str, Any]]:
    if spec.get("schema_version") != 1:
        raise ValueError("suite spec schema_version must equal 1")
    seed = int(spec["seed"])
    per_family = int(spec["per_family"])
    families = spec.get("families")
    if per_family <= 0 or not isinstance(families, list) or not families:
        raise ValueError("suite spec needs positive per_family and non-empty families")
    rng = random.Random(seed)
    cases: list[dict[str, Any]] = []
    for family in families:
        if family not in BUILDERS:
            raise ValueError(f"unknown family: {family}")
        for index in range(per_family):
            case = BUILDERS[family](index, rng)
            order_only = copy.deepcopy(case["tool_results"]["base"])
            record_key = _top_level_record_key(order_only)
            if record_key is None:
                shared_order: list[int] = []
                order_only_order: list[int] = []
            else:
                record_count = len(order_only[record_key])
                shared_order = list(range(record_count))
                rng.shuffle(shared_order)
                if record_count > 1:
                    offset = rng.randint(1, record_count - 1)
                    order_only_order = (
                        shared_order[offset:] + shared_order[:offset]
                    )
                else:
                    order_only_order = list(shared_order)
            for tool_result in case["tool_results"].values():
                _apply_record_order(tool_result, shared_order)
            _apply_record_order(order_only, order_only_order)
            case["tool_results"]["order_only"] = order_only
            case["expected"]["order_only"] = case["expected"]["base"]
            cases.append(case)
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a deterministic uptake-relation suite.")
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    cases = generate_cases(spec)
    atomic_write_json(
        args.output,
        {
            "schema_version": 1,
            "generation": {
                "seed": int(spec["seed"]),
                "per_family": int(spec["per_family"]),
                "families": list(spec["families"]),
                "record_order": (
                    "shared_random_order_for_field_variants_plus_order_only_control"
                ),
            },
            "cases": cases,
        },
    )
    print(json.dumps({"case_count": len(cases), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
