from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize
import torch
import transformers
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def question_text(row: dict[str, object]) -> str:
    return "\n".join(
        str(message["content"])
        for group in row["question"]
        for message in group
        if message.get("role") == "user"
    )


def gold_names(row: dict[str, object]) -> tuple[str, ...]:
    return tuple(sorted({name for call in row["ground_truth"] for name in call}))


def tool_parameter_schema(
    tool: dict[str, object],
) -> tuple[dict[str, dict[str, object]], list[str]]:
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
                raise ValueError(
                    f"Cannot resolve embedded required parameter {name} for {tool['name']}"
                )
            properties[name] = matches[0]
    if any(not isinstance(value, dict) for value in properties.values()):
        raise ValueError(f"Non-object parameter schema for {tool['name']}")
    return properties, required


def schema_text(tool: dict[str, object]) -> str:
    properties, required_names = tool_parameter_schema(tool)
    required = set(required_names)
    fields = [
        f"function name: {tool['name']}",
        f"function description: {tool.get('description', '')}",
    ]
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


def stable_ranking(names: list[str], scores: np.ndarray) -> list[str]:
    return [
        names[index]
        for index in sorted(
            range(len(names)),
            key=lambda index: (
                -float(scores[index]),
                sha256_bytes(names[index].encode("utf-8")),
            ),
        )
    ]


def item_metrics(
    rankings: list[list[str]], gold: list[tuple[str, ...]]
) -> tuple[np.ndarray, np.ndarray]:
    accuracy: list[float] = []
    reciprocal_rank: list[float] = []
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
    items: list[dict[str, object]] = []
    for expanded in expanded_rows:
        item_id = str(expanded["id"])
        if item_id not in questions or item_id not in gold:
            raise ValueError(f"Unaligned id: {item_id}")
        query = question_text(questions[item_id])
        if question_text(expanded) != query:
            raise ValueError(f"Question mismatch for {item_id}")
        tools = list(expanded["function"])
        names = [str(tool["name"]) for tool in tools]
        if len(names) != len(set(names)):
            raise ValueError(f"Duplicate function name for {item_id}")
        accepted = gold_names(gold[item_id])
        if not set(accepted).issubset(names):
            raise ValueError(f"Gold function missing from menu for {item_id}")
        thin_names = {str(tool["name"]) for tool in questions[item_id]["function"]}
        if not thin_names.issubset(names):
            raise ValueError(f"Thin function missing from expanded menu for {item_id}")
        items.append(
            {
                "id": item_id,
                "query": query,
                "query_sha256": sha256_bytes(query.encode("utf-8")),
                "tools": tools,
                "names": names,
                "gold": accepted,
                "thin_names": tuple(sorted(thin_names)),
                "related_names": tuple(sorted(set(names) - thin_names)),
            }
        )
    if len(items) != len(questions) or len(items) != len(gold):
        raise ValueError("Input files do not contain the same ids")
    return items


def encode_cross_features(
    items: list[dict[str, object]],
    model_path: Path,
    *,
    device: str,
    batch_size: int,
    max_length: int,
) -> int:
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_path, local_files_only=True
    )
    model.to(device)
    model.eval()
    records: list[tuple[int, int, str, str]] = []
    for item_index, item in enumerate(items):
        for tool_index, tool in enumerate(item["tools"]):
            records.append(
                (item_index, tool_index, str(item["query"]), schema_text(tool))
            )
    logits: list[np.ndarray] = []
    vectors: list[np.ndarray] = []
    with torch.inference_mode():
        for start in range(0, len(records), batch_size):
            batch = records[start : start + batch_size]
            encoded = tokenizer(
                [record[2] for record in batch],
                [record[3] for record in batch],
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt",
            )
            encoded = {name: value.to(device) for name, value in encoded.items()}
            output = model(
                **encoded, output_hidden_states=True, return_dict=True
            )
            logits.append(output.logits.detach().float().cpu().numpy().reshape(-1))
            vectors.append(
                output.hidden_states[-1][:, 0, :]
                .detach()
                .float()
                .cpu()
                .numpy()
            )
    all_logits = np.concatenate(logits)
    all_vectors = np.concatenate(vectors)
    cursor = 0
    for item in items:
        count = len(item["names"])
        item["cross_scores"] = all_logits[cursor : cursor + count].astype(
            np.float64
        )
        item["vectors"] = all_vectors[cursor : cursor + count].astype(np.float64)
        cursor += count
    return int(all_vectors.shape[1])


def pair_records(
    items: list[dict[str, object]], indices: list[int]
) -> tuple[np.ndarray, np.ndarray, int]:
    margins: list[float] = []
    differences: list[np.ndarray] = []
    rows_used = 0
    for item_index in indices:
        item = items[item_index]
        names = item["names"]
        gold_indices = [names.index(name) for name in item["gold"]]
        related_indices = [
            names.index(name)
            for name in item["related_names"]
            if name not in item["gold"]
        ]
        if not gold_indices or not related_indices:
            continue
        rows_used += 1
        for gold_index in gold_indices:
            for negative_index in related_indices:
                margins.append(
                    float(
                        item["cross_scores"][gold_index]
                        - item["cross_scores"][negative_index]
                    )
                )
                differences.append(
                    item["vectors"][gold_index] - item["vectors"][negative_index]
                )
    if not differences:
        raise ValueError("No related-negative training pairs")
    return np.asarray(margins), np.asarray(differences), rows_used


def fit_unanchored_adapter(
    base_margins: np.ndarray,
    differences: np.ndarray,
    dimension: int,
    *,
    l2: float,
    maxiter: int,
) -> tuple[np.ndarray, dict[str, object]]:
    def objective(vector: np.ndarray) -> tuple[float, np.ndarray]:
        margins = base_margins + differences @ vector
        loss = float(np.logaddexp(0.0, -margins).mean())
        gradient_weights = -1.0 / (1.0 + np.exp(np.clip(margins, -60.0, 60.0)))
        gradient = (differences.T @ gradient_weights) / len(margins)
        return loss + 0.5 * l2 * float(vector @ vector), gradient + l2 * vector

    result = minimize(
        objective,
        np.zeros(dimension, dtype=np.float64),
        method="L-BFGS-B",
        jac=True,
        options={"maxiter": maxiter, "ftol": 1e-12, "gtol": 1e-8},
    )
    if not result.success:
        raise RuntimeError(f"Adapter optimization failed: {result.message}")
    return np.asarray(result.x), {
        "success": bool(result.success),
        "iterations": int(result.nit),
        "objective": float(result.fun),
        "gradient_max_abs": float(np.max(np.abs(result.jac))),
    }


def anchor_scale(
    items: list[dict[str, object]],
    indices: list[int],
    vector: np.ndarray,
    *,
    retained_fraction: float,
) -> tuple[float, dict[str, object]]:
    limits: list[float] = []
    constrained_pairs = 0
    constrained_rows = 0
    for item_index in indices:
        item = items[item_index]
        names = item["names"]
        thin_indices = [names.index(name) for name in item["thin_names"]]
        thin_gold = [index for index in thin_indices if names[index] in item["gold"]]
        thin_negative = [
            index for index in thin_indices if names[index] not in item["gold"]
        ]
        if not thin_gold or not thin_negative:
            continue
        base_ranking = stable_ranking(
            [names[index] for index in thin_indices],
            item["cross_scores"][thin_indices],
        )
        if base_ranking[0] not in item["gold"]:
            continue
        constrained_rows += 1
        for gold_index in thin_gold:
            for negative_index in thin_negative:
                base_margin = float(
                    item["cross_scores"][gold_index]
                    - item["cross_scores"][negative_index]
                )
                if base_margin <= 0.0:
                    continue
                residual_margin = float(
                    (item["vectors"][gold_index] - item["vectors"][negative_index])
                    @ vector
                )
                constrained_pairs += 1
                if residual_margin < 0.0:
                    limits.append(
                        (1.0 - retained_fraction)
                        * base_margin
                        / (-residual_margin)
                    )
    scale = min(1.0, min(limits)) if limits else 1.0
    if scale < 0.0 or not math.isfinite(scale):
        raise ValueError("Invalid anchor scale")
    return float(scale), {
        "constrained_rows": constrained_rows,
        "constrained_pairs": constrained_pairs,
        "active_limits": len(limits),
        "minimum_limit": float(min(limits)) if limits else None,
        "retained_fraction": retained_fraction,
    }


def score_items(
    items: list[dict[str, object]],
    indices: list[int],
    vector: np.ndarray,
) -> dict[int, np.ndarray]:
    return {
        index: items[index]["cross_scores"] + items[index]["vectors"] @ vector
        for index in indices
    }


def make_folds(items: list[dict[str, object]], folds: int) -> list[list[int]]:
    result = [[] for _ in range(folds)]
    for index, item in enumerate(items):
        fold = int(str(item["query_sha256"])[:16], 16) % folds
        result[fold].append(index)
    if any(not group for group in result):
        raise ValueError("A grouped fold is empty")
    return result


def metric_record(
    rankings: list[list[str]], gold: list[tuple[str, ...]]
) -> dict[str, object]:
    accuracy, mrr = item_metrics(rankings, gold)
    return {
        "accuracy": float(accuracy.mean()),
        "mrr": float(mrr.mean()),
        "accuracy_items": accuracy,
        "mrr_items": mrr,
    }


def serializable_metric(record: dict[str, object]) -> dict[str, float]:
    return {"accuracy": float(record["accuracy"]), "mrr": float(record["mrr"])}


def comparison(
    candidate: dict[str, object],
    baseline: dict[str, object],
    *,
    repeats: int,
    seed: int,
) -> dict[str, object]:
    accuracy_delta = candidate["accuracy_items"] - baseline["accuracy_items"]
    mrr_delta = candidate["mrr_items"] - baseline["mrr_items"]
    return {
        "accuracy": float(accuracy_delta.mean()),
        "mrr": float(mrr_delta.mean()),
        "accuracy_bootstrap_95": bootstrap_interval(
            accuracy_delta, repeats, seed
        ),
        "mrr_bootstrap_95": bootstrap_interval(mrr_delta, repeats, seed + 1),
        "corrections": int(np.sum(accuracy_delta == 1.0)),
        "regressions": int(np.sum(accuracy_delta == -1.0)),
    }


def environment_record(
    model_path: Path, config: dict[str, object], elapsed: float
) -> dict[str, object]:
    return {
        "python_executable": sys.executable,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
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
        )
        .stdout.strip()
        .splitlines()[0],
        "device": config["device"],
        "seed": config["seed"],
        "elapsed_seconds": elapsed,
        "cross_model_manifest": model_manifest(model_path),
    }


def main() -> int:
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
    started = time.perf_counter()
    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
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
    model_path = Path(config["cross_model_path"]).resolve()
    dimension = encode_cross_features(
        items,
        model_path,
        device=str(config["device"]),
        batch_size=int(config["batch_size"]),
        max_length=int(config["max_length"]),
    )
    baseline_rankings = [
        stable_ranking(item["names"], item["cross_scores"]) for item in items
    ]
    fold_records: list[dict[str, object]] = []
    unanchored_scores: dict[int, np.ndarray] = {}
    anchored_scores: dict[int, np.ndarray] = {}
    if args.phase == "development":
        folds = make_folds(items, int(config["folds"]))
        all_indices = set(range(len(items)))
        for fold_index, heldout in enumerate(folds):
            train = sorted(all_indices - set(heldout))
            margins, differences, rows_used = pair_records(items, train)
            unanchored, optimization = fit_unanchored_adapter(
                margins,
                differences,
                dimension,
                l2=float(config["l2"]),
                maxiter=int(config["optimizer_maxiter"]),
            )
            scale, anchor = anchor_scale(
                items,
                train,
                unanchored,
                retained_fraction=float(config["anchor_margin_fraction"]),
            )
            unanchored_scores.update(score_items(items, heldout, unanchored))
            anchored_scores.update(score_items(items, heldout, scale * unanchored))
            fold_records.append(
                {
                    "fold": fold_index,
                    "train_rows": len(train),
                    "heldout_rows": len(heldout),
                    "related_pair_rows": rows_used,
                    "related_pairs": len(margins),
                    "optimization": optimization,
                    "anchor": anchor,
                    "anchor_scale": scale,
                    "unanchored_vector_norm": float(np.linalg.norm(unanchored)),
                }
            )
        full_margins, full_differences, full_rows_used = pair_records(
            items, list(range(len(items)))
        )
        full_unanchored, full_optimization = fit_unanchored_adapter(
            full_margins,
            full_differences,
            dimension,
            l2=float(config["l2"]),
            maxiter=int(config["optimizer_maxiter"]),
        )
        full_scale, full_anchor = anchor_scale(
            items,
            list(range(len(items))),
            full_unanchored,
            retained_fraction=float(config["anchor_margin_fraction"]),
        )
        selected = {
            "dimension": dimension,
            "unanchored_vector": full_unanchored.tolist(),
            "anchor_scale": full_scale,
            "anchored_vector": (full_scale * full_unanchored).tolist(),
            "related_pair_rows": full_rows_used,
            "related_pairs": len(full_margins),
            "optimization": full_optimization,
            "anchor": full_anchor,
        }
    else:
        if not args.selected_params or not args.development_query_hashes:
            raise ValueError("Confirmation requires frozen Development parameters and hashes")
        selected = json.loads(Path(args.selected_params).read_text(encoding="utf-8"))[
            "adapter"
        ]
        unanchored = np.asarray(selected["unanchored_vector"], dtype=np.float64)
        anchored = np.asarray(selected["anchored_vector"], dtype=np.float64)
        if len(unanchored) != dimension or len(anchored) != dimension:
            raise ValueError("Frozen adapter dimension does not match model")
        indices = list(range(len(items)))
        unanchored_scores.update(score_items(items, indices, unanchored))
        anchored_scores.update(score_items(items, indices, anchored))
    unanchored_rankings = [
        stable_ranking(item["names"], unanchored_scores[index])
        for index, item in enumerate(items)
    ]
    anchored_rankings = [
        stable_ranking(item["names"], anchored_scores[index])
        for index, item in enumerate(items)
    ]
    gold = [item["gold"] for item in items]
    baseline_metrics = metric_record(baseline_rankings, gold)
    unanchored_metrics = metric_record(unanchored_rankings, gold)
    anchored_metrics = metric_record(anchored_rankings, gold)
    repeats = int(config["bootstrap_repeats"])
    seed = int(config["seed"])
    anchored_delta = comparison(
        anchored_metrics, baseline_metrics, repeats=repeats, seed=seed
    )
    unanchored_delta = comparison(
        unanchored_metrics, baseline_metrics, repeats=repeats, seed=seed + 10
    )
    query_hashes = sorted(str(item["query_sha256"]) for item in items)
    overlap: list[str] = []
    if args.phase == "confirmation":
        development_hashes = set(
            json.loads(
                Path(args.development_query_hashes).read_text(encoding="utf-8")
            )
        )
        overlap = sorted(development_hashes.intersection(query_hashes))
    if args.phase == "development":
        gates = {
            "top1_delta_at_least_0_02": anchored_delta["accuracy"] >= 0.02,
            "mrr_bootstrap_lower_above_zero": anchored_delta[
                "mrr_bootstrap_95"
            ][0]
            > 0.0,
            "net_corrections_positive": anchored_delta["corrections"]
            > anchored_delta["regressions"],
            "anchor_reduces_regressions": anchored_delta["regressions"]
            < unanchored_delta["regressions"],
            "anchor_retains_at_least_three_quarters_of_corrections": anchored_delta[
                "corrections"
            ]
            * 4
            >= unanchored_delta["corrections"] * 3,
        }
    else:
        gates = {
            "query_hashes_disjoint": not overlap,
            "top1_delta_positive": anchored_delta["accuracy"] > 0.0,
            "mrr_delta_positive": anchored_delta["mrr"] > 0.0,
            "top1_bootstrap_lower_nonnegative": anchored_delta[
                "accuracy_bootstrap_95"
            ][0]
            >= 0.0,
            "net_corrections_positive": anchored_delta["corrections"]
            > anchored_delta["regressions"],
            "anchor_regressions_no_more_than_unanchored": anchored_delta[
                "regressions"
            ]
            <= unanchored_delta["regressions"],
        }
    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=False)
    with (output / "raw.jsonl").open(
        "w", encoding="utf-8", newline="\n"
    ) as stream:
        for index, item in enumerate(items):
            tools = []
            for tool_index, tool in enumerate(item["tools"]):
                tools.append(
                    {
                        "name": item["names"][tool_index],
                        "schema": schema_text(tool),
                        "cross_encoder_logit": float(
                            item["cross_scores"][tool_index]
                        ),
                        "cls_vector": item["vectors"][tool_index].tolist(),
                        "unanchored_score": float(
                            unanchored_scores[index][tool_index]
                        ),
                        "anchored_score": float(
                            anchored_scores[index][tool_index]
                        ),
                        "is_thin_tool": item["names"][tool_index]
                        in item["thin_names"],
                        "is_related_added_tool": item["names"][tool_index]
                        in item["related_names"],
                    }
                )
            stream.write(
                json.dumps(
                    {
                        "id": item["id"],
                        "query": item["query"],
                        "query_sha256": item["query_sha256"],
                        "gold": item["gold"],
                        "thin_names": item["thin_names"],
                        "related_names": item["related_names"],
                        "rankings": {
                            "cross_encoder": baseline_rankings[index],
                            "unanchored_related_adapter": unanchored_rankings[
                                index
                            ],
                            "thin_anchor_adapter": anchored_rankings[index],
                        },
                        "tools": tools,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )
    (output / "selected_params.json").write_text(
        json.dumps(
            {"adapter": selected, "folds": fold_records},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output / "query_hashes.json").write_text(
        json.dumps(query_hashes, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    summary = {
        "phase": args.phase,
        "items": len(items),
        "input_sha256": {
            name: sha256_file(path) for name, path in input_paths.items()
        },
        "config_sha256": sha256_file(config_path),
        "metrics": {
            "cross_encoder": serializable_metric(baseline_metrics),
            "unanchored_related_adapter": serializable_metric(
                unanchored_metrics
            ),
            "thin_anchor_adapter": serializable_metric(anchored_metrics),
        },
        "unanchored_minus_cross_encoder": unanchored_delta,
        "thin_anchor_minus_cross_encoder": anchored_delta,
        "development_query_hash_overlap": overlap,
        "gates": gates,
        "all_gates_passed": all(gates.values()),
        "folds": fold_records,
        "elapsed_seconds": time.perf_counter() - started,
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output / "environment.json").write_text(
        json.dumps(
            environment_record(
                model_path, config, time.perf_counter() - started
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "phase": args.phase,
                "items": len(items),
                "baseline_top1": baseline_metrics["accuracy"],
                "unanchored_top1": unanchored_metrics["accuracy"],
                "anchored_top1": anchored_metrics["accuracy"],
                "anchored_delta": anchored_delta["accuracy"],
                "all_gates_passed": all(gates.values()),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
