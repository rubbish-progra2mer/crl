from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.knowledge import KnowledgeStore
from crl_v3.research_retrieval import (
    bind_research_knowledge_root,
    build_research_bundle,
    hypothesis_queries,
    materialized_result,
    parse_explicit_queries,
    publish_search_snapshot,
    verify_existing_search,
)
from crl_v3.workspace import ResearchWorkspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a Run-local, non-authoritative research retrieval view from the "
            "fixed product knowledge base."
        )
    )
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", default="v001")
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--hypothesis-id")
    inputs.add_argument(
        "--query",
        action="append",
        metavar="PURPOSE=TEXT",
        help="repeat for problem, failure, operator, prior, or measurement",
    )
    parser.add_argument("--card-limit", type=int, default=10)
    parser.add_argument("--passage-limit", type=int, default=10)
    parser.add_argument("--save-search", metavar="SEARCH_ID")
    parser.add_argument(
        "--full-json",
        action="store_true",
        help="print the complete legacy retrieval payload, including route hits",
    )
    return parser


def _compact_stdout_payload(
    materialized: dict[str, object],
) -> dict[str, object]:
    request = materialized["request"]
    result = materialized["result"]
    assert isinstance(request, dict) and isinstance(result, dict)
    compact_map = result["compact_research_map"]
    diagnostics = result["diagnostics"]
    queries = result["queries"]
    assert isinstance(compact_map, dict)
    assert isinstance(diagnostics, dict)
    assert isinstance(queries, list)

    route_coverage = []
    for query in queries:
        assert isinstance(query, dict)
        route_coverage.append(
            {
                "query_id": query["query_id"],
                "purpose": query["purpose"],
                "routes": [
                    {
                        "route": route["route"],
                        "hit_count": len(route["hits"]),
                        "degraded": route["degraded"],
                        "degradation_reason": route["degradation_reason"],
                    }
                    for route in query["routes"]
                ],
            }
        )

    snapshot = materialized.get("snapshot")
    artifact_paths: dict[str, str] = {}
    if isinstance(snapshot, dict):
        snapshot_path = Path(str(snapshot["path"]))
        artifact_paths = {
            name: str(snapshot_path / name)
            for name in ("request.json", "result.json", "report.md")
        }
    return {
        "schema_version": 1,
        "stdout_format": "compact-v1",
        "created_at_utc": result["created_at_utc"],
        "query": {
            "input_mode": request["input_mode"],
            "input_identity": request["input_identity"],
            "queries": request["queries"],
            "limits": request["limits"],
        },
        "representative_compact_map": {
            "label": compact_map["label"],
            "deduplication_key": compact_map["deduplication_key"],
            "ranking_kind": compact_map["ranking_kind"],
            "entry_count": compact_map["entry_count"],
            "representative_selection": compact_map["representative_selection"],
            "representative_entry_count": compact_map[
                "representative_entry_count"
            ],
            "representative_entries": compact_map["representative_entries"],
        },
        "route_coverage": route_coverage,
        "coverage": {
            "unique_card_count": len(diagnostics["unique_card_ids"]),
            "unique_evidence_count": len(diagnostics["unique_evidence_ids"]),
            "unique_passage_count": len(diagnostics["unique_passage_ids"]),
            "paper_count": len(diagnostics["paper_route_hits"]),
            "observation_count": diagnostics["observation_count"],
            "noisy_observation_count": diagnostics["noisy_observation_count"],
        },
        "persistence": {
            "full_result_persisted": snapshot is not None,
            "status": "saved_snapshot" if snapshot is not None else "not_saved",
            "message": (
                "完整结果已持久化到 snapshot artifacts。"
                if snapshot is not None
                else "完整结果未持久化；如需保留，请使用 --save-search。"
            ),
            "snapshot": snapshot,
            "artifact_paths": artifact_paths,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    arguments = build_parser().parse_args(argv)
    store: KnowledgeStore | None = None
    try:
        lexical_product_root = arguments.product_root.absolute()
        product_root, knowledge_root = bind_research_knowledge_root(
            lexical_product_root, lexical_product_root / "knowledge_base"
        )
        store = KnowledgeStore(knowledge_root / "knowledge.sqlite", read_only=True)
        workspace = ResearchWorkspace(
            arguments.run_root,
            knowledge_store=store,
            version=arguments.version,
            product_root=product_root,
        )

        if arguments.save_search:
            verify_existing_search(workspace, arguments.save_search)

        if arguments.hypothesis_id:
            document = workspace.read_hypotheses(required=True)
            assert document is not None
            matches = [
                record
                for record in document.portfolio.hypotheses
                if record.hypothesis_id == arguments.hypothesis_id
            ]
            if not matches:
                raise KeyError(f"unknown hypothesis id: {arguments.hypothesis_id}")
            record = matches[0]
            queries = hypothesis_queries(record)
            input_mode = "hypothesis"
            input_identity: dict[str, object] = {
                "run_id": workspace.workspace_path.name,
                "version": workspace.version,
                "hypothesis_id": record.hypothesis_id,
                "hypothesis_revision": record.revision,
                "portfolio_path": Path(document.path)
                .relative_to(workspace.workspace_path)
                .as_posix(),
                "portfolio_sha256": document.sha256,
            }
        else:
            queries = parse_explicit_queries(arguments.query or ())
            input_mode = "explicit"
            input_identity = {
                "run_id": workspace.workspace_path.name,
                "version": workspace.version,
                "query_count": len(queries),
            }

        bundle = build_research_bundle(
            product_root,
            knowledge_root,
            store,
            queries,
            input_mode=input_mode,
            input_identity=input_identity,
            card_limit=arguments.card_limit,
            passage_limit=arguments.passage_limit,
            additional_code_paths=(Path(__file__),),
        )
        if arguments.save_search:
            publication = publish_search_snapshot(
                workspace, arguments.save_search, bundle
            )
            payload = materialized_result(
                bundle, created_at_utc=publication.created_at_utc
            )
            payload["snapshot"] = asdict(publication)
        else:
            payload = materialized_result(bundle)
        if not arguments.full_json:
            payload = _compact_stdout_payload(payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (
        FileExistsError,
        FileNotFoundError,
        ImportError,
        KeyError,
        OSError,
        RuntimeError,
        sqlite3.Error,
        UnicodeError,
        ValueError,
    ) as error:
        print(f"query_research: {error}", file=sys.stderr)
        return 2
    finally:
        if store is not None:
            store.close()


if __name__ == "__main__":
    raise SystemExit(main())
