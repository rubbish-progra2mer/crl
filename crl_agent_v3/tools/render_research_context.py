from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.research_context import render_research_context
from crl_v3.workspace import ResearchWorkspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render one deterministic, read-only CRL Research Context View."
    )
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", default="v001")
    parser.add_argument("--hypothesis-id", action="append", default=[])
    parser.add_argument("--search-id", action="append", default=[])
    budget = parser.add_mutually_exclusive_group()
    budget.add_argument("--max-characters", "--max-chars", dest="max_characters", type=int)
    budget.add_argument(
        "--max-approx-tokens", "--max-tokens", dest="max_approx_tokens", type=int
    )
    for name in (
        "charter",
        "portfolio",
        "research-bundle",
        "prior-audit",
        "falsification",
        "experiments",
        "markdown",
    ):
        parser.add_argument(
            f"--include-{name}",
            action=argparse.BooleanOptionalAction,
            default=True,
        )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        workspace = ResearchWorkspace(
            arguments.run_root,
            version=arguments.version,
            product_root=arguments.product_root,
        )
        rendered = render_research_context(
            workspace,
            hypothesis_ids=arguments.hypothesis_id,
            search_ids=arguments.search_id,
            max_characters=arguments.max_characters,
            max_approx_tokens=arguments.max_approx_tokens,
            include_charter=arguments.include_charter,
            include_portfolio=arguments.include_portfolio,
            include_research_bundle=arguments.include_research_bundle,
            include_prior_audit=arguments.include_prior_audit,
            include_falsification=arguments.include_falsification,
            include_experiments=arguments.include_experiments,
            include_markdown=arguments.include_markdown,
        )
        sys.stdout.buffer.write(rendered)
        return 0
    except (
        FileNotFoundError,
        KeyError,
        OSError,
        UnicodeError,
        ValueError,
    ) as error:
        print(f"render_research_context: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
