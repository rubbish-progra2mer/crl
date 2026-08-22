from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from crl_v3.experiment import (
    experiment_material_errors,
    supporting_attempt_execution_sha256,
)
from crl_v3.review import (
    list_reviewer_reports,
    read_review_request,
    review_material_errors,
)
from crl_v3.workspace import (
    PERMANENT_TERMINAL_FILE_STATUS,
    RESUMABLE_STATUSES,
    ResearchWorkspace,
    _atomic_write_text,
    _assert_read_target,
    _publish_once,
    _required_content,
    _required_file,
    _sha256,
    _single_named_field,
    _status_value,
)


@dataclass(frozen=True, slots=True)
class DecisionDocument:
    path: str
    version: str
    content: str
    request_sha256: str
    report_sha256s: tuple[str, str, str]
    sha256: str


@dataclass(frozen=True, slots=True)
class TerminalDocument:
    path: str
    status: str
    version: str
    content: str
    sha256: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SecretScan:
    environment_secret: bool
    heuristic_pattern: bool

    @property
    def contains_possible_credential(self) -> bool:
        return self.environment_secret or self.heuristic_pattern


@dataclass(frozen=True, slots=True)
class _RunSecretFinding:
    relative: Path
    unsafe: bool
    scan: SecretScan | None
    third_party: bool
    raw_search_payload: bool
    source_code: bool
    text_secret_target: bool
    high_confidence_path: bool
    private_key: bool


_DECISION_SCHEMA_VERSION = 2
_DELIVERY_SCHEMA_VERSION = 3
_DECISION_META_PREFIX = "<!-- CRL_DECISION_META "
_TERMINAL_META_PREFIX = "<!-- CRL_TERMINAL_META "
_META_SUFFIX = " -->"
_SECRET_PATTERNS = (
    re.compile(rb"(?i)(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*[^\s]{8,4096}"),
    re.compile(rb"\bsk-[A-Za-z0-9_-]{12,4096}\b"),
    re.compile(rb"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{12,4096}={0,2}\b"),
)
_PRIVATE_KEY_PATTERN = re.compile(
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)
_HIGH_CONFIDENCE_SECRET_NAME = re.compile(
    r"(?i)(?:^credentials?(?:\.(?:json|ini|yaml|yml|txt))?$|"
    r"credential[_-]?store|token[_-]?dump|auth[_-]?cache|"
    r"session[_-]?cache|id_rsa|id_ed25519|\.pfx$|\.p12$)"
)
_ENVIRONMENT_VARIABLE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_SENSITIVE_ENVIRONMENT_NAME_TOKENS = (
    "API_KEY",
    "TOKEN",
    "SECRET",
    "PASSWORD",
    "CREDENTIAL",
)
_THIRD_PARTY_PATH_PARTS = {
    "external",
    "vendor",
    "third_party",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "site-packages",
}
_TEXT_SECRET_SUFFIXES = {
    ".cfg",
    ".csv",
    ".html",
    ".htm",
    ".ini",
    ".json",
    ".jsonl",
    ".log",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
_VERSIONED_DELIVERY_PATTERN = re.compile(r"^DELIVERY_(v\d{3,})\.md$")
_VERSIONED_NO_DELIVERY_PATTERN = re.compile(r"^NO_DELIVERY_(v\d{3,})\.md$")
_SECRET_WARNING_REPRESENTATIVE_LIMIT = 5


def write_review_decision(
    workspace: ResearchWorkspace,
    content: str,
    *,
    measurement_key: str | None = None,
) -> DecisionDocument:
    if workspace.contract_version == "3":
        from crl_v3.reviewer_decision import write_fixed_review_decision

        return write_fixed_review_decision(
            workspace, content, measurement_key=measurement_key
        )  # type: ignore[return-value]
    workspace.assert_run_writable()
    errors = review_material_errors(workspace)
    if errors:
        raise ValueError("review materials are incomplete:\n- " + "\n- ".join(errors))
    request = read_review_request(workspace)
    reports = list_reviewer_reports(workspace)
    body = _required_content(content).rstrip()
    metadata = _json_metadata(
        {
            "schema_version": _DECISION_SCHEMA_VERSION,
            "version": workspace.version,
            "request_sha256": request.sha256,
            "report_sha256s": {
                str(report.reviewer_number): report.sha256 for report in reports
            },
        }
    )
    rendered = "\n".join(
        (
            "# Main AI Decision After Review",
            f"{_DECISION_META_PREFIX}{metadata}{_META_SUFFIX}",
            "",
            body,
            "",
        )
    )
    path = workspace.document_path("decision")
    _metadata_line(
        rendered,
        _DECISION_META_PREFIX,
        {"schema_version", "version", "request_sha256", "report_sha256s"},
    )
    workspace.assert_write_target(path)
    _publish_once(path, rendered.encode("utf-8"), within=workspace.workspace_path)
    return read_review_decision(workspace)


def read_review_decision(workspace: ResearchWorkspace) -> DecisionDocument:
    if workspace.contract_version == "3":
        from crl_v3.reviewer_decision import read_fixed_review_decision

        return read_fixed_review_decision(workspace)  # type: ignore[return-value]
    path = workspace.document_path("decision")
    data = _required_file(path, within=workspace.workspace_path)
    content = data.decode("utf-8")
    metadata = _metadata_line(
        content,
        _DECISION_META_PREFIX,
        {"schema_version", "version", "request_sha256", "report_sha256s"},
    )
    if metadata.get("schema_version") != _DECISION_SCHEMA_VERSION:
        raise ValueError("unsupported review decision schema version")
    version = _metadata_string(metadata, "version")
    if version != workspace.version:
        raise ValueError("review decision version does not match workspace version")
    request_sha256 = _metadata_string(metadata, "request_sha256")
    request = read_review_request(workspace)
    if request_sha256 != request.sha256:
        raise ValueError("review decision is bound to a different review request")
    reports = list_reviewer_reports(workspace)
    report_sha256s_value = metadata.get("report_sha256s")
    if not isinstance(report_sha256s_value, dict) or set(report_sha256s_value) != {
        "1",
        "2",
        "3",
    }:
        raise ValueError("review decision report SHA-256 map is invalid")
    report_sha256s = tuple(
        _mapping_digest(report_sha256s_value, str(number)) for number in (1, 2, 3)
    )
    actual_report_sha256s = tuple(report.sha256 for report in reports)
    if report_sha256s != actual_report_sha256s:
        raise ValueError("review decision is bound to different reviewer reports")
    return DecisionDocument(
        str(path),
        version,
        content,
        request_sha256,
        report_sha256s,
        _sha256(data),
    )


def delivery_material_errors(
    workspace: ResearchWorkspace,
    supporting_attempt_ids: Iterable[str] | None = None,
) -> tuple[str, ...]:
    if workspace.contract_version == "3":
        from crl_v3.reviewer_decision import fixed_delivery_errors

        return fixed_delivery_errors(workspace, supporting_attempt_ids)
    errors: list[str] = []
    try:
        seed_data = _required_file(
            workspace.seed_path, within=workspace.workspace_path
        )
        if not seed_data.decode("utf-8").strip():
            raise ValueError(f"empty final Seed: {workspace.seed_path.name}")
    except (FileNotFoundError, UnicodeError, ValueError) as error:
        errors.append(f"missing or invalid final Seed: {error}")
    if supporting_attempt_ids is None:
        errors.append("explicit supporting attempt ids are required for Delivery")
    else:
        errors.extend(experiment_material_errors(workspace, supporting_attempt_ids))
    errors.extend(review_material_errors(workspace))
    try:
        read_review_decision(workspace)
    except (FileNotFoundError, UnicodeDecodeError, ValueError) as error:
        errors.append(str(error))
    errors.extend(secret_scan_errors(workspace.workspace_path))
    try:
        history = _conclusion_history(workspace)
        if history and int(workspace.version[1:]) <= int(history[-1].version[1:]):
            errors.append(
                "new Delivery requires a scientific version newer than prior conclusion history"
            )
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"invalid prior conclusion history: {error}")
    if (workspace.workspace_path / "TERMINATED_BY_USER.md").exists():
        errors.append("TERMINATED_BY_USER.md already exists")
    return tuple(dict.fromkeys(errors))


def write_delivery(
    workspace: ResearchWorkspace,
    *,
    supporting_attempt_ids: Iterable[str],
) -> TerminalDocument:
    if workspace.contract_version == "3":
        from crl_v3.reviewer_decision import write_fixed_delivery

        return write_fixed_delivery(
            workspace, supporting_attempt_ids=supporting_attempt_ids
        )
    workspace.assert_run_writable()
    attempt_ids = tuple(dict.fromkeys(str(item).strip() for item in supporting_attempt_ids))
    errors = delivery_material_errors(workspace, attempt_ids)
    if errors:
        raise ValueError("delivery is mechanically incomplete:\n- " + "\n- ".join(errors))
    request = read_review_request(workspace)
    decision = read_review_decision(workspace)
    seed_data = _required_file(
        workspace.seed_path, within=workspace.workspace_path
    )
    seed_relative = workspace.seed_path.relative_to(workspace.workspace_path).as_posix()
    attempts = [
        {
            "attempt_id": attempt_id,
            "execution_sha256": supporting_attempt_execution_sha256(
                workspace, attempt_id
            ),
        }
        for attempt_id in attempt_ids
    ]
    metadata = _json_metadata(
        {
            "schema_version": _DELIVERY_SCHEMA_VERSION,
            "status": "DELIVERED",
            "version": workspace.version,
            "seed_path": seed_relative,
            "seed_sha256": _sha256(seed_data),
            "request_sha256": request.sha256,
            "decision_sha256": decision.sha256,
            "supporting_attempts": attempts,
        }
    )
    rendered = "\n".join(
        (
            "# CRL Research Seed Delivery",
            f"{_TERMINAL_META_PREFIX}{metadata}{_META_SUFFIX}",
            "",
            f"- Final version: {workspace.version}",
            f"- Seed: {seed_relative}",
            f"- Seed SHA-256: {_sha256(seed_data)}",
            f"- Review request SHA-256: {request.sha256}",
            f"- Decision SHA-256: {decision.sha256}",
            "- Supporting attempts:",
            *(
                f"  - {item['attempt_id']} (execution SHA-256: "
                f"{item['execution_sha256']})"
                for item in attempts
            ),
            "",
            "本轮已交付。正式科研内容以所引用 Seed 的确切字节为准。",
            "",
        )
    )
    data = rendered.encode("utf-8")
    _raise_if_secret_bytes(data, "Delivery record")
    _metadata_line(
        rendered,
        _TERMINAL_META_PREFIX,
        {
            "schema_version",
            "status",
            "version",
            "seed_path",
            "seed_sha256",
            "request_sha256",
            "decision_sha256",
            "supporting_attempts",
        },
    )
    prior_deliveries = read_delivery_history(workspace)
    path = (
        workspace.workspace_path / "DELIVERY.md"
        if not prior_deliveries
        else workspace.workspace_path / f"DELIVERY_{workspace.version}.md"
    )
    workspace.assert_write_target(path)
    _commit_terminal(
        workspace,
        path,
        data,
        status="DELIVERED",
        version=workspace.version,
        event="DELIVERY_PUBLISHED",
        event_at=_utc_now(),
    )
    return read_delivery(workspace, path=path)


def read_delivery(
    workspace: ResearchWorkspace, *, path: str | Path | None = None
) -> TerminalDocument:
    if workspace.contract_version == "3":
        from crl_v3.reviewer_decision import read_fixed_delivery

        return read_fixed_delivery(workspace, path=path)
    if path is None:
        versioned = workspace.workspace_path / f"DELIVERY_{workspace.version}.md"
        path = (
            versioned
            if versioned.is_file()
            else workspace.workspace_path / "DELIVERY.md"
        )
    path = Path(path)
    data = _required_file(path, within=workspace.workspace_path)
    content = data.decode("utf-8")
    metadata = _metadata_line(
        content,
        _TERMINAL_META_PREFIX,
        {
            "schema_version",
            "status",
            "version",
            "seed_path",
            "seed_sha256",
            "request_sha256",
            "decision_sha256",
            "supporting_attempts",
        },
    )
    if metadata.get("schema_version") != _DELIVERY_SCHEMA_VERSION:
        raise ValueError("unsupported Delivery schema version")
    status = _metadata_string(metadata, "status")
    version = _metadata_string(metadata, "version")
    if status != "DELIVERED" or version != workspace.version:
        raise ValueError("Delivery status or version does not match the workspace")
    seed_path = _metadata_string(metadata, "seed_path")
    expected_seed_path = workspace.seed_path.relative_to(workspace.workspace_path).as_posix()
    if seed_path != expected_seed_path:
        raise ValueError("Delivery points to a different final Seed")
    seed_sha256 = _metadata_digest(metadata, "seed_sha256")
    if _sha256(
        _required_file(workspace.seed_path, within=workspace.workspace_path)
    ) != seed_sha256:
        raise ValueError("Delivery Seed SHA-256 no longer matches")
    request_sha256 = _metadata_digest(metadata, "request_sha256")
    request = read_review_request(workspace)
    if request.sha256 != request_sha256:
        raise ValueError("Delivery review request SHA-256 no longer matches")
    decision_sha256 = _metadata_digest(metadata, "decision_sha256")
    decision = read_review_decision(workspace)
    if decision.sha256 != decision_sha256:
        raise ValueError("Delivery decision SHA-256 no longer matches")
    attempts_value = metadata.get("supporting_attempts")
    if not isinstance(attempts_value, list) or not attempts_value:
        raise ValueError("Delivery supporting attempts are invalid")
    attempt_ids: list[str] = []
    for index, item in enumerate(attempts_value):
        if not isinstance(item, dict) or set(item) != {
            "attempt_id",
            "execution_sha256",
        }:
            raise ValueError(
                f"Delivery supporting attempt {index} does not match the schema"
            )
        attempt_id = item.get("attempt_id")
        execution_sha256 = item.get("execution_sha256")
        if not isinstance(attempt_id, str) or not attempt_id.strip():
            raise ValueError(f"Delivery supporting attempt {index} id is invalid")
        if (
            not isinstance(execution_sha256, str)
            or re.fullmatch(r"[0-9a-f]{64}", execution_sha256) is None
        ):
            raise ValueError(
                f"Delivery supporting attempt {index} execution SHA-256 is invalid"
            )
        attempt_id = attempt_id.strip()
        if attempt_id in attempt_ids:
            raise ValueError("Delivery supporting attempt ids contain duplicates")
        attempt_ids.append(attempt_id)
        try:
            current_sha256 = supporting_attempt_execution_sha256(
                workspace, attempt_id
            )
        except (FileNotFoundError, OSError, UnicodeError, ValueError) as error:
            raise ValueError(
                f"Delivery supporting attempt {attempt_id} is no longer valid: {error}"
            ) from error
        if current_sha256 != execution_sha256:
            raise ValueError(
                "Delivery supporting attempt execution SHA-256 no longer matches: "
                + attempt_id
            )
    return TerminalDocument(str(path), status, version, content, _sha256(data))


def delivery_record_paths(run_root: Path) -> tuple[Path, ...]:
    root = run_root / "DELIVERY.md"
    versioned = sorted(
        (
            path
            for path in run_root.glob("DELIVERY_v*.md")
            if _VERSIONED_DELIVERY_PATTERN.fullmatch(path.name)
        ),
        key=lambda path: int(
            _VERSIONED_DELIVERY_PATTERN.fullmatch(path.name).group(1)[1:]
        ),
    )
    return ((root,) if root.is_file() else ()) + tuple(versioned)


def read_delivery_history(
    workspace: ResearchWorkspace,
) -> tuple[TerminalDocument, ...]:
    paths = delivery_record_paths(workspace.workspace_path)
    if not paths:
        return ()
    if paths[0].name != "DELIVERY.md":
        raise ValueError("versioned Delivery records require an existing DELIVERY.md root")
    records: list[TerminalDocument] = []
    versions: set[str] = set()
    previous_number = -1
    for path in paths:
        try:
            header = read_terminal(path, expected_status="DELIVERED")
            if header.version in versions:
                raise ValueError(f"duplicate Delivery version: {header.version}")
            number = int(header.version[1:])
            if number <= previous_number:
                raise ValueError("Delivery versions are not strictly increasing")
            if path.name != "DELIVERY.md":
                match = _VERSIONED_DELIVERY_PATTERN.fullmatch(path.name)
                assert match is not None
                if match.group(1) != header.version:
                    raise ValueError(
                        f"Delivery filename and metadata version disagree: {path.name}"
                    )
            version_workspace = ResearchWorkspace(
                workspace.workspace_path,
                version=header.version,
                product_root=workspace.product_root,
            )
            record = read_delivery(version_workspace, path=path)
        except ValueError as error:
            raise ValueError(
                f"invalid Delivery conclusion artifact {path}: {error}"
            ) from error
        records.append(record)
        versions.add(header.version)
        previous_number = number
    return tuple(records)


def no_delivery_record_paths(run_root: Path) -> tuple[Path, ...]:
    root = run_root / "NO_DELIVERY.md"
    versioned = sorted(
        (
            path
            for path in run_root.glob("NO_DELIVERY_v*.md")
            if _VERSIONED_NO_DELIVERY_PATTERN.fullmatch(path.name)
        ),
        key=lambda path: int(
            _VERSIONED_NO_DELIVERY_PATTERN.fullmatch(path.name).group(1)[1:]
        ),
    )
    return ((root,) if root.is_file() else ()) + tuple(versioned)


def read_no_delivery_history(
    workspace: ResearchWorkspace,
) -> tuple[TerminalDocument, ...]:
    paths = no_delivery_record_paths(workspace.workspace_path)
    if not paths:
        return ()
    if paths[0].name != "NO_DELIVERY.md":
        raise ValueError(
            "versioned No-Delivery records require an existing NO_DELIVERY.md root"
        )
    records: list[TerminalDocument] = []
    versions: set[str] = set()
    previous_number = -1
    for path in paths:
        try:
            record = read_terminal(path, expected_status="CONCLUDED_NO_DELIVERY")
            if record.version in versions:
                raise ValueError(f"duplicate No-Delivery version: {record.version}")
            number = int(record.version[1:])
            if number <= previous_number:
                raise ValueError("No-Delivery versions are not strictly increasing")
            if path.name != "NO_DELIVERY.md":
                match = _VERSIONED_NO_DELIVERY_PATTERN.fullmatch(path.name)
                assert match is not None
                if match.group(1) != record.version:
                    raise ValueError(
                        "No-Delivery filename and metadata version disagree: "
                        + path.name
                    )
        except ValueError as error:
            raise ValueError(
                f"invalid No-Delivery conclusion artifact {path}: {error}"
            ) from error
        records.append(record)
        versions.add(record.version)
        previous_number = number
    return tuple(records)


def write_no_delivery(
    workspace: ResearchWorkspace, content: str
) -> TerminalDocument:
    workspace.assert_run_writable()
    _assert_no_delivery_mode(workspace)
    for terminal in PERMANENT_TERMINAL_FILE_STATUS:
        if (workspace.workspace_path / terminal).exists():
            raise FileExistsError(f"{terminal} already exists")
    history = _conclusion_history(workspace)
    if history and int(workspace.version[1:]) <= int(history[-1].version[1:]):
        raise ValueError(
            "new No-Delivery requires a scientific version newer than prior conclusion history"
        )
    prior_no_delivery = read_no_delivery_history(workspace)
    secret_findings = _scan_run_secret_findings(workspace.workspace_path)
    existing_secret_errors = _secret_scan_errors_from_findings(
        secret_findings, for_no_delivery=True
    )
    if existing_secret_errors:
        raise ValueError("Run contains possible credentials:\n- " + "\n- ".join(existing_secret_errors))
    rendered = _render_terminal(
        "# CRL No-Go Conclusion",
        "CONCLUDED_NO_DELIVERY",
        workspace.version,
        content,
    )
    data = rendered.encode("utf-8")
    path = (
        workspace.workspace_path / "NO_DELIVERY.md"
        if not prior_no_delivery
        else workspace.workspace_path / f"NO_DELIVERY_{workspace.version}.md"
    )
    _raise_if_secret_bytes(data, path.name)
    _metadata_line(rendered, _TERMINAL_META_PREFIX, {"status", "version"})
    workspace.assert_write_target(path)
    warnings = _secret_scan_warnings_from_findings(secret_findings)
    _commit_terminal(
        workspace,
        path,
        data,
        status="CONCLUDED_NO_DELIVERY",
        version=workspace.version,
        event="NO_DELIVERY_CONCLUDED",
        event_at=_utc_now(),
    )
    return read_terminal(
        path, "CONCLUDED_NO_DELIVERY", workspace.version, warnings=warnings
    )


def _assert_no_delivery_mode(workspace: ResearchWorkspace) -> None:
    charter_path = workspace.workspace_path / "RUN_CHARTER.md"
    status_path = workspace.workspace_path / "RUN_STATUS.md"
    charter_mode = _single_named_field(
        charter_path,
        "MODE",
        label="RUN_CHARTER.md",
        within=workspace.workspace_path,
    )
    status_mode = _single_named_field(
        status_path,
        "MODE",
        label="RUN_STATUS.md",
        within=workspace.workspace_path,
    )
    if charter_mode != status_mode:
        raise ValueError(
            "Run MODE identity differs between RUN_CHARTER.md and RUN_STATUS.md"
        )
    if charter_mode != "DIRECTED" or status_mode != "DIRECTED":
        raise ValueError(
            "No-Delivery requires MODE: DIRECTED in both RUN_CHARTER.md "
            f"and RUN_STATUS.md; found MODE: {charter_mode}"
        )
    _single_named_field(
        charter_path,
        "DEFAULT_DOMAIN",
        label="RUN_CHARTER.md",
        within=workspace.workspace_path,
    )


def write_user_termination(
    workspace: ResearchWorkspace,
    *,
    note: str = "",
    terminated_at: str,
) -> TerminalDocument:
    status = _status_value(workspace.workspace_path / "RUN_STATUS.md")
    if status not in RESUMABLE_STATUSES:
        raise ValueError(f"Run cannot be terminated from status {status}")
    for terminal in PERMANENT_TERMINAL_FILE_STATUS:
        if (workspace.workspace_path / terminal).exists():
            raise FileExistsError(f"terminal Run already contains {terminal}")
    history = _conclusion_history(workspace)
    if history and int(workspace.version[1:]) <= int(history[-1].version[1:]):
        raise ValueError(
            "user termination requires a scientific version newer than prior "
            "conclusion history"
        )
    existing_secret_errors = secret_scan_errors(
        workspace.workspace_path, for_no_delivery=True
    )
    if existing_secret_errors:
        raise ValueError("Run contains possible credentials:\n- " + "\n- ".join(existing_secret_errors))
    body_lines = [
        "用户明确要求永久终止本轮 Run。",
        "",
        f"- Terminated at: {terminated_at}",
        f"- Final version: {workspace.version}",
    ]
    if note.strip():
        body_lines.extend((f"- Note: {note.strip()}",))
    rendered = _render_terminal(
        "# CRL Run Terminated By User",
        "TERMINATED_BY_USER",
        workspace.version,
        "\n".join(body_lines),
    )
    data = rendered.encode("utf-8")
    _raise_if_secret_bytes(data, "TERMINATED_BY_USER.md")
    path = workspace.workspace_path / "TERMINATED_BY_USER.md"
    workspace.assert_write_target(path)
    _commit_terminal(
        workspace,
        path,
        data,
        status="TERMINATED_BY_USER",
        version=workspace.version,
        event="RUN_TERMINATED_BY_USER",
        event_at=terminated_at,
    )
    return read_terminal(path, "TERMINATED_BY_USER", workspace.version)


def _conclusion_history(
    workspace: ResearchWorkspace,
) -> tuple[TerminalDocument, ...]:
    records = (*read_delivery_history(workspace), *read_no_delivery_history(workspace))
    by_version: dict[str, TerminalDocument] = {}
    for record in records:
        if record.version in by_version:
            raise ValueError(
                "multiple scientific conclusions exist for version " + record.version
            )
        by_version[record.version] = record
    return tuple(sorted(records, key=lambda item: int(item.version[1:])))


def read_terminal(
    path: Path,
    expected_status: str | None = None,
    expected_version: str | None = None,
    *,
    warnings: tuple[str, ...] = (),
) -> TerminalDocument:
    data = _required_file(path, within=path.parent)
    content = data.decode("utf-8")
    if path.name == "DELIVERY.md" or _VERSIONED_DELIVERY_PATTERN.fullmatch(path.name):
        schema_version = _terminal_schema_version(content)
        fields = (
            {
                "schema_version",
                "status",
                "version",
                "seed_path",
                "seed_sha256",
                "decision_sha256",
                "implementation_key",
                "packet_key",
                "measurement_key",
                "canonical_evaluation_id",
                "aggregate_sha256",
                "implementation_manifest_sha256",
                "evidence_inventory_sha256",
                "supporting_attempts",
            }
            if schema_version == 4
            else {
            "schema_version",
            "status",
            "version",
            "seed_path",
            "seed_sha256",
            "request_sha256",
            "decision_sha256",
            "supporting_attempts",
            }
        )
    else:
        fields = {"status", "version"}
    metadata = _metadata_line(content, _TERMINAL_META_PREFIX, fields)
    status = _metadata_string(metadata, "status")
    version = _metadata_string(metadata, "version")
    if expected_status is not None and status != expected_status:
        raise ValueError(f"terminal status mismatch: {status}")
    if expected_version is not None and version != expected_version:
        raise ValueError(f"terminal version mismatch: {version}")
    return TerminalDocument(
        str(path), status, version, content, _sha256(data), warnings
    )


def _terminal_schema_version(content: str) -> object:
    lines = [
        line
        for line in content.splitlines()[:3]
        if line.startswith(_TERMINAL_META_PREFIX) and line.endswith(_META_SUFFIX)
    ]
    if len(lines) != 1:
        raise ValueError("missing or duplicate bounded terminal metadata")
    value = json.loads(
        lines[0][len(_TERMINAL_META_PREFIX) : -len(_META_SUFFIX)]
    )
    if not isinstance(value, dict):
        raise ValueError("terminal metadata must be an object")
    return value.get("schema_version")


def _render_terminal(
    title: str,
    status: str,
    version: str,
    content: str,
    *,
    metadata_override: dict[str, object] | None = None,
) -> str:
    metadata = _json_metadata(
        {"status": status, "version": version}
        if metadata_override is None
        else metadata_override
    )
    return "\n".join(
        (
            title,
            f"{_TERMINAL_META_PREFIX}{metadata}{_META_SUFFIX}",
            "",
            _required_content(content).rstrip(),
            "",
        )
    )


def _commit_terminal(
    workspace: ResearchWorkspace,
    path: Path,
    data: bytes,
    *,
    status: str,
    version: str,
    event: str,
    event_at: str,
) -> None:
    """Publish one terminal, rolling it back if the two controls cannot follow."""

    _publish_once(path, data, within=workspace.workspace_path)
    try:
        _update_status_and_ledger(
            workspace,
            status=status,
            version=version,
        artifact=path.name,
        artifact_sha256=_sha256(data),
        event=event,
            event_at=event_at,
        )
    except BaseException as error:
        try:
            current = _required_file(path, within=workspace.workspace_path)
            if current != data:
                raise OSError("published terminal changed before rollback")
            path.unlink()
            if path.exists():
                raise OSError("published terminal still exists after rollback")
        except BaseException as rollback_error:
            raise OSError(
                "terminal commit failed and terminal rollback was incomplete: "
                f"{rollback_error}"
            ) from error
        raise


def _update_status_and_ledger(
    workspace: ResearchWorkspace,
    *,
    status: str,
    version: str,
    artifact: str,
    artifact_sha256: str,
    event: str,
    event_at: str,
) -> None:
    status_path = workspace.workspace_path / "RUN_STATUS.md"
    ledger_path = workspace.workspace_path / "RUN_LEDGER.md"
    original_status = _required_file(
        status_path, within=workspace.workspace_path
    ).decode("utf-8")
    original_ledger = _required_file(
        ledger_path, within=workspace.workspace_path
    ).decode("utf-8")
    updates = {
        "STATUS": status,
        "CURRENT_VERSION": version,
        "LAST_DURABLE_ARTIFACT": artifact,
        "UPDATED_AT": event_at,
    }
    lines = original_status.splitlines()
    for name, value in updates.items():
        prefix = f"{name}:"
        matches = [index for index, line in enumerate(lines) if line.startswith(prefix)]
        if matches:
            lines[matches[0]] = f"{name}: {value}"
            for index in reversed(matches[1:]):
                del lines[index]
        else:
            lines.append(f"{name}: {value}")
    status_text = "\n".join(lines).rstrip() + "\n"
    ledger_text = original_ledger.rstrip() + (
        f"\n\n- EVENT: {event}\n"
        f"  AT: {event_at}\n"
        f"  VERSION: {version}\n"
        f"  ARTIFACT: {artifact}\n"
        f"  ARTIFACT_SHA256: {artifact_sha256}\n"
    )
    try:
        _atomic_write_text(
            ledger_path, ledger_text, within=workspace.workspace_path
        )
        _atomic_write_text(
            status_path, status_text, within=workspace.workspace_path
        )
    except BaseException as error:
        rollback_errors = []
        for control_path, original in (
            (ledger_path, original_ledger),
            (status_path, original_status),
        ):
            try:
                _atomic_write_text(
                    control_path, original, within=workspace.workspace_path
                )
            except BaseException as rollback_error:
                rollback_errors.append(
                    f"{control_path.name}: {rollback_error}"
                )
        if rollback_errors:
            raise OSError(
                "terminal control update failed and rollback was incomplete: "
                + "; ".join(rollback_errors)
            ) from error
        raise


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def environment_secrets() -> tuple[bytes, ...]:
    values = []
    for name, value in os.environ.items():
        if _is_sensitive_environment_item(name, value):
            encoded = value.encode("utf-8", errors="ignore")
            if encoded:
                values.append(encoded)
    return tuple(sorted(set(values), key=len, reverse=True))


def child_process_environment(
    allowed_sensitive_names: Iterable[str] = (),
) -> tuple[dict[str, str], tuple[str, ...]]:
    """Copy the normal environment while withholding ambient credentials by default."""

    source = dict(os.environ)
    names_by_case = {name.casefold(): name for name in source}
    sensitive_names = {
        name
        for name, value in source.items()
        if _is_sensitive_environment_item(name, value)
    }
    allowed: set[str] = set()
    for requested in allowed_sensitive_names:
        if (
            not isinstance(requested, str)
            or _ENVIRONMENT_VARIABLE_NAME.fullmatch(requested) is None
        ):
            raise ValueError(
                "allowed sensitive environment variables must be named without values"
            )
        actual = names_by_case.get(requested.casefold())
        if actual is None:
            raise ValueError(
                f"allowed sensitive environment variable is unavailable: {requested}"
            )
        if actual not in sensitive_names:
            raise ValueError(
                "allowed sensitive environment variable is not classified as sensitive: "
                + requested
            )
        allowed.add(actual)

    sensitive_values = {source[name] for name in sensitive_names}
    child = {
        name: value
        for name, value in source.items()
        if name in allowed
        or (name not in sensitive_names and value not in sensitive_values)
    }
    return child, tuple(sorted(allowed, key=str.casefold))


def _is_sensitive_environment_item(name: str, value: str) -> bool:
    return bool(
        value
        and len(value) >= 8
        and any(token in name.upper() for token in _SENSITIVE_ENVIRONMENT_NAME_TOKENS)
    )


def redact_secrets(data: bytes, secrets: tuple[bytes, ...] | None = None) -> bytes:
    values = environment_secrets() if secrets is None else secrets
    for value in values:
        data = data.replace(value, b"[REDACTED]")
    for pattern in _SECRET_PATTERNS:
        data = pattern.sub(b"[REDACTED]", data)
    return data


def redact_file(
    source: Path,
    destination: Path,
    secrets: tuple[bytes, ...] | None = None,
) -> bool:
    """Stream one file through bounded credential redaction."""

    values = environment_secrets() if secrets is None else secrets
    window = max(max((len(value) for value in values), default=0) + 8, 8192)
    buffer = b""
    changed = False
    with source.open("rb") as source_handle, destination.open("xb") as target_handle:
        while chunk := source_handle.read(1024 * 1024):
            buffer += chunk
            safe = len(buffer) - window
            if safe <= 0:
                continue
            rendered, consumed, replaced = _redact_safe_prefix(buffer, safe, values)
            target_handle.write(rendered)
            buffer = buffer[consumed:]
            changed = changed or replaced
        rendered, consumed, replaced = _redact_safe_prefix(
            buffer, len(buffer), values
        )
        if consumed != len(buffer):
            raise RuntimeError("credential redaction did not consume its final buffer")
        target_handle.write(rendered)
        target_handle.flush()
        os.fsync(target_handle.fileno())
        changed = changed or replaced
    return changed


def contains_secret(data: bytes, secrets: tuple[bytes, ...] | None = None) -> bool:
    return scan_secret_bytes(data, secrets).contains_possible_credential


def scan_secret_bytes(
    data: bytes, secrets: tuple[bytes, ...] | None = None
) -> SecretScan:
    values = environment_secrets() if secrets is None else secrets
    return SecretScan(
        environment_secret=any(value and value in data for value in values),
        heuristic_pattern=any(pattern.search(data) for pattern in _SECRET_PATTERNS),
    )


def scan_file_secrets(
    path: Path, secrets: tuple[bytes, ...] | None = None
) -> SecretScan:
    values = environment_secrets() if secrets is None else secrets
    overlap = max(max((len(value) for value in values), default=0) + 8, 8192)
    tail = b""
    exact = False
    heuristic = False
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            data = tail + chunk
            scan = scan_secret_bytes(data, values)
            exact = exact or scan.environment_secret
            heuristic = heuristic or scan.heuristic_pattern
            tail = data[-overlap:]
    return SecretScan(exact, heuristic)


def secret_scan_errors(
    run_root: Path,
    *,
    for_no_delivery: bool = False,
    paths: Iterable[Path] | None = None,
) -> tuple[str, ...]:
    return _secret_scan_errors_from_findings(
        _scan_run_secret_findings(run_root, paths=paths),
        for_no_delivery=for_no_delivery,
    )


def _secret_scan_errors_from_findings(
    findings: tuple[_RunSecretFinding, ...], *, for_no_delivery: bool
) -> tuple[str, ...]:
    errors: list[str] = []
    for finding in findings:
        if finding.unsafe:
            errors.append(
                "Run file is not a safe regular Run-local file: "
                + finding.relative.as_posix()
            )
            continue
        scan = finding.scan
        assert scan is not None
        heuristic_blocks = scan.heuristic_pattern and (
            not for_no_delivery
            or (
                finding.text_secret_target
                and not finding.third_party
                and not finding.raw_search_payload
                and not finding.source_code
            )
        )
        if (
            scan.environment_secret
            or finding.high_confidence_path
            or finding.private_key
            or heuristic_blocks
        ):
            kind = (
                "environment secret"
                if scan.environment_secret
                else "private key"
                if finding.private_key
                else "sensitive credential path"
                if finding.high_confidence_path
                else "credential-like text"
            )
            errors.append(
                f"{kind} in Run file: {finding.relative.as_posix()}"
            )
    return tuple(errors)


def secret_scan_warnings(
    run_root: Path, *, paths: Iterable[Path] | None = None
) -> tuple[str, ...]:
    return _secret_scan_warnings_from_findings(
        _scan_run_secret_findings(
            run_root, check_private_keys=False, paths=paths
        )
    )


def _secret_scan_warnings_from_findings(
    findings: tuple[_RunSecretFinding, ...],
) -> tuple[str, ...]:
    warnings = []
    heuristic_paths = []
    for finding in findings:
        if finding.unsafe:
            warnings.append(
                "Run file is not a safe regular Run-local file and was not scanned: "
                + finding.relative.as_posix()
            )
            continue
        scan = finding.scan
        assert scan is not None
        if (
            scan.heuristic_pattern
            and not scan.environment_secret
            and (
                not finding.text_secret_target
                or finding.third_party
                or finding.raw_search_payload
                or finding.source_code
            )
        ):
            heuristic_paths.append(finding.relative.as_posix())
    if heuristic_paths:
        representatives = heuristic_paths[:_SECRET_WARNING_REPRESENTATIVE_LIMIT]
        warnings.append(
            "credential-like patterns require Main AI researcher review but are not "
            f"terminal blockers in {len(heuristic_paths)} Run files; representative "
            f"paths ({len(representatives)}/{len(heuristic_paths)}): "
            + ", ".join(representatives)
        )
    return tuple(warnings)


def _scan_run_secret_findings(
    run_root: Path,
    *,
    check_private_keys: bool = True,
    paths: Iterable[Path] | None = None,
) -> tuple[_RunSecretFinding, ...]:
    findings = []
    secrets = environment_secrets()
    root = run_root.resolve()
    candidates = (
        tuple(item for item in run_root.rglob("*") if item.is_file())
        if paths is None
        else tuple(paths)
    )
    for path in sorted(candidates):
        relative = path.relative_to(run_root)
        try:
            safe_path = _assert_read_target(path, root)
        except (OSError, ValueError):
            findings.append(
                _RunSecretFinding(
                    relative=relative,
                    unsafe=True,
                    scan=None,
                    third_party=False,
                    raw_search_payload=False,
                    source_code=False,
                    text_secret_target=False,
                    high_confidence_path=False,
                    private_key=False,
                )
            )
            continue
        scan = scan_file_secrets(safe_path, secrets)
        third_party = _is_third_party_path(relative)
        findings.append(
            _RunSecretFinding(
                relative=relative,
                unsafe=False,
                scan=scan,
                third_party=third_party,
                raw_search_payload=_is_raw_search_payload(relative),
                source_code=path.suffix.casefold()
                in {".py", ".pyi", ".ps1", ".sh"},
                text_secret_target=_is_text_secret_target(path),
                high_confidence_path=_is_high_confidence_secret_path(
                    relative, third_party=third_party
                ),
                private_key=(
                    (
                        _file_starts_with_private_key(safe_path)
                        if third_party
                        else _file_contains_private_key(safe_path)
                    )
                    if check_private_keys
                    else False
                ),
            )
        )
    return tuple(findings)


def _is_text_secret_target(path: Path) -> bool:
    return path.suffix.casefold() in _TEXT_SECRET_SUFFIXES


def _is_third_party_path(relative: Path) -> bool:
    return any(part.casefold() in _THIRD_PARTY_PATH_PARTS for part in relative.parts[:-1])


def _is_high_confidence_secret_path(relative: Path, *, third_party: bool) -> bool:
    name = relative.name.casefold()
    if name == ".env" or (
        name.startswith(".env.")
        and not name.endswith((".template", ".example", ".sample"))
    ):
        return True
    if name.startswith(".env.") and name.endswith((".template", ".example", ".sample")):
        return False
    if third_party:
        return False
    return _HIGH_CONFIDENCE_SECRET_NAME.search(relative.name) is not None


def _file_starts_with_private_key(path: Path) -> bool:
    with path.open("rb") as handle:
        prefix = handle.read(4096).lstrip()
    return _PRIVATE_KEY_PATTERN.match(prefix) is not None


def _file_contains_private_key(path: Path) -> bool:
    tail = b""
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            data = tail + chunk
            if _PRIVATE_KEY_PATTERN.search(data):
                return True
            tail = data[-128:]
    return False


def _is_raw_search_payload(relative: Path) -> bool:
    return re.search(
        r"(?:^|/)hypotheses_v\d{3,}/searches/[^/]+/result\.json$",
        relative.as_posix(),
    ) is not None


def _redact_safe_prefix(
    data: bytes, safe: int, secrets: tuple[bytes, ...]
) -> tuple[bytes, int, bool]:
    spans: list[tuple[int, int]] = []
    for value in secrets:
        start = 0
        while value and (index := data.find(value, start)) >= 0:
            spans.append((index, index + len(value)))
            start = index + max(len(value), 1)
    for pattern in _SECRET_PATTERNS:
        spans.extend((match.start(), match.end()) for match in pattern.finditer(data))
    spans.sort()
    merged: list[list[int]] = []
    for start, end in spans:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    output = bytearray()
    position = 0
    replaced = False
    for start, end in merged:
        if start >= safe:
            break
        if end <= position:
            continue
        output.extend(data[position:start])
        output.extend(b"[REDACTED]")
        position = end
        replaced = True
    consumed = max(position, safe)
    output.extend(data[position:consumed])
    return bytes(output), consumed, replaced


def _raise_if_secret_bytes(data: bytes, label: str) -> None:
    if contains_secret(data):
        raise ValueError(f"possible credential in terminal content: {label}")


def _json_metadata(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def _metadata_line(content: str, prefix: str, fields: set[str]) -> dict[str, object]:
    lines = content.splitlines()
    matches = [line for line in lines[:3] if line.startswith(prefix) and line.endswith(_META_SUFFIX)]
    if len(matches) != 1:
        raise ValueError("missing or duplicate bounded metadata")
    try:
        payload = json.loads(matches[0][len(prefix) : -len(_META_SUFFIX)])
    except json.JSONDecodeError as error:
        raise ValueError("invalid metadata JSON") from error
    if not isinstance(payload, dict) or set(payload) != fields:
        raise ValueError("metadata fields do not match the schema")
    return payload


def _metadata_string(metadata: dict[str, object], name: str) -> str:
    value = metadata.get(name)
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ValueError(f"metadata {name} must be non-empty single-line text")
    return value.strip()


def _metadata_digest(metadata: dict[str, object], name: str) -> str:
    value = _metadata_string(metadata, name)
    if re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError(f"metadata {name} must be a lowercase SHA-256 digest")
    return value


def _mapping_digest(mapping: dict[str, object], name: str) -> str:
    value = mapping.get(name)
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError(f"review report SHA-256 {name} is invalid")
    return value
