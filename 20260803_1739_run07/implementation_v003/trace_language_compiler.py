"""Exact observation compiler for sets of correct and harmful traces."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class TraceExample:
    example_id: str
    features: Mapping[str, Any]


@dataclass(frozen=True)
class LanguageCertificate:
    selected_features: tuple[str, ...]
    accepted_signatures: frozenset[tuple[tuple[str, Any], ...]]
    pair_witness: Mapping[str, str]
    cost: int
    available_features: tuple[str, ...]

    def verify(self, example: TraceExample) -> bool:
        return signature(example, self.selected_features) in self.accepted_signatures


class UnseparableLanguage(ValueError):
    def __init__(self, collisions: Sequence[tuple[str, str]]):
        self.collisions = tuple(collisions)
        super().__init__(f"correct/harmful observation collision: {self.collisions[:8]}")


def freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple((key, freeze(value[key])) for key in sorted(value))
    if isinstance(value, (list, tuple)):
        return tuple(freeze(item) for item in value)
    if isinstance(value, set):
        return tuple(sorted(freeze(item) for item in value))
    return value


def signature(
    example: TraceExample, features: Iterable[str]
) -> tuple[tuple[str, Any], ...]:
    return tuple((feature, freeze(example.features[feature])) for feature in features)


def _distinguishing_features(
    correct: Sequence[TraceExample],
    harmful: Sequence[TraceExample],
    available: Sequence[str],
) -> dict[tuple[str, str], set[str]]:
    pairs: dict[tuple[str, str], set[str]] = {}
    for left in correct:
        for right in harmful:
            pairs[(left.example_id, right.example_id)] = {
                feature
                for feature in available
                if freeze(left.features[feature]) != freeze(right.features[feature])
            }
    return pairs


def _exact_cover(
    pairs: Mapping[tuple[str, str], set[str]],
    available: Sequence[str],
    costs: Mapping[str, int],
) -> tuple[str, ...]:
    candidates: list[tuple[int, int, tuple[str, ...]]] = []
    for size in range(len(available) + 1):
        for subset in combinations(available, size):
            if all(any(feature in distinguishing for feature in subset) for distinguishing in pairs.values()):
                candidates.append((sum(costs[item] for item in subset), size, subset))
        if candidates:
            minimum = min(item[0] for item in candidates)
            if all(sum(sorted(costs.values())[: size + 1]) > minimum for _ in (0,)):
                break
    if not candidates:
        raise AssertionError("cover expected after collision check")
    return min(candidates, key=lambda item: (item[0], item[1], item[2]))[2]


def _greedy_cover(
    pairs: Mapping[tuple[str, str], set[str]],
    available: Sequence[str],
    costs: Mapping[str, int],
) -> tuple[str, ...]:
    uncovered = set(pairs)
    selected: list[str] = []
    while uncovered:
        ranked = []
        for feature in available:
            if feature in selected:
                continue
            hit = {pair for pair in uncovered if feature in pairs[pair]}
            if hit:
                ranked.append((-len(hit) / costs[feature], costs[feature], feature, hit))
        if not ranked:
            raise AssertionError("greedy cover expected after collision check")
        ranked.sort(key=lambda item: (item[0], item[1], item[2]))
        _, _, feature, hit = ranked[0]
        selected.append(feature)
        uncovered.difference_update(hit)
    return tuple(selected)


def compile_language(
    correct: Sequence[TraceExample],
    harmful: Sequence[TraceExample],
    available_features: Iterable[str],
    costs: Mapping[str, int],
    *,
    optimizer: str = "exact",
) -> LanguageCertificate:
    if not correct or not harmful:
        raise ValueError("both correct and harmful trace sets must be non-empty")
    available = tuple(dict.fromkeys(available_features))
    pairs = _distinguishing_features(correct, harmful, available)
    collisions = [pair for pair, features in pairs.items() if not features]
    if collisions:
        raise UnseparableLanguage(collisions)
    if optimizer == "exact":
        selected = _exact_cover(pairs, available, costs)
    elif optimizer == "greedy":
        selected = _greedy_cover(pairs, available, costs)
    else:
        raise ValueError(optimizer)
    witnesses: dict[str, str] = {}
    for pair in sorted(pairs):
        witnesses[f"{pair[0]}::{pair[1]}"] = next(
            feature for feature in selected if feature in pairs[pair]
        )
    accepted = frozenset(signature(example, selected) for example in correct)
    return LanguageCertificate(
        selected,
        accepted,
        witnesses,
        sum(costs[item] for item in selected),
        available,
    )


def validate_certificate(
    certificate: LanguageCertificate,
    correct: Sequence[TraceExample],
    harmful: Sequence[TraceExample],
) -> bool:
    return all(certificate.verify(item) for item in correct) and not any(
        certificate.verify(item) for item in harmful
    )

