from __future__ import annotations

import argparse
import copy
import json
import random
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from are.simulation.apps.cab import CabApp
from are.simulation.tool_utils import OperationType
from are.simulation.types import CompletedOracleEvent, EventLog
from are.simulation.validation.configs import ScriptedGraphPerEventJudgeConfig
from are.simulation.validation.judge import GraphPerEventJudge
from are.simulation.validation.judge_states import GraphPerEventJudgeState
from are.simulation.validation.utils.event_utils import AgentEventFilter


def git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def new_cab(seed: int, start_time: float) -> tuple[CabApp, list[Any]]:
    app = CabApp()
    app.rng = random.Random(seed)
    events: list[Any] = []
    app.register_to_env("judge-collision", events.append)
    app.time_manager.reset(start_time=start_time)
    return app, events


def ride_projection(app: CabApp, ride: Any) -> dict[str, Any]:
    return {
        "ride_id": ride.ride_id,
        "price": ride.price,
        "delay": ride.delay,
        "status": ride.status,
        "quotation_history_size": len(app.quotation_history),
    }


def event_projection(event: Any) -> dict[str, Any]:
    return {
        "event_id": event.event_id,
        "event_type": event.event_type.value,
        "tool_name": event.tool_name,
        "function": event.action.function_name,
        "operation_type": event.action.operation_type.value,
        "args": {
            key: value
            for key, value in event.action.args.items()
            if key != "self"
        },
        "kept_by_agent_filter": AgentEventFilter()(event),
    }


def semantic_trace(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {key: value for key, value in event.items() if key != "event_id"}
        for event in events
    ]


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
        "rationale": str(judgment.failure),
        "retained_events": [event_projection(event) for event in judge.state.agent_events],
        "semantic_retained_trace": semantic_trace(
            [event_projection(event) for event in judge.state.agent_events]
        ),
        "agent_to_oracle": dict(judgment.agent_event_id_to_oracle_event_id),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    call_args = {
        "start_location": "A",
        "end_location": "B",
        "service_type": "Default",
        "ride_time": "2025-01-01 12:00:00",
    }
    start_time = 1_750_000_000.0

    direct_app, direct_events = new_cab(seed=314159, start_time=start_time)
    direct_ride = direct_app.order_ride(**call_args)
    direct_order_event = copy.deepcopy(direct_events[-1])

    prequote_app, prequote_events = new_cab(seed=314159, start_time=start_time)
    prequote_app.get_quotation(**call_args)
    prequote_read_event = copy.deepcopy(prequote_events[-1])
    prequote_ride = prequote_app.order_ride(**call_args)

    assert prequote_read_event.action.operation_type == OperationType.READ
    assert AgentEventFilter()(prequote_read_event) is False

    oracle_event = CompletedOracleEvent(
        **direct_order_event.__dict__,
        absolute_event_time=direct_order_event.event_time,
    )
    direct_judgment = judge_world(direct_events, oracle_event)
    prequote_judgment = judge_world(prequote_events, oracle_event)
    direct_world = ride_projection(direct_app, direct_ride)
    prequote_world = ride_projection(prequote_app, prequote_ride)

    assert direct_judgment["success"] is True
    assert prequote_judgment["success"] is True
    assert direct_world != prequote_world
    assert (
        direct_judgment["semantic_retained_trace"]
        == prequote_judgment["semantic_retained_trace"]
    )

    result = {
        "source": {
            "repository": "facebookresearch/meta-agents-research-environments",
            "revision": git_revision(args.are_root.resolve()),
            "python": sys.executable,
        },
        "experiment": "Official GraphPerEventJudge score collision induced by an erased READ action.",
        "configuration": {
            "judge": "GraphPerEventJudge",
            "config": "ScriptedGraphPerEventJudgeConfig",
            "soft_checkers_disabled": True,
            "oracle": "Direct order_ride write event",
        },
        "prequote_read_event": event_projection(prequote_read_event),
        "direct": {
            "world": direct_world,
            "judgment": direct_judgment,
        },
        "prequote_then_order": {
            "world": prequote_world,
            "judgment": prequote_judgment,
        },
        "collision": {
            "same_raw_retained_trace": direct_judgment["retained_events"]
            == prequote_judgment["retained_events"],
            "same_semantic_retained_trace": direct_judgment[
                "semantic_retained_trace"
            ]
            == prequote_judgment["semantic_retained_trace"],
            "same_success_score": direct_judgment["success"]
            == prequote_judgment["success"],
            "different_final_world": direct_world != prequote_world,
        },
        "scope_limit": (
            "This seeded source-level witness proves a verifier score collision after a READ "
            "is erased; raw retained events still differ in generated event UUIDs. "
            "It does not estimate prevalence across the 800 Gaia2 scenarios or leaderboard impact."
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
