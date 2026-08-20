from __future__ import annotations

from random import Random

from dqbp_core import run_episode
from statefault_bench import build_domains, validate_domains


def test_domain_contracts() -> None:
    validate_domains(build_domains())


def test_oracle_is_exact_and_free() -> None:
    for domain in build_domains():
        for branch in domain.branches:
            result = run_episode(
                domain, branch, method="oracle", budget=0, rng=Random(0)
            )
            assert result.success
            assert result.probe_cost == 0


def test_full_readback_identifies_every_branch_decision() -> None:
    for domain in build_domains():
        for branch in domain.branches:
            result = run_episode(
                domain, branch, method="full_readback", budget=0, rng=Random(0)
            )
            assert result.success, (domain.name, branch.name, result)


def test_budget_is_respected_by_budgeted_methods() -> None:
    for domain in build_domains():
        for branch in domain.branches:
            for method in ("fixed_readback", "state_information_gain", "dqbp"):
                result = run_episode(
                    domain, branch, method=method, budget=2, rng=Random(0)
                )
                assert result.probe_cost <= 2
