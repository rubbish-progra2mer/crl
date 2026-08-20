from __future__ import annotations

from formal_pdeo_experiment import build_systematic_cases, run_formal


def test_systematic_suite_has_all_required_splits() -> None:
    cases = build_systematic_cases()
    splits = {case.split for case in cases}
    assert splits == {
        "known_branches",
        "paired_obligation_and_nuisance_faults",
        "systematic_nuisance_variants",
        "systematic_obligation_faults",
    }
    assert len(cases) >= 100


def test_formal_primary_and_cost_claims_hold_in_fixture() -> None:
    metrics, _ = run_formal()
    by_name = {record["name"]: record for record in metrics["records"]}
    assert (
        by_name[
            "pdeo_unsafe_commit_rate_systematic_obligation_faults"
        ]["value"]
        == 0.0
    )
    assert (
        by_name[
            "pdeo_average_probe_cost_systematic_obligation_faults"
        ]["value"]
        < by_name[
            "tool_local_contract_average_probe_cost_systematic_obligation_faults"
        ]["value"]
    )
