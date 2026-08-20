from __future__ import annotations

import itertools
import unittest
from dataclasses import replace
from unittest.mock import patch

from joint_coverage_kernel import (
    Claim,
    Observation,
    Record,
    ScopeCell,
    SourceIdentity,
    canonical_request_payload,
    evaluate_claim,
    marginal_coverage_would_accept,
    verify_certificate,
)


SOURCE = SourceIdentity(
    "test",
    "list-v1",
    "subject-1",
    "joint-scope-v1",
    "adapter-v1",
    "semantic-normalization-v1",
    "canonical-json-v1",
)


def observation(
    name: str,
    cell: ScopeCell,
    records: tuple[Record, ...] = (),
    *,
    cursor: str | int = 0,
    next_cursor: str | int | None = None,
    snapshot: str = "s1",
    source: SourceIdentity = SOURCE,
    silently_truncated: bool = False,
    request_source: SourceIdentity | None = None,
    request_cell: ScopeCell | None = None,
    request_cursor: str | int | None = None,
    request_snapshot: str | None = None,
    request_payload: str | None = None,
) -> Observation:
    effective_request_source = source if request_source is None else request_source
    effective_request_cell = cell if request_cell is None else request_cell
    effective_request_cursor = cursor if request_cursor is None else request_cursor
    effective_request_snapshot = snapshot if request_snapshot is None else request_snapshot
    payload = (
        canonical_request_payload(
            effective_request_source,
            effective_request_cell,
            effective_request_cursor,
            effective_request_snapshot,
        )
        if request_payload is None
        else request_payload
    )
    return Observation(
        observation_id=name,
        connector_id=source.connector_id,
        cell=cell,
        cursor=cursor,
        next_cursor=next_cursor,
        records=records,
        snapshot_id=snapshot,
        query_signature=source.query_signature,
        authentication_subject=source.authentication_subject,
        scope_schema_version=source.scope_schema_version,
        adapter_version=source.adapter_version,
        semantic_normalization_version=source.semantic_normalization_version,
        request_serialization_version=source.request_serialization_version,
        request_payload=payload,
        silently_truncated=silently_truncated,
    )


class JointCoverageKernelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ar = ScopeCell("A", "recent", "active")
        self.ao = ScopeCell("A", "old", "active")
        self.br = ScopeCell("B", "recent", "active")
        self.bo = ScopeCell("B", "old", "active")

    def claim(
        self,
        scope: tuple[ScopeCell, ...],
        quantifier: str = "exists",
        *,
        source: SourceIdentity = SOURCE,
        initial_cursor: str | int = 0,
    ) -> Claim:
        return Claim(
            "c",
            quantifier,
            "matches_target",
            scope,
            "s1",
            source,
            initial_cursor=initial_cursor,
        )

    def test_same_observation_changes_permission_by_claim(self) -> None:
        trace = [observation("o", self.ar)]
        local = evaluate_claim(self.claim((self.ar,)), trace)
        global_claim = evaluate_claim(self.claim((self.ar, self.ao)), trace)
        self.assertEqual(local.decision, "FALSE")
        self.assertEqual(global_claim.decision, "UNKNOWN")

    def test_positive_witness_needs_no_global_coverage(self) -> None:
        record = Record("r", self.ar, True, True)
        result = evaluate_claim(
            self.claim((self.ar, self.ao)),
            [observation("o", self.ar, (record,), next_cursor="opaque-next")],
        )
        self.assertEqual(result.decision, "TRUE")
        self.assertEqual(result.certificate.proof_type, "positive_witness")
        self.assertTrue(verify_certificate(self.claim((self.ar, self.ao)), [observation("o", self.ar, (record,), next_cursor="opaque-next")], result.certificate))

    def test_forall_counterexample_is_a_witness(self) -> None:
        record = Record("r", self.ar, False, False)
        claim = Claim("c", "forall", "compliant", (self.ar, self.ao), "s1", SOURCE)
        trace = [observation("o", self.ar, (record,), next_cursor="next")]
        result = evaluate_claim(claim, trace)
        self.assertEqual(result.decision, "FALSE")
        self.assertEqual(result.certificate.proof_type, "counterexample_witness")
        self.assertTrue(verify_certificate(claim, trace, result.certificate))

    def test_out_of_scope_record_cannot_be_exists_witness(self) -> None:
        record = Record("outside", self.br, True, True)
        trace = [observation("misplaced", self.ar, (record,))]
        claim = self.claim((self.ar,))
        result = evaluate_claim(claim, trace)
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertEqual(result.certificate.reason, "evidence conflict prevents a source-bound page-chain proof")
        forged = replace(
            result.certificate,
            decision="TRUE",
            proof_type="positive_witness",
            observation_digests=(trace[0].digest,),
            witness_record_id="outside",
            reason="a source-bound in-scope attested record decides the claim",
        )
        self.assertFalse(verify_certificate(claim, trace, forged))

    def test_out_of_scope_record_cannot_be_forall_counterexample(self) -> None:
        record = Record("outside", self.br, False, False)
        trace = [observation("misplaced", self.ar, (record,))]
        claim = Claim("f", "forall", "compliant", (self.ar,), "s1", SOURCE)
        result = evaluate_claim(claim, trace)
        self.assertEqual(result.decision, "UNKNOWN")
        forged = replace(
            result.certificate,
            decision="FALSE",
            proof_type="counterexample_witness",
            observation_digests=(trace[0].digest,),
            witness_record_id="outside",
            reason="a source-bound in-scope attested record decides the claim",
        )
        self.assertFalse(verify_certificate(claim, trace, forged))

    def test_different_connectors_cannot_compose_one_page_chain(self) -> None:
        foreign = replace(SOURCE, connector_id="foreign")
        first = observation("p0", self.ar, next_cursor="opaque-1")
        second = observation(
            "p1-foreign",
            self.ar,
            cursor="opaque-1",
            next_cursor=None,
            source=foreign,
        )
        claim = self.claim((self.ar,))
        result = evaluate_claim(claim, [first, second])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertTrue(verify_certificate(claim, [first, second], result.certificate))

    def test_empty_response_cannot_be_relabelled_as_another_cell(self) -> None:
        claim = self.claim((self.br,))
        relabelled = observation(
            "actual-request-a-labelled-b",
            self.br,
            request_cell=self.ar,
        )
        result = evaluate_claim(claim, [relabelled])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertEqual(
            result.certificate.reason,
            "evidence conflict prevents a source-bound page-chain proof",
        )
        forged = replace(
            result.certificate,
            decision="FALSE",
            proof_type="joint_scope_coverage",
            observation_digests=(relabelled.digest,),
            covered_cells=(self.br,),
            missing_cells=(),
            reason="complete source-bound page chains cover the exact joint claim scope",
        )
        self.assertFalse(verify_certificate(claim, [relabelled], forged))

    def test_outer_source_relabel_cannot_hide_same_request_witness(self) -> None:
        claim = self.claim((self.ar,))
        empty = observation("empty", self.ar)
        foreign_outer = replace(SOURCE, connector_id="foreign")
        hidden = observation(
            "hidden-witness",
            self.ar,
            (Record("positive", self.ar, True, True),),
            source=foreign_outer,
            request_source=SOURCE,
        )
        left = evaluate_claim(claim, [empty, hidden])
        right = evaluate_claim(claim, [hidden, empty])
        self.assertEqual(left.decision, "UNKNOWN")
        self.assertEqual(right.decision, "UNKNOWN")
        self.assertEqual(left.certificate.digest, right.certificate.digest)
        self.assertTrue(verify_certificate(claim, [empty, hidden], left.certificate))
        self.assertTrue(verify_certificate(claim, [hidden, empty], right.certificate))

    def test_outer_source_relabel_cannot_hide_forall_counterexample(self) -> None:
        claim = Claim("f", "forall", "compliant", (self.ar,), "s1", SOURCE)
        empty = observation("empty", self.ar)
        hidden = observation(
            "hidden-counterexample",
            self.ar,
            (Record("negative", self.ar, False, False),),
            source=replace(SOURCE, connector_id="foreign"),
            request_source=SOURCE,
        )
        result = evaluate_claim(claim, [empty, hidden])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertTrue(verify_certificate(claim, [empty, hidden], result.certificate))

    def test_outer_cell_relabel_cannot_route_request_conflict_out(self) -> None:
        claim = self.claim((self.ar,))
        empty = observation("empty", self.ar)
        hidden = observation(
            "outer-cell-b-payload-a",
            self.br,
            (Record("positive", self.ar, True, True),),
            request_cell=self.ar,
        )
        result = evaluate_claim(claim, [empty, hidden])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertTrue(verify_certificate(claim, [empty, hidden], result.certificate))

    def test_outside_request_cannot_hide_in_scope_record(self) -> None:
        claim = self.claim((self.ar,))
        empty = observation("empty", self.ar)
        hidden = observation(
            "request-b-record-a",
            self.br,
            (Record("positive-a", self.ar, True, True),),
        )
        left = evaluate_claim(claim, [empty, hidden])
        right = evaluate_claim(claim, [hidden, empty])
        self.assertEqual(left.decision, "UNKNOWN")
        self.assertEqual(right.decision, "UNKNOWN")
        self.assertEqual(left.certificate.digest, right.certificate.digest)
        self.assertTrue(verify_certificate(claim, [empty, hidden], left.certificate))

    def test_outside_request_cannot_hide_in_scope_forall_counterexample(self) -> None:
        claim = Claim("f", "forall", "compliant", (self.ar,), "s1", SOURCE)
        empty = observation("empty", self.ar)
        hidden = observation(
            "request-b-record-a",
            self.br,
            (Record("negative-a", self.ar, False, False),),
        )
        result = evaluate_claim(claim, [empty, hidden])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertTrue(verify_certificate(claim, [empty, hidden], result.certificate))

    def test_self_consistent_outside_request_and_record_are_irrelevant(self) -> None:
        claim = self.claim((self.ar,))
        empty = observation("empty", self.ar)
        outside = observation(
            "request-b-record-b",
            self.br,
            (Record("positive-b", self.br, True, True),),
        )
        result = evaluate_claim(claim, [empty, outside])
        self.assertEqual(result.decision, "FALSE")
        self.assertTrue(verify_certificate(claim, [empty, outside], result.certificate))

    def test_outer_snapshot_relabel_cannot_route_request_conflict_out(self) -> None:
        claim = self.claim((self.ar,))
        empty = observation("empty", self.ar)
        hidden = observation(
            "outer-s2-payload-s1",
            self.ar,
            (Record("positive", self.ar, True, True),),
            snapshot="s2",
            request_snapshot="s1",
        )
        result = evaluate_claim(claim, [empty, hidden])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertTrue(verify_certificate(claim, [empty, hidden], result.certificate))

    def test_outer_source_identity_fields_are_cross_checked_before_filtering(self) -> None:
        claim = self.claim((self.ar,))
        empty = observation("empty", self.ar)
        mutations = {
            "operation": replace(SOURCE, query_signature="other-operation"),
            "subject": replace(SOURCE, authentication_subject="subject-2"),
            "schema": replace(SOURCE, scope_schema_version="scope-v2"),
            "adapter": replace(SOURCE, adapter_version="adapter-v2"),
            "semantic_normalization": replace(
                SOURCE, semantic_normalization_version="semantic-normalization-v2"
            ),
            "serialization": replace(
                SOURCE, request_serialization_version="canonical-json-v2"
            ),
        }
        for name, outer_source in mutations.items():
            with self.subTest(name=name):
                hidden = observation(
                    f"hidden-{name}",
                    self.ar,
                    (Record(f"positive-{name}", self.ar, True, True),),
                    source=outer_source,
                    request_source=SOURCE,
                )
                result = evaluate_claim(claim, [empty, hidden])
                self.assertEqual(result.decision, "UNKNOWN")
                self.assertTrue(
                    verify_certificate(claim, [empty, hidden], result.certificate)
                )

    def test_true_foreign_page_is_ignored_when_both_representations_agree(self) -> None:
        claim = self.claim((self.ar,))
        empty = observation("empty", self.ar)
        foreign = replace(SOURCE, connector_id="foreign")
        unrelated = observation(
            "true-foreign",
            self.ar,
            (Record("foreign-positive", self.ar, True, True),),
            source=foreign,
        )
        result = evaluate_claim(claim, [empty, unrelated])
        self.assertEqual(result.decision, "FALSE")
        self.assertTrue(verify_certificate(claim, [empty, unrelated], result.certificate))

    def test_certificate_cannot_hide_outer_label_conflict(self) -> None:
        claim = self.claim((self.ar,))
        empty = observation("empty", self.ar)
        certificate = evaluate_claim(claim, [empty]).certificate
        hidden = observation(
            "hidden",
            self.ar,
            (Record("positive", self.ar, True, True),),
            source=replace(SOURCE, connector_id="foreign"),
            request_source=SOURCE,
        )
        self.assertFalse(verify_certificate(claim, [empty, hidden], certificate))

    def test_noncanonical_payload_targeting_claim_is_unknown(self) -> None:
        claim = self.claim((self.ar,))
        malformed = observation("malformed", self.ar, request_payload="{}")
        result = evaluate_claim(claim, [malformed])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertTrue(verify_certificate(claim, [malformed], result.certificate))

    def test_cross_coordinate_source_snapshot_scope_split_fails_closed(self) -> None:
        foreign = replace(SOURCE, connector_id="foreign")
        cases = (
            (
                self.claim((self.ar,)),
                Record("positive-a", self.ar, True, True),
            ),
            (
                Claim("f", "forall", "compliant", (self.ar,), "s1", SOURCE),
                Record("negative-a", self.ar, False, False),
            ),
        )
        for claim, record in cases:
            clean = observation(f"clean-{claim.quantifier}", self.ar)
            hidden = observation(
                f"split-{claim.quantifier}",
                self.br,
                (record,),
                source=SOURCE,
                snapshot="s2",
                request_source=foreign,
                request_cell=self.br,
                request_snapshot="s1",
            )
            left = evaluate_claim(claim, [clean, hidden])
            right = evaluate_claim(claim, [hidden, clean])
            with self.subTest(quantifier=claim.quantifier):
                self.assertEqual(left.decision, "UNKNOWN")
                self.assertEqual(right.decision, "UNKNOWN")
                self.assertEqual(left.certificate.digest, right.certificate.digest)
                self.assertIn(
                    hidden.digest, left.certificate.audit_observation_digests
                )
                self.assertTrue(
                    verify_certificate(claim, [clean, hidden], left.certificate)
                )

    def test_cross_coordinate_split_mirror_fails_closed(self) -> None:
        foreign = replace(SOURCE, connector_id="foreign")
        claim = self.claim((self.ar,))
        clean = observation("clean", self.ar)
        hidden = observation(
            "split-mirror",
            self.br,
            (Record("positive-a", self.ar, True, True),),
            source=foreign,
            snapshot="s1",
            request_source=SOURCE,
            request_cell=self.br,
            request_snapshot="s2",
        )
        result = evaluate_claim(claim, [clean, hidden])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertIn(hidden.digest, result.certificate.audit_observation_digests)
        self.assertTrue(verify_certificate(claim, [clean, hidden], result.certificate))

    def test_noncanonical_outside_request_with_in_scope_record_is_global_conflict(self) -> None:
        claim = self.claim((self.ar,))
        clean = observation("clean", self.ar)
        noncanonical = canonical_request_payload(SOURCE, self.br, 0, "s1") + " "
        hidden = observation(
            "noncanonical-outside-request",
            self.br,
            (Record("positive-a", self.ar, True, True),),
            request_payload=noncanonical,
        )
        result = evaluate_claim(claim, [clean, hidden])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertIn(hidden.digest, result.certificate.audit_observation_digests)
        self.assertTrue(verify_certificate(claim, [clean, hidden], result.certificate))

    def test_true_foreign_noncanonical_page_records_availability_cost(self) -> None:
        claim = self.claim((self.ar,))
        clean = observation("clean", self.ar)
        foreign = replace(SOURCE, connector_id="foreign")
        invalid_foreign_payload = (
            canonical_request_payload(foreign, self.br, 0, "s2") + " "
        )
        unrelated = observation(
            "foreign-invalid",
            self.br,
            (Record("foreign-b", self.br, True, True),),
            source=foreign,
            snapshot="s2",
            request_payload=invalid_foreign_payload,
        )
        result = evaluate_claim(claim, [clean, unrelated])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertTrue(verify_certificate(claim, [clean, unrelated], result.certificate))

    def test_clean_certificate_cannot_survive_cross_coordinate_split(self) -> None:
        claim = self.claim((self.ar,))
        clean = observation("clean", self.ar)
        certificate = evaluate_claim(claim, [clean]).certificate
        hidden = observation(
            "split-hidden",
            self.br,
            (Record("positive-a", self.ar, True, True),),
            snapshot="s2",
            request_source=replace(SOURCE, connector_id="foreign"),
            request_cell=self.br,
            request_snapshot="s1",
        )
        self.assertFalse(verify_certificate(claim, [clean, hidden], certificate))

    def test_conflicting_same_cursor_is_unknown_and_order_invariant(self) -> None:
        continuing = observation("continue", self.ar, next_cursor="next")
        terminating = observation("terminate", self.ar, next_cursor=None)
        claim = self.claim((self.ar,))
        left = evaluate_claim(claim, [continuing, terminating])
        right = evaluate_claim(claim, [terminating, continuing])
        self.assertEqual(left.decision, "UNKNOWN")
        self.assertEqual(right.decision, "UNKNOWN")
        self.assertEqual(left.certificate.digest, right.certificate.digest)
        self.assertEqual(left.certificate.reason, "evidence conflict prevents a source-bound page-chain proof")

    def test_witness_plus_same_cursor_conflict_is_unknown_in_both_orders(self) -> None:
        witness = observation(
            "witness-continue",
            self.ar,
            (Record("inside", self.ar, True, True),),
            next_cursor="next",
        )
        conflicting = observation("conflicting-termination", self.ar)
        claim = self.claim((self.ar,))
        left = evaluate_claim(claim, [witness, conflicting])
        right = evaluate_claim(claim, [conflicting, witness])
        self.assertEqual(left.decision, "UNKNOWN")
        self.assertEqual(right.decision, "UNKNOWN")
        self.assertEqual(left.certificate.digest, right.certificate.digest)
        self.assertTrue(verify_certificate(claim, [witness, conflicting], left.certificate))
        self.assertTrue(verify_certificate(claim, [conflicting, witness], right.certificate))

    def test_wrong_request_binding_poisoning_a_witness_is_unknown(self) -> None:
        witness = observation(
            "valid-witness",
            self.ar,
            (Record("inside", self.ar, True, True),),
            next_cursor="next",
        )
        wrong_request = observation(
            "wrong-request",
            self.ar,
            cursor="next",
            request_cell=self.ao,
        )
        claim = self.claim((self.ar,))
        result = evaluate_claim(claim, [witness, wrong_request])
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertTrue(verify_certificate(claim, [witness, wrong_request], result.certificate))

    def test_mixed_query_signature_cannot_finish_production_chain(self) -> None:
        claim = self.claim((self.ar,))
        first = observation("p0", self.ar, next_cursor="next")
        second = observation(
            "p1-other-query",
            self.ar,
            cursor="next",
            source=replace(SOURCE, query_signature="other-query"),
        )
        self.assertEqual(evaluate_claim(claim, [first, second]).decision, "UNKNOWN")

    def test_mixed_authentication_subject_cannot_finish_production_chain(self) -> None:
        claim = self.claim((self.ar,))
        first = observation("p0", self.ar, next_cursor="next")
        second = observation(
            "p1-other-subject",
            self.ar,
            cursor="next",
            source=replace(SOURCE, authentication_subject="subject-2"),
        )
        self.assertEqual(evaluate_claim(claim, [first, second]).decision, "UNKNOWN")

    def test_mixed_scope_schema_cannot_finish_production_chain(self) -> None:
        claim = self.claim((self.ar,))
        first = observation("p0", self.ar, next_cursor="next")
        second = observation(
            "p1-other-schema",
            self.ar,
            cursor="next",
            source=replace(SOURCE, scope_schema_version="joint-scope-v2"),
        )
        self.assertEqual(evaluate_claim(claim, [first, second]).decision, "UNKNOWN")

    def test_query_signature_replacement_invalidates_certificate(self) -> None:
        claim = self.claim((self.ar,))
        original = [observation("o", self.ar)]
        certificate = evaluate_claim(claim, original).certificate
        replacement_source = replace(SOURCE, query_signature="different-query")
        replacement = [observation("o", self.ar, source=replacement_source)]
        self.assertFalse(verify_certificate(claim, replacement, certificate))

    def test_authentication_subject_replacement_invalidates_certificate(self) -> None:
        claim = self.claim((self.ar,))
        original = [observation("o", self.ar)]
        certificate = evaluate_claim(claim, original).certificate
        replacement_source = replace(SOURCE, authentication_subject="subject-2")
        replacement = [observation("o", self.ar, source=replacement_source)]
        self.assertFalse(verify_certificate(claim, replacement, certificate))

    def test_scope_schema_replacement_invalidates_certificate(self) -> None:
        claim = self.claim((self.ar,))
        original = [observation("o", self.ar)]
        certificate = evaluate_claim(claim, original).certificate
        replacement_source = replace(SOURCE, scope_schema_version="joint-scope-v2")
        replacement = [observation("o", self.ar, source=replacement_source)]
        self.assertFalse(verify_certificate(claim, replacement, certificate))

    def test_semantic_normalization_replacement_invalidates_certificate(self) -> None:
        claim = self.claim((self.ar,))
        original = [observation("o", self.ar)]
        certificate = evaluate_claim(claim, original).certificate
        replacement_source = replace(
            SOURCE, semantic_normalization_version="semantic-normalization-v2"
        )
        replacement = [observation("o", self.ar, source=replacement_source)]
        self.assertFalse(verify_certificate(claim, replacement, certificate))

    def test_opaque_cursor_protocol_closes_without_order_comparison(self) -> None:
        claim = self.claim((self.ar,), initial_cursor="start-token")
        trace = [
            observation("p0", self.ar, cursor="start-token", next_cursor="z-token"),
            observation("pz", self.ar, cursor="z-token", next_cursor="a-token"),
            observation("pa", self.ar, cursor="a-token", next_cursor=None),
        ]
        result = evaluate_claim(claim, trace)
        self.assertEqual(result.decision, "FALSE")
        self.assertTrue(verify_certificate(claim, trace, result.certificate))

    def test_opaque_cursor_cycle_fails_closed(self) -> None:
        claim = self.claim((self.ar,), initial_cursor="start")
        trace = [
            observation("p0", self.ar, cursor="start", next_cursor="next"),
            observation("p1", self.ar, cursor="next", next_cursor="start"),
        ]
        result = evaluate_claim(claim, trace)
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertEqual(result.certificate.reason, "evidence conflict prevents a source-bound page-chain proof")

    def test_marginal_hole_is_rejected(self) -> None:
        claim = self.claim((self.ar, self.ao, self.br, self.bo))
        diagonal = [observation("ar", self.ar), observation("bo", self.bo)]
        self.assertTrue(marginal_coverage_would_accept(claim.scope, (self.ar, self.bo)))
        result = evaluate_claim(claim, diagonal)
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertEqual(set(result.certificate.missing_cells), {self.ao, self.br})

    def test_incompatible_snapshots_do_not_compose(self) -> None:
        first = observation("p0", self.ar, cursor=0, next_cursor="next", snapshot="s1")
        second = observation("p1", self.ar, cursor="next", next_cursor=None, snapshot="s2")
        result = evaluate_claim(self.claim((self.ar,)), [first, second])
        self.assertEqual(result.decision, "UNKNOWN")

    def test_certificate_detects_observation_replacement(self) -> None:
        claim = self.claim((self.ar,))
        original = [observation("o", self.ar)]
        result = evaluate_claim(claim, original)
        self.assertTrue(verify_certificate(claim, original, result.certificate))
        replacement_record = Record("replacement", self.ar, False, True)
        replacement = [observation("o", self.ar, (replacement_record,))]
        self.assertFalse(verify_certificate(claim, replacement, result.certificate))

    def test_certificate_mutation_corpus_is_rejected(self) -> None:
        claim = self.claim((self.ar,))
        complete = observation("complete", self.ar)
        certificate = evaluate_claim(claim, [complete]).certificate
        mutations = {
            "hidden_conflicting_page": [
                complete,
                observation("conflict", self.ar, next_cursor="next"),
            ],
            "cursor_loop": [
                observation("loop-0", self.ar, next_cursor="next"),
                observation("loop-1", self.ar, cursor="next", next_cursor=0),
            ],
            "wrong_termination": [
                observation("complete", self.ar, next_cursor="unfetched"),
            ],
            "wrong_cell_request_binding": [
                observation("complete", self.ar, request_cell=self.ao),
            ],
        }
        for name, mutated_trace in mutations.items():
            with self.subTest(name=name):
                self.assertFalse(verify_certificate(claim, mutated_trace, certificate))

        two_cell_claim = self.claim((self.ar, self.ao))
        first = observation("ar", self.ar)
        foreign = observation(
            "ao-foreign",
            self.ao,
            source=replace(SOURCE, connector_id="foreign"),
        )
        insufficient = evaluate_claim(two_cell_claim, [first, foreign]).certificate
        cross_source_forgery = replace(
            insufficient,
            decision="FALSE",
            proof_type="joint_scope_coverage",
            covered_cells=(self.ao, self.ar),
            missing_cells=(),
            observation_digests=(first.digest, foreign.digest),
            reason="complete source-bound page chains cover the exact joint claim scope",
        )
        self.assertFalse(
            verify_certificate(two_cell_claim, [first, foreign], cross_source_forgery)
        )

    def test_independent_verifier_does_not_call_production_evaluator(self) -> None:
        claim = self.claim((self.ar,))
        trace = [observation("o", self.ar)]
        certificate = evaluate_claim(claim, trace).certificate
        with patch("joint_coverage_kernel.evaluate_claim", side_effect=AssertionError("must not run")):
            self.assertTrue(verify_certificate(claim, trace, certificate))

    def test_exhaustive_joint_coverage_has_no_false_negative_certificate(self) -> None:
        universe = (self.ar, self.ao, self.br, self.bo)
        for observed_bits in itertools.product((False, True), repeat=len(universe)):
            observations = [
                observation(f"o-{index}", cell)
                for index, (cell, present) in enumerate(zip(universe, observed_bits))
                if present
            ]
            result = evaluate_claim(self.claim(universe), observations)
            expected_complete = all(observed_bits)
            self.assertEqual(result.decision == "FALSE", expected_complete)
            self.assertTrue(verify_certificate(self.claim(universe), observations, result.certificate))


if __name__ == "__main__":
    unittest.main(verbosity=2)
