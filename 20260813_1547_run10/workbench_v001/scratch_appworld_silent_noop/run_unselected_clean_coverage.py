from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch

from witness_compiler import (
    compile_witness,
    evaluate_witness,
    resolve_bindings,
)


APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
OUTPUT_PATH = Path(__file__).with_name("unselected_clean_coverage.json")


@dataclass(frozen=True)
class Fixture:
    task_id: str
    app_name: str
    write_api: str


FIXTURES = (
    Fixture("d4e9306_1", "spotify", "follow_artist"),
    Fixture("3ab5b8b_1", "spotify", "download_song"),
    Fixture("df61dc5_1", "venmo", "like_transaction"),
    Fixture("57c3486_1", "spotify", "like_song"),
    Fixture("68ee2c9_1", "file_system", "move_file"),
    Fixture("6171bbc_1", "spotify", "create_playlist"),
    Fixture("396c5a2_1", "spotify", "add_to_queue"),
    Fixture("4fab96f_1", "venmo", "remind_payment_request"),
    Fixture("b119b1f_1", "spotify", "previous_song"),
    Fixture("b119b1f_2", "spotify", "next_song"),
)


@dataclass
class CoverageResult:
    task_id: str
    write_api: str
    target_call_count: int
    selected_response: dict[str, Any] | None
    compiled: bool
    read_api: str | None
    relation_count: int
    witness_result: bool | None
    read_error: str | None
    terminal_success: bool
    terminal_test_count: int
    execute_message: str


def _plain(value: Any) -> dict[str, Any]:
    return json.loads(json.dumps(value, default=str))


def _main_user(world: AppWorld) -> MainUserMunch:
    assert world.models is not None
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("AppWorld supervisor was not found in the task input database.")
    return MainUserMunch.from_main_user(model)


def run_fixture(fixture: Fixture) -> CoverageResult:
    world = AppWorld(
        task_id=fixture.task_id,
        experiment_name=f"scratch_v001_unselected_clean_{fixture.task_id}_{fixture.write_api}",
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        parse_datetimes=True,
        munchify_response=True,
    )
    call_count = 0
    selected_response: dict[str, Any] | None = None
    compiled_plan: dict[str, Any] | None = None
    witness_result: bool | None = None
    read_error: str | None = None
    try:
        app = getattr(world.apis, fixture.app_name)
        original_write: Callable[..., Any] = getattr(app, fixture.write_api)

        def intercepted_write(*args: Any, **kwargs: Any) -> Any:
            nonlocal call_count, selected_response, compiled_plan, witness_result, read_error
            call_count += 1
            response = original_write(*args, **kwargs)
            if call_count != 1:
                return response
            selected_response = _plain(response)
            plan = compile_witness(
                getattr(world.task.api_docs, fixture.app_name),
                fixture.write_api,
                kwargs,
                selected_response,
            )
            if plan is None:
                return response
            compiled_plan = plan.to_dict()
            read_arguments = resolve_bindings(plan, kwargs, selected_response)
            read_api: Callable[..., Any] = getattr(app, plan.read_api)
            try:
                read_response = read_api(**read_arguments)
                witness_result = evaluate_witness(plan, read_response, kwargs)
            except Exception as exception:
                witness_result = False
                read_error = f"{type(exception).__name__}: {exception}"
            return response

        setattr(app, fixture.write_api, intercepted_write)
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
        tracker = world.evaluate(suppress_errors=True)
        return CoverageResult(
            task_id=fixture.task_id,
            write_api=f"{fixture.app_name}.{fixture.write_api}",
            target_call_count=call_count,
            selected_response=selected_response,
            compiled=compiled_plan is not None,
            read_api=None if compiled_plan is None else str(compiled_plan["read_api"]),
            relation_count=(
                0 if compiled_plan is None else len(compiled_plan["relations"])
            ),
            witness_result=witness_result,
            read_error=read_error,
            terminal_success=bool(tracker.success),
            terminal_test_count=int(tracker.num_tests),
            execute_message=execute_message,
        )
    finally:
        world.close()


def main() -> None:
    results: list[CoverageResult] = []
    for fixture in FIXTURES:
        result = run_fixture(fixture)
        results.append(result)
        print(
            json.dumps(
                {
                    "task_id": result.task_id,
                    "write_api": result.write_api,
                    "compiled": result.compiled,
                    "read_api": result.read_api,
                    "witness_result": result.witness_result,
                    "terminal_success": result.terminal_success,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    payload = {
        "artifact_class": "scratch",
        "claim_boundary": (
            "Unselected clean dev trajectories measure witness coverage and false alarms only. "
            "They do not measure fault detection, recovery, or held-out agent performance."
        ),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "benchmark": {
            "name": "AppWorld",
            "git_commit": APPWORLD_COMMIT,
            "dataset": "dev",
            "fixture_count": len(FIXTURES),
        },
        "results": [asdict(result) for result in results],
    }
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as file:
        file.write(serialized)


if __name__ == "__main__":
    main()
