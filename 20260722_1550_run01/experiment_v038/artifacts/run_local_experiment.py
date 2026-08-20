from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_fact(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": str(path),
        "size_bytes": len(data),
        "sha256": _sha256(data),
    }


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture one local experiment execution.")
    parser.add_argument("--capture-dir", required=True, type=Path)
    parser.add_argument("--cwd", required=True, type=Path)
    parser.add_argument("--input", action="append", default=[], type=Path)
    parser.add_argument("--output", action="append", default=[], type=Path)
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.argv[:1] == ["--"]:
        args.argv = args.argv[1:]
    if not args.argv:
        parser.error("an executable and its arguments are required after --")
    return args


def _reject(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    try:
        args = _parse_args()
        capture_dir = args.capture_dir.resolve()
        cwd = args.cwd.resolve()
        if capture_dir.exists():
            _reject(f"capture directory already exists: {capture_dir}")
        if not cwd.is_dir():
            _reject(f"cwd is not an existing directory: {cwd}")

        inputs = [path.resolve() for path in args.input]
        outputs = [path.resolve() for path in args.output]
        for input_path in inputs:
            if not input_path.is_file():
                _reject(f"input is not an existing file: {input_path}")
        for output_path in outputs:
            if output_path.exists():
                _reject(f"output already exists before execution: {output_path}")

        capture_dir.mkdir(parents=True)
    except ValueError as error:
        print(f"run_local_experiment: {error}", file=sys.stderr)
        return 2

    input_facts = [_file_fact(path) for path in inputs]
    output_facts: list[dict[str, Any]] = [
        {"path": str(path), "before": {"exists": False}} for path in outputs
    ]
    started_at_utc = _utc_now()
    started = time.perf_counter()
    completed = subprocess.run(
        args.argv,
        cwd=cwd,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    duration_seconds = time.perf_counter() - started
    finished_at_utc = _utc_now()

    for output_fact, output_path in zip(output_facts, outputs, strict=True):
        if output_path.exists():
            after = _file_fact(output_path)
            after.pop("path")
            output_fact["after"] = {"exists": True, **after}
        else:
            output_fact["after"] = {"exists": False}

    stdout_path = capture_dir / "stdout.bin"
    stderr_path = capture_dir / "stderr.bin"
    stdout_path.write_bytes(completed.stdout)
    stderr_path.write_bytes(completed.stderr)
    execution = {
        "schema_version": SCHEMA_VERSION,
        "argv": args.argv,
        "cwd": str(cwd),
        "started_at_utc": started_at_utc,
        "finished_at_utc": finished_at_utc,
        "duration_seconds": duration_seconds,
        "exit_code": completed.returncode,
        "runner": {
            "path": str(Path(__file__).resolve()),
            "sha256": _sha256(Path(__file__).read_bytes()),
        },
        "python": {
            "executable": sys.executable,
            "version": platform.python_version(),
        },
        "platform": platform.platform(),
        "inputs": input_facts,
        "outputs": output_facts,
        "stdout": {"size_bytes": len(completed.stdout), "sha256": _sha256(completed.stdout)},
        "stderr": {"size_bytes": len(completed.stderr), "sha256": _sha256(completed.stderr)},
    }
    (capture_dir / "execution.json").write_bytes(
        (json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
