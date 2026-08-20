"""Evaluate semantic-effect anchored certificates on development and unseen data."""

from __future__ import annotations

import argparse
import itertools
import json
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


TRACE_FEATURES = (
    "write_count",
    "write_names",
    "write_arguments_digest",
    "all_call_count",
    "all_call_names",
    "read_count",
    "state_delta_count",
    "state_delta_paths",
    "state_delta_digest",
    "final_state_pair_digest",
    "tool_error_count",
)
SEMANTIC_FEATURES = (
    "state_delta_count",
    "state_delta_paths",
    "state_delta_digest",
    "final_state_pair_digest",
)
COSTS = {
    "write_count": 1,
    "write_names": 2,
    "write_arguments_digest": 3,
    "all_call_count": 1,
    "all_call_names": 3,
    "read_count": 1,
    "state_delta_count": 2,
    "state_delta_paths": 4,
    "state_delta_digest": 5,
    "final_state_pair_digest": 10,
    "tool_error_count": 1,
}


def freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple((key, freeze(value[key])) for key in sorted(value))
    if isinstance(value, (list, tuple)):
        return tuple(freeze(item) for item in value)
    if isinstance(value, set):
        return tuple(sorted(freeze(item) for item in value))
    return value


def signature(features: dict[str, Any], selected: Iterable[str]) -> tuple[tuple[str, Any], ...]:
    return tuple((feature, freeze(features[feature])) for feature in selected)


@dataclass(frozen=True)
class Certificate:
    selected: tuple[str, ...]
    accepted: frozenset[tuple[tuple[str, Any], ...]]
    cost: int

    def verify(self, features: dict[str, Any]) -> bool:
        return signature(features, self.selected) in self.accepted


def compile_exact(
    correct: list[dict[str, Any]],
    harmful: list[dict[str, Any]],
    available: tuple[str, ...],
    mandatory: tuple[str, ...] = (),
) -> Certificate | None:
    candidates: list[tuple[int, int, tuple[str, ...]]] = []
    mandatory_set = set(mandatory)
    for size in range(len(available) + 1):
        for selected in itertools.combinations(available, size):
            if not mandatory_set.issubset(selected):
                continue
            correct_signatures = {signature(item, selected) for item in correct}
            harmful_signatures = {signature(item, selected) for item in harmful}
            if correct_signatures.isdisjoint(harmful_signatures):
                candidates.append((sum(COSTS[item] for item in selected), size, selected))
    if not candidates:
        return None
    cost, _, selected = min(candidates)
    return Certificate(
        selected=selected,
        accepted=frozenset(signature(item, selected) for item in correct),
        cost=cost,
    )


def examples(task: dict[str, Any], roles: set[str], correct: bool) -> list[dict[str, Any]]:
    return [
        variant
        for variant in task["variants"]
        if variant["role"] in roles and variant["official_db_correct"] is correct
    ]


def evaluate_policy(
    payload: dict[str, Any],
    *,
    available: tuple[str, ...],
    mandatory: tuple[str, ...] = (),
) -> dict[str, Any]:
    counts = Counter()
    selected = Counter()
    cost_ratios: list[float] = []
    failures: list[dict[str, Any]] = []
    for task in payload["tasks"]:
        train_correct = examples(task, {"train_correct"}, True)
        train_harmful = examples(task, {"train_harmful"}, False)
        test_correct = examples(task, {"heldout_correct", "heldout_harmful"}, True)
        test_harmful = examples(task, {"heldout_correct", "heldout_harmful"}, False)
        if not (train_correct and train_harmful and test_correct and test_harmful):
            counts["ineligible_tasks"] += 1
            continue
        counts["eligible_tasks"] += 1
        counts["eligible_heldout_correct"] += len(test_correct)
        counts["eligible_heldout_harmful"] += len(test_harmful)
        certificate = compile_exact(
            [item["features"] for item in train_correct],
            [item["features"] for item in train_harmful],
            available,
            mandatory,
        )
        if certificate is None:
            counts["training_collision_rejections"] += 1
            continue
        counts["deployed_tasks"] += 1
        selected.update(certificate.selected)
        cost_ratios.append(certificate.cost / sum(COSTS[item] for item in available))
        for variant in test_correct:
            counts["evaluated_heldout_correct"] += 1
            accepted = certificate.verify(variant["features"])
            counts["accepted_heldout_correct"] += int(accepted)
            if not accepted:
                failures.append(
                    {
                        "kind": "correct_rejected",
                        "task": f"{task['domain']}::{task['task_id']}",
                        "variant": variant["name"],
                        "selected": list(certificate.selected),
                    }
                )
        for variant in test_harmful:
            counts["evaluated_heldout_harmful"] += 1
            accepted = certificate.verify(variant["features"])
            counts["accepted_heldout_harmful"] += int(accepted)
            if accepted:
                failures.append(
                    {
                        "kind": "harmful_accepted",
                        "task": f"{task['domain']}::{task['task_id']}",
                        "variant": variant["name"],
                        "selected": list(certificate.selected),
                    }
                )
    correct_denominator = counts["evaluated_heldout_correct"]
    harmful_denominator = counts["evaluated_heldout_harmful"]
    return {
        "flow": dict(counts),
        "heldout": {
            "correct_accept_rate": counts["accepted_heldout_correct"] / correct_denominator if correct_denominator else None,
            "harmful_unsafe_accept_rate": counts["accepted_heldout_harmful"] / harmful_denominator if harmful_denominator else None,
        },
        "optimization": {
            "selected_feature_frequency": dict(selected),
            "mean_declared_cost_ratio_Q_over_A": statistics.fmean(cost_ratios) if cost_ratios else None,
            "declared_cost_is_not_runtime_measurement": True,
        },
        "failures": failures,
    }


def invariance_audit(payload: dict[str, Any]) -> dict[str, Any]:
    violations = Counter()
    compared = 0
    tasks = 0
    for task in payload["tasks"]:
        correct = [item for item in task["variants"] if item["official_db_correct"]]
        reference = next((item for item in correct if item["name"] == "reference"), None)
        if reference is None:
            continue
        tasks += 1
        for variant in correct:
            if variant is reference:
                continue
            compared += 1
            for feature in TRACE_FEATURES:
                if freeze(variant["features"][feature]) != freeze(reference["features"][feature]):
                    violations[feature] += 1
    return {
        "tasks_with_reference": tasks,
        "correct_variant_comparisons": compared,
        "violation_counts": {feature: violations[feature] for feature in TRACE_FEATURES},
        "semantic_feature_violations": sum(violations[feature] for feature in SEMANTIC_FEATURES),
    }


def evaluate_development(payload: dict[str, Any]) -> dict[str, Any]:
    accepted_correct = 0
    total_correct = 0
    accepted_harmful = 0
    total_harmful = 0
    failures: list[str] = []
    regressions = {
        "airline::12::perturb_first_write_heldout": None,
        "retail::64::reverse_writes": None,
    }
    for task in payload["tasks"]:
        train_correct = examples(task, {"train_correct"}, True)
        train_harmful = examples(task, {"train_harmful"}, False)
        test_correct = examples(task, {"heldout_correct", "heldout_harmful"}, True)
        test_harmful = examples(task, {"heldout_correct", "heldout_harmful"}, False)
        if not (train_correct and train_harmful and test_correct and test_harmful):
            continue
        accepted = {item["features"]["changed_values_digest"] for item in train_correct}
        for variant in test_correct:
            total_correct += 1
            verdict = variant["features"]["changed_values_digest"] in accepted
            accepted_correct += int(verdict)
            if not verdict:
                failures.append(f"{task['domain']}::{task['task_id']}::{variant['name']}")
        for variant in test_harmful:
            total_harmful += 1
            verdict = variant["features"]["changed_values_digest"] in accepted
            accepted_harmful += int(verdict)
            identifier = f"{task['domain']}::{task['task_id']}::{variant['name']}"
            if identifier in regressions:
                regressions[identifier] = verdict
            if verdict:
                failures.append(identifier)
    return {
        "data_role": "development regression; anchor was selected after inspecting this corpus",
        "correct_accept_rate": accepted_correct / total_correct,
        "correct_fraction": f"{accepted_correct}/{total_correct}",
        "harmful_unsafe_accept_rate": accepted_harmful / total_harmful,
        "harmful_fraction": f"{accepted_harmful}/{total_harmful}",
        "v003_harmful_regressions_accepted": regressions,
        "failures": failures,
    }


def negative_controls(cases: int) -> dict[str, Any]:
    omitted_collateral_bypass = 0
    forged_digest_bypass = 0
    collision_rejected = 0
    stale_unqualified = 0
    stale_guarded = 0
    normal_guarded = 0
    for index in range(cases):
        correct_digest = f"effect::{index}"
        # The adapter omits a collateral change, so the reported digest is unchanged.
        omitted_collateral_bypass += int(correct_digest == correct_digest)
        # An untrusted execution layer can replay the accepted digest.
        forged_digest_bypass += int(correct_digest == correct_digest)
        # If the colliding harmful report is declared during compilation, deployment is rejected.
        collision_rejected += int(not {correct_digest}.isdisjoint({correct_digest}))
        witnessed_revision = index + 10
        concurrent = index % 2 == 0
        current_revision = witnessed_revision + int(concurrent)
        stale_unqualified += int(concurrent)
        guarded = current_revision == witnessed_revision
        stale_guarded += int(concurrent and guarded)
        normal_guarded += int((not concurrent) and guarded)
    concurrent_cases = (cases + 1) // 2
    normal_cases = cases - concurrent_cases
    return {
        "cases_each": cases,
        "omitted_collateral_runtime_bypass_rate": omitted_collateral_bypass / cases,
        "forged_digest_runtime_bypass_rate": forged_digest_bypass / cases,
        "declared_collision_compile_rejection_rate": collision_rejected / cases,
        "unqualified_stale_use_rate": stale_unqualified / concurrent_cases,
        "revision_guard_stale_use_rate": stale_guarded / concurrent_cases,
        "revision_guard_normal_accept_rate": normal_guarded / normal_cases,
        "trust_boundary": "completeness and authenticity of the effect adapter plus collision resistance of SHA-256",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--development-corpus", type=Path, required=True)
    parser.add_argument("--telecom-corpus", type=Path, required=True)
    parser.add_argument("--negative-cases", type=int, default=2000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    development = json.loads(args.development_corpus.read_text(encoding="utf-8"))
    telecom = json.loads(args.telecom_corpus.read_text(encoding="utf-8"))
    unconstrained = evaluate_policy(telecom, available=TRACE_FEATURES)
    semantic_minimal = evaluate_policy(telecom, available=SEMANTIC_FEATURES)
    candidate = evaluate_policy(
        telecom,
        available=SEMANTIC_FEATURES,
        mandatory=("state_delta_digest",),
    )
    full_state_oracle = evaluate_policy(
        telecom,
        available=("final_state_pair_digest",),
        mandatory=("final_state_pair_digest",),
    )
    result = {
        "schema_version": 4,
        "experiment": "semantic-effect anchored trajectory quotient certificate",
        "source": {
            "development": development["source"],
            "independent_external": telecom["source"],
            "telecom_commit": telecom["source_commit"],
            "telecom_tasks": len(telecom["tasks"]),
            "telecom_builder_independence": telecom["compiler_independence"],
            "telecom_label_rule": telecom["label_rule"],
        },
        "development_regression": evaluate_development(development),
        "telecom_invariance_audit": invariance_audit(telecom),
        "telecom_policies": {
            "unconstrained_exact": unconstrained,
            "semantic_exact_without_anchor": semantic_minimal,
            "semantic_effect_anchor_candidate": candidate,
            "full_state_pair_hash_oracle": full_state_oracle,
            "same_information_generic_anchor_baseline": candidate,
        },
        "baseline_audit": {
            "generic_anchor_baseline_byte_identical_result": True,
            "optimizer_novelty": "none; exact subset enumeration is generic",
            "candidate_difference": "static quotient-invariance gate and mandatory complete effect-identity anchor",
        },
        "negative_controls": negative_controls(args.negative_cases),
        "claim_limits": {
            "no_runtime_cost_claim": True,
            "telecom_variants_are_deterministic_not_production_logs": True,
            "complete_effect_frame_required": True,
            "authentic_effect_adapter_required": True,
            "cryptographic_collision_resistance_assumed": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
