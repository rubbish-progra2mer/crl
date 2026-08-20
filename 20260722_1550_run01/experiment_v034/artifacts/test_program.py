from __future__ import annotations

import unittest

import numpy as np

import program


class ProgramTests(unittest.TestCase):
    def test_extracts_nested_and_direct_calls(self) -> None:
        nested = (
            'Reason first.\n{"type":"function","function":'
            '{"name":"Lookup","arguments":{"q":"x"}}}'
        )
        self.assertEqual(
            program.extract_call(nested),
            {"name": "Lookup", "arguments": {"q": "x"}},
        )
        direct = {"api_name": "SearchInbox", "parameters": {"sender": "a@example.com"}}
        self.assertEqual(
            program.extract_call(direct),
            {"name": "SearchInbox", "arguments": {"sender": "a@example.com"}},
        )

    def test_evidence_excludes_label_only_fields(self) -> None:
        row = {
            "history": [{"role": "user", "content": "find x"}],
            "functions": [
                {
                    "name": "Find",
                    "description": "find an item",
                    "parameters": {"type": "object", "properties": {}},
                }
            ],
            "rationale": "SECRET_LABEL_RATIONALE",
            "error type": "SECRET_ERROR_TYPE",
        }
        evidence = program.build_evidence(
            "bfcl", 0, row, {"name": "Find", "parameters": {}}
        )
        joined = "\n".join(evidence.values())
        self.assertNotIn("SECRET_LABEL_RATIONALE", joined)
        self.assertNotIn("SECRET_ERROR_TYPE", joined)
        self.assertIn("Find", evidence["matched_schema"])

    def test_empirical_midrank(self) -> None:
        values = np.asarray([0.0, 1.0, 1.0, 3.0])
        self.assertEqual(program.empirical_percentile(values, -1.0), 0.0)
        self.assertEqual(program.empirical_percentile(values, 1.0), 0.5)
        self.assertEqual(program.empirical_percentile(values, 4.0), 1.0)

    def test_ties_have_half_credit(self) -> None:
        self.assertEqual(program.tie_accuracy(1.0), 1.0)
        self.assertEqual(program.tie_accuracy(0.0), 0.5)
        self.assertEqual(program.tie_accuracy(-1.0), 0.0)

    def test_budget_allocation_is_bounded(self) -> None:
        budgets = program.allocate_budgets([2, 10, 20], 12)
        self.assertEqual(sum(budgets), 12)
        self.assertTrue(all(got <= need for got, need in zip(budgets, [2, 10, 20])))


if __name__ == "__main__":
    unittest.main()
