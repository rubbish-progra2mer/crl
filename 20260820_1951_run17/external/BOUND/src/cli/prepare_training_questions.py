"""Sample training questions from multiple sources without evaluation overlap."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from jsonl_io import read_jsonl, write_jsonl


def _parse_named_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected NAME=PATH")
    name, path = value.split("=", 1)
    return name, Path(path)


def _key(row: dict) -> str:
    return " ".join(str(row["question"]).lower().split())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--existing",
        action="append",
        type=_parse_named_path,
        required=True,
        help="Existing question source in NAME=PATH format. May be specified multiple times.",
    )
    parser.add_argument(
        "--additional-questions",
        type=Path,
        help="Optional file containing additional training questions.",
    )
    parser.add_argument(
        "--evaluation",
        action="append",
        type=Path,
        default=[],
        help="Evaluation question file to exclude from training. May be specified multiple times.",
    )
    parser.add_argument(
        "--existing-per-dataset",
        type=int,
        required=True,
        help="Number of questions to sample from each existing source.",
    )
    parser.add_argument(
        "--additional-count",
        type=int,
        default=0,
        help="Number of questions to sample from the additional question file.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSONL file.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)

    evaluation_keys = {
        _key(row)
        for path in args.evaluation
        for row in read_jsonl(path)
    }

    selected = []
    selected_keys = set()

    # Sample from existing question sources.
    for dataset_name, path in args.existing:
        rows = [
            row
            for row in read_jsonl(path)
            if _key(row) not in evaluation_keys
        ]
        rng.shuffle(rows)

        count = 0
        for row in rows:
            if count >= args.existing_per_dataset:
                break

            key = _key(row)
            if key in selected_keys:
                continue

            selected_keys.add(key)
            selected.append(
                {
                    **row,
                    "training_source": dataset_name,
                }
            )
            count += 1

        if count < args.existing_per_dataset:
            raise ValueError(
                f"{dataset_name}: requested {args.existing_per_dataset} questions, "
                f"but only found {count} unique non-evaluation questions"
            )

    # Optionally sample from an additional question source.
    if args.additional_questions is not None and args.additional_count > 0:
        additional = [
            row
            for row in read_jsonl(args.additional_questions)
            if _key(row) not in evaluation_keys
        ]
        rng.shuffle(additional)

        count = 0
        for row in additional:
            if count >= args.additional_count:
                break

            key = _key(row)
            if key in selected_keys:
                continue

            selected_keys.add(key)
            selected.append(
                {
                    **row,
                    "training_source": "additional",
                }
            )
            count += 1

        if count < args.additional_count:
            raise ValueError(
                f"requested {args.additional_count} additional questions, "
                f"but only found {count} unique non-evaluation questions"
            )

    rng.shuffle(selected)

    write_jsonl(args.output, selected)
    print(f"wrote {len(selected)} training questions")


if __name__ == "__main__":
    main()