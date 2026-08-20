"""Independent raw-page signer for the v009 trust-bridge experiment.

This process deliberately does not import the production kernel.  It generates
an ephemeral RSA key, decodes the controlled raw response bytes, signs a
session-linked page manifest, exports only public material, and destroys its
temporary private-key directory before returning.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _cell_key(cell: dict[str, str]) -> str:
    return f"{cell['entity']}|{cell['time_bucket']}|{cell['archive_state']}"


def _semantic_key(cell: dict[str, str]) -> str:
    return cell.get("semantic_id") or _cell_key(cell)


def _decode_raw_page(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"))
    expected = {
        "records",
        "next_cursor",
        "status",
        "permission_complete",
        "silently_truncated",
    }
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError("raw page has an unexpected schema")
    if value["status"] not in {"ok", "permission_denied", "error"}:
        raise ValueError("raw page has an invalid status")
    if not isinstance(value["records"], list):
        raise ValueError("raw page records must be a list")
    decoded: list[dict[str, Any]] = []
    for index, record in enumerate(value["records"]):
        if not isinstance(record, dict) or set(record) != {
            "record_id",
            "cell",
            "matches_target",
            "compliant",
        }:
            raise ValueError(f"raw record {index} has an unexpected schema")
        cell = record["cell"]
        if not isinstance(cell, dict) or set(cell) != {
            "entity",
            "time_bucket",
            "archive_state",
            "semantic_id",
        }:
            raise ValueError(f"raw record {index} has an invalid cell")
        if not isinstance(record["record_id"], str) or not record["record_id"]:
            raise ValueError(f"raw record {index} has no stable id")
        if not isinstance(record["matches_target"], bool) or not isinstance(
            record["compliant"], bool
        ):
            raise ValueError(f"raw record {index} has non-boolean predicates")
        decoded.append(
            {
                "record_id": record["record_id"],
                "cell": _cell_key(cell),
                "semantic_cell_id": _semantic_key(cell),
                "matches_target": record["matches_target"],
                "compliant": record["compliant"],
            }
        )
    value["decoded_records"] = decoded
    return value


def _request_payload(
    source: dict[str, Any],
    cell: dict[str, str],
    cursor: str | int,
    snapshot_id: str,
) -> str:
    return _canonical_json(
        {
            "adapter_version": source["adapter_version"],
            "attestation_key_id": source["attestation_key_id"],
            "attestation_public_key_e": source["attestation_public_key_e"],
            "attestation_public_key_n_hex": source[
                "attestation_public_key_n_hex"
            ],
            "attestation_scheme": source["attestation_scheme"],
            "authentication_subject": source["authentication_subject"],
            "connector_id": source["connector_id"],
            "cursor": cursor,
            "decoder_digest": source["decoder_digest"],
            "filters": {
                "archive_state": cell["archive_state"],
                "entity": cell["entity"],
                "semantic_cell_id": _semantic_key(cell),
                "time_bucket": cell["time_bucket"],
            },
            "operation": source["query_signature"],
            "request_serialization_version": source[
                "request_serialization_version"
            ],
            "scope_schema_version": source["scope_schema_version"],
            "semantic_normalization_version": source[
                "semantic_normalization_version"
            ],
            "snapshot_id": snapshot_id,
        }
    )


def _response_commitment(request_payload: str, page: dict[str, Any]) -> str:
    return _digest(
        {
            "schema_version": 1,
            "request_payload_digest": hashlib.sha256(
                request_payload.encode("utf-8")
            ).hexdigest(),
            "records": page["decoded_records"],
            "next_cursor": page["next_cursor"],
            "status": page["status"],
            "permission_complete": page["permission_complete"],
            "silently_truncated": page["silently_truncated"],
        }
    )


def _attestation_payload(
    source: dict[str, Any],
    request_payload: str,
    raw_sha256: str,
    response_commitment: str,
    session_id: str,
    sequence_index: int,
    previous_attestation_digest: str,
    cursor: str | int,
    page: dict[str, Any],
) -> str:
    return _canonical_json(
        {
            "schema_version": 1,
            "attestation_scheme": source["attestation_scheme"],
            "attestation_key_id": source["attestation_key_id"],
            "source_identity_digest": _digest(source),
            "decoder_digest": source["decoder_digest"],
            "request_payload_digest": hashlib.sha256(
                request_payload.encode("utf-8")
            ).hexdigest(),
            "raw_response_sha256": raw_sha256,
            "response_commitment": response_commitment,
            "session_id": session_id,
            "sequence_index": sequence_index,
            "previous_attestation_digest": previous_attestation_digest,
            "cursor": cursor,
            "next_cursor": page["next_cursor"],
            "status": page["status"],
            "permission_complete": page["permission_complete"],
            "silently_truncated": page["silently_truncated"],
            "attested": True,
        }
    )


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )


def _sign(openssl: str, private_key: Path, payload: str, temp: Path) -> str:
    payload_path = temp / "payload.json"
    signature_path = temp / "signature.bin"
    payload_path.write_text(payload, encoding="utf-8", newline="\n")
    _run(
        [
            openssl,
            "dgst",
            "-sha256",
            "-sign",
            str(private_key),
            "-out",
            str(signature_path),
            str(payload_path),
        ]
    )
    return signature_path.read_bytes().hex()


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--openssl", required=True)
    args = parser.parse_args()

    request = json.loads(args.input.read_text(encoding="utf-8"))
    source = dict(request["source"])
    decoder_digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    with tempfile.TemporaryDirectory(prefix="crl-v009-signer-") as temp_name:
        temp = Path(temp_name)
        private_key = temp / "ephemeral-private.pem"
        _run(
            [
                args.openssl,
                "genpkey",
                "-quiet",
                "-algorithm",
                "RSA",
                "-pkeyopt",
                "rsa_keygen_bits:2048",
                "-out",
                str(private_key),
            ]
        )
        modulus_result = _run(
            [args.openssl, "rsa", "-in", str(private_key), "-noout", "-modulus"]
        )
        modulus_line = modulus_result.stdout.strip()
        if not modulus_line.startswith("Modulus="):
            raise ValueError("OpenSSL did not return an RSA modulus")
        modulus_hex = modulus_line.split("=", 1)[1].lower()
        source.update(
            {
                "attestation_scheme": "rsa-pkcs1v15-sha256-v1",
                "attestation_key_id": "ephemeral-rsa-"
                + hashlib.sha256(bytes.fromhex(modulus_hex)).hexdigest()[:24],
                "attestation_public_key_n_hex": modulus_hex,
                "attestation_public_key_e": 65537,
                "decoder_digest": decoder_digest,
            }
        )

        raw_base = args.input.parent.resolve()
        manifests: list[dict[str, Any]] = []
        previous_by_group: dict[str, str] = {}
        sequence_by_group: dict[str, int] = {}
        session_by_group: dict[str, str] = {}
        session_seed = _digest(
            {
                "source": source,
                "pages": request["pages"],
                "signer_pid": os.getpid(),
            }
        )
        for item in request["pages"]:
            group = item["session_group"]
            if group not in session_by_group:
                session_by_group[group] = (
                    f"ephemeral:{group}:{session_seed[:24]}"
                )
                sequence_by_group[group] = 0
                previous_by_group[group] = ""
            raw_path = (raw_base / item["raw_path"]).resolve()
            if raw_base != raw_path and raw_base not in raw_path.parents:
                raise ValueError("raw page escapes signer input directory")
            raw = raw_path.read_bytes()
            page = _decode_raw_page(raw)
            request_payload = _request_payload(
                source,
                item["cell"],
                item["cursor"],
                item["snapshot_id"],
            )
            commitment = _response_commitment(request_payload, page)
            payload = _attestation_payload(
                source,
                request_payload,
                hashlib.sha256(raw).hexdigest(),
                commitment,
                session_by_group[group],
                sequence_by_group[group],
                previous_by_group[group],
                item["cursor"],
                page,
            )
            signature_hex = _sign(args.openssl, private_key, payload, temp)
            attestation_digest = _digest(
                {"payload": payload, "signature_hex": signature_hex}
            )
            manifests.append(
                {
                    "page_id": item["page_id"],
                    "session_group": group,
                    "raw_path": item["raw_path"],
                    "cell": item["cell"],
                    "cursor": item["cursor"],
                    "snapshot_id": item["snapshot_id"],
                    "request_payload": request_payload,
                    "response_commitment": commitment,
                    "raw_response_sha256": hashlib.sha256(raw).hexdigest(),
                    "attestation_session_id": session_by_group[group],
                    "attestation_sequence_index": sequence_by_group[group],
                    "previous_attestation_digest": previous_by_group[group],
                    "attestation_signature_hex": signature_hex,
                    "next_cursor": page["next_cursor"],
                    "status": page["status"],
                    "permission_complete": page["permission_complete"],
                    "silently_truncated": page["silently_truncated"],
                }
            )
            previous_by_group[group] = attestation_digest
            sequence_by_group[group] += 1

        output = {
            "schema_version": 1,
            "signer_pid": os.getpid(),
            "signer_executable": str(Path(sys.executable).resolve()),
            "openssl_executable": str(Path(args.openssl).resolve()),
            "source": source,
            "private_key_exported": False,
            "private_key_fields_present": False,
            "pages": manifests,
        }
        args.output.write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    print(
        json.dumps(
            {
                "signed_pages": len(manifests),
                "signer_pid": os.getpid(),
                "private_key_exported": False,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
