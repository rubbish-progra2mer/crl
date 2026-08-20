from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUN_ROOT / "implementation_v003"))

from joint_coverage_kernel import (  # noqa: E402
    Claim,
    Observation,
    ScopeCell,
    SourceIdentity,
    evaluate_claim,
    verify_certificate,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    actual_request_cell = ScopeCell("A", "recent", "active")
    labelled_response_cell = ScopeCell("B", "recent", "active")
    source = SourceIdentity("connector-a", "list-v1", "subject-1", "joint-v1")
    claim = Claim(
        "exists-b",
        "exists",
        "matches_target",
        (labelled_response_cell,),
        "s1",
        source,
    )
    relabelled_empty = Observation(
        "actual-a-labelled-b",
        source.connector_id,
        labelled_response_cell,
        0,
        None,
        (),
        "s1",
        query_signature=source.query_signature,
        authentication_subject=source.authentication_subject,
        scope_schema_version=source.scope_schema_version,
    )
    result = evaluate_claim(claim, [relabelled_empty])
    document = {
        "kernel": "frozen_v003",
        "actual_request_cell_external_fact": actual_request_cell.key,
        "observation_labelled_cell": labelled_response_cell.key,
        "v003_has_field_for_actual_request_cell": False,
        "decision": result.decision,
        "proof_type": result.certificate.proof_type,
        "certificate_valid": verify_certificate(
            claim, [relabelled_empty], result.certificate
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
