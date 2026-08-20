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


APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
OUTPUT_PATH = Path(__file__).with_name("multitask_auto_raw_results.json")


@dataclass(frozen=True)
class Fixture:
    task_id: str
    app_name: str
    write_api: str
    successful_call_index: int
    structure: str


FIXTURES = (
    Fixture("37a8675_1", "venmo", "create_transaction", 4, "single_atomic_write"),
    Fixture("530b157_1", "phone", "send_text_message", 1, "cross_app_partial_success"),
    Fixture("6171bbc_1", "spotify", "add_song_to_playlist", 1, "parent_child_missing_member"),
    Fixture("6c2c621_1", "file_system", "create_file", 1, "batch_missing_item"),
)


@dataclass
class ConditionResult:
    task_id: str
    structure: str
    condition: str
    injection_triggered: bool
    target_call_count: int
    selected_write_response: dict[str, Any] | None
    compiled_plan: dict[str, Any] | None
    witness_result: bool | None
    replayed: bool
    evaluation: dict[str, Any]
    failed_requirement_count: int
    execute_message: str


def _plain(value: Any) -> dict[str, Any]:
    return json.loads(json.dumps(value, default=str))


def _main_user(world: AppWorld) -> MainUserMunch:
    assert world.models is not None
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("AppWorld supervisor was not found in the task input database.")
    return MainUserMunch.from_main_user(model)


def _execute_witness(
    world: AppWorld,
    fixture: Fixture,
    write_arguments: dict[str, Any],
    write_response: dict[str, Any],
) -> tuple[WitnessPlan, bool]:
    app_docs = getattr(world.task.api_docs, fixture.app_name)
    plan = compile_witness(app_docs, fixture.write_api, write_arguments, write_response)
    if plan is None:
        raise RuntimeError("No executable witness could be compiled from public tool docs.")
    read_arguments = resolve_bindings(plan, write_arguments, write_response)
    read_api: Callable[..., Any] = getattr(
        getattr(world.apis, fixture.app_name), plan.read_api
    )
    try:
        read_response = read_api(**read_arguments)
    except Exception:
        return plan, False
    return plan, evaluate_witness(plan, read_response, write_arguments)


def run_condition(
    fixture: Fixture,
    condition: str,
    forged_response: dict[str, Any] | None = None,
) -> tuple[ConditionResult, list[dict[str, Any]]]:
    if condition not in {
        "clean",
        "clean_with_compiled_witness",
        "silent_noop",
        "silent_noop_with_compiled_witness",
    }:
        raise ValueError(f"Unknown condition: {condition}")
    inject = condition.startswith("silent_noop")
    use_compiler = condition.endswith("with_compiled_witness")
    world = AppWorld(
        task_id=fixture.task_id,
        experiment_name=f"scratch_v001_multi_{fixture.task_id}_{condition}",
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        parse_datetimes=True,
        munchify_response=True,
    )
    target_responses: list[dict[str, Any]] = []
    target_arguments: dict[str, Any] | None = None
    injection_triggered = False
    compiled_plan: WitnessPlan | None = None
    witness_result: bool | None = None
    replayed = False
    try:
        app = getattr(world.apis, fixture.app_name)
        original_write: Callable[..., Any] = getattr(app, fixture.write_api)

        def intercepted_write(*args: Any, **kwargs: Any) -> Any:
            nonlocal target_arguments, injection_triggered
            call_index = len(target_responses) + 1
            if call_index == fixture.successful_call_index:
                target_arguments = dict(kwargs)
            if inject and call_index == fixture.successful_call_index:
                if forged_response is None:
                    raise RuntimeError("Fault condition requires a clean paired response.")
                response = munchify(forged_response)
                injection_triggered = True
            else:
                response = original_write(*args, **kwargs)
            target_responses.append(_plain(response))
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

        if use_compiler:
            selected_response = (
                forged_response
                if inject
                else target_responses[fixture.successful_call_index - 1]
                if len(target_responses) >= fixture.successful_call_index
                else None
            )
            if target_arguments is None or selected_response is None:
                raise RuntimeError("The selected write call was not observed.")
            compiled_plan, witness_result = _execute_witness(
                world, fixture, target_arguments, selected_response
            )
            if inject and not witness_result:
                original_write(**target_arguments)
                replayed = True
            world.execute("pass")

        tracker = world.evaluate(suppress_errors=True)
        selected = (
            target_responses[fixture.successful_call_index - 1]
            if len(target_responses) >= fixture.successful_call_index
            else None
        )
        result = ConditionResult(
            task_id=fixture.task_id,
            structure=fixture.structure,
            condition=condition,
            injection_triggered=injection_triggered,
            target_call_count=len(target_responses),
            selected_write_response=selected,
            compiled_plan=None if compiled_plan is None else compiled_plan.to_dict(),
            witness_result=witness_result,
            replayed=replayed,
            evaluation=tracker.to_dict(stats_only=True),
            failed_requirement_count=len(tracker.failures),
            execute_message=execute_message,
        )
        return result, target_responses
    finally:
        world.close()


def main() -> None:
    results: list[ConditionResult] = []
    for fixture in FIXTURES:
        clean, clean_responses = run_condition(fixture, "clean")
        if not clean.evaluation["success"]:
            raise RuntimeError(f"Clean paired replay failed for {fixture.task_id}.")
        if len(clean_responses) < fixture.successful_call_index:
            raise RuntimeError(f"Target write did not reach the configured call index: {fixture}")
        forged_response = clean_responses[fixture.successful_call_index - 1]
        silent, _ = run_condition(fixture, "silent_noop", forged_response)
        clean_checked, _ = run_condition(fixture, "clean_with_compiled_witness")
        recovered, _ = run_condition(
            fixture, "silent_noop_with_compiled_witness", forged_response
        )
        results.extend([clean, clean_checked, silent, recovered])

    payload = {
        "artifact_class": "scratch",
        "claim_boundary": (
            "Deterministic dev-task replay tests whether one source-free compiler can construct "
            "and execute witnesses across four structures. Official solutions drive the task "
            "only as a controlled carrier; no agent-effect or held-out-generalization claim is made."
        ),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "benchmark": {
            "name": "AppWorld",
            "git_commit": APPWORLD_COMMIT,
            "dataset": "dev",
            "fixture_count": len(FIXTURES),
        },
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
