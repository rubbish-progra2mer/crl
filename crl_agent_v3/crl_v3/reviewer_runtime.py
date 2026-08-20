from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .reviewer_protocol import (
    EVALUATOR_VERSION,
    ROLES,
    finalize_evaluation,
    load_evaluator,
    output_schema_path,
    reviewer_runtime_identity_errors,
    role_prompt,
    validate_reviewer_output,
)
from .workspace import ResearchWorkspace, _publish_once, _required_file, _sha256


BACKEND_VERSION = "codex_exec_jsonl_v1"
_FORBIDDEN_EVENT_TERMS = (
    "tool_call", "function_call", "command_execution", "shell", "mcp", "web_search",
    "browser", "computer_use", "delegate", "subagent", "file_read", "file_write",
)


def reviewer_canary(*, timeout_seconds: float = 900) -> dict[str, object]:
    packet = (
        "# REVIEWER BACKEND CANARY\n\n"
        "This is synthetic runtime validation, not scientific material. Give all SCI dimensions "
        "score 0 because no scientific evidence is provided. Do not use tools.\n"
    ).encode("utf-8")
    result = _invoke_role("SCI", packet, timeout_seconds=timeout_seconds)
    return {
        "backend": BACKEND_VERSION,
        "valid": result["valid"],
        "invalid_reasons": result["invalid_reasons"],
        "executable": result["runtime"]["executable"],
        "codex_version": result["runtime"]["codex_version"],
        "returncode": result["runtime"]["returncode"],
        "event_count": result["runtime"]["event_count"],
        "tool_event_count": len(result["runtime"]["forbidden_events"]),
        "output": result.get("output"),
        "events_bytes": result["events"],
        "stderr_bytes": result["stderr"],
        "raw_output_bytes": result["raw_output"],
    }


def run_evaluation(
    workspace: ResearchWorkspace,
    evaluation_id: str,
    *,
    timeout_seconds: float = 1800,
) -> dict[str, object]:
    workspace.assert_run_writable()
    root = workspace.review_path / "evaluations" / evaluation_id
    if not root.is_dir():
        raise FileNotFoundError(f"evaluation does not exist: {evaluation_id}")
    request_data = _required_file(root / "request.json", within=workspace.workspace_path)
    request = json.loads(request_data.decode("utf-8"))
    request_sha256 = _sha256(request_data)
    packet = _required_file(root / "packet.md", within=workspace.workspace_path)
    if request.get("packet_key") != _sha256(packet):
        raise ValueError("review packet identity changed before execution")
    evaluator = load_evaluator()
    if request.get("evaluator_definition_sha256") != evaluator["definition_sha256"]:
        raise ValueError("evaluator definition changed after packet creation")
    if request.get("backend") != BACKEND_VERSION:
        raise ValueError("evaluation request targets another backend")

    for role in ROLES:
        role_root = workspace.assert_write_target(root / role)
        if role_root.exists():
            raise FileExistsError(f"reviewer role output already exists: {role}")
        role_root.mkdir()
        result = _invoke_role(role, packet, timeout_seconds=timeout_seconds)
        _write_binary_once(role_root / "events.jsonl", result["events"])
        _write_binary_once(role_root / "stderr.bin", result["stderr"])
        _write_binary_once(role_root / "raw_output.json", result["raw_output"])
        envelope = {
            "schema_version": 1,
            "reviewer_role": role,
            "evaluation_id": evaluation_id,
            "request_sha256": request_sha256,
            "measurement_key": request["measurement_key"],
            "packet_key": request["packet_key"],
            "evaluator_version": EVALUATOR_VERSION,
            "evaluator_definition_sha256": evaluator["definition_sha256"],
            "valid": result["valid"],
            "invalid_reasons": result["invalid_reasons"],
            "runtime": result["runtime"],
            "events_sha256": _sha256(result["events"]),
            "stderr_sha256": _sha256(result["stderr"]),
            "raw_output_sha256": _sha256(result["raw_output"]),
            "output": result.get("output"),
        }
        _publish_once(
            role_root / "report.json",
            _json_bytes(envelope),
            within=workspace.workspace_path,
        )
    return finalize_evaluation(workspace, evaluation_id)


def _invoke_role(
    role: str, packet: bytes, *, timeout_seconds: float
) -> dict[str, object]:
    evaluator = load_evaluator()
    executable = _codex_executable()
    version = _codex_version(executable)
    prompt = (
        role_prompt(role)
        + b"\n<REVIEW_PACKET>\n"
        + packet
        + b"</REVIEW_PACKET>\n\n"
        + _output_reminder(role).encode("utf-8")
    )
    with tempfile.TemporaryDirectory(prefix="crl-fixed-reviewer-") as temporary_text:
        temporary = Path(temporary_text)
        clean_home = temporary / "codex-home"
        clean_home.mkdir()
        shutil.copyfile(_saved_auth_path(), clean_home / "auth.json")
        isolated_workspace = temporary / "empty-workspace"
        isolated_workspace.mkdir()
        final_output = temporary / "final-output.json"
        arguments = [
            "exec",
            "--model", "gpt-5.6-sol",
            "--sandbox", "read-only",
            "--ephemeral",
            "--json",
            "--output-schema", str(output_schema_path(role)),
            "--output-last-message", str(final_output),
            "--skip-git-repo-check",
            "-C", str(isolated_workspace),
            "-c", "model_reasoning_effort=xhigh",
            "-c", "service_tier=fast",
            "-c", "mcp_servers={}",
            "-",
        ]
        command = _host_command(executable, arguments)
        try:
            completed = subprocess.run(
                command,
                input=prompt,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=_minimal_environment(codex_home=clean_home),
                timeout=timeout_seconds,
                check=False,
            )
            events = completed.stdout
            stderr = completed.stderr
            returncode = completed.returncode
            timed_out = False
        except subprocess.TimeoutExpired as caught:
            events = caught.stdout or b""
            stderr = caught.stderr or b""
            returncode = None
            timed_out = True
        raw_output = final_output.read_bytes() if final_output.is_file() else b""
    parsed_events, event_errors = _parse_events(events)
    forbidden = [event for event in parsed_events if _event_is_forbidden(event)]
    invalid = list(event_errors)
    if timed_out:
        invalid.append("reviewer process timed out")
    if returncode != 0:
        invalid.append(f"reviewer process returncode is {returncode}")
    if forbidden:
        invalid.append("reviewer emitted a forbidden tool or external-access event")
    output = None
    try:
        output = json.loads(raw_output.decode("utf-8"))
        validate_reviewer_output(role, output)
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        invalid.append(f"invalid structured reviewer output: {error}")
    runtime = {
        "backend": BACKEND_VERSION,
        "executable": str(executable),
        "codex_version": version,
        "requested_model": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
        "sandbox": "read-only",
        "ephemeral": True,
        "network_requested": False,
        "returncode": returncode,
        "timed_out": timed_out,
        "event_count": len(parsed_events),
        "forbidden_events": forbidden,
    }
    invalid.extend(
        reviewer_runtime_identity_errors(runtime, evaluator["manifest"])
    )
    return {
        "valid": not invalid,
        "invalid_reasons": sorted(set(invalid)),
        "events": events,
        "stderr": stderr,
        "raw_output": raw_output,
        "output": output,
        "runtime": runtime,
    }


def _output_reminder(role: str) -> str:
    dimensions = {
        "SCI": "problem_value, prior_separation, mechanism_clarity, scientific_specificity, claim_calibration",
        "EMP": "experimental_validity, baseline_fairness, measurement_reliability, robustness_falsification, result_strength",
        "ADV": "reproducibility_traceability, confound_leakage_control, boundary_generalization, adversarial_survivability, evidence_auditability",
    }[role]
    diagnostics = {
        "SCI": "strongest_scientific_contribution, biggest_scientific_risk, most_dangerous_prior_collision, mechanism_falsifier",
        "EMP": "strongest_empirical_evidence, biggest_empirical_threat, baseline_confound, killer_experiment, missing_validation",
        "ADV": "most_fatal_failure_mode, reproduction_breakpoint, hidden_assumption, boundary_warning, best_stress_test",
    }[role]
    return (
        "Return only JSON. Set review_protocol=CRL-IR-1.0, reviewer_role=" + role
        + ", evaluator_version=CRL-EVAL-1.0, model_identity=gpt-5.6-sol, reasoning_effort=xhigh. "
        + "Use exactly these score and reason keys: " + dimensions + ". "
        + "Use exactly these diagnostics keys: " + diagnostics + ". Also include critical_risk, confidence, and free_review.\n"
    )


def _parse_events(data: bytes) -> tuple[list[dict[str, Any]], list[str]]:
    events = []
    errors = []
    for number, line in enumerate(data.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except (UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid JSONL event at line {number}: {error}")
            continue
        if not isinstance(value, dict):
            errors.append(f"JSONL event at line {number} is not an object")
            continue
        events.append(value)
    if not events:
        errors.append("reviewer produced no JSONL events")
    return events, errors


def _event_is_forbidden(event: dict[str, Any]) -> bool:
    def visit(value: object, key: str | None = None) -> bool:
        if isinstance(value, dict):
            return any(visit(item, str(name)) for name, item in value.items())
        if isinstance(value, list):
            return any(visit(item, key) for item in value)
        if isinstance(value, str) and key in {"type", "tool", "tool_name", "name", "method"}:
            folded = value.casefold()
            return any(term in folded for term in _FORBIDDEN_EVENT_TERMS)
        return False
    return visit(event)


def _codex_executable() -> Path:
    fixed = Path(__file__).resolve().parents[2] / "runtimes" / "codex-cli" / "0.147.0" / "codex.cmd"
    if not fixed.is_file():
        raise FileNotFoundError(f"fixed Codex Reviewer runtime is unavailable: {fixed}")
    return fixed.resolve()


def _codex_version(executable: Path) -> str:
    completed = subprocess.run(
        _host_command(executable, ["--version"]),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_minimal_environment(),
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        return "unavailable"
    return completed.stdout.decode("utf-8", errors="replace").strip()


def _host_command(executable: Path, arguments: list[str]) -> list[str]:
    if os.name == "nt" and executable.suffix.casefold() in {".cmd", ".bat"}:
        command_line = subprocess.list2cmdline([str(executable), *arguments])
        return [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/s", "/c", command_line]
    return [str(executable), *arguments]


def _saved_auth_path() -> Path:
    configured = os.environ.get("CODEX_HOME")
    root = Path(configured) if configured else Path(os.environ["USERPROFILE"]) / ".codex"
    path = root / "auth.json"
    if not path.is_file():
        raise FileNotFoundError("saved Codex CLI login is unavailable")
    return path


def _minimal_environment(*, codex_home: Path | None = None) -> dict[str, str]:
    allowed = {
        "PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "USERPROFILE",
        "APPDATA", "LOCALAPPDATA", "TEMP", "TMP", "CODEX_HOME", "LANG",
        "SSL_CERT_FILE", "SSL_CERT_DIR", "ALLUSERSPROFILE", "PROGRAMDATA",
        "PROGRAMFILES", "PROGRAMFILES(X86)", "PROGRAMW6432", "SYSTEMDRIVE",
        "HOMEDRIVE", "HOMEPATH", "USERNAME", "USERDOMAIN", "COMPUTERNAME", "OS",
    }
    environment = {
        name: value
        for name, value in os.environ.items()
        if name.upper() in allowed and value
    }
    if codex_home is not None:
        environment["CODEX_HOME"] = str(codex_home)
    return environment


def _write_binary_once(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
