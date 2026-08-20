from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from conftest import make_run


TOOL = Path(__file__).resolve().parents[1] / "tools" / "render_research_context.py"


def test_cli_writes_only_deterministic_stdout(tmp_path: Path) -> None:
    product, run = make_run(tmp_path, status="CONCLUDED_NO_DELIVERY")
    arguments = [
        sys.executable,
        str(TOOL),
        "--product-root",
        str(product),
        "--run-root",
        str(run),
        "--version",
        "v001",
        "--no-include-charter",
        "--no-include-portfolio",
        "--no-include-research-bundle",
        "--no-include-prior-audit",
        "--no-include-falsification",
        "--no-include-experiments",
        "--no-include-markdown",
    ]
    before = {path: path.read_bytes() for path in run.rglob("*") if path.is_file()}

    first = subprocess.run(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    second = subprocess.run(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert first.stdout == second.stdout
    assert b"CRL Research Context View" in first.stdout
    assert first.stderr == b""
    assert {path: path.read_bytes() for path in run.rglob("*") if path.is_file()} == before
