from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def powerset(items: tuple[str, ...]):
    for size in range(len(items) + 1):
        yield from (frozenset(combo) for combo in combinations(items, size))


def construction(m: int):
    edges = ("bundle",) + tuple(f"shard_{i}" for i in range(m))
    epsilon = Fraction(1, m * m)
    total = Fraction(m, 1) + m * epsilon

    def covered(edge_set: frozenset[str]) -> Fraction:
        core = set()
        extras = set()
        if "bundle" in edge_set:
            core.update(range(m))
        for i in range(m):
            if f"shard_{i}" in edge_set:
                core.add(i)
                extras.add(i)
        return (Fraction(len(core), 1) + epsilon * len(extras)) / total

    return edges, epsilon, covered


def rational(value: Fraction) -> dict[str, object]:
    return {
        "fraction": f"{value.numerator}/{value.denominator}",
        "float": float(value),
    }


def exact_optimum(edges: tuple[str, ...], utility, budget: int):
    best_set = None
    best_value = Fraction(-1, 1)
    for combo in combinations(edges, budget):
        candidate = frozenset(combo)
        value = utility(candidate)
        if value > best_value:
            best_set = candidate
            best_value = value
    assert best_set is not None
    return best_set, best_value


def conditional_greedy(edges: tuple[str, ...], utility, budget: int):
    chosen = frozenset()
    for _ in range(budget):
        remaining = [edge for edge in edges if edge not in chosen]
        edge = max(
            remaining,
            key=lambda item: (utility(chosen | {item}) - utility(chosen), item),
        )
        chosen = chosen | {edge}
    return chosen, utility(chosen)


def verify_submodularity(m: int) -> dict[str, int]:
    edges, _, utility = construction(m)
    subsets = list(powerset(edges))
    monotonicity_violations = 0
    submodularity_violations = 0
    for left in subsets:
        for right in subsets:
            if left <= right and utility(left) > utility(right):
                monotonicity_violations += 1
            if left <= right:
                for edge in edges:
                    if edge in right:
                        continue
                    marginal_left = utility(left | {edge}) - utility(left)
                    marginal_right = utility(right | {edge}) - utility(right)
                    if marginal_left < marginal_right:
                        submodularity_violations += 1
    return {
        "monotonicity_violations": monotonicity_violations,
        "submodularity_violations": submodularity_violations,
    }


def run(output: Path) -> None:
    scales = (4, 8, 16, 32, 64)
    records = []
    all_assertions = []

    structural = verify_submodularity(6)
    all_assertions.append(structural["monotonicity_violations"] == 0)
    all_assertions.append(structural["submodularity_violations"] == 0)

    for m in scales:
        edges, epsilon, utility = construction(m)
        full = frozenset(edges)
        full_value = utility(full)
        loo = {
            edge: full_value - utility(full - {edge})
            for edge in edges
        }
        all_assertions.append(loo["bundle"] == 0)
        all_assertions.append(all(loo[f"shard_{i}"] > 0 for i in range(m)))

        order = sorted(edges, key=lambda edge: (loo[edge], edge), reverse=True)
        for k in range(1, m):
            selected = frozenset(order[:k])
            selected_value = utility(selected)

            if m <= 16:
                optimum_set, optimum_value = exact_optimum(edges, utility, k)
                optimum_method = "enumeration"
            else:
                optimum_set = frozenset({"bundle"} | {f"shard_{i}" for i in range(k - 1)})
                optimum_value = utility(optimum_set)
                optimum_method = "closed_form"

            greedy_set, greedy_value = conditional_greedy(edges, utility, k)
            expected_selected = Fraction(k, m)
            approximation_ratio = selected_value / optimum_value

            checks = {
                "selected_excludes_bundle": "bundle" not in selected,
                "selected_value_is_k_over_m": selected_value == expected_selected,
                "optimum_contains_bundle": "bundle" in optimum_set,
                "optimum_strictly_better": optimum_value > selected_value,
                "conditional_greedy_is_optimal": greedy_value == optimum_value,
                "k1_ratio_matches_formula": k != 1
                or approximation_ratio == Fraction(m * m + 1, m * m * m),
            }
            all_assertions.extend(checks.values())
            records.append(
                {
                    "m": m,
                    "k": k,
                    "epsilon": rational(epsilon),
                    "full_graph_bundle_effect": rational(loo["bundle"]),
                    "full_graph_shard_effect": rational(loo["shard_0"]),
                    "selected": sorted(selected),
                    "selected_value": rational(selected_value),
                    "optimum": sorted(optimum_set),
                    "optimum_value": rational(optimum_value),
                    "optimum_method": optimum_method,
                    "conditional_greedy": sorted(greedy_set),
                    "conditional_greedy_value": rational(greedy_value),
                    "approximation_ratio": rational(approximation_ratio),
                    "checks": checks,
                }
            )

    m64_k1 = next(row for row in records if row["m"] == 64 and row["k"] == 1)
    all_assertions.append(
        m64_k1["approximation_ratio"]["fraction"] == "4097/262144"
    )
    assert all(all_assertions)

    payload = {
        "schema_version": 1,
        "experiment": "e2_full_graph_marginal_counterexample",
        "structural_checks_m6": structural,
        "scales": list(scales),
        "record_count": len(records),
        "all_assertions_passed": True,
        "m64_k1": m64_k1,
        "records": records,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output)


if __name__ == "__main__":
    main()
