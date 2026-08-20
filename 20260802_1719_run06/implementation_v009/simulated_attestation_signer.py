"""Non-production RSA signer used only by deterministic simulated experiments.

The embedded private exponent is an openly published fixture key.  Production
verification never imports this module.  The real trust-bridge experiment uses
an ephemeral OpenSSL key held only by a separate signer process.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from typing import Sequence

from joint_coverage_kernel import (
    DEFAULT_ATTESTATION_PUBLIC_KEY_E,
    DEFAULT_ATTESTATION_PUBLIC_KEY_N_HEX,
    RSA_SHA256_DIGEST_INFO_PREFIX,
    Cursor,
    Record,
    SourceIdentity,
    canonical_page_attestation_payload,
    canonical_response_commitment,
)


FIXTURE_PRIVATE_EXPONENT_HEX = (
    "36a20d61a6b051d4997402669826d07e24fd8bee7821874035fb02f47e57cda3"
    "d7458f3dbc7ea9a89a80176f6db04e7aa8dfefc4336474f5062f8e350aa9bc6d"
    "9adf75bba0165c7f5f47e6951c80a1115a5d45b252143841adbc6d7c36d75604"
    "fbb59c6fdb10fdec8fbd32a7d64877f6d9f02885f448883b5b96511b4f4baa0f"
    "d4567217bd6f29e44478b8986104d54ff90560caf157ff8f926001a7091a70de0"
    "34d9dec314e011452fffa516be3bf4428187a83558af33a4bfee67cde5ea833b1"
    "f7780ea9124635140b2a62216704f0eca1a17154e7f5e6fa944f23e0dbf6bcccc"
    "08888dd3345d29252ee8f7045314feb22d2760be56317b0b19e01fef3a601"
)


def canonical_raw_response_bytes(
    records: Sequence[Record],
    next_cursor: Cursor | None,
    status: str,
    permission_complete: bool,
    silently_truncated: bool,
) -> bytes:
    return json.dumps(
        {
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
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


@lru_cache(maxsize=65536)
def fixture_sign(message: str) -> str:
    modulus = int(DEFAULT_ATTESTATION_PUBLIC_KEY_N_HEX, 16)
    private_exponent = int(FIXTURE_PRIVATE_EXPONENT_HEX, 16)
    width = (modulus.bit_length() + 7) // 8
    digest_info = RSA_SHA256_DIGEST_INFO_PREFIX + hashlib.sha256(
        message.encode("utf-8")
    ).digest()
    padding_length = width - len(digest_info) - 3
    encoded = b"\x00\x01" + b"\xff" * padding_length + b"\x00" + digest_info
    signature = pow(
        int.from_bytes(encoded, "big"), private_exponent, modulus
    ).to_bytes(width, "big")
    return signature.hex()


def attest_response(
    source: SourceIdentity,
    request_payload: str,
    records: Sequence[Record],
    next_cursor: Cursor | None,
    status: str,
    permission_complete: bool,
    silently_truncated: bool,
    *,
    cursor: Cursor,
    session_id: str,
    sequence_index: int,
    previous_attestation_digest: str,
) -> dict[str, object]:
    if (
        source.attestation_public_key_n_hex
        != DEFAULT_ATTESTATION_PUBLIC_KEY_N_HEX
        or source.attestation_public_key_e != DEFAULT_ATTESTATION_PUBLIC_KEY_E
    ):
        raise ValueError("the simulation signer only signs for its fixture public key")
    response_commitment = canonical_response_commitment(
        request_payload,
        records,
        next_cursor,
        status,
        permission_complete,
        silently_truncated,
    )
    raw_response = canonical_raw_response_bytes(
        records,
        next_cursor,
        status,
        permission_complete,
        silently_truncated,
    )
    raw_sha256 = hashlib.sha256(raw_response).hexdigest()
    payload = canonical_page_attestation_payload(
        source,
        request_payload,
        raw_sha256,
        response_commitment,
        session_id,
        sequence_index,
        previous_attestation_digest,
        cursor,
        next_cursor,
        status,
        permission_complete,
        silently_truncated,
    )
    return {
        "response_commitment": response_commitment,
        "raw_response_sha256": raw_sha256,
        "attestation_session_id": session_id,
        "attestation_sequence_index": sequence_index,
        "previous_attestation_digest": previous_attestation_digest,
        "attestation_signature_hex": fixture_sign(payload),
    }
