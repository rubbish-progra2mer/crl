from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any

import joblib
import numpy as np
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


def load_base(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("v031_audit_base_v012", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_description(prompt: str) -> str:
    left = "Task Description:"
    right = "Current terminal state:"
    start = prompt.find(left)
    end = prompt.find(right, start + len(left))
    if start < 0 or end < 0:
        raise ValueError("task description markers missing")
    value = prompt[start + len(left) : end].strip()
    if not value:
        raise ValueError("empty task description")
    return value


def task_fold(task_id: str, modulus: int) -> int:
    return hashlib.sha256(task_id.encode("utf-8")).digest()[1] % modulus


def operation_role(effect: str) -> str:
    if effect in MUTATION_EFFECTS:
        return "mutation"
    if effect == "verify":
        return "verify"
    if effect == "read":
        return "read"
    return "other"


def command_records(row: dict[str, Any], base: Any) -> list[dict[str, str]]:
    result = []
    for command in row["commands"]:
        for value in base.SEGMENT_SPLIT.split(str(command)):
            segment = value.strip()
            if not segment:
                continue
            executable = base.segment_executable(segment)
            effect = base.effect_for(executable, segment)
            result.append(
                {
                    "segment": segment,
                    "effect": effect,
                    "role": operation_role(effect),
                }
            )
    if not result:
        raise ValueError(f"row has no command segments: {row['row_id']}")
    return result


def prepare_rows(
    rows: list[dict[str, Any]], base: Any, fold_modulus: int
) -> list[dict[str, Any]]:
    if len(rows) != len({str(row["row_id"]) for row in rows}):
        raise ValueError("duplicate row IDs")
    result = []
    for row in rows:
        result.append(
            {
                "row_id": str(row["row_id"]),
                "task_id": str(row["task_id"]),
                "model": str(row["model"]),
                "source_dataset": str(row["source_dataset"]),
                "target": int(row["target"]),
                "fold": task_fold(str(row["task_id"]), fold_modulus),
                "description": extract_description(str(row["task_prompt"])),
                "action": base.action_text(row),
                "segments": command_records(row, base),
            }
        )
    result.sort(key=lambda item: (item["task_id"], item["model"], item["row_id"]))
    return result


def pooled(values: list[float], total: int) -> list[float]:
    if not values:
        return [0.0] * 5
    array = np.asarray(values, dtype=np.float64)
    return [
        len(values) / total,
        float(array.min()),
        float(array.mean()),
        float(array.max()),
        float(array.std()),
    ]


def make_dense(
    records: list[dict[str, str]], scores: list[float]
) -> dict[str, list[float]]:
    total = len(records)
    values = np.asarray(scores, dtype=np.float64)
    global_values = [
        float(total),
        float(values.min()),
        float(values.mean()),
        float(values.max()),
        float(values.std()),
    ]
    role_values: list[float] = []
    for role in ROLES:
        role_values.extend(
            pooled(
                [
                    score
                    for record, score in zip(records, scores, strict=True)
                    if record["role"] == role
                ],
                total,
            )
        )
    chronological: list[float] = []
    for group in range(4):
        chronological.extend(
            pooled(
                [
                    score
                    for index, score in enumerate(scores)
                    if min(3, (4 * index) // total) == group
                ],
                total,
            )
        )
    structural = [
        sum(record["role"] == role for record in records) / total for role in ROLES
    ]
    return {
        "structural_counts": structural,
        "global_relevance": global_values,
        "chronological_relevance": chronological,
        "role_gated_relevance": role_values,
    }


def recompute_relevance(
    examples: list[dict[str, Any]], model_dir: Path, config: dict[str, Any]
) -> tuple[dict[str, np.ndarray], list[dict[str, Any]]]:
    pairs: list[tuple[str, str]] = []
    identities: list[tuple[int, int]] = []
    for row_index, example in enumerate(examples):
        for segment_index, record in enumerate(example["segments"]):
            pairs.append((example["description"], record["segment"]))
            identities.append((row_index, segment_index))
    encoder = CrossEncoder(
        str(model_dir),
        max_length=512,
        device=str(config["cross_encoder_device"]),
    )
    scores = np.asarray(
        encoder.predict(
            pairs,
            batch_size=int(config["cross_encoder_batch_size"]),
            show_progress_bar=False,
        ),
        dtype=np.float64,
    ).reshape(-1)
    if len(scores) != len(identities):
        raise ValueError("cross-encoder output count mismatch")
    grouped: list[list[float]] = [[] for _ in examples]
    pair_rows = []
    for (row_index, segment_index), score in zip(identities, scores, strict=True):
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
    feature_lists: dict[str, list[list[float]]] = {
        name: [] for name in METHODS[2:]
    }
    for example, row_scores in zip(examples, grouped, strict=True):
        values = make_dense(example["segments"], row_scores)
        for method in feature_lists:
            feature_lists[method].append(values[method])
    return (
        {
            method: np.asarray(values, dtype=np.float64)
            for method, values in feature_lists.items()
        },
        pair_rows,
    )


def train_bundle(
    examples: list[dict[str, Any]],
    features: dict[str, np.ndarray],
    indexes: np.ndarray,
    base: Any,
    config: dict[str, Any],
) -> dict[str, Any]:
    targets = np.asarray(
        [examples[int(index)]["target"] for index in indexes], dtype=np.int64
    )
    base.ensure_two_classes(targets, "audit train")
    actions = [examples[int(index)]["action"] for index in indexes]
    action_vectorizer = base.make_vectorizer(config)
    action_matrix = action_vectorizer.fit_transform(actions).tocsr()
    direct_model = base.make_classifier(config)
    direct_model.fit(action_matrix, targets)
    task_vectorizer = base.make_vectorizer(config)
    task_matrix = task_vectorizer.fit_transform(
        [
            "TASK\n"
            + examples[int(index)]["description"]
            + "\nACTION\n"
            + examples[int(index)]["action"]
            for index in indexes
        ]
    ).tocsr()
    task_model = base.make_classifier(config)
    task_model.fit(task_matrix, targets)
    dense_models = {}
    for method in METHODS[2:]:
        scaler = StandardScaler().fit(features[method][indexes])
        matrix = sparse.hstack(
            [
                action_matrix,
                sparse.csr_matrix(scaler.transform(features[method][indexes])),
            ],
            format="csr",
        )
        classifier = base.make_classifier(config)
        classifier.fit(matrix, targets)
        dense_models[method] = {"scaler": scaler, "model": classifier}
    return {
        "action_vectorizer": action_vectorizer,
        "direct_model": direct_model,
        "task_vectorizer": task_vectorizer,
        "task_model": task_model,
        "dense_models": dense_models,
    }


def apply_bundle(
    bundle: dict[str, Any],
    examples: list[dict[str, Any]],
    features: dict[str, np.ndarray],
    indexes: np.ndarray,
) -> dict[str, np.ndarray]:
    action_matrix = bundle["action_vectorizer"].transform(
        [examples[int(index)]["action"] for index in indexes]
    ).tocsr()
    result = {
        "direct_action": np.asarray(
            bundle["direct_model"].predict_proba(action_matrix)[:, 1],
            dtype=np.float64,
        )
    }
    task_matrix = bundle["task_vectorizer"].transform(
        [
            "TASK\n"
            + examples[int(index)]["description"]
            + "\nACTION\n"
            + examples[int(index)]["action"]
            for index in indexes
        ]
    ).tocsr()
    result["task_concat"] = np.asarray(
        bundle["task_model"].predict_proba(task_matrix)[:, 1], dtype=np.float64
    )
    for method in METHODS[2:]:
        item = bundle["dense_models"][method]
        matrix = sparse.hstack(
            [
                action_matrix,
                sparse.csr_matrix(
                    item["scaler"].transform(features[method][indexes])
                ),
            ],
            format="csr",
        )
        result[method] = np.asarray(
            item["model"].predict_proba(matrix)[:, 1], dtype=np.float64
        )
    return result


def recompute_predictions(
    phase: str,
    examples: list[dict[str, Any]],
    features: dict[str, np.ndarray],
    base: Any,
    config: dict[str, Any],
    frozen_model: dict[str, Any] | None,
) -> tuple[dict[str, np.ndarray], list[dict[str, Any]]]:
    models = tuple(config["generator_models"])
    scores = {
        method: np.full(len(examples), np.nan, dtype=np.float64)
        for method in METHODS
    }
    folds = []
    if phase == "development":
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
                bundle = train_bundle(examples, features, train, base, config)
                local = apply_bundle(bundle, examples, features, heldout)
                for method in METHODS:
                    scores[method][heldout] = local[method]
                folds.append(
                    {
                        "target_model": target_model,
                        "fold": fold,
                        "train_rows": len(train),
                        "heldout_rows": len(heldout),
                        "train_tasks": len(
                            {examples[int(i)]["task_id"] for i in train}
                        ),
                        "heldout_tasks": len(
                            {examples[int(i)]["task_id"] for i in heldout}
                        ),
                    }
                )
    else:
        if frozen_model is None:
            raise ValueError("Confirmation audit requires frozen model")
        if tuple(frozen_model["models"]) != models:
            raise ValueError("frozen model set mismatch")
        overlap = set(frozen_model["development_task_ids"]) & {
            item["task_id"] for item in examples
        }
        if overlap:
            raise ValueError("Development/Confirmation task overlap")
        for target_model in models:
            indexes = np.asarray(
                [
                    index
                    for index, item in enumerate(examples)
                    if item["model"] == target_model
                ],
                dtype=np.int64,
            )
            local = apply_bundle(
                frozen_model["full_bundles"][target_model],
                examples,
                features,
                indexes,
            )
            for method in METHODS:
                scores[method][indexes] = local[method]
    if any(np.isnan(scores[method]).any() for method in METHODS):
        raise ValueError("audit did not score every row")
    return scores, folds


def tpr_five(y: np.ndarray, scores: np.ndarray) -> float:
    fpr, tpr, _ = roc_curve(y, scores)
    return float(tpr[np.flatnonzero(fpr <= 0.05)].max())


def calculate_metrics(
    y: np.ndarray, scores: dict[str, np.ndarray]
) -> dict[str, dict[str, float]]:
    return {
        method: {
            "auc": float(roc_auc_score(y, scores[method])),
            "tpr_at_5pct_fpr": tpr_five(y, scores[method]),
        }
        for method in METHODS
    }


def task_bootstrap(
    examples: list[dict[str, Any]],
    candidate: np.ndarray,
    comparator: np.ndarray,
    repeats: int,
    seed: int,
) -> dict[str, Any]:
    tasks = sorted({item["task_id"] for item in examples})
    task_indexes = {
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
    targets = np.asarray([item["target"] for item in examples], dtype=np.int64)
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(repeats):
        sampled = rng.choice(tasks, size=len(tasks), replace=True)
        indexes = np.concatenate([task_indexes[str(task)] for task in sampled])
        values.append(
            float(
                roc_auc_score(targets[indexes], candidate[indexes])
                - roc_auc_score(targets[indexes], comparator[indexes])
            )
        )
    return {
        "point": float(
            roc_auc_score(targets, candidate)
            - roc_auc_score(targets, comparator)
        ),
        "bootstrap_95": [
            float(np.quantile(values, 0.025)),
            float(np.quantile(values, 0.975)),
        ],
    }


def grouped_deltas(
    examples: list[dict[str, Any]],
    candidate: np.ndarray,
    comparator: np.ndarray,
    field: str,
) -> dict[str, dict[str, float]]:
    targets = np.asarray([item["target"] for item in examples], dtype=np.int64)
    result = {}
    for value in sorted({item[field] for item in examples}):
        indexes = np.asarray(
            [
                index
                for index, item in enumerate(examples)
                if item[field] == value
            ],
            dtype=np.int64,
        )
        left = float(roc_auc_score(targets[indexes], candidate[indexes]))
        right = float(roc_auc_score(targets[indexes], comparator[indexes]))
        result[value] = {
            "rows": len(indexes),
            "candidate_auc": left,
            "comparator_auc": right,
            "delta": left - right,
        }
    return result


def independent_summary(
    phase: str,
    examples: list[dict[str, Any]],
    scores: dict[str, np.ndarray],
    folds: list[dict[str, Any]],
    config: dict[str, Any],
    frozen_model: dict[str, Any] | None,
) -> dict[str, Any]:
    targets = np.asarray([item["target"] for item in examples], dtype=np.int64)
    metric_values = calculate_metrics(targets, scores)
    strongest = (
        max(COMPARATORS, key=lambda method: (metric_values[method]["auc"], method))
        if phase == "development"
        else str(frozen_model["strongest_development_comparator"])
    )
    delta = task_bootstrap(
        examples,
        scores["role_gated_relevance"],
        scores[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    generator_slices = grouped_deltas(
        examples,
        scores["role_gated_relevance"],
        scores[strongest],
        "model",
    )
    source_slices = grouped_deltas(
        examples,
        scores["role_gated_relevance"],
        scores[strongest],
        "source_dataset",
    )
    positive_generators = sum(item["delta"] > 0 for item in generator_slices.values())
    nonnegative_sources = sum(item["delta"] >= 0 for item in source_slices.values())
    candidate = metric_values["role_gated_relevance"]
    gates_config = config[
        "development_gates" if phase == "development" else "confirmation_gates"
    ]
    gates = {
        "candidate_auc": candidate["auc"] >= gates_config["candidate_auc_min"],
        "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
        >= gates_config["candidate_tpr_at_5fpr_min"],
        "auc_delta": delta["point"]
        >= (
            gates_config["candidate_auc_delta_min"]
            if phase == "development"
            else 0.0
        ),
        "bootstrap_lower": (
            delta["bootstrap_95"][0] > 0.0
            if phase == "development"
            else delta["bootstrap_95"][0] >= 0.0
        ),
        "strictly_beats_every_comparator": all(
            candidate["auc"] > metric_values[method]["auc"]
            for method in COMPARATORS
        ),
        "all_generator_slices_nonnegative": all(
            item["delta"] >= 0 for item in generator_slices.values()
        ),
        "minimum_positive_generator_slices": positive_generators
        >= gates_config["minimum_positive_generator_slices"],
        "minimum_nonnegative_source_slices": nonnegative_sources
        >= gates_config["minimum_nonnegative_source_slices"],
    }
    return {
        "phase": phase,
        "rows": len(examples),
        "tasks": len({item["task_id"] for item in examples}),
        "models": sorted({item["model"] for item in examples}),
        "source_datasets": dict(
            Counter(item["source_dataset"] for item in examples)
        ),
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


def verify_inputs(
    config: dict[str, Any],
    config_path: Path,
    datasets: list[Path],
    manifests: list[Path],
    phase: str,
) -> None:
    if len(datasets) != len(manifests):
        raise ValueError("dataset/manifest cardinality mismatch")
    expected = {
        (
            item["dataset_sha256"],
            item["manifest_sha256"],
            int(item["bucket"]),
        ): item["acquisition_phase"]
        for item in config["development_inputs"]
    }
    if phase == "development" and len(datasets) != len(expected):
        raise ValueError("Development input count mismatch")
    if phase == "confirmation" and len(datasets) != 1:
        raise ValueError("Confirmation requires one dataset")
    observed = set()
    for dataset, manifest_path in zip(datasets, manifests, strict=True):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        dataset_sha = sha256_path(dataset)
        manifest_sha = sha256_path(manifest_path)
        if manifest["dataset_sha256"] != dataset_sha:
            raise ValueError("manifest dataset SHA mismatch")
        if manifest["repository_commit"] != config["repository_commit"]:
            raise ValueError("repository commit mismatch")
        key = (dataset_sha, manifest_sha, int(manifest["bucket"]))
        if phase == "development":
            if expected.get(key) != manifest["phase"]:
                raise ValueError("Development input binding mismatch")
            observed.add(key)
        else:
            if int(manifest["bucket"]) != int(config["confirmation_bucket"]):
                raise ValueError("Confirmation bucket mismatch")
            if manifest["config_sha256"] != sha256_path(config_path):
                raise ValueError("Confirmation config SHA mismatch")
    if phase == "development" and observed != set(expected):
        raise ValueError("Development input set mismatch")


def maximum_error(left: Any, right: Any) -> float:
    if isinstance(left, bool) or isinstance(right, bool):
        if left != right:
            raise ValueError(f"boolean mismatch: {left!r} != {right!r}")
        return 0.0
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(float(left) - float(right))
    if isinstance(left, dict) and isinstance(right, dict):
        if set(left) != set(right):
            raise ValueError("mapping key mismatch")
        return max(
            (maximum_error(left[key], right[key]) for key in left),
            default=0.0,
        )
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            raise ValueError("list length mismatch")
        return max(
            (maximum_error(a, b) for a, b in zip(left, right, strict=True)),
            default=0.0,
        )
    if left != right:
        raise ValueError(f"value mismatch: {left!r} != {right!r}")
    return 0.0


def verify_pair_rows(
    observed: list[dict[str, Any]], expected: list[dict[str, Any]]
) -> float:
    if len(observed) != len(expected):
        raise ValueError("pair-score row count mismatch")
    maximum = 0.0
    for left, right in zip(observed, expected, strict=True):
        for key in (
            "row_id",
            "segment_index",
            "role",
            "effect",
            "task_sha256",
            "command_sha256",
        ):
            if left[key] != right[key]:
                raise ValueError(f"pair-score identity mismatch: {key}")
        maximum = max(maximum, abs(float(left["score"]) - float(right["score"])))
    return maximum


def verify_feature_rows(
    observed: list[dict[str, Any]],
    examples: list[dict[str, Any]],
    expected: dict[str, np.ndarray],
) -> float:
    if len(observed) != len(examples):
        raise ValueError("feature row count mismatch")
    maximum = 0.0
    for index, (left, example) in enumerate(zip(observed, examples, strict=True)):
        for key in ("row_id", "task_id", "model"):
            if left[key] != example[key]:
                raise ValueError(f"feature identity mismatch: {key}")
        if int(left["segment_count"]) != len(example["segments"]):
            raise ValueError("feature segment count mismatch")
        if set(left["features"]) != set(expected):
            raise ValueError("feature method set mismatch")
        for method in expected:
            values = np.asarray(left["features"][method], dtype=np.float64)
            maximum = max(
                maximum,
                float(np.max(np.abs(values - expected[method][index]))),
            )
    return maximum


def verify_prediction_rows(
    observed: list[dict[str, Any]],
    phase: str,
    examples: list[dict[str, Any]],
    expected: dict[str, np.ndarray],
) -> float:
    if len(observed) != len(examples):
        raise ValueError("prediction row count mismatch")
    maximum = 0.0
    for index, (left, example) in enumerate(zip(observed, examples, strict=True)):
        expected_identity = {
            "phase": phase,
            "row_id": example["row_id"],
            "task_id": example["task_id"],
            "model": example["model"],
            "source_dataset": example["source_dataset"],
            "target": example["target"],
            "fold": example["fold"],
        }
        for key, value in expected_identity.items():
            if left[key] != value:
                raise ValueError(f"prediction identity mismatch: {key}")
        if set(left["scores"]) != set(METHODS):
            raise ValueError("prediction method set mismatch")
        for method in METHODS:
            maximum = max(
                maximum,
                abs(float(left["scores"][method]) - expected[method][index]),
            )
    return maximum


def verify_frozen_full_models(
    frozen_model: dict[str, Any],
    examples: list[dict[str, Any]],
    features: dict[str, np.ndarray],
    base: Any,
    config: dict[str, Any],
) -> float:
    if tuple(frozen_model["methods"]) != METHODS:
        raise ValueError("frozen model methods mismatch")
    if frozen_model["experiment_id"] != config["experiment_id"]:
        raise ValueError("frozen experiment ID mismatch")
    if frozen_model["development_task_ids"] != sorted(
        {item["task_id"] for item in examples}
    ):
        raise ValueError("frozen Development tasks mismatch")
    maximum = 0.0
    for target_model in config["generator_models"]:
        train = np.asarray(
            [
                index
                for index, item in enumerate(examples)
                if item["model"] != target_model
            ],
            dtype=np.int64,
        )
        heldout = np.asarray(
            [
                index
                for index, item in enumerate(examples)
                if item["model"] == target_model
            ],
            dtype=np.int64,
        )
        independent = train_bundle(examples, features, train, base, config)
        expected = apply_bundle(independent, examples, features, heldout)
        observed = apply_bundle(
            frozen_model["full_bundles"][target_model],
            examples,
            features,
            heldout,
        )
        for method in METHODS:
            maximum = max(
                maximum,
                float(np.max(np.abs(expected[method] - observed[method]))),
            )
    return maximum


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
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()

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
    observed_model_files = sorted(
        path.name for path in args.model_dir.iterdir() if path.is_file()
    )
    if observed_model_files != sorted(config["model_files"]):
        raise ValueError("model file set mismatch")
    for name, digest in config["model_files"].items():
        if sha256_path(args.model_dir / name) != digest:
            raise ValueError(f"model SHA mismatch: {name}")

    base = load_base(args.base_module)
    source_rows = []
    for path in args.dataset:
        source_rows.extend(load_jsonl(path))
    examples = prepare_rows(
        source_rows, base, int(config["task_fold_modulus"])
    )
    features, pair_rows = recompute_relevance(examples, args.model_dir, config)
    frozen_model = joblib.load(args.frozen_model) if args.frozen_model else None
    scores, folds = recompute_predictions(
        args.phase,
        examples,
        features,
        base,
        config,
        frozen_model,
    )

    observed_pairs = load_jsonl(args.output_dir / "pair_scores.jsonl")
    observed_features = load_jsonl(args.output_dir / "feature_rows.jsonl")
    observed_predictions = load_jsonl(args.output_dir / "raw_predictions.jsonl")
    pair_error = verify_pair_rows(observed_pairs, pair_rows)
    feature_error = verify_feature_rows(observed_features, examples, features)
    prediction_error = verify_prediction_rows(
        observed_predictions, args.phase, examples, scores
    )
    observed_summary = json.loads(
        (args.output_dir / "summary.json").read_text(encoding="utf-8")
    )
    summary = independent_summary(
        args.phase, examples, scores, folds, config, frozen_model
    )
    comparable = {
        key: observed_summary[key]
        for key in summary
    }
    summary_error = maximum_error(comparable, summary)
    if observed_summary["pair_scores_sha256"] != sha256_path(
        args.output_dir / "pair_scores.jsonl"
    ):
        raise ValueError("summary pair-score SHA mismatch")
    if observed_summary["feature_rows_sha256"] != sha256_path(
        args.output_dir / "feature_rows.jsonl"
    ):
        raise ValueError("summary feature SHA mismatch")
    if observed_summary["raw_predictions_sha256"] != sha256_path(
        args.output_dir / "raw_predictions.jsonl"
    ):
        raise ValueError("summary prediction SHA mismatch")
    if observed_summary["config_sha256"] != sha256_path(args.config):
        raise ValueError("summary config SHA mismatch")
    if observed_summary["base_module_sha256"] != sha256_path(args.base_module):
        raise ValueError("summary base SHA mismatch")

    full_model_error = None
    if args.phase == "development":
        frozen_output = joblib.load(args.output_dir / "model.joblib")
        if (
            frozen_output["strongest_development_comparator"]
            != summary["strongest_comparator"]
        ):
            raise ValueError("frozen strongest comparator mismatch")
        full_model_error = verify_frozen_full_models(
            frozen_output, examples, features, base, config
        )

    tolerances = {
        "pair_score": 1e-6,
        "feature": 1e-12,
        "prediction": 1e-10,
        "summary": 1e-12,
        "full_model_prediction": 1e-10,
    }
    passed = (
        pair_error <= tolerances["pair_score"]
        and feature_error <= tolerances["feature"]
        and prediction_error <= tolerances["prediction"]
        and summary_error <= tolerances["summary"]
        and (
            full_model_error is None
            or full_model_error <= tolerances["full_model_prediction"]
        )
    )
    report = {
        "audit_ok": passed,
        "phase": args.phase,
        "rows": len(examples),
        "tasks": len({item["task_id"] for item in examples}),
        "pair_rows": len(pair_rows),
        "max_pair_score_error": pair_error,
        "max_feature_error": feature_error,
        "max_prediction_error": prediction_error,
        "max_summary_error": summary_error,
        "max_full_model_prediction_error": full_model_error,
        "tolerances": tolerances,
        "gates": summary["gates"],
        "all_gates_passed": summary["all_gates_passed"],
        "config_sha256": sha256_path(args.config),
        "base_module_sha256": sha256_path(args.base_module),
        "raw_predictions_sha256": sha256_path(
            args.output_dir / "raw_predictions.jsonl"
        ),
        "pair_scores_sha256": sha256_path(args.output_dir / "pair_scores.jsonl"),
        "feature_rows_sha256": sha256_path(args.output_dir / "feature_rows.jsonl"),
    }
    write_json(args.report, report)
    if not passed:
        raise ValueError("AUDIT_FAILED")
    print(
        json.dumps(
            {
                "status": "AUDIT_OK",
                "phase": args.phase,
                "rows": len(examples),
                "pairs": len(pair_rows),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
