"""Production-side raw consumer for the v009 trust-bridge experiment.

The consumer never receives private key material.  It independently decodes
raw bytes, constructs kernel observations, evaluates the claim, and invokes the
separate certificate verifier.  Mutation modes model decoder or transport
failures after the signer has committed the original page.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from independent_certificate_verifier import verify_certificate_independently
from joint_coverage_kernel import (
    Claim,
    Observation,
    Record,
    ScopeCell,
    SourceIdentity,
    canonical_response_commitment,
    evaluate_claim,
)


def _cell(value: dict[str, str]) -> ScopeCell:
    return ScopeCell(
        value["entity"],
        value["time_bucket"],
        value["archive_state"],
        value.get("semantic_id", ""),
    )


def _decode_raw_page(raw: bytes) -> tuple[tuple[Record, ...], dict[str, Any]]:
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict) or set(value) != {
        "records",
        "next_cursor",
        "status",
        "permission_complete",
        "silently_truncated",
    }:
        raise ValueError("consumer raw page has an unexpected schema")
    records = []
    for index, item in enumerate(value["records"]):
        if not isinstance(item, dict) or set(item) != {
            "record_id",
            "cell",
            "matches_target",
            "compliant",
        }:
            raise ValueError(f"consumer record {index} has an unexpected schema")
        records.append(
            Record(
                item["record_id"],
                _cell(item["cell"]),
                item["matches_target"],
                item["compliant"],
            )
        )
    return tuple(records), value


def _source(value: dict[str, Any]) -> SourceIdentity:
    return SourceIdentity(
        value["connector_id"],
        value["query_signature"],
        value["authentication_subject"],
        value["scope_schema_version"],
        value["adapter_version"],
        value["semantic_normalization_version"],
        value["request_serialization_version"],
        value["attestation_scheme"],
        value["attestation_key_id"],
        value["attestation_public_key_n_hex"],
        value["attestation_public_key_e"],
        value["decoder_digest"],
    )


def _unknown_before_kernel(
    case: dict[str, Any], reason: str, manifest: dict[str, Any]
) -> dict[str, Any]:
    expected = case["expected_decision"]
    return {
        "case": case["case"],
        "expected_decision": expected,
        "actual_decision": "UNKNOWN",
        "pass": expected == "UNKNOWN",
        "reason": reason,
        "certificate_valid_independently": None,
        "consumer_pid": os.getpid(),
        "signer_pid": manifest["signer_pid"],
        "processes_are_distinct": os.getpid() != manifest["signer_pid"],
        "private_key_visible_to_consumer": False,
    }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    case = json.loads(args.input.read_text(encoding="utf-8"))
    base = args.input.parent.resolve()
    manifest_path = (base / case["manifest_path"]).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    trust_anchor_path = (base / case["trust_anchor_path"]).resolve()
    trust_anchor = json.loads(trust_anchor_path.read_text(encoding="utf-8"))
    if manifest.get("private_key_exported") or manifest.get(
        "private_key_fields_present"
    ):
        result = _unknown_before_kernel(
            case, "signer manifest exposes private key material", manifest
        )
    elif manifest["source"] != trust_anchor["trusted_source"]:
        result = _unknown_before_kernel(
            case,
            "manifest source identity does not match the pinned public trust anchor",
            manifest,
        )
    else:
        source = _source(trust_anchor["trusted_source"])
        page_lookup = {item["page_id"]: item for item in manifest["pages"]}
        selected = [page_lookup[page_id] for page_id in case["selected_page_ids"]]
        mutation = case.get("mutation", "none")
        observations: list[Observation] = []
        raw_hash_failure: str | None = None
        mutation_applied = False

        for item in selected:
            raw_relative = case.get("raw_overrides", {}).get(
                item["page_id"], item["raw_path"]
            )
            raw_path = (base / raw_relative).resolve()
            if base != raw_path and base not in raw_path.parents:
                raise ValueError("consumer raw page escapes case directory")
            raw = raw_path.read_bytes()
            actual_raw_sha256 = hashlib.sha256(raw).hexdigest()
            if actual_raw_sha256 != item["raw_response_sha256"]:
                raw_hash_failure = item["page_id"]
                break
            records, page = _decode_raw_page(raw)
            next_cursor = page["next_cursor"]
            response_commitment = item["response_commitment"]
            attested = True
            signature_hex = item["attestation_signature_hex"]
            decoder_digest = source.decoder_digest
            session_id = item["attestation_session_id"]

            if mutation == "omit_first_record_and_rehash" and records and not mutation_applied:
                records = records[1:]
                response_commitment = canonical_response_commitment(
                    item["request_payload"],
                    records,
                    next_cursor,
                    page["status"],
                    page["permission_complete"],
                    page["silently_truncated"],
                )
                mutation_applied = True
            elif mutation == "false_terminal_and_rehash" and next_cursor is not None and not mutation_applied:
                next_cursor = None
                response_commitment = canonical_response_commitment(
                    item["request_payload"],
                    records,
                    next_cursor,
                    page["status"],
                    page["permission_complete"],
                    page["silently_truncated"],
                )
                mutation_applied = True
            elif mutation == "signature_flip" and not mutation_applied:
                signature_hex = (
                    ("0" if signature_hex[0] != "0" else "1") + signature_hex[1:]
                )
                mutation_applied = True
            elif mutation == "decoder_digest_relabel" and not mutation_applied:
                decoder_digest = "1" * 64
                mutation_applied = True
            elif mutation == "session_relabel" and not mutation_applied:
                session_id = "consumer-relabelled-session"
                mutation_applied = True
            elif mutation == "attested_false" and not mutation_applied:
                attested = False
                mutation_applied = True

            observations.append(
                Observation(
                    observation_id=item["page_id"],
                    connector_id=source.connector_id,
                    cell=_cell(item["cell"]),
                    cursor=item["cursor"],
                    next_cursor=next_cursor,
                    records=records,
                    snapshot_id=item["snapshot_id"],
                    status=page["status"],
                    attested=attested,
                    permission_complete=page["permission_complete"],
                    silently_truncated=page["silently_truncated"],
                    query_signature=source.query_signature,
                    authentication_subject=source.authentication_subject,
                    scope_schema_version=source.scope_schema_version,
                    adapter_version=source.adapter_version,
                    semantic_normalization_version=source.semantic_normalization_version,
                    request_serialization_version=source.request_serialization_version,
                    attestation_scheme=source.attestation_scheme,
                    attestation_key_id=source.attestation_key_id,
                    attestation_public_key_n_hex=source.attestation_public_key_n_hex,
                    attestation_public_key_e=source.attestation_public_key_e,
                    decoder_digest=decoder_digest,
                    request_payload=item["request_payload"],
                    response_commitment=response_commitment,
                    raw_response_sha256=item["raw_response_sha256"],
                    attestation_session_id=session_id,
                    attestation_sequence_index=item[
                        "attestation_sequence_index"
                    ],
                    previous_attestation_digest=item[
                        "previous_attestation_digest"
                    ],
                    attestation_signature_hex=signature_hex,
                )
            )

        if raw_hash_failure is not None:
            result = _unknown_before_kernel(
                case,
                f"raw response hash mismatch for {raw_hash_failure}",
                manifest,
            )
        else:
            claim_value = case["claim"]
            claim = Claim(
                claim_value["claim_id"],
                claim_value["quantifier"],
                claim_value["predicate"],
                tuple(_cell(cell) for cell in claim_value["scope"]),
                claim_value["snapshot_id"],
                source,
                initial_cursor=claim_value.get("initial_cursor", 0),
            )
            evaluation = evaluate_claim(claim, observations)
            independently_valid = verify_certificate_independently(
                claim, observations, evaluation.certificate
            )
            result = {
                "case": case["case"],
                "expected_decision": case["expected_decision"],
                "actual_decision": evaluation.decision,
                "pass": evaluation.decision == case["expected_decision"]
                and independently_valid,
                "reason": evaluation.certificate.reason,
                "proof_type": evaluation.certificate.proof_type,
                "certificate_digest": evaluation.certificate.digest,
                "certificate_valid_independently": independently_valid,
                "observation_count": len(observations),
                "consumer_pid": os.getpid(),
                "signer_pid": manifest["signer_pid"],
                "processes_are_distinct": os.getpid() != manifest["signer_pid"],
                "private_key_visible_to_consumer": False,
            }

    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
