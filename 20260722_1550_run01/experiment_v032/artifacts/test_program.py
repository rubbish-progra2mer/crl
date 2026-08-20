from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


MODULE_PATH = Path(__file__).with_name("program.py")
SPEC = importlib.util.spec_from_file_location("v032_program_test", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
PROGRAM = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROGRAM)


def test_task_description_extracts_only_bounded_text() -> None:
    prompt = "prefix\nTask Description:\nDo the work.\nCurrent terminal state:\nroot"
    assert PROGRAM.task_description(prompt) == "Do the work."


def test_fold_is_deterministic_and_bounded() -> None:
    first = PROGRAM.fold_for_task("task-7", 3)
    assert first == PROGRAM.fold_for_task("task-7", 3)
    assert first in {0, 1, 2}


def test_equal_task_weights_total_one_per_task() -> None:
    examples = [
        {"task_id": "a"},
        {"task_id": "a"},
        {"task_id": "b"},
    ]
    weights = PROGRAM.equal_task_weights(examples, np.asarray([0, 1, 2]))
    assert np.allclose(weights, [0.5, 0.5, 1.0])


def test_dense_features_have_fixed_dimensions() -> None:
    class Identity:
        def predict(self, value: np.ndarray) -> np.ndarray:
            return value

    task = np.asarray([[0.0, 1.0], [1.0, 0.0]])
    action = np.asarray([[1.0, 1.0], [0.0, 0.0]])
    result = PROGRAM.dense_features(task, action, Identity(), Identity())
    assert result["latent_additive"].shape == (2, 4)
    assert result["identity_innovation"].shape == (2, 2)
    assert np.array_equal(result["all_row_innovation"], np.abs(action - task))
    assert np.array_equal(result["successful_innovation"], np.abs(action - task))


def test_methods_fix_successful_candidate_last() -> None:
    assert PROGRAM.METHODS[-1] == "successful_innovation"
    assert "successful_innovation" not in PROGRAM.COMPARATORS
