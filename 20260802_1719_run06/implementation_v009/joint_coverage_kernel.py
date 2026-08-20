from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import asdict, dataclass, replace
from functools import cached_property, lru_cache
from typing import Iterable, Literal, Sequence


Quantifier = Literal["exists", "forall"]
Decision = Literal["TRUE", "FALSE", "UNKNOWN"]
Cursor = str | int

RSA_SHA256_DIGEST_INFO_PREFIX = bytes.fromhex(
    "3031300d060960864801650304020105000420"
)
DEFAULT_ATTESTATION_SCHEME = "rsa-pkcs1v15-sha256-v1"
DEFAULT_ATTESTATION_KEY_ID = "simulation-fixture-rsa-v009"
DEFAULT_ATTESTATION_PUBLIC_KEY_N_HEX = (
    "c3f9e41577a994bc979011dc1be02c75aa7756e724bd527175702330f9ec4553"
    "9bce355915b968d3eb9bb36e756acd5893380774d213e6e942ad6b24f9d8792a"
    "ba1847000db41e755c9c021684bf171772bd4687e9e5859e0e440814764fb669c"
    "98061604fd3103110c149a23e9c2e82acc859c3414d8cc36ffacc181b399bc91e"
    "85dea0706b7fac87e26d9d1b44f4288f78150e2ae4adcc27b07e070ad0944e66"
    "a911654106973777d8db37aa5f4ab1da87547714c35a78b6ddd9209c604184e4"
    "e2baa6442d71027646744d9c04e35240df75d8c892554cfcb23660adb9a79c96"
    "75d42f9e890aefc8eaaa93af66d7f8fdddfcf33664bc7d5cc353e8d0a9281b"
)
DEFAULT_ATTESTATION_PUBLIC_KEY_E = 65537
DEFAULT_DECODER_DIGEST = (
    "4d5e37ff162e3aa5e0e1ac6629d0dc9fd557415638b029624e8786c302ef4f63"
)


def _canonical_digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _cursor_sort_key(cursor: Cursor) -> tuple[str, str]:
    return type(cursor).__name__, str(cursor)


@dataclass(frozen=True, order=True)
class ScopeCell:
    """One indivisible cell in the joint entity x time x archive scope."""

    entity: str
    time_bucket: str
    archive_state: str
    semantic_id: str = ""

    def __post_init__(self) -> None:
        if not self.entity or not self.time_bucket or not self.archive_state:
            raise ValueError("scope cell coordinates must be non-empty")

    @property
    def key(self) -> str:
        return f"{self.entity}|{self.time_bucket}|{self.archive_state}"

    @property
    def semantic_key(self) -> str:
        return self.semantic_id or self.key


@dataclass(frozen=True, order=True)
class SourceIdentity:
    """Semantic source fields plus representation metadata for one proof chain."""

    connector_id: str
    query_signature: str
    authentication_subject: str
    scope_schema_version: str
    adapter_version: str
    semantic_normalization_version: str
    request_serialization_version: str
    attestation_scheme: str = DEFAULT_ATTESTATION_SCHEME
    attestation_key_id: str = DEFAULT_ATTESTATION_KEY_ID
    attestation_public_key_n_hex: str = DEFAULT_ATTESTATION_PUBLIC_KEY_N_HEX
    attestation_public_key_e: int = DEFAULT_ATTESTATION_PUBLIC_KEY_E
    decoder_digest: str = DEFAULT_DECODER_DIGEST

    def __post_init__(self) -> None:
        if not all(
            (
                self.connector_id,
                self.query_signature,
                self.authentication_subject,
                self.scope_schema_version,
                self.adapter_version,
                self.semantic_normalization_version,
                self.request_serialization_version,
                self.attestation_scheme,
                self.attestation_key_id,
                self.attestation_public_key_n_hex,
                self.decoder_digest,
            )
        ):
            raise ValueError("source identity fields must all be non-empty")
        try:
            modulus = int(self.attestation_public_key_n_hex, 16)
        except ValueError as error:
            raise ValueError("attestation RSA modulus must be hexadecimal") from error
        if modulus.bit_length() < 2048:
            raise ValueError("attestation RSA modulus must be at least 2048 bits")
        if self.attestation_public_key_e < 3 or self.attestation_public_key_e % 2 == 0:
            raise ValueError("attestation RSA exponent must be an odd integer")
        if len(self.decoder_digest) != 64:
            raise ValueError("decoder digest must be a SHA-256 hexadecimal digest")

    @cached_property
    def digest(self) -> str:
        return _canonical_digest(asdict(self))


@dataclass(frozen=True, order=True)
class RequestKey:
    """The authoritative request identity parsed from one canonical payload."""

    source: SourceIdentity
    cell: ScopeCell
    cursor: Cursor
    snapshot_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.cursor, (str, int)) or isinstance(self.cursor, bool):
            raise ValueError("request cursor must be a string or integer")
        if not self.snapshot_id:
            raise ValueError("request snapshot_id must not be empty")

    @cached_property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "source": asdict(self.source),
                "cell": self.cell.key,
                "cursor": self.cursor,
                "snapshot_id": self.snapshot_id,
            }
        )


def canonical_request_payload(
    source: SourceIdentity,
    cell: ScopeCell,
    cursor: Cursor,
    snapshot_id: str,
) -> str:
    """Serialize the exact per-page request fields that bind a response to one cell."""

    return json.dumps(
        {
            "adapter_version": source.adapter_version,
            "attestation_key_id": source.attestation_key_id,
            "attestation_public_key_e": source.attestation_public_key_e,
            "attestation_public_key_n_hex": source.attestation_public_key_n_hex,
            "attestation_scheme": source.attestation_scheme,
            "authentication_subject": source.authentication_subject,
            "connector_id": source.connector_id,
            "cursor": cursor,
            "decoder_digest": source.decoder_digest,
            "filters": {
                "archive_state": cell.archive_state,
                "entity": cell.entity,
                "semantic_cell_id": cell.semantic_key,
                "time_bucket": cell.time_bucket,
            },
            "operation": source.query_signature,
            "semantic_normalization_version": source.semantic_normalization_version,
            "request_serialization_version": source.request_serialization_version,
            "scope_schema_version": source.scope_schema_version,
            "snapshot_id": snapshot_id,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


@lru_cache(maxsize=65536)
def parse_canonical_request_payload(payload: str) -> RequestKey:
    """Strictly parse an exact canonical payload into its authoritative key."""

    try:
        value = json.loads(payload)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("request payload is not valid JSON") from error
    if not isinstance(value, dict) or set(value) != {
        "adapter_version",
        "attestation_key_id",
        "attestation_public_key_e",
        "attestation_public_key_n_hex",
        "attestation_scheme",
        "authentication_subject",
        "connector_id",
        "cursor",
        "decoder_digest",
        "filters",
        "operation",
        "semantic_normalization_version",
        "request_serialization_version",
        "scope_schema_version",
        "snapshot_id",
    }:
        raise ValueError("request payload has an unexpected top-level schema")
    filters = value["filters"]
    if not isinstance(filters, dict) or set(filters) != {
        "archive_state",
        "entity",
        "semantic_cell_id",
        "time_bucket",
    }:
        raise ValueError("request payload has an unexpected filter schema")
    scalar_names = (
        "adapter_version",
        "attestation_key_id",
        "attestation_public_key_n_hex",
        "attestation_scheme",
        "authentication_subject",
        "connector_id",
        "decoder_digest",
        "operation",
        "semantic_normalization_version",
        "request_serialization_version",
        "scope_schema_version",
        "snapshot_id",
    )
    if any(
        not isinstance(value[name], str) or not value[name]
        for name in scalar_names
    ) or any(
        not isinstance(filters[name], str) or not filters[name]
        for name in ("archive_state", "entity", "semantic_cell_id", "time_bucket")
    ):
        raise ValueError("request payload string fields must all be non-empty")
    cursor = value["cursor"]
    if not isinstance(cursor, (str, int)) or isinstance(cursor, bool):
        raise ValueError("request payload cursor must be a string or integer")
    exponent = value["attestation_public_key_e"]
    if not isinstance(exponent, int) or isinstance(exponent, bool):
        raise ValueError("request payload RSA exponent must be an integer")
    if json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) != payload:
        raise ValueError("request payload is not in the exact canonical form")
    return RequestKey(
        SourceIdentity(
            value["connector_id"],
            value["operation"],
            value["authentication_subject"],
            value["scope_schema_version"],
            value["adapter_version"],
            value["semantic_normalization_version"],
            value["request_serialization_version"],
            value["attestation_scheme"],
            value["attestation_key_id"],
            value["attestation_public_key_n_hex"],
            exponent,
            value["decoder_digest"],
        ),
        ScopeCell(
            filters["entity"],
            filters["time_bucket"],
            filters["archive_state"],
            filters["semantic_cell_id"],
        ),
        cursor,
        value["snapshot_id"],
    )


def request_payload_digest(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def canonical_response_commitment(
    request_payload: str,
    records: Sequence[Record],
    next_cursor: Cursor | None,
    status: str,
    permission_complete: bool,
    silently_truncated: bool,
) -> str:
    """Commit the independently attested, complete decoded response semantics."""

    return _canonical_digest(
        {
            "schema_version": 1,
            "request_payload_digest": request_payload_digest(request_payload),
            "records": [
                {
                    "record_id": record.record_id,
                    "cell": record.cell.key,
                    "semantic_cell_id": record.cell.semantic_key,
                    "matches_target": record.matches_target,
                    "compliant": record.compliant,
                }
                for record in records
            ],
            "next_cursor": next_cursor,
            "status": status,
            "permission_complete": permission_complete,
            "silently_truncated": silently_truncated,
        }
    )


def canonical_page_attestation_payload(
    source: SourceIdentity,
    request_payload: str,
    raw_response_sha256: str,
    response_commitment: str,
    session_id: str,
    sequence_index: int,
    previous_attestation_digest: str,
    cursor: Cursor,
    next_cursor: Cursor | None,
    status: str,
    permission_complete: bool,
    silently_truncated: bool,
) -> str:
    """Canonical signed envelope issued before the production decoder is trusted."""

    return json.dumps(
        {
            "schema_version": 1,
            "attestation_scheme": source.attestation_scheme,
            "attestation_key_id": source.attestation_key_id,
            "source_identity_digest": source.digest,
            "decoder_digest": source.decoder_digest,
            "request_payload_digest": request_payload_digest(request_payload),
            "raw_response_sha256": raw_response_sha256,
            "response_commitment": response_commitment,
            "session_id": session_id,
            "sequence_index": sequence_index,
            "previous_attestation_digest": previous_attestation_digest,
            "cursor": cursor,
            "next_cursor": next_cursor,
            "status": status,
            "permission_complete": permission_complete,
            "silently_truncated": silently_truncated,
            "attested": True,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


@lru_cache(maxsize=65536)
def verify_rsa_pkcs1v15_sha256(
    message: str,
    signature_hex: str,
    modulus_hex: str,
    exponent: int,
) -> bool:
    """Verify a PKCS#1 v1.5 SHA-256 signature with only public key material."""

    try:
        modulus = int(modulus_hex, 16)
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return False
    width = (modulus.bit_length() + 7) // 8
    if len(signature) != width:
        return False
    digest_info = RSA_SHA256_DIGEST_INFO_PREFIX + hashlib.sha256(
        message.encode("utf-8")
    ).digest()
    padding_length = width - len(digest_info) - 3
    if padding_length < 8:
        return False
    expected = b"\x00\x01" + b"\xff" * padding_length + b"\x00" + digest_info
    recovered = pow(int.from_bytes(signature, "big"), exponent, modulus).to_bytes(
        width, "big"
    )
    return hmac.compare_digest(recovered, expected)


def signed_page_attestation_digest(payload: str, signature_hex: str) -> str:
    return _canonical_digest({"payload": payload, "signature_hex": signature_hex})


@dataclass(frozen=True)
class Record:
    record_id: str
    cell: ScopeCell
    matches_target: bool
    compliant: bool


@dataclass(frozen=True)
class Claim:
    claim_id: str
    quantifier: Quantifier
    predicate: Literal["matches_target", "compliant"]
    scope: tuple[ScopeCell, ...]
    snapshot_id: str
    source: SourceIdentity
    text: str = ""
    initial_cursor: Cursor = 0

    def __post_init__(self) -> None:
        if not self.scope:
            raise ValueError("claim scope must not be empty")
        if len({cell.semantic_key for cell in self.scope}) != len(self.scope):
            raise ValueError("claim scope contains duplicate semantic joint cells")
        if not self.snapshot_id:
            raise ValueError("claim snapshot_id must not be empty")
        if not isinstance(self.initial_cursor, (str, int)) or isinstance(
            self.initial_cursor, bool
        ):
            raise ValueError("claim initial_cursor must be a string or integer")

    @cached_property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "claim_id": self.claim_id,
                "quantifier": self.quantifier,
                "predicate": self.predicate,
                "scope": [
                    {"raw": cell.key, "semantic": cell.semantic_key}
                    for cell in sorted(self.scope)
                ],
                "snapshot_id": self.snapshot_id,
                "source": asdict(self.source),
                "text": self.text,
                "initial_cursor": self.initial_cursor,
            }
        )

    @cached_property
    def request_binding_digest(self) -> str:
        return _canonical_digest(
            {
                "binding_rule": "signed-session-manifest-chain-v6",
                "source": asdict(self.source),
                "scope": [
                    {"raw": cell.key, "semantic": cell.semantic_key}
                    for cell in sorted(self.scope)
                ],
                "snapshot_id": self.snapshot_id,
                "initial_cursor": self.initial_cursor,
            }
        )

    def predicate_holds(self, record: Record) -> bool:
        return bool(getattr(record, self.predicate))

    def witness_for(self, record: Record) -> Decision | None:
        holds = self.predicate_holds(record)
        if self.quantifier == "exists" and holds:
            return "TRUE"
        if self.quantifier == "forall" and not holds:
            return "FALSE"
        return None

    @property
    def coverage_decision(self) -> Decision:
        return "FALSE" if self.quantifier == "exists" else "TRUE"


@dataclass(frozen=True)
class Observation:
    observation_id: str
    connector_id: str
    cell: ScopeCell
    cursor: Cursor
    next_cursor: Cursor | None
    records: tuple[Record, ...]
    snapshot_id: str
    status: Literal["ok", "permission_denied", "error"] = "ok"
    attested: bool = True
    permission_complete: bool = True
    silently_truncated: bool = False
    query_signature: str = ""
    authentication_subject: str = ""
    scope_schema_version: str = ""
    adapter_version: str = ""
    semantic_normalization_version: str = ""
    request_serialization_version: str = ""
    attestation_scheme: str = DEFAULT_ATTESTATION_SCHEME
    attestation_key_id: str = DEFAULT_ATTESTATION_KEY_ID
    attestation_public_key_n_hex: str = DEFAULT_ATTESTATION_PUBLIC_KEY_N_HEX
    attestation_public_key_e: int = DEFAULT_ATTESTATION_PUBLIC_KEY_E
    decoder_digest: str = DEFAULT_DECODER_DIGEST
    request_payload: str = ""
    response_commitment: str = ""
    raw_response_sha256: str = ""
    attestation_session_id: str = ""
    attestation_sequence_index: int = 0
    previous_attestation_digest: str = ""
    attestation_signature_hex: str = ""

    def __post_init__(self) -> None:
        SourceIdentity(
            self.connector_id,
            self.query_signature,
            self.authentication_subject,
            self.scope_schema_version,
            self.adapter_version,
            self.semantic_normalization_version,
            self.request_serialization_version,
            self.attestation_scheme,
            self.attestation_key_id,
            self.attestation_public_key_n_hex,
            self.attestation_public_key_e,
            self.decoder_digest,
        )
        if not self.snapshot_id:
            raise ValueError("observation snapshot_id must not be empty")
        if not isinstance(self.cursor, (str, int)) or isinstance(self.cursor, bool):
            raise ValueError("observation cursor must be a string or integer")
        if self.next_cursor is not None and (
            not isinstance(self.next_cursor, (str, int))
            or isinstance(self.next_cursor, bool)
        ):
            raise ValueError("observation next_cursor must be a string or integer")
        if self.attestation_sequence_index < 0:
            raise ValueError("attestation sequence index must be non-negative")

    @cached_property
    def source(self) -> SourceIdentity:
        return SourceIdentity(
            self.connector_id,
            self.query_signature,
            self.authentication_subject,
            self.scope_schema_version,
            self.adapter_version,
            self.semantic_normalization_version,
            self.request_serialization_version,
            self.attestation_scheme,
            self.attestation_key_id,
            self.attestation_public_key_n_hex,
            self.attestation_public_key_e,
            self.decoder_digest,
        )

    @cached_property
    def metadata_request_key(self) -> RequestKey:
        return RequestKey(self.source, self.cell, self.cursor, self.snapshot_id)

    @cached_property
    def payload_request_key(self) -> RequestKey:
        return parse_canonical_request_payload(self.request_payload)

    @cached_property
    def expected_response_commitment(self) -> str:
        return canonical_response_commitment(
            self.request_payload,
            self.records,
            self.next_cursor,
            self.status,
            self.permission_complete,
            self.silently_truncated,
        )

    @cached_property
    def expected_attestation_payload(self) -> str:
        return canonical_page_attestation_payload(
            self.source,
            self.request_payload,
            self.raw_response_sha256,
            self.response_commitment,
            self.attestation_session_id,
            self.attestation_sequence_index,
            self.previous_attestation_digest,
            self.cursor,
            self.next_cursor,
            self.status,
            self.permission_complete,
            self.silently_truncated,
        )

    @cached_property
    def attestation_digest(self) -> str:
        return signed_page_attestation_digest(
            self.expected_attestation_payload,
            self.attestation_signature_hex,
        )

    @cached_property
    def pre_attestation_digest(self) -> str:
        return _canonical_digest(
            {
                "observation_id": self.observation_id,
                "source": asdict(self.source),
                "request_payload": self.request_payload,
                "request_payload_digest": request_payload_digest(self.request_payload),
                "cell": self.cell.key,
                "cursor": self.cursor,
                "next_cursor": self.next_cursor,
                "records": [
                    {
                        "record_id": record.record_id,
                        "cell": record.cell.key,
                        "semantic_cell_id": record.cell.semantic_key,
                        "matches_target": record.matches_target,
                        "compliant": record.compliant,
                    }
                    for record in self.records
                ],
                "snapshot_id": self.snapshot_id,
                "status": self.status,
                "attested": self.attested,
                "permission_complete": self.permission_complete,
                "silently_truncated": self.silently_truncated,
            }
        )

    @cached_property
    def v008_projection_digest(self) -> str:
        """Project a v009 observation to the exact v008 observation digest.

        This projection is used only for paired clean-input regression.  It
        removes the v009 semantic-cell and asymmetric-attestation coordinates
        while retaining every field that v008 committed.
        """

        legacy_source = {
            "connector_id": self.connector_id,
            "query_signature": self.query_signature,
            "authentication_subject": self.authentication_subject,
            "scope_schema_version": self.scope_schema_version,
            "adapter_version": self.adapter_version,
            "semantic_normalization_version": self.semantic_normalization_version,
            "request_serialization_version": self.request_serialization_version,
        }
        legacy_request_payload = json.dumps(
            {
                "adapter_version": self.adapter_version,
                "authentication_subject": self.authentication_subject,
                "connector_id": self.connector_id,
                "cursor": self.cursor,
                "filters": {
                    "archive_state": self.cell.archive_state,
                    "entity": self.cell.entity,
                    "time_bucket": self.cell.time_bucket,
                },
                "operation": self.query_signature,
                "semantic_normalization_version": self.semantic_normalization_version,
                "request_serialization_version": self.request_serialization_version,
                "scope_schema_version": self.scope_schema_version,
                "snapshot_id": self.snapshot_id,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        legacy_records = [
            {
                "record_id": record.record_id,
                "cell": record.cell.key,
                "matches_target": record.matches_target,
                "compliant": record.compliant,
            }
            for record in self.records
        ]
        legacy_response_commitment = _canonical_digest(
            {
                "schema_version": 1,
                "request_payload_digest": hashlib.sha256(
                    legacy_request_payload.encode("utf-8")
                ).hexdigest(),
                "records": legacy_records,
                "next_cursor": self.next_cursor,
                "status": self.status,
                "permission_complete": self.permission_complete,
                "silently_truncated": self.silently_truncated,
            }
        )
        legacy_pre_attestation_digest = _canonical_digest(
            {
                "observation_id": self.observation_id,
                "source": legacy_source,
                "request_payload": legacy_request_payload,
                "request_payload_digest": hashlib.sha256(
                    legacy_request_payload.encode("utf-8")
                ).hexdigest(),
                "cell": self.cell.key,
                "cursor": self.cursor,
                "next_cursor": self.next_cursor,
                "records": legacy_records,
                "snapshot_id": self.snapshot_id,
                "status": self.status,
                "attested": self.attested,
                "permission_complete": self.permission_complete,
                "silently_truncated": self.silently_truncated,
            }
        )
        return _canonical_digest(
            {
                "pre_attestation_digest": legacy_pre_attestation_digest,
                "response_commitment": legacy_response_commitment,
            }
        )

    @cached_property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "pre_attestation_digest": self.pre_attestation_digest,
                "response_commitment": self.response_commitment,
                "raw_response_sha256": self.raw_response_sha256,
                "attestation_payload_digest": hashlib.sha256(
                    self.expected_attestation_payload.encode("utf-8")
                ).hexdigest(),
                "attestation_signature_hex": self.attestation_signature_hex,
            }
        )


@dataclass(frozen=True)
class RepairObligation:
    missing_cells: tuple[ScopeCell, ...]
    next_cursors: tuple[tuple[ScopeCell, Cursor], ...]
    blocked_cells: tuple[ScopeCell, ...]
    conflicted_cells: tuple[ScopeCell, ...]
    reason: str


@dataclass(frozen=True)
class CoverageCertificate:
    schema_version: int
    claim_digest: str
    source_identity_digest: str
    request_binding_digest: str
    decision: Decision
    proof_type: Literal[
        "positive_witness",
        "counterexample_witness",
        "joint_scope_coverage",
        "insufficient_coverage",
    ]
    audit_observation_digests: tuple[str, ...]
    observation_digests: tuple[str, ...]
    covered_cells: tuple[ScopeCell, ...]
    missing_cells: tuple[ScopeCell, ...]
    witness_record_id: str | None
    snapshot_id: str
    reason: str

    @property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "schema_version": self.schema_version,
                "claim_digest": self.claim_digest,
                "source_identity_digest": self.source_identity_digest,
                "request_binding_digest": self.request_binding_digest,
                "decision": self.decision,
                "proof_type": self.proof_type,
                "audit_observation_digests": list(
                    self.audit_observation_digests
                ),
                "observation_digests": list(self.observation_digests),
                "covered_cells": [cell.key for cell in self.covered_cells],
                "missing_cells": [cell.key for cell in self.missing_cells],
                "witness_record_id": self.witness_record_id,
                "snapshot_id": self.snapshot_id,
                "reason": self.reason,
            }
        )


@dataclass(frozen=True)
class Evaluation:
    decision: Decision
    certificate: CoverageCertificate
    obligation: RepairObligation | None


@dataclass(frozen=True)
class CellTrace:
    cell: ScopeCell
    complete: bool
    witness_pages: tuple[Observation, ...]
    next_cursor: Cursor
    chain_digests: tuple[str, ...]
    evidence_digests: tuple[str, ...]
    blocked: bool
    conflicted: bool
    reason: str


@dataclass(frozen=True)
class ObservationPreflight:
    audited_observations: tuple[Observation, ...]
    conflicting_observations: tuple[Observation, ...]

    @property
    def audit_digests(self) -> tuple[str, ...]:
        return tuple(sorted(item.digest for item in self.audited_observations))


_SEMANTIC_SOURCE_COORDINATES = (
    "connector_id",
    "query_signature",
    "authentication_subject",
)


_REPRESENTATION_COORDINATES = (
    "scope_schema_version",
    "adapter_version",
    "semantic_normalization_version",
    "request_serialization_version",
    "attestation_scheme",
    "attestation_key_id",
    "attestation_public_key_n_hex",
    "attestation_public_key_e",
    "decoder_digest",
)


@dataclass(frozen=True)
class PayloadParseState:
    """A total parse state: either one valid canonical key or one explicit error."""

    key: RequestKey | None
    error: str | None

    @property
    def valid(self) -> bool:
        return self.key is not None and self.error is None


@lru_cache(maxsize=65536)
def _payload_parse_state(payload: str) -> PayloadParseState:
    try:
        return PayloadParseState(parse_canonical_request_payload(payload), None)
    except ValueError as error:
        return PayloadParseState(None, str(error))


def _semantic_source_matches(left: SourceIdentity, right: SourceIdentity) -> bool:
    return all(
        getattr(left, name) == getattr(right, name)
        for name in _SEMANTIC_SOURCE_COORDINATES
    )


def _representation_matches(left: SourceIdentity, right: SourceIdentity) -> bool:
    return all(
        getattr(left, name) == getattr(right, name)
        for name in _REPRESENTATION_COORDINATES
    )


def _semantically_targets_claim(key: RequestKey, claim: Claim) -> bool:
    """Semantic relevance excludes representation versions by construction."""

    return (
        _semantic_source_matches(key.source, claim.source)
        and key.snapshot_id == claim.snapshot_id
        and any(key.cell.semantic_key == cell.semantic_key for cell in claim.scope)
    )


def _request_keys_equivalent(left: RequestKey, right: RequestKey) -> bool:
    return (
        left.source == right.source
        and left.cell.key == right.cell.key
        and left.cell.semantic_key == right.cell.semantic_key
        and left.cursor == right.cursor
        and left.snapshot_id == right.snapshot_id
    )


def _preflight_observations(
    claim: Claim,
    observations: Sequence[Observation],
) -> ObservationPreflight:
    """Validate every retained attested input before semantic routing."""

    audited: list[Observation] = []
    conflicts: list[Observation] = []
    for item in observations:
        # Every received observation is committed.  Unattested inputs fail closed
        # instead of disappearing from both the preflight and the certificate.
        audited.append(item)
        if not item.attested:
            conflicts.append(item)
            continue
        if (
            not item.response_commitment
            or item.response_commitment != item.expected_response_commitment
        ):
            conflicts.append(item)
            continue
        if (
            not item.raw_response_sha256
            or len(item.raw_response_sha256) != 64
            or not item.attestation_session_id
            or not item.attestation_signature_hex
            or not verify_rsa_pkcs1v15_sha256(
                item.expected_attestation_payload,
                item.attestation_signature_hex,
                claim.source.attestation_public_key_n_hex,
                claim.source.attestation_public_key_e,
            )
        ):
            conflicts.append(item)
            continue
        outer = item.metadata_request_key
        payload_state = _payload_parse_state(item.request_payload)
        if not payload_state.valid:
            conflicts.append(item)
            continue
        inner = payload_state.key
        assert inner is not None
        # Internal coherence is checked globally, before relevance classification.
        if not _request_keys_equivalent(outer, inner) or any(
            record.cell.semantic_key != inner.cell.semantic_key
            for record in item.records
        ):
            conflicts.append(item)
            continue
        # Representation homogeneity is checked before query, authentication,
        # snapshot, or raw-cell routing.  This prevents a representation version
        # from changing those encodings and thereby routing its own mismatch out.
        if not _representation_matches(inner.source, claim.source):
            conflicts.append(item)
    return ObservationPreflight(tuple(audited), tuple(conflicts))


def _unknown_reason(
    traces: dict[ScopeCell, CellTrace], missing: tuple[ScopeCell, ...]
) -> str:
    if any(traces[cell].conflicted for cell in missing):
        return "evidence conflict prevents a source-bound page-chain proof"
    if any(traces[cell].blocked for cell in missing):
        return "some claim cells are permission-blocked"
    return "fetch the missing source-bound page chains for the exact joint cells"


def _request_matches_claim(item: Observation, cell: ScopeCell, claim: Claim) -> bool:
    try:
        return (
            item.metadata_request_key.source == claim.source
            and item.payload_request_key.source == claim.source
            and item.metadata_request_key.snapshot_id == claim.snapshot_id
            and item.payload_request_key.snapshot_id == claim.snapshot_id
            and item.metadata_request_key.cursor == item.cursor
            and item.payload_request_key.cursor == item.cursor
            and item.metadata_request_key.cell.semantic_key == cell.semantic_key
            and item.payload_request_key.cell.semantic_key == cell.semantic_key
        )
    except ValueError:
        return False


def _trace_cell(
    cell: ScopeCell,
    observations: Sequence[Observation],
    claim: Claim,
    preflight: ObservationPreflight | None = None,
) -> CellTrace:
    if preflight is None:
        preflight = _preflight_observations(claim, observations)
    if preflight.conflicting_observations:
        return CellTrace(
            cell,
            False,
            (),
            claim.initial_cursor,
            (),
            preflight.audit_digests,
            False,
            True,
            "global_coherence_or_representation_conflict",
        )
    candidates = [
        item
        for item in preflight.audited_observations
        if _semantic_source_matches(item.payload_request_key.source, claim.source)
        and _representation_matches(item.payload_request_key.source, claim.source)
        and item.payload_request_key.snapshot_id == claim.snapshot_id
        and item.payload_request_key.cell.semantic_key == cell.semantic_key
    ]
    expected_source = candidates
    blocked = any(
        item.status == "permission_denied" or not item.permission_complete
        for item in expected_source
    )
    invalid_request_pages = [
        item
        for item in expected_source
        if item.status == "ok"
        and item.attested
        and item.permission_complete
        and item.snapshot_id == claim.snapshot_id
        and not _request_matches_claim(item, cell, claim)
    ]
    evidence_digests = tuple(sorted(item.digest for item in candidates))
    if invalid_request_pages:
        return CellTrace(
            cell,
            False,
            (),
            claim.initial_cursor,
            (),
            evidence_digests,
            blocked,
            True,
            "request_binding_mismatch",
        )
    compatible = [
        item
        for item in expected_source
        if item.status == "ok"
        and item.attested
        and item.permission_complete
        and item.snapshot_id == claim.snapshot_id
        and _request_matches_claim(item, cell, claim)
    ]

    if any(
        record.cell.semantic_key != item.cell.semantic_key
        for item in compatible
        for record in item.records
    ):
        return CellTrace(
            cell,
            False,
            (),
            claim.initial_cursor,
            (),
            evidence_digests,
            blocked,
            True,
            "record_cell_mismatch",
        )

    grouped: dict[Cursor, list[Observation]] = {}
    for item in compatible:
        grouped.setdefault(item.cursor, []).append(item)
    for cursor, group in grouped.items():
        if len(group) > 1:
            return CellTrace(
                cell,
                False,
                (),
                cursor,
                (),
                evidence_digests,
                blocked,
                True,
                "conflicting_cursor_pages",
            )

    pages = {
        cursor: sorted(group, key=lambda item: item.digest)[0]
        for cursor, group in grouped.items()
    }
    cursor: Cursor = claim.initial_cursor
    seen: set[Cursor] = set()
    chain: list[Observation] = []
    session_id: str | None = None
    while True:
        if cursor in seen:
            return CellTrace(
                cell,
                False,
                (),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                True,
                "cursor_cycle",
            )
        page = pages.get(cursor)
        if page is None:
            if chain:
                reason = "missing_page"
            elif candidates and not expected_source:
                reason = "source_identity_mismatch"
            elif expected_source and not compatible:
                reason = "no_compatible_attested_page"
            else:
                reason = "permission_gap" if blocked else "missing_page"
            return CellTrace(
                cell,
                False,
                tuple(chain),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
                reason,
            )
        seen.add(cursor)
        expected_sequence = len(chain)
        expected_previous = chain[-1].attestation_digest if chain else ""
        if (
            page.attestation_sequence_index != expected_sequence
            or page.previous_attestation_digest != expected_previous
            or (session_id is not None and page.attestation_session_id != session_id)
        ):
            return CellTrace(
                cell,
                False,
                (),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                True,
                "signed_session_chain_mismatch",
            )
        if session_id is None:
            session_id = page.attestation_session_id
        chain.append(page)
        if page.silently_truncated:
            return CellTrace(
                cell,
                False,
                tuple(chain),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
                "connector_declared_untrustworthy_truncation",
            )
        if page.next_cursor is None:
            orphaned = set(pages) - seen
            if orphaned:
                return CellTrace(
                    cell,
                    False,
                    (),
                    sorted(orphaned, key=_cursor_sort_key)[0],
                    tuple(item.digest for item in chain),
                    evidence_digests,
                    blocked,
                    True,
                    "orphan_page_conflict",
                )
            return CellTrace(
                cell,
                True,
                tuple(chain),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
                "complete_source_bound_page_chain",
            )
        cursor = page.next_cursor


def _certificate(
    claim: Claim,
    *,
    audit_observation_digests: tuple[str, ...],
    decision: Decision,
    proof_type: Literal[
        "positive_witness",
        "counterexample_witness",
        "joint_scope_coverage",
        "insufficient_coverage",
    ],
    observation_digests: tuple[str, ...],
    covered_cells: tuple[ScopeCell, ...],
    missing_cells: tuple[ScopeCell, ...],
    witness_record_id: str | None,
    reason: str,
) -> CoverageCertificate:
    return CoverageCertificate(
        schema_version=9,
        claim_digest=claim.digest,
        source_identity_digest=claim.source.digest,
        request_binding_digest=claim.request_binding_digest,
        decision=decision,
        proof_type=proof_type,
        audit_observation_digests=audit_observation_digests,
        observation_digests=observation_digests,
        covered_cells=covered_cells,
        missing_cells=missing_cells,
        witness_record_id=witness_record_id,
        snapshot_id=claim.snapshot_id,
        reason=reason,
    )


def evaluate_claim(claim: Claim, observations: Sequence[Observation]) -> Evaluation:
    preflight = _preflight_observations(claim, observations)
    if preflight.conflicting_observations:
        missing = tuple(sorted(claim.scope))
        reason = "evidence conflict prevents a source-bound page-chain proof"
        obligation = RepairObligation(
            missing_cells=missing,
            next_cursors=(),
            blocked_cells=(),
            conflicted_cells=missing,
            reason=reason,
        )
        certificate = _certificate(
            claim,
            audit_observation_digests=preflight.audit_digests,
            decision="UNKNOWN",
            proof_type="insufficient_coverage",
            observation_digests=preflight.audit_digests,
            covered_cells=(),
            missing_cells=missing,
            witness_record_id=None,
            reason=reason,
        )
        return Evaluation("UNKNOWN", certificate, obligation)
    traces = {
        cell: _trace_cell(cell, observations, claim, preflight)
        for cell in sorted(claim.scope)
    }
    covered = tuple(cell for cell, trace in traces.items() if trace.complete)
    missing = tuple(cell for cell, trace in traces.items() if not trace.complete)

    for cell in sorted(traces):
        trace = traces[cell]
        if trace.conflicted:
            continue
        pages = sorted(
            trace.witness_pages,
            key=lambda item: (_cursor_sort_key(item.cursor), item.digest),
        )
        for observation in pages:
            for record in observation.records:
                if (
                    record.cell.semantic_key != observation.cell.semantic_key
                    or not any(
                        record.cell.semantic_key == cell.semantic_key
                        for cell in claim.scope
                    )
                ):
                    continue
                decision = claim.witness_for(record)
                if decision is None:
                    continue
                proof_type = (
                    "positive_witness"
                    if decision == "TRUE"
                    else "counterexample_witness"
                )
                certificate = _certificate(
                    claim,
                    audit_observation_digests=preflight.audit_digests,
                    decision=decision,
                    proof_type=proof_type,
                    observation_digests=(observation.digest,),
                    covered_cells=covered,
                    missing_cells=missing,
                    witness_record_id=record.record_id,
                    reason="a source-bound in-scope attested record decides the claim",
                )
                return Evaluation(decision, certificate, None)

    if not missing:
        decision = claim.coverage_decision
        all_chain_digests = tuple(
            digest
            for cell in sorted(traces)
            for digest in traces[cell].chain_digests
        )
        certificate = _certificate(
            claim,
            audit_observation_digests=preflight.audit_digests,
            decision=decision,
            proof_type="joint_scope_coverage",
            observation_digests=all_chain_digests,
            covered_cells=covered,
            missing_cells=(),
            witness_record_id=None,
            reason="complete source-bound page chains cover the exact joint claim scope",
        )
        return Evaluation(decision, certificate, None)

    blocked = tuple(cell for cell in missing if traces[cell].blocked)
    conflicted = tuple(cell for cell in missing if traces[cell].conflicted)
    next_cursors = tuple(
        (cell, traces[cell].next_cursor)
        for cell in missing
        if not traces[cell].blocked and not traces[cell].conflicted
    )
    reason = _unknown_reason(traces, missing)
    obligation = RepairObligation(
        missing_cells=missing,
        next_cursors=next_cursors,
        blocked_cells=blocked,
        conflicted_cells=conflicted,
        reason=reason,
    )
    all_evidence_digests = tuple(
        digest
        for cell in sorted(traces)
        for digest in traces[cell].evidence_digests
    )
    certificate = _certificate(
        claim,
        audit_observation_digests=preflight.audit_digests,
        decision="UNKNOWN",
        proof_type="insufficient_coverage",
        observation_digests=all_evidence_digests,
        covered_cells=covered,
        missing_cells=missing,
        witness_record_id=None,
        reason=reason,
    )
    return Evaluation("UNKNOWN", certificate, obligation)


def next_page_requests(
    claim: Claim,
    observations: Sequence[Observation],
    cells: Iterable[ScopeCell] | None = None,
) -> tuple[tuple[ScopeCell, Cursor], ...]:
    """Return one source-bound continuation per incomplete, repairable cell."""

    requested_cells = claim.scope if cells is None else tuple(cells)
    trace_claim = claim
    if not set(requested_cells) <= set(claim.scope):
        trace_claim = replace(
            claim,
            scope=tuple(sorted(set(claim.scope) | set(requested_cells))),
        )
    requests: list[tuple[ScopeCell, Cursor]] = []
    preflight = _preflight_observations(trace_claim, observations)
    for cell in sorted(set(requested_cells)):
        trace = _trace_cell(cell, observations, trace_claim, preflight)
        if not trace.complete and not trace.blocked and not trace.conflicted:
            requests.append((cell, trace.next_cursor))
    return tuple(requests)


def complete_joint_cells(
    claim: Claim,
    observations: Sequence[Observation],
    cells: Iterable[ScopeCell] | None = None,
) -> tuple[ScopeCell, ...]:
    requested_cells = claim.scope if cells is None else tuple(cells)
    trace_claim = claim
    if not set(requested_cells) <= set(claim.scope):
        trace_claim = replace(
            claim,
            scope=tuple(sorted(set(claim.scope) | set(requested_cells))),
        )
    preflight = _preflight_observations(trace_claim, observations)
    return tuple(
        cell
        for cell in sorted(set(requested_cells))
        if _trace_cell(cell, observations, trace_claim, preflight).complete
    )


def verify_certificate(
    claim: Claim,
    observations: Sequence[Observation],
    certificate: CoverageCertificate,
) -> bool:
    """Verify against a separately implemented certificate specification."""

    from independent_certificate_verifier import verify_certificate_independently

    return verify_certificate_independently(claim, observations, certificate)


def marginal_coverage_would_accept(
    claim_scope: Iterable[ScopeCell],
    observed_complete_cells: Iterable[ScopeCell],
) -> bool:
    """The deliberately unsound marginal checker retained only as a foil."""

    claim_cells = tuple(claim_scope)
    observed_cells = tuple(observed_complete_cells)
    return (
        {cell.entity for cell in claim_cells}
        <= {cell.entity for cell in observed_cells}
        and {cell.time_bucket for cell in claim_cells}
        <= {cell.time_bucket for cell in observed_cells}
        and {cell.archive_state for cell in claim_cells}
        <= {cell.archive_state for cell in observed_cells}
    )


def cell_to_dict(cell: ScopeCell) -> dict[str, str]:
    return asdict(cell)
