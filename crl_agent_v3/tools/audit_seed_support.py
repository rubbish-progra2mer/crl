from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.seed_support import (
    audit_seed_support,
    publish_seed_support_audit,
    render_seed_support_json,
    render_seed_support_markdown,
)
from crl_v3.workspace import ResearchWorkspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render a pre-review advisory audit of explicit Seed support facts."
    )
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", default="v001")
    parser.add_argument("--supporting-attempt", action="append", default=[])
    parser.add_argument("--max-prior-age-days", type=float, default=30.0)
    parser.add_argument("--as-of-utc")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--save-audit-id")
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
        payload = audit_seed_support(
            workspace,
            arguments.supporting_attempt,
            max_prior_age_days=arguments.max_prior_age_days,
            as_of_utc=arguments.as_of_utc,
        )
        if arguments.save_audit_id:
            publish_seed_support_audit(workspace, payload, arguments.save_audit_id)
        output = (
            render_seed_support_json(payload)
            if arguments.format == "json"
            else render_seed_support_markdown(payload)
        )
        sys.stdout.write(output)
        return 0
    except (FileExistsError, FileNotFoundError, OSError, UnicodeError, ValueError) as error:
        print(f"audit_seed_support: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
