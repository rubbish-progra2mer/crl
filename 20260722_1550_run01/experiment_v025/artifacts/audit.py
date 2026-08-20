from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
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
    "role_concat",
    "command_duplicated",
    "fixed_halves",
    "anchor_bag",
    "viaf",
)
COMPARATORS = METHODS[:-1]
INSPECTION_RE = re.compile(
    r"(?:^|[\s;&|])\s*(?:cat|sed|grep|rg|find|ls|head|tail|less|more|strings|type|which|stat)\b",
    re.IGNORECASE,
)
CHECKER_RE = re.compile(
    r"(?:^|[^A-Za-z0-9])(?:check(?:er|ing)?|tests?|testing|pytest|unittest|verify|verifier|verification|grader|grading|score|scoring|eval|evaluator|evaluation|reward)(?:[^A-Za-z0-9]|$)",
    re.IGNORECASE,
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("v025_audit_base_v012", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_anchor_batch(batch: str) -> bool:
    return bool(INSPECTION_RE.search(batch) and CHECKER_RE.search(batch))


def role_text(batches: list[str]) -> str:
    return "\n".join(batches)


def fold_for_task(task_id: str, modulus: int) -> int:
    return hashlib.sha256(task_id.encode("utf-8")).digest()[1] % modulus


def prepare(rows: list[dict[str, Any]], base: Any, fold_modulus: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    examples = []
    sources = []
    for row in rows:
        commands = [str(value) for value in row["commands"]]
        outputs = [str(value) for value in row["terminal_outputs"]]
        matches = [index for index, batch in enumerate(commands) if is_anchor_batch(batch)]
        anchor_index = matches[0] if matches else None
        if anchor_index is None:
            before = commands
            from_anchor: list[str] = []
        else:
            before = commands[:anchor_index]
            from_anchor = commands[anchor_index:]
        half = (len(commands) + 1) // 2
        matching = [batch for batch in commands if is_anchor_batch(batch)]
        nonmatching = [batch for batch in commands if not is_anchor_batch(batch)]
        task_id = str(row["task_id"])
        row_id = str(row["row_id"])
        examples.append(
            {
                "row_id": row_id,
                "task_id": task_id,
                "target": int(row["target"]),
                "fold": fold_for_task(task_id, fold_modulus),
                "anchor_present": anchor_index is not None,
                "anchor_index": anchor_index,
                "mixed_text": base.action_text(row),
                "commands_text": role_text(commands),
                "outputs_text": role_text(outputs),
                "first_half_text": role_text(commands[:half]),
                "second_half_text": role_text(commands[half:]),
                "anchor_matching_text": role_text(matching),
                "anchor_nonmatching_text": role_text(nonmatching),
                "before_text": role_text(before),
                "from_anchor_text": role_text(from_anchor),
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


def labels(examples: list[dict[str, Any]], indexes: np.ndarray) -> np.ndarray:
    return np.asarray([examples[int(index)]["target"] for index in indexes], dtype=np.int64)


def matrices(examples: list[dict[str, Any]], indexes: np.ndarray, vectorizer: Any) -> dict[str, sparse.csr_matrix]:
    def transform(name: str) -> sparse.csr_matrix:
        return vectorizer.transform([examples[int(index)][name] for index in indexes]).tocsr()

    mixed = transform("mixed_text")
    commands = transform("commands_text")
    outputs = transform("outputs_text")
    first_half = transform("first_half_text")
    second_half = transform("second_half_text")
    anchor_matching = transform("anchor_matching_text")
    anchor_nonmatching = transform("anchor_nonmatching_text")
    before = transform("before_text")
    from_anchor = transform("from_anchor_text")
    return {
        "mixed": mixed,
        "commands": commands,
        "role_concat": sparse.hstack([commands, outputs], format="csr"),
        "command_duplicated": sparse.hstack([mixed, commands, commands], format="csr"),
        "fixed_halves": sparse.hstack([mixed, first_half, second_half], format="csr"),
        "anchor_bag": sparse.hstack([mixed, anchor_matching, anchor_nonmatching], format="csr"),
        "viaf": sparse.hstack([mixed, before, from_anchor], format="csr"),
    }


def metric_record(y: np.ndarray, scores: np.ndarray) -> dict[str, Any]:
    fpr, tpr, _ = roc_curve(y, scores)
    return {
        "auc": float(roc_auc_score(y, scores)),
        "tpr_at_5pct_fpr": float(np.max(tpr[fpr <= 0.05])),
        "rows": int(len(y)),
        "negatives": int(np.sum(y == 0)),
        "positives": int(np.sum(y == 1)),
    }


def bootstrap_delta(
    examples: list[dict[str, Any]], indexes: np.ndarray, candidate: np.ndarray, comparator: np.ndarray, repeats: int, seed: int
) -> dict[str, Any]:
    task_rows: dict[str, list[int]] = defaultdict(list)
    for local_index, example_index in enumerate(indexes):
        task_rows[examples[int(example_index)]["task_id"]].append(local_index)
    tasks = sorted(task_rows)
    y = labels(examples, indexes)
    point = float(roc_auc_score(y, candidate) - roc_auc_score(y, comparator))
    rng = np.random.default_rng(seed)
    samples = []
    for _ in range(repeats):
        selected = rng.choice(tasks, size=len(tasks), replace=True)
        row_indexes = [index for task_id in selected for index in task_rows[str(task_id)]]
        sampled_y = y[row_indexes]
        if len(np.unique(sampled_y)) != 2:
            raise ValueError("bootstrap sample lost one class")
        samples.append(
            float(
                roc_auc_score(sampled_y, candidate[row_indexes])
                - roc_auc_score(sampled_y, comparator[row_indexes])
            )
        )
    return {
        "point": point,
        "bootstrap_95": [float(np.quantile(samples, 0.025)), float(np.quantile(samples, 0.975))],
        "repeats": repeats,
        "resampling_unit": "task_id",
        "tasks": len(tasks),
    }


def stratum_delta(
    examples: list[dict[str, Any]], indexes: np.ndarray, scores: dict[str, np.ndarray], present: bool
) -> dict[str, Any]:
    local = [i for i, index in enumerate(indexes) if bool(examples[int(index)]["anchor_present"]) is present]
    y = labels(examples, indexes)[local]
    if set(y.tolist()) != {0, 1}:
        raise ValueError("anchor stratum lacks two classes")
    viaf = float(roc_auc_score(y, scores["viaf"][local]))
    duplicated = float(roc_auc_score(y, scores["command_duplicated"][local]))
    return {
        "rows": len(local),
        "negatives": int(np.sum(y == 0)),
        "positives": int(np.sum(y == 1)),
        "viaf_auc": viaf,
        "command_duplicated_auc": duplicated,
        "delta": viaf - duplicated,
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


def verify_manifest(
    manifest: dict[str, Any], config: dict[str, Any], config_path: Path, dataset_path: Path, phase: str
) -> list[str]:
    expected_bucket = int(config["development_bucket"] if phase == "development" else config["confirmation_bucket"])
    expected = {
        "phase": phase,
        "repository_url": config["repository_url"],
        "repository_commit": config["repository_commit"],
        "checked_out_commit": config["repository_commit"],
        "bucket": expected_bucket,
        "bucket_modulus": config["bucket_modulus"],
        "dataset_sha256": sha256_path(dataset_path),
        "config_sha256": sha256_path(config_path),
    }
    return [f"manifest mismatch: {name}" for name, value in expected.items() if manifest.get(name) != value]


def audit(args: argparse.Namespace) -> dict[str, Any]:
    config = read_json(args.config)
    manifest = read_json(args.input_manifest)
    summary = read_json(args.summary)
    raw = read_jsonl(args.raw_predictions)
    recorded_sources = read_jsonl(args.source_records)
    base = load_module(args.base_module)
    rows = base.load_jsonl(args.dataset)
    examples, sources = prepare(rows, base, int(config["fold_modulus"]))
    bundle = joblib.load(args.model)
    errors = verify_manifest(manifest, config, args.config, args.dataset, summary["phase"])
    checks = (
        (sha256_path(args.config), summary["config_sha256"], "config SHA mismatch"),
        (sha256_path(args.dataset), summary["dataset_sha256"], "dataset SHA mismatch"),
        (sha256_path(args.input_manifest), summary["input_manifest_sha256"], "manifest SHA mismatch"),
        (sha256_path(args.base_module), summary["base_module_sha256"], "base SHA mismatch"),
        (sha256_path(args.raw_predictions), summary["raw_predictions_sha256"], "raw SHA mismatch"),
        (sha256_path(args.source_records), summary["source_records_sha256"], "source records SHA mismatch"),
        (sha256_path(args.model), summary["model"]["sha256"], "model SHA mismatch"),
    )
    for actual, expected, message in checks:
        if actual != expected:
            errors.append(message)
    if summary.get("experiment_id") != "v025":
        errors.append("experiment ID mismatch")
    if sources != recorded_sources:
        errors.append("source records mismatch")
    if bundle.get("anchor_predicate_version") != "viaf-anchor-v1":
        errors.append("anchor predicate version mismatch")
    if set(bundle["full_models"]) != set(METHODS):
        errors.append("full model method set mismatch")

    indexes = np.arange(len(examples), dtype=np.int64)
    raw_map = {item["row_id"]: item for item in raw}
    expected_map = {item["row_id"]: item for item in examples}
    if len(raw_map) != len(raw):
        errors.append("duplicate raw row IDs")
    if set(raw_map) != set(expected_map):
        errors.append("raw row ID set mismatch")
    for row_id in set(raw_map) & set(expected_map):
        row = raw_map[row_id]
        item = expected_map[row_id]
        expected_fold = item["fold"] if summary["phase"] == "development" else None
        if (
            row["task_id"] != item["task_id"]
            or int(row["target"]) != item["target"]
            or row["fold"] != expected_fold
            or bool(row["anchor_present"]) != item["anchor_present"]
            or row["anchor_index"] != item["anchor_index"]
        ):
            errors.append(f"row identity mismatch {row_id}")

    recomputed = {name: np.zeros(len(examples), dtype=np.float64) for name in METHODS}
    fold_records = []
    if summary["phase"] == "development":
        fold_bundles = {int(item["fold"]): item for item in bundle["fold_bundles"]}
        if set(fold_bundles) != set(range(int(config["fold_modulus"]))):
            errors.append("fold bundle set mismatch")
        for fold in range(int(config["fold_modulus"])):
            heldout = np.asarray([i for i, item in enumerate(examples) if item["fold"] == fold], dtype=np.int64)
            train = np.asarray([i for i, item in enumerate(examples) if item["fold"] != fold], dtype=np.int64)
            item = fold_bundles[fold]
            if set(item["models"]) != set(METHODS):
                errors.append(f"fold {fold} model method set mismatch")
            task_ids = sorted({examples[int(i)]["task_id"] for i in heldout})
            if task_ids != item["heldout_task_ids"]:
                errors.append(f"fold {fold} heldout tasks mismatch")
            fold_matrices = matrices(examples, heldout, item["vectorizer"])
            if {name: int(value.shape[1]) for name, value in fold_matrices.items()} != item["feature_dimensions"]:
                errors.append(f"fold {fold} dimensions mismatch")
            for name in METHODS:
                recomputed[name][heldout] = item["models"][name].predict_proba(fold_matrices[name])[:, 1]
            heldout_y = labels(examples, heldout)
            fold_records.append(
                {
                    "fold": fold,
                    "train_tasks": len({examples[int(i)]["task_id"] for i in train}),
                    "train_rows": len(train),
                    "heldout_tasks": len(task_ids),
                    "heldout_rows": len(heldout),
                    "heldout_negatives": int(np.sum(heldout_y == 0)),
                    "heldout_positives": int(np.sum(heldout_y == 1)),
                    "vocabulary": len(item["vectorizer"].vocabulary_),
                }
            )
    else:
        overlap = set(item["task_id"] for item in examples) & set(bundle["development_task_ids"])
        if overlap:
            errors.append("Development/Confirmation task overlap")
        full_matrices = matrices(examples, indexes, bundle["full_vectorizer"])
        for name in METHODS:
            recomputed[name] = bundle["full_models"][name].predict_proba(full_matrices[name])[:, 1]

    max_score_error = 0.0
    for index, item in enumerate(examples):
        recorded = raw_map[item["row_id"]]["scores"]
        if set(recorded) != set(METHODS):
            errors.append(f"score method set mismatch {item['row_id']}")
            continue
        for name in METHODS:
            max_score_error = max(max_score_error, abs(float(recorded[name]) - float(recomputed[name][index])))
    if max_score_error > 1e-12:
        errors.append("model score replay mismatch")

    y = labels(examples, indexes)
    metrics = {name: metric_record(y, recomputed[name]) for name in METHODS}
    strongest = (
        max(COMPARATORS, key=lambda name: (metrics[name]["auc"], name))
        if summary["phase"] == "development"
        else str(bundle["strongest_development_comparator"])
    )
    delta = bootstrap_delta(
        examples,
        indexes,
        recomputed["viaf"],
        recomputed[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    strata = {
        "anchor_present": stratum_delta(examples, indexes, recomputed, True),
        "anchor_absent": stratum_delta(examples, indexes, recomputed, False),
    }
    candidate = metrics["viaf"]
    if summary["phase"] == "development":
        gate_config = config["development_gates"]
        gates = {
            "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"] >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_strongest": delta["point"] >= float(gate_config["candidate_auc_delta_min"]),
            "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] > 0.0,
            "strictly_beats_every_comparator": all(candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS),
            "anchor_present_delta": strata["anchor_present"]["delta"] > 0.0,
            "anchor_absent_delta": strata["anchor_absent"]["delta"] >= float(gate_config["anchor_absent_delta_min"]),
        }
    else:
        gate_config = config["confirmation_gates"]
        gates = {
            "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"] >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_frozen_strongest": delta["point"] > 0.0,
            "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] >= 0.0,
            "strictly_beats_every_comparator": all(candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS),
            "anchor_present_delta": strata["anchor_present"]["delta"] > 0.0,
            "anchor_absent_delta": strata["anchor_absent"]["delta"] >= float(gate_config["anchor_absent_delta_min"]),
            "task_ids_disjoint": True,
        }

    max_metric_error = max(
        maximum_error(metrics, summary["metrics"]),
        maximum_error(delta, summary["candidate_minus_strongest"]),
        maximum_error(strata, summary["anchor_strata"]),
        maximum_error(gates, summary["gates"]),
    )
    if summary["phase"] == "development":
        max_metric_error = max(max_metric_error, maximum_error(fold_records, summary["folds"]))
        full_matrices = matrices(examples, indexes, bundle["full_vectorizer"])
        full_dimensions = {name: int(value.shape[1]) for name, value in full_matrices.items()}
        max_metric_error = max(max_metric_error, maximum_error(full_dimensions, summary["full_feature_dimensions"]))
    if strongest != summary["strongest_comparator"]:
        errors.append("strongest comparator mismatch")
    if max_metric_error > 1e-12:
        errors.append("metric, gate, fold, or dimension mismatch")

    return {
        "schema_version": 1,
        "phase": summary["phase"],
        "status": "AUDIT_OK" if not errors else "AUDIT_ERROR",
        "errors": errors,
        "source_rows": len(rows),
        "evaluated_rows": len(examples),
        "tasks_checked": len({item["task_id"] for item in examples}),
        "source_records_checked": len(sources),
        "models_replayed": len(METHODS) * (int(config["fold_modulus"]) if summary["phase"] == "development" else 1),
        "scores_replayed": len(examples) * len(METHODS),
        "maximum_score_error": max_score_error,
        "maximum_metric_error": max_metric_error,
        "config_sha256": sha256_path(args.config),
        "dataset_sha256": sha256_path(args.dataset),
        "input_manifest_sha256": sha256_path(args.input_manifest),
        "raw_predictions_sha256": sha256_path(args.raw_predictions),
        "summary_sha256": sha256_path(args.summary),
        "model_sha256": sha256_path(args.model),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--input-manifest", type=Path, required=True)
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
