#!/usr/bin/env python3
"""把 v006 反例对应的 v007 失败关闭结果导出为结构化证据。"""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace

from test_protocol import KEY, NOW, _admit, _observations, _valid_bundle
from typed_model import (
    ClaimRef,
    canonical_bytes,
    canonical_hash,
    without_plan_hash,
    without_signature,
)


def main() -> int:
    bundle, request = _valid_bundle()
    contradictory = replace(
        bundle.record,
        failed_claims=bundle.record.passed_claims,
        signature="",
    )
    public_digest = hashlib.sha256(
        canonical_bytes(without_signature(contradictory))
    ).hexdigest()
    contradictory = replace(contradictory, signature=public_digest)
    minted = ClaimRef("finite_relation", "f" * 64)
    reversed_plan = replace(bundle.plan, probes=tuple(reversed(bundle.plan.probes)))
    rehashed_plan = replace(bundle.plan, probes=(bundle.plan.probes[0],))
    rehashed_plan = replace(
        rehashed_plan,
        plan_hash=canonical_hash(without_plan_hash(rehashed_plan)),
    )
    contradictory_report = replace(
        bundle.report,
        passed_claims=(),
        failed_claims=bundle.report.passed_claims,
    )
    cache = set()
    first = _admit(bundle, request, cache=cache)
    second = _admit(bundle, request, cache=cache)
    scenarios = {
        "honest_bundle_allowed": _admit(bundle, request).allowed,
        "public_hash_cannot_forge_signature_rejected": not _admit(
            replace(bundle, record=contradictory), request
        ).allowed,
        "minted_claim_rejected": not _admit(
            bundle,
            replace(
                request,
                required_claims=tuple(
                    sorted(request.required_claims + (minted,))
                ),
            ),
        ).allowed,
        "subset_claim_cross_contract_reuse_rejected": not _admit(
            bundle,
            replace(
                request,
                contract_hash="0" * 64,
                required_claims=(request.required_claims[0],),
            ),
        ).allowed,
        "plan_tamper_old_hash_rejected": not _admit(
            replace(bundle, plan=reversed_plan), request
        ).allowed,
        "plan_tamper_recomputed_hash_rejected": not _admit(
            replace(bundle, plan=rehashed_plan), request
        ).allowed,
        "contradictory_report_rejected": not _admit(
            replace(bundle, report=contradictory_report), request
        ).allowed,
        "raw_observation_tamper_rejected": not _admit(
            replace(bundle, observations=_observations("b")), request
        ).allowed,
        "first_nonce_use_allowed": first.allowed,
        "nonce_replay_rejected": not second.allowed,
        "expired_record_rejected": not _admit(
            bundle, request, now=NOW + 101
        ).allowed,
        "unknown_issuer_rejected": not _admit(
            bundle, request, issuers={}
        ).allowed,
        "tool_version_mismatch_rejected": not _admit(
            bundle, replace(request, tool_version="2.0")
        ).allowed,
    }
    result = {
        "schema": "v007-attack-audit-1",
        "scenario_count": len(scenarios),
        "passed": sum(scenarios.values()),
        "failed": sum(not value for value in scenarios.values()),
        "scenarios": scenarios,
        "signature_primitive": "HMAC-SHA256 shared-key prototype",
        "test_key_is_synthetic": KEY.startswith(b"v007-test-only"),
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if all(scenarios.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
