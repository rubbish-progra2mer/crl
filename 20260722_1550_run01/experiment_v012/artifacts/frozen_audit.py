from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve


METHODS = ("text", "structured", "candidate", "envelope")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def task_digest(task_id: str) -> bytes:
    return hashlib.sha256(task_id.encode("utf-8")).digest()


def expected_development_split(
    task_id: str,
    config: dict[str, Any],
) -> str:
    if task_id in set(config["selection_exposed_task_ids"]):
        return "train"
    value = task_digest(task_id)[1] % int(config["split_modulus"])
    if value in set(config["train_split_values"]):
        return "train"
    if value == int(config["validation_split_value"]):
        return "validation"
    if value == int(config["development_test_split_value"]):
        return "development_test"
    raise ValueError(f"Unassigned split value {value}")


def tpr_at_fpr(y: np.ndarray, scores: np.ndarray, limit: float = 0.05) -> float:
    fpr, tpr, _ = roc_curve(y, scores)
    return float(np.max(tpr[fpr <= limit]))


def fixed_threshold(
    y: np.ndarray,
    scores: np.ndarray,
    threshold: float,
) -> dict[str, float]:
    predicted = scores >= threshold
    return {
        "fpr": float(np.mean(predicted[y == 0])),
        "tpr": float(np.mean(predicted[y == 1])),
    }


def metrics(
    rows: list[dict[str, Any]],
    method: str,
    threshold: float,
) -> dict[str, Any]:
    y = np.asarray([row["target"] for row in rows], dtype=np.int64)
    scores = np.asarray(
        [row["scores"][method] for row in rows], dtype=np.float64
    )
    return {
        "auc": float(roc_auc_score(y, scores)),
        "tpr_at_5pct_fpr": tpr_at_fpr(y, scores),
        "threshold": threshold,
        "fixed_threshold": fixed_threshold(y, scores, threshold),
        "rows": len(rows),
        "negatives": int(np.sum(y == 0)),
        "positives": int(np.sum(y == 1)),
    }


def cluster_delta(
    rows: list[dict[str, Any]],
    comparator: str,
    *,
    repeats: int,
    seed: int,
) -> dict[str, Any]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(rows):
        grouped[str(row["task_id"])].append(index)
    tasks = sorted(grouped)
    y = np.asarray([row["target"] for row in rows], dtype=np.int64)
    candidate = np.asarray(
        [row["scores"]["candidate"] for row in rows], dtype=np.float64
    )
    baseline = np.asarray(
        [row["scores"][comparator] for row in rows], dtype=np.float64
    )
    rng = np.random.default_rng(seed)
    samples: list[float] = []
    for _ in range(repeats):
        selected = rng.choice(tasks, size=len(tasks), replace=True)
        indexes = [index for task in selected for index in grouped[str(task)]]
        sampled_y = y[indexes]
        if len(np.unique(sampled_y)) != 2:
            raise ValueError("A bootstrap sample lost one class")
        samples.append(
            float(
                roc_auc_score(sampled_y, candidate[indexes])
                - roc_auc_score(sampled_y, baseline[indexes])
            )
        )
    return {
        "point": float(
            roc_auc_score(y, candidate) - roc_auc_score(y, baseline)
        ),
        "bootstrap_95": [
            float(np.quantile(samples, 0.025)),
            float(np.quantile(samples, 0.975)),
        ],
        "repeats": repeats,
        "resampling_unit": "task_id",
        "tasks": len(tasks),
    }


def assert_close(actual: float, expected: float, label: str) -> None:
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"{label}: {actual} != {expected}")


def compare_metrics(
    actual: dict[str, Any],
    expected: dict[str, Any],
    prefix: str,
) -> None:
    for key in ("auc", "tpr_at_5pct_fpr", "threshold"):
        assert_close(float(actual[key]), float(expected[key]), f"{prefix}.{key}")
    for key in ("fpr", "tpr"):
        assert_close(
            float(actual["fixed_threshold"][key]),
            float(expected["fixed_threshold"][key]),
            f"{prefix}.fixed_threshold.{key}",
        )
    for key in ("rows", "negatives", "positives"):
        if int(actual[key]) != int(expected[key]):
            raise ValueError(f"{prefix}.{key} does not match")


def verify_source_manifest(
    repository: Path,
    manifest: dict[str, Any],
) -> int:
    checked = 0
    for item in manifest["source_files"]:
        path = repository / item["relative_path"]
        if path.stat().st_size != int(item["bytes"]):
            raise ValueError(f"Source byte count changed: {path}")
        if sha256_file(path) != item["sha256"]:
            raise ValueError(f"Source hash changed: {path}")
        checked += 1
    return checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--raw-predictions", required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--frozen-model", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    dataset_path = Path(args.dataset).resolve()
    manifest_path = Path(args.manifest).resolve()
    raw_path = Path(args.raw_predictions).resolve()
    reference_path = Path(args.references).resolve()
    summary_path = Path(args.summary).resolve()
    frozen_model_path = Path(args.frozen_model).resolve()
    report_path = Path(args.report).resolve()
    repository = Path(args.repository_root).resolve()

    config = json.loads(config_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    dataset = load_jsonl(dataset_path)
    raw = load_jsonl(raw_path)
    references = load_jsonl(reference_path)
    frozen = joblib.load(frozen_model_path)

    if sha256_file(dataset_path) != manifest["dataset_sha256"]:
        raise ValueError("Dataset hash does not match manifest")
    if sha256_file(config_path) != summary["config_sha256"]:
        raise ValueError("Config hash does not match summary")
    if sha256_file(dataset_path) != summary["dataset_sha256"]:
        raise ValueError("Dataset hash does not match summary")
    if sha256_file(manifest_path) != summary["manifest_sha256"]:
        raise ValueError("Manifest hash does not match summary")
    if sha256_file(frozen_model_path) != summary["frozen_model_sha256"]:
        raise ValueError("Frozen model hash does not match summary")
    if frozen["config_sha256"] != sha256_file(config_path):
        raise ValueError("Frozen model config binding does not match")
    if tuple(frozen["feature_names"]) != tuple(summary["feature_names"]):
        raise ValueError("Frozen model feature order does not match summary")
    if frozen["repository_commit"] != config["repository_commit"]:
        raise ValueError("Frozen model repository commit does not match")
    if manifest["repository_commit"] != config["repository_commit"]:
        raise ValueError("Repository commit mismatch")
    source_files_checked = verify_source_manifest(repository, manifest)

    manifest_sources = {
        item["relative_path"]: item["sha256"]
        for item in manifest["source_files"]
    }
    for row in dataset:
        if manifest_sources.get(row["source_relative_path"]) != row["source_sha256"]:
            raise ValueError(
                f"Dataset source binding failed for {row['row_id']}"
            )
    reference_ids = {row["reference_row_id"] for row in references}
    reference_tasks = {row["task_id"] for row in references}
    evaluated_ids = {row["row_id"] for row in raw}
    if reference_ids & evaluated_ids:
        raise ValueError("A reference row occurs in raw predictions")
    if any(
        len(row["structured_features"]) != len(summary["feature_names"])
        or not all(math.isfinite(float(value)) for value in row["structured_features"])
        for row in raw
    ):
        raise ValueError("Raw structured feature vector is invalid")

    development_tasks = set(frozen["development_task_ids"])
    if args.phase == "development":
        train_tasks = set(frozen["training_task_ids"])
        validation_tasks = set(frozen["validation_task_ids"])
        test_tasks = set(frozen["development_test_task_ids"])
        if train_tasks & validation_tasks or train_tasks & test_tasks or validation_tasks & test_tasks:
            raise ValueError("A Development task crosses partitions")
        if train_tasks | validation_tasks | test_tasks != reference_tasks:
            raise ValueError("Frozen Development partitions do not cover eligible tasks")
        for task_id in reference_tasks:
            expected = expected_development_split(task_id, config)
            actual = (
                "train"
                if task_id in train_tasks
                else "validation"
                if task_id in validation_tasks
                else "development_test"
            )
            if actual != expected:
                raise ValueError(f"Development split mismatch for {task_id}")
        if set(config["selection_exposed_task_ids"]) - train_tasks:
            raise ValueError("A selection-exposed task is not in training")
        if {row["task_id"] for row in raw} != test_tasks:
            raise ValueError("Raw Development rows are not the held-out task set")
    else:
        if development_tasks & reference_tasks:
            raise ValueError("Confirmation task overlaps Development")
        if {row["task_id"] for row in raw} != reference_tasks:
            raise ValueError("Raw Confirmation rows do not cover eligible tasks")

    thresholds = (
        summary["threshold_selection"]["thresholds"]
        if args.phase == "development"
        else summary["thresholds"]
    )
    recomputed = {
        method: metrics(raw, method, float(thresholds[method]))
        for method in METHODS
    }
    for method in METHODS:
        compare_metrics(
            recomputed[method],
            summary["metrics"][method],
            f"metrics.{method}",
        )

    comparator = (
        summary["strongest_comparator"]
        if args.phase == "development"
        else summary["frozen_strongest_comparator"]
    )
    delta = cluster_delta(
        raw,
        comparator,
        repeats=int(config["bootstrap_repeats"]),
        seed=int(config["seed"]) + (0 if args.phase == "development" else 1),
    )
    expected_delta = summary[
        "candidate_minus_strongest_comparator_auc"
        if args.phase == "development"
        else "candidate_minus_frozen_strongest_comparator_auc"
    ]
    assert_close(delta["point"], expected_delta["point"], "delta.point")
    for index in (0, 1):
        assert_close(
            delta["bootstrap_95"][index],
            expected_delta["bootstrap_95"][index],
            f"delta.bootstrap_95[{index}]",
        )

    candidate = recomputed["candidate"]
    if args.phase == "development":
        gate_config = config["development_gates"]
        gates = {
            "candidate_auc": candidate["auc"]
            >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
            >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_strongest_comparator": delta["point"]
            >= float(gate_config["candidate_auc_delta_min"]),
            "auc_delta_task_bootstrap_lower": delta["bootstrap_95"][0] > 0.0,
            "fixed_threshold_fpr": candidate["fixed_threshold"]["fpr"]
            <= float(gate_config["fixed_threshold_fpr_max"]),
            "fixed_threshold_tpr": candidate["fixed_threshold"]["tpr"]
            >= float(gate_config["fixed_threshold_tpr_min"]),
        }
    else:
        gate_config = config["confirmation_gates"]
        overlap = set(summary["development_task_overlap"])
        gates = {
            "task_ids_disjoint": not overlap,
            "candidate_auc": candidate["auc"]
            >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
            >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_frozen_strongest_comparator": delta["point"] > 0.0,
            "auc_delta_task_bootstrap_lower": delta["bootstrap_95"][0]
            >= float(gate_config["candidate_auc_delta_bootstrap_lower_min"]),
            "fixed_threshold_fpr": candidate["fixed_threshold"]["fpr"]
            <= float(gate_config["fixed_threshold_fpr_max"]),
            "fixed_threshold_tpr": candidate["fixed_threshold"]["tpr"]
            >= float(gate_config["fixed_threshold_tpr_min"]),
        }
    if gates != summary["gates"]:
        raise ValueError("Recomputed gates do not match summary")
    if all(gates.values()) != bool(summary["all_gates_passed"]):
        raise ValueError("Aggregate gate does not match summary")

    report = {
        "phase": args.phase,
        "status": "AUDIT_OK",
        "source_files_checked": source_files_checked,
        "dataset_rows_checked": len(dataset),
        "raw_prediction_rows_checked": len(raw),
        "reference_rows_checked": len(references),
        "reference_overlap": sorted(reference_ids & evaluated_ids),
        "task_partition_check": "OK",
        "metrics": recomputed,
        "comparator": comparator,
        "candidate_minus_comparator_auc": delta,
        "gates": gates,
        "all_gates_passed": all(gates.values()),
        "input_sha256": {
            "config": sha256_file(config_path),
            "dataset": sha256_file(dataset_path),
            "manifest": sha256_file(manifest_path),
            "raw_predictions": sha256_file(raw_path),
            "references": sha256_file(reference_path),
            "summary": sha256_file(summary_path),
            "frozen_model": sha256_file(frozen_model_path),
        },
    }
    report_path.parent.mkdir(parents=True, exist_ok=False)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "phase": args.phase,
                "status": report["status"],
                "all_gates_passed": report["all_gates_passed"],
                "source_files_checked": source_files_checked,
                "raw_prediction_rows_checked": len(raw),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
