from dataclasses import asdict, replace

import pytest

from independent_semantic_oracle import (
    oracle_identifiable,
    validate_candidate_witness,
)
from observation_closed_effects import (
    CLAIM_TARGET_IDENTITY,
    EffectContract,
    ObservedEvent,
    ProbeObservation,
    ProjectionSpec,
    UnsupportedContract,
    compile_contract,
    consume_record,
    evaluate_observations,
    issue_record,
    request_for_plan,
)


def make_contract(*, count=1, target="responsive"):
    return EffectContract(
        contract_version="test-contract-v1",
        primary_kind="write",
        exact_primary_count=count,
        allowed_auxiliary_kinds=(),
        target_requirement=target,
        payload_forbidden_factors=(),
    )


def make_projection(target="stable_anonymous"):
    return ProjectionSpec(
        projection_version="test-projection-v1",
        target_visibility=target,
        payload_visibility="stable_anonymous",
        normalizer_id="test-normalizer-v1",
    )


def clean_observations(plan):
    return tuple(
        ProbeObservation(
            probe.probe_id,
            (
                ObservedEvent(
                    plan.primary_kind,
                    probe.target_value,
                    "payload-token",
                ),
            ),
        )
        for probe in plan.probes
    )


@pytest.mark.parametrize("count", [0, 2, 3])
def test_non_unary_contract_fails_closed(count):
    with pytest.raises(UnsupportedContract):
        compile_contract(make_contract(count=count), make_projection())


def test_stable_anonymous_identity_is_rejected_with_valid_witness():
    plan = compile_contract(
        make_contract(target="identity"), make_projection("stable_anonymous")
    )
    assert CLAIM_TARGET_IDENTITY not in plan.identifiable_claims
    assert not oracle_identifiable(
        CLAIM_TARGET_IDENTITY, "stable_anonymous"
    )
    witness = plan.nonidentifiable[0]
    check = validate_candidate_witness(
        claim_id=witness.claim_id,
        visibility="stable_anonymous",
        world_true=asdict(witness.world_true),
        world_false=asdict(witness.world_false),
    )
    assert check["valid"] is True


def test_revealed_identity_can_be_observed_and_consumed():
    plan = compile_contract(
        make_contract(target="identity"), make_projection("revealed")
    )
    report = evaluate_observations(plan, clean_observations(plan))
    record = issue_record(
        plan,
        report,
        tool_id="tool:test",
        tool_version="1",
    )
    request = request_for_plan(
        plan,
        tool_id="tool:test",
        tool_version="1",
        evidence_hash=record.evidence_hash,
    )
    assert consume_record(record, request).allowed


def test_consumer_rejects_tamper_and_overclaim():
    plan = compile_contract(make_contract(), make_projection())
    report = evaluate_observations(plan, clean_observations(plan))
    record = issue_record(
        plan,
        report,
        tool_id="tool:test",
        tool_version="1",
    )
    request = request_for_plan(
        plan,
        tool_id="tool:test",
        tool_version="1",
        evidence_hash=record.evidence_hash,
    )
    tampered = replace(
        record,
        passed_claims=record.passed_claims + (CLAIM_TARGET_IDENTITY,),
    )
    overclaim = replace(
        request,
        required_claims=request.required_claims + (CLAIM_TARGET_IDENTITY,),
    )
    assert not consume_record(tampered, request).allowed
    assert not consume_record(record, overclaim).allowed


def test_consumer_rejects_witness_binding_tamper_and_unknown_schema():
    plan = compile_contract(make_contract(), make_projection())
    report = evaluate_observations(plan, clean_observations(plan))
    record = issue_record(
        plan,
        report,
        tool_id="tool:test",
        tool_version="1",
    )
    request = request_for_plan(
        plan,
        tool_id="tool:test",
        tool_version="1",
        evidence_hash=record.evidence_hash,
    )
    witness_tamper = replace(
        record,
        nonidentifiability_witness_hashes=("changed",),
    )
    unknown_schema = replace(record, schema_version=2)
    assert not consume_record(witness_tamper, request).allowed
    assert not consume_record(unknown_schema, request).allowed


def test_projection_changes_executable_or_nonidentifiable_result():
    stable = compile_contract(make_contract(), make_projection())
    local = compile_contract(
        make_contract(), make_projection("clone_local_anonymous")
    )
    assert stable.relations
    assert not stable.nonidentifiable
    assert not local.relations
    assert local.nonidentifiable
