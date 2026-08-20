from __future__ import annotations

import numpy as np
from scipy import sparse

from program import feature_matrices, prepare_examples


def test_role_factorization_and_capacity_controls() -> None:
    mixed = sparse.csr_matrix([[0.1, 0.2, 0.3]])
    commands = sparse.csr_matrix([[0.4, 0.5, 0.6]])
    outputs = sparse.csr_matrix([[0.7, 0.8, 0.9]])
    matrices = feature_matrices(mixed, commands, outputs)
    assert matrices["mixed"].shape[1] == 3
    assert matrices["role_concat"].shape[1] == 6
    for name in (
        "triple_mixed",
        "command_duplicated",
        "output_duplicated",
        "role_factorized",
    ):
        assert matrices[name].shape[1] == 9
    assert np.allclose(
        matrices["role_factorized"].toarray(),
        np.hstack([mixed.toarray(), commands.toarray(), outputs.toarray()]),
    )
    assert np.allclose(
        matrices["command_duplicated"].toarray(),
        np.hstack([mixed.toarray(), commands.toarray(), commands.toarray()]),
    )


def test_prepare_examples_keeps_all_rows_and_separates_roles() -> None:
    row = {
        "row_id": "row-a",
        "task_id": "task-a",
        "target": 1,
        "commands": ["echo done"],
        "terminal_outputs": ["done"],
        "source_relative_path": "tasks/task-a/trajectory.json",
        "source_sha256": "a" * 64,
    }

    class Base:
        @staticmethod
        def action_text(value):
            return "COMMANDS\necho done\nOUTPUTS\ndone"

    examples, sources = prepare_examples([row], Base())
    assert len(examples) == len(sources) == 1
    assert examples[0]["mixed_text"] == "COMMANDS\necho done\nOUTPUTS\ndone"
    assert examples[0]["command_text"] == "COMMANDS\necho done"
    assert examples[0]["output_text"] == "OUTPUTS\ndone"
