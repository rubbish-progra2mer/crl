from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch

from witness_compiler import compile_witness, evaluate_witness, resolve_bindings


OUTPUT_PATH = Path(__file__).with_name("false_alarm_diagnostics.json")
FIXTURES = (
    ("6171bbc_1", "spotify", "create_playlist"),
    ("4fab96f_1", "venmo", "remind_payment_request"),
)


def _plain(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


def _main_user(world: AppWorld) -> MainUserMunch:
    assert world.models is not None
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("AppWorld supervisor was not found in the task database.")
    return MainUserMunch.from_main_user(model)


def diagnose(task_id: str, app_name: str, write_api: str) -> dict[str, Any]:
    world = AppWorld(
        task_id=task_id,
        experiment_name=f"scratch_v001_false_alarm_diagnosis_{task_id}_{write_api}",
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        parse_datetimes=True,
        munchify_response=True,
    )
    observation: dict[str, Any] = {}
    try:
        app = getattr(world.apis, app_name)
        original_write: Callable[..., Any] = getattr(app, write_api)

        def intercepted_write(*args: Any, **kwargs: Any) -> Any:
            response = original_write(*args, **kwargs)
            response_plain = _plain(response)
            plan = compile_witness(
                getattr(world.task.api_docs, app_name),
                write_api,
                kwargs,
                response_plain,
            )
            observation.update(
                {
                    "write_arguments": _plain(kwargs),
                    "write_response": response_plain,
                    "plan": None if plan is None else plan.to_dict(),
                }
            )
            if plan is None:
                return response
            read_arguments = resolve_bindings(plan, kwargs, response_plain)
            read_response = getattr(app, plan.read_api)(**read_arguments)
            observation.update(
                {
                    "read_arguments": _plain(read_arguments),
                    "read_response": _plain(read_response),
                    "witness_result": evaluate_witness(plan, read_response, kwargs),
                }
            )
            return response

        setattr(app, write_api, intercepted_write)
        ground_truth = world.task.ground_truth
        assert ground_truth is not None
        world.shell.user_ns.update(
            {
                "official_solution": ground_truth.solution_module().solution,
                "main_user": _main_user(world),
                "public_data": ground_truth.public_data,
            }
        )
        execution_message = world.execute(
            "official_solution(main_user, apis, requester, public_data)"
        )
        tracker = world.evaluate(suppress_errors=True)
        return {
            "task_id": task_id,
            "write_api": f"{app_name}.{write_api}",
            "execution_message": execution_message,
            "terminal_success": bool(tracker.success),
            "terminal_test_count": int(tracker.num_tests),
            "observation": observation,
        }
    finally:
        world.close()


def main() -> None:
    results = [diagnose(*fixture) for fixture in FIXTURES]
    payload = {
        "artifact_class": "scratch_diagnostic",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "scope": "Clean-run diagnosis of two previously observed witness false alarms.",
        "results": results,
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    for result in results:
        observation = result["observation"]
        plan = observation.get("plan") or {}
        print(
            json.dumps(
                {
                    "task_id": result["task_id"],
                    "read_api": plan.get("read_api"),
                    "read_arguments": observation.get("read_arguments"),
                    "witness_result": observation.get("witness_result"),
                    "terminal_success": result["terminal_success"],
                },
                ensure_ascii=False,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
