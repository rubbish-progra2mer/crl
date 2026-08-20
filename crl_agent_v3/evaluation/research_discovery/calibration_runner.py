"""CRL 科研搜索奖励校准的隔离工作区与阶段运行器。"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import stat
import tempfile
import tomllib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from crl_v3.decision import environment_secrets, scan_secret_bytes

from .calibration import (
    CALIBRATION_PHASES,
    CALIBRATION_SCHEMA_VERSION,
    block_heldout_bridge_validation,
    build_frozen_task_split,
    evaluate_confirmation_gate,
    evaluate_pilot_gate,
    validate_frozen_task_split,
    validate_temporal_packet,
)


_EVENT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
_PREFLIGHT_AGENT_MODEL = "qwen3:8b"
_PREFLIGHT_USER_MODEL = "qwen2.5:7b"
_PREFLIGHT_EVALUATOR_MODEL = "qwen2.5:7b"
_PREFLIGHT_MAX_STEPS = 30
_PREFLIGHT_TIMEOUT_SECONDS = 120.0
_EVENT_FIELDS = {
    "schema_version",
    "phase",
    "event_id",
    "kind",
    "payload",
    "event_integrity_sha256",
}
_OUTCOME_COMMON_FIELDS = {
    "candidate_id",
    "block_id",
    "attempt_id",
    "fidelity",
    "scaffold_sha256",
    "scaffold_mode",
    "structural_cell",
    "attempt_manifest_sha256",
    "domain",
    "task_id",
    "repetition",
    "seed",
    "execution_status",
    "success",
    "reward",
    "termination_reason",
    "wall_time_seconds",
    "agent_model",
    "user_model",
    "evaluator_model",
    "max_steps",
    "timeout_seconds",
    "enforce_communication_protocol",
    "llm_log_path",
    "llm_log_manifest",
}
_OUTCOME_RAW_FIELDS = {"raw_result_path", "raw_result_sha256"}
_OUTCOME_RUNNER_FAILURE_FIELDS = {"error_type", "error_message"}
_AUDIT_FIELDS = {
    "candidate_id",
    "block_id",
    "attempt_id",
    "fidelity",
    "scaffold_sha256",
    "scaffold_mode",
    "structural_cell",
    "attempt_manifest_sha256",
    "attempt_manifest_path",
    "evaluator_lock_valid_before",
    "evaluator_lock_valid_after",
    "candidate_write_scope",
    "evaluator_model",
    "base_seed",
    "task_split_sha256",
    "scheduled_unit_count",
    "budget_parity",
}
_ATTEMPT_MANIFEST_FIELDS = {
    "schema_version",
    "phase",
    "fidelity",
    "block_id",
    "attempt_id",
    "candidate_id",
    "mode",
    "structural_cell",
    "scaffold_sha256",
    "task_split_sha256",
    "selected_tasks",
    "repetitions",
    "base_seed",
    "agent_model",
    "user_model",
    "evaluator_model",
    "model_identities",
    "max_steps",
    "timeout_seconds",
    "enforce_communication_protocol",
    "ollama_url",
    "tau2_root",
    "evaluator_lock_sha256",
    "runtime_python",
    "runtime_python_version",
    "runtime_dont_write_bytecode",
    "runtime_pycache_prefix",
    "runtime_dependencies",
    "runtime_dependencies_sha256",
    "runtime_dependency_tree",
    "manifest_sha256",
}
_SKIPPED_RELEASE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "simulations",
}


class CalibrationWorkspace:
    """约束所有校准产物只能位于指定的 Run 外研究工作区。"""

    def __init__(self, root: str | Path, research_workspace_root: str | Path):
        self.root = Path(os.path.abspath(root))
        self.research_workspace_root = Path(os.path.abspath(research_workspace_root))
        _assert_descendant(self.root, self.research_workspace_root)
        _reject_reparse_chain(self.research_workspace_root, self.root)

    def prepare(self) -> None:
        _reject_reparse_chain(self.research_workspace_root, self.root)
        self.root.mkdir(parents=True, exist_ok=True)
        for name in (
            "preflight",
            "pilot",
            "confirm",
            "temporal",
            "auxiliary_reviews",
        ):
            self.target(name).mkdir(exist_ok=True)

    def target(self, *parts: str) -> Path:
        path = self.root.joinpath(*parts)
        _assert_descendant(path, self.root)
        _reject_reparse_chain(self.root, path)
        return path

    def write_json_once(self, relative: str, value: object) -> bool:
        data = _json_bytes(value)
        _reject_secret_data(data, f"calibration JSON {relative}")
        return self._write_once(relative, data)

    def write_text_once(self, relative: str, text: str) -> bool:
        if "\r" in text:
            raise ValueError("calibration Markdown must use LF newlines")
        data = text.encode("utf-8")
        _reject_secret_data(data, f"calibration text {relative}")
        return self._write_once(relative, data)

    def write_bytes_once(self, relative: str, data: bytes) -> bool:
        _reject_secret_data(data, f"calibration artifact {relative}")
        return self._write_once(relative, data)

    def bind_read_file(self, path: str | Path) -> Path:
        target = Path(os.path.abspath(path))
        _assert_descendant(target, self.root)
        _reject_reparse_chain(self.root, target)
        if not target.is_file():
            raise FileNotFoundError(f"calibration input file is missing: {target}")
        return target

    def record_event(self, phase: str, event: Mapping[str, Any]) -> bool:
        if phase not in CALIBRATION_PHASES:
            raise ValueError(f"unknown calibration phase: {phase}")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or _EVENT_ID.fullmatch(event_id) is None:
            raise ValueError("event_id is invalid")
        normalized = dict(event)
        normalized.setdefault("schema_version", CALIBRATION_SCHEMA_VERSION)
        normalized.setdefault("phase", phase)
        if normalized["schema_version"] != CALIBRATION_SCHEMA_VERSION:
            raise ValueError("unsupported calibration event schema")
        if normalized["phase"] != phase:
            raise ValueError("event phase does not match destination phase")
        if not isinstance(normalized.get("kind"), str) or not normalized["kind"].strip():
            raise ValueError("event kind must be non-empty")
        if "event_integrity_sha256" in normalized:
            raise ValueError("event integrity hash is machine-generated")
        normalized["event_integrity_sha256"] = hashlib.sha256(
            _json_bytes(normalized)
        ).hexdigest()
        data = _json_bytes(normalized)
        _reject_secret_data(data, "calibration event")
        return self._write_once(f"{phase}/events/{event_id}.json", data)

    def read_events(self, phase: str) -> list[dict[str, Any]]:
        events_root = self.target(phase, "events")
        if not events_root.exists():
            return []
        if _is_reparse_point(events_root):
            raise ValueError(f"event directory must not be a reparse point: {events_root}")
        output: list[dict[str, Any]] = []
        for path in sorted(events_root.glob("*.json"), key=lambda item: item.name):
            _reject_reparse_chain(self.root, path)
            event = _read_json_object(path)
            if event.get("event_id") != path.stem:
                raise ValueError(f"event filename does not match event_id: {path}")
            declared = event.get("event_integrity_sha256")
            if declared is not None:
                unsigned = dict(event)
                unsigned.pop("event_integrity_sha256", None)
                if declared != hashlib.sha256(_json_bytes(unsigned)).hexdigest():
                    raise ValueError(f"calibration event integrity check failed: {path}")
            output.append(event)
        return output

    def _write_once(self, relative: str, data: bytes) -> bool:
        path = self.target(*Path(relative).parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        _reject_reparse_chain(self.root, path)
        if path.exists():
            if path.read_bytes() == data:
                return False
            raise FileExistsError(f"immutable calibration artifact differs: {path}")
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        except Exception:
            path.unlink(missing_ok=True)
            raise
        return True


def initialize_calibration(
    workspace: CalibrationWorkspace,
    *,
    tau2_root: str | Path,
    split_seed: int = 20260819,
) -> dict[str, Any]:
    """建立固定目录、协议、任务划分与外部评价器锁。"""

    workspace.prepare()
    workspace.write_text_once("protocol.md", render_calibration_protocol())
    split = build_frozen_task_split(tau2_root, seed=split_seed)
    workspace.write_json_once("frozen_task_split.json", split)
    evaluator_lock = build_evaluator_lock(tau2_root)
    workspace.write_json_once("preflight/evaluator_lock.json", evaluator_lock)
    return {
        "protocol_path": str(workspace.target("protocol.md")),
        "task_split_path": str(workspace.target("frozen_task_split.json")),
        "task_split_sha256": split["split_sha256"],
        "evaluator_lock_path": str(workspace.target("preflight", "evaluator_lock.json")),
        "evaluator_file_count": evaluator_lock["file_count"],
    }


def repair_frozen_task_split(
    workspace: CalibrationWorkspace,
    *,
    tau2_root: str | Path,
    split_seed: int = 20260819,
) -> dict[str, Any]:
    """保留旧划分并原子替换为绑定官方 base split 的修正版。"""

    workspace.prepare()
    target = workspace.target("frozen_task_split.json")
    corrected = build_frozen_task_split(tau2_root, seed=split_seed)
    corrected_data = _json_bytes(corrected)
    if not target.exists():
        workspace.write_bytes_once("frozen_task_split.json", corrected_data)
        return {"changed": True, "previous": None, "current": corrected["split_sha256"]}
    previous_data = target.read_bytes()
    if previous_data == corrected_data:
        return {
            "changed": False,
            "previous": corrected["split_sha256"],
            "current": corrected["split_sha256"],
        }
    previous_hash = hashlib.sha256(previous_data).hexdigest()
    invalidated_relative = (
        "preflight/invalidated/"
        f"frozen_task_split-before-base-filter-{previous_hash[:16]}.json"
    )
    workspace.write_bytes_once(invalidated_relative, previous_data)
    corrected_hash = hashlib.sha256(corrected_data).hexdigest()
    repair = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "defect": "task sampling used tasks.json without intersecting official base split",
        "previous_file_sha256": previous_hash,
        "previous_copy": invalidated_relative,
        "corrected_file_sha256": corrected_hash,
        "corrected_split_sha256": corrected["split_sha256"],
        "invalidated_execution_scope": "all tau2 outcomes bound to the previous split",
        "scientific_interpretation": "forbidden",
    }
    workspace.write_json_once(
        f"preflight/repairs/task-split-base-filter-{corrected_hash[:16]}.json", repair
    )
    _atomic_replace(target, corrected_data)
    return {
        "changed": True,
        "previous": previous_hash,
        "current": corrected["split_sha256"],
        "invalidated_copy": invalidated_relative,
    }


def repair_evaluator_lock(
    workspace: CalibrationWorkspace, *, tau2_root: str | Path
) -> dict[str, Any]:
    """保留旧锁并原子替换为覆盖完整执行源码与数据树的锁。"""

    workspace.prepare()
    target = workspace.target("preflight", "evaluator_lock.json")
    corrected = build_evaluator_lock(tau2_root)
    corrected_data = _json_bytes(corrected)
    if not target.exists():
        workspace.write_bytes_once("preflight/evaluator_lock.json", corrected_data)
        return {"changed": True, "previous": None, "current": corrected["lock_sha256"]}
    previous_data = target.read_bytes()
    if previous_data == corrected_data:
        return {
            "changed": False,
            "previous": corrected["lock_sha256"],
            "current": corrected["lock_sha256"],
        }
    previous_hash = hashlib.sha256(previous_data).hexdigest()
    invalidated_relative = (
        "preflight/invalidated/"
        f"evaluator-lock-before-full-execution-tree-{previous_hash[:16]}.json"
    )
    workspace.write_bytes_once(invalidated_relative, previous_data)
    repair = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "defect": "evaluator lock omitted executable tau2 agent, user, registry, and utility code",
        "previous_file_sha256": previous_hash,
        "previous_copy": invalidated_relative,
        "corrected_lock_sha256": corrected["lock_sha256"],
        "invalidated_execution_scope": "all tau2 outcomes bound only to the partial lock",
        "scientific_interpretation": "forbidden for calibration gates",
    }
    workspace.write_json_once(
        "preflight/repairs/evaluator-lock-full-execution-tree-"
        + corrected["lock_sha256"][:16]
        + ".json",
        repair,
    )
    _atomic_replace(target, corrected_data)
    return {
        "changed": True,
        "previous": previous_hash,
        "current": corrected["lock_sha256"],
        "invalidated_copy": invalidated_relative,
    }


def lock_tau2_preflight_selection(
    workspace: CalibrationWorkspace,
    selection: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """在任何所选结果产生前不可变地预注册四个预检角色。"""

    normalized = _validated_preflight_selection(selection)
    existing = workspace.read_events("preflight")
    identity_fields = ("candidate_id", "block_id", "attempt_id")
    for role, spec in normalized.items():
        if any(
            event.get("kind") == "tau2_outcome"
            and all(_payload(event).get(field) == spec[field] for field in identity_fields)
            for event in existing
        ):
            raise ValueError(
                f"preflight role {role} already has outcomes and cannot be registered post hoc"
            )
    split = _read_json_object(workspace.target("frozen_task_split.json"))
    validate_frozen_task_split(split)
    static_path = workspace.target("preflight", "current_static.json")
    if not static_path.is_file():
        raise ValueError("a passing current static preflight is required before selection lock")
    static_data = static_path.read_bytes()
    static = _read_json_object(static_path)
    evaluator_lock = _read_json_object(workspace.target("preflight", "evaluator_lock.json"))
    tau2_root = Path(str(static.get("tau2_root", "")))
    lock_check = verify_evaluator_lock(tau2_root, evaluator_lock)
    if (
        not isinstance(static.get("static_gate"), Mapping)
        or static["static_gate"].get("passed") is not True
        or static.get("task_split_sha256") != split["split_sha256"]
        or static.get("evaluator_lock_sha256") != evaluator_lock.get("lock_sha256")
        or not lock_check["valid"]
    ):
        raise ValueError("current static preflight is stale or not passing")
    locked_selection = {
        role: _locked_preflight_role(workspace, role, spec, split)
        for role, spec in normalized.items()
    }
    baseline_scaffold_hashes = {
        locked_selection[role]["scaffold_sha256"]
        for role in ("smoke", "baseline_a", "baseline_b")
    }
    if len(baseline_scaffold_hashes) != 1:
        raise ValueError("smoke and both baseline roles must use the same scaffold bytes")
    model_identities = static.get("model_identities")
    if not _valid_model_identities(
        model_identities,
        {_PREFLIGHT_AGENT_MODEL, _PREFLIGHT_USER_MODEL, "qwen3:14b"},
    ):
        raise ValueError("current static preflight lacks complete model identities")
    payload = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "selection": locked_selection,
        "task_split_sha256": split["split_sha256"],
        "static_snapshot_sha256": hashlib.sha256(static_data).hexdigest(),
        "execution_contract": {
            "tau2_root": str(tau2_root.resolve(strict=True)),
            "evaluator_lock_sha256": evaluator_lock["lock_sha256"],
            "agent_model": _PREFLIGHT_AGENT_MODEL,
            "user_model": _PREFLIGHT_USER_MODEL,
            "evaluator_model": _PREFLIGHT_EVALUATOR_MODEL,
            "model_identities": model_identities,
            "max_steps": _PREFLIGHT_MAX_STEPS,
            "timeout_seconds": _PREFLIGHT_TIMEOUT_SECONDS,
            "enforce_communication_protocol": False,
            "ollama_url": "http://127.0.0.1:11434",
        },
        "registration": "before_selected_outcomes",
    }
    payload["selection_lock_sha256"] = hashlib.sha256(_json_bytes(payload)).hexdigest()
    workspace.write_json_once("preflight/selection_lock.json", payload)
    return payload


def run_preflight(
    workspace: CalibrationWorkspace,
    *,
    tau2_root: str | Path,
    agent_model: str,
    user_model: str,
    reserve_model: str,
    evaluator_model: str = "qwen2.5:7b",
    split_seed: int = 20260819,
    ollama_url: str = "http://127.0.0.1:11434",
) -> dict[str, Any]:
    """执行不调用 τ² 任务的静态预检；真实 smoke 结果需另行记录。"""

    initialized = initialize_calibration(
        workspace, tau2_root=tau2_root, split_seed=split_seed
    )
    installed_models = query_ollama_models(ollama_url)
    model_identities = query_ollama_model_identities(
        {agent_model, user_model, evaluator_model, reserve_model}, ollama_url
    )
    release = inspect_tau2_release(tau2_root)
    isolated_release = _is_descendant(
        Path(os.path.abspath(tau2_root)), workspace.target("preflight", "runtime")
    )
    evaluator_lock = _read_json_object(workspace.target("preflight", "evaluator_lock.json"))
    lock_check = verify_evaluator_lock(tau2_root, evaluator_lock)
    models = {
        "agent": {"name": agent_model, "available": agent_model in installed_models},
        "user_simulator": {"name": user_model, "available": user_model in installed_models},
        "nl_assertion_evaluator": {
            "name": evaluator_model,
            "available": evaluator_model in installed_models,
        },
        "reserve": {"name": reserve_model, "available": reserve_model in installed_models},
    }
    report = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "phase": "preflight",
        "workspace": str(workspace.root),
        "tau2_root": str(Path(tau2_root).resolve(strict=True)),
        "tau2": release,
        "isolated_release": isolated_release,
        "models": models,
        "model_identities": model_identities,
        "evaluator_lock": lock_check,
        "evaluator_lock_sha256": evaluator_lock["lock_sha256"],
        "task_split_sha256": initialized["task_split_sha256"],
        "static_gate": {
            "passed": release["version"] == "1.0.1"
            and isolated_release
            and all(item["available"] for item in models.values())
            and lock_check["valid"],
            "mock_execution_required": True,
            "scientific_delivery_authority": False,
        },
    }
    report_hash = hashlib.sha256(_json_bytes(report)).hexdigest()[:16]
    workspace.write_json_once(f"preflight/snapshots/static-{report_hash}.json", report)
    _atomic_replace(workspace.target("preflight", "current_static.json"), _json_bytes(report))
    return report


def summarize_tau2_preflight(
    workspace: CalibrationWorkspace,
    selection: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """按显式 attempt 选择汇总 τ² 预检；不猜测哪个历史尝试有效。"""

    normalized = _validated_preflight_selection(selection)
    required = set(normalized)
    selection_lock_path = workspace.target("preflight", "selection_lock.json")
    if not selection_lock_path.is_file():
        raise ValueError("preflight selection must be locked before selected outcomes run")
    selection_lock = _read_json_object(selection_lock_path)
    _validate_preflight_selection_lock(selection_lock)
    split = _read_json_object(workspace.target("frozen_task_split.json"))
    validate_frozen_task_split(split)
    locked_selection = selection_lock["selection"]
    if selection_lock.get("task_split_sha256") != split.get("split_sha256") or any(
        any(locked_selection[role].get(field) != value for field, value in spec.items())
        for role, spec in normalized.items()
    ):
        raise ValueError("preflight selection does not match the immutable selection lock")
    execution_contract = selection_lock["execution_contract"]
    evaluator_lock = _read_json_object(workspace.target("preflight", "evaluator_lock.json"))
    current_lock_valid = bool(
        evaluator_lock.get("lock_sha256") == execution_contract["evaluator_lock_sha256"]
        and verify_evaluator_lock(execution_contract["tau2_root"], evaluator_lock)["valid"]
    )
    ground_truth_count = sum(
        int(item.get("action_count", 0)) > 0
        for domain in ("airline", "retail", "telecom")
        for item in split["low_fidelity"][domain]
    )
    expected_units = {
        "smoke": 10,
        "baseline_a": 24,
        "baseline_b": 24,
        "ground_truth": ground_truth_count,
    }
    all_events = workspace.read_events("preflight")
    attempts: dict[str, dict[str, Any]] = {}
    for role in sorted(required):
        spec = normalized[role]
        locked_role = locked_selection[role]
        spec_required = {"candidate_id", "block_id", "attempt_id", "fidelity"}
        outcome_events = [
            event
            for event in all_events
            if event.get("kind") == "tau2_outcome"
            and all(_payload(event).get(field) == spec[field] for field in spec_required)
        ]
        outcomes = [_payload(event) for event in outcome_events]
        keys = [
            (
                str(item.get("domain")),
                str(item.get("task_id")),
                int(item.get("repetition", -1)),
            )
            for item in outcomes
        ]
        if len(keys) != len(set(keys)):
            raise ValueError(f"duplicate tau2 outcome units in selected {role} attempt")
        completed = [
            item for item in outcomes if item.get("execution_status") == "completed"
        ]
        passes = sum(item.get("success") is True for item in completed)
        mechanics = len(outcomes) - len(completed)
        total = len(outcomes)
        audit_events = [
            event
            for event in all_events
            if event.get("kind") == "tau2_block_audit"
            and all(_payload(event).get(field) == spec[field] for field in spec_required)
        ]
        audits = [_payload(event) for event in audit_events]
        audit = audits[0] if len(audits) == 1 else {}
        expected_count = expected_units[role]
        manifest = _attempt_manifest_for_audit(workspace, audit)
        outcome_manifest_hashes = {
            item.get("attempt_manifest_sha256") for item in outcomes
        }
        expected_mode = "ground_truth" if role == "ground_truth" else "baseline"
        expected_fidelity = "smoke" if role == "smoke" else "low_fidelity"
        expected_model_identities = {
            name: execution_contract["model_identities"][name]
            for name in {
                execution_contract["agent_model"],
                execution_contract["user_model"],
                execution_contract["evaluator_model"],
            }
        }
        outcome_identity_valid = _preflight_outcome_identity_valid(
            outcomes, locked_role, execution_contract
        )
        event_envelopes_valid = all(
            _event_envelope_valid(event, kind="tau2_outcome")
            for event in outcome_events
        ) and len(audit_events) == 1 and _event_envelope_valid(
            audit_events[0], kind="tau2_block_audit"
        )
        outcome_assets_valid = all(
            _outcome_assets_valid(workspace, item) for item in outcomes
        )
        audit_contract_valid = _audit_contract_valid(
            audit,
            locked_role,
            execution_contract,
            str(split.get("split_sha256")),
            expected_count,
        )
        role_contract_valid = bool(
            manifest
            and manifest.get("phase") == "preflight"
            and manifest.get("candidate_id") == locked_role["candidate_id"]
            and manifest.get("block_id") == locked_role["block_id"]
            and manifest.get("attempt_id") == locked_role["attempt_id"]
            and manifest.get("mode") == expected_mode
            and manifest.get("fidelity") == expected_fidelity
            and manifest.get("task_split_sha256") == split.get("split_sha256")
            and manifest.get("scaffold_sha256") == locked_role["scaffold_sha256"]
            and manifest.get("selected_tasks") == locked_role["selected_tasks"]
            and manifest.get("base_seed") == locked_role["base_seed"]
            and manifest.get("agent_model") == execution_contract["agent_model"]
            and manifest.get("user_model") == execution_contract["user_model"]
            and manifest.get("evaluator_model") == execution_contract["evaluator_model"]
            and manifest.get("model_identities") == expected_model_identities
            and manifest.get("max_steps") == execution_contract["max_steps"]
            and manifest.get("timeout_seconds") == execution_contract["timeout_seconds"]
            and manifest.get("enforce_communication_protocol") is False
            and manifest.get("ollama_url") == execution_contract["ollama_url"]
            and os.path.normcase(str(manifest.get("tau2_root")))
            == os.path.normcase(str(execution_contract["tau2_root"]))
            and manifest.get("evaluator_lock_sha256")
            == execution_contract["evaluator_lock_sha256"]
            and manifest.get("repetitions") == locked_role["repetitions"]
            and _valid_runtime_identity(manifest)
            and audit_contract_valid
            and audit.get("attempt_manifest_sha256") == manifest.get("manifest_sha256")
            and audit.get("scaffold_sha256") == locked_role["scaffold_sha256"]
            and audit.get("base_seed") == locked_role["base_seed"]
            and outcome_manifest_hashes == {manifest.get("manifest_sha256")}
            and outcome_identity_valid
            and outcome_assets_valid
            and event_envelopes_valid
        )
        attempts[role] = {
            **dict(spec),
            "expected_unit_count": expected_count,
            "observed_unit_count": total,
            "completed_scientific_unit_count": len(completed),
            "scientific_pass_count": passes,
            "scientific_pass_rate": None if not completed else passes / len(completed),
            "mechanical_failure_count": mechanics,
            "mechanical_failure_rate": None if not total else mechanics / total,
            "evaluator_lock_valid_before": audit.get("evaluator_lock_valid_before") is True,
            "evaluator_lock_valid_after": audit.get("evaluator_lock_valid_after") is True,
            "role_contract_valid": role_contract_valid,
            "attempt_manifest_sha256": manifest.get("manifest_sha256") if manifest else None,
            "base_seed": manifest.get("base_seed") if manifest else None,
            "execution_identity": _execution_identity(manifest) if manifest else None,
            "outcome_assets_valid": outcome_assets_valid,
            "event_envelopes_valid": event_envelopes_valid,
            "audit_contract_valid": audit_contract_valid,
        }

    a_rate = attempts["baseline_a"]["scientific_pass_rate"]
    b_rate = attempts["baseline_b"]["scientific_pass_rate"]
    gt_rate = attempts["ground_truth"]["scientific_pass_rate"]
    checks: dict[str, bool] = {
        "all_attempts_complete": all(
            item["observed_unit_count"] == item["expected_unit_count"]
            for item in attempts.values()
        ),
        "all_evaluator_locks_valid": all(
            item["evaluator_lock_valid_before"]
            and item["evaluator_lock_valid_after"]
            for item in attempts.values()
        ),
        "all_role_contracts_valid": all(
            item["role_contract_valid"] for item in attempts.values()
        ),
        "current_evaluator_lock_valid": current_lock_valid,
        "all_attempts_share_execution_identity": len(
            {
                json.dumps(item["execution_identity"], ensure_ascii=False, sort_keys=True)
                for item in attempts.values()
                if item["execution_identity"] is not None
            }
        )
        == 1
        and all(item["execution_identity"] is not None for item in attempts.values()),
        "baseline_attempts_use_distinct_base_seeds": attempts["baseline_a"][
            "base_seed"
        ]
        is not None
        and attempts["baseline_b"]["base_seed"] is not None
        and attempts["baseline_a"]["base_seed"]
        != attempts["baseline_b"]["base_seed"],
        "smoke_has_no_mechanical_failure": attempts["smoke"][
            "mechanical_failure_count"
        ]
        == 0,
        "all_mechanical_failure_rates_at_most_5pct": all(
            item["mechanical_failure_rate"] is not None
            and item["mechanical_failure_rate"] <= 0.05
            for item in attempts.values()
        ),
        "baseline_a_pass_rate_between_10_and_80pct": a_rate is not None
        and 0.10 <= a_rate <= 0.80,
        "baseline_b_pass_rate_between_10_and_80pct": b_rate is not None
        and 0.10 <= b_rate <= 0.80,
        "baseline_repeat_variation_at_most_10pp": a_rate is not None
        and b_rate is not None
        and abs(a_rate - b_rate) <= 0.10,
        "ground_truth_pass_rate_at_least_70pct": gt_rate is not None
        and gt_rate >= 0.70,
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    summary = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "phase": "preflight",
        "selection": {role: dict(normalized[role]) for role in sorted(normalized)},
        "attempts": attempts,
        "gate": {
            "passed": all(checks.values()),
            "checks": checks,
            "failed_checks": failed_checks,
            "scientific_delivery_authority": False,
        },
    }
    digest = hashlib.sha256(_json_bytes(summary)).hexdigest()[:16]
    workspace.write_json_once(f"preflight/summaries/tau2-{digest}.json", summary)
    _atomic_replace(
        workspace.target("preflight", "current_diagnostic_summary.json"),
        _json_bytes(summary),
    )
    authoritative_ready = bool(
        checks["all_attempts_complete"]
        and checks["all_evaluator_locks_valid"]
        and checks["all_role_contracts_valid"]
        and checks["current_evaluator_lock_valid"]
        and checks["all_attempts_share_execution_identity"]
    )
    if authoritative_ready:
        workspace.write_json_once("preflight/authoritative_summary.json", summary)
    return summary


def summarize_pilot(workspace: CalibrationWorkspace) -> dict[str, Any]:
    raise RuntimeError(
        "pilot gate is disabled until candidate and bridge statistics are derived "
        "exclusively from immutable tau2 outcome manifests"
    )


def _unsafe_legacy_summarize_pilot(workspace: CalibrationWorkspace) -> dict[str, Any]:
    raise RuntimeError("legacy pilot summary is permanently disabled")


def _removed_legacy_summarize_pilot(workspace: CalibrationWorkspace) -> dict[str, Any]:
    raise RuntimeError("removed pilot summary implementation cannot be executed")

    # 不可达的旧格式读取逻辑暂留到迁移完成，不能形成授权产物。
    events = workspace.read_events("pilot")
    candidates = [item for item in events if item.get("kind") == "candidate_result"]
    observations = [item for item in events if item.get("kind") == "bridge_observation"]
    audits = [item for item in events if item.get("kind") == "isolation_audit"]
    implemented = sum(bool(_payload(item).get("implemented")) for item in candidates)
    implementation_rate = None if not candidates else implemented / len(candidates)
    completed_observations = [
        _payload(item)
        for item in observations
        if _payload(item).get("execution_status") == "completed"
    ]
    mechanical_observations = [
        item
        for item in observations
        if _payload(item).get("execution_status") != "completed"
    ]
    bridge = None
    if completed_observations:
        blocks = {str(item.get("block_id")) for item in completed_observations}
        if len(blocks) >= 2:
            bridge = block_heldout_bridge_validation(completed_observations)
    audit_payload = _payload(audits[-1]) if audits else {}
    summary: dict[str, Any] = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "phase": "pilot",
        "candidate_count": len(candidates),
        "implemented_candidate_count": implemented,
        "implementation_rate": implementation_rate,
        "high_fidelity_pass_count": sum(
            bool(item.get("high_success")) for item in completed_observations
        ),
        "high_fidelity_failure_count": sum(
            not bool(item.get("high_success")) for item in completed_observations
        ),
        "mechanical_observation_count": len(mechanical_observations),
        "isolation_valid": audit_payload.get("isolation_valid") is True,
        "evaluator_lock_valid": audit_payload.get("evaluator_lock_valid") is True,
        "bridge": bridge,
    }
    gate_input = {
        **summary,
        **(bridge or {}),
        "implementation_rate": -1 if implementation_rate is None else implementation_rate,
    }
    summary["gate"] = evaluate_pilot_gate(gate_input)
    digest = hashlib.sha256(_json_bytes(summary)).hexdigest()[:16]
    workspace.write_json_once(f"pilot/summaries/pilot-{digest}.json", summary)
    if summary["gate"]["passed"]:
        workspace.write_json_once(
            "confirm/authorized_by_pilot_gate.json",
            {
                "schema_version": CALIBRATION_SCHEMA_VERSION,
                "pilot_summary_sha256": hashlib.sha256(_json_bytes(summary)).hexdigest(),
                "authorization": "automatic_confirm_per_user_choice",
                "scientific_delivery_authority": False,
            },
        )
    return summary


def summarize_confirmation(workspace: CalibrationWorkspace) -> dict[str, Any]:
    raise RuntimeError(
        "confirmation gate is disabled until eight pre-registered blocks are derived "
        "exclusively from immutable tau2 outcome manifests"
    )


def _unsafe_legacy_summarize_confirmation(
    workspace: CalibrationWorkspace,
) -> dict[str, Any]:
    raise RuntimeError("legacy confirmation summary is permanently disabled")

    # 不可达的旧格式读取逻辑暂留到迁移完成，不能形成授权产物。
    authorization = workspace.target("confirm", "authorized_by_pilot_gate.json")
    if not authorization.is_file():
        raise ValueError("confirmation is not authorized by a passing pilot gate")
    events = workspace.read_events("confirm")
    block_events = [item for item in events if item.get("kind") == "block_advantage"]
    posterior_events = [
        item for item in events if item.get("kind") == "candidate_posterior"
    ]
    audit_events = [item for item in events if item.get("kind") == "confirmation_audit"]
    audit = _payload(audit_events[-1]) if audit_events else {}
    gate_input = {
        "block_advantages": [float(_payload(item)["advantage"]) for item in block_events],
        "candidate_posteriors": [_payload(item) for item in posterior_events],
        "domain_regression_constraints_pass": audit.get(
            "domain_regression_constraints_pass"
        ),
        "diversity_constraints_pass": audit.get("diversity_constraints_pass"),
        "isolation_valid": audit.get("isolation_valid"),
        "evaluator_lock_valid": audit.get("evaluator_lock_valid"),
    }
    summary = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "phase": "confirm",
        **gate_input,
        "gate": evaluate_confirmation_gate(gate_input),
    }
    digest = hashlib.sha256(_json_bytes(summary)).hexdigest()[:16]
    workspace.write_json_once(f"confirm/summaries/confirm-{digest}.json", summary)
    return summary


def run_temporal_validation(
    workspace: CalibrationWorkspace, packet_path: str | Path
) -> dict[str, Any]:
    packet = _read_json_object(workspace.bind_read_file(packet_path))
    validation = validate_temporal_packet(packet)
    packet_hash = hashlib.sha256(_json_bytes(packet)).hexdigest()
    report = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "phase": "temporal",
        "packet_sha256": packet_hash,
        "validation": validation,
        "clean_agent_model": "qwen2.5:7b",
        "clean_benchmark_version": "0.2.1",
        "realistic_codex_layer": "exploratory_only",
        "scientific_delivery_authority": False,
    }
    workspace.write_json_once("temporal/authoritative_validation.json", report)
    workspace.write_json_once(f"temporal/validations/{packet_hash[:16]}.json", report)
    return report


def build_calibration_report(workspace: CalibrationWorkspace) -> dict[str, Any]:
    split = _read_json_object(workspace.target("frozen_task_split.json"))
    validate_frozen_task_split(split)
    preflight_path = workspace.target("preflight", "authoritative_summary.json")
    diagnostic_path = workspace.target("preflight", "current_diagnostic_summary.json")
    preflight = (
        _read_json_object(preflight_path)
        if preflight_path.is_file()
        else _read_json_object(diagnostic_path)
        if diagnostic_path.is_file()
        else None
    )
    pilot = None
    confirm = None
    temporal_path = workspace.target("temporal", "authoritative_validation.json")
    temporal = _read_json_object(temporal_path) if temporal_path.is_file() else None
    report = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "generated_at": _utc_now(),
        "task_split_sha256": split["split_sha256"],
        "preflight": preflight,
        "preflight_authoritative": preflight_path.is_file(),
        "pilot": pilot,
        "confirm": confirm,
        "temporal": temporal,
        "interpretation": {
            "scope": "search-policy calibration only",
            "automatic_candidate_elimination": False,
            "automatic_delivery": False,
            "automatic_novelty_claim": False,
            "pilot_confirm_raw_derivation_available": False,
        },
    }
    json_data = _json_bytes(report)
    markdown = render_calibration_report(report)
    _atomic_replace(workspace.target("report.json"), json_data)
    _atomic_replace(workspace.target("report.md"), markdown.encode("utf-8"))
    return report


def build_evaluator_lock(tau2_root: str | Path) -> dict[str, Any]:
    root = Path(tau2_root)
    release = inspect_tau2_release(root)
    files: dict[str, str] = {}
    for path in _evaluator_files(root):
        relative = path.relative_to(root).as_posix()
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    lock = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "benchmark": release,
        "file_count": len(files),
        "files": files,
        "execution_scope": ["src/tau2", "data/tau2", "pyproject.toml"],
        "candidate_write_scope": "external isolated agent scaffold only",
    }
    lock["lock_sha256"] = hashlib.sha256(_json_bytes(lock)).hexdigest()
    return lock


def verify_evaluator_lock(
    tau2_root: str | Path, lock: Mapping[str, Any]
) -> dict[str, Any]:
    root = Path(tau2_root)
    expected_lock_hash = lock.get("lock_sha256")
    unsigned_lock = dict(lock)
    unsigned_lock.pop("lock_sha256", None)
    lock_hash_valid = isinstance(expected_lock_hash, str) and expected_lock_hash == hashlib.sha256(
        _json_bytes(unsigned_lock)
    ).hexdigest()
    locked_root = lock.get("benchmark", {}).get("root") if isinstance(lock.get("benchmark"), Mapping) else None
    root_matches = isinstance(locked_root, str) and os.path.normcase(
        str(Path(locked_root).resolve(strict=True))
    ) == os.path.normcase(str(root.resolve(strict=True)))
    files = lock.get("files")
    if not isinstance(files, Mapping):
        raise ValueError("evaluator lock files must be an object")
    missing: list[str] = []
    changed: list[str] = []
    for relative, expected in files.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise ValueError("invalid evaluator lock entry")
        path = root / Path(relative)
        _assert_descendant(path, root)
        _reject_reparse_chain(root, path)
        if not path.is_file():
            missing.append(relative)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            changed.append(relative)
    current_paths = {path.relative_to(root).as_posix() for path in _evaluator_files(root)}
    added = sorted(current_paths - set(files))
    return {
        "valid": lock_hash_valid and root_matches and not missing and not changed and not added,
        "lock_hash_valid": lock_hash_valid,
        "root_matches": root_matches,
        "missing": sorted(missing),
        "changed": sorted(changed),
        "added": added,
        "checked_file_count": len(files),
    }


def inspect_tau2_release(tau2_root: str | Path) -> dict[str, Any]:
    root = Path(tau2_root)
    pyproject = root / "pyproject.toml"
    data = pyproject.read_bytes()
    value = tomllib.loads(data.decode("utf-8", errors="strict"))
    version = value.get("project", {}).get("version")
    if not isinstance(version, str):
        raise ValueError("τ² pyproject does not declare a version")
    return {
        "name": value.get("project", {}).get("name"),
        "version": version,
        "root": str(root.resolve(strict=True)),
        "pyproject_sha256": hashlib.sha256(data).hexdigest(),
    }


def query_ollama_models(base_url: str = "http://127.0.0.1:11434") -> set[str]:
    request = urllib.request.Request(base_url.rstrip("/") + "/api/tags", method="GET")
    with urllib.request.urlopen(request, timeout=10) as response:
        value = json.loads(response.read().decode("utf-8", errors="strict"))
    models = value.get("models")
    if not isinstance(models, list):
        raise ValueError("Ollama /api/tags returned an invalid payload")
    output: set[str] = set()
    for item in models:
        if isinstance(item, Mapping):
            for key in ("name", "model"):
                name = item.get(key)
                if isinstance(name, str) and name:
                    output.add(name)
    return output


def query_ollama_model_identities(
    names: set[str], base_url: str = "http://127.0.0.1:11434"
) -> dict[str, dict[str, Any]]:
    normalized_url = base_url.rstrip("/")
    if normalized_url not in {"http://127.0.0.1:11434", "http://localhost:11434"}:
        raise ValueError("τ² calibration only permits the fixed local Ollama endpoint")
    request = urllib.request.Request(normalized_url + "/api/tags", method="GET")
    with urllib.request.urlopen(request, timeout=10) as response:
        value = json.loads(response.read().decode("utf-8", errors="strict"))
    models = value.get("models")
    if not isinstance(models, list):
        raise ValueError("Ollama model identity response is invalid")
    identities: dict[str, dict[str, Any]] = {}
    for name in sorted(names):
        matches = [
            item
            for item in models
            if isinstance(item, Mapping)
            and name in {item.get("name"), item.get("model")}
        ]
        if len(matches) != 1:
            raise ValueError(f"Ollama model identity is unavailable or ambiguous: {name}")
        item = matches[0]
        digest = item.get("digest")
        if not isinstance(digest, str) or not digest:
            raise ValueError(f"Ollama model digest is unavailable: {name}")
        identities[name] = {
            "digest": digest,
            "size": item.get("size"),
            "modified_at": item.get("modified_at"),
            "details": item.get("details"),
        }
    return identities


def render_calibration_protocol() -> str:
    return """# CRL 科研搜索奖励校准协议 v1

本目录是 Run 外的机器校准实验，不属于任何 CRL Research Run，不读取旧 Run 科研内容，
不写共享论文知识库，不自动淘汰候选、认证新颖性或形成 Delivery / No-Delivery。

## 冻结比较组

- 现行启发式组：读取原始结果，不接收标量排名。
- 朴素标量组：以任务平均通过率排序，执行失败按 0 计；该值只构成故意粗糙的对照。
- 约束奖励搜索组：硬约束优先，保留 Pareto 非支配档案；父代分配为 50% 后验
  Thompson 抽样、25% 最高不确定性、25% 最低结构覆盖。

## 科学效应与实验获取

科学效应以共同任务—种子单元的二元差 `d = y_candidate - y_baseline` 计算。机械失败从
科学配对效应中排除并单独报告。同一领域—任务跨配对块与重复合并为一个统计聚类；
至少 12 个独立任务后，
贝叶斯自助法才报告 `P(Δ>0)`、`P(Δ>0.05)` 和 `Q0.10(Δ)`，三者不求和。下一实验按
单位预期成本的 Beta-Bernoulli 预测熵下降选择。

## τ² 层

- 现实层冻结 τ² v1.0.1；Agent 为 `qwen3:8b`，用户模拟器为 `qwen2.5:7b`，
  `qwen3.5:9b` 与 `qwen3:14b` 只作预检失败后的辅助能力复核，不静默替换正式基线。
- τ² 官方 `NL_ASSERTION` 奖励所需的结构化评价器显式绑定 `qwen2.5:7b`；它是
  基准评价器的一部分并由 ground-truth 对照校准，不能被候选修改。该调用额外启用
  Ollama 的 `response_format={"type":"json_object"}`，只约束官方本来就要求的
  JSON 输出，不改变断言、提示或评分逻辑。
- smoke 为全部 10 个 mock 任务；低保真为三域各 8 个任务；高保真为 airline 20、
  retail 28、telecom 48 个任务，每个任务 3 次重复。
- 候选只能修改隔离的 Agent scaffold；评价器、任务、模型、工具、预算和留出集被冻结。
- 本地 Ollama 调用统一使用 `temperature=0`、`think=false`、最多 1024 输出 Token、
  单次模型调用 120 秒超时；这些执行参数对候选和基线完全相同。
- 半双工通信校验沿用 τ² 官方默认关闭值；混合文字—工具消息仍保存在原始轨迹中，
  但不被额外的非默认校验器改写成用户模拟器机械失败。
- 每个任务统一最多 30 个对话步；达到步数上限且得到评价时是预算内科学失败，墙钟超时
  则是机械失败。三组、基线和候选使用相同预算。
- 每个任务的本地模型调用日志按尝试隔离保存并记录文件哈希清单；评价异常也保留调用
  证据，但日志不进入科学分数。
- Windows 启动器强制 Python UTF-8 模式；核心执行函数拒绝在非 UTF-8 模式下直接运行，
  避免第三方基准的隐式文本编码产生部分无效块。
- 每个 attempt 在首个结果前写入不可变清单，绑定 scaffold、模型摘要、完整任务集合、
  划分、种子、预算、解释器、依赖版本和完整执行树锁；恢复时任一字段变化都会拒绝拼接。
- 每个 outcome 和 block audit 使用精确字段模式与事件自哈希。原始结果和日志必须位于该
  任务单元的规范路径；汇总会从原始 τ² JSON 重算任务、种子、奖励、终止原因、执行类别
  与成功标记的一致性，并在恢复和汇总时重新执行秘密扫描。
- 评价器锁覆盖 `src/tau2`、`data/tau2` 与 `pyproject.toml`，执行根必须与锁中根相同且
  位于校准工作区的隔离运行时。启动器剥离环境凭据，日志经秘密、重解析点、UTF-8 与
  LF 检查后才提交；事件是单元最终提交标记，孤立原始结果与日志只进入 orphaned 诊断区。
- 高保真样本至少 36 个候选，并跨低保真后验四分位与结构单元分层抽取。

## 小试与确认

四个预检角色必须在任何所选结果产生前写入不可变 selection lock，且按候选、块、尝试
三元组绑定四个不同 attempt；smoke 与两次基线使用字节完全相同的 baseline scaffold，ground-truth 使用独立的官方
ground-truth scaffold，两次基线使用不同基础种子。选择锁同时冻结 scaffold 摘要、模型
内容摘要、完整任务集合、基础种子、预算、当前静态预检和评价器锁。进入小试前，smoke 必须 10/10 完整
且无机械失败；两次独立低保真基线各 24 题，
机械失败率均不高于 5%、科学通过率均在 10%—80%，两次通过率相差不超过 10 个
百分点；同一低保真集里官方 `llm_agent_gt.check_valid_task` 支持的子集上，ground-truth
Agent 通过率至少 70%。不支持 ground-truth 的任务不进入该上界分母，也不算模型失败。
所有结果尝试由调用者显式绑定，脚本不从历史尝试中猜选。任何门槛失败只阻断小试，
不构成科研反证。

小试为 2 个配对块、每组 4 代、每代 6 个候选，第一代三组共享。只有实现率不低于
60%、高保真同时含通过与失败、每个留出块至少 12 个观察且所有折和全量桥接拟合均收敛、
块留一桥接 Brier 比基准率改善至少 10%、斜率为正、
顶部四分位优于底部四分位且隔离检查通过，才自动进入 8 个新配对块的确认实验。

当前代码有意关闭小试和确认入口，直到上述统计量能够完全从不可变 τ² outcome 与 attempt
manifest 机械推导；调用者提供的派生 JSON 或审计布尔值不能授权阶段推进。恢复入口后，
确认成功要求：约束组在至少 7/8 块优于启发式组；块优势中位数至少 5 个百分点；
至少一个候选 `P(Δ>0.05)>=0.95` 且 `Q0.10(Δ)>0`；领域退化约束、结构多样性与
评价器隔离均通过。这只支持是否采用搜索策略，不支持具体科研 Idea 的论文结论。

## 时间洁净层

时间洁净层使用 `qwen2.5:7b` 与 τ² v0.2.1，只允许 2025 年及以前材料；2026 年机制
P072、P074、P087 保持留出。Codex 现实层只作探索性结果。所有大语言模型辅助评审
必须标为 `llm_auxiliary` 与 `auxiliary_only`，不得进入主要科学结论。
"""


def render_calibration_report(report: Mapping[str, Any]) -> str:
    preflight = report.get("preflight")
    pilot = report.get("pilot")
    confirm = report.get("confirm")
    temporal = report.get("temporal")
    failed_checks: list[str] = []
    if isinstance(preflight, Mapping) and isinstance(preflight.get("gate"), Mapping):
        raw_failed_checks = preflight["gate"].get("failed_checks")
        if isinstance(raw_failed_checks, list):
            failed_checks = [str(item) for item in raw_failed_checks]
    lines = [
        "# CRL 科研搜索奖励校准报告",
        "",
        "本报告只评价搜索策略校准，不评价任何具体候选的新颖性或交付资格。",
        "",
        "## 阶段状态",
        "",
        f"- τ² 预检：{_phase_status(preflight)}",
        "- 小试：入口关闭；尚不能从不可变 τ² 原始结果机械推导",
        "- 确认：入口关闭；尚不能从不可变 τ² 原始结果机械推导",
        f"- 时间洁净层：{_phase_status(temporal)}",
    ]
    if preflight is not None and report.get("preflight_authoritative") is not True:
        lines.append("- 预检材料性质：运行中诊断，尚未形成权威汇总")
    if failed_checks:
        lines.extend(
            [
                "",
                "## 当前预检阻断",
                "",
                *[f"- {item}" for item in failed_checks],
            ]
        )
    lines.extend(
        [
            "",
            "## 权力边界",
            "",
            "- 自动淘汰科研候选：否",
            "- 自动认证新颖性：否",
            "- 自动形成 Delivery / No-Delivery：否",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _phase_status(value: object) -> str:
    if value is None:
        return "尚无结果"
    if isinstance(value, Mapping) and isinstance(value.get("gate"), Mapping):
        return "通过" if value["gate"].get("passed") else "未通过或材料不足"
    return "已有可复查材料"


def _evaluator_files(root: Path) -> list[Path]:
    roots = [
        root / "pyproject.toml",
        root / "src" / "tau2",
        root / "data" / "tau2",
    ]
    files: list[Path] = []
    for item in roots:
        if item.is_file():
            files.append(item)
            continue
        if not item.is_dir():
            raise FileNotFoundError(f"τ² evaluator path is missing: {item}")
        for directory, directory_names, file_names in os.walk(item, followlinks=False):
            current = Path(directory)
            if _is_reparse_point(current):
                raise ValueError(f"τ² evaluator tree contains a reparse point: {current}")
            for name in directory_names:
                child = current / name
                if _is_reparse_point(child):
                    raise ValueError(
                        f"τ² evaluator tree contains a reparse point: {child}"
                    )
                if name == "__pycache__":
                    raise ValueError(f"τ² evaluator tree contains executable bytecode cache: {child}")
            directory_names[:] = [
                name for name in directory_names if name not in _SKIPPED_RELEASE_DIRS
            ]
            for name in file_names:
                path = current / name
                if _is_reparse_point(path):
                    raise ValueError(f"τ² evaluator file is a reparse point: {path}")
                if path.suffix.casefold() in {".pyc", ".pyo"}:
                    raise ValueError(f"τ² evaluator tree contains executable bytecode: {path}")
                files.append(path)
    return sorted(set(files), key=lambda path: path.relative_to(root).as_posix())


def _validated_preflight_selection(
    selection: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    required = {"smoke", "baseline_a", "baseline_b", "ground_truth"}
    if set(selection) != required:
        raise ValueError(f"preflight selection must contain exactly {sorted(required)}")
    text_fields = {"candidate_id", "block_id", "attempt_id", "fidelity", "scaffold_path"}
    fields = text_fields | {"base_seed"}
    normalized: dict[str, dict[str, Any]] = {}
    for role in sorted(required):
        spec = selection[role]
        if (
            set(spec) != fields
            or not all(
                isinstance(spec.get(field), str) and str(spec[field]).strip()
                for field in text_fields
            )
            or not isinstance(spec.get("base_seed"), int)
            or isinstance(spec.get("base_seed"), bool)
        ):
            raise ValueError(f"invalid explicit preflight selection for {role}")
        normalized[role] = {field: spec[field] for field in sorted(fields)}
    expected_fidelity = {
        "smoke": "smoke",
        "baseline_a": "low_fidelity",
        "baseline_b": "low_fidelity",
        "ground_truth": "low_fidelity",
    }
    if any(normalized[role]["fidelity"] != expected for role, expected in expected_fidelity.items()):
        raise ValueError("preflight roles use an invalid fidelity")
    identity_fields = ("candidate_id", "block_id", "attempt_id")
    identities = {
        tuple(normalized[role][field] for field in identity_fields) for role in required
    }
    if len(identities) != len(required):
        raise ValueError("preflight roles must bind four distinct attempts")
    if not (
        normalized["smoke"]["candidate_id"]
        == normalized["baseline_a"]["candidate_id"]
        == normalized["baseline_b"]["candidate_id"]
    ):
        raise ValueError("smoke and both baseline roles must use the same candidate")
    if normalized["ground_truth"]["candidate_id"] == normalized["baseline_a"]["candidate_id"]:
        raise ValueError("ground-truth role must use a distinct ground-truth candidate")
    if normalized["baseline_a"]["base_seed"] == normalized["baseline_b"]["base_seed"]:
        raise ValueError("both baseline roles must pre-register distinct base seeds")
    return normalized


def _locked_preflight_role(
    workspace: CalibrationWorkspace,
    role: str,
    spec: Mapping[str, Any],
    split: Mapping[str, Any],
) -> dict[str, Any]:
    scaffold_source = Path(str(spec["scaffold_path"]))
    if not scaffold_source.is_absolute():
        scaffold_source = workspace.root / scaffold_source
    scaffold_path = workspace.bind_read_file(scaffold_source)
    scaffold_data = scaffold_path.read_bytes()
    scaffold = _read_json_object(scaffold_path)
    expected_mode = "ground_truth" if role == "ground_truth" else "baseline"
    if (
        scaffold.get("candidate_id") != spec["candidate_id"]
        or scaffold.get("mode") != expected_mode
        or not isinstance(scaffold.get("structural_cell"), str)
        or not scaffold.get("structural_cell")
    ):
        raise ValueError(f"preflight scaffold does not match role {role}")
    fidelity_key = "smoke" if role == "smoke" else "low_fidelity"
    selected_tasks = {
        domain: [
            str(item["task_id"])
            for item in items
            if role != "ground_truth" or int(item.get("action_count", 0)) > 0
        ]
        for domain, items in sorted(split[fidelity_key].items())
    }
    return {
        **dict(spec),
        "scaffold_resolved_relative": scaffold_path.relative_to(workspace.root).as_posix(),
        "scaffold_sha256": hashlib.sha256(scaffold_data).hexdigest(),
        "scaffold_mode": expected_mode,
        "structural_cell": scaffold["structural_cell"],
        "selected_tasks": selected_tasks,
        "repetitions": 1,
    }


def _valid_model_identities(value: object, expected_names: set[str]) -> bool:
    return bool(
        isinstance(value, Mapping)
        and set(value) == expected_names
        and all(
            isinstance(value[name], Mapping)
            and isinstance(value[name].get("digest"), str)
            and bool(value[name]["digest"])
            for name in expected_names
        )
    )


def _validate_preflight_selection_lock(value: Mapping[str, Any]) -> None:
    required = {
        "schema_version",
        "selection",
        "task_split_sha256",
        "static_snapshot_sha256",
        "execution_contract",
        "registration",
        "selection_lock_sha256",
    }
    unsigned = dict(value)
    declared = unsigned.pop("selection_lock_sha256", None)
    if (
        set(value) != required
        or declared != hashlib.sha256(_json_bytes(unsigned)).hexdigest()
        or not isinstance(value.get("selection"), Mapping)
        or not isinstance(value.get("execution_contract"), Mapping)
    ):
        raise ValueError("preflight selection lock is invalid")


def _preflight_unit_seed(
    base_seed: int, block_id: str, domain: str, task_id: str, repetition: int
) -> int:
    data = f"{base_seed}\0{block_id}\0{domain}\0{task_id}\0{repetition}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(data).digest()[:4], "big") & 0x7FFFFFFF


def _valid_runtime_identity(manifest: Mapping[str, Any]) -> bool:
    dependencies = manifest.get("runtime_dependencies")
    dependency_tree = manifest.get("runtime_dependency_tree")
    if (
        not isinstance(dependencies, Mapping)
        or not dependencies
        or not isinstance(dependency_tree, Mapping)
        or not isinstance(dependency_tree.get("sha256"), str)
        or not dependency_tree.get("sha256")
        or int(dependency_tree.get("file_count", 0)) <= 0
    ):
        return False
    dependency_hash = hashlib.sha256(
        json.dumps(
            dependencies, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()
    root = Path(str(manifest.get("tau2_root", "")))
    expected_python = root / ".venv" / (
        "Scripts/python.exe" if os.name == "nt" else "bin/python"
    )
    return bool(
        manifest.get("runtime_dependencies_sha256") == dependency_hash
        and manifest.get("runtime_dont_write_bytecode") is True
        and isinstance(manifest.get("runtime_pycache_prefix"), str)
        and bool(manifest["runtime_pycache_prefix"])
        and isinstance(manifest.get("runtime_python_version"), str)
        and bool(manifest["runtime_python_version"])
        and os.path.normcase(str(manifest.get("runtime_python")))
        == os.path.normcase(str(expected_python))
    )


def _execution_identity(manifest: Mapping[str, Any]) -> dict[str, Any]:
    fields = (
        "agent_model",
        "user_model",
        "evaluator_model",
        "model_identities",
        "max_steps",
        "timeout_seconds",
        "enforce_communication_protocol",
        "ollama_url",
        "tau2_root",
        "evaluator_lock_sha256",
        "runtime_python",
        "runtime_python_version",
        "runtime_dont_write_bytecode",
        "runtime_dependencies",
        "runtime_dependencies_sha256",
        "runtime_dependency_tree",
    )
    return {field: manifest.get(field) for field in fields}


def _preflight_outcome_identity_valid(
    outcomes: Sequence[Mapping[str, Any]],
    locked_role: Mapping[str, Any],
    execution_contract: Mapping[str, Any],
) -> bool:
    expected_keys = {
        (domain, task_id, repetition)
        for domain, task_ids in locked_role["selected_tasks"].items()
        for task_id in task_ids
        for repetition in range(locked_role["repetitions"])
    }
    actual_keys = {
        (
            str(item.get("domain")),
            str(item.get("task_id")),
            int(item.get("repetition", -1)),
        )
        for item in outcomes
    }
    if len(outcomes) != len(actual_keys) or actual_keys != expected_keys:
        return False
    for item in outcomes:
        status = item.get("execution_status")
        if status in {"completed", "infra_failure"}:
            expected_fields = _OUTCOME_COMMON_FIELDS | _OUTCOME_RAW_FIELDS
        elif status == "runner_failure":
            expected_fields = _OUTCOME_COMMON_FIELDS | _OUTCOME_RUNNER_FAILURE_FIELDS
        else:
            return False
        key = (
            str(item.get("domain")),
            str(item.get("task_id")),
            int(item.get("repetition", -1)),
        )
        if (
            set(item) != expected_fields
            or
            item.get("seed")
            != _preflight_unit_seed(
                locked_role["base_seed"], locked_role["block_id"], *key
            )
            or item.get("candidate_id") != locked_role["candidate_id"]
            or item.get("block_id") != locked_role["block_id"]
            or item.get("attempt_id") != locked_role["attempt_id"]
            or item.get("fidelity") != locked_role["fidelity"]
            or item.get("scaffold_sha256") != locked_role["scaffold_sha256"]
            or item.get("scaffold_mode") != locked_role["scaffold_mode"]
            or item.get("structural_cell") != locked_role["structural_cell"]
            or not isinstance(item.get("attempt_manifest_sha256"), str)
            or not item["attempt_manifest_sha256"]
            or item.get("agent_model") != execution_contract["agent_model"]
            or item.get("user_model") != execution_contract["user_model"]
            or item.get("evaluator_model") != execution_contract["evaluator_model"]
            or item.get("max_steps") != execution_contract["max_steps"]
            or item.get("timeout_seconds") != execution_contract["timeout_seconds"]
            or item.get("enforce_communication_protocol")
            != execution_contract["enforce_communication_protocol"]
            or not isinstance(item.get("success"), bool)
            or isinstance(item.get("wall_time_seconds"), bool)
            or not isinstance(item.get("wall_time_seconds"), (int, float))
            or not math.isfinite(float(item["wall_time_seconds"]))
            or float(item["wall_time_seconds"]) < 0
        ):
            return False
        reward = item.get("reward")
        if reward is not None and (
            isinstance(reward, bool)
            or not isinstance(reward, (int, float))
            or not math.isfinite(float(reward))
        ):
            return False
        if status == "runner_failure" and (
            item.get("success") is not False
            or reward is not None
            or item.get("termination_reason") is not None
            or not isinstance(item.get("error_type"), str)
            or not item["error_type"]
            or not isinstance(item.get("error_message"), str)
        ):
            return False
        if status != "runner_failure" and not isinstance(
            item.get("termination_reason"), str
        ):
            return False
    return True


def _short_task_identifier(value: object) -> str:
    readable = "".join(
        character if character.isascii() and character.isalnum() else "-"
        for character in str(value)
    )
    readable = "-".join(part for part in readable.split("-") if part) or "unit"
    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:10]
    return readable[:48].rstrip("-") + "-" + digest


def _expected_outcome_paths(outcome: Mapping[str, Any]) -> tuple[str, str]:
    prefix = (
        f"preflight/{outcome['candidate_id']}/{outcome['block_id']}/"
        f"{outcome['attempt_id']}/{outcome['fidelity']}/{outcome['domain']}/"
        f"{_short_task_identifier(outcome['task_id'])}-r{outcome['repetition']}"
    )
    raw_relative = prefix.replace("preflight/", "preflight/raw/", 1) + ".json"
    log_relative = prefix.replace("preflight/", "preflight/llm_logs/", 1)
    return raw_relative, log_relative


def _raw_reward(value: Mapping[str, Any]) -> float | None | object:
    reward_info = value.get("reward_info")
    if reward_info is None:
        return None
    if not isinstance(reward_info, Mapping):
        return _UNAVAILABLE
    reward = reward_info.get("reward")
    if isinstance(reward, bool) or not isinstance(reward, (int, float)):
        return _UNAVAILABLE
    return float(reward)


_UNAVAILABLE = object()


def _raw_outcome_matches(raw: Mapping[str, Any], outcome: Mapping[str, Any]) -> bool:
    reward = _raw_reward(raw)
    if reward is _UNAVAILABLE:
        return False
    outcome_reward = outcome.get("reward")
    rewards_match = (
        reward is None
        and outcome_reward is None
        or isinstance(reward, float)
        and isinstance(outcome_reward, (int, float))
        and not isinstance(outcome_reward, bool)
        and math.isclose(reward, float(outcome_reward), rel_tol=0.0, abs_tol=1e-12)
    )
    termination = raw.get("termination_reason")
    mechanical = {
        "user_error",
        "infrastructure_error",
        "context_window_exceeded",
        "unexpected_error",
        "timeout",
    }
    expected_status = (
        "infra_failure" if termination in mechanical or reward is None else "completed"
    )
    expected_success = bool(reward is not None and math.isclose(reward, 1.0))
    return bool(
        str(raw.get("task_id")) == str(outcome.get("task_id"))
        and raw.get("seed") == outcome.get("seed")
        and isinstance(termination, str)
        and termination == outcome.get("termination_reason")
        and rewards_match
        and outcome.get("execution_status") == expected_status
        and outcome.get("success") is expected_success
    )


def _outcome_assets_valid(
    workspace: CalibrationWorkspace, outcome: Mapping[str, Any]
) -> bool:
    try:
        expected_raw, expected_log = _expected_outcome_paths(outcome)
        raw_relative = outcome.get("raw_result_path")
        raw_hash = outcome.get("raw_result_sha256")
        requires_raw = outcome.get("execution_status") in {"completed", "infra_failure"}
        if requires_raw and (
            not isinstance(raw_relative, str) or not isinstance(raw_hash, str)
        ):
            return False
        if requires_raw and raw_relative != expected_raw:
            return False
        if not requires_raw and (raw_relative is not None or raw_hash is not None):
            return False
        if isinstance(raw_relative, str):
            raw_path = workspace.bind_read_file(workspace.root / Path(raw_relative))
            raw_data = raw_path.read_bytes()
            raw_value = _read_json_object(raw_path)
            scan = scan_secret_bytes(raw_data, environment_secrets())
            if (
                hashlib.sha256(raw_data).hexdigest() != raw_hash
                or scan.contains_possible_credential
                or _contains_sensitive_json(raw_value)
                or not _raw_outcome_matches(raw_value, outcome)
            ):
                return False

        log_relative = outcome.get("llm_log_path")
        expected_manifest = outcome.get("llm_log_manifest")
        if (
            not isinstance(log_relative, str)
            or log_relative != expected_log
            or not isinstance(expected_manifest, Mapping)
        ):
            return False
        log_root = workspace.target(*Path(log_relative).parts)
        if not log_root.is_dir() or _is_reparse_point(log_root):
            return False
        files: list[dict[str, Any]] = []
        for path in sorted(log_root.iterdir(), key=lambda item: item.name):
            if _is_reparse_point(path) or path.is_symlink() or not path.is_file():
                return False
            data = path.read_bytes()
            if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
                return False
            decoded = data.decode("utf-8", errors="strict")
            value = json.loads(decoded)
            scan = scan_secret_bytes(data, environment_secrets())
            if scan.contains_possible_credential or _contains_sensitive_json(value):
                return False
            files.append(
                {
                    "name": path.name,
                    "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
        return dict(expected_manifest) == {"file_count": len(files), "files": files}
    except (FileNotFoundError, OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return False


def _event_envelope_valid(event: Mapping[str, Any], *, kind: str) -> bool:
    if set(event) != _EVENT_FIELDS or event.get("kind") != kind:
        return False
    unsigned = dict(event)
    declared = unsigned.pop("event_integrity_sha256", None)
    return bool(
        event.get("schema_version") == CALIBRATION_SCHEMA_VERSION
        and event.get("phase") == "preflight"
        and isinstance(event.get("event_id"), str)
        and declared == hashlib.sha256(_json_bytes(unsigned)).hexdigest()
    )


def _audit_contract_valid(
    audit: Mapping[str, Any],
    locked_role: Mapping[str, Any],
    execution_contract: Mapping[str, Any],
    task_split_sha256: str,
    expected_count: int,
) -> bool:
    expected_manifest_path = (
        f"preflight/attempts/{locked_role['candidate_id']}/"
        f"{locked_role['block_id']}/{locked_role['attempt_id']}/manifest.json"
    )
    budget = audit.get("budget_parity")
    return bool(
        set(audit) == _AUDIT_FIELDS
        and audit.get("candidate_id") == locked_role["candidate_id"]
        and audit.get("block_id") == locked_role["block_id"]
        and audit.get("attempt_id") == locked_role["attempt_id"]
        and audit.get("fidelity") == locked_role["fidelity"]
        and audit.get("scaffold_sha256") == locked_role["scaffold_sha256"]
        and audit.get("scaffold_mode") == locked_role["scaffold_mode"]
        and audit.get("structural_cell") == locked_role["structural_cell"]
        and isinstance(audit.get("attempt_manifest_sha256"), str)
        and bool(audit["attempt_manifest_sha256"])
        and audit.get("attempt_manifest_path") == expected_manifest_path
        and isinstance(audit.get("evaluator_lock_valid_before"), bool)
        and isinstance(audit.get("evaluator_lock_valid_after"), bool)
        and audit.get("candidate_write_scope") == "declarative_scaffold_only"
        and audit.get("evaluator_model") == execution_contract["evaluator_model"]
        and audit.get("base_seed") == locked_role["base_seed"]
        and audit.get("task_split_sha256") == task_split_sha256
        and audit.get("scheduled_unit_count") == expected_count
        and isinstance(budget, Mapping)
        and set(budget)
        == {"max_steps", "timeout_seconds", "enforce_communication_protocol"}
        and budget.get("max_steps") == execution_contract["max_steps"]
        and budget.get("timeout_seconds") == execution_contract["timeout_seconds"]
        and budget.get("enforce_communication_protocol")
        == execution_contract["enforce_communication_protocol"]
    )


def _contains_sensitive_json(value: object) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key).upper()
            if isinstance(item, str) and len(item) >= 8 and any(
                token in key_text for token in ("API_KEY", "TOKEN", "SECRET", "PASSWORD")
            ):
                return True
            if _contains_sensitive_json(item):
                return True
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return any(_contains_sensitive_json(item) for item in value)
    return False


def _attempt_manifest_for_audit(
    workspace: CalibrationWorkspace, audit: Mapping[str, Any]
) -> dict[str, Any]:
    relative = audit.get("attempt_manifest_path")
    expected = audit.get("attempt_manifest_sha256")
    if not isinstance(relative, str) or not isinstance(expected, str):
        return {}
    try:
        path = workspace.bind_read_file(workspace.root / Path(relative))
        manifest = _read_json_object(path)
    except (FileNotFoundError, ValueError):
        return {}
    unsigned = dict(manifest)
    declared = unsigned.pop("manifest_sha256", None)
    if (
        set(manifest) != _ATTEMPT_MANIFEST_FIELDS
        or manifest.get("schema_version") != 1
        or declared != expected
        or hashlib.sha256(_json_bytes(unsigned)).hexdigest() != expected
    ):
        return {}
    return manifest


def _payload(event: Mapping[str, Any]) -> Mapping[str, Any]:
    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        raise ValueError(f"calibration event has no object payload: {event.get('event_id')}")
    return payload


def _read_json_object(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
        raise ValueError(f"calibration JSON must be UTF-8 without BOM and LF-only: {path}")
    try:
        value = json.loads(data.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid calibration JSON: {path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"calibration JSON root must be an object: {path}")
    return value


def _atomic_replace(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _assert_descendant(path: Path, root: Path) -> None:
    path_text = os.path.normcase(os.path.abspath(path))
    root_text = os.path.normcase(os.path.abspath(root))
    try:
        common = os.path.commonpath([path_text, root_text])
    except ValueError as error:
        raise ValueError(f"path is outside calibration workspace: {path}") from error
    if common != root_text:
        raise ValueError(f"path is outside calibration workspace: {path}")


def _is_descendant(path: Path, root: Path) -> bool:
    path_text = os.path.normcase(os.path.abspath(path))
    root_text = os.path.normcase(os.path.abspath(root))
    try:
        return os.path.commonpath([path_text, root_text]) == root_text
    except ValueError:
        return False


def _reject_reparse_chain(root: Path, target: Path) -> None:
    _assert_descendant(target, root)
    relative = Path(os.path.abspath(target)).relative_to(Path(os.path.abspath(root)))
    current = root
    if _path_exists(current) and _is_reparse_point(current):
        raise ValueError(f"calibration workspace must not be a reparse point: {current}")
    for part in relative.parts:
        current = current / part
        if _path_exists(current) and _is_reparse_point(current):
            raise ValueError(f"calibration path uses a reparse point: {current}")


def _path_exists(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError):
        return path.is_symlink()
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _reject_secret_data(data: bytes, label: str) -> None:
    scan = scan_secret_bytes(data, environment_secrets())
    if scan.environment_secret or scan.heuristic_pattern:
        raise ValueError(f"{label} contains a possible credential")
