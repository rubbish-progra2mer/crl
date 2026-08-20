from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import random
import sys
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import sklearn
import torch
import transformers
from sklearn.linear_model import LogisticRegression
from transformers import AutoModelForCausalLM, AutoTokenizer


OBLIGATIONS = ("mode", "tool", "arguments", "grounding", "progress")
PROMPT_KINDS = (*OBLIGATIONS, "holistic")
SYSTEM_PROMPT = (
    "You evaluate exactly one candidate next action in a tool-using interaction. "
    "Use only the supplied evidence. Do not compare against an unseen alternative. "
    "Answer only Yes or No."
)
INSTRUCTIONS = {
    "mode": (
        "Decide whether the candidate uses the correct next interaction mode: a tool "
        "call when execution is needed, or a natural-language response when asking, "
        "clarifying, reporting, or finishing is appropriate. If mode is correct, answer Yes."
    ),
    "tool": (
        "Decide whether the candidate's selected tool exists and is the functionally "
        "appropriate next operation. For a correct non-tool response this obligation is "
        "inapplicable and must be Yes."
    ),
    "arguments": (
        "Decide whether a structured call obeys its matched schema: parameter names, "
        "required fields, types, enums, and explicit constraints. For a non-tool response "
        "this obligation is inapplicable and must be Yes."
    ),
    "grounding": (
        "Decide whether argument values and factual assertions are supported by the user "
        "and prior tool evidence, preserve exact required content, and do not invent state. "
        "If no factual value is asserted, answer Yes."
    ),
    "progress": (
        "Decide whether the action respects prerequisites and ordering, responds to prior "
        "failures, avoids unjustified repetition or premature completion, and makes correct "
        "progress toward the request."
    ),
    "holistic": (
        "Considering the complete supplied history, tool metadata, and candidate action, "
        "decide whether this is a correct next action for completing the user's task."
    ),
}
METHODS = (
    "cccb",
    "holistic",
    "mode",
    "tool",
    "arguments",
    "grounding",
    "progress",
    "raw_min",
    "calibrated_mean",
    "calibrated_product",
    "pair_majority",
    "selected_single",
    "linear_ensemble",
)
COMPARATORS = tuple(name for name in METHODS if name != "cccb")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_text(value: Any) -> str:
    if isinstance(value, str):
        return value.replace("\r\n", "\n").replace("\r", "\n")
    return canonical_json(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=("development", "confirmation"))
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--evidence-packet", required=True, type=Path)
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--model-manifest", required=True, type=Path)
    parser.add_argument("--dataset", action="append", required=True)
    parser.add_argument("--frozen-state", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def parse_dataset_args(items: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"dataset must be source=path: {item}")
        source, raw_path = item.split("=", 1)
        source = source.strip().lower()
        if not source or source in result:
            raise ValueError(f"invalid or duplicate dataset source: {source}")
        result[source] = Path(raw_path).resolve()
    return result


def iter_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def call_from_object(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    nested = value.get("function")
    if isinstance(nested, dict) and isinstance(nested.get("name"), str):
        return {
            "name": nested["name"],
            "arguments": nested.get("arguments", nested.get("parameters", {})),
        }
    if isinstance(value.get("api_name"), str):
        return {"name": value["api_name"], "arguments": value.get("parameters", {})}
    if isinstance(value.get("name"), str) and any(
        key in value for key in ("parameters", "arguments")
    ):
        return {
            "name": value["name"],
            "arguments": value.get("parameters", value.get("arguments", {})),
        }
    return None


def extract_call(action: Any) -> dict[str, Any] | None:
    direct = call_from_object(action)
    if direct is not None:
        return direct
    if not isinstance(action, str):
        return None
    decoder = json.JSONDecoder()
    candidates: list[tuple[int, int, dict[str, Any]]] = []
    for position, char in enumerate(action):
        if char != "{":
            continue
        try:
            value, consumed = decoder.raw_decode(action[position:])
        except json.JSONDecodeError:
            continue
        call = call_from_object(value)
        if call is not None:
            candidates.append((position, consumed, call))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[1], item[0]))
    return candidates[-1][2]


def schema_name_candidates(item: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for key in ("name", "api_name"):
        value = item.get(key)
        if isinstance(value, str):
            names.append(value)
    values = item.get("api_names")
    if isinstance(values, list):
        names.extend(str(value) for value in values)
    return names


def find_matching_schema(functions: Any, name: str) -> dict[str, Any] | None:
    target = name.casefold()
    for item in iter_dicts(functions):
        if any(candidate.casefold() == target for candidate in schema_name_candidates(item)):
            return item
    return None


def history_system_text(history: Any) -> str:
    pieces: list[str] = []
    if isinstance(history, list):
        for message in history:
            if isinstance(message, dict) and message.get("role") == "system":
                pieces.append(stable_text(message.get("content", "")))
    return "\n".join(pieces)


def available_summary(functions: Any, fallback: str) -> str:
    if functions is None:
        return fallback
    records: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for item in iter_dicts(functions):
        names = tuple(schema_name_candidates(item))
        if not names or names in seen:
            continue
        seen.add(names)
        description = item.get("description", "")
        records.append(
            {
                "names": list(names),
                "description": stable_text(description)[:1000],
            }
        )
    return canonical_json(records)


def row_identity(source: str, index: int, row: dict[str, Any]) -> tuple[str, str]:
    if source == "bfcl":
        natural = str(row["sample_id"])
    else:
        natural = str(row.get("task", row.get("sample_id", row.get("index", index))))
    row_id = f"{source}:{index:04d}"
    cluster = f"{source}:{natural}"
    return row_id, cluster


def build_evidence(source: str, index: int, row: dict[str, Any], action: Any) -> dict[str, str]:
    history = row["history"]
    functions = row.get("functions")
    action_text = stable_text(action)
    system_fallback = history_system_text(history)
    full_schema = stable_text(functions) if functions is not None else system_fallback
    call = extract_call(action)
    if call is None:
        matched_schema = "NO_STRUCTURED_TOOL_CALL"
        call_text = "NO_STRUCTURED_TOOL_CALL"
    else:
        match = find_matching_schema(functions, call["name"]) if functions is not None else None
        matched_schema = (
            stable_text(match)
            if match is not None
            else "NO_EXACT_MATCH; EMBEDDED_OR_AVAILABLE_SCHEMA:\n" + full_schema
        )
        call_text = canonical_json(call)
    return {
        "source": source,
        "history": stable_text(history),
        "full_schema": full_schema,
        "available": available_summary(functions, system_fallback),
        "action": action_text,
        "call": call_text,
        "matched_schema": matched_schema,
    }


def evidence_sections(kind: str, evidence: dict[str, str]) -> list[tuple[str, str]]:
    if kind in ("mode", "tool"):
        return [("HISTORY", evidence["history"]), ("AVAILABLE_TOOLS", evidence["available"])]
    if kind == "arguments":
        return [("MATCHED_SCHEMA", evidence["matched_schema"])]
    if kind in ("grounding", "progress"):
        return [
            ("HISTORY", evidence["history"]),
            ("MATCHED_SCHEMA", evidence["matched_schema"]),
        ]
    if kind == "holistic":
        return [("HISTORY", evidence["history"]), ("TOOL_METADATA", evidence["full_schema"])]
    raise KeyError(kind)


def clip_token_ids(tokenizer: Any, token_ids: list[int], budget: int) -> str:
    if len(token_ids) <= budget:
        return tokenizer.decode(token_ids, skip_special_tokens=False)
    marker = tokenizer.encode("\n[...DETERMINISTIC_HEAD_TAIL_TRUNCATION...]\n", add_special_tokens=False)
    if budget <= len(marker) + 2:
        return tokenizer.decode(token_ids[:budget], skip_special_tokens=False)
    keep = budget - len(marker)
    head = (keep + 1) // 2
    tail = keep - head
    clipped = token_ids[:head] + marker + (token_ids[-tail:] if tail else [])
    return tokenizer.decode(clipped, skip_special_tokens=False)


def allocate_budgets(lengths: list[int], total: int) -> list[int]:
    budgets = [0] * len(lengths)
    active = set(range(len(lengths)))
    remaining = total
    while active and remaining > 0:
        share = max(1, remaining // len(active))
        progressed = False
        for index in list(active):
            need = lengths[index] - budgets[index]
            take = min(share, need, remaining)
            budgets[index] += take
            remaining -= take
            if budgets[index] >= lengths[index]:
                active.remove(index)
            progressed = progressed or take > 0
        if not progressed:
            break
    return budgets


def make_prompt(tokenizer: Any, kind: str, evidence: dict[str, str], cap: int) -> tuple[str, int]:
    action_block = f"CANDIDATE_ACTION:\n{evidence['action']}"
    sections = evidence_sections(kind, evidence)

    def render(section_values: list[str]) -> str:
        blocks = [f"OBLIGATION:\n{INSTRUCTIONS[kind]}", action_block]
        blocks.extend(
            f"{name}:\n{value}" for (name, _), value in zip(sections, section_values, strict=True)
        )
        user = "\n\n".join(blocks)
        return tokenizer.apply_chat_template(
            [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}],
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )

    empty_prompt = render(["" for _ in sections])
    fixed_tokens = len(tokenizer.encode(empty_prompt, add_special_tokens=False))
    if fixed_tokens >= cap:
        raise ValueError(f"untruncated action and instruction exceed prompt cap: {fixed_tokens}")
    encoded_sections = [
        tokenizer.encode(value, add_special_tokens=False) for _, value in sections
    ]
    budgets = allocate_budgets(
        [len(tokens) for tokens in encoded_sections],
        cap - fixed_tokens - 16,
    )
    clipped = [
        clip_token_ids(tokenizer, tokens, budget)
        for tokens, budget in zip(encoded_sections, budgets, strict=True)
    ]
    prompt = render(clipped)
    prompt_tokens = len(tokenizer.encode(prompt, add_special_tokens=False))
    while prompt_tokens > cap:
        overflow = prompt_tokens - cap
        target = max(range(len(budgets)), key=lambda index: budgets[index])
        budgets[target] = max(0, budgets[target] - overflow - 8)
        clipped[target] = clip_token_ids(tokenizer, encoded_sections[target], budgets[target])
        prompt = render(clipped)
        prompt_tokens = len(tokenizer.encode(prompt, add_special_tokens=False))
    return prompt, prompt_tokens


def load_rows(phase: str, dataset_paths: dict[str, Path], config: dict[str, Any]) -> list[dict[str, Any]]:
    expected = config["development_inputs"]
    if phase == "development" and set(dataset_paths) != set(expected):
        raise ValueError("development requires exactly gta, bfcl and tooltalk")
    if phase == "confirmation" and set(dataset_paths) != {"toolsandbox"}:
        raise ValueError("confirmation requires exactly toolsandbox")
    rows: list[dict[str, Any]] = []
    for source in sorted(dataset_paths):
        path = dataset_paths[source]
        if not path.is_file():
            raise FileNotFoundError(path)
        if phase == "development":
            spec = expected[source]
            if file_sha256(path) != spec["sha256"]:
                raise ValueError(f"dataset digest mismatch: {source}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"dataset is not a list: {source}")
        if phase == "development" and len(data) != expected[source]["rows"]:
            raise ValueError(f"dataset row count mismatch: {source}")
        if phase == "confirmation" and len(data) != config["conditional_confirmation"]["rows"]:
            raise ValueError("confirmation row count mismatch")
        for index, row in enumerate(data):
            row_id, cluster = row_identity(source, index, row)
            rows.append(
                {
                    "source": source,
                    "row_index": index,
                    "row_id": row_id,
                    "cluster": cluster,
                    "chosen": row["action_chosen"],
                    "rejected": row["action_rejected"],
                    "row": row,
                }
            )
    return rows


def score_prompts(
    model: Any,
    tokenizer: Any,
    prompt_records: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[tuple[str, str, str], dict[str, Any]]:
    order = sorted(range(len(prompt_records)), key=lambda i: prompt_records[i]["prompt_tokens"])
    batches: list[list[int]] = []
    current: list[int] = []
    current_max = 0
    for index in order:
        length = prompt_records[index]["prompt_tokens"]
        proposed_max = max(current_max, length)
        if current and (
            len(current) >= config["max_batch_size"]
            or proposed_max * (len(current) + 1) > config["max_batch_tokens"]
        ):
            batches.append(current)
            current = []
            current_max = 0
        current.append(index)
        current_max = max(current_max, length)
    if current:
        batches.append(current)

    results: dict[tuple[str, str, str], dict[str, Any]] = {}
    yes_id = config["yes_token_id"]
    no_id = config["no_token_id"]
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    for batch_number, batch_indices in enumerate(batches, start=1):
        prompts = [prompt_records[index]["prompt"] for index in batch_indices]
        encoded = tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            add_special_tokens=False,
        ).to("cuda")
        with torch.inference_mode():
            logits = model(**encoded, logits_to_keep=1).logits[:, -1, :].float()
            log_probs = torch.log_softmax(logits, dim=-1)
        for local_index, record_index in enumerate(batch_indices):
            record = prompt_records[record_index]
            yes_logp = float(log_probs[local_index, yes_id].cpu())
            no_logp = float(log_probs[local_index, no_id].cpu())
            key = (record["row_id"], record["slot"], record["kind"])
            results[key] = {
                "prompt_sha256": sha256_bytes(record["prompt"].encode("utf-8")),
                "prompt_tokens": record["prompt_tokens"],
                "yes_logp": yes_logp,
                "no_logp": no_logp,
                "log_odds": yes_logp - no_logp,
                "batch_number": batch_number,
            }
        del encoded, logits, log_probs
    torch.cuda.synchronize()
    return results


def tie_accuracy(margin: float) -> float:
    if margin > 0:
        return 1.0
    if margin < 0:
        return 0.0
    return 0.5


def empirical_percentile(sorted_values: np.ndarray, value: float) -> float:
    left = int(np.searchsorted(sorted_values, value, side="left"))
    right = int(np.searchsorted(sorted_values, value, side="right"))
    return (left + 0.5 * (right - left)) / len(sorted_values)


def fit_linear(pair_rows: list[dict[str, Any]], seed: int, c_value: float) -> LogisticRegression:
    differences = np.asarray(
        [
            [
                row["pointwise"]["chosen"][kind]["log_odds"]
                - row["pointwise"]["rejected"][kind]["log_odds"]
                for kind in OBLIGATIONS
            ]
            for row in pair_rows
        ],
        dtype=np.float64,
    )
    x = np.vstack([differences, -differences])
    y = np.concatenate(
        [np.ones(len(differences), dtype=np.int64), np.zeros(len(differences), dtype=np.int64)]
    )
    model = LogisticRegression(
        C=c_value,
        penalty="l2",
        solver="liblinear",
        fit_intercept=True,
        random_state=seed,
        max_iter=1000,
    )
    model.fit(x, y)
    return model


def criterion_accuracy(rows: list[dict[str, Any]], kind: str) -> float:
    return float(
        np.mean(
            [
                tie_accuracy(
                    row["pointwise"]["chosen"][kind]["log_odds"]
                    - row["pointwise"]["rejected"][kind]["log_odds"]
                )
                for row in rows
            ]
        )
    )


def build_full_state(rows: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    calibration = {}
    for kind in OBLIGATIONS:
        values = [
            row["pointwise"][slot][kind]["log_odds"]
            for row in rows
            for slot in ("chosen", "rejected")
        ]
        calibration[kind] = sorted(values)
    accuracies = {kind: criterion_accuracy(rows, kind) for kind in OBLIGATIONS}
    selected = sorted(accuracies, key=lambda name: (-accuracies[name], name))[0]
    linear = fit_linear(rows, config["seed"], config["linear_c"])
    return {
        "calibration": calibration,
        "selected_single": selected,
        "selected_single_training_accuracy": accuracies[selected],
        "single_accuracies": accuracies,
        "linear_coef": linear.coef_[0].tolist(),
        "linear_intercept": float(linear.intercept_[0]),
        "linear_classes": linear.classes_.tolist(),
    }


def apply_fold_state(
    target_rows: list[dict[str, Any]],
    calibration: dict[str, list[float]],
    selected_single: str,
    linear_coef: list[float],
    linear_intercept: float,
) -> None:
    sorted_calibration = {
        kind: np.asarray(values, dtype=np.float64) for kind, values in calibration.items()
    }
    coef = np.asarray(linear_coef, dtype=np.float64)
    for row in target_rows:
        percentiles: dict[str, dict[str, float]] = {"chosen": {}, "rejected": {}}
        method_scores: dict[str, dict[str, float]] = {"chosen": {}, "rejected": {}}
        for slot in ("chosen", "rejected"):
            logits = {
                kind: row["pointwise"][slot][kind]["log_odds"] for kind in OBLIGATIONS
            }
            for kind in OBLIGATIONS:
                percentiles[slot][kind] = empirical_percentile(
                    sorted_calibration[kind], logits[kind]
                )
                method_scores[slot][kind] = logits[kind]
            values = [percentiles[slot][kind] for kind in OBLIGATIONS]
            method_scores[slot]["cccb"] = min(values)
            method_scores[slot]["holistic"] = row["pointwise"][slot]["holistic"]["log_odds"]
            method_scores[slot]["raw_min"] = min(logits.values())
            method_scores[slot]["calibrated_mean"] = float(np.mean(values))
            method_scores[slot]["calibrated_product"] = float(
                sum(math.log(max(value, 1e-6)) for value in values)
            )
            method_scores[slot]["selected_single"] = logits[selected_single]
        differences = np.asarray(
            [
                row["pointwise"]["chosen"][kind]["log_odds"]
                - row["pointwise"]["rejected"][kind]["log_odds"]
                for kind in OBLIGATIONS
            ],
            dtype=np.float64,
        )
        margins = {
            name: method_scores["chosen"][name] - method_scores["rejected"][name]
            for name in (
                "cccb",
                "holistic",
                *OBLIGATIONS,
                "raw_min",
                "calibrated_mean",
                "calibrated_product",
                "selected_single",
            )
        }
        margins["pair_majority"] = float(np.sign(differences).sum())
        margins["linear_ensemble"] = float(differences @ coef + linear_intercept)
        row["percentiles"] = percentiles
        row["method_scores"] = method_scores
        row["margins"] = margins
        row["correctness"] = {name: tie_accuracy(margins[name]) for name in METHODS}


def bootstrap_delta(
    rows: list[dict[str, Any]],
    comparator: str,
    repeats: int,
    seed: int,
) -> dict[str, float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        grouped[row["cluster"]].append(
            row["correctness"]["cccb"] - row["correctness"][comparator]
        )
    cluster_names = sorted(grouped)
    sums = np.asarray([sum(grouped[name]) for name in cluster_names], dtype=np.float64)
    counts = np.asarray([len(grouped[name]) for name in cluster_names], dtype=np.float64)
    rng = np.random.default_rng(seed)
    samples = np.empty(repeats, dtype=np.float64)
    for repeat in range(repeats):
        chosen = rng.integers(0, len(cluster_names), size=len(cluster_names))
        samples[repeat] = sums[chosen].sum() / counts[chosen].sum()
    return {
        "repeats": repeats,
        "seed": seed,
        "clusters": len(cluster_names),
        "lower_2_5": float(np.quantile(samples, 0.025)),
        "median": float(np.quantile(samples, 0.5)),
        "upper_97_5": float(np.quantile(samples, 0.975)),
    }


def summarize(
    rows: list[dict[str, Any]],
    phase: str,
    config: dict[str, Any],
    frozen_strongest: str | None,
) -> dict[str, Any]:
    accuracy = {
        name: float(np.mean([row["correctness"][name] for row in rows])) for name in METHODS
    }
    if phase == "development":
        strongest = sorted(COMPARATORS, key=lambda name: (-accuracy[name], name))[0]
    else:
        if frozen_strongest not in COMPARATORS:
            raise ValueError("invalid frozen strongest comparator")
        strongest = str(frozen_strongest)
    delta = accuracy["cccb"] - accuracy[strongest]
    by_source = {}
    for source in sorted({row["source"] for row in rows}):
        subset = [row for row in rows if row["source"] == source]
        source_accuracy = {
            name: float(np.mean([row["correctness"][name] for row in subset]))
            for name in METHODS
        }
        by_source[source] = {
            "rows": len(subset),
            "accuracy": source_accuracy,
            "candidate_delta_vs_strongest": source_accuracy["cccb"]
            - source_accuracy[strongest],
        }
    bootstrap = bootstrap_delta(
        rows, strongest, config["bootstrap_repeats"], config["seed"]
    )
    strict_all = all(accuracy["cccb"] > accuracy[name] for name in COMPARATORS)
    swap_max_error = max(
        abs(row["margins"][name] + (-row["margins"][name]))
        for row in rows
        for name in METHODS
    )
    if phase == "development":
        gates_config = config["development_gates"]
        deltas = [record["candidate_delta_vs_strongest"] for record in by_source.values()]
        gates = {
            "candidate_accuracy": accuracy["cccb"] >= gates_config["candidate_accuracy_min"],
            "candidate_delta": delta >= gates_config["candidate_delta_min"],
            "bootstrap_lower_positive": bootstrap["lower_2_5"] > 0,
            "strictly_beats_all_comparators": strict_all,
            "each_source_accuracy": all(
                record["accuracy"]["cccb"] >= gates_config["source_accuracy_min"]
                for record in by_source.values()
            ),
            "all_source_deltas_nonnegative": all(value >= 0 for value in deltas),
            "minimum_positive_sources": sum(value > 0 for value in deltas)
            >= gates_config["minimum_positive_sources"],
            "action_swap_exact": swap_max_error == 0,
        }
    else:
        gates_config = config["confirmation_gates"]
        gates = {
            "candidate_accuracy": accuracy["cccb"] >= gates_config["candidate_accuracy_min"],
            "candidate_delta": delta > gates_config["candidate_delta_min"],
            "bootstrap_lower_nonnegative": bootstrap["lower_2_5"] >= 0,
            "strictly_beats_all_comparators": strict_all,
            "action_swap_exact": swap_max_error == 0,
        }
    return {
        "schema_version": 1,
        "experiment_id": config["experiment_id"],
        "phase": phase,
        "rows": len(rows),
        "pointwise_actions": 2 * len(rows),
        "prompt_evaluations": 2 * len(rows) * len(PROMPT_KINDS),
        "clusters": len({row["cluster"] for row in rows}),
        "accuracy": accuracy,
        "strongest_comparator": strongest,
        "candidate_delta_vs_strongest": delta,
        "by_source": by_source,
        "bootstrap": bootstrap,
        "swap_max_error": swap_max_error,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(
        (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        )
    )


def main() -> int:
    args = parse_args()
    if args.output_dir.exists():
        raise FileExistsError(args.output_dir)
    config_bytes = args.config.read_bytes()
    config = json.loads(config_bytes.decode("utf-8"))
    if config["experiment_id"] != "v034":
        raise ValueError("wrong experiment id")
    candidate_bytes = args.candidate.read_bytes()
    if sha256_bytes(candidate_bytes) != config["candidate_sha256"]:
        raise ValueError("candidate digest mismatch")
    evidence_bytes = args.evidence_packet.read_bytes()
    manifest_bytes = args.model_manifest.read_bytes()
    if sha256_bytes(manifest_bytes) != config["model_manifest_sha256"]:
        raise ValueError("model manifest digest mismatch")
    model_manifest = json.loads(manifest_bytes.decode("utf-8"))
    if (
        model_manifest["model_id"] != config["model_id"]
        or model_manifest["revision"] != config["model_revision"]
    ):
        raise ValueError("model identity mismatch")
    model_dir = args.model_dir.resolve()
    if Path(model_manifest["snapshot_path"]).resolve() != model_dir:
        raise ValueError("model path differs from manifest")
    weight_path = model_dir / "model.safetensors"
    if file_sha256(weight_path) != config["model_weight_sha256"]:
        raise ValueError("model weight digest mismatch")
    dataset_paths = parse_dataset_args(args.dataset)
    rows = load_rows(args.phase, dataset_paths, config)
    if args.phase == "confirmation" and args.frozen_state is None:
        raise ValueError("confirmation requires frozen state")
    if args.phase == "development" and args.frozen_state is not None:
        raise ValueError("development cannot take frozen state")

    random.seed(config["seed"])
    np.random.seed(config["seed"])
    torch.manual_seed(config["seed"])
    torch.cuda.manual_seed_all(config["seed"])
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable")

    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    if tokenizer.encode("Yes", add_special_tokens=False) != [config["yes_token_id"]]:
        raise ValueError("Yes token identity mismatch")
    if tokenizer.encode("No", add_special_tokens=False) != [config["no_token_id"]]:
        raise ValueError("No token identity mismatch")

    prompt_records: list[dict[str, Any]] = []
    pair_rows: list[dict[str, Any]] = []
    for record in rows:
        pair = {
            "row_id": record["row_id"],
            "source": record["source"],
            "row_index": record["row_index"],
            "cluster": record["cluster"],
            "pointwise": {"chosen": {}, "rejected": {}},
        }
        pair_rows.append(pair)
        for slot in ("chosen", "rejected"):
            evidence = build_evidence(
                record["source"], record["row_index"], record["row"], record[slot]
            )
            for kind in PROMPT_KINDS:
                prompt, prompt_tokens = make_prompt(
                    tokenizer, kind, evidence, config["max_prompt_tokens"]
                )
                prompt_records.append(
                    {
                        "row_id": record["row_id"],
                        "slot": slot,
                        "kind": kind,
                        "prompt": prompt,
                        "prompt_tokens": prompt_tokens,
                    }
                )

    started = time.perf_counter()
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        local_files_only=True,
        dtype=torch.bfloat16,
        attn_implementation="sdpa",
    ).to("cuda")
    model.eval()
    scores = score_prompts(model, tokenizer, prompt_records, config)
    inference_seconds = time.perf_counter() - started
    for pair in pair_rows:
        for slot in ("chosen", "rejected"):
            for kind in PROMPT_KINDS:
                pair["pointwise"][slot][kind] = scores[(pair["row_id"], slot, kind)]

    state: dict[str, Any]
    if args.phase == "development":
        fold_states = {}
        for source in sorted(dataset_paths):
            training = [row for row in pair_rows if row["source"] != source]
            target = [row for row in pair_rows if row["source"] == source]
            state_part = build_full_state(training, config)
            apply_fold_state(
                target,
                state_part["calibration"],
                state_part["selected_single"],
                state_part["linear_coef"],
                state_part["linear_intercept"],
            )
            fold_states[source] = state_part
        full_state = build_full_state(pair_rows, config)
        state = {
            "schema_version": 1,
            "experiment_id": config["experiment_id"],
            "model_id": config["model_id"],
            "model_revision": config["model_revision"],
            "fold_states": fold_states,
            "full_development_state": full_state,
        }
        summary = summarize(pair_rows, args.phase, config, None)
        state["development_strongest_comparator"] = summary["strongest_comparator"]
    else:
        state = json.loads(args.frozen_state.read_text(encoding="utf-8"))
        if state["experiment_id"] != config["experiment_id"]:
            raise ValueError("frozen state experiment mismatch")
        full_state = state["full_development_state"]
        apply_fold_state(
            pair_rows,
            full_state["calibration"],
            full_state["selected_single"],
            full_state["linear_coef"],
            full_state["linear_intercept"],
        )
        summary = summarize(
            pair_rows,
            args.phase,
            config,
            state["development_strongest_comparator"],
        )

    environment = {
        "captured_at_utc": datetime.now(UTC).isoformat(),
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scikit_learn": sklearn.__version__,
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "cuda_runtime": torch.version.cuda,
        "cuda_device": torch.cuda.get_device_name(0),
        "cuda_capability": list(torch.cuda.get_device_capability(0)),
        "model_id": config["model_id"],
        "model_revision": config["model_revision"],
        "model_weight_sha256": config["model_weight_sha256"],
        "dtype": "bfloat16",
        "attention": "sdpa",
        "inference_seconds": inference_seconds,
        "max_prompt_tokens_observed": max(
            record["prompt_tokens"] for record in prompt_records
        ),
        "prompt_evaluations": len(prompt_records),
        "pythondontwritebytecode": os.environ.get("PYTHONDONTWRITEBYTECODE"),
    }

    args.output_dir.mkdir()
    pointwise_path = args.output_dir / "pointwise_scores.jsonl"
    raw_path = args.output_dir / "raw_predictions.jsonl"
    with pointwise_path.open("wb") as handle:
        for row in pair_rows:
            for slot in ("chosen", "rejected"):
                output = {
                    "row_id": row["row_id"],
                    "source": row["source"],
                    "row_index": row["row_index"],
                    "cluster": row["cluster"],
                    "slot": slot,
                    "scores": row["pointwise"][slot],
                }
                handle.write((canonical_json(output) + "\n").encode("utf-8"))
    with raw_path.open("wb") as handle:
        for row in pair_rows:
            output = {
                "row_id": row["row_id"],
                "source": row["source"],
                "row_index": row["row_index"],
                "cluster": row["cluster"],
                "percentiles": row["percentiles"],
                "method_scores": row["method_scores"],
                "margins": row["margins"],
                "correctness": row["correctness"],
            }
            handle.write((canonical_json(output) + "\n").encode("utf-8"))
    write_json(args.output_dir / "summary.json", summary)
    write_json(args.output_dir / "environment.json", environment)
    write_json(args.output_dir / "frozen_state.json", state)
    print(
        canonical_json(
            {
                "status": f"{args.phase.upper()}_COMPLETE",
                "rows": len(pair_rows),
                "candidate_accuracy": summary["accuracy"]["cccb"],
                "strongest_comparator": summary["strongest_comparator"],
                "delta": summary["candidate_delta_vs_strongest"],
                "all_gates_pass": summary["all_gates_pass"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
