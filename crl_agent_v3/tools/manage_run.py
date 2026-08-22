from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path, PureWindowsPath
from typing import Any, Mapping, Sequence
from uuid import uuid4
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.workspace import ResearchWorkspace, _atomic_write_text, _required_file
from crl_v3.workspace import (
    CURRENT_CONTRACT_VERSION,
    PERMANENT_TERMINAL_FILE_STATUS,
    RESUMABLE_STATUSES,
    bind_run,
    require_current_contract,
    _is_reparse_point,
    _path_entry_exists,
)


RUN_PATTERN = re.compile(r"^(\d{8})_(\d{4})_run(\d{2,})$")
VERSION_PATTERN = re.compile(r"^v(\d{3,})$")
VERSION_IN_NAME = re.compile(r"(?:^|_)(v\d{3,})(?:\.md|$)")
PERMANENT_TERMINAL_STATUSES = set(PERMANENT_TERMINAL_FILE_STATUS.values())
CURRENT_VERSION = "v001"
DEFAULT_DOMAIN = "TEXT_AND_TOOL_LLM_AGENT"
SHANGHAI = ZoneInfo("Asia/Shanghai")
_TRANSITION_FIELDS = {
    "CHANGED_COORDINATE",
    "SURVIVING_FRONTIER",
    "NEXT_HIGH_INFORMATION_ACTION",
}
_OPTIONAL_TRANSITION_FIELDS = {"RESOURCE_NEEDED"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create, resume, pause, terminate, or advance one Contract v3 CRL Run."
        )
    )
    subparsers = parser.add_subparsers(dest="action", required=True)
    start = subparsers.add_parser("start")
    start.add_argument("--product-root", required=True, type=Path)
    start.add_argument("--run", help="explicit runNN, Run id, or absolute Run directory")
    direction = start.add_mutually_exclusive_group()
    direction.add_argument("--direction")
    direction.add_argument("--direction-file", type=Path)
    advance = subparsers.add_parser("advance-version")
    advance.add_argument("--product-root", required=True, type=Path)
    advance.add_argument("--run", required=True, help="explicit runNN, Run id, or absolute Run directory")
    advance.add_argument(
        "--transition-file",
        required=True,
        type=Path,
        help=(
            "UTF-8/LF JSON object containing CHANGED_COORDINATE, "
            "SURVIVING_FRONTIER, NEXT_HIGH_INFORMATION_ACTION, and optional "
            "RESOURCE_NEEDED"
        ),
    )
    pause = subparsers.add_parser("pause")
    pause.add_argument("--product-root", required=True, type=Path)
    pause.add_argument("--run", required=True, help="explicit runNN, Run id, or absolute Run directory")
    pause.add_argument("--note-file", type=Path)
    terminate = subparsers.add_parser("terminate")
    terminate.add_argument("--product-root", required=True, type=Path)
    terminate.add_argument("--run", required=True, help="explicit runNN, Run id, or absolute Run directory")
    terminate.add_argument("--note-file", type=Path)
    return parser


def start_run(
    product_root: str | Path,
    *,
    requested_run: str | None = None,
    direction: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    root = Path(product_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"product root is not an existing directory: {root}")
    normalized_direction = _normalize_direction(direction)
    if requested_run is not None:
        if normalized_direction is not None:
            raise ValueError("a resumed Run cannot receive a new research direction")
        return _resume_run(root, requested_run)
    return _create_run(root, normalized_direction, now)


def _resume_run(product_root: Path, requested_run: str) -> dict[str, Any]:
    from crl_v3.decision import read_delivery_history, read_no_delivery_history

    run_root = _resolve_requested_run(product_root, requested_run)
    require_current_contract(run_root)
    terminals = [
        name
        for name in PERMANENT_TERMINAL_FILE_STATUS
        if (run_root / name).is_file()
    ]
    if terminals:
        raise ValueError(
            f"terminal Run cannot be reopened because {', '.join(terminals)} exists: {run_root.name}"
        )
    fields = _read_fields(run_root / "RUN_STATUS.md")
    status = fields.get("STATUS")
    if status in PERMANENT_TERMINAL_STATUSES:
        raise ValueError(f"Run is not resumable: {run_root.name} ({status})")
    current_version = fields.get("CURRENT_VERSION", CURRENT_VERSION)
    _assert_no_future_version_files(run_root, current_version)
    workspace = ResearchWorkspace(run_root, version=current_version, product_root=product_root)
    deliveries = read_delivery_history(workspace)
    no_deliveries = read_no_delivery_history(workspace)
    conclusions = sorted(
        (*deliveries, *no_deliveries), key=lambda item: int(item.version[1:])
    )
    conclusion_versions = [item.version for item in conclusions]
    if len(conclusion_versions) != len(set(conclusion_versions)):
        raise ValueError("multiple scientific conclusions exist for one version")
    latest = conclusions[-1] if conclusions else None

    if status in {"DELIVERED", "CONCLUDED_NO_DELIVERY"}:
        expected = (
            "DELIVERED" if status == "DELIVERED" else "CONCLUDED_NO_DELIVERY"
        )
        if latest is None or latest.status != expected:
            raise ValueError(f"{status} Run has no matching valid conclusion record")
        if latest.version != current_version:
            raise ValueError(
                "latest scientific conclusion does not match "
                "RUN_STATUS.md CURRENT_VERSION"
            )
        match = VERSION_PATTERN.fullmatch(current_version)
        assert match is not None
        next_version = f"v{int(match.group(1)) + 1:03d}"
        timestamp = _normalize_now(None).isoformat(timespec="seconds")
        event = (
            "DELIVERED_RUN_RESUMED"
            if status == "DELIVERED"
            else "NO_DELIVERY_RUN_RESUMED"
        )
        prior_field = (
            "PRIOR_DELIVERY" if status == "DELIVERED" else "PRIOR_NO_DELIVERY"
        )
        _update_status_and_ledger(
            workspace,
            status_updates={
                "STATUS": "ACTIVE",
                "CURRENT_VERSION": next_version,
                "LAST_DURABLE_ARTIFACT": "RUN_LEDGER.md",
                "UPDATED_AT": timestamp,
            },
            ledger_entry=(
                f"- EVENT: {event}\n"
                f"  AT: {timestamp}\n"
                f"  FROM_VERSION: {current_version}\n"
                f"  VERSION: {next_version}\n"
                f"  {prior_field}: {Path(latest.path).name}\n"
                f"  {prior_field}_SHA256: {latest.sha256}\n"
            ),
        )
        status = "ACTIVE"
        current_version = next_version
    elif status == "PAUSED_BY_USER":
        if latest is not None and int(current_version[1:]) <= int(latest.version[1:]):
            raise ValueError(
                "paused Run version must be newer than its latest scientific conclusion"
            )
        timestamp = _normalize_now(None).isoformat(timespec="seconds")
        _update_status_and_ledger(
            workspace,
            status_updates={
                "STATUS": "ACTIVE",
                "LAST_DURABLE_ARTIFACT": "RUN_LEDGER.md",
                "UPDATED_AT": timestamp,
            },
            ledger_entry=(
                "- EVENT: RUN_RESUMED\n"
                f"  AT: {timestamp}\n"
                f"  FROM_STATUS: {status}\n"
                f"  VERSION: {current_version}\n"
            ),
        )
        status = "ACTIVE"
    elif status == "ACTIVE":
        if latest is not None and int(current_version[1:]) <= int(latest.version[1:]):
            raise ValueError(
                "active Run version must be newer than its latest scientific conclusion"
            )
    else:
        raise ValueError(f"Run is not resumable: {run_root.name} ({status})")
    return {
        "action": "resume",
        "run_id": run_root.name,
        "run_number": _run_number(run_root),
        "run_root": str(run_root),
        "status": status,
        "mode": fields.get("MODE"),
        "current_version": current_version,
    }


def advance_version(
    product_root: str | Path,
    requested_run: str,
    *,
    transition: Mapping[str, object],
    now: datetime | None = None,
) -> dict[str, Any]:
    root = Path(product_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"product root is not an existing directory: {root}")
    run_root = _resolve_requested_run(root, requested_run)
    require_current_contract(run_root)
    fields = _read_fields(run_root / "RUN_STATUS.md")
    current = fields.get("CURRENT_VERSION", CURRENT_VERSION)
    match = VERSION_PATTERN.fullmatch(current)
    if match is None:
        raise ValueError(f"invalid CURRENT_VERSION: {current!r}")
    _assert_no_future_version_files(run_root, current)
    workspace = ResearchWorkspace(run_root, version=current, product_root=root)
    workspace.assert_run_writable()
    next_version = f"v{int(match.group(1)) + 1:03d}"
    conflicts = [
        path.name
        for path in run_root.iterdir()
        if next_version in _versions_from_name(path.name)
    ]
    if conflicts:
        raise ValueError(
            f"next version {next_version} already has conflicting artifacts: "
            + ", ".join(sorted(conflicts))
        )
    timestamp = _normalize_now(now).isoformat(timespec="seconds")
    normalized_transition = _normalize_transition(transition)
    continuation_name = f"selection_context_{next_version}.md"
    continuation_path = workspace.assert_write_target(run_root / continuation_name)
    continuation_text = _render_transition_context(
        current,
        next_version,
        normalized_transition,
    )
    continuation_sha256 = _sha256_text(continuation_text)
    status_path = workspace.assert_write_target(run_root / "RUN_STATUS.md")
    ledger_path = workspace.assert_write_target(run_root / "RUN_LEDGER.md")
    status_text = _replace_control_fields(
        _read_utf8_lf(status_path, within=workspace.workspace_path),
        {
            "CURRENT_VERSION": next_version,
            "LAST_DURABLE_ARTIFACT": continuation_name,
            "UPDATED_AT": timestamp,
        },
    )
    ledger_text = _read_utf8_lf(
        ledger_path, within=workspace.workspace_path
    ).rstrip() + (
        "\n\n- EVENT: VERSION_ADVANCED\n"
        f"  AT: {timestamp}\n"
        f"  FROM_VERSION: {current}\n"
        f"  VERSION: {next_version}\n"
        f"  CONTINUATION: {continuation_name}\n"
        f"  CONTINUATION_SHA256: {continuation_sha256}\n"
    )
    original_status = _read_utf8_lf(
        status_path, within=workspace.workspace_path
    )
    original_ledger = _read_utf8_lf(
        ledger_path, within=workspace.workspace_path
    )
    continuation_created = False
    try:
        if continuation_path.exists() or continuation_path.is_symlink():
            raise FileExistsError(
                f"next version continuation already exists: {continuation_name}"
            )
        _atomic_write_text(
            continuation_path, continuation_text, within=run_root
        )
        continuation_created = True
        _atomic_write_text(ledger_path, ledger_text, within=run_root)
        _atomic_write_text(status_path, status_text, within=run_root)
    except BaseException as error:
        rollback_errors = []
        for path, content in (
            (ledger_path, original_ledger),
            (status_path, original_status),
        ):
            try:
                _atomic_write_text(path, content, within=run_root)
            except BaseException as rollback_error:
                rollback_errors.append(f"{path.name}: {rollback_error}")
        if continuation_created:
            try:
                continuation_path.unlink()
            except OSError as rollback_error:
                rollback_errors.append(
                    f"{continuation_path.name}: {rollback_error}"
                )
        if rollback_errors:
            raise OSError(
                "version advance failed and control-file rollback was incomplete: "
                + "; ".join(rollback_errors)
            ) from error
        raise
    return {
        "action": "advance_version",
        "run_id": run_root.name,
        "run_root": str(run_root),
        "previous_version": current,
        "current_version": next_version,
        "status": fields.get("STATUS"),
        "continuation_path": str(continuation_path),
        "continuation_sha256": continuation_sha256,
    }


def pause_run(
    product_root: str | Path,
    requested_run: str,
    *,
    note: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    root = Path(product_root).resolve()
    run_root = _resolve_requested_run(root, requested_run)
    require_current_contract(run_root)
    fields = _read_fields(run_root / "RUN_STATUS.md")
    status = fields.get("STATUS")
    if status != "ACTIVE":
        raise ValueError(f"only an ACTIVE Run can be paused: {run_root.name} ({status})")
    version = fields.get("CURRENT_VERSION", CURRENT_VERSION)
    workspace = ResearchWorkspace(run_root, version=version, product_root=root)
    workspace.assert_run_writable()
    timestamp = _normalize_now(now).isoformat(timespec="seconds")
    note_text = _normalize_note(note)
    ledger_entry = (
        "- EVENT: RUN_PAUSED_BY_USER\n"
        f"  AT: {timestamp}\n"
        f"  VERSION: {version}\n"
    )
    if note_text:
        ledger_entry += f"  NOTE: {note_text}\n"
    _update_status_and_ledger(
        workspace,
        status_updates={
            "STATUS": "PAUSED_BY_USER",
            "LAST_DURABLE_ARTIFACT": "RUN_LEDGER.md",
            "UPDATED_AT": timestamp,
        },
        ledger_entry=ledger_entry,
    )
    return {
        "action": "pause",
        "run_id": run_root.name,
        "run_root": str(run_root),
        "status": "PAUSED_BY_USER",
        "current_version": version,
    }


def terminate_run(
    product_root: str | Path,
    requested_run: str,
    *,
    note: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    from crl_v3.decision import write_user_termination

    root = Path(product_root).resolve()
    run_root = _resolve_requested_run(root, requested_run)
    require_current_contract(run_root)
    fields = _read_fields(run_root / "RUN_STATUS.md")
    status = fields.get("STATUS")
    if status not in RESUMABLE_STATUSES:
        raise ValueError(f"Run cannot be terminated from status {status}: {run_root.name}")
    version = fields.get("CURRENT_VERSION", CURRENT_VERSION)
    workspace = ResearchWorkspace(run_root, version=version, product_root=root)
    terminal = write_user_termination(
        workspace,
        note=_normalize_note(note),
        terminated_at=_normalize_now(now).isoformat(timespec="seconds"),
    )
    return {
        "action": "terminate",
        "run_id": run_root.name,
        "run_root": str(run_root),
        "status": terminal.status,
        "current_version": version,
        "terminal": terminal.path,
    }


def _resolve_requested_run(product_root: Path, requested_run: str) -> Path:
    requested_path = Path(requested_run)
    windows_path = PureWindowsPath(requested_run)
    if requested_path.is_absolute() or windows_path.is_absolute():
        return bind_run(product_root, requested_path)
    else:
        if any(separator in requested_run for separator in ("/", "\\")):
            raise ValueError("relative Run selector must be a Run id or runNN")
        candidates = []
        for path in _run_directories(product_root):
            match = RUN_PATTERN.fullmatch(path.name)
            assert match is not None
            if requested_run in {path.name, f"run{match.group(3)}"}:
                candidates.append(path)
        if not candidates:
            raise ValueError(f"requested Run does not exist: {requested_run}")
        if len(candidates) != 1:
            raise ValueError(f"requested Run is ambiguous: {requested_run}")
        return bind_run(product_root, candidates[0])


def _create_run(
    product_root: Path, direction: str | None, now: datetime | None
) -> dict[str, Any]:
    timestamp = _normalize_now(now)
    existing = _run_entries(product_root)
    next_number = max((_run_number_value(path) for path in existing), default=0) + 1
    run_number = f"run{next_number:02d}"
    run_id = f"{timestamp:%Y%m%d_%H%M}_{run_number}"
    run_root = product_root / run_id
    if _path_entry_exists(run_root):
        raise FileExistsError(f"Run directory already exists: {run_root}")
    mode = "DIRECTED" if direction is not None else "AUTONOMOUS"
    temporary = product_root / f".{run_id}.{uuid4().hex}.tmp"
    temporary.mkdir()
    try:
        _write_run_files(
            temporary,
            run_id,
            run_number,
            mode,
            direction,
            timestamp.isoformat(timespec="seconds"),
        )
        os.replace(temporary, run_root)
    except BaseException:
        if temporary.is_dir():
            for path in temporary.iterdir():
                if path.is_file():
                    path.unlink()
            temporary.rmdir()
        raise
    return {
        "action": "create",
        "run_id": run_id,
        "run_number": run_number,
        "run_root": str(run_root),
        "status": "ACTIVE",
        "mode": mode,
        "current_version": CURRENT_VERSION,
    }


def _write_run_files(
    run_root: Path,
    run_id: str,
    run_number: str,
    mode: str,
    direction: str | None,
    timestamp: str,
) -> None:
    direction_text = direction or "由主 AI 研究者在文本与工具型 LLM Agent 范围内自主选择。"
    charter = f"""# Run Charter

RUN_ID: {run_id}
RUN_NUMBER: {run_number}
CRL_CONTRACT_VERSION: {CURRENT_CONTRACT_VERSION}
DEFAULT_DOMAIN: {DEFAULT_DOMAIN}
CREATED_AT: {timestamp}
MODE: {mode}
CURRENT_VERSION: {CURRENT_VERSION}

## Research Direction

{direction_text}

## Boundary

- 本 Run 与其他 Run 完全隔离。
- 文本与工具型 LLM Agent 是本 Run 的默认硬边界。
- 主 AI 研究者是科研判断与行动主体。
- 只有准备交付一个研究种子时才启动三个全新、互相独立的文字审查者。
- 定向 Run 不得越出用户方向；方向无价值时产出 No-Go。
"""
    status = f"""# Run Status

RUN_ID: {run_id}
RUN_NUMBER: {run_number}
STATUS: ACTIVE
MODE: {mode}
CURRENT_VERSION: {CURRENT_VERSION}
LAST_DURABLE_ARTIFACT: RUN_LEDGER.md
NEXT_ACTION: 主 AI 研究者自主判断当前最有科研价值的下一步。
UPDATED_AT: {timestamp}
"""
    ledger = f"""# Run Ledger

- EVENT: RUN_CREATED
  AT: {timestamp}
  MODE: {mode}
  VERSION: {CURRENT_VERSION}
"""
    _write_new_utf8(run_root / "RUN_CHARTER.md", charter)
    _write_new_utf8(run_root / "RUN_STATUS.md", status)
    _write_new_utf8(run_root / "RUN_LEDGER.md", ledger)


def _write_new_utf8(path: Path, content: str) -> None:
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    if normalized.startswith("\ufeff"):
        raise ValueError("UTF-8 BOM marker is not allowed")
    with path.open("xb") as handle:
        handle.write((normalized.rstrip() + "\n").encode("utf-8"))
        handle.flush()
        os.fsync(handle.fileno())


def _read_fields(path: Path) -> dict[str, str]:
    content = _read_utf8_lf(path, within=path.parent)
    fields: dict[str, str] = {}
    for line in content.splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip():
            fields[key.strip()] = value.strip()
    return fields


def _read_utf8_lf(path: Path, *, within: Path | None = None) -> str:
    data = _required_file(path, within=within)
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"UTF-8 BOM is not allowed: {path}")
    if b"\r" in data:
        raise ValueError(f"only LF newlines are allowed: {path}")
    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"invalid UTF-8: {path}") from error
    if not content.strip():
        raise ValueError(f"empty Run control file: {path}")
    return content


def _normalize_direction(direction: str | None) -> str | None:
    if direction is None:
        return None
    normalized = direction.replace("\r\n", "\n").replace("\r", "\n")
    if normalized.startswith("\ufeff"):
        raise ValueError("research direction must not start with a BOM marker")
    return normalized if normalized.strip() else None


def _run_directories(product_root: Path) -> list[Path]:
    return sorted(
        path
        for path in product_root.iterdir()
        if RUN_PATTERN.fullmatch(path.name)
        and not _is_reparse_point(path)
        and path.is_dir()
    )


def _run_entries(product_root: Path) -> list[Path]:
    return sorted(
        path for path in product_root.iterdir() if RUN_PATTERN.fullmatch(path.name)
    )


def _run_number(path: Path) -> str:
    match = RUN_PATTERN.fullmatch(path.name)
    if match is None:
        raise ValueError(f"invalid Run directory name: {path.name}")
    return f"run{match.group(3)}"


def _run_number_value(path: Path) -> int:
    match = RUN_PATTERN.fullmatch(path.name)
    if match is None:
        raise ValueError(f"invalid Run directory name: {path.name}")
    return int(match.group(3))


def _normalize_now(value: datetime | None) -> datetime:
    if value is None:
        return datetime.now(SHANGHAI)
    if value.tzinfo is None:
        return value.replace(tzinfo=SHANGHAI)
    return value.astimezone(SHANGHAI)


def _versions_from_name(name: str) -> set[str]:
    return {match.group(1) for match in VERSION_IN_NAME.finditer(name)}


def _run_versions(run_root: Path) -> set[str]:
    versions: set[str] = set()
    for path in run_root.iterdir():
        versions.update(_versions_from_name(path.name))
    return versions


def _assert_no_future_version_files(run_root: Path, current: str) -> None:
    match = VERSION_PATTERN.fullmatch(current)
    if match is None:
        raise ValueError(f"invalid CURRENT_VERSION: {current!r}")
    current_number = int(match.group(1))
    future = sorted(
        version
        for version in _run_versions(run_root)
        if int(VERSION_PATTERN.fullmatch(version).group(1)) > current_number
    )
    if future:
        raise ValueError(
            f"Run has version artifacts newer than CURRENT_VERSION {current}: "
            + ", ".join(future)
        )


def _replace_control_fields(content: str, updates: dict[str, str]) -> str:
    lines = content.splitlines()
    for name, value in updates.items():
        prefix = f"{name}:"
        matches = [index for index, line in enumerate(lines) if line.startswith(prefix)]
        if matches:
            lines[matches[0]] = f"{name}: {value}"
            for index in reversed(matches[1:]):
                del lines[index]
        else:
            lines.append(f"{name}: {value}")
    return "\n".join(lines).rstrip() + "\n"


def _update_status_and_ledger(
    workspace: ResearchWorkspace,
    *,
    status_updates: dict[str, str],
    ledger_entry: str,
) -> None:
    status_path = workspace.assert_write_target(workspace.workspace_path / "RUN_STATUS.md")
    ledger_path = workspace.assert_write_target(workspace.workspace_path / "RUN_LEDGER.md")
    original_status = _read_utf8_lf(
        status_path, within=workspace.workspace_path
    )
    original_ledger = _read_utf8_lf(
        ledger_path, within=workspace.workspace_path
    )
    status_text = _replace_control_fields(original_status, status_updates)
    ledger_text = original_ledger.rstrip() + "\n\n" + ledger_entry.rstrip() + "\n"
    try:
        _atomic_write_text(ledger_path, ledger_text, within=workspace.workspace_path)
        _atomic_write_text(status_path, status_text, within=workspace.workspace_path)
    except BaseException as error:
        rollback_errors = []
        for path, content in (
            (ledger_path, original_ledger),
            (status_path, original_status),
        ):
            try:
                _atomic_write_text(path, content, within=workspace.workspace_path)
            except BaseException as rollback_error:
                rollback_errors.append(f"{path.name}: {rollback_error}")
        if rollback_errors:
            raise OSError(
                "control-file update failed and rollback was incomplete: "
                + "; ".join(rollback_errors)
            ) from error
        raise


def _normalize_note(note: str | None) -> str:
    if note is None:
        return ""
    normalized = note.replace("\r\n", "\n").replace("\r", "\n").strip()
    if "\n" in normalized:
        return " ".join(part.strip() for part in normalized.splitlines() if part.strip())
    return normalized


def _normalize_transition(value: Mapping[str, object]) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ValueError("version transition must be a JSON object")
    fields = set(value)
    missing = _TRANSITION_FIELDS - fields
    unknown = fields - _TRANSITION_FIELDS - _OPTIONAL_TRANSITION_FIELDS
    if missing or unknown:
        raise ValueError(
            "version transition fields do not match schema 1: "
            f"missing={sorted(missing)}, unknown={sorted(unknown)}"
        )
    normalized: dict[str, str] = {}
    for name in sorted(fields):
        item = value[name]
        if not isinstance(item, str) or not item.strip() or "\r" in item:
            raise ValueError(
                f"version transition {name} must be non-empty UTF-8 text with LF newlines"
            )
        normalized[name] = item.strip()
    return normalized


def _render_transition_context(
    current: str,
    next_version: str,
    transition: Mapping[str, str],
) -> str:
    lines = [
        f"# Scientific Continuation {next_version}",
        "",
        f"- FROM_VERSION: `{current}`",
        "",
        "## 当前最佳候选集合",
        "",
        "INCUMBENT_SET: INSUFFICIENT",
        "CHALLENGERS: INSUFFICIENT",
        f"SURVIVING_FRONTIER: {transition['SURVIVING_FRONTIER']}",
        "",
        "## 新增正向证据",
        "",
        "UNAVAILABLE：版本推进本身不产生科学证据。",
        "",
        "## 已失效或被杀范围",
        "",
        "UNAVAILABLE：由主研究者依据可追溯证据更新。",
        "",
        "## 剩余致命不确定性",
        "",
        f"SURVIVING_FRONTIER: {transition['SURVIVING_FRONTIER']}",
        "",
        "## 下一项最高信息量动作",
        "",
        f"NEXT_HIGH_INFORMATION_ACTION: {transition['NEXT_HIGH_INFORMATION_ACTION']}",
        "",
        "## 策略变化",
        "",
        f"CHANGED_COORDINATE: {transition['CHANGED_COORDINATE']}",
    ]
    resource = transition.get("RESOURCE_NEEDED")
    if resource is not None:
        lines.extend(["", "## RESOURCE_NEEDED", "", resource])
    return "\n".join(lines).rstrip() + "\n"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read_transition_file(path: Path) -> dict[str, object]:
    text = _read_utf8_lf(path)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid version transition JSON: {path}") from error
    if not isinstance(value, dict):
        raise ValueError("version transition JSON must be an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        if arguments.action == "advance-version":
            payload = advance_version(
                arguments.product_root,
                arguments.run,
                transition=_read_transition_file(arguments.transition_file),
            )
        elif arguments.action == "pause":
            note = _read_utf8_lf(arguments.note_file) if arguments.note_file else None
            payload = pause_run(arguments.product_root, arguments.run, note=note)
        elif arguments.action == "terminate":
            note = _read_utf8_lf(arguments.note_file) if arguments.note_file else None
            payload = terminate_run(arguments.product_root, arguments.run, note=note)
        else:
            direction = arguments.direction
            if arguments.direction_file is not None:
                direction = _read_utf8_lf(arguments.direction_file)
            payload = start_run(
                arguments.product_root,
                requested_run=arguments.run,
                direction=direction,
            )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"manage_run: {error}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
