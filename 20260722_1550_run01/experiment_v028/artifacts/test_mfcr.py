from __future__ import annotations

import numpy as np

from program import (
    field_texts,
    fit_bundle,
    fold_for_query,
    pair_training,
    prepare_examples,
    ranking,
    score_bundle,
)


CONFIG = {
    "field_order": ["full", "operation", "arguments"],
    "logistic_c": 1.0,
    "logistic_max_iter": 2000,
    "seed": 12027,
}


def test_field_views_are_deterministic_and_keep_embedded_schema_content() -> None:
    tool = {
        "name": "calendarEvent.create_item",
        "description": "Create an event.",
        "parameters": {
            "type": "dict",
            "properties": {
                "required": ["title", "startTime"],
                "title": {"type": "string", "description": "Event title."},
                "startTime": {
                    "type": "string",
                    "description": "Start time.",
                    "enum": ["morning", "evening"],
                },
            },
        },
    }
    first = field_texts(tool)
    second = field_texts(tool)
    assert first == second
    assert set(first) == {"full", "operation", "arguments"}
    assert "calendar event create item" in first["operation"]
    assert "title" in first["arguments"]
    assert "start time" in first["arguments"]
    assert "morning evening" in first["arguments"]
    assert first["full"] == first["operation"] + ". " + first["arguments"]


def test_prepare_examples_requires_matching_queries_and_gold_in_menu() -> None:
    question = {"id": "q1", "question": [[{"role": "user", "content": "find weather"}]]}
    expanded = {
        **question,
        "function": [
            {"name": "weather.get", "description": "Get weather", "parameters": {}},
            {"name": "calendar.get", "description": "Get event", "parameters": {}},
        ],
    }
    gold = {"id": "q1", "ground_truth": [{"weather.get": {}}]}
    examples = prepare_examples([expanded], [question], [gold], 5)
    assert len(examples) == 1
    assert examples[0]["query"] == "find weather"
    assert examples[0]["gold_names"] == ["weather.get"]
    assert 0 <= examples[0]["fold"] < 5


def test_query_fold_and_tie_break_are_deterministic() -> None:
    assert fold_for_query("multiple_7", 5) == fold_for_query("multiple_7", 5)
    example = {"tool_names": ["tool.b", "tool.a"]}
    first = ranking(example, np.asarray([0.0, 0.0]))
    second = ranking(example, np.asarray([0.0, 0.0]))
    assert first == second
    assert sorted(first) == [0, 1]


def toy_examples() -> tuple[list[dict], list[np.ndarray]]:
    examples = []
    features = []
    for index in range(4):
        examples.append(
            {
                "query_id": f"q{index}",
                "tool_names": ["gold", "near", "far"],
                "gold_names": ["gold"],
                "tools": [{}, {}, {}],
            }
        )
        features.append(
            np.asarray(
                [
                    [2.0 + index * 0.1, 3.0 + index * 0.2, 1.0],
                    [1.5, 1.0 + index * 0.1, 2.0],
                    [-1.0, -0.5, -1.5],
                ],
                dtype=np.float64,
            )
        )
    return examples, features


def test_pair_training_has_both_orientations_and_one_total_weight_per_query() -> None:
    examples, features = toy_examples()
    indexes = np.arange(len(examples), dtype=np.int64)
    x, y, weights, pairs = pair_training(examples, features, indexes)
    assert pairs == 8
    assert x.shape == (16, 3)
    assert np.array_equal(y[0::2], np.ones(8, dtype=np.int64))
    assert np.array_equal(y[1::2], np.zeros(8, dtype=np.int64))
    assert np.allclose(x[0::2], -x[1::2])
    assert np.isclose(np.sum(weights), len(examples))
    assert np.isclose(np.sum(weights[y == 1]), len(examples) / 2)
    assert np.isclose(np.sum(weights[y == 0]), len(examples) / 2)


def test_bundle_uses_query_weighted_pointwise_and_pairwise_models() -> None:
    examples, features = toy_examples()
    indexes = np.arange(len(examples), dtype=np.int64)
    bundle = fit_bundle(examples, features, indexes, CONFIG)
    assert bundle["train_queries"] == 4
    assert bundle["train_tools"] == 12
    assert bundle["train_gold_non_gold_pairs"] == 8
    assert np.isclose(bundle["pair_sample_weight_sum"], 4.0)
    assert set(bundle["pointwise_class_weight"]) == {0, 1}
    scores = score_bundle(bundle, features, indexes)
    assert set(scores) == {0, 1, 2, 3}
    for value in scores.values():
        assert set(value) == {
            "full_cross_encoder",
            "equal_fields",
            "pointwise_fields",
            "pairwise_full",
            "menu_relative_field_contrast",
        }
        assert all(array.shape == (3,) for array in value.values())
