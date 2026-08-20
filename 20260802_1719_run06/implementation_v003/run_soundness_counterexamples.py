from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

from joint_coverage_kernel import (
    Claim,
    Observation,
    Record,
    ScopeCell,
    SourceIdentity,
    evaluate_claim,
    verify_certificate,
)


SOURCE = SourceIdentity("connector-a", "list-v1", "subject-1", "joint-v1")


def obs(
    name: str,
    cell: ScopeCell,
    *,
    cursor: str | int = 0,
    next_cursor: str | int | None = None,
    records: tuple[Record, ...] = (),
    source: SourceIdentity = SOURCE,
    snapshot: str = "s1",
) -> Observation:
    return Observation(
        name,
        source.connector_id,
        cell,
        cursor,
        next_cursor,
        records,
        snapshot,
        query_signature=source.query_signature,
        authentication_subject=source.authentication_subject,
        scope_schema_version=source.scope_schema_version,
    )


def evaluated_row(
    case: str,
    claim: Claim,
    observations: list[Observation],
    expected_decision: str,
) -> dict[str, Any]:
    result = evaluate_claim(claim, observations)
    certificate_valid = verify_certificate(claim, observations, result.certificate)
    return {
        "case": case,
        "expected_decision_from_scope_and_source_facts": expected_decision,
        "actual_decision": result.decision,
        "proof_type": result.certificate.proof_type,
        "certificate_valid": certificate_valid,
        "unsafe_certified_commit": (
            result.decision != "UNKNOWN" and result.decision != expected_decision
        ),
        "pass": result.decision == expected_decision and certificate_valid,
        "certificate_digest": result.certificate.digest,
        "reason": result.certificate.reason,
    }


def build_panel() -> dict[str, Any]:
    cell_a = ScopeCell("A", "recent", "active")
    cell_b = ScopeCell("B", "recent", "active")
    exists = Claim("exists-a", "exists", "matches_target", (cell_a,), "s1", SOURCE)
    forall = Claim("forall-a", "forall", "compliant", (cell_a,), "s1", SOURCE)

    rows: list[dict[str, Any]] = []
    rows.append(
        evaluated_row(
            "out_of_scope_exists_witness",
            exists,
            [obs("misplaced-positive", cell_a, records=(Record("outside", cell_b, True, True),))],
            "UNKNOWN",
        )
    )
    rows.append(
        evaluated_row(
            "out_of_scope_forall_counterexample",
            forall,
            [obs("misplaced-negative", cell_a, records=(Record("outside", cell_b, False, False),))],
            "UNKNOWN",
        )
    )

    foreign_connector = replace(SOURCE, connector_id="connector-b")
    cross_source = [
        obs("a-0", cell_a, next_cursor="next"),
        obs("b-1", cell_a, cursor="next", source=foreign_connector),
    ]
    rows.append(
        evaluated_row(
            "cross_connector_page_chain",
            exists,
            cross_source,
            "UNKNOWN",
        )
    )

    continuing = obs("continue", cell_a, next_cursor="next")
    terminating = obs("terminate", cell_a, next_cursor=None)
    left = evaluated_row(
        "same_cursor_conflict_order_1",
        exists,
        [continuing, terminating],
        "UNKNOWN",
    )
    right = evaluated_row(
        "same_cursor_conflict_order_2",
        exists,
        [terminating, continuing],
        "UNKNOWN",
    )
    left["permutation_certificate_stable"] = (
        left["certificate_digest"] == right["certificate_digest"]
    )
    right["permutation_certificate_stable"] = (
        left["certificate_digest"] == right["certificate_digest"]
    )
    left["pass"] = bool(left["pass"] and left["permutation_certificate_stable"])
    right["pass"] = bool(right["pass"] and right["permutation_certificate_stable"])
    rows.extend((left, right))

    opaque_claim = replace(exists, claim_id="opaque", initial_cursor="start")
    opaque_trace = [
        obs("start", cell_a, cursor="start", next_cursor="z-token"),
        obs("z", cell_a, cursor="z-token", next_cursor="a-token"),
        obs("a", cell_a, cursor="a-token", next_cursor=None),
    ]
    rows.append(
        evaluated_row(
            "opaque_cursor_protocol_closure",
            opaque_claim,
            opaque_trace,
            "FALSE",
        )
    )

    cycle_claim = replace(exists, claim_id="cycle", initial_cursor="start")
    rows.append(
        evaluated_row(
            "opaque_cursor_cycle",
            cycle_claim,
            [
                obs("cycle-0", cell_a, cursor="start", next_cursor="again"),
                obs("cycle-1", cell_a, cursor="again", next_cursor="start"),
            ],
            "UNKNOWN",
        )
    )

    valid_witness = [
        obs(
            "valid-witness",
            cell_a,
            next_cursor="unread",
            records=(Record("inside", cell_a, True, True),),
        )
    ]
    rows.append(
        evaluated_row(
            "source_bound_in_scope_witness",
            exists,
            valid_witness,
            "TRUE",
        )
    )

    original_trace = [obs("complete", cell_a)]
    original_certificate = evaluate_claim(exists, original_trace).certificate
    replacements = {
        "query_signature_replacement": replace(SOURCE, query_signature="different-query"),
        "authentication_subject_replacement": replace(
            SOURCE, authentication_subject="subject-2"
        ),
        "scope_schema_replacement": replace(
            SOURCE, scope_schema_version="joint-v2"
        ),
    }
    for case, replacement_source in replacements.items():
        replacement_trace = [obs("complete", cell_a, source=replacement_source)]
        rejected = not verify_certificate(exists, replacement_trace, original_certificate)
        rows.append(
            {
                "case": case,
                "expected_decision_from_scope_and_source_facts": "certificate_rejected",
                "actual_decision": "certificate_rejected" if rejected else "certificate_accepted",
                "proof_type": original_certificate.proof_type,
                "certificate_valid": not rejected,
                "unsafe_certified_commit": not rejected,
                "pass": rejected,
                "reason": "source identity mutation must invalidate the original certificate",
            }
        )

    mismatch_trace = [
        obs(
            "misplaced-forgery",
            cell_a,
            records=(Record("outside-forgery", cell_b, True, True),),
        )
    ]
    unknown = evaluate_claim(exists, mismatch_trace)
    forged = replace(
        unknown.certificate,
        decision="TRUE",
        proof_type="positive_witness",
        observation_digests=(mismatch_trace[0].digest,),
        witness_record_id="outside-forgery",
        reason="a source-bound in-scope attested record decides the claim",
    )
    forged_rejected = not verify_certificate(exists, mismatch_trace, forged)
    rows.append(
        {
            "case": "forged_out_of_scope_witness_certificate",
            "expected_decision_from_scope_and_source_facts": "certificate_rejected",
            "actual_decision": "certificate_rejected" if forged_rejected else "certificate_accepted",
            "proof_type": forged.proof_type,
            "certificate_valid": not forged_rejected,
            "unsafe_certified_commit": not forged_rejected,
            "pass": forged_rejected,
            "reason": "independent verifier must reject evaluator-shaped forged evidence",
        }
    )

    return {
        "experiment": "source_bound_soundness_counterexamples_v003",
        "schema_version": 1,
        "case_count": len(rows),
        "passed": sum(bool(row["pass"]) for row in rows),
        "unsafe_certified_commits": sum(
            bool(row["unsafe_certified_commit"]) for row in rows
        ),
        "all_passed": all(bool(row["pass"]) for row in rows),
        "rows": rows,
    }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    panel = build_panel()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(panel, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({key: panel[key] for key in ("experiment", "case_count", "passed", "unsafe_certified_commits", "all_passed")}, ensure_ascii=False))
    if not panel["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
