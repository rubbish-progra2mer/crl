from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import scipy
import sklearn
import torch
from scipy import sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import Ridge
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler, normalize


METHODS = (
    "direct_action",
    "task_concat",
    "latent_additive",
    "identity_innovation",
    "all_row_innovation",
    "successful_innovation",
)
COMPARATORS = METHODS[:-1]
DENSE_METHODS = METHODS[2:]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


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
    spec = importlib.util.spec_from_file_location("v032_base_v012", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def task_description(prompt: str) -> str:
    start_marker = "Task Description:"
    end_marker = "Current terminal state:"
    start = prompt.find(start_marker)
    end = prompt.find(end_marker, start + len(start_marker))
    if start < 0 or end < 0:
        raise ValueError("task description markers missing")
    value = prompt[start + len(start_marker) : end].strip()
    if not value:
        raise ValueError("empty task description")
    return value


def fold_for_task(task_id: str, modulus: int) -> int:
    return hashlib.sha256(task_id.encode("utf-8")).digest()[1] % modulus


def verify_inputs(
    config: dict[str, Any],
    config_path: Path,
    datasets: list[Path],
    manifests: list[Path],
    phase: str,
) -> list[dict[str, Any]]:
    if len(datasets) != len(manifests):
        raise ValueError("dataset/manifest cardinality mismatch")
    if phase == "development":
        expected = {
            (
                item["dataset_sha256"],
                item["manifest_sha256"],
                int(item["bucket"]),
            ): item["acquisition_phase"]
            for item in config["development_inputs"]
        }
        if len(datasets) != len(expected):
            raise ValueError("Development input count mismatch")
    else:
        expected = None
        if len(datasets) != 1:
            raise ValueError("Confirmation requires one dataset")
    observed = set()
    values = []
    for dataset, manifest_path in zip(datasets, manifests, strict=True):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        dataset_sha = sha256_path(dataset)
        manifest_sha = sha256_path(manifest_path)
        bucket = int(manifest["bucket"])
        if manifest["dataset_sha256"] != dataset_sha:
            raise ValueError("manifest dataset SHA mismatch")
        if manifest["repository_commit"] != config["repository_commit"]:
            raise ValueError("repository commit mismatch")
        identity = (dataset_sha, manifest_sha, bucket)
        if expected is not None:
            if expected.get(identity) != manifest["phase"]:
                raise ValueError("Development input binding mismatch")
        else:
            if bucket != int(config["confirmation_bucket"]):
                raise ValueError("Confirmation bucket mismatch")
            if manifest["config_sha256"] != sha256_path(config_path):
                raise ValueError("Confirmation config SHA mismatch")
        observed.add(identity)
        values.append(manifest)
    if expected is not None and observed != set(expected):
        raise ValueError("Development input set mismatch")
    return values


def prepare_examples(
    rows: list[dict[str, Any]], base: Any, fold_modulus: int
) -> list[dict[str, Any]]:
    row_ids = [str(row["row_id"]) for row in rows]
    if len(set(row_ids)) != len(row_ids):
        raise ValueError("duplicate row IDs")
    examples = []
    for row in rows:
        target = int(row["target"])
        if target not in {0, 1}:
            raise ValueError("target must be binary")
        task_id = str(row["task_id"])
        examples.append(
            {
                "row_id": str(row["row_id"]),
                "task_id": task_id,
                "model": str(row["model"]),
                "source_dataset": str(row["source_dataset"]),
                "target": target,
                "fold": fold_for_task(task_id, fold_modulus),
                "task": task_description(str(row["task_prompt"])),
                "action": base.action_text(row),
            }
        )
    examples.sort(key=lambda item: (item["task_id"], item["model"], item["row_id"]))
    return examples


def equal_task_weights(examples: list[dict[str, Any]], indexes: np.ndarray) -> np.ndarray:
    counts = Counter(examples[int(index)]["task_id"] for index in indexes)
    return np.asarray(
        [1.0 / counts[examples[int(index)]["task_id"]] for index in indexes],
        dtype=np.float64,
    )


def latent_coordinates(
    vectorizer: Any,
    svd: TruncatedSVD,
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    task_matrix = vectorizer.transform(
        [examples[int(index)]["task"] for index in indexes]
    )
    action_matrix = vectorizer.transform(
        [examples[int(index)]["action"] for index in indexes]
    )
    task_latent = normalize(svd.transform(task_matrix), norm="l2")
    action_latent = normalize(svd.transform(action_matrix), norm="l2")
    return (
        np.asarray(task_latent, dtype=np.float64),
        np.asarray(action_latent, dtype=np.float64),
    )


def dense_features(
    task_latent: np.ndarray,
    action_latent: np.ndarray,
    all_map: Ridge,
    successful_map: Ridge,
) -> dict[str, np.ndarray]:
    all_prediction = np.asarray(all_map.predict(task_latent), dtype=np.float64)
    successful_prediction = np.asarray(
        successful_map.predict(task_latent), dtype=np.float64
    )
    return {
        "latent_additive": np.hstack([task_latent, action_latent]),
        "identity_innovation": np.abs(action_latent - task_latent),
        "all_row_innovation": np.abs(action_latent - all_prediction),
        "successful_innovation": np.abs(action_latent - successful_prediction),
    }


def fit_bundle(
    examples: list[dict[str, Any]],
    train: np.ndarray,
    base: Any,
    config: dict[str, Any],
) -> dict[str, Any]:
    y = np.asarray([examples[int(index)]["target"] for index in train], dtype=np.int64)
    base.ensure_two_classes(y, "train")

    direct_vectorizer = base.make_vectorizer(config)
    direct_matrix = direct_vectorizer.fit_transform(
        [examples[int(index)]["action"] for index in train]
    ).tocsr()
    direct_model = base.make_classifier(config)
    direct_model.fit(direct_matrix, y)

    concat_vectorizer = base.make_vectorizer(config)
    concat_matrix = concat_vectorizer.fit_transform(
        [
            "TASK\n"
            + examples[int(index)]["task"]
            + "\nACTION\n"
            + examples[int(index)]["action"]
            for index in train
        ]
    ).tocsr()
    concat_model = base.make_classifier(config)
    concat_model.fit(concat_matrix, y)

    latent_vectorizer = base.make_vectorizer(config)
    latent_matrix = latent_vectorizer.fit_transform(
        [examples[int(index)]["task"] for index in train]
        + [examples[int(index)]["action"] for index in train]
    )
    if latent_matrix.shape[1] <= int(config["latent_dimensions"]):
        raise ValueError("latent vocabulary too small")
    svd = TruncatedSVD(
        n_components=int(config["latent_dimensions"]),
        algorithm="randomized",
        n_iter=int(config["svd_iterations"]),
        random_state=int(config["seed"]),
    )
    svd.fit(latent_matrix)
    task_latent, action_latent = latent_coordinates(
        latent_vectorizer, svd, examples, train
    )

    all_map = Ridge(
        alpha=float(config["ridge_alpha"]),
        fit_intercept=True,
        solver="lsqr",
        max_iter=int(config["ridge_max_iter"]),
        tol=float(config["ridge_tolerance"]),
    )
    all_map.fit(
        task_latent,
        action_latent,
        sample_weight=equal_task_weights(examples, train),
    )

    successful_local = np.flatnonzero(y == 0)
    successful_indexes = train[successful_local]
    if len({examples[int(index)]["task_id"] for index in successful_indexes}) < 2:
        raise ValueError("insufficient successful tasks")
    successful_map = Ridge(
        alpha=float(config["ridge_alpha"]),
        fit_intercept=True,
        solver="lsqr",
        max_iter=int(config["ridge_max_iter"]),
        tol=float(config["ridge_tolerance"]),
    )
    successful_map.fit(
        task_latent[successful_local],
        action_latent[successful_local],
        sample_weight=equal_task_weights(examples, successful_indexes),
    )

    features = dense_features(task_latent, action_latent, all_map, successful_map)
    dense_models = {}
    for method in DENSE_METHODS:
        scaler = StandardScaler().fit(features[method])
        joined = sparse.hstack(
            [
                direct_matrix,
                sparse.csr_matrix(scaler.transform(features[method])),
            ],
            format="csr",
        )
        model = base.make_classifier(config)
        model.fit(joined, y)
        dense_models[method] = {"scaler": scaler, "model": model}

    return {
        "direct_vectorizer": direct_vectorizer,
        "direct_model": direct_model,
        "concat_vectorizer": concat_vectorizer,
        "concat_model": concat_model,
        "latent_vectorizer": latent_vectorizer,
        "svd": svd,
        "all_map": all_map,
        "successful_map": successful_map,
        "dense_models": dense_models,
        "training_rows": int(len(train)),
        "training_tasks": int(len({examples[int(index)]["task_id"] for index in train})),
        "successful_rows": int(len(successful_indexes)),
        "successful_tasks": int(
            len({examples[int(index)]["task_id"] for index in successful_indexes})
        ),
    }


def score_bundle(
    bundle: dict[str, Any],
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    direct_matrix = bundle["direct_vectorizer"].transform(
        [examples[int(index)]["action"] for index in indexes]
    ).tocsr()
    scores = {
        "direct_action": np.asarray(
            bundle["direct_model"].predict_proba(direct_matrix)[:, 1],
            dtype=np.float64,
        )
    }
    concat_matrix = bundle["concat_vectorizer"].transform(
        [
            "TASK\n"
            + examples[int(index)]["task"]
            + "\nACTION\n"
            + examples[int(index)]["action"]
            for index in indexes
        ]
    ).tocsr()
    scores["task_concat"] = np.asarray(
        bundle["concat_model"].predict_proba(concat_matrix)[:, 1],
        dtype=np.float64,
    )
    task_latent, action_latent = latent_coordinates(
        bundle["latent_vectorizer"], bundle["svd"], examples, indexes
    )
    features = dense_features(
        task_latent,
        action_latent,
        bundle["all_map"],
        bundle["successful_map"],
    )
    for method in DENSE_METHODS:
        dense = bundle["dense_models"][method]
        joined = sparse.hstack(
            [
                direct_matrix,
                sparse.csr_matrix(dense["scaler"].transform(features[method])),
            ],
            format="csr",
        )
        scores[method] = np.asarray(
            dense["model"].predict_proba(joined)[:, 1], dtype=np.float64
        )
    return scores, features


def tpr_at_fpr(y: np.ndarray, scores: np.ndarray, limit: float = 0.05) -> float:
    fpr, tpr, _ = roc_curve(y, scores)
    return float(np.max(tpr[fpr <= limit]))


def method_metrics(
    y: np.ndarray, scores: dict[str, np.ndarray]
) -> dict[str, dict[str, float]]:
    return {
        method: {
            "auc": float(roc_auc_score(y, scores[method])),
            "tpr_at_5pct_fpr": tpr_at_fpr(y, scores[method]),
            "rows": int(len(y)),
            "negatives": int(np.sum(y == 0)),
            "positives": int(np.sum(y == 1)),
        }
        for method in METHODS
    }


def cluster_bootstrap(
    examples: list[dict[str, Any]],
    candidate: np.ndarray,
    comparator: np.ndarray,
    repeats: int,
    seed: int,
) -> dict[str, Any]:
    tasks = sorted({item["task_id"] for item in examples})
    by_task = {
        task: np.asarray(
            [
                index
                for index, item in enumerate(examples)
                if item["task_id"] == task
            ],
            dtype=np.int64,
        )
        for task in tasks
    }
    y = np.asarray([item["target"] for item in examples], dtype=np.int64)
    point = float(roc_auc_score(y, candidate) - roc_auc_score(y, comparator))
    rng = np.random.default_rng(seed)
    values = []
    while len(values) < repeats:
        sampled = rng.choice(tasks, size=len(tasks), replace=True)
        indexes = np.concatenate([by_task[str(task)] for task in sampled])
        local_y = y[indexes]
        if len(np.unique(local_y)) != 2:
            continue
        values.append(
            float(
                roc_auc_score(local_y, candidate[indexes])
                - roc_auc_score(local_y, comparator[indexes])
            )
        )
    return {
        "point": point,
        "bootstrap_95": [
            float(np.quantile(values, 0.025)),
            float(np.quantile(values, 0.975)),
        ],
        "repeats": repeats,
        "resampling_unit": "task_id",
        "tasks": len(tasks),
    }


def slice_deltas(
    examples: list[dict[str, Any]],
    candidate: np.ndarray,
    comparator: np.ndarray,
    field: str,
) -> dict[str, dict[str, Any]]:
    y = np.asarray([item["target"] for item in examples], dtype=np.int64)
    result = {}
    for value in sorted({str(item[field]) for item in examples}):
        indexes = np.asarray(
            [
                index
                for index, item in enumerate(examples)
                if str(item[field]) == value
            ],
            dtype=np.int64,
        )
        local_y = y[indexes]
        if set(local_y.tolist()) != {0, 1}:
            raise ValueError(f"slice {field}={value} lacks both classes")
        candidate_auc = float(roc_auc_score(local_y, candidate[indexes]))
        comparator_auc = float(roc_auc_score(local_y, comparator[indexes]))
        result[value] = {
            "rows": int(len(indexes)),
            "negatives": int(np.sum(local_y == 0)),
            "positives": int(np.sum(local_y == 1)),
            "candidate_auc": candidate_auc,
            "strongest_auc": comparator_auc,
            "delta": candidate_auc - comparator_auc,
        }
    return result


def evaluate(
    phase: str,
    examples: list[dict[str, Any]],
    config: dict[str, Any],
    base: Any,
    frozen_model: dict[str, Any] | None,
) -> tuple[dict[str, Any] | None, dict[str, np.ndarray], dict[str, np.ndarray], dict[str, Any]]:
    models = tuple(config["generator_models"])
    dimensions = int(config["latent_dimensions"])
    if phase == "development":
        scores = {method: np.full(len(examples), np.nan) for method in METHODS}
        features = {
            "latent_additive": np.full((len(examples), dimensions * 2), np.nan),
            "identity_innovation": np.full((len(examples), dimensions), np.nan),
            "all_row_innovation": np.full((len(examples), dimensions), np.nan),
            "successful_innovation": np.full((len(examples), dimensions), np.nan),
        }
        folds = []
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
                bundle = fit_bundle(examples, train, base, config)
                local_scores, local_features = score_bundle(bundle, examples, heldout)
                for method in METHODS:
                    scores[method][heldout] = local_scores[method]
                for method in DENSE_METHODS:
                    features[method][heldout] = local_features[method]
                folds.append(
                    {
                        "target_model": target_model,
                        "fold": fold,
                        "train_rows": int(len(train)),
                        "heldout_rows": int(len(heldout)),
                        "train_tasks": bundle["training_tasks"],
                        "heldout_tasks": int(
                            len({examples[int(index)]["task_id"] for index in heldout})
                        ),
                        "successful_rows": bundle["successful_rows"],
                        "successful_tasks": bundle["successful_tasks"],
                        "latent_vocabulary": int(
                            len(bundle["latent_vectorizer"].vocabulary_)
                        ),
                    }
                )
        if any(np.isnan(scores[method]).any() for method in METHODS):
            raise ValueError("not every row received one OOF score")
        if any(np.isnan(features[method]).any() for method in DENSE_METHODS):
            raise ValueError("not every row received OOF dense features")
        full_bundles = {}
        for target_model in models:
            train = np.asarray(
                [
                    index
                    for index, item in enumerate(examples)
                    if item["model"] != target_model
                ],
                dtype=np.int64,
            )
            full_bundles[target_model] = fit_bundle(examples, train, base, config)
        model_bundle = {
            "schema_version": 1,
            "experiment_id": config["experiment_id"],
            "models": models,
            "methods": METHODS,
            "development_task_ids": sorted({item["task_id"] for item in examples}),
            "full_bundles": full_bundles,
        }
    else:
        if frozen_model is None:
            raise ValueError("Confirmation requires frozen model")
        if tuple(frozen_model["models"]) != models:
            raise ValueError("frozen model set mismatch")
        overlap = sorted(
            set(frozen_model["development_task_ids"])
            & {item["task_id"] for item in examples}
        )
        if overlap:
            raise ValueError("Development/Confirmation task overlap")
        scores = {method: np.full(len(examples), np.nan) for method in METHODS}
        features = {
            "latent_additive": np.full((len(examples), dimensions * 2), np.nan),
            "identity_innovation": np.full((len(examples), dimensions), np.nan),
            "all_row_innovation": np.full((len(examples), dimensions), np.nan),
            "successful_innovation": np.full((len(examples), dimensions), np.nan),
        }
        for target_model in models:
            indexes = np.asarray(
                [
                    index
                    for index, item in enumerate(examples)
                    if item["model"] == target_model
                ],
                dtype=np.int64,
            )
            local_scores, local_features = score_bundle(
                frozen_model["full_bundles"][target_model], examples, indexes
            )
            for method in METHODS:
                scores[method][indexes] = local_scores[method]
            for method in DENSE_METHODS:
                features[method][indexes] = local_features[method]
        if any(np.isnan(scores[method]).any() for method in METHODS):
            raise ValueError("not every Confirmation row received one score")
        if any(np.isnan(features[method]).any() for method in DENSE_METHODS):
            raise ValueError("not every Confirmation row received dense features")
        model_bundle = None
        folds = []

    y = np.asarray([item["target"] for item in examples], dtype=np.int64)
    metric_values = method_metrics(y, scores)
    strongest = (
        max(COMPARATORS, key=lambda method: (metric_values[method]["auc"], method))
        if phase == "development"
        else str(frozen_model["strongest_development_comparator"])
    )
    if phase == "development":
        model_bundle["strongest_development_comparator"] = strongest
    delta = cluster_bootstrap(
        examples,
        scores["successful_innovation"],
        scores[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    generator_slices = slice_deltas(
        examples,
        scores["successful_innovation"],
        scores[strongest],
        "model",
    )
    source_slices = slice_deltas(
        examples,
        scores["successful_innovation"],
        scores[strongest],
        "source_dataset",
    )
    positive_generators = sum(item["delta"] > 0 for item in generator_slices.values())
    nonnegative_sources = sum(item["delta"] >= 0 for item in source_slices.values())
    candidate = metric_values["successful_innovation"]
    gate_config = config[
        "development_gates" if phase == "development" else "confirmation_gates"
    ]
    gates = {
        "candidate_auc": candidate["auc"] >= gate_config["candidate_auc_min"],
        "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
        >= gate_config["candidate_tpr_at_5fpr_min"],
        "auc_delta": delta["point"]
        >= (
            gate_config["candidate_auc_delta_min"]
            if phase == "development"
            else 0.0
        ),
        "bootstrap_lower": delta["bootstrap_95"][0]
        > 0.0
        if phase == "development"
        else delta["bootstrap_95"][0] >= 0.0,
        "strictly_beats_every_comparator": all(
            candidate["auc"] > metric_values[method]["auc"] for method in COMPARATORS
        ),
        "all_generator_slices_nonnegative": all(
            item["delta"] >= 0 for item in generator_slices.values()
        ),
        "minimum_positive_generator_slices": positive_generators
        >= gate_config["minimum_positive_generator_slices"],
        "minimum_nonnegative_source_slices": nonnegative_sources
        >= gate_config["minimum_nonnegative_source_slices"],
    }
    summary = {
        "phase": phase,
        "rows": len(examples),
        "tasks": len({item["task_id"] for item in examples}),
        "models": sorted({item["model"] for item in examples}),
        "source_datasets": dict(Counter(item["source_dataset"] for item in examples)),
        "folds": folds,
        "metrics": metric_values,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "generator_slices": generator_slices,
        "source_slices": source_slices,
        "positive_generator_slices": positive_generators,
        "nonnegative_source_slices": nonnegative_sources,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
        "all_gates_passed": all(gates.values()),
    }
    return model_bundle, scores, features, summary


def environment_capture(started: float) -> dict[str, Any]:
    value = {
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
        "joblib": joblib.__version__,
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "elapsed_seconds": time.perf_counter() - started,
    }
    if torch.cuda.is_available():
        value.update(
            {
                "gpu": torch.cuda.get_device_name(0),
                "gpu_capability": list(torch.cuda.get_device_capability(0)),
            }
        )
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--evidence-packet", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, action="append", required=True)
    parser.add_argument("--input-manifest", type=Path, action="append", required=True)
    parser.add_argument("--base-module", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    args.output_dir.mkdir(parents=True, exist_ok=False)

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if sha256_path(args.candidate) != config["candidate_sha256"]:
        raise ValueError("Candidate SHA mismatch")
    if sha256_path(args.base_module) != config["base_module_sha256"]:
        raise ValueError("base module SHA mismatch")
    if not args.evidence_packet.is_file():
        raise ValueError("Evidence Packet missing")
    manifests = verify_inputs(
        config, args.config, args.dataset, args.input_manifest, args.phase
    )
    rows = [row for path in args.dataset for row in load_jsonl(path)]
    base = load_module(args.base_module)
    examples = prepare_examples(rows, base, int(config["task_fold_modulus"]))
    frozen_model = None
    if args.phase == "confirmation":
        if args.model is None:
            raise ValueError("Confirmation requires --model")
        frozen_model = joblib.load(args.model)
    elif args.model is not None:
        raise ValueError("Development does not accept --model")

    model_bundle, scores, features, summary = evaluate(
        args.phase, examples, config, base, frozen_model
    )
    environment = environment_capture(started)
    summary.update(
        {
            "experiment_id": config["experiment_id"],
            "candidate_sha256": sha256_path(args.candidate),
            "evidence_packet_sha256": sha256_path(args.evidence_packet),
            "config_sha256": sha256_path(args.config),
            "base_module_sha256": sha256_path(args.base_module),
            "dataset_sha256s": [sha256_path(path) for path in args.dataset],
            "manifest_sha256s": [
                sha256_path(path) for path in args.input_manifest
            ],
            "input_buckets": [int(item["bucket"]) for item in manifests],
            "environment": environment,
        }
    )
    raw_rows = [
        {
            "row_id": item["row_id"],
            "task_id": item["task_id"],
            "model": item["model"],
            "source_dataset": item["source_dataset"],
            "target": item["target"],
            "fold": item["fold"],
            "task_sha256": hashlib.sha256(item["task"].encode("utf-8")).hexdigest(),
            "action_sha256": hashlib.sha256(
                item["action"].encode("utf-8")
            ).hexdigest(),
            "scores": {
                method: float(scores[method][index]) for method in METHODS
            },
        }
        for index, item in enumerate(examples)
    ]
    feature_rows = [
        {
            "row_id": item["row_id"],
            "features": {
                method: [float(value) for value in features[method][index]]
                for method in DENSE_METHODS
            },
        }
        for index, item in enumerate(examples)
    ]
    write_jsonl(args.output_dir / "raw_predictions.jsonl", raw_rows)
    write_jsonl(args.output_dir / "feature_rows.jsonl", feature_rows)
    write_json(args.output_dir / "summary.json", summary)
    write_json(args.output_dir / "environment.json", environment)
    if model_bundle is not None:
        joblib.dump(model_bundle, args.output_dir / "model.joblib", compress=3)

    print(
        json.dumps(
            {
                "phase": args.phase,
                "candidate_auc": summary["metrics"]["successful_innovation"]["auc"],
                "strongest_comparator": summary["strongest_comparator"],
                "auc_delta": summary["candidate_minus_strongest"]["point"],
                "gates": f"{summary['gates_passed']}/{summary['gates_total']}",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
