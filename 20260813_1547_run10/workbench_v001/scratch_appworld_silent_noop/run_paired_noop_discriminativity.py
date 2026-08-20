from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch

from witness_compiler import compile_witness, evaluate_witness, resolve_bindings


APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
HERE = Path(__file__).resolve().parent
CLEAN_RESULTS_PATH = HERE / "unselected_clean_coverage.json"
OUTPUT_PATH = HERE / "paired_noop_discriminativity.json"


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
class ProbeResult:
    task_id: str
    write_api: str
    target_call_count: int
    compiled: bool
    read_api: str | None
    relation_count: int
    noop_witness_result: bool | None
    read_error: str | None
    write_arguments: dict[str, Any] | None
    authentic_response: dict[str, Any]
    plan: dict[str, Any] | None
    read_arguments: dict[str, Any] | None
    read_response: Any
    terminal_success: bool
    terminal_test_count: int
    execution_message: str


def _plain(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


def _main_user(world: AppWorld) -> MainUserMunch:
    assert world.models is not None
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("AppWorld supervisor was not found in the task database.")
    return MainUserMunch.from_main_user(model)


def _authentic_responses() -> dict[tuple[str, str], dict[str, Any]]:
    payload = json.loads(CLEAN_RESULTS_PATH.read_text(encoding="utf-8"))
    responses: dict[tuple[str, str], dict[str, Any]] = {}
    for result in payload["results"]:
        app_name, write_api = result["write_api"].split(".", maxsplit=1)
        response = result["selected_response"]
        if response is None:
            raise RuntimeError(f"Missing clean response for {result['task_id']} {write_api}.")
        responses[(result["task_id"], f"{app_name}.{write_api}")] = response
    return responses


def run_fixture(
    fixture: Fixture, authentic_response: dict[str, Any]
) -> ProbeResult:
    world = AppWorld(
        task_id=fixture.task_id,
        experiment_name=f"scratch_v001_paired_noop_{fixture.task_id}_{fixture.write_api}",
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        parse_datetimes=True,
        munchify_response=True,
    )
    observation: dict[str, Any] = {
        "target_call_count": 0,
        "compiled": False,
        "read_api": None,
        "relation_count": 0,
        "noop_witness_result": None,
        "read_error": None,
        "write_arguments": None,
        "plan": None,
        "read_arguments": None,
        "read_response": None,
    }
    try:
        app = getattr(world.apis, fixture.app_name)

        def silent_noop(*args: Any, **kwargs: Any) -> dict[str, Any]:
            observation["target_call_count"] += 1
            if observation["target_call_count"] != 1:
                return authentic_response
            observation["write_arguments"] = _plain(kwargs)
            plan = compile_witness(
                getattr(world.task.api_docs, fixture.app_name),
                fixture.write_api,
                kwargs,
                authentic_response,
            )
            if plan is None:
                return authentic_response
            observation["compiled"] = True
            observation["read_api"] = plan.read_api
            observation["relation_count"] = len(plan.relations)
            observation["plan"] = plan.to_dict()
            read_arguments = resolve_bindings(plan, kwargs, authentic_response)
            observation["read_arguments"] = _plain(read_arguments)
            try:
                read_response = getattr(app, plan.read_api)(**read_arguments)
                observation["read_response"] = _plain(read_response)
                observation["noop_witness_result"] = evaluate_witness(
                    plan, read_response, kwargs
                )
            except Exception as exception:
                observation["read_error"] = f"{type(exception).__name__}: {exception}"
            return authentic_response

        setattr(app, fixture.write_api, silent_noop)
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
        return ProbeResult(
            task_id=fixture.task_id,
            write_api=f"{fixture.app_name}.{fixture.write_api}",
            authentic_response=authentic_response,
            terminal_success=bool(tracker.success),
            terminal_test_count=int(tracker.num_tests),
            execution_message=execution_message,
            **observation,
        )
    finally:
        world.close()


def main() -> None:
    authentic_responses = _authentic_responses()
    results: list[ProbeResult] = []
    for fixture in FIXTURES:
        full_api = f"{fixture.app_name}.{fixture.write_api}"
        result = run_fixture(
            fixture, authentic_responses[(fixture.task_id, full_api)]
        )
        results.append(result)
        print(
            json.dumps(
                {
                    "task_id": result.task_id,
                    "write_api": result.write_api,
                    "compiled": result.compiled,
                    "read_api": result.read_api,
                    "noop_witness_result": result.noop_witness_result,
                    "terminal_success": result.terminal_success,
                    "read_error": result.read_error,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    payload = {
        "artifact_class": "scratch",
        "claim_boundary": (
            "Each no-op world starts from the same AppWorld dev task and follows the deterministic "
            "official solution prefix. The first target write returns the authentic response captured "
            "in the paired clean world but performs no state mutation. The compiler only receives "
            "public tool docs, instantiated arguments, and that response."
        ),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "benchmark": {
            "name": "AppWorld",
            "git_commit": APPWORLD_COMMIT,
            "dataset": "dev",
            "fixture_count": len(FIXTURES),
            "paired_clean_artifact": CLEAN_RESULTS_PATH.name,
        },
        "results": [asdict(result) for result in results],
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
