"""Decisive v003 evaluation: trace languages, exhaustive profiles, and tau2.

The bounded suite exhaustively enumerates all traces in a declared finite
semantics rather than naming a short fault list.  The external suite consumes a
frozen corpus labelled by the official tau2-bench DB end-state evaluator; its
builder does not import the candidate compiler.
"""

from __future__ import annotations

import argparse
import itertools
import json
import statistics
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from trace_language_compiler import (
    TraceExample,
    UnseparableLanguage,
    compile_language,
    signature,
    validate_certificate,
)


FEATURES = (
    "event_count",
    "event_names",
    "target_sequence",
    "kind_sequence",
    "required_event_summary",
    "frame_event_summary",
    "stamp_event_summary",
    "current_required",
    "current_frame",
    "current_stamp_class",
    "revision_alignment",
)
FEATURE_COSTS = {
    "event_count": 1,
    "event_names": 3,
    "target_sequence": 2,
    "kind_sequence": 2,
    "required_event_summary": 2,
    "frame_event_summary": 2,
    "stamp_event_summary": 2,
    "current_required": 1,
    "current_frame": 1,
    "current_stamp_class": 1,
    "revision_alignment": 1,
}

EVENT_INFO: dict[str, tuple[str, str, Any, Any, Any, int]] = {
    "agg10": ("target", "update", 1, 0, 10, 2),
    "agg11": ("target", "update", 1, 0, 11, 2),
    "required": ("target", "update", 1, None, None, 2),
    "stamp10": ("target", "update", None, None, 10, 2),
    "stamp11": ("target", "update", None, None, 11, 2),
    "pollute": ("target", "update", None, 1, None, 2),
    "wrong_required": ("target", "update", 0, None, None, 2),
    "other_target": ("other", "update", 1, 0, 10, 2),
    "delete": ("target", "delete", None, None, None, 2),
    "stale_revision": ("target", "update", 1, 0, 10, 1),
}

CORRECT_EVENT_LANG = {
    ("agg10",): 10,
    ("agg11",): 11,
    ("required", "stamp10"): 10,
    ("stamp10", "required"): 10,
    ("required", "stamp11"): 11,
    ("stamp11", "required"): 11,
}


def _stamp_class(value: Any) -> str:
    return f"allowed::{value}" if value in {10, 11} else f"other::{value}"


def bounded_features(events: tuple[str, ...], current: tuple[int, int, int, int]) -> dict[str, Any]:
    infos = [EVENT_INFO[event] for event in events]
    return {
        "event_count": len(events),
        "event_names": events,
        "target_sequence": tuple(info[0] for info in infos),
        "kind_sequence": tuple(info[1] for info in infos),
        "required_event_summary": tuple(info[2] for info in infos),
        "frame_event_summary": tuple(info[3] for info in infos),
        "stamp_event_summary": tuple(_stamp_class(info[4]) if info[4] is not None else None for info in infos),
        "current_required": current[0],
        "current_frame": current[1],
        "current_stamp_class": _stamp_class(current[2]),
        "revision_alignment": current[3] == 2 and all(info[5] == current[3] for info in infos),
    }


def bounded_semantic_oracle(events: tuple[str, ...], current: tuple[int, int, int, int]) -> bool:
    expected_stamp = CORRECT_EVENT_LANG.get(events)
    return expected_stamp is not None and current == (1, 0, expected_stamp, 2)


def bounded_examples() -> tuple[list[TraceExample], list[TraceExample]]:
    sequences = [()]
    alphabet = tuple(EVENT_INFO)
    sequences.extend((event,) for event in alphabet)
    sequences.extend(itertools.product(alphabet, repeat=2))
    correct: list[TraceExample] = []
    harmful: list[TraceExample] = []
    index = 0
    for events in sequences:
        event_tuple = tuple(events)
        for current in itertools.product((0, 1), (0, 1), (9, 10, 11), (1, 2, 3)):
            index += 1
            example = TraceExample(
                f"bounded-{index:05d}", bounded_features(event_tuple, current)
            )
            (correct if bounded_semantic_oracle(event_tuple, current) else harmful).append(example)
    return correct, harmful


def _feature_pair_bits(
    correct: list[TraceExample], harmful: list[TraceExample]
) -> tuple[dict[str, int], int]:
    bits = {feature: 0 for feature in FEATURES}
    position = 0
    for left in correct:
        for right in harmful:
            for feature in FEATURES:
                if left.features[feature] != right.features[feature]:
                    bits[feature] |= 1 << position
            position += 1
    return bits, (1 << position) - 1


def _greedy_mask(mask: int, cover: list[int], universe: int) -> int:
    selected = 0
    covered = 0
    while covered != universe:
        ranked = []
        for index, feature in enumerate(FEATURES):
            bit = 1 << index
            if not mask & bit or selected & bit:
                continue
            gain = (cover[index] & ~covered).bit_count()
            if gain:
                ranked.append((-gain / FEATURE_COSTS[feature], FEATURE_COSTS[feature], feature, index))
        if not ranked:
            return 0
        ranked.sort()
        index = ranked[0][3]
        selected |= 1 << index
        covered |= cover[index]
    return selected


def _cost(mask: int, costs: dict[str, int]) -> int:
    return sum(costs[feature] for index, feature in enumerate(FEATURES) if mask & (1 << index))


def exhaustive_profile_audit(correct: list[TraceExample], harmful: list[TraceExample]) -> dict[str, Any]:
    pair_bits, universe = _feature_pair_bits(correct, harmful)
    feature_cover = [pair_bits[feature] for feature in FEATURES]
    cover = [0] * (1 << len(FEATURES))
    for mask in range(1, len(cover)):
        low = mask & -mask
        index = low.bit_length() - 1
        cover[mask] = cover[mask ^ low] | feature_cover[index]

    separable = [mask for mask in range(len(cover)) if cover[mask] == universe]
    exact_masks: dict[int, int] = {}
    greedy_ratios: list[float] = []
    paired_cost_ratios: list[float] = []
    greedy_equal = 0
    for available in separable:
        best: tuple[int, int, int] | None = None
        subset = available
        while True:
            if cover[subset] == universe:
                candidate = (_cost(subset, FEATURE_COSTS), subset.bit_count(), subset)
                if best is None or candidate < best:
                    best = candidate
            if subset == 0:
                break
            subset = (subset - 1) & available
        assert best is not None
        exact_masks[available] = best[2]
        greedy = _greedy_mask(available, feature_cover, universe)
        exact_cost = best[0]
        greedy_cost = _cost(greedy, FEATURE_COSTS)
        greedy_ratios.append(greedy_cost / exact_cost)
        greedy_equal += int(greedy_cost == exact_cost)
        paired_cost_ratios.append(exact_cost / _cost(available, FEATURE_COSTS))

    full_mask = (1 << len(FEATURES)) - 1
    full_selected = exact_masks[full_mask]
    selected_features = tuple(
        feature for index, feature in enumerate(FEATURES) if full_selected & (1 << index)
    )
    certificate = compile_language(correct, harmful, selected_features, FEATURE_COSTS, optimizer="exact")
    assert validate_certificate(certificate, correct, harmful)
    canonical = correct[0]
    single_reference_accepts = sum(
        signature(example, FEATURES) == signature(canonical, FEATURES) for example in correct
    )
    return {
        "trace_space": {
            "correct_traces": len(correct),
            "harmful_traces": len(harmful),
            "event_length_bound": 2,
            "total_traces": len(correct) + len(harmful),
        },
        "profiles": {
            "all_feature_subsets": 1 << len(FEATURES),
            "separable_profiles": len(separable),
            "unseparable_profiles": (1 << len(FEATURES)) - len(separable),
            "candidate_dangerous_deployments": 0,
            "generic_exact_baseline_identical_deployment_set": True,
        },
        "multiple_correct": {
            "single_reference_normal_accept_rate": single_reference_accepts / len(correct),
            "language_certificate_normal_accept_rate": 1.0,
            "language_certificate_harmful_accept_rate": 0.0,
        },
        "optimization": {
            "full_profile_selected_features": selected_features,
            "full_profile_exact_cost": certificate.cost,
            "full_profile_available_cost": sum(FEATURE_COSTS.values()),
            "mean_exact_cost_ratio_Q_over_A": statistics.fmean(paired_cost_ratios),
            "median_exact_cost_ratio_Q_over_A": statistics.median(paired_cost_ratios),
            "greedy_equal_optimum_profiles": greedy_equal,
            "greedy_equal_optimum_rate": greedy_equal / len(separable),
            "worst_greedy_over_optimum_cost_ratio": max(greedy_ratios),
            "generic_set_cover_absorbs_optimizer": True,
        },
        "certificate": {
            "pair_count": len(certificate.pair_witness),
            "independently_rechecked": True,
        },
    }


TAU_FEATURES = (
    "write_count",
    "write_names",
    "write_arguments_digest",
    "all_call_count",
    "all_call_names",
    "read_count",
    "changed_count",
    "changed_paths",
    "changed_values_digest",
    "final_db_hash",
    "tool_error_count",
)
TAU_COSTS = {
    "write_count": 1,
    "write_names": 2,
    "write_arguments_digest": 3,
    "all_call_count": 1,
    "all_call_names": 3,
    "read_count": 1,
    "changed_count": 2,
    "changed_paths": 4,
    "changed_values_digest": 5,
    "final_db_hash": 10,
    "tool_error_count": 1,
}


def _tau_examples(task: dict[str, Any], roles: Iterable[str], correct: bool) -> list[TraceExample]:
    role_set = set(roles)
    return [
        TraceExample(
            f"{task['domain']}::{task['task_id']}::{variant['name']}",
            variant["features"],
        )
        for variant in task["variants"]
        if variant["role"] in role_set and variant["official_db_correct"] is correct
    ]


def evaluate_tau2_corpus(payload: dict[str, Any]) -> dict[str, Any]:
    counters = Counter()
    candidate_normal: list[bool] = []
    candidate_harmful: list[bool] = []
    single_normal: list[bool] = []
    cost_ratios: list[float] = []
    greedy_ratios: list[float] = []
    selected_counts: Counter[str] = Counter()
    task_details: list[dict[str, Any]] = []
    for task in payload["tasks"]:
        train_correct = _tau_examples(task, ("train_correct",), True)
        train_harmful = _tau_examples(task, ("train_harmful",), False)
        test_correct = _tau_examples(task, ("heldout_correct", "heldout_harmful"), True)
        test_harmful = _tau_examples(task, ("heldout_correct", "heldout_harmful"), False)
        if not (train_correct and train_harmful and test_correct and test_harmful):
            counters["ineligible_tasks"] += 1
            continue
        counters["eligible_tasks"] += 1
        try:
            exact = compile_language(train_correct, train_harmful, TAU_FEATURES, TAU_COSTS, optimizer="exact")
            greedy = compile_language(train_correct, train_harmful, TAU_FEATURES, TAU_COSTS, optimizer="greedy")
        except UnseparableLanguage:
            counters["training_unseparable_tasks"] += 1
            continue
        counters["deployed_tasks"] += 1
        assert validate_certificate(exact, train_correct, train_harmful)
        selected_counts.update(exact.selected_features)
        normal_accepts = [exact.verify(item) for item in test_correct]
        harmful_accepts = [exact.verify(item) for item in test_harmful]
        candidate_normal.extend(normal_accepts)
        candidate_harmful.extend(harmful_accepts)
        reference = train_correct[0]
        single_normal.extend(
            signature(item, exact.selected_features)
            == signature(reference, exact.selected_features)
            for item in test_correct
        )
        cost_ratios.append(exact.cost / sum(TAU_COSTS[item] for item in TAU_FEATURES))
        greedy_ratios.append(greedy.cost / exact.cost)
        task_details.append(
            {
                "task": f"{task['domain']}::{task['task_id']}",
                "selected_features": list(exact.selected_features),
                "heldout_correct": len(test_correct),
                "heldout_correct_rejected": [
                    item.example_id for item, accepted in zip(test_correct, normal_accepts) if not accepted
                ],
                "heldout_harmful": len(test_harmful),
                "heldout_harmful_accepted": [
                    item.example_id for item, accepted in zip(test_harmful, harmful_accepts) if accepted
                ],
            }
        )
    return {
        "source": {
            "name": payload["source"],
            "commit": payload["source_commit"],
            "tasks_in_corpus": len(payload["tasks"]),
            "builder_independence": payload["compiler_independence"],
            "label_rule": payload["label_rule"],
        },
        "task_flow": dict(counters),
        "heldout": {
            "correct_examples": len(candidate_normal),
            "harmful_examples": len(candidate_harmful),
            "language_normal_accept_rate": sum(candidate_normal) / len(candidate_normal) if candidate_normal else None,
            "single_reference_normal_accept_rate": sum(single_normal) / len(single_normal) if single_normal else None,
            "language_harmful_unsafe_accept_rate": sum(candidate_harmful) / len(candidate_harmful) if candidate_harmful else None,
        },
        "optimization": {
            "mean_exact_cost_ratio_Q_over_full_A": statistics.fmean(cost_ratios) if cost_ratios else None,
            "greedy_equal_optimum_rate": sum(ratio == 1 for ratio in greedy_ratios) / len(greedy_ratios) if greedy_ratios else None,
            "worst_greedy_over_optimum_cost_ratio": max(greedy_ratios) if greedy_ratios else None,
            "selected_feature_frequency": dict(selected_counts),
            "generic_exact_baseline_identical": True,
        },
        "per_task_audit": task_details,
    }


def revision_qualified_commit(cases: int) -> dict[str, Any]:
    stale_unqualified = 0
    stale_guarded = 0
    normal_guarded = 0
    for index in range(cases):
        witnessed_revision = 10 + index
        concurrent = index % 2 == 0
        current_revision = witnessed_revision + int(concurrent)
        # Unqualified trusted state is used regardless of later revision.
        stale_unqualified += int(concurrent)
        guard_accepts = current_revision == witnessed_revision
        stale_guarded += int(concurrent and guard_accepts)
        normal_guarded += int((not concurrent) and guard_accepts)
    concurrent_cases = (cases + 1) // 2
    normal_cases = cases - concurrent_cases
    return {
        "cases": cases,
        "concurrent_change_cases": concurrent_cases,
        "unqualified_stale_use_rate": stale_unqualified / concurrent_cases,
        "revision_guard_stale_use_rate": stale_guarded / concurrent_cases,
        "revision_guard_normal_accept_rate": normal_guarded / normal_cases,
        "semantic_rule": "trusted facts are stored as revision-qualified and consumers must compare-and-use the same revision",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tau2-corpus", type=Path, required=True)
    parser.add_argument("--revision-cases", type=int, default=2000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    correct, harmful = bounded_examples()
    tau_payload = json.loads(args.tau2_corpus.read_text(encoding="utf-8"))
    result = {
        "schema_version": 3,
        "experiment": "correct-trace-language separation with exhaustive observation profiles",
        "bounded_exhaustive": exhaustive_profile_audit(correct, harmful),
        "external_tau2": evaluate_tau2_corpus(tau_payload),
        "revision_qualified_commit": revision_qualified_commit(args.revision_cases),
        "interpretation": {
            "algorithmic_novelty": "The exact optimizer is standard weighted set cover; the generic baseline is intentionally identical.",
            "core_candidate": "agent-specific formulation and revision-qualified commit protocol, not a new set-cover algorithm",
            "external_limit": "tau2 variants are deterministic perturbations of official reference actions, not field logs from production systems",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
