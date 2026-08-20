from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path
from typing import Mapping, Sequence

from .experiment import valid_supporting_attempt_ids
from .recorded import implementation_key, implementation_manifest
from .seed_support import final_evidence_closure, final_evidence_mapping_errors
from .workspace import ResearchWorkspace, _publish_once, _required_file, _sha256, safe_relative_path


EVALUATOR_VERSION = "CRL-EVAL-1.0"
REVIEW_PROTOCOL = "CRL-IR-1.0"
ROLES = ("SCI", "EMP", "ADV")
SECTION_TITLES = (
    "Implementation / Seed Overview",
    "Closest Prior Evidence",
    "Core Experimental Evidence",
    "Baseline & Budget Facts",
    "Ablation / Robustness / Falsification Evidence",
    "Reproducibility Facts",
    "Known Limitations",
)
DIMENSION_WEIGHTS = {
    "SCI": {"problem_value": 20, "prior_separation": 25, "mechanism_clarity": 25, "scientific_specificity": 15, "claim_calibration": 15},
    "EMP": {"experimental_validity": 25, "baseline_fairness": 25, "measurement_reliability": 20, "robustness_falsification": 20, "result_strength": 10},
    "ADV": {"reproducibility_traceability": 25, "confound_leakage_control": 25, "boundary_generalization": 15, "adversarial_survivability": 25, "evidence_auditability": 10},
}
ROLE_WEIGHTS = {"SCI": 35, "EMP": 40, "ADV": 25}
DIAGNOSTIC_FIELDS = {
    "SCI": {"strongest_scientific_contribution", "biggest_scientific_risk", "most_dangerous_prior_collision", "mechanism_falsifier"},
    "EMP": {"strongest_empirical_evidence", "biggest_empirical_threat", "baseline_confound", "killer_experiment", "missing_validation"},
    "ADV": {"most_fatal_failure_mode", "reproduction_breakpoint", "hidden_assumption", "boundary_warning", "best_stress_test"},
}
_EVAL_ID = re.compile(r"eval-(\d{4,})")
_CODEX_CLI_VERSION = re.compile(
    r"(?:codex-cli\s+)?v?(\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)",
    re.IGNORECASE,
)
_MAX_PACKET_BYTES = 1024 * 1024


def evaluator_root() -> Path:
    return Path(__file__).resolve().parents[1] / "evaluation" / "reviewer" / EVALUATOR_VERSION


def load_evaluator() -> dict[str, object]:
    root = evaluator_root()
    manifest_data = _required_file(root / "evaluator.json", within=root)
    manifest = json.loads(manifest_data.decode("utf-8"))
    if not isinstance(manifest, dict) or manifest.get("evaluator_version") != EVALUATOR_VERSION:
        raise ValueError("invalid frozen evaluator definition")
    names = (
        "evaluator.json", "common.md", "SCI.md", "EMP.md", "ADV.md",
        "SCI.schema.json", "EMP.schema.json", "ADV.schema.json",
    )
    files = []
    for name in names:
        data = _required_file(root / name, within=root)
        files.append({"path": name, "size_bytes": len(data), "sha256": _sha256(data)})
    definition = {"evaluator_version": EVALUATOR_VERSION, "files": files}
    return {
        "manifest": manifest,
        "files": files,
        "definition_sha256": _sha256(_json_bytes(definition)),
        "root": str(root),
    }


def normalize_codex_cli_version(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    match = _CODEX_CLI_VERSION.fullmatch(value.strip())
    return match.group(1) if match is not None else None


def reviewer_runtime_identity_errors(
    runtime: object, evaluator_manifest: Mapping[str, object]
) -> tuple[str, ...]:
    expected_raw = evaluator_manifest.get("codex_cli_version")
    expected = normalize_codex_cli_version(expected_raw)
    if expected is None:
        return ("frozen evaluator codex_cli_version is invalid",)
    if not isinstance(runtime, dict):
        return ("reviewer runtime provenance is missing",)
    actual_raw = runtime.get("codex_version")
    actual = normalize_codex_cli_version(actual_raw)
    if actual is None:
        return (
            "reviewer Codex CLI version output is unavailable or unrecognized; "
            f"expected {expected}",
        )
    if actual != expected:
        return (
            "reviewer Codex CLI version mismatch: "
            f"expected {expected}, actual {actual}",
        )
    return ()


def role_prompt(role: str) -> bytes:
    name = _role(role)
    root = evaluator_root()
    common = _required_file(root / "common.md", within=root)
    specific = _required_file(root / f"{name}.md", within=root)
    return common.rstrip() + b"\n\n" + specific.rstrip() + b"\n"


def output_schema_path(role: str) -> Path:
    root = evaluator_root()
    return Path(_required_existing_path(root / f"{_role(role)}.schema.json", root))


def create_evaluation(
    workspace: ResearchWorkspace,
    sections: Mapping[int, Sequence[str | Path]],
    *,
    final_delivery: bool = False,
) -> dict[str, object]:
    workspace.assert_run_writable()
    manifest = implementation_manifest(workspace)
    if not manifest["files"]:
        raise ValueError("review requires at least one current implementation file")
    implementation_digest = implementation_key(manifest)
    normalized_sections, sources = _section_sources(workspace, sections)
    selected_paths = {item["path"] for item in sources}
    inventory = evidence_inventory(
        workspace, implementation_digest, selected_paths=selected_paths
    )
    inventory_bytes = _json_bytes(inventory)
    inventory_sha = _sha256(inventory_bytes)
    evaluator = load_evaluator()
    manifest_bytes = _json_bytes(manifest)
    core_evidence = None
    core_evidence_sha = None
    if final_delivery:
        seed_relative = workspace.seed_path.relative_to(workspace.workspace_path).as_posix()
        if seed_relative not in selected_paths:
            raise ValueError("final review packet must include the current final Seed")
        selected_valid_formal = [
            item
            for item in inventory["formal_attempts"]
            if item["association"] == "MATCH"
            and item["valid_review_support"] is True
            and item["selected_in_core"] is True
        ]
        if not selected_valid_formal:
            raise ValueError("final review packet must include a valid Formal support attempt")
        core_evidence = final_evidence_closure(
            workspace,
            [str(item["attempt_id"]) for item in selected_valid_formal],
        )
        mapping_errors = final_evidence_mapping_errors(core_evidence)
        if mapping_errors:
            raise ValueError(
                "final review explicit evidence mapping is invalid:\n- "
                + "\n- ".join(mapping_errors)
            )
        core_evidence_sha = _sha256(_json_bytes(core_evidence))
    packet = _render_packet(
        workspace,
        normalized_sections,
        inventory,
        inventory_sha,
        _sha256(manifest_bytes),
        implementation_digest,
        str(evaluator["definition_sha256"]),
        core_evidence,
        core_evidence_sha,
    )
    if len(packet) > _MAX_PACKET_BYTES:
        raise ValueError("review packet exceeds the fixed 1 MiB context bound")
    packet_digest = _sha256(packet)
    measurement_digest = _measurement_key(
        implementation_digest, packet_digest, str(evaluator["definition_sha256"])
    )
    evaluation_root = workspace.assert_write_target(workspace.review_path / "evaluations")
    evaluation_root.mkdir(parents=True, exist_ok=True)
    evaluation_id = _next_evaluation_id(evaluation_root)
    destination = workspace.assert_write_target(evaluation_root / evaluation_id)
    destination.mkdir()
    request = {
        "schema_version": 1,
        "evaluation_id": evaluation_id,
        "run_id": workspace.workspace_path.name,
        "contract_version": workspace.contract_version,
        "version": workspace.version,
        "evaluator_version": EVALUATOR_VERSION,
        "evaluator_definition_sha256": evaluator["definition_sha256"],
        "implementation_key": implementation_digest,
        "packet_key": packet_digest,
        "measurement_key": measurement_digest,
        "implementation_manifest_sha256": _sha256(manifest_bytes),
        "evidence_inventory_sha256": inventory_sha,
        "final_delivery_review": final_delivery,
        "source_materials": sources,
        "backend": evaluator["manifest"]["backend"],
    }
    if core_evidence_sha is not None:
        request["final_core_evidence_sha256"] = core_evidence_sha
    try:
        for name, data in (
            ("implementation_manifest.json", manifest_bytes),
            ("evidence_inventory.json", inventory_bytes),
            ("packet.md", packet),
            ("request.json", _json_bytes(request)),
        ):
            _publish_once(destination / name, data, within=workspace.workspace_path)
    except BaseException:
        for path in destination.iterdir():
            if path.is_file():
                path.unlink()
        destination.rmdir()
        raise
    return {**request, "path": str(destination)}


def evidence_inventory(
    workspace: ResearchWorkspace,
    current_implementation_key: str,
    *,
    selected_paths: set[str],
) -> dict[str, object]:
    valid_formal = set(valid_supporting_attempt_ids(workspace))
    formal = []
    associated_attempts: set[str] = set()
    attempts_root = workspace.experiment_path / "attempts"
    if attempts_root.is_dir():
        for directory in sorted(item for item in attempts_root.iterdir() if item.is_dir()):
            execution_path = directory / "execution.json"
            relative = execution_path.relative_to(workspace.workspace_path).as_posix()
            execution = None
            digest = None
            error = None
            try:
                data = _required_file(execution_path, within=workspace.workspace_path)
                execution = json.loads(data.decode("utf-8"))
                digest = _sha256(data)
            except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError, ValueError) as caught:
                error = str(caught)
            association = _formal_association(workspace, execution, current_implementation_key)
            if association == "MATCH":
                associated_attempts.add(directory.name)
            formal.append(
                {
                    "attempt_id": directory.name,
                    "path": relative,
                    "record_sha256": digest,
                    "schema_version": execution.get("schema_version") if isinstance(execution, dict) else None,
                    "status": _formal_status(execution),
                    "association": association,
                    "valid_review_support": directory.name in valid_formal,
                    "selected_in_core": _selected(relative, selected_paths),
                    "read_error": error,
                }
            )
    comparisons = []
    comparisons_root = workspace.experiment_path / "comparisons"
    if comparisons_root.is_dir():
        for directory in sorted(item for item in comparisons_root.iterdir() if item.is_dir()):
            path = directory / "comparison.json"
            relative = path.relative_to(workspace.workspace_path).as_posix()
            try:
                data = _required_file(path, within=workspace.workspace_path)
                value = json.loads(data.decode("utf-8"))
                ids = _comparison_attempt_ids(value)
                error = None
                digest = _sha256(data)
            except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError, ValueError) as caught:
                ids = set()
                error = str(caught)
                digest = None
            if ids & associated_attempts:
                comparisons.append(
                    {
                        "comparison_id": directory.name,
                        "path": relative,
                        "record_sha256": digest,
                        "attempt_ids": sorted(ids),
                        "selected_in_core": _selected(relative, selected_paths),
                        "read_error": error,
                    }
                )
    recorded = []
    recorded_root = workspace.experiment_path / "recorded"
    if recorded_root.is_dir():
        for directory in sorted(item for item in recorded_root.iterdir() if item.is_dir()):
            path = directory / "record.json"
            relative = path.relative_to(workspace.workspace_path).as_posix()
            try:
                data = _required_file(path, within=workspace.workspace_path)
                value = json.loads(data.decode("utf-8"))
                digest = _sha256(data)
                captured_key = value.get("implementation_key") if isinstance(value, dict) else None
                status = value.get("status") if isinstance(value, dict) else None
                error = None
            except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError, ValueError) as caught:
                digest = None
                captured_key = None
                status = None
                error = str(caught)
            association = (
                "MATCH" if captured_key == current_implementation_key
                else "MISMATCH" if isinstance(captured_key, str)
                else "ASSOCIATION_UNKNOWN"
            )
            recorded.append(
                {
                    "record_id": directory.name,
                    "path": relative,
                    "record_sha256": digest,
                    "status": status,
                    "association": association,
                    "selected_in_core": _selected(relative, selected_paths),
                    "read_error": error,
                }
            )
    return {
        "schema_version": 1,
        "version": workspace.version,
        "implementation_key": current_implementation_key,
        "formal_attempt_count": len(formal),
        "formal_attempts": formal,
        "comparison_count": len(comparisons),
        "comparisons": comparisons,
        "recorded_attempt_count": len(recorded),
        "recorded_attempts": recorded,
        "machine_judgment": "NONE_FACTS_ONLY",
    }


def validate_reviewer_output(role: str, value: object) -> dict[str, object]:
    name = _role(role)
    if not isinstance(value, dict):
        raise ValueError("reviewer output must be an object")
    required = {
        "review_protocol", "reviewer_role", "evaluator_version", "model_identity",
        "reasoning_effort", "scores", "reasons", "diagnostics", "critical_risk",
        "confidence", "free_review",
    }
    if set(value) != required:
        raise ValueError("reviewer output fields do not match the protocol")
    expected = {
        "review_protocol": REVIEW_PROTOCOL,
        "reviewer_role": name,
        "evaluator_version": EVALUATOR_VERSION,
        "model_identity": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise ValueError(f"reviewer output {field} mismatch")
    scores = value.get("scores")
    reasons = value.get("reasons")
    if not isinstance(scores, dict) or set(scores) != set(DIMENSION_WEIGHTS[name]):
        raise ValueError("reviewer score dimensions do not match role")
    if not all(type(score) is int and 0 <= score <= 4 for score in scores.values()):
        raise ValueError("reviewer scores must be integers from 0 to 4")
    if not isinstance(reasons, dict) or set(reasons) != set(scores) or not all(
        isinstance(item, str) and item.strip() for item in reasons.values()
    ):
        raise ValueError("reviewer reasons do not match role dimensions")
    diagnostics = value.get("diagnostics")
    if not isinstance(diagnostics, dict) or set(diagnostics) != DIAGNOSTIC_FIELDS[name] or not all(
        isinstance(item, str) and item.strip() for item in diagnostics.values()
    ):
        raise ValueError("reviewer diagnostics do not match role")
    if value.get("critical_risk") not in {"none", "serious", "potentially_fatal"}:
        raise ValueError("invalid reviewer critical_risk")
    if value.get("confidence") not in {"low", "medium", "high"}:
        raise ValueError("invalid reviewer confidence")
    if not isinstance(value.get("free_review"), str) or not value["free_review"].strip():
        raise ValueError("reviewer free_review is empty")
    return value


def role_score_basis_points(role: str, scores: Mapping[str, int]) -> int:
    name = _role(role)
    if set(scores) != set(DIMENSION_WEIGHTS[name]):
        raise ValueError("score dimensions do not match role")
    return sum(int(scores[dimension]) * weight * 25 for dimension, weight in DIMENSION_WEIGHTS[name].items())


def finalize_evaluation(workspace: ResearchWorkspace, evaluation_id: str) -> dict[str, object]:
    root = _evaluation_path(workspace, evaluation_id)
    request_data = _required_file(
        root / "request.json", within=workspace.workspace_path
    )
    request = json.loads(request_data.decode("utf-8"))
    if not isinstance(request, dict):
        raise ValueError("evaluation request is not an object")
    packet = _required_file(root / "packet.md", within=workspace.workspace_path)
    if request.get("packet_key") != _sha256(packet):
        raise ValueError("review packet identity changed before finalization")
    request_sha256 = _sha256(request_data)
    execution_identity = {
        "request_sha256": request_sha256,
        "packet_key": request.get("packet_key"),
        "measurement_key": request.get("measurement_key"),
    }
    evaluator = load_evaluator()
    reports = {}
    invalid_reasons = []
    for role in ROLES:
        envelope = _load_json(root / role / "report.json", workspace.workspace_path)
        mismatched_identity = [
            field
            for field, expected in execution_identity.items()
            if envelope.get(field) != expected
        ]
        if mismatched_identity:
            raise ValueError(
                f"reviewer execution input identity mismatch for {role}: "
                + ", ".join(mismatched_identity)
            )
        runtime_errors = reviewer_runtime_identity_errors(
            envelope.get("runtime"), evaluator["manifest"]
        )
        if runtime_errors:
            invalid_reasons.extend(f"{role}: {item}" for item in runtime_errors)
        if envelope.get("valid") is not True:
            invalid_reasons.extend(str(item) for item in envelope.get("invalid_reasons", []))
        if runtime_errors or envelope.get("valid") is not True:
            continue
        output = validate_reviewer_output(role, envelope.get("output"))
        reports[role] = {
            "output": output,
            "role_score_basis_points": role_score_basis_points(role, output["scores"]),
            "report_sha256": _file_sha256(root / role / "report.json"),
        }
    valid = len(reports) == 3 and not invalid_reasons
    previous = _valid_aggregates(workspace, str(request["measurement_key"]), exclude=evaluation_id)
    if valid:
        numerator = sum(reports[role]["role_score_basis_points"] * ROLE_WEIGHTS[role] for role in ROLES)
        measurement_kind = "CANONICAL_IMPLEMENTATION_SCORE" if not previous else "STABILITY_MEASUREMENT"
        canonical_evaluation_id = evaluation_id if not previous else str(previous[0]["evaluation_id"])
        series = [int(item["overall_score_numerator"]) for item in previous] + [numerator]
        stability = _stability(series)
    else:
        numerator = None
        measurement_kind = "INVALID_MEASUREMENT"
        canonical_evaluation_id = None
        stability = None
    aggregate = {
        "schema_version": 1,
        "evaluation_id": evaluation_id,
        "valid": valid,
        "invalid_reasons": sorted(set(invalid_reasons)),
        "evaluator_version": EVALUATOR_VERSION,
        "request_sha256": request_sha256,
        "implementation_key": request["implementation_key"],
        "packet_key": request["packet_key"],
        "measurement_key": request["measurement_key"],
        "measurement_kind": measurement_kind,
        "canonical_evaluation_id": canonical_evaluation_id,
        "role_results": reports,
        "overall_score_numerator": numerator,
        "overall_score_percent": _percent(numerator) if numerator is not None else None,
        "stability": stability,
        "score_is_gate": False,
    }
    data = _json_bytes(aggregate)
    _publish_once(root / "aggregate.json", data, within=workspace.workspace_path)
    _publish_once(root / "aggregate.md", _aggregate_markdown(aggregate), within=workspace.workspace_path)
    return aggregate


def canonical_evaluation(
    workspace: ResearchWorkspace, measurement_key: str
) -> dict[str, object] | None:
    items = _valid_aggregates(workspace, measurement_key)
    return items[0] if items else None


def implementation_measurement_history(
    workspace: ResearchWorkspace, implementation_digest: str
) -> list[dict[str, object]]:
    output = []
    root = workspace.review_path / "evaluations"
    if not root.is_dir():
        return output
    for directory in sorted(item for item in root.iterdir() if item.is_dir()):
        aggregate_path = directory / "aggregate.json"
        if not aggregate_path.is_file():
            continue
        value = _load_json(aggregate_path, workspace.workspace_path)
        if value.get("implementation_key") == implementation_digest:
            output.append(value)
    return output


def _section_sources(
    workspace: ResearchWorkspace, sections: Mapping[int, Sequence[str | Path]]
) -> tuple[list[tuple[int, str, list[tuple[str, bytes]]]], list[dict[str, object]]]:
    unknown = set(sections) - set(range(1, 8))
    if unknown:
        raise ValueError(f"unknown review packet sections: {sorted(unknown)}")
    normalized = []
    snapshots = []
    seen: set[str] = set()
    for number, title in enumerate(SECTION_TITLES, start=1):
        materials = []
        for value in sections.get(number, ()):
            relative = safe_relative_path(value)
            safe = workspace.assert_read_target(workspace.workspace_path / relative)
            data = _required_file(safe, within=workspace.workspace_path)
            text = data.decode("utf-8")
            if "\x00" in text:
                raise ValueError(f"review packet source is not text: {relative}")
            name = safe.relative_to(workspace.workspace_path).as_posix()
            if name in seen:
                raise ValueError(f"review source appears in multiple sections: {name}")
            seen.add(name)
            materials.append((name, data))
            snapshots.append({"path": name, "size_bytes": len(data), "sha256": _sha256(data), "section": number})
        normalized.append((number, title, materials))
    return normalized, snapshots


def _render_packet(
    workspace: ResearchWorkspace,
    sections: list[tuple[int, str, list[tuple[str, bytes]]]],
    inventory: dict[str, object],
    inventory_sha: str,
    manifest_sha: str,
    implementation_digest: str,
    evaluator_sha: str,
    core_evidence: Mapping[str, object] | None,
    core_evidence_sha: str | None,
) -> bytes:
    lines = [
        "# CRL Fixed Review Packet",
        "",
        f"- Contract: {workspace.contract_version}",
        f"- Scientific version: {workspace.version}",
        f"- Evaluator: {EVALUATOR_VERSION}",
        f"- Evaluator definition SHA-256: {evaluator_sha}",
        f"- Implementation key: {implementation_digest}",
        f"- Implementation manifest SHA-256: {manifest_sha}",
        f"- Evidence inventory SHA-256: {inventory_sha}",
        "",
    ]
    for number, title, materials in sections:
        lines.extend((f"## {number}. {title}", ""))
        if not materials:
            lines.extend(("NOT PROVIDED", ""))
            continue
        for path, data in materials:
            lines.extend((f"### Source: `{path}`", "", data.decode("utf-8").rstrip(), ""))
    if core_evidence is not None:
        lines.extend(
            (
                "## Final Core Evidence Closure (machine generated, bounded)",
                "",
                "This appendix exposes selected Formal Spec, Claim and metric facts; "
                "it does not judge scientific sufficiency.",
                f"Closure SHA-256: `{core_evidence_sha}`",
                "",
                "```json",
            )
        )
        lines.extend(
            json.dumps(
                core_evidence, ensure_ascii=False, indent=2, sort_keys=True
            ).splitlines()
        )
        lines.extend(("```", ""))
    lines.extend(("## Evidence Inventory (machine generated)", "", "```json"))
    lines.extend(json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True).splitlines())
    lines.extend(("```", ""))
    return "\n".join(lines).encode("utf-8")


def _formal_association(
    workspace: ResearchWorkspace, execution: object, current_key: str
) -> str:
    if not isinstance(execution, dict) or not isinstance(execution.get("implementation_files"), list):
        return "ASSOCIATION_UNKNOWN"
    files = []
    for item in execution["implementation_files"]:
        if not isinstance(item, dict) or not all(name in item for name in ("path", "size_bytes", "sha256")):
            return "ASSOCIATION_UNKNOWN"
        files.append({"path": item["path"], "size_bytes": item["size_bytes"], "sha256": item["sha256"]})
    manifest = {"schema_version": 1, "run_id": workspace.workspace_path.name, "version": workspace.version, "files": sorted(files, key=lambda item: str(item["path"]))}
    return "MATCH" if implementation_key(manifest) == current_key else "MISMATCH"


def _formal_status(execution: object) -> str | None:
    if not isinstance(execution, dict):
        return None
    if execution.get("timed_out") is True:
        return "TIMEOUT"
    if execution.get("runner_exit_code") == 0 and execution.get("command_exit_code") == 0:
        return "SUCCESS"
    return "FAILED"


def _comparison_attempt_ids(value: object) -> set[str]:
    if not isinstance(value, dict):
        return set()
    output = set()
    candidate = value.get("candidate_attempt")
    if isinstance(candidate, dict) and isinstance(candidate.get("attempt_id"), str):
        output.add(candidate["attempt_id"])
    for baseline in value.get("baseline_attempts", []):
        if isinstance(baseline, dict) and isinstance(baseline.get("attempt_id"), str):
            output.add(baseline["attempt_id"])
    return output


def _selected(relative: str, selected_paths: set[str]) -> bool:
    parent = str(Path(relative).parent).replace("\\", "/")
    return relative in selected_paths or any(path == parent or path.startswith(parent + "/") for path in selected_paths)


def _valid_aggregates(
    workspace: ResearchWorkspace, measurement_key: str, *, exclude: str | None = None
) -> list[dict[str, object]]:
    output = []
    root = workspace.review_path / "evaluations"
    if not root.is_dir():
        return output
    for directory in sorted(item for item in root.iterdir() if item.is_dir()):
        if directory.name == exclude or not (directory / "aggregate.json").is_file():
            continue
        value = _load_json(directory / "aggregate.json", workspace.workspace_path)
        if value.get("valid") is True and value.get("measurement_key") == measurement_key:
            output.append(value)
    return output


def _stability(series: list[int]) -> dict[str, object]:
    count = len(series)
    total = sum(series)
    mean = Decimal(total) / Decimal(count)
    variance = sum((Decimal(item) - mean) ** 2 for item in series) / Decimal(count)
    return {
        "valid_measurement_count": count,
        "overall_score_numerators": series,
        "mean_numerator": str(mean),
        "min_numerator": min(series),
        "max_numerator": max(series),
        "range_numerator": max(series) - min(series),
        "population_variance_numerator_squared": str(variance),
    }


def _aggregate_markdown(value: dict[str, object]) -> bytes:
    lines = [
        "# CRL Fixed Reviewer Aggregate",
        "",
        f"- Valid: {str(value['valid']).lower()}",
        f"- Measurement kind: `{value['measurement_kind']}`",
        f"- Implementation key: `{value['implementation_key']}`",
        f"- Packet key: `{value['packet_key']}`",
        f"- Measurement key: `{value['measurement_key']}`",
        f"- Canonical evaluation: `{value['canonical_evaluation_id']}`",
        f"- Overall score: {value['overall_score_percent'] if value['valid'] else 'INVALID'}",
        "- This score is not a delivery Gate or publication probability.",
        "",
    ]
    for role in ROLES:
        if role not in value["role_results"]:
            continue
        result = value["role_results"][role]
        output = result["output"]
        lines.extend((f"## {role}", "", f"- Role score (basis points): {result['role_score_basis_points']}", f"- Critical risk: `{output['critical_risk']}`", f"- Confidence: `{output['confidence']}`", "", "### Dimensions", ""))
        for dimension, score in output["scores"].items():
            lines.append(f"- `{dimension}`: {score}/4 — {output['reasons'][dimension]}")
        lines.extend(("", "### Free review", "", output["free_review"], ""))
    return "\n".join(lines).encode("utf-8")


def _percent(numerator: int) -> str:
    return f"{Decimal(numerator) / Decimal(10000):.4f}"


def _measurement_key(implementation_digest: str, packet_digest: str, evaluator_digest: str) -> str:
    return hashlib.sha256((implementation_digest + packet_digest + evaluator_digest).encode("ascii")).hexdigest()


def _next_evaluation_id(root: Path) -> str:
    numbers = [int(match.group(1)) for path in root.iterdir() if path.is_dir() and (match := _EVAL_ID.fullmatch(path.name))]
    return f"eval-{max(numbers, default=0) + 1:04d}"


def _evaluation_path(workspace: ResearchWorkspace, value: str) -> Path:
    if _EVAL_ID.fullmatch(value) is None:
        raise ValueError("invalid evaluation id")
    path = workspace.review_path / "evaluations" / value
    if not path.is_dir():
        raise FileNotFoundError(f"evaluation does not exist: {value}")
    return path


def _load_json(path: Path, within: Path) -> dict[str, object]:
    value = json.loads(_required_file(path, within=within).decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON artifact is not an object: {path}")
    return value


def _file_sha256(path: Path) -> str:
    return _sha256(path.read_bytes())


def _required_existing_path(path: Path, root: Path) -> str:
    _required_file(path, within=root)
    return str(path)


def _role(value: str) -> str:
    if value not in ROLES:
        raise ValueError(f"invalid reviewer role: {value}")
    return value


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
