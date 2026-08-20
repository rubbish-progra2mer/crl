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


METHODS = (
    "mixed",
    "commands",
    "outputs",
    "role_concat",
    "triple_mixed",
    "command_duplicated",
    "output_duplicated",
    "role_factorized",
)
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
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("v023_audit_base_v012", path)
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


def prepare(
    rows: list[dict[str, Any]], base: Any, phase: str, config: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    examples: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    for row in rows:
        task_id = str(row["task_id"])
        row_id = str(row["row_id"])
        examples.append(
            {
                "task_id": task_id,
                "row_id": row_id,
                "target": int(row["target"]),
                "mixed_text": base.action_text(row),
                "command_text": "COMMANDS\n" + "\n".join(str(value) for value in row["commands"]),
                "output_text": "OUTPUTS\n" + "\n".join(str(value) for value in row["terminal_outputs"]),
                "split": split_name(task_id, config) if phase == "development" else "confirmation",
            }
        )
        sources.append(
            {
                "row_id": row_id,
                "task_id": task_id,
                "source_relative_path": str(row["source_relative_path"]),
                "source_sha256": str(row["source_sha256"]),
            }
        )
    examples.sort(key=lambda item: (item["task_id"], item["row_id"]))
    sources.sort(key=lambda item: (item["task_id"], item["row_id"]))
    if len({item["row_id"] for item in examples}) != len(examples):
        raise ValueError("duplicate source row IDs")
    return examples, sources


def feature_matrices(
    examples: list[dict[str, Any]], vectorizer: Any
) -> dict[str, sparse.csr_matrix]:
    mixed = vectorizer.transform([item["mixed_text"] for item in examples]).tocsr()
    commands = vectorizer.transform([item["command_text"] for item in examples]).tocsr()
    outputs = vectorizer.transform([item["output_text"] for item in examples]).tocsr()
    return {
        "mixed": mixed,
        "commands": commands,
        "outputs": outputs,
        "role_concat": sparse.hstack([commands, outputs], format="csr"),
        "triple_mixed": sparse.hstack([mixed, mixed, mixed], format="csr"),
        "command_duplicated": sparse.hstack([mixed, commands, commands], format="csr"),
        "output_duplicated": sparse.hstack([mixed, outputs, outputs], format="csr"),
        "role_factorized": sparse.hstack([mixed, commands, outputs], format="csr"),
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


def bootstrap_delta(
    examples: list[dict[str, Any]],
    candidate: np.ndarray,
    comparator: np.ndarray,
    repeats: int,
    seed: int,
) -> dict[str, Any]:
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
        indexes = [index for task in selected for index in task_rows[str(task)]]
        sampled_y = y[indexes]
        if len(np.unique(sampled_y)) != 2:
            raise ValueError("bootstrap sample lost one class")
        samples.append(
            float(
                roc_auc_score(sampled_y, candidate[indexes])
                - roc_auc_score(sampled_y, comparator[indexes])
            )
        )
    return {
        "point": point,
        "bootstrap_95": [
            float(np.quantile(samples, 0.025)),
            float(np.quantile(samples, 0.975)),
        ],
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
    config = read_json(args.config)
    summary = read_json(args.summary)
    raw = read_jsonl(args.raw_predictions)
    recorded_sources = read_jsonl(args.source_records)
    base = load_module(args.base_module)
    rows = [row for path in args.dataset for row in base.load_jsonl(path)]
    examples, sources = prepare(rows, base, summary["phase"], config)
    bundle = joblib.load(args.model)
    errors: list[str] = []

    dataset_hashes = [sha256_path(path) for path in args.dataset]
    checks = (
        (sha256_path(args.config), summary["config_sha256"], "config SHA mismatch"),
        (dataset_hashes, summary["dataset_sha256s"], "dataset SHA sequence mismatch"),
        (sha256_path(args.base_module), summary["base_module_sha256"], "base SHA mismatch"),
        (sha256_path(args.raw_predictions), summary["raw_predictions_sha256"], "raw SHA mismatch"),
        (sha256_path(args.source_records), summary["source_records_sha256"], "source records SHA mismatch"),
        (sha256_path(args.model), summary["model"]["sha256"], "model SHA mismatch"),
    )
    for actual, expected, message in checks:
        if actual != expected:
            errors.append(message)
    if summary.get("experiment_id") != "v023":
        errors.append("experiment ID mismatch")
    if sources != recorded_sources:
        errors.append("source records mismatch")
    if set(bundle["models"]) != set(METHODS) or set(bundle["thresholds"]) != set(METHODS):
        errors.append("model or threshold method set mismatch")

    if summary["phase"] == "development":
        expected = [item for item in examples if item["split"] == "development_test"]
    else:
        expected = examples
        overlap = set(item["task_id"] for item in expected) & set(bundle["development_task_ids"])
        if overlap:
            errors.append("Development/Confirmation task overlap")

    raw_map = {item["row_id"]: item for item in raw}
    expected_map = {item["row_id"]: item for item in expected}
    if len(raw_map) != len(raw):
        errors.append("duplicate raw row IDs")
    if set(raw_map) != set(expected_map):
        errors.append("raw row ID set mismatch")
    for row_id in set(raw_map) & set(expected_map):
        row = raw_map[row_id]
        item = expected_map[row_id]
        if row["task_id"] != item["task_id"] or int(row["target"]) != item["target"]:
            errors.append(f"row identity mismatch {row_id}")

    matrices = feature_matrices(expected, bundle["vectorizer"])
    recomputed = {
        name: bundle["models"][name].predict_proba(matrices[name])[:, 1]
        for name in METHODS
    }
    max_score_error = 0.0
    for index, item in enumerate(expected):
        recorded = raw_map[item["row_id"]]["scores"]
        for name in METHODS:
            max_score_error = max(
                max_score_error,
                abs(float(recorded[name]) - float(recomputed[name][index])),
            )
    if max_score_error > 1e-12:
        errors.append("model score replay mismatch")

    y = np.asarray([item["target"] for item in expected], dtype=np.int64)
    metrics = {
        name: metric_record(y, recomputed[name], bundle["thresholds"][name])
        for name in METHODS
    }
    if summary["phase"] == "development":
        strongest = max(COMPARATORS, key=lambda name: (metrics[name]["auc"], name))
    else:
        strongest = str(bundle["strongest_development_comparator"])
    delta = bootstrap_delta(
        expected,
        recomputed["role_factorized"],
        recomputed[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    candidate = metrics["role_factorized"]
    if summary["phase"] == "development":
        gate_config = config["development_gates"]
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
        gate_config = config["confirmation_gates"]
        gates = {
            "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"] >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_frozen_strongest": delta["point"] > 0.0,
            "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] >= 0.0,
            "fixed_threshold_fpr": candidate["fixed_threshold"]["fpr"] <= float(gate_config["fixed_threshold_fpr_max"]),
            "fixed_threshold_tpr": candidate["fixed_threshold"]["tpr"] >= float(gate_config["fixed_threshold_tpr_min"]),
            "strictly_beats_every_comparator": all(candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS),
            "task_ids_disjoint": True,
        }

    dimensions = {name: int(matrices[name].shape[1]) for name in METHODS}
    max_metric_error = max(
        maximum_error(metrics, summary["metrics"]),
        maximum_error(delta, summary["candidate_minus_strongest"]),
        maximum_error(gates, summary["gates"]),
    )
    if summary["phase"] == "development":
        max_metric_error = max(max_metric_error, maximum_error(dimensions, summary["feature_dimensions"]))
    if strongest != summary["strongest_comparator"]:
        errors.append("strongest comparator mismatch")
    if max_metric_error > 1e-12:
        errors.append("metric, gate, or dimension mismatch")

    return {
        "schema_version": 1,
        "phase": summary["phase"],
        "status": "AUDIT_OK" if not errors else "AUDIT_ERROR",
        "errors": errors,
        "source_rows": len(rows),
        "evaluated_rows": len(expected),
        "tasks_checked": len({item["task_id"] for item in expected}),
        "source_records_checked": len(sources),
        "models_replayed": len(METHODS),
        "scores_replayed": len(expected) * len(METHODS),
        "maximum_score_error": max_score_error,
        "maximum_metric_error": max_metric_error,
        "config_sha256": sha256_path(args.config),
        "dataset_sha256s": dataset_hashes,
        "raw_predictions_sha256": sha256_path(args.raw_predictions),
        "summary_sha256": sha256_path(args.summary),
        "model_sha256": sha256_path(args.model),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", action="append", type=Path, required=True)
    parser.add_argument("--base-module", type=Path, required=True)
    parser.add_argument("--raw-predictions", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--source-records", type=Path, required=True)
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


if __name__ == "__main__":
    raise SystemExit(main())
