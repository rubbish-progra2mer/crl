"""Mutation-sufficient, causally bound effect-witness compiler.

This module intentionally knows nothing about the benchmark's terminal-state
oracle or concrete fault injector.  It compiles predicates over a read result
that is causally indexed by one operation nonce.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class EffectIntent:
    nonce: str
    target_id: str
    expected_fields: Mapping[str, Any]


@dataclass(frozen=True)
class EffectRecord:
    record_id: str
    current: Mapping[str, Any]


@dataclass(frozen=True)
class Predicate:
    name: str
    check: Callable[[Sequence[EffectRecord]], bool]


@dataclass(frozen=True)
class CompilationResult:
    selected: tuple[Predicate, ...]
    killed_mutants: int
    total_mutants: int

    @property
    def coverage(self) -> float:
        if not self.total_mutants:
            return 1.0
        return self.killed_mutants / self.total_mutants

    def verify(self, records: Sequence[EffectRecord]) -> bool:
        return all(predicate.check(records) for predicate in self.selected)


def _correct_relation(intent: EffectIntent) -> tuple[EffectRecord, ...]:
    return (EffectRecord(intent.target_id, dict(intent.expected_fields)),)


def _abstract_mutants(intent: EffectIntent) -> tuple[tuple[EffectRecord, ...], ...]:
    """Create abstract relation mutants, not benchmark runtime faults."""

    correct = _correct_relation(intent)[0]
    mutants: list[tuple[EffectRecord, ...]] = [
        (),
        (EffectRecord(f"wrong::{intent.target_id}", dict(intent.expected_fields)),),
        (correct, correct),
        (
            correct,
            EffectRecord(f"extra::{intent.target_id}", dict(intent.expected_fields)),
        ),
    ]
    for field, value in sorted(intent.expected_fields.items()):
        changed = dict(intent.expected_fields)
        changed[field] = _different_value(value)
        mutants.append((EffectRecord(intent.target_id, changed),))
    return tuple(mutants)


def _different_value(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    return f"wrong::{value}"


def candidate_predicates(intent: EffectIntent) -> tuple[Predicate, ...]:
    predicates: list[Predicate] = [
        Predicate("exactly_one_effect", lambda rows: len(rows) == 1),
        Predicate(
            "target_identity",
            lambda rows: len(rows) >= 1 and rows[0].record_id == intent.target_id,
        ),
    ]
    for field, expected in sorted(intent.expected_fields.items()):
        predicates.append(
            Predicate(
                f"field_equals::{field}",
                lambda rows, field=field, expected=expected: (
                    len(rows) >= 1 and rows[0].current.get(field) == expected
                ),
            )
        )
    return tuple(predicates)


def compile_witness(intent: EffectIntent) -> CompilationResult:
    """Greedily select a minimal deterministic mutant-killing conjunction."""

    correct = _correct_relation(intent)
    mutants = _abstract_mutants(intent)
    predicates = candidate_predicates(intent)
    viable = [predicate for predicate in predicates if predicate.check(correct)]
    uncovered = set(range(len(mutants)))
    selected: list[Predicate] = []

    while uncovered:
        ranked: list[tuple[int, str, Predicate, set[int]]] = []
        for predicate in viable:
            if predicate in selected:
                continue
            killed = {index for index in uncovered if not predicate.check(mutants[index])}
            ranked.append((len(killed), predicate.name, predicate, killed))
        if not ranked:
            break
        ranked.sort(key=lambda item: (-item[0], item[1]))
        gain, _, predicate, killed = ranked[0]
        if gain == 0:
            break
        selected.append(predicate)
        uncovered.difference_update(killed)

    result = CompilationResult(
        selected=tuple(selected),
        killed_mutants=len(mutants) - len(uncovered),
        total_mutants=len(mutants),
    )
    if uncovered:
        raise ValueError(
            f"effect intent is not witnessable: uncovered abstract mutants={sorted(uncovered)}"
        )
    return result


def weak_positive_witness(intent: EffectIntent, rows: Sequence[EffectRecord]) -> bool:
    """Same read result as the candidate, but only requires one matching row."""

    return any(
        row.record_id == intent.target_id
        and all(row.current.get(key) == value for key, value in intent.expected_fields.items())
        for row in rows
    )


def predicate_names(result: CompilationResult) -> tuple[str, ...]:
    return tuple(predicate.name for predicate in result.selected)


def verify_all(result: CompilationResult, batches: Iterable[Sequence[EffectRecord]]) -> list[bool]:
    return [result.verify(batch) for batch in batches]

