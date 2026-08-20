from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.prior_audit import create_prior_audit, download_prior_candidate_pdf
from crl_v3.knowledge import KnowledgeStore
from crl_v3.workspace import ResearchWorkspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create a Run-local, non-authoritative nearest-prior search snapshot, "
            "or explicitly download one selected candidate PDF."
        )
    )
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", default="v001")
    parser.add_argument("--hypothesis-id", required=True)
    parser.add_argument("--query", action="append")
    parser.add_argument("--seed-paper-id")
    parser.add_argument("--audit-id", required=True)
    parser.add_argument("--per-source-limit", type=int, default=20)
    parser.add_argument("--expansion-limit", type=int, default=100)
    parser.add_argument("--expansion-pages", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--download-candidate-id")
    parser.add_argument("--max-pdf-mib", type=int, default=50)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    arguments = build_parser().parse_args(argv)
    try:
        knowledge_store = None
        knowledge_database = (
            Path(arguments.product_root).resolve() / "knowledge_base" / "knowledge.sqlite"
        )
        if knowledge_database.is_file():
            knowledge_store = KnowledgeStore(knowledge_database, read_only=True)
        workspace = ResearchWorkspace(
            arguments.run_root,
            version=arguments.version,
            product_root=arguments.product_root,
            knowledge_store=knowledge_store,
        )
        try:
            if arguments.download_candidate_id:
                result = download_prior_candidate_pdf(
                    workspace,
                    arguments.audit_id,
                    arguments.hypothesis_id,
                    arguments.download_candidate_id,
                    timeout=arguments.timeout,
                    max_bytes=arguments.max_pdf_mib * 1024 * 1024,
                )
                payload = {"action": "download", **asdict(result)}
            else:
                publication = create_prior_audit(
                    workspace,
                    arguments.hypothesis_id,
                    arguments.query or (),
                    arguments.audit_id,
                    seed_paper_id=arguments.seed_paper_id,
                    per_source_limit=arguments.per_source_limit,
                    expansion_limit=arguments.expansion_limit,
                    expansion_pages=arguments.expansion_pages,
                    timeout=arguments.timeout,
                    max_retries=arguments.max_retries,
                )
                payload = {"action": "create", **asdict(publication)}
        finally:
            if knowledge_store is not None:
                knowledge_store.close()
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return 0
    except (FileExistsError, FileNotFoundError, KeyError, OSError, UnicodeError, ValueError) as error:
        message = str(error)
        secret = os.environ.get("S2_API_KEY")
        if secret:
            message = message.replace(secret, "[REDACTED]")
        print(f"audit_prior: {message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
