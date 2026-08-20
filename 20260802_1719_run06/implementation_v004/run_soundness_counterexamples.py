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
    canonical_request_payload,
    evaluate_claim,
    verify_certificate,
)


SOURCE = SourceIdentity(
    "connector-a",
    "list-v1",
    "subject-1",
    "joint-v1",
    "adapter-v1",
    "canonical-json-v1",
)


def obs(
    name: str,
    cell: ScopeCell,
    *,
    cursor: str | int = 0,
    next_cursor: str | int | None = None,
    records: tuple[Record, ...] = (),
    source: SourceIdentity = SOURCE,
    snapshot: str = "s1",
    request_source: SourceIdentity | None = None,
    request_cell: ScopeCell | None = None,
    request_cursor: str | int | None = None,
    request_snapshot: str | None = None,
    request_payload: str | None = None,
) -> Observation:
    payload = request_payload
    if payload is None:
        payload = canonical_request_payload(
            source if request_source is None else request_source,
            cell if request_cell is None else request_cell,
            cursor if request_cursor is None else request_cursor,
            snapshot if request_snapshot is None else request_snapshot,
        )
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
        adapter_version=source.adapter_version,
        request_serialization_version=source.request_serialization_version,
        request_payload=payload,
    )


def certificate_rejection_row(
    case: str,
    claim: Claim,
    observations: list[Observation],
    certificate: Any,
    reason: str,
) -> dict[str, Any]:
    rejected = not verify_certificate(claim, observations, certificate)
    return {
        "case": case,
        "expected_decision_from_scope_and_source_facts": "certificate_rejected",
        "actual_decision": "certificate_rejected" if rejected else "certificate_accepted",
        "proof_type": certificate.proof_type,
        "certificate_valid": not rejected,
        "unsafe_certified_commit": not rejected,
        "pass": rejected,
        "reason": reason,
    }


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
    rows.append(
        evaluated_row(
            "empty_page_requested_for_a_but_labelled_b",
            replace(exists, claim_id="exists-b", scope=(cell_b,)),
            [obs("relabelled-empty", cell_b, request_cell=cell_a)],
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
    for case, foreign_source in {
        "mixed_query_signature_page_chain": replace(
            SOURCE, query_signature="different-query"
        ),
        "mixed_authentication_subject_page_chain": replace(
            SOURCE, authentication_subject="subject-2"
        ),
        "mixed_scope_schema_page_chain": replace(
            SOURCE, scope_schema_version="joint-v2"
        ),
    }.items():
        rows.append(
            evaluated_row(
                case,
                exists,
                [
                    obs(f"{case}-0", cell_a, next_cursor="next"),
                    obs(f"{case}-1", cell_a, cursor="next", source=foreign_source),
                ],
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

    witness_page = obs(
        "witness-conflict",
        cell_a,
        next_cursor="next",
        records=(Record("inside-conflict", cell_a, True, True),),
    )
    conflicting_page = obs("witness-conflict-terminal", cell_a)
    witness_left = evaluated_row(
        "witness_same_cursor_conflict_order_1",
        exists,
        [witness_page, conflicting_page],
        "UNKNOWN",
    )
    witness_right = evaluated_row(
        "witness_same_cursor_conflict_order_2",
        exists,
        [conflicting_page, witness_page],
        "UNKNOWN",
    )
    stable = witness_left["certificate_digest"] == witness_right["certificate_digest"]
    witness_left["permutation_certificate_stable"] = stable
    witness_right["permutation_certificate_stable"] = stable
    witness_left["pass"] = bool(witness_left["pass"] and stable)
    witness_right["pass"] = bool(witness_right["pass"] and stable)
    rows.extend((witness_left, witness_right))

    rows.append(
        evaluated_row(
            "witness_plus_wrong_bound_continuation",
            exists,
            [
                obs(
                    "bound-witness",
                    cell_a,
                    next_cursor="next",
                    records=(Record("inside-bound", cell_a, True, True),),
                ),
                obs(
                    "wrong-bound-continuation",
                    cell_a,
                    cursor="next",
                    request_cell=cell_b,
                ),
            ],
            "UNKNOWN",
        )
    )

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
        "adapter_version_replacement": replace(SOURCE, adapter_version="adapter-v2"),
        "request_serialization_replacement": replace(
            SOURCE, request_serialization_version="canonical-json-v2"
        ),
    }
    for case, replacement_source in replacements.items():
        replacement_trace = [obs("complete", cell_a, source=replacement_source)]
        rows.append(
            certificate_rejection_row(
                case,
                exists,
                replacement_trace,
                original_certificate,
                "source identity mutation must invalidate the original certificate",
            )
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
    rows.append(
        certificate_rejection_row(
            "forged_out_of_scope_witness_certificate",
            exists,
            mismatch_trace,
            forged,
            "second verifier path must reject evaluator-shaped forged evidence",
        )
    )

    complete_trace = [obs("certificate-base", cell_a)]
    complete_certificate = evaluate_claim(exists, complete_trace).certificate
    certificate_mutations = {
        "certificate_hidden_conflict": [
            complete_trace[0],
            obs("certificate-hidden-conflict", cell_a, next_cursor="next"),
        ],
        "certificate_cursor_loop": [
            obs("certificate-loop-0", cell_a, next_cursor="next"),
            obs("certificate-loop-1", cell_a, cursor="next", next_cursor=0),
        ],
        "certificate_wrong_termination": [
            obs("certificate-base", cell_a, next_cursor="missing"),
        ],
        "certificate_wrong_cell_binding": [
            obs("certificate-base", cell_a, request_cell=cell_b),
        ],
    }
    for case, mutation_trace in certificate_mutations.items():
        rows.append(
            certificate_rejection_row(
                case,
                exists,
                mutation_trace,
                complete_certificate,
                "mutated observation set must invalidate the original certificate",
            )
        )

    two_cell_claim = replace(exists, claim_id="two-cell", scope=(cell_a, cell_b))
    first = obs("two-cell-a", cell_a)
    foreign = obs(
        "two-cell-b-foreign",
        cell_b,
        source=replace(SOURCE, connector_id="connector-b"),
    )
    insufficient = evaluate_claim(two_cell_claim, [first, foreign]).certificate
    cross_source_forgery = replace(
        insufficient,
        decision="FALSE",
        proof_type="joint_scope_coverage",
        covered_cells=(cell_a, cell_b),
        missing_cells=(),
        observation_digests=(first.digest, foreign.digest),
        reason="complete source-bound page chains cover the exact joint claim scope",
    )
    rows.append(
        certificate_rejection_row(
            "certificate_cross_source_coverage",
            two_cell_claim,
            [first, foreign],
            cross_source_forgery,
            "pages from different sources cannot certify one claim scope",
        )
    )

    return {
        "experiment": "request_bound_soundness_counterexamples_v004",
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
