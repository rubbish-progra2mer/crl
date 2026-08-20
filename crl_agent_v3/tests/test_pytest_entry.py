from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = PROJECT_ROOT.parent


def test_pytest_from_product_root_imports_crl_and_tools_without_pythonpath() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "crl_agent_v3/tests/test_build_knowledge_base.py",
            "--collect-only",
            "-q",
        ],
        cwd=PRODUCT_ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert completed.returncode == 0, completed.stderr
    assert "test_build_corpus_creates_database" in completed.stdout
    assert "ModuleNotFoundError" not in completed.stderr


def test_real_kb_marker_skips_without_explicit_asset_option() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "crl_agent_v3/tests/test_query_knowledge.py",
            "-q",
        ],
        cwd=PRODUCT_ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert completed.returncode == 0, completed.stderr
    assert "4 skipped" in completed.stdout

