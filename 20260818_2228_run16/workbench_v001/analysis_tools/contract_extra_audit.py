#!/usr/bin/env python3
"""Validate manual labels for Agent-Diff unmatched state changes.

The script does not assign scientific labels. It checks that a human-authored label
file covers the exact set produced by the frozen Formal attempt and summarizes the
result without converting it into a quality score.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    results = load_json(args.results)
    labels = load_json(args.labels)

    flagged = {
        item["test_id"]: item
        for item in results["actual_runs"]
        if item["passed"] and item.get("extras")
    }
    assigned: dict[str, str] = {}
    duplicates: list[str] = []
    for category, payload in labels["categories"].items():
        for test_id in payload["test_ids"]:
            if test_id in assigned:
                duplicates.append(test_id)
            assigned[test_id] = category

    missing = sorted(set(flagged) - set(assigned))
    unexpected = sorted(set(assigned) - set(flagged))
    if duplicates or missing or unexpected:
        raise SystemExit(
            "manual label coverage mismatch: "
            f"duplicates={duplicates}, missing={missing}, unexpected={unexpected}"
        )

    category_counts = Counter(assigned.values())
    service_counts = Counter(item["service"] for item in flagged.values())
    split_counts = Counter(item["split"] for item in flagged.values())
    category_by_service = Counter(
        (assigned[test_id], item["service"])
        for test_id, item in flagged.items()
    )
    passed_runs = [item for item in results["actual_runs"] if item["passed"]]
    suspicious_ids = labels["categories"]["task_external_suspicious"]["test_ids"]

    report = {
        "audit_id": labels["audit_id"],
        "coverage": {
            "formal_flagged_run_count": len(flagged),
            "labeled_run_count": len(assigned),
            "missing": missing,
            "unexpected": unexpected,
            "duplicates": duplicates,
        },
        "category_counts": dict(sorted(category_counts.items())),
        "service_counts": dict(sorted(service_counts.items())),
        "split_counts": dict(sorted(split_counts.items())),
        "category_by_service": {
            f"{category}|{service}": count
            for (category, service), count in sorted(category_by_service.items())
        },
        "score_sensitivity_facts": {
            "public_run_count": len(results["actual_runs"]),
            "original_passed_run_count": len(passed_runs),
            "global_strict_would_reject_original_passed_count": len(flagged),
            "manually_identified_task_external_suspicious_count": len(suspicious_ids),
            "observed_score_change_if_only_manually_suspicious_runs_were_rejected": 0,
        },
        "interpretation_boundary": (
            "The labels found no task-external suspicious effect in this checkpoint. "
            "This is an observed prompt/signature audit result, not proof of safety and "
            "not evidence that open-world contracts are generally adequate."
        ),
        "limitations": labels["limitations"],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
