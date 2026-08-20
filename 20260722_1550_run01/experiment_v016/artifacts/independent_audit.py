from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any, Sequence


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def macro_f1(truth: Sequence[str], prediction: Sequence[str]) -> float:
    labels = sorted(set(truth) | set(prediction))
    values: list[float] = []
    for label in labels:
        tp = sum(t == label and p == label for t, p in zip(truth, prediction))
        fp = sum(t != label and p == label for t, p in zip(truth, prediction))
        fn = sum(t == label and p != label for t, p in zip(truth, prediction))
        denominator = 2 * tp + fp + fn
        values.append(0.0 if denominator == 0 else 2 * tp / denominator)
    return sum(values) / len(values)


def percentile(sorted_values: Sequence[float], q: float) -> float:
    position = (len(sorted_values) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    fraction = position - lower
    return float(
        sorted_values[lower] * (1.0 - fraction)
        + sorted_values[upper] * fraction
    )


def accuracy(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    eligible = [row for row in rows if row["unanimous_label"] is not None]
    total = len(eligible)
    official = sum(
        row["official_label"] == row["unanimous_label"] for row in eligible
    )
    rgp = sum(row["rgp_label"] == row["unanimous_label"] for row in eligible)
    return {
        "rows": total,
        "official_correct": official,
        "rgp_correct": rgp,
        "official_accuracy": official / total,
        "rgp_accuracy": rgp / total,
        "accuracy_delta": (rgp - official) / total,
    }


def per_group(
    rows: Sequence[dict[str, Any]], key: str
) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(row)
    return {name: accuracy(groups[name]) for name in sorted(groups)}


def bootstrap(
    rows: Sequence[dict[str, Any]], resamples: int, seed: int
) -> dict[str, Any]:
    clusters: dict[str, dict[str, int]] = {}
    for row in rows:
        truth = row["unanimous_label"]
        if truth is None:
            continue
        item = clusters.setdefault(
            row["model_id"], {"rows": 0, "official": 0, "rgp": 0}
        )
        item["rows"] += 1
        item["official"] += int(row["official_label"] == truth)
        item["rgp"] += int(row["rgp_label"] == truth)
    names = sorted(clusters)
    rng = random.Random(seed)
    values: list[float] = []
    for _ in range(resamples):
        chosen = [names[rng.randrange(len(names))] for _ in names]
        total = sum(clusters[name]["rows"] for name in chosen)
        difference = sum(
            clusters[name]["rgp"] - clusters[name]["official"] for name in chosen
        )
        values.append(difference / total)
    values.sort()
    return {
        "unit": "generator_model",
        "cluster_count": len(names),
        "resamples": resamples,
        "seed": seed,
        "lower_95": percentile(values, 0.025),
        "median": percentile(values, 0.5),
        "upper_95": percentile(values, 0.975),
        "minimum": values[0],
        "maximum": values[-1],
    }


def maximum_numeric_error(left: Any, right: Any) -> float:
    errors: list[float] = []

    def walk(a: Any, b: Any) -> None:
        if isinstance(a, dict) and isinstance(b, dict):
            if set(a) != set(b):
                raise AssertionError(f"dictionary keys differ: {set(a) ^ set(b)}")
            for key in a:
                walk(a[key], b[key])
        elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
            if math.isinf(float(a)) and math.isinf(float(b)):
                errors.append(0.0)
            else:
                errors.append(abs(float(a) - float(b)))
        else:
            if a != b:
                raise AssertionError(f"values differ: {a!r} != {b!r}")

    walk(left, right)
    return max(errors, default=0.0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Independently recompute v015 metrics from frozen row output."
    )
    parser.add_argument("--rows", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--report-out", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_json(args.config)
    summary = load_json(args.summary)
    rows = [
        json.loads(line)
        for line in args.rows.read_text(encoding="utf-8").splitlines()
        if line
    ]
    keys = [(row["model_id"], row["task_id"]) for row in rows]
    duplicate_keys = len(keys) - len(set(keys))
    unanimous = [row for row in rows if row["unanimous_label"] is not None]
    recomputed_overall = accuracy(rows)
    truth = [row["unanimous_label"] for row in unanimous]
    official = [row["official_label"] for row in unanimous]
    rgp = [row["rgp_label"] for row in unanimous]
    official_macro = macro_f1(truth, official)
    rgp_macro = macro_f1(truth, rgp)
    corrections = sum(
        row["official_label"] != row["unanimous_label"]
        and row["rgp_label"] == row["unanimous_label"]
        for row in unanimous
    )
    regressions = sum(
        row["official_label"] == row["unanimous_label"]
        and row["rgp_label"] != row["unanimous_label"]
        for row in unanimous
    )
    per_model = per_group(rows, "model_id")
    per_domain = per_group(rows, "domain")
    bootstrap_config = config["bootstrap"]
    recomputed_bootstrap = bootstrap(
        rows, bootstrap_config["resamples"], bootstrap_config["seed"]
    )
    mechanism = [
        row
        for row in rows
        if row["official_label"] == "output_fabrication"
        and row["rgp_label"] == "correct"
        and row["unanimous_label"] == "correct"
    ]
    changed = [row for row in rows if row["official_label"] != row["rgp_label"]]
    structural_violations = [
        row
        for row in changed
        if (
            not row["tool_required"]
            or row["external_release_label"]
            or not row["expected_tool_called"]
            or not row["required_satisfied"]
            or row["official_label"] != "output_fabrication"
            or row["rgp_label"] != "correct"
        )
    ]
    supported_labels = set(config["supported_labels"])
    allowed_external = set(config["external_labels_passthrough"])
    baseline_identity_errors = sum(
        not row["external_release_label"]
        and row["official_recomputed_label"] != row["official_label"]
        for row in rows
    )
    unexpected_external_labels = sorted(
        {
            row["official_label"]
            for row in rows
            if row["external_release_label"]
            and row["official_label"] not in allowed_external
        }
    )
    mislabeled_supported_rows = sum(
        row["external_release_label"] == (row["official_label"] in supported_labels)
        for row in rows
    )
    positive_models = sum(
        metrics["accuracy_delta"] > 0 for metrics in per_model.values()
    )
    positive_domains = sum(
        metrics["accuracy_delta"] > 0 for metrics in per_domain.values()
    )
    expected = config["expected"]
    gates = config["gates"]
    correction_margin = corrections > regressions
    recomputed_metric_gates = {
        "baseline_identity": baseline_identity_errors == 0
        and not unexpected_external_labels
        and mislabeled_supported_rows == 0,
        "structural_invariance": not structural_violations,
        "primary_effect": recomputed_overall["accuracy_delta"]
        >= gates["minimum_accuracy_delta"],
        "cluster_uncertainty": recomputed_bootstrap["lower_95"]
        > gates["bootstrap_lower_bound_strictly_above"],
        "correction_margin": correction_margin,
        "model_spread": positive_models >= gates["minimum_positive_models"],
        "domain_spread": positive_domains >= gates["minimum_positive_domains"],
        "mechanism_support": len(mechanism)
        >= gates["minimum_supported_of_to_correct"]
        and len({row["domain"] for row in mechanism})
        >= gates["minimum_mechanism_domains"],
    }
    recorded_metric_gates = {
        key: summary["gate_checks"][key] for key in recomputed_metric_gates
    }
    recorded_metrics = summary["metrics"]
    recomputed_core = {
        "overall": recomputed_overall,
        "official_macro_f1": official_macro,
        "rgp_macro_f1": rgp_macro,
        "macro_f1_delta": rgp_macro - official_macro,
        "corrections": corrections,
        "regressions": regressions,
        "per_model": per_model,
        "per_domain": per_domain,
        "bootstrap": recomputed_bootstrap,
        "mechanism_transition_count": len(mechanism),
        "mechanism_domains": sorted({row["domain"] for row in mechanism}),
    }
    recorded_core = {key: recorded_metrics[key] for key in recomputed_core}
    maximum_error = maximum_numeric_error(recomputed_core, recorded_core)
    recorded_rows_sha256 = summary["outputs"]["rows_sha256"]
    report = {
        "schema_version": 2,
        "rows_path": str(args.rows),
        "rows_sha256": sha256_file(args.rows),
        "recorded_rows_sha256": recorded_rows_sha256,
        "summary_path": str(args.summary),
        "summary_sha256": sha256_file(args.summary),
        "config_path": str(args.config),
        "config_sha256": sha256_file(args.config),
        "row_count": len(rows),
        "unique_key_count": len(set(keys)),
        "duplicate_key_count": duplicate_keys,
        "unanimous_rows": len(unanimous),
        "judge_disagreement_rows": len(rows) - len(unanimous),
        "changed_rows": len(changed),
        "baseline_identity_errors": baseline_identity_errors,
        "unexpected_external_labels": unexpected_external_labels,
        "mislabeled_supported_rows": mislabeled_supported_rows,
        "structural_violations": len(structural_violations),
        "maximum_recorded_metric_error": maximum_error,
        "recomputed": recomputed_core,
        "recomputed_metric_gates": recomputed_metric_gates,
        "recorded_metric_gates": recorded_metric_gates,
        "audit_checks": {
            "rows_sha_matches_summary": sha256_file(args.rows)
            == recorded_rows_sha256,
            "summary_phase_matches_config": summary["phase"] == config["phase"],
            "manifest_sha_matches_config": summary["inputs"]["manifest_sha256"]
            == config["manifest_sha256"],
            "input_file_cardinalities_match": len(
                summary["inputs"]["verified_files"]
            )
            == expected["files"]
            and summary["inputs"]["trace_files"] == expected["trace_files"]
            and summary["inputs"]["judge_files"] == expected["judge_files"]
            and summary["inputs"]["ensemble_files_verified_but_unused"]
            == expected["ensemble_files"],
            "row_count_matches_config": len(rows) == expected["rows"],
            "keys_are_unique": duplicate_keys == 0,
            "model_count_matches_config": len(per_model) == expected["models"],
            "domain_count_matches_config": len(per_domain)
            == expected["domains"],
            "no_structural_violations": not structural_violations,
            "recorded_metrics_exact": maximum_error <= 1e-15,
            "recorded_metric_gates_match": recomputed_metric_gates
            == recorded_metric_gates,
        },
    }
    report["audit_ok"] = all(report["audit_checks"].values())
    write_json(args.report_out, report)
    print(f"rows={len(rows)} unique={len(set(keys))}")
    print(f"changed_rows={len(changed)}")
    print(f"maximum_recorded_metric_error={maximum_error:.18g}")
    print(f"audit_ok={str(report['audit_ok']).lower()}")
    return 0 if report["audit_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
