from __future__ import annotations

import argparse
import copy
import json
import random
import subprocess
import sys
from pathlib import Path
from typing import Any

from are.simulation.apps.agent_user_interface import AgentUserInterface, Sender
from are.simulation.apps.cab import CabApp
from are.simulation.apps.system import SystemApp
from are.simulation.tool_utils import OperationType
from are.simulation.validation.utils.event_utils import AgentEventFilter


def git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def serializable(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
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


def event_summary(event: Any) -> dict[str, Any]:
    action = event.action
    return {
        "event_type": event.event_type.value,
        "function": action.function_name if action else None,
        "operation_type": action.operation_type.value if action else None,
        "failed": event.failed(),
        "kept_by_agent_write_filter": AgentEventFilter()(event),
    }


def write_signature(events: list[Any]) -> list[dict[str, Any]]:
    output = []
    event_filter = AgentEventFilter()
    for event in events:
        if not event_filter(event):
            continue
        args = {
            name: serializable(value)
            for name, value in event.action.args.items()
            if name != "self"
        }
        output.append(
            {
                "app": event.action.app.name,
                "function": event.action.function_name,
                "args": args,
            }
        )
    return output


def run_message_consumption() -> dict[str, Any]:
    app = AgentUserInterface()
    events: list[Any] = []
    app.register_to_env("pilot", events.append)
    app.time_manager.reset(start_time=1_750_000_000.0)

    app.send_message_to_agent("status update")
    user_message = next(message for message in app.messages if message.sender == Sender.USER)
    before = {
        "already_read": user_message.already_read,
        "time_read": user_message.time_read,
    }
    events.clear()

    first_result = app.get_last_unread_messages()
    after_first = {
        "already_read": user_message.already_read,
        "time_read": user_message.time_read,
    }
    first_event = copy.deepcopy(events[-1])
    second_result = app.get_last_unread_messages()

    assert before["already_read"] is False
    assert after_first["already_read"] is True
    assert len(first_result) == 1
    assert len(second_result) == 0
    assert first_event.action.operation_type == OperationType.READ
    assert AgentEventFilter()(first_event) is False

    return {
        "before": before,
        "after_first_read": after_first,
        "first_result_count": len(first_result),
        "second_result_count": len(second_result),
        "first_read_event": event_summary(first_event),
        "mechanical_consequence": "The first read consumes unreadness, so the same subsequent read returns no message.",
    }


def new_cab(seed: int) -> tuple[CabApp, list[Any]]:
    app = CabApp()
    app.rng = random.Random(seed)
    events: list[Any] = []
    app.register_to_env("pilot", events.append)
    return app, events


def ride_projection(ride: Any) -> dict[str, Any]:
    return {
        "ride_id": ride.ride_id,
        "price": ride.price,
        "delay": ride.delay,
        "status": ride.status,
        "quotation_history_size": None,
    }


def run_quote_absorption() -> dict[str, Any]:
    args = {
        "start_location": "A",
        "end_location": "B",
        "service_type": "Default",
        "ride_time": "2025-01-01 12:00:00",
    }

    direct, direct_events = new_cab(314159)
    direct_ride = direct.order_ride(**args)
    direct_projection = ride_projection(direct_ride)
    direct_projection["quotation_history_size"] = len(direct.quotation_history)

    observed, observed_events = new_cab(314159)
    preliminary_quote = observed.get_quotation(**args)
    preliminary_event = copy.deepcopy(observed_events[-1])
    observed_ride = observed.order_ride(**args)
    observed_projection = ride_projection(observed_ride)
    observed_projection["quotation_history_size"] = len(observed.quotation_history)

    direct_signature = write_signature(direct_events)
    observed_signature = write_signature(observed_events)

    assert preliminary_event.action.operation_type == OperationType.READ
    assert AgentEventFilter()(preliminary_event) is False
    assert direct_signature == observed_signature
    assert direct_projection != observed_projection
    assert direct_ride.price != observed_ride.price

    return {
        "arguments": args,
        "preliminary_quote": ride_projection(preliminary_quote),
        "preliminary_read_event": event_summary(preliminary_event),
        "direct_order_world": direct_projection,
        "prequote_then_order_world": observed_projection,
        "filtered_write_trace_direct": direct_signature,
        "filtered_write_trace_prequote": observed_signature,
        "filtered_write_traces_equal": direct_signature == observed_signature,
        "final_worlds_equal": direct_projection == observed_projection,
        "mechanical_consequence": (
            "A read-classified quote mutates quotation history and RNG state. The later order has the same "
            "write name and arguments but a different booked ride price, delay, identifier, and history."
        ),
    }


def run_wait_state() -> dict[str, Any]:
    app = SystemApp()
    events: list[Any] = []
    app.register_to_env("pilot", events.append)
    app.time_manager.reset(start_time=1_750_000_000.0)
    callbacks = []
    app.wait_for_next_notification = lambda: callbacks.append("called")

    before = app.wait_for_notification_timeout
    app.wait_for_notification(timeout=30)
    event = copy.deepcopy(events[-1])
    after = app.wait_for_notification_timeout

    assert before is None
    assert after is not None
    assert after.timeout_timestamp - after.time_created == 30
    assert callbacks == ["called"]
    assert event.action.operation_type == OperationType.READ
    assert AgentEventFilter()(event) is False

    return {
        "before_timeout": None,
        "after_timeout": {
            "time_created": after.time_created,
            "timeout": after.timeout,
            "timeout_timestamp": after.timeout_timestamp,
        },
        "environment_callback_count": len(callbacks),
        "read_event": event_summary(event),
        "mechanical_consequence": "The read-classified wait installs timeout state and invokes the environment scheduler callback.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = {
        "source": {
            "repository": "facebookresearch/meta-agents-research-environments",
            "revision": git_revision(args.are_root.resolve()),
            "python": sys.executable,
        },
        "verifier_boundary": (
            "AgentEventFilter keeps only successful AGENT events whose declared operation_type is WRITE."
        ),
        "pilots": {
            "message_consumption": run_message_consumption(),
            "quote_absorption": run_quote_absorption(),
            "wait_state": run_wait_state(),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
