from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.hypotheses import (
    HYPOTHESIS_STATUSES,
    add_hypothesis,
    create_hypothesis_record,
    decision_warning_codes,
    empty_portfolio,
    hypothesis_record_to_dict,
    render_portfolio_markdown,
    transition_hypothesis,
    update_hypothesis,
)
from crl_v3.knowledge import KnowledgeStore
from crl_v3.workspace import ResearchWorkspace, _required_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage an optional Run-local, non-authoritative hypothesis portfolio."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    init = subparsers.add_parser("init")
    _add_workspace(init)

    add = subparsers.add_parser("add")
    _add_workspace(add)
    add.add_argument("--from-json", required=True, type=Path)

    update = subparsers.add_parser("update")
    _add_workspace(update)
    update.add_argument("hypothesis_id")
    update.add_argument("--patch-json", required=True, type=Path)

    transition = subparsers.add_parser("transition")
    _add_workspace(transition)
    transition.add_argument("hypothesis_id")
    transition.add_argument("--status", required=True, choices=HYPOTHESIS_STATUSES)
    transition.add_argument("--reason", required=True)
    transition.add_argument("--decision-json", type=Path)

    show = subparsers.add_parser("show")
    _add_workspace(show)
    show.add_argument("hypothesis_id")

    listing = subparsers.add_parser("list")
    _add_workspace(listing)

    validate = subparsers.add_parser("validate")
    _add_workspace(validate)

    render = subparsers.add_parser("render")
    _add_workspace(render)
    return parser


def _add_workspace(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", default="v001")


def _read_json(path: Path) -> dict[str, object]:
    data = _required_file(path)
    if not data:
        raise ValueError(f"empty JSON input: {path}")
    try:
        value = json.loads(data)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON input: {path}") from error
    if not isinstance(value, dict):
        raise ValueError("JSON input must be an object")
    return value


def _store(arguments: argparse.Namespace) -> KnowledgeStore | None:
    database = arguments.product_root / "knowledge_base" / "knowledge.sqlite"
    return KnowledgeStore(database, read_only=True) if database.is_file() else None


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    arguments = build_parser().parse_args(argv)
    store: KnowledgeStore | None = None
    try:
        store = _store(arguments)
        workspace = ResearchWorkspace(
            arguments.run_root,
            knowledge_store=store,
            version=arguments.version,
            product_root=arguments.product_root,
        )
        if arguments.action == "init":
            document = workspace.write_hypotheses(
                empty_portfolio(workspace.workspace_path.name, workspace.version),
                expected_sha256=None,
                create_only=True,
            )
            payload: dict[str, object] = _portfolio_facts(document)
            payload["action"] = "init"
        else:
            document = workspace.read_hypotheses(required=True)
            assert document is not None
            portfolio = document.portfolio
            if arguments.action == "add":
                record = create_hypothesis_record(_read_json(arguments.from_json))
                portfolio = add_hypothesis(
                    portfolio, record, knowledge_store=workspace.knowledge_store
                )
                written = workspace.write_hypotheses(
                    portfolio, expected_sha256=document.sha256
                )
                payload = _portfolio_facts(written)
                payload.update({"action": "add", "hypothesis_id": record.hypothesis_id})
            elif arguments.action == "update":
                portfolio = update_hypothesis(
                    portfolio,
                    arguments.hypothesis_id,
                    _read_json(arguments.patch_json),
                    knowledge_store=workspace.knowledge_store,
                )
                written = workspace.write_hypotheses(
                    portfolio, expected_sha256=document.sha256
                )
                payload = _portfolio_facts(written)
                payload.update(
                    {"action": "update", "hypothesis_id": arguments.hypothesis_id}
                )
            elif arguments.action == "transition":
                decision = (
                    _read_json(arguments.decision_json)
                    if arguments.decision_json is not None
                    else None
                )
                portfolio = transition_hypothesis(
                    portfolio,
                    arguments.hypothesis_id,
                    arguments.status,
                    arguments.reason,
                    decision=decision,
                    knowledge_store=workspace.knowledge_store,
                )
                written = workspace.write_hypotheses(
                    portfolio, expected_sha256=document.sha256
                )
                payload = _portfolio_facts(written)
                payload.update(
                    {
                        "action": "transition",
                        "hypothesis_id": arguments.hypothesis_id,
                        "status": arguments.status,
                    }
                )
                transitioned = next(
                    item
                    for item in portfolio.hypotheses
                    if item.hypothesis_id == arguments.hypothesis_id
                )
                payload["decision_warnings"] = (
                    list(decision_warning_codes(transitioned.decision_history[-1]))
                    if transitioned.decision_history
                    else []
                )
            elif arguments.action == "show":
                matches = [
                    item
                    for item in portfolio.hypotheses
                    if item.hypothesis_id == arguments.hypothesis_id
                ]
                if not matches:
                    raise KeyError(f"unknown hypothesis id: {arguments.hypothesis_id}")
                payload = {
                    "action": "show",
                    "hypothesis": hypothesis_record_to_dict(matches[0]),
                }
            elif arguments.action == "list":
                payload = {
                    "action": "list",
                    "run_id": portfolio.run_id,
                    "version": portfolio.version,
                    "portfolio_revision": portfolio.revision,
                    "hypotheses": [
                        {
                            "hypothesis_id": item.hypothesis_id,
                            "title": item.title,
                            "status": item.status,
                            "parent_ids": list(item.parent_ids),
                            "revision": item.revision,
                        }
                        for item in portfolio.hypotheses
                    ],
                }
            elif arguments.action == "validate":
                payload = {
                    "action": "validate",
                    "schema_version": portfolio.schema_version,
                    "run_id": portfolio.run_id,
                    "version": portfolio.version,
                    "portfolio_revision": portfolio.revision,
                    "record_count": len(portfolio.hypotheses),
                }
            else:
                sys.stdout.write(render_portfolio_markdown(portfolio))
                return 0
    except (KeyError, OSError, UnicodeError, ValueError) as error:
        print(f"manage_hypotheses: {error}", file=sys.stderr)
        return 1
    finally:
        if store is not None:
            store.close()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


def _portfolio_facts(document: object) -> dict[str, object]:
    return {
        "path": document.path,
        "sha256": document.sha256,
        "portfolio_revision": document.portfolio.revision,
        "record_count": len(document.portfolio.hypotheses),
    }


if __name__ == "__main__":
    raise SystemExit(main())
