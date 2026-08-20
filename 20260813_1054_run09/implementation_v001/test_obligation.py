from __future__ import annotations

from random import Random

from obligation_bench import build_obligation_domains, expected_gate
from obligation_core import (
    ABSTAIN,
    PROCEED,
    Atom,
    EvidenceProbe,
    PlanAction,
    backward_obligations,
    compile_obligations,
    minimum_cost_probe_cover,
    run_compiled_gate,
)
from run_obligation_experiment import _adaptive_gate


def test_backward_propagation_discharges_trusted_effect() -> None:
    commit = PlanAction("commit", (Atom("normalized", "YES"), Atom("safe", "YES")), {})
    prefix = PlanAction(
        "local_normalize",
        (Atom("raw", "VALID"),),
        {"normalized": "YES"},
        trusted_deterministic=True,
    )
    assert backward_obligations((prefix,), commit) == (
        Atom("raw", "VALID"),
        Atom("safe", "YES"),
    )


def test_minimum_cost_cover_uses_joint_probe() -> None:
    atoms = (Atom("a", "1"), Atom("b", "1"))
    probes = (
        EvidenceProbe("a", 2, frozenset({"a"})),
        EvidenceProbe("b", 2, frozenset({"b"})),
        EvidenceProbe("joint", 3, frozenset({"a", "b"})),
    )
    assert tuple(probe.name for probe in minimum_cost_probe_cover(atoms, probes)) == (
        "joint",
    )


def test_pdeo_blocks_all_unseen_faults() -> None:
    for domain in build_obligation_domains():
        compiled = compile_obligations(
            domain.prefix_actions, domain.protected_commit, domain.probes
        )
        for fault in domain.unseen_faults:
            result = run_compiled_gate(
                compiled, fault.observations, expected=expected_gate(fault)
            )
            assert result.selected == ABSTAIN
            assert not result.unsafe_commit


def test_dqbp_commits_on_at_least_one_unseen_fault() -> None:
    unsafe = 0
    for domain in build_obligation_domains():
        for fault in domain.unseen_faults:
            result = _adaptive_gate(
                domain, fault, "dqbp", budget=3, rng=Random(0)
            )
            unsafe += int(result.selected == PROCEED)
    assert unsafe >= 1
