from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import scipy
import sklearn
import torch
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


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for value in values:
            stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("v040_base_v012", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fold_for_task(task_id: str, modulus: int) -> int:
    return hashlib.sha256(task_id.encode("utf-8")).digest()[1] % modulus


def verify_inputs(
    config: dict[str, Any],
    config_path: Path,
    dataset_paths: list[Path],
    manifest_paths: list[Path],
    phase: str,
) -> list[dict[str, Any]]:
    if len(dataset_paths) != len(manifest_paths):
        raise ValueError("dataset/manifest cardinality mismatch")
    if phase == "development":
        expected = {
            (str(item["dataset_sha256"]), str(item["manifest_sha256"]), int(item["bucket"])):
            str(item["acquisition_phase"])
            for item in config["development_inputs"]
        }
        if len(dataset_paths) != len(expected):
            raise ValueError("Development input count mismatch")
    else:
        if len(dataset_paths) != 1:
            raise ValueError("Confirmation requires one dataset")
        expected = None

    manifests = []
    observed = set()
    for dataset_path, manifest_path in zip(dataset_paths, manifest_paths, strict=True):
        manifest = read_json(manifest_path)
        dataset_sha = sha256_path(dataset_path)
        manifest_sha = sha256_path(manifest_path)
        bucket = int(manifest["bucket"])
        if manifest["dataset_sha256"] != dataset_sha:
            raise ValueError("manifest dataset SHA mismatch")
        if manifest["repository_url"] != config["repository_url"]:
            raise ValueError("repository URL mismatch")
        if manifest["repository_commit"] != config["repository_commit"]:
            raise ValueError("repository commit mismatch")
        if manifest["checked_out_commit"] != config["repository_commit"]:
            raise ValueError("checked-out commit mismatch")
        if int(manifest["bucket_modulus"]) != int(config["bucket_modulus"]):
            raise ValueError("bucket modulus mismatch")
        input_key = (dataset_sha, manifest_sha, bucket)
        expected_phase = expected.get(input_key) if expected is not None else phase
        if expected_phase is not None and manifest["phase"] != expected_phase:
            raise ValueError("manifest acquisition phase mismatch")
        if phase == "confirmation":
            if bucket != int(config["confirmation_bucket"]):
                raise ValueError("Confirmation bucket mismatch")
            if manifest["config_sha256"] != sha256_path(config_path):
                raise ValueError("Confirmation config SHA mismatch")
        observed.add((dataset_sha, manifest_sha, bucket))
        manifests.append(manifest)
    if expected is not None and observed != set(expected):
        raise ValueError("Development input set mismatch")
    return manifests


def prepare_examples(
    rows: list[dict[str, Any]], base: Any, models: tuple[str, ...], fold_modulus: int
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    if len({str(row["row_id"]) for row in rows}) != len(rows):
        raise ValueError("duplicate row IDs")
    if set(str(row["model"]) for row in rows) != set(models):
        raise ValueError("generator model set mismatch")

    baseline_models: dict[str, set[str]] = defaultdict(set)
    all_tasks = sorted({str(row["task_id"]) for row in rows})
    for row in rows:
        if int(row["target"]) == 0:
            baseline_models[str(row["task_id"])].add(str(row["model"]))
    eligible_tasks = sorted(task for task in all_tasks if baseline_models[task] == set(models))
    eligible_set = set(eligible_tasks)
    excluded_tasks = sorted(set(all_tasks) - eligible_set)

    examples = []
    for row in rows:
        task_id = str(row["task_id"])
        if task_id not in eligible_set:
            continue
        examples.append(
            {
                "row": row,
                "row_id": str(row["row_id"]),
                "task_id": task_id,
                "model": str(row["model"]),
                "target": int(row["target"]),
                "fold": fold_for_task(task_id, fold_modulus),
                "text": base.action_text(row),
            }
        )
    examples.sort(key=lambda item: (item["task_id"], item["model"], item["row_id"]))
    return examples, eligible_tasks, excluded_tasks


def baseline_indexes(examples: list[dict[str, Any]]) -> dict[str, list[int]]:
    result: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(examples):
        if item["target"] == 0:
            result[item["task_id"]].append(index)
    for task_id in result:
        result[task_id].sort(key=lambda index: (examples[index]["model"], examples[index]["row_id"]))
    return result


def support_indexes(
    examples: list[dict[str, Any]],
    baselines: dict[str, list[int]],
    query_index: int,
    target_model: str,
) -> list[int]:
    query = examples[query_index]
    excluded_models = {query["model"], target_model}
    supports = [
        index
        for index in baselines[query["task_id"]]
        if examples[index]["model"] not in excluded_models
    ]
    if not supports:
        raise ValueError(f"query lacks allowed cross-model support: {query['row_id']}")
    return supports


def pair_indexes(
    examples: list[dict[str, Any]],
    baselines: dict[str, list[int]],
    query_indexes: np.ndarray,
    target_model: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    queries = []
    references = []
    weights = []
    counts = []
    for query_index in query_indexes:
        supports = support_indexes(examples, baselines, int(query_index), target_model)
        counts.append(len(supports))
        for support_index in supports:
            queries.append(int(query_index))
            references.append(support_index)
            weights.append(1.0 / len(supports))
    return (
        np.asarray(queries, dtype=np.int64),
        np.asarray(references, dtype=np.int64),
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
    no_abs = sparse.hstack([query, reference, reference], format="csr")
    candidate = sparse.hstack([query, reference, absolute], format="csr")
    return no_abs, candidate


def fit_bundle(
    examples: list[dict[str, Any]],
    baselines: dict[str, list[int]],
    train_indexes: np.ndarray,
    target_model: str,
    config: dict[str, Any],
    base: Any,
) -> dict[str, Any]:
    y = np.asarray([examples[int(index)]["target"] for index in train_indexes], dtype=np.int64)
    base.ensure_two_classes(y, "CMCD training rows")
    vectorizer = base.make_vectorizer(config)
    vectorizer.fit([examples[int(index)]["text"] for index in train_indexes])
    all_matrix = vectorizer.transform([item["text"] for item in examples]).tocsr()
    query = all_matrix[train_indexes]
    triple = sparse.hstack([query, query, query], format="csr")
    direct_model = base.make_classifier(config).fit(query, y)
    triple_model = base.make_classifier(config).fit(triple, y)

    pair_query, pair_reference, pair_weight, counts = pair_indexes(
        examples, baselines, train_indexes, target_model
    )
    pair_y = np.asarray([examples[int(index)]["target"] for index in pair_query], dtype=np.int64)
    query_class_counts = {value: int(np.sum(y == value)) for value in (0, 1)}
    query_class_weight = {
        value: len(y) / (2.0 * query_class_counts[value]) for value in (0, 1)
    }
    no_abs, candidate = pair_matrices(all_matrix, pair_query, pair_reference)
    no_abs_model = base.make_classifier(config).set_params(class_weight=query_class_weight)
    candidate_model = base.make_classifier(config).set_params(class_weight=query_class_weight)
    no_abs_model.fit(no_abs, pair_y, sample_weight=pair_weight)
    candidate_model.fit(candidate, pair_y, sample_weight=pair_weight)
    return {
        "target_model": target_model,
        "vectorizer": vectorizer,
        "direct_model": direct_model,
        "triple_model": triple_model,
        "no_abs_model": no_abs_model,
        "candidate_model": candidate_model,
        "train_rows": len(train_indexes),
        "train_pairs": len(pair_query),
        "train_query_class_counts": query_class_counts,
        "pair_class_weight": query_class_weight,
        "train_pair_weight_sum": float(np.sum(pair_weight)),
        "train_support_count_min": min(counts),
        "train_support_count_max": max(counts),
        "feature_dimensions": {
            "direct": int(query.shape[1]),
            "triple_query": int(triple.shape[1]),
            "consensus_no_abs": int(no_abs.shape[1]),
            "single_support": int(candidate.shape[1]),
            "cross_model_consensus": int(candidate.shape[1]),
            "generator_balanced_consensus": int(candidate.shape[1]),
        },
    }


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
    no_abs_pair_scores = bundle["no_abs_model"].predict_proba(no_abs)[:, 1]
    candidate_pair_scores = bundle["candidate_model"].predict_proba(candidate)[:, 1]
    offset = 0
    for local_index, count in enumerate(counts):
        end = offset + count
        scores["consensus_no_abs"][local_index] = float(np.mean(no_abs_pair_scores[offset:end]))
        scores["single_support"][local_index] = float(candidate_pair_scores[offset])
        scores["cross_model_consensus"][local_index] = float(
            np.mean(candidate_pair_scores[offset:end])
        )
        references = pair_reference[offset:end]
        scores["generator_balanced_consensus"][local_index] = generator_balanced_mean(
            candidate_pair_scores[offset:end], examples, references
        )
        offset = end
    if offset != len(pair_query):
        raise ValueError("pair aggregation cardinality mismatch")
    return scores, counts, len(pair_query)


def labels(examples: list[dict[str, Any]], indexes: np.ndarray) -> np.ndarray:
    return np.asarray([examples[int(index)]["target"] for index in indexes], dtype=np.int64)


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


def method_metrics(
    examples: list[dict[str, Any]], indexes: np.ndarray, global_scores: dict[str, np.ndarray]
) -> dict[str, dict[str, Any]]:
    y = labels(examples, indexes)
    return {name: metric_record(y, global_scores[name][indexes]) for name in METHODS}


def generator_slices(
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
    global_scores: dict[str, np.ndarray],
    strongest: str,
    models: tuple[str, ...],
) -> dict[str, Any]:
    result = {}
    for model in models:
        local = np.asarray(
            [int(index) for index in indexes if examples[int(index)]["model"] == model],
            dtype=np.int64,
        )
        y = labels(examples, local)
        candidate_auc = float(
            roc_auc_score(y, global_scores["generator_balanced_consensus"][local])
        )
        comparator_auc = float(roc_auc_score(y, global_scores[strongest][local]))
        result[model] = {
            "rows": len(local),
            "negatives": int(np.sum(y == 0)),
            "positives": int(np.sum(y == 1)),
            "candidate_auc": candidate_auc,
            "strongest_auc": comparator_auc,
            "delta": candidate_auc - comparator_auc,
        }
    return result


def fit_development(
    examples: list[dict[str, Any]],
    eligible_tasks: list[str],
    excluded_tasks: list[str],
    all_task_count: int,
    config: dict[str, Any],
    base: Any,
) -> tuple[dict[str, Any], dict[str, np.ndarray], list[dict[str, Any]], dict[str, Any]]:
    models = tuple(str(value) for value in config["generator_models"])
    folds = int(config["task_fold_modulus"])
    baselines = baseline_indexes(examples)
    global_scores = {name: np.full(len(examples), np.nan, dtype=np.float64) for name in METHODS}
    support_counts = np.zeros(len(examples), dtype=np.int64)
    fold_bundles = []
    fold_records = []
    for target_model in models:
        for fold in range(folds):
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
            bundle = fit_bundle(examples, baselines, train, target_model, config, base)
            scores, counts, heldout_pairs = score_bundle(bundle, examples, baselines, heldout)
            for name in METHODS:
                global_scores[name][heldout] = scores[name]
            support_counts[heldout] = np.asarray(counts, dtype=np.int64)
            bundle["fold"] = fold
            bundle["heldout_task_ids"] = sorted({examples[int(i)]["task_id"] for i in heldout})
            fold_bundles.append(bundle)
            heldout_y = labels(examples, heldout)
            fold_records.append(
                {
                    "target_model": target_model,
                    "fold": fold,
                    "train_tasks": len({examples[int(i)]["task_id"] for i in train}),
                    "train_rows": len(train),
                    "train_pairs": bundle["train_pairs"],
                    "heldout_tasks": len({examples[int(i)]["task_id"] for i in heldout}),
                    "heldout_rows": len(heldout),
                    "heldout_pairs": heldout_pairs,
                    "heldout_negatives": int(np.sum(heldout_y == 0)),
                    "heldout_positives": int(np.sum(heldout_y == 1)),
                    "vocabulary": len(bundle["vectorizer"].vocabulary_),
                    "support_count_min": min(counts),
                    "support_count_max": max(counts),
                }
            )
    indexes = np.arange(len(examples), dtype=np.int64)
    if any(np.isnan(global_scores[name]).any() for name in METHODS):
        raise ValueError("not every eligible row received one OOF score")

    metrics = method_metrics(examples, indexes, global_scores)
    strongest = max(COMPARATORS, key=lambda name: (metrics[name]["auc"], name))
    delta = bootstrap_delta(
        examples,
        indexes,
        global_scores["generator_balanced_consensus"],
        global_scores[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    slices = generator_slices(examples, indexes, global_scores, strongest, models)
    positive_slices = sum(record["delta"] > 0.0 for record in slices.values())
    candidate = metrics["generator_balanced_consensus"]
    gates_config = config["development_gates"]
    eligible_fraction = len(eligible_tasks) / all_task_count
    gates = {
        "candidate_auc": candidate["auc"] >= float(gates_config["candidate_auc_min"]),
        "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
        >= float(gates_config["candidate_tpr_at_5fpr_min"]),
        "auc_delta_vs_strongest": delta["point"] >= float(gates_config["candidate_auc_delta_min"]),
        "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] > 0.0,
        "strictly_beats_every_comparator": all(
            candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS
        ),
        "all_generator_slices_nonnegative": all(record["delta"] >= 0.0 for record in slices.values()),
        "minimum_positive_generator_slices": positive_slices
        >= int(gates_config["minimum_positive_generator_slices"]),
        "eligible_task_fraction": eligible_fraction
        >= float(gates_config["eligible_task_fraction_min"]),
    }

    full_bundles = {}
    for target_model in models:
        train = np.asarray(
            [index for index, item in enumerate(examples) if item["model"] != target_model],
            dtype=np.int64,
        )
        full_bundles[target_model] = fit_bundle(
            examples, baselines, train, target_model, config, base
        )
    model_bundle = {
        "schema_version": 1,
        "experiment_id": "v040",
        "models": models,
        "fold_bundles": fold_bundles,
        "full_bundles": full_bundles,
        "strongest_development_comparator": strongest,
        "development_task_ids": sorted(eligible_tasks),
        "excluded_development_task_ids": sorted(excluded_tasks),
        "method_names": METHODS,
    }
    summary = {
        "phase": "development",
        "evaluation": "three_fold_task_and_generator_oof",
        "source_tasks": all_task_count,
        "eligible_tasks": len(eligible_tasks),
        "eligible_task_fraction": eligible_fraction,
        "excluded_task_ids": excluded_tasks,
        "rows": len(examples),
        "support_count_min": int(np.min(support_counts)),
        "support_count_median": float(np.median(support_counts)),
        "support_count_max": int(np.max(support_counts)),
        "folds": fold_records,
        "metrics": metrics,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "generator_slices": slices,
        "positive_generator_slices": positive_slices,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
    }
    return model_bundle, global_scores, raw_predictions(
        examples, indexes, global_scores, support_counts, baselines, "development_oof"
    ), summary


def score_confirmation(
    examples: list[dict[str, Any]],
    eligible_tasks: list[str],
    excluded_tasks: list[str],
    all_task_count: int,
    config: dict[str, Any],
    model_bundle: dict[str, Any],
) -> tuple[dict[str, np.ndarray], list[dict[str, Any]], dict[str, Any]]:
    models = tuple(str(value) for value in config["generator_models"])
    if tuple(model_bundle["models"]) != models:
        raise ValueError("frozen generator model set mismatch")
    overlap = sorted(set(eligible_tasks) & set(model_bundle["development_task_ids"]))
    if overlap:
        raise ValueError("Development/Confirmation task overlap")
    baselines = baseline_indexes(examples)
    global_scores = {name: np.full(len(examples), np.nan, dtype=np.float64) for name in METHODS}
    support_counts = np.zeros(len(examples), dtype=np.int64)
    pair_records = []
    for target_model in models:
        indexes = np.asarray(
            [index for index, item in enumerate(examples) if item["model"] == target_model],
            dtype=np.int64,
        )
        scores, counts, pairs = score_bundle(
            model_bundle["full_bundles"][target_model], examples, baselines, indexes
        )
        for name in METHODS:
            global_scores[name][indexes] = scores[name]
        support_counts[indexes] = np.asarray(counts, dtype=np.int64)
        pair_records.append(
            {
                "target_model": target_model,
                "rows": len(indexes),
                "pairs": pairs,
                "support_count_min": min(counts),
                "support_count_max": max(counts),
            }
        )
    indexes = np.arange(len(examples), dtype=np.int64)
    if any(np.isnan(global_scores[name]).any() for name in METHODS):
        raise ValueError("not every Confirmation row received a score")
    metrics = method_metrics(examples, indexes, global_scores)
    strongest = str(model_bundle["strongest_development_comparator"])
    delta = bootstrap_delta(
        examples,
        indexes,
        global_scores["generator_balanced_consensus"],
        global_scores[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    slices = generator_slices(examples, indexes, global_scores, strongest, models)
    positive_slices = sum(record["delta"] > 0.0 for record in slices.values())
    candidate = metrics["generator_balanced_consensus"]
    gates_config = config["confirmation_gates"]
    eligible_fraction = len(eligible_tasks) / all_task_count
    gates = {
        "candidate_auc": candidate["auc"] >= float(gates_config["candidate_auc_min"]),
        "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
        >= float(gates_config["candidate_tpr_at_5fpr_min"]),
        "auc_delta_vs_frozen_strongest": delta["point"] > 0.0,
        "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] >= 0.0,
        "strictly_beats_every_comparator": all(
            candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS
        ),
        "all_generator_slices_nonnegative": all(record["delta"] >= 0.0 for record in slices.values()),
        "minimum_positive_generator_slices": positive_slices
        >= int(gates_config["minimum_positive_generator_slices"]),
        "eligible_task_fraction": eligible_fraction
        >= float(gates_config["eligible_task_fraction_min"]),
        "task_ids_disjoint": True,
    }
    summary = {
        "phase": "confirmation",
        "evaluation": "frozen_target_generator_bundles",
        "source_tasks": all_task_count,
        "eligible_tasks": len(eligible_tasks),
        "eligible_task_fraction": eligible_fraction,
        "excluded_task_ids": excluded_tasks,
        "rows": len(examples),
        "support_count_min": int(np.min(support_counts)),
        "support_count_median": float(np.median(support_counts)),
        "support_count_max": int(np.max(support_counts)),
        "pair_records": pair_records,
        "metrics": metrics,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "generator_slices": slices,
        "positive_generator_slices": positive_slices,
        "development_task_overlap": overlap,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
    }
    return global_scores, raw_predictions(
        examples, indexes, global_scores, support_counts, baselines, "confirmation"
    ), summary


def raw_predictions(
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
    scores: dict[str, np.ndarray],
    support_counts: np.ndarray,
    baselines: dict[str, list[int]],
    phase: str,
) -> list[dict[str, Any]]:
    result = []
    for index in indexes:
        item = examples[int(index)]
        supports = support_indexes(examples, baselines, int(index), item["model"])
        row = item["row"]
        result.append(
            {
                "phase": phase,
                "fold": item["fold"] if phase == "development_oof" else None,
                "row_id": item["row_id"],
                "task_id": item["task_id"],
                "model": item["model"],
                "target": item["target"],
                "source_dataset": row["source_dataset"],
                "observed_categories": row.get("observed_categories", []),
                "support_count": int(support_counts[int(index)]),
                "support_row_ids": [examples[support]["row_id"] for support in supports],
                "support_models": [examples[support]["model"] for support in supports],
                "scores": {name: float(scores[name][int(index)]) for name in METHODS},
            }
        )
    return result


def source_records(examples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "row_id": item["row_id"],
            "task_id": item["task_id"],
            "source_relative_path": str(item["row"]["source_relative_path"]),
            "source_sha256": str(item["row"]["source_sha256"]),
        }
        for item in examples
    ]


def environment_record(elapsed: float) -> dict[str, Any]:
    return {
        "python_executable": sys.executable,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
        "joblib": joblib.__version__,
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "training_device": "cpu",
        "elapsed_seconds": elapsed,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--evidence-packet", type=Path, required=True)
    parser.add_argument("--dataset", action="append", type=Path, required=True)
    parser.add_argument("--input-manifest", action="append", type=Path, required=True)
    parser.add_argument("--base-module", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    started = time.perf_counter()
    config = read_json(args.config)
    if sha256_path(args.candidate) != config["candidate_sha256"]:
        raise ValueError("Candidate SHA mismatch")
    if sha256_path(args.evidence_packet) != config["evidence_packet_sha256"]:
        raise ValueError("Evidence Packet SHA mismatch")
    if sha256_path(args.base_module) != config["base_module_sha256"]:
        raise ValueError("base module SHA mismatch")
    manifests = verify_inputs(
        config, args.config, args.dataset, args.input_manifest, args.phase
    )
    base = load_module(args.base_module)
    rows = []
    for dataset in args.dataset:
        rows.extend(base.load_jsonl(dataset))
    all_task_count = len({str(row["task_id"]) for row in rows})
    models = tuple(str(value) for value in config["generator_models"])
    examples, eligible_tasks, excluded_tasks = prepare_examples(
        rows, base, models, int(config["task_fold_modulus"])
    )
    args.output_dir.mkdir(parents=True, exist_ok=False)
    if args.phase == "development":
        model_bundle, scores, predictions, summary = fit_development(
            examples, eligible_tasks, excluded_tasks, all_task_count, config, base
        )
        model_path = args.output_dir / "model.joblib"
        joblib.dump(model_bundle, model_path)
    else:
        if args.model is None:
            raise ValueError("Confirmation requires a frozen model")
        model_bundle = joblib.load(args.model)
        scores, predictions, summary = score_confirmation(
            examples, eligible_tasks, excluded_tasks, all_task_count, config, model_bundle
        )
        model_path = args.model
    records = source_records(examples)
    write_jsonl(args.output_dir / "raw_predictions.jsonl", predictions)
    write_jsonl(args.output_dir / "source_records.jsonl", records)
    summary.update(
        {
            "schema_version": 1,
            "experiment_id": "v040",
            "config_sha256": sha256_path(args.config),
            "dataset_sha256s": [sha256_path(path) for path in args.dataset],
            "input_manifest_sha256s": [sha256_path(path) for path in args.input_manifest],
            "base_module_sha256": sha256_path(args.base_module),
            "source_rows": len(rows),
            "evaluated_rows": len(examples),
            "source_records_sha256": sha256_path(args.output_dir / "source_records.jsonl"),
            "raw_predictions_sha256": sha256_path(args.output_dir / "raw_predictions.jsonl"),
            "model": {
                "path": str(model_path),
                "bytes": model_path.stat().st_size,
                "sha256": sha256_path(model_path),
            },
            "input_buckets": [int(manifest["bucket"]) for manifest in manifests],
            "environment": environment_record(time.perf_counter() - started),
        }
    )
    write_json(args.output_dir / "summary.json", summary)
    print(
        json.dumps(
            {
                "phase": args.phase,
                "candidate_auc": summary["metrics"]["generator_balanced_consensus"]["auc"],
                "strongest_comparator": summary["strongest_comparator"],
                "auc_delta": summary["candidate_minus_strongest"]["point"],
                "gates": f"{summary['gates_passed']}/{summary['gates_total']}",
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
