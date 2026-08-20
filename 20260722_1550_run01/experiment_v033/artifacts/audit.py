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


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def load_base(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("v032_audit_base", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load audit base")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_task(prompt: str) -> str:
    left = prompt.find("Task Description:")
    right = prompt.find("Current terminal state:", left + 17)
    if left < 0 or right < 0:
        raise ValueError("task markers absent")
    value = prompt[left + len("Task Description:") : right].strip()
    if not value:
        raise ValueError("empty task")
    return value


def task_fold(task_id: str, modulus: int) -> int:
    return hashlib.sha256(task_id.encode("utf-8")).digest()[1] % modulus


def examples_from(
    datasets: list[Path], base: Any, fold_modulus: int
) -> list[dict[str, Any]]:
    rows = [row for path in datasets for row in read_jsonl(path)]
    if len({str(row["row_id"]) for row in rows}) != len(rows):
        raise ValueError("duplicate row IDs")
    values = []
    for row in rows:
        task_id = str(row["task_id"])
        target = int(row["target"])
        if target not in {0, 1}:
            raise ValueError("non-binary target")
        values.append(
            {
                "row_id": str(row["row_id"]),
                "task_id": task_id,
                "model": str(row["model"]),
                "source_dataset": str(row["source_dataset"]),
                "target": target,
                "fold": task_fold(task_id, fold_modulus),
                "task": extract_task(str(row["task_prompt"])),
                "action": base.action_text(row),
            }
        )
    values.sort(key=lambda item: (item["task_id"], item["model"], item["row_id"]))
    return values


def task_weights(examples: list[dict[str, Any]], indexes: np.ndarray) -> np.ndarray:
    counts = Counter(examples[int(index)]["task_id"] for index in indexes)
    return np.asarray(
        [1.0 / counts[examples[int(index)]["task_id"]] for index in indexes],
        dtype=np.float64,
    )


def coordinates(
    vectorizer: Any,
    svd: TruncatedSVD,
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    tasks = vectorizer.transform([examples[int(index)]["task"] for index in indexes])
    actions = vectorizer.transform(
        [examples[int(index)]["action"] for index in indexes]
    )
    return (
        np.asarray(normalize(svd.transform(tasks), norm="l2"), dtype=np.float64),
        np.asarray(normalize(svd.transform(actions), norm="l2"), dtype=np.float64),
    )


def feature_views(
    task: np.ndarray,
    action: np.ndarray,
    all_map: Ridge,
    successful_map: Ridge,
) -> dict[str, np.ndarray]:
    return {
        "latent_additive": np.hstack([task, action]),
        "identity_innovation": np.abs(action - task),
        "all_row_innovation": np.abs(
            action - np.asarray(all_map.predict(task), dtype=np.float64)
        ),
        "successful_innovation": np.abs(
            action - np.asarray(successful_map.predict(task), dtype=np.float64)
        ),
    }


def audit_fit_bundle(
    examples: list[dict[str, Any]],
    train: np.ndarray,
    base: Any,
    config: dict[str, Any],
) -> dict[str, Any]:
    labels = np.asarray(
        [examples[int(index)]["target"] for index in train], dtype=np.int64
    )
    base.ensure_two_classes(labels, "audit train")
    action_texts = [examples[int(index)]["action"] for index in train]

    direct_vectorizer = base.make_vectorizer(config)
    direct_matrix = direct_vectorizer.fit_transform(action_texts).tocsr()
    direct_model = base.make_classifier(config)
    direct_model.fit(direct_matrix, labels)

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
    concat_model.fit(concat_matrix, labels)

    latent_vectorizer = base.make_vectorizer(config)
    latent_matrix = latent_vectorizer.fit_transform(
        [examples[int(index)]["task"] for index in train] + action_texts
    )
    svd = TruncatedSVD(
        n_components=int(config["latent_dimensions"]),
        algorithm="randomized",
        n_iter=int(config["svd_iterations"]),
        random_state=int(config["seed"]),
    )
    svd.fit(latent_matrix)
    task_latent, action_latent = coordinates(
        latent_vectorizer, svd, examples, train
    )

    ridge_args = {
        "alpha": float(config["ridge_alpha"]),
        "fit_intercept": True,
        "solver": "lsqr",
        "max_iter": int(config["ridge_max_iter"]),
        "tol": float(config["ridge_tolerance"]),
    }
    all_map = Ridge(**ridge_args)
    all_map.fit(
        task_latent,
        action_latent,
        sample_weight=task_weights(examples, train),
    )
    successful_local = np.flatnonzero(labels == 0)
    successful_indexes = train[successful_local]
    successful_map = Ridge(**ridge_args)
    successful_map.fit(
        task_latent[successful_local],
        action_latent[successful_local],
        sample_weight=task_weights(examples, successful_indexes),
    )
    views = feature_views(task_latent, action_latent, all_map, successful_map)
    dense_models = {}
    for name in DENSE_METHODS:
        scaler = StandardScaler().fit(views[name])
        matrix = sparse.hstack(
            [
                direct_matrix,
                sparse.csr_matrix(scaler.transform(views[name])),
            ],
            format="csr",
        )
        model = base.make_classifier(config)
        model.fit(matrix, labels)
        dense_models[name] = {"scaler": scaler, "model": model}
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
    }


def audit_score_bundle(
    bundle: dict[str, Any],
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    direct = bundle["direct_vectorizer"].transform(
        [examples[int(index)]["action"] for index in indexes]
    ).tocsr()
    scores = {
        "direct_action": np.asarray(
            bundle["direct_model"].predict_proba(direct)[:, 1], dtype=np.float64
        )
    }
    concat = bundle["concat_vectorizer"].transform(
        [
            "TASK\n"
            + examples[int(index)]["task"]
            + "\nACTION\n"
            + examples[int(index)]["action"]
            for index in indexes
        ]
    ).tocsr()
    scores["task_concat"] = np.asarray(
        bundle["concat_model"].predict_proba(concat)[:, 1], dtype=np.float64
    )
    task_latent, action_latent = coordinates(
        bundle["latent_vectorizer"], bundle["svd"], examples, indexes
    )
    views = feature_views(
        task_latent,
        action_latent,
        bundle["all_map"],
        bundle["successful_map"],
    )
    for name in DENSE_METHODS:
        dense = bundle["dense_models"][name]
        matrix = sparse.hstack(
            [
                direct,
                sparse.csr_matrix(dense["scaler"].transform(views[name])),
            ],
            format="csr",
        )
        scores[name] = np.asarray(
            dense["model"].predict_proba(matrix)[:, 1], dtype=np.float64
        )
    return scores, views


def tpr5(labels: np.ndarray, scores: np.ndarray) -> float:
    fpr, tpr, _ = roc_curve(labels, scores)
    return float(np.max(tpr[fpr <= 0.05]))


def metrics(
    labels: np.ndarray, scores: dict[str, np.ndarray]
) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "auc": float(roc_auc_score(labels, scores[name])),
            "tpr_at_5pct_fpr": tpr5(labels, scores[name]),
            "rows": int(len(labels)),
            "negatives": int(np.sum(labels == 0)),
            "positives": int(np.sum(labels == 1)),
        }
        for name in METHODS
    }


def clustered_delta(
    examples: list[dict[str, Any]],
    candidate: np.ndarray,
    comparator: np.ndarray,
    repeats: int,
    seed: int,
) -> dict[str, Any]:
    tasks = sorted({item["task_id"] for item in examples})
    grouped = {
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
    labels = np.asarray([item["target"] for item in examples], dtype=np.int64)
    random = np.random.default_rng(seed)
    values = []
    while len(values) < repeats:
        sampled = random.choice(tasks, size=len(tasks), replace=True)
        indexes = np.concatenate([grouped[str(task)] for task in sampled])
        local = labels[indexes]
        if len(np.unique(local)) != 2:
            continue
        values.append(
            float(
                roc_auc_score(local, candidate[indexes])
                - roc_auc_score(local, comparator[indexes])
            )
        )
    return {
        "point": float(
            roc_auc_score(labels, candidate) - roc_auc_score(labels, comparator)
        ),
        "bootstrap_95": [
            float(np.quantile(values, 0.025)),
            float(np.quantile(values, 0.975)),
        ],
        "repeats": repeats,
        "resampling_unit": "task_id",
        "tasks": len(tasks),
    }


def sliced(
    examples: list[dict[str, Any]],
    candidate: np.ndarray,
    comparator: np.ndarray,
    field: str,
) -> dict[str, dict[str, Any]]:
    labels = np.asarray([item["target"] for item in examples], dtype=np.int64)
    output = {}
    for value in sorted({str(item[field]) for item in examples}):
        indexes = np.asarray(
            [
                index
                for index, item in enumerate(examples)
                if str(item[field]) == value
            ],
            dtype=np.int64,
        )
        local = labels[indexes]
        left = float(roc_auc_score(local, candidate[indexes]))
        right = float(roc_auc_score(local, comparator[indexes]))
        output[value] = {
            "rows": int(len(indexes)),
            "negatives": int(np.sum(local == 0)),
            "positives": int(np.sum(local == 1)),
            "candidate_auc": left,
            "strongest_auc": right,
            "delta": left - right,
        }
    return output


def recompute(
    examples: list[dict[str, Any]],
    base: Any,
    config: dict[str, Any],
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], dict[str, Any], dict[str, Any]]:
    dimensions = int(config["latent_dimensions"])
    scores = {name: np.full(len(examples), np.nan) for name in METHODS}
    features = {
        "latent_additive": np.full((len(examples), dimensions * 2), np.nan),
        "identity_innovation": np.full((len(examples), dimensions), np.nan),
        "all_row_innovation": np.full((len(examples), dimensions), np.nan),
        "successful_innovation": np.full((len(examples), dimensions), np.nan),
    }
    folds = []
    for target_model in tuple(config["generator_models"]):
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
            bundle = audit_fit_bundle(examples, train, base, config)
            local_scores, local_features = audit_score_bundle(
                bundle, examples, heldout
            )
            for name in METHODS:
                scores[name][heldout] = local_scores[name]
            for name in DENSE_METHODS:
                features[name][heldout] = local_features[name]
            successful_indexes = train[
                np.asarray(
                    [examples[int(index)]["target"] == 0 for index in train],
                    dtype=bool,
                )
            ]
            folds.append(
                {
                    "target_model": target_model,
                    "fold": fold,
                    "train_rows": int(len(train)),
                    "heldout_rows": int(len(heldout)),
                    "train_tasks": int(
                        len({examples[int(index)]["task_id"] for index in train})
                    ),
                    "heldout_tasks": int(
                        len({examples[int(index)]["task_id"] for index in heldout})
                    ),
                    "successful_rows": int(len(successful_indexes)),
                    "successful_tasks": int(
                        len(
                            {
                                examples[int(index)]["task_id"]
                                for index in successful_indexes
                            }
                        )
                    ),
                    "latent_vocabulary": int(
                        len(bundle["latent_vectorizer"].vocabulary_)
                    ),
                }
            )
    if any(np.isnan(scores[name]).any() for name in METHODS):
        raise ValueError("audit OOF scores incomplete")
    if any(np.isnan(features[name]).any() for name in DENSE_METHODS):
        raise ValueError("audit OOF features incomplete")

    labels = np.asarray([item["target"] for item in examples], dtype=np.int64)
    metric_values = metrics(labels, scores)
    strongest = max(
        COMPARATORS, key=lambda name: (metric_values[name]["auc"], name)
    )
    delta = clustered_delta(
        examples,
        scores["successful_innovation"],
        scores[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    generators = sliced(
        examples,
        scores["successful_innovation"],
        scores[strongest],
        "model",
    )
    sources = sliced(
        examples,
        scores["successful_innovation"],
        scores[strongest],
        "source_dataset",
    )
    positive_generators = sum(item["delta"] > 0 for item in generators.values())
    nonnegative_sources = sum(item["delta"] >= 0 for item in sources.values())
    candidate = metric_values["successful_innovation"]
    gate_config = config["development_gates"]
    gates = {
        "candidate_auc": candidate["auc"] >= gate_config["candidate_auc_min"],
        "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"]
        >= gate_config["candidate_tpr_at_5fpr_min"],
        "auc_delta": delta["point"] >= gate_config["candidate_auc_delta_min"],
        "bootstrap_lower": delta["bootstrap_95"][0] > 0.0,
        "strictly_beats_every_comparator": all(
            candidate["auc"] > metric_values[name]["auc"] for name in COMPARATORS
        ),
        "all_generator_slices_nonnegative": all(
            item["delta"] >= 0 for item in generators.values()
        ),
        "minimum_positive_generator_slices": positive_generators
        >= gate_config["minimum_positive_generator_slices"],
        "minimum_nonnegative_source_slices": nonnegative_sources
        >= gate_config["minimum_nonnegative_source_slices"],
    }
    summary = {
        "phase": "development",
        "rows": len(examples),
        "tasks": len({item["task_id"] for item in examples}),
        "models": sorted({item["model"] for item in examples}),
        "source_datasets": dict(Counter(item["source_dataset"] for item in examples)),
        "folds": folds,
        "metrics": metric_values,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "generator_slices": generators,
        "source_slices": sources,
        "positive_generator_slices": positive_generators,
        "nonnegative_source_slices": nonnegative_sources,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
        "all_gates_passed": all(gates.values()),
    }
    full_bundles = {}
    for target_model in tuple(config["generator_models"]):
        train = np.asarray(
            [
                index
                for index, item in enumerate(examples)
                if item["model"] != target_model
            ],
            dtype=np.int64,
        )
        full_bundles[target_model] = audit_fit_bundle(examples, train, base, config)
    return scores, features, summary, full_bundles


def maximum_numeric_error(left: Any, right: Any, path: str = "") -> float:
    if isinstance(left, dict):
        if set(left) != set(right):
            raise ValueError(f"mapping keys differ at {path}")
        return max(
            (
                maximum_numeric_error(left[key], right[key], f"{path}/{key}")
                for key in left
            ),
            default=0.0,
        )
    if isinstance(left, list):
        if len(left) != len(right):
            raise ValueError(f"list length differs at {path}")
        return max(
            (
                maximum_numeric_error(a, b, f"{path}/{index}")
                for index, (a, b) in enumerate(zip(left, right, strict=True))
            ),
            default=0.0,
        )
    if isinstance(left, (int, float)) and not isinstance(left, bool):
        return abs(float(left) - float(right))
    if left != right:
        raise ValueError(f"value differs at {path}: {left!r} != {right!r}")
    return 0.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--evidence-packet", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, action="append", required=True)
    parser.add_argument("--input-manifest", type=Path, action="append", required=True)
    parser.add_argument("--base-module", type=Path, required=True)
    parser.add_argument("--raw-predictions", type=Path, required=True)
    parser.add_argument("--feature-rows", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if digest(args.candidate) != config["candidate_sha256"]:
        raise ValueError("audit Candidate SHA mismatch")
    if digest(args.base_module) != config["base_module_sha256"]:
        raise ValueError("audit base SHA mismatch")
    if len(args.dataset) != len(config["development_inputs"]):
        raise ValueError("audit dataset count mismatch")
    expected = {
        (
            item["dataset_sha256"],
            item["manifest_sha256"],
            int(item["bucket"]),
            item["acquisition_phase"],
        )
        for item in config["development_inputs"]
    }
    observed = set()
    for dataset, manifest_path in zip(
        args.dataset, args.input_manifest, strict=True
    ):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        identity = (
            digest(dataset),
            digest(manifest_path),
            int(manifest["bucket"]),
            manifest["phase"],
        )
        if manifest["dataset_sha256"] != identity[0]:
            raise ValueError("audit manifest dataset mismatch")
        observed.add(identity)
    if observed != expected:
        raise ValueError("audit input binding mismatch")

    base = load_base(args.base_module)
    examples = examples_from(args.dataset, base, int(config["task_fold_modulus"]))
    scores, features, recomputed, full_bundles = recompute(examples, base, config)

    raw = read_jsonl(args.raw_predictions)
    if len(raw) != len(examples):
        raise ValueError("raw prediction row count mismatch")
    score_error = 0.0
    identity_error = 0
    for index, (source, item) in enumerate(zip(raw, examples, strict=True)):
        expected_identity = (
            item["row_id"],
            item["task_id"],
            item["model"],
            item["source_dataset"],
            item["target"],
            item["fold"],
            hashlib.sha256(item["task"].encode("utf-8")).hexdigest(),
            hashlib.sha256(item["action"].encode("utf-8")).hexdigest(),
        )
        observed_identity = (
            source["row_id"],
            source["task_id"],
            source["model"],
            source["source_dataset"],
            int(source["target"]),
            int(source["fold"]),
            source["task_sha256"],
            source["action_sha256"],
        )
        identity_error += observed_identity != expected_identity
        for name in METHODS:
            score_error = max(
                score_error, abs(float(source["scores"][name]) - scores[name][index])
            )

    frozen_features = read_jsonl(args.feature_rows)
    if len(frozen_features) != len(examples):
        raise ValueError("feature row count mismatch")
    feature_error = 0.0
    for index, source in enumerate(frozen_features):
        if source["row_id"] != examples[index]["row_id"]:
            raise ValueError("feature row identity mismatch")
        for name in DENSE_METHODS:
            observed_values = np.asarray(source["features"][name], dtype=np.float64)
            feature_error = max(
                feature_error,
                float(np.max(np.abs(observed_values - features[name][index]))),
            )

    frozen_summary = json.loads(args.summary.read_text(encoding="utf-8"))
    summary_subset = {
        key: frozen_summary[key]
        for key in (
            "phase",
            "rows",
            "tasks",
            "models",
            "source_datasets",
            "folds",
            "metrics",
            "strongest_comparator",
            "candidate_minus_strongest",
            "generator_slices",
            "source_slices",
            "positive_generator_slices",
            "nonnegative_source_slices",
            "gates",
            "gates_passed",
            "gates_total",
            "all_gates_passed",
        )
    }
    summary_error = maximum_numeric_error(summary_subset, recomputed)

    frozen_model = joblib.load(args.model)
    if tuple(frozen_model["methods"]) != METHODS:
        raise ValueError("frozen method identity mismatch")
    full_model_error = 0.0
    for target_model in tuple(config["generator_models"]):
        indexes = np.asarray(
            [
                index
                for index, item in enumerate(examples)
                if item["model"] == target_model
            ],
            dtype=np.int64,
        )
        expected_scores, expected_features = audit_score_bundle(
            full_bundles[target_model], examples, indexes
        )
        observed_scores, observed_features = audit_score_bundle(
            frozen_model["full_bundles"][target_model], examples, indexes
        )
        for name in METHODS:
            full_model_error = max(
                full_model_error,
                float(np.max(np.abs(expected_scores[name] - observed_scores[name]))),
            )
        for name in DENSE_METHODS:
            full_model_error = max(
                full_model_error,
                float(
                    np.max(
                        np.abs(expected_features[name] - observed_features[name])
                    )
                ),
            )

    tolerance = float(config["audit_tolerance"])
    status = (
        "AUDIT_OK"
        if identity_error == 0
        and score_error <= tolerance
        and feature_error <= tolerance
        and summary_error <= tolerance
        and full_model_error <= tolerance
        else "AUDIT_FAIL"
    )
    report = {
        "status": status,
        "evaluated_rows": len(examples),
        "tasks": len({item["task_id"] for item in examples}),
        "oof_scores_recomputed": len(examples) * len(METHODS),
        "dense_feature_values_recomputed": int(
            sum(features[name].size for name in DENSE_METHODS)
        ),
        "identity_mismatches": identity_error,
        "maximum_score_error": score_error,
        "maximum_feature_error": feature_error,
        "maximum_summary_error": summary_error,
        "maximum_frozen_full_model_error": full_model_error,
        "candidate_sha256": digest(args.candidate),
        "evidence_packet_sha256": digest(args.evidence_packet),
        "config_sha256": digest(args.config),
        "base_module_sha256": digest(args.base_module),
        "raw_predictions_sha256": digest(args.raw_predictions),
        "feature_rows_sha256": digest(args.feature_rows),
        "summary_sha256": digest(args.summary),
        "model_sha256": digest(args.model),
    }
    args.report.parent.mkdir(parents=True, exist_ok=False)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, sort_keys=True))
    return 0 if status == "AUDIT_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
