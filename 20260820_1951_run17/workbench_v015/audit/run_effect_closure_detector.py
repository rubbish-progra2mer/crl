from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from are.simulation.apps.agent_user_interface import AgentUserInterface
from are.simulation.apps.apartment_listing import ApartmentListingApp
from are.simulation.apps.cab import CabApp
from are.simulation.apps.system import SystemApp
from are.simulation.tool_utils import OperationType
from are.simulation.validation.utils.event_utils import AgentEventFilter


EXCLUDED_APP_FIELDS = {
    "_initial_args",
    "_initial_kwargs",
    "add_event_callbacks",
    "failure_probability",
    "is_state_modified",
    "name",
    "time_manager",
    "_tool_registries",
}


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


def normalize(value: Any, seen: set[int] | None = None) -> Any:
    if seen is None:
        seen = set()
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Enum):
        return normalize(value.value, seen)
    if isinstance(value, random.Random):
        payload = repr(value.getstate()).encode("utf-8")
        return {"random_state_sha256": sha256_bytes(payload)}
    if callable(value):
        return {"callable": type(value).__name__}

    identity = id(value)
    if identity in seen:
        return {"cycle": type(value).__name__}
    seen.add(identity)
    try:
        if isinstance(value, dict):
            return {
                str(key): normalize(item, seen)
                for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            }
        if isinstance(value, (list, tuple)):
            return [normalize(item, seen) for item in value]
        if isinstance(value, set):
            normalized = [normalize(item, seen) for item in value]
            return sorted(
                normalized,
                key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True),
            )
        if hasattr(value, "__dict__"):
            return {
                str(key): normalize(item, seen)
                for key, item in sorted(value.__dict__.items())
                if not callable(item)
            }
        return repr(value)
    finally:
        seen.remove(identity)


def app_state(app: Any) -> dict[str, Any]:
    return {
        key: normalize(value)
        for key, value in sorted(app.__dict__.items())
        if key not in EXCLUDED_APP_FIELDS and not callable(value)
    }


def state_hash(state: dict[str, Any]) -> str:
    encoded = json.dumps(
        state,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(encoded)


def changed_top_level_fields(
    before: dict[str, Any], after: dict[str, Any]
) -> list[str]:
    keys = sorted(set(before) | set(after))
    return [key for key in keys if before.get(key) != after.get(key)]


def result_summary(value: Any) -> dict[str, Any]:
    if value is None:
        return {"type": "NoneType"}
    if isinstance(value, (list, tuple, dict, set)):
        return {"type": type(value).__name__, "size": len(value)}
    return {"type": type(value).__name__}


def audit_read(
    *,
    label: str,
    app: Any,
    method_name: str,
    args: dict[str, Any],
    expected_effect: bool,
) -> dict[str, Any]:
    events: list[Any] = []
    app.register_to_env(f"effect-closure-{label}", events.append)
    before = app_state(app)
    result = getattr(app, method_name)(**args)
    after = app_state(app)
    event = events[-1]

    detected_effect = before != after
    assert event.action.operation_type == OperationType.READ
    assert AgentEventFilter()(event) is False
    assert detected_effect is expected_effect

    return {
        "label": label,
        "app": type(app).__name__,
        "method": method_name,
        "args": args,
        "declared_operation_type": event.action.operation_type.value,
        "kept_by_official_agent_write_filter": AgentEventFilter()(event),
        "expected_effect": expected_effect,
        "detected_effect": detected_effect,
        "changed_top_level_fields": changed_top_level_fields(before, after),
        "before_state_sha256": state_hash(before),
        "after_state_sha256": state_hash(after),
        "result": result_summary(result),
    }


def new_cab(seed: int, start_time: float) -> CabApp:
    app = CabApp()
    app.rng = random.Random(seed)
    app.time_manager.reset(start_time=start_time)
    return app


def ride_projection(ride: Any) -> dict[str, Any]:
    return {
        "price": ride.price,
        "delay": ride.delay,
        "status": ride.status,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    start_time = 1_750_000_000.0
    cab_args = {
        "start_location": "A",
        "end_location": "B",
        "service_type": "Default",
        "ride_time": "2025-01-01 12:00:00",
    }

    unread_app = AgentUserInterface()
    unread_app.time_manager.reset(start_time=start_time)
    unread_app.send_message_to_agent("stateful read audit")
    unread_case = audit_read(
        label="message_unreadness_consumption",
        app=unread_app,
        method_name="get_last_unread_messages",
        args={},
        expected_effect=True,
    )
    unread_case["downstream_probe"] = {
        "same_read_result_count_after_effect": len(
            unread_app.get_last_unread_messages()
        )
    }

    cab_app = new_cab(seed=314159, start_time=start_time)
    cab_case = audit_read(
        label="cab_quote_rng_and_history",
        app=cab_app,
        method_name="get_quotation",
        args=cab_args,
        expected_effect=True,
    )
    after_quote_ride = cab_app.order_ride(**cab_args)
    direct_cab = new_cab(seed=314159, start_time=start_time)
    direct_ride = direct_cab.order_ride(**cab_args)
    cab_case["downstream_probe"] = {
        "direct_order": ride_projection(direct_ride),
        "after_quote_order": ride_projection(after_quote_ride),
        "different_later_write_result": ride_projection(direct_ride)
        != ride_projection(after_quote_ride),
    }
    assert cab_case["downstream_probe"]["different_later_write_result"] is True

    wait_callbacks: list[str] = []
    wait_app = SystemApp()
    wait_app.time_manager.reset(start_time=start_time)
    wait_app.wait_for_next_notification = lambda: wait_callbacks.append("called")
    wait_case = audit_read(
        label="wait_installs_timeout",
        app=wait_app,
        method_name="wait_for_notification",
        args={"timeout": 30},
        expected_effect=True,
    )
    wait_case["downstream_probe"] = {
        "scheduler_callback_count": len(wait_callbacks),
        "timeout_installed": wait_app.wait_for_notification_timeout is not None,
    }

    apartment_app = ApartmentListingApp()
    apartment_case = audit_read(
        label="apartment_catalog_pure_control",
        app=apartment_app,
        method_name="list_all_apartments",
        args={},
        expected_effect=False,
    )

    last_agent_app = AgentUserInterface()
    last_agent_app.time_manager.reset(start_time=start_time)
    last_agent_app.send_message_to_user("control message")
    last_agent_case = audit_read(
        label="last_agent_message_pure_control",
        app=last_agent_app,
        method_name="get_last_message_from_agent",
        args={},
        expected_effect=False,
    )

    clock_app = SystemApp()
    clock_app.time_manager.reset(start_time=start_time)
    clock_case = audit_read(
        label="current_time_pure_control",
        app=clock_app,
        method_name="get_current_time",
        args={},
        expected_effect=False,
    )

    cases = [
        unread_case,
        cab_case,
        wait_case,
        apartment_case,
        last_agent_case,
        clock_case,
    ]
    true_positive = sum(
        case["expected_effect"] and case["detected_effect"] for case in cases
    )
    true_negative = sum(
        (not case["expected_effect"]) and (not case["detected_effect"])
        for case in cases
    )

    script_path = Path(__file__).resolve()
    result = {
        "source": {
            "repository": "facebookresearch/meta-agents-research-environments",
            "revision": git_revision(args.are_root.resolve()),
            "python": sys.executable,
            "script": str(script_path),
            "script_sha256": sha256_bytes(script_path.read_bytes()),
        },
        "effect_closure_rule": (
            "A declared READ is retained by the audit when a curated semantic app-state "
            "projection changes across the call; framework callbacks, registries, clock "
            "objects, and instrumentation flags are excluded."
        ),
        "official_baseline": (
            "AgentEventFilter discards every successful agent READ regardless of the "
            "detected semantic state delta."
        ),
        "cases": cases,
        "low_fidelity_summary": {
            "case_count": len(cases),
            "positive_controls": 3,
            "negative_controls": 3,
            "true_positive": true_positive,
            "true_negative": true_negative,
            "all_expected_labels_recovered": true_positive == 3
            and true_negative == 3,
        },
        "scope_limit": (
            "This is a six-case, researcher-curated source-level detector check on one "
            "frozen ARE revision. It tests changed computation and negative controls, "
            "not benchmark prevalence, an independently authored admission set, task "
            "success correction, model rankings, or leaderboard impact."
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
