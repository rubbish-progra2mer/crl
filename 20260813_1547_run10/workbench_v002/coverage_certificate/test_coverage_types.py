from __future__ import annotations

import unittest

from coverage_types import PageObservation, classify_observations


GET_DOC = {"method": "GET", "description": "Search records."}


def page(
    index: int,
    rows: list[dict[str, object]] | None,
    *,
    limit: int = 2,
    token: str | None = None,
    error: str | None = None,
) -> PageObservation:
    arguments: dict[str, object] = {
        "query": "",
        "page_index": index,
        "page_limit": limit,
    }
    if token is not None:
        arguments["access_token"] = token
    return PageObservation(index, limit, arguments, rows, error)


class CoverageTypeTests(unittest.TestCase):
    def classify(
        self,
        observations: list[PageObservation],
        *,
        api_doc: dict[str, object] = GET_DOC,
        authenticated: bool = False,
        fresh: bool = True,
    ):
        return classify_observations(
            api_doc=api_doc,
            observations=observations,
            matches=lambda row: row.get("id") == 9,
            require_authenticated_view=authenticated,
            require_freshness=True,
            freshness_guaranteed=fresh,
        )

    def test_positive_does_not_require_closed_pagination(self) -> None:
        certificate = self.classify([page(0, [{"id": 9}, {"id": 1}])])
        self.assertEqual(certificate.verdict, "PRESENT")

    def test_full_first_page_cannot_prove_absence(self) -> None:
        certificate = self.classify([page(0, [{"id": 1}, {"id": 2}])])
        self.assertEqual((certificate.verdict, certificate.reason), (
            "UNKNOWN",
            "pagination_not_closed",
        ))

    def test_short_terminal_page_proves_scoped_absence(self) -> None:
        certificate = self.classify(
            [page(0, [{"id": 1}, {"id": 2}]), page(1, [{"id": 3}])]
        )
        self.assertEqual(certificate.verdict, "ABSENT")

    def test_credential_change_invalidates_page_chain(self) -> None:
        certificate = self.classify(
            [
                page(0, [{"id": 1}, {"id": 2}], token="token-a"),
                page(1, [{"id": 3}], token="token-b"),
            ],
            authenticated=True,
        )
        self.assertEqual((certificate.verdict, certificate.reason), (
            "UNKNOWN",
            "permission_view_incomplete",
        ))

    def test_stale_positive_is_not_accepted_for_current_state(self) -> None:
        certificate = self.classify([page(0, [{"id": 9}])], fresh=False)
        self.assertEqual((certificate.verdict, certificate.reason), (
            "UNKNOWN",
            "freshness_not_established",
        ))

    def test_effectful_observer_cannot_issue_certificate(self) -> None:
        certificate = self.classify(
            [page(0, [{"id": 9}])], api_doc={"method": "POST"}
        )
        self.assertEqual((certificate.verdict, certificate.reason), (
            "UNKNOWN",
            "read_purity_not_established",
        ))


if __name__ == "__main__":
    unittest.main()
