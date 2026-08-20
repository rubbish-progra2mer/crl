from __future__ import annotations

import json
from pathlib import Path

import pytest

from crl_v3.experiment import (
    experiment_material_errors,
    list_experiment_files,
    read_experiment_plan,
    read_experiment_result,
    schema_7_attempt_integrity_execution_sha256,
)
from crl_v3.workspace import ResearchWorkspace
from conftest import (
    make_directory_reparse_point,
    make_file_symlink,
    make_run,
    record_successful_attempt,
    set_current_version,
)


def test_experiment_files_are_real_versioned_materials(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    set_current_version(run, "v003")
    workspace = ResearchWorkspace(run, version="v003", product_root=product)
    plan = workspace.write_experiment_plan("# Plan\n\n比较候选与基线。")
    assert not (run / "experiment_v003" / "attempts").exists()
    source = tmp_path / "method.py"
    source.write_text("print('ok')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(
        product,
        run,
        "v003",
        run / "implementation_v003" / "method.py",
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    result = workspace.write_experiment_result("# Result\n\n候选优于基线。")

    assert Path(plan.path) == run / "experiment_v003" / "plan.md"
    assert artifact.relative_path == "implementation_v003/method.py"
    assert read_experiment_plan(workspace).content == plan.content
    assert read_experiment_result(workspace).content == result.content
    assert experiment_material_errors(workspace) == ()
    assert {item.area for item in list_experiment_files(workspace)} == {
        "implementation",
        "experiment",
    }


def test_artifacts_and_attempts_cannot_be_overwritten(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "raw.txt"
    source.write_text("first", encoding="utf-8")
    workspace.save_experiment_artifact(
        source, "attempts/attempt-001/raw.txt", area="experiment"
    )
    source.write_text("second", encoding="utf-8")
    with pytest.raises(FileExistsError):
        workspace.save_experiment_artifact(
            source, "attempts/attempt-001/raw.txt", area="experiment"
        )
    assert (run / "experiment_v001/attempts/attempt-001/raw.txt").read_text(
        encoding="utf-8"
    ) == "first"


def test_delivery_material_check_only_reports_objective_absence(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    errors = experiment_material_errors(workspace)
    assert any("attempt" in item for item in errors)
    assert not any("experiment plan" in item for item in errors)
    assert not any("experiment result" in item for item in errors)


def test_workbench_remains_editable_after_review_lock(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_problem("problem")
    workspace.write_seed("seed")
    workspace.write_review_request("review", ["seed_v001.md", "problem_v001.md"])
    source = tmp_path / "scratch.txt"
    source.write_text("scratch", encoding="utf-8")
    workspace.save_experiment_artifact(source, "scratch.txt", area="workbench")
    assert (run / "workbench_v001/scratch.txt").is_file()


def test_junk_attempt_is_not_supporting_experimental_evidence(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_experiment_plan("plan")
    source = tmp_path / "method.py"
    source.write_text("print('x')\n", encoding="utf-8")
    workspace.save_experiment_artifact(source, "method.py", area="implementation")
    junk = tmp_path / "junk.bin"
    junk.write_bytes(b"not an execution record")
    workspace.save_experiment_artifact(
        junk, "attempts/attempt-001/junk.bin", area="experiment"
    )
    workspace.write_experiment_result("result")
    assert any(
        "no valid successful supporting experiment attempt" in error
        for error in experiment_material_errors(workspace)
    )


def test_one_valid_attempt_survives_extra_failed_attempt(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_experiment_plan("plan")
    source = tmp_path / "method.py"
    source.write_text("print('x')\n", encoding="utf-8")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(
        product, run, "v001", Path(artifact.path), attempt_id="attempt-success"
    )
    assert completed.returncode == 0
    failed = run / "experiment_v001/attempts/attempt-failed"
    failed.mkdir(parents=True)
    (failed / "execution.json").write_text("{}\n", encoding="utf-8", newline="\n")
    workspace.write_experiment_result("result")
    assert experiment_material_errors(workspace) == ()


def test_schema_7_integrity_accepts_failed_outcome_without_weakening_support(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    source = run / "workbench_v001" / "source.py"
    source.parent.mkdir()
    source.write_bytes(b"print('real')\n")
    completed = record_successful_attempt(
        product, run, "v001", source, attempt_id="attempt-failed-integrity"
    )
    assert completed.returncode == 0
    workspace = ResearchWorkspace(run, product_root=product, version="v001")
    execution_path = (
        run / "experiment_v001/attempts/attempt-failed-integrity/execution.json"
    )
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    execution["command_exit_code"] = 1
    execution["runner_exit_code"] = 1
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    assert schema_7_attempt_integrity_execution_sha256(
        workspace, "attempt-failed-integrity"
    )
    assert experiment_material_errors(workspace, ("attempt-failed-integrity",))


def test_plan_result_and_readme_are_not_attempt_requirements(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "method.py"
    source.write_text("print('method')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    assert not (run / "experiment_v001/plan.md").exists()
    assert not (run / "experiment_v001/result.md").exists()
    assert not (run / "implementation_v001/README.md").exists()
    assert experiment_material_errors(workspace, ("attempt-001",)) == ()


def test_schema_5_attempt_remains_valid_without_timeout_fields(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "method.py"
    source.write_text("print('method')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    execution_path = run / "experiment_v001/attempts/attempt-001/execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    execution["schema_version"] = 5
    for name in (
        "timed_out",
        "timeout_seconds",
        "termination_method",
        "process_tree_cleanup_ok",
    ):
        execution.pop(name)
    for name in (
        "metrics_contract_ok",
        "experiment_spec",
        "metrics",
        "budget_facts",
        "warnings",
    ):
        execution.pop(name)
    environment = execution["environment_facts"]
    runner = environment["runner"]
    execution["environment_facts"] = {
        "platform": environment["platform"],
        "python": runner["python"],
        "executable": runner["executable"]["path"],
    }
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    assert experiment_material_errors(workspace, ("attempt-001",)) == ()


def test_schema_6_attempt_remains_valid_without_schema_7_fields(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "method.py"
    source.write_text("print('method')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    execution_path = run / "experiment_v001/attempts/attempt-001/execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    execution["schema_version"] = 6
    for name in (
        "metrics_contract_ok",
        "experiment_spec",
        "metrics",
        "budget_facts",
        "warnings",
    ):
        execution.pop(name)
    environment = execution["environment_facts"]
    runner = environment["runner"]
    execution["environment_facts"] = {
        "platform": environment["platform"],
        "python": runner["python"],
        "executable": runner["executable"]["path"],
    }
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    assert experiment_material_errors(workspace, ("attempt-001",)) == ()


def test_schema_7_attempt_remains_valid_with_legacy_runner_environment(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "method.py"
    source.write_text("print('method')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    execution_path = run / "experiment_v001/attempts/attempt-001/execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    environment = execution["environment_facts"]
    runner = environment["runner"]
    execution["schema_version"] = 7
    execution["environment_facts"] = {
        "platform": environment["platform"],
        "python": runner["python"],
        "executable": runner["executable"]["path"],
        "cpu_count": environment["cpu_count"],
        "git": environment["git"],
        "dependencies": runner["dependencies"],
        "nvidia": environment["nvidia"],
        "runner_and_modules": runner["runner_and_modules"],
        "declared_facts": environment["declared_facts"],
    }
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    assert experiment_material_errors(workspace, ("attempt-001",)) == ()
    assert schema_7_attempt_integrity_execution_sha256(workspace, "attempt-001")


@pytest.mark.parametrize("mutation", ["missing_subject", "subject_sha256"])
def test_schema_8_subject_provenance_mutation_invalidates_attempt(
    tmp_path: Path, mutation: str
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "method.py"
    source.write_text("print('method')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    execution_path = run / "experiment_v001/attempts/attempt-001/execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    if mutation == "missing_subject":
        execution["environment_facts"].pop("subject")
    else:
        execution["environment_facts"]["subject"]["executable"]["sha256"] = "0" * 64
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    errors = experiment_material_errors(workspace, ("attempt-001",))
    assert any("subject" in error for error in errors)
    with pytest.raises(ValueError, match="subject"):
        schema_7_attempt_integrity_execution_sha256(workspace, "attempt-001")


@pytest.mark.parametrize("snapshot_name", ["spec.json", "metrics.json"])
def test_schema_7_snapshot_mutation_invalidates_attempt(
    tmp_path: Path, snapshot_name: str
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "method.py"
    source.write_text("print('method')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    snapshot = run / "experiment_v001/attempts/attempt-001" / snapshot_name
    snapshot.write_bytes(snapshot.read_bytes() + b" \n")
    errors = experiment_material_errors(workspace, ("attempt-001",))
    assert any(snapshot_name.split(".")[0] in item and "SHA-256" in item for item in errors)


def test_implementation_or_output_mutation_invalidates_attempt(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "method.py"
    source.write_text("print('method')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    Path(artifact.path).write_text("print('changed')\n", encoding="utf-8", newline="\n")
    errors = experiment_material_errors(workspace, ("attempt-001",))
    assert any("implementation file 0 SHA-256" in item for item in errors)

    Path(artifact.path).write_text("print('method')\n", encoding="utf-8", newline="\n")
    output = run / "experiment_v001/attempts/attempt-001/result.txt"
    output.write_text("changed\n", encoding="utf-8", newline="\n")
    errors = experiment_material_errors(workspace, ("attempt-001",))
    assert any("output 0" in item and "match" in item for item in errors)


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("version", "v999", "version"),
        ("attempt_id", "forged", "attempt_id"),
    ],
)
def test_forged_execution_identity_is_rejected(
    tmp_path: Path, field: str, value: str, expected: str
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_experiment_plan("plan")
    source = tmp_path / "method.py"
    source.write_text("print('x')\n", encoding="utf-8")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    execution_path = run / "experiment_v001/attempts/attempt-001/execution.json"
    import json

    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    execution[field] = value
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    workspace.write_experiment_result("result")
    assert any(expected in error for error in experiment_material_errors(workspace))


def test_forged_capture_path_or_output_retention_is_rejected(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_experiment_plan("plan")
    source = tmp_path / "method.py"
    source.write_text("print('x')\n", encoding="utf-8")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    execution_path = run / "experiment_v001/attempts/attempt-001/execution.json"
    import json

    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    del execution["capture"]["stdout"]["path"]
    execution["outputs"][0]["after"]["artifact_retained"] = False
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    workspace.write_experiment_result("result")
    errors = experiment_material_errors(workspace)
    assert any("stdout recorded path is missing" in error for error in errors)
    assert any("not marked as retained" in error for error in errors)


def test_attempt_execution_symlink_is_not_accepted_as_evidence(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    source = tmp_path / "method.py"
    source.write_text("print('x')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(product, run, "v001", Path(artifact.path))
    assert completed.returncode == 0
    execution = run / "experiment_v001/attempts/attempt-001/execution.json"
    outside = tmp_path / "outside-execution.json"
    outside.write_bytes(execution.read_bytes())
    execution.unlink()
    make_file_symlink(execution, outside)
    errors = experiment_material_errors(workspace, ("attempt-001",))
    assert any("reparse point" in error for error in errors)


@pytest.mark.windows
def test_experiment_junction_is_rejected_before_external_write(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    outside = tmp_path / "outside"
    make_directory_reparse_point(run / "experiment_v001", outside)
    workspace = ResearchWorkspace(run, product_root=product)
    with pytest.raises(ValueError, match="reparse point"):
        workspace.write_experiment_plan("must not escape")
    assert list(outside.iterdir()) == []


@pytest.mark.windows
def test_attempts_junction_is_rejected_before_evidence_read(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    (run / "experiment_v001").mkdir()
    outside = tmp_path / "outside-attempts"
    make_directory_reparse_point(run / "experiment_v001/attempts", outside)
    errors = experiment_material_errors(workspace, ("attempt-001",))
    assert any("reparse point" in error for error in errors)
