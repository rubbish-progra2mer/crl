from __future__ import annotations

import numpy as np
from scipy import sparse

from program import feature_matrices, fold_for_task, partition_commands


def test_fixed_anchor_partition() -> None:
    commands = [
        "pwd",
        "cat /usr/local/bin/check.sh",
        "printf hacked > /app/result.txt",
    ]
    parts = partition_commands(commands)
    assert parts["anchor_present"] is True
    assert parts["anchor_index"] == 1
    assert parts["before"] == ["pwd"]
    assert parts["from_anchor"] == commands[1:]
    assert parts["anchor_matching"] == ["cat /usr/local/bin/check.sh"]
    assert parts["anchor_nonmatching"] == [commands[0], commands[2]]
    assert parts["first_half"] == commands[:2]
    assert parts["second_half"] == commands[2:]


def test_no_anchor_and_noninspection_checker_execution() -> None:
    commands = ["pwd", "python solution.py", "./run_tests.sh", "ls latest"]
    parts = partition_commands(commands)
    assert parts["anchor_present"] is False
    assert parts["anchor_index"] is None
    assert parts["before"] == commands
    assert parts["from_anchor"] == []


def test_feature_dimensions_and_viaf_content() -> None:
    blocks = [sparse.csr_matrix([[float(i), float(i + 1)]]) for i in range(1, 10)]
    matrices = feature_matrices(*blocks)
    assert matrices["mixed"].shape[1] == 2
    assert matrices["role_concat"].shape[1] == 4
    for name in ("command_duplicated", "fixed_halves", "anchor_bag", "viaf"):
        assert matrices[name].shape[1] == 6
    assert np.allclose(
        matrices["viaf"].toarray(),
        np.hstack([blocks[0].toarray(), blocks[7].toarray(), blocks[8].toarray()]),
    )


def test_task_fold_is_deterministic_and_task_disjoint() -> None:
    values = {task: fold_for_task(task, 5) for task in ("task-a", "task-b", "task-c")}
    assert values == {task: fold_for_task(task, 5) for task in values}
    assert all(0 <= fold < 5 for fold in values.values())
