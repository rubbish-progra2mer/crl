#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from retrieval import (
    RetrievalIndex,
    load_or_build_families,
    ranking_to_columns,
    reciprocal_rank_fusion,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENCHMARK = ROOT / "benchmark" / "OADD-Bench" / "OADD_Bench.csv"
DEFAULT_METADATA = ROOT / "benchmark" / "HRS_metadata" / "metadata.jsonl"
DEFAULT_FIXES = ROOT / "benchmark" / "HRS_metadata" / "metadata_fixes.jsonl"
DEFAULT_CACHE = ROOT / "cache"


def load_cases(path: Path, limit: int | None = None) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    cases = []
    for row in rows[:limit]:
        targets = [value.strip() for value in row["hrs_column_ids"].split(";") if value.strip()]
        cases.append(
            {
                "record_id": row["record_id"],
                "question": row["research_question"],
                "years": {
                    value.strip()
                    for value in row["allowed_years"].split(";")
                    if value.strip()
                },
                "target_size": len(targets),
            }
        )
    return cases


def rank(
    method: str,
    index: RetrievalIndex,
    questions: list[str],
    top_k: int,
) -> list[list[int]]:
    if method == "bm25":
        return index.bm25(questions, top_k)
    if method == "tfidf":
        return index.tfidf(questions, top_k)
    if method == "bge-base":
        return index.bge(questions, top_k)
    if method == "splade++":
        return index.splade(questions, top_k)
    if method == "rank-fusion":
        source_rankings = [
            index.bm25(questions, top_k),
            index.tfidf(questions, top_k),
            index.bge(questions, top_k),
            index.splade(questions, top_k),
        ]
        return [
            reciprocal_rank_fusion(
                [source[case_index] for source in source_rankings], top_k
            )
            for case_index in range(len(questions))
        ]
    raise ValueError(method)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run question-only retrieval methods on OADD-Bench."
    )
    parser.add_argument(
        "--method",
        choices=("bm25", "tfidf", "bge-base", "splade++", "rank-fusion"),
        required=True,
    )
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--metadata-fixes", type=Path, default=DEFAULT_FIXES)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--provider", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--top-k", type=int, default=1000)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    if not args.metadata.exists():
        raise FileNotFoundError(
            f"Missing {args.metadata}. Run benchmark/HRS_metadata/prepare_metadata.py first."
        )
    cases = load_cases(args.benchmark, args.limit)
    families, fingerprint = load_or_build_families(
        args.metadata,
        args.metadata_fixes,
        args.cache_dir,
    )
    print(
        json.dumps(
            {
                "stage": "catalog",
                "families": len(families),
                "fingerprint": fingerprint,
            }
        ),
        flush=True,
    )
    index = RetrievalIndex(families, fingerprint, args.cache_dir, args.provider)
    rankings = rank(
        args.method,
        index,
        [case["question"] for case in cases],
        args.top_k,
    )

    output = args.output or ROOT / "results" / f"{args.method}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for case, ranking in zip(cases, rankings, strict=True):
            columns = ranking_to_columns(
                ranking,
                families,
                case["years"],
                5 * case["target_size"],
            )
            predictions = {
                str(multiplier): columns[: multiplier * case["target_size"]]
                for multiplier in (1, 2, 5)
            }
            handle.write(
                json.dumps(
                    {"record_id": case["record_id"], "predictions": predictions}
                )
                + "\n"
            )
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
