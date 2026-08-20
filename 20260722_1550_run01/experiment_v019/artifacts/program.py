from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import random
import sys
import time
from collections import Counter, deque
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
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


def line_sha256s(path: Path) -> list[str]:
    return [
        hashlib.sha256(line).hexdigest()
        for line in path.read_bytes().splitlines()
        if line.strip()
    ]


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_environment() -> dict[str, Any]:
    cuda_available = torch.cuda.is_available()
    return {
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
        "cuda_runtime": torch.version.cuda,
        "cuda_available": cuda_available,
        "gpu_names": [
            torch.cuda.get_device_name(index)
            for index in range(torch.cuda.device_count())
        ]
        if cuda_available
        else [],
        "training_device": "cpu",
    }


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


def load_instances(
    input_path: Path, bm25_type: type, candidate_size: int
) -> tuple[list[dict[str, Any]], int, int]:
    source_rows = [
        json.loads(line)
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    registry: dict[str, str] = {}
    queries: list[dict[str, str]] = []
    for line_index, source in enumerate(source_rows):
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
    corpus = [registry[name].lower().split() for name in tool_names]
    bm25 = bm25_type(corpus)
    instances: list[dict[str, Any]] = []
    for query in queries:
        gold_tool = query["gold_tool"]
        if gold_tool not in tool_to_index:
            continue
        scores = np.asarray(bm25.get_scores(query["query"].lower().split()), dtype=np.float32)
        gold_index = tool_to_index[gold_tool]
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
                "query": query["query"],
                "gold_tool": gold_tool,
                "gold_rank": gold_rank,
                "scores": candidate_scores[order],
                "n": actual_candidate_size,
            }
        )
    if len({item["query_id"] for item in instances}) != len(instances):
        raise ValueError("query IDs are not unique")
    return instances, len(tool_names), actual_candidate_size


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


def target_terminal_reward(policy_name: str, hit: float, k: int, p: float) -> float:
    if policy_name == "target_bor_dqn":
        return hit * -math.log2(max(p, 1e-12))
    if policy_name == "target_f1_dqn":
        return hit * (2.0 / (k + 1.0))
    raise ValueError(f"not a target policy: {policy_name}")


def terminal_utility(
    policy_name: str,
    hit: torch.Tensor,
    chance: torch.Tensor,
    k: torch.Tensor,
    controller: float,
) -> torch.Tensor:
    if policy_name == "target_bor_dqn":
        return hit * (-torch.log2(torch.clamp(chance, min=1e-12)))
    if policy_name == "target_f1_dqn":
        return hit * (2.0 / (k + 1.0))
    if policy_name == "unconstrained_ratio_dqn":
        return hit - controller * chance
    if policy_name == "coverage_constrained_chance_dqn":
        return controller * hit - chance
    raise ValueError(policy_name)


def updated_coverage_dual(
    current: float, coverage: float, target: float, step: float, maximum: float
) -> float:
    return float(np.clip(current + step * (target - coverage), 0.0, maximum))


def updated_ratio(coverage: float, mean_chance: float) -> float:
    return coverage / mean_chance


def rollout_k(instance: dict[str, Any], model: QNetwork) -> int:
    k = 1
    n = int(instance["n"])
    while True:
        features = torch.tensor(state_vector(instance, k)).unsqueeze(0)
        with torch.no_grad():
            action = int(model(features).argmax(1).item())
        if action == 0 or k >= n:
            return k
        k += 1


def evaluate_model(
    instances: list[dict[str, Any]],
    model: QNetwork,
    policy_name: str,
    seed: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for instance in instances:
        k = rollout_k(instance, model)
        n = int(instance["n"])
        hit = int(instance["gold_rank"] <= k)
        chance = k / n
        rows.append(
            {
                "query_id": instance["query_id"],
                "policy": policy_name,
                "seed": seed,
                "gold_rank": int(instance["gold_rank"]),
                "k": k,
                "n": n,
                "hit": hit,
                "chance_probability": chance,
                "target_surrogate": hit * -math.log2(chance),
            }
        )
    return rows


def evaluate_fixed(instances: list[dict[str, Any]], k: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for instance in instances:
        n = int(instance["n"])
        actual_k = min(k, n)
        hit = int(instance["gold_rank"] <= actual_k)
        chance = actual_k / n
        rows.append(
            {
                "query_id": instance["query_id"],
                "policy": f"fixed_k_{actual_k}",
                "seed": None,
                "gold_rank": int(instance["gold_rank"]),
                "k": actual_k,
                "n": n,
                "hit": hit,
                "chance_probability": chance,
                "target_surrogate": hit * -math.log2(chance),
            }
        )
    return rows


def policy_training_probe(
    instances: list[dict[str, Any]], model: QNetwork
) -> tuple[float, float, float]:
    ks = [rollout_k(instance, model) for instance in instances]
    hits = [int(item["gold_rank"] <= k) for item, k in zip(instances, ks)]
    chances = [k / int(item["n"]) for item, k in zip(instances, ks)]
    return float(np.mean(hits)), float(np.mean(ks)), float(np.mean(chances))


def initial_ratio(instances: list[dict[str, Any]], initial_k: int) -> float:
    hits = [int(item["gold_rank"] <= initial_k) for item in instances]
    chances = [min(initial_k, int(item["n"])) / int(item["n"]) for item in instances]
    return updated_ratio(float(np.mean(hits)), float(np.mean(chances)))


def train_policy(
    instances: list[dict[str, Any]],
    policy_name: str,
    seed: int,
    settings: dict[str, Any],
) -> tuple[QNetwork, list[dict[str, Any]], float]:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model = QNetwork()
    target = QNetwork()
    target.load_state_dict(model.state_dict())
    optimizer = optim.Adam(model.parameters(), lr=float(settings["learning_rate"]))
    replay: deque[tuple[Any, ...]] = deque(maxlen=int(settings["replay_capacity"]))
    episodes = int(settings["episodes"])
    batch_size = int(settings["batch_size"])
    target_every = int(settings["target_every_steps"])
    update_every = int(settings["controller_update_episodes"])
    target_coverage = float(settings["coverage_target"])
    dual_step = float(settings["dual_step"])
    dual_maximum = float(settings["dual_maximum"])
    if policy_name == "coverage_constrained_chance_dqn":
        controller = float(settings["dual_initial"])
    elif policy_name == "unconstrained_ratio_dqn":
        controller = initial_ratio(instances, int(settings["ratio_initial_k"]))
    else:
        controller = 0.0
    history: list[dict[str, Any]] = []
    environment_steps = 0

    for episode in range(1, episodes + 1):
        instance = random.choice(instances)
        n = int(instance["n"])
        k = 1
        done = False
        epsilon = float(settings["epsilon_end"]) + (
            float(settings["epsilon_start"]) - float(settings["epsilon_end"])
        ) * max(0.0, 1.0 - episode / episodes)
        while not done:
            state = state_vector(instance, k)
            if random.random() < epsilon:
                action = random.randint(0, 1)
            else:
                with torch.no_grad():
                    action = int(model(torch.tensor(state).unsqueeze(0)).argmax(1).item())
            if k >= n:
                action = 0
            if action == 0:
                hit = float(instance["gold_rank"] <= k)
                chance = k / n
                replay.append((state, action, hit, chance, float(k), None, 1.0))
                done = True
            else:
                next_k = k + 1
                if next_k >= n:
                    hit = float(instance["gold_rank"] <= n)
                    replay.append((state, action, hit, 1.0, float(n), None, 1.0))
                    done = True
                else:
                    next_state = state_vector(instance, next_k)
                    replay.append((state, action, 0.0, 0.0, float(next_k), next_state, 0.0))
                    k = next_k
            environment_steps += 1
            if len(replay) >= batch_size:
                batch = random.sample(replay, batch_size)
                states = torch.tensor(np.stack([item[0] for item in batch]))
                actions = torch.tensor([item[1] for item in batch], dtype=torch.long)
                hits = torch.tensor([item[2] for item in batch], dtype=torch.float32)
                chances = torch.tensor([item[3] for item in batch], dtype=torch.float32)
                depths = torch.tensor([item[4] for item in batch], dtype=torch.float32)
                dones = torch.tensor([item[6] for item in batch], dtype=torch.float32)
                terminal = terminal_utility(
                    policy_name, hits, chances, depths, controller
                )
                if policy_name in ("target_bor_dqn", "target_f1_dqn"):
                    rewards = torch.where(
                        dones.bool(),
                        terminal,
                        torch.full_like(terminal, -float(settings["target_step_cost"])),
                    )
                    gamma = float(settings["target_gamma"])
                else:
                    rewards = torch.where(dones.bool(), terminal, torch.zeros_like(terminal))
                    gamma = 1.0
                next_values = torch.zeros(batch_size, dtype=torch.float32)
                has_next = torch.tensor(
                    [item[5] is not None for item in batch], dtype=torch.bool
                )
                if bool(has_next.any()):
                    next_states = torch.tensor(
                        np.stack([item[5] for item in batch if item[5] is not None])
                    )
                    with torch.no_grad():
                        next_values[has_next] = target(next_states).max(1).values
                current_values = model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
                targets = rewards + (1.0 - dones) * gamma * next_values
                loss = nn.SmoothL1Loss()(current_values, targets)
                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), 5.0)
                optimizer.step()
            if environment_steps % target_every == 0:
                target.load_state_dict(model.state_dict())

        if policy_name in (
            "coverage_constrained_chance_dqn",
            "unconstrained_ratio_dqn",
        ) and episode % update_every == 0:
            coverage, mean_k, mean_chance = policy_training_probe(instances, model)
            before = controller
            if policy_name == "coverage_constrained_chance_dqn":
                controller = updated_coverage_dual(
                    before, coverage, target_coverage, dual_step, dual_maximum
                )
            else:
                controller = updated_ratio(coverage, mean_chance)
            history.append(
                {
                    "policy": policy_name,
                    "seed": seed,
                    "episode": episode,
                    "coverage": coverage,
                    "mean_k": mean_k,
                    "mean_chance": mean_chance,
                    "controller_before": before,
                    "controller_after": controller,
                }
            )
        if episode % 3000 == 0:
            print(
                f"training policy={policy_name} seed={seed} episode={episode}/{episodes}",
                flush=True,
            )
    return model, history, controller


def group_key(row: dict[str, Any]) -> tuple[str, int | None]:
    return str(row["policy"]), row.get("seed")


def summarize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, int | None], list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(group_key(row), []).append(row)
    summaries: list[dict[str, Any]] = []
    for (policy, seed), values in sorted(
        groups.items(), key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1])
    ):
        coverage = float(np.mean([int(value["hit"]) for value in values]))
        mean_k = float(np.mean([int(value["k"]) for value in values]))
        mean_chance = float(np.mean([float(value["chance_probability"]) for value in values]))
        summaries.append(
            {
                "policy": policy,
                "seed": seed,
                "rows": len(values),
                "coverage": coverage,
                "mean_k": mean_k,
                "mean_chance": mean_chance,
                "defined_bor": math.log2(coverage / mean_chance) if coverage else None,
                "mean_target_surrogate": float(
                    np.mean([float(value["target_surrogate"]) for value in values])
                ),
            }
        )
    return summaries


def policy_means(summaries: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for policy in sorted({item["policy"] for item in summaries}):
        items = [item for item in summaries if item["policy"] == policy]
        result[policy] = {
            "coverage": float(np.mean([item["coverage"] for item in items])),
            "mean_k": float(np.mean([item["mean_k"] for item in items])),
            "defined_bor": float(np.mean([item["defined_bor"] for item in items])),
            "groups": len(items),
        }
    return result


def preregistered_conditions(
    summaries: list[dict[str, Any]], means: dict[str, dict[str, float]]
) -> dict[str, Any]:
    candidate = means["coverage_constrained_chance_dqn"]
    target = means["target_bor_dqn"]
    seed_conditions: list[dict[str, Any]] = []
    for seed in (42, 123, 456):
        candidate_seed = next(
            item
            for item in summaries
            if item["policy"] == "coverage_constrained_chance_dqn" and item["seed"] == seed
        )
        target_seed = next(
            item
            for item in summaries
            if item["policy"] == "target_bor_dqn" and item["seed"] == seed
        )
        seed_conditions.append(
            {
                "seed": seed,
                "coverage_delta": candidate_seed["coverage"] - target_seed["coverage"],
                "mean_k_delta": candidate_seed["mean_k"] - target_seed["mean_k"],
                "condition": candidate_seed["coverage"] - target_seed["coverage"] >= -0.025
                and candidate_seed["mean_k"] < target_seed["mean_k"],
            }
        )
    candidate_is_dominated = False
    dominating_policy = None
    for policy, values in means.items():
        if policy == "coverage_constrained_chance_dqn":
            continue
        no_worse = values["coverage"] >= candidate["coverage"] and values["mean_k"] <= candidate["mean_k"]
        strict = values["coverage"] > candidate["coverage"] or values["mean_k"] < candidate["mean_k"]
        if no_worse and strict:
            candidate_is_dominated = True
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
        "matched_seed_conditions": seed_conditions,
        "matched_seed_condition_count": sum(item["condition"] for item in seed_conditions),
        "matched_seed_count_condition": sum(item["condition"] for item in seed_conditions) >= 2,
        "candidate_is_dominated": candidate_is_dominated,
        "dominating_policy": dominating_policy,
        "nondominance_condition": not candidate_is_dominated,
    }


def save_model(path: Path, model: QNetwork) -> dict[str, Any]:
    torch.save(model.state_dict(), path)
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256_path(path)}


def load_models(model_dir: Path, seeds: list[int]) -> dict[tuple[str, int], QNetwork]:
    models: dict[tuple[str, int], QNetwork] = {}
    for policy in POLICIES:
        for seed in seeds:
            path = model_dir / f"{policy}_seed{seed}.pt"
            model = QNetwork()
            model.load_state_dict(torch.load(path, map_location="cpu", weights_only=True))
            model.eval()
            models[(policy, seed)] = model
    return models


def run_development(
    arguments: argparse.Namespace, config: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    development = config["development"]
    if sha256_path(arguments.input) != development["input_sha256"]:
        raise ValueError("development input SHA mismatch")
    if len(line_sha256s(arguments.input)) != int(development["expected_lines"]):
        raise ValueError("development input line count mismatch")
    bm25_type = load_bm25(arguments.rank_bm25_wheel)
    instances, registry_size, candidate_size = load_instances(
        arguments.input, bm25_type, int(config["candidate_size"])
    )
    indices = np.arange(len(instances))
    train_indices, test_indices = train_test_split(
        indices,
        test_size=float(development["test_fraction"]),
        random_state=int(development["split_seed"]),
    )
    train_instances = [instances[int(index)] for index in train_indices]
    test_instances = [instances[int(index)] for index in test_indices]
    rows: list[dict[str, Any]] = []
    for fixed_k in config["fixed_k"]:
        rows.extend(evaluate_fixed(test_instances, int(fixed_k)))
    model_dir = arguments.output_dir / "models"
    model_dir.mkdir(parents=True, exist_ok=False)
    histories: list[dict[str, Any]] = []
    models: dict[str, dict[str, Any]] = {}
    final_controllers: dict[str, float] = {}
    for seed in config["seeds"]:
        for policy in POLICIES:
            model, history, controller = train_policy(
                train_instances, policy, int(seed), config["training"]
            )
            model_path = model_dir / f"{policy}_seed{seed}.pt"
            models[f"{policy}:{seed}"] = save_model(model_path, model)
            histories.extend(history)
            final_controllers[f"{policy}:{seed}"] = controller
            rows.extend(evaluate_model(test_instances, model, policy, int(seed)))
    split = {
        "method": "sklearn.model_selection.train_test_split",
        "split_seed": int(development["split_seed"]),
        "test_fraction": float(development["test_fraction"]),
        "train_query_ids": [item["query_id"] for item in train_instances],
        "test_query_ids": [item["query_id"] for item in test_instances],
    }
    write_json(arguments.output_dir / "split_manifest.json", split)
    write_json(arguments.output_dir / "controller_history.json", histories)
    extra = {
        "models": models,
        "final_controllers": final_controllers,
        "split_manifest": split,
        "registry_size": registry_size,
        "candidate_size": candidate_size,
        "query_count": len(instances),
    }
    return rows, extra, histories


def run_confirmation(
    arguments: argparse.Namespace, config: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    if arguments.input_manifest is None or arguments.model_dir is None:
        raise ValueError("confirmation requires --input-manifest and --model-dir")
    manifest = json.loads(arguments.input_manifest.read_text(encoding="utf-8"))
    if sha256_path(arguments.input) != manifest["sha256"]:
        raise ValueError("confirmation input SHA mismatch")
    bm25_type = load_bm25(arguments.rank_bm25_wheel)
    instances, registry_size, candidate_size = load_instances(
        arguments.input, bm25_type, int(config["candidate_size"])
    )
    rows: list[dict[str, Any]] = []
    for fixed_k in config["fixed_k"]:
        rows.extend(evaluate_fixed(instances, int(fixed_k)))
    models = load_models(arguments.model_dir, [int(seed) for seed in config["seeds"]])
    model_manifest: dict[str, dict[str, Any]] = {}
    for (policy, seed), model in models.items():
        rows.extend(evaluate_model(instances, model, policy, seed))
        path = arguments.model_dir / f"{policy}_seed{seed}.pt"
        model_manifest[f"{policy}:{seed}"] = {
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": sha256_path(path),
        }
    extra = {
        "models": model_manifest,
        "input_manifest": manifest,
        "registry_size": registry_size,
        "candidate_size": candidate_size,
        "query_count": len(instances),
    }
    return rows, extra, []


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--rank-bm25-wheel", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path)
    parser.add_argument("--input-manifest", type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    config = read_config(arguments.config)
    if sha256_path(arguments.rank_bm25_wheel) != config["rank_bm25"]["wheel_sha256"]:
        raise ValueError("rank-bm25 wheel SHA mismatch")
    started = time.perf_counter()
    arguments.output_dir.mkdir(parents=True, exist_ok=False)
    if arguments.phase == "development":
        rows, extra, _ = run_development(arguments, config)
    else:
        rows, extra, _ = run_confirmation(arguments, config)
    summaries = summarize_rows(rows)
    means = policy_means(summaries)
    conditions = preregistered_conditions(summaries, means)
    write_rows(arguments.output_dir / "raw_rows.jsonl", rows)
    summary = {
        "schema_version": 1,
        "experiment_id": "v019",
        "phase": arguments.phase,
        "config_path": str(arguments.config.resolve()),
        "config_sha256": sha256_path(arguments.config),
        "input_path": str(arguments.input.resolve()),
        "input_sha256": sha256_path(arguments.input),
        "input_line_sha256s": line_sha256s(arguments.input),
        "rank_bm25_wheel_path": str(arguments.rank_bm25_wheel.resolve()),
        "rank_bm25_wheel_sha256": sha256_path(arguments.rank_bm25_wheel),
        "row_count": len(rows),
        "policy_row_counts": {
            f"{policy}:{seed}": count
            for (policy, seed), count in sorted(
                Counter(group_key(row) for row in rows).items(),
                key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1]),
            )
        },
        "group_summaries": summaries,
        "policy_means": means,
        "preregistered_conditions": conditions,
        "runtime_environment": runtime_environment(),
        "elapsed_seconds": time.perf_counter() - started,
        **extra,
    }
    write_json(arguments.output_dir / "summary.json", summary)
    print(
        json.dumps(
            {
                "phase": arguments.phase,
                "rows": len(rows),
                "candidate_coverage": means["coverage_constrained_chance_dqn"]["coverage"],
                "candidate_mean_k": means["coverage_constrained_chance_dqn"]["mean_k"],
                "target_coverage": means["target_bor_dqn"]["coverage"],
                "target_mean_k": means["target_bor_dqn"]["mean_k"],
                "elapsed_seconds": summary["elapsed_seconds"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
