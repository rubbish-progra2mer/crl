from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch


TASK_ID = "37a8675_1"
APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
OUTPUT = Path(__file__).with_name("appworld_observer_ab_results.json")


def main_user(world: AppWorld) -> MainUserMunch:
    if world.models is None:
        raise RuntimeError("AppWorld models are unavailable.")
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("Supervisor was not found in the input database.")
    return MainUserMunch.from_main_user(model)


def parse_task(world: AppWorld) -> tuple[str, float, bool]:
    phone_match = re.search(r"\b(\d{10})\b", world.task.instruction)
    amount_match = re.search(r"\$(\d+(?:\.\d+)?)", world.task.instruction)
    if phone_match is None or amount_match is None:
        raise RuntimeError("Could not parse the public task instruction.")
    return phone_match.group(1), float(amount_match.group(1)), "privately" in world.task.instruction.lower()


def execute_payment(world: AppWorld) -> list[dict[str, Any]]:
    user = main_user(world)
    target_phone, amount, private = parse_task(world)
    trace: list[dict[str, Any]] = []
    if world.models is None:
        raise RuntimeError("AppWorld models are unavailable.")
    sender = world.models.venmo.User.find_one(email=dict(world.task.supervisor)["email"])
    if sender is None:
        raise RuntimeError("Venmo sender was not found.")
    sender.venmo_balance = amount + 100.0
    sender.save()
    trace.append({"fixture_setup": "sender_balance", "sufficient": True})
    phone_token = world.apis.phone.access_token_from(user)
    contacts = world.apis.phone.search_contacts(
        access_token=phone_token,
        query=target_phone,
        page_limit=20,
    )
    exact_contacts = [item for item in contacts if item["phone_number"] == target_phone]
    trace.append({"api": "phone.search_contacts", "match_count": len(exact_contacts)})
    if len(exact_contacts) != 1:
        raise RuntimeError("target_contact_not_unique")

    venmo_token = world.apis.venmo.access_token_from(user)
    receivers = world.apis.venmo.search_users(
        access_token=venmo_token,
        query=exact_contacts[0]["email"],
        page_limit=20,
    )
    exact_receivers = [item for item in receivers if item["email"] == exact_contacts[0]["email"]]
    trace.append({"api": "venmo.search_users", "match_count": len(exact_receivers)})
    if len(exact_receivers) != 1:
        raise RuntimeError("receiver_not_resolvable")

    response = world.apis.venmo.create_transaction(
        access_token=venmo_token,
        receiver_email=exact_contacts[0]["email"],
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
    if "transaction_id" not in response:
        raise RuntimeError("transaction_id_missing")
    completion = world.apis.supervisor.complete_task(answer=None, status="success")
    trace.append({"api": "supervisor.complete_task", "message": completion.get("message")})
    return trace


def run(condition: str) -> dict[str, Any]:
    world = AppWorld(
        task_id=TASK_ID,
        experiment_name=f"scratch_v007_observer_{condition}",
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        munchify_response=True,
    )
    try:
        if world.models is None:
            raise RuntimeError("AppWorld models are unavailable.")
        trace = execute_payment(world)
        before_players = world.models.spotify.MusicPlayer.size()
        observer_error = None
        if condition == "spotify_show_volume":
            try:
                spotify_token = world.apis.spotify.access_token_from(main_user(world))
                response = world.apis.spotify.show_volume(access_token=spotify_token)
                trace.append({"api": "spotify.show_volume", "response": dict(response)})
            except Exception as exc:
                observer_error = f"{type(exc).__name__}: {exc}"
                trace.append({"api": "spotify.show_volume", "error": observer_error})
        elif condition != "control":
            raise ValueError(condition)
        after_players = world.models.spotify.MusicPlayer.size()
        world.execute("pass")
        tracker = world.evaluate(suppress_errors=True)
        stats = tracker.to_dict(stats_only=True)
        total = int(stats["num_tests"])
        success = bool(stats["success"])
        passed = total if success else max(0, total - len(tracker.failures))
        return {
            "condition": condition,
            "observer_error": observer_error,
            "music_player_count_before": before_players,
            "music_player_count_after": after_players,
            "official_terminal_success": success,
            "official_passed": passed,
            "official_total": total,
            "failed_requirements": [item["requirement"].strip() for item in tracker.failures],
            "trace": trace,
        }
    finally:
        world.close()


def main() -> None:
    records = [run("control"), run("spotify_show_volume")]
    output = {
        "artifact_class": "scratch_dynamic_ab",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "benchmark": {
            "name": "AppWorld",
            "git_commit": APPWORLD_COMMIT,
            "dataset": "dev",
            "task_id": TASK_ID,
            "construction_did_not_call_official_solution": True,
        },
        "comparison": (
            "The action sequence is identical through official task completion. The treatment adds one documented "
            "GET-like spotify.show_volume observation that creates MusicPlayer state when absent."
        ),
        "shared_fixture_setup": "The sender Venmo balance is set to amount + 100 in both conditions; the evaluator ignores venmo.User changes.",
        "records": records,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
