from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import log2
from random import Random
from typing import Iterable, Mapping, Sequence


ABSTAIN = "ABSTAIN"


@dataclass(frozen=True, slots=True)
class Branch:
    """One documented-or-fault-template post-state hypothesis."""

    name: str
    decision: str
    observations: Mapping[str, str]
    prior: float


@dataclass(frozen=True, slots=True)
class Probe:
    """A read-only tool call available after an ambiguous write."""

    name: str
    cost: int


@dataclass(frozen=True, slots=True)
class Domain:
    name: str
    branches: tuple[Branch, ...]
    probes: tuple[Probe, ...]
    fixed_probe: str


@dataclass(frozen=True, slots=True)
class EpisodeResult:
    method: str
    true_branch: str
    true_decision: str
    selected_decision: str
    success: bool
    harmful_error: bool
    abstained: bool
    probe_cost: int
    probes: tuple[str, ...]
    candidate_count: int


def _normalize(weights: Mapping[str, float]) -> dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("posterior has no positive mass")
    return {key: value / total for key, value in weights.items() if value > 0}


def _entropy(weights: Iterable[float]) -> float:
    return -sum(value * log2(value) for value in weights if value > 0)


def _decision_error(
    posterior: Mapping[str, float], branch_by_name: Mapping[str, Branch]
) -> float:
    mass: dict[str, float] = defaultdict(float)
    for name, probability in posterior.items():
        mass[branch_by_name[name].decision] += probability
    return 1.0 - max(mass.values())


def _posterior_after_observation(
    posterior: Mapping[str, float],
    branch_by_name: Mapping[str, Branch],
    probe_name: str,
    observation: str,
) -> dict[str, float]:
    retained = {
        name: probability
        for name, probability in posterior.items()
        if branch_by_name[name].observations[probe_name] == observation
    }
    if not retained:
        return {}
    return _normalize(retained)


def _observation_groups(
    posterior: Mapping[str, float],
    branch_by_name: Mapping[str, Branch],
    probe_name: str,
) -> dict[str, dict[str, float]]:
    groups: dict[str, dict[str, float]] = defaultdict(dict)
    for name, probability in posterior.items():
        value = branch_by_name[name].observations[probe_name]
        groups[value][name] = probability
    return dict(groups)


def _expected_state_entropy(
    posterior: Mapping[str, float],
    branch_by_name: Mapping[str, Branch],
    probe_name: str,
) -> float:
    expected = 0.0
    for members in _observation_groups(posterior, branch_by_name, probe_name).values():
        mass = sum(members.values())
        conditional = (value / mass for value in members.values())
        expected += mass * _entropy(conditional)
    return expected


def _expected_decision_error(
    posterior: Mapping[str, float],
    branch_by_name: Mapping[str, Branch],
    probe_name: str,
) -> float:
    expected = 0.0
    for members in _observation_groups(posterior, branch_by_name, probe_name).values():
        mass = sum(members.values())
        conditional = _normalize(members)
        expected += mass * _decision_error(conditional, branch_by_name)
    return expected


def _select_probe(
    method: str,
    posterior: Mapping[str, float],
    branch_by_name: Mapping[str, Branch],
    probes: Sequence[Probe],
    used: set[str],
    remaining_budget: int,
) -> Probe | None:
    candidates = [
        probe
        for probe in probes
        if probe.name not in used and probe.cost <= remaining_budget
    ]
    if not candidates:
        return None

    if method == "dqbp":
        current = _decision_error(posterior, branch_by_name)
        utility = {
            probe.name: (
                current
                - _expected_decision_error(
                    posterior, branch_by_name, probe.name
                )
            )
            / probe.cost
            for probe in candidates
        }
    elif method == "state_information_gain":
        current = _entropy(posterior.values())
        utility = {
            probe.name: (
                current
                - _expected_state_entropy(
                    posterior, branch_by_name, probe.name
                )
            )
            / probe.cost
            for probe in candidates
        }
    else:
        raise ValueError(f"unsupported adaptive method: {method}")

    best = max(
        candidates,
        key=lambda probe: (utility[probe.name], -probe.cost, probe.name),
    )
    if utility[best.name] <= 1e-12:
        return None
    return best


def _aggregate_decision(
    posterior: Mapping[str, float], branch_by_name: Mapping[str, Branch]
) -> str:
    if not posterior:
        return ABSTAIN
    mass: dict[str, float] = defaultdict(float)
    for name, probability in posterior.items():
        mass[branch_by_name[name].decision] += probability
    best_value = max(mass.values())
    winners = [
        decision for decision, probability in mass.items() if abs(probability - best_value) < 1e-12
    ]
    return winners[0] if len(winners) == 1 else ABSTAIN


def run_episode(
    domain: Domain,
    true_branch: Branch,
    *,
    method: str,
    budget: int,
    rng: Random,
) -> EpisodeResult:
    del rng  # Reserved for a future randomized baseline; current methods are deterministic.
    branch_by_name = {branch.name: branch for branch in domain.branches}
    posterior = _normalize({branch.name: branch.prior for branch in domain.branches})
    probe_by_name = {probe.name: probe for probe in domain.probes}
    used: set[str] = set()
    trace: list[str] = []
    spent = 0

    if method in {"no_verification", "static_contract"}:
        pass
    elif method == "fixed_readback":
        probe = probe_by_name[domain.fixed_probe]
        if probe.cost <= budget:
            observed = true_branch.observations[probe.name]
            posterior = _posterior_after_observation(
                posterior, branch_by_name, probe.name, observed
            )
            trace.append(probe.name)
            spent += probe.cost
    elif method == "full_readback":
        for probe in sorted(domain.probes, key=lambda item: (item.cost, item.name)):
            observed = true_branch.observations[probe.name]
            posterior = _posterior_after_observation(
                posterior, branch_by_name, probe.name, observed
            )
            trace.append(probe.name)
            spent += probe.cost
            if len(posterior) <= 1:
                break
    elif method in {"dqbp", "state_information_gain"}:
        while spent < budget and posterior:
            if _decision_error(posterior, branch_by_name) <= 1e-12:
                break
            probe = _select_probe(
                method,
                posterior,
                branch_by_name,
                domain.probes,
                used,
                budget - spent,
            )
            if probe is None:
                break
            observed = true_branch.observations[probe.name]
            posterior = _posterior_after_observation(
                posterior, branch_by_name, probe.name, observed
            )
            used.add(probe.name)
            trace.append(probe.name)
            spent += probe.cost
    elif method == "oracle":
        posterior = {true_branch.name: 1.0}
    else:
        raise ValueError(f"unsupported method: {method}")

    selected = _aggregate_decision(posterior, branch_by_name)
    success = selected == true_branch.decision
    abstained = selected == ABSTAIN
    harmful_error = not success and not abstained
    return EpisodeResult(
        method=method,
        true_branch=true_branch.name,
        true_decision=true_branch.decision,
        selected_decision=selected,
        success=success,
        harmful_error=harmful_error,
        abstained=abstained,
        probe_cost=spent,
        probes=tuple(trace),
        candidate_count=len(posterior),
    )


def sample_branch(
    domain: Domain,
    rng: Random,
    *,
    condition: str,
) -> Branch:
    if condition not in {"in_distribution", "failure_heavy", "success_heavy"}:
        raise ValueError(f"unsupported sampling condition: {condition}")
    weights = []
    for branch in domain.branches:
        weight = branch.prior
        if condition == "failure_heavy" and branch.decision != "PROCEED":
            weight *= 2.5
        if condition == "success_heavy" and branch.decision == "PROCEED":
            weight *= 2.5
        weights.append(weight)
    return rng.choices(domain.branches, weights=weights, k=1)[0]
