from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import math
import os
import platform
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer


SYSTEM = (
    "You are a tool-using assistant. Continue the interaction by producing "
    "exactly the next assistant action. Preserve operational details."
)
METHODS = (
    "ecds",
    "full_diff_ll",
    "full_action_gain",
    "null_diff_ll",
    "full_action_ll",
)
CONTROLS = ("full_diff_ll", "full_action_gain", "null_diff_ll", "full_action_ll")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--model-manifest", type=Path, required=True)
    parser.add_argument("--dataset", action="append", default=[], required=True)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_text(value: Any) -> str:
    return value if isinstance(value, str) else canonical_json(value)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_dataset_args(items: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"dataset must be source=path: {item}")
        source, raw_path = item.split("=", 1)
        source = source.strip().lower()
        if not source or source in result:
            raise ValueError(f"invalid or duplicate source: {source}")
        result[source] = Path(raw_path).resolve()
    return result


def iter_dicts(value: Any) -> Iterable[dict[str, Any]]:
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


def schema_names(item: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for key in ("name", "api_name"):
        if isinstance(item.get(key), str):
            names.append(item[key])
    if isinstance(item.get("api_names"), list):
        names.extend(str(value) for value in item["api_names"])
    return names


def system_history(history: Any) -> str:
    if not isinstance(history, list):
        return ""
    return "\n".join(
        stable_text(message.get("content", ""))
        for message in history
        if isinstance(message, dict) and message.get("role") == "system"
    )


def implicated_contracts(functions: Any, history: Any, actions: tuple[Any, Any]) -> str:
    calls = [extract_call(action) for action in actions]
    targets = {str(call["name"]).casefold() for call in calls if call is not None}
    if not targets:
        return "NO_TOOL_CONTRACT_IMPLICATED"
    if functions is None:
        fallback = system_history(history)
        return "SYSTEM_MESSAGE_FALLBACK:\n" + (fallback or "NO_CONTRACT_AVAILABLE")
    matched: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in iter_dicts(functions):
        names = schema_names(item)
        if not names or not any(name.casefold() in targets for name in names):
            continue
        payload = canonical_json(item)
        if payload not in seen:
            seen.add(payload)
            matched.append(item)
    return canonical_json(matched) if matched else "NO_EXACT_CONTRACT_MATCH"


def row_identity(source: str, index: int, row: dict[str, Any]) -> tuple[str, str]:
    natural = (
        str(row["sample_id"])
        if source == "bfcl"
        else str(row.get("task", row.get("sample_id", row.get("index", index))))
    )
    return f"{source}:{index:04d}", f"{source}:{natural}"


def load_rows(
    phase: str, dataset_paths: dict[str, Path], config: dict[str, Any]
) -> list[dict[str, Any]]:
    if phase == "development":
        expected = config["development_inputs"]
    else:
        meta = config["conditional_confirmation"]
        expected = {meta["source"]: meta}
    if set(dataset_paths) != set(expected):
        raise ValueError(f"source mismatch: expected {sorted(expected)}")
    rows: list[dict[str, Any]] = []
    for source in sorted(dataset_paths):
        path = dataset_paths[source]
        meta = expected[source]
        if sha256_file(path) != meta["sha256"]:
            raise ValueError(f"dataset hash mismatch: {path}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list) or len(payload) != meta["rows"]:
            raise ValueError(f"dataset row mismatch: {path}")
        for index, row in enumerate(payload):
            row_id, cluster = row_identity(source, index, row)
            chosen = stable_text(row["action_chosen"])
            rejected = stable_text(row["action_rejected"])
            rows.append(
                {
                    "row_id": row_id,
                    "cluster": cluster,
                    "source": source,
                    "history": stable_text(row["history"]),
                    "contracts": implicated_contracts(
                        row.get("functions"),
                        row["history"],
                        (row["action_chosen"], row["action_rejected"]),
                    ),
                    "chosen": chosen,
                    "rejected": rejected,
                }
            )
    return rows


def difference_positions(
    chosen_ids: list[int], rejected_ids: list[int]
) -> tuple[list[int], list[int]]:
    chosen_diff: set[int] = set()
    rejected_diff: set[int] = set()
    matcher = difflib.SequenceMatcher(a=chosen_ids, b=rejected_ids, autojunk=False)
    for tag, chosen_start, chosen_end, rejected_start, rejected_end in matcher.get_opcodes():
        if tag == "equal":
            continue
        if chosen_start < chosen_end:
            chosen_diff.update(range(chosen_start, chosen_end))
        else:
            boundary = chosen_start if chosen_start < len(chosen_ids) else chosen_start - 1
            chosen_diff.add(boundary)
        if rejected_start < rejected_end:
            rejected_diff.update(range(rejected_start, rejected_end))
        else:
            boundary = (
                rejected_start
                if rejected_start < len(rejected_ids)
                else rejected_start - 1
            )
            rejected_diff.add(boundary)
    if not chosen_diff or not rejected_diff:
        raise ValueError("each action must contain at least one differential position")
    return sorted(chosen_diff), sorted(rejected_diff)


def clip_token_ids(tokenizer: Any, token_ids: list[int], budget: int) -> str:
    if len(token_ids) <= budget:
        return tokenizer.decode(token_ids, skip_special_tokens=False)
    marker = tokenizer.encode(
        "\n[...DETERMINISTIC_HEAD_TAIL_TRUNCATION...]\n", add_special_tokens=False
    )
    if budget <= len(marker) + 2:
        return tokenizer.decode(token_ids[:budget], skip_special_tokens=False)
    keep = budget - len(marker)
    head = (keep + 1) // 2
    tail = keep - head
    return tokenizer.decode(
        token_ids[:head] + marker + (token_ids[-tail:] if tail else []),
        skip_special_tokens=False,
    )


def allocate_budgets(lengths: list[int], total: int) -> list[int]:
    budgets = [0] * len(lengths)
    active = set(range(len(lengths)))
    remaining = total
    while active and remaining > 0:
        share = max(1, remaining // len(active))
        progress = False
        for index in list(active):
            take = min(share, lengths[index] - budgets[index], remaining)
            budgets[index] += take
            remaining -= take
            if budgets[index] >= lengths[index]:
                active.remove(index)
            progress = progress or take > 0
        if not progress:
            break
    return budgets


def render_context(tokenizer: Any, history: str, contracts: str) -> str:
    user = (
        "HISTORY:\n"
        + history
        + "\n\nIMPLICATED_CONTRACTS:\n"
        + contracts
        + "\n\nTASK:\nProduce exactly the next assistant action."
    )
    return tokenizer.apply_chat_template(
        [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


def make_full_context(
    tokenizer: Any, history: str, contracts: str, action_length: int, cap: int
) -> tuple[list[int], bool]:
    empty = render_context(tokenizer, "", "")
    fixed = len(tokenizer.encode(empty, add_special_tokens=False))
    available = cap - action_length - fixed - 16
    if available <= 0:
        raise ValueError("action and fixed context exceed sequence cap")
    raw = [
        tokenizer.encode(history, add_special_tokens=False),
        tokenizer.encode(contracts, add_special_tokens=False),
    ]
    budgets = allocate_budgets([len(value) for value in raw], available)
    clipped = [
        clip_token_ids(tokenizer, value, budget)
        for value, budget in zip(raw, budgets, strict=True)
    ]
    prompt = render_context(tokenizer, clipped[0], clipped[1])
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    while len(prompt_ids) + action_length > cap:
        overflow = len(prompt_ids) + action_length - cap
        target = max(range(2), key=lambda index: budgets[index])
        budgets[target] = max(0, budgets[target] - overflow - 8)
        clipped[target] = clip_token_ids(tokenizer, raw[target], budgets[target])
        prompt = render_context(tokenizer, clipped[0], clipped[1])
        prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    return prompt_ids, any(len(value) > budget for value, budget in zip(raw, budgets, strict=True))


def make_null_context(tokenizer: Any, action_length: int, cap: int) -> list[int]:
    prompt = render_context(tokenizer, "[EVIDENCE_WITHHELD]", "[EVIDENCE_WITHHELD]")
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    if len(prompt_ids) + action_length > cap:
        raise ValueError("null sequence exceeds cap")
    return prompt_ids


def build_sequence_records(
    rows: list[dict[str, Any]], tokenizer: Any, config: dict[str, Any]
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    cap = config["max_sequence_tokens"]
    for row in rows:
        chosen_ids = tokenizer.encode(row["chosen"], add_special_tokens=False)
        rejected_ids = tokenizer.encode(row["rejected"], add_special_tokens=False)
        if not chosen_ids or not rejected_ids:
            raise ValueError(f"empty action tokens: {row['row_id']}")
        chosen_diff, rejected_diff = difference_positions(chosen_ids, rejected_ids)
        for slot, action_ids, diff in (
            ("chosen", chosen_ids, chosen_diff),
            ("rejected", rejected_ids, rejected_diff),
        ):
            full_prompt, truncated = make_full_context(
                tokenizer, row["history"], row["contracts"], len(action_ids), cap
            )
            null_prompt = make_null_context(tokenizer, len(action_ids), cap)
            for context, prompt_ids in (("full", full_prompt), ("null", null_prompt)):
                input_ids = prompt_ids + action_ids
                records.append(
                    {
                        "sequence_id": f"{row['row_id']}::{slot}::{context}",
                        "row_id": row["row_id"],
                        "slot": slot,
                        "context": context,
                        "input_ids": input_ids,
                        "prompt_length": len(prompt_ids),
                        "action_ids": action_ids,
                        "diff_positions": diff,
                        "context_truncated": truncated if context == "full" else False,
                    }
                )
    return records


def validate_model(model_dir: Path, manifest_path: Path, config: dict[str, Any]) -> None:
    if sha256_file(manifest_path) != config["model_manifest_sha256"]:
        raise ValueError("model manifest hash mismatch")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["model_id"] != config["model_id"] or manifest["revision"] != config["model_revision"]:
        raise ValueError("model identity mismatch")
    if Path(manifest["snapshot_path"]).resolve() != model_dir.resolve():
        raise ValueError("model path mismatch")
    for record in manifest["files"]:
        path = Path(record["resolved_path"])
        if path.stat().st_size != record["bytes"] or sha256_file(path) != record["sha256"]:
            raise ValueError(f"model file mismatch: {path}")


def make_batches(records: list[dict[str, Any]], config: dict[str, Any]) -> list[list[int]]:
    batches: list[list[int]] = []
    current: list[int] = []
    max_input = 0
    max_action = 0
    for index, record in enumerate(records):
        proposed_input = max(max_input, len(record["input_ids"]))
        proposed_action = max(max_action, len(record["action_ids"]) + 1)
        size = len(current) + 1
        if current and (
            size > config["max_batch_size"]
            or proposed_input * size > config["max_batch_input_tokens"]
            or proposed_action * size > config["max_batch_logit_tokens"]
        ):
            batches.append(current)
            current = []
            max_input = 0
            max_action = 0
        current.append(index)
        max_input = max(max_input, len(record["input_ids"]))
        max_action = max(max_action, len(record["action_ids"]) + 1)
    if current:
        batches.append(current)
    return batches


def score_sequences(
    records: list[dict[str, Any]], tokenizer: Any, model: Any, config: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    batches = make_batches(records, config)
    pad_id = tokenizer.pad_token_id
    if pad_id is None:
        pad_id = tokenizer.eos_token_id
    results: dict[str, dict[str, Any]] = {}
    for batch_number, indices in enumerate(batches, start=1):
        max_length = max(len(records[index]["input_ids"]) for index in indices)
        max_action = max(len(records[index]["action_ids"]) for index in indices)
        inputs = torch.full(
            (len(indices), max_length), pad_id, dtype=torch.long, device="cuda"
        )
        attention = torch.zeros_like(inputs)
        for local, index in enumerate(indices):
            ids = torch.tensor(records[index]["input_ids"], dtype=torch.long, device="cuda")
            inputs[local, -len(ids) :] = ids
            attention[local, -len(ids) :] = 1
        with torch.inference_mode():
            logits = model(
                input_ids=inputs,
                attention_mask=attention,
                logits_to_keep=max_action + 1,
            ).logits
        for local, index in enumerate(indices):
            record = records[index]
            action_ids = record["action_ids"]
            length = len(action_ids)
            action_logits = logits[local, -(length + 1) : -1, :].float()
            targets = torch.tensor(action_ids, dtype=torch.long, device="cuda")
            target_logits = action_logits.gather(1, targets[:, None]).squeeze(1)
            log_probs = target_logits - torch.logsumexp(action_logits, dim=1)
            diff_index = torch.tensor(
                record["diff_positions"], dtype=torch.long, device="cuda"
            )
            all_mean = float(log_probs.mean().cpu())
            diff_mean = float(log_probs.index_select(0, diff_index).mean().cpu())
            results[record["sequence_id"]] = {
                "sequence_sha256": sha256_bytes(
                    np.asarray(record["input_ids"], dtype="<i8").tobytes()
                ),
                "action_sha256": sha256_bytes(
                    np.asarray(action_ids, dtype="<i8").tobytes()
                ),
                "diff_positions_sha256": sha256_bytes(
                    np.asarray(record["diff_positions"], dtype="<i8").tobytes()
                ),
                "sequence_tokens": len(record["input_ids"]),
                "prompt_tokens": record["prompt_length"],
                "action_tokens": length,
                "diff_tokens": len(record["diff_positions"]),
                "context_truncated": record["context_truncated"],
                "all_mean_logp": all_mean,
                "diff_mean_logp": diff_mean,
                "batch_number": batch_number,
            }
        del inputs, attention, logits
    torch.cuda.synchronize()
    return results


def tie_accuracy(margin: float) -> float:
    return 1.0 if margin > 0 else 0.0 if margin < 0 else 0.5


def build_raw_rows(
    rows: list[dict[str, Any]], scores: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        rid = row["row_id"]
        values = {
            slot: {
                context: scores[f"{rid}::{slot}::{context}"]
                for context in ("full", "null")
            }
            for slot in ("chosen", "rejected")
        }
        margins = {
            "ecds": (
                values["chosen"]["full"]["diff_mean_logp"]
                - values["chosen"]["null"]["diff_mean_logp"]
            )
            - (
                values["rejected"]["full"]["diff_mean_logp"]
                - values["rejected"]["null"]["diff_mean_logp"]
            ),
            "full_diff_ll": values["chosen"]["full"]["diff_mean_logp"]
            - values["rejected"]["full"]["diff_mean_logp"],
            "full_action_gain": (
                values["chosen"]["full"]["all_mean_logp"]
                - values["chosen"]["null"]["all_mean_logp"]
            )
            - (
                values["rejected"]["full"]["all_mean_logp"]
                - values["rejected"]["null"]["all_mean_logp"]
            ),
            "null_diff_ll": values["chosen"]["null"]["diff_mean_logp"]
            - values["rejected"]["null"]["diff_mean_logp"],
            "full_action_ll": values["chosen"]["full"]["all_mean_logp"]
            - values["rejected"]["full"]["all_mean_logp"],
        }
        output.append(
            {
                "row_id": rid,
                "cluster": row["cluster"],
                "source": row["source"],
                "scores": values,
                "methods": {
                    method: {"margin": margin, "accuracy": tie_accuracy(margin)}
                    for method, margin in margins.items()
                },
            }
        )
    return output


def mean_accuracy(rows: list[dict[str, Any]], method: str) -> float:
    return float(np.mean([row["methods"][method]["accuracy"] for row in rows]))


def bootstrap_delta(
    rows: list[dict[str, Any]], comparator: str, repeats: int, seed: int
) -> dict[str, Any]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in rows:
        grouped[row["source"]][row["cluster"]].append(row)
    rng = random.Random(seed)
    deltas = []
    for _ in range(repeats):
        sampled = []
        for source in sorted(grouped):
            clusters = sorted(grouped[source])
            for _ in clusters:
                selected = clusters[rng.randrange(len(clusters))]
                sampled.extend(grouped[source][selected])
        deltas.append(mean_accuracy(sampled, "ecds") - mean_accuracy(sampled, comparator))
    values = np.asarray(deltas, dtype=np.float64)
    return {
        "repeats": repeats,
        "seed": seed,
        "lower_95": float(np.quantile(values, 0.025)),
        "median": float(np.quantile(values, 0.5)),
        "upper_95": float(np.quantile(values, 0.975)),
    }


def summarize(
    raw: list[dict[str, Any]], config: dict[str, Any], phase: str, state: dict[str, Any] | None
) -> dict[str, Any]:
    overall = {method: mean_accuracy(raw, method) for method in METHODS}
    by_source = {}
    for source in sorted({row["source"] for row in raw}):
        subset = [row for row in raw if row["source"] == source]
        by_source[source] = {method: mean_accuracy(subset, method) for method in METHODS}
    strongest = (
        sorted(CONTROLS, key=lambda name: (-overall[name], name))[0]
        if phase == "development"
        else state["strongest_control"]
    )
    source_deltas = {
        source: metrics["ecds"] - metrics[strongest] for source, metrics in by_source.items()
    }
    return {
        "schema_version": 1,
        "experiment_id": config["experiment_id"],
        "phase": phase,
        "row_count": len(raw),
        "cluster_count": len({row["cluster"] for row in raw}),
        "sequence_count": len(raw) * 4,
        "source_counts": {
            source: sum(row["source"] == source for row in raw)
            for source in sorted(by_source)
        },
        "overall_accuracy": overall,
        "source_accuracy": by_source,
        "strongest_control": strongest,
        "candidate_delta": overall["ecds"] - overall[strongest],
        "source_deltas": source_deltas,
        "positive_source_count": sum(value > 0 for value in source_deltas.values()),
        "bootstrap_delta": bootstrap_delta(
            raw, strongest, config["bootstrap_repeats"], config["seed"]
        ),
        "truncated_sequence_count": sum(
            score["context_truncated"]
            for row in raw
            for slot in ("chosen", "rejected")
            for score in (row["scores"][slot]["full"],)
        ),
    }


def environment_capture() -> dict[str, Any]:
    device = torch.cuda.get_device_properties(0)
    return {
        "captured_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "python": platform.python_version(),
        "executable": sys.executable,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "cuda_runtime": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": device.name,
        "gpu_capability": [device.major, device.minor],
        "gpu_total_memory": device.total_memory,
        "python_dont_write_bytecode": os.environ.get("PYTHONDONTWRITEBYTECODE"),
    }


def compare_values(
    expected: Any,
    observed: Any,
    path: str,
    tolerance: float,
    counters: dict[str, Any],
) -> None:
    if isinstance(expected, bool) or isinstance(observed, bool):
        counters["exact_checked"] += 1
        if expected != observed:
            counters["mismatches"].append(path)
        return
    if isinstance(expected, (int, float)) and isinstance(observed, (int, float)):
        counters["numeric_checked"] += 1
        error = abs(float(expected) - float(observed))
        counters["max_numeric_error"] = max(counters["max_numeric_error"], error)
        if not math.isfinite(error) or error > tolerance:
            counters["mismatches"].append(path)
        return
    if isinstance(expected, dict) and isinstance(observed, dict):
        counters["exact_checked"] += 1
        if set(expected) != set(observed):
            counters["mismatches"].append(path + ".keys")
            return
        for key in sorted(expected):
            compare_values(
                expected[key], observed[key], f"{path}.{key}", tolerance, counters
            )
        return
    if isinstance(expected, list) and isinstance(observed, list):
        counters["exact_checked"] += 1
        if len(expected) != len(observed):
            counters["mismatches"].append(path + ".length")
            return
        for index, (left, right) in enumerate(zip(expected, observed, strict=True)):
            compare_values(left, right, f"{path}[{index}]", tolerance, counters)
        return
    counters["exact_checked"] += 1
    if expected != observed:
        counters["mismatches"].append(path)


def main() -> None:
    args = parse_args()
    config_path = args.config.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    datasets = parse_dataset_args(args.dataset)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    validate_model(args.model_dir.resolve(), args.model_manifest.resolve(), config)
    state = None
    if args.phase == "confirmation":
        if args.state is None:
            raise ValueError("--state required for confirmation")
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if state["candidate_sha256"] != config["candidate_sha256"]:
            raise ValueError("state candidate mismatch")
        if state["config_sha256"] != sha256_file(config_path):
            raise ValueError("state config mismatch")
    elif args.state is not None:
        raise ValueError("--state not used for development")

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_dir.resolve(), local_files_only=True, trust_remote_code=False
    )
    rows = load_rows(args.phase, datasets, config)
    records = build_sequence_records(rows, tokenizer, config)
    if len(records) != len(rows) * 4:
        raise ValueError("sequence count mismatch")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir.resolve(),
        local_files_only=True,
        trust_remote_code=False,
        dtype=torch.float16,
    ).to("cuda")
    model.eval()
    scores = score_sequences(records, tokenizer, model, config)
    expected_raw = build_raw_rows(rows, scores)
    expected_summary = summarize(expected_raw, config, args.phase, state)

    observed_raw = [
        json.loads(line)
        for line in args.raw.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    observed_summary = json.loads(args.summary.read_text(encoding="utf-8"))
    counters: dict[str, Any] = {
        "numeric_checked": 0,
        "exact_checked": 0,
        "max_numeric_error": 0.0,
        "mismatches": [],
    }
    compare_values(
        expected_raw,
        observed_raw,
        "raw",
        config["audit_tolerance"],
        counters,
    )
    compare_values(
        expected_summary,
        observed_summary,
        "summary",
        config["audit_tolerance"],
        counters,
    )
    report = {
        "schema_version": 1,
        "experiment_id": config["experiment_id"],
        "phase": args.phase,
        "audit_ok": not counters["mismatches"],
        "rows_recomputed": len(expected_raw),
        "sequences_recomputed": len(records),
        "numeric_values_checked": counters["numeric_checked"],
        "exact_values_checked": counters["exact_checked"],
        "max_numeric_error": counters["max_numeric_error"],
        "mismatch_count": len(counters["mismatches"]),
        "mismatches": counters["mismatches"][:100],
        "observed_raw_sha256": sha256_file(args.raw),
        "observed_summary_sha256": sha256_file(args.summary),
        "model_manifest_sha256": sha256_file(args.model_manifest),
        "config_sha256": sha256_file(config_path),
    }
    args.report.parent.mkdir(parents=True, exist_ok=False)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["audit_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
