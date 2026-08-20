from __future__ import annotations

import argparse
import json
import platform
import sys
from collections import defaultdict
from pathlib import Path
from random import Random
from time import perf_counter

from dqbp_core import EpisodeResult, run_episode, sample_branch
from statefault_bench import build_domains, validate_domains


METHODS = (
    "no_verification",
    "static_contract",
    "fixed_readback",
    "state_information_gain",
    "dqbp",
    "full_readback",
    "oracle",
)
CONDITIONS = ("in_distribution", "failure_heavy", "success_heavy")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes-per-domain", type=int, default=5000)
    parser.add_argument("--budget", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260813)
    parser.add_argument("--metrics-output", type=Path)
    parser.add_argument("--details-output", type=Path)
    return parser.parse_args()


def _summarize(results: list[EpisodeResult]) -> dict[str, float]:
    n = len(results)
    if n == 0:
        raise ValueError("cannot summarize empty results")
    return {
        "success_rate": sum(item.success for item in results) / n,
        "harmful_error_rate": sum(item.harmful_error for item in results) / n,
        "abstain_rate": sum(item.abstained for item in results) / n,
        "average_probe_cost": sum(item.probe_cost for item in results) / n,
        "average_probe_count": sum(len(item.probes) for item in results) / n,
    }


def main() -> int:
    args = parse_args()
    if args.episodes_per_domain <= 0:
        raise ValueError("episodes-per-domain must be positive")
    if args.budget < 0:
        raise ValueError("budget must be non-negative")

    started = perf_counter()
    domains = build_domains()
    validate_domains(domains)
    rng = Random(args.seed)
    grouped: dict[tuple[str, str, str], list[EpisodeResult]] = defaultdict(list)
    trace_counts: dict[tuple[str, str, str, tuple[str, ...]], int] = defaultdict(int)

    for condition in CONDITIONS:
        for domain in domains:
            for _ in range(args.episodes_per_domain):
                true_branch = sample_branch(domain, rng, condition=condition)
                for method in METHODS:
                    result = run_episode(
                        domain,
                        true_branch,
                        method=method,
                        budget=args.budget,
                        rng=rng,
                    )
                    grouped[(condition, domain.name, method)].append(result)
                    trace_counts[
                        (condition, domain.name, method, result.probes)
                    ] += 1

    summaries = {
        f"{condition}/{domain.name}/{method}": _summarize(
            grouped[(condition, domain.name, method)]
        )
        for condition in CONDITIONS
        for domain in domains
        for method in METHODS
    }

    pooled: dict[tuple[str, str], list[EpisodeResult]] = defaultdict(list)
    for (condition, _domain_name, method), values in grouped.items():
        pooled[(condition, method)].extend(values)
    pooled_summaries = {
        f"{condition}/{method}": _summarize(pooled[(condition, method)])
        for condition in CONDITIONS
        for method in METHODS
    }

    in_dist_dqbp = pooled_summaries["in_distribution/dqbp"]
    matched_baselines = (
        "no_verification",
        "static_contract",
        "fixed_readback",
        "state_information_gain",
    )
    best_baseline_success = max(
        pooled_summaries[f"in_distribution/{method}"]["success_rate"]
        for method in matched_baselines
    )
    primary_value = in_dist_dqbp["success_rate"] - best_baseline_success
    elapsed = perf_counter() - started

    details = {
        "schema_version": 1,
        "seed": args.seed,
        "episodes_per_domain": args.episodes_per_domain,
        "budget": args.budget,
        "conditions": list(CONDITIONS),
        "methods": list(METHODS),
        "domain_count": len(domains),
        "summaries": summaries,
        "pooled_summaries": pooled_summaries,
        "primary": {
            "name": "dqbp_success_advantage_over_best_budget_matched_baseline",
            "value": primary_value,
            "best_baseline_success": best_baseline_success,
            "dqbp_success": in_dist_dqbp["success_rate"],
        },
        "trace_counts": [
            {
                "condition": condition,
                "domain": domain,
                "method": method,
                "probes": list(probes),
                "count": count,
            }
            for (condition, domain, method, probes), count in sorted(
                trace_counts.items()
            )
        ],
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "wall_time_seconds": elapsed,
        },
    }

    if args.details_output:
        args.details_output.parent.mkdir(parents=True, exist_ok=True)
        args.details_output.write_text(
            json.dumps(details, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    total_n = args.episodes_per_domain * len(domains)
    metrics = {
        "schema_version": 1,
        "experiment_id": "dqbp-controller-v1",
        "records": [
            {
                "name": "dqbp_success_advantage_over_best_budget_matched_baseline",
                "value": primary_value,
                "unit": "proportion",
                "split": "in_distribution_pooled",
                "aggregation": "difference_of_episode_means",
                "n": total_n,
                "seed": args.seed,
            },
            {
                "name": "dqbp_success_rate",
                "value": in_dist_dqbp["success_rate"],
                "unit": "proportion",
                "split": "in_distribution_pooled",
                "aggregation": "episode_mean",
                "n": total_n,
                "seed": args.seed,
            },
            {
                "name": "dqbp_harmful_error_rate",
                "value": in_dist_dqbp["harmful_error_rate"],
                "unit": "proportion",
                "split": "in_distribution_pooled",
                "aggregation": "episode_mean",
                "n": total_n,
                "seed": args.seed,
            },
            {
                "name": "dqbp_average_probe_cost",
                "value": in_dist_dqbp["average_probe_cost"],
                "unit": "cost_units",
                "split": "in_distribution_pooled",
                "aggregation": "episode_mean",
                "n": total_n,
                "seed": args.seed,
            },
            {
                "name": "state_information_gain_success_rate",
                "value": pooled_summaries[
                    "in_distribution/state_information_gain"
                ]["success_rate"],
                "unit": "proportion",
                "split": "in_distribution_pooled",
                "aggregation": "episode_mean",
                "n": total_n,
                "seed": args.seed,
            },
            {
                "name": "fixed_readback_success_rate",
                "value": pooled_summaries["in_distribution/fixed_readback"][
                    "success_rate"
                ],
                "unit": "proportion",
                "split": "in_distribution_pooled",
                "aggregation": "episode_mean",
                "n": total_n,
                "seed": args.seed,
            },
        ],
        "resource_usage": {
            "tokens": 0,
            "api_calls": 0,
            "wall_time_seconds": elapsed,
            "gpu_time_seconds": 0,
            "estimated_cost": 0,
        },
        "errors": [],
        "warnings": [
            "Controller-isolation experiment; language-model plan extraction is not exercised."
        ],
    }
    if args.metrics_output:
        args.metrics_output.parent.mkdir(parents=True, exist_ok=True)
        args.metrics_output.write_text(
            json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    print(json.dumps(details["primary"], ensure_ascii=False))
    for condition in CONDITIONS:
        print(f"[{condition}]")
        for method in METHODS:
            item = pooled_summaries[f"{condition}/{method}"]
            print(
                f"{method:24s} success={item['success_rate']:.4f} "
                f"harm={item['harmful_error_rate']:.4f} "
                f"abstain={item['abstain_rate']:.4f} "
                f"probe_cost={item['average_probe_cost']:.3f}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
