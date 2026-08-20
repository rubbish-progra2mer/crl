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
    evaluate_claim,
    marginal_coverage_would_accept,
    verify_certificate,
)


SOURCE = SourceIdentity("test", "list-v1", "subject-1", "joint-scope-v1")


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
) -> Observation:
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
        foreign = SourceIdentity("foreign", "list-v1", "subject-1", "joint-scope-v1")
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
