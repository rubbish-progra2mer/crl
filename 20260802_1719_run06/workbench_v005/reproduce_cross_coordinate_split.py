"""Reproduce the v005 cross-coordinate relevance split found in review."""

from dataclasses import replace
import json
import sys
from pathlib import Path


IMPLEMENTATION = Path(__file__).resolve().parents[1] / "implementation_v005"
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


SOURCE = SourceIdentity(
    "test",
    "list-v1",
    "subject-1",
    "joint-scope-v1",
    "adapter-v1",
    "canonical-json-v1",
)
FOREIGN_SOURCE = replace(SOURCE, connector_id="foreign")
B = ScopeCell("B", "recent", "active")
A = ScopeCell("A", "recent", "active")
CLAIM = Claim("split", "exists", "matches_target", (B,), "s1", SOURCE)


def observation(
    observation_id: str,
    *,
    outer_source: SourceIdentity,
    outer_cell: ScopeCell,
    outer_snapshot: str,
    payload_source: SourceIdentity,
    payload_cell: ScopeCell,
    payload_snapshot: str,
    records: tuple[Record, ...] = (),
) -> Observation:
    return Observation(
        observation_id=observation_id,
        connector_id=outer_source.connector_id,
        cell=outer_cell,
        cursor=0,
        next_cursor=None,
        records=records,
        snapshot_id=outer_snapshot,
        query_signature=outer_source.query_signature,
        authentication_subject=outer_source.authentication_subject,
        scope_schema_version=outer_source.scope_schema_version,
        adapter_version=outer_source.adapter_version,
        request_serialization_version=outer_source.request_serialization_version,
        request_payload=canonical_request_payload(
            payload_source, payload_cell, 0, payload_snapshot
        ),
    )


clean = observation(
    "clean-empty-b",
    outer_source=SOURCE,
    outer_cell=B,
    outer_snapshot="s1",
    payload_source=SOURCE,
    payload_cell=B,
    payload_snapshot="s1",
)

# The outer representation supplies the expected source but the wrong snapshot;
# the payload representation supplies the expected snapshot but a foreign source.
# A real in-scope positive record is therefore missed by v005's per-key conjunctions.
split = observation(
    "split-positive-b",
    outer_source=SOURCE,
    outer_cell=A,
    outer_snapshot="s2",
    payload_source=FOREIGN_SOURCE,
    payload_cell=A,
    payload_snapshot="s1",
    records=(Record("positive-b", B, True, True),),
)

clean_only = evaluate_claim(CLAIM, [clean])
with_split = evaluate_claim(CLAIM, [clean, split])

output = {
    "independent_truth_with_split": "TRUE",
    "clean_only_decision": clean_only.decision,
    "clean_only_certificate_valid_on_clean_only": verify_certificate(
        CLAIM, [clean], clean_only.certificate
    ),
    "clean_only_certificate_valid_after_split_added": verify_certificate(
        CLAIM, [clean, split], clean_only.certificate
    ),
    "with_split_decision": with_split.decision,
    "with_split_certificate_valid": verify_certificate(
        CLAIM, [clean, split], with_split.certificate
    ),
    "split_digest_in_audit_commitment": split.digest
    in with_split.certificate.audit_observation_digests,
    "unsafe_wrong_certification": with_split.decision == "FALSE",
}

print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
