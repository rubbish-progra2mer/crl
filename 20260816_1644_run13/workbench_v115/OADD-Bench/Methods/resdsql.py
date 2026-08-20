#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
from collections import OrderedDict
from pathlib import Path
from typing import Any

from schema import (
    DenseSchemaRetriever,
    build_schema_vectors,
    load_or_build_schema,
    unique_codes,
)


ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_COMMIT = "7472f7a51fdd054d8139b1bc2627d955aff855e4"
CANDIDATE_POOL_SIZE = 1000
MAX_COLUMNS_PER_PACKET = 12
MAX_SEQUENCE_LENGTH = 512


def load_cases(path: Path, limit: int | None) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    cases = []
    for row in rows[:limit]:
        targets = [value for value in row["hrs_column_ids"].split(";") if value.strip()]
        cases.append(
            {
                "record_id": row["record_id"],
                "question": row["research_question"],
                "years": {
                    value.strip()
                    for value in row["allowed_years"].split(";")
                    if value.strip()
                },
                "target_size": len(targets),
            }
        )
    return cases


def compact(value: Any, limit: int) -> str:
    return " ".join(str(value or "").split())[:limit]


def table_text(row: dict[str, Any]) -> str:
    return compact(row.get("table_name") or row.get("table_key"), 160)


def column_text(row: dict[str, Any]) -> str:
    values = [
        compact(row.get("column_code"), 40),
        compact(row.get("label"), 100),
        compact(row.get("description"), 220),
    ]
    return " ; ".join(value for value in values if value)


def load_classifier(repo: Path) -> type:
    model_path = repo / "utils" / "classifier_model.py"
    if not model_path.exists():
        raise FileNotFoundError(f"Missing official RESDSQL model: {model_path}")
    spec = importlib.util.spec_from_file_location("resdsql_classifier", model_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {model_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.MyClassifier


def packet_tokens(question: str, table: str, columns: list[str]) -> tuple[list[str], int, list[int]]:
    tokens = [question, "|", table, ":"]
    column_word_ids = []
    for column in columns:
        column_word_ids.append(len(tokens))
        tokens.extend([column, ","])
    if columns:
        tokens.pop()
    return tokens, 2, column_word_ids


def packet_fits(tokenizer: Any, question: str, table: str, columns: list[str]) -> bool:
    tokens, _, column_word_ids = packet_tokens(question, table, columns)
    encoded = tokenizer(
        tokens,
        is_split_into_words=True,
        add_special_tokens=True,
        truncation=True,
        max_length=MAX_SEQUENCE_LENGTH,
    )
    retained = {word_id for word_id in encoded.word_ids() if word_id is not None}
    return all(word_id in retained for word_id in column_word_ids)


def make_packets(
    question: str,
    candidates: list[int],
    rows: list[dict[str, Any]],
    tokenizer: Any,
) -> list[dict[str, Any]]:
    by_table: OrderedDict[str, list[int]] = OrderedDict()
    for index in candidates:
        by_table.setdefault(rows[index]["table_key"], []).append(index)
    packets = []
    for indices in by_table.values():
        table = table_text(rows[indices[0]])
        pending: list[int] = []
        for index in indices:
            proposed = pending + [index]
            descriptions = [column_text(rows[value]) for value in proposed]
            if pending and (
                len(proposed) > MAX_COLUMNS_PER_PACKET
                or not packet_fits(tokenizer, question, table, descriptions)
            ):
                packets.append({"table": table, "indices": pending})
                pending = [index]
            else:
                pending = proposed
        if pending:
            packets.append({"table": table, "indices": pending})
    return packets


def prepare_batch(
    question: str,
    packets: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    tokenizer: Any,
    device: Any,
) -> tuple[Any, Any, list[list[int]], list[list[list[int]]], list[list[list[int]]], list[list[int]]]:
    batch_tokens, table_words, column_words = [], [], []
    for packet in packets:
        tokens, table_word, column_word = packet_tokens(
            question,
            packet["table"],
            [column_text(rows[index]) for index in packet["indices"]],
        )
        batch_tokens.append(tokens)
        table_words.append(table_word)
        column_words.append(column_word)
    encoded = tokenizer(
        batch_tokens,
        return_tensors="pt",
        is_split_into_words=True,
        padding="max_length",
        truncation=True,
        max_length=MAX_SEQUENCE_LENGTH,
    )
    questions, tables, columns, counts = [], [], [], []
    for batch_index, packet in enumerate(packets):
        word_ids = encoded.word_ids(batch_index=batch_index)
        question_ids = [index for index, word_id in enumerate(word_ids) if word_id == 0]
        table_ids = [
            index
            for index, word_id in enumerate(word_ids)
            if word_id == table_words[batch_index]
        ]
        column_ids = [
            [index for index, word_id in enumerate(word_ids) if word_id == column_word]
            for column_word in column_words[batch_index]
        ]
        if not question_ids or not table_ids or any(not value for value in column_ids):
            raise RuntimeError("RESDSQL packet was truncated unexpectedly")
        questions.append(question_ids)
        tables.append([table_ids])
        columns.append(column_ids)
        counts.append([len(packet["indices"])])
    return (
        encoded["input_ids"].to(device),
        encoded["attention_mask"].to(device),
        questions,
        columns,
        tables,
        counts,
    )


def rerank(
    case: dict[str, Any],
    candidates: list[int],
    rows: list[dict[str, Any]],
    tokenizer: Any,
    model: Any,
    torch: Any,
    device: Any,
    batch_size: int,
) -> list[int]:
    packets = make_packets(case["question"], candidates, rows, tokenizer)
    source_rank = {index: rank for rank, index in enumerate(candidates)}
    scored = []
    for start in range(0, len(packets), batch_size):
        batch = packets[start : start + batch_size]
        prepared = prepare_batch(case["question"], batch, rows, tokenizer, device)
        with torch.inference_mode():
            with torch.autocast(
                device_type="cuda",
                dtype=torch.float16,
                enabled=device.type == "cuda",
            ):
                outputs = model(
                    encoder_input_ids=prepared[0],
                    encoder_attention_mask=prepared[1],
                    batch_aligned_question_ids=prepared[2],
                    batch_aligned_column_info_ids=prepared[3],
                    batch_aligned_table_name_ids=prepared[4],
                    batch_column_number_in_each_table=prepared[5],
                )
        for local_index, packet in enumerate(batch):
            table_probability = float(
                torch.softmax(
                    outputs["batch_table_name_cls_logits"][local_index].float(), dim=1
                )[0, 1].cpu()
            )
            column_probabilities = torch.softmax(
                outputs["batch_column_info_cls_logits"][local_index].float(), dim=1
            )[:, 1].cpu().tolist()
            for index, probability in zip(
                packet["indices"], column_probabilities, strict=True
            ):
                combined = math.log(max(table_probability, 1e-12)) + math.log(
                    max(float(probability), 1e-12)
                )
                scored.append((combined, float(probability), source_rank[index], index))
    scored.sort(key=lambda value: (-value[0], -value[1], value[2]))
    return [value[3] for value in scored]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the adapted RESDSQL schema ranker.")
    parser.add_argument("--official-repo", type=Path, required=True)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=ROOT / "benchmark" / "OADD-Bench" / "OADD_Bench.csv",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=ROOT / "benchmark" / "HRS_metadata" / "metadata.jsonl",
    )
    parser.add_argument(
        "--metadata-fixes",
        type=Path,
        default=ROOT / "benchmark" / "HRS_metadata" / "metadata_fixes.jsonl",
    )
    parser.add_argument("--cache-dir", type=Path, default=ROOT / "cache")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "resdsql.jsonl")
    parser.add_argument("--provider", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    import torch
    from transformers import RobertaTokenizerFast

    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    checkpoint_state = args.checkpoint_dir / "dense_classifier.pt"
    if not checkpoint_state.exists():
        raise FileNotFoundError(checkpoint_state)
    cases = load_cases(args.benchmark, args.limit)
    rows, fingerprint = load_or_build_schema(
        args.metadata, args.metadata_fixes, args.cache_dir
    )
    vectors = build_schema_vectors(rows, fingerprint, args.cache_dir, args.provider)
    retriever = DenseSchemaRetriever(
        rows, vectors, args.cache_dir, args.provider
    )
    tokenizer = RobertaTokenizerFast.from_pretrained(
        args.checkpoint_dir, local_files_only=True
    )
    classifier_type = load_classifier(args.official_repo)
    model = classifier_type(str(args.checkpoint_dir), len(tokenizer), "test")
    state = torch.load(checkpoint_state, map_location="cpu", weights_only=True)
    incompatible = model.load_state_dict(state, strict=False)
    unexpected = set(incompatible.unexpected_keys) - {
        "plm_encoder.embeddings.position_ids"
    }
    if incompatible.missing_keys or unexpected:
        raise RuntimeError(
            f"Checkpoint mismatch: missing={incompatible.missing_keys}, unexpected={unexpected}"
        )
    device = torch.device(args.device)
    model.to(device).eval()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for position, case in enumerate(cases, start=1):
            candidates = retriever.search(
                case["question"], case["years"], CANDIDATE_POOL_SIZE
            )
            reranked = rerank(
                case,
                candidates,
                rows,
                tokenizer,
                model,
                torch,
                device,
                args.batch_size,
            )
            columns = unique_codes(
                [reranked, candidates], rows, 5 * case["target_size"]
            )
            predictions = {
                str(multiplier): columns[: multiplier * case["target_size"]]
                for multiplier in (1, 2, 5)
            }
            handle.write(
                json.dumps(
                    {"record_id": case["record_id"], "predictions": predictions}
                )
                + "\n"
            )
            handle.flush()
            print(
                json.dumps(
                    {
                        "stage": "resdsql",
                        "completed": position,
                        "total": len(cases),
                    }
                ),
                flush=True,
            )


if __name__ == "__main__":
    main()
