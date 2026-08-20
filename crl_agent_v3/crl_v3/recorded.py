from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from typing import Sequence

from .decision import child_process_environment, environment_secrets, redact_secrets
from .workspace import ResearchWorkspace, _is_reparse_point, _publish_once, safe_relative_path


_RECORD_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,63}")
_IMPLEMENTATION_EXCLUDES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def implementation_manifest(workspace: ResearchWorkspace) -> dict[str, object]:
    root = workspace.implementation_path
    files = []
    if root.is_dir():
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            if any(part in _IMPLEMENTATION_EXCLUDES for part in path.parts):
                continue
            safe = workspace.assert_read_target(path)
            data = safe.read_bytes()
            files.append(
                {
                    "path": safe.relative_to(workspace.workspace_path).as_posix(),
                    "size_bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
    manifest = {
        "schema_version": 1,
        "run_id": workspace.workspace_path.name,
        "version": workspace.version,
        "files": files,
    }
    return manifest


def implementation_key(manifest: dict[str, object]) -> str:
    return hashlib.sha256(_json_bytes(manifest)).hexdigest()


def run_recorded(
    workspace: ResearchWorkspace,
    record_id: str,
    command: Sequence[str],
    *,
    cwd: str | Path | None = None,
    timeout_seconds: float | None = None,
    inputs: Sequence[str | Path] = (),
    outputs: Sequence[str | Path] = (),
    allow_sensitive_environment: Sequence[str] = (),
) -> dict[str, object]:
    workspace.assert_run_writable()
    identifier = _record_id(record_id)
    argv = [str(item) for item in command]
    if not argv or any(not item for item in argv):
        raise ValueError("recorded command must be a non-empty string array")
    if timeout_seconds is not None and timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    secrets = environment_secrets()
    auxiliary_environment, _ = child_process_environment()
    research_environment, sensitive_environment_passthrough = (
        child_process_environment(allow_sensitive_environment)
    )
    working = _working_directory(workspace, cwd)
    input_facts = [_existing_file_fact(workspace, path) for path in inputs]
    output_paths = [_output_path(workspace, path) for path in outputs]
    manifest = implementation_manifest(workspace)
    key = implementation_key(manifest)
    root = workspace.assert_write_target(
        workspace.experiment_path / "recorded" / identifier
    )
    if root.exists():
        raise FileExistsError(f"recorded experiment already exists: {identifier}")
    root.mkdir(parents=True)
    started = _utc_now()
    _publish_once(
        root / "started.json",
        _json_bytes(
            {
                "schema_version": 1,
                "record_id": identifier,
                "run_id": workspace.workspace_path.name,
                "version": workspace.version,
                "started_at_utc": started,
                "argv": argv,
            }
        ),
        within=workspace.workspace_path,
    )
    before = monotonic()
    status = "FAILED"
    returncode: int | None = None
    timed_out = False
    error: str | None = None
    stdout = b""
    stderr = b""
    try:
        completed = subprocess.run(
            argv,
            cwd=working,
            env=research_environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
        stdout = completed.stdout
        stderr = completed.stderr
        returncode = completed.returncode
        status = "SUCCESS" if returncode == 0 else "FAILED"
    except subprocess.TimeoutExpired as caught:
        stdout = caught.stdout or b""
        stderr = caught.stderr or b""
        timed_out = True
        status = "TIMEOUT"
        error = str(caught)
    except (OSError, ValueError) as caught:
        error = str(caught)
        status = "LAUNCH_ERROR"
    duration = monotonic() - before
    redacted_stdout = redact_secrets(stdout, secrets)
    redacted_stderr = redact_secrets(stderr, secrets)
    _write_binary_once(root / "stdout.bin", redacted_stdout)
    _write_binary_once(root / "stderr.bin", redacted_stderr)
    output_facts = [
        _optional_file_fact(workspace, path) for path in output_paths
    ]
    record = {
        "schema_version": 1,
        "tier": "RECORDED_NON_SUPPORTING",
        "record_id": identifier,
        "run_id": workspace.workspace_path.name,
        "version": workspace.version,
        "status": status,
        "started_at_utc": started,
        "finished_at_utc": _utc_now(),
        "duration_seconds": duration,
        "argv": argv,
        "cwd": str(working),
        "returncode": returncode,
        "timed_out": timed_out,
        "timeout_seconds": timeout_seconds,
        "error": error,
        "capture": {
            "stdout": _binary_fact(root / "stdout.bin"),
            "stderr": _binary_fact(root / "stderr.bin"),
            "redaction_applied": redacted_stdout != stdout or redacted_stderr != stderr,
        },
        "inputs": input_facts,
        "outputs": output_facts,
        "implementation_key": key,
        "implementation_manifest": manifest,
        "environment": {
            "sensitive_environment_passthrough": list(
                sensitive_environment_passthrough
            ),
            "platform": platform.platform(),
            "python": platform.python_version(),
            "executable": sys.executable,
            "git": _git_facts(
                workspace.product_root, environment=auxiliary_environment
            ),
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "unavailable"),
        },
    }
    _publish_once(root / "record.json", _json_bytes(record), within=workspace.workspace_path)
    return record


def read_recorded(workspace: ResearchWorkspace, record_id: str) -> dict[str, object]:
    identifier = _record_id(record_id)
    path = workspace.assert_read_target(
        workspace.experiment_path / "recorded" / identifier / "record.json"
    )
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("record_id") != identifier:
        raise ValueError("recorded experiment identity is invalid")
    return value


def _working_directory(workspace: ResearchWorkspace, value: str | Path | None) -> Path:
    if value is None:
        path = workspace.workbench_path
        path.mkdir(parents=True, exist_ok=True)
    else:
        candidate = Path(value)
        path = candidate if candidate.is_absolute() else workspace.workspace_path / safe_relative_path(candidate)
    resolved = path.resolve(strict=True)
    if not resolved.is_dir() or not resolved.is_relative_to(workspace.workspace_path):
        raise ValueError("recorded cwd must be an existing Run-local directory")
    return resolved


def _output_path(workspace: ResearchWorkspace, value: str | Path) -> Path:
    path = Path(value)
    candidate = path if path.is_absolute() else workspace.workspace_path / safe_relative_path(path)
    target = workspace.assert_write_target(candidate)
    if not target.resolve(strict=False).is_relative_to(workspace.workspace_path):
        raise ValueError("recorded output must be Run-local")
    return target


def _existing_file_fact(workspace: ResearchWorkspace, value: str | Path) -> dict[str, object]:
    path = Path(value)
    candidate = path if path.is_absolute() else workspace.workspace_path / safe_relative_path(path)
    safe = workspace.assert_read_target(candidate)
    if not safe.is_file():
        raise ValueError(f"recorded input is not a file: {safe}")
    return _binary_fact(safe)


def _optional_file_fact(workspace: ResearchWorkspace, path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"path": str(path), "exists": False, "size_bytes": None, "sha256": None}
    safe = workspace.assert_read_target(path)
    return {"exists": True, **_binary_fact(safe)}


def _binary_fact(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": str(path), "size_bytes": path.stat().st_size, "sha256": digest}


def _write_binary_once(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _git_facts(
    root: Path, *, environment: dict[str, str] | None = None
) -> dict[str, object]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {"status": "unavailable", "commit": None}
    commit = completed.stdout.decode("ascii", errors="ignore").strip()
    if completed.returncode != 0 or re.fullmatch(r"[0-9a-f]{40,64}", commit) is None:
        return {"status": "unavailable", "commit": None}
    return {"status": "available", "commit": commit}


def _record_id(value: str) -> str:
    if not isinstance(value, str) or _RECORD_ID.fullmatch(value) is None:
        raise ValueError("record id must be 3-64 lowercase safe characters")
    return value


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
