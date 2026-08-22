from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import io
import json
import logging
import os
import random
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable

from run_gaia2_local_effect_trace_panel import (
    CUE_ORDER,
    git_revision,
    ollama_model_digest,
    run_one,
    sha256_file,
)
from run_gaia2_local_effect_trace_admission import select_independent_panel
from run_effect_closure_detector import (
    app_state,
    changed_top_level_fields,
    state_hash,
)

from are.simulation.apps.cab import CabApp
from are.simulation.apps.system import SystemApp
from are.simulation.data_handler.importer import JsonScenarioImporter
from are.simulation.scenarios.scenario_imported_from_json.utils import preprocess_scenario
from are.simulation.time_manager import TimeManager
from are.simulation.tool_utils import AppTool, OperationType
from are.simulation.types import CompletedEvent, EventLog, EventType
from are.simulation.validation.configs import ScriptedGraphPerEventJudgeConfig
from are.simulation.validation.judge import GraphPerEventJudge
from are.simulation.validation.utils.event_utils import AgentEventFilter, EnvAgentEventFilter
from are.simulation.validation.utils.scenario_utils import extract_oracle_events

TARGETS = {
    "cab_quote_information": "Cabs__list_rides",
    "explicit_email_read": "SystemApp__wait_for_notification",
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def serializable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): serializable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(item) for item in value]
    if hasattr(value, "value"):
        return serializable(value.value)
    return repr(value)


def semantic_event(event: Any, scenario_start_time: float) -> dict[str, Any]:
    action = event.action
    args = {
        str(key): serializable(value)
        for key, value in (action.args.items() if action else [])
        if key != "self"
    }
    return {
        "event_type": event.event_type.value,
        "tool_name": event.tool_name,
        "function": action.function_name if action else None,
        "operation_type": action.operation_type.value if action else None,
        "args": args,
        "failed": event.failed(),
        "relative_time": (
            float(event.event_time) - scenario_start_time
            if event.event_time is not None
            else None
        ),
    }


def trace_without_time(trace: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {key: value for key, value in event.items() if key != "relative_time"}
        for event in trace
    ]


def public_event_profile(event: Any, scenario_start_time: float) -> dict[str, Any]:
    semantic = semantic_event(event, scenario_start_time)
    args = semantic.pop("args")
    semantic["argument_keys"] = sorted(args)
    semantic["arguments_sha256"] = sha256_value(args)
    return semantic


def fail_if_soft_judge_called(*args: Any, **kwargs: Any) -> None:
    raise AssertionError("Soft judge must remain disabled in this scripted audit.")


def scripted_config() -> ScriptedGraphPerEventJudgeConfig:
    return ScriptedGraphPerEventJudgeConfig(
        engine=fail_if_soft_judge_called,
        event_id_to_checker_params={},
    )


class NaturalArgumentCapture:
    def __init__(self, target_tool: str) -> None:
        self.target_tool = target_tool
        self.original_call = AppTool.__call__
        self.records: list[dict[str, Any]] = []

    def install(self) -> None:
        capture = self

        def audited_call(tool: AppTool, *args: Any, **kwargs: Any):
            failed = False
            try:
                return capture.original_call(tool, *args, **kwargs)
            except Exception:
                failed = True
                raise
            finally:
                if tool.name == capture.target_tool:
                    capture.records.append(
                        {
                            "failed": failed,
                            "positional_count": len(args),
                            "kwargs": copy.deepcopy(kwargs),
                        }
                    )

        AppTool.__call__ = audited_call

    def uninstall(self) -> None:
        AppTool.__call__ = self.original_call


def capture_natural_call(
    item: dict[str, Any],
    *,
    panel_index: int,
    target_tool: str,
    model: str,
    endpoint: str,
    seed_base: int,
    num_predict: int,
    num_ctx: int,
    timeout: float,
    max_iterations: int,
    invalid_format_retries: int,
) -> tuple[dict[str, Any] | None, dict[str, Any], dict[str, Any]]:
    capture = NaturalArgumentCapture(target_tool)
    suppressed_stdout = io.StringIO()
    suppressed_stderr = io.StringIO()
    capture.install()
    try:
        with contextlib.redirect_stdout(suppressed_stdout), contextlib.redirect_stderr(
            suppressed_stderr
        ):
            replay = run_one(
                item,
                model=model,
                endpoint=endpoint,
                seed=seed_base + panel_index,
                num_predict=num_predict,
                num_ctx=num_ctx,
                timeout=timeout,
                max_iterations=max_iterations,
                invalid_format_retries=invalid_format_retries,
            )
    finally:
        capture.uninstall()

    successful = [record for record in capture.records if not record["failed"]]
    kwargs = None
    if successful:
        selected = successful[0]
        if selected["positional_count"] != 0:
            raise RuntimeError(f"Natural replay used positional arguments for {target_tool}.")
        kwargs = selected["kwargs"]
        if not isinstance(kwargs, dict):
            raise TypeError(f"Captured arguments for {target_tool} are not a dictionary.")

    public_capture = {
        "tool_name": target_tool,
        "argument_keys": sorted(kwargs) if kwargs is not None else [],
        "arguments_sha256": sha256_value(kwargs) if kwargs is not None else None,
        "successful_occurrence_count": len(successful),
    }
    suppressed = {
        "stdout_chars": len(suppressed_stdout.getvalue()),
        "stdout_sha256": sha256_bytes(suppressed_stdout.getvalue().encode("utf-8")),
        "stderr_chars": len(suppressed_stderr.getvalue()),
        "stderr_sha256": sha256_bytes(suppressed_stderr.getvalue().encode("utf-8")),
    }
    return kwargs, replay, {"capture": public_capture, "suppressed": suppressed}


def infer_wait_args_from_admission(
    prior: dict[str, Any], target_tool: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    target_calls = [
        call for call in prior["tool_calls"] if call["tool_name"] == target_tool
    ]
    observations = [
        observation
        for observation in prior["read_effect_observations"]
        if observation["tool_name"] == target_tool
        and not observation["failed"]
        and observation["scheduler_state_changed"]
        and observation["changed_scheduler_fields"] == ["offset"]
    ]
    if len(target_calls) != 1 or len(observations) != 1:
        raise RuntimeError("Frozen admission artifact lacks a unique successful wait witness.")
    if target_calls[0]["argument_keys"] != ["timeout"]:
        raise RuntimeError("Frozen admission wait witness has unexpected argument keys.")
    observation = observations[0]
    before = float(observation["before_scheduler_state"]["offset"])
    after = float(observation["after_scheduler_state"]["offset"])
    delta = after - before
    inferred_timeout = int(round(delta))
    if inferred_timeout <= 0 or abs(delta - inferred_timeout) > 0.01:
        raise RuntimeError("Admission scheduler delta does not identify an integer timeout.")
    return {"timeout": inferred_timeout}, {
        "method": "round frozen after-offset minus before-offset",
        "scheduler_delta_seconds": delta,
        "absolute_rounding_residual_seconds": abs(delta - inferred_timeout),
        "inferred_timeout_seconds": inferred_timeout,
        "prior_tool_argument_keys": target_calls[0]["argument_keys"],
    }


def prepare_scenario(item: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    scenario, _, _ = JsonScenarioImporter().import_from_json_to_benchmark(
        item["scenario_json"], load_completed_events=False
    )
    suppressed_stdout = io.StringIO()
    suppressed_stderr = io.StringIO()
    with contextlib.redirect_stdout(suppressed_stdout), contextlib.redirect_stderr(
        suppressed_stderr
    ):
        preprocess_scenario(
            scenario,
            judge_config=scripted_config(),
            max_scenario_duration=1800,
        )
    return scenario, {
        "stdout_chars": len(suppressed_stdout.getvalue()),
        "stdout_sha256": sha256_bytes(suppressed_stdout.getvalue().encode("utf-8")),
        "stderr_chars": len(suppressed_stderr.getvalue()),
        "stderr_sha256": sha256_bytes(suppressed_stderr.getvalue().encode("utf-8")),
    }


def oracle_turn(scenario: Any) -> tuple[list[Any], list[Any]]:
    oracle_events, _ = extract_oracle_events(scenario, EnvAgentEventFilter(), 0)
    user_events = [event for event in oracle_events if event.event_type == EventType.USER]
    agent_events = [event for event in oracle_events if event.event_type == EventType.AGENT]
    if not user_events or not agent_events:
        raise RuntimeError("Expected both user and agent oracle events in turn zero.")
    return user_events, agent_events


def clone_oracle_agent_events(
    oracle_agent_events: list[Any], current_time: Callable[[], float]
) -> list[CompletedEvent]:
    cloned = []
    for oracle_event in oracle_agent_events:
        event = oracle_event.copy()
        event.event_time = current_time()
        cloned.append(event)
    return cloned


def judge_world(scenario: Any, events: list[Any]) -> dict[str, Any]:
    judge = GraphPerEventJudge(scripted_config())
    judge.initialize_state(scenario)
    env = SimpleNamespace(
        event_log=EventLog.from_list_view([event.copy() for event in events])
    )
    judgment = judge(env)
    retained = [
        semantic_event(event, float(scenario.start_time))
        for event in judge.state.agent_events
    ]
    return {
        "success": bool(judgment.success),
        "failure_sha256": (
            sha256_bytes(str(judgment.failure).encode("utf-8"))
            if judgment.failure
            else None
        ),
        "matched_event_count": len(judgment.agent_event_id_to_oracle_event_id),
        "retained_event_count": len(retained),
        "retained_semantic_trace": retained,
        "retained_semantic_trace_without_time": trace_without_time(retained),
    }


def capsule(
    *,
    app_name: str,
    method: str,
    args: dict[str, Any],
    before_app: dict[str, Any],
    after_app: dict[str, Any],
    before_scheduler: dict[str, Any],
    after_scheduler: dict[str, Any],
) -> dict[str, Any] | None:
    app_changed = before_app != after_app
    scheduler_changed = before_scheduler != after_scheduler
    if not app_changed and not scheduler_changed:
        return None
    return {
        "kind": "READ_EFFECT_CAPSULE",
        "app": app_name,
        "method": method,
        "argument_keys": sorted(args),
        "arguments_sha256": sha256_value(args),
        "changed_app_fields": changed_top_level_fields(before_app, after_app),
        "before_app_state_sha256": state_hash(before_app),
        "after_app_state_sha256": state_hash(after_app),
        "changed_scheduler_fields": changed_top_level_fields(
            before_scheduler, after_scheduler
        ),
        "before_scheduler": before_scheduler,
        "after_scheduler": after_scheduler,
    }


def public_world(
    *,
    mode: str,
    events: list[Any],
    scenario_start_time: float,
    terminal_state: dict[str, Any],
    task_specific_state: dict[str, Any],
    effect_capsule: dict[str, Any] | None,
    judgment: dict[str, Any],
) -> dict[str, Any]:
    full_trace = [semantic_event(event, scenario_start_time) for event in events]
    official_trace = judgment["retained_semantic_trace"]
    closure_trace = (
        ([effect_capsule] if effect_capsule is not None else [])
        + trace_without_time(official_trace)
    )
    terminal_bytes = canonical_bytes(terminal_state)
    capsule_bytes = canonical_bytes(effect_capsule) if effect_capsule is not None else b""
    return {
        "mode": mode,
        "event_profiles": [
            public_event_profile(event, scenario_start_time) for event in events
        ],
        "full_trace_sha256": sha256_value(full_trace),
        "full_trace_without_time_sha256": sha256_value(trace_without_time(full_trace)),
        "official_retained_trace_sha256": sha256_value(official_trace),
        "official_retained_trace_without_time_sha256": sha256_value(
            trace_without_time(official_trace)
        ),
        "effect_capsule": effect_capsule,
        "effect_closure_trace_sha256": sha256_value(closure_trace),
        "terminal_state_sha256": sha256_bytes(terminal_bytes),
        "terminal_state_bytes": len(terminal_bytes),
        "task_specific_state": task_specific_state,
        "effect_capsule_bytes": len(capsule_bytes),
        "official_judgment": {
            key: value
            for key, value in judgment.items()
            if key
            not in {"retained_semantic_trace", "retained_semantic_trace_without_time"}
        },
    }


def run_cab_world(
    *,
    mode: str,
    scenario: Any,
    cab_args: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    scenario_start = float(scenario.start_time)
    user_events, oracle_agent_events = oracle_turn(scenario)
    manager = TimeManager()
    manager.reset(start_time=scenario_start)
    cab = CabApp()
    cab.rng = random.Random(seed)
    cab.time_manager = manager
    read_events: list[Any] = []
    cab.register_to_env(f"natural-cab-{mode}", read_events.append)

    before_app = app_state(cab)
    before_scheduler = {"offset": manager.offset, "pause_offset": manager.pause_offset}
    read_method = "none"
    read_args: dict[str, Any] = {}
    if mode == "pure_read":
        read_method = "get_ride_history_length"
        cab.get_ride_history_length()
    elif mode == "effectful_read":
        read_method = "list_rides"
        read_args = cab_args
        cab.list_rides(**cab_args)
    elif mode != "direct":
        raise ValueError(f"Unknown cab world mode: {mode}")
    after_app = app_state(cab)
    after_scheduler = {"offset": manager.offset, "pause_offset": manager.pause_offset}

    effect_capsule = (
        capsule(
            app_name="CabApp",
            method=read_method,
            args=read_args,
            before_app=before_app,
            after_app=after_app,
            before_scheduler=before_scheduler,
            after_scheduler=after_scheduler,
        )
        if mode != "direct"
        else None
    )
    agent_events = clone_oracle_agent_events(oracle_agent_events, manager.time)
    events = [event.copy() for event in user_events] + read_events + agent_events
    judgment = judge_world(scenario, events)
    return public_world(
        mode=mode,
        events=events,
        scenario_start_time=scenario_start,
        terminal_state={
            "app": after_app,
            "scheduler": after_scheduler,
        },
        task_specific_state={
            "quotation_history_size": len(cab.quotation_history),
            "ride_history_size": len(cab.ride_history),
        },
        effect_capsule=effect_capsule,
        judgment=judgment,
    )


def run_wait_world(
    *,
    mode: str,
    scenario: Any,
    wait_args: dict[str, Any],
) -> dict[str, Any]:
    scenario_start = float(scenario.start_time)
    user_events, oracle_agent_events = oracle_turn(scenario)
    manager = TimeManager()
    manager.reset(start_time=scenario_start)
    system = SystemApp()
    system.time_manager = manager
    read_events: list[Any] = []
    system.register_to_env(f"natural-wait-{mode}", read_events.append)

    def jump_to_timeout() -> None:
        timeout_state = system.wait_for_notification_timeout
        if timeout_state is None:
            raise RuntimeError("wait_for_notification callback lacks timeout state.")
        manager.add_offset(max(0.0, timeout_state.timeout_timestamp - manager.time()))
        system.reset_wait_for_notification_timeout()

    system.wait_for_next_notification = jump_to_timeout
    before_app = app_state(system)
    before_scheduler = {"offset": manager.offset, "pause_offset": manager.pause_offset}
    read_method = "none"
    read_args: dict[str, Any] = {}
    if mode == "pure_read":
        read_method = "get_current_time"
        system.get_current_time()
    elif mode == "effectful_read":
        read_method = "wait_for_notification"
        read_args = wait_args
        system.wait_for_notification(**wait_args)
    elif mode != "direct":
        raise ValueError(f"Unknown wait world mode: {mode}")
    after_app = app_state(system)
    after_scheduler = {"offset": manager.offset, "pause_offset": manager.pause_offset}

    effect_capsule = (
        capsule(
            app_name="SystemApp",
            method=read_method,
            args=read_args,
            before_app=before_app,
            after_app=after_app,
            before_scheduler=before_scheduler,
            after_scheduler=after_scheduler,
        )
        if mode != "direct"
        else None
    )
    agent_events = clone_oracle_agent_events(oracle_agent_events, manager.time)
    events = [event.copy() for event in user_events] + read_events + agent_events
    judgment = judge_world(scenario, events)
    return public_world(
        mode=mode,
        events=events,
        scenario_start_time=scenario_start,
        terminal_state={
            "app": after_app,
            "scheduler": after_scheduler,
        },
        task_specific_state={
            "scheduler_offset": after_scheduler["offset"],
            "first_agent_write_relative_time_seconds": int(
                round(float(agent_events[0].event_time) - scenario_start)
            ),
        },
        effect_capsule=effect_capsule,
        judgment=judgment,
    )


def compare_worlds(worlds: dict[str, dict[str, Any]]) -> dict[str, Any]:
    direct = worlds["direct"]
    pure = worlds["pure_read"]
    effectful = worlds["effectful_read"]
    return {
        "official_same_semantic_trace_without_time_all_three": len(
            {
                world["official_retained_trace_without_time_sha256"]
                for world in worlds.values()
            }
        )
        == 1,
        "official_same_success_direct_and_pure": direct["official_judgment"][
            "success"
        ]
        == pure["official_judgment"]["success"],
        "official_same_success_direct_and_effectful": direct["official_judgment"][
            "success"
        ]
        == effectful["official_judgment"]["success"],
        "full_trace_overseparates_pure_read": direct[
            "full_trace_without_time_sha256"
        ]
        != pure["full_trace_without_time_sha256"],
        "effect_closure_preserves_pure_read_equivalence": direct[
            "effect_closure_trace_sha256"
        ]
        == pure["effect_closure_trace_sha256"],
        "effect_closure_separates_effectful_read": direct[
            "effect_closure_trace_sha256"
        ]
        != effectful["effect_closure_trace_sha256"],
        "full_terminal_state_preserves_pure_read_equivalence": direct[
            "terminal_state_sha256"
        ]
        == pure["terminal_state_sha256"],
        "full_terminal_state_separates_effectful_read": direct[
            "terminal_state_sha256"
        ]
        != effectful["terminal_state_sha256"],
        "task_specific_state_preserves_pure_read_equivalence": direct[
            "task_specific_state"
        ]
        == pure["task_specific_state"],
        "task_specific_state_separates_effectful_read": direct[
            "task_specific_state"
        ]
        != effectful["task_specific_state"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--development-panel", type=Path, required=True)
    parser.add_argument("--admission-panel", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen2.5:7b")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--seed", type=int, default=20260831)
    parser.add_argument("--num-predict", type=int, default=768)
    parser.add_argument("--num-ctx", type=int, default=16384)
    parser.add_argument("--max-iterations", type=int, default=8)
    parser.add_argument("--invalid-format-retries", type=int, default=1)
    parser.add_argument("--request-timeout", type=float, default=300.0)
    args = parser.parse_args()

    for key in ("HF_HUB_OFFLINE", "HF_DATASETS_OFFLINE", "TRANSFORMERS_OFFLINE"):
        os.environ[key] = "1"
    logging.disable(logging.CRITICAL)

    selected, manifest, development_hash = select_independent_panel(
        args.source_dir.resolve(), args.development_panel.resolve()
    )
    admission = json.loads(args.admission_panel.read_text(encoding="utf-8"))
    admission_by_stratum = {
        item["panel_stratum"]: item for item in admission["results"]
    }
    selected_by_stratum = {item["panel_stratum"]: item for item in selected}

    acquisitions: dict[str, dict[str, Any]] = {}
    raw_args: dict[str, dict[str, Any]] = {}
    scenarios: dict[str, Any] = {}
    preprocessing_suppressed: dict[str, dict[str, Any]] = {}
    for stratum, target_tool in TARGETS.items():
        item = selected_by_stratum[stratum]
        panel_index = CUE_ORDER.index(stratum)
        captured_args, replay, capture_summary = capture_natural_call(
            item,
            panel_index=panel_index,
            target_tool=target_tool,
            model=args.model,
            endpoint=args.endpoint,
            seed_base=args.seed,
            num_predict=args.num_predict,
            num_ctx=args.num_ctx,
            timeout=args.request_timeout,
            max_iterations=args.max_iterations,
            invalid_format_retries=args.invalid_format_retries,
        )
        prior = admission_by_stratum[stratum]
        argument_source = "CURRENT_SAME_SETTINGS_REPLAY"
        inference = None
        if captured_args is None:
            if stratum != "explicit_email_read":
                raise RuntimeError(
                    f"Current replay did not execute required {target_tool}."
                )
            captured_args, inference = infer_wait_args_from_admission(
                prior, target_tool
            )
            argument_source = "FROZEN_ADMISSION_SCHEDULER_DELTA_INFERENCE"
        raw_args[stratum] = captured_args
        acquisitions[stratum] = {
            "scenario_identity_sha256": item["identity_sha256"],
            "task_text_sha256": item["task_text_sha256"],
            "matches_admission_identity": item["identity_sha256"]
            == prior["scenario_identity_sha256"],
            "tool_call_projection_matches_admission": replay["tool_calls"]
            == prior["tool_calls"],
            "count_projection_matches_admission": replay["counts"] == prior["counts"],
            "execution_completed_without_exception": replay[
                "execution_completed_without_exception"
            ],
            "argument_source": argument_source,
            "argument_inference": inference,
            "capture": capture_summary,
        }
        scenario, suppressed = prepare_scenario(item)
        scenarios[stratum] = scenario
        preprocessing_suppressed[stratum] = suppressed

    cab_args = raw_args["cab_quote_information"]
    if set(cab_args) != {"start_location", "end_location", "ride_time"}:
        raise ValueError(f"Unexpected natural list_rides arguments: {sorted(cab_args)}")
    wait_args = raw_args["explicit_email_read"]
    if set(wait_args) != {"timeout"} or int(wait_args["timeout"]) <= 0:
        raise ValueError(f"Unexpected natural wait arguments: {sorted(wait_args)}")
    wait_args = {"timeout": int(wait_args["timeout"])}

    cab_worlds = {
        mode: run_cab_world(
            mode=mode,
            scenario=scenarios["cab_quote_information"],
            cab_args=cab_args,
            seed=20260821,
        )
        for mode in ("direct", "pure_read", "effectful_read")
    }
    wait_worlds = {
        mode: run_wait_world(
            mode=mode,
            scenario=scenarios["explicit_email_read"],
            wait_args=wait_args,
        )
        for mode in ("direct", "pure_read", "effectful_read")
    }
    cab_comparisons = compare_worlds(cab_worlds)
    wait_comparisons = compare_worlds(wait_worlds)

    if not all(
        acquisitions[stratum]["matches_admission_identity"] for stratum in TARGETS
    ):
        raise AssertionError("Natural counterfactual selection drifted from admission identities.")
    if acquisitions["cab_quote_information"]["capture"]["capture"][
        "successful_occurrence_count"
    ] < 1:
        raise AssertionError("Cab replay lacks a successful target call.")
    if not all(
        acquisitions[stratum]["execution_completed_without_exception"]
        for stratum in TARGETS
    ):
        raise AssertionError("Natural replay raised an execution exception.")

    script_path = Path(__file__).resolve()
    result = {
        "source": {
            "repository": "facebookresearch/meta-agents-research-environments",
            "are_revision": git_revision(args.are_root.resolve()),
            "dataset": "meta-agents-research-environments/gaia2",
            "dataset_revision": "78ea3bdbdeec2bdcd6afa5420915d8a22f23ed99",
            "split": "validation",
            "parquet_files": manifest,
            "python": sys.executable,
            "script": str(script_path),
            "script_sha256": sha256_file(script_path),
            "development_panel_sha256": development_hash,
            "admission_panel": str(args.admission_panel.resolve()),
            "admission_panel_sha256": sha256_file(args.admission_panel.resolve()),
        },
        "model_replay": {
            "runtime": "Ollama loopback HTTP API",
            "model": args.model,
            "digest": ollama_model_digest(
                args.endpoint, args.model, args.request_timeout
            ),
            "temperature": 0,
            "seed_base": args.seed,
            "num_predict": args.num_predict,
            "num_ctx": args.num_ctx,
            "external_network_offline_flags": True,
            "strict_output_determinism_assumed": False,
            "task_text_or_model_reasoning_emitted": False,
        },
        "natural_acquisition": acquisitions,
        "scenario_preprocessing_suppressed_output": preprocessing_suppressed,
        "counterfactual_contract": {
            "selection": (
                "Reuse the admission panel's frozen task identities and same nominal local "
                "model settings. Require the Cab arguments from a current successful target "
                "call while recording, rather than rejecting, full-sequence replay drift. "
                "For wait, use a current capture when present; otherwise mechanically infer "
                "the integer timeout from the frozen admission scheduler delta. Emit only "
                "argument keys, hashes and the inference audit."
            ),
            "pairing": (
                "For each task, keep the same user event and oracle-completed downstream "
                "write sequence. Compare no inserted read, a same-app pure read, and the "
                "naturally observed effectful read."
            ),
            "judge": (
                "Official GraphPerEventJudge with ScriptedGraphPerEventJudgeConfig; soft "
                "checkers disabled. The official filter still removes successful READ events."
            ),
            "representations": [
                "official write-filtered graph judge",
                "full semantic trajectory",
                "full terminal app plus scheduler state",
                "task-specific terminal assertion",
                "selective read-effect capsule",
            ],
            "oracle_completion_disclosure": (
                "These are task-identity- and natural-call-derived counterfactual pairs, not "
                "unaltered submitted-model trajectories. Downstream writes are copied from "
                "the frozen task oracle and retimed by the counterfactual world's clock."
            ),
        },
        "pairs": {
            "cab_natural_list_rides": {
                "scenario_identity_sha256": acquisitions["cab_quote_information"][
                    "scenario_identity_sha256"
                ],
                "natural_read_argument_keys": sorted(cab_args),
                "natural_read_arguments_sha256": sha256_value(cab_args),
                "worlds": cab_worlds,
                "comparisons": cab_comparisons,
                "interpretation": (
                    "The naturally observed Cab list read can be erased while the same "
                    "task answer remains an official success. However, both full terminal "
                    "state and a trivial quotation-history assertion separate the latent "
                    "state change while preserving the pure-read control, so this pair does "
                    "not establish an advantage over strong state baselines or a changed "
                    "current-task conclusion."
                ),
            },
            "scheduler_natural_wait": {
                "scenario_identity_sha256": acquisitions["explicit_email_read"][
                    "scenario_identity_sha256"
                ],
                "natural_read_argument_keys": sorted(wait_args),
                "natural_read_arguments_sha256": sha256_value(wait_args),
                "worlds": wait_worlds,
                "comparisons": wait_comparisons,
                "interpretation": (
                    "The naturally observed wait shifts the same downstream oracle writes by "
                    "about its full timeout, yet the official scripted judge still returns "
                    "success. In this task every oracle dependency edge is only one second, "
                    "while the official time checker activates only above its one-second "
                    "threshold. Full scheduler terminal state and a rounded response-latency "
                    "assertion both separate the effect, so the collision still does not "
                    "establish a unique advantage over strong state or task-specific baselines."
                ),
            },
        },
        "candidate_impact": {
            "admission_status": "INSUFFICIENT_AND_WEAKENED",
            "positive_residual": (
                "Two natural task/function-derived official-success collisions remain when "
                "downstream oracle writes are held fixed: latent Cab quotation state and an "
                "approximately full-timeout scheduler delay."
            ),
            "negative_update": (
                "Full terminal state and simple task-specific assertions absorb both "
                "distinctions while preserving their pure-read controls. Neither pair shows "
                "a task conclusion or score correction uniquely supplied by selective effect "
                "capsules. Same-settings local replays are also not assumed to reproduce the "
                "same tool sequence, so one frozen wait witness cannot establish stability."
            ),
            "next_decision": (
                "Do not scale the 50+50 detector contract from these pairs. Kill or sharply "
                "redirect the evaluation-method candidate unless a distinct natural mechanism "
                "shows a task-relevant collision not absorbed by official downstream checks "
                "or fair terminal/proxy state baselines."
            ),
        },
        "scope_limit": (
            "Two frozen validation identities and two deterministic local replays are still a "
            "development audit. Oracle-completed counterfactuals do not estimate submitted-model "
            "prevalence, score corrections, rank changes, or benchmark-wide detector accuracy."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
