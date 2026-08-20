from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

import audit
import program


def test_views_preserve_operation_and_recursive_arguments() -> None:
    tool = {
        "name": "weather.getByCoordinatesDate",
        "description": "Get weather for coordinates and date",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "ISO date"},
                "location": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"},
                    },
                    "required": ["latitude", "longitude"],
                },
            },
            "required": ["date", "location"],
        },
    }
    views = program.view_texts(tool)
    assert tuple(views) == (
        "full",
        "without_operation",
        "without_arguments",
        "name_only",
    )
    assert "weather get by coordinates date" in views["name_only"]
    assert "operation description" not in views["without_operation"]
    assert "properties location properties latitude type: number" in views[
        "without_operation"
    ]
    assert "argument schema" not in views["without_arguments"]
    assert views["full"].startswith(views["without_arguments"])


def test_dcn_formula_and_controls() -> None:
    matrix = np.asarray(
        [
            [10.0, 8.0, 7.0, 1.0],
            [9.0, 4.0, 8.5, 0.0],
        ],
        dtype=np.float64,
    )
    scores = program.compute_method_scores(matrix)
    assert np.allclose(scores["full_schema"], [10.0, 9.0])
    assert np.allclose(scores["operation_schema"], [7.0, 8.5])
    assert np.allclose(scores["argument_schema"], [8.0, 4.0])
    assert np.allclose(scores["additive_support"], [12.5, 11.75])
    assert np.allclose(scores["max_support"], [13.0, 14.0])
    assert np.allclose(scores["dual_necessity"], [12.0, 9.5])


def test_fold_and_tie_break_are_deterministic() -> None:
    query_id = "multiple_109"
    expected_fold = hashlib.sha256(query_id.encode("utf-8")).digest()[1] % 5
    assert program.fold_for_query(query_id, 5) == expected_fold
    names = ["tool.b", "tool.a"]
    order = program.ranking(names, np.asarray([1.0, 1.0]))
    expected = sorted(
        range(2),
        key=lambda index: hashlib.sha256(names[index].encode("utf-8")).hexdigest(),
    )
    assert order == expected


def test_prepare_examples_rejects_missing_gold() -> None:
    question = {
        "id": "x",
        "question": [[{"role": "user", "content": "do x"}]],
        "function": [{"name": "tool.x", "description": "x", "parameters": {}}],
    }
    gold = {"id": "x", "ground_truth": [{"tool.y": {}}]}
    try:
        program.prepare_examples([question], [question], [gold], 5)
    except ValueError as error:
        assert "gold function absent" in str(error)
    else:
        raise AssertionError("missing gold must fail")


def test_methods_and_candidate_order_are_frozen() -> None:
    assert program.METHODS == (
        "full_schema",
        "operation_schema",
        "argument_schema",
        "additive_support",
        "max_support",
        "dual_necessity",
    )
    assert program.COMPARATORS == program.METHODS[:-1]
    assert Path(program.__file__).name == "program.py"


def test_independent_auditor_matches_text_and_score_formula() -> None:
    tool = {
        "name": "weather.getByCoordinatesDate",
        "description": "Get historical weather",
        "parameters": {"required": ["date"], "properties": {"date": {"type": "string"}}},
    }
    assert audit.independent_views(tool) == program.view_texts(tool)
    matrix = np.asarray([[4.0, 1.0, 3.0, 0.5]], dtype=np.float64)
    expected = program.compute_method_scores(matrix)
    observed = audit.independent_scores(matrix)
    assert tuple(observed) == program.METHODS
    for method in program.METHODS:
        assert np.array_equal(expected[method], observed[method])
