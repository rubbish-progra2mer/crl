from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split


POLICIES = (
    "target_bor_dqn",
    "target_f1_dqn",
    "unconstrained_ratio_dqn",
    "coverage_constrained_chance_dqn",
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_bm25(wheel_path: Path) -> type:
    sys.path.insert(0, str(wheel_path))
    try:
        from rank_bm25 import BM25Okapi
    finally:
        sys.path.pop(0)
    return BM25Okapi


def extract_query_text(question: Any) -> str:
    if not isinstance(question, list) or not question:
        return ""
    inner = question[0]
    if isinstance(inner, list):
        for message in inner:
            if isinstance(message, dict) and message.get("role") == "user":
                return str(message.get("content", ""))
    if isinstance(inner, dict) and inner.get("role") == "user":
        return str(inner.get("content", ""))
    return ""


def rebuild_instances(
    input_path: Path, wheel_path: Path, candidate_size: int
) -> list[dict[str, Any]]:
    raw = [
        json.loads(line)
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    registry: dict[str, str] = {}
    queries: list[dict[str, str]] = []
    for line_index, source in enumerate(raw):
        text = extract_query_text(source.get("question", []))
        functions = source.get("function", [])
        if not text or not isinstance(functions, list) or not functions:
            continue
        function = functions[0]
        name = str(function.get("name", ""))
        if not name:
            continue
        description = str(function.get("description", ""))
        parameters = function.get("parameters", {})
        properties = parameters.get("properties", {}) if isinstance(parameters, dict) else {}
        parameter_names = list(properties) if isinstance(properties, dict) else []
        tool_text = f"{name}: {description}"
        if parameter_names:
            tool_text += f". Parameters: {', '.join(parameter_names)}"
        registry[name] = tool_text
        queries.append(
            {
                "query_id": str(source.get("id", f"line_{line_index}")),
                "query": text[:500],
                "gold_tool": name,
            }
        )
    tool_names = sorted(registry)
    actual_candidate_size = min(candidate_size, len(tool_names))
    tool_to_index = {name: index for index, name in enumerate(tool_names)}
    bm25_type = load_bm25(wheel_path)
    bm25 = bm25_type([registry[name].lower().split() for name in tool_names])
    instances: list[dict[str, Any]] = []
    for query in queries:
        if query["gold_tool"] not in tool_to_index:
            continue
        scores = np.asarray(bm25.get_scores(query["query"].lower().split()), dtype=np.float32)
        gold_index = tool_to_index[query["gold_tool"]]
        ranked_global = np.argsort(-scores)
        hard = [index for index in ranked_global if index != gold_index][
            : actual_candidate_size - 1
        ]
        candidate = [gold_index, *hard]
        candidate_scores = scores[candidate]
        order = np.argsort(-candidate_scores)
        gold_rank = int(np.where(order == 0)[0][0] + 1)
        instances.append(
            {
                "query_id": query["query_id"],
                "gold_rank": gold_rank,
                "scores": candidate_scores[order],
                "n": actual_candidate_size,
            }
        )
    return instances


def state_vector(instance: dict[str, Any], k: int) -> np.ndarray:
    scores = instance["scores"]
    n = int(instance["n"])
    index = min(k - 1, n - 1)
    current = float(scores[index])
    following = float(scores[index + 1]) if index + 1 < n else current
    first = float(scores[0])
    mean = float(scores.mean())
    std = float(scores.std() + 1e-6)
    gap = current - following if index + 1 < n else 0.0
    return np.asarray(
        [
            k / n,
            math.log2(k + 1) / math.log2(n + 1),
            current,
            following,
            gap,
            (current - mean) / std,
            current / (abs(first) + 1e-6),
        ],
        dtype=np.float32,
    )


class QNetwork(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(7, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return self.net(value)


def rollout_k(instance: dict[str, Any], model: QNetwork) -> int:
    k = 1
    n = int(instance["n"])
    while True:
        with torch.no_grad():
            action = int(
                model(torch.tensor(state_vector(instance, k)).unsqueeze(0))
                .argmax(1)
                .item()
            )
        if action == 0 or k >= n:
            return k
        k += 1


def group_key(row: dict[str, Any]) -> tuple[str, int | None]:
    return str(row["policy"]), row.get("seed")


def independent_summaries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, int | None], list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(group_key(row), []).append(row)
    result: list[dict[str, Any]] = []
    for (policy, seed), values in sorted(
        groups.items(), key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1])
    ):
        coverage = sum(int(value["hit"]) for value in values) / len(values)
        mean_k = sum(int(value["k"]) for value in values) / len(values)
        mean_chance = sum(float(value["chance_probability"]) for value in values) / len(values)
        result.append(
            {
                "policy": policy,
                "seed": seed,
                "rows": len(values),
                "coverage": coverage,
                "mean_k": mean_k,
                "mean_chance": mean_chance,
                "defined_bor": math.log2(coverage / mean_chance) if coverage else None,
                "mean_target_surrogate": sum(float(value["target_surrogate"]) for value in values)
                / len(values),
            }
        )
    return result


def means(summaries: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for policy in sorted({item["policy"] for item in summaries}):
        selected = [item for item in summaries if item["policy"] == policy]
        output[policy] = {
            "coverage": sum(item["coverage"] for item in selected) / len(selected),
            "mean_k": sum(item["mean_k"] for item in selected) / len(selected),
            "defined_bor": sum(item["defined_bor"] for item in selected) / len(selected),
            "groups": len(selected),
        }
    return output


def conditions(
    summaries: list[dict[str, Any]], policy_means: dict[str, dict[str, float]]
) -> dict[str, Any]:
    candidate = policy_means["coverage_constrained_chance_dqn"]
    target = policy_means["target_bor_dqn"]
    per_seed: list[dict[str, Any]] = []
    for seed in (42, 123, 456):
        left = next(
            item
            for item in summaries
            if item["policy"] == "coverage_constrained_chance_dqn" and item["seed"] == seed
        )
        right = next(
            item
            for item in summaries
            if item["policy"] == "target_bor_dqn" and item["seed"] == seed
        )
        per_seed.append(
            {
                "seed": seed,
                "coverage_delta": left["coverage"] - right["coverage"],
                "mean_k_delta": left["mean_k"] - right["mean_k"],
                "condition": left["coverage"] - right["coverage"] >= -0.025
                and left["mean_k"] < right["mean_k"],
            }
        )
    dominated = False
    dominating_policy = None
    for policy, values in policy_means.items():
        if policy == "coverage_constrained_chance_dqn":
            continue
        no_worse = values["coverage"] >= candidate["coverage"] and values["mean_k"] <= candidate["mean_k"]
        strict = values["coverage"] > candidate["coverage"] or values["mean_k"] < candidate["mean_k"]
        if no_worse and strict:
            dominated = True
            dominating_policy = policy
            break
    return {
        "candidate_minus_target": {
            "coverage": candidate["coverage"] - target["coverage"],
            "mean_k": candidate["mean_k"] - target["mean_k"],
            "defined_bor": candidate["defined_bor"] - target["defined_bor"],
        },
        "mean_coverage_condition": candidate["coverage"] - target["coverage"] >= -0.01,
        "mean_k_condition": candidate["mean_k"] <= target["mean_k"] - 1.0,
        "defined_bor_condition": candidate["defined_bor"] >= target["defined_bor"] + 0.25,
        "matched_seed_conditions": per_seed,
        "matched_seed_condition_count": sum(item["condition"] for item in per_seed),
        "matched_seed_count_condition": sum(item["condition"] for item in per_seed) >= 2,
        "candidate_is_dominated": dominated,
        "dominating_policy": dominating_policy,
        "nondominance_condition": not dominated,
    }


def maximum_error(left: Any, right: Any) -> float:
    if isinstance(left, dict) and isinstance(right, dict):
        if set(left) != set(right):
            return math.inf
        return max((maximum_error(left[key], right[key]) for key in left), default=0.0)
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            return math.inf
        return max((maximum_error(a, b) for a, b in zip(left, right)), default=0.0)
    if isinstance(left, bool) or isinstance(right, bool) or left is None or right is None:
        return 0.0 if left == right else math.inf
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(float(left) - float(right))
    return 0.0 if left == right else math.inf


def audit(arguments: argparse.Namespace) -> dict[str, Any]:
    config = read_json(arguments.config)
    summary = read_json(arguments.summary)
    rows = read_rows(arguments.raw_rows)
    history = read_json(arguments.controller_history) if arguments.controller_history else []
    errors: list[str] = []
    max_metric_error = 0.0
    max_row_error = 0.0
    max_controller_error = 0.0
    max_policy_k_error = 0.0

    if sha256_path(arguments.config) != summary["config_sha256"]:
        errors.append("config SHA mismatch")
    if sha256_path(arguments.input) != summary["input_sha256"]:
        errors.append("input SHA mismatch")
    if sha256_path(arguments.rank_bm25_wheel) != summary["rank_bm25_wheel_sha256"]:
        errors.append("rank-bm25 wheel SHA mismatch")
    if len(rows) != int(summary["row_count"]):
        errors.append("row count mismatch")

    rebuilt = rebuild_instances(
        arguments.input, arguments.rank_bm25_wheel, int(config["candidate_size"])
    )
    if summary["phase"] == "development":
        rebuilt_indices = np.arange(len(rebuilt))
        _, rebuilt_test_indices = train_test_split(
            rebuilt_indices,
            test_size=float(config["development"]["test_fraction"]),
            random_state=int(config["development"]["split_seed"]),
        )
        expected_instances = [rebuilt[int(index)] for index in rebuilt_test_indices]
        expected_query_ids = set(summary["split_manifest"]["test_query_ids"])
        if expected_query_ids != {item["query_id"] for item in expected_instances}:
            errors.append("split manifest does not match independent reconstruction")
    else:
        expected_instances = rebuilt
        expected_query_ids = {item["query_id"] for item in rebuilt}
    expected_by_id = {item["query_id"]: item for item in expected_instances}

    expected_seeds = [int(value) for value in config["seeds"]]
    query_sets: dict[tuple[str, int | None], set[str]] = {}
    for row in rows:
        k = int(row["k"])
        n = int(row["n"])
        gold_rank = int(row["gold_rank"])
        hit = int(row["hit"])
        expected_hit = int(gold_rank <= k)
        expected_chance = k / n
        expected_surrogate = expected_hit * -math.log2(expected_chance)
        max_row_error = max(
            max_row_error,
            abs(hit - expected_hit),
            abs(float(row["chance_probability"]) - expected_chance),
            abs(float(row["target_surrogate"]) - expected_surrogate),
        )
        if not 1 <= k <= n:
            errors.append("depth outside [1,n]")
        rebuilt_item = expected_by_id.get(str(row["query_id"]))
        if rebuilt_item is None:
            errors.append("row query ID absent from reconstructed split")
        elif gold_rank != int(rebuilt_item["gold_rank"]) or n != int(rebuilt_item["n"]):
            errors.append("row gold rank or corpus size mismatch")
        query_sets.setdefault(group_key(row), set()).add(str(row["query_id"]))
    if max_row_error > 1e-12:
        errors.append("raw row arithmetic mismatch")

    learned_sets = [
        query_sets[(policy, seed)] for policy in POLICIES for seed in expected_seeds
    ]
    fixed_sets = [
        values for (policy, seed), values in query_sets.items() if policy.startswith("fixed_k_") and seed is None
    ]
    all_sets = learned_sets + fixed_sets
    if any(values != all_sets[0] for values in all_sets[1:]):
        errors.append("query sets differ across policies")
    if any(values != expected_query_ids for values in all_sets):
        errors.append("policy query set differs from reconstructed split")
    group_counts = Counter(group_key(row) for row in rows)
    if any(count != len(expected_query_ids) for count in group_counts.values()):
        errors.append("group row count does not equal reconstructed query count")

    computed_summaries = independent_summaries(rows)
    computed_means = means(computed_summaries)
    computed_conditions = conditions(computed_summaries, computed_means)
    max_metric_error = max(
        maximum_error(computed_summaries, summary["group_summaries"]),
        maximum_error(computed_means, summary["policy_means"]),
        maximum_error(computed_conditions, summary["preregistered_conditions"]),
    )
    if max_metric_error > 1e-12:
        errors.append("summary metric mismatch")

    expected_history_count = (
        len(expected_seeds)
        * 2
        * (int(config["training"]["episodes"]) // int(config["training"]["controller_update_episodes"]))
    )
    if summary["phase"] == "development" and len(history) != expected_history_count:
        errors.append("controller history count mismatch")
    history_groups: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for item in history:
        history_groups.setdefault((str(item["policy"]), int(item["seed"])), []).append(item)
        before = float(item["controller_before"])
        coverage = float(item["coverage"])
        mean_chance = float(item["mean_chance"])
        if item["policy"] == "coverage_constrained_chance_dqn":
            expected_after = float(
                np.clip(
                    before
                    + float(config["training"]["dual_step"])
                    * (float(config["training"]["coverage_target"]) - coverage),
                    0.0,
                    float(config["training"]["dual_maximum"]),
                )
            )
        elif item["policy"] == "unconstrained_ratio_dqn":
            expected_after = coverage / mean_chance
        else:
            errors.append("unexpected controller policy")
            continue
        max_controller_error = max(
            max_controller_error, abs(expected_after - float(item["controller_after"]))
        )
    if max_controller_error > 1e-12:
        errors.append("controller update mismatch")
    if summary["phase"] == "development":
        expected_episodes = list(
            range(
                int(config["training"]["controller_update_episodes"]),
                int(config["training"]["episodes"]) + 1,
                int(config["training"]["controller_update_episodes"]),
            )
        )
        for policy in ("coverage_constrained_chance_dqn", "unconstrained_ratio_dqn"):
            for seed in expected_seeds:
                group = history_groups.get((policy, seed), [])
                if [int(item["episode"]) for item in group] != expected_episodes:
                    errors.append(f"controller episode sequence mismatch {policy}:{seed}")
                    continue
                for previous, current in zip(group, group[1:]):
                    max_controller_error = max(
                        max_controller_error,
                        abs(
                            float(previous["controller_after"])
                            - float(current["controller_before"])
                        ),
                    )
        if max_controller_error > 1e-12 and "controller continuity mismatch" not in errors:
            errors.append("controller continuity mismatch")

    model_manifest = summary["models"]
    expected_model_keys = {
        f"{policy}:{seed}" for policy in POLICIES for seed in expected_seeds
    }
    if set(model_manifest) != expected_model_keys:
        errors.append("model manifest key mismatch")
    learned_rows = {
        (str(row["policy"]), int(row["seed"]), str(row["query_id"])): row
        for row in rows
        if row.get("seed") is not None
    }
    policy_actions_checked = 0
    for key, item in model_manifest.items():
        path = Path(item["path"])
        if not path.is_file():
            errors.append(f"missing model {key}")
            continue
        if path.stat().st_size != int(item["bytes"]) or sha256_path(path) != item["sha256"]:
            errors.append(f"model binding mismatch {key}")
            continue
        try:
            policy, seed_text = key.rsplit(":", 1)
            seed = int(seed_text)
            model = QNetwork()
            model.load_state_dict(torch.load(path, map_location="cpu", weights_only=True))
            model.eval()
        except (ValueError, RuntimeError) as error:
            errors.append(f"model load mismatch {key}: {error}")
            continue
        for instance in expected_instances:
            row = learned_rows.get((policy, seed, str(instance["query_id"])))
            if row is None:
                errors.append(f"missing learned row {key}:{instance['query_id']}")
                continue
            expected_k = rollout_k(instance, model)
            max_policy_k_error = max(max_policy_k_error, abs(expected_k - int(row["k"])))
            policy_actions_checked += 1
    if max_policy_k_error > 0:
        errors.append("learned policy rollout mismatch")

    return {
        "schema_version": 1,
        "phase": summary["phase"],
        "status": "AUDIT_OK" if not errors else "AUDIT_ERROR",
        "errors": errors,
        "rows_checked": len(rows),
        "groups_checked": len(group_counts),
        "query_ids_checked": len(all_sets[0]) if all_sets else 0,
        "controller_updates_checked": len(history),
        "models_checked": len(model_manifest),
        "policy_actions_checked": policy_actions_checked,
        "maximum_raw_row_error": max_row_error,
        "maximum_metric_error": max_metric_error,
        "maximum_controller_error": max_controller_error,
        "maximum_policy_k_error": max_policy_k_error,
        "config_sha256": sha256_path(arguments.config),
        "input_sha256": sha256_path(arguments.input),
        "raw_rows_sha256": sha256_path(arguments.raw_rows),
        "summary_sha256": sha256_path(arguments.summary),
        "controller_history_sha256": sha256_path(arguments.controller_history)
        if arguments.controller_history
        else None,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--rank-bm25-wheel", type=Path, required=True)
    parser.add_argument("--raw-rows", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--controller-history", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    report = audit(arguments)
    arguments.report.parent.mkdir(parents=True, exist_ok=False)
    arguments.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "rows_checked": report["rows_checked"],
                "maximum_metric_error": report["maximum_metric_error"],
                "maximum_controller_error": report["maximum_controller_error"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "AUDIT_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
