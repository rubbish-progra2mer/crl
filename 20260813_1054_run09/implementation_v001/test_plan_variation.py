from __future__ import annotations

from pathlib import Path

from formal_plan_variation_experiment import (
    build_cases,
    load_heldout_rules,
    run_formal,
)
from obligation_core import compile_obligations
from plan_variation_bench import (
    build_plan_variation_domains,
    validate_plan_variation_domains,
)


RULES = (
    Path(__file__).resolve().parents[1]
    / "experiment_v001"
    / "specs"
    / "pdeo-plan-heldout-rules-v2.json"
)


def test_compiled_obligations_change_with_plan() -> None:
    domains = build_plan_variation_domains()
    validate_plan_variation_domains(domains)
    for domain in domains:
        atom_sets = {
            frozenset(
                compile_obligations(
                    variant.prefix_actions, variant.protected_commit, domain.probes
                ).atoms
            )
            for variant in domain.variants
        }
        assert len(atom_sets) == len(domain.variants)


def test_heldout_suite_has_plan_and_state_variation() -> None:
    rules = load_heldout_rules(RULES)
    cases = build_cases(rules)
    assert len(rules) == 4
    assert sum(len(domain.variants) for domain in rules.values()) == 16
    assert len(cases) >= 150
    assert {case.split for case in cases} == {
        "canonical_safe",
        "obligation_plus_nuisance_faults",
        "paired_obligation_faults",
        "safe_nuisance_variants",
        "single_obligation_faults",
    }


def test_plan_variation_killer_conditions() -> None:
    metrics, _ = run_formal(RULES)
    by_name = {record["name"]: record for record in metrics["records"]}
    assert by_name["pdeo_compiled_obligation_exact_match_rate"]["value"] == 1.0
    assert by_name["pdeo_compiled_probe_set_exact_match_rate"]["value"] == 1.0
    assert (
        by_name["pdeo_unsafe_commit_rate_single_obligation_faults"]["value"]
        == 0.0
    )
    assert (
        by_name["pdeo_valid_commit_recall_safe_nuisance_variants"]["value"]
        == 1.0
    )
    assert (
        by_name["pdeo_mean_plan_probe_cost"]["value"]
        < by_name["static_domain_contract_mean_plan_probe_cost"]["value"]
    )
    assert by_name["pdeo_spec_omission_unsafe_commit_rate"]["value"] == 1.0
