from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np


SEEDS = (42, 123, 456)
DEVELOPMENT_FIXED_REFERENCE = {
    "fk_1": 0.600,
    "fk_3": 0.7833333333333333,
    "fk_5": 0.825,
    "fk_10": 0.850,
    "fk_20": 0.875,
    "fk_50": 0.9083333333333333,
}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def group_key(row: dict[str, Any]) -> tuple[str, int | None]:
    return str(row["policy"]), row["seed"]


def direct_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    hits = np.array([int(row["hit"]) for row in rows], dtype=np.float64)
    k = np.array([int(row["k"]) for row in rows], dtype=np.float64)
    n = np.array([int(row["n"]) for row in rows], dtype=np.float64)
    chance = k / n
    direct_rewards = hits * -np.log2(chance)
    observed = float(hits.mean())
    random_baseline = float(chance.mean())
    defined = math.log2(observed / random_baseline) if observed > 0 else None
    return {
        "query_count": len(rows),
        "found_fraction": observed,
        "mean_k": float(k.mean()),
        "std_k": float(k.std()),
        "notebook_statistic": float(direct_rewards.mean()),
        "defined_bor": defined,
        "mean_random_baseline": random_baseline,
        "max_stored_reward_error": float(
            np.max(
                np.abs(
                    direct_rewards
                    - np.array(
                        [float(row["target_reward"]) for row in rows],
                        dtype=np.float64,
                    )
                )
            )
        ),
        "max_stored_chance_error": float(
            np.max(
                np.abs(
                    chance
                    - np.array(
                        [float(row["chance_probability"]) for row in rows],
                        dtype=np.float64,
                    )
                )
            )
        ),
    }


def load_official_metric(source_root: Path):
    sys.path.insert(0, str(source_root))
    try:
        from bor.metrics import bits_over_random
    finally:
        sys.path.pop(0)
    return bits_over_random


def sign(value: float, tolerance: float = 1e-12) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def pairwise(
    metrics: dict[tuple[str, int | None], dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fixed = {
        policy: values
        for (policy, seed), values in metrics.items()
        if seed is None
    }
    reversals: list[dict[str, Any]] = []
    maxima: list[dict[str, Any]] = []
    for seed in SEEDS:
        policies = dict(fixed)
        policies.update(
            {
                policy: values
                for (policy, item_seed), values in metrics.items()
                if item_seed == seed
            }
        )
        names = sorted(policies)
        for left_index, left in enumerate(names):
            for right in names[left_index + 1 :]:
                notebook_delta = (
                    policies[left]["notebook_statistic"]
                    - policies[right]["notebook_statistic"]
                )
                defined_delta = (
                    policies[left]["defined_bor"]
                    - policies[right]["defined_bor"]
                )
                if (
                    sign(notebook_delta) != 0
                    and sign(defined_delta) != 0
                    and sign(notebook_delta) == -sign(defined_delta)
                ):
                    reversals.append(
                        {
                            "seed": seed,
                            "left": left,
                            "right": right,
                            "notebook_delta_left_minus_right": notebook_delta,
                            "defined_delta_left_minus_right": defined_delta,
                            "involves_learned_policy": left in {"bor_dqn", "f1_dqn"}
                            or right in {"bor_dqn", "f1_dqn"},
                        }
                    )
        notebook_winner = max(
            names, key=lambda name: (policies[name]["notebook_statistic"], name)
        )
        defined_winner = max(
            names, key=lambda name: (policies[name]["defined_bor"], name)
        )
        maxima.append(
            {
                "seed": seed,
                "notebook_winner": notebook_winner,
                "defined_bor_winner": defined_winner,
                "different": notebook_winner != defined_winner,
            }
        )
    return reversals, maxima


def aggregate_sample(rows: list[dict[str, Any]], indices: np.ndarray) -> tuple[float, float]:
    hits = np.array([int(rows[index]["hit"]) for index in indices], dtype=np.float64)
    chance = np.array(
        [int(rows[index]["k"]) / int(rows[index]["n"]) for index in indices],
        dtype=np.float64,
    )
    notebook = float(np.mean(hits * -np.log2(chance)))
    defined = math.log2(float(hits.mean()) / float(chance.mean()))
    return notebook, defined


def bootstrap(
    rows: list[dict[str, Any]], resamples: int, bootstrap_seed: int
) -> dict[str, Any]:
    by_policy: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        if row["seed"] is None and row["policy"] in {"fk_1", "fk_3"}:
            by_policy[row["policy"]][row["query_id"]] = row
    query_ids = sorted(set(by_policy["fk_1"]) & set(by_policy["fk_3"]))
    left = [by_policy["fk_3"][query_id] for query_id in query_ids]
    right = [by_policy["fk_1"][query_id] for query_id in query_ids]
    generator = np.random.default_rng(bootstrap_seed)
    notebook_delta = np.empty(resamples, dtype=np.float64)
    defined_delta = np.empty(resamples, dtype=np.float64)
    for resample_index in range(resamples):
        indices = generator.integers(0, len(query_ids), size=len(query_ids))
        left_notebook, left_defined = aggregate_sample(left, indices)
        right_notebook, right_defined = aggregate_sample(right, indices)
        notebook_delta[resample_index] = left_notebook - right_notebook
        defined_delta[resample_index] = left_defined - right_defined
    return {
        "query_count": len(query_ids),
        "resamples": resamples,
        "seed": bootstrap_seed,
        "notebook_probability_positive": float(np.mean(notebook_delta > 0)),
        "notebook_probability_negative": float(np.mean(notebook_delta < 0)),
        "defined_probability_positive": float(np.mean(defined_delta > 0)),
        "defined_probability_negative": float(np.mean(defined_delta < 0)),
        "notebook_ci95": [
            float(np.quantile(notebook_delta, 0.025)),
            float(np.quantile(notebook_delta, 0.975)),
        ],
        "defined_ci95": [
            float(np.quantile(defined_delta, 0.025)),
            float(np.quantile(defined_delta, 0.975)),
        ],
    }


def audit(arguments: argparse.Namespace) -> dict[str, Any]:
    rows = load_rows(arguments.rows)
    stored_summary = json.loads(arguments.summary.read_text(encoding="utf-8"))
    phase = stored_summary["phase"]
    grouped_rows: dict[tuple[str, int | None], list[dict[str, Any]]] = defaultdict(list)
    row_errors: list[str] = []
    for row in rows:
        if not (1 <= int(row["k"]) <= int(row["n"])):
            row_errors.append(f"invalid depth: {row['query_id']} {group_key(row)}")
        if bool(row["hit"]) != (int(row["gold_rank"]) <= int(row["k"])):
            row_errors.append(f"hit mismatch: {row['query_id']} {group_key(row)}")
        grouped_rows[group_key(row)].append(row)

    expected_queries = int(stored_summary["query_count"])
    count_errors: list[str] = []
    for key, group in grouped_rows.items():
        query_ids = [str(row["query_id"]) for row in group]
        if len(group) != expected_queries or len(set(query_ids)) != expected_queries:
            count_errors.append(f"{key}: rows={len(group)} unique={len(set(query_ids))}")

    official_bits = load_official_metric(arguments.official_bor_src)
    metrics: dict[tuple[str, int | None], dict[str, Any]] = {}
    max_official_error = 0.0
    max_summary_error = 0.0
    stored_groups = {
        (item["policy"], item["seed"]): item
        for item in stored_summary["group_summaries"]
    }
    for key, group in grouped_rows.items():
        values = direct_metrics(group)
        official = official_bits(
            observed=values["found_fraction"],
            random_baseline=values["mean_random_baseline"],
        )
        max_official_error = max(
            max_official_error, abs(values["defined_bor"] - official)
        )
        stored = stored_groups[key]
        for field in (
            "found_fraction",
            "mean_k",
            "std_k",
            "notebook_statistic",
            "defined_bor",
            "mean_random_baseline",
        ):
            max_summary_error = max(
                max_summary_error, abs(float(values[field]) - float(stored[field]))
            )
        metrics[key] = values

    reversals, maxima = pairwise(metrics)
    bootstrap_result = bootstrap(
        rows, arguments.bootstrap_resamples, arguments.bootstrap_seed
    )
    learned_reversal_seeds = sorted(
        {
            item["seed"]
            for item in reversals
            if item["involves_learned_policy"]
        }
    )
    fk_notebook_delta = (
        metrics[("fk_3", None)]["notebook_statistic"]
        - metrics[("fk_1", None)]["notebook_statistic"]
    )
    fk_defined_delta = (
        metrics[("fk_3", None)]["defined_bor"]
        - metrics[("fk_1", None)]["defined_bor"]
    )

    reproduction: dict[str, Any] | None = None
    reproduction_ok = True
    if phase == "development":
        reproduction = {"learned": {}, "fixed": {}}
        for policy, target_k, target_found in (
            ("bor_dqn", 7.4, 0.903),
            ("f1_dqn", 6.4, 0.889),
        ):
            policy_metrics = [
                metrics[(policy, seed)]
                for seed in SEEDS
            ]
            observed_k = float(np.mean([item["mean_k"] for item in policy_metrics]))
            observed_found = float(
                np.mean([item["found_fraction"] for item in policy_metrics])
            )
            reproduction["learned"][policy] = {
                "observed_mean_k": observed_k,
                "absolute_k_delta": abs(observed_k - target_k),
                "observed_found_fraction": observed_found,
                "absolute_found_delta": abs(observed_found - target_found),
            }
            reproduction_ok = reproduction_ok and abs(observed_k - target_k) <= 1.0
            reproduction_ok = (
                reproduction_ok and abs(observed_found - target_found) <= 0.03
            )
        for policy, target_found in DEVELOPMENT_FIXED_REFERENCE.items():
            observed = metrics[(policy, None)]["found_fraction"]
            delta = abs(observed - target_found)
            reproduction["fixed"][policy] = {
                "observed_found_fraction": observed,
                "absolute_found_delta": delta,
            }
            reproduction_ok = reproduction_ok and delta <= 0.01

    max_reward_error = max(
        values["max_stored_reward_error"] for values in metrics.values()
    )
    max_chance_error = max(
        values["max_stored_chance_error"] for values in metrics.values()
    )
    mechanical_checks = {
        "row_integrity": not row_errors and not count_errors,
        "stored_reward_identity_le_1e_12": max_reward_error <= 1e-12,
        "official_defined_identity_le_1e_12": max_official_error <= 1e-12,
        "stored_summary_identity_le_1e_12": max_summary_error <= 1e-12,
        "development_reproduction_within_tolerance": reproduction_ok
        if phase == "development"
        else None,
        "fk3_vs_fk1_strict_reversal": sign(fk_notebook_delta)
        == -sign(fk_defined_delta)
        and sign(fk_notebook_delta) != 0,
        "learned_reversal_in_at_least_two_seeds": len(learned_reversal_seeds) >= 2,
        "different_maximizer_in_at_least_one_seed": any(
            item["different"] for item in maxima
        ),
        "fk_bootstrap_notebook_positive_support": bootstrap_result[
            "notebook_probability_positive"
        ],
        "fk_bootstrap_defined_negative_support": bootstrap_result[
            "defined_probability_negative"
        ],
    }
    return {
        "schema_version": 1,
        "phase": phase,
        "rows_path": str(arguments.rows.resolve()),
        "rows_sha256": sha256_path(arguments.rows),
        "summary_path": str(arguments.summary.resolve()),
        "summary_sha256": sha256_path(arguments.summary),
        "official_bor_source": str(arguments.official_bor_src.resolve()),
        "row_count": len(rows),
        "group_row_counts": {
            f"{policy}:{seed}": count
            for (policy, seed), count in sorted(
                Counter(group_key(row) for row in rows).items(),
                key=lambda item: (
                    item[0][0],
                    -1 if item[0][1] is None else item[0][1],
                ),
            )
        },
        "row_errors": row_errors,
        "count_errors": count_errors,
        "max_stored_reward_error": max_reward_error,
        "max_stored_chance_error": max_chance_error,
        "max_official_defined_bor_error": max_official_error,
        "max_stored_summary_error": max_summary_error,
        "group_metrics": [
            {"policy": policy, "seed": seed, **values}
            for (policy, seed), values in sorted(
                metrics.items(),
                key=lambda item: (
                    item[0][0],
                    -1 if item[0][1] is None else item[0][1],
                ),
            )
        ],
        "strict_pairwise_reversals": reversals,
        "learned_reversal_seeds": learned_reversal_seeds,
        "per_seed_maxima": maxima,
        "fk3_minus_fk1": {
            "notebook_delta": fk_notebook_delta,
            "defined_delta": fk_defined_delta,
        },
        "bootstrap": bootstrap_result,
        "development_reproduction": reproduction,
        "mechanical_checks": mechanical_checks,
        "adjudication_note": (
            "Mechanical checks do not authorize Confirmation, Review, or Delivery; "
            "the main Codex must inspect the raw evidence and decide."
        ),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--official-bor-src", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-resamples", type=int, default=20_000)
    parser.add_argument("--bootstrap-seed", type=int, default=20_260_723)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    report = audit(arguments)
    arguments.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "phase": report["phase"],
                "row_count": report["row_count"],
                "reversal_count": len(report["strict_pairwise_reversals"]),
                "max_stored_reward_error": report["max_stored_reward_error"],
                "max_official_defined_bor_error": report[
                    "max_official_defined_bor_error"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
