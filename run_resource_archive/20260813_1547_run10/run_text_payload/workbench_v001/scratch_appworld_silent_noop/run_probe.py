from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch
from munch import munchify


TASK_ID = "37a8675_1"
SUCCESSFUL_WRITE_INDEX = 4
APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
OUTPUT_PATH = Path(__file__).with_name("raw_results.json")


@dataclass
class ConditionResult:
    condition: str
    toolgate_accepts: bool
    injected: bool
    witness_checked: bool
    witness_found_relation: bool | None
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


def _redact_response(value: Any) -> dict[str, Any]:
    return json.loads(json.dumps(value, default=str))


def run_condition(condition: str) -> ConditionResult:
    if condition not in {"clean", "silent_noop", "silent_noop_with_witness"}:
        raise ValueError(f"Unknown condition: {condition}")

    experiment_name = f"scratch_v001_{condition}"
    world = AppWorld(
        task_id=TASK_ID,
        experiment_name=experiment_name,
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        munchify_response=True,
    )
    injected = condition != "clean"
    use_witness = condition == "silent_noop_with_witness"
    write_responses: list[dict[str, Any]] = []
    successful_write_kwargs: dict[str, Any] | None = None
    replayed = False
    witness_found_relation: bool | None = None

    try:
        original_write: Callable[..., Any] = world.apis.venmo.create_transaction

        def intercepted_write(*args: Any, **kwargs: Any) -> Any:
            nonlocal successful_write_kwargs
            call_index = len(write_responses) + 1
            if injected and call_index == SUCCESSFUL_WRITE_INDEX:
                successful_write_kwargs = dict(kwargs)
                response = munchify({"message": "Sent money.", "transaction_id": 8216})
            else:
                response = original_write(*args, **kwargs)
            write_responses.append(
                {
                    "call_index": call_index,
                    "response": _redact_response(response),
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

        if use_witness:
            if successful_write_kwargs is None:
                raise RuntimeError("The expected schema-valid successful write was not injected.")
            access_token = successful_write_kwargs["access_token"]
            receiver_email = successful_write_kwargs["receiver_email"]
            amount = successful_write_kwargs["amount"]
            description = successful_write_kwargs["description"]
            private = successful_write_kwargs["private"]
            visible_transactions = world.apis.venmo.show_transactions(
                access_token=access_token,
                user_email=receiver_email,
                direction="sent",
                page_limit=20,
            )
            witness_found_relation = any(
                transaction["amount"] == amount
                and transaction["description"] == description
                and transaction["private"] is private
                and transaction["receiver"]["email"] == receiver_email
                for transaction in visible_transactions
            )
            if not witness_found_relation:
                original_write(**successful_write_kwargs)
                replayed = True
            # Persist the witness/replay state through AppWorld's ordinary execution path.
            world.execute("pass")

        tracker = world.evaluate(suppress_errors=True)
        toolgate_accepts = any(
            "transaction_id" in item["response"] for item in write_responses
        )
        return ConditionResult(
            condition=condition,
            toolgate_accepts=toolgate_accepts,
            injected=injected,
            witness_checked=use_witness,
            witness_found_relation=witness_found_relation,
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
        run_condition("silent_noop_with_witness"),
    ]
    payload = {
        "artifact_class": "scratch",
        "claim_boundary": (
            "This probe tests carrier feasibility and distinguishability only; "
            "the witness is hand-wired and does not establish automatic compilation."
        ),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "benchmark": {
            "name": "AppWorld",
            "git_commit": APPWORLD_COMMIT,
            "dataset": "dev",
            "task_id": TASK_ID,
            "official_terminal_tests": 6,
        },
        "fault": {
            "kind": "schema_valid_silent_noop",
            "target": "venmo.create_transaction",
            "injected_call_index": SUCCESSFUL_WRITE_INDEX,
            "forged_response": {"message": "Sent money.", "transaction_id": 8216},
        },
        "conditions": [asdict(result) for result in results],
    }
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as file:
        file.write(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
