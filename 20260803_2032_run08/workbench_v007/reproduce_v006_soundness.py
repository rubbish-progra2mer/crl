#!/usr/bin/env python3
"""复现 v006 记录、计划与见证完整性反例。"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, replace
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
V006 = RUN_ROOT / "implementation_v006"
sys.path.insert(0, str(V006))

from independent_semantic_oracle import validate_candidate_witness  # noqa: E402
from observation_closed_effects import (  # noqa: E402
    CLAIM_AUXILIARY,
    CLAIM_COUNT,
    CLAIM_TARGET_RESPONSIVE,
    AdmissionRequest,
    EffectContract,
    ObservedEvent,
    ProbeObservation,
    ProjectionSpec,
    _record_payload,
    canonical_hash,
    compile_contract,
    consume_record,
    evaluate_observations,
    issue_record,
    request_for_plan,
)


def contract() -> EffectContract:
    return EffectContract(
        contract_version="v006-repro-contract",
        primary_kind="write",
        exact_primary_count=1,
        allowed_auxiliary_kinds=(),
        target_requirement="responsive",
        payload_forbidden_factors=(),
    )


def projection(visibility: str = "stable_anonymous") -> ProjectionSpec:
    return ProjectionSpec(
        projection_version="v006-repro-projection",
        target_visibility=visibility,
        payload_visibility="stable_anonymous",
        normalizer_id="v006-repro-normalizer",
    )


def clean_observations(plan):
    return tuple(
        ProbeObservation(
            probe.probe_id,
            (
                ObservedEvent(
                    kind=plan.primary_kind,
                    target_token=probe.target_value,
                    payload_token="payload",
                ),
            ),
        )
        for probe in plan.probes
    )


def resign(record):
    unsigned = replace(record, record_digest="")
    return replace(
        unsigned,
        record_digest=canonical_hash(_record_payload(unsigned)),
    )


def main() -> int:
    plan = compile_contract(contract(), projection())
    report = evaluate_observations(plan, clean_observations(plan))
    record = issue_record(
        plan,
        report,
        tool_id="tool:v006-repro",
        tool_version="1",
    )
    request = request_for_plan(
        plan,
        tool_id="tool:v006-repro",
        tool_version="1",
        evidence_hash=record.evidence_hash,
    )

    contradictory = resign(
        replace(
            record,
            failed_claims=(CLAIM_TARGET_RESPONSIVE,),
        )
    )

    arbitrary = "relation.sequence.second_call_safe"
    minted = resign(
        replace(
            record,
            contract_claims=tuple(sorted(record.contract_claims + (arbitrary,))),
            passed_claims=tuple(sorted(record.passed_claims + (arbitrary,))),
        )
    )
    minted_request = replace(
        request,
        required_claims=(arbitrary,),
    )

    unrelated_nonidentifiable = resign(
        replace(
            record,
            nonidentifiable_claims=("relation.unrelated.nonidentifiable",),
            nonidentifiability_witness_hashes=("claimed-witness",),
        )
    )

    tampered_plan = replace(
        plan,
        relations=(),
        contract_claims=(CLAIM_AUXILIARY, CLAIM_COUNT),
        identifiable_claims=(CLAIM_AUXILIARY, CLAIM_COUNT),
        nonidentifiable=(),
    )
    tampered_report = evaluate_observations(
        tampered_plan, clean_observations(tampered_plan)
    )
    tampered_record = issue_record(
        tampered_plan,
        tampered_report,
        tool_id="tool:v006-repro",
        tool_version="1",
    )
    tampered_request = request_for_plan(
        tampered_plan,
        tool_id="tool:v006-repro",
        tool_version="1",
        evidence_hash=tampered_record.evidence_hash,
    )

    hidden_plan = compile_contract(contract(), projection("clone_local_anonymous"))
    witness = hidden_plan.nonidentifiable[0]
    false_shared_observation = replace(
        witness,
        shared_observation=("fabricated:not-the-derived-observation",),
    )
    witness_check = validate_candidate_witness(
        claim_id=false_shared_observation.claim_id,
        visibility="clone_local_anonymous",
        world_true=asdict(false_shared_observation.world_true),
        world_false=asdict(false_shared_observation.world_false),
    )

    outcomes = {
        "honest_allowed": consume_record(record, request).allowed,
        "same_claim_passed_and_failed_allowed": consume_record(
            contradictory, request
        ).allowed,
        "arbitrary_claim_minted_allowed": consume_record(
            minted, minted_request
        ).allowed,
        "unrelated_nonidentifiable_but_pass_allowed": consume_record(
            unrelated_nonidentifiable, request
        ).allowed,
        "tampered_plan_hash_unchanged": tampered_plan.plan_hash == plan.plan_hash,
        "tampered_plan_contract_hash_unchanged": (
            tampered_plan.contract_hash == plan.contract_hash
        ),
        "tampered_plan_admitted": consume_record(
            tampered_record, tampered_request
        ).allowed,
        "tampered_plan_removed_target_claim": (
            CLAIM_TARGET_RESPONSIVE not in tampered_plan.contract_claims
        ),
        "fabricated_shared_observation_declared": list(
            false_shared_observation.shared_observation
        ),
        "validator_accepted_worlds_without_checking_declared_shared_observation": (
            witness_check["valid"]
        ),
    }
    print(json.dumps(outcomes, ensure_ascii=False, indent=2, sort_keys=True))

    expected_true = tuple(outcomes.values())
    if not all(expected_true):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
