from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch

from witness_compiler import compile_witness, evaluate_witness, resolve_bindings


APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
OUTPUT_PATH = Path(__file__).with_name("discriminativity_probe.json")


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
    clean_post_result: bool | None
    rollback_noop_result: bool | None
    discriminative: bool | None
    read_error: str | None
    plan: dict[str, Any] | None
    write_arguments: dict[str, Any] | None
    write_response: dict[str, Any] | None
    clean_read_arguments: dict[str, Any] | None
    clean_read_response: Any
    rollback_read_response: Any
    execution_message: str


def _plain(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


def _main_user(world: AppWorld) -> MainUserMunch:
    assert world.models is not None
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("AppWorld supervisor was not found in the task database.")
    return MainUserMunch.from_main_user(model)


def run_fixture(fixture: Fixture) -> ProbeResult:
    experiment_name = f"scratch_v001_discriminativity_{fixture.task_id}_{fixture.write_api}"
    world = AppWorld(
        task_id=fixture.task_id,
        experiment_name=experiment_name,
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        parse_datetimes=True,
        munchify_response=True,
        # The trusted official dev solution calls this module's interceptor. The
        # interceptor needs AppWorld's checkpoint I/O, which the runtime monkey-
        # patch guard otherwise blocks as an unsafe file operation. Syntax checks
        # remain enabled; this setting is scoped to this deterministic Scratch probe.
        raise_on_unsafe_execution=False,
    )
    observation: dict[str, Any] = {
        "target_call_count": 0,
        "compiled": False,
        "read_api": None,
        "relation_count": 0,
        "clean_post_result": None,
        "rollback_noop_result": None,
        "discriminative": None,
        "read_error": None,
        "plan": None,
        "write_arguments": None,
        "write_response": None,
        "clean_read_arguments": None,
        "clean_read_response": None,
        "rollback_read_response": None,
    }
    try:
        app = getattr(world.apis, fixture.app_name)
        original_write: Callable[..., Any] = getattr(app, fixture.write_api)

        def intercepted_write(*args: Any, **kwargs: Any) -> Any:
            observation["target_call_count"] += 1
            if observation["target_call_count"] != 1:
                return original_write(*args, **kwargs)
            checkpoint_id = f"before_{fixture.app_name}_{fixture.write_api}"
            world.save_state(checkpoint_id)
            response = original_write(*args, **kwargs)
            response_plain = _plain(response)
            observation["write_arguments"] = _plain(kwargs)
            observation["write_response"] = response_plain
            plan = compile_witness(
                getattr(world.task.api_docs, fixture.app_name),
                fixture.write_api,
                kwargs,
                response_plain,
            )
            if plan is None:
                world.load_state(checkpoint_id)
                return response
            observation["compiled"] = True
            observation["read_api"] = plan.read_api
            observation["relation_count"] = len(plan.relations)
            observation["plan"] = plan.to_dict()
            read_arguments = resolve_bindings(plan, kwargs, response_plain)
            observation["clean_read_arguments"] = _plain(read_arguments)
            try:
                clean_response = getattr(app, plan.read_api)(**read_arguments)
                observation["clean_read_response"] = _plain(clean_response)
                observation["clean_post_result"] = evaluate_witness(
                    plan, clean_response, kwargs
                )
                world.load_state(checkpoint_id)
                rollback_app = getattr(world.apis, fixture.app_name)
                rollback_response = getattr(rollback_app, plan.read_api)(**read_arguments)
                observation["rollback_read_response"] = _plain(rollback_response)
                observation["rollback_noop_result"] = evaluate_witness(
                    plan, rollback_response, kwargs
                )
                observation["discriminative"] = bool(
                    observation["clean_post_result"]
                    and not observation["rollback_noop_result"]
                )
            except Exception as exception:
                observation["read_error"] = f"{type(exception).__name__}: {exception}"
                try:
                    world.load_state(checkpoint_id)
                except Exception:
                    pass
            return response

        setattr(app, fixture.write_api, intercepted_write)
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
        return ProbeResult(
            task_id=fixture.task_id,
            write_api=f"{fixture.app_name}.{fixture.write_api}",
            execution_message=execution_message,
            **observation,
        )
    finally:
        world.close()


def main() -> None:
    results: list[ProbeResult] = []
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
                    "clean_post_result": result.clean_post_result,
                    "rollback_noop_result": result.rollback_noop_result,
                    "discriminative": result.discriminative,
                    "read_error": result.read_error,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    payload = {
        "artifact_class": "scratch",
        "claim_boundary": (
            "The official dev solution only instantiates a valid write call. A named AppWorld "
            "checkpoint is captured before the real call; after observing the authentic response, "
            "the checkpoint is restored and the same response is treated as a silent no-op carrier. "
            "This measures immediate witness discriminativity, not agent-level recovery."
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
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
