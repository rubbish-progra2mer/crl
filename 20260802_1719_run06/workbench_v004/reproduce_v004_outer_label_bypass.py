from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUN_ROOT / "implementation_v004"))

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


def page(
    name: str,
    source: SourceIdentity,
    cell: ScopeCell,
    records: tuple[Record, ...],
    request_payload: str,
) -> Observation:
    return Observation(
        name,
        source.connector_id,
        cell,
        0,
        None,
        records,
        "s1",
        query_signature=source.query_signature,
        authentication_subject=source.authentication_subject,
        scope_schema_version=source.scope_schema_version,
        adapter_version=source.adapter_version,
        request_serialization_version=source.request_serialization_version,
        request_payload=request_payload,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cell = ScopeCell("B", "recent", "active")
    expected = SourceIdentity(
        "connector-s",
        "list-v1",
        "subject-1",
        "joint-v1",
        "adapter-v1",
        "canonical-json-v1",
    )
    relabelled = replace(expected, connector_id="connector-t")
    claim = Claim("exists-b", "exists", "matches_target", (cell,), "s1", expected)
    expected_payload = canonical_request_payload(expected, cell, 0, "s1")
    empty = page("empty", expected, cell, (), expected_payload)
    hidden_witness = page(
        "hidden-witness",
        relabelled,
        cell,
        (Record("positive", cell, True, True),),
        expected_payload,
    )
    observations = [empty, hidden_witness]
    result = evaluate_claim(claim, observations)
    document = {
        "kernel": "frozen_v004",
        "case": "outer_source_label_routes_expected_request_conflict_out_of_bucket",
        "outer_source_of_hidden_page": relabelled.connector_id,
        "payload_source_of_hidden_page": expected.connector_id,
        "same_payload_as_clean_page": hidden_witness.request_payload
        == empty.request_payload,
        "decision": result.decision,
        "proof_type": result.certificate.proof_type,
        "certificate_valid": verify_certificate(
            claim, observations, result.certificate
        ),
        "unsafe_certified_commit": result.decision == "FALSE",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(document, ensure_ascii=False))


if __name__ == "__main__":
    main()
