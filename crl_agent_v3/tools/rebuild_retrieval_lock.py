from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Mapping, Sequence
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.knowledge_audit import _card_source_signature, _file_sha256, _load_json_object


_RUN_NAME = re.compile(r"^\d{8}_\d{4}_run\d{2,}$")
_EVIDENCE_NAME = re.compile(r"[a-z][a-z0-9_-]{1,63}")
_replace = os.replace
_link = os.link


def rebuild_retrieval_lock(
    *,
    knowledge_root: str | Path,
    project_root: str | Path,
    accepted_attempt: str | Path,
    output: str | Path,
    replace: bool = False,
    accepted_evidence: Mapping[str, str | Path] | None = None,
    evaluation_kind: str | None = None,
) -> dict[str, object]:
    project = _existing_directory(project_root, "project_root")
    knowledge = _safe_directory(knowledge_root, project, "knowledge_root")
    attempt = _safe_directory(
        _resolve_under_project(project, accepted_attempt),
        project,
        "accepted_attempt",
    )
    destination = _validated_output(output, project, knowledge)
    if destination.exists() and not replace:
        raise FileExistsError(f"output already exists; use --replace explicitly: {destination}")

    previous = _matching_previous_lock(knowledge, project, attempt)
    evidence_paths = (
        _explicit_evidence_paths(accepted_evidence, project, attempt)
        if accepted_evidence is not None
        else _discover_accepted_evidence(attempt, project, previous)
    )
    source_paths = _source_snapshot_paths(knowledge, project)
    source_snapshot: dict[str, object] = {
        name: _path_identity(path, project) for name, path in source_paths.items()
    }
    cards_root = knowledge / "cards"
    try:
        safe_cards_root = _safe_directory(cards_root, project, "cards_root")
    except FileNotFoundError:
        safe_cards_root = None
    if safe_cards_root is not None:
        source_snapshot["card_source_signature"] = _card_source_signature(
            safe_cards_root, project_root=project
        )

    kind = evaluation_kind
    if kind is None and previous is not None and isinstance(previous.get("evaluation_kind"), str):
        kind = str(previous["evaluation_kind"])
    if kind is None:
        kind = "explicit_maintenance_lock_rebuild"
    if not kind.strip():
        raise ValueError("evaluation_kind must be non-empty")

    document: dict[str, object] = {
        "schema_version": 2,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "accepted_attempt": attempt.relative_to(project).as_posix(),
        "evaluation_kind": kind,
        "accepted_evidence": {
            name: _path_identity(path, project) for name, path in sorted(evidence_paths.items())
        },
        "source_snapshot": source_snapshot,
        "limitations": [
            "This lock records verified retrieval identity and is not a machine readiness gate.",
            "Publishing this lock does not modify Evidence, Cards, databases, or indexes.",
        ],
    }
    data = (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _revalidate_inputs(source_paths, evidence_paths, source_snapshot, document["accepted_evidence"])
    _atomic_publish(destination, data, replace=replace)
    return document


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="显式重算检索身份锁；该锁不是机器就绪门。"
    )
    parser.add_argument("--knowledge-root", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--accepted-attempt", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--accepted-evidence",
        action="append",
        default=[],
        metavar="NAME=PATH",
        help="可重复；省略时从匹配的现有锁或 attempt 中的 result/report 发现。",
    )
    parser.add_argument("--evaluation-kind")
    parser.add_argument("--replace", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        explicit = _parse_evidence_arguments(args.accepted_evidence)
        document = rebuild_retrieval_lock(
            knowledge_root=args.knowledge_root,
            project_root=args.project_root,
            accepted_attempt=args.accepted_attempt,
            output=args.output,
            replace=args.replace,
            accepted_evidence=explicit or None,
            evaluation_kind=args.evaluation_kind,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(f"rebuild_retrieval_lock: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _parse_evidence_arguments(values: Sequence[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for value in values:
        name, separator, raw_path = value.partition("=")
        if not separator or _EVIDENCE_NAME.fullmatch(name) is None or not raw_path:
            raise ValueError("accepted-evidence must use NAME=PATH with a safe lowercase name")
        if name in parsed:
            raise ValueError(f"duplicate accepted-evidence name: {name}")
        parsed[name] = Path(raw_path)
    return parsed


def _matching_previous_lock(knowledge: Path, project: Path, attempt: Path) -> dict[str, object] | None:
    candidate = knowledge / "evaluation" / "PRODUCTION_RETRIEVAL_LOCK.json"
    try:
        path = _safe_file(candidate, project, "existing retrieval lock")
    except FileNotFoundError:
        return None
    try:
        document = _load_json_object(path)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return None
    recorded = document.get("accepted_attempt")
    if not isinstance(recorded, str):
        return None
    try:
        recorded_path = _project_relative_file(project, recorded, require_file=False)
    except (FileNotFoundError, ValueError):
        return None
    return document if recorded_path == attempt else None


def _discover_accepted_evidence(
    attempt: Path,
    project: Path,
    previous: dict[str, object] | None,
) -> dict[str, Path]:
    if previous is not None and isinstance(previous.get("accepted_evidence"), dict):
        discovered: dict[str, Path] = {}
        for name, entry in sorted(previous["accepted_evidence"].items()):
            if _EVIDENCE_NAME.fullmatch(str(name)) is None or not isinstance(entry, dict):
                raise ValueError("existing lock contains an invalid accepted_evidence entry")
            path_value, expected_sha = entry.get("path"), entry.get("sha256")
            if not isinstance(path_value, str) or not isinstance(expected_sha, str):
                raise ValueError("existing lock accepted_evidence lacks path/SHA-256")
            path = _project_relative_file(project, path_value)
            _require_within(path, attempt, "accepted evidence")
            actual = _file_sha256(path)
            if actual != expected_sha:
                raise ValueError(f"accepted evidence SHA-256 mismatch: {path_value}")
            discovered[str(name)] = path
        if discovered:
            return discovered

    report_candidate = attempt / "report.md"
    try:
        report = _safe_file(report_candidate, project, "accepted attempt report")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"accepted attempt report is missing: {report_candidate}"
        ) from exc
    result_candidates: list[Path] = []
    for candidate in sorted(
        {*attempt.glob("*result*.json"), *attempt.glob("*replay*.json")},
        key=lambda path: path.name,
    ):
        result_candidates.append(
            _safe_file(candidate, project, "accepted attempt result")
        )
    if not result_candidates:
        raise FileNotFoundError(f"accepted attempt result JSON is missing: {attempt}")
    discovered = {"report": report}
    for index, path in enumerate(result_candidates, start=1):
        name = "result" if len(result_candidates) == 1 else f"result_{index:02d}_{_safe_name(path.stem)}"
        discovered[name] = path
    return discovered


def _explicit_evidence_paths(values: Mapping[str, str | Path], project: Path, attempt: Path) -> dict[str, Path]:
    if not values:
        raise ValueError("accepted_evidence must not be empty when supplied")
    result: dict[str, Path] = {}
    for name, value in values.items():
        if _EVIDENCE_NAME.fullmatch(name) is None:
            raise ValueError(f"invalid accepted evidence name: {name!r}")
        path = _resolve_under_project(project, value)
        path = _safe_file(path, project, "accepted evidence")
        _require_within(path, attempt, "accepted evidence")
        result[name] = path
    if not any("result" in name for name in result):
        raise ValueError("accepted evidence must include at least one result entry")
    if not any("report" in name for name in result):
        raise ValueError("accepted evidence must include a report entry")
    return result


def _source_snapshot_paths(knowledge: Path, project: Path) -> dict[str, Path]:
    candidates = {
        "scope": knowledge / "CORPUS_SCOPE.md",
        "card_schema": knowledge / "CARD_SCHEMA.md",
        "manifest": knowledge / "corpus" / "manifest.json",
        "evidence": knowledge / "corpus" / "evidence.json",
        "knowledge_db": knowledge / "knowledge.sqlite",
        "vector_index": knowledge / "passages.npz",
        "card_index": knowledge / "cards_fts.sqlite",
    }
    machine_candidate = project / "crl_agent_v3"
    try:
        _safe_directory(
            machine_candidate / "crl_v3", project, "machine crl_v3 directory"
        )
    except FileNotFoundError:
        machine = project
    else:
        machine = machine_candidate
    candidates.update(
        retrieval_code=machine / "crl_v3" / "retrieval.py",
        research_retrieval_code=machine / "crl_v3" / "research_retrieval.py",
        card_code=machine / "crl_v3" / "cards.py",
        knowledge_code=machine / "crl_v3" / "knowledge.py",
        vector_code=machine / "crl_v3" / "vector.py",
    )
    result: dict[str, Path] = {}
    for name, path in candidates.items():
        try:
            result[name] = _safe_file(path, project, f"source snapshot {name}")
        except FileNotFoundError:
            continue
    return result


def _revalidate_inputs(
    source_paths: Mapping[str, Path],
    evidence_paths: Mapping[str, Path],
    source_snapshot: Mapping[str, object],
    accepted_snapshot: object,
) -> None:
    assert isinstance(accepted_snapshot, dict)
    for name, path in source_paths.items():
        entry = source_snapshot[name]
        assert isinstance(entry, dict)
        if _file_sha256(path) != entry["sha256"]:
            raise ValueError(f"source snapshot changed during lock build: {path}")
    for name, path in evidence_paths.items():
        entry = accepted_snapshot[name]
        assert isinstance(entry, dict)
        if _file_sha256(path) != entry["sha256"]:
            raise ValueError(f"accepted evidence changed during lock build: {path}")


def _path_identity(path: Path, project: Path) -> dict[str, str]:
    safe = _safe_file(path, project, "lock source")
    return {"path": safe.relative_to(project).as_posix(), "sha256": _file_sha256(safe)}


def _validated_output(output: str | Path, project: Path, knowledge: Path) -> Path:
    destination = Path(os.path.abspath(output))
    _require_within(destination, project, "output")
    relative = destination.relative_to(project)
    if relative.parts and _RUN_NAME.fullmatch(relative.parts[0]):
        raise ValueError("output must not be inside a formal Run")
    if destination.suffix.casefold() != ".json":
        raise ValueError("output must be a .json file")
    try:
        within_knowledge = destination.relative_to(knowledge)
    except ValueError:
        within_knowledge = None
    if within_knowledge is not None and (not within_knowledge.parts or within_knowledge.parts[0] != "evaluation"):
        raise ValueError("output inside knowledge_root is allowed only under evaluation/")
    _reject_reparse_chain(destination.parent, project)
    destination.parent.mkdir(parents=True, exist_ok=True)
    _reject_reparse_chain(destination.parent, project)
    _require_within(destination.parent.resolve(strict=True), project, "output parent")
    if destination.is_symlink():
        raise ValueError("output must not be a symbolic link")
    return destination


def _atomic_publish(path: Path, data: bytes, *, replace: bool) -> None:
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if replace:
            _replace(temporary, path)
        else:
            _link(temporary, path)
            temporary.unlink()
    finally:
        temporary.unlink(missing_ok=True)


def _resolve_under_project(project: Path, value: str | Path) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project / candidate
    return Path(os.path.abspath(candidate))


def _project_relative_file(project: Path, value: str, *, require_file: bool = True) -> Path:
    pure = PurePosixPath(value)
    if not value or "\\" in value or pure.is_absolute() or ".." in pure.parts or any(part in {"", "."} for part in pure.parts):
        raise ValueError(f"invalid project-relative path: {value!r}")
    path = project.joinpath(*pure.parts)
    if require_file:
        return _safe_file(path, project, "project-relative file")
    _reject_reparse_chain(path, project)
    if not path.is_dir():
        raise FileNotFoundError(path)
    return path.resolve(strict=True)


def _safe_file(path: Path, project: Path, label: str) -> Path:
    lexical = Path(os.path.abspath(path))
    _require_within(lexical, project, label)
    _reject_reparse_chain(lexical, project)
    if not lexical.is_file():
        raise FileNotFoundError(lexical)
    resolved = lexical.resolve(strict=True)
    _require_within(resolved, project, label)
    return resolved


def _existing_directory(path: str | Path, label: str) -> Path:
    lexical = Path(os.path.abspath(path))
    if _is_reparse_point(lexical) or not lexical.is_dir():
        raise FileNotFoundError(f"{label} is not a real existing directory: {lexical}")
    return lexical.resolve(strict=True)


def _safe_directory(path: str | Path, project: Path, label: str) -> Path:
    lexical = Path(os.path.abspath(path))
    _require_within(lexical, project, label)
    _reject_reparse_chain(lexical, project)
    if not lexical.is_dir():
        raise FileNotFoundError(f"{label} is not a real existing directory: {lexical}")
    resolved = lexical.resolve(strict=True)
    _require_within(resolved, project, label)
    return resolved


def _require_within(path: Path, root: Path, label: str) -> None:
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes project_root: {path}") from exc


def _reject_reparse_chain(path: Path, root: Path) -> None:
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes project_root: {path}") from exc
    current = root
    for part in relative.parts:
        current = current / part
        if (current.exists() or current.is_symlink()) and _is_reparse_point(current):
            raise ValueError(f"path uses a reparse point: {current}")


def _is_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = os.lstat(path).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _safe_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    return normalized[:40] or "artifact"


if __name__ == "__main__":
    raise SystemExit(main())
