"""End-to-end two-process trust-bridge experiment for v009."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _cell(entity: str, semantic_id: str = "") -> dict[str, str]:
    return {
        "entity": entity,
        "time_bucket": "recent",
        "archive_state": "active",
        "semantic_id": semantic_id,
    }


def _raw_page(
    records: list[dict[str, Any]], next_cursor: str | None
) -> dict[str, Any]:
    return {
        "records": records,
        "next_cursor": next_cursor,
        "status": "ok",
        "permission_complete": True,
        "silently_truncated": False,
    }


def _record(
    record_id: str,
    cell: dict[str, str],
    matches_target: bool,
    compliant: bool,
) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "cell": cell,
        "matches_target": matches_target,
        "compliant": compliant,
    }


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--openssl", required=True)
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    implementation_dir = Path(__file__).resolve().parent

    cell_a = _cell("A")
    semantic_alias = "semantic:B:recent:active"
    alias_b1 = _cell("B-v1", semantic_alias)
    alias_b2 = _cell("B-v2", semantic_alias)
    snapshot = "controlled-snapshot-v009"

    raw_pages = {
        "raw-main-0.json": _raw_page([], "c1"),
        "raw-main-1.json": _raw_page(
            [_record("signed-positive", cell_a, True, True)], "c2"
        ),
        "raw-main-2.json": _raw_page([], None),
        "raw-other-1.json": _raw_page([], None),
        "raw-alias.json": _raw_page(
            [_record("alias-positive", alias_b2, True, True)], None
        ),
    }
    for name, value in raw_pages.items():
        _write_json(output_dir / name, value)
    tampered_raw = (output_dir / "raw-main-0.json").read_bytes() + b" "
    (output_dir / "raw-main-0-tampered.json").write_bytes(tampered_raw)

    signer_input = {
        "source": {
            "connector_id": "controlled-list-connector",
            "query_signature": "LIST controlled records",
            "authentication_subject": "trust-bridge-fixture",
            "scope_schema_version": "joint-semantic-cell-v1",
            "adapter_version": "independent-raw-signer-v1",
            "semantic_normalization_version": "semantic-cell-id-v1",
            "request_serialization_version": "canonical-json-v1",
        },
        "pages": [
            {
                "page_id": "main-0",
                "session_group": "main",
                "raw_path": "raw-main-0.json",
                "cell": cell_a,
                "cursor": 0,
                "snapshot_id": snapshot,
            },
            {
                "page_id": "main-1",
                "session_group": "main",
                "raw_path": "raw-main-1.json",
                "cell": cell_a,
                "cursor": "c1",
                "snapshot_id": snapshot,
            },
            {
                "page_id": "main-2",
                "session_group": "main",
                "raw_path": "raw-main-2.json",
                "cell": cell_a,
                "cursor": "c2",
                "snapshot_id": snapshot,
            },
            {
                "page_id": "other-1",
                "session_group": "other",
                "raw_path": "raw-other-1.json",
                "cell": cell_a,
                "cursor": "c1",
                "snapshot_id": snapshot,
            },
            {
                "page_id": "alias",
                "session_group": "alias",
                "raw_path": "raw-alias.json",
                "cell": alias_b2,
                "cursor": 0,
                "snapshot_id": snapshot,
            },
        ],
    }
    signer_input_path = output_dir / "signer-input.json"
    manifest_path = output_dir / "signed-manifest.json"
    _write_json(signer_input_path, signer_input)
    signer_result = _run(
        [
            sys.executable,
            str(implementation_dir / "independent_raw_page_signer.py"),
            "--input",
            str(signer_input_path),
            "--output",
            str(manifest_path),
            "--openssl",
            str(Path(args.openssl).resolve()),
        ]
    )
    (output_dir / "signer-stdout.txt").write_text(
        signer_result.stdout, encoding="utf-8", newline="\n"
    )
    (output_dir / "signer-stderr.txt").write_text(
        signer_result.stderr, encoding="utf-8", newline="\n"
    )
    trusted_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    trust_anchor_path = output_dir / "pinned-public-trust-anchor.json"
    _write_json(
        trust_anchor_path,
        {
            "schema_version": 1,
            "enrollment": "controlled out-of-band public-key pinning",
            "trusted_source": trusted_manifest["source"],
        },
    )

    attacker_raw_name = "raw-attacker-terminal.json"
    _write_json(output_dir / attacker_raw_name, _raw_page([], None))
    attacker_input = {
        "source": signer_input["source"],
        "pages": [
            {
                "page_id": "attacker-0",
                "session_group": "attacker",
                "raw_path": attacker_raw_name,
                "cell": cell_a,
                "cursor": 0,
                "snapshot_id": snapshot,
            }
        ],
    }
    attacker_input_path = output_dir / "attacker-signer-input.json"
    attacker_manifest_path = output_dir / "attacker-signed-manifest.json"
    _write_json(attacker_input_path, attacker_input)
    attacker_signer_result = _run(
        [
            sys.executable,
            str(implementation_dir / "independent_raw_page_signer.py"),
            "--input",
            str(attacker_input_path),
            "--output",
            str(attacker_manifest_path),
            "--openssl",
            str(Path(args.openssl).resolve()),
        ]
    )
    (output_dir / "attacker-signer-stdout.txt").write_text(
        attacker_signer_result.stdout, encoding="utf-8", newline="\n"
    )
    (output_dir / "attacker-signer-stderr.txt").write_text(
        attacker_signer_result.stderr, encoding="utf-8", newline="\n"
    )

    main_claim = {
        "claim_id": "trust-bridge-exists-a",
        "quantifier": "exists",
        "predicate": "matches_target",
        "scope": [cell_a],
        "snapshot_id": snapshot,
        "initial_cursor": 0,
    }
    alias_claim = {
        "claim_id": "trust-bridge-alias-exists",
        "quantifier": "exists",
        "predicate": "matches_target",
        "scope": [alias_b1],
        "snapshot_id": snapshot,
        "initial_cursor": 0,
    }
    cases = [
        {
            "case": "valid_three_page_signed_session",
            "expected_decision": "TRUE",
            "selected_page_ids": ["main-0", "main-1", "main-2"],
            "claim": main_claim,
        },
        {
            "case": "decoder_omission_plus_ordinary_rehash",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0", "main-1", "main-2"],
            "mutation": "omit_first_record_and_rehash",
            "claim": main_claim,
        },
        {
            "case": "false_terminal_plus_ordinary_rehash",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0"],
            "mutation": "false_terminal_and_rehash",
            "claim": main_claim,
        },
        {
            "case": "signature_bit_flip",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0", "main-1", "main-2"],
            "mutation": "signature_flip",
            "claim": main_claim,
        },
        {
            "case": "raw_response_byte_tamper",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0"],
            "raw_overrides": {"main-0": "raw-main-0-tampered.json"},
            "claim": main_claim,
        },
        {
            "case": "delete_middle_keep_orphan_terminal",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0", "main-2"],
            "claim": main_claim,
        },
        {
            "case": "splice_valid_page_from_other_session",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0", "other-1"],
            "claim": main_claim,
        },
        {
            "case": "identical_signed_page_replay",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0", "main-0"],
            "claim": main_claim,
        },
        {
            "case": "decoder_identity_relabel",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0", "main-1", "main-2"],
            "mutation": "decoder_digest_relabel",
            "claim": main_claim,
        },
        {
            "case": "attestation_session_relabel",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0", "main-1", "main-2"],
            "mutation": "session_relabel",
            "claim": main_claim,
        },
        {
            "case": "attestation_boolean_downgrade",
            "expected_decision": "UNKNOWN",
            "selected_page_ids": ["main-0", "main-1", "main-2"],
            "mutation": "attested_false",
            "claim": main_claim,
        },
        {
            "case": "same_version_raw_alias_with_signed_semantic_cell",
            "expected_decision": "TRUE",
            "selected_page_ids": ["alias"],
            "claim": alias_claim,
        },
        {
            "case": "self_consistent_attacker_resigned_manifest",
            "expected_decision": "UNKNOWN",
            "manifest_path": attacker_manifest_path.name,
            "selected_page_ids": ["attacker-0"],
            "claim": main_claim,
        },
    ]

    rows = []
    for index, case in enumerate(cases, start=1):
        case_value = dict(case)
        case_value.setdefault("manifest_path", manifest_path.name)
        case_value["trust_anchor_path"] = trust_anchor_path.name
        input_path = output_dir / f"consumer-input-{index:02d}.json"
        result_path = output_dir / f"consumer-result-{index:02d}.json"
        _write_json(input_path, case_value)
        completed = _run(
            [
                sys.executable,
                str(implementation_dir / "signed_manifest_consumer.py"),
                "--input",
                str(input_path),
                "--output",
                str(result_path),
            ]
        )
        (output_dir / f"consumer-stdout-{index:02d}.txt").write_text(
            completed.stdout, encoding="utf-8", newline="\n"
        )
        (output_dir / f"consumer-stderr-{index:02d}.txt").write_text(
            completed.stderr, encoding="utf-8", newline="\n"
        )
        rows.append(json.loads(result_path.read_text(encoding="utf-8")))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    attacker_manifest = json.loads(
        attacker_manifest_path.read_text(encoding="utf-8")
    )
    artifact_files = sorted(
        path.name for path in output_dir.iterdir() if path.is_file()
    )
    forbidden_private_suffixes = {".pem", ".key", ".pfx", ".p12"}
    private_key_artifacts = [
        name
        for name in artifact_files
        if Path(name).suffix.lower() in forbidden_private_suffixes
    ]
    signer_pid = manifest["signer_pid"]
    consumer_pids = sorted({row["consumer_pid"] for row in rows})
    result = {
        "experiment": "two_process_asymmetric_signed_manifest_v009",
        "schema_version": 1,
        "case_count": len(rows),
        "passed": sum(bool(row["pass"]) for row in rows),
        "all_passed": all(bool(row["pass"]) for row in rows),
        "signed_page_count": len(manifest["pages"]),
        "signer_pid": signer_pid,
        "attacker_signer_pid": attacker_manifest["signer_pid"],
        "consumer_pids": consumer_pids,
        "all_consumers_distinct_from_signer": all(
            pid not in {signer_pid, attacker_manifest["signer_pid"]}
            for pid in consumer_pids
        ),
        "private_key_exported": manifest["private_key_exported"],
        "private_key_artifacts": private_key_artifacts,
        "public_modulus_bits": int(
            manifest["source"]["attestation_public_key_n_hex"], 16
        ).bit_length(),
        "openssl_executable": manifest["openssl_executable"],
        "pinned_trust_anchor_sha256": hashlib.sha256(
            trust_anchor_path.read_bytes()
        ).hexdigest(),
        "rows": rows,
        "artifact_sha256": {
            name: hashlib.sha256((output_dir / name).read_bytes()).hexdigest()
            for name in artifact_files
        },
    }
    result["trust_boundary_checks_passed"] = bool(
        result["all_consumers_distinct_from_signer"]
        and not result["private_key_exported"]
        and not result["private_key_artifacts"]
        and result["public_modulus_bits"] >= 2048
    )
    result["all_passed"] = bool(
        result["all_passed"] and result["trust_boundary_checks_passed"]
    )
    _write_json(output_dir / "summary.json", result)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "experiment",
                    "case_count",
                    "passed",
                    "all_passed",
                    "signed_page_count",
                    "all_consumers_distinct_from_signer",
                    "private_key_artifacts",
                    "public_modulus_bits",
                    "trust_boundary_checks_passed",
                )
            },
            ensure_ascii=False,
        )
    )
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
