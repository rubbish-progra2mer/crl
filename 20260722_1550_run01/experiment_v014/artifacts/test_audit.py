from __future__ import annotations

import unittest

import audit


class FakeOfficial:
    @staticmethod
    def classify_failure_mode(task, trace, answer):
        return "correct" if not task["evaluation_criteria"]["tool_must_be_called"] else "unused"

    @staticmethod
    def detect_tool_skip(task, trace):
        return not trace.get("called", False)

    @staticmethod
    def _answer_correct(task, answer):
        return answer == "grounded"

    @staticmethod
    def detect_output_fabrication(task, trace, answer):
        return bool(trace.get("fabrication_predicate"))


def task(tool_required: bool = True):
    return {"evaluation_criteria": {"tool_must_be_called": tool_required}}


class RequiredGroundingPrecedenceTests(unittest.TestCase):
    def test_ctrl_is_unchanged(self):
        self.assertEqual(
            audit.rgp_classify(task(False), {}, "anything", FakeOfficial),
            "correct",
        )

    def test_missing_expected_tool_remains_tool_skip(self):
        self.assertEqual(
            audit.rgp_classify(task(), {"called": False}, "grounded", FakeOfficial),
            "tool_skip",
        )

    def test_required_grounding_precedes_fabrication_predicate(self):
        self.assertEqual(
            audit.rgp_classify(
                task(),
                {"called": True, "fabrication_predicate": True},
                "grounded",
                FakeOfficial,
            ),
            "correct",
        )

    def test_fabrication_remains_when_required_grounding_fails(self):
        self.assertEqual(
            audit.rgp_classify(
                task(),
                {"called": True, "fabrication_predicate": True},
                "not-grounded",
                FakeOfficial,
            ),
            "output_fabrication",
        )

    def test_unfaithful_nonfabrication_remains_result_ignore(self):
        self.assertEqual(
            audit.rgp_classify(
                task(),
                {"called": True, "fabrication_predicate": False},
                "not-grounded",
                FakeOfficial,
            ),
            "result_ignore",
        )

    def test_macro_f1_exact_on_perfect_predictions(self):
        labels = ["correct", "tool_skip", "correct"]
        self.assertEqual(audit.macro_f1(labels, labels), 1.0)


if __name__ == "__main__":
    unittest.main()
