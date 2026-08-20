from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import scipy
import sklearn
import torch
from sentence_transformers import CrossEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


METHODS = (
    "full_cross_encoder",
    "equal_fields",
    "pointwise_fields",
    "pairwise_full",
    "menu_relative_field_contrast",
)
COMPARATORS = METHODS[:-1]
CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


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


def split_identifier(value: str) -> str:
    value = CAMEL.sub(" ", value)
    return " ".join(part for part in re.split(r"[^A-Za-z0-9]+", value) if part).lower()


def scalar_text(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def flatten_schema(value: Any, path: tuple[str, ...] = ()) -> list[str]:
    records = []
    if isinstance(value, dict):
        for key in sorted(value):
            records.extend(flatten_schema(value[key], path + (str(key),)))
    elif isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            records.append(f"{' '.join(split_identifier(part) for part in path)}: {' '.join(scalar_text(item) for item in value)}")
        else:
            for index, item in enumerate(value):
                records.extend(flatten_schema(item, path + (str(index),)))
    else:
        records.append(f"{' '.join(split_identifier(part) for part in path)}: {scalar_text(value)}")
    return records


def field_texts(tool: dict[str, Any]) -> dict[str, str]:
    name = str(tool["name"])
    description = str(tool.get("description", ""))
    operation = f"tool name: {split_identifier(name)}. operation description: {description}"
    arguments = "argument schema: " + ". ".join(flatten_schema(tool.get("parameters", {})))
    return {
        "full": operation + ". " + arguments,
        "operation": operation,
        "arguments": arguments,
    }


def query_text(row: dict[str, Any]) -> str:
    texts = []
    for turn_group in row["question"]:
        for turn in turn_group:
            if str(turn.get("role", "")) == "user":
                texts.append(str(turn.get("content", "")))
    if not texts:
        raise ValueError(f"query has no user text: {row['id']}")
    return "\n".join(texts)


def gold_names(row: dict[str, Any]) -> list[str]:
    names = sorted({str(name) for call in row["ground_truth"] for name in call})
    if not names:
        raise ValueError(f"query has no gold function: {row['id']}")
    return names


def fold_for_query(query_id: str, modulus: int) -> int:
    return hashlib.sha256(query_id.encode("utf-8")).digest()[1] % modulus


def prepare_examples(
    expanded: list[dict[str, Any]], questions: list[dict[str, Any]], gold: list[dict[str, Any]], folds: int
) -> list[dict[str, Any]]:
    expanded_map = {str(row["id"]): row for row in expanded}
    question_map = {str(row["id"]): row for row in questions}
    gold_map = {str(row["id"]): row for row in gold}
    if len(expanded_map) != len(expanded) or len(question_map) != len(questions) or len(gold_map) != len(gold):
        raise ValueError("duplicate query IDs")
    if set(expanded_map) != set(question_map) or set(expanded_map) != set(gold_map):
        raise ValueError("input query ID sets differ")
    examples = []
    for query_id in sorted(expanded_map):
        expanded_row = expanded_map[query_id]
        question_row = question_map[query_id]
        if expanded_row["question"] != question_row["question"]:
            raise ValueError(f"question bytes differ for {query_id}")
        text = query_text(expanded_row)
        tools = list(expanded_row["function"])
        names = [str(tool["name"]) for tool in tools]
        if len(names) != len(set(names)):
            raise ValueError(f"duplicate tool names in {query_id}")
        gold_set = gold_names(gold_map[query_id])
        if not set(gold_set).issubset(names):
            raise ValueError(f"gold function absent from expanded menu {query_id}")
        examples.append(
            {
                "query_id": query_id,
                "query": text,
                "query_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "fold": fold_for_query(query_id, folds),
                "tools": tools,
                "tool_names": names,
                "gold_names": gold_set,
                "field_texts": [field_texts(tool) for tool in tools],
            }
        )
    return examples


def verify_model(model_dir: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    expected = config["cross_encoder_files"]
    observed = {path.relative_to(model_dir).as_posix(): path for path in model_dir.rglob("*") if path.is_file()}
    if set(observed) != set(expected):
        raise ValueError("cross-encoder file set mismatch")
    for relative_path in sorted(observed):
        path = observed[relative_path]
        digest = sha256_path(path)
        if digest != expected[relative_path]:
            raise ValueError(f"cross-encoder file SHA mismatch: {relative_path}")
        records.append({"relative_path": relative_path, "bytes": path.stat().st_size, "sha256": digest})
    return records


def score_fields(
    examples: list[dict[str, Any]], model: CrossEncoder, config: dict[str, Any]
) -> tuple[list[np.ndarray], int]:
    pairs = []
    locations = []
    fields = tuple(config["field_order"])
    for example_index, example in enumerate(examples):
        for tool_index, texts in enumerate(example["field_texts"]):
            for field_index, field in enumerate(fields):
                pairs.append((example["query"], texts[field]))
                locations.append((example_index, tool_index, field_index))
    values = np.asarray(
        model.predict(
            pairs,
            batch_size=int(config["cross_encoder_batch_size"]),
            show_progress_bar=False,
            convert_to_numpy=True,
        ),
        dtype=np.float64,
    ).reshape(-1)
    matrices = [np.zeros((len(example["tools"]), len(fields)), dtype=np.float64) for example in examples]
    for value, (example_index, tool_index, field_index) in zip(values, locations, strict=True):
        matrices[example_index][tool_index, field_index] = float(value)
    return matrices, len(pairs)


def tool_labels(example: dict[str, Any]) -> np.ndarray:
    gold = set(example["gold_names"])
    return np.asarray([int(name in gold) for name in example["tool_names"]], dtype=np.int64)


def pair_training(
    examples: list[dict[str, Any]], features: list[np.ndarray], indexes: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    differences = []
    labels = []
    weights = []
    pair_count = 0
    for index in indexes:
        matrix = features[int(index)]
        target = tool_labels(examples[int(index)])
        positives = np.flatnonzero(target == 1)
        negatives = np.flatnonzero(target == 0)
        pairs = [(int(pos), int(neg)) for pos in positives for neg in negatives]
        if not pairs:
            raise ValueError(f"query lacks gold/non-gold pair {examples[int(index)]['query_id']}")
        pair_count += len(pairs)
        weight = 0.5 / len(pairs)
        for positive, negative in pairs:
            difference = matrix[positive] - matrix[negative]
            differences.extend((difference, -difference))
            labels.extend((1, 0))
            weights.extend((weight, weight))
    return (
        np.asarray(differences, dtype=np.float64),
        np.asarray(labels, dtype=np.int64),
        np.asarray(weights, dtype=np.float64),
        pair_count,
    )


def classifier(config: dict[str, Any], *, intercept: bool, class_weight: Any = None) -> LogisticRegression:
    return LogisticRegression(
        C=float(config["logistic_c"]),
        max_iter=int(config["logistic_max_iter"]),
        solver="liblinear",
        fit_intercept=intercept,
        class_weight=class_weight,
        random_state=int(config["seed"]),
    )


def fit_bundle(
    examples: list[dict[str, Any]], raw_features: list[np.ndarray], train: np.ndarray, config: dict[str, Any]
) -> dict[str, Any]:
    scaler = StandardScaler().fit(np.vstack([raw_features[int(index)] for index in train]))
    scaled = [scaler.transform(matrix) for matrix in raw_features]
    pair_x, pair_y, pair_weight, pair_count = pair_training(examples, scaled, train)
    pairwise_fields = classifier(config, intercept=False).fit(pair_x, pair_y, sample_weight=pair_weight)
    full_x, full_y, full_weight, _ = pair_training(
        examples, [matrix[:, :1] for matrix in scaled], train
    )
    pairwise_full = classifier(config, intercept=False).fit(
        full_x, full_y, sample_weight=full_weight
    )

    point_x = np.vstack([scaled[int(index)] for index in train])
    point_y = np.concatenate([tool_labels(examples[int(index)]) for index in train])
    point_weight = np.concatenate(
        [np.full(len(examples[int(index)]["tools"]), 1.0 / len(examples[int(index)]["tools"])) for index in train]
    )
    weighted_counts = {value: float(np.sum(point_weight[point_y == value])) for value in (0, 1)}
    class_weight = {value: len(train) / (2.0 * weighted_counts[value]) for value in (0, 1)}
    pointwise = classifier(config, intercept=True, class_weight=class_weight).fit(
        point_x, point_y, sample_weight=point_weight
    )
    return {
        "scaler": scaler,
        "pairwise_fields": pairwise_fields,
        "pairwise_full": pairwise_full,
        "pointwise_fields": pointwise,
        "train_queries": len(train),
        "train_tools": int(sum(len(examples[int(index)]["tools"]) for index in train)),
        "train_gold_non_gold_pairs": pair_count,
        "pointwise_class_weight": class_weight,
        "pair_sample_weight_sum": float(np.sum(pair_weight)),
        "field_order": tuple(config["field_order"]),
    }


def score_bundle(bundle: dict[str, Any], raw_features: list[np.ndarray], indexes: np.ndarray) -> dict[int, dict[str, np.ndarray]]:
    result = {}
    for index in indexes:
        matrix = raw_features[int(index)]
        scaled = bundle["scaler"].transform(matrix)
        result[int(index)] = {
            "full_cross_encoder": matrix[:, 0].copy(),
            "equal_fields": np.mean(scaled, axis=1),
            "pointwise_fields": bundle["pointwise_fields"].decision_function(scaled),
            "pairwise_full": bundle["pairwise_full"].decision_function(scaled[:, :1]),
            "menu_relative_field_contrast": bundle["pairwise_fields"].decision_function(scaled),
        }
    return result


def tie_digest(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def ranking(example: dict[str, Any], scores: np.ndarray) -> list[int]:
    return sorted(range(len(scores)), key=lambda index: (-float(scores[index]), tie_digest(example["tool_names"][index])))


def query_records(
    examples: list[dict[str, Any]], raw_features: list[np.ndarray], scores: dict[int, dict[str, np.ndarray]], phase: str
) -> list[dict[str, Any]]:
    records = []
    for index, example in enumerate(examples):
        methods = {}
        for method in METHODS:
            order = ranking(example, scores[index][method])
            gold = set(example["gold_names"])
            first_gold = next(position for position, tool_index in enumerate(order, 1) if example["tool_names"][tool_index] in gold)
            methods[method] = {
                "ranking": [example["tool_names"][tool_index] for tool_index in order],
                "top1_correct": example["tool_names"][order[0]] in gold,
                "reciprocal_rank": 1.0 / first_gold,
            }
        tools = []
        for tool_index, tool_name in enumerate(example["tool_names"]):
            tools.append(
                {
                    "tool_name": tool_name,
                    "is_gold": tool_name in set(example["gold_names"]),
                    "field_texts": example["field_texts"][tool_index],
                    "field_scores": {
                        name: float(raw_features[index][tool_index, field_index])
                        for field_index, name in enumerate(("full", "operation", "arguments"))
                    },
                    "method_scores": {method: float(scores[index][method][tool_index]) for method in METHODS},
                }
            )
        records.append(
            {
                "phase": phase,
                "query_id": example["query_id"],
                "query": example["query"],
                "query_sha256": example["query_sha256"],
                "fold": example["fold"] if phase == "development_oof" else None,
                "gold_names": example["gold_names"],
                "methods": methods,
                "tools": tools,
            }
        )
    return records


def metrics(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    return {
        method: {
            "top1": float(np.mean([record["methods"][method]["top1_correct"] for record in records])),
            "mrr": float(np.mean([record["methods"][method]["reciprocal_rank"] for record in records])),
            "queries": len(records),
        }
        for method in METHODS
    }


def bootstrap(
    records: list[dict[str, Any]], candidate: str, comparator: str, repeats: int, seed: int
) -> dict[str, Any]:
    top_candidate = np.asarray([record["methods"][candidate]["top1_correct"] for record in records], dtype=np.float64)
    top_comparator = np.asarray([record["methods"][comparator]["top1_correct"] for record in records], dtype=np.float64)
    mrr_candidate = np.asarray([record["methods"][candidate]["reciprocal_rank"] for record in records])
    mrr_comparator = np.asarray([record["methods"][comparator]["reciprocal_rank"] for record in records])
    rng = np.random.default_rng(seed)
    top_samples = []
    mrr_samples = []
    for _ in range(repeats):
        indexes = rng.integers(0, len(records), size=len(records))
        top_samples.append(float(np.mean(top_candidate[indexes] - top_comparator[indexes])))
        mrr_samples.append(float(np.mean(mrr_candidate[indexes] - mrr_comparator[indexes])))
    return {
        "comparator": comparator,
        "top1_point": float(np.mean(top_candidate - top_comparator)),
        "top1_bootstrap_95": [float(np.quantile(top_samples, 0.025)), float(np.quantile(top_samples, 0.975))],
        "mrr_point": float(np.mean(mrr_candidate - mrr_comparator)),
        "mrr_bootstrap_95": [float(np.quantile(mrr_samples, 0.025)), float(np.quantile(mrr_samples, 0.975))],
        "repeats": repeats,
        "unit": "query_row",
    }


def corrections(records: list[dict[str, Any]], candidate: str, comparator: str) -> dict[str, int]:
    candidate_values = [bool(record["methods"][candidate]["top1_correct"]) for record in records]
    comparator_values = [bool(record["methods"][comparator]["top1_correct"]) for record in records]
    return {
        "corrections": sum(c and not b for c, b in zip(candidate_values, comparator_values, strict=True)),
        "regressions": sum(b and not c for c, b in zip(candidate_values, comparator_values, strict=True)),
    }


def development(
    examples: list[dict[str, Any]], raw_features: list[np.ndarray], config: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    folds = int(config["query_fold_modulus"])
    scores: dict[int, dict[str, np.ndarray]] = {}
    fold_bundles = []
    fold_metadata = []
    for fold in range(folds):
        train = np.asarray([index for index, example in enumerate(examples) if example["fold"] != fold], dtype=np.int64)
        heldout = np.asarray([index for index, example in enumerate(examples) if example["fold"] == fold], dtype=np.int64)
        bundle = fit_bundle(examples, raw_features, train, config)
        scores.update(score_bundle(bundle, raw_features, heldout))
        bundle["fold"] = fold
        bundle["heldout_query_ids"] = [examples[int(index)]["query_id"] for index in heldout]
        fold_bundles.append(bundle)
        fold_metadata.append(
            {
                "fold": fold,
                "train_queries": len(train),
                "heldout_queries": len(heldout),
                "train_tools": bundle["train_tools"],
                "train_gold_non_gold_pairs": bundle["train_gold_non_gold_pairs"],
                "pair_sample_weight_sum": bundle["pair_sample_weight_sum"],
            }
        )
    if set(scores) != set(range(len(examples))):
        raise ValueError("not every Development query received one OOF score")
    records = query_records(examples, raw_features, scores, "development_oof")
    metric = metrics(records)
    strongest = max(COMPARATORS, key=lambda name: (metric[name]["top1"], metric[name]["mrr"], name))
    delta = bootstrap(records, METHODS[-1], strongest, int(config["bootstrap_repeats"]), int(config["seed"]))
    vs_full = corrections(records, METHODS[-1], "full_cross_encoder")
    fold_slices = {}
    for fold in range(folds):
        subset = [record for record in records if int(record["fold"]) == fold]
        subset_metrics = metrics(subset)
        fold_slices[str(fold)] = {
            "queries": len(subset),
            "candidate_mrr": subset_metrics[METHODS[-1]]["mrr"],
            "strongest_mrr": subset_metrics[strongest]["mrr"],
            "mrr_delta": subset_metrics[METHODS[-1]]["mrr"] - subset_metrics[strongest]["mrr"],
        }
    positive_folds = sum(value["mrr_delta"] > 0.0 for value in fold_slices.values())
    gate_config = config["development_gates"]
    candidate = metric[METHODS[-1]]
    gates = {
        "candidate_top1": candidate["top1"] >= float(gate_config["candidate_top1_min"]),
        "top1_delta_vs_full": candidate["top1"] - metric["full_cross_encoder"]["top1"]
        >= float(gate_config["top1_delta_vs_full_min"]),
        "strictly_beats_every_comparator_top1": all(candidate["top1"] > metric[name]["top1"] for name in COMPARATORS),
        "mrr_bootstrap_lower_vs_strongest": delta["mrr_bootstrap_95"][0] > 0.0,
        "positive_net_corrections_vs_full": vs_full["corrections"] > vs_full["regressions"],
        "all_fold_mrr_deltas_nonnegative": all(value["mrr_delta"] >= 0.0 for value in fold_slices.values()),
        "minimum_positive_folds": positive_folds >= int(gate_config["minimum_positive_folds"]),
    }
    full_indexes = np.arange(len(examples), dtype=np.int64)
    full_bundle = fit_bundle(examples, raw_features, full_indexes, config)
    model_bundle = {
        "schema_version": 1,
        "experiment_id": "v028",
        "field_order": tuple(config["field_order"]),
        "fold_bundles": fold_bundles,
        "full_bundle": full_bundle,
        "strongest_development_comparator": strongest,
        "development_query_hashes": sorted(example["query_sha256"] for example in examples),
        "development_query_ids": sorted(example["query_id"] for example in examples),
        "methods": METHODS,
    }
    summary = {
        "phase": "development",
        "evaluation": "five_fold_query_oof",
        "queries": len(examples),
        "tools": sum(len(example["tools"]) for example in examples),
        "folds": fold_metadata,
        "metrics": metric,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "candidate_vs_full_corrections": vs_full,
        "fold_slices": fold_slices,
        "positive_folds": positive_folds,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
    }
    return model_bundle, records, summary


def confirmation(
    examples: list[dict[str, Any]], raw_features: list[np.ndarray], model_bundle: dict[str, Any], config: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    overlap = sorted(set(example["query_sha256"] for example in examples) & set(model_bundle["development_query_hashes"]))
    if overlap:
        raise ValueError("Development/Confirmation normalized-query hash overlap")
    indexes = np.arange(len(examples), dtype=np.int64)
    scores = score_bundle(model_bundle["full_bundle"], raw_features, indexes)
    records = query_records(examples, raw_features, scores, "confirmation")
    metric = metrics(records)
    strongest = str(model_bundle["strongest_development_comparator"])
    delta = bootstrap(records, METHODS[-1], strongest, int(config["bootstrap_repeats"]), int(config["seed"]))
    changes = corrections(records, METHODS[-1], strongest)
    candidate = metric[METHODS[-1]]
    gates = {
        "candidate_top1_above_frozen_strongest": candidate["top1"] > metric[strongest]["top1"],
        "candidate_mrr_above_frozen_strongest": candidate["mrr"] > metric[strongest]["mrr"],
        "top1_bootstrap_lower_nonnegative": delta["top1_bootstrap_95"][0] >= 0.0,
        "positive_net_corrections": changes["corrections"] > changes["regressions"],
        "strictly_beats_every_comparator_top1": all(candidate["top1"] > metric[name]["top1"] for name in COMPARATORS),
        "query_hashes_disjoint": True,
    }
    summary = {
        "phase": "confirmation",
        "evaluation": "frozen_full_development_bundle",
        "queries": len(examples),
        "tools": sum(len(example["tools"]) for example in examples),
        "metrics": metric,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "corrections": changes,
        "development_query_overlap": overlap,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
    }
    return records, summary


def environment(elapsed: float) -> dict[str, Any]:
    return {
        "python_executable": sys.executable,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": "cuda",
        "elapsed_seconds": elapsed,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--evidence-packet", type=Path, required=True)
    parser.add_argument("--expanded", type=Path, required=True)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--input-manifest", type=Path)
    parser.add_argument("--development-model", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    started = time.perf_counter()
    config = read_json(args.config)
    config_sha256 = sha256_path(args.config)
    if sha256_path(args.candidate) != config["candidate_sha256"]:
        raise ValueError("Candidate SHA mismatch")
    if sha256_path(args.evidence_packet) != config["evidence_packet_sha256"]:
        raise ValueError("Evidence Packet SHA mismatch")
    if args.phase == "development":
        expected = config["development_inputs"]
        observed = {
            "questions_sha256": sha256_path(args.questions),
            "expanded_sha256": sha256_path(args.expanded),
            "gold_sha256": sha256_path(args.gold),
        }
        if observed != expected:
            raise ValueError("Development input SHA mismatch")
    else:
        if args.input_manifest is None or args.development_model is None:
            raise ValueError("Confirmation requires manifest and Development model")
        manifest = read_json(args.input_manifest)
        if manifest["phase"] != "confirmation" or manifest["config_sha256"] != sha256_path(args.config):
            raise ValueError("Confirmation manifest identity mismatch")
        if manifest["questions_sha256"] != sha256_path(args.questions) or manifest["gold_sha256"] != sha256_path(args.gold):
            raise ValueError("Confirmation manifest data SHA mismatch")
    model_files = verify_model(args.model_dir, config)
    expanded = read_jsonl(args.expanded)
    questions = read_jsonl(args.questions)
    gold = read_jsonl(args.gold)
    examples = prepare_examples(expanded, questions, gold, int(config["query_fold_modulus"]))
    cross_encoder = CrossEncoder(str(args.model_dir), device=str(config["device"]), local_files_only=True)
    raw_features, inference_pairs = score_fields(examples, cross_encoder, config)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    if args.phase == "development":
        model_bundle, records, summary = development(examples, raw_features, config)
        model_bundle.update(
            {
                "config_sha256": config_sha256,
                "candidate_sha256": config["candidate_sha256"],
                "evidence_packet_sha256": config["evidence_packet_sha256"],
            }
        )
        model_path = args.output_dir / "model.joblib"
        joblib.dump(model_bundle, model_path)
    else:
        model_path = args.development_model
        model_bundle = joblib.load(model_path)
        expected_model_identity = {
            "config_sha256": config_sha256,
            "candidate_sha256": config["candidate_sha256"],
            "evidence_packet_sha256": config["evidence_packet_sha256"],
        }
        if any(model_bundle.get(name) != value for name, value in expected_model_identity.items()):
            raise ValueError("frozen Development model identity mismatch")
        if tuple(model_bundle.get("methods", ())) != METHODS or tuple(model_bundle.get("field_order", ())) != tuple(config["field_order"]):
            raise ValueError("frozen Development model method/field identity mismatch")
        records, summary = confirmation(examples, raw_features, model_bundle, config)
    write_jsonl(args.output_dir / "raw.jsonl", records)
    write_json(args.output_dir / "query_hashes.json", sorted(example["query_sha256"] for example in examples))
    env = environment(time.perf_counter() - started)
    write_json(args.output_dir / "environment.json", env)
    summary.update(
        {
            "schema_version": 1,
            "experiment_id": "v028",
            "config_sha256": config_sha256,
            "candidate_sha256": sha256_path(args.candidate),
            "evidence_packet_sha256": sha256_path(args.evidence_packet),
            "expanded_sha256": sha256_path(args.expanded),
            "questions_sha256": sha256_path(args.questions),
            "gold_sha256": sha256_path(args.gold),
            "model_files": model_files,
            "cross_encoder_pairs": inference_pairs,
            "raw_sha256": sha256_path(args.output_dir / "raw.jsonl"),
            "query_hashes_sha256": sha256_path(args.output_dir / "query_hashes.json"),
            "environment_sha256": sha256_path(args.output_dir / "environment.json"),
            "model": {"path": str(model_path), "bytes": model_path.stat().st_size, "sha256": sha256_path(model_path)},
            "environment": env,
        }
    )
    write_json(args.output_dir / "summary.json", summary)
    print(
        json.dumps(
            {
                "phase": args.phase,
                "candidate_top1": summary["metrics"][METHODS[-1]]["top1"],
                "strongest_comparator": summary["strongest_comparator"],
                "top1_delta": summary["candidate_minus_strongest"]["top1_point"],
                "gates": f"{summary['gates_passed']}/{summary['gates_total']}",
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
