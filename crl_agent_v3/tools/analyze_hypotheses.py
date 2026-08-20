from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.portfolio_analysis import (
    DEFAULT_NEAR_DUPLICATE_THRESHOLD,
    DEFAULT_STALE_DAYS,
    DESCRIPTOR_FIELDS,
    analysis_json_bytes,
    analyze_portfolio,
    render_analysis_markdown,
    save_analysis,
)
from crl_v3.workspace import ResearchWorkspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze one fixed Run-local hypothesis portfolio without scoring, "
            "ranking, selection, status changes, or novelty claims."
        )
    )
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", default="v001")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--status", action="append", default=[])
    parser.add_argument(
        "--descriptor",
        action="append",
        default=[],
        metavar="FIELD=VALUE",
        help="repeatable exact descriptor filter",
    )
    parser.add_argument(
        "--lineage",
        action="append",
        default=[],
        metavar="HYPOTHESIS_ID",
        help="include each named hypothesis and its descendants",
    )
    parser.add_argument(
        "--near-duplicate-threshold",
        type=float,
        default=DEFAULT_NEAR_DUPLICATE_THRESHOLD,
    )
    parser.add_argument("--stale-days", type=int, default=DEFAULT_STALE_DAYS)
    parser.add_argument(
        "--as-of",
        help="UTC timestamp; defaults to the portfolio updated_at_utc for determinism",
    )
    parser.add_argument("--save", metavar="ANALYSIS_ID")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    arguments = build_parser().parse_args(argv)
    try:
        workspace = ResearchWorkspace(
            arguments.run_root,
            version=arguments.version,
            product_root=arguments.product_root,
        )
        document = workspace.read_hypotheses(required=False)
        report = analyze_portfolio(
            document.portfolio if document is not None else None,
            statuses=arguments.status,
            descriptor_filters=_parse_descriptor_filters(arguments.descriptor),
            lineage_roots=arguments.lineage,
            near_duplicate_threshold=arguments.near_duplicate_threshold,
            stale_days=arguments.stale_days,
            as_of=arguments.as_of,
            source_path=(
                Path(document.path).relative_to(workspace.workspace_path).as_posix()
                if document is not None
                else workspace.hypotheses_path.relative_to(
                    workspace.workspace_path
                ).as_posix()
            ),
            source_sha256=document.sha256 if document is not None else None,
            run_id=workspace.workspace_path.name,
            version=workspace.version,
        )
        if arguments.save:
            report["saved_path"] = (
                workspace.hypotheses_path.parent
                / "analysis"
                / arguments.save
            ).relative_to(workspace.workspace_path).as_posix()
            save_analysis(workspace, arguments.save, report)
        if arguments.format == "markdown":
            sys.stdout.write(render_analysis_markdown(report))
        else:
            sys.stdout.write(analysis_json_bytes(report).decode("utf-8"))
        return 0
    except (
        FileExistsError,
        FileNotFoundError,
        KeyError,
        OSError,
        UnicodeError,
        ValueError,
    ) as error:
        print(f"analyze_hypotheses: {error}", file=sys.stderr)
        return 1


def _parse_descriptor_filters(values: Sequence[str]) -> dict[str, tuple[str, ...]]:
    filters: dict[str, list[str]] = defaultdict(list)
    for value in values:
        field, separator, expected = value.partition("=")
        if not separator or field not in DESCRIPTOR_FIELDS or not expected:
            raise ValueError(
                "descriptor filters must use FIELD=VALUE with a schema 1 descriptor field"
            )
        filters[field].append(expected)
    return {field: tuple(items) for field, items in filters.items()}


if __name__ == "__main__":
    raise SystemExit(main())
