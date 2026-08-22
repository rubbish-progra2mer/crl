"""Build process-level preference data from normalized student rollouts."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, Iterable

from jsonl_io import read_jsonl, write_jsonl
from preferences import (
    construct_preferences,
    to_training_record,
    validate_training_record,
)
from teacher import Teacher


def filter_observable_state_conflicts(
    pairs: Iterable[Dict[str, Any]],
) -> list[Dict[str, Any]]:
    """Deduplicate pairs and remove every ambiguously labeled observable state."""

    unique_pairs = []
    seen_pairs = set()
    actions_by_state: dict[str, set[str]] = {}
    for pair in pairs:
        state_signature = json.dumps(
            pair["prompt"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        pair_signature = json.dumps(
            [pair["prompt"], pair["chosen"], pair["rejected"]],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        if pair_signature in seen_pairs:
            continue
        seen_pairs.add(pair_signature)
        unique_pairs.append((state_signature, pair))
        chosen_action = str(pair["chosen"]["action"])
        actions_by_state.setdefault(state_signature, set()).add(chosen_action)

    ambiguous_states = {
        state_signature
        for state_signature, actions in actions_by_state.items()
        if len(actions) > 1
    }
    return [
        pair
        for state_signature, pair in unique_pairs
        if state_signature not in ambiguous_states
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rollouts", required=True)
    parser.add_argument(
        "--output",
        required=True,
        help="Teacher-side preference records",
    )
    parser.add_argument(
        "--train-output",
        required=True,
        help="Brief-free DPO records",
    )
    parser.add_argument("--teacher-model", default="deepseek-v4-flash")
    parser.add_argument(
        "--teacher-base-url",
        default=os.getenv("TEACHER_BASE_URL"),
    )
    parser.add_argument(
        "--teacher-api-key",
        default=os.getenv("TEACHER_API_KEY"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    teacher = Teacher(
        args.teacher_model,
        args.teacher_base_url,
        args.teacher_api_key,
    )

    generated_pairs = []
    for rollout in read_jsonl(args.rollouts):
        generated_pairs.extend(construct_preferences(rollout, teacher))

    # The policy cannot distinguish identical observable states. Remove exact
    # duplicates, and delete every state that has conflicting chosen actions.
    pairs = filter_observable_state_conflicts(generated_pairs)

    training_records = [to_training_record(pair) for pair in pairs]
    for record in training_records:
        validate_training_record(record)

    write_jsonl(args.output, pairs)
    write_jsonl(args.train_output, training_records)
    print(f"wrote {len(pairs)} preference pairs")


if __name__ == "__main__":
    main()
