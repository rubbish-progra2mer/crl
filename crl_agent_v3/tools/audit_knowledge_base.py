from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Sequence
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.knowledge_audit import audit_knowledge_base


_RUN_NAME = re.compile(r"^\d{8}_\d{4}_run\d{2,}$")
_link = os.link


def build_parser() -> argparse.ArgumentParser:
    project = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        description="只读执行独立知识库维护审计；结果不是启动门或科研评分。"
    )
    parser.add_argument("--knowledge-root", type=Path, default=project / "knowledge_base")
    parser.add_argument("--project-root", type=Path, default=project)
    parser.add_argument("--lock", type=Path)
    parser.add_argument(
        "--write-report",
        type=Path,
        metavar="MAINTENANCE_DIRECTORY",
        help="把同一 JSON 原子写入明确指定的维护目录；不会写入正式 Run。",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        report = audit_knowledge_base(
            args.knowledge_root,
            project_root=args.project_root,
            lock_path=args.lock,
        )
        payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.write_report is not None:
            destination = _report_destination(args.write_report, args.project_root)
            _publish_once(destination, payload.encode("utf-8"))
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        print(f"audit_knowledge_base: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(payload)
    return 0


def _report_destination(directory: Path, project_root: Path) -> Path:
    project = project_root.resolve(strict=True)
    target_directory = Path(os.path.abspath(directory))
    try:
        relative = target_directory.relative_to(project)
    except ValueError as exc:
        raise ValueError("write-report maintenance directory must be within project_root") from exc
    if relative.parts and _RUN_NAME.fullmatch(relative.parts[0]):
        raise ValueError("write-report must not target a formal Run")
    current = project
    for part in relative.parts:
        current = current / part
        if (current.exists() or current.is_symlink()) and _is_reparse_point(current):
            raise ValueError(f"write-report path uses a reparse point: {current}")
    target_directory.mkdir(parents=True, exist_ok=True)
    resolved = target_directory.resolve(strict=True)
    try:
        resolved.relative_to(project)
    except ValueError as exc:
        raise ValueError("write-report directory resolves outside project_root") from exc
    return resolved / "knowledge_audit.json"


def _publish_once(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"maintenance report already exists: {path}")
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        _link(temporary, path)
        temporary.unlink()
    finally:
        temporary.unlink(missing_ok=True)


def _is_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = os.lstat(path).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


if __name__ == "__main__":
    raise SystemExit(main())
