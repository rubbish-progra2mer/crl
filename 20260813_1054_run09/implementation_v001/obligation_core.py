from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Mapping, Sequence


PROCEED = "PROCEED"
ABSTAIN = "ABSTAIN"


@dataclass(frozen=True, order=True, slots=True)
class Atom:
    field: str
    expected: str


@dataclass(frozen=True, slots=True)
class PlanAction:
    name: str
    preconditions: tuple[Atom, ...]
    effects: Mapping[str, str]
    trusted_deterministic: bool = True


@dataclass(frozen=True, slots=True)
class EvidenceProbe:
    name: str
    cost: int
    covers: frozenset[str]


@dataclass(frozen=True, slots=True)
class CompiledObligations:
    atoms: tuple[Atom, ...]
    probes: tuple[EvidenceProbe, ...]
    total_cost: int


@dataclass(frozen=True, slots=True)
class GateResult:
    method: str
    selected: str
    expected: str
    probe_names: tuple[str, ...]
    probe_cost: int

    @property
    def correct(self) -> bool:
        return self.selected == self.expected

    @property
    def unsafe_commit(self) -> bool:
        return self.selected == PROCEED and self.expected != PROCEED


def backward_obligations(
    prefix_actions: Sequence[PlanAction],
    protected_commit: PlanAction,
) -> tuple[Atom, ...]:
    """Compute evidence required at the post-write checkpoint.

    The protected commit is not executed by this function. Trusted deterministic
    prefix actions may establish future atoms; untrusted external actions cannot
    discharge evidence obligations merely through their declared effects.
    """

    required = set(protected_commit.preconditions)
    for action in reversed(prefix_actions):
        transformed: set[Atom] = set()
        for atom in required:
            if atom.field not in action.effects or not action.trusted_deterministic:
                transformed.add(atom)
                continue
            produced = action.effects[atom.field]
            if produced != atom.expected:
                raise ValueError(
                    f"plan action {action.name} establishes {atom.field}={produced}, "
                    f"but downstream requires {atom.expected}"
                )
        transformed.update(action.preconditions)
        required = transformed
    return tuple(sorted(required))


def minimum_cost_probe_cover(
    atoms: Sequence[Atom], probes: Sequence[EvidenceProbe]
) -> tuple[EvidenceProbe, ...]:
    required_fields = {atom.field for atom in atoms}
    if not required_fields:
        return ()

    candidates: list[tuple[tuple[int, int, tuple[str, ...]], tuple[EvidenceProbe, ...]]] = []
    for size in range(1, len(probes) + 1):
        for subset in combinations(probes, size):
            covered: set[str] = set()
            for probe in subset:
                covered.update(probe.covers)
            if required_fields.issubset(covered):
                key = (
                    sum(probe.cost for probe in subset),
                    len(subset),
                    tuple(sorted(probe.name for probe in subset)),
                )
                candidates.append((key, tuple(sorted(subset, key=lambda item: item.name))))
    if not candidates:
        missing = required_fields - set().union(*(probe.covers for probe in probes))
        raise ValueError(f"no probe cover for required fields: {sorted(missing)}")
    return min(candidates, key=lambda item: item[0])[1]


def compile_obligations(
    prefix_actions: Sequence[PlanAction],
    protected_commit: PlanAction,
    probes: Sequence[EvidenceProbe],
) -> CompiledObligations:
    atoms = backward_obligations(prefix_actions, protected_commit)
    selected = minimum_cost_probe_cover(atoms, probes)
    return CompiledObligations(
        atoms=atoms,
        probes=selected,
        total_cost=sum(probe.cost for probe in selected),
    )


def evaluate_atoms(atoms: Sequence[Atom], state: Mapping[str, str]) -> bool:
    return all(state.get(atom.field) == atom.expected for atom in atoms)


def run_compiled_gate(
    compiled: CompiledObligations,
    state: Mapping[str, str],
    *,
    expected: str,
    method: str = "pdeo",
) -> GateResult:
    visible_fields: set[str] = set()
    for probe in compiled.probes:
        visible_fields.update(probe.covers)
    observed = {field: state[field] for field in visible_fields if field in state}
    selected = PROCEED if evaluate_atoms(compiled.atoms, observed) else ABSTAIN
    return GateResult(
        method=method,
        selected=selected,
        expected=expected,
        probe_names=tuple(probe.name for probe in compiled.probes),
        probe_cost=compiled.total_cost,
    )


def run_atom_gate(
    method: str,
    atoms: Sequence[Atom],
    probes: Sequence[EvidenceProbe],
    state: Mapping[str, str],
    *,
    expected: str,
) -> GateResult:
    selected_probes = minimum_cost_probe_cover(atoms, probes) if atoms else ()
    visible_fields: set[str] = set()
    for probe in selected_probes:
        visible_fields.update(probe.covers)
    observed = {field: state[field] for field in visible_fields if field in state}
    selected = PROCEED if evaluate_atoms(atoms, observed) else ABSTAIN
    return GateResult(
        method=method,
        selected=selected,
        expected=expected,
        probe_names=tuple(probe.name for probe in selected_probes),
        probe_cost=sum(probe.cost for probe in selected_probes),
    )
