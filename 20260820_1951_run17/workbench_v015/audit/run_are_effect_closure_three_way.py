from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from are.simulation.apps.apartment_listing import ApartmentListingApp
from are.simulation.apps.cab import CabApp
from are.simulation.tool_utils import OperationType
from are.simulation.types import CompletedOracleEvent, EventLog
from are.simulation.validation.configs import ScriptedGraphPerEventJudgeConfig
from are.simulation.validation.judge import GraphPerEventJudge
from are.simulation.validation.judge_states import GraphPerEventJudgeState
from are.simulation.validation.utils.event_utils import AgentEventFilter

from run_effect_closure_detector import (
    app_state,
    changed_top_level_fields,
    state_hash,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def serializable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [serializable(item) for item in value]
    if isinstance(value, tuple):
        return [serializable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): serializable(item) for key, item in value.items()}
    if hasattr(value, "value"):
        return serializable(value.value)
    return repr(value)


def semantic_event(event: Any) -> dict[str, Any]:
    action = event.action
    return {
        "event_type": event.event_type.value,
        "app": action.app.name if action else None,
        "function": action.function_name if action else None,
        "operation_type": action.operation_type.value if action else None,
        "args": {
            key: serializable(value)
            for key, value in (action.args.items() if action else [])
            if key != "self"
        },
        "failed": event.failed(),
    }


def retained_semantic_trace(events: list[Any]) -> list[dict[str, Any]]:
    event_filter = AgentEventFilter()
    return [semantic_event(event) for event in events if event_filter(event)]


def fail_if_soft_judge_called(*args: Any, **kwargs: Any) -> None:
    raise AssertionError("Soft judge must remain disabled in this scripted pilot.")


def judge_world(events: list[Any], oracle_event: CompletedOracleEvent) -> dict[str, Any]:
    judge = GraphPerEventJudge(
        ScriptedGraphPerEventJudgeConfig(
            engine=fail_if_soft_judge_called,
            event_id_to_checker_params={},
        )
    )
    judge.state = GraphPerEventJudgeState(
        initialized=True,
        nb_turns=1,
        turn_idx=-1,
        scenario_start_time=oracle_event.event_time or 0.0,
        scenario_tasks=["Book the specified cab ride."],
        user_details=None,
        turn_to_agent_events=[],
        turn_to_oracle_events=[[copy.deepcopy(oracle_event)]],
        turn_to_oracle_graph=[{oracle_event.event_id: []}],
        oracle_event_id_to_turn_idx={oracle_event.event_id: 0},
    )
    env = SimpleNamespace(event_log=EventLog.from_list_view(copy.deepcopy(events)))
    judgment = judge(env)
    return {
        "success": bool(judgment.success),
        "retained_event_ids": [event.event_id for event in judge.state.agent_events],
        "retained_semantic_trace": [
            semantic_event(event) for event in judge.state.agent_events
        ],
    }


def effect_capsule(
    *,
    position: int,
    app: Any,
    method: str,
    args: dict[str, Any],
    call: Any,
) -> tuple[Any, dict[str, Any] | None]:
    before = app_state(app)
    result = call()
    after = app_state(app)
    if before == after:
        return result, None
    return result, {
        "kind": "READ_EFFECT_CAPSULE",
        "position": position,
        "app": type(app).__name__,
        "method": method,
        "args": args,
        "changed_top_level_fields": changed_top_level_fields(before, after),
        "before_state_sha256": state_hash(before),
        "after_state_sha256": state_hash(after),
    }


def new_cab(seed: int, start_time: float) -> CabApp:
    app = CabApp()
    app.rng = random.Random(seed)
    app.time_manager.reset(start_time=start_time)
    return app


def ride_projection(app: CabApp, ride: Any) -> dict[str, Any]:
    return {
        "price": ride.price,
        "delay": ride.delay,
        "status": ride.status,
        "quotation_history_size": len(app.quotation_history),
    }


def run_world(
    *,
    mode: str,
    cab_args: dict[str, Any],
    seed: int,
    start_time: float,
) -> dict[str, Any]:
    events: list[Any] = []
    capsules: list[dict[str, Any]] = []
    cab = new_cab(seed=seed, start_time=start_time)
    cab.register_to_env(f"effect-closure-{mode}", events.append)

    if mode == "pure_read":
        apartment = ApartmentListingApp()
        apartment.time_manager.reset(start_time=start_time)
        apartment.register_to_env(f"effect-closure-{mode}", events.append)
        _, capsule = effect_capsule(
            position=len(events),
            app=apartment,
            method="list_all_apartments",
            args={},
            call=apartment.list_all_apartments,
        )
        assert events[-1].action.operation_type == OperationType.READ
        assert capsule is None
    elif mode == "effectful_read":
        _, capsule = effect_capsule(
            position=len(events),
            app=cab,
            method="get_quotation",
            args=cab_args,
            call=lambda: cab.get_quotation(**cab_args),
        )
        assert events[-1].action.operation_type == OperationType.READ
        assert capsule is not None
        capsules.append(capsule)
    elif mode != "direct":
        raise ValueError(f"Unknown mode: {mode}")

    ride = cab.order_ride(**cab_args)
    write_trace = retained_semantic_trace(events)
    closure_trace = capsules + [
        {"kind": "RETAINED_WRITE", **event} for event in write_trace
    ]
    return {
        "mode": mode,
        "events": events,
        "full_semantic_trace": [semantic_event(event) for event in events],
        "official_retained_semantic_trace": write_trace,
        "effect_capsules": capsules,
        "effect_closure_trace": closure_trace,
        "cab_world": ride_projection(cab, ride),
        "order_event": copy.deepcopy(events[-1]),
    }


def public_world(world: dict[str, Any], judgment: dict[str, Any]) -> dict[str, Any]:
    return {
        "mode": world["mode"],
        "full_semantic_trace": world["full_semantic_trace"],
        "official_retained_semantic_trace": world[
            "official_retained_semantic_trace"
        ],
        "effect_capsules": world["effect_capsules"],
        "effect_closure_trace": world["effect_closure_trace"],
        "cab_world": world["cab_world"],
        "official_judgment": judgment,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    start_time = 1_750_000_000.0
    seed = 314159
    cab_args = {
        "start_location": "A",
        "end_location": "B",
        "service_type": "Default",
        "ride_time": "2025-01-01 12:00:00",
    }
    direct = run_world(
        mode="direct",
        cab_args=cab_args,
        seed=seed,
        start_time=start_time,
    )
    pure = run_world(
        mode="pure_read",
        cab_args=cab_args,
        seed=seed,
        start_time=start_time,
    )
    effectful = run_world(
        mode="effectful_read",
        cab_args=cab_args,
        seed=seed,
        start_time=start_time,
    )

    oracle = CompletedOracleEvent(
        **direct["order_event"].__dict__,
        absolute_event_time=direct["order_event"].event_time,
    )
    direct_judgment = judge_world(direct["events"], oracle)
    pure_judgment = judge_world(pure["events"], oracle)
    effectful_judgment = judge_world(effectful["events"], oracle)

    same_official_semantics = (
        direct_judgment["retained_semantic_trace"]
        == pure_judgment["retained_semantic_trace"]
        == effectful_judgment["retained_semantic_trace"]
    )
    same_official_score = (
        direct_judgment["success"]
        == pure_judgment["success"]
        == effectful_judgment["success"]
        is True
    )
    full_trace_overseparates_pure = (
        direct["full_semantic_trace"] != pure["full_semantic_trace"]
    )
    closure_preserves_pure_equivalence = (
        direct["effect_closure_trace"] == pure["effect_closure_trace"]
    )
    closure_separates_effectful = (
        direct["effect_closure_trace"] != effectful["effect_closure_trace"]
    )
    pure_world_equal = direct["cab_world"] == pure["cab_world"]
    effectful_world_different = (
        direct["cab_world"] != effectful["cab_world"]
    )

    assert same_official_semantics is True
    assert same_official_score is True
    assert full_trace_overseparates_pure is True
    assert closure_preserves_pure_equivalence is True
    assert closure_separates_effectful is True
    assert pure_world_equal is True
    assert effectful_world_different is True

    script_path = Path(__file__).resolve()
    result = {
        "source": {
            "repository": "facebookresearch/meta-agents-research-environments",
            "revision": git_revision(args.are_root.resolve()),
            "python": sys.executable,
            "script": str(script_path),
            "script_sha256": sha256_bytes(script_path.read_bytes()),
        },
        "experiment": (
            "Three-way ARE replay comparing the official write-only judge, full raw "
            "trajectory retention, and read-effect closure."
        ),
        "worlds": {
            "direct": public_world(direct, direct_judgment),
            "pure_read_then_write": public_world(pure, pure_judgment),
            "effectful_read_then_write": public_world(
                effectful, effectful_judgment
            ),
        },
        "comparisons": {
            "official_same_semantic_retained_trace_all_three": same_official_semantics,
            "official_same_success_score_all_three": same_official_score,
            "full_trace_separates_harmless_pure_read": full_trace_overseparates_pure,
            "effect_closure_preserves_pure_read_equivalence": closure_preserves_pure_equivalence,
            "effect_closure_separates_effectful_read": closure_separates_effectful,
            "pure_read_preserves_later_cab_world": pure_world_equal,
            "effectful_read_changes_later_cab_world": effectful_world_different,
        },
        "changed_computation": (
            "Retain successful writes as before, but add a compact capsule only when a "
            "nominal READ changes the curated semantic app-state projection."
        ),
        "baseline_delta": (
            "The official write-only filter merges the effectful and direct worlds. "
            "Full raw trajectory retention separates both effectful and harmless pure reads. "
            "Effect closure separates the effectful read while preserving equivalence under "
            "the harmless pure-read insertion in this seeded witness."
        ),
        "scope_limit": (
            "This is one curated three-world source-level witness on one ARE revision. "
            "It does not prove a general semantic-state projection, task-level reward "
            "improvement, natural prevalence, ranking changes, or leaderboard impact."
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
