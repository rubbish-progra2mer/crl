from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence

from joint_coverage_kernel import (
    Claim,
    CoverageCertificate,
    Cursor,
    Observation,
    ScopeCell,
)


@dataclass(frozen=True)
class _IndependentTrace:
    complete: bool
    witness_pages: tuple[Observation, ...]
    chain_digests: tuple[str, ...]
    evidence_digests: tuple[str, ...]
    blocked: bool
    conflicted: bool


@dataclass(frozen=True)
class _IndependentRequestKey:
    source_fields: tuple[str, ...]
    cell: ScopeCell
    cursor: Cursor
    snapshot_id: str


@dataclass(frozen=True)
class _IndependentPreflight:
    audited: tuple[Observation, ...]
    conflicts: tuple[Observation, ...]

    @property
    def audit_digests(self) -> tuple[str, ...]:
        return tuple(sorted(item.digest for item in self.audited))


def _response_commitment_from_spec(item: Observation) -> str:
    encoded = json.dumps(
        {
            "schema_version": 1,
            "request_payload_digest": hashlib.sha256(
                item.request_payload.encode("utf-8")
            ).hexdigest(),
            "records": [
                {
                    "record_id": record.record_id,
                    "cell": record.cell.key,
                    "matches_target": record.matches_target,
                    "compliant": record.compliant,
                }
                for record in item.records
            ],
            "next_cursor": item.next_cursor,
            "status": item.status,
            "permission_complete": item.permission_complete,
            "silently_truncated": item.silently_truncated,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _cursor_key(cursor: Cursor) -> tuple[str, str]:
    return type(cursor).__name__, str(cursor)


@lru_cache(maxsize=65536)
def _request_payload_from_spec(
    claim: Claim,
    cell: ScopeCell,
    cursor: Cursor,
) -> str:
    source = claim.source
    return json.dumps(
        {
            "adapter_version": source.adapter_version,
            "authentication_subject": source.authentication_subject,
            "connector_id": source.connector_id,
            "cursor": cursor,
            "filters": {
                "archive_state": cell.archive_state,
                "entity": cell.entity,
                "time_bucket": cell.time_bucket,
            },
            "operation": source.query_signature,
            "semantic_normalization_version": source.semantic_normalization_version,
            "request_serialization_version": source.request_serialization_version,
            "scope_schema_version": source.scope_schema_version,
            "snapshot_id": claim.snapshot_id,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


@lru_cache(maxsize=65536)
def _source_fields_from_claim(claim: Claim) -> tuple[str, ...]:
    source = claim.source
    return (
        source.connector_id,
        source.query_signature,
        source.authentication_subject,
        source.scope_schema_version,
        source.adapter_version,
        source.semantic_normalization_version,
        source.request_serialization_version,
    )


@lru_cache(maxsize=65536)
def _metadata_key(item: Observation) -> _IndependentRequestKey:
    source = item.source
    return _IndependentRequestKey(
        (
            source.connector_id,
            source.query_signature,
            source.authentication_subject,
            source.scope_schema_version,
            source.adapter_version,
            source.semantic_normalization_version,
            source.request_serialization_version,
        ),
        item.cell,
        item.cursor,
        item.snapshot_id,
    )


@lru_cache(maxsize=65536)
def _payload_key_from_spec(payload: str) -> _IndependentRequestKey:
    try:
        value = json.loads(payload)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("invalid request payload") from error
    expected_top = {
        "adapter_version",
        "authentication_subject",
        "connector_id",
        "cursor",
        "filters",
        "operation",
        "semantic_normalization_version",
        "request_serialization_version",
        "scope_schema_version",
        "snapshot_id",
    }
    if not isinstance(value, dict) or set(value) != expected_top:
        raise ValueError("invalid request payload schema")
    filters = value["filters"]
    if not isinstance(filters, dict) or set(filters) != {
        "archive_state",
        "entity",
        "time_bucket",
    }:
        raise ValueError("invalid request filter schema")
    strings = (
        "adapter_version",
        "authentication_subject",
        "connector_id",
        "operation",
        "semantic_normalization_version",
        "request_serialization_version",
        "scope_schema_version",
        "snapshot_id",
    )
    if any(not isinstance(value[name], str) or not value[name] for name in strings):
        raise ValueError("invalid request string field")
    if any(
        not isinstance(filters[name], str) or not filters[name]
        for name in ("archive_state", "entity", "time_bucket")
    ):
        raise ValueError("invalid request filter field")
    cursor = value["cursor"]
    if not isinstance(cursor, (str, int)) or isinstance(cursor, bool):
        raise ValueError("invalid request cursor")
    if json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) != payload:
        raise ValueError("request payload is not canonical")
    return _IndependentRequestKey(
        (
            value["connector_id"],
            value["operation"],
            value["authentication_subject"],
            value["scope_schema_version"],
            value["adapter_version"],
            value["semantic_normalization_version"],
            value["request_serialization_version"],
        ),
        ScopeCell(
            filters["entity"],
            filters["time_bucket"],
            filters["archive_state"],
        ),
        cursor,
        value["snapshot_id"],
    )


def _semantic_source_matches(
    left: tuple[str, ...], right: tuple[str, ...]
) -> bool:
    return left[:3] == right[:3]


def _representation_matches(
    left: tuple[str, ...], right: tuple[str, ...]
) -> bool:
    return left[3:] == right[3:]


def _semantically_targets_claim(
    key: _IndependentRequestKey, claim: Claim
) -> bool:
    claim_source = _source_fields_from_claim(claim)
    return (
        _semantic_source_matches(key.source_fields, claim_source)
        and key.snapshot_id == claim.snapshot_id
        and key.cell in claim.scope
    )


def _preflight_from_spec(
    claim: Claim,
    observations: Sequence[Observation],
) -> _IndependentPreflight:
    audited: list[Observation] = []
    conflicts: list[Observation] = []
    for item in observations:
        audited.append(item)
        if not item.attested:
            conflicts.append(item)
            continue
        if (
            not item.response_commitment
            or item.response_commitment != _response_commitment_from_spec(item)
        ):
            conflicts.append(item)
            continue
        outer = _metadata_key(item)
        try:
            inner = _payload_key_from_spec(item.request_payload)
        except ValueError:
            conflicts.append(item)
            continue
        if outer != inner or any(record.cell != inner.cell for record in item.records):
            conflicts.append(item)
            continue
        if not _representation_matches(
            inner.source_fields, _source_fields_from_claim(claim)
        ):
            conflicts.append(item)
    return _IndependentPreflight(tuple(audited), tuple(conflicts))


def _request_binding_digest_from_spec(claim: Claim) -> str:
    encoded = json.dumps(
        {
            "binding_rule": "homogeneous-attested-response-commitment-v5",
            "source": {
                "adapter_version": claim.source.adapter_version,
                "authentication_subject": claim.source.authentication_subject,
                "connector_id": claim.source.connector_id,
                "query_signature": claim.source.query_signature,
                "semantic_normalization_version": claim.source.semantic_normalization_version,
                "request_serialization_version": claim.source.request_serialization_version,
                "scope_schema_version": claim.source.scope_schema_version,
            },
            "scope": [cell.key for cell in sorted(claim.scope)],
            "snapshot_id": claim.snapshot_id,
            "initial_cursor": claim.initial_cursor,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _trace_from_spec(
    claim: Claim,
    cell: ScopeCell,
    observations: Sequence[Observation],
    preflight: _IndependentPreflight,
) -> _IndependentTrace:
    if preflight.conflicts:
        return _IndependentTrace(
            False,
            (),
            (),
            preflight.audit_digests,
            False,
            True,
        )
    candidates = [
        item
        for item in preflight.audited
        if _semantic_source_matches(
            _payload_key_from_spec(item.request_payload).source_fields,
            _source_fields_from_claim(claim),
        )
        and _representation_matches(
            _payload_key_from_spec(item.request_payload).source_fields,
            _source_fields_from_claim(claim),
        )
        and _payload_key_from_spec(item.request_payload).snapshot_id
        == claim.snapshot_id
        and _payload_key_from_spec(item.request_payload).cell == cell
    ]
    source_bound = candidates
    blocked = any(
        item.status == "permission_denied" or not item.permission_complete
        for item in source_bound
    )
    invalid_requests = [
        item
        for item in source_bound
        if item.status == "ok"
        and item.attested
        and item.permission_complete
        and item.snapshot_id == claim.snapshot_id
        and item.request_payload != _request_payload_from_spec(claim, cell, item.cursor)
    ]
    evidence_digests = tuple(sorted(item.digest for item in candidates))
    if invalid_requests:
        return _IndependentTrace(False, (), (), evidence_digests, blocked, True)
    valid = [
        item
        for item in source_bound
        if item.status == "ok"
        and item.attested
        and item.permission_complete
        and item.snapshot_id == claim.snapshot_id
        and item.request_payload == _request_payload_from_spec(claim, cell, item.cursor)
    ]
    if any(record.cell != item.cell for item in valid for record in item.records):
        return _IndependentTrace(False, (), (), evidence_digests, blocked, True)

    by_cursor: dict[Cursor, list[Observation]] = {}
    for item in valid:
        by_cursor.setdefault(item.cursor, []).append(item)
    if any(len({item.digest for item in group}) > 1 for group in by_cursor.values()):
        return _IndependentTrace(False, (), (), evidence_digests, blocked, True)
    pages = {
        cursor: sorted(group, key=lambda item: item.digest)[0]
        for cursor, group in by_cursor.items()
    }

    cursor = claim.initial_cursor
    seen: set[Cursor] = set()
    chain: list[Observation] = []
    while True:
        if cursor in seen:
            return _IndependentTrace(
                False,
                (),
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                True,
            )
        page = pages.get(cursor)
        if page is None:
            return _IndependentTrace(
                False,
                tuple(chain),
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
            )
        seen.add(cursor)
        chain.append(page)
        if page.silently_truncated:
            return _IndependentTrace(
                False,
                tuple(chain),
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
            )
        if page.next_cursor is None:
            if set(pages) - seen:
                return _IndependentTrace(
                    False,
                    (),
                    tuple(item.digest for item in chain),
                    evidence_digests,
                    blocked,
                    True,
                )
            return _IndependentTrace(
                True,
                tuple(chain),
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
            )
        cursor = page.next_cursor


def _expected_reason(
    traces: dict[ScopeCell, _IndependentTrace],
    missing: tuple[ScopeCell, ...],
) -> str:
    if any(traces[cell].conflicted for cell in missing):
        return "evidence conflict prevents a source-bound page-chain proof"
    if any(traces[cell].blocked for cell in missing):
        return "some claim cells are permission-blocked"
    return "fetch the missing source-bound page chains for the exact joint cells"


def _base_fields_valid(claim: Claim, certificate: CoverageCertificate) -> bool:
    return (
        certificate.schema_version == 8
        and certificate.claim_digest == claim.digest
        and certificate.source_identity_digest == claim.source.digest
        and certificate.request_binding_digest
        == _request_binding_digest_from_spec(claim)
        and certificate.snapshot_id == claim.snapshot_id
    )


def verify_certificate_independently(
    claim: Claim,
    observations: Sequence[Observation],
    certificate: CoverageCertificate,
) -> bool:
    """Check certificate soundness without calling the production evaluator or tracer."""

    if not _base_fields_valid(claim, certificate):
        return False
    preflight = _preflight_from_spec(claim, observations)
    if certificate.audit_observation_digests != preflight.audit_digests:
        return False
    if preflight.conflicts:
        missing = tuple(sorted(claim.scope))
        return (
            certificate.decision == "UNKNOWN"
            and certificate.proof_type == "insufficient_coverage"
            and certificate.observation_digests == preflight.audit_digests
            and certificate.covered_cells == ()
            and certificate.missing_cells == missing
            and certificate.witness_record_id is None
            and certificate.reason
            == "evidence conflict prevents a source-bound page-chain proof"
        )
    traces = {
        cell: _trace_from_spec(claim, cell, observations, preflight)
        for cell in sorted(claim.scope)
    }
    covered = tuple(cell for cell in sorted(traces) if traces[cell].complete)
    missing = tuple(cell for cell in sorted(traces) if not traces[cell].complete)
    if certificate.covered_cells != covered or certificate.missing_cells != missing:
        return False

    if certificate.proof_type in {"positive_witness", "counterexample_witness"}:
        candidates: list[tuple[Observation, object, str]] = []
        for cell in sorted(traces):
            trace = traces[cell]
            if trace.conflicted:
                continue
            for observation in sorted(
                trace.witness_pages,
                key=lambda item: (_cursor_key(item.cursor), item.digest),
            ):
                for record in observation.records:
                    if record.cell != observation.cell or record.cell not in claim.scope:
                        continue
                    decision = claim.witness_for(record)
                    if decision is not None:
                        candidates.append((observation, record, decision))
        if not candidates:
            return False
        observation, record, decision = candidates[0]
        expected_proof = (
            "positive_witness" if decision == "TRUE" else "counterexample_witness"
        )
        return (
            certificate.decision == decision
            and certificate.proof_type == expected_proof
            and certificate.observation_digests == (observation.digest,)
            and certificate.witness_record_id == record.record_id
            and certificate.reason
            == "a source-bound in-scope attested record decides the claim"
        )

    if certificate.proof_type == "joint_scope_coverage":
        if missing:
            return False
        chain_digests = tuple(
            digest
            for cell in sorted(traces)
            for digest in traces[cell].chain_digests
        )
        return (
            certificate.decision == claim.coverage_decision
            and certificate.observation_digests == chain_digests
            and certificate.witness_record_id is None
            and certificate.reason
            == "complete source-bound page chains cover the exact joint claim scope"
        )

    if certificate.proof_type == "insufficient_coverage":
        if not missing:
            return False
        evidence_digests = tuple(
            digest
            for cell in sorted(traces)
            for digest in traces[cell].evidence_digests
        )
        return (
            certificate.decision == "UNKNOWN"
            and certificate.observation_digests == evidence_digests
            and certificate.witness_record_id is None
            and certificate.reason == _expected_reason(traces, missing)
        )

    return False
