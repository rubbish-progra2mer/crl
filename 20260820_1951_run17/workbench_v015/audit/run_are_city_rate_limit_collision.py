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

from are.simulation.apps.cab import CabApp
from are.simulation.apps.city import CityApp
from are.simulation.types import CompletedOracleEvent, EventLog
from are.simulation.validation.configs import ScriptedGraphPerEventJudgeConfig
from are.simulation.validation.judge import GraphPerEventJudge
from are.simulation.validation.judge_states import GraphPerEventJudgeState
from are.simulation.validation.utils.event_utils import AgentEventFilter


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def fail_if_soft_judge_called(*args: Any, **kwargs: Any) -> None:
    raise AssertionError("Soft judge must remain disabled in this scripted pilot.")


def event_projection(event: Any) -> dict[str, Any]:
    return {
        "event_id": event.event_id,
        "event_type": event.event_type.value,
        "tool_name": event.tool_name,
        "function": event.action.function_name,
        "operation_type": event.action.operation_type.value,
        "failed": event.failed(),
        "args": {
            key: value for key, value in event.action.args.items() if key != "self"
        },
        "kept_by_agent_filter": AgentEventFilter()(event),
    }


def semantic_trace(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {key: value for key, value in event.items() if key != "event_id"}
        for event in events
    ]


def judge_world(
    events: list[Any], oracle_event: CompletedOracleEvent
) -> dict[str, Any]:
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
        scenario_tasks=["Complete the task using the available city and cab tools."],
        user_details=None,
        turn_to_agent_events=[],
        turn_to_oracle_events=[[copy.deepcopy(oracle_event)]],
        turn_to_oracle_graph=[{oracle_event.event_id: []}],
        oracle_event_id_to_turn_idx={oracle_event.event_id: 0},
    )
    environment = SimpleNamespace(
        event_log=EventLog.from_list_view(copy.deepcopy(events))
    )
    judgment = judge(environment)
    retained = [event_projection(event) for event in judge.state.agent_events]
    return {
        "success": bool(judgment.success),
        "rationale": str(judgment.failure),
        "retained_events": retained,
        "semantic_retained_trace": semantic_trace(retained),
        "agent_to_oracle": dict(judgment.agent_event_id_to_oracle_event_id),
    }


def row_city_state(row_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    outer = json.loads(row_path.read_text(encoding="utf-8"))
    row = outer["rows"][0]["row"]
    data = json.loads(row["data"])
    city = next(app for app in data["apps"] if app["class_name"] == "CityApp")
    user_event = next(event for event in data["events"] if event["event_type"] == "USER")
    user_text = next(
        argument["value"]
        for argument in user_event["action"]["args"]
        if argument["name"] == "content"
    )
    tool_descriptions = data["augmentation"].get("tool_descriptions_mapping", {})
    row_facts = {
        "local_rows_present": len(outer["rows"]),
        "reported_split_row_count": outer.get("num_rows_total"),
        "split": row["split"],
        "city_app_present": True,
        "user_text_mentions_violent_crime_rate": "violent crime rate"
        in user_text.lower(),
        "city_get_crime_rate_tool_described": "City__get_crime_rate"
        in tool_descriptions,
    }
    return city["app_state"], row_facts


def new_world(
    city_state: dict[str, Any], seed: int, start_time: float
) -> tuple[CityApp, CabApp, list[Any]]:
    events: list[Any] = []
    city = CityApp()
    city.load_state(copy.deepcopy(city_state))
    city.register_to_env("city-rate-limit-collision", events.append)
    city.time_manager.reset(start_time=start_time)
    cab = CabApp()
    cab.rng = random.Random(seed)
    cab.register_to_env("city-rate-limit-collision", events.append)
    cab.time_manager.reset(start_time=start_time)
    return city, cab, events


def city_call(app: CityApp, zip_code: str) -> dict[str, Any]:
    try:
        app.get_crime_rate(zip_code)
        return {"success": True, "error_type": None}
    except Exception as exc:
        return {"success": False, "error_type": type(exc).__name__}


def city_projection(app: CityApp) -> dict[str, Any]:
    return {
        "api_call_count": app.api_call_count,
        "api_call_limit": app.api_call_limit,
        "rate_limit_time_is_set": app.rate_limit_time is not None,
        "rate_limit_exceeded": app.rate_limit_exceeded,
        "crime_data_size": len(app.crime_data),
    }


def ride_projection(ride: Any) -> dict[str, Any]:
    return {
        "ride_id": ride.ride_id,
        "price": ride.price,
        "delay": ride.delay,
        "status": ride.status,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--gaia2-row", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    city_state, row_facts = row_city_state(args.gaia2_row)
    zip_code = sorted(city_state["crime_data"])[0]
    start_time = 1_750_000_000.0
    cab_args = {
        "start_location": "A",
        "end_location": "B",
        "service_type": "Default",
        "ride_time": "2025-01-01 12:00:00",
    }

    direct_city, direct_cab, direct_events = new_world(
        city_state, seed=314159, start_time=start_time
    )
    direct_ride = direct_cab.order_ride(**cab_args)
    direct_order_event = copy.deepcopy(
        next(
            event
            for event in direct_events
            if event.action.function_name == "order_ride"
        )
    )
    direct_capability_probe = city_call(direct_city, zip_code)

    stressed_city, stressed_cab, stressed_events = new_world(
        city_state, seed=314159, start_time=start_time
    )
    stress_successes = 0
    for _ in range(stressed_city.api_call_limit):
        stress_successes += int(city_call(stressed_city, zip_code)["success"])
    limit_trigger = city_call(stressed_city, zip_code)
    stressed_ride = stressed_cab.order_ride(**cab_args)
    stressed_capability_probe = city_call(stressed_city, zip_code)

    oracle_event = CompletedOracleEvent(
        **direct_order_event.__dict__,
        absolute_event_time=direct_order_event.event_time,
    )
    direct_judgment = judge_world(direct_events, oracle_event)
    stressed_judgment = judge_world(stressed_events, oracle_event)

    assert stress_successes == stressed_city.api_call_limit
    assert limit_trigger["success"] is False
    assert direct_capability_probe["success"] is True
    assert stressed_capability_probe["success"] is False
    assert direct_judgment["success"] is True
    assert stressed_judgment["success"] is True
    assert (
        direct_judgment["semantic_retained_trace"]
        == stressed_judgment["semantic_retained_trace"]
    )
    assert ride_projection(direct_ride) == ride_projection(stressed_ride)
    assert city_projection(direct_city) != city_projection(stressed_city)

    result = {
        "source": {
            "repository": "facebookresearch/meta-agents-research-environments",
            "revision": git_revision(args.are_root.resolve()),
            "python": sys.executable,
            "script_sha256": sha256_file(Path(__file__)),
            "gaia2_row_sha256": sha256_file(args.gaia2_row),
        },
        "experiment": (
            "Official GraphPerEventJudge score collision after erased READ actions exhaust "
            "the City API rate limit and change subsequent action feasibility."
        ),
        "local_natural_task_facts": row_facts,
        "stress": {
            "successful_reads_before_limit": stress_successes,
            "limit_trigger": limit_trigger,
            "direct_capability_probe": direct_capability_probe,
            "stressed_capability_probe": stressed_capability_probe,
        },
        "direct": {
            "city_world": city_projection(direct_city),
            "cab_world": ride_projection(direct_ride),
            "judgment": direct_judgment,
        },
        "stressed": {
            "city_world": city_projection(stressed_city),
            "cab_world": ride_projection(stressed_ride),
            "judgment": stressed_judgment,
        },
        "collision": {
            "same_raw_retained_trace": direct_judgment["retained_events"]
            == stressed_judgment["retained_events"],
            "same_semantic_retained_trace": direct_judgment[
                "semantic_retained_trace"
            ]
            == stressed_judgment["semantic_retained_trace"],
            "same_success_score": direct_judgment["success"]
            == stressed_judgment["success"],
            "same_cab_world": ride_projection(direct_ride)
            == ride_projection(stressed_ride),
            "different_city_capability_state": city_projection(direct_city)
            != city_projection(stressed_city),
            "different_next_city_read_outcome": direct_capability_probe["success"]
            != stressed_capability_probe["success"],
        },
        "scope_limit": (
            "The local file contains only one of 160 reported validation rows. The pilot proves "
            "mechanical reachability and a score collision for the official app and judge, not "
            "prevalence, natural agent call counts, or leaderboard impact."
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
