from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from conftest import make_run, record_successful_attempt
from crl_v3.comparison import (
    _build_payload,
    _load_closed_attempt,
    compare_attempts,
    render_comparison_report,
)
from crl_v3.falsification import create_plan
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
    transition_hypothesis,
)
from crl_v3.research_context import (
    APPROX_TOKEN_CHARS,
    PRIORITY_MINIMUM_CHARS,
    approximate_token_count,
    render_research_context,
)
from crl_v3.research_retrieval import ResearchBundle, publish_search_snapshot
from crl_v3.workspace import ResearchWorkspace


def _record(hypothesis_id: str, marker: str):
    return create_hypothesis_record(
        {
            "hypothesis_id": hypothesis_id,
            "title": f"{marker} title",
            "parent_ids": [],
            "lineage_note": f"{marker} lineage",
            "problem": f"{marker} problem",
            "target_failure": {
                "summary": f"{marker} failure",
                "card_ids": [],
                "evidence_ids": [],
            },
            "changed_computation": {
                "baseline": f"{marker} baseline",
                "intervention": f"{marker} intervention",
                "information_available": f"{marker} information",
                "timing": f"{marker} timing",
                "budget_effect": f"{marker} budget",
            },
            "mechanism_claim": f"{marker} claim",
            "falsifier": f"{marker} falsifier",
            "minimal_killer_experiment": f"{marker} killer",
            "nearest_prior_risk": f"{marker} prior",
            "alternative_explanations": [f"{marker} alternative"],
            "descriptors": {
                "problem_family": "agent",
                "computation_stage": "planning",
                "intervention_family": "verification",
                "information_source": "trace",
                "timing_class": "pre-action",
                "budget_class": "fixed",
                "evaluation_mode": "counterexample",
            },
            "literature_refs": [],
        },
        now="2026-08-10T00:00:00Z",
    )


def _portfolio(workspace: ResearchWorkspace) -> None:
    portfolio = empty_portfolio(
        workspace.workspace_path.name,
        workspace.version,
        now="2026-08-10T00:00:00Z",
    )
    portfolio = add_hypothesis(
        portfolio,
        _record("hypothesis-active", "ACTIVE_MARKER"),
        now="2026-08-10T00:00:01Z",
    )
    portfolio = transition_hypothesis(
        portfolio,
        "hypothesis-active",
        "active",
        "explicitly active",
        now="2026-08-10T00:00:02Z",
    )
    portfolio = add_hypothesis(
        portfolio,
        _record("hypothesis-draft", "DRAFT_MARKER"),
        now="2026-08-10T00:00:03Z",
    )
    workspace.write_hypotheses(portfolio, expected_sha256=None, create_only=True)


def _plan(workspace: ResearchWorkspace) -> None:
    create_plan(
        workspace,
        {
            "hypothesis_id": "hypothesis-active",
            "plan_id": "plan-active",
            "claims": [
                {
                    "claim_id": "claim-active",
                    "claim_text": "claim",
                    "scope": "scope",
                    "observable": "observable",
                    "falsifier": "EXPLICIT_COUNTEREVIDENCE_MARKER",
                    "minimum_effect_or_decision_rule": "rule",
                    "alternative_explanations": [],
                    "killer_experiment_id": "experiment-active",
                    "supporting_experiment_ids": [],
                    "status": "proposed",
                    "status_reason": "explicitly proposed",
                }
            ],
            "global_confounders": [],
        },
        now="2026-08-10T00:00:04Z",
    )


def _bundle(run_id: str) -> ResearchBundle:
    return ResearchBundle(
        request={
            "schema_version": 1,
            "bundle_kind": "run_local_non_authoritative_research_retrieval",
            "input_mode": "explicit",
            "input_identity": {"run_id": run_id, "version": "v001"},
            "queries": [],
            "limits": {"card_per_route": 1, "passage_hybrid": 1},
            "knowledge_identity": {},
            "code_identity": {},
        },
        result={
            "schema_version": 1,
            "bundle_kind": "run_local_non_authoritative_research_retrieval",
            "queries": [
                {
                    "query_id": "q001",
                    "purpose": "problem",
                    "original_query": "agent",
                    "normalized_query": "agent",
                    "routes": [
                        {
                            "route": "paper_card_fts",
                            "degraded": False,
                            "degradation_reason": None,
                            "hits": [],
                        },
                        {
                            "route": "passage_hybrid",
                            "degraded": False,
                            "degradation_reason": None,
                            "hits": [],
                        },
                    ],
                }
            ],
            "diagnostics": {
                "unique_card_ids": [],
                "unique_evidence_ids": [],
                "unique_passage_ids": [],
                "paper_route_hits": [],
            },
        },
    )


def _clone_attempt_without_metrics(run: Path) -> None:
    source = run / "experiment_v001" / "attempts" / "candidate-failed-fixture"
    target = run / "experiment_v001" / "attempts" / "baseline-failed-fixture"
    shutil.copytree(source, target)
    execution_path = target / "execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))

    def replace_paths(value: object) -> object:
        if isinstance(value, str):
            return value.replace(str(source.resolve()), str(target.resolve())).replace(
                source.relative_to(run).as_posix(), target.relative_to(run).as_posix()
            )
        if isinstance(value, list):
            return [replace_paths(item) for item in value]
        if isinstance(value, dict):
            return {name: replace_paths(item) for name, item in value.items()}
        return value

    execution = replace_paths(execution)
    assert isinstance(execution, dict)
    execution["attempt_id"] = target.name
    execution["command_exit_code"] = 1
    execution["runner_exit_code"] = 1
    execution["metrics_contract_ok"] = False
    execution["metrics"]["snapshot"] = None
    execution["metrics"]["validation_errors"] = ["metrics output is missing"]
    (target / "metrics.json").unlink()
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def test_budget_is_deterministic_fair_and_discloses_every_omission(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    _portfolio(workspace)
    _plan(workspace)
    workspace.write_memory("M" * 12000)

    budget = 6000
    first = render_research_context(
        workspace,
        max_characters=budget,
        include_research_bundle=False,
        include_prior_audit=False,
        include_experiments=False,
    )
    second = render_research_context(
        workspace,
        max_characters=budget,
        include_research_bundle=False,
        include_prior_audit=False,
        include_experiments=False,
    )

    assert first == second
    text = first.decode("utf-8")
    assert len(text) <= budget
    assert "PRIORITY: `active-candidate`" in text
    assert "PRIORITY: `explicit-falsification`" in text
    assert f"INCLUDED_CHARACTERS: `{PRIORITY_MINIMUM_CHARS}/" in text
    assert "memory_v001.md" in text
    assert "OMITTED_CHARACTERS=" in text
    assert "不读取或使用分数" in text

    token_view = render_research_context(
        workspace,
        max_approx_tokens=1600,
        include_research_bundle=False,
        include_prior_audit=False,
        include_experiments=False,
    ).decode("utf-8")
    assert len(token_view) <= 1600 * APPROX_TOKEN_CHARS
    assert approximate_token_count(token_view) <= 1600


def test_all_authority_classes_and_attempt_comparison_facts_are_rendered(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    publish_search_snapshot(
        workspace,
        "search-001",
        _bundle(run.name),
        now="2026-08-10T00:01:00Z",
    )
    source = run / "inputs" / "input.txt"
    source.parent.mkdir()
    source.write_bytes(b"input\n")
    first = record_successful_attempt(
        product, run, "v001", source, attempt_id="candidate-001"
    )
    second = record_successful_attempt(
        product, run, "v001", source, attempt_id="baseline-001"
    )
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    compare_attempts(workspace, "comparison-001", "candidate-001", ["baseline-001"])

    rendered = render_research_context(workspace).decode("utf-8")

    for authority in (
        "EXTERNAL_EVIDENCE",
        "CARD_SYNTHESIS",
        "RUN_HYPOTHESIS",
        "RUN_EXPERIMENT_FACT",
        "RESEARCHER_INTERPRETATION",
    ):
        assert f"AUTHORITY_CLASS: `{authority}`" in rendered
    assert "attempt:candidate-001:metrics" in rendered
    assert "comparison:comparison-001" in rendered
    assert "SOURCE_PATH:" in rendered
    assert "SOURCE_SHA256:" in rendered


def test_historical_schema_1_comparison_remains_readable(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    source = run / "workbench_v001" / "source.py"
    source.parent.mkdir()
    source.write_bytes(b"print('fixture')\n")
    for attempt_id in ("candidate-legacy", "baseline-legacy"):
        completed = record_successful_attempt(
            product, run, "v001", source, attempt_id=attempt_id
        )
        assert completed.returncode == 0, completed.stderr
    workspace = ResearchWorkspace(run, product_root=product)
    candidate = _load_closed_attempt(workspace, "candidate-legacy")
    baseline = _load_closed_attempt(workspace, "baseline-legacy")
    payload = _build_payload(
        workspace,
        "comparison-legacy",
        candidate,
        (baseline,),
        schema_version=1,
    )
    destination = run / "experiment_v001/comparisons/comparison-legacy"
    destination.mkdir(parents=True)
    (destination / "comparison.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (destination / "report.md").write_text(
        render_comparison_report(payload), encoding="utf-8", newline="\n"
    )

    rendered = render_research_context(workspace).decode("utf-8")

    assert "comparison:comparison-legacy" in rendered
    assert '"schema_version": 1' in rendered


def test_tampered_bundle_is_rejected_and_closed_run_remains_read_only(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    publication = publish_search_snapshot(
        workspace,
        "search-001",
        _bundle(run.name),
        now="2026-08-10T00:01:00Z",
    )
    before = {path: path.read_bytes() for path in run.rglob("*") if path.is_file()}
    status = (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    (run / "RUN_STATUS.md").write_text(
        status.replace("STATUS: ACTIVE", "STATUS: DELIVERED"),
        encoding="utf-8",
        newline="\n",
    )
    closed_before = {path: path.read_bytes() for path in run.rglob("*") if path.is_file()}
    closed_workspace = ResearchWorkspace(run, product_root=product)
    assert render_research_context(closed_workspace)
    assert {path: path.read_bytes() for path in run.rglob("*") if path.is_file()} == closed_before

    result = Path(publication.path) / "result.json"
    result.write_bytes(result.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="snapshot"):
        render_research_context(closed_workspace)
    assert before[result] != result.read_bytes()


def test_failed_attempt_without_metrics_comparison_is_readable_but_tamper_is_not(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    source = run / "workbench_v001" / "source.py"
    source.parent.mkdir()
    source.write_bytes(b"print('fixture')\n")
    completed = record_successful_attempt(
        product,
        run,
        "v001",
        source,
        attempt_id="candidate-failed-fixture",
    )
    assert completed.returncode == 0, completed.stderr
    _clone_attempt_without_metrics(run)
    workspace = ResearchWorkspace(run, product_root=product)
    publication = compare_attempts(
        workspace,
        "comparison-metrics-unavailable",
        "candidate-failed-fixture",
        ["baseline-failed-fixture"],
    )

    rendered = render_research_context(workspace).decode("utf-8")
    assert "comparison:comparison-metrics-unavailable" in rendered
    assert "metrics output is missing" in rendered
    assert "attempt:baseline-failed-fixture:execution" in rendered

    comparison_path = Path(publication.path) / "comparison.json"
    comparison_bytes = comparison_path.read_bytes()
    comparison_path.write_bytes(comparison_bytes.replace(b'"failed_attempts": 1', b'"failed_attempts": 0', 1))
    with pytest.raises(ValueError, match="comparison"):
        render_research_context(workspace)
    comparison_path.write_bytes(comparison_bytes)

    candidate_metrics = (
        run
        / "experiment_v001"
        / "attempts"
        / "candidate-failed-fixture"
        / "metrics.json"
    )
    candidate_metrics.write_bytes(candidate_metrics.read_bytes() + b" \n")
    with pytest.raises(ValueError, match="SHA-256"):
        render_research_context(workspace)


def test_empty_materials_cross_run_and_noncurrent_version_are_rejected(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    before = {path: path.read_bytes() for path in run.iterdir() if path.is_file()}
    rendered = render_research_context(
        workspace,
        include_charter=False,
        include_portfolio=False,
        include_research_bundle=False,
        include_prior_audit=False,
        include_falsification=False,
        include_experiments=False,
        include_markdown=False,
    ).decode("utf-8")
    assert "（无已纳入片段）" in rendered
    assert "（无省略内容）" in rendered
    assert {path: path.read_bytes() for path in run.iterdir() if path.is_file()} == before

    other_product = tmp_path / "other-product"
    other_product.mkdir()
    with pytest.raises(ValueError, match="direct child"):
        ResearchWorkspace(run, product_root=other_product)

    status = (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    (run / "RUN_STATUS.md").write_text(
        status.replace("CURRENT_VERSION: v001", "CURRENT_VERSION: v002"),
        encoding="utf-8",
        newline="\n",
    )
    stale = ResearchWorkspace(run, product_root=product, version="v001")
    with pytest.raises(ValueError, match="CURRENT_VERSION v002"):
        render_research_context(stale)
