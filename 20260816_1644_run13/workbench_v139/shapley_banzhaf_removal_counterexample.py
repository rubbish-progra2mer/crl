from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


PLAYERS = ("p1", "p2", "p3", "p4")


def coalitions(players: tuple[str, ...] = PLAYERS):
    for size in range(len(players) + 1):
        for members in itertools.combinations(players, size):
            yield frozenset(members)


def make_game(a: int, b: int, t: int) -> dict[frozenset[str], Fraction]:
    """构造单调的二元实例平均效用合作博弈。"""
    total = a + b + t
    values: dict[frozenset[str], Fraction] = {}
    for coalition in coalitions():
        success_count = 0
        if "p1" in coalition:
            success_count += a
        if "p2" in coalition:
            success_count += b
        if {"p1", "p3", "p4"}.issubset(coalition):
            success_count += t
        values[coalition] = Fraction(success_count, total)
    return values


def shapley(values: dict[frozenset[str], Fraction], player: str) -> Fraction:
    n = len(PLAYERS)
    result = Fraction(0)
    others = tuple(p for p in PLAYERS if p != player)
    for coalition in coalitions(others):
        size = len(coalition)
        weight = Fraction(math.factorial(size) * math.factorial(n - size - 1), math.factorial(n))
        result += weight * (values[coalition | {player}] - values[coalition])
    return result


def banzhaf(values: dict[frozenset[str], Fraction], player: str) -> Fraction:
    others = tuple(p for p in PLAYERS if p != player)
    marginal_sum = sum(
        (values[coalition | {player}] - values[coalition] for coalition in coalitions(others)),
        Fraction(0),
    )
    return marginal_sum / (2 ** len(others))


def all_coalition_mean(values: dict[frozenset[str], Fraction]) -> Fraction:
    return sum(values.values(), Fraction(0)) / len(values)


def mean_without(values: dict[frozenset[str], Fraction], player: str) -> Fraction:
    eligible = [value for coalition, value in values.items() if player not in coalition]
    return sum(eligible, Fraction(0)) / len(eligible)


def unique_top(scores: dict[str, Fraction]) -> str | None:
    best = max(scores.values())
    winners = [player for player, score in scores.items() if score == best]
    return winners[0] if len(winners) == 1 else None


def is_monotone(values: dict[frozenset[str], Fraction]) -> bool:
    for left, left_value in values.items():
        for right, right_value in values.items():
            if left.issubset(right) and left_value > right_value:
                return False
    return True


def fraction_record(value: Fraction) -> dict[str, object]:
    return {"fraction": str(value), "float": float(value)}


def analyze_game(a: int, b: int, t: int) -> dict[str, object]:
    values = make_game(a, b, t)
    shapley_scores = {player: shapley(values, player) for player in PLAYERS}
    banzhaf_scores = {player: banzhaf(values, player) for player in PLAYERS}
    global_mean = all_coalition_mean(values)
    residual_means = {player: mean_without(values, player) for player in PLAYERS}
    removal_drops = {player: global_mean - residual_means[player] for player in PLAYERS}
    identity_holds = {
        player: removal_drops[player] == banzhaf_scores[player] / 2 for player in PLAYERS
    }
    return {
        "parameters": {"a": a, "b": b, "t": t, "binary_instances": a + b + t},
        "monotone": is_monotone(values),
        "bounded_unit_interval": all(Fraction(0) <= value <= Fraction(1) for value in values.values()),
        "shapley": {player: fraction_record(value) for player, value in shapley_scores.items()},
        "banzhaf": {player: fraction_record(value) for player, value in banzhaf_scores.items()},
        "global_coalition_mean": fraction_record(global_mean),
        "mean_after_removal": {
            player: fraction_record(value) for player, value in residual_means.items()
        },
        "removal_drop": {player: fraction_record(value) for player, value in removal_drops.items()},
        "identity_holds": identity_holds,
        "shapley_unique_top": unique_top(shapley_scores),
        "banzhaf_unique_top": unique_top(banzhaf_scores),
        "removal_drop_unique_top": unique_top(removal_drops),
        "coalitions": [
            {
                "members": sorted(coalition),
                "success_count": int(value * (a + b + t)),
                "utility": fraction_record(value),
            }
            for coalition, value in sorted(values.items(), key=lambda item: (len(item[0]), sorted(item[0])))
        ],
    }


def grid_audit(limit: int) -> dict[str, object]:
    reversal_count = 0
    identity_violation_count = 0
    monotonicity_violation_count = 0
    first_reversal: dict[str, int] | None = None
    total_games = 0
    for a in range(1, limit + 1):
        for b in range(1, limit + 1):
            for t in range(1, limit + 1):
                total_games += 1
                values = make_game(a, b, t)
                if not is_monotone(values):
                    monotonicity_violation_count += 1
                shapley_scores = {player: shapley(values, player) for player in PLAYERS}
                banzhaf_scores = {player: banzhaf(values, player) for player in PLAYERS}
                global_mean = all_coalition_mean(values)
                drops = {player: global_mean - mean_without(values, player) for player in PLAYERS}
                if any(drops[player] != banzhaf_scores[player] / 2 for player in PLAYERS):
                    identity_violation_count += 1
                if unique_top(shapley_scores) == "p1" and unique_top(banzhaf_scores) == "p2":
                    reversal_count += 1
                    if first_reversal is None:
                        first_reversal = {"a": a, "b": b, "t": t}
    return {
        "limit": limit,
        "total_games": total_games,
        "reversal_count": reversal_count,
        "first_reversal": first_reversal,
        "identity_violation_count": identity_violation_count,
        "monotonicity_violation_count": monotonicity_violation_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--grid-limit", type=int, default=32)
    args = parser.parse_args()

    example = analyze_game(a=1, b=8, t=24)
    grid = grid_audit(args.grid_limit)
    assertions = {
        "example_monotone_and_bounded": bool(example["monotone"] and example["bounded_unit_interval"]),
        "shapley_unique_top_is_p1": example["shapley_unique_top"] == "p1",
        "banzhaf_unique_top_is_p2": example["banzhaf_unique_top"] == "p2",
        "removal_drop_unique_top_is_p2": example["removal_drop_unique_top"] == "p2",
        "example_identity_all_players": all(example["identity_holds"].values()),
        "grid_contains_reversal": grid["reversal_count"] > 0,
        "grid_identity_zero_violations": grid["identity_violation_count"] == 0,
        "grid_monotonicity_zero_violations": grid["monotonicity_violation_count"] == 0,
    }
    payload = {
        "experiment": "skillshapley-removal-target-counterexample",
        "example": example,
        "grid_audit": grid,
        "assertions": assertions,
        "all_assertions_passed": all(assertions.values()),
        "interpretation_boundary": (
            "仅检验单步均匀联盟删除目标与班扎夫值的代数对齐及其与沙普利排序的可分离性；"
            "不评价真实 SkillsBench 排序，也不评价 BAES 的沙普利近似精度。"
        ),
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    if not payload["all_assertions_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
