from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


IDENTITY_FIELDS = ("world_id", "claim_id", "budget", "method")
INPUT_FIELDS = ("initial_observation_digest",)
BEHAVIOR_FIELDS = (
    "connector_profile",
    "scope_family",
    "quantifier",
    "predicate",
    "scope_size",
    "truth",
    "decision",
    "correct",
    "unsafe_commit",
    "tool_calls",
    "certificate_valid",
    "proof_type",
    "reason",
)
CONFIG_FIELDS = (
    "seeds",
    "worlds_per_seed",
    "budgets",
    "task_count",
    "episode_count",
    "methods",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def keyed(rows: list[dict[str, Any]]) -> dict[tuple[Any, ...], dict[str, Any]]:
    result: dict[tuple[Any, ...], dict[str, Any]] = {}
    for row in rows:
        key = tuple(row[field] for field in IDENTITY_FIELDS)
        if key in result:
            raise ValueError(f"duplicate row identity: {key!r}")
        result[key] = row
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--baseline-execution", type=Path, required=True)
    parser.add_argument("--candidate-execution", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    baseline = load(args.baseline)
    candidate = load(args.candidate)
    baseline_execution = load(args.baseline_execution)
    candidate_execution = load(args.candidate_execution)

    configuration_mismatches = {
        field: {"baseline": baseline[field], "candidate": candidate[field]}
        for field in CONFIG_FIELDS
        if baseline[field] != candidate[field]
    }
    baseline_rows = keyed(baseline["rows"])
    candidate_rows = keyed(candidate["rows"])
    missing_in_candidate = sorted(set(baseline_rows) - set(candidate_rows))
    extra_in_candidate = sorted(set(candidate_rows) - set(baseline_rows))
    input_mismatches: list[dict[str, Any]] = []
    behavior_mismatches: list[dict[str, Any]] = []
    for key in sorted(set(baseline_rows) & set(candidate_rows)):
        left = baseline_rows[key]
        right = candidate_rows[key]
        changed_inputs = {
            field: {"baseline": left[field], "candidate": right[field]}
            for field in INPUT_FIELDS
            if left[field] != right[field]
        }
        if changed_inputs:
            input_mismatches.append(
                {"identity": list(key), "changed": changed_inputs}
            )
        changed_behavior = {
            field: {"baseline": left[field], "candidate": right[field]}
            for field in BEHAVIOR_FIELDS
            if left[field] != right[field]
        }
        if changed_behavior:
            behavior_mismatches.append(
                {"identity": list(key), "changed": changed_behavior}
            )

    baseline_duration = float(baseline_execution["duration_seconds"])
    candidate_duration = float(candidate_execution["duration_seconds"])
    report = {
        "experiment": "v006_v007_exact_clean_regression_comparison",
        "schema_version": 1,
        "inputs": {
            "baseline_result_sha256": sha256(args.baseline),
            "candidate_result_sha256": sha256(args.candidate),
            "baseline_execution_sha256": sha256(args.baseline_execution),
            "candidate_execution_sha256": sha256(args.candidate_execution),
        },
        "compared_configuration_fields": list(CONFIG_FIELDS),
        "compared_input_fields": list(INPUT_FIELDS),
        "compared_behavior_fields": list(BEHAVIOR_FIELDS),
        "configuration_mismatch_count": len(configuration_mismatches),
        "configuration_mismatches": configuration_mismatches,
        "baseline_row_count": len(baseline_rows),
        "candidate_row_count": len(candidate_rows),
        "missing_in_candidate_count": len(missing_in_candidate),
        "extra_in_candidate_count": len(extra_in_candidate),
        "input_mismatch_count": len(input_mismatches),
        "input_mismatch_samples": input_mismatches[:20],
        "behavior_mismatch_count": len(behavior_mismatches),
        "behavior_mismatch_samples": behavior_mismatches[:20],
        "baseline_duration_seconds": baseline_duration,
        "candidate_duration_seconds": candidate_duration,
        "candidate_to_baseline_duration_ratio": candidate_duration
        / baseline_duration,
    }
    report["all_exact_clean_rows_equal"] = not any(
        (
            configuration_mismatches,
            missing_in_candidate,
            extra_in_candidate,
            input_mismatches,
            behavior_mismatches,
        )
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["all_exact_clean_rows_equal"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
