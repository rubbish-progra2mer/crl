from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.falsification import (
    add_claim,
    create_experiment_spec,
    experiment_spec_warning_codes,
    create_plan,
    list_experiment_specs,
    read_plan,
    render_plan_markdown,
    update_claim,
    validate_repository,
)
from crl_v3.knowledge import KnowledgeStore
from crl_v3.workspace import ResearchWorkspace, _required_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Manage explicit Run-local Claim—Falsifier—Experiment records without "
            "making scientific judgments."
        )
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    create_plan_parser = subparsers.add_parser("create-plan")
    _add_workspace(create_plan_parser)
    create_plan_parser.add_argument("--from-json", required=True, type=Path)

    add_claim_parser = subparsers.add_parser("add-claim")
    _add_workspace(add_claim_parser)
    add_claim_parser.add_argument("plan_id")
    add_claim_parser.add_argument("--from-json", required=True, type=Path)

    update_claim_parser = subparsers.add_parser("update-claim")
    _add_workspace(update_claim_parser)
    update_claim_parser.add_argument("plan_id")
    update_claim_parser.add_argument("claim_id")
    update_claim_parser.add_argument("--patch-json", required=True, type=Path)

    create_spec_parser = subparsers.add_parser("create-experiment-spec")
    _add_workspace(create_spec_parser)
    create_spec_parser.add_argument("--from-json", required=True, type=Path)

    validate_parser = subparsers.add_parser("validate")
    _add_workspace(validate_parser)

    render_parser = subparsers.add_parser("render")
    _add_workspace(render_parser)
    render_parser.add_argument("plan_id")
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
        if arguments.action == "create-plan":
            document = create_plan(workspace, _read_json(arguments.from_json))
            payload: dict[str, object] = {
                "action": "create-plan",
                "path": document.path,
                "sha256": document.sha256,
                "plan_id": document.plan.plan_id,
                "claim_count": len(document.plan.claims),
            }
        elif arguments.action == "add-claim":
            document = add_claim(
                workspace,
                arguments.plan_id,
                _read_json(arguments.from_json),
            )
            payload = {
                "action": "add-claim",
                "path": document.path,
                "sha256": document.sha256,
                "plan_id": document.plan.plan_id,
                "claim_count": len(document.plan.claims),
            }
        elif arguments.action == "update-claim":
            document = update_claim(
                workspace,
                arguments.plan_id,
                arguments.claim_id,
                _read_json(arguments.patch_json),
            )
            claim = next(
                item
                for item in document.plan.claims
                if item.claim_id == arguments.claim_id
            )
            payload = {
                "action": "update-claim",
                "path": document.path,
                "sha256": document.sha256,
                "plan_id": document.plan.plan_id,
                "claim_id": claim.claim_id,
                "status": claim.status,
            }
        elif arguments.action == "create-experiment-spec":
            document = create_experiment_spec(
                workspace, _read_json(arguments.from_json)
            )
            payload = {
                "action": "create-experiment-spec",
                "path": document.path,
                "sha256": document.sha256,
                "experiment_id": document.spec.experiment_id,
                "purpose": document.spec.purpose,
                "warnings": list(experiment_spec_warning_codes(document.spec)),
            }
        elif arguments.action == "validate":
            payload = {"action": "validate", **validate_repository(workspace)}
        else:
            document = read_plan(workspace, arguments.plan_id)
            specs = tuple(
                item.spec
                for item in list_experiment_specs(workspace)
                if item.spec.hypothesis_id == document.plan.hypothesis_id
            )
            portfolio = workspace.read_hypotheses(required=True)
            assert portfolio is not None
            hypothesis = next(
                item
                for item in portfolio.portfolio.hypotheses
                if item.hypothesis_id == document.plan.hypothesis_id
            )
            sys.stdout.write(
                render_plan_markdown(
                    document.plan, hypothesis=hypothesis, specs=specs
                )
            )
            return 0
    except (KeyError, OSError, StopIteration, UnicodeError, ValueError) as error:
        print(f"manage_falsification: {error}", file=sys.stderr)
        return 1
    finally:
        if store is not None:
            store.close()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
