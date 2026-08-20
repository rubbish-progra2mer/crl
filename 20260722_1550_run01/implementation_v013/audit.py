from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


SEEDS = (42, 123, 456)
FIXED_KS = (1, 3, 5, 10, 20, 50)
OFFICIAL_REFERENCE = {
    "bor_dqn": {"mean_k": 7.4, "found_fraction": 0.903},
    "f1_dqn": {"mean_k": 6.4, "found_fraction": 0.889},
    "fixed_found_fraction": {
        "fk_1": 0.600,
        "fk_3": 0.7833333333333333,
        "fk_5": 0.825,
        "fk_10": 0.850,
        "fk_20": 0.875,
        "fk_50": 0.9083333333333333,
    },
}


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
    elif isinstance(inner, dict) and inner.get("role") == "user":
        return str(inner.get("content", ""))
    return ""


def load_queries(input_path: Path, bm25_type: type) -> tuple[list[dict[str, Any]], int]:
    raw = [
        json.loads(line)
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    registry: dict[str, str] = {}
    entries: list[dict[str, str]] = []
    for line_index, entry in enumerate(raw):
        query_text = extract_query_text(entry.get("question", []))
        functions = entry.get("function", [])
        if not query_text or not isinstance(functions, list) or not functions:
            continue
        function = functions[0]
        name = function.get("name", "")
        if not name:
            continue
        description = function.get("description", "")
        parameters = function.get("parameters", {})
        properties = parameters.get("properties", {}) if isinstance(parameters, dict) else {}
        parameter_names = list(properties.keys()) if isinstance(properties, dict) else []
        if parameter_names:
            tool_text = (
                f"{name}: {description}. Parameters: {', '.join(parameter_names)}"
            )
        else:
            tool_text = f"{name}: {description}"
        registry[name] = tool_text
        entries.append(
            {
                "query_id": str(entry.get("id", f"line_{line_index}")),
                "text": query_text[:500],
                "correct_tool": str(name),
            }
        )

    tool_names = list(registry)
    tool_descriptions = [registry[name] for name in tool_names]
    tool_to_index = {name: index for index, name in enumerate(tool_names)}
    bm25 = bm25_type([description.lower().split() for description in tool_descriptions])

    queries: list[dict[str, Any]] = []
    for entry in entries:
        if entry["correct_tool"] not in tool_to_index:
            continue
        scores = bm25.get_scores(entry["text"].lower().split())
        ranked = sorted(enumerate(scores), key=lambda item: -item[1])
        gold_index = tool_to_index[entry["correct_tool"]]
        gold_rank = next(
            rank
            for rank, (tool_index, _) in enumerate(ranked, start=1)
            if tool_index == gold_index
        )
        queries.append(
            {
                "query_id": entry["query_id"],
                "text": entry["text"],
                "rel": {gold_index},
                "R_q": 1,
                "correct_tool": entry["correct_tool"],
                "ranked": ranked,
                "gold_rank": gold_rank,
            }
        )
    if len({query["query_id"] for query in queries}) != len(queries):
        raise ValueError("query IDs are not unique")
    return queries, len(tool_names)


class Environment:
    def __init__(
        self,
        queries: list[dict[str, Any]],
        corpus_size: int,
        *,
        delta_k: int = 1,
        max_k: int = 100,
    ) -> None:
        self.queries = queries
        self.corpus_size = corpus_size
        self.delta_k = delta_k
        self.max_k = max_k
        self.query: dict[str, Any]
        self.k = 0
        self.found = False
        self.top_score = 0.0
        self.gap = 0.0
        self.score_std = 0.0

    def new_query(self) -> np.ndarray:
        self.query = random.choice(self.queries)
        self.k = 0
        self.found = False
        self.top_score = 0.0
        self.gap = 0.0
        self.score_std = 0.0
        return self.state()

    def step(
        self, action: int
    ) -> tuple[np.ndarray, dict[str, Any] | None, bool]:
        if action == 0:
            return self.state(), self.reward(), True
        self.k = min(self.k + self.delta_k, self.max_k)
        ranked = self.query["ranked"][: self.k]
        self.found = any(index in self.query["rel"] for index, _ in ranked)
        if ranked:
            scores = [score for _, score in ranked]
            self.top_score = float(scores[0])
            top_three = scores[: min(3, len(scores))]
            rest = scores[min(3, len(scores)) : min(10, len(scores))]
            self.gap = float(np.mean(top_three) - np.mean(rest)) if rest else 0.0
            self.score_std = float(np.std(scores))
        if self.k >= self.max_k:
            return self.state(), self.reward(), True
        return self.state(), None, False

    def random_probability(self, k: int) -> float:
        relevant = self.query["R_q"]
        if k >= self.corpus_size or relevant >= self.corpus_size:
            return 1.0
        probability = 1 - math.comb(
            self.corpus_size - relevant, k
        ) / math.comb(self.corpus_size, k)
        return max(1e-12, probability)

    def state(self) -> np.ndarray:
        k = max(self.k, 1)
        chance = self.random_probability(k)
        ceiling = -math.log2(chance)
        expected_relevant = k * self.query["R_q"] / self.corpus_size
        return np.array(
            [
                self.k / self.max_k,
                self.top_score / 15.0,
                self.gap / 5.0,
                self.score_std / 5.0,
                min(expected_relevant, 5.0) / 5.0,
                min(ceiling, 10.0) / 10.0,
                float(self.found),
            ],
            dtype=np.float32,
        )

    def reward(self) -> dict[str, Any]:
        k = max(self.k, 1)
        chance = self.random_probability(k)
        return {
            "bor": -math.log2(chance) if self.found else 0.0,
            "f1": 1.0 if self.found else 0.0,
            "p_rand": chance,
            "k": k,
            "found": self.found,
            "R_q": self.query["R_q"],
        }


class DQN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(7, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.net(features)


class ReplayBuffer:
    def __init__(self, capacity: int = 20_000) -> None:
        self.buffer: deque[tuple[Any, ...]] = deque(maxlen=capacity)

    def push(self, *values: Any) -> None:
        self.buffer.append(values)

    def sample(
        self, size: int
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        batch = random.sample(self.buffer, min(size, len(self.buffer)))
        states, actions, rewards, next_states, done = zip(*batch)
        return (
            torch.FloatTensor(np.array(states)),
            torch.LongTensor(actions),
            torch.FloatTensor(rewards),
            torch.FloatTensor(np.array(next_states)),
            torch.FloatTensor(done),
        )

    def __len__(self) -> int:
        return len(self.buffer)


def train_dqn(
    environment: Environment,
    reward_key: str,
    seed: int,
    *,
    episodes: int,
    step_cost: float = 0.005,
    batch_size: int = 64,
    gamma: float = 0.95,
) -> DQN:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    policy = DQN()
    target = DQN()
    target.load_state_dict(policy.state_dict())
    optimizer = optim.Adam(policy.parameters(), lr=1e-3)
    replay = ReplayBuffer()
    epsilon = 0.5
    for episode in range(episodes):
        if episode > episodes * 0.7:
            epsilon = 0.03
        elif episode > episodes * 0.4:
            epsilon = 0.1
        state = environment.new_query()
        while True:
            if random.random() < epsilon:
                action = random.randint(0, 1)
            else:
                with torch.no_grad():
                    action = (
                        policy(torch.FloatTensor(state).unsqueeze(0))
                        .argmax(1)
                        .item()
                    )
            next_state, terminal_reward, done = environment.step(action)
            reward = terminal_reward[reward_key] if done else -step_cost
            replay.push(state, action, reward, next_state, float(done))
            state = next_state
            if len(replay) >= batch_size:
                (
                    state_batch,
                    action_batch,
                    reward_batch,
                    next_state_batch,
                    done_batch,
                ) = replay.sample(batch_size)
                current_q = (
                    policy(state_batch)
                    .gather(1, action_batch.unsqueeze(1))
                    .squeeze(1)
                )
                with torch.no_grad():
                    target_q = reward_batch + gamma * target(next_state_batch).max(1)[
                        0
                    ] * (1 - done_batch)
                loss = nn.MSELoss()(current_q, target_q)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            if done:
                break
        if episode % 500 == 0:
            target.load_state_dict(policy.state_dict())
        if (episode + 1) % 5000 == 0:
            print(
                f"training reward={reward_key} seed={seed} "
                f"episode={episode + 1}/{episodes}",
                flush=True,
            )
    return policy


def evaluate_policy(
    policy: DQN,
    queries: list[dict[str, Any]],
    corpus_size: int,
    policy_name: str,
    seed: int,
) -> list[dict[str, Any]]:
    environment = Environment(
        queries, corpus_size, delta_k=1, max_k=min(corpus_size, 100)
    )
    rows: list[dict[str, Any]] = []
    for query in queries:
        environment.queries = [query]
        state = environment.new_query()
        while True:
            with torch.no_grad():
                action = (
                    policy(torch.FloatTensor(state).unsqueeze(0)).argmax(1).item()
                )
            next_state, reward, done = environment.step(action)
            if done:
                assert reward is not None
                rows.append(make_row(query, corpus_size, policy_name, seed, reward))
                break
            state = next_state
    return rows


def evaluate_fixed(
    queries: list[dict[str, Any]], corpus_size: int, target_k: int
) -> list[dict[str, Any]]:
    environment = Environment(
        queries, corpus_size, delta_k=1, max_k=min(corpus_size, 100)
    )
    rows: list[dict[str, Any]] = []
    for query in queries:
        environment.queries = [query]
        environment.new_query()
        for _ in range(target_k):
            environment.step(1)
        _, reward, _ = environment.step(0)
        assert reward is not None
        rows.append(make_row(query, corpus_size, f"fk_{target_k}", None, reward))
    return rows


def make_row(
    query: dict[str, Any],
    corpus_size: int,
    policy: str,
    seed: int | None,
    reward: dict[str, Any],
) -> dict[str, Any]:
    k = int(reward["k"])
    hit = bool(reward["found"])
    return {
        "query_id": query["query_id"],
        "policy": policy,
        "seed": seed,
        "gold_rank": int(query["gold_rank"]),
        "k": k,
        "n": corpus_size,
        "hit": hit,
        "target_reward": float(reward["bor"]),
        "chance_probability": float(reward["p_rand"]),
    }


def group_key(row: dict[str, Any]) -> tuple[str, int | None]:
    return str(row["policy"]), row["seed"]


def aggregate_rows(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    materialized = list(rows)
    hits = np.array([float(row["hit"]) for row in materialized], dtype=np.float64)
    depths = np.array([float(row["k"]) for row in materialized], dtype=np.float64)
    chance = np.array(
        [float(row["k"]) / float(row["n"]) for row in materialized],
        dtype=np.float64,
    )
    target = np.array(
        [float(row["target_reward"]) for row in materialized], dtype=np.float64
    )
    direct_notebook = hits * -np.log2(chance)
    observed = float(hits.mean())
    random_baseline = float(chance.mean())
    defined = math.log2(observed / random_baseline) if observed > 0 else None
    return {
        "query_count": len(materialized),
        "found_fraction": observed,
        "mean_k": float(depths.mean()),
        "std_k": float(depths.std()),
        "notebook_statistic": float(target.mean()),
        "notebook_direct_recompute": float(direct_notebook.mean()),
        "defined_bor": defined,
        "mean_random_baseline": random_baseline,
    }


def summarize_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, int | None], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[group_key(row)].append(row)
    summaries: list[dict[str, Any]] = []
    for (policy, seed), group in sorted(
        groups.items(), key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1])
    ):
        summaries.append({"policy": policy, "seed": seed, **aggregate_rows(group)})
    return summaries


def summaries_by_seed(
    group_summaries: list[dict[str, Any]],
) -> dict[int, dict[str, dict[str, Any]]]:
    fixed = {
        summary["policy"]: summary
        for summary in group_summaries
        if summary["seed"] is None
    }
    result: dict[int, dict[str, dict[str, Any]]] = {}
    for seed in SEEDS:
        result[seed] = dict(fixed)
        for summary in group_summaries:
            if summary["seed"] == seed:
                result[seed][summary["policy"]] = summary
    return result


def sign(value: float, tolerance: float = 1e-12) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def pairwise_reversals(
    group_summaries: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    reversals: list[dict[str, Any]] = []
    maxima: list[dict[str, Any]] = []
    for seed, policies in summaries_by_seed(group_summaries).items():
        names = sorted(policies)
        for left_index, left in enumerate(names):
            for right in names[left_index + 1 :]:
                left_summary = policies[left]
                right_summary = policies[right]
                notebook_delta = (
                    left_summary["notebook_statistic"]
                    - right_summary["notebook_statistic"]
                )
                defined_delta = (
                    left_summary["defined_bor"] - right_summary["defined_bor"]
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


def paired_fixed_bootstrap(
    rows: list[dict[str, Any]],
    *,
    left_policy: str,
    right_policy: str,
    resamples: int,
    seed: int,
) -> dict[str, Any]:
    policy_rows: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        if row["policy"] in {left_policy, right_policy} and row["seed"] is None:
            policy_rows[row["policy"]][row["query_id"]] = row
    query_ids = sorted(set(policy_rows[left_policy]) & set(policy_rows[right_policy]))
    left = [policy_rows[left_policy][query_id] for query_id in query_ids]
    right = [policy_rows[right_policy][query_id] for query_id in query_ids]
    generator = np.random.default_rng(seed)
    notebook_deltas = np.empty(resamples, dtype=np.float64)
    defined_deltas = np.empty(resamples, dtype=np.float64)
    for index in range(resamples):
        sample = generator.integers(0, len(query_ids), size=len(query_ids))
        left_sample = [left[item] for item in sample]
        right_sample = [right[item] for item in sample]
        left_metrics = aggregate_rows(left_sample)
        right_metrics = aggregate_rows(right_sample)
        notebook_deltas[index] = (
            left_metrics["notebook_statistic"]
            - right_metrics["notebook_statistic"]
        )
        defined_deltas[index] = (
            left_metrics["defined_bor"] - right_metrics["defined_bor"]
        )
    return {
        "left_policy": left_policy,
        "right_policy": right_policy,
        "query_count": len(query_ids),
        "resamples": resamples,
        "seed": seed,
        "notebook_delta_left_minus_right": {
            "observed": aggregate_rows(left)["notebook_statistic"]
            - aggregate_rows(right)["notebook_statistic"],
            "ci95": [
                float(np.quantile(notebook_deltas, 0.025)),
                float(np.quantile(notebook_deltas, 0.975)),
            ],
            "probability_positive": float(np.mean(notebook_deltas > 0)),
            "probability_negative": float(np.mean(notebook_deltas < 0)),
        },
        "defined_delta_left_minus_right": {
            "observed": aggregate_rows(left)["defined_bor"]
            - aggregate_rows(right)["defined_bor"],
            "ci95": [
                float(np.quantile(defined_deltas, 0.025)),
                float(np.quantile(defined_deltas, 0.975)),
            ],
            "probability_positive": float(np.mean(defined_deltas > 0)),
            "probability_negative": float(np.mean(defined_deltas < 0)),
        },
    }


def reproduction_deltas(
    group_summaries: list[dict[str, Any]],
) -> dict[str, Any]:
    learned: dict[str, list[dict[str, Any]]] = defaultdict(list)
    fixed: dict[str, dict[str, Any]] = {}
    for summary in group_summaries:
        if summary["seed"] is None:
            fixed[summary["policy"]] = summary
        else:
            learned[summary["policy"]].append(summary)
    report: dict[str, Any] = {"learned": {}, "fixed": {}}
    for policy in ("bor_dqn", "f1_dqn"):
        observed_k = float(np.mean([item["mean_k"] for item in learned[policy]]))
        observed_found = float(
            np.mean([item["found_fraction"] for item in learned[policy]])
        )
        reference = OFFICIAL_REFERENCE[policy]
        report["learned"][policy] = {
            "observed_mean_k": observed_k,
            "official_mean_k": reference["mean_k"],
            "absolute_k_delta": abs(observed_k - reference["mean_k"]),
            "observed_found_fraction": observed_found,
            "official_found_fraction": reference["found_fraction"],
            "absolute_found_delta": abs(
                observed_found - reference["found_fraction"]
            ),
        }
    for policy, reference_found in OFFICIAL_REFERENCE[
        "fixed_found_fraction"
    ].items():
        observed = fixed[policy]["found_fraction"]
        report["fixed"][policy] = {
            "observed_found_fraction": observed,
            "official_found_fraction": reference_found,
            "absolute_found_delta": abs(observed - reference_found),
        }
    return report


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(
                json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
            )


def development_run(arguments: argparse.Namespace) -> dict[str, Any]:
    bm25_type = load_bm25(arguments.rank_bm25_wheel)
    queries, corpus_size = load_queries(arguments.input, bm25_type)
    random.seed(SEEDS[0])
    random.shuffle(queries)
    split_index = int(len(queries) * 0.7)
    train_queries = queries[:split_index]
    test_queries = queries[split_index:]
    max_k = min(corpus_size, 100)
    rows: list[dict[str, Any]] = []
    for fixed_k in FIXED_KS:
        if fixed_k <= max_k:
            rows.extend(evaluate_fixed(test_queries, corpus_size, fixed_k))

    models_dir = arguments.output_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=False)
    for seed in SEEDS:
        for policy_name, reward_key in (
            ("bor_dqn", "bor"),
            ("f1_dqn", "f1"),
        ):
            environment = Environment(
                train_queries, corpus_size, delta_k=1, max_k=max_k
            )
            policy = train_dqn(
                environment,
                reward_key,
                seed,
                episodes=arguments.episodes,
            )
            model_path = models_dir / f"{policy_name}_seed{seed}.pt"
            torch.save(policy.state_dict(), model_path)
            rows.extend(
                evaluate_policy(
                    policy,
                    test_queries,
                    corpus_size,
                    policy_name,
                    seed,
                )
            )

    split_manifest = {
        "split_seed": SEEDS[0],
        "train_fraction": 0.7,
        "train_query_ids": [query["query_id"] for query in train_queries],
        "test_query_ids": [query["query_id"] for query in test_queries],
    }
    write_json(arguments.output_dir / "split_manifest.json", split_manifest)
    return finalize(arguments, rows, corpus_size, len(queries))


def confirmation_run(arguments: argparse.Namespace) -> dict[str, Any]:
    bm25_type = load_bm25(arguments.rank_bm25_wheel)
    queries, corpus_size = load_queries(arguments.input, bm25_type)
    max_k = min(corpus_size, 100)
    rows: list[dict[str, Any]] = []
    for fixed_k in FIXED_KS:
        if fixed_k <= max_k:
            rows.extend(evaluate_fixed(queries, corpus_size, fixed_k))
    for seed in SEEDS:
        for policy_name in ("bor_dqn", "f1_dqn"):
            model_path = arguments.model_dir / f"{policy_name}_seed{seed}.pt"
            policy = DQN()
            policy.load_state_dict(
                torch.load(model_path, map_location="cpu", weights_only=True)
            )
            policy.eval()
            rows.extend(
                evaluate_policy(policy, queries, corpus_size, policy_name, seed)
            )
    return finalize(arguments, rows, corpus_size, len(queries))


def finalize(
    arguments: argparse.Namespace,
    rows: list[dict[str, Any]],
    corpus_size: int,
    query_count: int,
) -> dict[str, Any]:
    group_summaries = summarize_groups(rows)
    reversals, maxima = pairwise_reversals(group_summaries)
    bootstrap = paired_fixed_bootstrap(
        rows,
        left_policy="fk_3",
        right_policy="fk_1",
        resamples=arguments.bootstrap_resamples,
        seed=arguments.bootstrap_seed,
    )
    summary: dict[str, Any] = {
        "schema_version": 1,
        "phase": arguments.phase,
        "input_path": str(arguments.input.resolve()),
        "input_sha256": sha256_path(arguments.input),
        "input_line_sha256s": line_sha256s(arguments.input),
        "rank_bm25_wheel_path": str(arguments.rank_bm25_wheel.resolve()),
        "rank_bm25_wheel_sha256": sha256_path(arguments.rank_bm25_wheel),
        "corpus_size": corpus_size,
        "query_count": query_count,
        "row_count": len(rows),
        "episodes": arguments.episodes if arguments.phase == "development" else None,
        "seeds": list(SEEDS),
        "fixed_ks": [value for value in FIXED_KS if value <= min(corpus_size, 100)],
        "group_summaries": group_summaries,
        "strict_pairwise_reversals": reversals,
        "per_seed_maxima": maxima,
        "fk3_minus_fk1_bootstrap": bootstrap,
        "policy_row_counts": {
            f"{policy}:{seed}": count
            for (policy, seed), count in sorted(
                Counter(group_key(row) for row in rows).items(),
                key=lambda item: (
                    item[0][0],
                    -1 if item[0][1] is None else item[0][1],
                ),
            )
        },
    }
    if arguments.phase == "development":
        summary["official_reproduction"] = reproduction_deltas(group_summaries)
    write_rows(arguments.output_dir / "raw_rows.jsonl", rows)
    write_json(arguments.output_dir / "summary.json", summary)
    return summary


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--rank-bm25-wheel", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path)
    parser.add_argument("--episodes", type=int, default=15_000)
    parser.add_argument("--bootstrap-resamples", type=int, default=20_000)
    parser.add_argument("--bootstrap-seed", type=int, default=20_260_723)
    arguments = parser.parse_args()
    if arguments.phase == "confirmation" and arguments.model_dir is None:
        parser.error("--model-dir is required for confirmation")
    return arguments


def main() -> int:
    arguments = parse_arguments()
    started = time.perf_counter()
    arguments.output_dir.mkdir(parents=True, exist_ok=False)
    summary = (
        development_run(arguments)
        if arguments.phase == "development"
        else confirmation_run(arguments)
    )
    print(
        json.dumps(
            {
                "phase": arguments.phase,
                "query_count": summary["query_count"],
                "row_count": summary["row_count"],
                "strict_reversal_count": len(
                    summary["strict_pairwise_reversals"]
                ),
                "elapsed_seconds": time.perf_counter() - started,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
