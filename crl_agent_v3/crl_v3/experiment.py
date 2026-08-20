from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

from crl_v3.workspace import (
    ResearchWorkspace,
    _atomic_write_text,
    _required_file,
    _sha256,
    _validate_utf8_lf,
    safe_relative_path,
)


SUPPORTED_REVIEW_SUPPORT_EXECUTION_SCHEMAS = frozenset({5, 6, 7, 8})
CURRENT_FORMAL_EXECUTION_SCHEMA = 8
INTEGRITY_EXECUTION_SCHEMAS = frozenset({7, 8})


_METRICS_REQUIRED_FIELDS = {
    "schema_version",
    "experiment_id",
    "records",
    "resource_usage",
    "errors",
    "warnings",
}
_METRIC_RECORD_REQUIRED_FIELDS = {
    "name",
    "value",
    "unit",
    "split",
    "aggregation",
    "n",
}
_METRIC_RECORD_OPTIONAL_FIELDS = {"seed", "replicate"}
_RESOURCE_USAGE_FIELDS = {
    "tokens",
    "api_calls",
    "wall_time_seconds",
    "gpu_time_seconds",
    "estimated_cost",
}


@dataclass(frozen=True, slots=True)
class ExperimentPlanDocument:
    path: str
    content: str
    sha256: str


@dataclass(frozen=True, slots=True)
class ExperimentArtifact:
    path: str
    relative_path: str
    area: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class ExperimentResultDocument:
    path: str
    content: str
    sha256: str


def write_experiment_plan(
    workspace: ResearchWorkspace, content: str
) -> ExperimentPlanDocument:
    path = workspace.experiment_path / "plan.md"
    workspace._assert_narrative_mutable(path)
    data = _atomic_write_text(path, content, within=workspace.workspace_path)
    return ExperimentPlanDocument(str(path), data.decode("utf-8"), _sha256(data))


def read_experiment_plan(workspace: ResearchWorkspace) -> ExperimentPlanDocument:
    path = workspace.experiment_path / "plan.md"
    data = _read_required_markdown(workspace, path)
    return ExperimentPlanDocument(str(path), data.decode("utf-8"), _sha256(data))


def save_experiment_artifact(
    workspace: ResearchWorkspace,
    source: str | Path,
    relative_path: str,
    *,
    area: str = "experiment",
    replace: bool = False,
) -> ExperimentArtifact:
    workspace.assert_run_writable()
    source_path = Path(source).resolve()
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    relative = safe_relative_path(relative_path)
    roots = {
        "experiment": workspace.experiment_path,
        "implementation": workspace.implementation_path,
        "workbench": workspace.workbench_path,
    }
    if area not in roots:
        raise ValueError(f"unsupported artifact area: {area!r}")
    if replace and area != "workbench":
        raise ValueError("replace=True is only allowed for workbench artifacts")
    target = workspace.assert_write_target(roots[area] / relative)
    workspace._assert_narrative_mutable(target)
    if source_path == target.resolve():
        raise ValueError("artifact source and destination must differ")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not replace:
        raise FileExistsError(f"experiment artifact already exists: {target}")
    temporary = target.with_name(f".{target.name}.{uuid4().hex}.tmp")
    try:
        with source_path.open("rb") as source_handle, temporary.open("xb") as target_handle:
            shutil.copyfileobj(source_handle, target_handle)
            target_handle.flush()
            os.fsync(target_handle.fileno())
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    size_bytes, digest = _file_size_sha256(target)
    return ExperimentArtifact(
        path=str(target),
        relative_path=target.relative_to(workspace.workspace_path).as_posix(),
        area=area,
        size_bytes=size_bytes,
        sha256=digest,
    )


def write_experiment_result(
    workspace: ResearchWorkspace, content: str
) -> ExperimentResultDocument:
    path = workspace.experiment_path / "result.md"
    workspace._assert_narrative_mutable(path)
    data = _atomic_write_text(path, content, within=workspace.workspace_path)
    return ExperimentResultDocument(str(path), data.decode("utf-8"), _sha256(data))


def read_experiment_result(workspace: ResearchWorkspace) -> ExperimentResultDocument:
    path = workspace.experiment_path / "result.md"
    data = _read_required_markdown(workspace, path)
    return ExperimentResultDocument(str(path), data.decode("utf-8"), _sha256(data))


def list_experiment_files(workspace: ResearchWorkspace) -> tuple[ExperimentArtifact, ...]:
    artifacts: list[ExperimentArtifact] = []
    for area, root in (
        ("implementation", workspace.implementation_path),
        ("experiment", workspace.experiment_path),
        ("workbench", workspace.workbench_path),
    ):
        workspace.assert_write_target(root)
        if not root.is_dir():
            continue
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            workspace.assert_write_target(path)
            size_bytes, digest = _file_size_sha256(path)
            artifacts.append(
                ExperimentArtifact(
                    path=str(path),
                    relative_path=path.relative_to(workspace.workspace_path).as_posix(),
                    area=area,
                    size_bytes=size_bytes,
                    sha256=digest,
                )
            )
    return tuple(artifacts)


def experiment_material_errors(
    workspace: ResearchWorkspace,
    attempt_ids: Iterable[str] | None = None,
) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        attempts = workspace.assert_write_target(
            workspace.experiment_path / "attempts"
        )
    except ValueError as error:
        return (f"invalid experiment attempts directory: {error}",)
    requested = None if attempt_ids is None else tuple(
        dict.fromkeys(_attempt_id(item) for item in attempt_ids)
    )
    if requested is not None and not requested:
        return ("at least one supporting attempt id is required",)
    attempt_dirs: list[Path] = []
    if requested is not None:
        for attempt_id in requested:
            try:
                attempt_dirs.append(
                    workspace.assert_write_target(attempts / attempt_id)
                )
            except ValueError as error:
                errors.append(f"invalid supporting attempt {attempt_id}: {error}")
    elif attempts.is_dir():
        for path in sorted(attempts.iterdir()):
            if path.is_dir():
                try:
                    workspace.assert_write_target(path)
                except ValueError:
                    continue
                attempt_dirs.append(path)
    if not attempt_dirs:
        errors.append(f"missing experiment attempt directory: {attempts}")
    elif requested is not None:
        for attempt in attempt_dirs:
            attempt_errors = _supporting_attempt_errors(workspace, attempt)
            if attempt_errors:
                errors.append(
                    f"invalid supporting attempt {attempt.name}: "
                    + "; ".join(attempt_errors)
                )
    else:
        attempt_results = [
            (attempt, _supporting_attempt_errors(workspace, attempt))
            for attempt in attempt_dirs
        ]
        if not any(not attempt_errors for _, attempt_errors in attempt_results):
            details = []
            for attempt, attempt_errors in attempt_results[:3]:
                summary = "; ".join(attempt_errors[:3]) or "not a supporting attempt"
                details.append(f"{attempt.name}: {summary}")
            errors.append(
                "no valid successful supporting experiment attempt: "
                + " | ".join(details)
            )
    return tuple(errors)


def valid_supporting_attempt_ids(workspace: ResearchWorkspace) -> tuple[str, ...]:
    try:
        attempts = workspace.assert_write_target(
            workspace.experiment_path / "attempts"
        )
    except ValueError:
        return ()
    if not attempts.is_dir():
        return ()
    valid = []
    for attempt in sorted(attempts.iterdir()):
        if not attempt.is_dir():
            continue
        try:
            workspace.assert_write_target(attempt)
        except ValueError:
            continue
        if not _supporting_attempt_errors(workspace, attempt):
            valid.append(attempt.name)
    return tuple(valid)


def file_fact(path: Path) -> dict[str, Any]:
    size_bytes, digest = _file_size_sha256(path)
    return {"path": str(path), "size_bytes": size_bytes, "sha256": digest}


def validate_metrics_json_bytes(
    data: bytes,
    *,
    expected_experiment_id: str,
    primary_metric: str,
) -> dict[str, Any]:
    """Validate schema 1 metric facts without interpreting metric quality."""

    if not data:
        raise ValueError("metrics JSON is empty")
    if len(data) > 16 * 1024 * 1024:
        raise ValueError("metrics JSON is unreasonably large")
    _validate_utf8_lf(data, "metrics JSON")
    try:
        value = json.loads(data.decode("utf-8"), parse_constant=_reject_json_constant)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid metrics JSON: {error}") from error
    if not isinstance(value, dict):
        raise ValueError("metrics JSON must contain an object")
    missing = _METRICS_REQUIRED_FIELDS - set(value)
    if missing:
        raise ValueError(f"metrics JSON is missing required fields: {sorted(missing)}")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("metrics schema_version must be integer 1")
    if value["experiment_id"] != expected_experiment_id:
        raise ValueError("metrics experiment_id does not match the experiment spec")

    records = value["records"]
    if not isinstance(records, list) or not records:
        raise ValueError("metrics records must be a non-empty array")
    metric_names: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"metrics record {index} must be an object")
        fields = set(record)
        missing_record = _METRIC_RECORD_REQUIRED_FIELDS - fields
        unsupported = fields - (
            _METRIC_RECORD_REQUIRED_FIELDS | _METRIC_RECORD_OPTIONAL_FIELDS
        )
        if missing_record or unsupported:
            raise ValueError(
                f"metrics record {index} fields are invalid; "
                f"missing={sorted(missing_record)}, unsupported={sorted(unsupported)}"
            )
        name = _nonempty_metric_text(record["name"], f"metrics record {index} name")
        metric_names.add(name)
        for field in ("unit", "split", "aggregation"):
            _nonempty_metric_text(
                record[field], f"metrics record {index} {field}"
            )
        metric_value = record["value"]
        if type(metric_value) not in {int, float} or not math.isfinite(metric_value):
            raise ValueError(f"metrics record {index} value must be a finite number")
        if type(record["n"]) is not int or record["n"] < 0:
            raise ValueError(f"metrics record {index} n must be a non-negative integer")
        for field in _METRIC_RECORD_OPTIONAL_FIELDS & fields:
            item = record[field]
            if type(item) is int:
                continue
            if not isinstance(item, str) or not item.strip() or "\r" in item or "\n" in item:
                raise ValueError(
                    f"metrics record {index} {field} must be an integer or non-empty text"
                )
    if primary_metric not in metric_names:
        raise ValueError("experiment spec primary_metric is absent from metrics records")

    usage = value["resource_usage"]
    if not isinstance(usage, dict):
        raise ValueError("metrics resource_usage must be an object")
    missing_usage = _RESOURCE_USAGE_FIELDS - set(usage)
    if missing_usage:
        raise ValueError(
            f"metrics resource_usage is missing fields: {sorted(missing_usage)}"
        )
    for field in _RESOURCE_USAGE_FIELDS:
        _validate_resource_usage_value(field, usage[field])
    for field in ("errors", "warnings"):
        items = value[field]
        if not isinstance(items, list) or not all(
            isinstance(item, str) and item.strip() and "\r" not in item
            for item in items
        ):
            raise ValueError(f"metrics {field} must be an array of non-empty strings")
    _validate_finite_numbers(value, "metrics")
    return value


def supporting_attempt_execution_sha256(
    workspace: ResearchWorkspace, attempt_id: str
) -> str:
    """Return the exact validated execution record identity for one attempt."""

    attempt = workspace.experiment_path / "attempts" / _attempt_id(attempt_id)
    errors = _supporting_attempt_errors(workspace, attempt)
    if errors:
        raise ValueError(
            f"invalid supporting attempt {attempt.name}: " + "; ".join(errors)
        )
    data = _required_file(
        attempt / "execution.json", within=workspace.workspace_path
    )
    return _sha256(data)


def formal_attempt_integrity_execution_sha256(
    workspace: ResearchWorkspace, attempt_id: str
) -> str:
    """Return one schema 7+ identity after outcome-neutral integrity checks."""

    attempt = workspace.experiment_path / "attempts" / _attempt_id(attempt_id)
    errors = _attempt_errors(workspace, attempt, require_supporting=False)
    if errors:
        raise ValueError(
            f"invalid formal attempt integrity {attempt.name}: " + "; ".join(errors)
        )
    data = _required_file(
        attempt / "execution.json", within=workspace.workspace_path
    )
    return _sha256(data)


def schema_7_attempt_integrity_execution_sha256(
    workspace: ResearchWorkspace, attempt_id: str
) -> str:
    """Backward-compatible name for Formal schema 7+ integrity validation."""

    return formal_attempt_integrity_execution_sha256(workspace, attempt_id)


def _supporting_attempt_errors(
    workspace: ResearchWorkspace, attempt: Path
) -> tuple[str, ...]:
    return _attempt_errors(workspace, attempt, require_supporting=True)


def _attempt_errors(
    workspace: ResearchWorkspace,
    attempt: Path,
    *,
    require_supporting: bool,
) -> tuple[str, ...]:
    errors: list[str] = []
    execution_path = attempt / "execution.json"
    try:
        execution_path = workspace.assert_read_target(execution_path)
    except ValueError as error:
        return (str(error),)
    except FileNotFoundError:
        return ("missing execution.json",)
    try:
        data = _required_file(execution_path, within=workspace.workspace_path)
        if len(data) > 4 * 1024 * 1024:
            raise ValueError("execution.json is unreasonably large")
        execution = json.loads(data.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return (f"invalid execution.json: {error}",)
    if not isinstance(execution, dict):
        return ("execution.json must contain an object",)

    schema_version = execution.get("schema_version")
    if require_supporting and schema_version not in SUPPORTED_REVIEW_SUPPORT_EXECUTION_SCHEMAS:
        errors.append("execution schema_version is not supported")
    elif not require_supporting and schema_version not in INTEGRITY_EXECUTION_SCHEMAS:
        errors.append("execution schema_version does not support integrity validation")

    expected_scalars = {
        "run_root": str(workspace.workspace_path),
        "version": workspace.version,
        "attempt_id": attempt.name,
    }
    if require_supporting:
        expected_scalars.update(
            {
                "command_exit_code": 0,
                "runner_exit_code": 0,
                "command_error": None,
                "output_contract_ok": True,
                "evidence_contract_ok": True,
            }
        )
    for name, expected in expected_scalars.items():
        if execution.get(name) != expected:
            errors.append(f"execution {name} does not equal {expected!r}")
    if not require_supporting:
        if execution.get("command_exit_code") is not None and type(
            execution.get("command_exit_code")
        ) is not int:
            errors.append("execution command_exit_code must be integer or null")
        if type(execution.get("runner_exit_code")) is not int:
            errors.append("execution runner_exit_code must be integer")
        if execution.get("command_error") is not None and not isinstance(
            execution.get("command_error"), str
        ):
            errors.append("execution command_error must be text or null")
        for name in ("output_contract_ok", "evidence_contract_ok"):
            if type(execution.get(name)) is not bool:
                errors.append(f"execution {name} must be boolean")

    if schema_version in {6, 7, 8}:
        timed_out = execution.get("timed_out")
        timeout_seconds = execution.get("timeout_seconds")
        termination_method = execution.get("termination_method")
        cleanup_ok = execution.get("process_tree_cleanup_ok")
        if type(timed_out) is not bool:
            errors.append("execution timed_out must be boolean")
        if timeout_seconds is not None and (
            type(timeout_seconds) not in {int, float}
            or not math.isfinite(timeout_seconds)
            or timeout_seconds <= 0
        ):
            errors.append("execution timeout_seconds must be null or positive")
        if timed_out is True:
            if require_supporting:
                errors.append("execution timed_out is true")
            if timeout_seconds is None:
                errors.append("timed-out execution has no timeout_seconds")
            if not isinstance(termination_method, str) or not termination_method:
                errors.append("timed-out execution has no termination_method")
            if type(cleanup_ok) is not bool:
                errors.append("timed-out execution has no process_tree_cleanup_ok fact")
        else:
            if termination_method is not None:
                errors.append("non-timeout execution has a termination_method")
            if cleanup_ok is not None:
                errors.append("non-timeout execution has a process_tree_cleanup_ok fact")

    argv = execution.get("argv")
    if not isinstance(argv, list) or not argv or not all(
        isinstance(item, str) and item for item in argv
    ):
        errors.append("execution argv must be a non-empty string array")
    cwd_value = execution.get("cwd")
    if not isinstance(cwd_value, str):
        errors.append("execution cwd is missing")
    else:
        cwd = Path(cwd_value).resolve()
        if not cwd.is_dir() or not cwd.is_relative_to(workspace.workspace_path):
            errors.append("execution cwd is not an existing Run-local directory")
    environment = execution.get("environment_facts")
    if schema_version == 8:
        if (
            not isinstance(environment, dict)
            or not isinstance(environment.get("platform"), str)
            or not environment["platform"]
        ):
            errors.append("execution environment_facts are incomplete")
    elif not isinstance(environment, dict) or not all(
        isinstance(environment.get(name), str) and environment[name]
        for name in ("platform", "python", "executable")
    ):
        errors.append("execution environment_facts are incomplete")
    if schema_version in {7, 8}:
        errors.extend(
            _schema_7_errors(
                workspace,
                attempt,
                execution,
                environment if isinstance(environment, dict) else None,
                schema_version=schema_version,
                require_valid_metrics=require_supporting,
            )
        )
    seed = execution.get("seed")
    if not isinstance(seed, dict) or seed.get("status") not in {"set", "not_set"}:
        errors.append("execution seed must explicitly be set or not_set")
    elif seed.get("status") == "set" and not isinstance(seed.get("value"), str):
        errors.append("execution seed value must be text")

    implementation_files = execution.get("implementation_files")
    if not isinstance(implementation_files, list) or not implementation_files:
        errors.append("execution implementation_files must be a non-empty array")
    else:
        seen = set()
        implementation_root = workspace.implementation_path.resolve()
        for index, fact in enumerate(implementation_files):
            if not isinstance(fact, dict) or not isinstance(fact.get("path"), str):
                errors.append(f"implementation file {index} fact is invalid")
                continue
            try:
                relative = safe_relative_path(fact["path"])
                expected_path = workspace.assert_write_target(
                    workspace.workspace_path / relative
                )
            except ValueError as error:
                errors.append(f"implementation file {index} path is invalid: {error}")
                continue
            if expected_path in seen:
                errors.append(f"implementation file {index} is duplicated")
                continue
            seen.add(expected_path)
            if not expected_path.resolve().is_relative_to(implementation_root):
                errors.append(
                    f"implementation file {index} is outside current implementation directory"
                )
                continue
            errors.extend(
                _recorded_file_errors(
                    workspace,
                    fact,
                    expected_path,
                    f"implementation file {index}",
                    require_recorded_path=False,
                    require_nonempty=True,
                )
            )

    capture = execution.get("capture")
    if not isinstance(capture, dict):
        errors.append("execution capture is missing")
    else:
        for name in ("stdout", "stderr"):
            expected_path = attempt / f"{name}.bin"
            errors.extend(
                _recorded_file_errors(
                    workspace,
                    capture.get(name),
                    expected_path,
                    name,
                    require_run_local=True,
                )
            )

    stdout_as_evidence = execution.get("stdout_as_evidence")
    if type(stdout_as_evidence) is not bool:
        errors.append("execution stdout_as_evidence must be boolean")

    inputs = execution.get("inputs")
    if not isinstance(inputs, list):
        errors.append("execution inputs must be an array")
    else:
        for index, fact in enumerate(inputs):
            if not isinstance(fact, dict) or not isinstance(fact.get("path"), str):
                errors.append(f"input {index} fact is invalid")
                continue
            try:
                input_path = workspace.assert_formal_input(Path(fact["path"]))
            except (FileNotFoundError, OSError, ValueError) as error:
                errors.append(f"input {index} path is invalid: {error}")
                continue
            errors.extend(
                _recorded_file_errors(
                    workspace,
                    fact,
                    input_path,
                    f"input {index}",
                )
            )

    outputs = execution.get("outputs")
    retained_nonempty_output = False
    if not isinstance(outputs, list):
        errors.append("execution outputs must be an array")
    else:
        for index, fact in enumerate(outputs):
            if not isinstance(fact, dict) or not isinstance(fact.get("path"), str):
                errors.append(f"output {index} fact is invalid")
                continue
            output_path = Path(fact["path"]).resolve()
            if not output_path.is_relative_to(attempt.resolve()):
                errors.append(f"output {index} is outside its attempt")
                continue
            after = fact.get("after")
            if not isinstance(after, dict):
                errors.append(f"output {index} after fact is missing")
                continue
            if after.get("exists") is not True:
                if require_supporting:
                    errors.append(f"output {index} was not retained")
                continue
            if after.get("contains_possible_credential") is not False:
                errors.append(f"output {index} contains a possible credential")
            if after.get("artifact_retained") is not True:
                if require_supporting:
                    errors.append(f"output {index} is not marked as retained")
                continue
            if isinstance(after.get("size_bytes"), int) and after["size_bytes"] > 0:
                retained_nonempty_output = retained_nonempty_output or (
                    after.get("artifact_retained") is True
                    and after.get("contains_possible_credential") is False
                )
            errors.extend(
                _recorded_file_errors(
                    workspace,
                    after,
                    output_path,
                    f"output {index}",
                    require_recorded_path=False,
                    require_run_local=True,
                )
            )
    stdout_evidence = False
    if isinstance(capture, dict) and isinstance(capture.get("stdout"), dict):
        stdout = capture["stdout"]
        stdout_evidence = bool(
            stdout_as_evidence is True
            and isinstance(stdout.get("size_bytes"), int)
            and stdout["size_bytes"] > 0
            and stdout.get("redaction_applied") is False
        )
    if require_supporting and not (stdout_evidence or retained_nonempty_output):
        errors.append("attempt has no retained non-empty evidence channel")
    return tuple(errors)


def _schema_7_errors(
    workspace: ResearchWorkspace,
    attempt: Path,
    execution: dict[str, Any],
    environment: dict[str, Any] | None,
    *,
    schema_version: int,
    require_valid_metrics: bool,
) -> tuple[str, ...]:
    errors: list[str] = []
    metrics_contract_ok = execution.get("metrics_contract_ok")
    if type(metrics_contract_ok) is not bool:
        errors.append("execution metrics_contract_ok must be boolean")
    elif require_valid_metrics and metrics_contract_ok is not True:
        errors.append("execution metrics_contract_ok does not equal True")

    spec_fact = execution.get("experiment_spec")
    spec = None
    if not isinstance(spec_fact, dict):
        errors.append("execution experiment_spec is missing")
    else:
        snapshot = spec_fact.get("snapshot")
        errors.extend(
            _recorded_file_errors(
                workspace,
                snapshot,
                attempt / "spec.json",
                "experiment spec snapshot",
                require_run_local=True,
                require_nonempty=True,
            )
        )
        if not errors or not any("experiment spec snapshot" in item for item in errors):
            try:
                from crl_v3.falsification import (
                    experiment_spec_from_mapping,
                    validate_experiment_spec,
                )

                spec_data = _required_file(
                    attempt / "spec.json", within=workspace.workspace_path
                )
                _validate_utf8_lf(spec_data, "experiment spec snapshot")
                spec_value = json.loads(
                    spec_data.decode("utf-8"), parse_constant=_reject_json_constant
                )
                spec = experiment_spec_from_mapping(spec_value)
                validate_experiment_spec(
                    spec,
                    expected_run_id=workspace.workspace_path.name,
                    expected_version=workspace.version,
                )
                expected_source = (
                    workspace.experiment_path
                    / "specs"
                    / f"{spec.experiment_id}.json"
                ).relative_to(workspace.workspace_path).as_posix()
                if spec_fact.get("source_path") != expected_source:
                    errors.append("experiment spec source_path does not match its identity")
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
                errors.append(f"invalid experiment spec snapshot: {error}")

    metrics_fact = execution.get("metrics")
    if not isinstance(metrics_fact, dict):
        errors.append("execution metrics fact is missing")
    else:
        source_path = metrics_fact.get("source_path")
        if not isinstance(source_path, str):
            errors.append("metrics source_path is missing")
        else:
            try:
                metrics_source = workspace.workspace_path / safe_relative_path(
                    source_path
                )
                if not metrics_source.is_relative_to(attempt):
                    errors.append("metrics source_path is outside its attempt")
            except ValueError as error:
                errors.append(f"metrics source_path is invalid: {error}")
        validation_errors = metrics_fact.get("validation_errors")
        if not isinstance(validation_errors, list) or not all(
            isinstance(item, str) and item for item in validation_errors
        ):
            errors.append("metrics validation_errors fact is invalid")
        if "snapshot" not in metrics_fact:
            errors.append("metrics snapshot fact is missing")
        snapshot = metrics_fact.get("snapshot")
        if snapshot is None:
            if metrics_contract_ok is True:
                errors.append("metrics snapshot is missing despite a valid metrics contract")
            if not validation_errors:
                errors.append("missing metrics snapshot has no recorded validation error")
            if (attempt / "metrics.json").exists():
                errors.append("unrecorded metrics snapshot exists")
        else:
            if metrics_contract_ok is not True:
                errors.append("metrics snapshot exists despite an invalid metrics contract")
            before = len(errors)
            errors.extend(
                _recorded_file_errors(
                    workspace,
                    snapshot,
                    attempt / "metrics.json",
                    "metrics snapshot",
                    require_run_local=True,
                    require_nonempty=True,
                )
            )
            if len(errors) == before and spec is not None:
                try:
                    metrics_data = _required_file(
                        attempt / "metrics.json", within=workspace.workspace_path
                    )
                    validate_metrics_json_bytes(
                        metrics_data,
                        expected_experiment_id=spec.experiment_id,
                        primary_metric=spec.primary_metric,
                    )
                except (OSError, UnicodeError, ValueError) as error:
                    errors.append(f"invalid metrics snapshot: {error}")
    if environment is None:
        return tuple(errors)
    cpu_count = environment.get("cpu_count")
    if not (
        type(cpu_count) is int
        and cpu_count > 0
        or _is_unavailable_fact(cpu_count)
    ):
        errors.append("execution environment cpu_count fact is invalid")
    for name in ("git", "nvidia"):
        fact = environment.get(name)
        if not isinstance(fact, dict) or fact.get("status") not in {
            "available",
            "unavailable",
        }:
            errors.append(f"execution environment {name} fact is invalid")
        elif fact.get("status") == "unavailable" and not isinstance(
            fact.get("reason"), str
        ):
            errors.append(f"execution environment {name} unavailable reason is missing")
    if schema_version == 7:
        dependencies = environment.get("dependencies")
        if not isinstance(dependencies, dict):
            errors.append("execution environment dependencies fact is missing")
        else:
            errors.extend(
                _recorded_file_errors(
                    workspace,
                    dependencies.get("snapshot"),
                    attempt / "dependencies.txt",
                    "dependency snapshot",
                    require_run_local=True,
                    require_nonempty=True,
                )
            )
        modules = environment.get("runner_and_modules")
        errors.extend(_runner_module_errors(modules))
    else:
        errors.extend(
            _schema_8_provenance_errors(workspace, attempt, execution, environment)
        )
    declared = environment.get("declared_facts")
    if not isinstance(declared, dict) or not all(
        isinstance(name, str) and isinstance(value, str)
        for name, value in declared.items()
    ):
        errors.append("execution declared_facts are invalid")
    budget = execution.get("budget_facts")
    if not isinstance(budget, dict):
        errors.append("execution budget_facts are missing")
    elif budget.get("spec_budget_ceiling") is None or not isinstance(
        budget.get("warnings"), list
    ):
        errors.append("execution budget_facts are incomplete")
    elif spec is not None and budget.get("spec_budget_ceiling") != spec.budget_ceiling:
        errors.append("execution budget ceiling does not match the spec snapshot")
    return tuple(errors)


def _schema_8_provenance_errors(
    workspace: ResearchWorkspace,
    attempt: Path,
    execution: dict[str, Any],
    environment: dict[str, Any],
) -> tuple[str, ...]:
    errors: list[str] = []
    runner = environment.get("runner")
    runner_executable: dict[str, Any] | None = None
    if not isinstance(runner, dict):
        errors.append("execution runner provenance is missing")
    else:
        if not isinstance(runner.get("python"), str) or not runner["python"]:
            errors.append("execution runner Python identity is missing")
        executable = runner.get("executable")
        if not isinstance(executable, dict) or executable.get("status") != "bound":
            errors.append("execution runner executable identity is invalid")
        else:
            runner_executable = executable
            path = executable.get("path")
            if not isinstance(path, str):
                errors.append("execution runner executable path is missing")
            else:
                errors.extend(
                    _recorded_file_errors(
                        workspace,
                        executable,
                        Path(path),
                        "runner executable",
                    )
                )
        dependencies = runner.get("dependencies")
        if not isinstance(dependencies, dict):
            errors.append("execution runner dependencies fact is missing")
        else:
            if dependencies.get("scope") != "formal_runner_machine_environment":
                errors.append("execution runner dependency scope is invalid")
            if dependencies.get("subject_relationship") != "unbound":
                errors.append("execution subject dependency relationship is invalid")
            errors.extend(
                _recorded_file_errors(
                    workspace,
                    dependencies.get("snapshot"),
                    attempt / "dependencies.txt",
                    "runner dependency snapshot",
                    require_run_local=True,
                    require_nonempty=True,
                )
            )
        errors.extend(_runner_module_errors(runner.get("runner_and_modules")))

    subject = environment.get("subject")
    if not isinstance(subject, dict):
        errors.append("execution subject provenance is missing")
        return tuple(errors)
    argv = execution.get("argv")
    argv0 = argv[0] if isinstance(argv, list) and argv else None
    if not isinstance(argv0, str) or subject.get("argv0") != argv0:
        errors.append("execution subject argv0 does not match argv")
    executable = subject.get("executable")
    relationship = subject.get("runner_relationship")
    if not isinstance(executable, dict) or executable.get("status") not in {
        "bound",
        "unbound",
    }:
        errors.append("execution subject executable identity is invalid")
    elif executable.get("status") == "bound":
        if executable.get("resolution") not in {
            "absolute_path",
            "cwd_relative_path",
            "path_search",
        }:
            errors.append("execution subject executable resolution is invalid")
        path = executable.get("path")
        if not isinstance(path, str):
            errors.append("execution subject executable path is missing")
        else:
            errors.extend(
                _recorded_file_errors(
                    workspace,
                    executable,
                    Path(path),
                    "subject executable",
                )
            )
            if runner_executable is not None and isinstance(
                runner_executable.get("path"), str
            ):
                expected_relationship = (
                    "same_executable"
                    if Path(path).resolve()
                    == Path(runner_executable["path"]).resolve()
                    else "different_executable"
                )
                if relationship != expected_relationship:
                    errors.append("execution subject/runner relationship is invalid")
    else:
        if not isinstance(executable.get("reason"), str) or not executable["reason"]:
            errors.append("execution unbound subject executable reason is missing")
        if relationship != "unbound":
            errors.append("execution unbound subject relationship is invalid")
        if _explicit_subject_executable(execution) is not None:
            errors.append("execution explicit subject executable must be file-bound")

    runtime = subject.get("runtime")
    runner_python = runner.get("python") if isinstance(runner, dict) else None
    if relationship == "same_executable":
        if (
            not isinstance(runtime, dict)
            or runtime.get("status") != "bound_to_runner_python"
            or runtime.get("python") != runner_python
        ):
            errors.append("execution same-runtime subject identity is invalid")
    elif (
        not isinstance(runtime, dict)
        or runtime.get("status") != "unbound"
        or not isinstance(runtime.get("reason"), str)
        or not runtime["reason"]
    ):
        errors.append("execution unbound subject runtime fact is invalid")

    dependencies = subject.get("dependencies")
    if (
        not isinstance(dependencies, dict)
        or dependencies.get("status") != "unbound"
        or not isinstance(dependencies.get("reason"), str)
        or not dependencies["reason"]
    ):
        errors.append("execution subject dependencies must be explicitly unbound")
    subject_environment = subject.get("environment")
    if (
        not isinstance(subject_environment, dict)
        or subject_environment.get("status") != "partially_bound"
        or subject_environment.get("policy")
        != "sanitized_parent_with_explicit_sensitive_passthrough"
        or not isinstance(subject_environment.get("unbound_reason"), str)
        or not subject_environment["unbound_reason"]
    ):
        errors.append("execution subject environment binding fact is invalid")
    return tuple(errors)


def _runner_module_errors(modules: object) -> tuple[str, ...]:
    if not isinstance(modules, list) or not modules:
        return ("execution runner_and_modules must be a non-empty array",)
    errors = []
    for index, fact in enumerate(modules):
        if not isinstance(fact, dict) or not all(
            isinstance(fact.get(field), expected)
            for field, expected in (
                ("path", str),
                ("size_bytes", int),
                ("sha256", str),
            )
        ):
            errors.append(f"runner/module fact {index} is invalid")
    return tuple(errors)


def _explicit_subject_executable(execution: dict[str, Any]) -> Path | None:
    argv = execution.get("argv")
    cwd = execution.get("cwd")
    if not isinstance(argv, list) or not argv or not isinstance(argv[0], str):
        return None
    candidate = Path(argv[0])
    if not candidate.is_absolute() and candidate.parent == Path("."):
        return None
    if not candidate.is_absolute():
        if not isinstance(cwd, str):
            return None
        candidate = Path(cwd) / candidate
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    return resolved if resolved.is_file() else None


def _recorded_file_errors(
    workspace: ResearchWorkspace,
    fact: object,
    expected_path: Path,
    label: str,
    *,
    require_recorded_path: bool = True,
    require_nonempty: bool = False,
    require_run_local: bool = False,
) -> tuple[str, ...]:
    if not isinstance(fact, dict):
        return (f"{label} file fact is missing",)
    errors = []
    recorded_path = fact.get("path")
    if require_recorded_path and not isinstance(recorded_path, str):
        errors.append(f"{label} recorded path is missing")
    elif require_recorded_path and recorded_path is not None and (
        not isinstance(recorded_path, str)
        or Path(recorded_path).resolve() != expected_path.resolve()
    ):
        errors.append(f"{label} path does not match")
    lexical = Path(os.path.abspath(expected_path))
    if lexical.is_relative_to(workspace.workspace_path):
        try:
            expected_path = workspace.assert_read_target(lexical)
        except ValueError as error:
            return (f"{label} path is unsafe: {error}",)
        except FileNotFoundError:
            return (f"{label} file is missing",)
    else:
        if require_run_local:
            return (f"{label} file is outside the Run",)
        expected_path = lexical
    if not expected_path.is_file():
        errors.append(f"{label} file is missing")
        return tuple(errors)
    actual = file_fact(expected_path)
    if require_nonempty and actual["size_bytes"] <= 0:
        errors.append(f"{label} file is empty")
    if fact.get("size_bytes") != actual["size_bytes"]:
        errors.append(f"{label} size does not match")
    if fact.get("sha256") != actual["sha256"]:
        errors.append(f"{label} SHA-256 does not match")
    return tuple(errors)


def _attempt_id(value: str) -> str:
    text = str(value).strip()
    relative = safe_relative_path(text)
    if len(relative.parts) != 1 or not text:
        raise ValueError(f"attempt id must be one safe path component: {value!r}")
    return text


def _file_size_sha256(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def _nonempty_metric_text(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or "\r" in value
        or "\n" in value
    ):
        raise ValueError(f"{label} must be non-empty single-line text")
    return value


def _validate_resource_usage_value(name: str, value: object) -> None:
    if value is None or value == "unknown":
        return
    if name in {"tokens", "api_calls"}:
        if type(value) is not int or value < 0:
            raise ValueError(
                f"metrics resource_usage.{name} must be a non-negative integer, null, or unknown"
            )
        return
    if type(value) not in {int, float} or not math.isfinite(value) or value < 0:
        raise ValueError(
            f"metrics resource_usage.{name} must be a finite non-negative number, null, or unknown"
        )


def _validate_finite_numbers(value: object, label: str) -> None:
    if type(value) in {int, float}:
        if not math.isfinite(value):
            raise ValueError(f"{label} contains a non-finite number")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_finite_numbers(item, f"{label}[{index}]")
    elif isinstance(value, dict):
        for name, item in value.items():
            _validate_finite_numbers(item, f"{label}.{name}")


def _is_unavailable_fact(value: object) -> bool:
    return (
        isinstance(value, dict)
        and value.get("status") == "unavailable"
        and isinstance(value.get("reason"), str)
        and bool(value["reason"])
    )


def _read_required_markdown(
    workspace: ResearchWorkspace, path: Path
) -> bytes:
    try:
        data = _required_file(path, within=workspace.workspace_path)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"missing experiment document: {path}") from error
    if not data or not data.decode("utf-8", errors="ignore").strip():
        raise ValueError(f"empty experiment document: {path}")
    _validate_utf8_lf(data, str(path))
    return data
