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
    "direct",
    "triple_query",
    "consensus_no_abs",
    "single_support",
    "cross_model_consensus",
    "generator_balanced_consensus",
)
COMPARATORS = METHODS[:-1]


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
    spec = importlib.util.spec_from_file_location("v040_audit_base_v012", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fold_for_task(task_id: str, modulus: int) -> int:
    return hashlib.sha256(task_id.encode("utf-8")).digest()[1] % modulus


def prepare(
    rows: list[dict[str, Any]], base: Any, models: tuple[str, ...], fold_modulus: int
) -> tuple[list[dict[str, Any]], list[str], list[str], list[dict[str, Any]]]:
    if len({str(row["row_id"]) for row in rows}) != len(rows):
        raise ValueError("duplicate source row IDs")
    if {str(row["model"]) for row in rows} != set(models):
        raise ValueError("generator model set mismatch")
    baseline_models: dict[str, set[str]] = defaultdict(set)
    all_tasks = sorted({str(row["task_id"]) for row in rows})
    for row in rows:
        if int(row["target"]) == 0:
            baseline_models[str(row["task_id"])].add(str(row["model"]))
    eligible = sorted(task for task in all_tasks if baseline_models[task] == set(models))
    eligible_set = set(eligible)
    excluded = sorted(set(all_tasks) - eligible_set)
    examples = []
    sources = []
    for row in rows:
        task_id = str(row["task_id"])
        if task_id not in eligible_set:
            continue
        item = {
            "row": row,
            "row_id": str(row["row_id"]),
            "task_id": task_id,
            "model": str(row["model"]),
            "target": int(row["target"]),
            "fold": fold_for_task(task_id, fold_modulus),
            "text": base.action_text(row),
        }
        examples.append(item)
    examples.sort(key=lambda item: (item["task_id"], item["model"], item["row_id"]))
    for item in examples:
        row = item["row"]
        sources.append(
            {
                "row_id": item["row_id"],
                "task_id": item["task_id"],
                "source_relative_path": str(row["source_relative_path"]),
                "source_sha256": str(row["source_sha256"]),
            }
        )
    return examples, eligible, excluded, sources


def baseline_indexes(examples: list[dict[str, Any]]) -> dict[str, list[int]]:
    result: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(examples):
        if item["target"] == 0:
            result[item["task_id"]].append(index)
    for task_id in result:
        result[task_id].sort(key=lambda index: (examples[index]["model"], examples[index]["row_id"]))
    return result


def supports(
    examples: list[dict[str, Any]], baselines: dict[str, list[int]], query_index: int, target_model: str
) -> list[int]:
    query = examples[query_index]
    excluded_models = {query["model"], target_model}
    result = [
        index
        for index in baselines[query["task_id"]]
        if examples[index]["model"] not in excluded_models
    ]
    if not result:
        raise ValueError(f"missing cross-model support {query['row_id']}")
    return result


def pair_indexes(
    examples: list[dict[str, Any]],
    baselines: dict[str, list[int]],
    indexes: np.ndarray,
    target_model: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    query_indexes = []
    reference_indexes = []
    weights = []
    counts = []
    for index in indexes:
        allowed = supports(examples, baselines, int(index), target_model)
        counts.append(len(allowed))
        for reference in allowed:
            query_indexes.append(int(index))
            reference_indexes.append(reference)
            weights.append(1.0 / len(allowed))
    return (
        np.asarray(query_indexes, dtype=np.int64),
        np.asarray(reference_indexes, dtype=np.int64),
        np.asarray(weights, dtype=np.float64),
        counts,
    )


def generator_balanced_mean(
    values: np.ndarray,
    examples: list[dict[str, Any]],
    reference_indexes: np.ndarray,
) -> float:
    grouped: dict[str, list[float]] = defaultdict(list)
    for value, index in zip(values, reference_indexes, strict=True):
        grouped[str(examples[int(index)]["model"])].append(float(value))
    return float(np.mean([np.mean(grouped[model]) for model in sorted(grouped)]))


def pair_matrices(
    matrix: sparse.csr_matrix, query_indexes: np.ndarray, reference_indexes: np.ndarray
) -> tuple[sparse.csr_matrix, sparse.csr_matrix]:
    query = matrix[query_indexes]
    reference = matrix[reference_indexes]
    absolute = abs(query - reference).tocsr()
    return (
        sparse.hstack([query, reference, reference], format="csr"),
        sparse.hstack([query, reference, absolute], format="csr"),
    )


def labels(examples: list[dict[str, Any]], indexes: np.ndarray) -> np.ndarray:
    return np.asarray([examples[int(index)]["target"] for index in indexes], dtype=np.int64)


def score_bundle(
    bundle: dict[str, Any],
    examples: list[dict[str, Any]],
    baselines: dict[str, list[int]],
    indexes: np.ndarray,
) -> tuple[dict[str, np.ndarray], list[int], int]:
    matrix = bundle["vectorizer"].transform([item["text"] for item in examples]).tocsr()
    query = matrix[indexes]
    scores = {
        "direct": bundle["direct_model"].predict_proba(query)[:, 1],
        "triple_query": bundle["triple_model"].predict_proba(
            sparse.hstack([query, query, query], format="csr")
        )[:, 1],
        "consensus_no_abs": np.zeros(len(indexes), dtype=np.float64),
        "single_support": np.zeros(len(indexes), dtype=np.float64),
        "cross_model_consensus": np.zeros(len(indexes), dtype=np.float64),
        "generator_balanced_consensus": np.zeros(len(indexes), dtype=np.float64),
    }
    pair_query, pair_reference, _, counts = pair_indexes(
        examples, baselines, indexes, str(bundle["target_model"])
    )
    no_abs, candidate = pair_matrices(matrix, pair_query, pair_reference)
    no_abs_scores = bundle["no_abs_model"].predict_proba(no_abs)[:, 1]
    pair_scores = bundle["candidate_model"].predict_proba(candidate)[:, 1]
    offset = 0
    for local_index, count in enumerate(counts):
        end = offset + count
        scores["consensus_no_abs"][local_index] = float(np.mean(no_abs_scores[offset:end]))
        scores["single_support"][local_index] = float(pair_scores[offset])
        scores["cross_model_consensus"][local_index] = float(np.mean(pair_scores[offset:end]))
        references = pair_reference[offset:end]
        scores["generator_balanced_consensus"][local_index] = generator_balanced_mean(
            pair_scores[offset:end], examples, references
        )
        offset = end
    if offset != len(pair_query):
        raise ValueError("pair aggregation cardinality mismatch")
    return scores, counts, len(pair_query)


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
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
    candidate: np.ndarray,
    comparator: np.ndarray,
    repeats: int,
    seed: int,
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
        rows = [row for task in selected for row in task_rows[str(task)]]
        sampled_y = y[rows]
        if len(np.unique(sampled_y)) != 2:
            raise ValueError("bootstrap sample lost one class")
        samples.append(
            float(
                roc_auc_score(sampled_y, candidate[rows])
                - roc_auc_score(sampled_y, comparator[rows])
            )
        )
    return {
        "point": point,
        "bootstrap_95": [float(np.quantile(samples, 0.025)), float(np.quantile(samples, 0.975))],
        "repeats": repeats,
        "resampling_unit": "task_id",
        "tasks": len(tasks),
    }


def generator_slices(
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
    scores: dict[str, np.ndarray],
    strongest: str,
    models: tuple[str, ...],
) -> dict[str, Any]:
    result = {}
    for model in models:
        local = np.asarray(
            [int(index) for index in indexes if examples[int(index)]["model"] == model], dtype=np.int64
        )
        y = labels(examples, local)
        candidate_auc = float(
            roc_auc_score(y, scores["generator_balanced_consensus"][local])
        )
        comparator_auc = float(roc_auc_score(y, scores[strongest][local]))
        result[model] = {
            "rows": len(local),
            "negatives": int(np.sum(y == 0)),
            "positives": int(np.sum(y == 1)),
            "candidate_auc": candidate_auc,
            "strongest_auc": comparator_auc,
            "delta": candidate_auc - comparator_auc,
        }
    return result


def maximum_error(left: Any, right: Any) -> float:
    if isinstance(left, dict) and isinstance(right, dict):
        if set(left) != set(right):
            return math.inf
        return max((maximum_error(left[key], right[key]) for key in left), default=0.0)
    if isinstance(left, (list, tuple)) and isinstance(right, (list, tuple)):
        if len(left) != len(right):
            return math.inf
        return max((maximum_error(a, b) for a, b in zip(left, right)), default=0.0)
    if isinstance(left, bool) or isinstance(right, bool) or left is None or right is None:
        return 0.0 if left == right else math.inf
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(float(left) - float(right))
    return 0.0 if left == right else math.inf


def validate_bundle_metadata(
    bundle: dict[str, Any],
    examples: list[dict[str, Any]],
    baselines: dict[str, list[int]],
    train: np.ndarray,
    target_model: str,
) -> list[str]:
    errors = []
    pair_query, _, pair_weight, counts = pair_indexes(
        examples, baselines, train, target_model
    )
    y = labels(examples, train)
    class_counts = {value: int(np.sum(y == value)) for value in (0, 1)}
    class_weight = {value: len(y) / (2.0 * class_counts[value]) for value in (0, 1)}
    expected = {
        "target_model": target_model,
        "train_rows": len(train),
        "train_pairs": len(pair_query),
        "train_query_class_counts": class_counts,
        "pair_class_weight": class_weight,
        "train_pair_weight_sum": float(np.sum(pair_weight)),
        "train_support_count_min": min(counts),
        "train_support_count_max": max(counts),
    }
    for key, value in expected.items():
        if maximum_error(bundle.get(key), value) > 1e-12:
            errors.append(f"bundle metadata mismatch {target_model}:{key}")
    if maximum_error(bundle["no_abs_model"].class_weight, class_weight) > 1e-12:
        errors.append(f"no-abs class weight mismatch {target_model}")
    if maximum_error(bundle["candidate_model"].class_weight, class_weight) > 1e-12:
        errors.append(f"Candidate class weight mismatch {target_model}")
    return errors


def verify_manifests(
    config: dict[str, Any],
    config_path: Path,
    datasets: list[Path],
    manifests: list[Path],
    phase: str,
) -> list[str]:
    errors = []
    if len(datasets) != len(manifests):
        return ["dataset/manifest cardinality mismatch"]
    observed = set()
    for dataset_path, manifest_path in zip(datasets, manifests, strict=True):
        manifest = read_json(manifest_path)
        dataset_sha = sha256_path(dataset_path)
        manifest_sha = sha256_path(manifest_path)
        bucket = int(manifest["bucket"])
        acquisition_phase = phase
        if phase == "development":
            matching = [
                item
                for item in config["development_inputs"]
                if int(item["bucket"]) == bucket
                and str(item["dataset_sha256"]) == dataset_sha
                and str(item["manifest_sha256"]) == manifest_sha
            ]
            if len(matching) == 1:
                acquisition_phase = str(matching[0]["acquisition_phase"])
        expected = {
            "phase": acquisition_phase,
            "repository_url": config["repository_url"],
            "repository_commit": config["repository_commit"],
            "checked_out_commit": config["repository_commit"],
            "bucket_modulus": config["bucket_modulus"],
            "dataset_sha256": dataset_sha,
        }
        if phase == "confirmation":
            expected.update(
                {
                    "bucket": config["confirmation_bucket"],
                    "config_sha256": sha256_path(config_path),
                }
            )
        for key, value in expected.items():
            if manifest.get(key) != value:
                errors.append(f"manifest mismatch {bucket}:{key}")
        observed.add((dataset_sha, manifest_sha, bucket))
    if phase == "development":
        expected_inputs = {
            (str(item["dataset_sha256"]), str(item["manifest_sha256"]), int(item["bucket"]))
            for item in config["development_inputs"]
        }
        if observed != expected_inputs:
            errors.append("Development input set mismatch")
    elif len(datasets) != 1:
        errors.append("Confirmation input count mismatch")
    return errors


def audit(args: argparse.Namespace) -> dict[str, Any]:
    config = read_json(args.config)
    summary = read_json(args.summary)
    phase = str(summary["phase"])
    base = load_module(args.base_module)
    rows = []
    for dataset in args.dataset:
        rows.extend(base.load_jsonl(dataset))
    models = tuple(str(value) for value in config["generator_models"])
    examples, eligible, excluded, sources = prepare(
        rows, base, models, int(config["task_fold_modulus"])
    )
    baselines = baseline_indexes(examples)
    raw = read_jsonl(args.raw_predictions)
    recorded_sources = read_jsonl(args.source_records)
    model_bundle = joblib.load(args.model)
    errors = verify_manifests(config, args.config, args.dataset, args.input_manifest, phase)
    identity_checks = (
        (sha256_path(args.candidate), config["candidate_sha256"], "Candidate SHA mismatch"),
        (
            sha256_path(args.evidence_packet),
            config["evidence_packet_sha256"],
            "Evidence Packet SHA mismatch",
        ),
        (sha256_path(args.base_module), config["base_module_sha256"], "base SHA mismatch"),
        (sha256_path(args.config), summary["config_sha256"], "config SHA mismatch"),
        (sha256_path(args.base_module), summary["base_module_sha256"], "summary base SHA mismatch"),
        (sha256_path(args.raw_predictions), summary["raw_predictions_sha256"], "raw SHA mismatch"),
        (sha256_path(args.source_records), summary["source_records_sha256"], "source SHA mismatch"),
        (sha256_path(args.model), summary["model"]["sha256"], "model SHA mismatch"),
    )
    for actual, expected, message in identity_checks:
        if actual != expected:
            errors.append(message)
    if summary.get("experiment_id") != "v040" or model_bundle.get("experiment_id") != "v040":
        errors.append("experiment ID mismatch")
    if tuple(model_bundle.get("models", ())) != models:
        errors.append("model family set mismatch")
    if tuple(model_bundle.get("method_names", ())) != METHODS:
        errors.append("method set mismatch")
    if phase == "development":
        if model_bundle.get("development_task_ids") != sorted(eligible):
            errors.append("frozen Development task IDs mismatch")
        if model_bundle.get("excluded_development_task_ids") != sorted(excluded):
            errors.append("frozen excluded task IDs mismatch")
    if sources != recorded_sources:
        errors.append("source records mismatch")
    if summary.get("dataset_sha256s") != [sha256_path(path) for path in args.dataset]:
        errors.append("summary dataset SHA list mismatch")
    if summary.get("input_manifest_sha256s") != [sha256_path(path) for path in args.input_manifest]:
        errors.append("summary manifest SHA list mismatch")
    if summary.get("input_buckets") != [int(read_json(path)["bucket"]) for path in args.input_manifest]:
        errors.append("summary input bucket list mismatch")
    if int(summary.get("source_rows", -1)) != len(rows) or int(summary.get("evaluated_rows", -1)) != len(examples):
        errors.append("summary source/evaluated row count mismatch")
    if int(summary["model"].get("bytes", -1)) != args.model.stat().st_size:
        errors.append("summary model byte count mismatch")

    indexes = np.arange(len(examples), dtype=np.int64)
    recomputed = {name: np.full(len(examples), np.nan, dtype=np.float64) for name in METHODS}
    support_counts = np.zeros(len(examples), dtype=np.int64)
    fold_records = []
    pair_records = []
    if phase == "development":
        expected_keys = {(model, fold) for model in models for fold in range(int(config["task_fold_modulus"]))}
        fold_bundles = {(str(item["target_model"]), int(item["fold"])): item for item in model_bundle["fold_bundles"]}
        if set(fold_bundles) != expected_keys or len(fold_bundles) != len(model_bundle["fold_bundles"]):
            errors.append("fold bundle key set mismatch")
        for target_model in models:
            for fold in range(int(config["task_fold_modulus"])):
                train = np.asarray(
                    [
                        index
                        for index, item in enumerate(examples)
                        if item["fold"] != fold and item["model"] != target_model
                    ],
                    dtype=np.int64,
                )
                heldout = np.asarray(
                    [
                        index
                        for index, item in enumerate(examples)
                        if item["fold"] == fold and item["model"] == target_model
                    ],
                    dtype=np.int64,
                )
                bundle = fold_bundles[(target_model, fold)]
                errors.extend(validate_bundle_metadata(bundle, examples, baselines, train, target_model))
                expected_tasks = sorted({examples[int(index)]["task_id"] for index in heldout})
                if bundle.get("heldout_task_ids") != expected_tasks:
                    errors.append(f"heldout tasks mismatch {target_model}:{fold}")
                scores, counts, heldout_pairs = score_bundle(bundle, examples, baselines, heldout)
                for name in METHODS:
                    recomputed[name][heldout] = scores[name]
                support_counts[heldout] = np.asarray(counts, dtype=np.int64)
                y = labels(examples, heldout)
                fold_records.append(
                    {
                        "target_model": target_model,
                        "fold": fold,
                        "train_tasks": len({examples[int(index)]["task_id"] for index in train}),
                        "train_rows": len(train),
                        "train_pairs": bundle["train_pairs"],
                        "heldout_tasks": len(expected_tasks),
                        "heldout_rows": len(heldout),
                        "heldout_pairs": heldout_pairs,
                        "heldout_negatives": int(np.sum(y == 0)),
                        "heldout_positives": int(np.sum(y == 1)),
                        "vocabulary": len(bundle["vectorizer"].vocabulary_),
                        "support_count_min": min(counts),
                        "support_count_max": max(counts),
                    }
                )
        if set(model_bundle["full_bundles"]) != set(models):
            errors.append("full bundle key set mismatch")
        else:
            for target_model in models:
                train = np.asarray(
                    [index for index, item in enumerate(examples) if item["model"] != target_model],
                    dtype=np.int64,
                )
                errors.extend(
                    validate_bundle_metadata(
                        model_bundle["full_bundles"][target_model],
                        examples,
                        baselines,
                        train,
                        target_model,
                    )
                )
    elif phase == "confirmation":
        overlap = sorted(set(eligible) & set(model_bundle["development_task_ids"]))
        if overlap:
            errors.append("Development/Confirmation task overlap")
        for target_model in models:
            heldout = np.asarray(
                [index for index, item in enumerate(examples) if item["model"] == target_model],
                dtype=np.int64,
            )
            bundle = model_bundle["full_bundles"][target_model]
            scores, counts, pairs = score_bundle(bundle, examples, baselines, heldout)
            for name in METHODS:
                recomputed[name][heldout] = scores[name]
            support_counts[heldout] = np.asarray(counts, dtype=np.int64)
            pair_records.append(
                {
                    "target_model": target_model,
                    "rows": len(heldout),
                    "pairs": pairs,
                    "support_count_min": min(counts),
                    "support_count_max": max(counts),
                }
            )
    else:
        errors.append("unknown phase")
    if any(np.isnan(recomputed[name]).any() for name in METHODS):
        errors.append("incomplete score replay")

    raw_map = {str(item["row_id"]): item for item in raw}
    if len(raw_map) != len(raw) or set(raw_map) != {item["row_id"] for item in examples}:
        errors.append("raw row identity set mismatch")
    max_score_error = 0.0
    for index, item in enumerate(examples):
        recorded = raw_map.get(item["row_id"])
        if recorded is None:
            continue
        expected_supports = supports(examples, baselines, index, item["model"])
        identity = {
            "phase": "development_oof" if phase == "development" else "confirmation",
            "fold": item["fold"] if phase == "development" else None,
            "row_id": item["row_id"],
            "task_id": item["task_id"],
            "model": item["model"],
            "target": item["target"],
            "source_dataset": item["row"]["source_dataset"],
            "observed_categories": item["row"].get("observed_categories", []),
            "support_count": int(support_counts[index]),
            "support_row_ids": [examples[value]["row_id"] for value in expected_supports],
            "support_models": [examples[value]["model"] for value in expected_supports],
        }
        for key, value in identity.items():
            if recorded.get(key) != value:
                errors.append(f"raw identity mismatch {item['row_id']}:{key}")
        if set(recorded.get("scores", {})) != set(METHODS):
            errors.append(f"raw method set mismatch {item['row_id']}")
            continue
        for name in METHODS:
            max_score_error = max(
                max_score_error, abs(float(recorded["scores"][name]) - float(recomputed[name][index]))
            )
    if max_score_error > 1e-12:
        errors.append("model score replay mismatch")

    y = labels(examples, indexes)
    metrics = {name: metric_record(y, recomputed[name]) for name in METHODS}
    strongest = (
        max(COMPARATORS, key=lambda name: (metrics[name]["auc"], name))
        if phase == "development"
        else str(model_bundle["strongest_development_comparator"])
    )
    if phase == "development" and model_bundle.get("strongest_development_comparator") != strongest:
        errors.append("frozen strongest Development comparator mismatch")
    delta = bootstrap_delta(
        examples,
        indexes,
        recomputed["generator_balanced_consensus"],
        recomputed[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    slices = generator_slices(examples, indexes, recomputed, strongest, models)
    positive_slices = sum(record["delta"] > 0.0 for record in slices.values())
    candidate = metrics["generator_balanced_consensus"]
    eligible_fraction = len(eligible) / len({str(row["task_id"]) for row in rows})
    if phase == "development":
        gate_config = config["development_gates"]
        gates = {
            "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
            >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_strongest": delta["point"]
            >= float(gate_config["candidate_auc_delta_min"]),
            "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] > 0.0,
            "strictly_beats_every_comparator": all(
                candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS
            ),
            "all_generator_slices_nonnegative": all(
                record["delta"] >= 0.0 for record in slices.values()
            ),
            "minimum_positive_generator_slices": positive_slices
            >= int(gate_config["minimum_positive_generator_slices"]),
            "eligible_task_fraction": eligible_fraction
            >= float(gate_config["eligible_task_fraction_min"]),
        }
    else:
        gate_config = config["confirmation_gates"]
        gates = {
            "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
            "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
            >= float(gate_config["candidate_tpr_at_5fpr_min"]),
            "auc_delta_vs_frozen_strongest": delta["point"] > 0.0,
            "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] >= 0.0,
            "strictly_beats_every_comparator": all(
                candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS
            ),
            "all_generator_slices_nonnegative": all(
                record["delta"] >= 0.0 for record in slices.values()
            ),
            "minimum_positive_generator_slices": positive_slices
            >= int(gate_config["minimum_positive_generator_slices"]),
            "eligible_task_fraction": eligible_fraction
            >= float(gate_config["eligible_task_fraction_min"]),
            "task_ids_disjoint": True,
        }
    structural = {
        "source_tasks": len({str(row["task_id"]) for row in rows}),
        "eligible_tasks": len(eligible),
        "eligible_task_fraction": eligible_fraction,
        "excluded_task_ids": excluded,
        "rows": len(examples),
        "support_count_min": int(np.min(support_counts)),
        "support_count_median": float(np.median(support_counts)),
        "support_count_max": int(np.max(support_counts)),
        "metrics": metrics,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "generator_slices": slices,
        "positive_generator_slices": positive_slices,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
    }
    structural["folds" if phase == "development" else "pair_records"] = (
        fold_records if phase == "development" else pair_records
    )
    if phase == "confirmation":
        structural["development_task_overlap"] = []
    max_metric_error = max(
        (maximum_error(value, summary.get(key)) for key, value in structural.items()), default=0.0
    )
    if max_metric_error > 1e-12:
        errors.append("metric, gate, slice, or structural replay mismatch")

    return {
        "schema_version": 1,
        "phase": phase,
        "status": "AUDIT_OK" if not errors else "AUDIT_ERROR",
        "errors": errors,
        "source_rows": len(rows),
        "evaluated_rows": len(examples),
        "eligible_tasks": len(eligible),
        "excluded_tasks": len(excluded),
        "source_records_checked": len(sources),
        "bundles_replayed": len(models) * int(config["task_fold_modulus"])
        if phase == "development"
        else len(models),
        "scores_replayed": len(examples) * len(METHODS),
        "maximum_score_error": max_score_error,
        "maximum_metric_error": max_metric_error,
        "config_sha256": sha256_path(args.config),
        "candidate_sha256": sha256_path(args.candidate),
        "evidence_packet_sha256": sha256_path(args.evidence_packet),
        "dataset_sha256s": [sha256_path(path) for path in args.dataset],
        "input_manifest_sha256s": [sha256_path(path) for path in args.input_manifest],
        "raw_predictions_sha256": sha256_path(args.raw_predictions),
        "summary_sha256": sha256_path(args.summary),
        "model_sha256": sha256_path(args.model),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--evidence-packet", type=Path, required=True)
    parser.add_argument("--dataset", action="append", type=Path, required=True)
    parser.add_argument("--input-manifest", action="append", type=Path, required=True)
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
                "bundles_replayed": report["bundles_replayed"],
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
