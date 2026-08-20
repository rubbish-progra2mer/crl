from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.cards import load_valid_cards, rebuild_card_index, search_cards
from crl_v3.knowledge import KnowledgeStore, normalize_fts_query


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mechanical CRL Card utilities")
    subparsers = parser.add_subparsers(dest="action", required=True)

    validate = subparsers.add_parser("validate", help="validate Markdown Cards")
    validate.add_argument("--cards-root", required=True)
    validate.add_argument("--knowledge-db", required=True)
    validate.add_argument("--project-root", required=True)

    rebuild = subparsers.add_parser(
        "rebuild-index", help="rebuild the derived Card FTS index"
    )
    rebuild.add_argument("--cards-root", required=True)
    rebuild.add_argument("--knowledge-db", required=True)
    rebuild.add_argument("--project-root", required=True)
    rebuild.add_argument("--index", required=True)

    search = subparsers.add_parser("search", help="search one or more Card kinds")
    search.add_argument("--cards-root", required=True)
    search.add_argument("--index", required=True)
    search.add_argument("--query", required=True)
    search.add_argument(
        "--kind",
        action="append",
        choices=("failure", "operator", "paper"),
        required=True,
    )
    search.add_argument("--limit", type=int, default=20)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.action in {"validate", "rebuild-index"}:
            knowledge_db = Path(args.knowledge_db)
            if not knowledge_db.is_file():
                raise FileNotFoundError(
                    f"knowledge database is not a file: {knowledge_db}"
                )
            store = KnowledgeStore(
                knowledge_db,
                read_only=True,
            )
            try:
                if args.action == "validate":
                    cards = load_valid_cards(
                        args.cards_root,
                        store=store,
                        project_root=args.project_root,
                    )
                    kind_counts = {
                        kind: sum(card.metadata.card_kind == kind for card in cards)
                        for kind in ("failure", "operator", "paper")
                    }
                    payload = {
                        "action": "validate",
                        "card_count": len(cards),
                        "kind_counts": kind_counts,
                    }
                else:
                    result = rebuild_card_index(
                        args.cards_root,
                        args.index,
                        store=store,
                        project_root=args.project_root,
                    )
                    payload = {
                        "action": "rebuild-index",
                        "index_path": str(result.index_path),
                        "card_count": result.card_count,
                        "source_signature": result.source_signature,
                    }
            finally:
                store.close()
        else:
            normalized = normalize_fts_query(args.query)
            hits = search_cards(
                args.cards_root,
                args.index,
                args.query,
                kinds=tuple(args.kind),
                limit=args.limit,
            )
            payload = {
                "action": "search",
                "original_query": normalized.original_query,
                "normalized_query": normalized.normalized_query,
                "english_keyword_hint": normalized.english_keyword_hint,
                "kinds": sorted(set(args.kind)),
                "hits": [asdict(hit) for hit in hits],
            }
    except (OSError, sqlite3.Error, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
