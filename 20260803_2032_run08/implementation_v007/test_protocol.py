#!/usr/bin/env python3
"""v007 声称可靠性与协议攻击回归。"""

from __future__ import annotations

import hashlib
from dataclasses import replace

import pytest

from compiler import (
    compile_contract,
    contract_claim_refs,
    validate_plan,
    validate_witness,
)
from protocol import evaluate_observations, issue_attestation, verify_and_admit
from typed_model import (
    AdmissionBundle,
    AdmissionRequest,
    BooleanExpr,
    ChannelProjection,
    ClaimRef,
    CompareExpr,
    EffectContract,
    EvidenceBundle,
    FieldRef,
    HiddenWorld,
    IntegrityError,
    LiteralValue,
    MappingEntry,
    ObservedEvent,
    ProbeObservation,
    ProbeSpec,
    ProjectionMap,
    ProjectionPolicy,
    RelationClaim,
    SchemaError,
    canonical_bytes,
    canonical_hash,
    canonical_roundtrip,
    decode_contract,
    decode_projection,
    without_plan_hash,
    without_signature,
)


KEY = b"v007-test-only-shared-secret-32b"
NOW = 1_800_000_000


def _probe(probe_id: str) -> ProbeSpec:
    return ProbeSpec(probe_id=probe_id, factors=(("case", probe_id),))


def _contract(*, boolean: bool = False) -> EffectContract:
    p1, p2 = _probe("p1"), _probe("p2")
    equality = CompareExpr(
        operator="eq",
        left=FieldRef(probe_id="p1", channel="target"),
        right=FieldRef(probe_id="p2", channel="target"),
    )
    formula = equality
    if boolean:
        formula = BooleanExpr(
            operator="and",
            children=(
                equality,
                BooleanExpr(
                    operator="not",
                    children=(
                        CompareExpr(
                            operator="ne",
                            left=FieldRef(probe_id="p1", channel="payload"),
                            right=LiteralValue(value="x"),
                        ),
                    ),
                ),
            ),
        )
    return EffectContract(
        contract_id="example.effect",
        contract_version="7",
        primary_kind="write",
        allowed_auxiliary_kinds=("audit",),
        structural_probe=_probe("structural"),
        relation_claims=(
            RelationClaim(
                display_name="same target",
                probes=(p1, p2),
                formula=formula,
            ),
        ),
    )


def _projection(kind: str = "global_bijection") -> ProjectionPolicy:
    return ProjectionPolicy(
        policy_id="example.projection",
        policy_version="7",
        target=ChannelProjection(kind=kind, domain=("a", "b")),
        payload=ChannelProjection(kind="identity", domain=("x", "y")),
    )


def _observations(target2: str = "a") -> tuple[ProbeObservation, ...]:
    return (
        ProbeObservation(
            probe_id="p1",
            events=(
                ObservedEvent(kind="write", target_token="a", payload_token="x"),
                ObservedEvent(kind="audit", target_token="a", payload_token="x"),
            ),
        ),
        ProbeObservation(
            probe_id="p2",
            events=(
                ObservedEvent(
                    kind="write", target_token=target2, payload_token="y"
                ),
            ),
        ),
    )


def _valid_bundle(*, boolean: bool = False):
    contract = _contract(boolean=boolean)
    projection = _projection()
    plan = compile_contract(contract, projection)
    observations = _observations()
    report = evaluate_observations(contract, projection, plan, observations)
    evidence = EvidenceBundle(contract, projection, plan, observations, report)
    record = issue_attestation(
        evidence,
        issuer_id="issuer-A",
        issuer_key=KEY,
        tool_id="tool-A",
        tool_version="1.0",
        issued_at=NOW - 10,
        expires_at=NOW + 100,
        nonce="nonce-001",
    )
    bundle = AdmissionBundle(
        contract, projection, plan, observations, report, record
    )
    request = AdmissionRequest(
        tool_id="tool-A",
        tool_version="1.0",
        contract_hash=plan.contract_hash,
        projection_hash=plan.projection_hash,
        plan_hash=plan.plan_hash,
        required_claims=contract_claim_refs(contract),
    )
    return bundle, request


def _admit(bundle, request, *, now=NOW, cache=None, issuers=None):
    return verify_and_admit(
        bundle,
        request,
        trusted_issuers={"issuer-A": KEY} if issuers is None else issuers,
        replay_cache=set() if cache is None else cache,
        now=now,
    )


def test_valid_signed_bundle_is_admitted() -> None:
    bundle, request = _valid_bundle()
    decision = _admit(bundle, request)
    assert decision.allowed, decision.reasons


def test_boolean_ast_compiles_and_executes_without_claim_specific_branch() -> None:
    bundle, request = _valid_bundle(boolean=True)
    assert _admit(bundle, request).allowed
    bad_observations = _observations(target2="b")
    report = evaluate_observations(
        bundle.contract, bundle.projection, bundle.plan, bad_observations
    )
    assert report.failed_claims


def test_canonical_contract_and_projection_roundtrip() -> None:
    contract, projection = _contract(), _projection()
    assert canonical_roundtrip(contract, decode_contract) == contract
    assert canonical_roundtrip(projection, decode_projection) == projection


def test_relation_plan_does_not_add_unrequested_structural_probe() -> None:
    plan = compile_contract(_contract(), _projection())
    assert tuple(probe.probe_id for probe in plan.probes) == ("p1", "p2")


def test_literal_outside_declared_domain_is_rejected() -> None:
    contract = _contract(boolean=True)
    claim = contract.relation_claims[0]
    bad_formula = CompareExpr(
        operator="eq",
        left=FieldRef(probe_id="p1", channel="payload"),
        right=LiteralValue(value="outside"),
    )
    bad_contract = replace(
        contract,
        relation_claims=(replace(claim, formula=bad_formula),),
    )
    with pytest.raises(SchemaError):
        compile_contract(bad_contract, _projection())


def test_forged_self_contradictory_record_is_rejected_even_with_public_hash() -> None:
    bundle, request = _valid_bundle()
    record = replace(
        bundle.record,
        failed_claims=bundle.record.passed_claims,
        status="pass",
        signature="",
    )
    forged_public_digest = hashlib.sha256(
        canonical_bytes(without_signature(record))
    ).hexdigest()
    forged = replace(bundle, record=replace(record, signature=forged_public_digest))
    assert not _admit(forged, request).allowed


def test_minted_claim_is_rejected() -> None:
    bundle, request = _valid_bundle()
    minted = ClaimRef("finite_relation", "f" * 64)
    bad_request = replace(
        request, required_claims=tuple(sorted(request.required_claims + (minted,)))
    )
    assert not _admit(bundle, bad_request).allowed


def test_subset_claim_cannot_be_reused_under_a_different_contract_binding() -> None:
    bundle, request = _valid_bundle()
    confused = replace(
        request,
        contract_hash="0" * 64,
        required_claims=(request.required_claims[0],),
    )
    assert not _admit(bundle, confused).allowed


def test_plan_field_tamper_with_old_hash_is_rejected() -> None:
    bundle, request = _valid_bundle()
    tampered = replace(bundle.plan, probes=tuple(reversed(bundle.plan.probes)))
    assert not _admit(replace(bundle, plan=tampered), request).allowed


def test_plan_field_tamper_with_recomputed_unkeyed_hash_is_rejected() -> None:
    bundle, request = _valid_bundle()
    tampered = replace(bundle.plan, probes=(bundle.plan.probes[0],))
    tampered = replace(
        tampered, plan_hash=canonical_hash(without_plan_hash(tampered))
    )
    with pytest.raises(IntegrityError):
        validate_plan(tampered, bundle.contract, bundle.projection)
    assert not _admit(replace(bundle, plan=tampered), request).allowed


def test_report_and_raw_observation_tampering_are_rejected() -> None:
    bundle, request = _valid_bundle()
    contradictory_report = replace(
        bundle.report,
        passed_claims=(),
        failed_claims=bundle.report.passed_claims,
    )
    assert not _admit(replace(bundle, report=contradictory_report), request).allowed
    assert not _admit(replace(bundle, observations=_observations("b")), request).allowed


def test_replay_expiry_unknown_issuer_and_tool_mismatch_are_rejected() -> None:
    bundle, request = _valid_bundle()
    cache: set[str] = set()
    assert _admit(bundle, request, cache=cache).allowed
    assert not _admit(bundle, request, cache=cache).allowed
    assert not _admit(bundle, request, now=NOW + 101).allowed
    assert not _admit(bundle, request, issuers={}).allowed
    assert not _admit(bundle, replace(request, tool_version="2.0")).allowed


def test_probe_local_renaming_yields_valid_nonidentifiability_witness() -> None:
    contract = _contract()
    projection = _projection("probe_local_bijection")
    plan = compile_contract(contract, projection)
    assert len(plan.nonidentifiable) == 1
    witness = plan.nonidentifiable[0]
    validate_witness(witness, contract.relation_claims[0], projection)
    report = evaluate_observations(contract, projection, plan, _observations())
    evidence = EvidenceBundle(contract, projection, plan, _observations(), report)
    record = issue_attestation(
        evidence,
        issuer_id="issuer-A",
        issuer_key=KEY,
        tool_id="tool-A",
        tool_version="1.0",
        issued_at=NOW - 1,
        expires_at=NOW + 1,
        nonce="nonidentifiable",
    )
    request = AdmissionRequest(
        tool_id="tool-A",
        tool_version="1.0",
        contract_hash=plan.contract_hash,
        projection_hash=plan.projection_hash,
        plan_hash=plan.plan_hash,
        required_claims=contract_claim_refs(contract),
    )
    assert record.status == "fail"
    assert not _admit(
        AdmissionBundle(contract, projection, plan, _observations(), report, record),
        request,
    ).allowed


def test_fabricated_shared_observation_and_illegal_map_are_rejected() -> None:
    contract = _contract()
    projection = _projection("probe_local_bijection")
    witness = compile_contract(contract, projection).nonidentifiable[0]
    with pytest.raises(IntegrityError):
        validate_witness(
            replace(witness, shared_observation=("fabricated",)),
            contract.relation_claims[0],
            projection,
        )
    world = witness.world_true
    first = world.projection_maps[0]
    illegal = replace(
        first,
        entries=(MappingEntry("a", "a"), MappingEntry("b", "a")),
    )
    bad_world = replace(
        world, projection_maps=(illegal,) + world.projection_maps[1:]
    )
    with pytest.raises(IntegrityError):
        validate_witness(
            replace(witness, world_true=bad_world),
            contract.relation_claims[0],
            projection,
        )
