from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from conftest import make_run
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
)
from crl_v3.workspace import ResearchWorkspace


TOOL = Path(__file__).resolve().parents[1] / "tools" / "analyze_hypotheses.py"


def _payload(hypothesis_id: str, descriptor: str) -> dict[str, object]:
    text = f"中文 English {hypothesis_id}"
    return {
        "hypothesis_id": hypothesis_id,
        "title": text,
        "parent_ids": [],
        "lineage_note": "根候选",
        "problem": text,
        "target_failure": {"summary": text, "card_ids": [], "evidence_ids": []},
        "changed_computation": {
            "baseline": text,
            "intervention": text,
            "information_available": text,
            "timing": text,
            "budget_effect": text,
        },
        "mechanism_claim": text,
        "falsifier": text,
        "minimal_killer_experiment": text,
        "nearest_prior_risk": text,
        "alternative_explanations": [text],
        "descriptors": {
            "problem_family": descriptor,
            "computation_stage": descriptor,
            "intervention_family": descriptor,
            "information_source": descriptor,
            "timing_class": descriptor,
            "budget_class": descriptor,
            "evaluation_mode": descriptor,
        },
        "literature_refs": [],
    }


def _run(product: Path, run: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--version",
            "v001",
            *arguments,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _write_portfolio(product: Path, run: Path) -> bytes:
    workspace = ResearchWorkspace(run, product_root=product, version="v001")
    portfolio = empty_portfolio(run.name, "v001", now="2026-01-01T00:00:00Z")
    for hypothesis_id, descriptor in (("h-one", "family-a"), ("h-two", "family-b")):
        portfolio = add_hypothesis(
            portfolio,
            create_hypothesis_record(
                _payload(hypothesis_id, descriptor), now="2026-01-01T00:00:00Z"
            ),
            now="2026-02-01T00:00:00Z",
        )
    workspace.write_hypotheses(
        portfolio, expected_sha256=None, create_only=True
    )
    return workspace.hypotheses_path.read_bytes()


def test_cli_json_markdown_filters_and_no_status_mutation(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    before = _write_portfolio(product, run)

    first = _run(
        product,
        run,
        "--descriptor",
        "problem_family=family-a",
        "--status",
        "draft",
    )
    second = _run(
        product,
        run,
        "--descriptor",
        "problem_family=family-a",
        "--status",
        "draft",
    )
    assert first.returncode == second.returncode == 0, first.stderr.decode("utf-8")
    assert first.stdout == second.stdout
    report = json.loads(first.stdout)
    assert report["selected_hypothesis_ids"] == ["h-one"]

    markdown = _run(product, run, "--format", "markdown")
    assert markdown.returncode == 0, markdown.stderr.decode("utf-8")
    assert "假设组合结构诊断" in markdown.stdout.decode("utf-8")
    assert (run / "hypotheses_v001" / "portfolio.json").read_bytes() == before


def test_cli_optional_save_is_fixed_utf8_lf_and_never_overwrites(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    _write_portfolio(product, run)

    saved = _run(product, run, "--save", "analysis-001")
    assert saved.returncode == 0, saved.stderr.decode("utf-8")
    report = json.loads(saved.stdout)
    directory = run / "hypotheses_v001" / "analysis" / "analysis-001"
    assert report["saved_path"] == "hypotheses_v001/analysis/analysis-001"
    assert json.loads((directory / "analysis.json").read_bytes()) == report
    for path in (directory / "analysis.json", directory / "analysis.md"):
        data = path.read_bytes()
        assert not data.startswith(b"\xef\xbb\xbf")
        assert b"\r" not in data

    before = {path.name: path.read_bytes() for path in directory.iterdir()}
    rejected = _run(product, run, "--save", "analysis-001")
    assert rejected.returncode == 1
    assert b"already exists" in rejected.stderr
    assert {path.name: path.read_bytes() for path in directory.iterdir()} == before


def test_cli_legacy_missing_and_empty_portfolios_are_successful_facts(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path / "legacy")
    legacy = _run(product, run)
    assert legacy.returncode == 0, legacy.stderr.decode("utf-8")
    assert json.loads(legacy.stdout)["source"]["portfolio_state"] == "absent"

    product_empty, run_empty = make_run(tmp_path / "empty")
    workspace = ResearchWorkspace(run_empty, product_root=product_empty, version="v001")
    workspace.write_hypotheses(
        empty_portfolio(run_empty.name, "v001"),
        expected_sha256=None,
        create_only=True,
    )
    empty = _run(product_empty, run_empty)
    assert empty.returncode == 0, empty.stderr.decode("utf-8")
    assert json.loads(empty.stdout)["source"]["portfolio_state"] == "empty"

