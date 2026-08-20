import argparse
import json
from collections import defaultdict
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def safe_rate(numerator, denominator):
    return numerator / denominator if denominator else None


def condition_summary(rows):
    scorable = [row for row in rows if row.get("permission") in {"allowed", "blocked"}]
    correct = [
        row for row in scorable
        if row["permission"] == row["expected_permission"]
    ]
    proceed = [row for row in scorable if row["expected_permission"] == "allowed"]
    hold = [row for row in scorable if row["expected_permission"] == "blocked"]
    return {
        "n_total": len(rows),
        "n_scorable": len(scorable),
        "n_correct": len(correct),
        "accuracy": safe_rate(len(correct), len(scorable)),
        "proceed_accuracy": safe_rate(
            sum(row["permission"] == "allowed" for row in proceed), len(proceed)
        ),
        "hold_accuracy": safe_rate(
            sum(row["permission"] == "blocked" for row in hold), len(hold)
        ),
        "parse_or_infrastructure_errors": len(rows) - len(scorable),
    }


def main():
    args = parse_args()
    inputs = json.loads(args.inputs.read_text(encoding="utf-8"))
    results = json.loads(args.results.read_text(encoding="utf-8"))
    by_condition = defaultdict(list)
    by_case = defaultdict(dict)
    for row in results["results"]:
        by_condition[row["condition"]].append(row)
        by_case[row["scenario_id"]][row["condition"]] = row

    transitions = defaultdict(int)
    transition_rows = []
    for scenario_id, pair in sorted(by_case.items()):
        canonical = pair.get("canonical", {}).get("permission")
        preserved = pair.get("payload_preserving", {}).get("permission")
        expected = pair.get("canonical", pair.get("payload_preserving", {})).get(
            "expected_permission"
        )
        if canonical not in {"allowed", "blocked"} or preserved not in {
            "allowed",
            "blocked",
        }:
            continue
        canonical_correct = canonical == expected
        preserved_correct = preserved == expected
        if not canonical_correct and preserved_correct:
            label = "wrong_to_correct"
        elif canonical_correct and not preserved_correct:
            label = "correct_to_wrong"
        elif canonical != preserved:
            label = "wrong_to_other_wrong"
        else:
            label = "unchanged"
        transitions[label] += 1
        if label != "unchanged":
            transition_rows.append(
                {
                    "scenario_id": scenario_id,
                    "expected": expected,
                    "canonical": canonical,
                    "payload_preserving": preserved,
                    "transition": label,
                }
            )

    output = {
        "schema_version": "crl.evidence_transport_probe_analysis.v1",
        "model": results["model"],
        "selection_rule": inputs["selection_rule"],
        "corpus_audit": inputs["corpus_audit"],
        "condition_summaries": {
            condition: condition_summary(rows)
            for condition, rows in sorted(by_condition.items())
        },
        "paired_transitions": dict(sorted(transitions.items())),
        "changed_cases": transition_rows,
        "interpretation_boundary": (
            "Post-hoc mechanism probe on 20 public scenarios and one local model. "
            "It is not a preregistered benchmark result and does not estimate deployment prevalence."
        ),
    }
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

