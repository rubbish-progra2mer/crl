#!/usr/bin/env python3
"""Summarize direct pair-judge results."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report: dict[str, Any] = {"results": []}
    for path in args.results:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data["rows"]
        scorable = [row for row in rows if row["response"].get("ok")]
        positives = [row for row in scorable if row["gold"] == "DIFFERENT"]
        negatives = [row for row in scorable if row["gold"] == "SAME"]
        by_group: dict[str, list[bool]] = defaultdict(list)
        errors = []
        for row in scorable:
            correct = row["response"]["decision"] == row["gold"]
            by_group[f"cell={row['cell']}"] .append(correct)
            by_group[f"subclass={row['subclass']}"] .append(correct)
            if not correct:
                errors.append({"id": row["id"], "gold": row["gold"], "prediction": row["response"]["decision"], "reason": row["response"].get("parsed", {}).get("reason")})
        report["results"].append({
            "model": data["model"],
            "total": len(rows),
            "scorable": len(scorable),
            "accuracy": sum(row["response"]["decision"] == row["gold"] for row in scorable) / len(scorable) if scorable else None,
            "violation_recall": sum(row["response"]["decision"] == "DIFFERENT" for row in positives) / len(positives) if positives else None,
            "faithful_specificity": sum(row["response"]["decision"] == "SAME" for row in negatives) / len(negatives) if negatives else None,
            "group_accuracy": {key: sum(values) / len(values) for key, values in sorted(by_group.items())},
            "errors": errors,
        })
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")


if __name__ == "__main__":
    main()
