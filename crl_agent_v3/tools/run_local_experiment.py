from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.decision import (
    SecretScan,
    child_process_environment,
    contains_secret,
    environment_secrets,
    redact_file,
    redact_secrets,
    scan_secret_bytes,
)
from crl_v3.experiment import file_fact, validate_metrics_json_bytes
from crl_v3.falsification import (
    experiment_spec_from_mapping,
    list_plans,
    validate_experiment_spec,
)
from crl_v3.knowledge import KnowledgeStore
from crl_v3.workspace import ResearchWorkspace


SCHEMA_VERSION = 8
TIMEOUT_EXIT_CODE = 124
_TERMINATION_GRACE_SECONDS = 5.0
_ATTEMPT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
_DECLARED_FACT_KEY = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_DECLARED_FACT_KEYS = {
    "dataset",
    "dataset_revision",
    "model",
    "model_revision",
    "prompt_revision",
    "provider",
    "tokenizer_revision",
}
_HARD_BUDGET_KEYS = {
    "duration_seconds",
    "tokens",
    "api_calls",
    "gpu_time_seconds",
}


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _positive_seconds(value: str) -> float:
    try:
        seconds = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("timeout must be a positive number") from error
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("timeout must be a positive number")
    return seconds


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one foreground experiment inside a bound CRL Run attempt."
    )
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--cwd", required=True, type=Path)
    parser.add_argument("--experiment-spec", required=True, type=Path)
    parser.add_argument("--metrics-output", required=True, type=Path)
    parser.add_argument(
        "--implementation-file", action="append", required=True, type=Path
    )
    parser.add_argument("--input", action="append", default=[], type=Path)
    parser.add_argument("--output", action="append", default=[], type=Path)
    parser.add_argument("--stdout-as-evidence", action="store_true")
    parser.add_argument("--timeout-seconds", type=_positive_seconds)
    parser.add_argument("--declared-fact", action="append", default=[])
    parser.add_argument(
        "--allow-sensitive-env",
        action="append",
        default=[],
        metavar="NAME",
        help="pass one named ambient sensitive variable to the experiment child",
    )
    seed = parser.add_mutually_exclusive_group(required=True)
    seed.add_argument("--seed")
    seed.add_argument("--seed-not-set", action="store_true")
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    return parser


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    if arguments.argv[:1] == ["--"]:
        arguments.argv = arguments.argv[1:]
    if not arguments.argv:
        parser.error("an executable and its arguments are required after --")
    if not arguments.output and not arguments.stdout_as_evidence:
        parser.error("declare at least one --output or use --stdout-as-evidence")
    return arguments


def main(argv: Sequence[str] | None = None) -> int:
    secrets = environment_secrets()
    raw_arguments = tuple(sys.argv[1:] if argv is None else argv)
    try:
        _reject_secret_values(raw_arguments, secrets)
        arguments = _parse_args(argv)
        if _ATTEMPT_ID.fullmatch(arguments.attempt_id) is None:
            raise ValueError("attempt-id must be a safe 1-80 character identifier")
        if arguments.seed is not None and not arguments.seed.strip():
            raise ValueError("--seed must contain a non-empty explicit value")
        auxiliary_environment, _ = child_process_environment()
        research_environment, sensitive_environment_passthrough = (
            child_process_environment(arguments.allow_sensitive_env)
        )
        workspace = ResearchWorkspace(
            arguments.run_root,
            version=arguments.version,
            product_root=arguments.product_root,
        )
        workspace.assert_run_writable()
        cwd = arguments.cwd.resolve()
        implementation_files = [path.resolve() for path in arguments.implementation_file]
        inputs = [path.resolve() for path in arguments.input]
        outputs = [path.resolve() for path in arguments.output]
        experiment_spec_path = Path(os.path.abspath(arguments.experiment_spec))
        metrics_output = Path(os.path.abspath(arguments.metrics_output))
        capture_dir = workspace.experiment_path / "attempts" / arguments.attempt_id
        _validate_paths(
            workspace,
            capture_dir,
            cwd,
            implementation_files,
            inputs,
            outputs,
            experiment_spec_path,
            metrics_output,
        )
        knowledge_database = workspace.product_root / "knowledge_base" / "knowledge.sqlite"
        knowledge_store = (
            KnowledgeStore(knowledge_database, read_only=True)
            if knowledge_database.is_file()
            else None
        )
        try:
            validation_workspace = ResearchWorkspace(
                arguments.run_root,
                knowledge_store=knowledge_store,
                version=arguments.version,
                product_root=arguments.product_root,
            )
            spec_data, spec = _load_experiment_spec(
                validation_workspace, experiment_spec_path
            )
        finally:
            if knowledge_store is not None:
                knowledge_store.close()
        if contains_secret(spec_data, secrets):
            raise ValueError("experiment spec contains a possible credential")
        declared_facts = _parse_declared_facts(arguments.declared_fact, secrets)
        runner_executable = Path(sys.executable).resolve(strict=True)
        runner_executable_fact = {
            "status": "bound",
            **file_fact(runner_executable),
        }
        subject_provenance = _subject_provenance(
            arguments.argv[0],
            cwd=cwd,
            environment=research_environment,
            runner_executable=runner_executable,
        )
        dependency_data, dependency_source = _dependency_snapshot_bytes()
        git_fact = _git_facts(
            workspace.implementation_path, environment=auxiliary_environment
        )
        nvidia_fact = _nvidia_facts(environment=auxiliary_environment)
        runner_module_facts = _runner_and_module_facts()
        capture_dir.mkdir(parents=True)
        for output in outputs:
            output.parent.mkdir(parents=True, exist_ok=True)
        metrics_output.parent.mkdir(parents=True, exist_ok=True)
        spec_snapshot_path = workspace.assert_write_target(capture_dir / "spec.json")
        dependency_snapshot_path = workspace.assert_write_target(
            capture_dir / "dependencies.txt"
        )
        spec_snapshot_path.write_bytes(spec_data)
        dependency_snapshot_path.write_bytes(dependency_data)
    except (OSError, UnicodeError, ValueError) as error:
        message = redact_secrets(str(error).encode("utf-8", errors="replace"), secrets)
        print("run_local_experiment: " + message.decode("utf-8", errors="replace"), file=sys.stderr)
        return 2

    implementation_facts = []
    for path in implementation_files:
        fact = file_fact(path)
        fact["path"] = path.relative_to(workspace.workspace_path).as_posix()
        implementation_facts.append(fact)
    input_facts = [file_fact(path) for path in inputs]
    output_facts: list[dict[str, Any]] = [
        {"path": str(path), "before": {"exists": False}} for path in outputs
    ]
    started_at = _utc_now()
    timer = time.perf_counter()
    timed_out = False
    termination_method: str | None = None
    process_tree_cleanup_ok: bool | None = None
    stdout_path = workspace.assert_write_target(capture_dir / "stdout.bin")
    stderr_path = workspace.assert_write_target(capture_dir / "stderr.bin")
    with tempfile.TemporaryDirectory(
        prefix="crl-experiment-capture-", ignore_cleanup_errors=True
    ) as temporary:
        raw_stdout = Path(temporary) / "stdout.raw"
        raw_stderr = Path(temporary) / "stderr.raw"
        try:
            with raw_stdout.open("xb") as stdout_handle, raw_stderr.open(
                "xb"
            ) as stderr_handle:
                popen_options: dict[str, Any] = {}
                if os.name == "nt":
                    popen_options["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
                else:
                    popen_options["start_new_session"] = True
                process = subprocess.Popen(
                    arguments.argv,
                    cwd=cwd,
                    env=research_environment,
                    shell=False,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    **popen_options,
                )
                try:
                    command_exit_code = process.wait(timeout=arguments.timeout_seconds)
                    command_error: str | None = None
                except subprocess.TimeoutExpired:
                    timed_out = True
                    termination_method, process_tree_cleanup_ok = _terminate_process_tree(
                        process, environment=auxiliary_environment
                    )
                    command_exit_code = process.returncode
                    command_error = (
                        "TimeoutExpired: experiment exceeded "
                        f"{arguments.timeout_seconds:g} seconds"
                    )
        except OSError as error:
            command_error = f"{type(error).__name__}: {error}"
            command_exit_code = None
            if not raw_stdout.exists():
                raw_stdout.write_bytes(b"")
            raw_stderr.write_bytes(str(error).encode("utf-8", errors="replace"))
        stdout_redacted = redact_file(raw_stdout, stdout_path, secrets)
        stderr_redacted = redact_file(raw_stderr, stderr_path, secrets)
    duration = time.perf_counter() - timer
    finished_at = _utc_now()

    metrics_fact, metrics_payload = _capture_metrics(
        workspace,
        metrics_output,
        capture_dir / "metrics.json",
        spec.experiment_id,
        spec.primary_metric,
        secrets,
    )
    metrics_contract_ok = not metrics_fact["validation_errors"]

    output_contract_ok = True
    for fact, output in zip(output_facts, outputs, strict=True):
        if output.is_file():
            workspace.assert_write_target(output)
            after, scan = _file_fact_and_scan(output, secrets)
            after.pop("path")
            detection = []
            if scan.environment_secret:
                detection.append("environment_secret")
            if scan.heuristic_pattern:
                detection.append("credential_pattern")
            retained = not scan.contains_possible_credential
            fact["after"] = {
                "exists": True,
                **after,
                "contains_possible_credential": scan.contains_possible_credential,
                "credential_detection": detection,
                "artifact_retained": retained,
            }
            if not retained:
                output_contract_ok = False
                _remove_sensitive_output(output)
        else:
            output_contract_ok = False
            fact["after"] = {
                "exists": output.exists(),
                "kind": "directory" if output.is_dir() else "missing",
            }

    if command_error is not None:
        command_error = redact_secrets(
            command_error.encode("utf-8", errors="replace"), secrets
        ).decode("utf-8", errors="replace")
    stdout_fact = file_fact(stdout_path)
    stdout_evidence_ok = bool(
        arguments.stdout_as_evidence
        and stdout_fact["size_bytes"] > 0
        and not stdout_redacted
    )
    output_evidence_ok = any(
        isinstance(fact.get("after"), dict)
        and fact["after"].get("artifact_retained") is True
        and isinstance(fact["after"].get("size_bytes"), int)
        and fact["after"]["size_bytes"] > 0
        for fact in output_facts
    )
    evidence_contract_ok = stdout_evidence_ok or output_evidence_ok
    runner_exit_code = TIMEOUT_EXIT_CODE if timed_out else (
        command_exit_code
        if command_exit_code not in (None, 0)
        else (
            0
            if command_exit_code == 0
            and output_contract_ok
            and evidence_contract_ok
            and metrics_contract_ok
            else 2
        )
    )
    budget_facts = _budget_facts(
        spec.budget_ceiling,
        duration,
        metrics_payload.get("resource_usage")
        if isinstance(metrics_payload, dict)
        else None,
    )
    execution = {
        "schema_version": SCHEMA_VERSION,
        "run_root": str(workspace.workspace_path),
        "version": workspace.version,
        "attempt_id": arguments.attempt_id,
        "argv": arguments.argv,
        "cwd": str(cwd),
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "duration_seconds": duration,
        "command_exit_code": command_exit_code,
        "runner_exit_code": runner_exit_code,
        "command_error": command_error,
        "timed_out": timed_out,
        "timeout_seconds": arguments.timeout_seconds,
        "termination_method": termination_method,
        "process_tree_cleanup_ok": process_tree_cleanup_ok,
        "seed": (
            {"status": "not_set"}
            if arguments.seed_not_set
            else {"status": "set", "value": arguments.seed}
        ),
        "implementation_files": implementation_facts,
        "inputs": input_facts,
        "outputs": output_facts,
        "output_contract_ok": output_contract_ok,
        "metrics_contract_ok": metrics_contract_ok,
        "stdout_as_evidence": arguments.stdout_as_evidence,
        "evidence_contract_ok": evidence_contract_ok,
        "capture": {
            "stdout": {**stdout_fact, "redaction_applied": stdout_redacted},
            "stderr": {**file_fact(stderr_path), "redaction_applied": stderr_redacted},
        },
        "experiment_spec": {
            "source_path": experiment_spec_path.relative_to(
                workspace.workspace_path
            ).as_posix(),
            "snapshot": file_fact(spec_snapshot_path),
        },
        "metrics": metrics_fact,
        "budget_facts": budget_facts,
        "environment_facts": {
            "sensitive_environment_passthrough": list(
                sensitive_environment_passthrough
            ),
            "platform": platform.platform(),
            "cpu_count": (
                os.cpu_count()
                if os.cpu_count() is not None
                else {
                    "status": "unavailable",
                    "reason": "os.cpu_count returned None",
                }
            ),
            "git": git_fact,
            "nvidia": nvidia_fact,
            "runner": {
                "python": sys.version,
                "executable": runner_executable_fact,
                "dependencies": {
                    "scope": "formal_runner_machine_environment",
                    "subject_relationship": "unbound",
                    **dependency_source,
                    "snapshot": file_fact(dependency_snapshot_path),
                },
                "runner_and_modules": runner_module_facts,
            },
            "subject": subject_provenance,
            "declared_facts": declared_facts,
        },
        "warnings": budget_facts["warnings"],
    }
    execution_data = (
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if contains_secret(execution_data, secrets):
        execution_data = redact_secrets(execution_data, secrets)
        execution = json.loads(execution_data.decode("utf-8"))
        runner_exit_code = 2
        execution["runner_exit_code"] = runner_exit_code
        execution_data = (
            json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
    execution_path = workspace.assert_write_target(capture_dir / "execution.json")
    execution_path.write_bytes(execution_data)
    print(json.dumps(execution, ensure_ascii=False, sort_keys=True))
    return int(runner_exit_code)


def _terminate_process_tree(
    process: subprocess.Popen[Any], *, environment: dict[str, str] | None = None
) -> tuple[str, bool]:
    if process.poll() is not None:
        return "already_exited_after_timeout", True
    if os.name == "nt":
        method = "windows_ctrl_break"
        try:
            process.send_signal(signal.CTRL_BREAK_EVENT)
        except (OSError, ValueError):
            method = "windows_taskkill_tree"
        else:
            try:
                process.wait(timeout=_TERMINATION_GRACE_SECONDS)
                return method, True
            except subprocess.TimeoutExpired:
                method = "windows_ctrl_break_then_taskkill_tree"
        try:
            killed = subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=_TERMINATION_GRACE_SECONDS,
                check=False,
            )
            process.wait(timeout=_TERMINATION_GRACE_SECONDS)
            return method, killed.returncode == 0 and process.poll() is not None
        except (OSError, subprocess.TimeoutExpired):
            return method, False

    method = "posix_sigterm_group"
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except (OSError, ProcessLookupError):
        if process.poll() is not None:
            return "already_exited_after_timeout", True
    try:
        process.wait(timeout=_TERMINATION_GRACE_SECONDS)
        return method, True
    except subprocess.TimeoutExpired:
        method = "posix_sigterm_then_sigkill_group"
    try:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=_TERMINATION_GRACE_SECONDS)
        return method, process.poll() is not None
    except (OSError, ProcessLookupError, subprocess.TimeoutExpired):
        return method, False


def _validate_paths(
    workspace: ResearchWorkspace,
    capture_dir: Path,
    cwd: Path,
    implementation_files: list[Path],
    inputs: list[Path],
    outputs: list[Path],
    experiment_spec_path: Path,
    metrics_output: Path,
) -> None:
    if capture_dir.exists():
        raise ValueError(f"attempt directory already exists: {capture_dir}")
    attempts_root = workspace.assert_write_target(
        workspace.experiment_path / "attempts"
    )
    workspace.assert_write_target(capture_dir)
    if capture_dir.parent != attempts_root:
        raise ValueError("attempt directory must be a direct child of the current attempts directory")
    reserved = {
        capture_dir / "dependencies.txt",
        capture_dir / "execution.json",
        capture_dir / "metrics.json",
        capture_dir / "spec.json",
        capture_dir / "stderr.bin",
        capture_dir / "stdout.bin",
    }
    workspace.assert_write_target(cwd)
    if not cwd.is_dir() or not cwd.is_relative_to(workspace.workspace_path):
        raise ValueError("cwd must be an existing directory inside the bound Run")
    implementation_root = workspace.implementation_path.resolve()
    seen_implementation: set[Path] = set()
    for path in implementation_files:
        workspace.assert_write_target(path)
        if (
            not path.is_file()
            or path.stat().st_size <= 0
            or not path.is_relative_to(implementation_root)
        ):
            raise ValueError(
                "implementation-file must be a non-empty file inside the current "
                f"implementation directory: {path}"
            )
        if path in seen_implementation:
            raise ValueError(f"duplicate implementation-file: {path}")
        seen_implementation.add(path)
    for path in inputs:
        try:
            workspace.assert_formal_input(path)
        except FileNotFoundError as error:
            raise ValueError(f"input is not an existing file: {path}") from error
    for path in outputs:
        workspace.assert_write_target(path)
        if not path.is_relative_to(capture_dir):
            raise ValueError(f"declared output must be inside this attempt directory: {path}")
        if path in reserved:
            raise ValueError(f"declared output collides with a reserved attempt artifact: {path}")
        if path.exists():
            raise ValueError(f"output already exists before execution: {path}")
    workspace.assert_read_target(experiment_spec_path)
    workspace.assert_write_target(metrics_output)
    if not metrics_output.is_relative_to(capture_dir):
        raise ValueError("metrics-output must be inside this attempt directory")
    if metrics_output in reserved:
        raise ValueError("metrics-output collides with a reserved attempt artifact")
    if metrics_output.exists():
        raise ValueError(f"metrics-output already exists before execution: {metrics_output}")


def _load_experiment_spec(workspace: ResearchWorkspace, path: Path) -> tuple[bytes, Any]:
    safe_path = workspace.assert_read_target(path)
    data = safe_path.read_bytes()
    if not data or len(data) > 4 * 1024 * 1024:
        raise ValueError("experiment spec must be a non-empty reasonably sized JSON file")
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
        raise ValueError("experiment spec must be UTF-8 without BOM and use LF newlines")
    try:
        value = json.loads(data.decode("utf-8"), parse_constant=_reject_json_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid experiment spec JSON: {error}") from error
    spec = experiment_spec_from_mapping(value)
    validate_experiment_spec(
        spec,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
    )
    expected_path = workspace.experiment_path / "specs" / f"{spec.experiment_id}.json"
    if safe_path != workspace.assert_read_target(expected_path):
        raise ValueError("experiment-spec path does not match its experiment_id")

    portfolio = workspace.read_hypotheses(required=True)
    assert portfolio is not None
    hypothesis_ids = {
        item.hypothesis_id for item in portfolio.portfolio.hypotheses
    }
    if spec.hypothesis_id not in hypothesis_ids:
        raise ValueError("experiment spec hypothesis_id is not current in this Run version")
    claims: dict[str, str] = {}
    for document in list_plans(workspace):
        for claim in document.plan.claims:
            if claim.claim_id in claims:
                raise ValueError("claim_id appears in multiple falsification plans")
            claims[claim.claim_id] = document.plan.hypothesis_id
    missing = sorted(set(spec.claim_ids) - set(claims))
    if missing:
        raise ValueError(f"experiment spec references unknown current claim ids: {missing}")
    mismatched = sorted(
        claim_id
        for claim_id in spec.claim_ids
        if claims[claim_id] != spec.hypothesis_id
    )
    if mismatched:
        raise ValueError(
            f"experiment spec claim ids belong to another hypothesis: {mismatched}"
        )
    return data, spec


def _parse_declared_facts(
    values: Sequence[str], secrets: tuple[bytes, ...]
) -> dict[str, str]:
    facts: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ValueError("declared-fact must use KEY=VALUE")
        key, value = item.split("=", 1)
        if _DECLARED_FACT_KEY.fullmatch(key) is None or key not in _DECLARED_FACT_KEYS:
            raise ValueError(f"declared-fact key is not allowed: {key!r}")
        if not value.strip() or "\r" in value or "\n" in value or len(value) > 4096:
            raise ValueError("declared-fact value must be non-empty single-line text")
        if key in facts:
            raise ValueError(f"duplicate declared-fact key: {key}")
        if contains_secret(value.encode("utf-8"), secrets):
            raise ValueError(f"declared-fact {key} contains a possible credential")
        facts[key] = value
    return facts


def _dependency_snapshot_bytes() -> tuple[bytes, dict[str, str]]:
    lock_path = Path(__file__).resolve().parents[1] / "CRL_ENVIRONMENT_LOCK.txt"
    if lock_path.is_file():
        data = lock_path.read_bytes()
        return data, {"source_type": "lock_file", "source_path": str(lock_path)}
    distributions = sorted(
        {
            f"{distribution.metadata.get('Name') or 'unknown'}=={distribution.version}"
            for distribution in importlib.metadata.distributions()
        },
        key=str.casefold,
    )
    data = ("\n".join(distributions) + "\n").encode("utf-8")
    return data, {
        "source_type": "installed_distributions",
        "source_path": "unavailable: CRL_ENVIRONMENT_LOCK.txt not found",
    }


def _git_facts(
    implementation_root: Path, *, environment: dict[str, str] | None = None
) -> dict[str, Any]:
    try:
        root = _command_stdout(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=implementation_root,
            environment=environment,
        ).decode("utf-8").strip()
        commit = _command_stdout(
            ["git", "rev-parse", "HEAD"],
            cwd=implementation_root,
            environment=environment,
        ).decode("ascii").strip()
        status = _command_stdout(
            ["git", "status", "--porcelain=v1", "-z"],
            cwd=implementation_root,
            environment=environment,
        )
        diff = _command_stdout(
            ["git", "diff", "--binary", "HEAD", "--"],
            cwd=implementation_root,
            environment=environment,
        )
    except (OSError, UnicodeError, subprocess.SubprocessError, ValueError) as error:
        return {"status": "unavailable", "reason": f"{type(error).__name__}: {error}"}
    return {
        "status": "available",
        "repository_root": root,
        "commit": commit,
        "dirty": bool(status),
        "diff_sha256": hashlib.sha256(diff).hexdigest(),
    }


def _nvidia_facts(
    *, environment: dict[str, str] | None = None
) -> dict[str, Any]:
    try:
        rows = _command_stdout(
            [
                "nvidia-smi",
                "--query-gpu=index,name,driver_version,memory.total",
                "--format=csv,noheader,nounits",
            ],
            environment=environment,
        ).decode("utf-8")
        summary = _command_stdout(
            ["nvidia-smi"], environment=environment
        ).decode("utf-8")
    except (OSError, UnicodeError, subprocess.SubprocessError, ValueError) as error:
        return {"status": "unavailable", "reason": f"{type(error).__name__}: {error}"}
    gpus = []
    for row in rows.splitlines():
        parts = [item.strip() for item in row.split(",", 3)]
        if len(parts) == 4:
            gpus.append(
                {
                    "index": parts[0],
                    "name": parts[1],
                    "driver_version": parts[2],
                    "memory_total_mib": parts[3],
                }
            )
    cuda = re.search(r"CUDA Version:\s*([0-9.]+)", summary)
    return {
        "status": "available",
        "gpus": gpus,
        "cuda_version": (
            cuda.group(1)
            if cuda is not None
            else {"status": "unavailable", "reason": "not reported by nvidia-smi"}
        ),
    }


def _command_stdout(
    argv: list[str],
    *,
    cwd: Path | None = None,
    environment: dict[str, str] | None = None,
) -> bytes:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(f"command exited with code {completed.returncode}")
    return completed.stdout


def _runner_and_module_facts() -> list[dict[str, Any]]:
    project = Path(__file__).resolve().parents[1]
    paths = (
        Path(__file__).resolve(),
        project / "crl_v3" / "experiment.py",
        project / "crl_v3" / "falsification.py",
        project / "crl_v3" / "workspace.py",
        project / "crl_v3" / "decision.py",
    )
    facts = []
    for path in paths:
        fact = file_fact(path)
        fact["path"] = path.relative_to(project).as_posix()
        facts.append(fact)
    return facts


def _subject_provenance(
    argv0: str,
    *,
    cwd: Path,
    environment: dict[str, str],
    runner_executable: Path,
) -> dict[str, Any]:
    candidate = Path(argv0)
    if candidate.is_absolute():
        resolution = "absolute_path"
    elif candidate.parent != Path("."):
        candidate = cwd / candidate
        resolution = "cwd_relative_path"
    else:
        located = shutil.which(argv0, path=environment.get("PATH"))
        if located is None:
            return _unbound_subject_provenance(
                argv0, "subject executable could not be resolved without execution"
            )
        candidate = Path(located)
        resolution = "path_search"
    try:
        executable = candidate.resolve(strict=True)
    except (OSError, RuntimeError):
        return _unbound_subject_provenance(
            argv0, "subject executable path could not be bound to an existing file"
        )
    if not executable.is_file():
        return _unbound_subject_provenance(
            argv0, "subject executable path is not a regular file"
        )

    relationship = (
        "same_executable"
        if executable == runner_executable
        else "different_executable"
    )
    runtime = (
        {
            "status": "bound_to_runner_python",
            "python": sys.version,
        }
        if relationship == "same_executable"
        else {
            "status": "unbound",
            "reason": (
                "subject runtime type and version are not inferred from executable bytes"
            ),
        }
    )
    return {
        "argv0": argv0,
        "executable": {
            "status": "bound",
            "resolution": resolution,
            **file_fact(executable),
        },
        "runner_relationship": relationship,
        "runtime": runtime,
        "dependencies": {
            "status": "unbound",
            "reason": (
                "subject dependencies are not automatically inspected or inferred "
                "from runner dependencies"
            ),
        },
        "environment": {
            "status": "partially_bound",
            "policy": "sanitized_parent_with_explicit_sensitive_passthrough",
            "unbound_reason": (
                "non-sensitive subject environment names and values are not persisted"
            ),
        },
    }


def _unbound_subject_provenance(argv0: str, reason: str) -> dict[str, Any]:
    return {
        "argv0": argv0,
        "executable": {"status": "unbound", "reason": reason},
        "runner_relationship": "unbound",
        "runtime": {
            "status": "unbound",
            "reason": "subject runtime identity is unavailable without an executable binding",
        },
        "dependencies": {
            "status": "unbound",
            "reason": (
                "subject dependencies are not automatically inspected or inferred "
                "from runner dependencies"
            ),
        },
        "environment": {
            "status": "partially_bound",
            "policy": "sanitized_parent_with_explicit_sensitive_passthrough",
            "unbound_reason": (
                "non-sensitive subject environment names and values are not persisted"
            ),
        },
    }


def _capture_metrics(
    workspace: ResearchWorkspace,
    source: Path,
    snapshot: Path,
    experiment_id: str,
    primary_metric: str,
    secrets: tuple[bytes, ...],
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    fact: dict[str, Any] = {
        "source_path": source.relative_to(workspace.workspace_path).as_posix(),
        "snapshot": None,
        "contains_possible_credential": False,
        "credential_detection": [],
        "validation_errors": [],
    }
    if not source.is_file():
        fact["validation_errors"].append("metrics output is missing")
        return fact, None
    try:
        workspace.assert_read_target(source)
        source_fact, scan = _file_fact_and_scan(source, secrets)
        fact["source_size_bytes"] = source_fact["size_bytes"]
        fact["source_sha256"] = source_fact["sha256"]
        detection = []
        if scan.environment_secret:
            detection.append("environment_secret")
        if scan.heuristic_pattern:
            detection.append("credential_pattern")
        fact["contains_possible_credential"] = scan.contains_possible_credential
        fact["credential_detection"] = detection
        if scan.contains_possible_credential:
            _remove_sensitive_output(source)
            fact["validation_errors"].append(
                "metrics output contained a possible credential and was removed"
            )
            return fact, None
        data = source.read_bytes()
        payload = validate_metrics_json_bytes(
            data,
            expected_experiment_id=experiment_id,
            primary_metric=primary_metric,
        )
        snapshot = workspace.assert_write_target(snapshot)
        snapshot.write_bytes(data)
        fact["snapshot"] = file_fact(snapshot)
        return fact, payload
    except (OSError, UnicodeError, ValueError) as error:
        fact["validation_errors"].append(f"{type(error).__name__}: {error}")
        return fact, None


def _budget_facts(
    ceiling: str,
    duration_seconds: float,
    resource_usage: object,
) -> dict[str, Any]:
    usage = resource_usage if isinstance(resource_usage, dict) else {}
    actual = {
        "duration_seconds": duration_seconds,
        "tokens": usage.get("tokens", "unknown"),
        "api_calls": usage.get("api_calls", "unknown"),
        "gpu_time_seconds": usage.get("gpu_time_seconds", "unknown"),
    }
    limits: dict[str, int | float] | None = None
    comparison: dict[str, str] = {
        "status": "unavailable",
        "reason": "budget_ceiling is not a machine-readable JSON object",
    }
    try:
        value = json.loads(ceiling)
        if (
            isinstance(value, dict)
            and value
            and set(value) <= _HARD_BUDGET_KEYS
            and all(_valid_budget_limit(name, item) for name, item in value.items())
        ):
            limits = value
            comparison = {"status": "compared"}
    except json.JSONDecodeError:
        pass
    warnings = []
    if limits is not None:
        for name, limit in limits.items():
            observed = actual[name]
            if type(observed) in {int, float} and observed > limit:
                warnings.append(
                    f"hard budget exceeded: {name} actual={observed} limit={limit}"
                )
    return {
        "spec_budget_ceiling": ceiling,
        "machine_readable_limits": limits,
        "comparison": comparison,
        "actual": actual,
        "warnings": warnings,
    }


def _valid_budget_limit(name: str, value: object) -> bool:
    if name in {"tokens", "api_calls"}:
        return type(value) is int and value >= 0
    return type(value) in {int, float} and math.isfinite(value) and value >= 0


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def _reject_secret_values(values: Sequence[str], secrets: tuple[bytes, ...]) -> None:
    rendered = "\0".join(str(item) for item in values).encode("utf-8", errors="ignore")
    if contains_secret(rendered, secrets):
        raise ValueError("command-line arguments or paths contain a possible credential")


def _file_fact_and_scan(
    path: Path, secrets: tuple[bytes, ...]
) -> tuple[dict[str, Any], SecretScan]:
    digest = hashlib.sha256()
    size = 0
    overlap = max(max((len(value) for value in secrets), default=0) + 8, 8192)
    tail = b""
    exact = False
    heuristic = False
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            size += len(chunk)
            digest.update(chunk)
            scan = scan_secret_bytes(tail + chunk, secrets)
            exact = exact or scan.environment_secret
            heuristic = heuristic or scan.heuristic_pattern
            tail = (tail + chunk)[-overlap:]
    return (
        {"path": str(path), "size_bytes": size, "sha256": digest.hexdigest()},
        SecretScan(exact, heuristic),
    )


def _remove_sensitive_output(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        with path.open("wb") as handle:
            handle.flush()
            os.fsync(handle.fileno())
        path.unlink(missing_ok=True)
    if path.exists():
        raise OSError(f"could not remove credential-bearing output: {path}")


if __name__ == "__main__":
    raise SystemExit(main())
