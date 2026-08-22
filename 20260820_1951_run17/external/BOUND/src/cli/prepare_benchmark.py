"""Download or normalize supported benchmark question files."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable

from jsonl_io import write_jsonl


BENCHMARKS = (
    "hotpotqa", "musique", "2wikimultihopqa", "bamboogle", "frames", "gaia", "browsecomp_plus"
)


def _answers(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value is None:
        return []
    text = str(value).strip()
    return [text] if text else []


def _standard_record(
    identifier: Any,
    question: Any,
    answers: Any,
    benchmark: str,
    split: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = {
        "id": "" if identifier is None else str(identifier).strip(),
        "question": "" if question is None else str(question).strip(),
        "answers": _answers(answers),
        "metadata": {"benchmark": benchmark, "split": split},
    }
    if extra:
        record["metadata"].update(extra)
    if not record["id"] or not record["question"] or not record["answers"]:
        raise ValueError(f"incomplete {benchmark} record: {record['id']!r}")
    return record

def _from_huggingface(name: str, split: str | None) -> Iterable[dict[str, Any]]:
    from datasets import load_dataset

    if name == "hotpotqa":
        selected_split = split or "validation"
        dataset = load_dataset("hotpotqa/hotpot_qa", "distractor", split=selected_split)
        for row in dataset:
            yield _standard_record(row["id"], row["question"], row["answer"], name, selected_split)
    elif name == "frames":
        selected_split = split or "test"
        dataset = load_dataset("google/frames-benchmark", split=selected_split)
        for index, row in enumerate(dataset):
            yield _standard_record(
                row.get("Unnamed: 0", index), row["Prompt"], row["Answer"], name, selected_split,
                {"reasoning_types": row.get("reasoning_types")},
            )
    elif name == "gaia":
        selected_split = split or "validation"
        dataset = load_dataset("gaia-benchmark/GAIA", "2023_all", split=selected_split)
        for row in dataset:
            if str(row.get("file_name", "")).strip():
                continue
            yield _standard_record(
                row["task_id"], row["Question"], row["Final answer"], name, selected_split,
                {"level": row.get("Level"), "text_only": True},
            )
    else:
        raise ValueError(f"{name} requires --source-path from its official release")


def _load_source(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    with path.open("r", encoding="utf-8") as handle:
        if path.suffix.lower() == ".jsonl":
            return [json.loads(line) for line in handle if line.strip()]
        value = json.load(handle)
    if isinstance(value, list):
        return value
    raise ValueError("source JSON must contain a list")


def _first(row: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    return None


def _from_source(name: str, split: str, path: Path) -> Iterable[dict[str, Any]]:
    for index, row in enumerate(_load_source(path)):
        identifier = _first(row, ("id", "_id", "query_id", "task_id", "ID"))
        question = _first(row, ("question", "query", "Question", "Question Text"))
        answers = _first(row, ("answers", "answer", "Answer", "Final answer"))
        yield _standard_record(identifier if identifier is not None else index, question, answers, name, split)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", required=True, choices=BENCHMARKS)
    parser.add_argument("--output", required=True)
    parser.add_argument("--split")
    parser.add_argument("--source-path", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.source_path:
        records = _from_source(args.benchmark, args.split or "official", args.source_path)
    else:
        records = _from_huggingface(args.benchmark, args.split)
    count = write_jsonl(args.output, records)
    print(f"wrote {count} normalized {args.benchmark} records")


if __name__ == "__main__":
    main()
