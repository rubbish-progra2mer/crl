from __future__ import annotations

import unittest

import program


class ProgramTests(unittest.TestCase):
    def test_extracts_direct_and_embedded_calls(self) -> None:
        direct = {"name": "cp", "parameters": {"source": "a", "destination": "b"}}
        embedded = (
            'reasoning\n{"type":"function","function":{"name":"OCR",'
            '"arguments":{"image":"x.png"}}}'
        )
        self.assertEqual(program.extract_call(direct)["name"], "cp")
        self.assertEqual(program.extract_call(embedded)["name"], "OCR")

    def test_replacement_positions_are_symmetric(self) -> None:
        chosen, rejected = program.difference_positions(
            [10, 20, 30, 40], [10, 21, 31, 40]
        )
        self.assertEqual(chosen, [1, 2])
        self.assertEqual(rejected, [1, 2])

    def test_insertion_uses_following_boundary_on_empty_side(self) -> None:
        chosen, rejected = program.difference_positions(
            [10, 20, 30], [10, 99, 20, 30]
        )
        self.assertEqual(chosen, [1])
        self.assertEqual(rejected, [1])

    def test_end_deletion_uses_preceding_boundary_on_empty_side(self) -> None:
        chosen, rejected = program.difference_positions(
            [10, 20], [10, 20, 30]
        )
        self.assertEqual(chosen, [1])
        self.assertEqual(rejected, [2])

    def test_contract_selection_and_ties(self) -> None:
        functions = [
            {"name": "Read", "description": "read a file"},
            {"name": "Write", "description": "write a file"},
        ]
        contracts = program.implicated_contracts(
            functions,
            [],
            ({"name": "Read", "arguments": {}}, {"name": "Read", "arguments": {}}),
        )
        self.assertIn("read a file", contracts)
        self.assertNotIn("write a file", contracts)
        self.assertEqual(program.tie_accuracy(0.0), 0.5)

    def test_summary_freezes_strongest_control(self) -> None:
        raw = [
            {
                "row_id": "x:0000",
                "cluster": "x:a",
                "source": "x",
                "methods": {
                    "ecds": {"accuracy": 1.0},
                    "full_diff_ll": {"accuracy": 0.0},
                    "full_action_gain": {"accuracy": 1.0},
                    "null_diff_ll": {"accuracy": 0.0},
                    "full_action_ll": {"accuracy": 0.0},
                },
                "scores": {
                    slot: {"full": {"context_truncated": False}}
                    for slot in ("chosen", "rejected")
                },
            }
        ]
        config = {
            "experiment_id": "v037",
            "bootstrap_repeats": 10,
            "seed": 3701,
        }
        summary = program.summarize(raw, config, "development", None)
        self.assertEqual(summary["strongest_control"], "full_action_gain")
        self.assertEqual(summary["candidate_delta"], 0.0)


if __name__ == "__main__":
    unittest.main()
