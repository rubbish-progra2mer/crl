from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linear_sum_assignment
import sentence_transformers
from sentence_transformers import CrossEncoder, SentenceTransformer
import torch
import transformers


TOKEN_RE = re.compile(r"[a-z0-9_]+")
NUMBER_RE = re.compile(
    r"(?<![\w.])[+-]?\d+(?:[,.]\d+)*(?:\s*(?:%|degrees?|days?|weeks?|months?|years?|hours?|minutes?|seconds?|km|miles?|meters?|feet|inches?|kg|lbs?))?",
    re.IGNORECASE,
)
DATE_RE = re.compile(
    r"\b(?:today|tomorrow|yesterday|tonight|next\s+(?:day|week|month|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday)|last\s+(?:day|week|month|year)|upcoming\s+\d+\s+days?|(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(?:,\s*\d{4})?|\d{1,2}:\d{2}(?:\s*[ap]m)?)\b",
    re.IGNORECASE,
)
BOOL_RE = re.compile(r"\b(?:true|false|yes|no|enabled|disabled)\b", re.IGNORECASE)
ENTITY_RE = re.compile(
    r"\b[A-Z][A-Za-z0-9_.-]*(?:\s+(?:[A-Z][A-Za-z0-9_.-]*|of|the|and|for|in)){0,4}\b"
)
ENTITY_STOP = {
    "can i",
    "could i",
    "do i",
    "find",
    "give",
    "how",
    "i",
    "please",
    "show",
    "tell",
    "what",
    "when",
    "where",
    "which",
    "who",
    "would i",
}
DATE_WORDS = {
    "date",
    "day",
    "month",
    "time",
    "timestamp",
    "week",
    "year",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def question_text(row: dict[str, object]) -> str:
    turns = row["question"]
    return "\n".join(
        str(message["content"])
        for group in turns
        for message in group
        if message.get("role") == "user"
    )


def gold_names(row: dict[str, object]) -> tuple[str, ...]:
    names = {name for call in row["ground_truth"] for name in call}
    return tuple(sorted(names))


def normalize_text(text: str) -> str:
    return " ".join(TOKEN_RE.findall(text.lower()))


def tool_parameter_schema(tool: dict[str, object]) -> tuple[dict[str, dict[str, object]], list[str]]:
    parameters = tool.get("parameters") or {}
    properties = dict(parameters.get("properties") or {})
    required = [str(name) for name in parameters.get("required") or []]
    embedded_required = properties.pop("required", None)
    if embedded_required is not None:
        if required or not isinstance(embedded_required, list):
            raise ValueError(f"Ambiguous embedded required schema for {tool['name']}")
        required = [str(name) for name in embedded_required]
        for name in required:
            if name in properties:
                continue
            matches = [
                value[name]
                for value in properties.values()
                if isinstance(value, dict) and isinstance(value.get(name), dict)
            ]
            if len(matches) != 1:
                raise ValueError(f"Cannot resolve embedded required parameter {name} for {tool['name']}")
            properties[name] = matches[0]
    if any(not isinstance(value, dict) for value in properties.values()):
        raise ValueError(f"Non-object parameter schema for {tool['name']}")
    return properties, required


def schema_text(tool: dict[str, object]) -> str:
    properties, required_names = tool_parameter_schema(tool)
    required = set(required_names)
    fields = [f"function name: {tool['name']}", f"function description: {tool.get('description', '')}"]
    for name in sorted(properties):
        value = properties[name]
        fields.append(
            "parameter: "
            + json.dumps(
                {
                    "name": name,
                    "required": name in required,
                    "type": value.get("type", ""),
                    "description": value.get("description", ""),
                    "enum": value.get("enum", []),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return "\n".join(fields)


def required_parameters(tool: dict[str, object]) -> list[dict[str, object]]:
    properties, required = tool_parameter_schema(tool)
    records = []
    for name in required:
        value = properties[name]
        records.append(
            {
                "name": name,
                "type": value.get("type", ""),
                "description": value.get("description", ""),
                "enum": value.get("enum", []),
                "text": f"{name}: {value.get('description', '')}",
            }
        )
    return records


def span_type(text: str) -> str:
    normalized = normalize_text(text)
    if BOOL_RE.fullmatch(text.strip()):
        return "boolean"
    if DATE_RE.search(text) or DATE_WORDS.intersection(normalized.split()):
        return "date_time"
    if NUMBER_RE.fullmatch(text.strip()):
        return "number"
    return "text"


def parameter_type(parameter: dict[str, object]) -> str:
    words = set(normalize_text(f"{parameter['name']} {parameter['description']}").split())
    if DATE_WORDS.intersection(words):
        return "date_time"
    kind = str(parameter["type"]).lower()
    if kind in {"integer", "float", "number"}:
        return "number"
    if kind in {"boolean", "bool"}:
        return "boolean"
    return "text"


def extract_spans(query: str) -> list[dict[str, object]]:
    found: list[tuple[int, int, str, str]] = []
    for source, pattern in (
        ("quoted", re.compile(r'"([^"\r\n]{1,100})"')),
        ("date_time", DATE_RE),
        ("number", NUMBER_RE),
        ("boolean", BOOL_RE),
        ("entity", ENTITY_RE),
    ):
        for match in pattern.finditer(query):
            text = match.group(1) if source == "quoted" else match.group(0)
            start = match.start(1) if source == "quoted" else match.start()
            end = match.end(1) if source == "quoted" else match.end()
            normalized = normalize_text(text)
            if normalized and normalized not in ENTITY_STOP and len(normalized.split()) <= 8:
                found.append((start, end, text.strip(), source))
    found.sort(key=lambda item: (item[0], -(item[1] - item[0]), item[2].lower()))
    spans = []
    seen = set()
    for start, end, text, source in found:
        key = normalize_text(text)
        if key in seen:
            continue
        seen.add(key)
        spans.append(
            {
                "text": text,
                "normalized": key,
                "type": span_type(text),
                "source": source,
                "start": start,
                "end": end,
            }
        )
    return spans


def type_compatibility(span_kind: str, parameter_kind: str) -> float:
    if span_kind == parameter_kind:
        return 1.0
    if {span_kind, parameter_kind} == {"date_time", "text"}:
        return 0.25
    return -1.0


def zscores(values: np.ndarray) -> np.ndarray:
    std = float(values.std())
    if std == 0.0:
        return np.zeros_like(values)
    return (values - float(values.mean())) / std


def bm25_scores(query: str, documents: list[str]) -> np.ndarray:
    tokenized = [TOKEN_RE.findall(document.lower()) for document in documents]
    query_tokens = TOKEN_RE.findall(query.lower())
    n = len(tokenized)
    average_length = sum(map(len, tokenized)) / n
    document_frequency = Counter()
    for tokens in tokenized:
        document_frequency.update(set(tokens))
    scores = []
    for tokens in tokenized:
        counts = Counter(tokens)
        length_norm = 1.2 * (1.0 - 0.75 + 0.75 * len(tokens) / average_length)
        score = 0.0
        for term in query_tokens:
            frequency = counts[term]
            if not frequency:
                continue
            inverse_frequency = math.log(1.0 + (n - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5))
            score += inverse_frequency * frequency * 2.2 / (frequency + length_norm)
        scores.append(score)
    return np.asarray(scores, dtype=np.float64)


def edge_features(
    spans: list[dict[str, object]],
    parameters: list[dict[str, object]],
    span_vectors: np.ndarray,
    parameter_vectors: np.ndarray,
) -> list[list[dict[str, object]]]:
    matrix = []
    for span_index, span in enumerate(spans):
        row = []
        for parameter_index, parameter in enumerate(parameters):
            enum_values = [normalize_text(str(value)) for value in parameter["enum"]]
            enum_exact = bool(span["normalized"] in enum_values)
            row.append(
                {
                    "cosine": float(span_vectors[span_index] @ parameter_vectors[parameter_index]),
                    "type_compatibility": type_compatibility(str(span["type"]), parameter_type(parameter)),
                    "enum_exact": enum_exact,
                }
            )
        matrix.append(row)
    return matrix


def alignment_score(
    edges: list[list[dict[str, object]]],
    span_count: int,
    parameter_count: int,
    *,
    type_bonus: float,
    enum_bonus: float,
    null_threshold: float,
    unmatched_penalty: float,
    relaxed: bool,
) -> tuple[float, list[dict[str, object]], list[list[float]], list[list[float]]]:
    if parameter_count == 0:
        return 0.0, [], [], []
    if span_count == 0:
        return -unmatched_penalty, [], [], []
    edge_scores = np.asarray(
        [
            [
                edge["cosine"]
                + type_bonus * edge["type_compatibility"]
                + enum_bonus * float(edge["enum_exact"])
                for edge in row
            ]
            for row in edges
        ],
        dtype=np.float64,
    )
    threshold_margins = edge_scores - null_threshold
    assignments: list[dict[str, object]] = []
    if relaxed:
        matched_parameters = set()
        mass = 0.0
        for span_index in range(span_count):
            parameter_index = int(threshold_margins[span_index].argmax())
            margin = float(threshold_margins[span_index, parameter_index])
            if margin > 0.0:
                value = float(edge_scores[span_index, parameter_index])
                matched_parameters.add(parameter_index)
                mass += value
                assignments.append(
                    {"span": span_index, "parameter": parameter_index, "edge_score": value, "threshold_margin": margin}
                )
    else:
        augmented = np.concatenate(
            [threshold_margins, np.zeros((span_count, span_count), dtype=np.float64)], axis=1
        )
        row_indices, column_indices = linear_sum_assignment(-augmented)
        matched_parameters = set()
        mass = 0.0
        for span_index, parameter_index in zip(row_indices.tolist(), column_indices.tolist()):
            if parameter_index < parameter_count and threshold_margins[span_index, parameter_index] > 0.0:
                value = float(edge_scores[span_index, parameter_index])
                margin = float(threshold_margins[span_index, parameter_index])
                matched_parameters.add(parameter_index)
                mass += value
                assignments.append(
                    {"span": span_index, "parameter": parameter_index, "edge_score": value, "threshold_margin": margin}
                )
    unmatched_fraction = (parameter_count - len(matched_parameters)) / parameter_count
    score = mass / parameter_count - unmatched_penalty * unmatched_fraction
    return float(score), assignments, edge_scores.tolist(), threshold_margins.tolist()


def rank(names: list[str], scores: np.ndarray) -> list[str]:
    return [
        names[index]
        for index in sorted(
            range(len(names)),
            key=lambda index: (-float(scores[index]), sha256_bytes(names[index].encode("utf-8"))),
        )
    ]


def item_metrics(rankings: list[list[str]], gold: list[tuple[str, ...]]) -> tuple[np.ndarray, np.ndarray]:
    accuracy = []
    reciprocal_rank = []
    for ordered, accepted in zip(rankings, gold):
        ranks = [ordered.index(name) + 1 for name in accepted if name in ordered]
        best = min(ranks) if ranks else len(ordered) + 1
        accuracy.append(float(best == 1))
        reciprocal_rank.append(1.0 / best)
    return np.asarray(accuracy), np.asarray(reciprocal_rank)


def bootstrap_interval(values: np.ndarray, repeats: int, seed: int) -> list[float]:
    generator = np.random.default_rng(seed)
    means = np.empty(repeats, dtype=np.float64)
    for start in range(0, repeats, 1000):
        count = min(1000, repeats - start)
        indices = generator.integers(0, len(values), size=(count, len(values)))
        means[start : start + count] = values[indices].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def model_manifest(path: Path) -> list[dict[str, object]]:
    return [
        {
            "relative_path": file.relative_to(path).as_posix(),
            "bytes": file.stat().st_size,
            "sha256": sha256_file(file),
        }
        for file in sorted(path.rglob("*"))
        if file.is_file()
    ]


def build_items(
    expanded_rows: list[dict[str, object]],
    question_rows: list[dict[str, object]],
    gold_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    questions = {str(row["id"]): row for row in question_rows}
    gold = {str(row["id"]): row for row in gold_rows}
    items = []
    for expanded in expanded_rows:
        item_id = str(expanded["id"])
        query = question_text(questions[item_id])
        if question_text(expanded) != query:
            raise ValueError(f"Question mismatch for {item_id}")
        tools = list(expanded["function"])
        names = [str(tool["name"]) for tool in tools]
        accepted = gold_names(gold[item_id])
        if not set(accepted).issubset(names):
            raise ValueError(f"Gold function missing from menu for {item_id}")
        items.append(
            {
                "id": item_id,
                "query": query,
                "query_sha256": sha256_bytes(query.encode("utf-8")),
                "tools": tools,
                "names": names,
                "gold": accepted,
                "spans": extract_spans(query),
            }
        )
    return items


def encode_features(
    items: list[dict[str, object]],
    dense_model: SentenceTransformer,
    cross_model: CrossEncoder,
    batch_size: int,
) -> None:
    queries = [str(item["query"]) for item in items]
    query_vectors = dense_model.encode(
        queries, batch_size=batch_size, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False
    )
    schema_records = []
    span_records = []
    parameter_records = []
    for item_index, item in enumerate(items):
        for tool_index, tool in enumerate(item["tools"]):
            schema_records.append((item_index, tool_index, schema_text(tool)))
            for parameter_index, parameter in enumerate(required_parameters(tool)):
                parameter_records.append((item_index, tool_index, parameter_index, parameter))
        for span_index, span in enumerate(item["spans"]):
            span_records.append((item_index, span_index, span))
    schema_vectors = dense_model.encode(
        [record[2] for record in schema_records],
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    cross_scores = np.asarray(
        cross_model.predict(
            [(queries[item_index], text) for item_index, _, text in schema_records],
            batch_size=batch_size,
            show_progress_bar=False,
        )
    ).reshape(-1)
    span_vectors = dense_model.encode(
        [str(record[2]["text"]) for record in span_records],
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    ) if span_records else np.empty((0, 384), dtype=np.float32)
    parameter_vectors = dense_model.encode(
        [str(record[3]["text"]) for record in parameter_records],
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    ) if parameter_records else np.empty((0, 384), dtype=np.float32)

    schema_cursor = 0
    span_cursor = 0
    parameter_cursor = 0
    for item_index, item in enumerate(items):
        menu_size = len(item["tools"])
        item["dense_scores"] = np.asarray(
            [float(query_vectors[item_index] @ schema_vectors[schema_cursor + offset]) for offset in range(menu_size)]
        )
        item["cross_scores"] = cross_scores[schema_cursor : schema_cursor + menu_size].astype(np.float64)
        item["bm25_scores"] = bm25_scores(str(item["query"]), [record[2] for record in schema_records[schema_cursor : schema_cursor + menu_size]])
        schema_cursor += menu_size
        item_span_vectors = span_vectors[span_cursor : span_cursor + len(item["spans"])]
        span_cursor += len(item["spans"])
        item["parameters"] = []
        item["edges"] = []
        for tool in item["tools"]:
            parameters = required_parameters(tool)
            vectors = parameter_vectors[parameter_cursor : parameter_cursor + len(parameters)]
            parameter_cursor += len(parameters)
            item["parameters"].append(parameters)
            item["edges"].append(edge_features(item["spans"], parameters, item_span_vectors, vectors))


def score_alignment(items: list[dict[str, object]], parameters: dict[str, float], relaxed: bool) -> tuple[list[np.ndarray], list[list[dict[str, object]]]]:
    score_rows = []
    details = []
    for item in items:
        scores = []
        item_details = []
        for tool_index in range(len(item["tools"])):
            score, assignments, edge_scores, threshold_margins = alignment_score(
                item["edges"][tool_index],
                len(item["spans"]),
                len(item["parameters"][tool_index]),
                type_bonus=parameters["type_bonus"],
                enum_bonus=parameters["enum_bonus"],
                null_threshold=parameters["null_threshold"],
                unmatched_penalty=parameters["unmatched_penalty"],
                relaxed=relaxed,
            )
            scores.append(score)
            item_details.append(
                {
                    "assignments": assignments,
                    "edge_scores": edge_scores,
                    "threshold_margins": threshold_margins,
                }
            )
        score_rows.append(np.asarray(scores, dtype=np.float64))
        details.append(item_details)
    return score_rows, details


def fused_rankings(items: list[dict[str, object]], alignment_scores: list[np.ndarray], weight: float) -> list[list[str]]:
    return [
        rank(item["names"], zscores(item["cross_scores"]) + weight * zscores(alignment))
        for item, alignment in zip(items, alignment_scores)
    ]


def metrics_for_rankings(rankings: list[list[str]], items: list[dict[str, object]]) -> dict[str, object]:
    accuracy, reciprocal_rank = item_metrics(rankings, [item["gold"] for item in items])
    return {
        "accuracy": float(accuracy.mean()),
        "mrr": float(reciprocal_rank.mean()),
        "accuracy_items": accuracy,
        "mrr_items": reciprocal_rank,
    }


def parameter_grid(config: dict[str, object]) -> list[dict[str, float]]:
    return [
        {
            "fusion_weight": float(weight),
            "type_bonus": float(type_bonus),
            "enum_bonus": float(config["enum_bonus"]),
            "null_threshold": float(null_threshold),
            "unmatched_penalty": float(unmatched_penalty),
        }
        for weight in config["fusion_weights"]
        for type_bonus in config["type_bonuses"]
        for null_threshold in config["null_thresholds"]
        for unmatched_penalty in config["unmatched_penalties"]
    ]


def select_parameters(items: list[dict[str, object]], config: dict[str, object], relaxed: bool) -> tuple[dict[str, float], list[dict[str, object]]]:
    results = []
    for parameters in parameter_grid(config):
        alignment, _ = score_alignment(items, parameters, relaxed)
        metrics = metrics_for_rankings(fused_rankings(items, alignment, parameters["fusion_weight"]), items)
        results.append(
            {
                "parameters": parameters,
                "accuracy": metrics["accuracy"],
                "mrr": metrics["mrr"],
            }
        )
    results.sort(
        key=lambda result: (
            -result["accuracy"],
            -result["mrr"],
            result["parameters"]["fusion_weight"],
            result["parameters"]["type_bonus"],
            result["parameters"]["unmatched_penalty"],
            result["parameters"]["null_threshold"],
        )
    )
    return results[0]["parameters"], results


def base_method(items: list[dict[str, object]], key: str) -> tuple[list[list[str]], dict[str, object]]:
    rankings = [rank(item["names"], item[key]) for item in items]
    return rankings, metrics_for_rankings(rankings, items)


def serializable_metrics(metrics: dict[str, object]) -> dict[str, float]:
    return {"accuracy": metrics["accuracy"], "mrr": metrics["mrr"]}


def run(args: argparse.Namespace) -> None:
    started = time.perf_counter()
    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    dense_path = (config_path.parent / config["dense_model_path"]).resolve()
    cross_path = (config_path.parent / config["cross_model_path"]).resolve()
    input_paths = {
        "expanded": Path(args.expanded).resolve(),
        "questions": Path(args.questions).resolve(),
        "gold": Path(args.gold).resolve(),
    }
    items = build_items(
        load_jsonl(input_paths["expanded"]),
        load_jsonl(input_paths["questions"]),
        load_jsonl(input_paths["gold"]),
    )
    torch.manual_seed(int(config["seed"]))
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False
    dense_model = SentenceTransformer(str(dense_path), device=config["device"], local_files_only=True)
    cross_model = CrossEncoder(str(cross_path), device=config["device"], local_files_only=True)
    encode_features(items, dense_model, cross_model, int(config["batch_size"]))

    base_rankings, cross_metrics = base_method(items, "cross_scores")
    dense_rankings, dense_metrics = base_method(items, "dense_scores")
    bm25_rankings, bm25_metrics = base_method(items, "bm25_scores")

    if args.phase == "development":
        selected, grid = select_parameters(items, config, relaxed=False)
        selected_relaxed = dict(selected)
        relaxed_grid = []
    else:
        selected = json.loads(Path(args.selected_params).read_text(encoding="utf-8"))["tppa"]
        selected_relaxed = dict(selected)
        grid = []
        relaxed_grid = []

    alignment, alignment_details = score_alignment(items, selected, relaxed=False)
    candidate_rankings = fused_rankings(items, alignment, selected["fusion_weight"])
    candidate_metrics = metrics_for_rankings(candidate_rankings, items)
    relaxed_alignment, relaxed_details = score_alignment(items, selected_relaxed, relaxed=True)
    relaxed_rankings = fused_rankings(items, relaxed_alignment, selected_relaxed["fusion_weight"])
    relaxed_metrics = metrics_for_rankings(relaxed_rankings, items)

    top1_difference = candidate_metrics["accuracy_items"] - cross_metrics["accuracy_items"]
    mrr_difference = candidate_metrics["mrr_items"] - cross_metrics["mrr_items"]
    corrections = int(np.sum(top1_difference == 1.0))
    regressions = int(np.sum(top1_difference == -1.0))
    bootstrap_repeats = int(config["bootstrap_repeats"])
    seed = int(config["seed"])
    top1_interval = bootstrap_interval(top1_difference, bootstrap_repeats, seed)
    mrr_interval = bootstrap_interval(mrr_difference, bootstrap_repeats, seed + 1)

    contrast_mask = []
    for item in items:
        cross_z = zscores(item["cross_scores"])
        gold_indices = [index for index, name in enumerate(item["names"]) if name in item["gold"]]
        distractor_indices = [index for index, name in enumerate(item["names"]) if name not in item["gold"]]
        if not gold_indices or not distractor_indices:
            contrast_mask.append(False)
            continue
        order_key = lambda index: (
            -float(cross_z[index]),
            sha256_bytes(item["names"][index].encode("utf-8")),
        )
        gold_index = min(gold_indices, key=order_key)
        distractor_index = min(distractor_indices, key=order_key)
        gold_signature = tuple(sorted(parameter_type(parameter) for parameter in item["parameters"][gold_index]))
        distractor_signature = tuple(
            sorted(parameter_type(parameter) for parameter in item["parameters"][distractor_index])
        )
        gap = abs(float(cross_z[gold_index] - cross_z[distractor_index]))
        contrast_mask.append(
            gap <= float(config["contrast_z_gap"]) and gold_signature != distractor_signature
        )
    contrast_mask_array = np.asarray(contrast_mask, dtype=bool)
    contrast_delta = float(top1_difference[contrast_mask_array].mean()) if contrast_mask_array.any() else 0.0
    outside_delta = float(top1_difference[~contrast_mask_array].mean()) if (~contrast_mask_array).any() else 0.0

    query_hashes = sorted(item["query_sha256"] for item in items)
    overlap = []
    if args.phase == "confirmation":
        development_hashes = set(json.loads(Path(args.development_query_hashes).read_text(encoding="utf-8")))
        overlap = sorted(development_hashes.intersection(query_hashes))

    accuracy_delta = float(candidate_metrics["accuracy"] - cross_metrics["accuracy"])
    mean_mrr_delta = float(candidate_metrics["mrr"] - cross_metrics["mrr"])
    if args.phase == "development":
        gates = {
            "top1_delta_at_least_0_02": accuracy_delta >= 0.02,
            "mrr_bootstrap_lower_above_zero": mrr_interval[0] > 0.0,
            "net_corrections_positive": corrections > regressions,
            "contrast_advantage_larger": contrast_mask_array.any() and contrast_delta > outside_delta,
        }
    else:
        gates = {
            "query_hashes_disjoint": not overlap,
            "top1_delta_positive": accuracy_delta > 0.0,
            "mrr_delta_positive": mean_mrr_delta > 0.0,
            "top1_bootstrap_lower_nonnegative": top1_interval[0] >= 0.0,
            "net_corrections_positive": corrections > regressions,
        }

    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=False)
    raw_path = output / "raw.jsonl"
    with raw_path.open("w", encoding="utf-8", newline="\n") as stream:
        for item_index, item in enumerate(items):
            tool_records = []
            candidate_scores = zscores(item["cross_scores"]) + selected["fusion_weight"] * zscores(alignment[item_index])
            relaxed_scores = zscores(item["cross_scores"]) + selected_relaxed["fusion_weight"] * zscores(relaxed_alignment[item_index])
            for tool_index, tool in enumerate(item["tools"]):
                tool_records.append(
                    {
                        "name": item["names"][tool_index],
                        "schema": schema_text(tool),
                        "required_parameters": item["parameters"][tool_index],
                        "edge_features": item["edges"][tool_index],
                        "tppa": alignment_details[item_index][tool_index],
                        "relaxed": relaxed_details[item_index][tool_index],
                        "scores": {
                            "bm25": float(item["bm25_scores"][tool_index]),
                            "dense": float(item["dense_scores"][tool_index]),
                            "cross_encoder": float(item["cross_scores"][tool_index]),
                            "tppa_alignment": float(alignment[item_index][tool_index]),
                            "relaxed_alignment": float(relaxed_alignment[item_index][tool_index]),
                            "candidate_fused": float(candidate_scores[tool_index]),
                            "relaxed_fused": float(relaxed_scores[tool_index]),
                        },
                    }
                )
            record = {
                "id": item["id"],
                "query": item["query"],
                "query_sha256": item["query_sha256"],
                "gold": item["gold"],
                "spans": item["spans"],
                "parameter_contrast": bool(contrast_mask[item_index]),
                "rankings": {
                    "bm25": bm25_rankings[item_index],
                    "dense": dense_rankings[item_index],
                    "cross_encoder": base_rankings[item_index],
                    "relaxed": relaxed_rankings[item_index],
                    "tppa": candidate_rankings[item_index],
                },
                "tools": tool_records,
            }
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    selected_path = output / "selected_params.json"
    selected_path.write_text(
        json.dumps({"tppa": selected, "relaxed": selected_relaxed}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    query_hash_path = output / "query_hashes.json"
    query_hash_path.write_text(json.dumps(query_hashes, indent=2) + "\n", encoding="utf-8", newline="\n")
    summary = {
        "phase": args.phase,
        "items": len(items),
        "input_sha256": {name: sha256_file(path) for name, path in input_paths.items()},
        "config_sha256": sha256_file(config_path),
        "selected_parameters": {"tppa": selected, "relaxed": selected_relaxed},
        "grid": grid,
        "relaxed_grid": relaxed_grid,
        "metrics": {
            "bm25": serializable_metrics(bm25_metrics),
            "dense": serializable_metrics(dense_metrics),
            "cross_encoder": serializable_metrics(cross_metrics),
            "relaxed": serializable_metrics(relaxed_metrics),
            "tppa": serializable_metrics(candidate_metrics),
        },
        "tppa_minus_cross_encoder": {
            "accuracy": accuracy_delta,
            "mrr": mean_mrr_delta,
            "accuracy_bootstrap_95": top1_interval,
            "mrr_bootstrap_95": mrr_interval,
            "corrections": corrections,
            "regressions": regressions,
        },
        "parameter_contrast": {
            "count": int(contrast_mask_array.sum()),
            "accuracy_delta_inside": contrast_delta,
            "accuracy_delta_outside": outside_delta,
        },
        "development_query_hash_overlap": overlap,
        "gates": gates,
        "all_gates_passed": all(gates.values()),
        "elapsed_seconds": time.perf_counter() - started,
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    environment = {
        "python_executable": sys.executable,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "sentence_transformers": sentence_transformers.__version__,
        "transformers": transformers.__version__,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0),
        "cuda_capability": list(torch.cuda.get_device_capability(0)),
        "nvidia_driver": subprocess.run(
            ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip().splitlines()[0],
        "device": config["device"],
        "seed": seed,
        "dense_model_manifest": model_manifest(dense_path),
        "cross_model_manifest": model_manifest(cross_path),
    }
    (output / "environment.json").write_text(
        json.dumps(environment, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"phase": args.phase, "items": len(items), "all_gates_passed": summary["all_gates_passed"], "summary": str(output / 'summary.json')}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--expanded", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--gold", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--selected-params")
    parser.add_argument("--development-query-hashes")
    args = parser.parse_args()
    if args.phase == "confirmation" and (not args.selected_params or not args.development_query_hashes):
        parser.error("confirmation requires --selected-params and --development-query-hashes")
    run(args)


if __name__ == "__main__":
    main()
