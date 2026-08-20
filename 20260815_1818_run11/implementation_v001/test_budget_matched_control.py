from __future__ import annotations

import json
from pathlib import Path

import budget_matched_control as module


CASES_PATH = Path(__file__).with_name("cases.json")


def first_case() -> dict:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"][0]


def base_answers(case: dict) -> dict[str, str]:
    expected = case["expected"]
    answers = {
        "base": str(expected["base"]),
        "relevant": str(expected["relevant"]),
        "irrelevant_plain": str(expected["irrelevant_plain"]),
        "irrelevant_adversarial": str(expected["irrelevant_adversarial"]),
        "order_only": str(expected["order_only"]),
    }
    answers.update({f"repeat_{index}": str(expected["base"]) for index in range(1, 6)})
    return answers


def row(case: dict, answers: dict[str, str]) -> dict:
    return module.build_row(
        case=case,
        agent_id="test-agent",
        experiment_seed=123,
        answers=answers,
        calls=[],
        warnings=[],
    )


def test_groups_have_equal_budget_and_ten_interleaved_calls() -> None:
    assert len(module.TRANSFORM_GROUP) == 6
    assert len(module.REPEAT_CONTROL_GROUP) == 6
    assert len(module.CALL_IDS) == 10
    assert set(module.TRANSFORM_GROUP) & set(module.REPEAT_CONTROL_GROUP) == {
        "base",
        "repeat_1",
    }
    assert all(
        module.source_variant(call_id) == "base"
        for call_id in module.REPEAT_CONTROL_GROUP
    )


def test_build_row_distinguishes_transform_and_repeat_failures() -> None:
    case = first_case()
    answers = base_answers(case)
    clean = row(case, answers)
    assert clean["metrics"]["transform_pass"] is True
    assert clean["metrics"]["repeat_control_pass"] is True

    transform_answers = dict(answers)
    transform_answers["irrelevant_plain"] = "not-the-base-answer"
    transform_only = row(case, transform_answers)
    assert transform_only["metrics"]["transform_fail"] is True
    assert transform_only["metrics"]["repeat_control_fail"] is False

    control_answers = dict(answers)
    control_answers["repeat_5"] = "not-the-base-answer"
    control_only = row(case, control_answers)
    assert control_only["metrics"]["transform_fail"] is False
    assert control_only["metrics"]["repeat_control_fail"] is True


def test_paired_summary_uses_base_correct_rows_and_discordant_counts() -> None:
    case = first_case()
    clean_answers = base_answers(case)
    clean = row(case, clean_answers)

    transform_answers = dict(clean_answers)
    transform_answers["order_only"] = "wrong-order-answer"
    transform_only = row(case, transform_answers)

    control_answers = dict(clean_answers)
    control_answers["repeat_3"] = "wrong-repeat-answer"
    control_only = row(case, control_answers)

    both_answers = dict(transform_answers)
    both_answers["repeat_4"] = "another-wrong-repeat-answer"
    both = row(case, both_answers)

    wrong_base_answers = dict(clean_answers)
    wrong_base_answers["base"] = "wrong-base"
    wrong_base = row(case, wrong_base_answers)

    summary = module.paired_summary(
        [clean, transform_only, transform_only, control_only, both, wrong_base]
    )
    assert summary["n_all"] == 6
    assert summary["n_base_correct"] == 5
    assert summary["both_pass"] == 1
    assert summary["transform_only_fail"] == 2
    assert summary["control_only_fail"] == 1
    assert summary["both_fail"] == 1
    assert summary["transform_failure_rate"] == 3 / 5
    assert summary["repeat_control_failure_rate"] == 2 / 5
    assert summary["excess_failure_rate"] == 1 / 5
    assert 0.0 <= summary["exact_mcnemar_pvalue"] <= 1.0


def test_exact_mcnemar_handles_no_discordance() -> None:
    assert module.exact_mcnemar_pvalue(0, 0) == 1.0
    assert module.exact_mcnemar_pvalue(10, 0) < 0.01
