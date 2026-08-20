#!/usr/bin/env python3
"""穷举受支持合同域，审计编译分区、见证与消费失败关闭。"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, replace
from pathlib import Path

from independent_semantic_oracle import (
    oracle_identifiable,
    validate_candidate_witness,
)
from observation_closed_effects import (
    CLAIM_AUXILIARY,
    CLAIM_COUNT,
    CLAIM_TARGET_IDENTITY,
    CLAIM_TARGET_RESPONSIVE,
    EffectContract,
    ObservedEvent,
    ProbeObservation,
    ProjectionSpec,
    UnsupportedContract,
    compile_contract,
    consume_record,
    evaluate_observations,
    issue_record,
    payload_claim,
    request_for_plan,
)


VISIBILITIES = (
    "revealed",
    "stable_anonymous",
    "clone_local_anonymous",
)
TARGET_REQUIREMENTS = ("none", "responsive", "identity")
FACTOR_SETS = (
    (),
    ("ambient_canary",),
    ("sensitive_input",),
    ("ambient_canary", "sensitive_input"),
)
AUXILIARY_SETS = ((), ("audit",), ("metric",), ("audit", "metric"))
PRIMARY_KINDS = ("write", "message_send")


def clean_observations(plan):
    identity_expected = {
        relation.left_probe: relation.expected_value
        for relation in plan.relations
        if relation.relation_kind == "target_equals_expected"
    }
    return tuple(
        ProbeObservation(
            probe.probe_id,
            (
                ObservedEvent(
                    plan.primary_kind,
                    str(
                        identity_expected.get(
                            probe.probe_id,
                            f"target-token:{probe.target_value}",
                        )
                    ),
                    "stable-payload-token",
                ),
            ),
        )
        for probe in plan.probes
    )


def requested_relation_claims(contract: EffectContract) -> tuple[str, ...]:
    claims: list[str] = []
    if contract.target_requirement == "responsive":
        claims.append(CLAIM_TARGET_RESPONSIVE)
    elif contract.target_requirement == "identity":
        claims.append(CLAIM_TARGET_IDENTITY)
    claims.extend(payload_claim(factor) for factor in contract.payload_forbidden_factors)
    return tuple(sorted(claims))


def claim_visibility(claim: str, projection: ProjectionSpec) -> str:
    if claim.startswith("relation.payload."):
        return projection.payload_visibility
    return projection.target_visibility


def run_audit(output_path: Path) -> dict[str, object]:
    failures: list[dict[str, object]] = []
    total = 0
    admissible = 0
    rejected_for_nonidentifiability = 0
    witness_count = 0
    oracle_checks = 0
    stale_rejections = 0
    expected_stale_rejections = 0
    plan_hashes: set[str] = set()
    baseline_correct = 0
    baseline_total = 0

    combinations = itertools.product(
        PRIMARY_KINDS,
        AUXILIARY_SETS,
        TARGET_REQUIREMENTS,
        FACTOR_SETS,
        VISIBILITIES,
        VISIBILITIES,
    )
    for index, (
        primary_kind,
        auxiliary,
        target_requirement,
        factors,
        target_visibility,
        payload_visibility,
    ) in enumerate(combinations):
        total += 1
        contract = EffectContract(
            contract_version="exhaustive-contract-v1",
            primary_kind=primary_kind,
            exact_primary_count=1,
            allowed_auxiliary_kinds=auxiliary,
            target_requirement=target_requirement,  # type: ignore[arg-type]
            payload_forbidden_factors=factors,
        )
        projection = ProjectionSpec(
            projection_version="exhaustive-projection-v1",
            target_visibility=target_visibility,  # type: ignore[arg-type]
            payload_visibility=payload_visibility,  # type: ignore[arg-type]
            normalizer_id="exhaustive-normalizer-v1",
        )
        plan = compile_contract(contract, projection)
        if plan.plan_hash in plan_hashes:
            failures.append({"index": index, "reason": "duplicate_plan_hash"})
        plan_hashes.add(plan.plan_hash)

        relation_claims = set(requested_relation_claims(contract))
        identifiable = set(plan.identifiable_claims) - {CLAIM_COUNT, CLAIM_AUXILIARY}
        nonidentifiable = {item.claim_id for item in plan.nonidentifiable}
        if identifiable | nonidentifiable != relation_claims:
            failures.append(
                {
                    "index": index,
                    "reason": "claim_partition_incomplete",
                    "expected": sorted(relation_claims),
                    "identifiable": sorted(identifiable),
                    "nonidentifiable": sorted(nonidentifiable),
                }
            )
        if identifiable & nonidentifiable:
            failures.append({"index": index, "reason": "claim_partition_overlap"})

        probe_ids = {probe.probe_id for probe in plan.probes}
        if len(probe_ids) != len(plan.probes):
            failures.append({"index": index, "reason": "duplicate_probe_id"})
        for relation in plan.relations:
            if relation.left_probe not in probe_ids or (
                relation.right_probe is not None
                and relation.right_probe not in probe_ids
            ):
                failures.append(
                    {"index": index, "reason": "relation_references_missing_probe"}
                )

        for claim in relation_claims:
            oracle_checks += 1
            visibility = claim_visibility(claim, projection)
            oracle_value = oracle_identifiable(claim, visibility)
            candidate_value = claim in identifiable
            if candidate_value != oracle_value:
                failures.append(
                    {
                        "index": index,
                        "reason": "oracle_mismatch",
                        "claim": claim,
                        "visibility": visibility,
                    }
                )
            # 观察不感知基线总是声称可辨识。
            baseline_total += 1
            baseline_correct += int(oracle_value)

        for witness in plan.nonidentifiable:
            witness_count += 1
            check = validate_candidate_witness(
                claim_id=witness.claim_id,
                visibility=claim_visibility(witness.claim_id, projection),
                world_true=asdict(witness.world_true),
                world_false=asdict(witness.world_false),
            )
            if not check["valid"]:
                failures.append(
                    {
                        "index": index,
                        "reason": "invalid_witness",
                        "claim": witness.claim_id,
                    }
                )

        report = evaluate_observations(plan, clean_observations(plan))
        record = issue_record(
            plan,
            report,
            tool_id=f"tool:{index}",
            tool_version="1",
        )
        request = request_for_plan(
            plan,
            tool_id=f"tool:{index}",
            tool_version="1",
            evidence_hash=record.evidence_hash,
        )
        decision = consume_record(record, request)
        expected_allowed = not nonidentifiable
        admissible += int(decision.allowed)
        rejected_for_nonidentifiability += int(
            bool(nonidentifiable) and not decision.allowed
        )
        if decision.allowed != expected_allowed:
            failures.append(
                {
                    "index": index,
                    "reason": "clean_consumer_mismatch",
                    "expected_allowed": expected_allowed,
                    "actual_allowed": decision.allowed,
                }
            )

        stale_requests = (
            replace(request, tool_id="stale"),
            replace(request, tool_version="stale"),
            replace(request, contract_hash="stale"),
            replace(request, projection_hash="stale"),
            replace(request, probe_catalog_hash="stale"),
            replace(request, plan_hash="stale"),
            replace(request, evidence_hash="stale"),
        )
        for stale in stale_requests:
            expected_stale_rejections += 1
            rejected = not consume_record(record, stale).allowed
            stale_rejections += int(rejected)
            if not rejected:
                failures.append(
                    {"index": index, "reason": "stale_binding_accepted"}
                )

        tampered = replace(record, status="pass" if record.status != "pass" else "x")
        if consume_record(tampered, request).allowed:
            failures.append({"index": index, "reason": "tampered_record_accepted"})

    rejection_checks = 0
    for count in (0, 2, 3):
        rejection_checks += 1
        try:
            compile_contract(
                EffectContract(
                    contract_version="non-unary-v1",
                    primary_kind="write",
                    exact_primary_count=count,
                    allowed_auxiliary_kinds=(),
                    target_requirement="responsive",
                    payload_forbidden_factors=("ambient_canary",),
                ),
                ProjectionSpec(
                    projection_version="non-unary-projection-v1",
                    target_visibility="stable_anonymous",
                    payload_visibility="stable_anonymous",
                    normalizer_id="non-unary-normalizer-v1",
                ),
            )
        except UnsupportedContract:
            continue
        failures.append({"reason": "non_unary_accepted", "count": count})

    summary = {
        "schema_version": 1,
        "supported_contract_projection_combinations": total,
        "unique_plan_hashes": len(plan_hashes),
        "oracle_claim_checks": oracle_checks,
        "candidate_oracle_mismatches": sum(
            item.get("reason") == "oracle_mismatch" for item in failures
        ),
        "validated_nonidentifiability_witnesses": witness_count,
        "admissible_clean_combinations": admissible,
        "rejected_clean_combinations_with_nonidentifiable_claims": rejected_for_nonidentifiability,
        "stale_binding_rejections": stale_rejections,
        "expected_stale_binding_rejections": expected_stale_rejections,
        "non_unary_rejection_checks": rejection_checks,
        "observation_unaware_baseline_correct": baseline_correct,
        "observation_unaware_baseline_total": baseline_total,
        "failure_count": len(failures),
        "failures": failures,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if failures:
        raise AssertionError(f"穷举审计发现 {len(failures)} 个失败")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    arguments = parser.parse_args()
    summary = run_audit(Path(arguments.output))
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
