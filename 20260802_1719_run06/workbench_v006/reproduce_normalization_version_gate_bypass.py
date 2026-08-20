"""Reproduce the v006 normalization-version hard-gate bypass."""

from dataclasses import replace
import json
import sys
from pathlib import Path


IMPLEMENTATION = Path(__file__).resolve().parents[1] / "implementation_v006"
sys.path.insert(0, str(IMPLEMENTATION))

from joint_coverage_kernel import (  # noqa: E402
    Claim,
    Observation,
    Record,
    ScopeCell,
    SourceIdentity,
    canonical_request_payload,
    evaluate_claim,
    verify_certificate,
)


SOURCE_V2 = SourceIdentity(
    "test",
    "list-v1",
    "subject-1",
    "joint-scope-v1",
    "adapter-v1",
    "semantic-normalization-v2",
    "canonical-json-v1",
)
SOURCE_V1 = replace(
    SOURCE_V2, semantic_normalization_version="semantic-normalization-v1"
)
A = ScopeCell("A", "recent", "active")
B = ScopeCell("B", "recent", "active")
CLAIM = Claim("normalization-gate", "exists", "matches_target", (B,), "s1", SOURCE_V2)


def observation(
    observation_id: str,
    outer_source: SourceIdentity,
    outer_cell: ScopeCell,
    payload_source: SourceIdentity,
    payload_cell: ScopeCell,
    records: tuple[Record, ...] = (),
) -> Observation:
    return Observation(
        observation_id=observation_id,
        connector_id=outer_source.connector_id,
        cell=outer_cell,
        cursor=0,
        next_cursor=None,
        records=records,
        snapshot_id="s1",
        query_signature=outer_source.query_signature,
        authentication_subject=outer_source.authentication_subject,
        scope_schema_version=outer_source.scope_schema_version,
        adapter_version=outer_source.adapter_version,
        semantic_normalization_version=outer_source.semantic_normalization_version,
        request_serialization_version=outer_source.request_serialization_version,
        request_payload=canonical_request_payload(payload_source, payload_cell, 0, "s1"),
    )


clean = observation("clean-empty-b-v2", SOURCE_V2, B, SOURCE_V2, B)
hidden = observation(
    "v1-outer-b-payload-a-record-b",
    SOURCE_V1,
    B,
    SOURCE_V1,
    A,
    (Record("positive-b", B, True, True),),
)

clean_result = evaluate_claim(CLAIM, [clean])
combined_result = evaluate_claim(CLAIM, [clean, hidden])
output = {
    "cross_version_semantics_assumed_equivalent": True,
    "independent_truth_with_hidden_record": "TRUE",
    "clean_decision": clean_result.decision,
    "clean_certificate_valid_after_hidden_added": verify_certificate(
        CLAIM, [clean, hidden], clean_result.certificate
    ),
    "combined_decision": combined_result.decision,
    "combined_certificate_valid": verify_certificate(
        CLAIM, [clean, hidden], combined_result.certificate
    ),
    "hidden_digest_in_audit_commitment": hidden.digest
    in combined_result.certificate.audit_observation_digests,
    "unsafe_wrong_certification": combined_result.decision == "FALSE",
}
print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
