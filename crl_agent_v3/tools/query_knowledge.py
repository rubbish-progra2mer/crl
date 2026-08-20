from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.cards import CardSearchHit, parse_card, search_cards
from crl_v3.knowledge import KnowledgeStore, normalize_fts_query, paper_payload
from crl_v3.retrieval import hybrid_search


CARD_KINDS = ("failure", "operator", "paper")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only access to the external CRL paper knowledge base."
    )
    parser.add_argument(
        "--knowledge-root",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "knowledge_base",
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    cards = subparsers.add_parser("cards", help="search Card full-text index")
    cards.add_argument("--query", required=True)
    cards.add_argument("--kind", action="append", choices=CARD_KINDS)
    cards.add_argument("--limit", type=int, default=20)

    passages = subparsers.add_parser("passages", help="search authoritative passages")
    passages.add_argument("--query", required=True)
    passages.add_argument("--limit", type=int, default=20)

    hybrid = subparsers.add_parser("hybrid", help="combine passage FTS and vector recall")
    hybrid.add_argument("--query", required=True)
    hybrid.add_argument("--limit", type=int, default=10)

    evidence = subparsers.add_parser("evidence", help="list Evidence for one paper")
    evidence.add_argument("--paper-id", required=True)

    paper = subparsers.add_parser("paper", help="read one paper identity")
    paper.add_argument("--paper-id", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    arguments = build_parser().parse_args(argv)
    root = arguments.knowledge_root.resolve()
    database = root / "knowledge.sqlite"
    payload: dict[str, object] = {
        "action": arguments.action,
        "knowledge_root": str(root),
        "database_path": str(database),
    }
    store: KnowledgeStore | None = None
    try:
        store = KnowledgeStore(database, read_only=True)
        if arguments.action in {"cards", "passages", "hybrid"}:
            normalized = normalize_fts_query(arguments.query)
            payload.update(asdict(normalized))
        if arguments.action == "cards":
            kinds = tuple(arguments.kind or CARD_KINDS)
            hits = search_cards(
                root / "cards",
                root / "cards_fts.sqlite",
                arguments.query,
                kinds=kinds,
                limit=arguments.limit,
            )
            payload.update(
                {
                    "source_path": str(root / "cards_fts.sqlite"),
                    "kinds": list(kinds),
                    "hits": [
                        _card_hit_payload(root, hit, store) for hit in hits
                    ],
                }
            )
        elif arguments.action == "passages":
            hits = store.search(arguments.query, limit=arguments.limit)
            payload.update(
                {
                    "source_path": str(database),
                    "hits": [asdict(hit) for hit in hits],
                }
            )
        elif arguments.action == "hybrid":
            result = hybrid_search(
                store,
                root / "passages.npz",
                arguments.query,
                limit=arguments.limit,
            )
            payload.update(
                {
                    "source_path": str(root / "passages.npz"),
                    "degraded": result.degraded,
                    "degradation_reason": result.degradation_reason,
                    "hits": [asdict(hit) for hit in result.hits],
                }
            )
        elif arguments.action == "evidence":
            paper = store.get_paper(arguments.paper_id)
            if paper is None:
                raise ValueError(f"unknown paper id: {arguments.paper_id}")
            payload.update(
                {
                    "paper_id": arguments.paper_id,
                    "source_path": str(database),
                    "evidence": [
                        asdict(item) for item in store.list_evidence(arguments.paper_id)
                    ],
                }
            )
        else:
            paper = store.get_paper(arguments.paper_id)
            if paper is None:
                raise ValueError(f"unknown paper id: {arguments.paper_id}")
            payload.update(
                {
                    "paper_id": arguments.paper_id,
                    "source_path": str(database),
                    "paper": paper_payload(root, paper),
                }
            )
    except (ImportError, OSError, RuntimeError, sqlite3.Error, ValueError) as error:
        print(f"query_knowledge: {error}", file=sys.stderr)
        return 2
    finally:
        if store is not None:
            store.close()
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _card_hit_payload(
    knowledge_root: Path,
    hit: CardSearchHit,
    store: KnowledgeStore,
) -> dict[str, object]:
    payload = asdict(hit)
    card = parse_card(knowledge_root / "cards" / hit.relative_path)
    payload["paper_id"] = card.metadata.paper_id
    evidence_locations = []
    for evidence_id in card.metadata.evidence_ids:
        evidence = store.get_evidence(evidence_id)
        if evidence is None:
            raise ValueError(f"Card refers to unknown Evidence: {evidence_id}")
        evidence_locations.append(
            {
                "evidence_id": evidence.evidence_id,
                "paper_id": evidence.paper_id,
                "locator": evidence.locator,
                "page_start": evidence.page_start,
                "page_end": evidence.page_end,
                "fulltext_is_current": evidence.fulltext_is_current,
                "passage_is_current": evidence.passage_is_current,
            }
        )
    payload["evidence_locations"] = evidence_locations
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
