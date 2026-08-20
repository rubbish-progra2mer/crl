from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Literal


Verdict = Literal["PRESENT", "ABSENT", "UNKNOWN"]


@dataclass(frozen=True)
class PageObservation:
    page_index: int
    page_limit: int
    arguments: dict[str, Any]
    response: list[dict[str, Any]] | None
    error: str | None = None


@dataclass(frozen=True)
class CoverageCertificate:
    verdict: Verdict
    reason: str
    matched_page: int | None
    obligations: dict[str, bool]
    observed_pages: tuple[int, ...]
    observed_item_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _scope_arguments(arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in arguments.items()
        if key not in {"page_index", "page_limit", "access_token"}
    }


def _credential_present(arguments: dict[str, Any]) -> bool:
    token = arguments.get("access_token")
    return isinstance(token, str) and bool(token.strip())


def classify_observations(
    *,
    api_doc: dict[str, Any],
    observations: list[PageObservation],
    matches: Callable[[dict[str, Any]], bool],
    require_authenticated_view: bool,
    require_freshness: bool,
    freshness_guaranteed: bool,
) -> CoverageCertificate:
    """Classify a scoped existence claim without treating incomplete reads as absence.

    The classifier is intentionally conservative. It proves only absence within the
    exact query and credential view represented by the observations. A positive row
    is sufficient for PRESENT even when the remaining result set is incomplete.
    """

    ordered = sorted(observations, key=lambda observation: observation.page_index)
    observed_pages = tuple(observation.page_index for observation in ordered)
    observed_item_count = sum(
        len(observation.response or []) for observation in ordered
    )

    successful_reads = bool(ordered) and all(
        observation.error is None and isinstance(observation.response, list)
        for observation in ordered
    )
    read_only = str(api_doc.get("method", "")).upper() == "GET"
    same_scope = bool(ordered) and len(
        {
            repr(sorted(_scope_arguments(observation.arguments).items()))
            for observation in ordered
        }
    ) == 1
    same_limit = bool(ordered) and len(
        {observation.page_limit for observation in ordered}
    ) == 1
    contiguous_from_zero = bool(ordered) and observed_pages == tuple(
        range(len(ordered))
    )
    credential_consistent = bool(ordered) and len(
        {repr(observation.arguments.get("access_token")) for observation in ordered}
    ) == 1
    authenticated_view = bool(ordered) and _credential_present(ordered[0].arguments)
    permission_sufficient = not require_authenticated_view or authenticated_view
    terminal_short_page = (
        successful_reads
        and same_limit
        and bool(ordered)
        and len(ordered[-1].response or []) < ordered[-1].page_limit
    )
    freshness_sufficient = not require_freshness or freshness_guaranteed

    obligations = {
        "successful_reads": successful_reads,
        "read_only": read_only,
        "same_scope": same_scope,
        "same_limit": same_limit,
        "contiguous_from_zero": contiguous_from_zero,
        "credential_consistent": credential_consistent,
        "permission_sufficient": permission_sufficient,
        "terminal_short_page": terminal_short_page,
        "freshness_sufficient": freshness_sufficient,
    }

    positive_witness_page: int | None = None
    if successful_reads:
        for observation in ordered:
            assert observation.response is not None
            if any(matches(row) for row in observation.response):
                positive_witness_page = observation.page_index
                break

    if not successful_reads:
        reason = "read_error_or_missing_response"
    elif not read_only:
        reason = "read_purity_not_established"
    elif not same_scope or not same_limit or not contiguous_from_zero:
        reason = "incoherent_page_scope"
    elif not credential_consistent or not permission_sufficient:
        reason = "permission_view_incomplete"
    elif not freshness_sufficient:
        reason = "freshness_not_established"
    elif positive_witness_page is not None:
        return CoverageCertificate(
            verdict="PRESENT",
            reason="positive_witness",
            matched_page=positive_witness_page,
            obligations=obligations,
            observed_pages=observed_pages,
            observed_item_count=observed_item_count,
        )
    elif not terminal_short_page:
        reason = "pagination_not_closed"
    else:
        return CoverageCertificate(
            verdict="ABSENT",
            reason="closed_scope_negative_certificate",
            matched_page=None,
            obligations=obligations,
            observed_pages=observed_pages,
            observed_item_count=observed_item_count,
        )

    return CoverageCertificate(
        verdict="UNKNOWN",
        reason=reason,
        matched_page=None,
        obligations=obligations,
        observed_pages=observed_pages,
        observed_item_count=observed_item_count,
    )
