#!/usr/bin/env python3
"""Audit whether public Replay Gap forks yield enough outcome labels for router training."""

from __future__ import annotations

import argparse
import gzip
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return (math.nan, math.nan)
    proportion = successes / total
    denominator = 1.0 + z * z / total
    center = (proportion + z * z / (2.0 * total)) / denominator
    radius = z * math.sqrt(
        proportion * (1.0 - proportion) / total + z * z / (4.0 * total * total)
    ) / denominator
    return center - radius, center + radius


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with gzip.open(args.index, "rt", encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream]

    bases = {
        (row["run"], row["instance_id"]): row
        for row in rows
        if row["arm"] == "base"
    }
    grouped: dict[tuple[str, str, int], dict[str, dict]] = defaultdict(dict)
    for row in rows:
        if row["arm"] != "branch":
            continue
        grouped[(row["run"], row["instance_id"], row["fork_step"])][
            row["model_alias"]
        ] = row

    complete = {
        key: arms for key, arms in grouped.items() if {"small", "large"}.issubset(arms)
    }
    cross_outcomes = Counter()
    per_run = Counter()
    same_model_control_flips = []
    missing_base = []

    for (run, instance_id, fork_step), arms in complete.items():
        small_resolved = bool(arms["small"]["resolved"])
        large_resolved = bool(arms["large"]["resolved"])
        if large_resolved and not small_resolved:
            label = "large_only"
        elif small_resolved and not large_resolved:
            label = "small_only"
        elif large_resolved and small_resolved:
            label = "both_resolve"
        else:
            label = "neither_resolves"
        cross_outcomes[label] += 1
        per_run[(run, label)] += 1

        base = bases.get((run, instance_id))
        if base is None:
            missing_base.append((run, instance_id, fork_step))
            continue
        control_alias = "small" if arms["small"]["direction"] == "up" else "large"
        if bool(arms[control_alias]["resolved"]) != bool(base["resolved"]):
            same_model_control_flips.append(
                {
                    "run": run,
                    "instance_id": instance_id,
                    "fork_step": fork_step,
                    "control_alias": control_alias,
                    "base_resolved": bool(base["resolved"]),
                    "control_resolved": bool(arms[control_alias]["resolved"]),
                }
            )

    informative = cross_outcomes["large_only"] + cross_outcomes["small_only"]
    lower, upper = wilson_interval(informative, len(complete))
    expected_flips_in_20pct_test = informative * 0.2

    result = {
        "source_rows": len(rows),
        "base_rows": sum(row["arm"] == "base" for row in rows),
        "branch_rows": sum(row["arm"] == "branch" for row in rows),
        "complete_same_state_small_large_pairs": len(complete),
        "cross_model_outcomes": dict(sorted(cross_outcomes.items())),
        "informative_success_treatment_pairs": informative,
        "informative_rate": informative / len(complete) if complete else None,
        "informative_rate_wilson_95": [lower, upper],
        "expected_informative_pairs_in_random_20pct_test": expected_flips_in_20pct_test,
        "same_model_control_outcome_flips": same_model_control_flips,
        "missing_base_count": len(missing_base),
        "per_run_outcomes": {
            run: {
                label: per_run[(run, label)]
                for label in ("large_only", "small_only", "both_resolve", "neither_resolves")
            }
            for run in sorted({key[0] for key in complete})
        },
        "interpretation_boundary": (
            "This audit measures label density only. It does not train or evaluate a router, "
            "and it does not show that richer process rewards would be equally sparse."
        ),
    }

    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
