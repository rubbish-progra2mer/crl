#!/usr/bin/env python3
"""Analyze source-compiled witness and direct-pair predictions."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def choice_map(call: dict[str, Any] | None) -> dict[str, int] | None:
    if not call or not call.get("ok") or not isinstance(call.get("parsed"), dict):
        return None
    choices = call["parsed"].get("choices")
    if not isinstance(choices, list):
        return None
    output: dict[str, int] = {}
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        witness_id = choice.get("id")
        option_index = choice.get("option_index")
        if isinstance(option_index, str) and option_index.strip().isdigit():
            option_index = int(option_index.strip())
        if isinstance(witness_id, str) and isinstance(option_index, int) and not isinstance(option_index, bool):
            output[witness_id] = option_index
    return output


def witness_prediction(row: dict[str, Any], strict: bool) -> tuple[str | None, int]:
    witnesses = row.get("validated_witnesses") or []
    root = choice_map(row.get("root_execution"))
    candidate = choice_map(row.get("candidate_execution"))
    if root is None or candidate is None:
        return None, 0
    valid: list[tuple[int, int]] = []
    for witness in witnesses:
        witness_id = witness["id"]
        if witness_id not in root or witness_id not in candidate:
            continue
        option_count = len(witness["options"])
        root_index = root[witness_id]
        candidate_index = candidate[witness_id]
        if not 0 <= root_index < option_count or not 0 <= candidate_index < option_count:
            continue
        if strict and root_index != witness["expected_index"]:
            continue
        valid.append((root_index, candidate_index))
    if not valid:
        return None, 0
    prediction = "DIFFERENT" if any(left != right for left, right in valid) else "SAME"
    return prediction, len(valid)


def direct_prediction(row: dict[str, Any]) -> str | None:
    call = row.get("direct_pair_judge") or {}
    if not call.get("ok") or not isinstance(call.get("parsed"), dict):
        return None
    decision = call["parsed"].get("decision")
    if isinstance(decision, str):
        decision = decision.strip().upper()
    return decision if decision in {"SAME", "DIFFERENT"} else None


def metrics(rows: list[dict[str, Any]], predictor) -> dict[str, Any]:
    records: list[tuple[dict[str, Any], str, int | None]] = []
    for row in rows:
        value = predictor(row)
        if isinstance(value, tuple):
            prediction, count = value
        else:
            prediction, count = value, None
        if prediction is not None:
            records.append((row, prediction, count))
    total = len(rows)
    scorable = len(records)
    correct = sum(prediction == row["gold"] for row, prediction, _ in records)
    positives = [(row, prediction) for row, prediction, _ in records if row["gold"] == "DIFFERENT"]
    negatives = [(row, prediction) for row, prediction, _ in records if row["gold"] == "SAME"]
    recall = sum(prediction == "DIFFERENT" for row, prediction in positives) / len(positives) if positives else None
    specificity = sum(prediction == "SAME" for row, prediction in negatives) / len(negatives) if negatives else None
    by_class: dict[str, list[bool]] = defaultdict(list)
    for row, prediction, _ in records:
        by_class[row["mutation_class"]].append(prediction == row["gold"])
    counts = [count for _, _, count in records if count is not None]
    return {
        "total": total,
        "scorable": scorable,
        "parse_rate": scorable / total if total else None,
        "accuracy_on_scorable": correct / scorable if scorable else None,
        "balanced_accuracy_on_scorable": (recall + specificity) / 2 if recall is not None and specificity is not None else None,
        "violation_recall": recall,
        "faithful_control_specificity": specificity,
        "mean_valid_witnesses": sum(counts) / len(counts) if counts else None,
        "class_accuracy": {key: sum(values) / len(values) for key, values in sorted(by_class.items())},
        "prediction_counts": dict(Counter(prediction for _, prediction, _ in records)),
    }


def resource_use(rows: list[dict[str, Any]]) -> dict[str, Any]:
    calls: list[dict[str, Any]] = []
    for row in rows:
        for key in ("compiler", "root_execution", "candidate_execution", "direct_pair_judge"):
            call = row.get(key)
            if isinstance(call, dict):
                calls.append(call)
    return {
        "attempted_calls": len(calls),
        "successful_calls": sum(bool(call.get("ok")) for call in calls),
        "wall_seconds_sum": round(sum(float(call.get("wall_seconds") or 0) for call in calls), 4),
        "prompt_tokens_sum": sum(int(call.get("prompt_eval_count") or 0) for call in calls),
        "generated_tokens_sum": sum(int(call.get("eval_count") or 0) for call in calls),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report: dict[str, Any] = {"results": []}
    for path in args.results:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        rows = data["rows"]
        case_predictions = []
        for row in rows:
            strict_prediction, strict_count = witness_prediction(row, True)
            lenient_prediction, lenient_count = witness_prediction(row, False)
            case_predictions.append({
                "id": row["id"],
                "mutation_class": row["mutation_class"],
                "gold": row["gold"],
                "strict_prediction": strict_prediction,
                "strict_valid_witnesses": strict_count,
                "lenient_prediction": lenient_prediction,
                "lenient_valid_witnesses": lenient_count,
                "direct_prediction": direct_prediction(row),
            })
        report["results"].append({
            "path": str(path.resolve()),
            "model": data["model"],
            "case_count": len(rows),
            "strict_source_compiled_witness": metrics(rows, lambda row: witness_prediction(row, True)),
            "lenient_source_compiled_witness": metrics(rows, lambda row: witness_prediction(row, False)),
            "direct_pair_judge": metrics(rows, direct_prediction),
            "compiler_schema_valid_rate": sum(bool(row.get("validated_witnesses")) for row in rows) / len(rows) if rows else None,
            "resource_use": resource_use(rows),
            "case_predictions": case_predictions,
        })
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")


if __name__ == "__main__":
    main()
