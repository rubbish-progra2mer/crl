from __future__ import annotations

import importlib.util
import json
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("causal_uptake_eval.py")
SPEC = importlib.util.spec_from_file_location("causal_uptake_eval", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

GENERATOR_PATH = Path(__file__).with_name("generate_suite.py")
GENERATOR_SPEC = importlib.util.spec_from_file_location("generate_suite", GENERATOR_PATH)
assert GENERATOR_SPEC and GENERATOR_SPEC.loader
GENERATOR = importlib.util.module_from_spec(GENERATOR_SPEC)
GENERATOR_SPEC.loader.exec_module(GENERATOR)

ORACLE_PATH = Path(__file__).with_name("independent_oracle.py")
ORACLE_SPEC = importlib.util.spec_from_file_location("independent_oracle", ORACLE_PATH)
assert ORACLE_SPEC and ORACLE_SPEC.loader
ORACLE = importlib.util.module_from_spec(ORACLE_SPEC)
ORACLE_SPEC.loader.exec_module(ORACLE)


def test_case_contract_and_deterministic_relations() -> None:
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    assert len(cases) == 20
    case = cases[0]
    faithful = {
        variant: MODULE.deterministic_answer("faithful", case, variant)
        for variant in MODULE.VARIANTS
    }
    row = MODULE.make_row(
        case=case,
        agent_id="deterministic::faithful",
        backend="deterministic",
        answers=faithful,
        call_records=[],
        warnings=[],
    )
    assert row["metrics"]["bidirectional_relation"] is True
    assert row["metrics"]["repeat_stable"] is True


def test_bidirectional_relation_accepts_selective_uptake_and_rejects_other_flows() -> None:
    case = MODULE.load_cases(Path(__file__).with_name("cases.json"))[0]
    wrong_answers = {
        variant: MODULE.deterministic_answer("wrong_equivariant", case, variant)
        for variant in MODULE.VARIANTS
    }
    wrong_row = MODULE.make_row(
        case=case,
        agent_id="deterministic::wrong_equivariant",
        backend="deterministic",
        answers=wrong_answers,
        call_records=[],
        warnings=[],
    )
    assert wrong_row["metrics"]["exact_base"] is False
    assert wrong_row["metrics"]["bidirectional_relation"] is True
    misdirected_answers = {
        variant: MODULE.deterministic_answer("misdirected_selective", case, variant)
        for variant in MODULE.VARIANTS
    }
    misdirected_row = MODULE.make_row(
        case=case,
        agent_id="deterministic::misdirected_selective",
        backend="deterministic",
        answers=misdirected_answers,
        call_records=[],
        warnings=[],
    )
    assert misdirected_row["metrics"]["selective_change"] is True
    assert misdirected_row["metrics"]["bidirectional_relation"] is False
    repeat_only_answers = {
        variant: MODULE.deterministic_answer(
            "repeat_only_unstable", case, variant
        )
        for variant in MODULE.VARIANTS
    }
    repeat_only_row = MODULE.make_row(
        case=case,
        agent_id="deterministic::repeat_only_unstable",
        backend="deterministic",
        answers=repeat_only_answers,
        call_records=[],
        warnings=[],
    )
    assert repeat_only_row["metrics"]["relevant_relation"] is True
    assert repeat_only_row["metrics"]["irrelevant_invariant"] is True
    assert repeat_only_row["metrics"]["repeat_stable"] is False
    assert repeat_only_row["metrics"]["bidirectional_relation"] is False
    for policy in ("ignore", "distractor", "repeat_only_unstable", "unstable"):
        answers = {
            variant: MODULE.deterministic_answer(policy, case, variant)
            for variant in MODULE.VARIANTS
        }
        row = MODULE.make_row(
            case=case,
            agent_id=f"deterministic::{policy}",
            backend="deterministic",
            answers=answers,
            call_records=[],
            warnings=[],
        )
        assert row["metrics"]["bidirectional_relation"] is False


def test_relation_oracle_does_not_read_exact_answer_anchors() -> None:
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    bijection_case = cases[0]
    source, target = next(iter(bijection_case["relation"]["mapping"].items()))
    assert MODULE.relevant_relation_holds(bijection_case, source, target)
    assert not MODULE.relevant_relation_holds(bijection_case, source, source)
    numeric_case = next(case for case in cases if case["family"] == "valid_sum")
    delta = numeric_case["relation"]["delta"]
    assert MODULE.relevant_relation_holds(numeric_case, "100", str(100 + delta))
    assert not MODULE.relevant_relation_holds(numeric_case, "18", str(19 + delta))


def test_json_parser_and_scalar_enumeration() -> None:
    answer, warning = MODULE.parse_model_answer('{"answer": 18}')
    assert answer == "18"
    assert warning is None
    values = set(MODULE.scalar_strings({"a": [1, True, "x"]}))
    assert values == {"1", "true", "x"}
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    numeric_case = next(case for case in cases if case["family"] == "tier_score")
    identifier_case = next(
        case for case in cases if case["family"] == "filtered_argmin"
    )
    explanation = (
        "Cached guess is 7, but routing_score should be severity (7) "
        "+ bonus (8) = 15."
    )
    assert MODULE.canonicalize_case_answer(numeric_case, explanation) == "15"
    assert (
        MODULE.canonicalize_case_answer(identifier_case, "The answer is M00-A.")
        == "M00-A"
    )


def test_generator_is_deterministic_and_covers_all_families() -> None:
    spec = json.loads(Path(__file__).with_name("suite_spec.json").read_text(encoding="utf-8"))
    first = GENERATOR.generate_cases(spec)
    second = GENERATOR.generate_cases(spec)
    assert first == second
    assert len(first) == 20
    assert {case["family"] for case in first} == set(spec["families"])


def test_order_is_factored_into_a_separate_control_and_shortcuts_fail() -> None:
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    identifier_cases = [
        case
        for case in cases
        if case["family"] in {"filtered_argmin", "latest_confirmed"}
    ]
    for case in identifier_cases:
        collection = "items" if case["family"] == "filtered_argmin" else "events"
        identifier = "item_id" if case["family"] == "filtered_argmin" else "event_id"
        base_order = tuple(
            record[identifier]
            for record in case["tool_results"]["base"][collection]
        )
        for variant in ("irrelevant_plain", "irrelevant_adversarial"):
            variant_order = tuple(
                record[identifier]
                for record in case["tool_results"][variant][collection]
            )
            assert variant_order == base_order
        order_only = tuple(
            record[identifier]
            for record in case["tool_results"]["order_only"][collection]
        )
        assert order_only != base_order
    for policy in ("position_first", "position_third"):
        passed = 0
        for case in cases:
            answers = {
                variant: MODULE.deterministic_answer(policy, case, variant)
                for variant in MODULE.VARIANTS
            }
            row = MODULE.make_row(
                case=case,
                agent_id=f"deterministic::{policy}",
                backend="deterministic",
                answers=answers,
                call_records=[],
                warnings=[],
            )
            passed += int(row["metrics"]["bidirectional_relation"])
        assert passed == 0


def test_independent_oracle_recomputes_all_frozen_cases() -> None:
    payload = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))
    result = ORACLE.validate_suite(payload)
    assert result["case_count"] == 20
    assert result["passed_count"] == 20
    assert result["all_passed"] is True
