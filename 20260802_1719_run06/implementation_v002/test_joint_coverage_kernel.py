from __future__ import annotations

import itertools
import unittest

from joint_coverage_kernel import (
    Claim,
    Observation,
    Record,
    ScopeCell,
    evaluate_claim,
    marginal_coverage_would_accept,
    verify_certificate,
)


def observation(
    name: str,
    cell: ScopeCell,
    records: tuple[Record, ...] = (),
    *,
    cursor: int = 0,
    next_cursor: int | None = None,
    snapshot: str = "s1",
) -> Observation:
    return Observation(
        observation_id=name,
        connector_id="test",
        cell=cell,
        cursor=cursor,
        next_cursor=next_cursor,
        records=records,
        snapshot_id=snapshot,
    )


class JointCoverageKernelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ar = ScopeCell("A", "recent", "active")
        self.ao = ScopeCell("A", "old", "active")
        self.br = ScopeCell("B", "recent", "active")
        self.bo = ScopeCell("B", "old", "active")

    def claim(self, scope: tuple[ScopeCell, ...], quantifier: str = "exists") -> Claim:
        return Claim("c", quantifier, "matches_target", scope, "s1")

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
            [observation("o", self.ar, (record,), next_cursor=2)],
        )
        self.assertEqual(result.decision, "TRUE")
        self.assertEqual(result.certificate.proof_type, "positive_witness")

    def test_forall_counterexample_is_a_witness(self) -> None:
        record = Record("r", self.ar, False, False)
        result = evaluate_claim(
            Claim("c", "forall", "compliant", (self.ar, self.ao), "s1"),
            [observation("o", self.ar, (record,), next_cursor=2)],
        )
        self.assertEqual(result.decision, "FALSE")
        self.assertEqual(result.certificate.proof_type, "counterexample_witness")

    def test_marginal_hole_is_rejected(self) -> None:
        claim = self.claim((self.ar, self.ao, self.br, self.bo))
        diagonal = [observation("ar", self.ar), observation("bo", self.bo)]
        self.assertTrue(marginal_coverage_would_accept(claim.scope, (self.ar, self.bo)))
        result = evaluate_claim(claim, diagonal)
        self.assertEqual(result.decision, "UNKNOWN")
        self.assertEqual(set(result.certificate.missing_cells), {self.ao, self.br})

    def test_incompatible_snapshots_do_not_compose(self) -> None:
        first = observation("p0", self.ar, cursor=0, next_cursor=2, snapshot="s1")
        second = observation("p2", self.ar, cursor=2, next_cursor=None, snapshot="s2")
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


if __name__ == "__main__":
    unittest.main()
