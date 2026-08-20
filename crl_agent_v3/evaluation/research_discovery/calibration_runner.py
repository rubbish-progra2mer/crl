"""CRL 科研搜索奖励校准的隔离工作区与阶段运行器。"""

from __future__ import annotations

import hashlib
import json
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
            output.append(_read_json_object(path))
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
        "tau2": release,
        "isolated_release": isolated_release,
        "models": models,
        "evaluator_lock": lock_check,
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
    return report


def summarize_tau2_preflight(
    workspace: CalibrationWorkspace,
    selection: Mapping[str, Mapping[str, str]],
) -> dict[str, Any]:
    """按显式 attempt 选择汇总 τ² 预检；不猜测哪个历史尝试有效。"""

    required = {"smoke", "baseline_a", "baseline_b", "ground_truth"}
    if set(selection) != required:
        raise ValueError(
            f"preflight selection must contain exactly {sorted(required)}"
        )
    expected_units = {
        "smoke": 10,
        "baseline_a": 24,
        "baseline_b": 24,
        "ground_truth": 24,
    }
    all_events = workspace.read_events("preflight")
    attempts: dict[str, dict[str, Any]] = {}
    for role in sorted(required):
        spec = selection[role]
        spec_required = {"candidate_id", "block_id", "attempt_id", "fidelity"}
        if set(spec) != spec_required or not all(
            isinstance(spec.get(field), str) and str(spec[field]).strip()
            for field in spec_required
        ):
            raise ValueError(f"invalid explicit preflight selection for {role}")
        outcomes = [
            _payload(event)
            for event in all_events
            if event.get("kind") == "tau2_outcome"
            and all(_payload(event).get(field) == spec[field] for field in spec_required)
        ]
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
        audits = [
            _payload(event)
            for event in all_events
            if event.get("kind") == "tau2_block_audit"
            and all(_payload(event).get(field) == spec[field] for field in spec_required)
        ]
        audit = audits[-1] if audits else {}
        expected_count = audit.get("scheduled_unit_count", expected_units[role])
        if not isinstance(expected_count, int) or expected_count < 1:
            raise ValueError(f"invalid scheduled unit count in selected {role} audit")
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
    summary = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "phase": "preflight",
        "selection": {role: dict(selection[role]) for role in sorted(selection)},
        "attempts": attempts,
        "gate": {
            "passed": all(checks.values()),
            "checks": checks,
            "scientific_delivery_authority": False,
        },
    }
    digest = hashlib.sha256(_json_bytes(summary)).hexdigest()[:16]
    workspace.write_json_once(f"preflight/summaries/tau2-{digest}.json", summary)
    return summary


def summarize_pilot(workspace: CalibrationWorkspace) -> dict[str, Any]:
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
    workspace.write_json_once(f"temporal/validations/{packet_hash[:16]}.json", report)
    return report


def build_calibration_report(workspace: CalibrationWorkspace) -> dict[str, Any]:
    split = _read_json_object(workspace.target("frozen_task_split.json"))
    validate_frozen_task_split(split)
    pilot = _latest_json(workspace.target("pilot", "summaries"))
    confirm = _latest_json(workspace.target("confirm", "summaries"))
    temporal = _latest_json(workspace.target("temporal", "validations"))
    report = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "generated_at": _utc_now(),
        "task_split_sha256": split["split_sha256"],
        "pilot": pilot,
        "confirm": confirm,
        "temporal": temporal,
        "interpretation": {
            "scope": "search-policy calibration only",
            "automatic_candidate_elimination": False,
            "automatic_delivery": False,
            "automatic_novelty_claim": False,
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
    return {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "benchmark": release,
        "file_count": len(files),
        "files": files,
        "candidate_write_scope": "external isolated agent scaffold only",
    }


def verify_evaluator_lock(
    tau2_root: str | Path, lock: Mapping[str, Any]
) -> dict[str, Any]:
    root = Path(tau2_root)
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
        "valid": not missing and not changed and not added,
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
科学配对效应中排除并单独报告。贝叶斯自助法报告 `P(Δ>0)`、`P(Δ>0.05)` 和
`Q0.10(Δ)`，三者不求和。下一实验按单位预期成本的 Beta-Bernoulli 预测熵下降选择。

## τ² 层

- 现实层冻结 τ² v1.0.1；Agent 为 `qwen3:8b`，用户模拟器为 `qwen2.5:7b`，
  `qwen3.5:9b` 只作预检失败后的同档增强复核。
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
- 高保真样本至少 36 个候选，并跨低保真后验四分位与结构单元分层抽取。

## 小试与确认

进入小试前，smoke 必须 10/10 完整且无机械失败；两次独立低保真基线各 24 题，
机械失败率均不高于 5%、科学通过率均在 10%—80%，两次通过率相差不超过 10 个
百分点；同一低保真集里官方 `llm_agent_gt.check_valid_task` 支持的子集上，ground-truth
Agent 通过率至少 70%。不支持 ground-truth 的任务不进入该上界分母，也不算模型失败。
所有结果尝试由调用者显式绑定，脚本不从历史尝试中猜选。任何门槛失败只阻断小试，
不构成科研反证。

小试为 2 个配对块、每组 4 代、每代 6 个候选，第一代三组共享。只有实现率不低于
60%、高保真同时含通过与失败、块留一桥接 Brier 比基准率改善至少 10%、斜率为正、
顶部四分位优于底部四分位且隔离检查通过，才自动进入 8 个新配对块的确认实验。

确认成功要求：约束组在至少 7/8 块优于启发式组；块优势中位数至少 5 个百分点；
至少一个候选 `P(Δ>0.05)>=0.95` 且 `Q0.10(Δ)>0`；领域退化约束、结构多样性与
评价器隔离均通过。这只支持是否采用搜索策略，不支持具体科研 Idea 的论文结论。

## 时间洁净层

时间洁净层使用 `qwen2.5:7b` 与 τ² v0.2.1，只允许 2025 年及以前材料；2026 年机制
P072、P074、P087 保持留出。Codex 现实层只作探索性结果。所有大语言模型辅助评审
必须标为 `llm_auxiliary` 与 `auxiliary_only`，不得进入主要科学结论。
"""


def render_calibration_report(report: Mapping[str, Any]) -> str:
    pilot = report.get("pilot")
    confirm = report.get("confirm")
    temporal = report.get("temporal")
    lines = [
        "# CRL 科研搜索奖励校准报告",
        "",
        "本报告只评价搜索策略校准，不评价任何具体候选的新颖性或交付资格。",
        "",
        "## 阶段状态",
        "",
        f"- 小试：{_phase_status(pilot)}",
        f"- 确认：{_phase_status(confirm)}",
        f"- 时间洁净层：{_phase_status(temporal)}",
        "",
        "## 权力边界",
        "",
        "- 自动淘汰科研候选：否",
        "- 自动认证新颖性：否",
        "- 自动形成 Delivery / No-Delivery：否",
    ]
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
        root / "src" / "tau2" / "evaluator",
        root / "src" / "tau2" / "runner",
        root / "src" / "tau2" / "data_model",
        root / "src" / "tau2" / "domains",
        root / "data" / "tau2" / "domains",
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
            directory_names[:] = [
                name for name in directory_names if name not in _SKIPPED_RELEASE_DIRS
            ]
            for name in file_names:
                path = current / name
                if _is_reparse_point(path):
                    raise ValueError(f"τ² evaluator file is a reparse point: {path}")
                files.append(path)
    return sorted(set(files), key=lambda path: path.relative_to(root).as_posix())


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


def _latest_json(directory: Path) -> dict[str, Any] | None:
    if not directory.is_dir():
        return None
    if _is_reparse_point(directory):
        raise ValueError(f"calibration summary directory is a reparse point: {directory}")
    paths = list(directory.glob("*.json"))
    for path in paths:
        if _is_reparse_point(path):
            raise ValueError(f"calibration summary is a reparse point: {path}")
    paths.sort(key=lambda path: path.stat().st_mtime_ns)
    return None if not paths else _read_json_object(paths[-1])


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
