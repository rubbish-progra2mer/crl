from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from scipy import sparse
from sklearn.metrics import roc_auc_score, roc_curve


METHODS = ("text", "reference_concat", "absolute_delta", "rced", "signed_residual")
COMPARATORS = METHODS[:-1]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("v020_audit_base_v012", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def task_digest(task_id: str) -> bytes:
    return hashlib.sha256(task_id.encode("utf-8")).digest()


def split_name(task_id: str, config: dict[str, Any]) -> str:
    if task_id in set(config["selection_exposed_task_ids"]):
        return "train"
    value = task_digest(task_id)[1] % int(config["split_modulus"])
    if value in set(config["train_split_values"]):
        return "train"
    if value == int(config["validation_split_value"]):
        return "validation"
    if value == int(config["development_test_split_value"]):
        return "development_test"
    raise ValueError("unassigned split")


def prepare(rows: list[dict[str, Any]], base: Any, phase: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["task_id"])].append(row)
    examples: list[dict[str, Any]] = []
    references: list[dict[str, Any]] = []
    for task_id in sorted(grouped):
        task_rows = grouped[task_id]
        baselines = sorted(
            (row for row in task_rows if int(row["target"]) == 0),
            key=lambda row: (row["model"], row["label"], row["source_relative_path"]),
        )
        positives = [row for row in task_rows if int(row["target"]) == 1]
        if len(baselines) < 2 or not positives:
            continue
        reference = baselines[0]
        reference_text = base.action_text(reference)
        reference_profile = base.trajectory_profile(reference)
        references.append(
            {
                "task_id": task_id,
                "reference_row_id": reference["row_id"],
                "source_relative_path": reference["source_relative_path"],
                "source_sha256": reference["source_sha256"],
            }
        )
        for row in baselines[1:] + positives:
            examples.append(
                {
                    "task_id": task_id,
                    "row_id": row["row_id"],
                    "reference_row_id": reference["row_id"],
                    "target": int(row["target"]),
                    "text": base.action_text(row),
                    "reference_text": reference_text,
                    "rced_features": base.relative_features(
                        base.trajectory_profile(row), reference_profile
                    ),
                    "split": split_name(task_id, CONFIG) if phase == "development" else "confirmation",
                }
            )
    examples.sort(key=lambda item: (item["task_id"], item["row_id"]))
    return examples, references


def feature_matrices(examples: list[dict[str, Any]], vectorizer: Any, scaler: Any) -> dict[str, sparse.csr_matrix]:
    current = vectorizer.transform([item["text"] for item in examples]).tocsr()
    reference = vectorizer.transform([item["reference_text"] for item in examples]).tocsr()
    common = current.minimum(reference)
    novel = (current - common).tocsr()
    missing = (reference - common).tocsr()
    absolute = (current - reference).tocsr()
    absolute.data = np.abs(absolute.data)
    absolute.eliminate_zeros()
    numeric = sparse.csr_matrix(
        scaler.transform(np.vstack([item["rced_features"] for item in examples]))
    )
    return {
        "text": current,
        "reference_concat": sparse.hstack([current, reference], format="csr"),
        "absolute_delta": sparse.hstack([current, absolute], format="csr"),
        "rced": sparse.hstack([current, numeric], format="csr"),
        "signed_residual": sparse.hstack([current, novel, missing], format="csr"),
    }


def tpr_at_fpr(y: np.ndarray, scores: np.ndarray, limit: float = 0.05) -> float:
    fpr, tpr, _ = roc_curve(y, scores)
    return float(np.max(tpr[fpr <= limit]))


def metric_record(y: np.ndarray, scores: np.ndarray, threshold: float) -> dict[str, Any]:
    predicted = scores >= threshold
    negatives = y == 0
    positives = y == 1
    return {
        "auc": float(roc_auc_score(y, scores)),
        "tpr_at_5pct_fpr": tpr_at_fpr(y, scores),
        "threshold": float(threshold),
        "fixed_threshold": {
            "fpr": float(np.mean(predicted[negatives])),
            "tpr": float(np.mean(predicted[positives])),
        },
        "rows": int(len(y)),
        "negatives": int(np.sum(negatives)),
        "positives": int(np.sum(positives)),
    }


def bootstrap_delta(examples: list[dict[str, Any]], candidate: np.ndarray, comparator: np.ndarray, repeats: int, seed: int) -> dict[str, Any]:
    task_rows: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(examples):
        task_rows[item["task_id"]].append(index)
    tasks = sorted(task_rows)
    y = np.asarray([item["target"] for item in examples], dtype=np.int64)
    point = float(roc_auc_score(y, candidate) - roc_auc_score(y, comparator))
    rng = np.random.default_rng(seed)
    samples: list[float] = []
    for _ in range(repeats):
        selected = rng.choice(tasks, size=len(tasks), replace=True)
        indexes = [index for task_id in selected for index in task_rows[str(task_id)]]
        sampled_y = y[indexes]
        if len(np.unique(sampled_y)) < 2:
            raise ValueError("bootstrap sample lost a class")
        samples.append(
            float(
                roc_auc_score(sampled_y, candidate[indexes])
                - roc_auc_score(sampled_y, comparator[indexes])
            )
        )
    return {
        "point": point,
        "bootstrap_95": [float(np.quantile(samples, 0.025)), float(np.quantile(samples, 0.975))],
        "repeats": repeats,
        "resampling_unit": "task_id",
        "tasks": len(tasks),
    }


def maximum_error(left: Any, right: Any) -> float:
    if isinstance(left, dict) and isinstance(right, dict):
        if set(left) != set(right):
            return math.inf
        return max((maximum_error(left[key], right[key]) for key in left), default=0.0)
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            return math.inf
        return max((maximum_error(a, b) for a, b in zip(left, right)), default=0.0)
    if isinstance(left, bool) or isinstance(right, bool) or left is None or right is None:
        return 0.0 if left == right else math.inf
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(float(left) - float(right))
    return 0.0 if left == right else math.inf


def audit(args: argparse.Namespace) -> dict[str, Any]:
    global CONFIG
    CONFIG = read_json(args.config)
    summary = read_json(args.summary)
    raw = read_jsonl(args.raw_predictions)
    recorded_references = read_jsonl(args.reference_records)
    base = load_module(args.base_module)
    rows = base.load_jsonl(args.dataset)
    examples, references = prepare(rows, base, summary["phase"])
    bundle = joblib.load(args.model)
    errors: list[str] = []

    if sha256_path(args.config) != summary["config_sha256"]:
        errors.append("config SHA mismatch")
    if sha256_path(args.dataset) != summary["dataset_sha256"]:
        errors.append("dataset SHA mismatch")
    if sha256_path(args.base_module) != summary["base_module_sha256"]:
        errors.append("base module SHA mismatch")
    if sha256_path(args.raw_predictions) != summary["raw_predictions_sha256"]:
        errors.append("raw predictions SHA mismatch")
    if sha256_path(args.reference_records) != summary["reference_records_sha256"]:
        errors.append("reference records SHA mismatch")
    if sha256_path(args.model) != summary["model"]["sha256"]:
        errors.append("model SHA mismatch")
    if references != recorded_references:
        errors.append("reference records mismatch")

    if summary["phase"] == "development":
        expected = [item for item in examples if item["split"] == "development_test"]
    else:
        expected = examples
        overlap = set(item["task_id"] for item in expected) & set(bundle["development_task_ids"])
        if overlap:
            errors.append("Development/Confirmation task overlap")
    expected_map = {item["row_id"]: item for item in expected}
    raw_map = {item["row_id"]: item for item in raw}
    if len(raw_map) != len(raw):
        errors.append("duplicate raw row IDs")
    if set(raw_map) != set(expected_map):
        errors.append("raw row ID set mismatch")
    reference_ids = {item["reference_row_id"] for item in references}
    if reference_ids & set(raw_map):
        errors.append("reference row appears in evaluated rows")
    for row_id in set(raw_map) & set(expected_map):
        row = raw_map[row_id]
        item = expected_map[row_id]
        if (
            row["task_id"] != item["task_id"]
            or row["reference_row_id"] != item["reference_row_id"]
            or int(row["target"]) != item["target"]
        ):
            errors.append(f"row identity mismatch {row_id}")

    matrices = feature_matrices(expected, bundle["vectorizer"], bundle["scaler"])
    recomputed_scores = {
        name: bundle["models"][name].predict_proba(matrices[name])[:, 1]
        for name in METHODS
    }
    max_score_error = 0.0
    for index, item in enumerate(expected):
        recorded = raw_map[item["row_id"]]["scores"]
        for name in METHODS:
            max_score_error = max(
                max_score_error,
                abs(float(recorded[name]) - float(recomputed_scores[name][index])),
            )
    if max_score_error > 1e-12:
        errors.append("model score replay mismatch")

    y = np.asarray([item["target"] for item in expected], dtype=np.int64)
    metrics = {
        name: metric_record(y, recomputed_scores[name], bundle["thresholds"][name])
        for name in METHODS
    }
    if summary["phase"] == "development":
        strongest = max(COMPARATORS, key=lambda name: (metrics[name]["auc"], name))
    else:
        strongest = str(bundle["strongest_development_comparator"])
    delta = bootstrap_delta(
        expected,
        recomputed_scores["signed_residual"],
        recomputed_scores[strongest],
        int(CONFIG["bootstrap_repeats"]),
        int(CONFIG["seed"]),
    )
    candidate = metrics["signed_residual"]
    if summary["phase"] == "development":
        gate_config = CONFIG["development_gates"]
        gates = {
            "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"] >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_strongest": delta["point"] >= float(gate_config["candidate_auc_delta_min"]),
            "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] > 0.0,
            "fixed_threshold_fpr": candidate["fixed_threshold"]["fpr"] <= float(gate_config["fixed_threshold_fpr_max"]),
            "fixed_threshold_tpr": candidate["fixed_threshold"]["tpr"] >= float(gate_config["fixed_threshold_tpr_min"]),
            "strictly_beats_every_comparator": all(candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS),
        }
    else:
        gate_config = CONFIG["confirmation_gates"]
        gates = {
            "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"] >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_frozen_strongest": delta["point"] > 0.0,
            "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] >= 0.0,
            "fixed_threshold_fpr": candidate["fixed_threshold"]["fpr"] <= float(gate_config["fixed_threshold_fpr_max"]),
            "fixed_threshold_tpr": candidate["fixed_threshold"]["tpr"] >= float(gate_config["fixed_threshold_tpr_min"]),
            "task_ids_disjoint": True,
        }
    max_metric_error = max(
        maximum_error(metrics, summary["metrics"]),
        maximum_error(delta, summary["candidate_minus_strongest"]),
        maximum_error(gates, summary["gates"]),
    )
    if strongest != summary["strongest_comparator"]:
        errors.append("strongest comparator mismatch")
    if max_metric_error > 1e-12:
        errors.append("metric/gate mismatch")

    return {
        "schema_version": 1,
        "phase": summary["phase"],
        "status": "AUDIT_OK" if not errors else "AUDIT_ERROR",
        "errors": errors,
        "source_rows": len(rows),
        "eligible_tasks": len(references),
        "evaluated_rows": len(expected),
        "references_checked": len(references),
        "models_replayed": len(METHODS),
        "scores_replayed": len(expected) * len(METHODS),
        "maximum_score_error": max_score_error,
        "maximum_metric_error": max_metric_error,
        "config_sha256": sha256_path(args.config),
        "dataset_sha256": sha256_path(args.dataset),
        "raw_predictions_sha256": sha256_path(args.raw_predictions),
        "summary_sha256": sha256_path(args.summary),
        "model_sha256": sha256_path(args.model),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--base-module", type=Path, required=True)
    parser.add_argument("--raw-predictions", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--reference-records", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    report = audit(args)
    args.report.parent.mkdir(parents=True, exist_ok=False)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "evaluated_rows": report["evaluated_rows"],
                "scores_replayed": report["scores_replayed"],
                "maximum_score_error": report["maximum_score_error"],
                "maximum_metric_error": report["maximum_metric_error"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "AUDIT_OK" else 1


CONFIG: dict[str, Any] = {}


if __name__ == "__main__":
    raise SystemExit(main())
