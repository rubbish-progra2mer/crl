from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import CrossEncoder


METHODS = (
    "full_schema",
    "operation_schema",
    "argument_schema",
    "additive_support",
    "max_support",
    "dual_necessity",
)
COMPARATORS = METHODS[:-1]
VIEWS = ("full", "without_operation", "without_arguments", "name_only")
CAMEL_PATTERN = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def json_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def json_lines(path: Path) -> list[dict[str, Any]]:
    result = []
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                result.append(json.loads(line))
    return result


def identifier_words(value: str) -> str:
    expanded = CAMEL_PATTERN.sub(" ", value)
    return " ".join(
        token for token in re.split(r"[^A-Za-z0-9]+", expanded) if token
    ).lower()


def primitive(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def schema_records(node: Any, trail: tuple[str, ...] = ()) -> list[str]:
    result: list[str] = []
    if isinstance(node, dict):
        for key in sorted(node.keys()):
            result.extend(schema_records(node[key], trail + (str(key),)))
    elif isinstance(node, list):
        if all(not isinstance(item, (dict, list)) for item in node):
            heading = " ".join(identifier_words(piece) for piece in trail)
            result.append(f"{heading}: {' '.join(primitive(item) for item in node)}")
        else:
            for position, item in enumerate(node):
                result.extend(schema_records(item, trail + (str(position),)))
    else:
        heading = " ".join(identifier_words(piece) for piece in trail)
        result.append(f"{heading}: {primitive(node)}")
    return result


def independent_views(tool: dict[str, Any]) -> dict[str, str]:
    name = f"tool name: {identifier_words(str(tool['name']))}."
    description = f"operation description: {str(tool.get('description', ''))}."
    arguments = "argument schema: " + ". ".join(
        schema_records(tool.get("parameters", {}))
    )
    return {
        "full": name + " " + description + " " + arguments,
        "without_operation": name + " " + arguments,
        "without_arguments": name + " " + description,
        "name_only": name,
    }


def independent_query(row: dict[str, Any]) -> str:
    parts: list[str] = []
    for group in row["question"]:
        for turn in group:
            if str(turn.get("role", "")) == "user":
                parts.append(str(turn.get("content", "")))
    if not parts:
        raise ValueError(f"query has no user turn: {row['id']}")
    return "\n".join(parts)


def independent_gold(row: dict[str, Any]) -> list[str]:
    names = sorted({str(key) for call in row["ground_truth"] for key in call})
    if not names:
        raise ValueError(f"gold is empty: {row['id']}")
    return names


def query_fold(query_id: str, modulus: int) -> int:
    return hashlib.sha256(query_id.encode("utf-8")).digest()[1] % modulus


def build_examples(
    expanded_rows: list[dict[str, Any]],
    question_rows: list[dict[str, Any]],
    gold_rows: list[dict[str, Any]],
    modulus: int,
) -> list[dict[str, Any]]:
    expanded = {str(row["id"]): row for row in expanded_rows}
    questions = {str(row["id"]): row for row in question_rows}
    gold = {str(row["id"]): row for row in gold_rows}
    if (
        len(expanded) != len(expanded_rows)
        or len(questions) != len(question_rows)
        or len(gold) != len(gold_rows)
    ):
        raise ValueError("duplicate input ID")
    if set(expanded) != set(questions) or set(expanded) != set(gold):
        raise ValueError("input ID sets differ")
    examples = []
    for query_id in sorted(expanded):
        row = expanded[query_id]
        if row["question"] != questions[query_id]["question"]:
            raise ValueError(f"question structure differs: {query_id}")
        query = independent_query(row)
        tools = list(row["function"])
        names = [str(tool["name"]) for tool in tools]
        if len(names) != len(set(names)):
            raise ValueError(f"duplicate tool: {query_id}")
        gold_names = independent_gold(gold[query_id])
        if not set(gold_names).issubset(names):
            raise ValueError(f"missing gold tool: {query_id}")
        examples.append(
            {
                "id": query_id,
                "query": query,
                "query_sha": hashlib.sha256(query.encode("utf-8")).hexdigest(),
                "fold": query_fold(query_id, modulus),
                "names": names,
                "gold": gold_names,
                "views": [independent_views(tool) for tool in tools],
            }
        )
    return examples


def check_model(model_dir: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    expected = config["cross_encoder_files"]
    found = {
        item.relative_to(model_dir).as_posix(): item
        for item in model_dir.rglob("*")
        if item.is_file()
    }
    if set(found) != set(expected):
        raise ValueError("model file set mismatch")
    result = []
    for relative in sorted(found):
        digest = file_sha(found[relative])
        if digest != expected[relative]:
            raise ValueError(f"model file hash mismatch: {relative}")
        result.append(
            {
                "relative_path": relative,
                "bytes": found[relative].stat().st_size,
                "sha256": digest,
            }
        )
    return result


def rescore(
    examples: list[dict[str, Any]],
    model_dir: Path,
    config: dict[str, Any],
) -> tuple[list[np.ndarray], int]:
    pairs: list[tuple[str, str]] = []
    locations: list[tuple[int, int, int]] = []
    for example_index, example in enumerate(examples):
        for tool_index, views in enumerate(example["views"]):
            for view_index, view in enumerate(VIEWS):
                pairs.append((example["query"], views[view]))
                locations.append((example_index, tool_index, view_index))
    model = CrossEncoder(
        str(model_dir), device=str(config["device"]), local_files_only=True
    )
    predictions = np.asarray(
        model.predict(
            pairs,
            batch_size=int(config["cross_encoder_batch_size"]),
            show_progress_bar=False,
            convert_to_numpy=True,
        ),
        dtype=np.float64,
    ).reshape(-1)
    matrices = [
        np.zeros((len(example["names"]), len(VIEWS)), dtype=np.float64)
        for example in examples
    ]
    for prediction, location in zip(predictions, locations, strict=True):
        example_index, tool_index, view_index = location
        matrices[example_index][tool_index, view_index] = float(prediction)
    return matrices, len(pairs)


def independent_scores(matrix: np.ndarray) -> dict[str, np.ndarray]:
    full = matrix[:, 0]
    no_operation = matrix[:, 1]
    no_arguments = matrix[:, 2]
    operation_drop = full - no_operation
    argument_drop = full - no_arguments
    return {
        "full_schema": full,
        "operation_schema": no_arguments,
        "argument_schema": no_operation,
        "additive_support": full + (operation_drop + argument_drop) / 2.0,
        "max_support": full + np.maximum(operation_drop, argument_drop),
        "dual_necessity": full + np.minimum(operation_drop, argument_drop),
    }


def tie_hash(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def ordered(names: list[str], values: np.ndarray) -> list[str]:
    indexes = sorted(
        range(len(names)), key=lambda index: (-float(values[index]), tie_hash(names[index]))
    )
    return [names[index] for index in indexes]


def replay_records(
    examples: list[dict[str, Any]],
    matrices: list[np.ndarray],
    raw: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str], float, float]:
    errors: list[str] = []
    replayed: list[dict[str, Any]] = []
    maximum_view_error = 0.0
    maximum_method_error = 0.0
    if len(raw) != len(examples):
        errors.append("raw row count mismatch")
        return replayed, errors, math.inf, math.inf
    for example, matrix, record in zip(examples, matrices, raw, strict=True):
        if (
            record.get("query_id") != example["id"]
            or record.get("query") != example["query"]
            or record.get("query_sha256") != example["query_sha"]
            or int(record.get("fold", -1)) != example["fold"]
            or record.get("gold_names") != example["gold"]
        ):
            errors.append(f"query identity mismatch: {example['id']}")
        raw_tools = record.get("tools", [])
        if len(raw_tools) != len(example["names"]):
            errors.append(f"tool count mismatch: {example['id']}")
            continue
        expected_scores = independent_scores(matrix)
        gold = set(example["gold"])
        expected_methods = {}
        for method in METHODS:
            ranking = ordered(example["names"], expected_scores[method])
            reciprocal_rank = 1.0 / next(
                position
                for position, name in enumerate(ranking, 1)
                if name in gold
            )
            expected_methods[method] = {
                "ranking": ranking,
                "top1_correct": ranking[0] in gold,
                "reciprocal_rank": reciprocal_rank,
            }
            observed = record.get("methods", {}).get(method, {})
            if (
                observed.get("ranking") != ranking
                or bool(observed.get("top1_correct")) != (ranking[0] in gold)
                or abs(float(observed.get("reciprocal_rank", math.inf)) - reciprocal_rank)
                > 1e-12
            ):
                errors.append(f"method ranking/metric mismatch: {example['id']}:{method}")
        for tool_index, (name, tool_record) in enumerate(
            zip(example["names"], raw_tools, strict=True)
        ):
            if (
                tool_record.get("tool_name") != name
                or bool(tool_record.get("is_gold")) != (name in gold)
                or tool_record.get("view_texts") != example["views"][tool_index]
            ):
                errors.append(f"tool identity/text mismatch: {example['id']}:{name}")
            for view_index, view in enumerate(VIEWS):
                observed = float(tool_record.get("view_scores", {}).get(view, math.inf))
                maximum_view_error = max(
                    maximum_view_error, abs(observed - float(matrix[tool_index, view_index]))
                )
            operation_drop = float(matrix[tool_index, 0] - matrix[tool_index, 1])
            argument_drop = float(matrix[tool_index, 0] - matrix[tool_index, 2])
            if (
                abs(float(tool_record.get("operation_drop", math.inf)) - operation_drop)
                > 1e-12
                or abs(float(tool_record.get("argument_drop", math.inf)) - argument_drop)
                > 1e-12
            ):
                errors.append(f"deletion drop mismatch: {example['id']}:{name}")
            for method in METHODS:
                observed = float(
                    tool_record.get("method_scores", {}).get(method, math.inf)
                )
                maximum_method_error = max(
                    maximum_method_error,
                    abs(observed - float(expected_scores[method][tool_index])),
                )
        replayed.append(
            {
                "fold": example["fold"],
                "methods": expected_methods,
            }
        )
    if maximum_view_error > 1e-6:
        errors.append(f"maximum repeated view-score error exceeds tolerance: {maximum_view_error}")
    if maximum_method_error > 1e-12:
        errors.append(f"maximum method-score error exceeds tolerance: {maximum_method_error}")
    return replayed, errors, maximum_view_error, maximum_method_error


def replay_metrics(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    return {
        method: {
            "top1": float(
                np.mean([record["methods"][method]["top1_correct"] for record in records])
            ),
            "mrr": float(
                np.mean([record["methods"][method]["reciprocal_rank"] for record in records])
            ),
            "queries": len(records),
        }
        for method in METHODS
    }


def replay_bootstrap(
    records: list[dict[str, Any]],
    comparator: str,
    repeats: int,
    seed: int,
) -> dict[str, Any]:
    candidate_top = np.asarray(
        [record["methods"][METHODS[-1]]["top1_correct"] for record in records],
        dtype=np.float64,
    )
    comparator_top = np.asarray(
        [record["methods"][comparator]["top1_correct"] for record in records],
        dtype=np.float64,
    )
    candidate_mrr = np.asarray(
        [record["methods"][METHODS[-1]]["reciprocal_rank"] for record in records],
        dtype=np.float64,
    )
    comparator_mrr = np.asarray(
        [record["methods"][comparator]["reciprocal_rank"] for record in records],
        dtype=np.float64,
    )
    rng = np.random.default_rng(seed)
    top_samples = np.empty(repeats)
    mrr_samples = np.empty(repeats)
    for index in range(repeats):
        sample = rng.integers(0, len(records), size=len(records))
        top_samples[index] = np.mean(candidate_top[sample] - comparator_top[sample])
        mrr_samples[index] = np.mean(candidate_mrr[sample] - comparator_mrr[sample])
    return {
        "comparator": comparator,
        "top1_point": float(np.mean(candidate_top - comparator_top)),
        "top1_bootstrap_95": [
            float(np.quantile(top_samples, 0.025)),
            float(np.quantile(top_samples, 0.975)),
        ],
        "mrr_point": float(np.mean(candidate_mrr - comparator_mrr)),
        "mrr_bootstrap_95": [
            float(np.quantile(mrr_samples, 0.025)),
            float(np.quantile(mrr_samples, 0.975)),
        ],
        "repeats": repeats,
        "unit": "query_row",
    }


def replay_changes(
    records: list[dict[str, Any]], comparator: str
) -> dict[str, int]:
    candidate = [record["methods"][METHODS[-1]]["top1_correct"] for record in records]
    baseline = [record["methods"][comparator]["top1_correct"] for record in records]
    return {
        "corrections": sum(c and not b for c, b in zip(candidate, baseline, strict=True)),
        "regressions": sum(b and not c for c, b in zip(candidate, baseline, strict=True)),
    }


def compare_numeric(
    expected: Any,
    observed: Any,
    path: str,
    errors: list[str],
) -> float:
    maximum = 0.0
    if isinstance(expected, dict):
        if not isinstance(observed, dict) or set(expected) - set(observed):
            errors.append(f"summary structure mismatch: {path}")
            return math.inf
        for key, value in expected.items():
            maximum = max(
                maximum,
                compare_numeric(value, observed[key], f"{path}.{key}", errors),
            )
    elif isinstance(expected, list):
        if not isinstance(observed, list) or len(expected) != len(observed):
            errors.append(f"summary list mismatch: {path}")
            return math.inf
        for index, value in enumerate(expected):
            maximum = max(
                maximum,
                compare_numeric(value, observed[index], f"{path}[{index}]", errors),
            )
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        try:
            error = abs(float(expected) - float(observed))
        except (TypeError, ValueError):
            errors.append(f"summary numeric mismatch: {path}")
            return math.inf
        maximum = max(maximum, error)
        if error > 1e-12:
            errors.append(f"summary numeric mismatch: {path}")
    elif expected != observed:
        errors.append(f"summary value mismatch: {path}")
    return maximum


def audit(args: argparse.Namespace) -> dict[str, Any]:
    errors: list[str] = []
    config = json_file(args.config)
    if config.get("experiment_id") != "v029":
        errors.append("config experiment identity mismatch")
    if file_sha(args.candidate) != config["candidate_sha256"]:
        errors.append("Candidate hash mismatch")
    if file_sha(args.evidence_packet) != config["evidence_packet_sha256"]:
        errors.append("Evidence Packet hash mismatch")
    model_files = check_model(args.model_dir, config)
    summary = json_file(args.summary)
    phase = summary.get("phase")
    if phase not in {"development", "confirmation"}:
        errors.append("summary phase invalid")
    if phase == "development":
        expected_inputs = config["development_inputs"]
        observed_inputs = {
            "questions_sha256": file_sha(args.questions),
            "expanded_sha256": file_sha(args.expanded),
            "gold_sha256": file_sha(args.gold),
        }
        if observed_inputs != expected_inputs:
            errors.append("Development input identity mismatch")
    examples = build_examples(
        json_lines(args.expanded),
        json_lines(args.questions),
        json_lines(args.gold),
        int(config["query_fold_modulus"]),
    )
    matrices, pair_count = rescore(examples, args.model_dir, config)
    raw = json_lines(args.raw)
    replayed, replay_errors, max_view_error, max_method_error = replay_records(
        examples, matrices, raw
    )
    errors.extend(replay_errors)
    metrics = replay_metrics(replayed)
    if phase == "development":
        strongest = max(
            COMPARATORS,
            key=lambda name: (metrics[name]["top1"], metrics[name]["mrr"], name),
        )
        delta = replay_bootstrap(
            replayed,
            strongest,
            int(config["bootstrap_repeats"]),
            int(config["seed"]),
        )
        changes = replay_changes(replayed, "full_schema")
        folds = {}
        for fold in range(int(config["query_fold_modulus"])):
            subset = [record for record in replayed if record["fold"] == fold]
            fold_metrics = replay_metrics(subset)
            folds[str(fold)] = {
                "queries": len(subset),
                "candidate_mrr": fold_metrics[METHODS[-1]]["mrr"],
                "strongest_mrr": fold_metrics[strongest]["mrr"],
                "mrr_delta": (
                    fold_metrics[METHODS[-1]]["mrr"]
                    - fold_metrics[strongest]["mrr"]
                ),
            }
        positive_folds = sum(value["mrr_delta"] > 0.0 for value in folds.values())
        gate_config = config["development_gates"]
        candidate = metrics[METHODS[-1]]
        gates = {
            "candidate_top1": candidate["top1"]
            >= float(gate_config["candidate_top1_min"]),
            "top1_delta_vs_full": (
                candidate["top1"] - metrics["full_schema"]["top1"]
            )
            >= float(gate_config["top1_delta_vs_full_min"]),
            "strictly_beats_every_comparator_top1": all(
                candidate["top1"] > metrics[name]["top1"] for name in COMPARATORS
            ),
            "mrr_bootstrap_lower_vs_strongest": delta["mrr_bootstrap_95"][0] > 0.0,
            "positive_net_corrections_vs_full": changes["corrections"]
            > changes["regressions"],
            "all_fold_mrr_deltas_nonnegative": all(
                value["mrr_delta"] >= 0.0 for value in folds.values()
            ),
            "minimum_positive_folds": positive_folds
            >= int(gate_config["minimum_positive_folds"]),
        }
        expected_core = {
            "metrics": metrics,
            "strongest_comparator": strongest,
            "candidate_minus_strongest": delta,
            "candidate_vs_full_corrections": changes,
            "fold_slices": folds,
            "positive_folds": positive_folds,
            "gates": gates,
            "gates_passed": sum(gates.values()),
            "gates_total": len(gates),
        }
    else:
        if args.development_summary is None or args.input_manifest is None:
            errors.append("Confirmation audit lacks frozen Development/manifest")
            strongest = ""
            expected_core = {}
        else:
            development = json_file(args.development_summary)
            manifest = json_file(args.input_manifest)
            strongest = str(development["strongest_comparator"])
            delta = replay_bootstrap(
                replayed,
                strongest,
                int(config["bootstrap_repeats"]),
                int(config["seed"]),
            )
            changes = replay_changes(replayed, strongest)
            candidate = metrics[METHODS[-1]]
            gates = {
                "candidate_top1_above_frozen_strongest": candidate["top1"]
                > metrics[strongest]["top1"],
                "candidate_mrr_above_frozen_strongest": candidate["mrr"]
                > metrics[strongest]["mrr"],
                "top1_bootstrap_lower_nonnegative": delta["top1_bootstrap_95"][0]
                >= 0.0,
                "positive_net_corrections": changes["corrections"]
                > changes["regressions"],
                "strictly_beats_every_comparator_top1": all(
                    candidate["top1"] > metrics[name]["top1"] for name in COMPARATORS
                ),
                "query_hashes_disjoint": not (
                    set(example["query_sha"] for example in examples)
                    & set(development["query_hashes"])
                ),
            }
            if (
                manifest.get("config_sha256") != file_sha(args.config)
                or manifest.get("phase") != "confirmation"
                or manifest.get("questions_sha256") != file_sha(args.questions)
                or manifest.get("gold_sha256") != file_sha(args.gold)
            ):
                errors.append("Confirmation manifest data mismatch")
            expected_core = {
                "metrics": metrics,
                "strongest_comparator": strongest,
                "candidate_minus_strongest": delta,
                "corrections": changes,
                "development_query_overlap": [],
                "gates": gates,
                "gates_passed": sum(gates.values()),
                "gates_total": len(gates),
            }
    maximum_metric_error = compare_numeric(
        expected_core, summary, "summary", errors
    )
    query_hashes = json_file(args.query_hashes)
    expected_hashes = sorted(example["query_sha"] for example in examples)
    if query_hashes != expected_hashes or summary.get("query_hashes") != expected_hashes:
        errors.append("query hash output mismatch")
    environment = json_file(args.environment)
    if (
        environment.get("python") != "3.11.15"
        or not environment.get("cuda_available")
        or environment.get("gpu") != "NVIDIA GeForce RTX 5060 Ti"
    ):
        errors.append("environment identity mismatch")
    bindings = {
        "config_sha256": file_sha(args.config),
        "candidate_sha256": file_sha(args.candidate),
        "evidence_packet_sha256": file_sha(args.evidence_packet),
        "expanded_sha256": file_sha(args.expanded),
        "questions_sha256": file_sha(args.questions),
        "gold_sha256": file_sha(args.gold),
        "raw_sha256": file_sha(args.raw),
        "query_hashes_sha256": file_sha(args.query_hashes),
        "environment_sha256": file_sha(args.environment),
    }
    for key, value in bindings.items():
        if summary.get(key) != value:
            errors.append(f"summary binding mismatch: {key}")
    if summary.get("model_files") != model_files:
        errors.append("summary model manifest mismatch")
    if int(summary.get("cross_encoder_pairs", -1)) != pair_count:
        errors.append("summary pair count mismatch")
    return {
        "schema_version": 1,
        "status": "AUDIT_OK" if not errors else "AUDIT_FAILED",
        "phase": phase,
        "queries": len(examples),
        "tools": sum(len(example["names"]) for example in examples),
        "cross_encoder_pairs_replayed": pair_count,
        "method_scores_replayed": sum(len(example["names"]) for example in examples)
        * len(METHODS),
        "maximum_view_score_error": max_view_error,
        "maximum_method_score_error": max_method_error,
        "maximum_metric_error": maximum_metric_error,
        "errors": errors,
        "config_sha256": file_sha(args.config),
        "candidate_sha256": file_sha(args.candidate),
        "evidence_packet_sha256": file_sha(args.evidence_packet),
        "raw_sha256": file_sha(args.raw),
        "summary_sha256": file_sha(args.summary),
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
    parser.add_argument("--development-summary", type=Path)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--query-hashes", type=Path, required=True)
    parser.add_argument("--environment", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
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
                "cross_encoder_pairs_replayed": report[
                    "cross_encoder_pairs_replayed"
                ],
                "method_scores_replayed": report["method_scores_replayed"],
                "maximum_view_score_error": report["maximum_view_score_error"],
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
