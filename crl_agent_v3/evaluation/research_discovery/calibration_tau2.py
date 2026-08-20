"""隔离执行冻结 τ² 任务的校准适配器。

候选只能提供声明式 JSON scaffold；本模块把它转换为固定的 LLMAgent 子类，
避免候选代码直接进入评价器进程。评价器在执行前后都与冻结锁比较。
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Mapping, Sequence

from crl_v3.decision import environment_secrets, redact_secrets

from .calibration_runner import CalibrationWorkspace, verify_evaluator_lock


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
    timeout_seconds: float = 300.0,
) -> dict[str, Any]:
    """顺序运行一组冻结任务，并将每个任务—种子单元保存为幂等事件。"""

    if os.name == "nt" and sys.flags.utf8_mode == 0:
        raise RuntimeError(
            "τ² execution on Windows requires Python UTF-8 mode; "
            "use tools/run_tau2_calibration_block.py"
        )
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

    root = Path(os.path.abspath(tau2_root))
    lock_path = workspace.target("preflight", "evaluator_lock.json")
    evaluator_lock = _read_json(lock_path)
    lock_before = verify_evaluator_lock(root, evaluator_lock)
    if not lock_before["valid"]:
        raise ValueError(f"τ² evaluator lock failed before execution: {lock_before}")
    split = _read_json(workspace.target("frozen_task_split.json"))
    scaffold = load_agent_scaffold(workspace, scaffold_path)
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

    existing_ids = {
        str(item.get("event_id")) for item in workspace.read_events(phase)
    }
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
                    resumed += 1
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
                log_path = workspace.target(*Path(log_relative).parts)
                log_path.mkdir(parents=True, exist_ok=True)
                tau2["set_llm_log_dir"](log_path)
                tau2["set_llm_log_mode"]("all")
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
                    workspace.write_json_once(raw_relative, raw)
                    termination = str(simulation.termination_reason.value)
                    reward = (
                        None
                        if simulation.reward_info is None
                        else float(simulation.reward_info.reward)
                    )
                    status = classify_tau2_execution(termination, reward)
                    success = bool(reward is not None and math.isclose(reward, 1.0))
                    payload = {
                        "block_id": block_id,
                        "attempt_id": attempt_id,
                        "fidelity": fidelity,
                        "candidate_id": scaffold["candidate_id"],
                        "scaffold_sha256": scaffold["scaffold_sha256"],
                        "structural_cell": scaffold["structural_cell"],
                        "domain": domain,
                        "task_id": task_id,
                        "repetition": repetition,
                        "seed": seed,
                        "execution_status": status,
                        "success": success,
                        "reward": reward,
                        "termination_reason": termination,
                        "wall_time_seconds": time.perf_counter() - started,
                        "agent_model": agent_model,
                        "user_model": user_model,
                        "evaluator_model": evaluator_model,
                        "max_steps": max_steps,
                        "timeout_seconds": timeout_seconds,
                        "enforce_communication_protocol": False,
                        "raw_result_path": raw_relative,
                        "raw_result_sha256": hashlib.sha256(
                            workspace.target(*Path(raw_relative).parts).read_bytes()
                        ).hexdigest(),
                        "llm_log_path": log_relative,
                        "llm_log_manifest": _log_manifest(log_path),
                    }
                except Exception as error:
                    status, scientific_failure_reason = classify_tau2_exception(error)
                    success = False
                    reward = 0.0 if status == "completed" else None
                    payload = {
                        "block_id": block_id,
                        "attempt_id": attempt_id,
                        "fidelity": fidelity,
                        "candidate_id": scaffold["candidate_id"],
                        "scaffold_sha256": scaffold["scaffold_sha256"],
                        "structural_cell": scaffold["structural_cell"],
                        "domain": domain,
                        "task_id": task_id,
                        "repetition": repetition,
                        "seed": seed,
                        "execution_status": status,
                        "success": False,
                        "reward": None,
                        "termination_reason": scientific_failure_reason,
                        "wall_time_seconds": time.perf_counter() - started,
                        "agent_model": agent_model,
                        "user_model": user_model,
                        "evaluator_model": evaluator_model,
                        "max_steps": max_steps,
                        "timeout_seconds": timeout_seconds,
                        "enforce_communication_protocol": False,
                        "error_type": type(error).__name__,
                        "error_message": _safe_error_message(error),
                        "llm_log_path": log_relative,
                        "llm_log_manifest": _log_manifest(log_path),
                    }
                workspace.record_event(
                    phase,
                    {
                        "event_id": event_id,
                        "kind": "tau2_outcome",
                        "payload": payload,
                    },
                )
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
    if audit_id not in existing_ids:
        workspace.record_event(
            phase,
            {
                "event_id": audit_id,
                "kind": "tau2_block_audit",
                "payload": {
                    "block_id": block_id,
                    "attempt_id": attempt_id,
                    "fidelity": fidelity,
                    "candidate_id": scaffold["candidate_id"],
                    "evaluator_lock_valid_before": lock_before["valid"],
                    "evaluator_lock_valid_after": lock_after["valid"],
                    "candidate_write_scope": "declarative_scaffold_only",
                    "evaluator_model": evaluator_model,
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


def classify_tau2_exception(error: Exception) -> tuple[str, str | None]:
    """只把评价器确认的“预期实体缺失”异常重分类为科学失败。"""

    traceback_files = [
        Path(frame.filename).name.casefold()
        for frame in traceback.extract_tb(error.__traceback__)
    ]
    return _classify_tau2_exception(error, traceback_files)


def _classify_tau2_exception(
    error: Exception, traceback_files: Sequence[str]
) -> tuple[str, str | None]:
    message = str(error)
    expected_entity_absent = (
        isinstance(error, ValueError)
        and message.endswith(" not found")
        and any(
            message.startswith(prefix)
            for prefix in ("Task ", "User ", "Notification ")
        )
    )
    in_environment_evaluator = any(
        Path(filename).name.casefold() == "evaluator_env.py"
        for filename in traceback_files
    )
    if expected_entity_absent and in_environment_evaluator:
        return "completed", "environment_evaluator_expected_entity_absent"
    return "runner_failure", None


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
    digest = hashlib.sha256(readable.encode("utf-8")).hexdigest()[:10]
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


def _log_manifest(root: Path) -> dict[str, Any]:
    files = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if path.is_symlink() or path.is_dir():
            raise ValueError(f"unexpected entry in τ² LLM log directory: {path}")
        data = path.read_bytes()
        files.append(
            {
                "name": path.name,
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return {"file_count": len(files), "files": files}


def _read_json(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
        raise ValueError(f"calibration JSON must be UTF-8 without BOM and LF-only: {path}")
    value = json.loads(data.decode("utf-8", errors="strict"))
    if not isinstance(value, dict):
        raise ValueError(f"calibration JSON root must be an object: {path}")
    return value
