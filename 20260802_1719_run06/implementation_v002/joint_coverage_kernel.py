from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Iterable, Literal, Sequence


Quantifier = Literal["exists", "forall"]
Decision = Literal["TRUE", "FALSE", "UNKNOWN"]


def _canonical_digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, order=True)
class ScopeCell:
    """One indivisible cell in the joint entity x time x archive scope."""

    entity: str
    time_bucket: str
    archive_state: str

    @property
    def key(self) -> str:
        return f"{self.entity}|{self.time_bucket}|{self.archive_state}"


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
    text: str = ""

    def __post_init__(self) -> None:
        if not self.scope:
            raise ValueError("claim scope must not be empty")
        if len(set(self.scope)) != len(self.scope):
            raise ValueError("claim scope contains duplicate joint cells")

    @property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "claim_id": self.claim_id,
                "quantifier": self.quantifier,
                "predicate": self.predicate,
                "scope": [cell.key for cell in sorted(self.scope)],
                "snapshot_id": self.snapshot_id,
                "text": self.text,
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
    cursor: int
    next_cursor: int | None
    records: tuple[Record, ...]
    snapshot_id: str
    status: Literal["ok", "permission_denied", "error"] = "ok"
    attested: bool = True
    permission_complete: bool = True
    silently_truncated: bool = False

    @property
    def digest(self) -> str:
        return _canonical_digest(
            {
                "observation_id": self.observation_id,
                "connector_id": self.connector_id,
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
    next_cursors: tuple[tuple[ScopeCell, int], ...]
    blocked_cells: tuple[ScopeCell, ...]
    reason: str


@dataclass(frozen=True)
class CoverageCertificate:
    schema_version: int
    claim_digest: str
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
    records: tuple[Record, ...]
    next_cursor: int
    observation_digests: tuple[str, ...]
    blocked: bool
    reason: str


def _trace_cell(
    cell: ScopeCell,
    observations: Sequence[Observation],
    snapshot_id: str,
) -> CellTrace:
    candidates = [item for item in observations if item.cell == cell]
    blocked = any(
        item.status == "permission_denied" or not item.permission_complete
        for item in candidates
    )
    pages = {
        item.cursor: item
        for item in candidates
        if item.status == "ok"
        and item.attested
        and item.permission_complete
        and item.snapshot_id == snapshot_id
    }
    cursor = 0
    records: list[Record] = []
    digests: list[str] = []
    seen: set[int] = set()
    while cursor in pages and cursor not in seen:
        seen.add(cursor)
        page = pages[cursor]
        if any(record.cell != cell for record in page.records):
            return CellTrace(
                cell,
                False,
                tuple(records),
                cursor,
                tuple(digests),
                blocked,
                "record_cell_mismatch",
            )
        records.extend(page.records)
        digests.append(page.digest)
        if page.silently_truncated:
            return CellTrace(
                cell,
                False,
                tuple(records),
                cursor,
                tuple(digests),
                blocked,
                "connector_declared_untrustworthy_truncation",
            )
        if page.next_cursor is None:
            return CellTrace(
                cell,
                True,
                tuple(records),
                cursor,
                tuple(digests),
                blocked,
                "complete_page_chain",
            )
        if page.next_cursor <= cursor:
            return CellTrace(
                cell,
                False,
                tuple(records),
                cursor,
                tuple(digests),
                blocked,
                "non_progressing_cursor",
            )
        cursor = page.next_cursor
    reason = "permission_gap" if blocked else "missing_page"
    if candidates and not pages:
        reason = "no_compatible_attested_page"
    return CellTrace(
        cell,
        False,
        tuple(records),
        cursor,
        tuple(digests),
        blocked,
        reason,
    )


def evaluate_claim(claim: Claim, observations: Sequence[Observation]) -> Evaluation:
    traces = {
        cell: _trace_cell(cell, observations, claim.snapshot_id)
        for cell in sorted(claim.scope)
    }
    compatible_observations = [
        item
        for item in observations
        if item.cell in traces
        and item.status == "ok"
        and item.attested
        and item.permission_complete
        and item.snapshot_id == claim.snapshot_id
    ]
    compatible_observations.sort(key=lambda item: (item.cell.key, item.cursor, item.digest))
    for observation in compatible_observations:
        for record in observation.records:
            decision = claim.witness_for(record)
            if decision is None:
                continue
            proof_type = (
                "positive_witness" if decision == "TRUE" else "counterexample_witness"
            )
            certificate = CoverageCertificate(
                schema_version=2,
                claim_digest=claim.digest,
                decision=decision,
                proof_type=proof_type,
                observation_digests=(observation.digest,),
                covered_cells=tuple(
                    cell for cell, trace in traces.items() if trace.complete
                ),
                missing_cells=tuple(
                    cell for cell, trace in traces.items() if not trace.complete
                ),
                witness_record_id=record.record_id,
                snapshot_id=claim.snapshot_id,
                reason="a compatible attested record decides the claim",
            )
            return Evaluation(decision, certificate, None)

    covered = tuple(cell for cell, trace in traces.items() if trace.complete)
    missing = tuple(cell for cell, trace in traces.items() if not trace.complete)
    all_digests = tuple(
        digest
        for cell in sorted(traces)
        for digest in traces[cell].observation_digests
    )
    if not missing:
        decision = claim.coverage_decision
        certificate = CoverageCertificate(
            schema_version=2,
            claim_digest=claim.digest,
            decision=decision,
            proof_type="joint_scope_coverage",
            observation_digests=all_digests,
            covered_cells=covered,
            missing_cells=(),
            witness_record_id=None,
            snapshot_id=claim.snapshot_id,
            reason="the union of complete joint cells covers the exact claim scope",
        )
        return Evaluation(decision, certificate, None)

    blocked = tuple(cell for cell in missing if traces[cell].blocked)
    next_cursors = tuple(
        (cell, traces[cell].next_cursor)
        for cell in missing
        if not traces[cell].blocked
    )
    obligation = RepairObligation(
        missing_cells=missing,
        next_cursors=next_cursors,
        blocked_cells=blocked,
        reason=(
            "some claim cells are permission-blocked"
            if blocked
            else "fetch the missing page chains for the exact joint cells"
        ),
    )
    certificate = CoverageCertificate(
        schema_version=2,
        claim_digest=claim.digest,
        decision="UNKNOWN",
        proof_type="insufficient_coverage",
        observation_digests=all_digests,
        covered_cells=covered,
        missing_cells=missing,
        witness_record_id=None,
        snapshot_id=claim.snapshot_id,
        reason=obligation.reason,
    )
    return Evaluation("UNKNOWN", certificate, obligation)


def next_page_requests(
    cells: Iterable[ScopeCell],
    observations: Sequence[Observation],
    snapshot_id: str,
) -> tuple[tuple[ScopeCell, int], ...]:
    """Return one deterministic continuation request per incomplete, unblocked cell."""

    requests: list[tuple[ScopeCell, int]] = []
    for cell in sorted(set(cells)):
        trace = _trace_cell(cell, observations, snapshot_id)
        if not trace.complete and not trace.blocked:
            requests.append((cell, trace.next_cursor))
    return tuple(requests)


def complete_joint_cells(
    cells: Iterable[ScopeCell],
    observations: Sequence[Observation],
    snapshot_id: str,
) -> tuple[ScopeCell, ...]:
    return tuple(
        cell
        for cell in sorted(set(cells))
        if _trace_cell(cell, observations, snapshot_id).complete
    )


def verify_certificate(
    claim: Claim,
    observations: Sequence[Observation],
    certificate: CoverageCertificate,
) -> bool:
    """Recompute the proof result from exact bytes and reject certificate drift."""

    expected = evaluate_claim(claim, observations).certificate
    return expected.digest == certificate.digest


def marginal_coverage_would_accept(
    claim_scope: Iterable[ScopeCell],
    observed_complete_cells: Iterable[ScopeCell],
) -> bool:
    """The deliberately unsound v001-style marginal checker used as a foil."""

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
