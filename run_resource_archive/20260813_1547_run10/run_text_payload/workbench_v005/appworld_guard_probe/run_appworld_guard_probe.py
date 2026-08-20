from __future__ import annotations

import itertools
import json
import random
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch


TASK_ID = "37a8675_1"
APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
OUTPUT = Path(__file__).with_name("appworld_guard_results.json")
PREDICATES = ("contact_present", "receiver_resolvable", "sufficient_balance")
SEED = 20260813


@dataclass
class ExecutionResult:
    requested_state: dict[str, bool]
    observed_state: dict[str, bool]
    procedure_success: bool
    procedure_error: str | None
    official_terminal_success: bool
    official_passed: int
    official_total: int
    failed_requirements: list[str]
    api_trace: list[dict[str, Any]]


def main_user(world: AppWorld) -> MainUserMunch:
    if world.models is None:
        raise RuntimeError("AppWorld models are unavailable.")
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("Supervisor was not found in the input database.")
    return MainUserMunch.from_main_user(model)


def parse_task(world: AppWorld) -> tuple[str, float, bool]:
    instruction = world.task.instruction
    phone_match = re.search(r"\b(\d{10})\b", instruction)
    amount_match = re.search(r"\$(\d+(?:\.\d+)?)", instruction)
    if phone_match is None or amount_match is None:
        raise RuntimeError(f"Could not parse task instruction: {instruction}")
    return phone_match.group(1), float(amount_match.group(1)), "privately" in instruction.lower()


def mutate_state(world: AppWorld, requested: dict[str, bool], target_phone: str, amount: float) -> None:
    if world.models is None:
        raise RuntimeError("AppWorld models are unavailable.")
    supervisor = dict(world.task.supervisor)
    phone_user = world.models.phone.User.find_one(phone_number=supervisor["phone_number"])
    venmo_user = world.models.venmo.User.find_one(email=supervisor["email"])
    if phone_user is None or venmo_user is None:
        raise RuntimeError("Supervisor app accounts were not found.")
    contact = world.models.phone.Contact.find_one(user_id=phone_user.id, phone_number=target_phone)
    if contact is None:
        raise RuntimeError("Target contact was not present in the clean fixture.")

    if not requested["contact_present"]:
        contact.delete()
    elif not requested["receiver_resolvable"]:
        contact.email = "no-such-venmo-user@example.com"
        contact.save()

    venmo_user.venmo_balance = amount + 100.0 if requested["sufficient_balance"] else max(0.0, amount - 1.0)
    venmo_user.save()


def execute_fixed_procedure(world: AppWorld, target_phone: str, amount: float, private: bool) -> tuple[bool, str | None, list[dict[str, Any]], dict[str, bool]]:
    user = main_user(world)
    trace: list[dict[str, Any]] = []
    observed = {name: False for name in PREDICATES}
    try:
        phone_token = world.apis.phone.access_token_from(user)
        contacts = world.apis.phone.search_contacts(
            access_token=phone_token,
            query=target_phone,
            page_limit=20,
        )
        exact_contacts = [item for item in contacts if item["phone_number"] == target_phone]
        observed["contact_present"] = len(exact_contacts) == 1
        trace.append({"api": "phone.search_contacts", "match_count": len(exact_contacts)})
        if len(exact_contacts) != 1:
            raise RuntimeError("target_contact_not_unique")
        receiver_email = exact_contacts[0]["email"]

        venmo_token = world.apis.venmo.access_token_from(user)
        receivers = world.apis.venmo.search_users(
            access_token=venmo_token,
            query=receiver_email,
            page_limit=20,
        )
        exact_receivers = [item for item in receivers if item["email"] == receiver_email]
        observed["receiver_resolvable"] = len(exact_receivers) == 1
        trace.append({"api": "venmo.search_users", "match_count": len(exact_receivers)})
        if len(exact_receivers) != 1:
            raise RuntimeError("receiver_not_resolvable")

        account = world.apis.venmo.show_account(access_token=venmo_token)
        observed["sufficient_balance"] = float(account["venmo_balance"]) >= amount
        trace.append(
            {
                "api": "venmo.show_account",
                "balance_sufficient": observed["sufficient_balance"],
            }
        )
        response = world.apis.venmo.create_transaction(
            access_token=venmo_token,
            receiver_email=receiver_email,
            amount=amount,
            description="",
            private=private,
        )
        trace.append(
            {
                "api": "venmo.create_transaction",
                "message": response.get("message"),
                "has_transaction_id": "transaction_id" in response,
            }
        )
        if "transaction_id" in response:
            completion = world.apis.supervisor.complete_task(answer=None, status="success")
            trace.append({"api": "supervisor.complete_task", "message": completion.get("message")})
        world.execute("pass")
        return "transaction_id" in response, None, trace, observed
    except Exception as exc:  # AppWorld wraps API failures in runtime-specific exception types.
        world.execute("pass")
        return False, f"{type(exc).__name__}: {exc}", trace, observed


def run_state(bits: tuple[bool, ...]) -> ExecutionResult:
    requested = dict(zip(PREDICATES, bits))
    state_code = "".join("1" if value else "0" for value in bits)
    world = AppWorld(
        task_id=TASK_ID,
        experiment_name=f"scratch_v005_guard_{state_code}",
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        munchify_response=True,
    )
    try:
        target_phone, amount, private = parse_task(world)
        mutate_state(world, requested, target_phone, amount)
        procedure_success, procedure_error, trace, observed = execute_fixed_procedure(
            world, target_phone, amount, private
        )
        tracker = world.evaluate(suppress_errors=True)
        stats = tracker.to_dict(stats_only=True)
        total = int(stats["num_tests"])
        terminal_success = bool(stats["success"])
        passed = total if terminal_success else max(0, total - len(tracker.failures))
        return ExecutionResult(
            requested_state=requested,
            observed_state=observed,
            procedure_success=procedure_success,
            procedure_error=procedure_error,
            official_terminal_success=terminal_success,
            official_passed=passed,
            official_total=total,
            failed_requirements=[failure["requirement"].strip() for failure in tracker.failures],
            api_trace=trace,
        )
    finally:
        world.close()


def conjunction_hypotheses() -> list[tuple[int, ...]]:
    hypotheses: list[tuple[int, ...]] = []
    for size in range(len(PREDICATES) + 1):
        hypotheses.extend(itertools.combinations(range(len(PREDICATES)), size))
    return hypotheses


def predicts(hypothesis: tuple[int, ...], state: tuple[bool, ...]) -> bool:
    return all(state[index] for index in hypothesis)


def consistent(hypothesis: tuple[int, ...], observations: list[tuple[tuple[bool, ...], bool]]) -> bool:
    return all(predicts(hypothesis, state) is label for state, label in observations)


def learn_guard(outcomes: dict[tuple[bool, ...], bool]) -> dict[str, Any]:
    source = (True, True, True)
    paired_queries = [source, (False, True, True), (True, False, True), (True, True, False)]
    paired_observations = [(state, outcomes[state]) for state in paired_queries]
    paired_space = [item for item in conjunction_hypotheses() if consistent(item, paired_observations)]

    rng = random.Random(SEED)
    random_records: list[dict[str, Any]] = []
    alternatives = [state for state in outcomes if state != source]
    for _ in range(500):
        queries = [source, *rng.sample(alternatives, 3)]
        observations = [(state, outcomes[state]) for state in queries]
        space = [item for item in conjunction_hypotheses() if consistent(item, observations)]
        prediction = min(space, key=lambda item: (len(item), item))
        exact = all(predicts(prediction, state) is label for state, label in outcomes.items())
        false_admissions = sum(predicts(prediction, state) and not label for state, label in outcomes.items())
        random_records.append({"exact": exact, "false_admissions": false_admissions})

    paired_prediction = min(paired_space, key=lambda item: (len(item), item))
    return {
        "hypothesis_class": "positive conjunctions over the three declared observable predicates",
        "known_positive_source": dict(zip(PREDICATES, source)),
        "paired_single_predicate_interventions": [dict(zip(PREDICATES, state)) for state in paired_queries[1:]],
        "paired_prediction": [PREDICATES[index] for index in paired_prediction],
        "paired_version_space_size": len(paired_space),
        "paired_exact": all(predicts(paired_prediction, state) is label for state, label in outcomes.items()),
        "paired_false_admissions": sum(
            predicts(paired_prediction, state) and not label for state, label in outcomes.items()
        ),
        "random_same_budget_trials": len(random_records),
        "random_exact_rate": sum(item["exact"] for item in random_records) / len(random_records),
        "random_mean_false_admissions": sum(item["false_admissions"] for item in random_records) / len(random_records),
    }


def main() -> None:
    records = [run_state(bits) for bits in itertools.product((False, True), repeat=len(PREDICATES))]
    outcomes = {
        tuple(record.requested_state[name] for name in PREDICATES): record.official_terminal_success
        for record in records
    }
    payload: dict[str, Any] = {
        "artifact_class": "scratch",
        "claim_boundary": (
            "This dev-set probe checks whether declared observable predicates can be intervened on and "
            "whether fixed-procedure replay yields an independently scored applicability function. "
            "The predicate catalogue and state mutators are hand-declared; this is not automatic predicate discovery."
        ),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "benchmark": {
            "name": "AppWorld",
            "git_commit": APPWORLD_COMMIT,
            "dataset": "dev",
            "task_id": TASK_ID,
            "construction_did_not_call_official_solution": True,
            "evaluation": "world.evaluate hidden from the fixed procedure",
        },
        "predicate_catalogue": list(PREDICATES),
        "records": [asdict(record) for record in records],
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    payload["guard_learning"] = learn_guard(outcomes)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
