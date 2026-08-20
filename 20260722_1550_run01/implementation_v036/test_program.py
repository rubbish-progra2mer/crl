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

    def test_difference_removes_exact_shared_fields(self) -> None:
        left = {"api_name": "Search", "parameters": {"query": "x", "limit": 5}}
        right = {"api_name": "Search", "parameters": {"query": "y", "limit": 5}}
        left_delta, right_delta, _, _, meta = program.build_difference(left, right)
        self.assertNotIn("arg.limit", left_delta)
        self.assertNotIn("arg.limit", right_delta)
        self.assertIn("arg.query", left_delta)
        self.assertEqual(meta["difference_keys"], ["arg.query"])
        self.assertEqual(meta["shared_field_count"], 3)

    def test_absent_argument_is_explicit(self) -> None:
        left = {"name": "Login", "parameters": {"user": "u", "password": "p"}}
        right = {"name": "Login", "parameters": {"user": "u"}}
        _, right_delta, _, _, meta = program.build_difference(left, right)
        self.assertIn("[ABSENT]", right_delta)
        self.assertEqual(meta["difference_keys"], ["arg.password"])

    def test_text_difference_spans_are_symmetric(self) -> None:
        left, right, left_call, right_call, meta = program.build_difference(
            "ask for the file", "open the file"
        )
        self.assertIsNone(left_call)
        self.assertIsNone(right_call)
        self.assertIn("ask", left)
        self.assertIn("open", right)
        self.assertGreater(meta["left_span_count"], 0)
        self.assertGreater(meta["right_span_count"], 0)

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


if __name__ == "__main__":
    unittest.main()
