from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from crl_v3.workspace import (
    ResearchWorkspace,
    _publish_once,
    _required_content,
    _required_file,
    _sha256,
    safe_relative_path,
)


_REQUEST_META_PREFIX = "<!-- CRL_REVIEW_REQUEST_META "
_REPORT_META_PREFIX = "<!-- CRL_REVIEW_REPORT_META "
_META_SUFFIX = " -->"
_REQUEST_SCHEMA_VERSION = 2
_REPORT_SCHEMA_VERSION = 2


@dataclass(frozen=True, slots=True)
class ReviewMaterialSnapshot:
    path: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class ReviewRequestDocument:
    path: str
    version: str
    content: str
    reading_paths: tuple[str, ...]
    materials: tuple[ReviewMaterialSnapshot, ...]
    sha256: str


@dataclass(frozen=True, slots=True)
class ReviewerReportDocument:
    path: str
    version: str
    reviewer_number: int
    reviewer_id: str
    content: str
    report_text: str
    request_sha256: str
    sha256: str


def write_review_request(
    workspace: ResearchWorkspace,
    content: str,
    reading_paths: Iterable[str | Path],
) -> ReviewRequestDocument:
    """发布三位独立文字审查者共同阅读的当前版本材料。"""

    workspace.assert_run_writable()
    normalized = tuple(
        dict.fromkeys(_normalize_reading_path(workspace, item) for item in reading_paths)
    )
    if not normalized:
        raise ValueError("review reading list must not be empty")
    seed_relative = workspace.seed_path.relative_to(workspace.workspace_path).as_posix()
    if seed_relative not in normalized:
        raise ValueError(f"final review must include {seed_relative}")
    materials = tuple(_snapshot_material(workspace, item) for item in normalized)
    body = _required_content(content).rstrip()
    metadata = json.dumps(
        {
            "schema_version": _REQUEST_SCHEMA_VERSION,
            "version": workspace.version,
            "materials": [
                {
                    "path": item.path,
                    "size_bytes": item.size_bytes,
                    "sha256": item.sha256,
                }
                for item in materials
            ],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    rendered = "\n".join(
        (
            "# Review Request",
            f"{_REQUEST_META_PREFIX}{metadata}{_META_SUFFIX}",
            "",
            "## Reading List",
            "",
            *(f"- {path}" for path in normalized),
            "",
            "## Main AI Note",
            "",
            body,
            "",
        )
    )
    path = workspace.review_path / "request.md"
    workspace.assert_write_target(path)
    _publish_once(path, rendered.encode("utf-8"), within=workspace.workspace_path)
    return read_review_request(workspace)


def read_review_request(workspace: ResearchWorkspace) -> ReviewRequestDocument:
    path = workspace.review_path / "request.md"
    data = _required_file(path, within=workspace.workspace_path)
    content = data.decode("utf-8")
    metadata = _metadata_line(
        content,
        _REQUEST_META_PREFIX,
        {"schema_version", "version", "materials"},
    )
    if metadata.get("schema_version") != _REQUEST_SCHEMA_VERSION:
        raise ValueError("unsupported review request schema version")
    version = _metadata_string(metadata, "version")
    if version != workspace.version:
        raise ValueError("review request version does not match workspace version")
    reading_paths = _reading_paths(content)
    if not reading_paths:
        raise ValueError("review request reading list is empty")
    if len(reading_paths) != len(set(reading_paths)):
        raise ValueError("review request reading list contains duplicate paths")
    for item in reading_paths:
        _normalize_reading_path(workspace, item)
    materials = _parse_materials(metadata.get("materials"))
    if tuple(item.path for item in materials) != reading_paths:
        raise ValueError("review request material snapshot disagrees with reading list")
    seed_relative = workspace.seed_path.relative_to(workspace.workspace_path).as_posix()
    if seed_relative not in reading_paths:
        raise ValueError(f"review request does not include {seed_relative}")
    return ReviewRequestDocument(
        path=str(path),
        version=version,
        content=content,
        reading_paths=reading_paths,
        materials=materials,
        sha256=_sha256(data),
    )


def render_review_input(workspace: ResearchWorkspace) -> bytes:
    """渲染可逐字节交给三位审查者的确定性完整输入。"""

    request = read_review_request(workspace)
    errors = _material_snapshot_errors(workspace, request)
    if errors:
        raise ValueError("reviewed materials changed:\n- " + "\n- ".join(errors))

    request_data = _required_file(Path(request.path), within=workspace.workspace_path)
    chunks = [
        b"===== REVIEW REQUEST =====\n",
        f"REQUEST_SHA256: {request.sha256}\n".encode("ascii"),
        request_data,
    ]
    if not request_data.endswith(b"\n"):
        chunks.append(b"\n")
    chunks.append(b"===== END REVIEW REQUEST =====\n")

    for material in request.materials:
        material_path = workspace.workspace_path / material.path
        data = _required_file(material_path, within=workspace.workspace_path)
        chunks.extend(
            (
                b"\n===== BEGIN MATERIAL =====\n",
                f"PATH: {material.path}\n".encode("utf-8"),
                f"SIZE_BYTES: {material.size_bytes}\n".encode("ascii"),
                f"SHA256: {material.sha256}\n".encode("ascii"),
                data,
            )
        )
        if not data.endswith(b"\n"):
            chunks.append(b"\n")
        chunks.append(b"===== END MATERIAL =====\n")
    return b"".join(chunks)


def write_reviewer_report(
    workspace: ResearchWorkspace,
    reviewer_number: int,
    reviewer_id: str,
    content: str,
) -> ReviewerReportDocument:
    workspace.assert_run_writable()
    request = read_review_request(workspace)
    material_errors = _material_snapshot_errors(workspace, request)
    if material_errors:
        raise ValueError("reviewed materials changed:\n- " + "\n- ".join(material_errors))
    number = _reviewer_number(reviewer_number)
    identity = _single_line(reviewer_id, "reviewer_id")
    path = workspace.review_path / f"reviewer_{number}.md"
    workspace.assert_write_target(path)
    if identity in _all_reviewer_ids(workspace.workspace_path, exclude=path):
        raise ValueError("reviewer context identifier was already used in this Run")
    body = _required_content(content).rstrip()
    metadata = json.dumps(
        {
            "schema_version": _REPORT_SCHEMA_VERSION,
            "version": workspace.version,
            "reviewer_number": number,
            "reviewer_id": identity,
            "request_sha256": request.sha256,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    rendered = "\n".join(
        (
            f"# Reviewer {number} Report",
            f"{_REPORT_META_PREFIX}{metadata}{_META_SUFFIX}",
            "",
            "## Independent Opinion",
            "",
            body,
            "",
        )
    )
    _publish_once(path, rendered.encode("utf-8"), within=workspace.workspace_path)
    return read_reviewer_report(workspace, number)


def read_reviewer_report(
    workspace: ResearchWorkspace, reviewer_number: int
) -> ReviewerReportDocument:
    number = _reviewer_number(reviewer_number)
    path = workspace.review_path / f"reviewer_{number}.md"
    data = _required_file(path, within=workspace.workspace_path)
    content = data.decode("utf-8")
    metadata = _metadata_line(
        content,
        _REPORT_META_PREFIX,
        {
            "schema_version",
            "version",
            "reviewer_number",
            "reviewer_id",
            "request_sha256",
        },
    )
    if metadata.get("schema_version") != _REPORT_SCHEMA_VERSION:
        raise ValueError("unsupported reviewer report schema version")
    version = _metadata_string(metadata, "version")
    saved_number = metadata["reviewer_number"]
    if version != workspace.version or saved_number != number:
        raise ValueError("reviewer report metadata does not match its path")
    identity = _metadata_string(metadata, "reviewer_id")
    request_sha256 = _metadata_string(metadata, "request_sha256")
    request = read_review_request(workspace)
    if request_sha256 != request.sha256:
        raise ValueError("reviewer report is bound to a different review request")
    marker = "## Independent Opinion\n\n"
    if content.count(marker) != 1:
        raise ValueError("reviewer report opinion section is invalid")
    report_text = content.split(marker, 1)[1]
    if not report_text.strip():
        raise ValueError("reviewer report opinion is empty")
    return ReviewerReportDocument(
        path=str(path),
        version=version,
        reviewer_number=number,
        reviewer_id=identity,
        content=content,
        report_text=report_text,
        request_sha256=request_sha256,
        sha256=_sha256(data),
    )


def list_reviewer_reports(
    workspace: ResearchWorkspace,
) -> tuple[ReviewerReportDocument, ...]:
    reports = []
    for number in (1, 2, 3):
        path = workspace.review_path / f"reviewer_{number}.md"
        if path.is_file():
            reports.append(read_reviewer_report(workspace, number))
    identities = [report.reviewer_id for report in reports]
    if len(identities) != len(set(identities)):
        raise ValueError("reviewer context identifiers are not distinct")
    return tuple(reports)


def review_material_errors(workspace: ResearchWorkspace) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        request = read_review_request(workspace)
        errors.extend(_material_snapshot_errors(workspace, request))
    except (FileNotFoundError, UnicodeDecodeError, ValueError) as error:
        errors.append(str(error))
        request = None
    try:
        reports = list_reviewer_reports(workspace)
    except (FileNotFoundError, UnicodeDecodeError, ValueError) as error:
        errors.append(str(error))
        reports = ()
    if len(reports) != 3:
        errors.append(f"expected 3 reviewer reports, found {len(reports)}")
    if request is not None:
        for report in reports:
            if report.request_sha256 != request.sha256:
                errors.append(
                    f"reviewer {report.reviewer_number} request SHA-256 does not match"
                )
    return tuple(errors)


def _normalize_reading_path(
    workspace: ResearchWorkspace, value: str | Path
) -> str:
    relative = safe_relative_path(value)
    lexical = workspace.assert_write_target(workspace.workspace_path / relative)
    try:
        candidate = workspace.assert_read_target(lexical)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"review reading file does not exist: {relative.as_posix()}"
        ) from error
    if candidate.suffix.casefold() != ".md":
        raise ValueError(f"reviewers may only receive Markdown files: {relative.as_posix()}")
    _required_file(candidate, within=workspace.workspace_path)
    normalized = candidate.relative_to(workspace.workspace_path).as_posix()
    if not _belongs_to_version(normalized, workspace.version):
        raise ValueError(
            f"review reading file is not associated with {workspace.version}: {normalized}"
        )
    return normalized


def _belongs_to_version(relative_path: str, version: str) -> bool:
    relative_path = relative_path.casefold()
    version = version.casefold()
    first = relative_path.split("/", 1)[0]
    if first in {
        f"experiment_{version}",
        f"implementation_{version}",
        f"workbench_{version}",
    }:
        return True
    if first == f"audit_{version}":
        parts = relative_path.split("/")
        return (
            len(parts) == 2
            and parts[1].startswith("seed_support_")
            and parts[1].endswith(".md")
        )
    return relative_path.endswith(f"_{version}.md") and not relative_path.startswith("review_")


def _snapshot_material(
    workspace: ResearchWorkspace, relative_path: str
) -> ReviewMaterialSnapshot:
    path = workspace.workspace_path / relative_path
    data = _required_file(path, within=workspace.workspace_path)
    return ReviewMaterialSnapshot(relative_path, len(data), _sha256(data))


def _parse_materials(value: object) -> tuple[ReviewMaterialSnapshot, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError("review request materials must be a non-empty array")
    materials = []
    seen = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != {"path", "size_bytes", "sha256"}:
            raise ValueError(f"review material {index} does not match the schema")
        path = item.get("path")
        size = item.get("size_bytes")
        digest = item.get("sha256")
        if (
            not isinstance(path, str)
            or not path
            or type(size) is not int
            or size <= 0
            or not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        ):
            raise ValueError(f"review material {index} contains invalid facts")
        if path in seen:
            raise ValueError(f"duplicate review material path: {path}")
        seen.add(path)
        materials.append(ReviewMaterialSnapshot(path, size, digest))
    return tuple(materials)


def _material_snapshot_errors(
    workspace: ResearchWorkspace, request: ReviewRequestDocument
) -> tuple[str, ...]:
    errors = []
    for snapshot in request.materials:
        try:
            normalized = _normalize_reading_path(workspace, snapshot.path)
            current = _snapshot_material(workspace, normalized)
            if current.size_bytes != snapshot.size_bytes:
                errors.append(f"review material size changed: {snapshot.path}")
            if current.sha256 != snapshot.sha256:
                errors.append(f"review material SHA-256 changed: {snapshot.path}")
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"invalid review material {snapshot.path}: {error}")
    return tuple(errors)


def _reading_paths(content: str) -> tuple[str, ...]:
    marker = "## Reading List\n\n"
    end_marker = "\n\n## Main AI Note"
    if content.count(marker) != 1 or content.count(end_marker) != 1:
        raise ValueError("review request reading-list section is invalid")
    block = content.split(marker, 1)[1].split(end_marker, 1)[0]
    paths = []
    for line in block.splitlines():
        if line.startswith("- ") and line[2:].strip():
            paths.append(line[2:].strip())
        elif line.strip():
            raise ValueError("review request reading-list entry is invalid")
    return tuple(paths)


def _metadata_line(content: str, prefix: str, fields: set[str]) -> dict[str, object]:
    lines = content.splitlines()
    matches = [line for line in lines[:3] if line.startswith(prefix) and line.endswith(_META_SUFFIX)]
    if len(matches) != 1:
        raise ValueError("missing or duplicate bounded review metadata")
    payload = matches[0][len(prefix) : -len(_META_SUFFIX)]
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as error:
        raise ValueError("invalid review metadata JSON") from error
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError("review metadata fields do not match the schema")
    return value


def _metadata_string(metadata: dict[str, object], name: str) -> str:
    value = metadata.get(name)
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ValueError(f"review metadata {name} must be non-empty single-line text")
    return value.strip()


def _all_reviewer_ids(run_root: Path, *, exclude: Path | None = None) -> set[str]:
    identities: set[str] = set()
    root = run_root.resolve()
    for path in sorted(run_root.glob("review_v*/reviewer_*.md")):
        if exclude is not None and path == exclude:
            continue
        try:
            content = _required_file(path, within=root).decode("utf-8")
            metadata = _metadata_line(
                content,
                _REPORT_META_PREFIX,
                {
                    "schema_version",
                    "version",
                    "reviewer_number",
                    "reviewer_id",
                    "request_sha256",
                },
            )
            if metadata.get("schema_version") != _REPORT_SCHEMA_VERSION:
                raise ValueError("unsupported reviewer report schema version")
            identities.add(_metadata_string(metadata, "reviewer_id"))
        except (OSError, UnicodeError, ValueError):
            raise ValueError(f"cannot verify prior reviewer identity: {path}")
    return identities


def _single_line(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ValueError(f"{name} must be non-empty single-line text")
    return value.strip()


def _reviewer_number(value: int) -> int:
    if type(value) is not int or value not in (1, 2, 3):
        raise ValueError("reviewer_number must be 1, 2, or 3")
    return value
