"""隔离执行冻结 τ² 任务的校准适配器。

候选只能提供声明式 JSON scaffold；本模块把它转换为固定的 LLMAgent 子类，
避免候选代码直接进入评价器进程。评价器在执行前后都与冻结锁比较。
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import os
import shutil
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any, Mapping, Sequence

from crl_v3.decision import (
    environment_secrets,
    redact_secrets,
    scan_secret_bytes,
)

from .calibration import validate_frozen_task_split

from .calibration_runner import (
    CalibrationWorkspace,
    _is_reparse_point,
    _validate_preflight_selection_lock,
    query_ollama_model_identities,
    verify_evaluator_lock,
)


SCAFFOLD_SCHEMA_VERSION = 1
SCAFFOLD_MODES = ("baseline", "custom", "ground_truth")
FIDELITIES = ("smoke", "low_fidelity", "high_fidelity")


def load_agent_scaffold(
    workspace: CalibrationWorkspace, path: str | Path
) -> dict[str, Any]:
    source = workspace.bind_read_file(path)
    data = source.read_bytes()
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
        raise ValueError("agent scaffold must be UTF-8 without BOM and LF-only")
    try:
        value = json.loads(data.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid agent scaffold JSON: {source}") from error
    if not isinstance(value, dict):
        raise ValueError("agent scaffold root must be an object")
    required = {"schema_version", "candidate_id", "mode", "structural_cell"}
    optional = {"instruction", "notes"}
    extras = set(value) - required - optional
    missing = required - set(value)
    if extras or missing:
        raise ValueError(
            f"agent scaffold fields mismatch; missing={sorted(missing)}, extra={sorted(extras)}"
        )
    if value["schema_version"] != SCAFFOLD_SCHEMA_VERSION:
        raise ValueError("unsupported agent scaffold schema")
    for field in ("candidate_id", "structural_cell"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise ValueError(f"agent scaffold {field} must be non-empty text")
    mode = value["mode"]
    if mode not in SCAFFOLD_MODES:
        raise ValueError(f"unsupported scaffold mode: {mode}")
    instruction = value.get("instruction")
    if mode == "custom":
        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError("custom scaffold must provide a non-empty instruction")
        if len(instruction) > 12_000:
            raise ValueError("custom scaffold instruction exceeds 12000 characters")
    elif instruction not in (None, ""):
        raise ValueError("baseline and ground_truth scaffolds cannot override instruction")
    value["scaffold_sha256"] = hashlib.sha256(data).hexdigest()
    value["_source_path"] = str(source)
    return value


def run_tau2_block(
    workspace: CalibrationWorkspace,
    *,
    tau2_root: str | Path,
    phase: str,
    fidelity: str,
    block_id: str,
    attempt_id: str,
    scaffold_path: str | Path,
    agent_model: str,
    user_model: str,
    evaluator_model: str = "qwen2.5:7b",
    domains: Sequence[str] | None = None,
    repetitions: int | None = None,
    base_seed: int = 20260819,
    ollama_url: str = "http://127.0.0.1:11434",
    max_steps: int = 30,
    timeout_seconds: float = 120.0,
) -> dict[str, Any]:
    """顺序运行一组冻结任务，并将每个任务—种子单元保存为幂等事件。"""

    if os.name == "nt" and sys.flags.utf8_mode == 0:
        raise RuntimeError(
            "τ² execution on Windows requires Python UTF-8 mode; "
            "use tools/run_tau2_calibration_block.py"
        )
    if environment_secrets():
        raise RuntimeError("τ² execution refuses ambient sensitive environment variables")
    if not sys.dont_write_bytecode:
        raise RuntimeError("τ² execution requires Python bytecode writes to be disabled")
    if sys.pycache_prefix is None:
        raise RuntimeError("τ² execution requires an isolated empty bytecode read prefix")
    bytecode_prefix = Path(sys.pycache_prefix)
    if bytecode_prefix.exists() and any(bytecode_prefix.iterdir()):
        raise RuntimeError("τ² bytecode read prefix must be empty")
    if phase not in ("preflight", "pilot", "confirm"):
        raise ValueError("τ² block phase must be preflight, pilot, or confirm")
    if fidelity not in FIDELITIES:
        raise ValueError(f"unsupported τ² fidelity: {fidelity}")
    if not isinstance(block_id, str) or not block_id.strip():
        raise ValueError("block_id must be non-empty text")
    if not isinstance(attempt_id, str) or not attempt_id.strip():
        raise ValueError("attempt_id must be non-empty text")
    if max_steps < 1 or timeout_seconds <= 0:
        raise ValueError("τ² execution budget must be positive")

    for label, value in (
        ("block_id", block_id),
        ("attempt_id", attempt_id),
    ):
        _validate_path_component(value, label)

    root = Path(os.path.abspath(tau2_root)).resolve(strict=True)
    runtime_root = workspace.target("preflight", "runtime").resolve(strict=True)
    common_root = os.path.commonpath((str(root), str(runtime_root)))
    if os.path.normcase(common_root) != os.path.normcase(str(runtime_root)):
        raise ValueError("τ² root must stay inside the calibration preflight runtime")
    expected_python = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if os.path.normcase(str(Path(sys.executable).resolve(strict=True))) != os.path.normcase(
        str(expected_python.resolve(strict=True))
    ):
        raise RuntimeError(f"τ² execution requires its isolated interpreter: {expected_python}")
    lock_path = workspace.target("preflight", "evaluator_lock.json")
    evaluator_lock = _read_json(lock_path)
    lock_before = verify_evaluator_lock(root, evaluator_lock)
    if not lock_before["valid"]:
        raise ValueError(f"τ² evaluator lock failed before execution: {lock_before}")
    split = _read_json(workspace.target("frozen_task_split.json"))
    validate_frozen_task_split(split)
    _recover_stale_staging(workspace, phase)
    scaffold = load_agent_scaffold(workspace, scaffold_path)
    _validate_path_component(scaffold["candidate_id"], "candidate_id")
    selected = _selected_tasks(
        split,
        fidelity,
        domains,
        require_expected_actions=scaffold["mode"] == "ground_truth",
    )
    if repetitions is None:
        repetitions = int(split["repetitions"][fidelity])
    if repetitions < 1:
        raise ValueError("repetitions must be positive")

    attempt_manifest_relative = (
        f"{phase}/attempts/{scaffold['candidate_id']}/{block_id}/{attempt_id}/manifest.json"
    )
    attempt_manifest = _build_attempt_manifest(
        root=root,
        evaluator_lock=evaluator_lock,
        split=split,
        scaffold=scaffold,
        phase=phase,
        fidelity=fidelity,
        block_id=block_id,
        attempt_id=attempt_id,
        selected=selected,
        repetitions=repetitions,
        base_seed=base_seed,
        agent_model=agent_model,
        user_model=user_model,
        evaluator_model=evaluator_model,
        ollama_url=ollama_url,
        max_steps=max_steps,
        timeout_seconds=timeout_seconds,
    )
    _enforce_locked_preflight_contract(workspace, attempt_manifest)
    workspace.write_json_once(attempt_manifest_relative, attempt_manifest)
    attempt_manifest_sha256 = str(attempt_manifest["manifest_sha256"])

    existing_events = workspace.read_events(phase)
    existing_by_id = {
        str(item.get("event_id")): item
        for item in existing_events
        if isinstance(item.get("event_id"), str)
    }
    existing_ids = set(existing_by_id)
    tau2 = _import_tau2(root)
    tau2["configure_nl_evaluator"](
        _ollama_model(evaluator_model), _evaluator_llm_args(ollama_url)
    )
    agent_name = _register_agent(tau2, scaffold)
    completed = 0
    resumed = 0
    mechanical = 0
    scientific_failures = 0
    scientific_passes = 0
    for domain, task_ids in selected.items():
        tasks = tau2["get_tasks"](
            task_set_name=domain,
            task_split_name="base",
            task_ids=task_ids,
        )
        tasks_by_id = {str(task.id): task for task in tasks}
        for task_id in task_ids:
            task = tasks_by_id[task_id]
            for repetition in range(repetitions):
                event_id = _event_id(
                    scaffold["candidate_id"],
                    block_id,
                    attempt_id,
                    fidelity,
                    domain,
                    task_id,
                    repetition,
                )
                if event_id in existing_ids:
                    existing_payload = existing_by_id[event_id].get("payload")
                    if (
                        not isinstance(existing_payload, Mapping)
                        or existing_payload.get("attempt_manifest_sha256")
                        != attempt_manifest_sha256
                        or not _committed_outcome_assets_valid(workspace, existing_payload)
                    ):
                        raise ValueError(
                            "existing τ² unit is not bound to the current manifest and "
                            f"intact assets: {event_id}"
                        )
                    resumed += 1
                    existing_status = existing_payload.get("execution_status")
                    if existing_status != "completed":
                        mechanical += 1
                    elif existing_payload.get("success") is True:
                        scientific_passes += 1
                    else:
                        scientific_failures += 1
                    continue
                seed = _unit_seed(base_seed, block_id, domain, task_id, repetition)
                started = time.perf_counter()
                raw_relative = (
                    f"{phase}/raw/{scaffold['candidate_id']}/{block_id}/{attempt_id}/"
                    f"{fidelity}/{domain}/{_short_identifier(task_id)}-r{repetition}.json"
                )
                log_relative = (
                    f"{phase}/llm_logs/{scaffold['candidate_id']}/{block_id}/{attempt_id}/"
                    f"{fidelity}/{domain}/{_short_identifier(task_id)}-r{repetition}"
                )
                final_log_path = workspace.target(*Path(log_relative).parts)
                final_raw_path = workspace.target(*Path(raw_relative).parts)
                _quarantine_orphaned_unit(
                    workspace,
                    phase=phase,
                    event_id=event_id,
                    raw_path=final_raw_path,
                    log_path=final_log_path,
                )
                staging_root = workspace.target(phase, "staging")
                staging_root.mkdir(exist_ok=True)
                stage_root = Path(
                    tempfile.mkdtemp(
                        prefix=(
                            "crl-tau2-"
                            + _safe_identifier(event_id)[:32]
                            + "-"
                            + hashlib.sha256(event_id.encode("utf-8")).hexdigest()[:12]
                            + "-"
                        ),
                        dir=staging_root,
                    )
                )
                log_path = stage_root / "logs"
                log_path.mkdir()
                tau2["set_llm_log_dir"](log_path)
                tau2["set_llm_log_mode"]("all")
                raw: dict[str, Any] | None = None
                try:
                    try:
                        config = tau2["TextRunConfig"](
                            domain=domain,
                            agent=agent_name,
                            user="user_simulator",
                            llm_agent=_ollama_model(agent_model),
                            llm_args_agent=_llm_args(ollama_url),
                            llm_user=_ollama_model(user_model),
                            llm_args_user=_llm_args(ollama_url),
                            max_steps=max_steps,
                            max_errors=10,
                            timeout=timeout_seconds,
                            seed=seed,
                            enforce_communication_protocol=False,
                        )
                        simulation = tau2["run_single_task"](
                            config,
                            task,
                            seed=seed,
                            save_dir=None,
                            verbose_logs=False,
                            auto_review=False,
                        )
                        raw = simulation.model_dump(mode="json")
                        termination = str(simulation.termination_reason.value)
                        reward = (
                            None
                            if simulation.reward_info is None
                            else float(simulation.reward_info.reward)
                        )
                        status = classify_tau2_execution(termination, reward)
                        success = bool(reward is not None and math.isclose(reward, 1.0))
                        payload = {
                            **_attempt_identity_payload(
                                scaffold,
                                block_id=block_id,
                                attempt_id=attempt_id,
                                fidelity=fidelity,
                                manifest_sha256=attempt_manifest_sha256,
                            ),
                            "domain": domain,
                            "task_id": task_id,
                            "repetition": repetition,
                            "seed": seed,
                            "execution_status": status,
                            "success": success,
                            "reward": reward,
                            "termination_reason": termination,
                            "wall_time_seconds": time.perf_counter() - started,
                        }
                    except Exception as error:
                        status = "runner_failure"
                        success = False
                        reward = None
                        payload = {
                            **_attempt_identity_payload(
                                scaffold,
                                block_id=block_id,
                                attempt_id=attempt_id,
                                fidelity=fidelity,
                                manifest_sha256=attempt_manifest_sha256,
                            ),
                            "domain": domain,
                            "task_id": task_id,
                            "repetition": repetition,
                            "seed": seed,
                            "execution_status": status,
                            "success": False,
                            "reward": None,
                            "termination_reason": None,
                            "wall_time_seconds": time.perf_counter() - started,
                            "error_type": type(error).__name__,
                            "error_message": _safe_error_message(error),
                        }
                    payload.update(
                        {
                            "agent_model": agent_model,
                            "user_model": user_model,
                            "evaluator_model": evaluator_model,
                            "max_steps": max_steps,
                            "timeout_seconds": timeout_seconds,
                            "enforce_communication_protocol": False,
                            "llm_log_path": log_relative,
                            "llm_log_manifest": _log_manifest(log_path),
                        }
                    )
                    if raw is not None:
                        workspace.write_json_once(raw_relative, raw)
                        payload["raw_result_path"] = raw_relative
                        payload["raw_result_sha256"] = hashlib.sha256(
                            final_raw_path.read_bytes()
                        ).hexdigest()
                    _publish_log_directory(log_path, final_log_path)
                    workspace.record_event(
                        phase,
                        {
                            "event_id": event_id,
                            "kind": "tau2_outcome",
                            "payload": payload,
                        },
                    )
                finally:
                    if stage_root.exists():
                        shutil.rmtree(stage_root)
                    if stage_root.exists():
                        raise RuntimeError(f"failed to remove τ² staging directory: {stage_root}")
                existing_ids.add(event_id)
                completed += 1
                if status != "completed":
                    mechanical += 1
                elif success:
                    scientific_passes += 1
                else:
                    scientific_failures += 1

    lock_after = verify_evaluator_lock(root, evaluator_lock)
    audit_id = _event_id(
        scaffold["candidate_id"],
        block_id,
        attempt_id,
        fidelity,
        "audit",
        "evaluator",
        0,
    )
    if audit_id in existing_ids:
        audit_payload = existing_by_id[audit_id].get("payload")
        if (
            not isinstance(audit_payload, Mapping)
            or audit_payload.get("attempt_manifest_sha256")
            != attempt_manifest_sha256
        ):
            raise ValueError("existing τ² audit is not bound to the current attempt manifest")
    else:
        workspace.record_event(
            phase,
            {
                "event_id": audit_id,
                "kind": "tau2_block_audit",
                "payload": {
                    **_attempt_identity_payload(
                        scaffold,
                        block_id=block_id,
                        attempt_id=attempt_id,
                        fidelity=fidelity,
                        manifest_sha256=attempt_manifest_sha256,
                    ),
                    "attempt_manifest_path": attempt_manifest_relative,
                    "evaluator_lock_valid_before": lock_before["valid"],
                    "evaluator_lock_valid_after": lock_after["valid"],
                    "candidate_write_scope": "declarative_scaffold_only",
                    "evaluator_model": evaluator_model,
                    "base_seed": base_seed,
                    "task_split_sha256": split["split_sha256"],
                    "scheduled_unit_count": sum(len(ids) for ids in selected.values())
                    * repetitions,
                    "budget_parity": {
                        "max_steps": max_steps,
                        "timeout_seconds": timeout_seconds,
                        "enforce_communication_protocol": False,
                    },
                },
            },
        )
    if not lock_after["valid"]:
        raise RuntimeError(f"τ² evaluator changed during execution: {lock_after}")
    return {
        "candidate_id": scaffold["candidate_id"],
        "block_id": block_id,
        "attempt_id": attempt_id,
        "fidelity": fidelity,
        "scheduled_unit_count": sum(len(ids) for ids in selected.values()) * repetitions,
        "newly_completed_unit_count": completed,
        "resumed_unit_count": resumed,
        "mechanical_failure_count": mechanical,
        "scientific_pass_count": scientific_passes,
        "scientific_failure_count": scientific_failures,
        "evaluator_lock_valid": lock_after["valid"],
        "evaluator_model": evaluator_model,
        "scientific_delivery_authority": False,
    }


def _import_tau2(root: Path) -> dict[str, Any]:
    source = root / "src"
    if not source.is_dir():
        raise FileNotFoundError(f"τ² source directory is missing: {source}")
    loaded = sys.modules.get("tau2")
    if loaded is not None:
        loaded_path = Path(getattr(loaded, "__file__", "")).resolve()
        if source.resolve() not in loaded_path.parents:
            raise RuntimeError(f"another τ² installation is already imported: {loaded_path}")
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))
    from tau2.agent.llm_agent import AGENT_INSTRUCTION, LLMAgent
    from tau2.data_model.simulation import TextRunConfig
    from tau2.registry import registry
    from tau2.runner.batch import run_single_task
    from tau2.runner.helpers import get_tasks
    import tau2.evaluator.evaluator_nl_assertions as nl_assertions
    from tau2.utils.llm_utils import set_llm_log_dir, set_llm_log_mode
    from loguru import logger

    logger.remove()
    logger.add(sys.stderr, level="ERROR")

    def configure_nl_evaluator(model: str, llm_args: Mapping[str, Any]) -> None:
        nl_assertions.DEFAULT_LLM_NL_ASSERTIONS = model
        nl_assertions.DEFAULT_LLM_NL_ASSERTIONS_ARGS = dict(llm_args)

    return {
        "AGENT_INSTRUCTION": AGENT_INSTRUCTION,
        "LLMAgent": LLMAgent,
        "TextRunConfig": TextRunConfig,
        "registry": registry,
        "run_single_task": run_single_task,
        "get_tasks": get_tasks,
        "configure_nl_evaluator": configure_nl_evaluator,
        "set_llm_log_dir": set_llm_log_dir,
        "set_llm_log_mode": set_llm_log_mode,
    }


def _register_agent(tau2: Mapping[str, Any], scaffold: Mapping[str, Any]) -> str:
    mode = scaffold["mode"]
    if mode == "baseline":
        return "llm_agent"
    if mode == "ground_truth":
        return "llm_agent_gt"
    instruction = str(scaffold["instruction"]).strip()
    llm_agent = tau2["LLMAgent"]

    class DeclarativeCalibrationAgent(llm_agent):
        @property
        def system_prompt(self) -> str:
            return (
                "<instructions>\n"
                + instruction
                + "\n</instructions>\n<policy>\n"
                + self.domain_policy
                + "\n</policy>"
            )

    def factory(tools, domain_policy, **kwargs):
        return DeclarativeCalibrationAgent(
            tools=tools,
            domain_policy=domain_policy,
            llm=kwargs.get("llm"),
            llm_args=kwargs.get("llm_args"),
        )

    name = "calibration_" + str(scaffold["scaffold_sha256"])[:16]
    if tau2["registry"].get_agent_factory(name) is None:
        tau2["registry"].register_agent_factory(factory, name)
    return name


def _selected_tasks(
    split: Mapping[str, Any],
    fidelity: str,
    domains: Sequence[str] | None,
    *,
    require_expected_actions: bool = False,
) -> dict[str, list[str]]:
    section = split.get(fidelity)
    if not isinstance(section, Mapping):
        raise ValueError(f"task split is missing {fidelity}")
    allowed = tuple(section)
    requested = allowed if domains is None else tuple(domains)
    unknown = set(requested) - set(allowed)
    if unknown:
        raise ValueError(f"domains are unavailable for {fidelity}: {sorted(unknown)}")
    output: dict[str, list[str]] = {}
    for domain in requested:
        tasks = section.get(domain)
        if not isinstance(tasks, list):
            raise ValueError(f"invalid frozen task list for {fidelity}/{domain}")
        output[domain] = [
            str(item["task_id"])
            for item in tasks
            if not require_expected_actions or int(item.get("action_count", 0)) > 0
        ]
    return output


def classify_tau2_execution(termination: str, reward: float | None) -> str:
    """把墙钟/基础设施终止与可比较预算内的 Agent 失败分开。"""

    mechanical_terminations = {
        "user_error",
        "infrastructure_error",
        "context_window_exceeded",
        "unexpected_error",
        "timeout",
    }
    if termination in mechanical_terminations or reward is None:
        return "infra_failure"
    return "completed"


def windows_utf8_subprocess_environment(
    environment: Mapping[str, str], *, os_name: str, utf8_mode: int
) -> dict[str, str] | None:
    """为 Windows 启动器构造强制 UTF-8 的子进程环境。"""

    if os_name != "nt" or utf8_mode != 0:
        return None
    updated = dict(environment)
    updated["PYTHONUTF8"] = "1"
    updated["PYTHONIOENCODING"] = "utf-8"
    return updated


def _ollama_model(name: str) -> str:
    return name if name.startswith("ollama") else "ollama_chat/" + name


def _llm_args(ollama_url: str) -> dict[str, Any]:
    return {
        "temperature": 0.0,
        "num_retries": 1,
        "api_base": ollama_url.rstrip("/"),
        "max_tokens": 1024,
        "timeout": 120.0,
        "think": False,
    }


def _evaluator_llm_args(ollama_url: str) -> dict[str, Any]:
    """为只接受 JSON 的官方 NL_ASSERTION 评价调用启用 Ollama JSON 模式。"""

    arguments = _llm_args(ollama_url)
    arguments["response_format"] = {"type": "json_object"}
    return arguments


def _unit_seed(
    base_seed: int, block_id: str, domain: str, task_id: str, repetition: int
) -> int:
    data = f"{base_seed}\0{block_id}\0{domain}\0{task_id}\0{repetition}".encode(
        "utf-8"
    )
    return int.from_bytes(hashlib.sha256(data).digest()[:4], "big") & 0x7FFFFFFF


def _event_id(
    candidate_id: str,
    block_id: str,
    attempt_id: str,
    fidelity: str,
    domain: str,
    task_id: str,
    repetition: int,
) -> str:
    readable = "-".join(
        _safe_identifier(value)
        for value in (
            candidate_id,
            block_id,
            attempt_id,
            fidelity,
            domain,
            task_id,
            f"r{repetition}",
        )
    )
    raw_identity = json.dumps(
        [
            str(candidate_id),
            str(block_id),
            str(attempt_id),
            str(fidelity),
            str(domain),
            str(task_id),
            int(repetition),
        ],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    digest = hashlib.sha256(raw_identity).hexdigest()[:10]
    return (readable[:116].rstrip("-") + "-" + digest).strip("-")


def _safe_identifier(value: object) -> str:
    text = "".join(
        character if character.isascii() and character.isalnum() else "-"
        for character in str(value)
    )
    return "-".join(part for part in text.split("-") if part) or "unit"


def _short_identifier(value: object) -> str:
    readable = _safe_identifier(value)
    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:10]
    return readable[:48].rstrip("-") + "-" + digest


def _safe_error_message(error: Exception) -> str:
    data = str(error).encode("utf-8", errors="replace")[:4000]
    return redact_secrets(data, environment_secrets()).decode("utf-8", errors="replace")


def _build_attempt_manifest(
    *,
    root: Path,
    evaluator_lock: Mapping[str, Any],
    split: Mapping[str, Any],
    scaffold: Mapping[str, Any],
    phase: str,
    fidelity: str,
    block_id: str,
    attempt_id: str,
    selected: Mapping[str, Sequence[str]],
    repetitions: int,
    base_seed: int,
    agent_model: str,
    user_model: str,
    evaluator_model: str,
    ollama_url: str,
    max_steps: int,
    timeout_seconds: float,
) -> dict[str, Any]:
    manifest = {
        "schema_version": 1,
        "phase": phase,
        "fidelity": fidelity,
        "block_id": block_id,
        "attempt_id": attempt_id,
        "candidate_id": scaffold["candidate_id"],
        "mode": scaffold["mode"],
        "structural_cell": scaffold["structural_cell"],
        "scaffold_sha256": scaffold["scaffold_sha256"],
        "task_split_sha256": split["split_sha256"],
        "selected_tasks": {
            domain: list(task_ids) for domain, task_ids in sorted(selected.items())
        },
        "repetitions": repetitions,
        "base_seed": base_seed,
        "agent_model": agent_model,
        "user_model": user_model,
        "evaluator_model": evaluator_model,
        "model_identities": query_ollama_model_identities(
            {agent_model, user_model, evaluator_model}, ollama_url
        ),
        "max_steps": max_steps,
        "timeout_seconds": float(timeout_seconds),
        "enforce_communication_protocol": False,
        "ollama_url": ollama_url.rstrip("/"),
        "tau2_root": str(root),
        "evaluator_lock_sha256": evaluator_lock.get("lock_sha256"),
        "runtime_python": str(Path(sys.executable).resolve(strict=True)),
        "runtime_python_version": sys.version,
        "runtime_dont_write_bytecode": sys.dont_write_bytecode,
        "runtime_pycache_prefix": str(Path(str(sys.pycache_prefix)).resolve(strict=False)),
        "runtime_dependencies": _runtime_dependency_versions(),
        "runtime_dependency_tree": _runtime_dependency_tree_identity(root),
    }
    manifest["runtime_dependencies_sha256"] = hashlib.sha256(
        json.dumps(
            manifest["runtime_dependencies"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    manifest["manifest_sha256"] = hashlib.sha256(
        _canonical_json_bytes(manifest)
    ).hexdigest()
    return manifest


def _attempt_identity_payload(
    scaffold: Mapping[str, Any],
    *,
    block_id: str,
    attempt_id: str,
    fidelity: str,
    manifest_sha256: str,
) -> dict[str, Any]:
    return {
        "block_id": block_id,
        "attempt_id": attempt_id,
        "fidelity": fidelity,
        "candidate_id": scaffold["candidate_id"],
        "scaffold_sha256": scaffold["scaffold_sha256"],
        "scaffold_mode": scaffold["mode"],
        "structural_cell": scaffold["structural_cell"],
        "attempt_manifest_sha256": manifest_sha256,
    }


def _enforce_locked_preflight_contract(
    workspace: CalibrationWorkspace, manifest: Mapping[str, Any]
) -> None:
    if manifest.get("phase") != "preflight":
        return
    lock_path = workspace.target("preflight", "selection_lock.json")
    if not lock_path.is_file():
        return
    selection_lock = _read_json(lock_path)
    _validate_preflight_selection_lock(selection_lock)
    identity_fields = ("candidate_id", "block_id", "attempt_id")
    matches = [
        spec
        for spec in selection_lock["selection"].values()
        if all(manifest.get(field) == spec.get(field) for field in identity_fields)
    ]
    if not matches:
        return
    if len(matches) != 1:
        raise ValueError("selected preflight attempt identity is ambiguous")
    role = matches[0]
    execution = selection_lock["execution_contract"]
    expected_identities = {
        name: execution["model_identities"][name]
        for name in {
            execution["agent_model"],
            execution["user_model"],
            execution["evaluator_model"],
        }
    }
    checks = (
        manifest.get("fidelity") == role["fidelity"],
        manifest.get("scaffold_sha256") == role["scaffold_sha256"],
        manifest.get("mode") == role["scaffold_mode"],
        manifest.get("selected_tasks") == role["selected_tasks"],
        manifest.get("repetitions") == role["repetitions"],
        manifest.get("base_seed") == role["base_seed"],
        manifest.get("task_split_sha256") == selection_lock["task_split_sha256"],
        manifest.get("agent_model") == execution["agent_model"],
        manifest.get("user_model") == execution["user_model"],
        manifest.get("evaluator_model") == execution["evaluator_model"],
        manifest.get("model_identities") == expected_identities,
        manifest.get("max_steps") == execution["max_steps"],
        manifest.get("timeout_seconds") == execution["timeout_seconds"],
        manifest.get("enforce_communication_protocol")
        == execution["enforce_communication_protocol"],
        manifest.get("ollama_url") == execution["ollama_url"],
        os.path.normcase(str(manifest.get("tau2_root")))
        == os.path.normcase(str(execution["tau2_root"])),
        manifest.get("evaluator_lock_sha256") == execution["evaluator_lock_sha256"],
    )
    if not all(checks):
        raise ValueError("selected preflight attempt differs from its immutable contract")


def _runtime_dependency_versions() -> dict[str, list[str]]:
    versions: dict[str, set[str]] = {}
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata.get("Name")
        if not isinstance(name, str) or not name.strip():
            continue
        normalized = name.strip().casefold().replace("_", "-")
        versions.setdefault(normalized, set()).add(str(distribution.version))
    return {name: sorted(values) for name, values in sorted(versions.items())}


def _runtime_dependency_tree_identity(root: Path) -> dict[str, Any]:
    environment_root = (root / ".venv").resolve(strict=True)
    site_packages = (
        environment_root / ("Lib/site-packages" if os.name == "nt" else "lib")
    )
    if os.name != "nt":
        candidates = sorted(site_packages.glob("python*/site-packages"))
        if len(candidates) != 1:
            raise ValueError("isolated dependency site-packages path is ambiguous")
        site_packages = candidates[0]
    site_packages = site_packages.resolve(strict=True)
    hasher = hashlib.sha256()
    file_count = 0
    for directory, directory_names, file_names in os.walk(site_packages, followlinks=False):
        current = Path(directory)
        if _is_reparse_point(current):
            raise ValueError(f"dependency tree contains a reparse point: {current}")
        for name in directory_names:
            child = current / name
            if _is_reparse_point(child):
                raise ValueError(f"dependency tree contains a reparse point: {child}")
        directory_names[:] = [name for name in directory_names if name != "__pycache__"]
        for name in sorted(file_names):
            path = current / name
            if path.suffix.casefold() in {".pyc", ".pyo"}:
                continue
            if _is_reparse_point(path):
                raise ValueError(f"dependency file is a reparse point: {path}")
            relative = path.relative_to(site_packages).as_posix().encode("utf-8")
            data_hash = hashlib.sha256(path.read_bytes()).digest()
            hasher.update(len(relative).to_bytes(4, "big"))
            hasher.update(relative)
            hasher.update(data_hash)
            file_count += 1
    return {
        "root": str(site_packages),
        "file_count": file_count,
        "sha256": hasher.hexdigest(),
        "bytecode_files_excluded": True,
    }


def _validate_path_component(value: str, label: str) -> None:
    if not value or len(value) > 64 or any(
        not (character.isascii() and (character.isalnum() or character in "._-"))
        for character in value
    ):
        raise ValueError(f"{label} must be a 1-64 character portable path identifier")
    if value in {".", ".."} or value.endswith((".", " ")):
        raise ValueError(f"{label} must not use a Windows path alias")
    if value.casefold().split(".")[0] in {
        "con",
        "prn",
        "aux",
        "nul",
        *(f"com{index}" for index in range(1, 10)),
        *(f"lpt{index}" for index in range(1, 10)),
    }:
        raise ValueError(f"{label} must not be a reserved Windows device name")


def _quarantine_orphaned_unit(
    workspace: CalibrationWorkspace,
    *,
    phase: str,
    event_id: str,
    raw_path: Path,
    log_path: Path,
) -> None:
    existing = [path for path in (raw_path, log_path) if path.exists()]
    if not existing:
        return
    destination = workspace.target(
        phase, "orphaned", event_id, uuid.uuid4().hex
    )
    destination.mkdir(parents=True)
    for path in existing:
        if _is_reparse_point(path):
            raise ValueError(f"orphaned τ² unit asset is a reparse point: {path}")
        target = destination / ("llm_logs" if path.is_dir() else path.name)
        shutil.move(str(path), str(target))


def _recover_stale_staging(workspace: CalibrationWorkspace, phase: str) -> None:
    staging_root = workspace.target(phase, "staging")
    if not staging_root.exists():
        return
    if _is_reparse_point(staging_root) or not staging_root.is_dir():
        raise ValueError(f"unsafe τ² staging root: {staging_root}")
    for stage in sorted(staging_root.iterdir(), key=lambda path: path.name):
        if _is_reparse_point(stage) or not stage.is_dir():
            raise ValueError(f"unsafe τ² staging entry: {stage}")
        file_count = 0
        possible_credential = False
        for directory, directory_names, file_names in os.walk(stage, followlinks=False):
            current = Path(directory)
            if _is_reparse_point(current):
                raise ValueError(f"stale τ² staging tree contains a reparse point: {current}")
            for name in directory_names:
                child = current / name
                if _is_reparse_point(child):
                    raise ValueError(
                        f"stale τ² staging tree contains a reparse point: {child}"
                    )
            for name in file_names:
                path = current / name
                if _is_reparse_point(path):
                    raise ValueError(f"stale τ² staging file is a reparse point: {path}")
                data = path.read_bytes()
                file_count += 1
                possible_credential = possible_credential or scan_secret_bytes(
                    data, environment_secrets()
                ).contains_possible_credential
        record = {
            "schema_version": 1,
            "phase": phase,
            "staging_directory_name_sha256": hashlib.sha256(
                stage.name.encode("utf-8")
            ).hexdigest(),
            "file_count": file_count,
            "possible_credential_detected": possible_credential,
            "action": "deleted_without_scientific_interpretation",
        }
        digest = hashlib.sha256(_canonical_json_bytes(record)).hexdigest()[:16]
        shutil.rmtree(stage)
        if stage.exists():
            raise RuntimeError(f"failed to delete stale τ² staging directory: {stage}")
        workspace.write_json_once(f"{phase}/orphaned/staging/{digest}.json", record)


def _committed_outcome_assets_valid(
    workspace: CalibrationWorkspace, payload: Mapping[str, Any]
) -> bool:
    try:
        raw_relative = payload.get("raw_result_path")
        raw_hash = payload.get("raw_result_sha256")
        if payload.get("execution_status") == "completed" and (
            not isinstance(raw_relative, str) or not isinstance(raw_hash, str)
        ):
            return False
        if isinstance(raw_relative, str):
            raw_path = workspace.bind_read_file(workspace.root / Path(raw_relative))
            raw_data = raw_path.read_bytes()
            raw_value = _read_json(raw_path)
            raw_scan = scan_secret_bytes(raw_data, environment_secrets())
            if (
                hashlib.sha256(raw_data).hexdigest() != raw_hash
                or raw_scan.contains_possible_credential
                or _contains_sensitive_json(raw_value)
            ):
                return False
        log_relative = payload.get("llm_log_path")
        expected_manifest = payload.get("llm_log_manifest")
        if not isinstance(log_relative, str) or not isinstance(expected_manifest, Mapping):
            return False
        log_path = workspace.target(*Path(log_relative).parts)
        if not log_path.is_dir():
            return False
        return dict(expected_manifest) == _log_manifest(log_path, normalize=False)
    except (FileNotFoundError, OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return False


def _publish_log_directory(staged: Path, destination: Path) -> None:
    if destination.exists():
        raise FileExistsError(f"τ² LLM log destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.replace(staged, destination)


def _canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _log_manifest(root: Path, *, normalize: bool = True) -> dict[str, Any]:
    files = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if _is_reparse_point(path) or path.is_symlink() or path.is_dir():
            raise ValueError(f"unexpected entry in τ² LLM log directory: {path}")
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            raise ValueError(f"τ² LLM log must not contain a UTF-8 BOM: {path}")
        data.decode("utf-8", errors="strict")
        normalized = data.replace(b"\r\n", b"\n") if normalize else data
        if b"\r" in normalized:
            raise ValueError(f"τ² LLM log contains a non-LF newline: {path}")
        scan = scan_secret_bytes(normalized, environment_secrets())
        try:
            log_value = json.loads(normalized.decode("utf-8", errors="strict"))
        except json.JSONDecodeError as error:
            raise ValueError(f"τ² LLM log is not valid JSON: {path}") from error
        if scan.contains_possible_credential or _contains_sensitive_json(log_value):
            raise ValueError(f"τ² LLM log contains possible credential material: {path}")
        if normalize and normalized != data:
            path.write_bytes(normalized)
        data = normalized
        files.append(
            {
                "name": path.name,
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return {"file_count": len(files), "files": files}


def _contains_sensitive_json(value: object) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key).upper()
            if (
                isinstance(item, str)
                and len(item) >= 8
                and any(
                    token in key_text
                    for token in ("API_KEY", "TOKEN", "SECRET", "PASSWORD")
                )
            ):
                return True
            if _contains_sensitive_json(item):
                return True
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return any(_contains_sensitive_json(item) for item in value)
    return False


def _read_json(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
        raise ValueError(f"calibration JSON must be UTF-8 without BOM and LF-only: {path}")
    value = json.loads(data.decode("utf-8", errors="strict"))
    if not isinstance(value, dict):
        raise ValueError(f"calibration JSON root must be an object: {path}")
    return value
