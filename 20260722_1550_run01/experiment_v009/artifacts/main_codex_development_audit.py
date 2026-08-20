from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment


TOKEN_RE = re.compile(r"[a-z0-9_]+")
DATE_WORDS = {"date", "day", "month", "time", "timestamp", "week", "year"}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def name_hash(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def normalize(text: str) -> str:
    return " ".join(TOKEN_RE.findall(text.lower()))


def parameter_type(parameter: dict[str, object]) -> str:
    words = set(normalize(f"{parameter['name']} {parameter['description']}").split())
    if DATE_WORDS.intersection(words):
        return "date_time"
    kind = str(parameter["type"]).lower()
    if kind in {"integer", "float", "number"}:
        return "number"
    if kind in {"boolean", "bool"}:
        return "boolean"
    return "text"


def zscores(values: np.ndarray) -> np.ndarray:
    standard_deviation = float(values.std())
    if standard_deviation == 0.0:
        return np.zeros_like(values)
    return (values - float(values.mean())) / standard_deviation


def rank(names: list[str], scores: np.ndarray) -> list[str]:
    return [
        names[index]
        for index in sorted(
            range(len(names)),
            key=lambda index: (-float(scores[index]), name_hash(names[index])),
        )
    ]


def alignment(
    features: list[list[dict[str, object]]],
    span_count: int,
    parameter_count: int,
    parameters: dict[str, float],
    relaxed: bool,
) -> tuple[float, list[dict[str, object]], list[list[float]], list[list[float]]]:
    if parameter_count == 0:
        return 0.0, [], [], []
    if span_count == 0:
        return -parameters["unmatched_penalty"], [], [], []
    edge_scores = np.asarray(
        [
            [
                float(edge["cosine"])
                + parameters["type_bonus"] * float(edge["type_compatibility"])
                + parameters["enum_bonus"] * float(bool(edge["enum_exact"]))
                for edge in row
            ]
            for row in features
        ],
        dtype=np.float64,
    )
    margins = edge_scores - parameters["null_threshold"]
    assignments: list[dict[str, object]] = []
    matched: set[int] = set()
    mass = 0.0
    if relaxed:
        pairs = [(span, int(margins[span].argmax())) for span in range(span_count)]
    else:
        augmented = np.concatenate(
            [margins, np.zeros((span_count, span_count), dtype=np.float64)], axis=1
        )
        rows, columns = linear_sum_assignment(-augmented)
        pairs = list(zip(rows.tolist(), columns.tolist()))
    for span_index, parameter_index in pairs:
        if parameter_index >= parameter_count or margins[span_index, parameter_index] <= 0.0:
            continue
        edge_score = float(edge_scores[span_index, parameter_index])
        margin = float(margins[span_index, parameter_index])
        matched.add(parameter_index)
        mass += edge_score
        assignments.append(
            {
                "span": span_index,
                "parameter": parameter_index,
                "edge_score": edge_score,
                "threshold_margin": margin,
            }
        )
    unmatched_fraction = (parameter_count - len(matched)) / parameter_count
    score = mass / parameter_count - parameters["unmatched_penalty"] * unmatched_fraction
    return float(score), assignments, edge_scores.tolist(), margins.tolist()


def item_metrics(rankings: list[list[str]], records: list[dict[str, object]]) -> tuple[np.ndarray, np.ndarray]:
    accuracy = []
    reciprocal_rank = []
    for ordered, record in zip(rankings, records, strict=True):
        accepted = set(record["gold"])
        ranks = [index + 1 for index, name in enumerate(ordered) if name in accepted]
        best = min(ranks) if ranks else len(ordered) + 1
        accuracy.append(float(best == 1))
        reciprocal_rank.append(1.0 / best)
    return np.asarray(accuracy), np.asarray(reciprocal_rank)


def bootstrap(values: np.ndarray, repeats: int, seed: int) -> list[float]:
    generator = np.random.default_rng(seed)
    means = np.empty(repeats, dtype=np.float64)
    for start in range(0, repeats, 1000):
        count = min(1000, repeats - start)
        indices = generator.integers(0, len(values), size=(count, len(values)))
        means[start : start + count] = values[indices].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def grid(config: dict[str, object]) -> list[dict[str, float]]:
    return [
        {
            "fusion_weight": float(weight),
            "type_bonus": float(type_bonus),
            "enum_bonus": float(config["enum_bonus"]),
            "null_threshold": float(null_threshold),
            "unmatched_penalty": float(unmatched_penalty),
        }
        for weight, type_bonus, null_threshold, unmatched_penalty in itertools.product(
            config["fusion_weights"],
            config["type_bonuses"],
            config["null_thresholds"],
            config["unmatched_penalties"],
        )
    ]


def method_rankings(records: list[dict[str, object]], score_name: str) -> list[list[str]]:
    return [
        rank(
            [str(tool["name"]) for tool in record["tools"]],
            np.asarray([float(tool["scores"][score_name]) for tool in record["tools"]]),
        )
        for record in records
    ]


def evaluate_tuple(
    records: list[dict[str, object]], parameters: dict[str, float]
) -> tuple[list[list[str]], float, float]:
    rankings = []
    for record in records:
        names = [str(tool["name"]) for tool in record["tools"]]
        cross = np.asarray([float(tool["scores"]["cross_encoder"]) for tool in record["tools"]])
        aligned = []
        for tool in record["tools"]:
            score, _, _, _ = alignment(
                tool["edge_features"],
                len(record["spans"]),
                len(tool["required_parameters"]),
                parameters,
                False,
            )
            aligned.append(score)
        fused = zscores(cross) + parameters["fusion_weight"] * zscores(np.asarray(aligned))
        rankings.append(rank(names, fused))
    accuracy, reciprocal_rank = item_metrics(rankings, records)
    return rankings, float(accuracy.mean()), float(reciprocal_rank.mean())


def audit(args: argparse.Namespace) -> dict[str, object]:
    records = load_jsonl(args.raw)
    summary = load_json(args.summary)
    selected = load_json(args.selected)
    config = load_json(args.config)
    environment = load_json(args.environment)
    execution = load_json(args.execution)
    query_hashes = load_json(args.query_hashes)
    assert len(records) == 200
    assert len({record["id"] for record in records}) == 200
    assert execution["exit_code"] == 0 and len(execution["inputs"]) == 22
    assert all(output["after"]["exists"] for output in execution["outputs"])
    assert query_hashes == sorted(record["query_sha256"] for record in records)
    assert selected["tppa"] == selected["relaxed"]
    assert environment["python"] == "3.11.15"
    assert environment["gpu"] == "NVIDIA GeForce RTX 5060 Ti"
    assert environment["cuda_capability"] == [12, 0]

    alignment_max_error = 0.0
    assignment_count = 0
    edge_cell_count = 0
    for record in records:
        for tool in record["tools"]:
            edge_cell_count += sum(len(row) for row in tool["edge_features"])
            for method, relaxed in (("tppa", False), ("relaxed", True)):
                score, assignments, edge_scores, margins = alignment(
                    tool["edge_features"],
                    len(record["spans"]),
                    len(tool["required_parameters"]),
                    selected[method],
                    relaxed,
                )
                stored = tool[method]
                assert assignments == stored["assignments"]
                assert np.allclose(edge_scores, stored["edge_scores"], rtol=0.0, atol=1e-12)
                assert np.allclose(margins, stored["threshold_margins"], rtol=0.0, atol=1e-12)
                error = abs(score - float(tool["scores"][f"{method}_alignment"]))
                alignment_max_error = max(alignment_max_error, error)
                assignment_count += len(assignments)
    assert alignment_max_error <= 1e-12

    method_score_names = {
        "bm25": "bm25",
        "dense": "dense",
        "cross_encoder": "cross_encoder",
        "relaxed": "relaxed_fused",
        "tppa": "candidate_fused",
    }
    metrics: dict[str, dict[str, float]] = {}
    metric_max_error = 0.0
    item_values: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for method, score_name in method_score_names.items():
        rankings = method_rankings(records, score_name)
        assert all(ranking == record["rankings"][method] for ranking, record in zip(rankings, records, strict=True))
        accuracy, reciprocal_rank = item_metrics(rankings, records)
        item_values[method] = (accuracy, reciprocal_rank)
        metrics[method] = {"accuracy": float(accuracy.mean()), "mrr": float(reciprocal_rank.mean())}
        for metric in ("accuracy", "mrr"):
            metric_max_error = max(
                metric_max_error,
                abs(metrics[method][metric] - float(summary["metrics"][method][metric])),
            )
    assert metric_max_error <= 1e-12

    grid_rows = []
    grid_max_error = 0.0
    for parameters in grid(config):
        _, accuracy, mrr = evaluate_tuple(records, parameters)
        grid_rows.append({"parameters": parameters, "accuracy": accuracy, "mrr": mrr})
    grid_rows.sort(
        key=lambda result: (
            -result["accuracy"],
            -result["mrr"],
            result["parameters"]["fusion_weight"],
            result["parameters"]["type_bonus"],
            result["parameters"]["unmatched_penalty"],
            result["parameters"]["null_threshold"],
        )
    )
    assert len(grid_rows) == len(summary["grid"]) == 384
    for actual, stored in zip(grid_rows, summary["grid"], strict=True):
        assert actual["parameters"] == stored["parameters"]
        grid_max_error = max(
            grid_max_error,
            abs(actual["accuracy"] - float(stored["accuracy"])),
            abs(actual["mrr"] - float(stored["mrr"])),
        )
    assert grid_rows[0]["parameters"] == selected["tppa"]
    assert grid_max_error <= 1e-12

    candidate_accuracy, candidate_mrr = item_values["tppa"]
    cross_accuracy, cross_mrr = item_values["cross_encoder"]
    top1_difference = candidate_accuracy - cross_accuracy
    mrr_difference = candidate_mrr - cross_mrr
    top1_interval = bootstrap(top1_difference, int(config["bootstrap_repeats"]), int(config["seed"]))
    mrr_interval = bootstrap(mrr_difference, int(config["bootstrap_repeats"]), int(config["seed"]) + 1)
    assert np.allclose(top1_interval, summary["tppa_minus_cross_encoder"]["accuracy_bootstrap_95"], atol=1e-12)
    assert np.allclose(mrr_interval, summary["tppa_minus_cross_encoder"]["mrr_bootstrap_95"], atol=1e-12)
    corrections = int(np.sum(top1_difference == 1.0))
    regressions = int(np.sum(top1_difference == -1.0))

    contrast = []
    for record in records:
        tools = record["tools"]
        names = [str(tool["name"]) for tool in tools]
        cross = zscores(np.asarray([float(tool["scores"]["cross_encoder"]) for tool in tools]))
        accepted = set(record["gold"])
        gold_indices = [index for index, name in enumerate(names) if name in accepted]
        distractor_indices = [index for index, name in enumerate(names) if name not in accepted]
        if not gold_indices or not distractor_indices:
            value = False
        else:
            key = lambda index: (-float(cross[index]), name_hash(names[index]))
            gold_index = min(gold_indices, key=key)
            distractor_index = min(distractor_indices, key=key)
            gold_signature = tuple(sorted(parameter_type(p) for p in tools[gold_index]["required_parameters"]))
            distractor_signature = tuple(
                sorted(parameter_type(p) for p in tools[distractor_index]["required_parameters"])
            )
            value = (
                abs(float(cross[gold_index] - cross[distractor_index])) <= float(config["contrast_z_gap"])
                and gold_signature != distractor_signature
            )
        assert value == bool(record["parameter_contrast"])
        contrast.append(value)
    contrast_mask = np.asarray(contrast, dtype=bool)
    inside = float(top1_difference[contrast_mask].mean())
    outside = float(top1_difference[~contrast_mask].mean())
    assert int(contrast_mask.sum()) == summary["parameter_contrast"]["count"]
    assert abs(inside - summary["parameter_contrast"]["accuracy_delta_inside"]) <= 1e-12
    assert abs(outside - summary["parameter_contrast"]["accuracy_delta_outside"]) <= 1e-12

    accuracy_delta = float(top1_difference.mean())
    mean_mrr_delta = float(mrr_difference.mean())
    gates = {
        "top1_delta_at_least_0_02": accuracy_delta >= 0.02,
        "mrr_bootstrap_lower_above_zero": mrr_interval[0] > 0.0,
        "net_corrections_positive": corrections > regressions,
        "contrast_advantage_larger": bool(contrast_mask.any() and inside > outside),
    }
    assert gates == summary["gates"]

    return {
        "schema_version": 1,
        "phase": "development",
        "raw_sha256": sha256_file(args.raw),
        "summary_sha256": sha256_file(args.summary),
        "selected_params_sha256": sha256_file(args.selected),
        "query_hashes_sha256": sha256_file(args.query_hashes),
        "environment_sha256": sha256_file(args.environment),
        "execution_sha256": sha256_file(args.execution),
        "raw_rows": len(records),
        "tool_records": sum(len(record["tools"]) for record in records),
        "edge_cells": edge_cell_count,
        "assignments_verified": assignment_count,
        "grid_rows_verified": len(grid_rows),
        "alignment_max_abs_error": alignment_max_error,
        "metric_max_abs_error": metric_max_error,
        "grid_max_abs_error": grid_max_error,
        "metrics": metrics,
        "tppa_minus_cross_encoder": {
            "accuracy": accuracy_delta,
            "mrr": mean_mrr_delta,
            "accuracy_bootstrap_95": top1_interval,
            "mrr_bootstrap_95": mrr_interval,
            "corrections": corrections,
            "regressions": regressions,
        },
        "parameter_contrast": {
            "count": int(contrast_mask.sum()),
            "accuracy_delta_inside": inside,
            "accuracy_delta_outside": outside,
        },
        "gates": gates,
        "all_gates_passed": all(gates.values()),
        "environment": {
            "python": environment["python"],
            "torch": environment["torch"],
            "torch_cuda": environment["torch_cuda"],
            "gpu": environment["gpu"],
            "cuda_capability": environment["cuda_capability"],
            "nvidia_driver": environment["nvidia_driver"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--selected", required=True, type=Path)
    parser.add_argument("--query-hashes", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--environment", required=True, type=Path)
    parser.add_argument("--execution", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = audit(args)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"audit": "passed", "all_gates_passed": report["all_gates_passed"]}, sort_keys=True))


if __name__ == "__main__":
    main()
