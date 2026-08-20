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
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer


PAIR_SYSTEM = (
    "You are a strict evaluator of the next action in a tool-using interaction. "
    "Judge operational correctness from the supplied history and tool contracts. "
    "Ignore verbosity, confidence, style, and candidate position. "
    "Respond with exactly A or B and no other text."
)
POINT_SYSTEM = (
    "You are a strict evaluator of one proposed next action in a tool-using "
    "interaction. Decide whether the action is operationally supported by the "
    "supplied history and tool contracts. Ignore style and verbosity. "
    "Respond with exactly Yes or No and no other text."
)
METHODS = ("sdej", "full_pair", "full_pointwise", "delta_no_evidence", "delta_forward")
CONTROL_METHODS = ("full_pair", "full_pointwise", "delta_no_evidence", "delta_forward")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--model-manifest", type=Path, required=True)
    parser.add_argument("--dataset", action="append", default=[], required=True)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--state", type=Path)
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
            raise ValueError(f"invalid or duplicate dataset source: {source}")
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


def normalize_arguments(value: Any) -> Any:
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return value
        if isinstance(decoded, (dict, list)):
            return decoded
    return value


def flatten_value(value: Any, prefix: str = "arg") -> dict[str, str]:
    value = normalize_arguments(value)
    if isinstance(value, dict):
        if not value:
            return {prefix: "{}"}
        result: dict[str, str] = {}
        for key in sorted(value, key=str):
            result.update(flatten_value(value[key], f"{prefix}.{key}"))
        return result
    if isinstance(value, list):
        if not value:
            return {prefix: "[]"}
        result = {}
        for index, child in enumerate(value):
            result.update(flatten_value(child, f"{prefix}[{index}]"))
        return result
    return {prefix: canonical_json(value)}


def action_fields(action: Any) -> tuple[dict[str, str], dict[str, Any] | None]:
    call = extract_call(action)
    if call is None:
        return {"mode": "text", "text": stable_text(action)}, None
    fields = {"mode": "call", "tool": str(call["name"])}
    fields.update(flatten_value(call.get("arguments", {})))
    return fields, call


def text_spans(left: str, right: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    left_tokens = re.findall(r"\w+|[^\w\s]", left, flags=re.UNICODE)
    right_tokens = re.findall(r"\w+|[^\w\s]", right, flags=re.UNICODE)
    matcher = difflib.SequenceMatcher(a=left_tokens, b=right_tokens, autojunk=False)
    left_spans: list[dict[str, Any]] = []
    right_spans: list[dict[str, Any]] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if i1 != i2:
            left_spans.append(
                {"op": tag, "start": i1, "end": i2, "tokens": left_tokens[i1:i2]}
            )
        if j1 != j2:
            right_spans.append(
                {"op": tag, "start": j1, "end": j2, "tokens": right_tokens[j1:j2]}
            )
    return left_spans, right_spans


def build_difference(
    chosen: Any, rejected: Any
) -> tuple[str, str, dict[str, Any] | None, dict[str, Any] | None, dict[str, Any]]:
    left_fields, left_call = action_fields(chosen)
    right_fields, right_call = action_fields(rejected)
    if left_call is None and right_call is None:
        left_spans, right_spans = text_spans(stable_text(chosen), stable_text(rejected))
        left_payload: Any = {"mode": "text", "different_spans": left_spans}
        right_payload: Any = {"mode": "text", "different_spans": right_spans}
        meta = {
            "shared_field_count": 1 if stable_text(chosen) == stable_text(rejected) else 0,
            "difference_keys": ["text"],
            "left_span_count": len(left_spans),
            "right_span_count": len(right_spans),
        }
        return (
            canonical_json(left_payload),
            canonical_json(right_payload),
            left_call,
            right_call,
            meta,
        )
    keys = sorted(set(left_fields) | set(right_fields))
    shared = [key for key in keys if left_fields.get(key) == right_fields.get(key)]
    different = [key for key in keys if key not in shared]
    left_payload = {
        key: left_fields[key] if key in left_fields else "[ABSENT]" for key in different
    }
    right_payload = {
        key: right_fields[key] if key in right_fields else "[ABSENT]" for key in different
    }
    meta = {
        "shared_field_count": len(shared),
        "difference_keys": different,
        "left_span_count": 0,
        "right_span_count": 0,
    }
    return (
        canonical_json(left_payload),
        canonical_json(right_payload),
        left_call,
        right_call,
        meta,
    )


def schema_names(item: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for key in ("name", "api_name"):
        value = item.get(key)
        if isinstance(value, str):
            result.append(value)
    values = item.get("api_names")
    if isinstance(values, list):
        result.extend(str(value) for value in values)
    return result


def system_history(history: Any) -> str:
    if not isinstance(history, list):
        return ""
    return "\n".join(
        stable_text(message.get("content", ""))
        for message in history
        if isinstance(message, dict) and message.get("role") == "system"
    )


def implicated_contracts(
    functions: Any,
    history: Any,
    calls: tuple[dict[str, Any] | None, dict[str, Any] | None],
) -> str:
    target_names = {
        str(call["name"]).casefold() for call in calls if call is not None
    }
    if not target_names:
        return "NO_TOOL_CONTRACT_IMPLICATED"
    if functions is None:
        fallback = system_history(history)
        return "SYSTEM_MESSAGE_FALLBACK:\n" + (fallback or "NO_CONTRACT_AVAILABLE")
    matched: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in iter_dicts(functions):
        names = schema_names(item)
        if not names or not any(name.casefold() in target_names for name in names):
            continue
        payload = canonical_json(item)
        if payload not in seen:
            seen.add(payload)
            matched.append(item)
    if not matched:
        return "NO_EXACT_CONTRACT_MATCH"
    return canonical_json(matched)


def row_identity(source: str, index: int, row: dict[str, Any]) -> tuple[str, str]:
    if source == "bfcl":
        natural = str(row["sample_id"])
    else:
        natural = str(row.get("task", row.get("sample_id", row.get("index", index))))
    return f"{source}:{index:04d}", f"{source}:{natural}"


def load_rows(
    phase: str, dataset_paths: dict[str, Path], config: dict[str, Any]
) -> list[dict[str, Any]]:
    if phase == "development":
        expected = config["development_inputs"]
        if set(dataset_paths) != set(expected):
            raise ValueError(f"development sources must be {sorted(expected)}")
    else:
        expected = {
            config["conditional_confirmation"]["source"]: config["conditional_confirmation"]
        }
        if set(dataset_paths) != set(expected):
            raise ValueError(f"confirmation source must be {sorted(expected)}")
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
            left_delta, right_delta, left_call, right_call, delta_meta = build_difference(
                row["action_chosen"], row["action_rejected"]
            )
            history = stable_text(row["history"])
            contracts = implicated_contracts(
                row.get("functions"), row["history"], (left_call, right_call)
            )
            rows.append(
                {
                    "row_id": row_id,
                    "cluster": cluster,
                    "source": source,
                    "history": history,
                    "contracts": contracts,
                    "chosen": stable_text(row["action_chosen"]),
                    "rejected": stable_text(row["action_rejected"]),
                    "chosen_delta": left_delta,
                    "rejected_delta": right_delta,
                    "delta_meta": delta_meta,
                }
            )
    return rows


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


def render_chat(tokenizer: Any, system: str, user: str) -> str:
    return tokenizer.apply_chat_template(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


def make_prompt(
    tokenizer: Any,
    system: str,
    fixed_blocks: list[tuple[str, str]],
    variable_blocks: list[tuple[str, str]],
    cap: int,
) -> tuple[str, int]:
    def render(values: list[str]) -> str:
        blocks = [f"{name}:\n{value}" for name, value in fixed_blocks]
        blocks.extend(
            f"{name}:\n{value}"
            for (name, _), value in zip(variable_blocks, values, strict=True)
        )
        return render_chat(tokenizer, system, "\n\n".join(blocks))

    empty = render(["" for _ in variable_blocks])
    fixed_tokens = len(tokenizer.encode(empty, add_special_tokens=False))
    if fixed_tokens >= cap:
        raise ValueError(f"untruncated fixed prompt exceeds cap: {fixed_tokens}")
    encoded = [
        tokenizer.encode(value, add_special_tokens=False) for _, value in variable_blocks
    ]
    budgets = allocate_budgets(
        [len(tokens) for tokens in encoded], cap - fixed_tokens - 16
    )
    clipped = [
        clip_token_ids(tokenizer, tokens, budget)
        for tokens, budget in zip(encoded, budgets, strict=True)
    ]
    prompt = render(clipped)
    prompt_tokens = len(tokenizer.encode(prompt, add_special_tokens=False))
    while prompt_tokens > cap and budgets:
        overflow = prompt_tokens - cap
        target = max(range(len(budgets)), key=lambda index: budgets[index])
        budgets[target] = max(0, budgets[target] - overflow - 8)
        clipped[target] = clip_token_ids(tokenizer, encoded[target], budgets[target])
        prompt = render(clipped)
        prompt_tokens = len(tokenizer.encode(prompt, add_special_tokens=False))
    if prompt_tokens > cap:
        raise ValueError(f"prompt exceeds cap: {prompt_tokens}")
    return prompt, prompt_tokens


def build_prompt_records(
    rows: list[dict[str, Any]], tokenizer: Any, config: dict[str, Any]
) -> list[dict[str, Any]]:
    cap = config["max_prompt_tokens"]
    records: list[dict[str, Any]] = []
    for row in rows:
        common_vars = [("HISTORY", row["history"]), ("IMPLICATED_CONTRACTS", row["contracts"])]
        specs = [
            (
                "sdej_forward",
                "pair",
                PAIR_SYSTEM,
                [
                    (
                        "TASK",
                        "Choose the next action supported by the evidence. Compare only the listed non-shared fields.",
                    ),
                    ("A_DIFFERENCE", row["chosen_delta"]),
                    ("B_DIFFERENCE", row["rejected_delta"]),
                ],
                common_vars,
            ),
            (
                "sdej_reverse",
                "pair",
                PAIR_SYSTEM,
                [
                    (
                        "TASK",
                        "Choose the next action supported by the evidence. Compare only the listed non-shared fields.",
                    ),
                    ("A_DIFFERENCE", row["rejected_delta"]),
                    ("B_DIFFERENCE", row["chosen_delta"]),
                ],
                common_vars,
            ),
            (
                "full_pair_forward",
                "pair",
                PAIR_SYSTEM,
                [
                    ("TASK", "Choose the next action supported by the evidence."),
                    ("A_ACTION", row["chosen"]),
                    ("B_ACTION", row["rejected"]),
                ],
                common_vars,
            ),
            (
                "full_pair_reverse",
                "pair",
                PAIR_SYSTEM,
                [
                    ("TASK", "Choose the next action supported by the evidence."),
                    ("A_ACTION", row["rejected"]),
                    ("B_ACTION", row["chosen"]),
                ],
                common_vars,
            ),
            (
                "delta_no_evidence_forward",
                "pair",
                PAIR_SYSTEM,
                [
                    (
                        "TASK",
                        "Choose the more operationally plausible next action from only the listed non-shared fields.",
                    ),
                    ("A_DIFFERENCE", row["chosen_delta"]),
                    ("B_DIFFERENCE", row["rejected_delta"]),
                ],
                [],
            ),
            (
                "delta_no_evidence_reverse",
                "pair",
                PAIR_SYSTEM,
                [
                    (
                        "TASK",
                        "Choose the more operationally plausible next action from only the listed non-shared fields.",
                    ),
                    ("A_DIFFERENCE", row["rejected_delta"]),
                    ("B_DIFFERENCE", row["chosen_delta"]),
                ],
                [],
            ),
            (
                "pointwise_chosen",
                "point",
                POINT_SYSTEM,
                [
                    ("TASK", "Is this proposed next action operationally supported?"),
                    ("PROPOSED_ACTION", row["chosen"]),
                ],
                common_vars,
            ),
            (
                "pointwise_rejected",
                "point",
                POINT_SYSTEM,
                [
                    ("TASK", "Is this proposed next action operationally supported?"),
                    ("PROPOSED_ACTION", row["rejected"]),
                ],
                common_vars,
            ),
        ]
        for name, score_kind, system, fixed, variables in specs:
            prompt, prompt_tokens = make_prompt(tokenizer, system, fixed, variables, cap)
            records.append(
                {
                    "prompt_id": f"{row['row_id']}::{name}",
                    "row_id": row["row_id"],
                    "name": name,
                    "score_kind": score_kind,
                    "prompt": prompt,
                    "prompt_tokens": prompt_tokens,
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
        raise ValueError("model snapshot path mismatch")
    for record in manifest["files"]:
        path = Path(record["resolved_path"])
        if path.resolve().parent != model_dir.resolve():
            raise ValueError(f"model file outside snapshot: {path}")
        if path.stat().st_size != record["bytes"] or sha256_file(path) != record["sha256"]:
            raise ValueError(f"model file mismatch: {path}")


def score_prompts(
    prompt_records: list[dict[str, Any]],
    tokenizer: Any,
    model: Any,
    config: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    batches: list[list[int]] = []
    current: list[int] = []
    current_max = 0
    for index, record in enumerate(prompt_records):
        proposed_max = max(current_max, record["prompt_tokens"])
        if current and (
            len(current) >= config["max_batch_size"]
            or proposed_max * (len(current) + 1) > config["max_batch_tokens"]
        ):
            batches.append(current)
            current = []
            current_max = 0
        current.append(index)
        current_max = max(current_max, record["prompt_tokens"])
    if current:
        batches.append(current)

    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    results: dict[str, dict[str, Any]] = {}
    for batch_number, indices in enumerate(batches, start=1):
        prompts = [prompt_records[index]["prompt"] for index in indices]
        encoded = tokenizer(
            prompts, return_tensors="pt", padding=True, add_special_tokens=False
        ).to("cuda")
        with torch.inference_mode():
            logits = model(**encoded, logits_to_keep=1).logits[:, -1, :].float()
            log_probs = torch.log_softmax(logits, dim=-1)
        for local_index, record_index in enumerate(indices):
            record = prompt_records[record_index]
            if record["score_kind"] == "pair":
                left = float(log_probs[local_index, config["a_token_id"]].cpu())
                right = float(log_probs[local_index, config["b_token_id"]].cpu())
                probability = 1.0 / (1.0 + math.exp(right - left))
                labels = {"a_logp": left, "b_logp": right, "a_probability": probability}
            else:
                left = float(log_probs[local_index, config["yes_token_id"]].cpu())
                right = float(log_probs[local_index, config["no_token_id"]].cpu())
                probability = 1.0 / (1.0 + math.exp(right - left))
                labels = {
                    "yes_logp": left,
                    "no_logp": right,
                    "yes_probability": probability,
                }
            results[record["prompt_id"]] = {
                "prompt_sha256": sha256_bytes(record["prompt"].encode("utf-8")),
                "prompt_tokens": record["prompt_tokens"],
                "batch_number": batch_number,
                **labels,
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


def pair_aligned(
    scores: dict[str, dict[str, Any]], row_id: str, prefix: str
) -> tuple[float, float, float, float]:
    forward = scores[f"{row_id}::{prefix}_forward"]["a_probability"]
    reverse_a = scores[f"{row_id}::{prefix}_reverse"]["a_probability"]
    reverse = 1.0 - reverse_a
    probability = 0.5 * (forward + reverse)
    consistency = 1.0 if (forward > 0.5) == (reverse > 0.5) else 0.0
    return probability, probability - 0.5, consistency, forward


def build_raw_rows(
    rows: list[dict[str, Any]], scores: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        row_id = row["row_id"]
        sdej_prob, sdej_margin, consistency, forward = pair_aligned(scores, row_id, "sdej")
        full_prob, full_margin, full_consistency, _ = pair_aligned(
            scores, row_id, "full_pair"
        )
        noev_prob, noev_margin, noev_consistency, _ = pair_aligned(
            scores, row_id, "delta_no_evidence"
        )
        chosen_yes = scores[f"{row_id}::pointwise_chosen"]["yes_probability"]
        rejected_yes = scores[f"{row_id}::pointwise_rejected"]["yes_probability"]
        point_margin = chosen_yes - rejected_yes
        methods = {
            "sdej": {
                "margin": sdej_margin,
                "accuracy": tie_accuracy(sdej_margin),
                "aligned_chosen_probability": sdej_prob,
                "order_consistency": consistency,
            },
            "full_pair": {
                "margin": full_margin,
                "accuracy": tie_accuracy(full_margin),
                "aligned_chosen_probability": full_prob,
                "order_consistency": full_consistency,
            },
            "full_pointwise": {
                "margin": point_margin,
                "accuracy": tie_accuracy(point_margin),
                "chosen_yes_probability": chosen_yes,
                "rejected_yes_probability": rejected_yes,
            },
            "delta_no_evidence": {
                "margin": noev_margin,
                "accuracy": tie_accuracy(noev_margin),
                "aligned_chosen_probability": noev_prob,
                "order_consistency": noev_consistency,
            },
            "delta_forward": {
                "margin": forward - 0.5,
                "accuracy": tie_accuracy(forward - 0.5),
                "chosen_probability": forward,
            },
        }
        prompt_names = (
            "sdej_forward",
            "sdej_reverse",
            "full_pair_forward",
            "full_pair_reverse",
            "delta_no_evidence_forward",
            "delta_no_evidence_reverse",
            "pointwise_chosen",
            "pointwise_rejected",
        )
        output.append(
            {
                "row_id": row_id,
                "cluster": row["cluster"],
                "source": row["source"],
                "projection_sha256": sha256_bytes(
                    canonical_json(
                        {
                            "history": row["history"],
                            "contracts": row["contracts"],
                            "chosen": row["chosen"],
                            "rejected": row["rejected"],
                            "chosen_delta": row["chosen_delta"],
                            "rejected_delta": row["rejected_delta"],
                            "delta_meta": row["delta_meta"],
                        }
                    ).encode("utf-8")
                ),
                "delta_meta": row["delta_meta"],
                "prompts": {name: scores[f"{row_id}::{name}"] for name in prompt_names},
                "methods": methods,
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
    deltas: list[float] = []
    for _ in range(repeats):
        sampled: list[dict[str, Any]] = []
        for source in sorted(grouped):
            clusters = sorted(grouped[source])
            for _ in clusters:
                chosen_cluster = clusters[rng.randrange(len(clusters))]
                sampled.extend(grouped[source][chosen_cluster])
        candidate = mean_accuracy(sampled, "sdej")
        control = mean_accuracy(sampled, comparator)
        deltas.append(candidate - control)
    values = np.asarray(deltas, dtype=np.float64)
    return {
        "repeats": repeats,
        "seed": seed,
        "lower_95": float(np.quantile(values, 0.025)),
        "median": float(np.quantile(values, 0.5)),
        "upper_95": float(np.quantile(values, 0.975)),
    }


def summarize(
    raw_rows: list[dict[str, Any]], config: dict[str, Any], phase: str, state: dict[str, Any] | None
) -> dict[str, Any]:
    overall = {method: mean_accuracy(raw_rows, method) for method in METHODS}
    by_source: dict[str, dict[str, float]] = {}
    for source in sorted({row["source"] for row in raw_rows}):
        subset = [row for row in raw_rows if row["source"] == source]
        by_source[source] = {method: mean_accuracy(subset, method) for method in METHODS}
    if phase == "development":
        strongest = sorted(CONTROL_METHODS, key=lambda name: (-overall[name], name))[0]
    else:
        if state is None:
            raise ValueError("confirmation requires state")
        strongest = state["strongest_control"]
    source_deltas = {
        source: metrics["sdej"] - metrics[strongest] for source, metrics in by_source.items()
    }
    bootstrap = bootstrap_delta(
        raw_rows, strongest, config["bootstrap_repeats"], config["seed"]
    )
    return {
        "schema_version": 1,
        "experiment_id": config["experiment_id"],
        "phase": phase,
        "row_count": len(raw_rows),
        "cluster_count": len({row["cluster"] for row in raw_rows}),
        "source_counts": {
            source: sum(row["source"] == source for row in raw_rows)
            for source in sorted({row["source"] for row in raw_rows})
        },
        "overall_accuracy": overall,
        "source_accuracy": by_source,
        "strongest_control": strongest,
        "candidate_delta": overall["sdej"] - overall[strongest],
        "source_deltas": source_deltas,
        "positive_source_count": sum(delta > 0 for delta in source_deltas.values()),
        "candidate_order_consistency": float(
            np.mean([row["methods"]["sdej"]["order_consistency"] for row in raw_rows])
        ),
        "bootstrap_delta": bootstrap,
        "prompt_count": len(raw_rows) * 8,
        "delta_statistics": {
            "mean_shared_field_count": float(
                np.mean([row["delta_meta"]["shared_field_count"] for row in raw_rows])
            ),
            "mean_difference_key_count": float(
                np.mean([len(row["delta_meta"]["difference_keys"]) for row in raw_rows])
            ),
        },
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
    dataset_paths = parse_dataset_args(args.dataset)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    validate_model(args.model_dir.resolve(), args.model_manifest.resolve(), config)
    state = None
    if args.phase == "confirmation":
        if args.state is None:
            raise ValueError("--state is required for confirmation")
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if state["candidate_sha256"] != config["candidate_sha256"]:
            raise ValueError("state candidate mismatch")
        if state["config_sha256"] != sha256_file(config_path):
            raise ValueError("state config mismatch")
    elif args.state is not None:
        raise ValueError("--state is not used for development")

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_dir.resolve(), local_files_only=True, trust_remote_code=False
    )
    expected_tokens = {
        "A": config["a_token_id"],
        "B": config["b_token_id"],
        "Yes": config["yes_token_id"],
        "No": config["no_token_id"],
    }
    for text, token_id in expected_tokens.items():
        if tokenizer.encode(text, add_special_tokens=False) != [token_id]:
            raise ValueError(f"token id mismatch for {text}")
    rows = load_rows(args.phase, dataset_paths, config)
    prompt_records = build_prompt_records(rows, tokenizer, config)
    if len(prompt_records) != len(rows) * 8:
        raise ValueError("prompt count mismatch")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir.resolve(),
        local_files_only=True,
        trust_remote_code=False,
        dtype=torch.float16,
    ).to("cuda")
    model.eval()
    scores = score_prompts(prompt_records, tokenizer, model, config)
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
        "prompts_recomputed": len(prompt_records),
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
