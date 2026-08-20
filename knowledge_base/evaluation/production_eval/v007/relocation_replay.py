from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r"D:\Desktop\crl\crl_agent_v3")

from crl_v3.cards import card_index_status, load_valid_cards, search_cards
from crl_v3.knowledge import KnowledgeStore
from crl_v3.retrieval import hybrid_search
from crl_v3.vector import vector_index_status


FROZEN_HASHES = {
    "manifest": ("knowledge_base/corpus/manifest.json", "801d44135f74a05653c4ee26c2731694460bd75047996dd22557d50ac0dc29bf"),
    "evidence": ("knowledge_base/corpus/evidence.json", "704731a935eafaa921f55d812259d96b44ad38b0de463d0e40b793ee4de60bfd"),
    "knowledge_db": ("knowledge_base/knowledge.sqlite", "dc3136ca20a4dafcb0c29d4d0bc00f8acd64d5d7f022b3bc2c47a3789d2fba90"),
    "vector_index": ("knowledge_base/passages.npz", "0c2554340178942c029464eb92359ab9e7381ba178e7cb8df8b563a13a0f464b"),
    "card_fts_index": ("knowledge_base/cards_fts.sqlite", "174198091e3200eec9d0c89c571325d8b8aa9e05ea784e7f630969546842e8fc"),
    "card_implementation": ("crl_v3/cards.py", "bc4cbe510286f003a27d51196b0e9d922f81dd0a18f0ad431f842d532272b9d6"),
    "retrieval_implementation": ("crl_v3/retrieval.py", "13e73c964984f970458cb09de8754eb6ef9e90df2fa42920fea618eee06308e4"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--split", choices=("calibration", "blind"), required=True)
    parser.add_argument("--queries", required=True)
    parser.add_argument("--queries-sha", required=True)
    parser.add_argument("--judgments", required=True)
    parser.add_argument("--judgments-sha", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    queries_path = (root / args.queries).resolve()
    judgments_path = (root / args.judgments).resolve()
    output_path = (root / args.output).resolve()
    report_path = (root / args.report).resolve() if args.report else None
    for path in (output_path, report_path):
        if path is not None and path.exists():
            raise FileExistsError(f"one-shot output already exists: {path}")

    frozen_inputs: dict[str, dict[str, object]] = {}
    for name, (relative, expected) in FROZEN_HASHES.items():
        path = root / relative
        actual = sha256(path)
        frozen_inputs[name] = {
            "path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "matches": actual == expected,
        }
    for name, path, relative, expected in (
        ("queries", queries_path, args.queries, args.queries_sha),
        ("judgments", judgments_path, args.judgments, args.judgments_sha),
    ):
        actual = sha256(path)
        frozen_inputs[name] = {
            "path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "matches": actual == expected,
        }
    mismatches = [name for name, item in frozen_inputs.items() if not item["matches"]]
    if mismatches:
        raise ValueError(f"frozen input mismatch: {mismatches}")

    queries_doc = json.loads(queries_path.read_text(encoding="utf-8"))
    judgments_doc = json.loads(judgments_path.read_text(encoding="utf-8"))
    queries = queries_doc["queries"]
    judgments = judgments_doc["judgments"]
    if len(queries) != len(judgments):
        raise ValueError("query/judgment counts differ")
    judgment_by_id = {item["query_id"]: item for item in judgments}
    if len(judgment_by_id) != len(judgments):
        raise ValueError("duplicate judgment query_id")
    if [item["query_id"] for item in queries] != [item["query_id"] for item in judgments]:
        raise ValueError("judgment order or identities differ from queries")
    critical_gaps = [
        item["query_id"]
        for item in judgments
        if item["critical"] is True and item["corpus_gap"] is True
    ]
    if critical_gaps:
        raise ValueError(f"critical corpus gaps must stop before retrieval: {critical_gaps}")

    cards_root = root / "knowledge_base/cards"
    card_index = root / "knowledge_base/cards_fts.sqlite"
    knowledge_db = root / "knowledge_base/knowledge.sqlite"
    vector_index = root / "knowledge_base/passages.npz"
    store = KnowledgeStore(knowledge_db)
    try:
        card_status = card_index_status(cards_root, card_index)
        vector_status = vector_index_status(store, vector_index)
        if card_status.get("ready") is not True or vector_status.get("ready") is not True:
            raise ValueError(f"derived indexes not ready: {card_status}; {vector_status}")
        cards = load_valid_cards(
            cards_root,
            store=store,
            project_root=root / "knowledge_base",
        )
        card_by_id = {card.metadata.card_id: card for card in cards}
        with sqlite3.connect(card_index) as connection:
            row = connection.execute(
                "SELECT source_signature FROM card_index_metadata WHERE singleton = 1"
            ).fetchone()
        if row is None:
            raise ValueError("Card source signature missing")
        source_signature = str(row[0])

        per_query = []
        for query_item in queries:
            query_id = query_item["query_id"]
            judgment = judgment_by_id[query_id]
            if query_item["critical"] is not judgment["critical"]:
                raise ValueError(f"critical label mismatch: {query_id}")
            target_kind = query_item["target_kind"]
            card_hits = search_cards(
                cards_root,
                card_index,
                query_item["query"],
                kinds=(target_kind,),
                limit=10,
            )
            passage_result = hybrid_search(
                store,
                vector_index,
                query_item["query"],
                limit=10,
            )
            relevant_cards = set(judgment["relevant_card_ids"])
            relevant_evidence = set(judgment["relevant_evidence_ids"])
            relevant_passages = set(judgment["relevant_passage_ids"])
            top5_relevant = [hit.card_id for hit in card_hits[:5] if hit.card_id in relevant_cards]
            top10_relevant = [hit.card_id for hit in card_hits if hit.card_id in relevant_cards]
            source_chain_cards = []
            for card_id in top5_relevant:
                card = card_by_id.get(card_id)
                if card is None:
                    continue
                shared_evidence = set(card.metadata.evidence_ids) & relevant_evidence
                if any(
                    (evidence := store.get_evidence(evidence_id)) is not None
                    and evidence.passage_id in relevant_passages
                    and evidence.fulltext_is_current
                    and evidence.passage_is_current is True
                    for evidence_id in shared_evidence
                ):
                    source_chain_cards.append(card_id)
            card_top5_pass = bool(top5_relevant)
            source_chain_pass = bool(source_chain_cards)
            critical = bool(query_item["critical"])
            critical_pass = card_top5_pass and source_chain_pass if critical else None
            blocking = critical and critical_pass is not True
            passage_hits = [
                hit.passage_id for hit in passage_result.hits if hit.passage_id in relevant_passages
            ]
            per_query.append(
                {
                    "query_id": query_id,
                    "query": query_item["query"],
                    "target_kind": target_kind,
                    "judgment": {
                        "critical": critical,
                        "corpus_gap": bool(judgment["corpus_gap"]),
                        "relevant_card_ids": judgment["relevant_card_ids"],
                        "relevant_evidence_ids": judgment["relevant_evidence_ids"],
                        "relevant_passage_ids": judgment["relevant_passage_ids"],
                        "rationale": judgment["rationale"],
                    },
                    "card_fts": {
                        "target_kind": target_kind,
                        "limit": 10,
                        "critical_top_k": 5,
                        "hits": [dict(asdict(hit), position=position) for position, hit in enumerate(card_hits, start=1)],
                        "relevant_card_ids_in_top5": top5_relevant,
                        "relevant_card_ids_in_top10": top10_relevant,
                        "card_top5_hit": card_top5_pass,
                    },
                    "source_chain": {
                        "cards_in_top5": source_chain_cards,
                        "pass": source_chain_pass,
                    },
                    "passage_hybrid": {
                        "diagnostic_only": True,
                        "limit": 10,
                        "degraded": passage_result.degraded,
                        "degradation_reason": passage_result.degradation_reason,
                        "hits": [asdict(hit) for hit in passage_result.hits],
                        "relevant_passage_ids": passage_hits,
                        "diagnostic_hit": bool(passage_hits),
                    },
                    "decision": {
                        "critical": critical,
                        "critical_pass": critical_pass,
                        "blocking": blocking,
                    },
                }
            )
    finally:
        store.close()

    critical_items = [item for item in per_query if item["decision"]["critical"]]
    ordinary_items = [item for item in per_query if not item["decision"]["critical"]]
    blocking_ids = [item["query_id"] for item in critical_items if item["decision"]["blocking"]]
    ordinary_misses = [item["query_id"] for item in ordinary_items if not item["card_fts"]["card_top5_hit"]]
    passage_hits = sum(item["passage_hybrid"]["diagnostic_hit"] for item in per_query)
    degraded_ids = [item["query_id"] for item in per_query if item["passage_hybrid"]["degraded"]]
    verdict = "PASS" if not blocking_ids and not degraded_ids else "FAIL"
    result = {
        "schema_version": 1,
        "evaluation_id": f"CRL_PRODUCT_RELOCATION_v007_{args.split}_retrieval",
        "created_at": datetime.now().astimezone().isoformat(),
        "protocol": {
            "card_search": "target_kind FTS, unchanged query, limit 10, top-5 critical Gate",
            "source_chain": "relevant Card in top-5 must share pre-frozen Evidence whose exact current Passage is pre-frozen relevant",
            "passage_search": "current FTS plus vector hybrid, limit 10, diagnostic only",
            "no_tuning": True,
        },
        "frozen_inputs": frozen_inputs,
        "card_source_signature": source_signature,
        "index_status": {"card_fts": card_status, "vector": vector_status},
        "per_query": per_query,
        "summary": {
            "total_queries": len(per_query),
            "critical_queries": len(critical_items),
            "critical_pass": len(critical_items) - len(blocking_ids),
            "critical_fail": len(blocking_ids),
            "blocking_query_ids": blocking_ids,
            "ordinary_queries": len(ordinary_items),
            "ordinary_card_top5_miss_count": len(ordinary_misses),
            "ordinary_card_top5_miss_query_ids": ordinary_misses,
            "passage_hybrid_top10_diagnostic_hits": passage_hits,
            "passage_hybrid_degraded_query_ids": degraded_ids,
            "verdict": verdict,
        },
        "integrity_concerns": [],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if report_path is not None:
        report = (
            f"# Production retrieval v007 relocation {args.split} report\n\n"
            f"- Verdict: `{verdict}`\n"
            f"- Total / critical: {len(per_query)} / {len(critical_items)}\n"
            f"- Critical pass / fail: {len(critical_items) - len(blocking_ids)} / {len(blocking_ids)}\n"
            f"- Blocking query IDs: {blocking_ids}\n"
            f"- Ordinary Card top-5 misses: {len(ordinary_misses)}\n"
            f"- Passage hybrid top-10 diagnostic hits: {passage_hits}\n"
            f"- Degraded Passage queries: {degraded_ids}\n\n"
            "Card top-k tests knowledge discovery; Card to Evidence to Passage validates factual support. "
            "Raw Passage hybrid top-k is diagnostic and is not the sole blocking condition.\n"
        )
        report_path.write_text(report, encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
