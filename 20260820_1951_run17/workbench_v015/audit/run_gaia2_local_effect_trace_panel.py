from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import time
import types
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

import polars as pl


try:
    import xxhash as _xxhash  # noqa: F401

    XXHASH_IMPORT_SHIM = False
except ModuleNotFoundError:
    # The frozen ARE preprocessing module imports its cache/export helper eagerly,
    # even though this trace-only pilot invokes neither cache nor export. Supply the
    # narrow import surface so the official preprocessing function remains usable.
    class _FallbackXXH64:
        def __init__(self, data: bytes = b"") -> None:
            self._hash = hashlib.blake2b(data, digest_size=8)

        def update(self, data: bytes) -> None:
            self._hash.update(data)

        def hexdigest(self) -> str:
            return self._hash.hexdigest()

    xxhash_module = types.ModuleType("xxhash")
    xxhash_module.xxh64 = _FallbackXXH64  # type: ignore[attr-defined]
    sys.modules["xxhash"] = xxhash_module
    XXHASH_IMPORT_SHIM = True

from are.simulation.agents.agent_builder import AgentBuilder
from are.simulation.agents.agent_config_builder import AgentConfigBuilder
from are.simulation.agents.are_simulation_agent_config import LLMEngineConfig
from are.simulation.agents.llm.llm_engine import LLMEngine, LLMEngineException
from are.simulation.data_handler.importer import JsonScenarioImporter
from are.simulation.environment import Environment, EnvironmentConfig
from are.simulation.notification_system import VerboseNotificationSystem
from are.simulation.scenarios.config import ScenarioRunnerConfig
from are.simulation.scenarios.scenario_imported_from_json.utils import (
    preprocess_scenario_from_config,
)
from are.simulation.tool_utils import AppTool
from are.simulation.types import EnvironmentType, SimulatedGenerationTimeConfig

from run_effect_closure_detector import (
    app_state,
    changed_top_level_fields,
    state_hash,
)


CONFIGS = ("execution", "search", "adaptability", "time", "ambiguity")
CUE_ORDER = (
    "city_crime_information",
    "cab_quote_information",
    "timed_wait_for_response",
    "explicit_email_read",
)
CUE_RULES = {
    "city_crime_information": {
        "required_classes": {"CityApp"},
        "patterns": [
            r"\b(?:crime|violent crime|property crime)\b.{0,100}\b(?:rate|statistics?|compare|comparison|safer|safest|dangerous|danger)\b",
            r"\b(?:rate|statistics?|compare|comparison|safer|safest|dangerous|danger)\b.{0,100}\b(?:crime|violent crime|property crime)\b",
        ],
    },
    "cab_quote_information": {
        "required_classes": {"CabApp"},
        "patterns": [
            r"\b(?:cab|taxi|ride)\b.{0,100}\b(?:quote|quotation|fare|price|cost|cheapest|expensive|estimate)\b",
            r"\b(?:quote|quotation|fare|price|cost|cheapest|expensive|estimate)\b.{0,100}\b(?:cab|taxi|ride)\b",
        ],
    },
    "timed_wait_for_response": {
        "required_classes": {"SystemApp"},
        "patterns": [
            r"\b(?:wait|unless|if)\b.{0,140}\b(?:reply|respond|response|notification)\b.{0,100}\b(?:second|seconds|minute|minutes|hour|hours)\b",
            r"\b(?:second|seconds|minute|minutes|hour|hours)\b.{0,100}\b(?:reply|respond|response|notification)\b",
        ],
    },
    "explicit_email_read": {
        "required_classes": {"EmailClientApp", "EmailClientV2", "Mail"},
        "patterns": [
            r"\b(?:read|open|unread|mark)\b.{0,60}\b(?:email|emails|mail)\b",
            r"\b(?:email|emails|mail)\b.{0,60}\b(?:read|open|unread|mark)\b",
        ],
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def decode_arg_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def action_args(action: dict[str, Any]) -> dict[str, Any]:
    return {
        str(item["name"]): decode_arg_value(item.get("value"))
        for item in action.get("args") or []
        if isinstance(item, dict) and "name" in item
    }


def user_texts(payload: dict[str, Any]) -> list[str]:
    texts = []
    for event in payload.get("events") or []:
        if event.get("event_type") != "USER":
            continue
        content = action_args(event.get("action") or {}).get("content")
        if isinstance(content, str) and content.strip():
            texts.append(content.strip())
    return texts


def match_cues(payload: dict[str, Any], text: str) -> list[str]:
    classes = {
        str(app.get("class_name"))
        for app in payload.get("apps") or []
        if isinstance(app, dict) and app.get("class_name")
    }
    classes.add("SystemApp")
    normalized = re.sub(r"\s+", " ", text.lower()).strip()
    return [
        label
        for label, rule in CUE_RULES.items()
        if classes & rule["required_classes"]
        and any(re.search(pattern, normalized) for pattern in rule["patterns"])
    ]


def select_panel(source_dir: Path, per_cue: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates: list[dict[str, Any]] = []
    manifest = []
    for config in CONFIGS:
        path = source_dir / f"gaia2_{config}_validation.parquet"
        if not path.is_file():
            raise FileNotFoundError(path)
        manifest.append(
            {
                "config": config,
                "path": str(path.resolve()),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
        frame = pl.read_parquet(path, columns=["id", "scenario_id", "split", "data"])
        if frame.height != 160 or set(frame["split"].to_list()) != {"validation"}:
            raise ValueError(f"Unexpected frozen Gaia2 partition: {path}")
        for row in frame.iter_rows(named=True):
            payload = json.loads(row["data"])
            texts = user_texts(payload)
            combined_text = "\n".join(texts)
            cues = match_cues(payload, combined_text)
            if not cues:
                continue
            identity = f"{config}\0{row['id']}\0{row['scenario_id']}"
            candidates.append(
                {
                    "config": config,
                    "identity_sha256": sha256_text(identity),
                    "task_text_sha256": sha256_text(combined_text),
                    "cues": cues,
                    "scenario_json": row["data"],
                }
            )

    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    for cue in CUE_ORDER:
        eligible = sorted(
            (item for item in candidates if cue in item["cues"]),
            key=lambda item: item["identity_sha256"],
        )
        added = 0
        for item in eligible:
            if item["identity_sha256"] in used:
                continue
            selected.append({**item, "panel_stratum": cue})
            used.add(item["identity_sha256"])
            added += 1
            if added == per_cue:
                break
        if added != per_cue:
            raise ValueError(f"Not enough unique scenarios for cue {cue}: {added}/{per_cue}")
    return selected, manifest


def local_json_request(url: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "127.0.0.1",
        "localhost",
        "::1",
    }:
        raise ValueError(f"Only loopback model endpoints are allowed: {url}")
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


class OllamaTextEngine(LLMEngine):
    def __init__(
        self,
        *,
        model: str,
        endpoint: str,
        seed: int,
        num_predict: int,
        num_ctx: int,
        timeout: float,
    ) -> None:
        super().__init__(model)
        self.endpoint = endpoint
        self.seed = seed
        self.num_predict = num_predict
        self.num_ctx = num_ctx
        self.timeout = timeout
        self.calls: list[dict[str, Any]] = []

    def chat_completion(
        self,
        messages: list[dict[str, Any]],
        stop_sequences: list[str] = [],
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any]]:
        converted = []
        attachment_count = 0
        for message in messages:
            raw_role = message["role"]
            role = str(raw_role.value) if hasattr(raw_role, "value") else str(raw_role)
            role = {"tool-response": "user", "tool-call": "assistant"}.get(role, role)
            content = message.get("content", "")
            attachments = message.get("attachments") or []
            attachment_count += len(attachments)
            if attachments:
                raise LLMEngineException("Frozen panel is text-only; attachments are unsupported.")
            converted.append({"role": role, "content": content})

        started = time.perf_counter()
        request_seed = self.seed + len(self.calls)
        try:
            response = local_json_request(
                self.endpoint,
                {
                    "model": self.model_name,
                    "messages": converted,
                    "stream": False,
                    "think": False,
                    "options": {
                        "temperature": 0,
                        "seed": request_seed,
                        "num_predict": self.num_predict,
                        "num_ctx": self.num_ctx,
                    },
                },
                self.timeout,
            )
        except (OSError, ValueError, urllib.error.URLError, json.JSONDecodeError) as error:
            raise LLMEngineException("Local Ollama request failed.", error) from error
        elapsed = time.perf_counter() - started
        content = str((response.get("message") or {}).get("content") or "")
        raw_content_sha256 = sha256_text(content)
        for stop_token in stop_sequences:
            content = content.split(stop_token)[0]
        self.calls.append(
            {
                "call_index": len(self.calls),
                "request_seed": request_seed,
                "message_count": len(converted),
                "message_roles": [message["role"] for message in converted],
                "message_content_chars": [
                    len(str(message["content"])) for message in converted
                ],
                "attachment_count": attachment_count,
                "raw_content_sha256": raw_content_sha256,
                "raw_content_chars": len(str((response.get("message") or {}).get("content") or "")),
                "returned_content_sha256": sha256_text(content),
                "returned_content_chars": len(content),
                "contains_thought_token": "Thought:" in content,
                "contains_action_token": "Action:" in content,
                "prompt_eval_count": response.get("prompt_eval_count"),
                "eval_count": response.get("eval_count"),
                "done_reason": response.get("done_reason"),
                "elapsed_seconds": elapsed,
            }
        )
        metadata = {
            "prompt_tokens": response.get("prompt_eval_count", 0),
            "completion_tokens": response.get("eval_count", 0),
            "total_tokens": response.get("prompt_eval_count", 0)
            + response.get("eval_count", 0),
            "completion_duration": elapsed,
        }
        return content, metadata


class CappedAgentConfigBuilder(AgentConfigBuilder):
    def __init__(self, max_iterations: int) -> None:
        self.max_iterations = max_iterations

    def build(self, agent_name: str):
        config = super().build(agent_name)
        config.get_base_agent_config().max_iterations = self.max_iterations
        return config


class CapturingAgentBuilder(AgentBuilder):
    def __init__(
        self,
        engine: OllamaTextEngine,
        invalid_format_retries: int,
        max_iterations: int,
    ) -> None:
        self.engine = engine
        self.invalid_format_retries = invalid_format_retries
        self.max_iterations = max_iterations
        self.last_agent = None
        self.last_env = None

    def build(self, agent_config, env=None, mock_responses=None):
        class FixedEngineBuilder:
            def __init__(self, fixed_engine: OllamaTextEngine) -> None:
                self.fixed_engine = fixed_engine

            def create_engine(self, engine_config, mock_responses=None):
                if mock_responses is not None:
                    raise ValueError("Mock responses are outside this pilot.")
                return self.fixed_engine

        delegate = AgentBuilder(llm_engine_builder=FixedEngineBuilder(self.engine))
        agent = delegate.build(agent_config, env=env, mock_responses=mock_responses)
        agent.max_iterations = self.max_iterations
        agent.react_agent.max_iterations = self.max_iterations
        agent.react_agent.invalid_format_retries = self.invalid_format_retries
        self.last_agent = agent
        self.last_env = env
        return agent


class ReadEffectCapture:
    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []
        self.original_call = AppTool.__call__

    def install(self) -> None:
        capture = self

        def time_effect_state(app: Any) -> dict[str, Any] | None:
            manager = getattr(app, "time_manager", None)
            if manager is None:
                return None
            return {
                "offset": getattr(manager, "offset", None),
                "pause_offset": getattr(manager, "pause_offset", None),
            }

        def audited_call(tool: AppTool, *args: Any, **kwargs: Any):
            if tool.write_operation is not False or tool.class_instance is None:
                return capture.original_call(tool, *args, **kwargs)
            before = app_state(tool.class_instance)
            before_time_effect = time_effect_state(tool.class_instance)
            failed = False
            try:
                return capture.original_call(tool, *args, **kwargs)
            except Exception:
                failed = True
                raise
            finally:
                after = app_state(tool.class_instance)
                after_time_effect = time_effect_state(tool.class_instance)
                semantic_state_changed = before != after
                scheduler_state_changed = before_time_effect != after_time_effect
                capture.records.append(
                    {
                        "call_index": len(capture.records),
                        "tool_name": tool.name,
                        "declared_operation_type": "READ",
                        "failed": failed,
                        "semantic_state_changed": semantic_state_changed,
                        "changed_top_level_fields": changed_top_level_fields(before, after),
                        "before_state_sha256": state_hash(before),
                        "after_state_sha256": state_hash(after),
                        "scheduler_state_changed": scheduler_state_changed,
                        "changed_scheduler_fields": changed_top_level_fields(
                            before_time_effect or {}, after_time_effect or {}
                        ),
                        "before_scheduler_state": before_time_effect,
                        "after_scheduler_state": after_time_effect,
                        "effect_closure_changed": semantic_state_changed
                        or scheduler_state_changed,
                    }
                )

        AppTool.__call__ = audited_call

    def uninstall(self) -> None:
        AppTool.__call__ = self.original_call


def tool_call_projection(agent: Any) -> list[dict[str, Any]]:
    from are.simulation.agents.agent_log import ToolCallLog

    output = []
    for log in agent.react_agent.get_agent_logs():
        if not isinstance(log, ToolCallLog):
            continue
        arguments = log.tool_arguments
        keys = sorted(arguments) if isinstance(arguments, dict) else []
        output.append(
            {
                "call_index": len(output),
                "tool_name": log.tool_name,
                "argument_keys": keys,
            }
        )
    return output


def ollama_model_digest(endpoint: str, model: str, timeout: float) -> str | None:
    tags_url = endpoint.rsplit("/api/chat", 1)[0] + "/api/tags"
    parsed = urllib.parse.urlparse(tags_url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "127.0.0.1",
        "localhost",
        "::1",
    }:
        raise ValueError(f"Only loopback model endpoints are allowed: {endpoint}")
    request = urllib.request.Request(tags_url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return None
    for item in payload.get("models") or []:
        if item.get("name") == model or item.get("model") == model:
            return item.get("digest")
    return None


def run_one(
    item: dict[str, Any],
    *,
    model: str,
    endpoint: str,
    seed: int,
    num_predict: int,
    num_ctx: int,
    timeout: float,
    max_iterations: int,
    invalid_format_retries: int,
) -> dict[str, Any]:
    scenario, _, _ = JsonScenarioImporter().import_from_json_to_benchmark(
        item["scenario_json"], load_completed_events=False
    )
    config = ScenarioRunnerConfig(
        model=model,
        model_provider="local-ollama-loopback",
        endpoint=endpoint,
        agent="default",
        oracle=False,
        export=False,
        max_turns=1,
        use_custom_logger=False,
        simulated_generation_time_mode="measured",
        judge_engine_config=None,
    )
    preprocess_started = time.perf_counter()
    preprocess_scenario_from_config(scenario, config)
    preprocess_seconds = time.perf_counter() - preprocess_started

    engine = OllamaTextEngine(
        model=model,
        endpoint=endpoint,
        seed=seed,
        num_predict=num_predict,
        num_ctx=num_ctx,
        timeout=timeout,
    )
    agent_builder = CapturingAgentBuilder(
        engine,
        invalid_format_retries,
        max_iterations,
    )
    env_config = EnvironmentConfig(
        oracle_mode=False,
        queue_based_loop=False,
        wait_for_user_input_timeout=config.wait_for_user_input_timeout,
        time_increment_in_seconds=scenario.time_increment_in_seconds,
        exit_when_no_events=False,
    )
    if scenario.start_time and scenario.start_time > 0:
        env_config.start_time = scenario.start_time
    env = Environment(
        environment_type=EnvironmentType.CLI,
        config=env_config,
        notification_system=VerboseNotificationSystem(),
    )
    env.run(scenario, wait_for_end=False)

    agent_config = CappedAgentConfigBuilder(max_iterations).build("default")
    agent_config.max_turns = 1
    base_config = agent_config.get_base_agent_config()
    base_config.use_custom_logger = False
    base_config.llm_engine_config = LLMEngineConfig(
        model_name=model,
        provider="local-ollama-loopback",
        endpoint=endpoint,
    )
    base_config.simulated_generation_time_config = SimulatedGenerationTimeConfig(
        mode="measured"
    )
    agent = agent_builder.build(agent_config=agent_config, env=env)
    capture = ReadEffectCapture()
    capture.install()
    started = time.perf_counter()
    execution_exception: Exception | None = None
    agent_output: Any = None
    try:
        agent_output = agent.run_scenario(
            scenario=scenario,
            notification_system=env.notification_system,
        ).output
    except Exception as error:
        execution_exception = error
    finally:
        capture.uninstall()
        env.stop()
    elapsed = time.perf_counter() - started

    tool_calls = (
        tool_call_projection(agent_builder.last_agent)
        if agent_builder.last_agent is not None
        else []
    )
    return {
        "panel_stratum": item["panel_stratum"],
        "config": item["config"],
        "scenario_identity_sha256": item["identity_sha256"],
        "task_text_sha256": item["task_text_sha256"],
        "matched_cues": item["cues"],
        "preprocess_seconds": preprocess_seconds,
        "run_seconds": elapsed,
        "execution_completed_without_exception": execution_exception is None,
        "exception_type": type(execution_exception).__name__ if execution_exception else None,
        "agent_output_sha256": (
            sha256_text(str(agent_output)) if agent_output is not None else None
        ),
        "model_calls": engine.calls,
        "tool_calls": tool_calls,
        "read_effect_observations": capture.records,
        "counts": {
            "model_calls": len(engine.calls),
            "tool_calls": len(tool_calls),
            "declared_read_calls": len(capture.records),
            "effectful_read_calls": sum(
                record["effect_closure_changed"] for record in capture.records
            ),
            "pure_read_calls": sum(
                not record["effect_closure_changed"] for record in capture.records
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--per-cue", type=int, default=1)
    parser.add_argument("--panel-limit", type=int)
    parser.add_argument("--max-iterations", type=int, default=12)
    parser.add_argument("--invalid-format-retries", type=int, default=2)
    parser.add_argument("--num-predict", type=int, default=1024)
    parser.add_argument("--num-ctx", type=int, default=16384)
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--request-timeout", type=float, default=300.0)
    args = parser.parse_args()

    if (
        args.per_cue <= 0
        or args.max_iterations <= 0
        or args.num_predict <= 0
        or args.num_ctx <= 0
    ):
        raise ValueError("Panel and generation bounds must be positive.")
    if args.panel_limit is not None and args.panel_limit <= 0:
        raise ValueError("--panel-limit must be positive when supplied.")

    for key in ("HF_HUB_OFFLINE", "HF_DATASETS_OFFLINE", "TRANSFORMERS_OFFLINE"):
        os.environ[key] = "1"
    logging.getLogger().setLevel(logging.ERROR)

    panel, manifest = select_panel(args.source_dir.resolve(), args.per_cue)
    if args.panel_limit is not None:
        panel = panel[: args.panel_limit]

    results = []
    for index, item in enumerate(panel):
        result = run_one(
            item,
            model=args.model,
            endpoint=args.endpoint,
            seed=args.seed + index,
            num_predict=args.num_predict,
            num_ctx=args.num_ctx,
            timeout=args.request_timeout,
            max_iterations=args.max_iterations,
            invalid_format_retries=args.invalid_format_retries,
        )
        results.append(result)

    aggregate = Counter()
    for result in results:
        aggregate.update(result["counts"])
    aggregate["scenarios"] = len(results)
    aggregate["scenarios_with_effectful_read"] = sum(
        result["counts"]["effectful_read_calls"] > 0 for result in results
    )
    aggregate["scenarios_with_any_declared_read"] = sum(
        result["counts"]["declared_read_calls"] > 0 for result in results
    )

    script_path = Path(__file__).resolve()
    output = {
        "source": {
            "repository": "facebookresearch/meta-agents-research-environments",
            "are_revision": git_revision(args.are_root.resolve()),
            "dataset": "meta-agents-research-environments/gaia2",
            "dataset_revision": "78ea3bdbdeec2bdcd6afa5420915d8a22f23ed99",
            "split": "validation",
            "parquet_files": manifest,
            "python": sys.executable,
            "polars": pl.__version__,
            "script": str(script_path),
            "script_sha256": sha256_file(script_path),
        },
        "model": {
            "runtime": "Ollama loopback HTTP API",
            "model": args.model,
            "digest": ollama_model_digest(args.endpoint, args.model, args.request_timeout),
            "endpoint_scope": "loopback only",
            "temperature": 0,
            "seed_base": args.seed,
            "seed_schedule": "seed_base + scenario_index + model_call_index",
            "num_predict": args.num_predict,
            "num_ctx": args.num_ctx,
            "think": False,
        },
        "frozen_panel_contract": {
            "selection": (
                "For each cue stratum in the fixed order, select the lexicographically smallest "
                "SHA-256 scenario identities not already selected. Selection is independent of model output."
            ),
            "cue_order": list(CUE_ORDER),
            "per_cue": args.per_cue,
            "panel_limit": args.panel_limit,
            "selected_scenarios": len(panel),
            "task_text_emitted": False,
        },
        "execution_contract": {
            "agent": "official ARE default ReAct JSON agent and tool descriptions",
            "judge": "disabled; trace acquisition only",
            "max_iterations_per_turn": args.max_iterations,
            "invalid_format_retries": args.invalid_format_retries,
            "simulated_generation_time_mode": "measured",
            "external_network_offline_flags": True,
            "non_loopback_model_endpoint_allowed": False,
            "filesystem_app_dependency_available_in_venv": False,
            "cache_export_xxhash_import_shim": XXHASH_IMPORT_SHIM,
            "cache_or_export_invoked": False,
            "effect_closure_projection": (
                "curated app state plus TimeManager offset and pause_offset; real clock "
                "bookkeeping, callbacks, registries and instrumentation flags are excluded"
            ),
        },
        "results": results,
        "aggregate": dict(sorted(aggregate.items())),
        "interpretation_boundary": (
            "This is a deterministic, low-fidelity local model panel on public frozen Gaia2 "
            "validation scenarios. It uses the official default agent loop and real app calls, "
            "but disables the judge, caps iterations and format retries, uses one local model, "
            "and lacks the optional filesystem dependency. It can establish that naturally "
            "generated local trajectories do or do not invoke state-changing declared READs in "
            "this panel; it cannot estimate official submitted-model prevalence, task-score "
            "corrections, leaderboard or ranking impact, or independent admission performance."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
