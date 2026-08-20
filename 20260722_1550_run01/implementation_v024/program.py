from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
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
    spec = importlib.util.spec_from_file_location("v024_base_v012", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_anchor_batch(batch: str) -> bool:
    return bool(INSPECTION_RE.search(batch) and CHECKER_RE.search(batch))


def role_text(batches: list[str]) -> str:
    return "\n".join(batches)


def partition_commands(commands: list[str]) -> dict[str, Any]:
    anchor_indexes = [index for index, batch in enumerate(commands) if is_anchor_batch(batch)]
    anchor_index = anchor_indexes[0] if anchor_indexes else None
    if anchor_index is None:
        before = commands
        from_anchor: list[str] = []
    else:
        before = commands[:anchor_index]
        from_anchor = commands[anchor_index:]
    half = (len(commands) + 1) // 2
    matching = [batch for batch in commands if is_anchor_batch(batch)]
    nonmatching = [batch for batch in commands if not is_anchor_batch(batch)]
    return {
        "anchor_present": anchor_index is not None,
        "anchor_index": anchor_index,
        "before": before,
        "from_anchor": from_anchor,
        "first_half": commands[:half],
        "second_half": commands[half:],
        "anchor_matching": matching,
        "anchor_nonmatching": nonmatching,
    }


def fold_for_task(task_id: str, modulus: int) -> int:
    return hashlib.sha256(task_id.encode("utf-8")).digest()[1] % modulus


def prepare_examples(
    rows: list[dict[str, Any]], base: Any, fold_modulus: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    examples: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    for row in rows:
        commands = [str(value) for value in row["commands"]]
        outputs = [str(value) for value in row["terminal_outputs"]]
        parts = partition_commands(commands)
        task_id = str(row["task_id"])
        row_id = str(row["row_id"])
        examples.append(
            {
                "row": row,
                "row_id": row_id,
                "task_id": task_id,
                "target": int(row["target"]),
                "fold": fold_for_task(task_id, fold_modulus),
                "anchor_present": bool(parts["anchor_present"]),
                "anchor_index": parts["anchor_index"],
                "mixed_text": base.action_text(row),
                "commands_text": role_text(commands),
                "outputs_text": role_text(outputs),
                "first_half_text": role_text(parts["first_half"]),
                "second_half_text": role_text(parts["second_half"]),
                "anchor_matching_text": role_text(parts["anchor_matching"]),
                "anchor_nonmatching_text": role_text(parts["anchor_nonmatching"]),
                "before_text": role_text(parts["before"]),
                "from_anchor_text": role_text(parts["from_anchor"]),
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
        raise ValueError("duplicate row IDs")
    return examples, sources


def feature_matrices(
    mixed: sparse.csr_matrix,
    commands: sparse.csr_matrix,
    outputs: sparse.csr_matrix,
    first_half: sparse.csr_matrix,
    second_half: sparse.csr_matrix,
    anchor_matching: sparse.csr_matrix,
    anchor_nonmatching: sparse.csr_matrix,
    before: sparse.csr_matrix,
    from_anchor: sparse.csr_matrix,
) -> dict[str, sparse.csr_matrix]:
    return {
        "mixed": mixed,
        "commands": commands,
        "role_concat": sparse.hstack([commands, outputs], format="csr"),
        "command_duplicated": sparse.hstack([mixed, commands, commands], format="csr"),
        "fixed_halves": sparse.hstack([mixed, first_half, second_half], format="csr"),
        "anchor_bag": sparse.hstack([mixed, anchor_matching, anchor_nonmatching], format="csr"),
        "viaf": sparse.hstack([mixed, before, from_anchor], format="csr"),
    }


def transform(examples: list[dict[str, Any]], indexes: np.ndarray, vectorizer: Any) -> dict[str, sparse.csr_matrix]:
    def texts(name: str) -> list[str]:
        return [examples[int(index)][name] for index in indexes]

    return feature_matrices(
        vectorizer.transform(texts("mixed_text")).tocsr(),
        vectorizer.transform(texts("commands_text")).tocsr(),
        vectorizer.transform(texts("outputs_text")).tocsr(),
        vectorizer.transform(texts("first_half_text")).tocsr(),
        vectorizer.transform(texts("second_half_text")).tocsr(),
        vectorizer.transform(texts("anchor_matching_text")).tocsr(),
        vectorizer.transform(texts("anchor_nonmatching_text")).tocsr(),
        vectorizer.transform(texts("before_text")).tocsr(),
        vectorizer.transform(texts("from_anchor_text")).tocsr(),
    )


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


def task_bootstrap_delta(
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
    samples: list[float] = []
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
        "bootstrap_95": [
            float(np.quantile(samples, 0.025)),
            float(np.quantile(samples, 0.975)),
        ],
        "repeats": repeats,
        "resampling_unit": "task_id",
        "tasks": len(tasks),
    }


def stratum_delta(
    examples: list[dict[str, Any]], indexes: np.ndarray, scores: dict[str, np.ndarray], present: bool
) -> dict[str, Any]:
    local = [
        local_index
        for local_index, example_index in enumerate(indexes)
        if bool(examples[int(example_index)]["anchor_present"]) is present
    ]
    y = labels(examples, indexes)[local]
    if set(y.tolist()) != {0, 1}:
        raise ValueError("anchor stratum lacks two classes")
    return {
        "rows": len(local),
        "negatives": int(np.sum(y == 0)),
        "positives": int(np.sum(y == 1)),
        "viaf_auc": float(roc_auc_score(y, scores["viaf"][local])),
        "command_duplicated_auc": float(roc_auc_score(y, scores["command_duplicated"][local])),
        "delta": float(
            roc_auc_score(y, scores["viaf"][local])
            - roc_auc_score(y, scores["command_duplicated"][local])
        ),
    }


def raw_predictions(
    examples: list[dict[str, Any]], indexes: np.ndarray, scores: dict[str, np.ndarray], phase: str
) -> list[dict[str, Any]]:
    result = []
    for local_index, example_index in enumerate(indexes):
        item = examples[int(example_index)]
        row = item["row"]
        result.append(
            {
                "phase": phase,
                "fold": item["fold"] if phase == "development_oof" else None,
                "task_id": item["task_id"],
                "row_id": item["row_id"],
                "target": item["target"],
                "model": row["model"],
                "source_dataset": row["source_dataset"],
                "observed_categories": row.get("observed_categories", []),
                "anchor_present": item["anchor_present"],
                "anchor_index": item["anchor_index"],
                "command_batches": len(row["commands"]),
                "scores": {name: float(scores[name][local_index]) for name in METHODS},
            }
        )
    return result


def fit_models(matrices: dict[str, sparse.csr_matrix], y: np.ndarray, config: dict[str, Any], base: Any) -> dict[str, Any]:
    return {name: base.make_classifier(config).fit(matrices[name], y) for name in METHODS}


def fit_development(
    examples: list[dict[str, Any]], config: dict[str, Any], base: Any
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    indexes = np.arange(len(examples), dtype=np.int64)
    y = labels(examples, indexes)
    base.ensure_two_classes(y, "development")
    fold_count = int(config["fold_modulus"])
    oof_scores = {name: np.zeros(len(examples), dtype=np.float64) for name in METHODS}
    fold_bundles = []
    fold_records = []
    for fold in range(fold_count):
        train = np.asarray([i for i, item in enumerate(examples) if item["fold"] != fold], dtype=np.int64)
        heldout = np.asarray([i for i, item in enumerate(examples) if item["fold"] == fold], dtype=np.int64)
        y_train = labels(examples, train)
        y_heldout = labels(examples, heldout)
        base.ensure_two_classes(y_train, f"fold {fold} train")
        base.ensure_two_classes(y_heldout, f"fold {fold} heldout")
        vectorizer = base.make_vectorizer(config)
        vectorizer.fit([examples[int(index)]["mixed_text"] for index in train])
        train_matrices = transform(examples, train, vectorizer)
        models = fit_models(train_matrices, y_train, config, base)
        heldout_matrices = transform(examples, heldout, vectorizer)
        for name in METHODS:
            oof_scores[name][heldout] = models[name].predict_proba(heldout_matrices[name])[:, 1]
        fold_bundles.append(
            {
                "fold": fold,
                "vectorizer": vectorizer,
                "models": models,
                "heldout_task_ids": sorted({examples[int(i)]["task_id"] for i in heldout}),
                "feature_dimensions": {name: int(train_matrices[name].shape[1]) for name in METHODS},
            }
        )
        fold_records.append(
            {
                "fold": fold,
                "train_tasks": len({examples[int(i)]["task_id"] for i in train}),
                "train_rows": len(train),
                "heldout_tasks": len({examples[int(i)]["task_id"] for i in heldout}),
                "heldout_rows": len(heldout),
                "heldout_negatives": int(np.sum(y_heldout == 0)),
                "heldout_positives": int(np.sum(y_heldout == 1)),
                "vocabulary": len(vectorizer.vocabulary_),
            }
        )

    metrics = {name: metric_record(y, oof_scores[name]) for name in METHODS}
    strongest = max(COMPARATORS, key=lambda name: (metrics[name]["auc"], name))
    delta = task_bootstrap_delta(
        examples,
        indexes,
        oof_scores["viaf"],
        oof_scores[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    strata = {
        "anchor_present": stratum_delta(examples, indexes, oof_scores, True),
        "anchor_absent": stratum_delta(examples, indexes, oof_scores, False),
    }
    candidate = metrics["viaf"]
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

    full_vectorizer = base.make_vectorizer(config)
    full_vectorizer.fit([item["mixed_text"] for item in examples])
    full_matrices = transform(examples, indexes, full_vectorizer)
    full_models = fit_models(full_matrices, y, config, base)
    bundle = {
        "fold_bundles": fold_bundles,
        "full_vectorizer": full_vectorizer,
        "full_models": full_models,
        "strongest_development_comparator": strongest,
        "development_task_ids": sorted({item["task_id"] for item in examples}),
        "full_feature_dimensions": {name: int(full_matrices[name].shape[1]) for name in METHODS},
        "anchor_predicate_version": "viaf-anchor-v1",
    }
    summary = {
        "phase": "development",
        "evaluation": "five_fold_task_oof",
        "folds": fold_records,
        "tasks": len(bundle["development_task_ids"]),
        "rows": len(examples),
        "anchor_rows": int(sum(item["anchor_present"] for item in examples)),
        "metrics": metrics,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "anchor_strata": strata,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
        "full_feature_dimensions": bundle["full_feature_dimensions"],
    }
    return bundle, raw_predictions(examples, indexes, oof_scores, "development_oof"), summary


def score_confirmation(
    examples: list[dict[str, Any]], config: dict[str, Any], base: Any, bundle: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    tasks = sorted({item["task_id"] for item in examples})
    overlap = sorted(set(tasks) & set(bundle["development_task_ids"]))
    if overlap:
        raise ValueError("Development and Confirmation tasks overlap")
    indexes = np.arange(len(examples), dtype=np.int64)
    y = labels(examples, indexes)
    base.ensure_two_classes(y, "confirmation")
    matrices = transform(examples, indexes, bundle["full_vectorizer"])
    scores = {
        name: bundle["full_models"][name].predict_proba(matrices[name])[:, 1]
        for name in METHODS
    }
    metrics = {name: metric_record(y, scores[name]) for name in METHODS}
    strongest = str(bundle["strongest_development_comparator"])
    delta = task_bootstrap_delta(
        examples,
        indexes,
        scores["viaf"],
        scores[strongest],
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    strata = {
        "anchor_present": stratum_delta(examples, indexes, scores, True),
        "anchor_absent": stratum_delta(examples, indexes, scores, False),
    }
    candidate = metrics["viaf"]
    gate_config = config["confirmation_gates"]
    gates = {
        "candidate_auc": candidate["auc"] >= float(gate_config["candidate_auc_min"]),
        "candidate_tpr_at_5pct_fpr": candidate["tpr_at_5pct_fpr"] >= float(gate_config["candidate_tpr_at_5fpr_min"]),
        "auc_delta_vs_frozen_strongest": delta["point"] > 0.0,
        "auc_delta_bootstrap_lower": delta["bootstrap_95"][0] >= 0.0,
        "strictly_beats_every_comparator": all(candidate["auc"] > metrics[name]["auc"] for name in COMPARATORS),
        "anchor_present_delta": strata["anchor_present"]["delta"] > 0.0,
        "anchor_absent_delta": strata["anchor_absent"]["delta"] >= float(gate_config["anchor_absent_delta_min"]),
        "task_ids_disjoint": not overlap,
    }
    return raw_predictions(examples, indexes, scores, "confirmation"), {
        "phase": "confirmation",
        "tasks": len(tasks),
        "rows": len(examples),
        "anchor_rows": int(sum(item["anchor_present"] for item in examples)),
        "metrics": metrics,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "anchor_strata": strata,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
        "development_task_overlap": overlap,
        "confirmation_task_ids": tasks,
    }


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


def verify_manifest(
    manifest: dict[str, Any], config: dict[str, Any], config_path: Path, dataset_path: Path, phase: str
) -> None:
    expected_bucket = int(config["development_bucket"] if phase == "development" else config["confirmation_bucket"])
    checks = {
        "phase": phase,
        "repository_url": config["repository_url"],
        "repository_commit": config["repository_commit"],
        "checked_out_commit": config["repository_commit"],
        "bucket": expected_bucket,
        "bucket_modulus": config["bucket_modulus"],
        "dataset_sha256": sha256_path(dataset_path),
        "config_sha256": sha256_path(config_path),
    }
    for name, expected in checks.items():
        if manifest.get(name) != expected:
            raise ValueError(f"manifest mismatch: {name}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--input-manifest", type=Path, required=True)
    parser.add_argument("--base-module", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    started = time.perf_counter()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    manifest = json.loads(args.input_manifest.read_text(encoding="utf-8"))
    if sha256_path(args.base_module) != config["base_module_sha256"]:
        raise ValueError("base module SHA mismatch")
    verify_manifest(manifest, config, args.config, args.dataset, args.phase)
    base = load_module(args.base_module)
    rows = base.load_jsonl(args.dataset)
    examples, sources = prepare_examples(rows, base, int(config["fold_modulus"]))
    args.output_dir.mkdir(parents=True, exist_ok=False)
    if args.phase == "development":
        bundle, predictions, summary = fit_development(examples, config, base)
        model_path = args.output_dir / "model.joblib"
        joblib.dump(bundle, model_path)
        summary["model"] = {
            "path": str(model_path),
            "bytes": model_path.stat().st_size,
            "sha256": sha256_path(model_path),
        }
    else:
        if args.model is None:
            raise ValueError("Confirmation requires model")
        bundle = joblib.load(args.model)
        predictions, summary = score_confirmation(examples, config, base, bundle)
        summary["model"] = {
            "path": str(args.model),
            "bytes": args.model.stat().st_size,
            "sha256": sha256_path(args.model),
        }
    write_jsonl(args.output_dir / "raw_predictions.jsonl", predictions)
    write_jsonl(args.output_dir / "source_records.jsonl", sources)
    summary.update(
        {
            "schema_version": 1,
            "experiment_id": "v024",
            "config_sha256": sha256_path(args.config),
            "dataset_sha256": sha256_path(args.dataset),
            "input_manifest_sha256": sha256_path(args.input_manifest),
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
                "candidate_auc": summary["metrics"]["viaf"]["auc"],
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
