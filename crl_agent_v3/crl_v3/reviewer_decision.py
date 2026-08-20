from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .experiment import experiment_material_errors, supporting_attempt_execution_sha256
from .recorded import implementation_key, implementation_manifest
from .reviewer_protocol import (
    canonical_evaluation,
    evidence_inventory,
    implementation_measurement_history,
)
from .seed_support import final_evidence_closure, final_evidence_mapping_errors
from .workspace import ResearchWorkspace, _publish_once, _required_content, _required_file, _sha256


_META_PREFIX = "<!-- CRL_FIXED_DECISION_META "
_META_SUFFIX = " -->"


@dataclass(frozen=True, slots=True)
class FixedDecisionDocument:
    path: str
    version: str
    content: str
    implementation_key: str
    packet_key: str
    measurement_key: str
    canonical_evaluation_id: str
    aggregate_sha256: str
    sha256: str


def write_fixed_review_decision(
    workspace: ResearchWorkspace,
    content: str,
    *,
    measurement_key: str | None = None,
) -> FixedDecisionDocument:
    workspace.assert_run_writable()
    aggregate = _select_canonical(workspace, measurement_key)
    evaluation_id = str(aggregate["evaluation_id"])
    evaluation_root = workspace.review_path / "evaluations" / evaluation_id
    request = _load_json(evaluation_root / "request.json", workspace)
    aggregate_data = _required_file(evaluation_root / "aggregate.json", within=workspace.workspace_path)
    manifest_data = _required_file(
        evaluation_root / "implementation_manifest.json", within=workspace.workspace_path
    )
    inventory_data = _required_file(
        evaluation_root / "evidence_inventory.json", within=workspace.workspace_path
    )
    role_report_sha256s = {
        role: _sha256(
            _required_file(evaluation_root / role / "report.json", within=workspace.workspace_path)
        )
        for role in ("SCI", "EMP", "ADV")
    }
    history = [
        {
            "evaluation_id": item["evaluation_id"],
            "measurement_key": item["measurement_key"],
            "measurement_kind": item["measurement_kind"],
            "canonical_evaluation_id": item["canonical_evaluation_id"],
            "overall_score_percent": item["overall_score_percent"],
        }
        for item in implementation_measurement_history(
            workspace, str(aggregate["implementation_key"])
        )
    ]
    metadata = {
        "schema_version": 3,
        "version": workspace.version,
        "implementation_key": aggregate["implementation_key"],
        "packet_key": aggregate["packet_key"],
        "measurement_key": aggregate["measurement_key"],
        "canonical_evaluation_id": evaluation_id,
        "aggregate_sha256": _sha256(aggregate_data),
        "implementation_manifest_sha256": _sha256(manifest_data),
        "evidence_inventory_sha256": _sha256(inventory_data),
        "role_report_sha256s": role_report_sha256s,
        "implementation_review_history": history,
        "final_delivery_review": request.get("final_delivery_review") is True,
    }
    rendered = "\n".join(
        (
            "# Main AI Decision After Fixed Review",
            _META_PREFIX + json.dumps(metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + _META_SUFFIX,
            "",
            _required_content(content).rstrip(),
            "",
        )
    )
    path = workspace.document_path("decision")
    _publish_once(path, rendered.encode("utf-8"), within=workspace.workspace_path)
    return read_fixed_review_decision(workspace)


def read_fixed_review_decision(workspace: ResearchWorkspace) -> FixedDecisionDocument:
    path = workspace.document_path("decision")
    data = _required_file(path, within=workspace.workspace_path)
    content = data.decode("utf-8")
    metadata = _decision_metadata(content)
    if metadata.get("schema_version") != 3 or metadata.get("version") != workspace.version:
        raise ValueError("fixed review decision schema or version mismatch")
    required = {
        "schema_version", "version", "implementation_key", "packet_key",
        "measurement_key", "canonical_evaluation_id", "aggregate_sha256",
        "implementation_manifest_sha256", "evidence_inventory_sha256",
        "role_report_sha256s", "implementation_review_history", "final_delivery_review",
    }
    if set(metadata) != required:
        raise ValueError("fixed review decision metadata fields are invalid")
    aggregate = _select_canonical(workspace, str(metadata["measurement_key"]))
    evaluation_id = str(metadata["canonical_evaluation_id"])
    if aggregate.get("evaluation_id") != evaluation_id:
        raise ValueError("fixed decision does not bind the canonical evaluation")
    evaluation_root = workspace.review_path / "evaluations" / evaluation_id
    checks = {
        "aggregate_sha256": evaluation_root / "aggregate.json",
        "implementation_manifest_sha256": evaluation_root / "implementation_manifest.json",
        "evidence_inventory_sha256": evaluation_root / "evidence_inventory.json",
    }
    for field, artifact in checks.items():
        current = _sha256(_required_file(artifact, within=workspace.workspace_path))
        if metadata.get(field) != current:
            raise ValueError(f"fixed decision {field} does not match its artifact")
    report_hashes = metadata.get("role_report_sha256s")
    if not isinstance(report_hashes, dict) or set(report_hashes) != {"SCI", "EMP", "ADV"}:
        raise ValueError("fixed decision role report hashes are invalid")
    for role, expected in report_hashes.items():
        current = _sha256(
            _required_file(
                evaluation_root / role / "report.json",
                within=workspace.workspace_path,
            )
        )
        if expected != current:
            raise ValueError("fixed decision is bound to different reviewer reports")
    if metadata.get("implementation_key") != aggregate.get("implementation_key") or metadata.get("packet_key") != aggregate.get("packet_key"):
        raise ValueError("fixed decision identity keys do not match aggregate")
    return FixedDecisionDocument(
        path=str(path),
        version=workspace.version,
        content=content,
        implementation_key=str(metadata["implementation_key"]),
        packet_key=str(metadata["packet_key"]),
        measurement_key=str(metadata["measurement_key"]),
        canonical_evaluation_id=evaluation_id,
        aggregate_sha256=str(metadata["aggregate_sha256"]),
        sha256=_sha256(data),
    )


def fixed_delivery_errors(
    workspace: ResearchWorkspace,
    supporting_attempt_ids: Iterable[str] | None,
) -> tuple[str, ...]:
    from .decision import _conclusion_history, secret_scan_errors

    errors = []
    try:
        seed = _required_file(workspace.seed_path, within=workspace.workspace_path)
        if not seed.decode("utf-8").strip():
            raise ValueError("empty final Seed")
    except (FileNotFoundError, UnicodeError, ValueError) as error:
        errors.append(f"missing or invalid final Seed: {error}")
    attempt_ids = None if supporting_attempt_ids is None else tuple(dict.fromkeys(str(item).strip() for item in supporting_attempt_ids))
    if not attempt_ids:
        errors.append("explicit Formal supporting attempt ids are required")
    else:
        errors.extend(experiment_material_errors(workspace, attempt_ids))
    try:
        decision = read_fixed_review_decision(workspace)
        aggregate = _select_canonical(workspace, decision.measurement_key)
        evaluation_root = workspace.review_path / "evaluations" / decision.canonical_evaluation_id
        request_data = _required_file(
            evaluation_root / "request.json", within=workspace.workspace_path
        )
        request = json.loads(request_data.decode("utf-8"))
        if not isinstance(request, dict):
            raise ValueError("final Review request is not an object")
        expected_request_sha = aggregate.get("request_sha256")
        if not isinstance(expected_request_sha, str):
            errors.append(
                "final canonical Review does not bind request.json byte identity"
            )
        elif _sha256(request_data) != expected_request_sha:
            errors.append("final Review request.json changed after canonical measurement")
        packet_data = _required_file(
            evaluation_root / "packet.md", within=workspace.workspace_path
        )
        if _sha256(packet_data) != aggregate.get("packet_key"):
            errors.append("final Review packet.md changed after canonical measurement")
        if request.get("packet_key") != aggregate.get("packet_key"):
            errors.append("final Review request and canonical packet identity disagree")
        if request.get("final_delivery_review") is not True:
            errors.append("Delivery requires a final-delivery Review packet")
        current_manifest = implementation_manifest(workspace)
        current_key = implementation_key(current_manifest)
        if current_key != decision.implementation_key:
            errors.append("current implementation differs from the final canonical Review")
        selected_paths = {str(item["path"]) for item in request.get("source_materials", []) if isinstance(item, dict) and isinstance(item.get("path"), str)}
        current_inventory = evidence_inventory(
            workspace, current_key, selected_paths=selected_paths
        )
        current_inventory_data = _json_bytes(current_inventory)
        frozen_inventory = _required_file(
            evaluation_root / "evidence_inventory.json", within=workspace.workspace_path
        )
        if current_inventory_data != frozen_inventory:
            errors.append("experiment evidence inventory changed after final Review")
        inventory = json.loads(frozen_inventory.decode("utf-8"))
        supporting = {
            item["attempt_id"]
            for item in inventory.get("formal_attempts", [])
            if isinstance(item, dict)
            and item.get("association") == "MATCH"
            and item.get("valid_review_support") is True
            and item.get("selected_in_core") is True
        }
        expected_core_evidence_sha = request.get("final_core_evidence_sha256")
        if not isinstance(expected_core_evidence_sha, str):
            errors.append(
                "final Review does not bind a machine-generated core evidence closure"
            )
        else:
            try:
                current_core_evidence = final_evidence_closure(
                    workspace, sorted(supporting)
                )
                errors.extend(final_evidence_mapping_errors(current_core_evidence))
                if _sha256(_json_bytes(current_core_evidence)) != expected_core_evidence_sha:
                    errors.append("final core evidence changed after final Review")
            except (FileNotFoundError, OSError, UnicodeError, ValueError) as error:
                errors.append(f"final core evidence cannot be revalidated: {error}")
        if attempt_ids and not set(attempt_ids).issubset(supporting):
            errors.append("selected Delivery attempts are not bound into the final Review packet")
        seed_relative = workspace.seed_path.relative_to(workspace.workspace_path).as_posix()
        seed_sources = [item for item in request.get("source_materials", []) if isinstance(item, dict) and item.get("path") == seed_relative]
        if len(seed_sources) != 1 or seed_sources[0].get("sha256") != _sha256(seed):
            errors.append("final Seed is not byte-bound into the final Review packet")
        if aggregate.get("measurement_kind") != "CANONICAL_IMPLEMENTATION_SCORE":
            errors.append("final decision does not bind a canonical Implementation Score")
    except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        errors.append(f"invalid fixed Review decision: {error}")
    errors.extend(secret_scan_errors(workspace.workspace_path))
    try:
        history = _conclusion_history(workspace)
        if history and int(workspace.version[1:]) <= int(history[-1].version[1:]):
            errors.append("new Delivery requires a scientific version newer than prior conclusion history")
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"invalid prior conclusion history: {error}")
    if (workspace.workspace_path / "TERMINATED_BY_USER.md").exists():
        errors.append("TERMINATED_BY_USER.md already exists")
    return tuple(dict.fromkeys(errors))


def write_fixed_delivery(
    workspace: ResearchWorkspace, *, supporting_attempt_ids: Iterable[str]
):
    from .decision import (
        _commit_terminal,
        _json_metadata,
        _render_terminal,
        _utc_now,
        read_delivery_history,
        read_terminal,
        secret_scan_warnings,
    )

    workspace.assert_run_writable()
    attempt_ids = tuple(dict.fromkeys(str(item).strip() for item in supporting_attempt_ids))
    errors = fixed_delivery_errors(workspace, attempt_ids)
    if errors:
        raise ValueError("delivery is mechanically incomplete:\n- " + "\n- ".join(errors))
    decision = read_fixed_review_decision(workspace)
    evaluation_root = workspace.review_path / "evaluations" / decision.canonical_evaluation_id
    seed_data = _required_file(workspace.seed_path, within=workspace.workspace_path)
    inventory_data = _required_file(evaluation_root / "evidence_inventory.json", within=workspace.workspace_path)
    manifest_data = _required_file(evaluation_root / "implementation_manifest.json", within=workspace.workspace_path)
    aggregate_data = _required_file(evaluation_root / "aggregate.json", within=workspace.workspace_path)
    metadata = {
        "schema_version": 4,
        "status": "DELIVERED",
        "version": workspace.version,
        "seed_path": workspace.seed_path.relative_to(workspace.workspace_path).as_posix(),
        "seed_sha256": _sha256(seed_data),
        "decision_sha256": decision.sha256,
        "implementation_key": decision.implementation_key,
        "packet_key": decision.packet_key,
        "measurement_key": decision.measurement_key,
        "canonical_evaluation_id": decision.canonical_evaluation_id,
        "aggregate_sha256": _sha256(aggregate_data),
        "implementation_manifest_sha256": _sha256(manifest_data),
        "evidence_inventory_sha256": _sha256(inventory_data),
        "supporting_attempts": [
            {"attempt_id": attempt_id, "execution_sha256": supporting_attempt_execution_sha256(workspace, attempt_id)}
            for attempt_id in attempt_ids
        ],
    }
    rendered = _render_terminal(
        "# CRL Research Seed Delivery",
        "DELIVERED",
        workspace.version,
        "\n".join(
            (
                f"- Final Seed: {metadata['seed_path']}",
                f"- Final implementation key: {decision.implementation_key}",
                f"- Canonical measurement key: {decision.measurement_key}",
                f"- Canonical evaluation: {decision.canonical_evaluation_id}",
            )
        ),
        metadata_override=metadata,
    )
    prior_deliveries = read_delivery_history(workspace)
    path = (
        workspace.workspace_path / "DELIVERY.md"
        if not prior_deliveries
        else workspace.workspace_path / f"DELIVERY_{workspace.version}.md"
    )
    data = rendered.encode("utf-8")
    _commit_terminal(
        workspace,
        path,
        data,
        status="DELIVERED",
        version=workspace.version,
        event="SEED_DELIVERED",
        event_at=_utc_now(),
    )
    return read_terminal(
        path, "DELIVERED", workspace.version, warnings=secret_scan_warnings(workspace.workspace_path)
    )


def read_fixed_delivery(
    workspace: ResearchWorkspace, *, path: str | Path | None = None
):
    from .decision import read_terminal

    if path is None:
        versioned = workspace.workspace_path / f"DELIVERY_{workspace.version}.md"
        path = versioned if versioned.is_file() else workspace.workspace_path / "DELIVERY.md"
    target = Path(path)
    terminal = read_terminal(target, "DELIVERED", workspace.version)
    data = _required_file(target, within=workspace.workspace_path)
    metadata = _terminal_metadata(data.decode("utf-8"))
    seed = _required_file(workspace.seed_path, within=workspace.workspace_path)
    if metadata.get("seed_sha256") != _sha256(seed):
        raise ValueError("fixed Delivery Seed SHA-256 no longer matches")
    decision = read_fixed_review_decision(workspace)
    if metadata.get("decision_sha256") != decision.sha256:
        raise ValueError("fixed Delivery decision SHA-256 no longer matches")
    evaluation_root = workspace.review_path / "evaluations" / decision.canonical_evaluation_id
    checks = {
        "aggregate_sha256": evaluation_root / "aggregate.json",
        "implementation_manifest_sha256": evaluation_root / "implementation_manifest.json",
        "evidence_inventory_sha256": evaluation_root / "evidence_inventory.json",
    }
    for field, artifact in checks.items():
        if metadata.get(field) != _sha256(
            _required_file(artifact, within=workspace.workspace_path)
        ):
            raise ValueError(f"fixed Delivery {field} no longer matches")
    if any(
        metadata.get(field) != getattr(decision, field)
        for field in ("implementation_key", "packet_key", "measurement_key", "canonical_evaluation_id")
    ):
        raise ValueError("fixed Delivery Reviewer identity keys no longer match")
    attempts = metadata.get("supporting_attempts")
    if not isinstance(attempts, list) or not attempts:
        raise ValueError("fixed Delivery supporting attempts are invalid")
    for item in attempts:
        if not isinstance(item, dict) or set(item) != {"attempt_id", "execution_sha256"}:
            raise ValueError("fixed Delivery supporting attempt entry is invalid")
        if item["execution_sha256"] != supporting_attempt_execution_sha256(
            workspace, str(item["attempt_id"])
        ):
            raise ValueError("fixed Delivery supporting attempt changed")
    return terminal


def _select_canonical(
    workspace: ResearchWorkspace, measurement_key: str | None
) -> dict[str, object]:
    if measurement_key is not None:
        value = canonical_evaluation(workspace, measurement_key)
        if value is None:
            raise ValueError("no valid canonical Review exists for measurement key")
        return value
    root = workspace.review_path / "evaluations"
    candidates = []
    if root.is_dir():
        for directory in sorted((item for item in root.iterdir() if item.is_dir()), reverse=True):
            path = directory / "aggregate.json"
            if not path.is_file():
                continue
            value = _load_json(path, workspace)
            if value.get("valid") is True:
                canonical = canonical_evaluation(workspace, str(value["measurement_key"]))
                if canonical is not None:
                    candidates.append(canonical)
                    break
    if not candidates:
        raise ValueError("no valid fixed Review measurement is available")
    return candidates[0]


def _decision_metadata(content: str) -> dict[str, object]:
    matches = [line for line in content.splitlines()[:3] if line.startswith(_META_PREFIX) and line.endswith(_META_SUFFIX)]
    if len(matches) != 1:
        raise ValueError("missing or duplicate fixed decision metadata")
    value = json.loads(matches[0][len(_META_PREFIX) : -len(_META_SUFFIX)])
    if not isinstance(value, dict):
        raise ValueError("fixed decision metadata is not an object")
    return value


def _terminal_metadata(content: str) -> dict[str, object]:
    prefix = "<!-- CRL_TERMINAL_META "
    matches = [line for line in content.splitlines()[:3] if line.startswith(prefix) and line.endswith(_META_SUFFIX)]
    if len(matches) != 1:
        raise ValueError("missing or duplicate fixed Delivery metadata")
    value = json.loads(matches[0][len(prefix) : -len(_META_SUFFIX)])
    if not isinstance(value, dict) or value.get("schema_version") != 4:
        raise ValueError("unsupported fixed Delivery schema")
    return value


def _load_json(path: Path, workspace: ResearchWorkspace) -> dict[str, object]:
    value = json.loads(_required_file(path, within=workspace.workspace_path).decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON artifact is not an object: {path}")
    return value


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
