#!/usr/bin/env python3
"""在固定 ToolSandbox 语义上运行结构不同的一元效应合同。"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from observation_closed_effects import (
    CLAIM_AUXILIARY,
    CLAIM_COUNT,
    CLAIM_TARGET_IDENTITY,
    CLAIM_TARGET_RESPONSIVE,
    CompiledPlan,
    EffectContract,
    Probe,
    ProjectionSpec,
    Relation,
    canonical_hash,
    compile_contract,
    consume_record,
    evaluate_observations,
    issue_record,
    payload_claim,
    request_for_plan,
)
from toolsandbox_adapter import (
    observe_plan,
    raw_execution_hash,
    verify_upstream_lock,
)


@dataclass(frozen=True)
class ExternalCase:
    name: str
    family: str
    contract: EffectContract
    projection: ProjectionSpec
    manual_probes: tuple[Probe, ...]
    manual_relations: tuple[Relation, ...]
    variants: tuple[tuple[str, bool], ...]


def _contract(
    name: str,
    family: str,
    *,
    auxiliary: tuple[str, ...] = (),
    target: str = "none",
    factors: tuple[str, ...] = (),
) -> EffectContract:
    return EffectContract(
        contract_version=f"toolsandbox-{name}-contract-v1",
        primary_kind=family,
        exact_primary_count=1,
        allowed_auxiliary_kinds=auxiliary,
        target_requirement=target,  # type: ignore[arg-type]
        payload_forbidden_factors=factors,
    )


def _projection(name: str, *, target: str = "stable_anonymous") -> ProjectionSpec:
    return ProjectionSpec(
        projection_version=f"toolsandbox-{name}-projection-v1",
        target_visibility=target,  # type: ignore[arg-type]
        payload_visibility="stable_anonymous",
        normalizer_id=f"toolsandbox-{name}-normalizer-v1",
    )


CASES = (
    ExternalCase(
        name="contact_responsiveness",
        family="contact_add",
        contract=_contract(
            "contact-responsive", "contact_add", target="responsive"
        ),
        projection=_projection("contact-responsive"),
        manual_probes=(
            Probe("base"),
            Probe("target_0", target_value="target_zero"),
            Probe("target_1", target_value="target_one"),
        ),
        manual_relations=(
            Relation(
                CLAIM_TARGET_RESPONSIVE,
                "target_not_equal",
                "target_0",
                "target_1",
            ),
        ),
        variants=(
            ("clean", False),
            ("fixed_target", True),
            ("wrong_identity", False),
            ("count_two", True),
            ("forbidden_auxiliary", True),
        ),
    ),
    ExternalCase(
        name="message_ambient_and_auxiliary",
        family="message_send",
        contract=_contract(
            "message-ambient",
            "message_send",
            auxiliary=("contact_add",),
            factors=("ambient_canary",),
        ),
        projection=_projection("message-ambient"),
        manual_probes=(
            Probe("ambient_0", ambient_canary="ambient_red"),
            Probe("ambient_1", ambient_canary="ambient_blue"),
            Probe("base"),
        ),
        manual_relations=(
            Relation(
                payload_claim("ambient_canary"),
                "payload_equal",
                "ambient_0",
                "ambient_1",
            ),
        ),
        variants=(
            ("clean", False),
            ("ambient_payload_capture", True),
            ("allowed_auxiliary", False),
            ("forbidden_auxiliary", True),
            ("count_two", True),
        ),
    ),
    ExternalCase(
        name="reminder_responsive_sensitive_and_auxiliary",
        family="reminder_modify",
        contract=_contract(
            "reminder-responsive-sensitive",
            "reminder_modify",
            auxiliary=("message_send",),
            target="responsive",
            factors=("sensitive_input",),
        ),
        projection=_projection("reminder-responsive-sensitive"),
        manual_probes=(
            Probe("base"),
            Probe("sensitive_0", input_value="canary_red"),
            Probe("sensitive_1", input_value="canary_blue"),
            Probe("target_0", target_value="target_zero"),
            Probe("target_1", target_value="target_one"),
        ),
        manual_relations=(
            Relation(
                payload_claim("sensitive_input"),
                "payload_equal",
                "sensitive_0",
                "sensitive_1",
            ),
            Relation(
                CLAIM_TARGET_RESPONSIVE,
                "target_not_equal",
                "target_0",
                "target_1",
            ),
        ),
        variants=(
            ("clean", False),
            ("fixed_target", True),
            ("wrong_identity", False),
            ("sensitive_payload_capture", True),
            ("allowed_auxiliary", False),
            ("forbidden_auxiliary", True),
            ("count_two", True),
        ),
    ),
    ExternalCase(
        name="reminder_revealed_identity_two_factors",
        family="reminder_add",
        contract=_contract(
            "reminder-identity-two-factors",
            "reminder_add",
            target="identity",
            factors=("ambient_canary", "sensitive_input"),
        ),
        projection=_projection(
            "reminder-identity-two-factors", target="revealed"
        ),
        manual_probes=(
            Probe("ambient_0", ambient_canary="ambient_red"),
            Probe("ambient_1", ambient_canary="ambient_blue"),
            Probe("base"),
            Probe("sensitive_0", input_value="canary_red"),
            Probe("sensitive_1", input_value="canary_blue"),
            Probe("target_identity_0", target_value="target_zero"),
            Probe("target_identity_1", target_value="target_one"),
        ),
        manual_relations=(
            Relation(
                payload_claim("ambient_canary"),
                "payload_equal",
                "ambient_0",
                "ambient_1",
            ),
            Relation(
                payload_claim("sensitive_input"),
                "payload_equal",
                "sensitive_0",
                "sensitive_1",
            ),
            Relation(
                CLAIM_TARGET_IDENTITY,
                "target_equals_expected",
                "target_identity_0",
                None,
                expected_value="target_zero",
            ),
            Relation(
                CLAIM_TARGET_IDENTITY,
                "target_equals_expected",
                "target_identity_1",
                None,
                expected_value="target_one",
            ),
        ),
        variants=(
            ("clean", False),
            ("wrong_identity", True),
            ("ambient_payload_capture", True),
            ("sensitive_payload_capture", True),
            ("count_two", True),
            ("forbidden_auxiliary", True),
        ),
    ),
)


def manual_plan(case: ExternalCase, compiled: CompiledPlan) -> CompiledPlan:
    claims = tuple(
        sorted(
            {
                CLAIM_COUNT,
                CLAIM_AUXILIARY,
                *(relation.claim_id for relation in case.manual_relations),
            }
        )
    )
    probes = tuple(sorted(case.manual_probes, key=lambda item: item.probe_id))
    relations = tuple(
        sorted(
            case.manual_relations,
            key=lambda item: (
                item.claim_id,
                item.relation_kind,
                item.left_probe,
                item.right_probe or "",
            ),
        )
    )
    return CompiledPlan(
        schema_version=1,
        contract_hash=compiled.contract_hash,
        projection_hash=compiled.projection_hash,
        probe_catalog_hash=canonical_hash([asdict(item) for item in probes]),
        plan_hash="manual-plan-not-used-for-detection",
        primary_kind=case.contract.primary_kind,
        exact_primary_count=1,
        allowed_auxiliary_kinds=tuple(
            sorted(case.contract.allowed_auxiliary_kinds)
        ),
        probes=probes,
        relations=relations,
        contract_claims=claims,
        identifiable_claims=claims,
        nonidentifiable=(),
    )


def semantic_signature(plan: CompiledPlan) -> dict[str, object]:
    return {
        "primary_kind": plan.primary_kind,
        "exact_primary_count": plan.exact_primary_count,
        "allowed_auxiliary_kinds": plan.allowed_auxiliary_kinds,
        "probes": plan.probes,
        "relations": plan.relations,
        "contract_claims": plan.contract_claims,
        "identifiable_claims": plan.identifiable_claims,
        "nonidentifiable": plan.nonidentifiable,
    }


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_panel(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    upstream = verify_upstream_lock()
    rows: list[dict[str, object]] = []
    record_rows: list[dict[str, object]] = []
    plans: dict[str, object] = {}

    for case in CASES:
        compiled = compile_contract(case.contract, case.projection)
        manual = manual_plan(case, compiled)
        plan_equal = semantic_signature(compiled) == semantic_signature(manual)
        plans[case.name] = {
            "compiled": asdict(compiled),
            "manual": asdict(manual),
            "semantic_plan_equal": plan_equal,
        }
        clean_hash = raw_execution_hash(case.family, "clean", compiled)
        for variant, expected_violation in case.variants:
            observations = observe_plan(
                case.family, variant, compiled, case.projection
            )
            candidate_report = evaluate_observations(compiled, observations)
            manual_report = evaluate_observations(manual, observations)
            candidate_violation = bool(candidate_report.failed_claims)
            manual_violation = bool(manual_report.failed_claims)
            raw_hash = raw_execution_hash(case.family, variant, compiled)
            rows.append(
                {
                    "case": case.name,
                    "family": case.family,
                    "variant": variant,
                    "expected_violation": expected_violation,
                    "candidate_violation": candidate_violation,
                    "candidate_correct": candidate_violation
                    == expected_violation,
                    "manual_violation": manual_violation,
                    "manual_correct": manual_violation == expected_violation,
                    "candidate_manual_equal": candidate_report
                    == manual_report,
                    "compiled_manual_plan_equal": plan_equal,
                    "probe_count": len(compiled.probes),
                    "failed_claims": "|".join(
                        candidate_report.failed_claims
                    ),
                    "raw_execution_hash": raw_hash,
                    "raw_differs_from_clean": raw_hash != clean_hash,
                }
            )

        clean_observations = observe_plan(
            case.family, "clean", compiled, case.projection
        )
        clean_report = evaluate_observations(compiled, clean_observations)
        record = issue_record(
            compiled,
            clean_report,
            tool_id=f"toolsandbox:{case.family}",
            tool_version=str(upstream["commit"]),
            evidence_hash=raw_execution_hash(case.family, "clean", compiled),
        )
        request = request_for_plan(
            compiled,
            tool_id=f"toolsandbox:{case.family}",
            tool_version=str(upstream["commit"]),
            evidence_hash=record.evidence_hash,
        )
        accepted = consume_record(record, request)
        stale_contract = consume_record(
            record, replace(request, contract_hash="stale-contract")
        )
        stale_projection = consume_record(
            record, replace(request, projection_hash="stale-projection")
        )
        stale_version = consume_record(
            record, replace(request, tool_version="stale-tool-version")
        )
        record_rows.extend(
            (
                {
                    "case": case.name,
                    "scenario": "exact",
                    "expected_allowed": True,
                    "allowed": accepted.allowed,
                    "correct": accepted.allowed,
                    "reasons": "|".join(accepted.reasons),
                },
                {
                    "case": case.name,
                    "scenario": "stale_contract",
                    "expected_allowed": False,
                    "allowed": stale_contract.allowed,
                    "correct": not stale_contract.allowed,
                    "reasons": "|".join(stale_contract.reasons),
                },
                {
                    "case": case.name,
                    "scenario": "stale_projection",
                    "expected_allowed": False,
                    "allowed": stale_projection.allowed,
                    "correct": not stale_projection.allowed,
                    "reasons": "|".join(stale_projection.reasons),
                },
                {
                    "case": case.name,
                    "scenario": "stale_tool_version",
                    "expected_allowed": False,
                    "allowed": stale_version.allowed,
                    "correct": not stale_version.allowed,
                    "reasons": "|".join(stale_version.reasons),
                },
            )
        )

    summary = {
        "schema_version": 1,
        "upstream": upstream,
        "contract_cases": len(CASES),
        "structurally_distinct_contract_shapes": len(
            {
                (
                    case.contract.target_requirement,
                    case.contract.allowed_auxiliary_kinds,
                    case.contract.payload_forbidden_factors,
                    case.projection.target_visibility,
                )
                for case in CASES
            }
        ),
        "variant_rows": len(rows),
        "candidate_correct": sum(bool(row["candidate_correct"]) for row in rows),
        "manual_correct": sum(bool(row["manual_correct"]) for row in rows),
        "candidate_manual_equal": sum(
            bool(row["candidate_manual_equal"]) for row in rows
        ),
        "compiled_manual_plan_equal": sum(
            bool(row["compiled_manual_plan_equal"]) for row in rows
        ),
        "record_scenarios": len(record_rows),
        "record_scenarios_correct": sum(
            bool(row["correct"]) for row in record_rows
        ),
    }
    if summary["candidate_correct"] != summary["variant_rows"]:
        raise AssertionError("ToolSandbox 候选结果存在错误")
    if summary["manual_correct"] != summary["variant_rows"]:
        raise AssertionError("ToolSandbox 手写基线结果存在错误")
    if summary["candidate_manual_equal"] != summary["variant_rows"]:
        raise AssertionError("候选与手写基线检测结果不一致")
    if summary["compiled_manual_plan_equal"] != summary["variant_rows"]:
        raise AssertionError("至少一个编译计划未匹配手写计划")
    if summary["record_scenarios_correct"] != summary["record_scenarios"]:
        raise AssertionError("ToolSandbox 记录消费场景存在错误")

    _write_csv(output_dir / "toolsandbox_results.csv", rows)
    _write_csv(output_dir / "toolsandbox_record_scenarios.csv", record_rows)
    (output_dir / "toolsandbox_plans.json").write_text(
        json.dumps(plans, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "toolsandbox_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    arguments = parser.parse_args()
    summary = run_panel(Path(arguments.output_dir))
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
