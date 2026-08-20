from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

from conftest import (
    make_directory_reparse_point,
    make_run,
    metrics_json,
    prepare_experiment_spec,
)
from crl_v3.experiment import (
    experiment_material_errors,
    schema_7_attempt_integrity_execution_sha256,
    valid_supporting_attempt_ids,
)
from crl_v3.knowledge import KnowledgeStore, Paper, Passage
from crl_v3.workspace import ResearchWorkspace
import tools.run_local_experiment as runner_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNNER = PROJECT_ROOT / "tools" / "run_local_experiment.py"


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path]:
    product, run = make_run(tmp_path)
    implementation = run / "implementation_v001"
    implementation.mkdir()
    (implementation / "method.py").write_bytes(b"def method():\n    return 1\n")
    experiment = run / "experiment_v001"
    experiment.mkdir()
    (experiment / "plan.md").write_bytes(b"# Plan\n\nreal attempt\n")
    return product, run, implementation


def _sibling_run(product: Path, current_run: Path) -> Path:
    sibling = product / "20260731_1201_run02"
    sibling.mkdir()
    for name in ("RUN_CHARTER.md", "RUN_STATUS.md", "RUN_LEDGER.md"):
        content = (current_run / name).read_text(encoding="utf-8")
        (sibling / name).write_text(
            content.replace(current_run.name, sibling.name),
            encoding="utf-8",
            newline="\n",
        )
    return sibling


def test_runner_binds_fixed_read_only_knowledge_for_spec_evidence_ids(
    tmp_path: Path,
) -> None:
    product, run, implementation = _fixture(tmp_path)
    knowledge = product / "knowledge_base"
    knowledge.mkdir()
    database = knowledge / "knowledge.sqlite"
    source = "coverage evidence for a formal experiment"
    source_sha256 = hashlib.sha256(source.encode("utf-8")).hexdigest()
    passage = Passage(
        passage_id="P001:p0001:s0001",
        paper_id="P001",
        section="Abstract",
        page_start=1,
        page_end=1,
        char_start=0,
        char_end=len(source),
        text=source,
        text_sha256=source_sha256,
    )
    store = KnowledgeStore(database, read_only=False)
    store.add_paper(
        Paper(
            paper_id="P001",
            title="Coverage Evidence",
            year=2026,
            source="test",
            venue="Test",
            publication_status="fixture",
            fulltext_path="fulltext/P001.md",
            fulltext_sha256=source_sha256,
        ),
        [passage],
    )
    store.add_evidence(
        evidence_id="ev-runner-fixed-kb",
        paper_id="P001",
        fulltext_sha256=source_sha256,
        evidence_kind="text",
        section="Abstract",
        page_start=1,
        page_end=1,
        locator="fixture",
        source_content=source,
        codex_note="fixture",
        passage_id=passage.passage_id,
        passage_text_sha256=passage.text_sha256,
        quote_start=0,
        quote_end=len(source),
    )
    store.close()

    spec_path = prepare_experiment_spec(
        product, run, experiment_id="experiment-fixed-kb-evidence"
    )
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["independent_ground_truth"]["external_evidence_ids"] = [
        "ev-runner-fixed-kb"
    ]
    spec_path.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    completed = _run(
        product,
        run,
        "fixed-kb-evidence",
        implementation,
        [sys.executable, "-c", "print('formal evidence binding')"],
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8")
    execution = json.loads(
        (
            run
            / "experiment_v001"
            / "attempts"
            / "fixed-kb-evidence"
            / "execution.json"
        ).read_text(encoding="utf-8")
    )
    assert execution["command_exit_code"] == 0
    assert execution["evidence_contract_ok"] is True


def _run(
    product: Path,
    run: Path,
    attempt_id: str,
    cwd: Path,
    command: list[str],
    *,
    inputs: tuple[Path, ...] = (),
    outputs: tuple[Path, ...] = (),
    env: dict[str, str] | None = None,
    timeout_seconds: float | None = None,
    write_metrics: bool = True,
    metrics_payload: str | None = None,
    declared_facts: tuple[str, ...] = (),
    allow_sensitive_env: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[bytes]:
    experiment_id = f"experiment-{attempt_id}"
    spec = prepare_experiment_spec(
        product, run, "v001", experiment_id=experiment_id
    )
    capture = run / "experiment_v001" / "attempts" / attempt_id
    metrics = capture / "metrics-output.json"
    argv = [
        sys.executable,
        str(RUNNER),
        "--product-root",
        str(product),
        "--run-root",
        str(run),
        "--version",
        "v001",
        "--attempt-id",
        attempt_id,
        "--cwd",
        str(cwd),
        "--experiment-spec",
        str(spec),
        "--metrics-output",
        str(metrics),
        "--seed-not-set",
        "--implementation-file",
        str(run / "implementation_v001" / "method.py"),
    ]
    for path in inputs:
        argv.extend(("--input", str(path)))
    for path in outputs:
        argv.extend(("--output", str(path)))
    if timeout_seconds is not None:
        argv.extend(("--timeout-seconds", str(timeout_seconds)))
    for fact in declared_facts:
        argv.extend(("--declared-fact", fact))
    for name in allow_sensitive_env:
        argv.extend(("--allow-sensitive-env", name))
    if not outputs:
        argv.append("--stdout-as-evidence")
    if write_metrics:
        payload = metrics_payload or metrics_json(experiment_id)
        wrapper = (
            "from pathlib import Path; import subprocess,sys; "
            "completed=subprocess.run(sys.argv[3:]); "
            "Path(sys.argv[1]).write_text(sys.argv[2], encoding='utf-8', newline='\\n'); "
            "raise SystemExit(completed.returncode)"
        )
        command = [sys.executable, "-c", wrapper, str(metrics), payload, *command]
    argv.extend(("--", *command))
    return subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)


def test_runner_captures_real_command_output_exit_code_and_files(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    script = cwd / "experiment.py"
    capture = run / "experiment_v001" / "attempts" / "attempt-001"
    output = capture / "result.txt"
    script.write_text(
        "from pathlib import Path\n"
        "import sys\n"
        "Path(sys.argv[1]).write_text('value=7', encoding='utf-8')\n"
        "print('stdout-value')\n"
        "print('stderr-value', file=sys.stderr)\n",
        encoding="utf-8",
    )
    completed = _run(
        product,
        run,
        "attempt-001",
        cwd,
        [sys.executable, str(script), str(output)],
        inputs=(script,),
        outputs=(output,),
        declared_facts=("model=test-model", "dataset=test-dataset"),
    )
    assert completed.returncode == 0
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    assert record["schema_version"] == 8
    assert record["command_exit_code"] == 0
    assert record["output_contract_ok"] is True
    assert record["cwd"] == str(cwd.resolve())
    assert "platform" in record["environment_facts"]
    assert record["environment_facts"]["cpu_count"]
    assert record["environment_facts"]["git"]["status"] in {
        "available",
        "unavailable",
    }
    assert record["environment_facts"]["nvidia"]["status"] in {
        "available",
        "unavailable",
    }
    assert record["environment_facts"]["declared_facts"] == {
        "dataset": "test-dataset",
        "model": "test-model",
    }
    runner = record["environment_facts"]["runner"]
    subject = record["environment_facts"]["subject"]
    assert runner["python"] == sys.version
    assert Path(runner["executable"]["path"]).resolve() == Path(sys.executable).resolve()
    assert runner["executable"]["sha256"] == hashlib.sha256(
        Path(sys.executable).read_bytes()
    ).hexdigest()
    assert runner["dependencies"]["scope"] == "formal_runner_machine_environment"
    assert runner["dependencies"]["subject_relationship"] == "unbound"
    assert subject["argv0"] == record["argv"][0]
    assert subject["runner_relationship"] == "same_executable"
    assert subject["runtime"] == {
        "status": "bound_to_runner_python",
        "python": sys.version,
    }
    assert subject["dependencies"]["status"] == "unbound"
    assert (capture / "dependencies.txt").is_file()
    assert record["metrics_contract_ok"] is True
    assert (capture / "spec.json").read_bytes() == (
        run / "experiment_v001/specs/experiment-attempt-001.json"
    ).read_bytes()
    assert (capture / "metrics.json").is_file()
    assert (capture / "stdout.bin").read_bytes() in {b"stdout-value\r\n", b"stdout-value\n"}
    assert b"stderr-value" in (capture / "stderr.bin").read_bytes()
    assert record["inputs"] == [
        {
            "path": str(script.resolve()),
            "size_bytes": script.stat().st_size,
            "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        }
    ]


@pytest.mark.windows
def test_subject_runtime_provenance_distinguishes_non_runner_executable(
    tmp_path: Path,
) -> None:
    product, run, cwd = _fixture(tmp_path)
    powershell = shutil.which("powershell.exe")
    if powershell is None:
        pytest.skip("PowerShell executable is unavailable")
    attempt_id = "attempt-powershell-subject"
    experiment_id = f"experiment-{attempt_id}"
    capture = run / "experiment_v001/attempts" / attempt_id
    metrics = capture / "metrics-output.json"
    script = cwd / "subject.ps1"
    script.write_text(
        "param([string]$Metrics, [string]$Payload)\n"
        "$utf8 = New-Object System.Text.UTF8Encoding($false)\n"
        "[System.IO.File]::WriteAllText($Metrics, $Payload, $utf8)\n"
        "Write-Output 'different-runtime-evidence'\n",
        encoding="utf-8",
        newline="\n",
    )

    completed = _run(
        product,
        run,
        attempt_id,
        cwd,
        [
            str(Path(powershell).resolve()),
            "-NoProfile",
            "-NonInteractive",
            "-File",
            str(script),
            "-Metrics",
            str(metrics),
            "-Payload",
            metrics_json(experiment_id),
        ],
        inputs=(script,),
        write_metrics=False,
    )

    assert completed.returncode == 0
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    runner = record["environment_facts"]["runner"]
    subject = record["environment_facts"]["subject"]
    assert Path(runner["executable"]["path"]).resolve() == Path(sys.executable).resolve()
    assert Path(subject["executable"]["path"]).resolve() == Path(powershell).resolve()
    assert subject["executable"]["status"] == "bound"
    assert subject["runner_relationship"] == "different_executable"
    assert subject["runtime"]["status"] == "unbound"
    assert subject["dependencies"]["status"] == "unbound"
    assert runner["dependencies"]["subject_relationship"] == "unbound"


def test_sibling_run_input_is_rejected_before_child_start(
    tmp_path: Path,
) -> None:
    product, run, cwd = _fixture(tmp_path)
    sibling = _sibling_run(product, run)
    sentinel = sibling / "sentinel.txt"
    sentinel.write_text("sibling evidence\n", encoding="utf-8", newline="\n")
    marker = cwd / "child-started.txt"

    completed = _run(
        product,
        run,
        "attempt-sibling-input",
        cwd,
        [
            sys.executable,
            "-c",
            "from pathlib import Path; import sys; Path(sys.argv[1]).write_text('started'); print('evidence')",
            str(marker),
        ],
        inputs=(sentinel,),
    )

    assert completed.returncode == 2
    assert b"formal input belongs to another CRL Run" in completed.stderr
    assert sibling.name.encode("utf-8") in completed.stderr
    assert not marker.exists()
    assert not (run / "experiment_v001/attempts/attempt-sibling-input").exists()
    workspace = ResearchWorkspace(run, product_root=product)
    assert valid_supporting_attempt_ids(workspace) == ()


def test_sibling_run_input_cannot_hide_behind_directory_reparse(
    tmp_path: Path,
) -> None:
    product, run, cwd = _fixture(tmp_path)
    sibling = _sibling_run(product, run)
    sentinel = sibling / "sentinel.txt"
    sentinel.write_text("sibling evidence\n", encoding="utf-8", newline="\n")
    alias = tmp_path / "external-looking-run"
    make_directory_reparse_point(alias, sibling)

    completed = _run(
        product,
        run,
        "attempt-sibling-symlink",
        cwd,
        [sys.executable, "-c", "print('must not run')"],
        inputs=(alias / "sentinel.txt",),
    )

    assert completed.returncode == 2
    assert b"formal input belongs to another CRL Run" in completed.stderr
    assert not (run / "experiment_v001/attempts/attempt-sibling-symlink").exists()


def test_external_formal_input_keeps_provenance_and_supporting_validity(
    tmp_path: Path,
) -> None:
    product, run, cwd = _fixture(tmp_path)
    external = tmp_path / "external-dataset.bin"
    external.write_bytes(b"external research dataset\x00v1")

    completed = _run(
        product,
        run,
        "attempt-external-input",
        cwd,
        [sys.executable, "-c", "print('external evidence')"],
        inputs=(external,),
    )

    assert completed.returncode == 0
    capture = run / "experiment_v001/attempts/attempt-external-input"
    execution_path = capture / "execution.json"
    record = json.loads(execution_path.read_text(encoding="utf-8"))
    assert record["inputs"] == [
        {
            "path": str(external.resolve()),
            "size_bytes": external.stat().st_size,
            "sha256": hashlib.sha256(external.read_bytes()).hexdigest(),
        }
    ]
    workspace = ResearchWorkspace(run, product_root=product)
    assert valid_supporting_attempt_ids(workspace) == ("attempt-external-input",)

    sibling = _sibling_run(product, run)
    sentinel = sibling / "sentinel.bin"
    sentinel.write_bytes(b"sibling evidence")
    record["inputs"] = [
        {
            "path": str(sentinel.resolve()),
            "size_bytes": sentinel.stat().st_size,
            "sha256": hashlib.sha256(sentinel.read_bytes()).hexdigest(),
        }
    ]
    execution_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    assert valid_supporting_attempt_ids(workspace) == ()
    errors = experiment_material_errors(workspace, ("attempt-external-input",))
    assert any("formal input belongs to another CRL Run" in error for error in errors)


def test_formal_child_withholds_ambient_secret_but_keeps_normal_environment(
    tmp_path: Path,
) -> None:
    product, run, cwd = _fixture(tmp_path)
    env = os.environ.copy()
    env["CRL_TEST_API_KEY"] = "formal-ambient-secret-123456789"
    env["CRL_TEST_NORMAL_ENV"] = "ordinary-environment-value"
    script = (
        "import json,os,sys; "
        "print(json.dumps({'secret_visible': 'CRL_TEST_API_KEY' in os.environ, "
        "'normal': os.environ['CRL_TEST_NORMAL_ENV'], "
        "'python_exists': os.path.isfile(sys.executable)}))"
    )

    completed = _run(
        product,
        run,
        "attempt-sanitized-env",
        cwd,
        [sys.executable, "-c", script],
        env=env,
    )

    assert completed.returncode == 0
    capture = run / "experiment_v001/attempts/attempt-sanitized-env"
    payload = json.loads((capture / "stdout.bin").read_text(encoding="utf-8"))
    assert payload == {
        "secret_visible": False,
        "normal": "ordinary-environment-value",
        "python_exists": True,
    }
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    assert record["environment_facts"]["sensitive_environment_passthrough"] == []


def test_formal_explicit_secret_is_scoped_to_research_child(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run, cwd = _fixture(tmp_path)
    attempt_id = "attempt-scoped-passthrough"
    capture = run / "experiment_v001/attempts" / attempt_id
    output = capture / "visibility.txt"
    metrics = capture / "metrics-output.json"
    secret_name = "CRL_SCOPED_API_KEY"
    monkeypatch.setenv(secret_name, "formal-scoped-secret-123456789")
    monkeypatch.setenv("CRL_TEST_NORMAL_ENV", "ordinary-environment-value")
    auxiliary_environments: list[dict[str, str]] = []

    def git_facts(
        _root: Path, *, environment: dict[str, str] | None = None
    ) -> dict[str, object]:
        assert environment is not None
        auxiliary_environments.append(environment)
        return {"status": "unavailable", "reason": "test probe"}

    def nvidia_facts(
        *, environment: dict[str, str] | None = None
    ) -> dict[str, object]:
        assert environment is not None
        auxiliary_environments.append(environment)
        return {"status": "unavailable", "reason": "test probe"}

    monkeypatch.setattr(runner_module, "_git_facts", git_facts)
    monkeypatch.setattr(runner_module, "_nvidia_facts", nvidia_facts)
    spec = prepare_experiment_spec(
        product, run, "v001", experiment_id=f"experiment-{attempt_id}"
    )
    script = (
        "from pathlib import Path; import os,sys; "
        "Path(sys.argv[1]).write_text(str(sys.argv[4] in os.environ), encoding='utf-8'); "
        "Path(sys.argv[2]).write_text(sys.argv[3], encoding='utf-8', newline='\\n')"
    )

    code = runner_module.main(
        [
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--version",
            "v001",
            "--attempt-id",
            attempt_id,
            "--cwd",
            str(cwd),
            "--experiment-spec",
            str(spec),
            "--metrics-output",
            str(metrics),
            "--seed-not-set",
            "--implementation-file",
            str(run / "implementation_v001" / "method.py"),
            "--output",
            str(output),
            "--allow-sensitive-env",
            secret_name,
            "--",
            sys.executable,
            "-c",
            script,
            str(output),
            str(metrics),
            metrics_json(f"experiment-{attempt_id}"),
            secret_name,
        ]
    )

    assert code == 0
    assert output.read_text(encoding="utf-8") == "True"
    assert len(auxiliary_environments) == 2
    for environment in auxiliary_environments:
        assert secret_name not in environment
        assert environment["CRL_TEST_NORMAL_ENV"] == "ordinary-environment-value"


def test_failed_child_still_records_schema_8_facts(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    completed = _run(
        product,
        run,
        "attempt-failed",
        cwd,
        [sys.executable, "-c", "import sys; print('failed'); sys.exit(7)"],
    )
    assert completed.returncode == 7
    capture = run / "experiment_v001/attempts/attempt-failed"
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    assert record["schema_version"] == 8
    assert record["command_exit_code"] == 7
    assert record["metrics_contract_ok"] is True
    assert (capture / "spec.json").is_file()
    assert (capture / "metrics.json").is_file()
    workspace = ResearchWorkspace(run, product_root=product, version="v001")
    assert schema_7_attempt_integrity_execution_sha256(workspace, "attempt-failed")
    assert experiment_material_errors(workspace, ("attempt-failed",))


def test_missing_metrics_is_a_mechanical_failure(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    completed = _run(
        product,
        run,
        "attempt-missing-metrics",
        cwd,
        [sys.executable, "-c", "print('evidence')"],
        write_metrics=False,
    )
    assert completed.returncode == 2
    record = json.loads(
        (run / "experiment_v001/attempts/attempt-missing-metrics/execution.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["metrics_contract_ok"] is False
    assert "missing" in record["metrics"]["validation_errors"][0]
    workspace = ResearchWorkspace(run, product_root=product, version="v001")
    assert schema_7_attempt_integrity_execution_sha256(
        workspace, "attempt-missing-metrics"
    )
    assert experiment_material_errors(workspace, ("attempt-missing-metrics",))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_metrics_are_rejected(tmp_path: Path, value: float) -> None:
    product, run, cwd = _fixture(tmp_path)
    experiment_id = "experiment-attempt-non-finite"
    payload = json.loads(metrics_json(experiment_id))
    payload["records"][0]["value"] = value
    completed = _run(
        product,
        run,
        "attempt-non-finite",
        cwd,
        [sys.executable, "-c", "print('evidence')"],
        metrics_payload=json.dumps(payload) + "\n",
    )
    assert completed.returncode == 2
    record = json.loads(
        (run / "experiment_v001/attempts/attempt-non-finite/execution.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["metrics_contract_ok"] is False
    assert any(
        "non-finite" in item for item in record["metrics"]["validation_errors"]
    )


def test_wrong_metrics_experiment_id_is_rejected(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    completed = _run(
        product,
        run,
        "attempt-wrong-id",
        cwd,
        [sys.executable, "-c", "print('evidence')"],
        metrics_payload=metrics_json("another-experiment"),
    )
    assert completed.returncode == 2
    record = json.loads(
        (run / "experiment_v001/attempts/attempt-wrong-id/execution.json").read_text(
            encoding="utf-8"
        )
    )
    assert any(
        "experiment_id" in item for item in record["metrics"]["validation_errors"]
    )


def test_missing_spec_primary_metric_is_rejected_without_judging_value(
    tmp_path: Path,
) -> None:
    product, run, cwd = _fixture(tmp_path)
    experiment_id = "experiment-attempt-missing-primary"
    payload = json.loads(metrics_json(experiment_id))
    payload["records"][0]["name"] = "different_metric"
    payload["records"][0]["value"] = -999999.0
    completed = _run(
        product,
        run,
        "attempt-missing-primary",
        cwd,
        [sys.executable, "-c", "print('evidence')"],
        metrics_payload=json.dumps(payload) + "\n",
    )
    assert completed.returncode == 2
    record = json.loads(
        (run / "experiment_v001/attempts/attempt-missing-primary/execution.json").read_text(
            encoding="utf-8"
        )
    )
    assert any(
        "primary_metric" in item
        for item in record["metrics"]["validation_errors"]
    )


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("run_id", "20260731_1201_run02", "run_id"),
        ("version", "v999", "version"),
        ("hypothesis_id", "unknown-hypothesis", "hypothesis"),
        ("claim_ids", ["unknown-claim"], "claim"),
    ],
)
def test_spec_identity_is_validated_before_child_start(
    tmp_path: Path, field: str, value: object, expected: str
) -> None:
    product, run, cwd = _fixture(tmp_path)
    attempt_id = "attempt-invalid-spec"
    spec = prepare_experiment_spec(
        product,
        run,
        "v001",
        experiment_id=f"experiment-{attempt_id}",
    )
    payload = json.loads(spec.read_text(encoding="utf-8"))
    payload[field] = value
    spec.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    marker = cwd / "must-not-start.txt"
    completed = _run(
        product,
        run,
        attempt_id,
        cwd,
        [
            sys.executable,
            "-c",
            "from pathlib import Path; import sys; Path(sys.argv[1]).write_text('started')",
            str(marker),
        ],
    )
    assert completed.returncode == 2
    assert expected.encode() in completed.stderr
    assert not marker.exists()
    assert not (run / f"experiment_v001/attempts/{attempt_id}").exists()


def test_secret_bearing_metrics_are_removed_without_leaking(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    attempt_id = "attempt-secret-metrics"
    experiment_id = f"experiment-{attempt_id}"
    capture = run / "experiment_v001/attempts" / attempt_id
    metrics = capture / "metrics-output.json"
    secret = "sk-metrics-secret-value-123456789"
    env = os.environ.copy()
    env["CRL_TEST_API_KEY"] = secret
    script = (
        "from pathlib import Path; import json,os,sys; "
        "payload=json.loads(sys.argv[2]); payload['warnings']=[os.environ['CRL_TEST_API_KEY']]; "
        "Path(sys.argv[1]).write_text(json.dumps(payload), encoding='utf-8'); print('evidence')"
    )
    completed = _run(
        product,
        run,
        attempt_id,
        cwd,
        [sys.executable, "-c", script, str(metrics), metrics_json(experiment_id)],
        env=env,
        write_metrics=False,
        allow_sensitive_env=("CRL_TEST_API_KEY",),
    )
    assert completed.returncode == 2
    assert not metrics.exists()
    assert not (capture / "metrics.json").exists()
    combined = completed.stdout + completed.stderr
    combined += b"".join(path.read_bytes() for path in capture.iterdir() if path.is_file())
    assert secret.encode() not in combined


def test_original_spec_mutation_does_not_change_attempt_snapshot(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    completed = _run(
        product,
        run,
        "attempt-spec-snapshot",
        cwd,
        [sys.executable, "-c", "print('evidence')"],
    )
    assert completed.returncode == 0
    capture = run / "experiment_v001/attempts/attempt-spec-snapshot"
    snapshot = (capture / "spec.json").read_bytes()
    source = run / "experiment_v001/specs/experiment-attempt-spec-snapshot.json"
    source.write_text("{}\n", encoding="utf-8", newline="\n")

    workspace = ResearchWorkspace(run, product_root=product)
    assert (capture / "spec.json").read_bytes() == snapshot
    assert experiment_material_errors(workspace, ("attempt-spec-snapshot",)) == ()


def test_unavailable_git_and_nvidia_are_explicit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def unavailable(*_args: object, **_kwargs: object) -> bytes:
        raise FileNotFoundError("tool unavailable")

    monkeypatch.setattr(runner_module, "_command_stdout", unavailable)
    assert runner_module._git_facts(tmp_path)["status"] == "unavailable"
    assert runner_module._nvidia_facts()["status"] == "unavailable"


def test_declared_fact_containing_secret_is_rejected_before_attempt(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    secret = "sk-declared-fact-secret-123456789"
    env = os.environ.copy()
    env["CRL_TEST_API_KEY"] = secret
    completed = _run(
        product,
        run,
        "attempt-declared-secret",
        cwd,
        [sys.executable, "-c", "print('must not run')"],
        env=env,
        declared_facts=(f"provider={secret}",),
    )
    assert completed.returncode == 2
    assert secret.encode() not in completed.stderr
    assert not (run / "experiment_v001/attempts/attempt-declared-secret").exists()


def test_machine_comparable_budget_overrun_is_warning_not_scientific_failure(
    tmp_path: Path,
) -> None:
    product, run, cwd = _fixture(tmp_path)
    completed = _run(
        product,
        run,
        "attempt-budget-warning",
        cwd,
        [sys.executable, "-c", "print('evidence')"],
        metrics_payload=metrics_json(
            "experiment-attempt-budget-warning", tokens=101
        ),
    )
    assert completed.returncode == 0
    record = json.loads(
        (run / "experiment_v001/attempts/attempt-budget-warning/execution.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["warnings"]
    assert "tokens" in record["warnings"][0]
    assert "supported" not in json.dumps(record).lower()
    assert "falsified" not in json.dumps(record).lower()


def test_explicit_timeout_does_not_change_a_successful_attempt(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    completed = _run(
        product,
        run,
        "attempt-001",
        cwd,
        [sys.executable, "-c", "print('finished')"],
        timeout_seconds=5,
    )

    assert completed.returncode == 0
    record = json.loads(
        (run / "experiment_v001/attempts/attempt-001/execution.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["timed_out"] is False
    assert record["timeout_seconds"] == 5
    assert record["termination_method"] is None
    assert record["process_tree_cleanup_ok"] is None


@pytest.mark.windows
def test_timeout_records_failure_and_ends_spawned_child_process(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    capture = run / "experiment_v001/attempts/attempt-timeout"
    child_pid_path = capture / "child.pid"
    script = cwd / "spawn_child.py"
    script.write_text(
        "from pathlib import Path\n"
        "import subprocess, sys, time\n"
        "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
        "Path(sys.argv[1]).write_text(str(child.pid), encoding='utf-8')\n"
        "print('child-started', flush=True)\n"
        "time.sleep(60)\n",
        encoding="utf-8",
        newline="\n",
    )

    completed = _run(
        product,
        run,
        "attempt-timeout",
        cwd,
        [sys.executable, str(script), str(child_pid_path)],
        inputs=(script,),
        outputs=(child_pid_path,),
        timeout_seconds=0.5,
    )

    assert completed.returncode == 124
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    assert record["timed_out"] is True
    assert record["timeout_seconds"] == 0.5
    assert isinstance(record["termination_method"], str)
    assert record["process_tree_cleanup_ok"] is True
    workspace = ResearchWorkspace(run, product_root=product)
    assert any(
        "timed_out" in error
        for error in experiment_material_errors(workspace, ("attempt-timeout",))
    )

    child_pid = int(child_pid_path.read_text(encoding="utf-8"))
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and _windows_pid_exists(child_pid):
        time.sleep(0.1)
    assert not _windows_pid_exists(child_pid)


@pytest.mark.windows
def test_process_tree_cleanup_failure_is_reported(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _StuckProcess:
        pid = 987654321

        @staticmethod
        def poll() -> None:
            return None

        @staticmethod
        def send_signal(_signal: int) -> None:
            raise OSError("signal unavailable")

        @staticmethod
        def wait(timeout: float) -> None:
            raise subprocess.TimeoutExpired("stuck", timeout)

    monkeypatch.setattr(
        runner_module.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 1),
    )

    method, cleanup_ok = runner_module._terminate_process_tree(_StuckProcess())

    assert method == "windows_taskkill_tree"
    assert cleanup_ok is False


def test_cleanup_failure_still_preserves_timeout_execution_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run, cwd = _fixture(tmp_path)
    capture = run / "experiment_v001/attempts/attempt-timeout-cleanup-failed"
    spec = prepare_experiment_spec(
        product,
        run,
        "v001",
        experiment_id="experiment-attempt-timeout-cleanup-failed",
    )
    secret_name = "CRL_TIMEOUT_API_KEY"
    monkeypatch.setenv(secret_name, "timeout-scoped-secret-123456789")
    termination_environments: list[dict[str, str]] = []

    def failed_cleanup(
        _process: object, *, environment: dict[str, str] | None = None
    ) -> tuple[str, bool]:
        assert environment is not None
        termination_environments.append(environment)
        return "simulated_cleanup_failure", False

    monkeypatch.setattr(
        runner_module,
        "_terminate_process_tree",
        failed_cleanup,
    )

    code = runner_module.main(
        [
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--version",
            "v001",
            "--attempt-id",
            "attempt-timeout-cleanup-failed",
            "--cwd",
            str(cwd),
            "--experiment-spec",
            str(spec),
            "--metrics-output",
            str(capture / "metrics-output.json"),
            "--seed-not-set",
            "--implementation-file",
            str(run / "implementation_v001" / "method.py"),
            "--stdout-as-evidence",
            "--timeout-seconds",
            "0.05",
            "--allow-sensitive-env",
            secret_name,
            "--",
            sys.executable,
            "-c",
            "import time; print('started', flush=True); time.sleep(0.5)",
        ]
    )

    assert code == 124
    assert len(termination_environments) == 1
    assert secret_name not in termination_environments[0]
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    assert record["timed_out"] is True
    assert record["termination_method"] == "simulated_cleanup_failure"
    assert record["process_tree_cleanup_ok"] is False
    assert (capture / "stdout.bin").is_file()
    assert (capture / "stderr.bin").is_file()
    workspace = ResearchWorkspace(run, product_root=product)
    assert experiment_material_errors(
        workspace, ("attempt-timeout-cleanup-failed",)
    )
    time.sleep(0.6)


def test_runner_refuses_to_overwrite_attempt_directory(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    capture = run / "experiment_v001" / "attempts" / "attempt-001"
    capture.mkdir(parents=True)
    completed = _run(
        product, run, "attempt-001", cwd, [sys.executable, "-c", "print('x')"]
    )
    assert completed.returncode == 2
    assert b"already exists" in completed.stderr


def test_nonempty_stdout_can_be_the_only_evidence_channel(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    completed = _run(
        product, run, "attempt-001", cwd, [sys.executable, "-c", "print('evidence')"]
    )
    assert completed.returncode == 0
    record = json.loads(
        (run / "experiment_v001/attempts/attempt-001/execution.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["stdout_as_evidence"] is True
    assert record["evidence_contract_ok"] is True


def test_empty_stdout_without_output_cannot_be_evidence(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    completed = _run(
        product, run, "attempt-001", cwd, [sys.executable, "-c", "pass"]
    )
    assert completed.returncode == 2
    record = json.loads(
        (run / "experiment_v001/attempts/attempt-001/execution.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["evidence_contract_ok"] is False


def test_missing_declared_output_is_mechanical_failure(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    capture = run / "experiment_v001" / "attempts" / "attempt-001"
    output = capture / "missing.txt"
    completed = _run(
        product,
        run,
        "attempt-001",
        cwd,
        [sys.executable, "-c", "print('ran')"],
        outputs=(output,),
    )
    assert completed.returncode == 2
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    assert record["command_exit_code"] == 0
    assert record["output_contract_ok"] is False


def test_environment_secret_is_redacted_from_capture_and_console(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    secret = "sk-test-secret-value-123456789"
    env = os.environ.copy()
    env["CRL_TEST_API_KEY"] = secret
    script = "import os; print(os.environ['CRL_TEST_API_KEY'])"
    capture = run / "experiment_v001" / "attempts" / "attempt-001"
    completed = _run(
        product,
        run,
        "attempt-001",
        cwd,
        [sys.executable, "-c", script],
        env=env,
        allow_sensitive_env=("CRL_TEST_API_KEY",),
    )
    assert completed.returncode == 2
    combined = completed.stdout + completed.stderr
    combined += b"".join(path.read_bytes() for path in capture.iterdir() if path.is_file())
    assert secret.encode("utf-8") not in combined
    assert b"[REDACTED]" in (capture / "stdout.bin").read_bytes()
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    assert record["environment_facts"]["sensitive_environment_passthrough"] == [
        "CRL_TEST_API_KEY"
    ]


def test_secret_in_command_argument_is_rejected_before_execution(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    secret = "secret-value-123456"
    env = os.environ.copy()
    env["CRL_TEST_TOKEN"] = secret
    capture = run / "experiment_v001" / "attempts" / "attempt-001"
    completed = _run(
        product,
        run,
        "attempt-001",
        cwd,
        [sys.executable, "-c", "print('x')", secret],
        env=env,
    )
    assert completed.returncode == 2
    assert not capture.exists()
    assert secret.encode("utf-8") not in completed.stderr


def test_secret_bearing_declared_output_is_removed_but_facts_remain(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    secret = "sk-output-secret-value-123456789"
    env = os.environ.copy()
    env["CRL_TEST_API_KEY"] = secret
    capture = run / "experiment_v001/attempts/attempt-001"
    output = capture / "sensitive.bin"
    script = (
        "from pathlib import Path; import os,sys; "
        "Path(sys.argv[1]).write_bytes(b'prefix-' + os.environ['CRL_TEST_API_KEY'].encode())"
    )
    completed = _run(
        product,
        run,
        "attempt-001",
        cwd,
        [sys.executable, "-c", script, str(output)],
        outputs=(output,),
        env=env,
        allow_sensitive_env=("CRL_TEST_API_KEY",),
    )
    assert completed.returncode == 2
    assert not output.exists()
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    after = record["outputs"][0]["after"]
    assert after["artifact_retained"] is False
    assert after["contains_possible_credential"] is True
    assert after["credential_detection"] == ["environment_secret", "credential_pattern"]
    assert isinstance(after["size_bytes"], int) and after["size_bytes"] > 0
    assert len(after["sha256"]) == 64
    assert secret.encode() not in (capture / "execution.json").read_bytes()


def test_secret_crossing_one_mebibyte_boundary_is_removed_and_redacted(
    tmp_path: Path,
) -> None:
    product, run, cwd = _fixture(tmp_path)
    secret = "sk-boundary-secret-value-123456789"
    env = os.environ.copy()
    env["CRL_TEST_API_KEY"] = secret
    capture = run / "experiment_v001/attempts/attempt-001"
    output = capture / "boundary.bin"
    script = (
        "from pathlib import Path; import os,sys; "
        "prefix=b'x'*(1024*1024-5); key=os.environ['CRL_TEST_API_KEY'].encode(); "
        "Path(sys.argv[1]).write_bytes(prefix+key); sys.stdout.buffer.write(prefix+key)"
    )
    completed = _run(
        product,
        run,
        "attempt-001",
        cwd,
        [sys.executable, "-c", script, str(output)],
        outputs=(output,),
        env=env,
        allow_sensitive_env=("CRL_TEST_API_KEY",),
    )
    assert completed.returncode == 2
    assert not output.exists()
    stdout = (capture / "stdout.bin").read_bytes()
    assert secret.encode() not in stdout
    assert b"[REDACTED]" in stdout


def test_large_capture_and_output_have_streamed_exact_file_facts(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    capture = run / "experiment_v001/attempts/attempt-001"
    output = capture / "large.bin"
    script = (
        "from pathlib import Path; import sys; data=(b'0123456789abcdef'*(700000)); "
        "Path(sys.argv[1]).write_bytes(data); sys.stdout.buffer.write(data)"
    )
    completed = _run(
        product,
        run,
        "attempt-001",
        cwd,
        [sys.executable, "-c", script, str(output)],
        outputs=(output,),
    )
    assert completed.returncode == 0
    record = json.loads((capture / "execution.json").read_text(encoding="utf-8"))
    import hashlib

    expected = hashlib.sha256(output.read_bytes()).hexdigest()
    assert record["outputs"][0]["after"]["sha256"] == expected
    assert record["capture"]["stdout"]["sha256"] == expected
    assert record["capture"]["stdout"]["size_bytes"] == output.stat().st_size


@pytest.mark.windows
def test_attempts_junction_is_rejected_before_external_capture(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    outside = tmp_path / "outside-attempts"
    make_directory_reparse_point(run / "experiment_v001/attempts", outside)
    completed = _run(
        product, run, "attempt-001", cwd, [sys.executable, "-c", "print('x')"]
    )
    assert completed.returncode == 2
    assert b"reparse point" in completed.stderr
    assert list(outside.iterdir()) == []


def test_seed_must_be_explicitly_nonempty_or_marked_not_set(tmp_path: Path) -> None:
    product, run, cwd = _fixture(tmp_path)
    spec = prepare_experiment_spec(
        product, run, "v001", experiment_id="experiment-attempt-001"
    )
    capture = run / "experiment_v001/attempts/attempt-001"
    argv = [
        sys.executable,
        str(RUNNER),
        "--product-root",
        str(product),
        "--run-root",
        str(run),
        "--version",
        "v001",
        "--attempt-id",
        "attempt-001",
        "--cwd",
        str(cwd),
        "--experiment-spec",
        str(spec),
        "--metrics-output",
        str(capture / "metrics-output.json"),
        "--seed",
        "",
        "--implementation-file",
        str(run / "implementation_v001" / "method.py"),
        "--stdout-as-evidence",
        "--",
        sys.executable,
        "-c",
        "print('must not run')",
    ]
    completed = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert completed.returncode == 2
    assert b"non-empty explicit value" in completed.stderr
    assert not capture.exists()


def _windows_pid_exists(pid: int) -> bool:
    completed = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return f'"{pid}"'.encode("ascii") in completed.stdout
