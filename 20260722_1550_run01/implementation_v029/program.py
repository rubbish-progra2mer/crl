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

import numpy as np
import torch
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
    return " ".join(
        part
        for part in re.split(r"[^A-Za-z0-9]+", CAMEL.sub(" ", value))
        if part
    ).lower()


def scalar_text(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def flatten_schema(value: Any, path: tuple[str, ...] = ()) -> list[str]:
    records: list[str] = []
    if isinstance(value, dict):
        for key in sorted(value):
            records.extend(flatten_schema(value[key], path + (str(key),)))
    elif isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            label = " ".join(split_identifier(part) for part in path)
            records.append(f"{label}: {' '.join(scalar_text(item) for item in value)}")
        else:
            for index, item in enumerate(value):
                records.extend(flatten_schema(item, path + (str(index),)))
    else:
        label = " ".join(split_identifier(part) for part in path)
        records.append(f"{label}: {scalar_text(value)}")
    return records


def view_texts(tool: dict[str, Any]) -> dict[str, str]:
    name = f"tool name: {split_identifier(str(tool['name']))}."
    description = f"operation description: {str(tool.get('description', ''))}."
    arguments = "argument schema: " + ". ".join(
        flatten_schema(tool.get("parameters", {}))
    )
    return {
        "full": f"{name} {description} {arguments}",
        "without_operation": f"{name} {arguments}",
        "without_arguments": f"{name} {description}",
        "name_only": name,
    }


def query_text(row: dict[str, Any]) -> str:
    texts = [
        str(turn.get("content", ""))
        for group in row["question"]
        for turn in group
        if str(turn.get("role", "")) == "user"
    ]
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
    expanded: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    gold: list[dict[str, Any]],
    folds: int,
) -> list[dict[str, Any]]:
    expanded_map = {str(row["id"]): row for row in expanded}
    question_map = {str(row["id"]): row for row in questions}
    gold_map = {str(row["id"]): row for row in gold}
    if (
        len(expanded_map) != len(expanded)
        or len(question_map) != len(questions)
        or len(gold_map) != len(gold)
    ):
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
                "tool_names": names,
                "gold_names": gold_set,
                "views": [view_texts(tool) for tool in tools],
            }
        )
    return examples


def verify_model(model_dir: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    expected = config["cross_encoder_files"]
    observed = {
        path.relative_to(model_dir).as_posix(): path
        for path in model_dir.rglob("*")
        if path.is_file()
    }
    if set(observed) != set(expected):
        raise ValueError("cross-encoder file set mismatch")
    records = []
    for relative_path in sorted(observed):
        path = observed[relative_path]
        digest = sha256_path(path)
        if digest != expected[relative_path]:
            raise ValueError(f"cross-encoder file SHA mismatch: {relative_path}")
        records.append(
            {
                "relative_path": relative_path,
                "bytes": path.stat().st_size,
                "sha256": digest,
            }
        )
    return records


def score_views(
    examples: list[dict[str, Any]],
    model: CrossEncoder,
    config: dict[str, Any],
) -> tuple[list[np.ndarray], int]:
    fields = tuple(config["view_order"])
    pairs: list[tuple[str, str]] = []
    locations: list[tuple[int, int, int]] = []
    for example_index, example in enumerate(examples):
        for tool_index, texts in enumerate(example["views"]):
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
    matrices = [
        np.zeros((len(example["tool_names"]), len(fields)), dtype=np.float64)
        for example in examples
    ]
    for value, location in zip(values, locations, strict=True):
        example_index, tool_index, field_index = location
        matrices[example_index][tool_index, field_index] = float(value)
    return matrices, len(pairs)


def compute_method_scores(matrix: np.ndarray) -> dict[str, np.ndarray]:
    full = matrix[:, 0]
    without_operation = matrix[:, 1]
    without_arguments = matrix[:, 2]
    operation_drop = full - without_operation
    argument_drop = full - without_arguments
    return {
        "full_schema": full.copy(),
        "operation_schema": without_arguments.copy(),
        "argument_schema": without_operation.copy(),
        "additive_support": full + 0.5 * (operation_drop + argument_drop),
        "max_support": full + np.maximum(operation_drop, argument_drop),
        "dual_necessity": full + np.minimum(operation_drop, argument_drop),
    }


def tie_digest(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def ranking(names: list[str], scores: np.ndarray) -> list[int]:
    return sorted(
        range(len(scores)),
        key=lambda index: (-float(scores[index]), tie_digest(names[index])),
    )


def query_records(
    examples: list[dict[str, Any]],
    raw_features: list[np.ndarray],
    phase: str,
) -> list[dict[str, Any]]:
    records = []
    fields = ("full", "without_operation", "without_arguments", "name_only")
    for example, matrix in zip(examples, raw_features, strict=True):
        scores = compute_method_scores(matrix)
        gold = set(example["gold_names"])
        methods = {}
        for method in METHODS:
            order = ranking(example["tool_names"], scores[method])
            first_gold = next(
                position
                for position, tool_index in enumerate(order, 1)
                if example["tool_names"][tool_index] in gold
            )
            methods[method] = {
                "ranking": [example["tool_names"][index] for index in order],
                "top1_correct": example["tool_names"][order[0]] in gold,
                "reciprocal_rank": 1.0 / first_gold,
            }
        tools = []
        for index, name in enumerate(example["tool_names"]):
            full = float(matrix[index, 0])
            operation_drop = full - float(matrix[index, 1])
            argument_drop = full - float(matrix[index, 2])
            tools.append(
                {
                    "tool_name": name,
                    "is_gold": name in gold,
                    "view_texts": example["views"][index],
                    "view_scores": {
                        field: float(matrix[index, field_index])
                        for field_index, field in enumerate(fields)
                    },
                    "operation_drop": operation_drop,
                    "argument_drop": argument_drop,
                    "method_scores": {
                        method: float(scores[method][index]) for method in METHODS
                    },
                }
            )
        records.append(
            {
                "phase": phase,
                "query_id": example["query_id"],
                "query": example["query"],
                "query_sha256": example["query_sha256"],
                "fold": example["fold"],
                "gold_names": example["gold_names"],
                "methods": methods,
                "tools": tools,
            }
        )
    return records


def metrics(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
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


def bootstrap(
    records: list[dict[str, Any]],
    candidate: str,
    comparator: str,
    repeats: int,
    seed: int,
) -> dict[str, Any]:
    candidate_top1 = np.asarray(
        [record["methods"][candidate]["top1_correct"] for record in records],
        dtype=np.float64,
    )
    comparator_top1 = np.asarray(
        [record["methods"][comparator]["top1_correct"] for record in records],
        dtype=np.float64,
    )
    candidate_mrr = np.asarray(
        [record["methods"][candidate]["reciprocal_rank"] for record in records],
        dtype=np.float64,
    )
    comparator_mrr = np.asarray(
        [record["methods"][comparator]["reciprocal_rank"] for record in records],
        dtype=np.float64,
    )
    rng = np.random.default_rng(seed)
    top_samples = np.empty(repeats, dtype=np.float64)
    mrr_samples = np.empty(repeats, dtype=np.float64)
    for repeat in range(repeats):
        indexes = rng.integers(0, len(records), size=len(records))
        top_samples[repeat] = np.mean(
            candidate_top1[indexes] - comparator_top1[indexes]
        )
        mrr_samples[repeat] = np.mean(
            candidate_mrr[indexes] - comparator_mrr[indexes]
        )
    return {
        "comparator": comparator,
        "top1_point": float(np.mean(candidate_top1 - comparator_top1)),
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


def corrections(
    records: list[dict[str, Any]], candidate: str, comparator: str
) -> dict[str, int]:
    candidate_values = [
        bool(record["methods"][candidate]["top1_correct"]) for record in records
    ]
    comparator_values = [
        bool(record["methods"][comparator]["top1_correct"]) for record in records
    ]
    return {
        "corrections": sum(
            candidate_value and not comparator_value
            for candidate_value, comparator_value in zip(
                candidate_values, comparator_values, strict=True
            )
        ),
        "regressions": sum(
            comparator_value and not candidate_value
            for candidate_value, comparator_value in zip(
                candidate_values, comparator_values, strict=True
            )
        ),
    }


def development_summary(
    records: list[dict[str, Any]], config: dict[str, Any]
) -> dict[str, Any]:
    metric = metrics(records)
    strongest = max(
        COMPARATORS,
        key=lambda name: (metric[name]["top1"], metric[name]["mrr"], name),
    )
    delta = bootstrap(
        records,
        METHODS[-1],
        strongest,
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    vs_full = corrections(records, METHODS[-1], "full_schema")
    fold_slices = {}
    for fold in range(int(config["query_fold_modulus"])):
        subset = [record for record in records if int(record["fold"]) == fold]
        subset_metrics = metrics(subset)
        fold_slices[str(fold)] = {
            "queries": len(subset),
            "candidate_mrr": subset_metrics[METHODS[-1]]["mrr"],
            "strongest_mrr": subset_metrics[strongest]["mrr"],
            "mrr_delta": (
                subset_metrics[METHODS[-1]]["mrr"]
                - subset_metrics[strongest]["mrr"]
            ),
        }
    positive_folds = sum(
        value["mrr_delta"] > 0.0 for value in fold_slices.values()
    )
    candidate = metric[METHODS[-1]]
    gate_config = config["development_gates"]
    gates = {
        "candidate_top1": candidate["top1"]
        >= float(gate_config["candidate_top1_min"]),
        "top1_delta_vs_full": (
            candidate["top1"] - metric["full_schema"]["top1"]
        )
        >= float(gate_config["top1_delta_vs_full_min"]),
        "strictly_beats_every_comparator_top1": all(
            candidate["top1"] > metric[name]["top1"] for name in COMPARATORS
        ),
        "mrr_bootstrap_lower_vs_strongest": delta["mrr_bootstrap_95"][0] > 0.0,
        "positive_net_corrections_vs_full": vs_full["corrections"]
        > vs_full["regressions"],
        "all_fold_mrr_deltas_nonnegative": all(
            value["mrr_delta"] >= 0.0 for value in fold_slices.values()
        ),
        "minimum_positive_folds": positive_folds
        >= int(gate_config["minimum_positive_folds"]),
    }
    return {
        "phase": "development",
        "evaluation": "fixed_formula_with_five_query_hash_slices",
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


def confirmation_summary(
    records: list[dict[str, Any]],
    development: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    metric = metrics(records)
    strongest = str(development["strongest_comparator"])
    delta = bootstrap(
        records,
        METHODS[-1],
        strongest,
        int(config["bootstrap_repeats"]),
        int(config["seed"]),
    )
    changes = corrections(records, METHODS[-1], strongest)
    candidate = metric[METHODS[-1]]
    gates = {
        "candidate_top1_above_frozen_strongest": candidate["top1"]
        > metric[strongest]["top1"],
        "candidate_mrr_above_frozen_strongest": candidate["mrr"]
        > metric[strongest]["mrr"],
        "top1_bootstrap_lower_nonnegative": delta["top1_bootstrap_95"][0] >= 0.0,
        "positive_net_corrections": changes["corrections"]
        > changes["regressions"],
        "strictly_beats_every_comparator_top1": all(
            candidate["top1"] > metric[name]["top1"] for name in COMPARATORS
        ),
        "query_hashes_disjoint": True,
    }
    return {
        "phase": "confirmation",
        "evaluation": "fixed_formula",
        "metrics": metric,
        "strongest_comparator": strongest,
        "candidate_minus_strongest": delta,
        "corrections": changes,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
    }


def environment(elapsed: float) -> dict[str, Any]:
    return {
        "python_executable": sys.executable,
        "python": platform.python_version(),
        "numpy": np.__version__,
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
    parser.add_argument("--development-summary", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    started = time.perf_counter()
    config = read_json(args.config)
    config_sha256 = sha256_path(args.config)
    if config["experiment_id"] != "v029":
        raise ValueError("config experiment identity mismatch")
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
        development = None
    else:
        if args.input_manifest is None or args.development_summary is None:
            raise ValueError(
                "Confirmation requires acquisition manifest and Development summary"
            )
        manifest = read_json(args.input_manifest)
        if (
            manifest["phase"] != "confirmation"
            or manifest["config_sha256"] != config_sha256
            or manifest["questions_sha256"] != sha256_path(args.questions)
            or manifest["gold_sha256"] != sha256_path(args.gold)
        ):
            raise ValueError("Confirmation manifest identity mismatch")
        development = read_json(args.development_summary)
        if (
            development.get("experiment_id") != "v029"
            or development.get("config_sha256") != config_sha256
            or development.get("candidate_sha256") != config["candidate_sha256"]
            or development.get("evidence_packet_sha256")
            != config["evidence_packet_sha256"]
            or tuple(development.get("methods", ())) != METHODS
        ):
            raise ValueError("Development summary identity mismatch")
    model_files = verify_model(args.model_dir, config)
    examples = prepare_examples(
        read_jsonl(args.expanded),
        read_jsonl(args.questions),
        read_jsonl(args.gold),
        int(config["query_fold_modulus"]),
    )
    if development is not None:
        overlap = sorted(
            set(example["query_sha256"] for example in examples)
            & set(development["query_hashes"])
        )
        if overlap:
            raise ValueError("Development/Confirmation normalized-query hash overlap")
    model = CrossEncoder(
        str(args.model_dir), device=str(config["device"]), local_files_only=True
    )
    raw_features, inference_pairs = score_views(examples, model, config)
    records = query_records(examples, raw_features, args.phase)
    if args.phase == "development":
        summary = development_summary(records, config)
    else:
        assert development is not None
        summary = confirmation_summary(records, development, config)
        summary["development_query_overlap"] = []
    args.output_dir.mkdir(parents=True, exist_ok=False)
    write_jsonl(args.output_dir / "raw.jsonl", records)
    query_hashes = sorted(example["query_sha256"] for example in examples)
    write_json(args.output_dir / "query_hashes.json", query_hashes)
    env = environment(time.perf_counter() - started)
    write_json(args.output_dir / "environment.json", env)
    summary.update(
        {
            "schema_version": 1,
            "experiment_id": "v029",
            "methods": METHODS,
            "queries": len(examples),
            "tools": sum(len(example["tool_names"]) for example in examples),
            "config_sha256": config_sha256,
            "candidate_sha256": sha256_path(args.candidate),
            "evidence_packet_sha256": sha256_path(args.evidence_packet),
            "expanded_sha256": sha256_path(args.expanded),
            "questions_sha256": sha256_path(args.questions),
            "gold_sha256": sha256_path(args.gold),
            "model_files": model_files,
            "cross_encoder_pairs": inference_pairs,
            "query_hashes": query_hashes,
            "raw_sha256": sha256_path(args.output_dir / "raw.jsonl"),
            "query_hashes_sha256": sha256_path(
                args.output_dir / "query_hashes.json"
            ),
            "environment_sha256": sha256_path(args.output_dir / "environment.json"),
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
