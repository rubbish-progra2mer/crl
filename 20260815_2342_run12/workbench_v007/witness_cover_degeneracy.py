#!/usr/bin/env python3
"""Mechanical degeneracy scan for h-009.

This is a Run-local exploratory pilot, not a CRL Formal attempt.  It asks a
narrow question before any model calls: when verifier observability varies,
does a semantic witness-cover constraint select a non-trivial set, and does an
ordinary uncovered-mass greedy already recover the same certificate?
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Witness:
    name: str
    covers: frozenset[int]
    cost: int
    position: str


@dataclass(frozen=True)
class Task:
    task_id: str
    domain: str
    predicate_count: int
    risk: tuple[float, ...]
    witnesses: tuple[Witness, ...]

    @property
    def universe(self) -> frozenset[int]:
        return frozenset(range(self.predicate_count))


def union_coverage(witnesses: Iterable[Witness]) -> frozenset[int]:
    covered: set[int] = set()
    for witness in witnesses:
        covered.update(witness.covers)
    return frozenset(covered)


def total_cost(witnesses: Iterable[Witness]) -> int:
    return sum(witness.cost for witness in witnesses)


def exact_min_cover(task: Task) -> tuple[Witness, ...]:
    best: tuple[Witness, ...] | None = None
    best_key: tuple[int, int, tuple[str, ...]] | None = None
    for size in range(1, len(task.witnesses) + 1):
        for subset in itertools.combinations(task.witnesses, size):
            if union_coverage(subset) != task.universe:
                continue
            key = (total_cost(subset), len(subset), tuple(sorted(w.name for w in subset)))
            if best_key is None or key < best_key:
                best = subset
                best_key = key
    if best is None:
        raise RuntimeError(f"no cover for {task.task_id}")
    return best


def fit_by_order(order: list[Witness], budget: int) -> tuple[Witness, ...]:
    selected: list[Witness] = []
    spent = 0
    for witness in order:
        if spent + witness.cost <= budget:
            selected.append(witness)
            spent += witness.cost
    return tuple(selected)


def greedy_uncovered(task: Task, budget: int) -> tuple[Witness, ...]:
    selected: list[Witness] = []
    covered: set[int] = set()
    remaining = list(task.witnesses)
    spent = 0
    while remaining:
        affordable = [w for w in remaining if spent + w.cost <= budget]
        if not affordable:
            break
        best = max(
            affordable,
            key=lambda w: (
                sum(task.risk[i] for i in w.covers if i not in covered) / w.cost,
                len(w.covers - covered),
                -w.cost,
                w.name,
            ),
        )
        if not (best.covers - covered):
            break
        selected.append(best)
        covered.update(best.covers)
        spent += best.cost
        remaining.remove(best)
        if covered == set(task.universe):
            break
    return tuple(selected)


def risk_top(task: Task, budget: int) -> tuple[Witness, ...]:
    order = sorted(
        task.witnesses,
        key=lambda w: (
            sum(task.risk[i] for i in w.covers) / w.cost,
            len(w.covers),
            -w.cost,
            w.name,
        ),
        reverse=True,
    )
    return fit_by_order(order, budget)


def terminal_first(task: Task, budget: int) -> tuple[Witness, ...]:
    rank = {"terminal": 0, "initial": 1, "intermediate": 2}
    order = sorted(
        task.witnesses,
        key=lambda w: (
            rank[w.position],
            -sum(task.risk[i] for i in w.covers),
            w.cost,
            w.name,
        ),
    )
    return fit_by_order(order, budget)


def random_fit(task: Task, budget: int, seed: int) -> tuple[Witness, ...]:
    order = list(task.witnesses)
    random.Random(seed).shuffle(order)
    return fit_by_order(order, budget)


def make_task(
    rng: random.Random,
    domain: str,
    task_index: int,
    terminal_fraction: float,
) -> Task:
    n = rng.randint(3, 6)
    risk = tuple(round(rng.uniform(0.2, 1.0), 4) for _ in range(n))
    terminal_count = min(n, max(0, math.ceil(terminal_fraction * n)))
    terminal_cover = frozenset(rng.sample(range(n), terminal_count))
    witnesses: list[Witness] = [
        Witness("terminal_status", terminal_cover, 1, "terminal")
    ]

    # Every effect predicate is independently observable, so a complete cover
    # always exists.  Group witnesses model read APIs that expose several
    # related fields at once without being complete final-state oracles.
    for predicate in range(n):
        witnesses.append(
            Witness(f"initial_read_{predicate}", frozenset({predicate}), 1, "initial")
        )
    for group_index in range(n + 1):
        size = rng.randint(2, min(4, n))
        group = frozenset(rng.sample(range(n), size))
        witnesses.append(
            Witness(
                f"group_read_{group_index}",
                group,
                1 if size <= 3 else 2,
                "intermediate",
            )
        )
    return Task(
        task_id=f"{domain}-{task_index:04d}",
        domain=domain,
        predicate_count=n,
        risk=risk,
        witnesses=tuple(witnesses),
    )


def evaluate_selection(task: Task, selected: tuple[Witness, ...]) -> dict[str, float | int | bool]:
    covered = union_coverage(selected)
    missing = task.universe - covered
    total_risk = sum(task.risk)
    missing_risk = sum(task.risk[i] for i in missing)
    # An assertive policy proceeds after all selected witnesses pass. A single
    # silent no-op is injected uniformly over effect predicates.
    unsafe_uniform = len(missing) / task.predicate_count
    unsafe_risk_weighted = missing_risk / total_risk
    return {
        "certificate": not missing,
        "selected_count": len(selected),
        "cost": total_cost(selected),
        "missing_count": len(missing),
        "unsafe_uniform": unsafe_uniform,
        "unsafe_risk_weighted": unsafe_risk_weighted,
        # Conservative variants block clean tasks whenever no certificate can
        # be formed; this is the utility price of a poor selection order.
        "clean_false_block_if_conservative": bool(missing),
    }


def run_scan(tasks_per_cell: int, seed: int) -> dict[str, object]:
    domains = ("access", "payment", "deployment")
    fractions = (0.0, 0.25, 0.5, 0.75, 1.0)
    rows: list[dict[str, object]] = []
    aggregates: dict[tuple[float, str], dict[str, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    rng = random.Random(seed)

    for terminal_fraction in fractions:
        for domain in domains:
            for task_index in range(tasks_per_cell):
                task = make_task(rng, domain, task_index, terminal_fraction)
                exact = exact_min_cover(task)
                budget = total_cost(exact)
                strategies = {
                    "exact_cover": exact,
                    "greedy_uncovered": greedy_uncovered(task, budget),
                    "risk_top": risk_top(task, budget),
                    "terminal_first": terminal_first(task, budget),
                    "random": random_fit(task, budget, seed + task_index),
                }
                for strategy, selected in strategies.items():
                    metrics = evaluate_selection(task, selected)
                    row = {
                        "terminal_fraction": terminal_fraction,
                        "domain": domain,
                        "task_id": task.task_id,
                        "predicate_count": task.predicate_count,
                        "budget": budget,
                        "strategy": strategy,
                        "selected": [w.name for w in selected],
                        **metrics,
                    }
                    rows.append(row)
                    agg = aggregates[(terminal_fraction, strategy)]
                    agg["n"] += 1
                    for key in (
                        "certificate",
                        "cost",
                        "unsafe_uniform",
                        "unsafe_risk_weighted",
                        "clean_false_block_if_conservative",
                    ):
                        agg[key] += float(metrics[key])

    summary_rows: list[dict[str, object]] = []
    for (terminal_fraction, strategy), agg in sorted(aggregates.items()):
        n = agg["n"]
        summary_rows.append(
            {
                "terminal_fraction": terminal_fraction,
                "strategy": strategy,
                "tasks": int(n),
                "certificate_rate": agg["certificate"] / n,
                "mean_cost": agg["cost"] / n,
                "assertive_unsafe_uniform": agg["unsafe_uniform"] / n,
                "assertive_unsafe_risk_weighted": agg["unsafe_risk_weighted"] / n,
                "conservative_clean_false_block": agg[
                    "clean_false_block_if_conservative"
                ]
                / n,
            }
        )

    exact_rows = [row for row in rows if row["strategy"] == "exact_cover"]
    terminal_only = sum(
        1 for row in exact_rows if row["selected"] == ["terminal_status"]
    )
    return {
        "schema_version": 1,
        "seed": seed,
        "tasks_per_domain_fraction_cell": tasks_per_cell,
        "task_count": len(exact_rows),
        "terminal_only_exact_rate": terminal_only / len(exact_rows),
        "summary": summary_rows,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks-per-cell", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260816)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_scan(args.tasks_per_cell, args.seed)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    for row in result["summary"]:
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))
    print(
        json.dumps(
            {
                "task_count": result["task_count"],
                "terminal_only_exact_rate": result["terminal_only_exact_rate"],
                "output": str(args.output),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
