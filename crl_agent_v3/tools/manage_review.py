from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.review import (
    read_review_request,
    render_review_input,
    review_material_errors,
)
from crl_v3.workspace import ResearchWorkspace
from crl_v3.workspace import _required_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the thin three-reviewer text stage.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    request = subparsers.add_parser("create-request")
    _add_workspace(request)
    request.add_argument("--body-file", required=True, type=Path)
    request.add_argument("--reading", action="append", required=True)

    report = subparsers.add_parser("save-report")
    _add_workspace(report)
    report.add_argument("--reviewer-number", required=True, type=int, choices=(1, 2, 3))
    report.add_argument("--reviewer-id", required=True)
    report.add_argument("--report-file", required=True, type=Path)

    render = subparsers.add_parser("render-input")
    _add_workspace(render)

    status = subparsers.add_parser("status")
    _add_workspace(status)
    return parser


def _add_workspace(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", default="v001")


def _read_utf8(path: Path) -> str:
    return _required_file(path).decode("utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        workspace = ResearchWorkspace(
            arguments.run_root,
            version=arguments.version,
            product_root=arguments.product_root,
        )
        if arguments.action == "render-input":
            sys.stdout.buffer.write(render_review_input(workspace))
            return 0
        if arguments.action == "create-request":
            document = workspace.write_review_request(
                _read_utf8(arguments.body_file), arguments.reading
            )
            payload = {
                "action": arguments.action,
                "path": document.path,
                "sha256": document.sha256,
                "reading_paths": document.reading_paths,
                "materials": [
                    {
                        "path": item.path,
                        "size_bytes": item.size_bytes,
                        "sha256": item.sha256,
                    }
                    for item in document.materials
                ],
            }
        elif arguments.action == "save-report":
            document = workspace.write_reviewer_report(
                arguments.reviewer_number,
                arguments.reviewer_id,
                _read_utf8(arguments.report_file),
            )
            payload = {
                "action": arguments.action,
                "path": document.path,
                "sha256": document.sha256,
                "reviewer_number": document.reviewer_number,
                "reviewer_id": document.reviewer_id,
                "request_sha256": document.request_sha256,
            }
        else:
            reports = workspace.list_reviewer_reports()
            request_path = workspace.review_path / "request.md"
            request_exists = request_path.is_file()
            request = read_review_request(workspace) if request_exists else None
            material_errors = review_material_errors(workspace)
            payload = {
                "action": arguments.action,
                "request_exists": request_exists,
                "reviewers": [
                    {
                        "number": report.reviewer_number,
                        "id": report.reviewer_id,
                        "path": report.path,
                    }
                    for report in reports
                ],
                "reading_paths": list(request.reading_paths) if request else [],
                "request_sha256": request.sha256 if request else None,
                "materials": [
                    {
                        "path": item.path,
                        "size_bytes": item.size_bytes,
                        "sha256": item.sha256,
                    }
                    for item in request.materials
                ] if request else [],
                "complete": not material_errors,
                "material_errors": list(material_errors),
                "decision_exists": workspace.document_path("decision").is_file(),
            }
    except (OSError, UnicodeError, ValueError) as error:
        print(f"manage_review: {error}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
