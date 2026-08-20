#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--benchmark", type=Path, default=Path("benchmark/OADD-Bench/OADD_Bench.csv"))
    args = parser.parse_args()

    with args.benchmark.open(newline="", encoding="utf-8") as handle:
        targets = {
            row["record_id"]: {code.strip().upper() for code in row["hrs_column_ids"].split(";")}
            for row in csv.DictReader(handle)
        }
    predictions = {
        row["record_id"]: row["predictions"]
        for row in (json.loads(line) for line in args.predictions.read_text(encoding="utf-8").splitlines())
    }

    summary = {}
    for budget in ("1", "2", "5"):
        recalls, hits, positives = [], 0, 0
        for record_id, target in targets.items():
            output = [code.strip().upper() for code in predictions[record_id][budget]]
            limit = int(budget) * len(target)
            if len(output) != len(set(output)) or len(output) > limit:
                raise ValueError(f"invalid output for {record_id} at {budget}R")
            overlap = len(target & set(output))
            recalls.append(overlap / len(target))
            hits += overlap
            positives += len(target)
        summary[f"recall@{budget}R"] = {
            "macro": sum(recalls) / len(recalls),
            "micro": hits / positives,
        }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
