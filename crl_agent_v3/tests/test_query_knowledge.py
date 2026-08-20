from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest


pytestmark = pytest.mark.real_kb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = PROJECT_ROOT.parent
KNOWLEDGE_ROOT = PRODUCT_ROOT / "knowledge_base"
QUERY_TOOL = PROJECT_ROOT / "tools" / "query_knowledge.py"


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(QUERY_TOOL),
            "--knowledge-root",
            str(KNOWLEDGE_ROOT),
            *arguments,
        ],
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_read_only_query_tool_reports_normalized_query_and_locations() -> None:
    database_before = (KNOWLEDGE_ROOT / "knowledge.sqlite").stat()
    completed = _run("passages", "--query", "ReAct tool use", "--limit", "3")
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["original_query"] == "ReAct tool use"
    assert payload["normalized_query"] == '"ReAct" OR "tool" OR "use"'
    assert payload["database_path"].endswith("knowledge.sqlite")
    assert payload["hits"]
    assert {"paper_id", "passage_id", "page_start", "page_end", "rank"} <= set(
        payload["hits"][0]
    )
    database_after = (KNOWLEDGE_ROOT / "knowledge.sqlite").stat()
    assert database_after.st_size == database_before.st_size
    assert database_after.st_mtime_ns == database_before.st_mtime_ns


def test_query_tool_rejects_punctuation_and_keeps_chinese_query() -> None:
    punctuation = _run("passages", "--query", "，。！？")
    assert punctuation.returncode == 2
    assert "punctuation" in punctuation.stderr
    chinese = _run("passages", "--query", "工具调用", "--limit", "1")
    assert chinese.returncode == 0, chinese.stderr
    payload = json.loads(chinese.stdout)
    assert payload["normalized_query"] == '"工具调用"'
    assert payload["english_keyword_hint"]


def test_card_query_returns_existing_score_and_evidence_locations() -> None:
    completed = _run("cards", "--query", "tool use", "--limit", "1")
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    hit = payload["hits"][0]
    assert isinstance(hit["rank"], float)
    assert hit["relative_path"].endswith(".md")
    assert hit["evidence_locations"]
    assert {
        "evidence_id",
        "paper_id",
        "locator",
        "page_start",
        "page_end",
    } <= set(hit["evidence_locations"][0])


def test_paper_query_resolves_current_external_fulltext() -> None:
    completed = _run("paper", "--paper-id", "P001")
    assert completed.returncode == 0, completed.stderr
    paper = json.loads(completed.stdout)["paper"]
    fulltext_path = Path(paper["fulltext_path"])
    assert fulltext_path.parent == KNOWLEDGE_ROOT / "papers"
    assert fulltext_path.is_file()
    assert (
        hashlib.sha256(fulltext_path.read_bytes()).hexdigest()
        == paper["fulltext_sha256"]
    )
    assert paper["fulltext_is_current"] is True
    assert paper["recorded_fulltext_path"] != paper["fulltext_path"]
