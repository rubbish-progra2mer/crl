from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import scipy
import sklearn
import torch
from scipy import sparse


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


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for value in values:
            handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("v023_base_v012", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_examples(rows: list[dict[str, Any]], base: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    examples: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    for row in rows:
        command_text = "COMMANDS\n" + "\n".join(str(value) for value in row["commands"])
        output_text = "OUTPUTS\n" + "\n".join(str(value) for value in row["terminal_outputs"])
        examples.append(
            {
                "row": row,
                "row_id": str(row["row_id"]),
                "task_id": str(row["task_id"]),
                "target": int(row["target"]),
                "mixed_text": base.action_text(row),
                "command_text": command_text,
                "output_text": output_text,
            }
        )
        sources.append(
            {
                "row_id": str(row["row_id"]),
                "task_id": str(row["task_id"]),
                "source_relative_path": str(row["source_relative_path"]),
                "source_sha256": str(row["source_sha256"]),
            }
        )
    examples.sort(key=lambda item: (item["task_id"], item["row_id"]))
    sources.sort(key=lambda item: (item["task_id"], item["row_id"]))
    if len({item["row_id"] for item in examples}) != len(examples):
        raise ValueError("duplicate row IDs")
    return examples, sources


def feature_matrices(
    mixed: sparse.csr_matrix,
    commands: sparse.csr_matrix,
    outputs: sparse.csr_matrix,
) -> dict[str, sparse.csr_matrix]:
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


def indexes_for(examples: list[dict[str, Any]], split: str) -> np.ndarray:
    return np.asarray(
        [index for index, item in enumerate(examples) if item.get("split") == split],
        dtype=np.int64,
    )


def labels_for(examples: list[dict[str, Any]], indexes: np.ndarray) -> np.ndarray:
    return np.asarray([examples[int(index)]["target"] for index in indexes], dtype=np.int64)


def transform_partition(
    examples: list[dict[str, Any]], indexes: np.ndarray, vectorizer: Any
) -> dict[str, sparse.csr_matrix]:
    mixed = vectorizer.transform([examples[int(index)]["mixed_text"] for index in indexes]).tocsr()
    commands = vectorizer.transform([examples[int(index)]["command_text"] for index in indexes]).tocsr()
    outputs = vectorizer.transform([examples[int(index)]["output_text"] for index in indexes]).tocsr()
    return feature_matrices(mixed, commands, outputs)


def metric_bundle(
    base: Any,
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
    scores: dict[str, np.ndarray],
    thresholds: dict[str, float],
) -> dict[str, Any]:
    y = labels_for(examples, indexes)
    return {name: base.metric_record(y, scores[name], thresholds[name]) for name in METHODS}


def raw_predictions(
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
    scores: dict[str, np.ndarray],
    split: str,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for local_index, example_index in enumerate(indexes):
        item = examples[int(example_index)]
        row = item["row"]
        result.append(
            {
                "split": split,
                "task_id": item["task_id"],
                "row_id": item["row_id"],
                "target": item["target"],
                "model": row["model"],
                "source_dataset": row["source_dataset"],
                "observed_categories": row.get("observed_categories", []),
                "scores": {name: float(scores[name][local_index]) for name in METHODS},
            }
        )
    return result


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


def fit_development(
    examples: list[dict[str, Any]], config: dict[str, Any], base: Any
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    for item in examples:
        item["split"] = base.split_name(item["task_id"], config)
    train = indexes_for(examples, "train")
    validation = indexes_for(examples, "validation")
    test = indexes_for(examples, "development_test")
    y_train = labels_for(examples, train)
    y_validation = labels_for(examples, validation)
    y_test = labels_for(examples, test)
    for name, values in (("train", y_train), ("validation", y_validation), ("test", y_test)):
        base.ensure_two_classes(values, name)

    vectorizer = base.make_vectorizer(config)
    train_mixed = vectorizer.fit_transform(
        [examples[int(index)]["mixed_text"] for index in train]
    ).tocsr()
    train_commands = vectorizer.transform(
        [examples[int(index)]["command_text"] for index in train]
    ).tocsr()
    train_outputs = vectorizer.transform(
        [examples[int(index)]["output_text"] for index in train]
    ).tocsr()
    train_features = feature_matrices(train_mixed, train_commands, train_outputs)
    models = {
        name: base.make_classifier(config).fit(train_features[name], y_train)
        for name in METHODS
    }

    validation_features = transform_partition(examples, validation, vectorizer)
    validation_scores = {
        name: models[name].predict_proba(validation_features[name])[:, 1]
        for name in METHODS
    }
    thresholds = {
        name: base.select_threshold(y_validation, validation_scores[name])
        for name in METHODS
    }
    test_features = transform_partition(examples, test, vectorizer)
    test_scores = {
        name: models[name].predict_proba(test_features[name])[:, 1]
        for name in METHODS
    }
    metrics = metric_bundle(base, examples, test, test_scores, thresholds)
    strongest = max(COMPARATORS, key=lambda name: (metrics[name]["auc"], name))
    delta = base.task_cluster_auc_delta(
        examples,
        test,
        test_scores["role_factorized"],
        test_scores[strongest],
        repeats=int(config["bootstrap_repeats"]),
        seed=int(config["seed"]),
    )
    candidate = metrics["role_factorized"]
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
    tasks = sorted({item["task_id"] for item in examples})
    bundle = {
        "vectorizer": vectorizer,
        "models": models,
        "thresholds": thresholds,
        "strongest_development_comparator": strongest,
        "development_task_ids": tasks,
        "feature_dimensions": {name: int(train_features[name].shape[1]) for name in METHODS},
    }
    summary = {
        "phase": "development",
        "partition": {
            "train": {"tasks": len({examples[int(i)]["task_id"] for i in train}), "rows": len(train)},
            "validation": {"tasks": len({examples[int(i)]["task_id"] for i in validation}), "rows": len(validation)},
            "development_test": {"tasks": len({examples[int(i)]["task_id"] for i in test}), "rows": len(test)},
        },
        "metrics": metrics,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
        "thresholds": thresholds,
        "feature_dimensions": bundle["feature_dimensions"],
        "training_task_ids": sorted({examples[int(i)]["task_id"] for i in train}),
        "validation_task_ids": sorted({examples[int(i)]["task_id"] for i in validation}),
        "development_test_task_ids": sorted({examples[int(i)]["task_id"] for i in test}),
    }
    return bundle, raw_predictions(examples, test, test_scores, "development_test"), summary


def score_confirmation(
    examples: list[dict[str, Any]], config: dict[str, Any], base: Any, bundle: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    confirmation_tasks = sorted({item["task_id"] for item in examples})
    overlap = sorted(set(confirmation_tasks) & set(bundle["development_task_ids"]))
    if overlap:
        raise ValueError("Development and Confirmation tasks overlap")
    for item in examples:
        item["split"] = "confirmation"
    indexes = np.arange(len(examples), dtype=np.int64)
    y = labels_for(examples, indexes)
    base.ensure_two_classes(y, "confirmation")
    matrices = transform_partition(examples, indexes, bundle["vectorizer"])
    scores = {
        name: bundle["models"][name].predict_proba(matrices[name])[:, 1]
        for name in METHODS
    }
    metrics = metric_bundle(base, examples, indexes, scores, bundle["thresholds"])
    strongest = str(bundle["strongest_development_comparator"])
    delta = base.task_cluster_auc_delta(
        examples,
        indexes,
        scores["role_factorized"],
        scores[strongest],
        repeats=int(config["bootstrap_repeats"]),
        seed=int(config["seed"]),
    )
    candidate = metrics["role_factorized"]
    gate_config = config["confirmation_gates"]
    gates = {
        "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
        "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"] >= float(gate_config["candidate_tpr_at_5fpr_min"]),
        "auc_delta_vs_frozen_strongest": delta["point"] > 0.0,
        "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] >= 0.0,
        "fixed_threshold_fpr": candidate["fixed_threshold"]["fpr"] <= float(gate_config["fixed_threshold_fpr_max"]),
        "fixed_threshold_tpr": candidate["fixed_threshold"]["tpr"] >= float(gate_config["fixed_threshold_tpr_min"]),
        "strictly_beats_every_comparator": all(candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS),
        "task_ids_disjoint": not overlap,
    }
    summary = {
        "phase": "confirmation",
        "tasks": len(confirmation_tasks),
        "rows": len(examples),
        "metrics": metrics,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
        "development_task_overlap": overlap,
        "confirmation_task_ids": confirmation_tasks,
        "thresholds": bundle["thresholds"],
    }
    return raw_predictions(examples, indexes, scores, "confirmation"), summary


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", action="append", type=Path, required=True)
    parser.add_argument("--base-module", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--input-manifest", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    started = time.perf_counter()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if sha256_path(args.base_module) != config["base_module_sha256"]:
        raise ValueError("base module SHA mismatch")
    dataset_hashes = [sha256_path(path) for path in args.dataset]
    if args.phase == "development":
        if dataset_hashes != list(config["development_dataset_sha256s"]):
            raise ValueError("Development dataset SHA sequence mismatch")
    else:
        if len(args.dataset) != 1 or args.model is None or args.input_manifest is None:
            raise ValueError("Confirmation requires one dataset, model and input manifest")
        manifest = json.loads(args.input_manifest.read_text(encoding="utf-8"))
        if dataset_hashes[0] != manifest["dataset_sha256"]:
            raise ValueError("Confirmation dataset SHA mismatch")

    base = load_module(args.base_module)
    rows = [row for path in args.dataset for row in base.load_jsonl(path)]
    examples, sources = prepare_examples(rows, base)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    if args.phase == "development":
        bundle, predictions, summary = fit_development(examples, config, base)
        model_path = args.output_dir / "model.joblib"
        joblib.dump(bundle, model_path)
        summary["model"] = {"path": str(model_path), "bytes": model_path.stat().st_size, "sha256": sha256_path(model_path)}
    else:
        bundle = joblib.load(args.model)
        predictions, summary = score_confirmation(examples, config, base, bundle)
        summary["model"] = {"path": str(args.model), "bytes": args.model.stat().st_size, "sha256": sha256_path(args.model)}
        summary["input_manifest_sha256"] = sha256_path(args.input_manifest)

    write_jsonl(args.output_dir / "raw_predictions.jsonl", predictions)
    write_jsonl(args.output_dir / "source_records.jsonl", sources)
    summary.update(
        {
            "schema_version": 1,
            "experiment_id": "v023",
            "config_sha256": sha256_path(args.config),
            "dataset_sha256s": dataset_hashes,
            "base_module_sha256": sha256_path(args.base_module),
            "source_rows": len(rows),
            "evaluated_rows": len(examples),
            "source_records_sha256": sha256_path(args.output_dir / "source_records.jsonl"),
            "raw_predictions_sha256": sha256_path(args.output_dir / "raw_predictions.jsonl"),
            "environment": environment_record(time.perf_counter() - started),
        }
    )
    write_json(args.output_dir / "summary.json", summary)
    print(
        json.dumps(
            {
                "phase": args.phase,
                "candidate_auc": summary["metrics"]["role_factorized"]["auc"],
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
