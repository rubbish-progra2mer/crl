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
    "semantic-normalization-v1",
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
        semantic_normalization_version=source.semantic_normalization_version,
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

    def append_ordered_attack(
        case_prefix: str,
        claim: Claim,
        clean: Observation,
        hidden: Observation,
        independent_world_truth: str,
    ) -> None:
        first = evaluated_row(
            f"{case_prefix}_order_1", claim, [clean, hidden], "UNKNOWN"
        )
        second = evaluated_row(
            f"{case_prefix}_order_2", claim, [hidden, clean], "UNKNOWN"
        )
        stable = first["certificate_digest"] == second["certificate_digest"]
        for row in (first, second):
            row["independent_world_truth"] = independent_world_truth
            row["permutation_certificate_stable"] = stable
            row["pass"] = bool(row["pass"] and stable)
        rows.extend((first, second))
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

    clean_empty = obs("clean-empty", cell_a)
    outer_foreign = replace(SOURCE, connector_id="connector-t")
    hidden_witness = obs(
        "outer-t-payload-s-witness",
        cell_a,
        records=(Record("hidden-positive", cell_a, True, True),),
        source=outer_foreign,
        request_source=SOURCE,
    )
    relabel_left = evaluated_row(
        "outer_source_relabel_exists_order_1",
        exists,
        [clean_empty, hidden_witness],
        "UNKNOWN",
    )
    relabel_right = evaluated_row(
        "outer_source_relabel_exists_order_2",
        exists,
        [hidden_witness, clean_empty],
        "UNKNOWN",
    )
    relabel_stable = (
        relabel_left["certificate_digest"] == relabel_right["certificate_digest"]
    )
    relabel_left["permutation_certificate_stable"] = relabel_stable
    relabel_right["permutation_certificate_stable"] = relabel_stable
    relabel_left["pass"] = bool(relabel_left["pass"] and relabel_stable)
    relabel_right["pass"] = bool(relabel_right["pass"] and relabel_stable)
    rows.extend((relabel_left, relabel_right))

    hidden_counterexample = obs(
        "outer-t-payload-s-counterexample",
        cell_a,
        records=(Record("hidden-negative", cell_a, False, False),),
        source=outer_foreign,
        request_source=SOURCE,
    )
    rows.append(
        evaluated_row(
            "outer_source_relabel_forall",
            forall,
            [clean_empty, hidden_counterexample],
            "UNKNOWN",
        )
    )

    for case, outer_source in {
        "outer_operation_relabel": replace(
            SOURCE, query_signature="different-operation"
        ),
        "outer_subject_relabel": replace(
            SOURCE, authentication_subject="subject-2"
        ),
        "outer_scope_schema_relabel": replace(
            SOURCE, scope_schema_version="joint-v2"
        ),
        "outer_adapter_relabel": replace(SOURCE, adapter_version="adapter-v2"),
        "outer_semantic_normalization_relabel": replace(
            SOURCE,
            semantic_normalization_version="semantic-normalization-v2",
        ),
        "outer_serialization_relabel": replace(
            SOURCE, request_serialization_version="canonical-json-v2"
        ),
    }.items():
        rows.append(
            evaluated_row(
                case,
                exists,
                [
                    clean_empty,
                    obs(
                        f"{case}-hidden",
                        cell_a,
                        records=(Record(f"{case}-positive", cell_a, True, True),),
                        source=outer_source,
                        request_source=SOURCE,
                    ),
                ],
                "UNKNOWN",
            )
        )

    rows.append(
        evaluated_row(
            "outer_cell_relabel",
            exists,
            [
                clean_empty,
                obs(
                    "outer-b-payload-a",
                    cell_b,
                    records=(Record("outer-cell-positive", cell_a, True, True),),
                    request_cell=cell_a,
                ),
            ],
            "UNKNOWN",
        )
    )
    rows.append(
        evaluated_row(
            "outer_snapshot_relabel",
            exists,
            [
                clean_empty,
                obs(
                    "outer-s2-payload-s1",
                    cell_a,
                    records=(Record("outer-snapshot-positive", cell_a, True, True),),
                    snapshot="s2",
                    request_snapshot="s1",
                ),
            ],
            "UNKNOWN",
        )
    )
    rows.append(
        evaluated_row(
            "outer_cursor_relabel",
            exists,
            [
                clean_empty,
                obs(
                    "outer-other-cursor-payload-zero",
                    cell_a,
                    cursor="other",
                    request_cursor=0,
                ),
            ],
            "UNKNOWN",
        )
    )

    true_foreign = replace(SOURCE, connector_id="true-foreign")
    rows.append(
        evaluated_row(
            "self_consistent_foreign_page_is_irrelevant",
            exists,
            [
                clean_empty,
                obs(
                    "true-foreign-positive",
                    cell_a,
                    records=(Record("foreign-positive", cell_a, True, True),),
                    source=true_foreign,
                ),
            ],
            "FALSE",
        )
    )

    clean_certificate = evaluate_claim(exists, [clean_empty]).certificate
    rows.append(
        certificate_rejection_row(
            "certificate_cannot_hide_outer_source_relabel",
            exists,
            [clean_empty, hidden_witness],
            clean_certificate,
            "certificate must bind the full relevant observation multiset",
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
        "semantic_normalization_replacement": replace(
            SOURCE,
            semantic_normalization_version="semantic-normalization-v2",
        ),
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

    mismatch_matrix: list[tuple[str, dict[str, Any]]] = [
        (
            "connector",
            {
                "source": replace(SOURCE, connector_id="matrix-connector"),
                "request_source": SOURCE,
            },
        ),
        (
            "operation",
            {
                "source": replace(SOURCE, query_signature="matrix-operation"),
                "request_source": SOURCE,
            },
        ),
        (
            "authentication_subject",
            {
                "source": replace(
                    SOURCE, authentication_subject="matrix-subject"
                ),
                "request_source": SOURCE,
            },
        ),
        (
            "scope_schema",
            {
                "source": replace(SOURCE, scope_schema_version="matrix-scope"),
                "request_source": SOURCE,
            },
        ),
        (
            "adapter_version",
            {
                "source": replace(SOURCE, adapter_version="matrix-adapter"),
                "request_source": SOURCE,
            },
        ),
        (
            "semantic_normalization_version",
            {
                "source": replace(
                    SOURCE,
                    semantic_normalization_version="matrix-normalization",
                ),
                "request_source": SOURCE,
            },
        ),
        (
            "serialization_version",
            {
                "source": replace(
                    SOURCE,
                    request_serialization_version="matrix-serialization",
                ),
                "request_source": SOURCE,
            },
        ),
        (
            "cell",
            {
                "cell": cell_b,
                "request_cell": cell_a,
            },
        ),
        (
            "snapshot",
            {
                "snapshot": "matrix-snapshot",
                "request_snapshot": "s1",
            },
        ),
        (
            "cursor",
            {
                "cursor": "matrix-cursor",
                "request_cursor": 0,
            },
        ),
    ]
    for field, raw_kwargs in mismatch_matrix:
        for quantifier, matrix_claim in (("exists", exists), ("forall", forall)):
            matrix_record = Record(
                f"matrix-{field}-{quantifier}",
                cell_a,
                quantifier == "exists",
                quantifier != "forall",
            )
            kwargs = dict(raw_kwargs)
            outer_cell = kwargs.pop("cell", cell_a)
            hidden = obs(
                f"matrix-{field}-{quantifier}-hidden",
                outer_cell,
                records=(matrix_record,),
                **kwargs,
            )
            clean = obs(f"matrix-{field}-{quantifier}-clean", cell_a)
            first = evaluated_row(
                f"matrix_{field}_{quantifier}_order_1",
                matrix_claim,
                [clean, hidden],
                "UNKNOWN",
            )
            second = evaluated_row(
                f"matrix_{field}_{quantifier}_order_2",
                matrix_claim,
                [hidden, clean],
                "UNKNOWN",
            )
            stable = first["certificate_digest"] == second["certificate_digest"]
            first["permutation_certificate_stable"] = stable
            second["permutation_certificate_stable"] = stable
            first["pass"] = bool(first["pass"] and stable)
            second["pass"] = bool(second["pass"] and stable)
            rows.extend((first, second))

    for quantifier, record, matrix_claim in (
        (
            "exists",
            Record("outside-request-in-scope-positive", cell_a, True, True),
            exists,
        ),
        (
            "forall",
            Record("outside-request-in-scope-negative", cell_a, False, False),
            forall,
        ),
    ):
        clean = obs(f"record-route-{quantifier}-clean", cell_a)
        hidden = obs(
            f"record-route-{quantifier}-hidden",
            cell_b,
            records=(record,),
        )
        first = evaluated_row(
            f"outside_request_in_scope_record_{quantifier}_order_1",
            matrix_claim,
            [clean, hidden],
            "UNKNOWN",
        )
        second = evaluated_row(
            f"outside_request_in_scope_record_{quantifier}_order_2",
            matrix_claim,
            [hidden, clean],
            "UNKNOWN",
        )
        stable = first["certificate_digest"] == second["certificate_digest"]
        first["permutation_certificate_stable"] = stable
        second["permutation_certificate_stable"] = stable
        first["pass"] = bool(first["pass"] and stable)
        second["pass"] = bool(second["pass"] and stable)
        rows.extend((first, second))

    split_source_mutations = {
        "connector": replace(SOURCE, connector_id="split-connector"),
        "operation": replace(SOURCE, query_signature="split-operation"),
        "authentication_subject": replace(
            SOURCE, authentication_subject="split-subject"
        ),
        "scope_schema": replace(
            SOURCE, scope_schema_version="split-scope"
        ),
        "adapter_version": replace(SOURCE, adapter_version="split-adapter"),
        "semantic_normalization_version": replace(
            SOURCE, semantic_normalization_version="split-normalization"
        ),
        "serialization_version": replace(
            SOURCE, request_serialization_version="split-serialization"
        ),
    }
    for field, foreign_source in split_source_mutations.items():
        for quantifier, split_claim in (("exists", exists), ("forall", forall)):
            record = Record(
                f"split-{field}-{quantifier}-record",
                cell_a,
                quantifier == "exists",
                quantifier != "forall",
            )
            truth = "TRUE" if quantifier == "exists" else "FALSE"
            clean = obs(f"split-{field}-{quantifier}-clean", cell_a)
            outer_match_hidden = obs(
                f"split-{field}-{quantifier}-outer-match",
                cell_b,
                records=(record,),
                source=SOURCE,
                snapshot="s2",
                request_source=foreign_source,
                request_cell=cell_b,
                request_snapshot="s1",
            )
            append_ordered_attack(
                f"cross_coordinate_{field}_{quantifier}_outer_source_match",
                split_claim,
                clean,
                outer_match_hidden,
                truth,
            )
            payload_match_hidden = obs(
                f"split-{field}-{quantifier}-payload-match",
                cell_b,
                records=(record,),
                source=foreign_source,
                snapshot="s1",
                request_source=SOURCE,
                request_cell=cell_b,
                request_snapshot="s2",
            )
            append_ordered_attack(
                f"cross_coordinate_{field}_{quantifier}_payload_source_match",
                split_claim,
                clean,
                payload_match_hidden,
                truth,
            )

    for quantifier, split_claim, record, truth in (
        (
            "exists",
            exists,
            Record("noncanonical-positive-a", cell_a, True, True),
            "TRUE",
        ),
        (
            "forall",
            forall,
            Record("noncanonical-negative-a", cell_a, False, False),
            "FALSE",
        ),
    ):
        noncanonical_payload = canonical_request_payload(
            SOURCE, cell_b, 0, "s1"
        ) + " "
        hidden = obs(
            f"noncanonical-{quantifier}-hidden",
            cell_b,
            records=(record,),
            request_payload=noncanonical_payload,
        )
        append_ordered_attack(
            f"noncanonical_outside_request_in_scope_record_{quantifier}",
            split_claim,
            obs(f"noncanonical-{quantifier}-clean", cell_a),
            hidden,
            truth,
        )

    clean_for_certificate = obs("split-certificate-clean", cell_a)
    clean_certificate = evaluate_claim(exists, [clean_for_certificate]).certificate
    split_hidden = obs(
        "split-certificate-hidden",
        cell_b,
        records=(Record("split-certificate-positive", cell_a, True, True),),
        snapshot="s2",
        request_source=replace(SOURCE, connector_id="split-certificate-foreign"),
        request_cell=cell_b,
        request_snapshot="s1",
    )
    rows.append(
        certificate_rejection_row(
            "certificate_cannot_hide_cross_coordinate_split",
            exists,
            [clean_for_certificate, split_hidden],
            clean_certificate,
            "global retained-input audit commitment must include the split page",
        )
    )
    noncanonical_hidden = obs(
        "noncanonical-certificate-hidden",
        cell_b,
        request_payload=canonical_request_payload(SOURCE, cell_b, 0, "s1")
        + " ",
    )
    rows.append(
        certificate_rejection_row(
            "certificate_cannot_hide_noncanonical_payload",
            exists,
            [clean_for_certificate, noncanonical_hidden],
            clean_certificate,
            "an invalid canonical payload is a global retained-input conflict",
        )
    )

    foreign_source = replace(SOURCE, connector_id="true-foreign")
    foreign_invalid = obs(
        "true-foreign-noncanonical",
        cell_b,
        records=(Record("true-foreign-b", cell_b, True, True),),
        source=foreign_source,
        snapshot="s2",
        request_payload=canonical_request_payload(
            foreign_source, cell_b, 0, "s2"
        )
        + " ",
    )
    availability_row = evaluated_row(
        "true_foreign_noncanonical_payload_is_global_conflict",
        exists,
        [obs("true-foreign-control-clean", cell_a), foreign_invalid],
        "UNKNOWN",
    )
    availability_row["independent_world_truth"] = "FALSE"
    availability_row["availability_cost"] = (
        "a retained noncanonical page poisons unrelated claims without a trusted router"
    )
    rows.append(availability_row)

    clean = obs("record-route-control-clean", cell_a)
    outside_consistent = obs(
        "record-route-control-outside",
        cell_b,
        records=(Record("outside-positive", cell_b, True, True),),
    )
    rows.append(
        evaluated_row(
            "self_consistent_outside_request_and_record_are_irrelevant",
            exists,
            [clean, outside_consistent],
            "FALSE",
        )
    )
    clean_certificate = evaluate_claim(exists, [clean]).certificate
    record_routed_conflict = obs(
        "record-route-certificate-hidden",
        cell_b,
        records=(Record("record-route-positive", cell_a, True, True),),
    )
    rows.append(
        certificate_rejection_row(
            "certificate_cannot_hide_record_routed_conflict",
            exists,
            [clean, record_routed_conflict],
            clean_certificate,
            "global coherence rejects a record whose decoded cell differs from its request",
        )
    )

    # v006 reviewer counterexample: a representation-version field previously acted
    # as a relevance gate.  The exact outer-v1/B, payload-v1/A, record-B split must
    # now fail closed for both existential and universal claims in either order.
    version_v2 = replace(
        SOURCE, semantic_normalization_version="semantic-normalization-v2"
    )
    exists_b_v2 = Claim(
        "exists-b-v2", "exists", "matches_target", (cell_b,), "s1", version_v2
    )
    forall_b_v2 = Claim(
        "forall-b-v2", "forall", "compliant", (cell_b,), "s1", version_v2
    )
    for quantifier, version_claim, hidden_record, truth in (
        (
            "exists",
            exists_b_v2,
            Record("v1-positive-b", cell_b, True, True),
            "TRUE",
        ),
        (
            "forall",
            forall_b_v2,
            Record("v1-negative-b", cell_b, False, False),
            "FALSE",
        ),
    ):
        version_clean = obs(
            f"v2-{quantifier}-clean-b", cell_b, source=version_v2
        )
        version_hidden = obs(
            f"v1-{quantifier}-outer-b-payload-a-record-b",
            cell_b,
            records=(hidden_record,),
            source=SOURCE,
            request_source=SOURCE,
            request_cell=cell_a,
        )
        append_ordered_attack(
            f"v006_normalization_version_gate_bypass_{quantifier}",
            version_claim,
            version_clean,
            version_hidden,
            truth,
        )
        old_version_certificate = evaluate_claim(
            version_claim, [version_clean]
        ).certificate
        rows.append(
            certificate_rejection_row(
                f"v006_normalization_old_certificate_rejected_{quantifier}",
                version_claim,
                [version_clean, version_hidden],
                old_version_certificate,
                "the global audit commitment cannot omit the version-gate attack page",
            )
        )

    # A self-consistent page is semantically relevant before its representation
    # version is checked.  Each representation mismatch therefore yields UNKNOWN.
    representation_mutations = {
        "scope_schema_version": replace(SOURCE, scope_schema_version="joint-v2"),
        "adapter_version": replace(SOURCE, adapter_version="adapter-v2"),
        "semantic_normalization_version": replace(
            SOURCE, semantic_normalization_version="semantic-normalization-v2"
        ),
        "request_serialization_version": replace(
            SOURCE, request_serialization_version="canonical-json-v2"
        ),
    }
    for field, mismatched_source in representation_mutations.items():
        rows.append(
            evaluated_row(
                f"semantically_relevant_{field}_mismatch",
                replace(exists, claim_id=f"representation-{field}"),
                [
                    obs(
                        f"representation-{field}-page",
                        cell_a,
                        source=mismatched_source,
                    )
                ],
                "UNKNOWN",
            )
        )

    # Reviewer 1's common-wrong-authentication construction is globally
    # incoherent because request A carries a decoded record for B.
    wrong_auth = replace(SOURCE, authentication_subject="subject-bob")
    exists_b = Claim("exists-b", "exists", "matches_target", (cell_b,), "s1", SOURCE)
    forall_b = Claim("forall-b", "forall", "compliant", (cell_b,), "s1", SOURCE)
    for quantifier, wrong_auth_claim, wrong_auth_record, truth in (
        ("exists", exists_b, Record("bob-positive-b", cell_b, True, True), "TRUE"),
        ("forall", forall_b, Record("bob-negative-b", cell_b, False, False), "FALSE"),
    ):
        append_ordered_attack(
            f"shared_wrong_auth_request_a_record_b_{quantifier}",
            wrong_auth_claim,
            obs(f"wrong-auth-{quantifier}-clean-b", cell_b),
            obs(
                f"wrong-auth-{quantifier}-request-a-record-b",
                cell_a,
                records=(wrong_auth_record,),
                source=wrong_auth,
            ),
            truth,
        )

    # A truly foreign but self-consistent page remains semantically irrelevant;
    # nevertheless it is committed by the global audit and invalidates old bytes.
    audit_clean = obs("global-audit-clean", cell_a)
    audit_certificate = evaluate_claim(exists, [audit_clean]).certificate
    consistent_foreign = obs(
        "global-audit-consistent-foreign",
        cell_b,
        source=foreign_source,
        snapshot="s2",
    )
    rows.append(
        evaluated_row(
            "consistent_foreign_page_remains_semantically_irrelevant",
            exists,
            [audit_clean, consistent_foreign],
            "FALSE",
        )
    )
    rows.append(
        certificate_rejection_row(
            "consistent_foreign_page_invalidates_old_global_audit_certificate",
            exists,
            [audit_clean, consistent_foreign],
            audit_certificate,
            "all retained attested inputs are committed even when semantically foreign",
        )
    )

    return {
        "experiment": "cross_representation_soundness_counterexamples_v007",
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
