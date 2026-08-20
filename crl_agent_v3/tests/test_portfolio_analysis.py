from __future__ import annotations

from dataclasses import replace

from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
)
from crl_v3.portfolio_analysis import (
    analyze_portfolio,
    jaccard_similarity,
    render_analysis_markdown,
    tokenize_text,
)


def _payload(
    hypothesis_id: str,
    *,
    title: str = "",
    parents: list[str] | None = None,
    descriptor: str = "",
) -> dict[str, object]:
    return {
        "hypothesis_id": hypothesis_id,
        "title": title,
        "parent_ids": parents or [],
        "lineage_note": "测试谱系",
        "problem": title,
        "target_failure": {
            "summary": f"failure {descriptor}" if descriptor else "",
            "card_ids": [],
            "evidence_ids": [],
        },
        "changed_computation": {
            "baseline": title,
            "intervention": title,
            "information_available": title,
            "timing": title,
            "budget_effect": title,
        },
        "mechanism_claim": title,
        "falsifier": title,
        "minimal_killer_experiment": title,
        "nearest_prior_risk": title,
        "alternative_explanations": [title] if title else [],
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


def _portfolio(*payloads: dict[str, object]):
    portfolio = empty_portfolio(
        "20260810_1200_run01", "v001", now="2026-01-01T00:00:00Z"
    )
    for index, payload in enumerate(payloads):
        day = index + 1
        record = create_hypothesis_record(
            payload, now=f"2026-01-{day:02d}T00:00:00Z"
        )
        portfolio = add_hypothesis(
            portfolio, record, now=f"2026-02-{day:02d}T00:00:00Z"
        )
    return portfolio


def test_descriptor_distributions_cross_matrices_and_identical_structures() -> None:
    portfolio = _portfolio(
        _payload("same-a", title="first", descriptor="shared"),
        _payload("same-b", title="second", descriptor="shared"),
        _payload("missing", title="third"),
    )

    report = analyze_portfolio(portfolio)

    problem = report["descriptor_distributions"]["problem_family"]
    assert problem["counts"] == {"(missing)": 1, "shared": 2}
    assert problem["missing_count"] == 1
    matrix = report["cross_matrices"]["problem_family_x_computation_stage"]
    assert matrix["counts"]["shared"]["shared"] == 2
    purpose = report["cross_matrices"]["evaluation_mode_x_claim_purpose"]
    assert purpose["columns"] == ["unknown"]
    assert report["identical_structures"][0]["hypothesis_ids"] == [
        "same-a",
        "same-b",
    ]
    assert "schema 1 does not record claim purpose" in " ".join(
        report["method_notes"]
    )


def test_lineage_depth_branches_isolation_staleness_and_lineage_filter() -> None:
    portfolio = _portfolio(
        _payload("root"),
        _payload("left", parents=["root"]),
        _payload("right", parents=["root"]),
        _payload("leaf", parents=["left"]),
        _payload("isolated"),
    )
    portfolio = replace(portfolio, updated_at_utc="2026-03-10T00:00:00Z")

    report = analyze_portfolio(portfolio, stale_days=30)
    lineage = report["lineage"]
    assert lineage["max_depth"] == 2
    assert lineage["branch_count_by_hypothesis"]["root"] == 2
    assert lineage["isolated_hypothesis_ids"] == ["isolated"]
    assert lineage["stale_hypothesis_ids"] == [
        "isolated",
        "leaf",
        "left",
        "right",
        "root",
    ]

    subtree = analyze_portfolio(portfolio, lineage_roots=["left"])
    assert subtree["selected_hypothesis_ids"] == ["left", "leaf"]
    assert subtree["lineage"]["depth_by_hypothesis"] == {"leaf": 1, "left": 0}


def test_mixed_chinese_english_near_duplicate_and_fully_different() -> None:
    portfolio = _portfolio(
        _payload(
            "mixed-a",
            title="预算约束 Budget aware tool planning 失败恢复",
            descriptor="a",
        ),
        _payload(
            "mixed-b",
            title="预算约束 budget aware tool planning 失败恢复",
            descriptor="b",
        ),
        _payload(
            "different",
            title="Causal evaluator for memory retention",
            descriptor="c",
        ),
    )

    report = analyze_portfolio(portfolio)

    warnings = report["near_duplicates"]["warnings"]
    assert [(item["left_id"], item["right_id"]) for item in warnings] == [
        ("mixed-a", "mixed-b")
    ]
    assert warnings[0]["field_similarities"]["claim"] == 1.0
    assert "does not establish novelty" in report["diagnostic_scope"]


def test_similarity_boundary_and_deterministic_output() -> None:
    assert jaccard_similarity(
        tokenize_text("alpha beta gamma"), tokenize_text("alpha beta delta")
    ) == 0.5
    portfolio = _portfolio(
        _payload("a", title="alpha beta gamma"),
        _payload("b", title="alpha beta delta"),
    )
    at_boundary = analyze_portfolio(portfolio, near_duplicate_threshold=0.5)
    above_boundary = analyze_portfolio(portfolio, near_duplicate_threshold=0.500001)
    assert at_boundary["near_duplicates"]["warning_count"] == 1
    assert above_boundary["near_duplicates"]["warning_count"] == 0
    assert analyze_portfolio(portfolio) == analyze_portfolio(portfolio)
    assert render_analysis_markdown(at_boundary) == render_analysis_markdown(
        at_boundary
    )


def test_empty_and_absent_portfolios_are_explicit_facts() -> None:
    empty = empty_portfolio(
        "20260810_1200_run01", "v001", now="2026-01-01T00:00:00Z"
    )
    empty_report = analyze_portfolio(empty)
    absent_report = analyze_portfolio(
        None, run_id="20260810_1200_run01", version="v001"
    )

    assert empty_report["source"]["portfolio_state"] == "empty"
    assert absent_report["source"]["portfolio_state"] == "absent"
    assert empty_report["selected_record_count"] == 0
    assert absent_report["selected_record_count"] == 0
    assert empty_report["lineage"]["max_depth"] == 0
    assert "Gate" not in render_analysis_markdown(empty_report)


def test_filters_do_not_mutate_records_or_statuses() -> None:
    portfolio = _portfolio(
        _payload("one", title="one", descriptor="family-a"),
        _payload("two", title="two", descriptor="family-b"),
    )
    before = portfolio

    report = analyze_portfolio(
        portfolio,
        statuses=["draft"],
        descriptor_filters={"problem_family": ["family-a"]},
    )

    assert report["selected_hypothesis_ids"] == ["one"]
    assert portfolio == before
    assert [record.status for record in portfolio.hypotheses] == ["draft", "draft"]
