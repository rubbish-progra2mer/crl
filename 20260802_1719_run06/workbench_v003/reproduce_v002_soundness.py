from __future__ import annotations

import json
import sys
from pathlib import Path


V002 = Path(__file__).resolve().parents[1] / "implementation_v002"
sys.path.insert(0, str(V002))

from joint_coverage_kernel import Claim, Observation, Record, ScopeCell, evaluate_claim, verify_certificate


def row(name: str, claim: Claim, observations: list[Observation]) -> dict[str, object]:
    result = evaluate_claim(claim, observations)
    return {
        "case": name,
        "decision": result.decision,
        "proof_type": result.certificate.proof_type,
        "certificate_valid": verify_certificate(claim, observations, result.certificate),
        "reason": result.certificate.reason,
    }


def main() -> None:
    cell_a = ScopeCell("A", "recent", "active")
    cell_b = ScopeCell("B", "recent", "active")
    claim = Claim("scope-a", "exists", "matches_target", (cell_a,), "s1")
    misplaced = Observation(
        "misplaced",
        "connector-a",
        cell_a,
        0,
        None,
        (Record("outside", cell_b, True, True),),
        "s1",
    )

    negative = Claim("negative-a", "exists", "matches_target", (cell_a,), "s1")
    first = Observation("a-0", "connector-a", cell_a, 0, 1, (), "s1")
    foreign_end = Observation("b-1", "connector-b", cell_a, 1, None, (), "s1")

    continuing = Observation("continue", "connector-a", cell_a, 0, 1, (), "s1")
    terminating = Observation("terminate", "connector-a", cell_a, 0, None, (), "s1")

    rows = [
        row("out_of_scope_positive_witness", claim, [misplaced]),
        row("cross_connector_page_chain", negative, [first, foreign_end]),
        row("conflicting_cursor_order_1", negative, [continuing, terminating]),
        row("conflicting_cursor_order_2", negative, [terminating, continuing]),
    ]
    print(json.dumps({"kernel": "v002", "rows": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
