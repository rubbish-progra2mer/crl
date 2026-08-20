from __future__ import annotations

import argparse
import json
import math
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


@dataclass(frozen=True)
class Turn:
    session_id: str
    turn_index: int
    text: str

    @property
    def key(self) -> tuple[str, int]:
        return (self.session_id, self.turn_index)


@dataclass
class RetrievalState:
    seen_sessions: set[str] = field(default_factory=set)
    seen_hit_turns: set[tuple[str, int]] = field(default_factory=set)
    observed_turns: set[tuple[str, int]] = field(default_factory=set)


def expanded_keys(
    turn: Turn, session_lengths: dict[str, int], window_radius: int
) -> set[tuple[str, int]]:
    lower = max(0, turn.turn_index - window_radius)
    upper = min(session_lengths[turn.session_id] - 1, turn.turn_index + window_radius)
    return {(turn.session_id, i) for i in range(lower, upper + 1)}


def eligible(
    turn: Turn,
    mode: str,
    state: RetrievalState,
    session_lengths: dict[str, int],
    window_radius: int,
) -> bool:
    if mode == "session":
        return turn.session_id not in state.seen_sessions
    if mode == "none":
        return True
    if mode == "hit_turn":
        return turn.key not in state.seen_hit_turns
    if mode == "observed_interval":
        window = expanded_keys(turn, session_lengths, window_radius)
        return bool(window - state.observed_turns)
    raise ValueError(f"unknown mode: {mode}")


def bm25_scores(query: str, candidates: list[Turn]) -> dict[tuple[str, int], float]:
    query_terms = tokenize(query)
    documents = {turn.key: tokenize(turn.text) for turn in candidates}
    if not documents:
        return {}

    document_count = len(documents)
    average_length = sum(len(tokens) for tokens in documents.values()) / document_count
    document_frequency: Counter[str] = Counter()
    for tokens in documents.values():
        document_frequency.update(set(tokens))

    k1 = 1.2
    b = 0.75
    scores: dict[tuple[str, int], float] = {}
    for key, tokens in documents.items():
        frequencies = Counter(tokens)
        score = 0.0
        for term in query_terms:
            frequency = frequencies[term]
            if frequency == 0:
                continue
            df = document_frequency[term]
            inverse_document_frequency = math.log(1.0 + (document_count - df + 0.5) / (df + 0.5))
            denominator = frequency + k1 * (
                1.0 - b + b * len(tokens) / max(average_length, 1.0)
            )
            score += inverse_document_frequency * frequency * (k1 + 1.0) / denominator
        if score > 0.0:
            scores[key] = score
    return scores


def rank_with_ties_broken(items: list[tuple[object, float]]) -> dict[object, int]:
    ordered = sorted(items, key=lambda item: (-item[1], str(item[0])))
    return {key: rank for rank, (key, _) in enumerate(ordered, start=1)}


def search(
    query: str,
    turns: list[Turn],
    session_lengths: dict[str, int],
    state: RetrievalState,
    mode: str,
    window_radius: int,
    top_k: int,
) -> dict[str, object]:
    candidates = [
        turn
        for turn in turns
        if eligible(turn, mode, state, session_lengths, window_radius)
    ]
    scores = bm25_scores(query, candidates)
    turn_by_key = {turn.key: turn for turn in candidates}

    turn_ranks = rank_with_ties_broken(list(scores.items()))
    session_scores: dict[str, float] = defaultdict(float)
    for key, score in scores.items():
        session_scores[key[0]] += score
    session_ranks = rank_with_ties_broken(list(session_scores.items()))

    fused: list[tuple[tuple[str, int], float]] = []
    for key in scores:
        fused_score = 1.0 / (60 + turn_ranks[key]) + 1.0 / (
            60 + session_ranks[key[0]]
        )
        fused.append((key, fused_score))
    fused.sort(key=lambda item: (-item[1], item[0]))
    hit_keys = [key for key, _ in fused[:top_k]]

    windows: list[set[tuple[str, int]]] = []
    for key in hit_keys:
        hit = turn_by_key[key]
        window = expanded_keys(hit, session_lengths, window_radius)
        windows.append(window)
        state.seen_sessions.add(hit.session_id)
        state.seen_hit_turns.add(hit.key)
        state.observed_turns.update(window)

    return {
        "query": query,
        "hit_keys": [[session, index] for session, index in hit_keys],
        "window_keys": [
            [[session, index] for session, index in sorted(window)] for window in windows
        ],
    }


def build_archive(seed: int) -> tuple[list[Turn], dict[str, int], dict[str, object]]:
    rng = random.Random(seed)
    vocabulary = [
        "meeting",
        "project",
        "garden",
        "coffee",
        "budget",
        "museum",
        "weather",
        "recipe",
        "travel",
        "report",
        "calendar",
        "design",
    ]
    query_one = f"first_marker_{seed}"
    query_two = f"second_marker_{seed}"
    first_position = rng.randint(2, 5)
    second_position = rng.randint(17, 21)

    turns: list[Turn] = []
    target_session = f"target_{seed}"
    target_length = 24
    for index in range(target_length):
        words = rng.sample(vocabulary, 4)
        if index == first_position:
            words.extend([query_one, "first", "evidence"])
        if index == second_position:
            words.extend([query_two, "second", "evidence"])
        turns.append(Turn(target_session, index, " ".join(words)))

    session_lengths = {target_session: target_length}
    for session_number in range(12):
        session_id = f"distractor_{seed}_{session_number}"
        length = rng.randint(8, 14)
        session_lengths[session_id] = length
        for index in range(length):
            words = rng.sample(vocabulary, 5)
            words.append(f"noise_{session_number}_{index}")
            turns.append(Turn(session_id, index, " ".join(words)))

    rng.shuffle(turns)
    metadata = {
        "target_session": target_session,
        "query_one": query_one,
        "query_two": query_two,
        "first_position": first_position,
        "second_position": second_position,
    }
    return turns, session_lengths, metadata


def run_seed(seed: int, mode: str, window_radius: int, top_k: int) -> dict[str, object]:
    turns, session_lengths, metadata = build_archive(seed)
    state = RetrievalState()
    first = search(
        str(metadata["query_one"]),
        turns,
        session_lengths,
        state,
        mode,
        window_radius,
        top_k,
    )
    observed_after_first = set(state.observed_turns)
    second = search(
        str(metadata["query_two"]),
        turns,
        session_lengths,
        state,
        mode,
        window_radius,
        top_k,
    )
    third = search(
        str(metadata["query_one"]),
        turns,
        session_lengths,
        state,
        mode,
        window_radius,
        top_k,
    )

    target_session = str(metadata["target_session"])
    first_key = [target_session, int(metadata["first_position"])]
    second_key = [target_session, int(metadata["second_position"])]
    third_windows = [
        {(session, int(index)) for session, index in window}
        for window in third["window_keys"]
    ]
    fully_covered_repeat = any(
        bool(window) and window.issubset(observed_after_first) for window in third_windows
    )

    return {
        "seed": seed,
        "mode": mode,
        "first_target_retrieved": first_key in first["hit_keys"],
        "second_target_retrieved": second_key in second["hit_keys"],
        "third_fully_covered_repeat": fully_covered_repeat,
        "unique_observed_turns": len(state.observed_turns),
        "metadata": metadata,
        "rounds": [first, second, third],
    }


def aggregate(results: list[dict[str, object]]) -> dict[str, object]:
    count = len(results)
    return {
        "seeds": count,
        "first_target_recall": sum(bool(row["first_target_retrieved"]) for row in results)
        / count,
        "second_target_recall": sum(bool(row["second_target_retrieved"]) for row in results)
        / count,
        "third_fully_covered_repeat_rate": sum(
            bool(row["third_fully_covered_repeat"]) for row in results
        )
        / count,
        "mean_unique_observed_turns": sum(
            int(row["unique_observed_turns"]) for row in results
        )
        / count,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    modes = ["session", "none", "hit_turn", "observed_interval"]
    all_results = {
        mode: [run_seed(seed, mode, window_radius=2, top_k=5) for seed in range(101)]
        for mode in modes
    }
    aggregates = {mode: aggregate(rows) for mode, rows in all_results.items()}

    assertions = {
        "session_loses_second_target_all_seeds": all(
            not row["second_target_retrieved"] for row in all_results["session"]
        ),
        "fine_grained_modes_recover_second_target_all_seeds": all(
            row["second_target_retrieved"]
            for mode in ["none", "hit_turn", "observed_interval"]
            for row in all_results[mode]
        ),
        "observed_interval_suppresses_covered_repeat_all_seeds": all(
            not row["third_fully_covered_repeat"]
            for row in all_results["observed_interval"]
        ),
        "no_dedup_repeats_covered_window_all_seeds": all(
            row["third_fully_covered_repeat"] for row in all_results["none"]
        ),
    }

    payload = {
        "experiment": "refind-dedup-granularity-counterexample",
        "configuration": {
            "seeds": list(range(101)),
            "window_radius": 2,
            "top_k": 5,
            "target_session_turns": 24,
            "distractor_sessions": 12,
            "query_protocol": ["first evidence", "second evidence", "first evidence again"],
            "retrieval": "turn-level BM25 plus session-sum RRF",
        },
        "aggregates": aggregates,
        "assertions": assertions,
        "all_registered_assertions_pass": all(assertions.values()),
        "per_seed": all_results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"aggregates": aggregates, "assertions": assertions}, indent=2))


if __name__ == "__main__":
    main()
