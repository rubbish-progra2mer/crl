from program import dense_features, fold_for_task, role_for, task_description


def test_task_description_exact_markers():
    prompt = "prefix\nTask Description:\nDo the real task.\n\nCurrent terminal state:\nstate"
    assert task_description(prompt) == "Do the real task."


def test_role_mapping():
    assert role_for("write") == "mutation"
    assert role_for("permission") == "mutation"
    assert role_for("verify") == "verify"
    assert role_for("read") == "read"
    assert role_for("other") == "other"


def test_dense_role_and_chronological_capacity():
    records = [
        {"role": "read"},
        {"role": "mutation"},
        {"role": "verify"},
        {"role": "other"},
    ]
    values = dense_features(records, [1.0, -2.0, 3.0, 4.0])
    assert len(values["structural_counts"]) == 4
    assert len(values["global_relevance"]) == 5
    assert len(values["chronological_relevance"]) == 20
    assert len(values["role_gated_relevance"]) == 20
    assert values["role_gated_relevance"][1] == -2.0
    assert values["role_gated_relevance"][5] == 0.25
    assert values["role_gated_relevance"][6] == 3.0


def test_empty_role_is_zero_filled():
    records = [{"role": "read"}, {"role": "read"}]
    values = dense_features(records, [1.0, 2.0])
    assert values["role_gated_relevance"][:10] == [0.0] * 10


def test_fold_is_deterministic():
    assert fold_for_task("task-1", 3) == fold_for_task("task-1", 3)
    assert 0 <= fold_for_task("task-1", 3) < 3
