from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")
VIEWS = {
    "query_only",
    "aligned_full",
    "mismatched_full_1",
    "mismatched_full_2",
    "mismatched_full_3",
    "generic_full",
}


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"Expected JSON object row: {path}")
            rows.append(value)
    return rows


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def target_ids(row: dict[str, object]) -> set[str]:
    labels = json.loads(str(row["labels"]))
    return {
        str(item["id"])
        for item in labels
        if isinstance(item, dict) and "id" in item
    }


def retrieval_metrics(
    ranked_ids: list[str], targets: set[str]
) -> dict[str, float]:
    gains = [1.0 if item in targets else 0.0 for item in ranked_ids[:10]]
    dcg = sum(
        gain / math.log2(rank + 2.0) for rank, gain in enumerate(gains)
    )
    ideal = sum(
        1.0 / math.log2(rank + 2.0)
        for rank in range(min(10, len(targets)))
    )
    hits = sum(gains)
    return {
        "ndcg_at_10": dcg / ideal if ideal else 0.0,
        "recall_at_10": hits / len(targets),
        "completeness_at_10": 1.0 if hits == len(targets) else 0.0,
    }


def expected_donors(
    queries: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    metadata = [
        (
            row,
            target_ids(row),
            len(tokenize(str(row["instruction"]))),
        )
        for row in queries
    ]
    assignments: dict[str, list[dict[str, object]]] = {}
    for row, labels, length in metadata:
        candidates = []
        for other, other_labels, other_length in metadata:
            if row["id"] == other["id"] or labels.intersection(other_labels):
                continue
            tie = hashlib.sha256(
                f"{row['id']}\0{other['id']}".encode("utf-8")
            ).hexdigest()
            candidates.append(
                (
                    abs(length - other_length),
                    tie,
                    other,
                    other_labels,
                    other_length,
                )
            )
        ordered = sorted(candidates, key=lambda item: (item[0], item[1]))
        if len(ordered) < 3:
            raise AssertionError(f"Insufficient donors: {row['id']}")
        assignments[str(row["id"])] = [
            {
                "instruction": str(donor["instruction"]),
                "donor_query_id": str(donor["id"]),
                "donor_source_config": "confirmation",
                "donor_target_ids": sorted(donor_labels),
                "donor_token_length": donor_length,
                "recipient_token_length": length,
                "token_length_difference": difference,
                "target_overlap_count": len(labels.intersection(donor_labels)),
            }
            for difference, _, donor, donor_labels, donor_length in ordered[:3]
        ]
    return assignments


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", required=True, type=Path)
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()

    queries = read_jsonl(args.queries)
    corpus = read_jsonl(args.corpus)
    raw = read_jsonl(args.raw)
    summary = read_json(args.summary)

    query_by_id = {str(row["id"]): row for row in queries}
    corpus_ids = [str(row["id"]) for row in corpus]
    corpus_id_set = set(corpus_ids)
    assert len(queries) == 1000
    assert len(query_by_id) == 1000
    assert len(corpus_ids) == len(corpus_id_set) == 9309
    assert len(raw) == 12000

    expected_keys = {
        (retriever, str(query["source_config"]), str(query["id"]), view)
        for retriever in ("bm25", "minilm")
        for query in queries
        for view in VIEWS
    }
    observed_keys = {
        (
            str(row["retriever"]),
            str(row["source_config"]),
            str(row["query_id"]),
            str(row["view"]),
        )
        for row in raw
    }
    assert len(observed_keys) == len(raw)
    assert observed_keys == expected_keys

    donors = expected_donors(queries)
    doc_token_sets = [
        set(tokenize(str(row["documentation"]))) for row in corpus
    ]
    document_frequency: Counter[str] = Counter()
    for terms in doc_token_sets:
        document_frequency.update(terms)
    document_count = len(corpus)
    idf = {
        term: math.log(
            1.0
            + (document_count - frequency + 0.5) / (frequency + 0.5)
        )
        for term, frequency in document_frequency.items()
    }
    corpus_index = {
        document_id: index for index, document_id in enumerate(corpus_ids)
    }

    supports: dict[str, tuple[float, list[float]]] = {}
    for query_id, query in query_by_id.items():
        targets = target_ids(query)
        target_terms: set[str] = set()
        for target in targets:
            assert target in corpus_index
            target_terms.update(doc_token_sets[corpus_index[target]])

        def support(instruction: str) -> float:
            terms = set(tokenize(instruction))
            denominator = sum(idf.get(term, 0.0) for term in terms)
            numerator = sum(
                idf.get(term, 0.0)
                for term in terms.intersection(target_terms)
            )
            return numerator / denominator if denominator else 0.0

        supports[query_id] = (
            support(str(query["instruction"])),
            [support(str(item["instruction"])) for item in donors[query_id]],
        )

    metric_max_abs_error = 0.0
    lexical_support_max_abs_error = 0.0
    for row in raw:
        query_id = str(row["query_id"])
        query = query_by_id[query_id]
        targets = target_ids(query)
        assert str(row["source_config"]) == str(query["source_config"])
        assert set(row["target_ids"]) == targets
        assert row["matched_donors"] == donors[query_id]
        ranked = [str(value) for value in row["ranked_ids"]]
        assert len(ranked) == 10
        assert len(set(ranked)) == 10
        assert set(ranked) <= corpus_id_set
        recomputed = retrieval_metrics(ranked, targets)
        for name, value in recomputed.items():
            metric_max_abs_error = max(
                metric_max_abs_error,
                abs(value - float(row["metrics"][name])),
            )
        aligned_support, mismatch_supports = supports[query_id]
        lexical_support_max_abs_error = max(
            lexical_support_max_abs_error,
            abs(aligned_support - float(row["aligned_lexical_support"])),
            *[
                abs(expected - float(observed))
                for expected, observed in zip(
                    mismatch_supports,
                    row["mismatched_lexical_supports"],
                    strict=True,
                )
            ],
        )

    assert metric_max_abs_error == 0.0
    assert lexical_support_max_abs_error <= 1e-15

    raw_by_key = {
        (
            str(row["retriever"]),
            str(row["source_config"]),
            str(row["query_id"]),
            str(row["view"]),
        ): row
        for row in raw
    }
    sources = [f"confirmation-block-{index:02d}" for index in range(10)]
    rng = np.random.default_rng(20260722)
    recomputed_retrievers: dict[str, dict[str, object]] = {}
    summary_max_abs_error = 0.0
    for retriever in ("bm25", "minilm"):
        source_effects: dict[str, float] = {}
        for source in sources:
            query_ids = [
                str(query["id"])
                for query in queries
                if query["source_config"] == source
            ]
            assert len(query_ids) == 100
            deltas = []
            control_stdevs = []
            for query_id in query_ids:
                aligned = float(
                    raw_by_key[
                        (retriever, source, query_id, "aligned_full")
                    ]["metrics"]["ndcg_at_10"]
                )
                controls = [
                    float(
                        raw_by_key[
                            (
                                retriever,
                                source,
                                query_id,
                                f"mismatched_full_{index}",
                            )
                        ]["metrics"]["ndcg_at_10"]
                    )
                    for index in range(1, 4)
                ]
                deltas.append(aligned - float(np.mean(controls)))
                control_stdevs.append(float(np.std(controls)))
            effect = float(np.mean(deltas))
            source_effects[source] = effect
            recorded_source = summary["retrievers"][retriever][
                "source_effects"
            ][source]
            summary_max_abs_error = max(
                summary_max_abs_error,
                abs(
                    effect
                    - float(
                        recorded_source[
                            "aligned_minus_mean_mismatched_ndcg_at_10"
                        ]
                    )
                ),
                abs(
                    float(np.mean(control_stdevs))
                    - float(
                        recorded_source[
                            "mean_control_ndcg_standard_deviation"
                        ]
                    )
                ),
            )
        effects = np.asarray(list(source_effects.values()), dtype=np.float64)
        bootstrap = np.empty(20000, dtype=np.float64)
        for index in range(20000):
            bootstrap[index] = float(
                rng.choice(effects, size=len(effects), replace=True).mean()
            )
        mechanism = float(
            np.mean(
                [
                    aligned - float(np.mean(mismatches))
                    for aligned, mismatches in supports.values()
                ]
            )
        )
        recomputed = {
            "equal_block_mean": float(effects.mean()),
            "block_median": float(np.median(effects)),
            "bootstrap_95": [
                float(np.quantile(bootstrap, 0.025)),
                float(np.quantile(bootstrap, 0.975)),
            ],
            "positive_blocks": int(np.sum(effects > 0.0)),
            "mechanism_mean": mechanism,
            "source_effects": source_effects,
        }
        recorded = summary["retrievers"][retriever]
        comparisons = [
            (
                recomputed["equal_block_mean"],
                recorded[
                    "equal_source_mean_aligned_minus_mean_mismatched_ndcg_at_10"
                ],
            ),
            (recomputed["block_median"], recorded["median_source_effect"]),
            (recomputed["bootstrap_95"][0], recorded["cluster_bootstrap_95_percent"][0]),
            (recomputed["bootstrap_95"][1], recorded["cluster_bootstrap_95_percent"][1]),
            (
                recomputed["mechanism_mean"],
                recorded["mean_aligned_minus_mean_mismatched_lexical_support"],
            ),
        ]
        for expected, observed in comparisons:
            summary_max_abs_error = max(
                summary_max_abs_error, abs(float(expected) - float(observed))
            )
        assert recomputed["equal_block_mean"] > 0.0
        assert recomputed["block_median"] > 0.0
        assert recomputed["bootstrap_95"][0] > 0.0
        assert recomputed["positive_blocks"] == 10
        assert recomputed["mechanism_mean"] > 0.0
        recomputed_retrievers[retriever] = recomputed

    assert summary_max_abs_error <= 1e-15
    assert summary["matching"]["donor_pairs"] == 3000
    assert summary["matching"]["target_overlap_pairs"] == 0

    report = {
        "schema_version": 1,
        "audit": "main_codex_independent_confirmation_audit",
        "query_rows": len(queries),
        "corpus_rows": len(corpus),
        "raw_cells": len(raw),
        "unique_cell_keys": len(observed_keys),
        "complete_unique_top10_rows": len(raw),
        "deterministic_donor_pairs_verified": 3000,
        "target_overlap_pairs": 0,
        "metric_max_abs_error": metric_max_abs_error,
        "lexical_support_max_abs_error": lexical_support_max_abs_error,
        "summary_max_abs_error": summary_max_abs_error,
        "retrievers": recomputed_retrievers,
        "all_preregistered_confirmation_gates_pass": True,
    }
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
