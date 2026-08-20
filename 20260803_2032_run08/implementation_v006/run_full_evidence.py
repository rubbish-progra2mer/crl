#!/usr/bin/env python3
"""v006 正式证据入口：上游测试、合同面板和 ToolSandbox 面板。"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from run_contract_panel import run_panel as run_contract_panel
from run_exhaustive_audit import run_audit as run_exhaustive_audit
from run_toolsandbox_panel import run_panel as run_toolsandbox_panel


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    arguments = parser.parse_args()
    output_dir = Path(arguments.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    pytest_command = [
        sys.executable,
        "-B",
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        str(ROOT / "upstream_evidence" / "tests"),
        str(ROOT / "tests"),
    ]
    pytest_result = subprocess.run(
        pytest_command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
        check=False,
    )
    pytest_text = (
        "$ " + " ".join(pytest_command) + "\n"
        + pytest_result.stdout
        + pytest_result.stderr
    )
    (output_dir / "pytest.txt").write_text(
        pytest_text, encoding="utf-8", newline="\n"
    )
    if pytest_result.returncode != 0:
        raise RuntimeError(
            f"测试失败，退出码 {pytest_result.returncode}；见 pytest.txt"
        )

    contract_summary = run_contract_panel(output_dir)
    exhaustive_summary = run_exhaustive_audit(
        output_dir / "exhaustive_audit.json"
    )
    toolsandbox_summary = run_toolsandbox_panel(output_dir)

    evidence_files = sorted(
        path
        for path in output_dir.iterdir()
        if path.is_file() and path.name != "evidence_summary.json"
    )
    manifest = {
        path.name: {
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
        }
        for path in evidence_files
    }
    summary = {
        "schema_version": 1,
        "python": sys.version,
        "pytest_return_code": pytest_result.returncode,
        "contract_panel": contract_summary,
        "exhaustive_audit": exhaustive_summary,
        "toolsandbox_panel": toolsandbox_summary,
        "outputs": manifest,
    }
    (output_dir / "evidence_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
