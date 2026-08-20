"""Mutation-audited compiler for snapshot-bound effect witnesses.

The compiler sees abstract effect traces and an observation capability.  It
does not import the benchmark's concrete fault injector or terminal oracle.
For every harmful abstract mutant it must select at least one observable
feature that distinguishes that mutant from the canonical correct trace.  If
that is impossible, compilation fails closed and returns the indistinguishable
counterexamples.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class EffectSpec:
    nonce: str
    operation: str
    target_id: str
    schema_fields: tuple[str, ...]
    allowed_updates: Mapping[str, Any]
    before: Mapping[str, Any] | None

    def desired(self) -> dict[str, Any] | None:
        if self.operation == "delete":
            return None
        if self.operation == "create":
            return dict(self.allowed_updates)
        if self.operation != "update" or self.before is None:
            raise ValueError(f"invalid effect specification: {self.operation}")
        result = dict(self.before)
        result.update(self.allowed_updates)
        return result

    @property
    def frame_fields(self) -> tuple[str, ...]:
        return tuple(sorted(set(self.schema_fields) - set(self.allowed_updates)))


@dataclass(frozen=True)
class EffectEvent:
    nonce: str
    target_id: str
    kind: str
    before: Mapping[str, Any] | None
    after: Mapping[str, Any] | None
    ordinal: int
    commit_version: int


@dataclass(frozen=True)
class EffectTrace:
    events: tuple[EffectEvent, ...]
    current_exists: bool
    current: Mapping[str, Any] | None
    current_version: int


FEATURE_COSTS: dict[str, int] = {
    "event_count": 1,
    "event_targets": 1,
    "event_kinds": 1,
    "event_before_allowed": 2,
    "event_after_allowed": 2,
    "event_before_frame": 2,
    "event_after_frame": 2,
    "current_exists": 1,
    "current_allowed": 2,
    "current_frame": 2,
    "version_alignment": 1,
}
ALL_FEATURES = tuple(FEATURE_COSTS)


@dataclass(frozen=True)
class CompilationResult:
    selected_features: tuple[str, ...]
    certificate: Mapping[str, str]
    correct_signature: tuple[tuple[str, Any], ...]
    abstract_mutants: int
    available_features: tuple[str, ...]

    @property
    def read_cost(self) -> int:
        return sum(FEATURE_COSTS[name] for name in self.selected_features)

    def verify(self, spec: EffectSpec, trace: EffectTrace) -> bool:
        return project(spec, trace, self.selected_features) == self.correct_signature


class UnwitnessableEffect(ValueError):
    def __init__(self, mutant_names: Sequence[str]):
        self.mutant_names = tuple(mutant_names)
        super().__init__(
            "effect is not distinguishable with available observation features: "
            + ", ".join(self.mutant_names)
        )


def canonical_trace(spec: EffectSpec, *, version: int = 11) -> EffectTrace:
    desired = spec.desired()
    event = EffectEvent(
        nonce=spec.nonce,
        target_id=spec.target_id,
        kind=spec.operation,
        before=None if spec.before is None else dict(spec.before),
        after=None if desired is None else dict(desired),
        ordinal=1,
        commit_version=version,
    )
    return EffectTrace(
        events=(event,),
        current_exists=desired is not None,
        current=None if desired is None else dict(desired),
        current_version=version,
    )


def _different(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 37
    if isinstance(value, float):
        return value + 37.0
    if isinstance(value, list):
        return [*value, "unexpected"]
    return f"unexpected::{value}"


def _replace_event(event: EffectEvent, **updates: Any) -> EffectEvent:
    values = {
        "nonce": event.nonce,
        "target_id": event.target_id,
        "kind": event.kind,
        "before": event.before,
        "after": event.after,
        "ordinal": event.ordinal,
        "commit_version": event.commit_version,
    }
    values.update(updates)
    return EffectEvent(**values)


def abstract_mutants(spec: EffectSpec) -> tuple[tuple[str, EffectTrace], ...]:
    """Abstract mutants used only by the method compiler."""

    correct = canonical_trace(spec)
    event = correct.events[0]
    mutants: list[tuple[str, EffectTrace]] = [
        (
            "missing_effect",
            EffectTrace((), spec.before is not None, spec.before, 10),
        ),
        (
            "wrong_identity",
            EffectTrace(
                (_replace_event(event, target_id=f"other::{spec.target_id}"),),
                correct.current_exists,
                correct.current,
                correct.current_version,
            ),
        ),
        (
            "duplicate_event",
            EffectTrace(
                (event, _replace_event(event, ordinal=2)),
                correct.current_exists,
                correct.current,
                correct.current_version,
            ),
        ),
        (
            "collateral_event",
            EffectTrace(
                (
                    event,
                    _replace_event(
                        event,
                        target_id=f"collateral::{spec.target_id}",
                        ordinal=2,
                    ),
                ),
                correct.current_exists,
                correct.current,
                correct.current_version,
            ),
        ),
        (
            "delete_recreate_cycle",
            EffectTrace(
                (
                    _replace_event(event, kind="delete", after=None, ordinal=1),
                    _replace_event(event, kind="create", before=None, ordinal=2),
                ),
                correct.current_exists,
                correct.current,
                correct.current_version,
            ),
        ),
        (
            "revision_mismatch",
            EffectTrace(
                correct.events,
                correct.current_exists,
                correct.current,
                correct.current_version + 1,
            ),
        ),
    ]

    desired = spec.desired()
    if desired is not None and spec.allowed_updates:
        field = sorted(spec.allowed_updates)[0]
        bad_after = dict(desired)
        bad_after[field] = _different(bad_after[field])
        mutants.append(
            (
                "wrong_required_value",
                EffectTrace(
                    (_replace_event(event, after=bad_after),),
                    True,
                    bad_after,
                    correct.current_version,
                ),
            )
        )

    if desired is not None and spec.frame_fields:
        field = spec.frame_fields[0]
        polluted = dict(desired)
        polluted[field] = _different(polluted[field])
        mutants.extend(
            (
                (
                    "same_entity_frame_pollution",
                    EffectTrace(
                        (_replace_event(event, after=polluted),),
                        True,
                        polluted,
                        correct.current_version,
                    ),
                ),
                (
                    "same_entity_field_deletion",
                    EffectTrace(
                        (
                            _replace_event(
                                event,
                                after={key: value for key, value in desired.items() if key != field},
                            ),
                        ),
                        True,
                        {key: value for key, value in desired.items() if key != field},
                        correct.current_version,
                    ),
                ),
            )
        )

    if spec.operation != "delete":
        rollback = None if spec.before is None else dict(spec.before)
        mutants.append(
            (
                "rollback_before_observation",
                EffectTrace(
                    correct.events,
                    rollback is not None,
                    rollback,
                    correct.current_version,
                ),
            )
        )
    else:
        mutants.append(
            (
                "resurrection_before_observation",
                EffectTrace(
                    correct.events,
                    True,
                    spec.before,
                    correct.current_version,
                ),
            )
        )
    return tuple(mutants)


def _parts(record: Mapping[str, Any] | None, fields: Iterable[str]) -> tuple[tuple[str, Any], ...] | None:
    if record is None:
        return None
    return tuple((field, record.get(field, "<MISSING>")) for field in sorted(fields))


def feature_value(spec: EffectSpec, trace: EffectTrace, feature: str) -> Any:
    events = trace.events
    if feature == "event_count":
        return len(events)
    if feature == "event_targets":
        return tuple(event.target_id for event in events)
    if feature == "event_kinds":
        return tuple(event.kind for event in events)
    if feature == "event_before_allowed":
        return tuple(_parts(event.before, spec.allowed_updates) for event in events)
    if feature == "event_after_allowed":
        return tuple(_parts(event.after, spec.allowed_updates) for event in events)
    if feature == "event_before_frame":
        return tuple(_parts(event.before, spec.frame_fields) for event in events)
    if feature == "event_after_frame":
        return tuple(_parts(event.after, spec.frame_fields) for event in events)
    if feature == "current_exists":
        return trace.current_exists
    if feature == "current_allowed":
        return _parts(trace.current, spec.allowed_updates)
    if feature == "current_frame":
        return _parts(trace.current, spec.frame_fields)
    if feature == "version_alignment":
        return tuple(event.commit_version == trace.current_version for event in events)
    raise KeyError(feature)


def project(
    spec: EffectSpec, trace: EffectTrace, features: Iterable[str]
) -> tuple[tuple[str, Any], ...]:
    return tuple((name, feature_value(spec, trace, name)) for name in features)


def compile_witness(
    spec: EffectSpec, available_features: Iterable[str]
) -> CompilationResult:
    """Select a low-cost distinguishing projection and emit its certificate."""

    available = tuple(dict.fromkeys(available_features))
    unknown = sorted(set(available) - set(ALL_FEATURES))
    if unknown:
        raise ValueError(f"unknown observation features: {unknown}")
    correct = canonical_trace(spec)
    mutants = abstract_mutants(spec)
    distinguishing: dict[str, set[str]] = {}
    for mutant_name, mutant in mutants:
        distinguishing[mutant_name] = {
            feature
            for feature in available
            if feature_value(spec, correct, feature)
            != feature_value(spec, mutant, feature)
        }
    unobservable = sorted(name for name, choices in distinguishing.items() if not choices)
    if unobservable:
        raise UnwitnessableEffect(unobservable)

    uncovered = set(distinguishing)
    selected: list[str] = []
    while uncovered:
        ranked: list[tuple[float, int, str, set[str]]] = []
        for feature in available:
            if feature in selected:
                continue
            killed = {name for name in uncovered if feature in distinguishing[name]}
            if killed:
                cost = FEATURE_COSTS[feature]
                ranked.append((-len(killed) / cost, cost, feature, killed))
        if not ranked:
            raise AssertionError("observable mutants unexpectedly uncovered")
        ranked.sort(key=lambda item: (item[0], item[1], item[2]))
        _, _, feature, killed = ranked[0]
        selected.append(feature)
        uncovered.difference_update(killed)

    certificate: dict[str, str] = {}
    for mutant_name in sorted(distinguishing):
        certificate[mutant_name] = next(
            feature for feature in selected if feature in distinguishing[mutant_name]
        )
    signature = project(spec, correct, selected)
    return CompilationResult(
        selected_features=tuple(selected),
        certificate=certificate,
        correct_signature=signature,
        abstract_mutants=len(mutants),
        available_features=available,
    )


def direct_exact_available(
    spec: EffectSpec, trace: EffectTrace, available_features: Iterable[str]
) -> bool:
    features = tuple(available_features)
    return project(spec, trace, features) == project(spec, canonical_trace(spec), features)
