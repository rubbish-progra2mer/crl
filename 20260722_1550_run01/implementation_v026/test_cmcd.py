from __future__ import annotations

from types import SimpleNamespace

import numpy as np
from scipy import sparse

from program import (
    baseline_indexes,
    fit_bundle,
    fold_for_task,
    pair_indexes,
    pair_matrices,
    prepare_examples,
    score_bundle,
    support_indexes,
)


MODELS = ("model-a", "model-b", "model-c")


def row(row_id: str, task: str, model: str, target: int, text: str | None = None) -> dict:
    return {
        "row_id": row_id,
        "task_id": task,
        "model": model,
        "target": target,
        "text": text or row_id,
    }


class ActionBase:
    @staticmethod
    def action_text(value: dict) -> str:
        return str(value["text"])


def test_eligibility_requires_successful_baseline_from_all_three_models() -> None:
    rows = [
        row("g-a", "good", "model-a", 0),
        row("g-b", "good", "model-b", 0),
        row("g-c", "good", "model-c", 0),
        row("g-x", "good", "model-a", 1),
        row("b-a", "bad", "model-a", 0),
        row("b-b", "bad", "model-b", 0),
        row("b-x", "bad", "model-c", 1),
    ]
    examples, eligible, excluded = prepare_examples(rows, ActionBase, MODELS, 3)
    assert eligible == ["good"]
    assert excluded == ["bad"]
    assert {item["task_id"] for item in examples} == {"good"}


def test_supports_exclude_both_query_and_bundle_target_models() -> None:
    examples, _, _ = prepare_examples(
        [
            row("a0", "task", "model-a", 0),
            row("b0", "task", "model-b", 0),
            row("c0", "task", "model-c", 0),
            row("b1", "task", "model-b", 1),
        ],
        ActionBase,
        MODELS,
        3,
    )
    baselines = baseline_indexes(examples)
    query = next(index for index, item in enumerate(examples) if item["row_id"] == "b1")
    allowed = support_indexes(examples, baselines, query, "model-a")
    assert [examples[index]["row_id"] for index in allowed] == ["c0"]


def test_pair_matrices_have_exact_absolute_deviation_block() -> None:
    matrix = sparse.csr_matrix([[1.0, 3.0], [4.0, 2.0], [0.0, 5.0]])
    no_abs, candidate = pair_matrices(
        matrix,
        np.asarray([0, 1], dtype=np.int64),
        np.asarray([1, 2], dtype=np.int64),
    )
    query = matrix[[0, 1]].toarray()
    reference = matrix[[1, 2]].toarray()
    assert no_abs.shape == candidate.shape == (2, 6)
    assert np.allclose(no_abs.toarray(), np.hstack([query, reference, reference]))
    assert np.allclose(candidate.toarray(), np.hstack([query, reference, np.abs(query - reference)]))


def test_task_fold_is_deterministic_and_bounded() -> None:
    tasks = ("task-a", "task-b", "task-c")
    first = {task: fold_for_task(task, 3) for task in tasks}
    second = {task: fold_for_task(task, 3) for task in tasks}
    assert first == second
    assert all(0 <= fold < 3 for fold in first.values())


class FixedVectorizer:
    def __init__(self, values: dict[str, float]) -> None:
        self.values = values

    def transform(self, texts: list[str]) -> sparse.csr_matrix:
        return sparse.csr_matrix([[self.values[text]] for text in texts], dtype=np.float64)


class ColumnProbability:
    def __init__(self, column: int, scale: float = 10.0) -> None:
        self.column = column
        self.scale = scale

    def predict_proba(self, matrix: sparse.csr_matrix) -> np.ndarray:
        probability = np.asarray(matrix[:, self.column].toarray()).ravel() / self.scale
        return np.column_stack([1.0 - probability, probability])


def test_single_support_and_consensus_use_first_and_mean_respectively() -> None:
    examples = [
        {"row_id": "a1", "task_id": "task", "model": "model-a", "target": 1, "text": "q"},
        {"row_id": "b0", "task_id": "task", "model": "model-b", "target": 0, "text": "b"},
        {"row_id": "c0", "task_id": "task", "model": "model-c", "target": 0, "text": "c"},
    ]
    examples.sort(key=lambda item: (item["task_id"], item["model"], item["row_id"]))
    bundle = {
        "target_model": "model-a",
        "vectorizer": FixedVectorizer({"q": 2.0, "b": 1.0, "c": 5.0}),
        "direct_model": ColumnProbability(0),
        "triple_model": ColumnProbability(0),
        "no_abs_model": ColumnProbability(2),
        "candidate_model": ColumnProbability(2),
    }
    query = np.asarray([0], dtype=np.int64)
    scores, counts, pairs = score_bundle(bundle, examples, baseline_indexes(examples), query)
    assert counts == [2]
    assert pairs == 2
    assert np.isclose(scores["single_support"][0], 0.1)
    assert np.isclose(scores["cross_model_consensus"][0], 0.2)
    assert np.isclose(scores["consensus_no_abs"][0], 0.3)


class TrainingVectorizer:
    vocabulary_ = {"x": 0, "y": 1}

    def fit(self, texts: list[str]) -> "TrainingVectorizer":
        return self

    def transform(self, texts: list[str]) -> sparse.csr_matrix:
        return sparse.csr_matrix(
            [[float(len(text) % 3), float((len(text) + 1) % 5)] for text in texts],
            dtype=np.float64,
        )


class CapturingClassifier:
    def __init__(self) -> None:
        self.class_weight: str | dict[int, float] = "balanced"
        self.sample_weight: np.ndarray | None = None

    def set_params(self, **values: object) -> "CapturingClassifier":
        if "class_weight" in values:
            self.class_weight = values["class_weight"]  # type: ignore[assignment]
        return self

    def fit(
        self, matrix: sparse.csr_matrix, target: np.ndarray, sample_weight: np.ndarray | None = None
    ) -> "CapturingClassifier":
        self.sample_weight = None if sample_weight is None else np.asarray(sample_weight)
        return self


def test_pair_loss_weights_each_query_once_and_balances_query_classes() -> None:
    examples = [
        {"row_id": "b0", "task_id": "task", "model": "model-b", "target": 0, "text": "b0"},
        {"row_id": "b1", "task_id": "task", "model": "model-b", "target": 1, "text": "b1"},
        {"row_id": "c0", "task_id": "task", "model": "model-c", "target": 0, "text": "c0"},
        {"row_id": "c0b", "task_id": "task", "model": "model-c", "target": 0, "text": "c0b"},
        {"row_id": "c1", "task_id": "task", "model": "model-c", "target": 1, "text": "c1"},
    ]
    examples.sort(key=lambda item: (item["task_id"], item["model"], item["row_id"]))
    created: list[CapturingClassifier] = []

    def make_classifier(_: dict) -> CapturingClassifier:
        classifier = CapturingClassifier()
        created.append(classifier)
        return classifier

    base = SimpleNamespace(
        ensure_two_classes=lambda target, label: None,
        make_vectorizer=lambda config: TrainingVectorizer(),
        make_classifier=make_classifier,
    )
    train = np.arange(len(examples), dtype=np.int64)
    baselines = baseline_indexes(examples)
    bundle = fit_bundle(examples, baselines, train, "model-a", {}, base)
    pair_query, _, weights, counts = pair_indexes(examples, baselines, train, "model-a")
    assert counts == [2, 2, 1, 1, 1]
    for query_index in train:
        assert np.isclose(np.sum(weights[pair_query == query_index]), 1.0)
    expected_class_weight = {0: 5.0 / 6.0, 1: 5.0 / 4.0}
    assert bundle["pair_class_weight"] == expected_class_weight
    assert np.isclose(bundle["train_pair_weight_sum"], 5.0)
    for classifier in created[-2:]:
        assert classifier.class_weight == expected_class_weight
        assert classifier.sample_weight is not None
        assert np.allclose(classifier.sample_weight, weights)
    effective = weights * np.asarray(
        [expected_class_weight[examples[int(index)]["target"]] for index in pair_query]
    )
    pair_targets = np.asarray([examples[int(index)]["target"] for index in pair_query])
    assert np.isclose(np.sum(effective[pair_targets == 0]), 2.5)
    assert np.isclose(np.sum(effective[pair_targets == 1]), 2.5)
