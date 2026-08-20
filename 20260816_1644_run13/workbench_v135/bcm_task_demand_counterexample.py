import json
from itertools import combinations
from pathlib import Path

import numpy as np


FEATURES = [
    "total_steps",
    "mean_action_length",
    "max_action_length",
    "file_search_count",
    "file_view_count",
    "file_edit_count",
    "test_execution_count",
    "action_entropy",
    "consecutive_repetition_max",
    "unique_action_ratio",
    "error_flag_count",
    "step_velocity",
]
SEARCH_INDEX = FEATURES.index("file_search_count")
EDIT_INDEX = FEATURES.index("file_edit_count")


def cosine(first, second):
    denominator = np.linalg.norm(first) * np.linalg.norm(second)
    if denominator == 0:
        return 0.0
    return float(np.dot(first, second) / denominator)


def calculate_bcm(matrix):
    if len(matrix) < 2:
        return 1.0
    return float(np.mean([cosine(matrix[i], matrix[j]) for i, j in combinations(range(len(matrix)), 2)]))


def build_systems(noise_seed=None, noise_std=0.02):
    rng = np.random.default_rng(noise_seed)
    systems = {"task_responsive": [], "task_invariant": []}
    for task in ("search_required", "edit_required"):
        for repeat in range(8):
            responsive = np.zeros(len(FEATURES), dtype=float)
            responsive[SEARCH_INDEX if task == "search_required" else EDIT_INDEX] = 1.0
            invariant = np.zeros(len(FEATURES), dtype=float)
            invariant[SEARCH_INDEX] = 1.0
            if noise_seed is not None:
                responsive[[SEARCH_INDEX, EDIT_INDEX]] += rng.normal(0.0, noise_std, size=2)
                invariant[[SEARCH_INDEX, EDIT_INDEX]] += rng.normal(0.0, noise_std, size=2)
            systems["task_responsive"].append(
                {
                    "task": task,
                    "repeat": repeat,
                    "resolved": int(repeat % 2 == 0),
                    "fingerprint": responsive,
                }
            )
            systems["task_invariant"].append(
                {
                    "task": task,
                    "repeat": repeat,
                    "resolved": int(task == "search_required"),
                    "fingerprint": invariant,
                }
            )
    return systems


def demand_align(row):
    vector = row["fingerprint"].copy()
    if row["task"] == "edit_required":
        vector[SEARCH_INDEX], vector[EDIT_INDEX] = vector[EDIT_INDEX], vector[SEARCH_INDEX]
    return vector


def summarize(rows):
    matrix = np.vstack([row["fingerprint"] for row in rows])
    within_scores = []
    for task in ("search_required", "edit_required"):
        within_scores.append(calculate_bcm(np.vstack([row["fingerprint"] for row in rows if row["task"] == task])))
    aligned_matrix = np.vstack([demand_align(row) for row in rows])
    by_outcome = {}
    for outcome in (0, 1):
        outcome_matrix = np.vstack([row["fingerprint"] for row in rows if row["resolved"] == outcome])
        by_outcome[str(outcome)] = calculate_bcm(outcome_matrix)
    return {
        "n": len(rows),
        "success_rate": float(np.mean([row["resolved"] for row in rows])),
        "global_bcm": calculate_bcm(matrix),
        "within_task_bcm": float(np.mean(within_scores)),
        "demand_aligned_bcm": calculate_bcm(aligned_matrix),
        "outcome_stratified_bcm": by_outcome,
    }


def ranking_holds(summary):
    responsive = summary["task_responsive"]
    invariant = summary["task_invariant"]
    return {
        "matched_success": bool(responsive["success_rate"] == invariant["success_rate"]),
        "raw_favors_invariant": bool(invariant["global_bcm"] > responsive["global_bcm"]),
        "within_task_tied": bool(np.isclose(invariant["within_task_bcm"], responsive["within_task_bcm"])),
        "aligned_favors_responsive": bool(responsive["demand_aligned_bcm"] > invariant["demand_aligned_bcm"]),
    }


def main():
    deterministic = {name: summarize(rows) for name, rows in build_systems().items()}
    criteria = ranking_holds(deterministic)
    robustness = []
    for seed in range(101):
        noisy = {name: summarize(rows) for name, rows in build_systems(noise_seed=seed).items()}
        noisy_criteria = ranking_holds(noisy)
        robustness.append(
            {
                "seed": seed,
                "raw_margin": noisy["task_invariant"]["global_bcm"] - noisy["task_responsive"]["global_bcm"],
                "aligned_margin": noisy["task_responsive"]["demand_aligned_bcm"] - noisy["task_invariant"]["demand_aligned_bcm"],
                "directions_hold": noisy_criteria["raw_favors_invariant"] and noisy_criteria["aligned_favors_responsive"],
            }
        )
    output = {
        "target_formula": "mean upper-triangle pairwise cosine similarity",
        "feature_count": len(FEATURES),
        "deterministic": deterministic,
        "preregistered_criteria": criteria,
        "all_deterministic_criteria_pass": bool(all(criteria.values())),
        "robustness": {
            "seeds": len(robustness),
            "direction_holds_count": sum(item["directions_hold"] for item in robustness),
            "raw_margin_min": min(item["raw_margin"] for item in robustness),
            "raw_margin_max": max(item["raw_margin"] for item in robustness),
            "aligned_margin_min": min(item["aligned_margin"] for item in robustness),
            "aligned_margin_max": max(item["aligned_margin"] for item in robustness),
        },
    }
    output_path = Path(__file__).with_name("bcm_task_demand_metrics.json")
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, indent=2, ensure_ascii=False))
    if not all(criteria.values()) or output["robustness"]["direction_holds_count"] != len(robustness):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
