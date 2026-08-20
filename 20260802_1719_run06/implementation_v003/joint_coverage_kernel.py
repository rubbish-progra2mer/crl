from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Hashable, Iterable, Literal, Sequence


Quantifier = Literal["exists", "forall"]
Decision = Literal["TRUE", "FALSE", "UNKNOWN"]
Cursor = str | int


def _canonical_digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _cursor_sort_key(cursor: Cursor) -> tuple[str, str]:
    return type(cursor).__name__, str(cursor)


@dataclass(frozen=True, order=True)
class ScopeCell:
    """One indivisible cell in the joint entity x time x archive scope."""

    entity: str
    time_bucket: str
    archive_state: str

    @property
    def key(self) -> str:
        return f"{self.entity}|{self.time_bucket}|{self.archive_state}"


@dataclass(frozen=True, order=True)
class SourceIdentity:
    """The semantic identity that every page in one proof chain must share."""

    connector_id: str
    query_signature: str
    authentication_subject: str
    scope_schema_version: str

    def __post_init__(self) -> None:
        if not all(
            (
                self.connector_id,
                self.query_signature,
                self.authentication_subject,
                self.scope_schema_version,
            )
        ):
            raise ValueError("source identity fields must all be non-empty")

    @property
    def digest(self) -> str:
        return _canonical_digest(asdict(self))


@dataclass(frozen=True)
class Record:
    record_id: str
    cell: ScopeCell
    matches_target: bool
    compliant: bool


@dataclass(frozen=True)
class Claim:
    claim_id: str
    quantifier: Quantifier
    predicate: Literal["matches_target", "compliant"]
    scope: tuple[ScopeCell, ...]
    snapshot_id: str
    source: SourceIdentity
    text: str = ""
    initial_cursor: Cursor = 0

    def __post_init__(self) -> None:
        if not self.scope:
            raise ValueError("claim scope must not be empty")
        if len(set(self.scope)) != len(self.scope):
            raise ValueError("claim scope contains duplicate joint cells")
        if not self.snapshot_id:
            raise ValueError("claim snapshot_id must not be empty")
        if not isinstance(self.initial_cursor, Hashable):
            raise ValueError("claim initial_cursor must be hashable")

    @property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "claim_id": self.claim_id,
                "quantifier": self.quantifier,
                "predicate": self.predicate,
                "scope": [cell.key for cell in sorted(self.scope)],
                "snapshot_id": self.snapshot_id,
                "source": asdict(self.source),
                "text": self.text,
                "initial_cursor": self.initial_cursor,
            }
        )

    def predicate_holds(self, record: Record) -> bool:
        return bool(getattr(record, self.predicate))

    def witness_for(self, record: Record) -> Decision | None:
        holds = self.predicate_holds(record)
        if self.quantifier == "exists" and holds:
            return "TRUE"
        if self.quantifier == "forall" and not holds:
            return "FALSE"
        return None

    @property
    def coverage_decision(self) -> Decision:
        return "FALSE" if self.quantifier == "exists" else "TRUE"


@dataclass(frozen=True)
class Observation:
    observation_id: str
    connector_id: str
    cell: ScopeCell
    cursor: Cursor
    next_cursor: Cursor | None
    records: tuple[Record, ...]
    snapshot_id: str
    status: Literal["ok", "permission_denied", "error"] = "ok"
    attested: bool = True
    permission_complete: bool = True
    silently_truncated: bool = False
    query_signature: str = ""
    authentication_subject: str = ""
    scope_schema_version: str = ""

    def __post_init__(self) -> None:
        SourceIdentity(
            self.connector_id,
            self.query_signature,
            self.authentication_subject,
            self.scope_schema_version,
        )
        if not self.snapshot_id:
            raise ValueError("observation snapshot_id must not be empty")
        if not isinstance(self.cursor, Hashable):
            raise ValueError("observation cursor must be hashable")
        if self.next_cursor is not None and not isinstance(self.next_cursor, Hashable):
            raise ValueError("observation next_cursor must be hashable")

    @property
    def source(self) -> SourceIdentity:
        return SourceIdentity(
            self.connector_id,
            self.query_signature,
            self.authentication_subject,
            self.scope_schema_version,
        )

    @property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "observation_id": self.observation_id,
                "source": asdict(self.source),
                "cell": self.cell.key,
                "cursor": self.cursor,
                "next_cursor": self.next_cursor,
                "records": [
                    {
                        "record_id": record.record_id,
                        "cell": record.cell.key,
                        "matches_target": record.matches_target,
                        "compliant": record.compliant,
                    }
                    for record in self.records
                ],
                "snapshot_id": self.snapshot_id,
                "status": self.status,
                "attested": self.attested,
                "permission_complete": self.permission_complete,
                "silently_truncated": self.silently_truncated,
            }
        )


@dataclass(frozen=True)
class RepairObligation:
    missing_cells: tuple[ScopeCell, ...]
    next_cursors: tuple[tuple[ScopeCell, Cursor], ...]
    blocked_cells: tuple[ScopeCell, ...]
    conflicted_cells: tuple[ScopeCell, ...]
    reason: str


@dataclass(frozen=True)
class CoverageCertificate:
    schema_version: int
    claim_digest: str
    source_identity_digest: str
    decision: Decision
    proof_type: Literal[
        "positive_witness",
        "counterexample_witness",
        "joint_scope_coverage",
        "insufficient_coverage",
    ]
    observation_digests: tuple[str, ...]
    covered_cells: tuple[ScopeCell, ...]
    missing_cells: tuple[ScopeCell, ...]
    witness_record_id: str | None
    snapshot_id: str
    reason: str

    @property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "schema_version": self.schema_version,
                "claim_digest": self.claim_digest,
                "source_identity_digest": self.source_identity_digest,
                "decision": self.decision,
                "proof_type": self.proof_type,
                "observation_digests": list(self.observation_digests),
                "covered_cells": [cell.key for cell in self.covered_cells],
                "missing_cells": [cell.key for cell in self.missing_cells],
                "witness_record_id": self.witness_record_id,
                "snapshot_id": self.snapshot_id,
                "reason": self.reason,
            }
        )


@dataclass(frozen=True)
class Evaluation:
    decision: Decision
    certificate: CoverageCertificate
    obligation: RepairObligation | None


@dataclass(frozen=True)
class CellTrace:
    cell: ScopeCell
    complete: bool
    witness_pages: tuple[Observation, ...]
    next_cursor: Cursor
    chain_digests: tuple[str, ...]
    evidence_digests: tuple[str, ...]
    blocked: bool
    conflicted: bool
    reason: str


def _unknown_reason(
    traces: dict[ScopeCell, CellTrace], missing: tuple[ScopeCell, ...]
) -> str:
    if any(traces[cell].conflicted for cell in missing):
        return "evidence conflict prevents a source-bound page-chain proof"
    if any(traces[cell].blocked for cell in missing):
        return "some claim cells are permission-blocked"
    return "fetch the missing source-bound page chains for the exact joint cells"


def _trace_cell(
    cell: ScopeCell,
    observations: Sequence[Observation],
    claim: Claim,
) -> CellTrace:
    candidates = [item for item in observations if item.cell == cell]
    expected_source = [item for item in candidates if item.source == claim.source]
    blocked = any(
        item.status == "permission_denied" or not item.permission_complete
        for item in expected_source
    )
    compatible = [
        item
        for item in expected_source
        if item.status == "ok"
        and item.attested
        and item.permission_complete
        and item.snapshot_id == claim.snapshot_id
    ]
    evidence_digests = tuple(sorted(item.digest for item in candidates))

    if any(record.cell != item.cell for item in compatible for record in item.records):
        return CellTrace(
            cell,
            False,
            (),
            claim.initial_cursor,
            (),
            evidence_digests,
            blocked,
            True,
            "record_cell_mismatch",
        )

    grouped: dict[Cursor, list[Observation]] = {}
    for item in compatible:
        grouped.setdefault(item.cursor, []).append(item)
    for cursor, group in grouped.items():
        if len({item.digest for item in group}) > 1:
            return CellTrace(
                cell,
                False,
                (),
                cursor,
                (),
                evidence_digests,
                blocked,
                True,
                "conflicting_cursor_pages",
            )

    pages = {
        cursor: sorted(group, key=lambda item: item.digest)[0]
        for cursor, group in grouped.items()
    }
    cursor: Cursor = claim.initial_cursor
    seen: set[Cursor] = set()
    chain: list[Observation] = []
    while True:
        if cursor in seen:
            return CellTrace(
                cell,
                False,
                (),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                True,
                "cursor_cycle",
            )
        page = pages.get(cursor)
        if page is None:
            if chain:
                reason = "missing_page"
            elif candidates and not expected_source:
                reason = "source_identity_mismatch"
            elif expected_source and not compatible:
                reason = "no_compatible_attested_page"
            else:
                reason = "permission_gap" if blocked else "missing_page"
            return CellTrace(
                cell,
                False,
                tuple(chain),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
                reason,
            )
        seen.add(cursor)
        chain.append(page)
        if page.silently_truncated:
            return CellTrace(
                cell,
                False,
                tuple(chain),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
                "connector_declared_untrustworthy_truncation",
            )
        if page.next_cursor is None:
            orphaned = set(pages) - seen
            if orphaned:
                return CellTrace(
                    cell,
                    False,
                    (),
                    sorted(orphaned, key=_cursor_sort_key)[0],
                    tuple(item.digest for item in chain),
                    evidence_digests,
                    blocked,
                    True,
                    "orphan_page_conflict",
                )
            return CellTrace(
                cell,
                True,
                tuple(chain),
                cursor,
                tuple(item.digest for item in chain),
                evidence_digests,
                blocked,
                False,
                "complete_source_bound_page_chain",
            )
        cursor = page.next_cursor


def _certificate(
    claim: Claim,
    *,
    decision: Decision,
    proof_type: Literal[
        "positive_witness",
        "counterexample_witness",
        "joint_scope_coverage",
        "insufficient_coverage",
    ],
    observation_digests: tuple[str, ...],
    covered_cells: tuple[ScopeCell, ...],
    missing_cells: tuple[ScopeCell, ...],
    witness_record_id: str | None,
    reason: str,
) -> CoverageCertificate:
    return CoverageCertificate(
        schema_version=3,
        claim_digest=claim.digest,
        source_identity_digest=claim.source.digest,
        decision=decision,
        proof_type=proof_type,
        observation_digests=observation_digests,
        covered_cells=covered_cells,
        missing_cells=missing_cells,
        witness_record_id=witness_record_id,
        snapshot_id=claim.snapshot_id,
        reason=reason,
    )


def evaluate_claim(claim: Claim, observations: Sequence[Observation]) -> Evaluation:
    traces = {
        cell: _trace_cell(cell, observations, claim)
        for cell in sorted(claim.scope)
    }
    covered = tuple(cell for cell, trace in traces.items() if trace.complete)
    missing = tuple(cell for cell, trace in traces.items() if not trace.complete)

    for cell in sorted(traces):
        trace = traces[cell]
        if trace.conflicted:
            continue
        pages = sorted(
            trace.witness_pages,
            key=lambda item: (_cursor_sort_key(item.cursor), item.digest),
        )
        for observation in pages:
            for record in observation.records:
                if record.cell != observation.cell or record.cell not in claim.scope:
                    continue
                decision = claim.witness_for(record)
                if decision is None:
                    continue
                proof_type = (
                    "positive_witness"
                    if decision == "TRUE"
                    else "counterexample_witness"
                )
                certificate = _certificate(
                    claim,
                    decision=decision,
                    proof_type=proof_type,
                    observation_digests=(observation.digest,),
                    covered_cells=covered,
                    missing_cells=missing,
                    witness_record_id=record.record_id,
                    reason="a source-bound in-scope attested record decides the claim",
                )
                return Evaluation(decision, certificate, None)

    if not missing:
        decision = claim.coverage_decision
        all_chain_digests = tuple(
            digest
            for cell in sorted(traces)
            for digest in traces[cell].chain_digests
        )
        certificate = _certificate(
            claim,
            decision=decision,
            proof_type="joint_scope_coverage",
            observation_digests=all_chain_digests,
            covered_cells=covered,
            missing_cells=(),
            witness_record_id=None,
            reason="complete source-bound page chains cover the exact joint claim scope",
        )
        return Evaluation(decision, certificate, None)

    blocked = tuple(cell for cell in missing if traces[cell].blocked)
    conflicted = tuple(cell for cell in missing if traces[cell].conflicted)
    next_cursors = tuple(
        (cell, traces[cell].next_cursor)
        for cell in missing
        if not traces[cell].blocked and not traces[cell].conflicted
    )
    reason = _unknown_reason(traces, missing)
    obligation = RepairObligation(
        missing_cells=missing,
        next_cursors=next_cursors,
        blocked_cells=blocked,
        conflicted_cells=conflicted,
        reason=reason,
    )
    all_evidence_digests = tuple(
        digest
        for cell in sorted(traces)
        for digest in traces[cell].evidence_digests
    )
    certificate = _certificate(
        claim,
        decision="UNKNOWN",
        proof_type="insufficient_coverage",
        observation_digests=all_evidence_digests,
        covered_cells=covered,
        missing_cells=missing,
        witness_record_id=None,
        reason=reason,
    )
    return Evaluation("UNKNOWN", certificate, obligation)


def next_page_requests(
    claim: Claim,
    observations: Sequence[Observation],
    cells: Iterable[ScopeCell] | None = None,
) -> tuple[tuple[ScopeCell, Cursor], ...]:
    """Return one source-bound continuation per incomplete, repairable cell."""

    requested_cells = claim.scope if cells is None else tuple(cells)
    requests: list[tuple[ScopeCell, Cursor]] = []
    for cell in sorted(set(requested_cells)):
        trace = _trace_cell(cell, observations, claim)
        if not trace.complete and not trace.blocked and not trace.conflicted:
            requests.append((cell, trace.next_cursor))
    return tuple(requests)


def complete_joint_cells(
    claim: Claim,
    observations: Sequence[Observation],
    cells: Iterable[ScopeCell] | None = None,
) -> tuple[ScopeCell, ...]:
    requested_cells = claim.scope if cells is None else tuple(cells)
    return tuple(
        cell
        for cell in sorted(set(requested_cells))
        if _trace_cell(cell, observations, claim).complete
    )


def verify_certificate(
    claim: Claim,
    observations: Sequence[Observation],
    certificate: CoverageCertificate,
) -> bool:
    """Verify against a separately implemented certificate specification."""

    from independent_certificate_verifier import verify_certificate_independently

    return verify_certificate_independently(claim, observations, certificate)


def marginal_coverage_would_accept(
    claim_scope: Iterable[ScopeCell],
    observed_complete_cells: Iterable[ScopeCell],
) -> bool:
    """The deliberately unsound marginal checker retained only as a foil."""

    claim_cells = tuple(claim_scope)
    observed_cells = tuple(observed_complete_cells)
    return (
        {cell.entity for cell in claim_cells}
        <= {cell.entity for cell in observed_cells}
        and {cell.time_bucket for cell in claim_cells}
        <= {cell.time_bucket for cell in observed_cells}
        and {cell.archive_state for cell in claim_cells}
        <= {cell.archive_state for cell in observed_cells}
    )


def cell_to_dict(cell: ScopeCell) -> dict[str, str]:
    return asdict(cell)
