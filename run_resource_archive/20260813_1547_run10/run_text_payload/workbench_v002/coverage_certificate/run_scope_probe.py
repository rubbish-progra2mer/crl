from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from appworld import AppWorld
from appworld.apps.admin.models import MainUserMunch

from coverage_types import PageObservation, classify_observations


APPWORLD_COMMIT = "a072b7a86e7c1d5b1d7175659d750ebb9b79f10a"
HERE = Path(__file__).resolve().parent
OUTPUT_PATH = HERE / "scope_probe_results.json"


@dataclass(frozen=True)
class ProbeCase:
    case_id: str
    expected_semantics: str
    naive_first_page: str
    certificate_verdict: str
    certificate_reason: str
    certificate: dict[str, Any]


def _plain(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


def _main_user(world: AppWorld) -> MainUserMunch:
    assert world.models is not None
    model = world.models.admin.MainUser.find_one(**dict(world.task.supervisor))
    if model is None:
        raise RuntimeError("AppWorld supervisor was not found in the task database.")
    return MainUserMunch.from_main_user(model)


def _page(
    *,
    call: Callable[..., Any],
    arguments: dict[str, Any],
    page_index: int,
    page_limit: int,
) -> PageObservation:
    concrete_arguments = {
        **arguments,
        "page_index": page_index,
        "page_limit": page_limit,
    }
    try:
        response = _plain(call(**concrete_arguments))
        if not isinstance(response, list):
            raise TypeError(f"Expected list response, got {type(response).__name__}.")
        return PageObservation(
            page_index=page_index,
            page_limit=page_limit,
            arguments={key: value for key, value in concrete_arguments.items()},
            response=response,
        )
    except Exception as exception:
        return PageObservation(
            page_index=page_index,
            page_limit=page_limit,
            arguments={key: value for key, value in concrete_arguments.items()},
            response=None,
            error=f"{type(exception).__name__}: {exception}",
        )


def _collect_until_closed(
    *,
    call: Callable[..., Any],
    arguments: dict[str, Any],
    page_limit: int,
    max_pages: int,
) -> list[PageObservation]:
    observations: list[PageObservation] = []
    for page_index in range(max_pages):
        observation = _page(
            call=call,
            arguments=arguments,
            page_index=page_index,
            page_limit=page_limit,
        )
        observations.append(observation)
        if observation.error is not None:
            break
        assert observation.response is not None
        if len(observation.response) < page_limit:
            break
    return observations


def _case(
    *,
    case_id: str,
    expected_semantics: str,
    naive_first_page: str,
    api_doc: dict[str, Any],
    observations: list[PageObservation],
    matches: Callable[[dict[str, Any]], bool],
    require_authenticated_view: bool = False,
    require_freshness: bool = False,
    freshness_guaranteed: bool = False,
) -> ProbeCase:
    certificate = classify_observations(
        api_doc=api_doc,
        observations=observations,
        matches=matches,
        require_authenticated_view=require_authenticated_view,
        require_freshness=require_freshness,
        freshness_guaranteed=freshness_guaranteed,
    )
    return ProbeCase(
        case_id=case_id,
        expected_semantics=expected_semantics,
        naive_first_page=naive_first_page,
        certificate_verdict=certificate.verdict,
        certificate_reason=certificate.reason,
        certificate=certificate.to_dict(),
    )


def run_probe() -> list[ProbeCase]:
    world = AppWorld(
        task_id="6171bbc_1",
        experiment_name="scratch_v002_observation_scope_probe",
        ground_truth_mode="full",
        add_login_shortcut=True,
        allow_datetime_change=True,
        parse_datetimes=True,
        munchify_response=True,
    )
    try:
        main_user = _main_user(world)
        spotify = world.apis.spotify
        login = spotify.login(
            username=main_user.email,
            password=main_user.account_passwords.spotify,
        )
        access_token = str(login["access_token"])
        search_users_doc = _plain(world.task.api_docs.spotify["search_users"])
        search_playlists_doc = _plain(
            world.task.api_docs.spotify["search_playlists"]
        )

        user_page_zero = _page(
            call=spotify.search_users,
            arguments={"query": ""},
            page_index=0,
            page_limit=5,
        )
        user_page_one = _page(
            call=spotify.search_users,
            arguments={"query": ""},
            page_index=1,
            page_limit=5,
        )
        assert user_page_zero.response and user_page_one.response
        head_email = str(user_page_zero.response[0]["email"])
        tail_email = str(user_page_one.response[0]["email"])

        public_playlist_pages = _collect_until_closed(
            call=spotify.search_playlists,
            arguments={"query": "", "owner_email": main_user.email},
            page_limit=20,
            max_pages=10,
        )
        authenticated_playlist_pages = _collect_until_closed(
            call=spotify.search_playlists,
            arguments={
                "query": "",
                "owner_email": main_user.email,
                "access_token": access_token,
            },
            page_limit=20,
            max_pages=10,
        )
        authenticated_rows = [
            row
            for observation in authenticated_playlist_pages
            for row in (observation.response or [])
        ]
        private_rows = [row for row in authenticated_rows if not row["is_public"]]
        if not private_rows:
            raise RuntimeError("Controlled fixture has no private playlist.")
        private_playlist_id = int(private_rows[0]["playlist_id"])
        nonexistent_playlist_id = max(
            int(row["playlist_id"]) for row in authenticated_rows
        ) + 1_000_000

        invalid_read = _page(
            call=spotify.search_playlists,
            arguments={
                "query": "",
                "owner_email": main_user.email,
                "access_token": access_token,
            },
            page_index=-1,
            page_limit=20,
        )

        return [
            _case(
                case_id="positive_head_page",
                expected_semantics="PRESENT",
                naive_first_page="PRESENT",
                api_doc=search_users_doc,
                observations=[user_page_zero],
                matches=lambda row: row.get("email") == head_email,
            ),
            _case(
                case_id="tail_hidden_by_first_page",
                expected_semantics="PRESENT",
                naive_first_page="ABSENT",
                api_doc=search_users_doc,
                observations=[user_page_zero],
                matches=lambda row: row.get("email") == tail_email,
            ),
            _case(
                case_id="tail_found_after_next_page",
                expected_semantics="PRESENT",
                naive_first_page="ABSENT",
                api_doc=search_users_doc,
                observations=[user_page_zero, user_page_one],
                matches=lambda row: row.get("email") == tail_email,
            ),
            _case(
                case_id="private_item_hidden_without_credential",
                expected_semantics="PRESENT_IN_REQUIRED_AUTHENTICATED_VIEW",
                naive_first_page="ABSENT",
                api_doc=search_playlists_doc,
                observations=public_playlist_pages,
                matches=lambda row: row.get("playlist_id") == private_playlist_id,
                require_authenticated_view=True,
            ),
            _case(
                case_id="private_item_visible_with_credential",
                expected_semantics="PRESENT",
                naive_first_page="PRESENT",
                api_doc=search_playlists_doc,
                observations=authenticated_playlist_pages,
                matches=lambda row: row.get("playlist_id") == private_playlist_id,
                require_authenticated_view=True,
            ),
            _case(
                case_id="closed_authenticated_scope_true_absence",
                expected_semantics="ABSENT_WITHIN_AUTHENTICATED_OWNER_SCOPE",
                naive_first_page="ABSENT",
                api_doc=search_playlists_doc,
                observations=authenticated_playlist_pages,
                matches=lambda row: row.get("playlist_id")
                == nonexistent_playlist_id,
                require_authenticated_view=True,
            ),
            _case(
                case_id="read_error",
                expected_semantics="UNKNOWN",
                naive_first_page="ABSENT_OR_ERROR_DEPENDING_ON_AGENT",
                api_doc=search_playlists_doc,
                observations=[invalid_read],
                matches=lambda row: False,
                require_authenticated_view=True,
            ),
            _case(
                case_id="closed_scope_without_freshness_contract",
                expected_semantics="UNKNOWN_FOR_POST_WRITE_ABSENCE",
                naive_first_page="ABSENT",
                api_doc=search_playlists_doc,
                observations=authenticated_playlist_pages,
                matches=lambda row: row.get("playlist_id")
                == nonexistent_playlist_id,
                require_authenticated_view=True,
                require_freshness=True,
                freshness_guaranteed=False,
            ),
        ]
    finally:
        world.close()


def main() -> None:
    cases = run_probe()
    payload = {
        "artifact_class": "scratch",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "claim_boundary": (
            "The fixture constructor uses one AppWorld dev task and its synthetic supervisor "
            "credentials to instantiate public API calls. The classifier receives only public "
            "API documentation, concrete read arguments, raw responses/errors, and declared "
            "scope requirements. This probe measures observation typing, not agent terminal success."
        ),
        "benchmark": {
            "name": "AppWorld",
            "git_commit": APPWORLD_COMMIT,
            "dataset": "dev",
            "task_id": "6171bbc_1",
            "case_count": len(cases),
        },
        "cases": [asdict(case) for case in cases],
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    for case in cases:
        print(
            json.dumps(
                {
                    "case_id": case.case_id,
                    "expected": case.expected_semantics,
                    "naive": case.naive_first_page,
                    "certificate": case.certificate_verdict,
                    "reason": case.certificate_reason,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
