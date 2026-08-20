from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import platform
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable

import numpy as np


TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")
ROWS_ENDPOINT = "https://datasets-server.huggingface.co/rows"
META_ENDPOINT = "https://huggingface.co/api/datasets"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"Expected JSON object row: {path}")
            rows.append(value)
    return rows


def fetch_json(url: str, delay_seconds: float = 0.0) -> dict[str, object]:
    if delay_seconds:
        time.sleep(delay_seconds)
    request = urllib.request.Request(url, headers={"User-Agent": "CRL-ToolRet-Audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object from {url}")
    return value


def dataset_sha(dataset_id: str) -> str:
    encoded = "/".join(urllib.parse.quote(part, safe="") for part in dataset_id.split("/"))
    value = fetch_json(f"{META_ENDPOINT}/{encoded}")
    sha = value.get("sha")
    if not isinstance(sha, str):
        raise ValueError(f"Dataset metadata has no SHA: {dataset_id}")
    return sha


def rows_url(dataset_id: str, config: str, split: str, offset: int) -> str:
    query = urllib.parse.urlencode(
        {
            "dataset": dataset_id,
            "config": config,
            "split": split,
            "offset": offset,
            "length": 100,
        }
    )
    return f"{ROWS_ENDPOINT}?{query}"


def fetch_rows(
    dataset_id: str,
    config: str,
    split: str,
    workers: int,
    delay_seconds: float,
) -> list[dict[str, object]]:
    first = fetch_json(rows_url(dataset_id, config, split, 0), delay_seconds)
    total = first.get("num_rows_total")
    if not isinstance(total, int):
        raise ValueError(f"Rows response has no total: {dataset_id}/{config}")
    pages: dict[int, dict[str, object]] = {0: first}
    offsets = list(range(100, total, 100))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        values = executor.map(
            lambda offset: fetch_json(
                rows_url(dataset_id, config, split, offset), delay_seconds
            ),
            offsets,
        )
        for offset, value in zip(offsets, values, strict=True):
            pages[offset] = value

    rows: list[dict[str, object]] = []
    for offset in sorted(pages):
        raw_rows = pages[offset].get("rows")
        if not isinstance(raw_rows, list):
            raise ValueError(f"Rows page is malformed: {dataset_id}/{config}/{offset}")
        for item in raw_rows:
            if not isinstance(item, dict) or not isinstance(item.get("row"), dict):
                raise ValueError(f"Row is malformed: {dataset_id}/{config}/{offset}")
            rows.append(item["row"])
    if len(rows) != total:
        raise ValueError(f"Row count mismatch for {dataset_id}/{config}: {len(rows)} != {total}")
    return rows


def acquire(args: argparse.Namespace) -> int:
    config = read_json(args.config)
    query_spec = config["query_dataset"]
    tool_spec = config["tool_dataset"]
    if not isinstance(query_spec, dict) or not isinstance(tool_spec, dict):
        raise ValueError("Dataset configuration is malformed")
    query_id = str(query_spec["id"])
    tool_id = str(tool_spec["id"])
    expected_query_sha = str(query_spec["revision"])
    expected_tool_sha = str(tool_spec["revision"])
    actual_query_sha = dataset_sha(query_id)
    actual_tool_sha = dataset_sha(tool_id)
    if actual_query_sha != expected_query_sha or actual_tool_sha != expected_tool_sha:
        raise ValueError("Pinned dataset revision is no longer the served revision")

    phase_configs = config["phases"]
    if not isinstance(phase_configs, dict) or not isinstance(phase_configs.get(args.phase), list):
        raise ValueError(f"Unknown phase: {args.phase}")
    workers = int(config["http_workers"])
    delay_seconds = float(config["http_delay_seconds"])
    query_rows: list[dict[str, object]] = []
    query_counts: dict[str, int] = {}
    for source_config in phase_configs[args.phase]:
        rows = fetch_rows(
            query_id,
            str(source_config),
            str(query_spec["split"]),
            workers,
            delay_seconds,
        )
        query_counts[str(source_config)] = len(rows)
        for row in rows:
            row["source_config"] = str(source_config)
            query_rows.append(row)
    write_jsonl(args.queries_output, query_rows)

    corpus_counts: dict[str, int] = {}
    if args.corpus_output is not None:
        corpus_rows: list[dict[str, object]] = []
        raw_tool_configs = tool_spec.get("configs")
        if not isinstance(raw_tool_configs, list):
            raise ValueError("Tool configs are malformed")
        for tool_config in raw_tool_configs:
            rows = fetch_rows(
                tool_id,
                str(tool_config),
                str(tool_spec["split"]),
                workers,
                delay_seconds,
            )
            corpus_counts[str(tool_config)] = len(rows)
            for row in rows:
                corpus_rows.append(
                    {
                        "category": str(tool_config),
                        "documentation": row["documentation"],
                        "id": row["id"],
                    }
                )
        write_jsonl(args.corpus_output, corpus_rows)

    manifest = {
        "schema_version": 1,
        "phase": args.phase,
        "query_dataset": {"id": query_id, "revision": actual_query_sha},
        "tool_dataset": {"id": tool_id, "revision": actual_tool_sha},
        "query_configs": list(phase_configs[args.phase]),
        "query_counts": query_counts,
        "queries": {
            "path": str(args.queries_output.resolve()),
            "sha256": sha256_file(args.queries_output),
            "rows": len(query_rows),
        },
        "corpus_counts": corpus_counts,
    }
    if args.corpus_output is not None:
        manifest["corpus"] = {
            "path": str(args.corpus_output.resolve()),
            "sha256": sha256_file(args.corpus_output),
            "rows": sum(corpus_counts.values()),
        }
    write_json(args.manifest_output, manifest)
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def target_ids(row: dict[str, object]) -> set[str]:
    labels = json.loads(str(row["labels"]))
    if not isinstance(labels, list):
        raise ValueError("Query labels are malformed")
    ids = {str(item["id"]) for item in labels if isinstance(item, dict) and "id" in item}
    if not ids:
        raise ValueError(f"Query has no targets: {row.get('id')}")
    return ids


def query_key(row: dict[str, object]) -> tuple[str, str]:
    return str(row["source_config"]), str(row["id"])


def assign_mismatches(
    rows: list[dict[str, object]], donor_count: int
) -> dict[tuple[str, str], list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["source_config"])].append(row)
    assignments: dict[tuple[str, str], list[dict[str, object]]] = {}
    for source_config, source_rows in grouped.items():
        metadata = [
            (row, target_ids(row), len(tokenize(str(row["instruction"]))))
            for row in source_rows
        ]
        for row, labels, length in metadata:
            candidates: list[tuple[int, str, dict[str, object], set[str], int]] = []
            for other, other_labels, other_length in metadata:
                if row["id"] == other["id"] or labels.intersection(other_labels):
                    continue
                tie = hashlib.sha256(
                    f"{row['id']}\0{other['id']}".encode("utf-8")
                ).hexdigest()
                candidates.append(
                    (abs(length - other_length), tie, other, other_labels, other_length)
                )
            ordered = sorted(candidates, key=lambda item: (item[0], item[1]))
            if len(ordered) < donor_count:
                raise ValueError(
                    f"Fewer than {donor_count} wrong-target instruction matches for {row['id']}"
                )
            assignments[query_key(row)] = [
                {
                    "instruction": str(donor["instruction"]),
                    "donor_query_id": str(donor["id"]),
                    "donor_source_config": source_config,
                    "donor_target_ids": sorted(donor_labels),
                    "donor_token_length": donor_length,
                    "recipient_token_length": length,
                    "token_length_difference": difference,
                    "target_overlap_count": len(labels.intersection(donor_labels)),
                }
                for difference, _, donor, donor_labels, donor_length in ordered[:donor_count]
            ]
    return assignments


def query_views(
    row: dict[str, object], mismatches: list[dict[str, object]], generic_instruction: str
) -> dict[str, str]:
    query = str(row["query"])
    aligned = str(row["instruction"])
    views = {
        "query_only": query,
        "aligned_full": f"{aligned}\n{query}",
        "generic_full": f"{generic_instruction}\n{query}",
    }
    for index, mismatch in enumerate(mismatches, start=1):
        views[f"mismatched_full_{index}"] = f"{mismatch['instruction']}\n{query}"
    return views


class BM25:
    def __init__(self, documents: list[str], k1: float, b: float) -> None:
        self.k1 = k1
        self.b = b
        self.doc_lengths = np.asarray([len(tokenize(text)) for text in documents], dtype=np.float64)
        self.avgdl = float(self.doc_lengths.mean())
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for index, text in enumerate(documents):
            for term, frequency in Counter(tokenize(text)).items():
                self.postings[term].append((index, frequency))
        count = len(documents)
        self.document_count = count
        self.idf = {
            term: math.log(1.0 + (count - len(items) + 0.5) / (len(items) + 0.5))
            for term, items in self.postings.items()
        }

    def topk(self, query: str, k: int) -> list[int]:
        scores: dict[int, float] = defaultdict(float)
        for term in set(tokenize(query)):
            idf = self.idf.get(term)
            if idf is None:
                continue
            for index, frequency in self.postings[term]:
                denominator = frequency + self.k1 * (
                    1.0 - self.b + self.b * self.doc_lengths[index] / self.avgdl
                )
                scores[index] += idf * frequency * (self.k1 + 1.0) / denominator
        ranked = [
            item[2]
            for item in heapq.nlargest(
                k,
                ((score, -index, index) for index, score in scores.items()),
            )
        ]
        if len(ranked) < k:
            selected = set(ranked)
            ranked.extend(
                index
                for index in range(self.document_count)
                if index not in selected
            )
        return ranked[:k]


def retrieval_metrics(ranked_ids: list[str], targets: set[str], k: int) -> dict[str, float]:
    gains = [1.0 if item in targets else 0.0 for item in ranked_ids[:k]]
    dcg = sum(gain / math.log2(rank + 2.0) for rank, gain in enumerate(gains))
    ideal = sum(1.0 / math.log2(rank + 2.0) for rank in range(min(k, len(targets))))
    hits = sum(gains)
    return {
        "ndcg_at_10": dcg / ideal if ideal else 0.0,
        "recall_at_10": hits / len(targets),
        "completeness_at_10": 1.0 if hits == len(targets) else 0.0,
    }


def lexical_support(
    instruction: str,
    targets: set[str],
    doc_tokens: list[set[str]],
    index_by_id: dict[str, int],
    idf: dict[str, float],
) -> float:
    target_terms: set[str] = set()
    for target in targets:
        index = index_by_id.get(target)
        if index is not None:
            target_terms.update(doc_tokens[index])
    terms = set(tokenize(instruction))
    denominator = sum(idf.get(term, 0.0) for term in terms)
    numerator = sum(idf.get(term, 0.0) for term in terms.intersection(target_terms))
    return numerator / denominator if denominator else 0.0


def summarize(
    raw_rows: list[dict[str, object]],
    source_configs: list[str],
    donor_count: int,
    seed: int,
    replicates: int,
) -> dict[str, object]:
    matching_rows = [
        row
        for row in raw_rows
        if row["retriever"] == "bm25" and row["view"] == "aligned_full"
    ]
    donors = [donor for row in matching_rows for donor in row["matched_donors"]]
    differences = [int(donor["token_length_difference"]) for donor in donors]
    summary: dict[str, object] = {
        "sources": source_configs,
        "matching": {
            "queries": len(matching_rows),
            "donors_per_query": donor_count,
            "donor_pairs": len(donors),
            "mean_token_length_difference": float(np.mean(differences)),
            "max_token_length_difference": max(differences),
            "target_overlap_pairs": sum(
                int(donor["target_overlap_count"]) > 0 for donor in donors
            ),
        },
        "retrievers": {},
    }
    rng = np.random.default_rng(seed)
    for retriever in ("bm25", "minilm"):
        source_effects: dict[str, dict[str, float]] = {}
        for source in source_configs:
            selected = [
                row
                for row in raw_rows
                if row["retriever"] == retriever and row["source_config"] == source
            ]
            by_query: dict[str, dict[str, dict[str, float]]] = defaultdict(dict)
            for row in selected:
                by_query[str(row["query_id"])][str(row["view"])] = row["metrics"]
            mismatch_views = [f"mismatched_full_{index}" for index in range(1, donor_count + 1)]
            ndcg_deltas = []
            control_stdevs = []
            for values in by_query.values():
                controls = [float(values[view]["ndcg_at_10"]) for view in mismatch_views]
                ndcg_deltas.append(
                    float(values["aligned_full"]["ndcg_at_10"]) - float(np.mean(controls))
                )
                control_stdevs.append(float(np.std(controls)))
            source_effects[source] = {
                "queries": float(len(ndcg_deltas)),
                "aligned_minus_mean_mismatched_ndcg_at_10": float(np.mean(ndcg_deltas)),
                "mean_control_ndcg_standard_deviation": float(np.mean(control_stdevs)),
            }
        effects = np.asarray(
            [source_effects[source]["aligned_minus_mean_mismatched_ndcg_at_10"] for source in source_configs],
            dtype=np.float64,
        )
        bootstrap = np.empty(replicates, dtype=np.float64)
        for index in range(replicates):
            bootstrap[index] = float(rng.choice(effects, size=len(effects), replace=True).mean())
        lexical = [
            float(row["aligned_lexical_support"])
            - float(np.mean(row["mismatched_lexical_supports"]))
            for row in raw_rows
            if row["retriever"] == retriever and row["view"] == "aligned_full"
        ]
        summary["retrievers"][retriever] = {
            "source_effects": source_effects,
            "equal_source_mean_aligned_minus_mean_mismatched_ndcg_at_10": float(effects.mean()),
            "median_source_effect": float(np.median(effects)),
            "cluster_bootstrap_95_percent": [
                float(np.quantile(bootstrap, 0.025)),
                float(np.quantile(bootstrap, 0.975)),
            ],
            "positive_source_count": int(np.sum(effects > 0.0)),
            "non_positive_sources": [
                source for source, effect in zip(source_configs, effects, strict=True) if effect <= 0.0
            ],
            "mean_aligned_minus_mean_mismatched_lexical_support": float(np.mean(lexical)),
        }
    return summary


def environment_record(model_id: str, model_revision: str) -> dict[str, object]:
    import sentence_transformers
    import torch

    driver = subprocess.run(
        ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()
    return {
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "numpy": np.__version__,
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0),
        "capability": list(torch.cuda.get_device_capability(0)),
        "nvidia_driver": driver,
        "sentence_transformers": sentence_transformers.__version__,
        "sentence_transformer_model": model_id,
        "sentence_transformer_revision": model_revision,
    }


def evaluate(args: argparse.Namespace) -> int:
    from sentence_transformers import SentenceTransformer

    config = read_json(args.config)
    corpus = read_jsonl(args.corpus)
    queries = read_jsonl(args.queries)
    source_configs = [str(value) for value in config["phases"][args.phase]]
    observed_sources = sorted({str(row["source_config"]) for row in queries})
    if observed_sources != sorted(source_configs):
        raise ValueError("Query source configs do not match the frozen phase")
    ids = [str(row["id"]) for row in corpus]
    if len(ids) != len(set(ids)):
        raise ValueError("Corpus IDs are not unique")
    index_by_id = {value: index for index, value in enumerate(ids)}
    documents = [str(row["documentation"]) for row in corpus]
    donor_count = int(config["mismatch_donors"])
    mismatches = assign_mismatches(queries, donor_count)
    generic = str(config["generic_instruction"])
    views = {
        query_key(row): query_views(row, mismatches[query_key(row)], generic)
        for row in queries
    }
    expected_views = {str(value) for value in config["views"]}
    if any(set(value) != expected_views for value in views.values()):
        raise ValueError("Constructed query views do not match the frozen config")

    bm25_config = config["retrievers"]["bm25"]
    bm25 = BM25(documents, float(bm25_config["k1"]), float(bm25_config["b"]))
    doc_tokens = [set(tokenize(text)) for text in documents]
    raw: list[dict[str, object]] = []
    top_k = int(config["top_k"])
    for row in queries:
        query_id = str(row["id"])
        key = query_key(row)
        matches = mismatches[key]
        targets = target_ids(row)
        aligned_support = lexical_support(
            str(row["instruction"]), targets, doc_tokens, index_by_id, bm25.idf
        )
        mismatch_supports = [
            lexical_support(
                str(match["instruction"]), targets, doc_tokens, index_by_id, bm25.idf
            )
            for match in matches
        ]
        for view, text in views[key].items():
            ranked = [ids[index] for index in bm25.topk(text, top_k)]
            raw.append(
                {
                    "aligned_lexical_support": aligned_support,
                    "matched_donors": matches,
                    "metrics": retrieval_metrics(ranked, targets, top_k),
                    "mismatched_lexical_supports": mismatch_supports,
                    "query_id": query_id,
                    "ranked_ids": ranked,
                    "retriever": "bm25",
                    "source_config": row["source_config"],
                    "target_ids": sorted(targets),
                    "view": view,
                }
            )

    minilm_config = config["retrievers"]["minilm"]
    model = SentenceTransformer(
        str(minilm_config["model"]),
        device=str(minilm_config["device"]),
        revision=str(minilm_config["revision"]),
        local_files_only=True,
    )
    if args.corpus_embeddings.exists():
        corpus_embeddings = np.load(args.corpus_embeddings)
        if corpus_embeddings.shape[0] != len(corpus):
            raise ValueError("Corpus embedding row count does not match corpus")
    else:
        corpus_embeddings = model.encode(
            documents,
            batch_size=int(minilm_config["batch_size"]),
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True,
        ).astype(np.float32)
        np.save(args.corpus_embeddings, corpus_embeddings)

    dense_inputs: list[tuple[dict[str, object], str, str]] = []
    for row in queries:
        for view, text in views[query_key(row)].items():
            dense_inputs.append((row, view, text))
    batch_size = int(minilm_config["batch_size"])
    for start in range(0, len(dense_inputs), batch_size):
        batch = dense_inputs[start : start + batch_size]
        query_embeddings = model.encode(
            [item[2] for item in batch],
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype(np.float32)
        scores = query_embeddings @ corpus_embeddings.T
        candidates = np.argpartition(scores, -top_k, axis=1)[:, -top_k:]
        for offset, (row, view, _) in enumerate(batch):
            indices = candidates[offset]
            ordered = indices[np.argsort(scores[offset, indices])[::-1]]
            ranked = [ids[int(index)] for index in ordered]
            query_id = str(row["id"])
            matches = mismatches[query_key(row)]
            targets = target_ids(row)
            aligned_support = lexical_support(
                str(row["instruction"]), targets, doc_tokens, index_by_id, bm25.idf
            )
            mismatch_supports = [
                lexical_support(
                    str(match["instruction"]), targets, doc_tokens, index_by_id, bm25.idf
                )
                for match in matches
            ]
            raw.append(
                {
                    "aligned_lexical_support": aligned_support,
                    "matched_donors": matches,
                    "metrics": retrieval_metrics(ranked, targets, top_k),
                    "mismatched_lexical_supports": mismatch_supports,
                    "query_id": query_id,
                    "ranked_ids": ranked,
                    "retriever": "minilm",
                    "source_config": row["source_config"],
                    "target_ids": sorted(targets),
                    "view": view,
                }
            )

    bootstrap_config = config["bootstrap"]
    summary = summarize(
        raw,
        source_configs,
        donor_count,
        int(bootstrap_config["seed"]),
        int(bootstrap_config["replicates"]),
    )
    summary.update(
        {
            "schema_version": 2,
            "phase": args.phase,
            "corpus_rows": len(corpus),
            "query_rows": len(queries),
            "config_sha256": sha256_file(args.config),
            "corpus_sha256": sha256_file(args.corpus),
            "queries_sha256": sha256_file(args.queries),
            "corpus_embeddings_sha256": sha256_file(args.corpus_embeddings),
        }
    )
    write_jsonl(args.raw_output, raw)
    write_json(args.summary_output, summary)
    write_json(
        args.environment_output,
        environment_record(
            str(minilm_config["model"]), str(minilm_config["revision"])
        ),
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    root.add_argument("--config", required=True, type=Path)
    actions = root.add_subparsers(dest="action", required=True)

    acquire_parser = actions.add_parser("acquire")
    acquire_parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    acquire_parser.add_argument("--queries-output", required=True, type=Path)
    acquire_parser.add_argument("--corpus-output", type=Path)
    acquire_parser.add_argument("--manifest-output", required=True, type=Path)

    evaluate_parser = actions.add_parser("evaluate")
    evaluate_parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    evaluate_parser.add_argument("--corpus", required=True, type=Path)
    evaluate_parser.add_argument("--queries", required=True, type=Path)
    evaluate_parser.add_argument("--corpus-embeddings", required=True, type=Path)
    evaluate_parser.add_argument("--raw-output", required=True, type=Path)
    evaluate_parser.add_argument("--summary-output", required=True, type=Path)
    evaluate_parser.add_argument("--environment-output", required=True, type=Path)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.action == "acquire":
        return acquire(args)
    return evaluate(args)


if __name__ == "__main__":
    raise SystemExit(main())
