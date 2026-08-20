from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch
from munch import munchify

from witness_compiler import (
    WitnessPlan,
    compile_witness,
    evaluate_witness,
    resolve_bindings,
)


TASK_ID = "37a8675_1"
APP_NAME = "venmo"
WRITE_API = "create_transaction"
SUCCESSFUL_WRITE_INDEX = 4
APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
OUTPUT_PATH = Path(__file__).with_name("auto_raw_results.json")


@dataclass
class ConditionResult:
    condition: str
    toolgate_accepts: bool
    injected: bool
    compiled_plan: dict[str, Any] | None
    witness_result: bool | None
    replayed: bool
    write_responses: list[dict[str, Any]]
    evaluation: dict[str, Any]
    failed_requirements: list[str]
    execute_message: str


def _main_user(world: AppWorld) -> MainUserMunch:
    assert world.models is not None
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("AppWorld supervisor was not found in the task input database.")
    return MainUserMunch.from_main_user(model)


def _plain(value: Any) -> dict[str, Any]:
    return json.loads(json.dumps(value, default=str))


def _run_compiled_witness(
    world: AppWorld,
    write_arguments: dict[str, Any],
    write_response: dict[str, Any],
) -> tuple[WitnessPlan, bool]:
    app_docs = getattr(world.task.api_docs, APP_NAME)
    plan = compile_witness(app_docs, WRITE_API, write_arguments, write_response)
    if plan is None:
        raise RuntimeError("No executable witness could be compiled from public tool docs.")
    read_arguments = resolve_bindings(plan, write_arguments, write_response)
    read_api: Callable[..., Any] = getattr(getattr(world.apis, APP_NAME), plan.read_api)
    try:
        read_response = read_api(**read_arguments)
    except Exception:
        return plan, False
    return plan, evaluate_witness(plan, read_response, write_arguments)


def run_condition(condition: str) -> ConditionResult:
    valid_conditions = {"clean", "silent_noop", "silent_noop_with_compiled_witness"}
    if condition not in valid_conditions:
        raise ValueError(f"Unknown condition: {condition}")
    injected = condition != "clean"
    use_compiler = condition == "silent_noop_with_compiled_witness"
    world = AppWorld(
        task_id=TASK_ID,
        experiment_name=f"scratch_v001_auto_{condition}",
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        munchify_response=True,
    )
    write_responses: list[dict[str, Any]] = []
    successful_write_arguments: dict[str, Any] | None = None
    successful_write_response: dict[str, Any] | None = None
    compiled_plan: WitnessPlan | None = None
    witness_result: bool | None = None
    replayed = False
    try:
        original_write: Callable[..., Any] = world.apis.venmo.create_transaction

        def intercepted_write(*args: Any, **kwargs: Any) -> Any:
            nonlocal successful_write_arguments, successful_write_response
            call_index = len(write_responses) + 1
            if injected and call_index == SUCCESSFUL_WRITE_INDEX:
                successful_write_arguments = dict(kwargs)
                response = munchify({"message": "Sent money.", "transaction_id": 8216})
                successful_write_response = _plain(response)
            else:
                response = original_write(*args, **kwargs)
            write_responses.append(
                {
                    "call_index": call_index,
                    "response": _plain(response),
                    "executed": not (injected and call_index == SUCCESSFUL_WRITE_INDEX),
                }
            )
            return response

        world.apis.venmo.create_transaction = intercepted_write
        ground_truth = world.task.ground_truth
        assert ground_truth is not None
        official_solution = ground_truth.solution_module().solution
        world.shell.user_ns.update(
            {
                "official_solution": official_solution,
                "main_user": _main_user(world),
                "public_data": ground_truth.public_data,
            }
        )
        execute_message = world.execute(
            "official_solution(main_user, apis, requester, public_data)"
        )

        if use_compiler:
            if successful_write_arguments is None or successful_write_response is None:
                raise RuntimeError("The expected schema-valid no-op was not injected.")
            compiled_plan, witness_result = _run_compiled_witness(
                world, successful_write_arguments, successful_write_response
            )
            if not witness_result:
                original_write(**successful_write_arguments)
                replayed = True
            world.execute("pass")

        tracker = world.evaluate(suppress_errors=True)
        return ConditionResult(
            condition=condition,
            toolgate_accepts=any(
                "transaction_id" in item["response"] for item in write_responses
            ),
            injected=injected,
            compiled_plan=None if compiled_plan is None else compiled_plan.to_dict(),
            witness_result=witness_result,
            replayed=replayed,
            write_responses=write_responses,
            evaluation=tracker.to_dict(stats_only=True),
            failed_requirements=[
                failure["requirement"].strip() for failure in tracker.failures
            ],
            execute_message=execute_message,
        )
    finally:
        world.close()


def main() -> None:
    results = [
        run_condition("clean"),
        run_condition("silent_noop"),
        run_condition("silent_noop_with_compiled_witness"),
    ]
    payload = {
        "artifact_class": "scratch",
        "claim_boundary": (
            "The compiler sees only public tool docs and the instantiated write call. "
            "This one-task deterministic replay tests automatic plan construction and "
            "carrier feasibility, not generalization or method-paper sufficiency."
        ),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "benchmark": {
            "name": "AppWorld",
            "git_commit": APPWORLD_COMMIT,
            "dataset": "dev",
            "task_id": TASK_ID,
            "official_terminal_tests": 6,
        },
        "compiler_inputs": [
            "public API name/method/path/description",
            "public parameter and response schemas",
            "instantiated write arguments",
            "observed write response",
        ],
        "compiler_forbidden_inputs": [
            "service source code",
            "task ground truth",
            "evaluation program",
            "historical correct traces",
        ],
        "conditions": [asdict(result) for result in results],
    }
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as file:
        file.write(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
