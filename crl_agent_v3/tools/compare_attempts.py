from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.comparison import compare_attempts
from crl_v3.workspace import ResearchWorkspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create a fixed Run-local factual parity comparison without selecting "
            "a winner or changing scientific state."
        )
    )
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", default="v001")
    parser.add_argument("--comparison-id", required=True)
    parser.add_argument("--candidate-attempt", required=True)
    parser.add_argument("--baseline-attempt", action="append", required=True)
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
        publication = compare_attempts(
            workspace,
            arguments.comparison_id,
            arguments.candidate_attempt,
            arguments.baseline_attempt,
        )
        print(json.dumps(asdict(publication), ensure_ascii=False, sort_keys=True))
        return 0
    except (FileExistsError, FileNotFoundError, OSError, UnicodeError, ValueError) as error:
        print(f"compare_attempts: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
