from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .diagnosis import collect_diagnosis, show_diagnosis
from .recall import rebuild_recall, resume_recall, search_recall
from .recorded import run_recorded
from .reviewer_protocol import create_evaluation, implementation_measurement_history
from .reviewer_runtime import reviewer_canary, run_evaluation
from .tool_forge import create_run_tool
from .workspace import (
    CURRENT_CONTRACT_VERSION,
    RUN_PATTERN,
    ResearchWorkspace,
    _current_version,
    _required_file,
    bind_run,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crl", description="Thin optional capability entry for one bound CRL Run."
    )
    subparsers = parser.add_subparsers(dest="capability", required=True)
    subparsers.add_parser("capabilities")

    recall = subparsers.add_parser("recall")
    _workspace_arguments(recall)
    recall_actions = recall.add_subparsers(dest="action", required=True)
    rebuild = recall_actions.add_parser("rebuild")
    rebuild.add_argument("--semantic", action="store_true")
    search = recall_actions.add_parser("search")
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=12)
    resume = recall_actions.add_parser("resume")
    resume.add_argument("--limit", type=int, default=16)

    diagnose = subparsers.add_parser("diagnose")
    _workspace_arguments(diagnose)
    diagnose_actions = diagnose.add_subparsers(dest="action", required=True)
    collect = diagnose_actions.add_parser("collect")
    collect.add_argument("--diagnosis-id", required=True)
    show = diagnose_actions.add_parser("show")
    show.add_argument("--diagnosis-id", required=True)

    tool = subparsers.add_parser("tool")
    _workspace_arguments(tool)
    tool_actions = tool.add_subparsers(dest="action", required=True)
    create = tool_actions.add_parser("create")
    create.add_argument("--name", required=True)

    recorded = subparsers.add_parser("recorded")
    _workspace_arguments(recorded)
    recorded_actions = recorded.add_subparsers(dest="action", required=True)
    run = recorded_actions.add_parser("run")
    run.add_argument("--record-id", required=True)
    run.add_argument("--cwd")
    run.add_argument("--timeout", type=float)
    run.add_argument("--input", action="append", default=[])
    run.add_argument("--output", action="append", default=[])
    run.add_argument(
        "--allow-sensitive-env", action="append", default=[], metavar="NAME"
    )
    run.add_argument("command", nargs=argparse.REMAINDER)

    review = subparsers.add_parser("review")
    review_actions = review.add_subparsers(dest="action", required=True)
    canary = review_actions.add_parser("canary")
    canary.add_argument("--timeout", type=float, default=900)
    create_review = review_actions.add_parser("create")
    _workspace_arguments(create_review)
    create_review.add_argument("--section", action="append", default=[])
    create_review.add_argument("--final-delivery", action="store_true")
    run_review = review_actions.add_parser("run")
    _workspace_arguments(run_review)
    run_review.add_argument("--evaluation-id", required=True)
    run_review.add_argument("--timeout", type=float, default=1800)
    review_status = review_actions.add_parser("status")
    _workspace_arguments(review_status)
    review_status.add_argument("--implementation-key", required=True)
    decide = review_actions.add_parser("decide")
    _workspace_arguments(decide)
    decide.add_argument("--measurement-key")
    decide.add_argument("--body-file", required=True, type=Path)
    deliver = review_actions.add_parser("deliver")
    _workspace_arguments(deliver)
    deliver.add_argument("--supporting-attempt", action="append", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    arguments = build_parser().parse_args(argv)
    try:
        if arguments.capability == "capabilities":
            payload = {
                "contract_version": CURRENT_CONTRACT_VERSION,
                "required": [],
                "optional": {
                    "recall": ["rebuild", "search", "resume"],
                    "diagnose": ["collect", "show"],
                    "tool": ["create"],
                    "recorded": ["run"],
                    "review": ["canary", "create", "run", "status", "decide", "deliver"],
                },
                "formal_runner": "tools/run_local_experiment.py",
                "workflow_gate": False,
            }
        elif arguments.capability == "review" and arguments.action == "canary":
            result = reviewer_canary(timeout_seconds=arguments.timeout)
            payload = {key: value for key, value in result.items() if not key.endswith("_bytes")}
        else:
            workspace = _workspace_from_arguments(arguments)
            payload = _dispatch(arguments, workspace)
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as error:
        print(f"crl: {error}", file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _dispatch(arguments: argparse.Namespace, workspace: ResearchWorkspace) -> object:
    if arguments.capability == "recall":
        if arguments.action == "rebuild":
            return rebuild_recall(workspace, semantic=arguments.semantic)
        if arguments.action == "search":
            return search_recall(workspace, arguments.query, limit=arguments.limit)
        return resume_recall(workspace, limit=arguments.limit)
    if arguments.capability == "diagnose":
        if arguments.action == "collect":
            return collect_diagnosis(workspace, arguments.diagnosis_id)
        return show_diagnosis(workspace, arguments.diagnosis_id)
    if arguments.capability == "tool":
        return create_run_tool(workspace, arguments.name)
    if arguments.capability == "review":
        if arguments.action == "create":
            return create_evaluation(
                workspace,
                _review_sections(arguments.section),
                final_delivery=arguments.final_delivery,
            )
        if arguments.action == "run":
            return run_evaluation(
                workspace,
                arguments.evaluation_id,
                timeout_seconds=arguments.timeout,
            )
        if arguments.action == "decide":
            body_path = workspace.assert_read_target(arguments.body_file)
            content = _required_file(
                body_path, within=workspace.workspace_path
            ).decode("utf-8")
            decision = workspace.write_review_decision(
                content, measurement_key=arguments.measurement_key
            )
            return {
                "path": decision.path,
                "sha256": decision.sha256,
                "measurement_key": decision.measurement_key,
                "canonical_evaluation_id": decision.canonical_evaluation_id,
            }
        if arguments.action == "deliver":
            terminal = workspace.write_delivery(
                supporting_attempt_ids=arguments.supporting_attempt
            )
            return {
                "path": terminal.path,
                "sha256": terminal.sha256,
                "status": terminal.status,
                "version": terminal.version,
            }
        return implementation_measurement_history(
            workspace, arguments.implementation_key
        )
    command = list(arguments.command)
    if command[:1] == ["--"]:
        command = command[1:]
    return run_recorded(
        workspace,
        arguments.record_id,
        command,
        cwd=arguments.cwd,
        timeout_seconds=arguments.timeout,
        inputs=arguments.input,
        outputs=arguments.output,
        allow_sensitive_environment=arguments.allow_sensitive_env,
    )


def _workspace_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--product-root",
        type=Path,
        help="Product root override; otherwise inferred from the current Run.",
    )
    parser.add_argument(
        "--run-root",
        type=Path,
        help="Run root override; otherwise discovered by walking upward from cwd.",
    )
    parser.add_argument(
        "--version",
        help="Research version override; otherwise read from RUN_STATUS.md.",
    )


def _workspace_from_arguments(arguments: argparse.Namespace) -> ResearchWorkspace:
    cwd = Path.cwd().resolve(strict=True)
    discovered = _discover_run_root(cwd)
    requested = arguments.run_root
    product = arguments.product_root
    if requested is None:
        if discovered is None:
            raise ValueError(
                "cannot discover a CRL Run from cwd; provide --run-root and "
                "optionally --product-root"
            )
        requested = discovered
    if product is None:
        requested_path = Path(requested)
        if requested_path.is_absolute():
            inferred_run = requested_path
        elif discovered is not None and requested_path in {
            Path("."),
            Path(discovered.name),
        }:
            inferred_run = discovered
        else:
            inferred_run = (cwd / requested_path).absolute()
        product = inferred_run.parent
        requested = inferred_run
    bound = bind_run(product, requested)
    version = arguments.version or _current_version(
        bound / "RUN_STATUS.md", within=bound
    )
    return ResearchWorkspace(bound, product_root=product, version=version)


def _discover_run_root(cwd: Path) -> Path | None:
    for candidate in (cwd, *cwd.parents):
        if RUN_PATTERN.fullmatch(candidate.name) is None:
            continue
        if all(
            (candidate / name).is_file()
            for name in ("RUN_CHARTER.md", "RUN_STATUS.md", "RUN_LEDGER.md")
        ):
            return candidate
    return None


def _review_sections(values: Sequence[str]) -> dict[int, list[str]]:
    sections: dict[int, list[str]] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("review section must use NUMBER=RUN_RELATIVE_PATH")
        number_text, path = value.split("=", 1)
        try:
            number = int(number_text)
        except ValueError as error:
            raise ValueError("review section number must be 1-7") from error
        if number not in range(1, 8) or not path:
            raise ValueError("review section must use a number from 1 to 7 and a path")
        sections.setdefault(number, []).append(path)
    return sections


if __name__ == "__main__":
    raise SystemExit(main())
