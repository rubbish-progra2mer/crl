from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
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
from sentence_transformers import CrossEncoder
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler


METHODS = (
    "direct_action",
    "task_concat",
    "structural_counts",
    "global_relevance",
    "chronological_relevance",
    "role_gated_relevance",
)
COMPARATORS = METHODS[:-1]
ROLES = ("mutation", "verify", "read", "other")
MUTATION_EFFECTS = {"write", "delete", "permission", "package", "service", "network"}


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
    spec = importlib.util.spec_from_file_location("v031_base_v012", path)
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


def role_for(effect: str) -> str:
    if effect in MUTATION_EFFECTS:
        return "mutation"
    if effect == "verify":
        return "verify"
    if effect == "read":
        return "read"
    return "other"


def segment_records(row: dict[str, Any], base: Any) -> list[dict[str, Any]]:
    records = []
    for command in row["commands"]:
        for raw in base.SEGMENT_SPLIT.split(str(command)):
            segment = raw.strip()
            if not segment:
                continue
            executable = base.segment_executable(segment)
            effect = base.effect_for(executable, segment)
            records.append(
                {
                    "segment": segment,
                    "effect": effect,
                    "role": role_for(effect),
                }
            )
    if not records:
        raise ValueError(f"row has no command segments: {row['row_id']}")
    return records


def five_stats(values: list[float], total: int) -> list[float]:
    if not values:
        return [0.0, 0.0, 0.0, 0.0, 0.0]
    array = np.asarray(values, dtype=np.float64)
    return [
        len(values) / total,
        float(np.min(array)),
        float(np.mean(array)),
        float(np.max(array)),
        float(np.std(array)),
    ]


def dense_features(
    records: list[dict[str, Any]], scores: list[float]
) -> dict[str, list[float]]:
    total = len(records)
    global_values = list(scores)
    global_features = [
        float(total),
        float(np.min(global_values)),
        float(np.mean(global_values)),
        float(np.max(global_values)),
        float(np.std(global_values)),
    ]
    role_features = []
    for role in ROLES:
        role_features.extend(
            five_stats(
                [score for record, score in zip(records, scores) if record["role"] == role],
                total,
            )
        )
    chronological = []
    for group in range(4):
        values = [
            score
            for index, score in enumerate(scores)
            if min(3, (4 * index) // total) == group
        ]
        chronological.extend(five_stats(values, total))
    structural = [
        sum(record["role"] == role for record in records) / total for role in ROLES
    ]
    return {
        "structural_counts": structural,
        "global_relevance": global_features,
        "chronological_relevance": chronological,
        "role_gated_relevance": role_features,
    }


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
    seen = set()
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
        key = (dataset_sha, manifest_sha, bucket)
        if expected is not None:
            if expected.get(key) != manifest["phase"]:
                raise ValueError("Development input binding mismatch")
        else:
            if bucket != int(config["confirmation_bucket"]):
                raise ValueError("Confirmation bucket mismatch")
            if manifest["config_sha256"] != sha256_path(config_path):
                raise ValueError("Confirmation config SHA mismatch")
        seen.add(key)
        values.append(manifest)
    if expected is not None and seen != set(expected):
        raise ValueError("Development input set mismatch")
    return values


def verify_model(model_dir: Path, config: dict[str, Any]) -> None:
    observed = sorted(path.name for path in model_dir.iterdir() if path.is_file())
    expected = sorted(config["model_files"])
    if observed != expected:
        raise ValueError("model file set mismatch")
    for name, digest in config["model_files"].items():
        if sha256_path(model_dir / name) != digest:
            raise ValueError(f"model SHA mismatch: {name}")


def prepare_examples(
    rows: list[dict[str, Any]], base: Any, fold_modulus: int
) -> list[dict[str, Any]]:
    if len({row["row_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate row IDs")
    examples = []
    for row in rows:
        description = task_description(str(row["task_prompt"]))
        examples.append(
            {
                "row": row,
                "row_id": str(row["row_id"]),
                "task_id": str(row["task_id"]),
                "model": str(row["model"]),
                "source_dataset": str(row["source_dataset"]),
                "target": int(row["target"]),
                "fold": fold_for_task(str(row["task_id"]), fold_modulus),
                "description": description,
                "action": base.action_text(row),
                "segments": segment_records(row, base),
            }
        )
    examples.sort(key=lambda item: (item["task_id"], item["model"], item["row_id"]))
    return examples


def compute_relevance(
    examples: list[dict[str, Any]], model_dir: Path, config: dict[str, Any]
) -> tuple[dict[str, np.ndarray], list[dict[str, Any]]]:
    pairs = []
    identity = []
    for row_index, example in enumerate(examples):
        for segment_index, record in enumerate(example["segments"]):
            pairs.append((example["description"], record["segment"]))
            identity.append((row_index, segment_index))
    model = CrossEncoder(
        str(model_dir),
        max_length=512,
        device=str(config["cross_encoder_device"]),
    )
    values = np.asarray(
        model.predict(
            pairs,
            batch_size=int(config["cross_encoder_batch_size"]),
            show_progress_bar=False,
        ),
        dtype=np.float64,
    ).reshape(-1)
    if len(values) != len(identity):
        raise ValueError("cross-encoder output count mismatch")
    grouped: list[list[float]] = [[] for _ in examples]
    pair_rows = []
    for (row_index, segment_index), score in zip(identity, values, strict=True):
        example = examples[row_index]
        record = example["segments"][segment_index]
        grouped[row_index].append(float(score))
        pair_rows.append(
            {
                "row_id": example["row_id"],
                "segment_index": segment_index,
                "role": record["role"],
                "effect": record["effect"],
                "task_sha256": hashlib.sha256(
                    example["description"].encode("utf-8")
                ).hexdigest(),
                "command_sha256": hashlib.sha256(
                    record["segment"].encode("utf-8")
                ).hexdigest(),
                "score": float(score),
            }
        )
    feature_arrays: dict[str, list[list[float]]] = {
        name: [] for name in METHODS if name not in {"direct_action", "task_concat"}
    }
    for example, scores in zip(examples, grouped, strict=True):
        if len(scores) != len(example["segments"]):
            raise ValueError("segment score cardinality mismatch")
        features = dense_features(example["segments"], scores)
        for name in feature_arrays:
            feature_arrays[name].append(features[name])
    return (
        {name: np.asarray(values, dtype=np.float64) for name, values in feature_arrays.items()},
        pair_rows,
    )


def fit_bundle(
    examples: list[dict[str, Any]],
    features: dict[str, np.ndarray],
    train: np.ndarray,
    base: Any,
    config: dict[str, Any],
) -> dict[str, Any]:
    y = np.asarray([examples[int(i)]["target"] for i in train], dtype=np.int64)
    base.ensure_two_classes(y, "train")
    action_vectorizer = base.make_vectorizer(config)
    action_matrix = action_vectorizer.fit_transform(
        [examples[int(i)]["action"] for i in train]
    ).tocsr()
    direct_model = base.make_classifier(config)
    direct_model.fit(action_matrix, y)
    task_vectorizer = base.make_vectorizer(config)
    task_matrix = task_vectorizer.fit_transform(
        [
            "TASK\n" + examples[int(i)]["description"] + "\nACTION\n" + examples[int(i)]["action"]
            for i in train
        ]
    ).tocsr()
    task_model = base.make_classifier(config)
    task_model.fit(task_matrix, y)
    dense_models = {}
    for method in METHODS[2:]:
        scaler = StandardScaler().fit(features[method][train])
        joined = sparse.hstack(
            [action_matrix, sparse.csr_matrix(scaler.transform(features[method][train]))],
            format="csr",
        )
        model = base.make_classifier(config)
        model.fit(joined, y)
        dense_models[method] = {"scaler": scaler, "model": model}
    return {
        "action_vectorizer": action_vectorizer,
        "direct_model": direct_model,
        "task_vectorizer": task_vectorizer,
        "task_model": task_model,
        "dense_models": dense_models,
    }


def score_bundle(
    bundle: dict[str, Any],
    examples: list[dict[str, Any]],
    features: dict[str, np.ndarray],
    indexes: np.ndarray,
) -> dict[str, np.ndarray]:
    action_matrix = bundle["action_vectorizer"].transform(
        [examples[int(i)]["action"] for i in indexes]
    ).tocsr()
    scores = {
        "direct_action": bundle["direct_model"].predict_proba(action_matrix)[:, 1]
    }
    task_matrix = bundle["task_vectorizer"].transform(
        [
            "TASK\n" + examples[int(i)]["description"] + "\nACTION\n" + examples[int(i)]["action"]
            for i in indexes
        ]
    ).tocsr()
    scores["task_concat"] = bundle["task_model"].predict_proba(task_matrix)[:, 1]
    for method in METHODS[2:]:
        item = bundle["dense_models"][method]
        joined = sparse.hstack(
            [
                action_matrix,
                sparse.csr_matrix(item["scaler"].transform(features[method][indexes])),
            ],
            format="csr",
        )
        scores[method] = item["model"].predict_proba(joined)[:, 1]
    return {name: np.asarray(value, dtype=np.float64) for name, value in scores.items()}


def tpr_at_fpr(y: np.ndarray, score: np.ndarray) -> float:
    fpr, tpr, _ = roc_curve(y, score)
    valid = np.flatnonzero(fpr <= 0.05)
    return float(np.max(tpr[valid]))


def metrics(y: np.ndarray, scores: dict[str, np.ndarray]) -> dict[str, dict[str, float]]:
    return {
        method: {
            "auc": float(roc_auc_score(y, scores[method])),
            "tpr_at_5pct_fpr": tpr_at_fpr(y, scores[method]),
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
    indexes = {
        task: np.asarray(
            [index for index, item in enumerate(examples) if item["task_id"] == task],
            dtype=np.int64,
        )
        for task in tasks
    }
    y = np.asarray([item["target"] for item in examples], dtype=np.int64)
    point = float(roc_auc_score(y, candidate) - roc_auc_score(y, comparator))
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(repeats):
        sampled = rng.choice(tasks, size=len(tasks), replace=True)
        chosen = np.concatenate([indexes[str(task)] for task in sampled])
        values.append(
            float(
                roc_auc_score(y[chosen], candidate[chosen])
                - roc_auc_score(y[chosen], comparator[chosen])
            )
        )
    return {
        "point": point,
        "bootstrap_95": [
            float(np.quantile(values, 0.025)),
            float(np.quantile(values, 0.975)),
        ],
    }


def slice_deltas(
    examples: list[dict[str, Any]],
    candidate: np.ndarray,
    comparator: np.ndarray,
    field: str,
) -> dict[str, dict[str, float]]:
    y = np.asarray([item["target"] for item in examples], dtype=np.int64)
    result = {}
    for value in sorted({item[field] for item in examples}):
        indexes = np.asarray(
            [i for i, item in enumerate(examples) if item[field] == value],
            dtype=np.int64,
        )
        candidate_auc = float(roc_auc_score(y[indexes], candidate[indexes]))
        comparator_auc = float(roc_auc_score(y[indexes], comparator[indexes]))
        result[value] = {
            "rows": len(indexes),
            "candidate_auc": candidate_auc,
            "comparator_auc": comparator_auc,
            "delta": candidate_auc - comparator_auc,
        }
    return result


def prediction_rows(
    phase: str,
    examples: list[dict[str, Any]],
    scores: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    return [
        {
            "phase": phase,
            "row_id": item["row_id"],
            "task_id": item["task_id"],
            "model": item["model"],
            "source_dataset": item["source_dataset"],
            "target": item["target"],
            "fold": item["fold"],
            "scores": {method: float(scores[method][index]) for method in METHODS},
        }
        for index, item in enumerate(examples)
    ]


def feature_rows(
    examples: list[dict[str, Any]], features: dict[str, np.ndarray]
) -> list[dict[str, Any]]:
    return [
        {
            "row_id": item["row_id"],
            "task_id": item["task_id"],
            "model": item["model"],
            "segment_count": len(item["segments"]),
            "features": {
                method: [float(value) for value in features[method][index]]
                for method in features
            },
        }
        for index, item in enumerate(examples)
    ]


def evaluate(
    phase: str,
    examples: list[dict[str, Any]],
    features: dict[str, np.ndarray],
    config: dict[str, Any],
    base: Any,
    frozen_model: dict[str, Any] | None,
) -> tuple[dict[str, Any] | None, dict[str, np.ndarray], dict[str, Any]]:
    models = tuple(config["generator_models"])
    y = np.asarray([item["target"] for item in examples], dtype=np.int64)
    if phase == "development":
        scores = {method: np.full(len(examples), np.nan) for method in METHODS}
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
                bundle = fit_bundle(examples, features, train, base, config)
                local = score_bundle(bundle, examples, features, heldout)
                for method in METHODS:
                    scores[method][heldout] = local[method]
                folds.append(
                    {
                        "target_model": target_model,
                        "fold": fold,
                        "train_rows": len(train),
                        "heldout_rows": len(heldout),
                        "train_tasks": len({examples[int(i)]["task_id"] for i in train}),
                        "heldout_tasks": len(
                            {examples[int(i)]["task_id"] for i in heldout}
                        ),
                    }
                )
        if any(np.isnan(scores[method]).any() for method in METHODS):
            raise ValueError("not every row received one OOF score")
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
            full_bundles[target_model] = fit_bundle(
                examples, features, train, base, config
            )
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
        for target_model in models:
            indexes = np.asarray(
                [
                    index
                    for index, item in enumerate(examples)
                    if item["model"] == target_model
                ],
                dtype=np.int64,
            )
            local = score_bundle(
                frozen_model["full_bundles"][target_model],
                examples,
                features,
                indexes,
            )
            for method in METHODS:
                scores[method][indexes] = local[method]
        if any(np.isnan(scores[method]).any() for method in METHODS):
            raise ValueError("not every Confirmation row received one score")
        model_bundle = None
        folds = []

    metric_values = metrics(y, scores)
    strongest = (
        max(COMPARATORS, key=lambda method: (metric_values[method]["auc"], method))
        if phase == "development"
        else str(frozen_model["strongest_development_comparator"])
    )
    if phase == "development":
        model_bundle["strongest_development_comparator"] = strongest
    delta = cluster_bootstrap(
        examples,
        scores["role_gated_relevance"],
        scores[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    generator_slices = slice_deltas(
        examples,
        scores["role_gated_relevance"],
        scores[strongest],
        "model",
    )
    source_slices = slice_deltas(
        examples,
        scores["role_gated_relevance"],
        scores[strongest],
        "source_dataset",
    )
    positive_generators = sum(item["delta"] > 0 for item in generator_slices.values())
    nonnegative_sources = sum(item["delta"] >= 0 for item in source_slices.values())
    candidate = metric_values["role_gated_relevance"]
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
    return model_bundle, scores, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--dataset", action="append", required=True, type=Path)
    parser.add_argument("--input-manifest", action="append", required=True, type=Path)
    parser.add_argument("--base-module", required=True, type=Path)
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--frozen-model", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    verify_inputs(
        config,
        args.config,
        args.dataset,
        args.input_manifest,
        args.phase,
    )
    if sha256_path(args.base_module) != config["base_module_sha256"]:
        raise ValueError("base module SHA mismatch")
    verify_model(args.model_dir, config)
    base = load_module(args.base_module)
    rows = []
    for path in args.dataset:
        rows.extend(load_jsonl(path))
    examples = prepare_examples(rows, base, int(config["task_fold_modulus"]))
    features, pair_rows = compute_relevance(examples, args.model_dir, config)
    frozen = joblib.load(args.frozen_model) if args.frozen_model else None
    model_bundle, scores, summary = evaluate(
        args.phase, examples, features, config, base, frozen
    )
    args.output_dir.mkdir()
    write_jsonl(args.output_dir / "pair_scores.jsonl", pair_rows)
    write_jsonl(args.output_dir / "feature_rows.jsonl", feature_rows(examples, features))
    write_jsonl(
        args.output_dir / "raw_predictions.jsonl",
        prediction_rows(args.phase, examples, scores),
    )
    summary["pair_scores_sha256"] = sha256_path(
        args.output_dir / "pair_scores.jsonl"
    )
    summary["feature_rows_sha256"] = sha256_path(
        args.output_dir / "feature_rows.jsonl"
    )
    summary["raw_predictions_sha256"] = sha256_path(
        args.output_dir / "raw_predictions.jsonl"
    )
    summary["config_sha256"] = sha256_path(args.config)
    summary["base_module_sha256"] = sha256_path(args.base_module)
    summary["elapsed_seconds"] = time.perf_counter() - started
    write_json(args.output_dir / "summary.json", summary)
    if args.phase == "development":
        joblib.dump(model_bundle, args.output_dir / "model.joblib")
    write_json(
        args.output_dir / "environment.json",
        {
            "python": platform.python_version(),
            "python_executable": sys.executable,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sklearn": sklearn.__version__,
            "torch": torch.__version__,
            "torch_cuda": torch.version.cuda,
            "cuda_available": torch.cuda.is_available(),
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "capability": (
                ".".join(map(str, torch.cuda.get_device_capability(0)))
                if torch.cuda.is_available()
                else None
            ),
        },
    )
    print(
        json.dumps(
            {
                "phase": args.phase,
                "candidate_auc": summary["metrics"]["role_gated_relevance"]["auc"],
                "strongest_comparator": summary["strongest_comparator"],
                "gates": f"{summary['gates_passed']}/{summary['gates_total']}",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
