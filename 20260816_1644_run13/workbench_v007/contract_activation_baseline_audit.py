from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from collections import defaultdict
from pathlib import Path


def evaluate_policy(policy: dict, state: dict[str, bool]) -> bool:
    def matches(group: dict) -> bool:
        return all(state[item["field"]] is item["value"] for item in group["all"])

    return any(matches(group) for group in policy["allow_any"]) and not any(
        matches(group) for group in policy["deny_any"]
    )


def all_states(fields: tuple[str, ...]) -> list[dict[str, bool]]:
    return [dict(zip(fields, values, strict=True)) for values in itertools.product((False, True), repeat=len(fields))]


def stable_seed(base_seed: int, replicate: int, task_id: str, label: str) -> int:
    digest = hashlib.sha256(f"{base_seed}:{replicate}:{task_id}:{label}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def uniform_suite(worlds: list[dict[str, bool]], count: int, *, seed: int) -> list[dict[str, bool]]:
    return random.Random(seed).sample(worlds, count)


def field_balanced_suite(
    worlds: list[dict[str, bool]], fields: tuple[str, ...], *, seed: int
) -> list[dict[str, bool]]:
    picker = random.Random(seed)
    suite = []
    for field in fields:
        for value in (False, True):
            pool = [state for state in worlds if state[field] is value]
            suite.append(picker.choice(pool))
    return suite


def disagreement_suite(rows: list[dict], worlds: list[dict[str, bool]], count: int) -> list[dict[str, bool]]:
    predictions = [
        [evaluate_policy(row["candidate_policy"], state) for state in worlds]
        for row in rows
    ]
    unresolved_pairs = {
        (left, right)
        for left in range(len(rows))
        for right in range(left + 1, len(rows))
        if predictions[left] != predictions[right]
    }
    selected: list[int] = []
    while len(selected) < count:
        best_index = None
        best_score = -1
        for state_index in range(len(worlds)):
            if state_index in selected:
                continue
            score = sum(
                predictions[left][state_index] != predictions[right][state_index]
                for left, right in unresolved_pairs
            )
            if score > best_score:
                best_score = score
                best_index = state_index
        if best_index is None:
            raise ValueError("could not construct disagreement suite")
        selected.append(best_index)
        unresolved_pairs = {
            pair
            for pair in unresolved_pairs
            if predictions[pair[0]][best_index] == predictions[pair[1]][best_index]
        }
    return [worlds[index] for index in selected]


def suite_accuracy(row: dict, suite: list[dict[str, bool]], reference: dict) -> float:
    return sum(
        evaluate_policy(row["candidate_policy"], state) == evaluate_policy(reference, state)
        for state in suite
    ) / len(suite)


def select_hidden_accuracy(rows: list[dict], suite: list[dict[str, bool]], reference: dict) -> float:
    selected = max(
        rows,
        key=lambda row: (suite_accuracy(row, suite, reference), -row["candidate_index"]),
    )
    return selected["hidden_accuracy"]


def quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def evaluate_fixed_suites(
    grouped: dict[tuple[str, str], list[dict]],
    tasks: dict[str, dict],
    suites: dict[tuple[str, str], list[dict[str, bool]]],
) -> tuple[float, float]:
    latent = []
    caught = 0
    selections = []
    for key, rows in grouped.items():
        model, task_id = key
        task = tasks[task_id]
        suite = suites[key]
        for row in rows:
            if row.get("latent_fault"):
                latent.append(row)
                if suite_accuracy(row, suite, task["reference"]) < 1.0:
                    caught += 1
        selections.append(select_hidden_accuracy(rows, suite, task["reference"]))
    recall = caught / len(latent) if latent else 0.0
    return recall, sum(selections) / len(selections)


def main() -> int:
    started = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-details", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260816)
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--details-output", type=Path, required=True)
    args = parser.parse_args()
    if args.replicates < 100:
        raise ValueError("replicates must be at least 100")

    source = json.loads(args.source_details.read_text(encoding="utf-8"))
    tasks = {task["task_id"]: task for task in source["tasks"]}
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in source["candidate_records"]:
        if row.get("error") is None and row.get("candidate_error") is None:
            grouped[(row["model"], row["task_id"])].append(row)
    for rows in grouped.values():
        rows.sort(key=lambda item: item["candidate_index"])

    worlds_by_task = {
        task_id: all_states(tuple(task["fields"])) for task_id, task in tasks.items()
    }
    activation_by_task = {
        task_id: [
            pair[name]
            for pair in source["designs"][task_id]["activation_pairs"]
            for name in ("false_state", "true_state")
        ]
        for task_id in tasks
    }
    activation_suites = {
        key: activation_by_task[key[1]] for key in grouped
    }
    disagreement_suites = {
        key: disagreement_suite(rows, worlds_by_task[key[1]], len(activation_by_task[key[1]]))
        for key, rows in grouped.items()
    }
    activation_recall, activation_selection = evaluate_fixed_suites(
        grouped, tasks, activation_suites
    )
    disagreement_recall, disagreement_selection = evaluate_fixed_suites(
        grouped, tasks, disagreement_suites
    )

    replicate_rows = []
    for replicate in range(args.replicates):
        uniform_suites = {}
        balanced_suites = {}
        for key in grouped:
            _, task_id = key
            task_worlds = worlds_by_task[task_id]
            fields = tuple(tasks[task_id]["fields"])
            count = len(activation_by_task[task_id])
            uniform_suites[key] = uniform_suite(
                task_worlds,
                count,
                seed=stable_seed(args.seed, replicate, task_id, "uniform"),
            )
            balanced_suites[key] = field_balanced_suite(
                task_worlds,
                fields,
                seed=stable_seed(args.seed, replicate, task_id, "balanced"),
            )
        uniform_recall, uniform_selection = evaluate_fixed_suites(
            grouped, tasks, uniform_suites
        )
        balanced_recall, balanced_selection = evaluate_fixed_suites(
            grouped, tasks, balanced_suites
        )
        replicate_rows.append(
            {
                "replicate": replicate,
                "uniform_fault_recall": uniform_recall,
                "uniform_selection_hidden_accuracy": uniform_selection,
                "balanced_fault_recall": balanced_recall,
                "balanced_selection_hidden_accuracy": balanced_selection,
            }
        )

    def stats(name: str) -> dict:
        values = [row[name] for row in replicate_rows]
        return {
            "mean": sum(values) / len(values),
            "p05": quantile(values, 0.05),
            "p50": quantile(values, 0.50),
            "p95": quantile(values, 0.95),
            "min": min(values),
            "max": max(values),
        }

    uniform_recall_stats = stats("uniform_fault_recall")
    uniform_selection_stats = stats("uniform_selection_hidden_accuracy")
    balanced_recall_stats = stats("balanced_fault_recall")
    balanced_selection_stats = stats("balanced_selection_hidden_accuracy")
    strongest_baseline_recall = max(
        uniform_recall_stats["mean"], balanced_recall_stats["mean"], disagreement_recall
    )
    strongest_baseline_selection = max(
        uniform_selection_stats["mean"], balanced_selection_stats["mean"], disagreement_selection
    )
    latent_fault_count = sum(row.get("latent_fault") is True for rows in grouped.values() for row in rows)
    summary = {
        "latent_fault_count": latent_fault_count,
        "state_budget_per_candidate": 10,
        "replicates": args.replicates,
        "activation_fault_recall": activation_recall,
        "activation_selection_hidden_accuracy": activation_selection,
        "uniform_fault_recall": uniform_recall_stats,
        "uniform_selection_hidden_accuracy": uniform_selection_stats,
        "balanced_fault_recall": balanced_recall_stats,
        "balanced_selection_hidden_accuracy": balanced_selection_stats,
        "disagreement_fault_recall": disagreement_recall,
        "disagreement_selection_hidden_accuracy": disagreement_selection,
        "strongest_baseline_fault_recall": strongest_baseline_recall,
        "strongest_baseline_selection_hidden_accuracy": strongest_baseline_selection,
        "activation_fault_recall_advantage_over_strongest_baseline": activation_recall - strongest_baseline_recall,
        "activation_selection_advantage_over_strongest_baseline": activation_selection - strongest_baseline_selection,
    }
    details = {
        "schema_version": 1,
        "experiment": "contract-activation-baseline-audit-v007",
        "source_details": str(args.source_details),
        "seed": args.seed,
        "summary": summary,
        "disagreement_suites": {
            f"{model}|{task_id}": suite for (model, task_id), suite in disagreement_suites.items()
        },
        "replicate_records": replicate_rows,
    }

    records = []
    metric_values = {
        "activation_fault_recall_advantage_over_strongest_baseline": summary["activation_fault_recall_advantage_over_strongest_baseline"],
        "activation_selection_advantage_over_strongest_baseline": summary["activation_selection_advantage_over_strongest_baseline"],
        "activation_fault_recall": activation_recall,
        "uniform_mean_fault_recall": uniform_recall_stats["mean"],
        "balanced_mean_fault_recall": balanced_recall_stats["mean"],
        "disagreement_fault_recall": disagreement_recall,
        "activation_selection_hidden_accuracy": activation_selection,
        "uniform_mean_selection_hidden_accuracy": uniform_selection_stats["mean"],
        "balanced_mean_selection_hidden_accuracy": balanced_selection_stats["mean"],
        "disagreement_selection_hidden_accuracy": disagreement_selection,
    }
    task_group_count = len(grouped)
    for name, value in metric_values.items():
        if "selection" in name:
            sample_count = args.replicates if "mean" in name else task_group_count
        else:
            sample_count = args.replicates if "mean" in name else latent_fault_count
        records.append(
            {
                "name": name,
                "value": value,
                "unit": "proportion",
                "split": "overall",
                "aggregation": "mean_over_replicates" if "mean" in name else "micro_over_fixed_candidate_pool",
                "n": sample_count,
                "seed": args.seed,
            }
        )
    metrics = {
        "schema_version": 1,
        "experiment_id": "contract-activation-baseline-audit-001",
        "records": records,
        "resource_usage": {
            "tokens": 0,
            "api_calls": 0,
            "wall_time_seconds": time.time() - started,
            "gpu_time_seconds": None,
            "estimated_cost": 0,
        },
        "errors": [],
        "warnings": [],
    }
    for path, payload in ((args.details_output, details), (args.metrics_output, metrics)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
