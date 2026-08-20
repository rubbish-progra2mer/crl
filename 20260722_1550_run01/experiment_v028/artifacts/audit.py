from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sentence_transformers import CrossEncoder
from sklearn.metrics import roc_auc_score


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


def split_identifier(value: str) -> str:
    value = CAMEL.sub(" ", value)
    return " ".join(part for part in re.split(r"[^A-Za-z0-9]+", value) if part).lower()


def scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def schema_lines(value: Any, path: tuple[str, ...] = ()) -> list[str]:
    records = []
    if isinstance(value, dict):
        for key in sorted(value):
            records.extend(schema_lines(value[key], path + (str(key),)))
    elif isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            records.append(f"{' '.join(split_identifier(part) for part in path)}: {' '.join(scalar(item) for item in value)}")
        else:
            for index, item in enumerate(value):
                records.extend(schema_lines(item, path + (str(index),)))
    else:
        records.append(f"{' '.join(split_identifier(part) for part in path)}: {scalar(value)}")
    return records


def views(tool: dict[str, Any]) -> dict[str, str]:
    operation = (
        f"tool name: {split_identifier(str(tool['name']))}. operation description: "
        f"{str(tool.get('description', ''))}"
    )
    arguments = "argument schema: " + ". ".join(schema_lines(tool.get("parameters", {})))
    return {"full": operation + ". " + arguments, "operation": operation, "arguments": arguments}


def query_text(row: dict[str, Any]) -> str:
    texts = [
        str(turn.get("content", ""))
        for group in row["question"]
        for turn in group
        if str(turn.get("role", "")) == "user"
    ]
    if not texts:
        raise ValueError(f"missing user query {row['id']}")
    return "\n".join(texts)


def gold_names(row: dict[str, Any]) -> list[str]:
    result = sorted({str(name) for call in row["ground_truth"] for name in call})
    if not result:
        raise ValueError(f"missing gold functions {row['id']}")
    return result


def query_fold(query_id: str, modulus: int) -> int:
    return hashlib.sha256(query_id.encode("utf-8")).digest()[1] % modulus


def prepare(
    expanded: list[dict[str, Any]], questions: list[dict[str, Any]], gold: list[dict[str, Any]], folds: int
) -> list[dict[str, Any]]:
    em = {str(row["id"]): row for row in expanded}
    qm = {str(row["id"]): row for row in questions}
    gm = {str(row["id"]): row for row in gold}
    if len(em) != len(expanded) or len(qm) != len(questions) or len(gm) != len(gold):
        raise ValueError("duplicate query IDs")
    if set(em) != set(qm) or set(em) != set(gm):
        raise ValueError("query ID sets differ")
    examples = []
    for query_id in sorted(em):
        if em[query_id]["question"] != qm[query_id]["question"]:
            raise ValueError(f"question mismatch {query_id}")
        text = query_text(em[query_id])
        tools = list(em[query_id]["function"])
        names = [str(tool["name"]) for tool in tools]
        gold_set = gold_names(gm[query_id])
        if len(names) != len(set(names)) or not set(gold_set).issubset(names):
            raise ValueError(f"tool/gold identity error {query_id}")
        examples.append(
            {
                "query_id": query_id,
                "query": text,
                "query_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "fold": query_fold(query_id, folds),
                "tools": tools,
                "tool_names": names,
                "gold_names": gold_set,
                "field_texts": [views(tool) for tool in tools],
            }
        )
    return examples


def verify_model(model_dir: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    observed = {path.relative_to(model_dir).as_posix(): path for path in model_dir.rglob("*") if path.is_file()}
    expected = config["cross_encoder_files"]
    if set(observed) != set(expected):
        raise ValueError("model file set mismatch")
    records = []
    for name in sorted(observed):
        digest = sha256_path(observed[name])
        if digest != expected[name]:
            raise ValueError(f"model SHA mismatch {name}")
        records.append({"relative_path": name, "bytes": observed[name].stat().st_size, "sha256": digest})
    return records


def cross_scores(
    examples: list[dict[str, Any]], model: CrossEncoder, config: dict[str, Any]
) -> tuple[list[np.ndarray], int]:
    fields = tuple(config["field_order"])
    pairs = []
    locations = []
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
    matrices = [np.zeros((len(example["tools"]), len(fields))) for example in examples]
    for value, location in zip(values, locations, strict=True):
        matrices[location[0]][location[1], location[2]] = float(value)
    return matrices, len(pairs)


def labels(example: dict[str, Any]) -> np.ndarray:
    gold = set(example["gold_names"])
    return np.asarray([int(name in gold) for name in example["tool_names"]], dtype=np.int64)


def expected_bundle_metadata(
    examples: list[dict[str, Any]], raw_features: list[np.ndarray], indexes: np.ndarray
) -> dict[str, Any]:
    tools = int(sum(len(examples[int(index)]["tools"]) for index in indexes))
    pairs = 0
    point_weights = []
    point_labels = []
    for index in indexes:
        target = labels(examples[int(index)])
        pair_count = int(np.sum(target == 1) * np.sum(target == 0))
        pairs += pair_count
        point_weights.extend([1.0 / len(target)] * len(target))
        point_labels.extend(target.tolist())
    point_weights_array = np.asarray(point_weights)
    point_labels_array = np.asarray(point_labels)
    weighted_counts = {
        value: float(np.sum(point_weights_array[point_labels_array == value])) for value in (0, 1)
    }
    class_weight = {value: len(indexes) / (2.0 * weighted_counts[value]) for value in (0, 1)}
    stacked = np.vstack([raw_features[int(index)] for index in indexes])
    mean = np.mean(stacked, axis=0)
    variance = np.var(stacked, axis=0)
    scale = np.sqrt(variance)
    scale[scale == 0.0] = 1.0
    return {
        "train_queries": len(indexes),
        "train_tools": tools,
        "train_gold_non_gold_pairs": pairs,
        "pointwise_class_weight": class_weight,
        "pair_sample_weight_sum": float(len(indexes)),
        "scaler_mean": mean,
        "scaler_scale": scale,
    }


def validate_bundle(
    bundle: dict[str, Any], examples: list[dict[str, Any]], raw_features: list[np.ndarray], indexes: np.ndarray
) -> list[str]:
    errors = []
    expected = expected_bundle_metadata(examples, raw_features, indexes)
    for name in ("train_queries", "train_tools", "train_gold_non_gold_pairs", "pointwise_class_weight", "pair_sample_weight_sum"):
        if maximum_error(bundle.get(name), expected[name]) > 1e-10:
            errors.append(f"bundle metadata mismatch {name}")
    if tuple(bundle.get("field_order", ())) != ("full", "operation", "arguments"):
        errors.append("bundle field order mismatch")
    if np.max(np.abs(bundle["scaler"].mean_ - expected["scaler_mean"])) > 1e-10:
        errors.append("bundle scaler mean mismatch")
    if np.max(np.abs(bundle["scaler"].scale_ - expected["scaler_scale"])) > 1e-10:
        errors.append("bundle scaler scale mismatch")
    if maximum_error(bundle["pointwise_fields"].class_weight, expected["pointwise_class_weight"]) > 1e-10:
        errors.append("pointwise class weight mismatch")
    return errors


def score_bundle(bundle: dict[str, Any], features: list[np.ndarray], indexes: np.ndarray) -> dict[int, dict[str, np.ndarray]]:
    scores = {}
    for index in indexes:
        raw = features[int(index)]
        scaled = bundle["scaler"].transform(raw)
        scores[int(index)] = {
            "full_cross_encoder": raw[:, 0],
            "equal_fields": np.mean(scaled, axis=1),
            "pointwise_fields": bundle["pointwise_fields"].decision_function(scaled),
            "pairwise_full": bundle["pairwise_full"].decision_function(scaled[:, :1]),
            "menu_relative_field_contrast": bundle["pairwise_fields"].decision_function(scaled),
        }
    return scores


def tie_hash(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def rank(example: dict[str, Any], scores: np.ndarray) -> list[int]:
    return sorted(range(len(scores)), key=lambda index: (-float(scores[index]), tie_hash(example["tool_names"][index])))


def record_metrics(examples: list[dict[str, Any]], scores: dict[int, dict[str, np.ndarray]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records = []
    for index, example in enumerate(examples):
        method_values = {}
        for method in METHODS:
            order = rank(example, scores[index][method])
            gold = set(example["gold_names"])
            first = next(position for position, tool_index in enumerate(order, 1) if example["tool_names"][tool_index] in gold)
            method_values[method] = {
                "ranking": [example["tool_names"][tool_index] for tool_index in order],
                "top1_correct": example["tool_names"][order[0]] in gold,
                "reciprocal_rank": 1.0 / first,
            }
        records.append(method_values)
    metric = {
        method: {
            "top1": float(np.mean([record[method]["top1_correct"] for record in records])),
            "mrr": float(np.mean([record[method]["reciprocal_rank"] for record in records])),
            "queries": len(records),
        }
        for method in METHODS
    }
    return records, metric


def bootstrap(records: list[dict[str, Any]], comparator: str, repeats: int, seed: int) -> dict[str, Any]:
    candidate = METHODS[-1]
    ct = np.asarray([record[candidate]["top1_correct"] for record in records], dtype=np.float64)
    bt = np.asarray([record[comparator]["top1_correct"] for record in records], dtype=np.float64)
    cm = np.asarray([record[candidate]["reciprocal_rank"] for record in records])
    bm = np.asarray([record[comparator]["reciprocal_rank"] for record in records])
    rng = np.random.default_rng(seed)
    top_samples = []
    mrr_samples = []
    for _ in range(repeats):
        indexes = rng.integers(0, len(records), size=len(records))
        top_samples.append(float(np.mean(ct[indexes] - bt[indexes])))
        mrr_samples.append(float(np.mean(cm[indexes] - bm[indexes])))
    return {
        "comparator": comparator,
        "top1_point": float(np.mean(ct - bt)),
        "top1_bootstrap_95": [float(np.quantile(top_samples, 0.025)), float(np.quantile(top_samples, 0.975))],
        "mrr_point": float(np.mean(cm - bm)),
        "mrr_bootstrap_95": [float(np.quantile(mrr_samples, 0.025)), float(np.quantile(mrr_samples, 0.975))],
        "repeats": repeats,
        "unit": "query_row",
    }


def changes(records: list[dict[str, Any]], comparator: str) -> dict[str, int]:
    return {
        "corrections": sum(record[METHODS[-1]]["top1_correct"] and not record[comparator]["top1_correct"] for record in records),
        "regressions": sum(record[comparator]["top1_correct"] and not record[METHODS[-1]]["top1_correct"] for record in records),
    }


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


def audit(args: argparse.Namespace) -> dict[str, Any]:
    config = read_json(args.config)
    summary = read_json(args.summary)
    raw = read_jsonl(args.raw)
    hashes = read_json(args.query_hashes)
    model_bundle = joblib.load(args.model)
    errors = []
    identity = (
        (sha256_path(args.candidate), config["candidate_sha256"], "Candidate SHA mismatch"),
        (sha256_path(args.evidence_packet), config["evidence_packet_sha256"], "Evidence Packet SHA mismatch"),
        (sha256_path(args.config), summary["config_sha256"], "config SHA mismatch"),
        (sha256_path(args.expanded), summary["expanded_sha256"], "expanded SHA mismatch"),
        (sha256_path(args.questions), summary["questions_sha256"], "questions SHA mismatch"),
        (sha256_path(args.gold), summary["gold_sha256"], "gold SHA mismatch"),
        (sha256_path(args.raw), summary["raw_sha256"], "raw SHA mismatch"),
        (sha256_path(args.query_hashes), summary["query_hashes_sha256"], "query hashes SHA mismatch"),
        (sha256_path(args.environment), summary["environment_sha256"], "environment SHA mismatch"),
        (sha256_path(args.model), summary["model"]["sha256"], "model SHA mismatch"),
    )
    for actual, expected, message in identity:
        if actual != expected:
            errors.append(message)
    model_files = verify_model(args.model_dir, config)
    if model_files != summary["model_files"]:
        errors.append("model file manifest mismatch")
    if tuple(model_bundle.get("methods", ())) != METHODS or tuple(model_bundle.get("field_order", ())) != tuple(config["field_order"]):
        errors.append("frozen model method/field identity mismatch")
    expected_model_identity = {
        "config_sha256": sha256_path(args.config),
        "candidate_sha256": config["candidate_sha256"],
        "evidence_packet_sha256": config["evidence_packet_sha256"],
    }
    if any(model_bundle.get(name) != value for name, value in expected_model_identity.items()):
        errors.append("frozen model identity mismatch")
    if int(summary["model"].get("bytes", -1)) != args.model.stat().st_size:
        errors.append("model byte count mismatch")
    if read_json(args.environment) != summary.get("environment"):
        errors.append("environment content mismatch")
    phase = str(summary["phase"])
    if phase == "development":
        observed = {
            "questions_sha256": sha256_path(args.questions),
            "expanded_sha256": sha256_path(args.expanded),
            "gold_sha256": sha256_path(args.gold),
        }
        if observed != config["development_inputs"]:
            errors.append("Development input set mismatch")
    else:
        if args.input_manifest is None:
            errors.append("Confirmation manifest missing")
        else:
            manifest = read_json(args.input_manifest)
            if (
                manifest.get("phase") != "confirmation"
                or manifest.get("config_sha256") != sha256_path(args.config)
                or manifest.get("questions_sha256") != sha256_path(args.questions)
                or manifest.get("gold_sha256") != sha256_path(args.gold)
            ):
                errors.append("Confirmation manifest mismatch")

    examples = prepare(
        read_jsonl(args.expanded), read_jsonl(args.questions), read_jsonl(args.gold), int(config["query_fold_modulus"])
    )
    if hashes != sorted(example["query_sha256"] for example in examples):
        errors.append("query hash content mismatch")
    cross_encoder = CrossEncoder(str(args.model_dir), device=str(config["device"]), local_files_only=True)
    feature_values, inference_pairs = cross_scores(examples, cross_encoder, config)
    if inference_pairs != int(summary["cross_encoder_pairs"]):
        errors.append("cross-encoder pair count mismatch")
    if len(raw) != len(examples):
        errors.append("raw query count mismatch")
    raw_map = {str(record["query_id"]): record for record in raw}
    if len(raw_map) != len(raw) or set(raw_map) != {example["query_id"] for example in examples}:
        errors.append("raw query ID set mismatch")

    scores: dict[int, dict[str, np.ndarray]] = {}
    if phase == "development":
        fold_bundles = {int(bundle["fold"]): bundle for bundle in model_bundle["fold_bundles"]}
        if set(fold_bundles) != set(range(int(config["query_fold_modulus"]))) or len(fold_bundles) != len(model_bundle["fold_bundles"]):
            errors.append("fold bundle set mismatch")
        fold_metadata = []
        for fold in range(int(config["query_fold_modulus"])):
            train = np.asarray([index for index, example in enumerate(examples) if example["fold"] != fold], dtype=np.int64)
            heldout = np.asarray([index for index, example in enumerate(examples) if example["fold"] == fold], dtype=np.int64)
            bundle = fold_bundles[fold]
            errors.extend(f"fold {fold}: {message}" for message in validate_bundle(bundle, examples, feature_values, train))
            heldout_ids = [examples[int(index)]["query_id"] for index in heldout]
            if bundle.get("heldout_query_ids") != heldout_ids:
                errors.append(f"fold {fold} heldout ID mismatch")
            scores.update(score_bundle(bundle, feature_values, heldout))
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
        full_indexes = np.arange(len(examples), dtype=np.int64)
        errors.extend(
            f"full bundle: {message}"
            for message in validate_bundle(model_bundle["full_bundle"], examples, feature_values, full_indexes)
        )
    else:
        overlap = sorted(
            set(example["query_sha256"] for example in examples) & set(model_bundle["development_query_hashes"])
        )
        if overlap:
            errors.append("Development/Confirmation query overlap")
        indexes = np.arange(len(examples), dtype=np.int64)
        scores.update(score_bundle(model_bundle["full_bundle"], feature_values, indexes))
        fold_metadata = []
    if set(scores) != set(range(len(examples))):
        errors.append("incomplete score replay")

    max_field_error = 0.0
    max_method_error = 0.0
    for index, example in enumerate(examples):
        record = raw_map.get(example["query_id"])
        if record is None:
            continue
        expected_identity = {
            "phase": "development_oof" if phase == "development" else "confirmation",
            "query_id": example["query_id"],
            "query": example["query"],
            "query_sha256": example["query_sha256"],
            "fold": example["fold"] if phase == "development" else None,
            "gold_names": example["gold_names"],
        }
        for name, value in expected_identity.items():
            if record.get(name) != value:
                errors.append(f"raw identity mismatch {example['query_id']}:{name}")
        tool_map = {str(tool["tool_name"]): tool for tool in record["tools"]}
        if len(tool_map) != len(record["tools"]) or set(tool_map) != set(example["tool_names"]):
            errors.append(f"raw tool set mismatch {example['query_id']}")
            continue
        for tool_index, tool_name in enumerate(example["tool_names"]):
            tool = tool_map[tool_name]
            if tool["field_texts"] != example["field_texts"][tool_index]:
                errors.append(f"field text mismatch {example['query_id']}:{tool_name}")
            for field_index, field in enumerate(config["field_order"]):
                max_field_error = max(
                    max_field_error,
                    abs(float(tool["field_scores"][field]) - float(feature_values[index][tool_index, field_index])),
                )
            for method in METHODS:
                max_method_error = max(
                    max_method_error,
                    abs(float(tool["method_scores"][method]) - float(scores[index][method][tool_index])),
                )
                order = rank(example, scores[index][method])
                expected_ranking = [example["tool_names"][tool_index] for tool_index in order]
                if record["methods"][method]["ranking"] != expected_ranking:
                    errors.append(f"ranking mismatch {example['query_id']}:{method}")
                gold = set(example["gold_names"])
                expected_top1 = expected_ranking[0] in gold
                expected_first = next(position for position, name in enumerate(expected_ranking, 1) if name in gold)
                if bool(record["methods"][method]["top1_correct"]) != expected_top1:
                    errors.append(f"raw top1 mismatch {example['query_id']}:{method}")
                if abs(float(record["methods"][method]["reciprocal_rank"]) - 1.0 / expected_first) > 1e-12:
                    errors.append(f"raw reciprocal-rank mismatch {example['query_id']}:{method}")
    if max_field_error > 1e-6:
        errors.append("cross-encoder field replay mismatch")
    if max_method_error > 1e-9:
        errors.append("frozen ranker score replay mismatch")

    record_values, metric = record_metrics(examples, scores)
    strongest = (
        max(COMPARATORS, key=lambda name: (metric[name]["top1"], metric[name]["mrr"], name))
        if phase == "development"
        else str(model_bundle["strongest_development_comparator"])
    )
    delta = bootstrap(record_values, strongest, int(config["bootstrap_repeats"]), int(config["seed"]))
    if phase == "development":
        vs_full = changes(record_values, "full_cross_encoder")
        fold_slices = {}
        for fold in range(int(config["query_fold_modulus"])):
            local_indexes = [index for index, example in enumerate(examples) if example["fold"] == fold]
            local_records = [record_values[index] for index in local_indexes]
            local_metric = {
                method: {
                    "mrr": float(np.mean([record[method]["reciprocal_rank"] for record in local_records]))
                }
                for method in METHODS
            }
            fold_slices[str(fold)] = {
                "queries": len(local_records),
                "candidate_mrr": local_metric[METHODS[-1]]["mrr"],
                "strongest_mrr": local_metric[strongest]["mrr"],
                "mrr_delta": local_metric[METHODS[-1]]["mrr"] - local_metric[strongest]["mrr"],
            }
        positive_folds = sum(value["mrr_delta"] > 0.0 for value in fold_slices.values())
        gate_config = config["development_gates"]
        candidate_metric = metric[METHODS[-1]]
        gates = {
            "candidate_top1": candidate_metric["top1"] >= float(gate_config["candidate_top1_min"]),
            "top1_delta_vs_full": candidate_metric["top1"] - metric["full_cross_encoder"]["top1"]
            >= float(gate_config["top1_delta_vs_full_min"]),
            "strictly_beats_every_comparator_top1": all(
                candidate_metric["top1"] > metric[name]["top1"] for name in COMPARATORS
            ),
            "mrr_bootstrap_lower_vs_strongest": delta["mrr_bootstrap_95"][0] > 0.0,
            "positive_net_corrections_vs_full": vs_full["corrections"] > vs_full["regressions"],
            "all_fold_mrr_deltas_nonnegative": all(value["mrr_delta"] >= 0.0 for value in fold_slices.values()),
            "minimum_positive_folds": positive_folds >= int(gate_config["minimum_positive_folds"]),
        }
        structure = {
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
        if model_bundle.get("strongest_development_comparator") != strongest:
            errors.append("frozen strongest comparator mismatch")
    else:
        change = changes(record_values, strongest)
        candidate_metric = metric[METHODS[-1]]
        gates = {
            "candidate_top1_above_frozen_strongest": candidate_metric["top1"] > metric[strongest]["top1"],
            "candidate_mrr_above_frozen_strongest": candidate_metric["mrr"] > metric[strongest]["mrr"],
            "top1_bootstrap_lower_nonnegative": delta["top1_bootstrap_95"][0] >= 0.0,
            "positive_net_corrections": change["corrections"] > change["regressions"],
            "strictly_beats_every_comparator_top1": all(
                candidate_metric["top1"] > metric[name]["top1"] for name in COMPARATORS
            ),
            "query_hashes_disjoint": True,
        }
        structure = {
            "metrics": metric,
            "strongest_comparator": strongest,
            "candidate_minus_strongest": delta,
            "corrections": change,
            "development_query_overlap": [],
            "gates": gates,
            "gates_passed": sum(gates.values()),
            "gates_total": len(gates),
        }
    max_metric_error = max(
        (maximum_error(value, summary.get(name)) for name, value in structure.items()), default=0.0
    )
    if max_metric_error > 1e-12:
        errors.append("metric, gate, fold, or structure mismatch")
    if int(summary.get("queries", -1)) != len(examples):
        errors.append("summary query count mismatch")
    if int(summary.get("tools", -1)) != sum(len(example["tools"]) for example in examples):
        errors.append("summary tool count mismatch")
    return {
        "schema_version": 1,
        "phase": phase,
        "status": "AUDIT_OK" if not errors else "AUDIT_ERROR",
        "errors": errors,
        "queries": len(examples),
        "tools": sum(len(example["tools"]) for example in examples),
        "cross_encoder_pairs_replayed": inference_pairs,
        "method_scores_replayed": sum(len(example["tools"]) for example in examples) * len(METHODS),
        "maximum_field_score_error": max_field_error,
        "maximum_method_score_error": max_method_error,
        "maximum_metric_error": max_metric_error,
        "config_sha256": sha256_path(args.config),
        "candidate_sha256": sha256_path(args.candidate),
        "evidence_packet_sha256": sha256_path(args.evidence_packet),
        "raw_sha256": sha256_path(args.raw),
        "summary_sha256": sha256_path(args.summary),
        "model_sha256": sha256_path(args.model),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--evidence-packet", type=Path, required=True)
    parser.add_argument("--expanded", type=Path, required=True)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--input-manifest", type=Path)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--query-hashes", type=Path, required=True)
    parser.add_argument("--environment", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
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
                "queries": report["queries"],
                "cross_encoder_pairs_replayed": report["cross_encoder_pairs_replayed"],
                "method_scores_replayed": report["method_scores_replayed"],
                "maximum_field_score_error": report["maximum_field_score_error"],
                "maximum_method_score_error": report["maximum_method_score_error"],
                "maximum_metric_error": report["maximum_metric_error"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "AUDIT_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
