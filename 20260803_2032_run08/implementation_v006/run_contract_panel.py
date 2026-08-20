#!/usr/bin/env python3
"""运行 v006 合同差分、独立语义判定和消费闭环面板。"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Callable

from independent_semantic_oracle import (
    expected_identifiability_table,
    oracle_counterexample,
    validate_candidate_witness,
)
from observation_closed_effects import (
    CLAIM_AUXILIARY,
    CLAIM_COUNT,
    CLAIM_TARGET_IDENTITY,
    CLAIM_TARGET_RESPONSIVE,
    AdmissionDecision,
    AdmissionRequest,
    CompiledPlan,
    CoverageRecord,
    EffectContract,
    ObservedEvent,
    ProbeObservation,
    ProjectionSpec,
    UnsupportedContract,
    canonical_hash,
    compile_contract,
    consume_record,
    evaluate_observations,
    issue_record,
    payload_claim,
    request_for_plan,
)


def contract(
    name: str,
    *,
    primary_kind: str = "write",
    count: int = 1,
    auxiliary: tuple[str, ...] = (),
    target: str = "none",
    factors: tuple[str, ...] = (),
) -> EffectContract:
    return EffectContract(
        contract_version=f"contract-{name}-v1",
        primary_kind=primary_kind,
        exact_primary_count=count,
        allowed_auxiliary_kinds=auxiliary,
        target_requirement=target,  # type: ignore[arg-type]
        payload_forbidden_factors=factors,
    )


def projection(
    name: str,
    *,
    target: str = "stable_anonymous",
    payload: str = "stable_anonymous",
) -> ProjectionSpec:
    return ProjectionSpec(
        projection_version=f"projection-{name}-v1",
        target_visibility=target,  # type: ignore[arg-type]
        payload_visibility=payload,  # type: ignore[arg-type]
        normalizer_id=f"normalizer-{name}-v1",
    )


PANEL = (
    (
        "responsive_stable",
        contract("responsive", target="responsive"),
        projection("stable"),
        {
            "probe_ids": ("base", "target_0", "target_1"),
            "relation_claims": (CLAIM_TARGET_RESPONSIVE,),
            "nonidentifiable": (),
        },
    ),
    (
        "identity_revealed",
        contract("identity-revealed", target="identity"),
        projection("revealed", target="revealed"),
        {
            "probe_ids": ("base", "target_identity_0", "target_identity_1"),
            "relation_claims": (CLAIM_TARGET_IDENTITY,),
            "nonidentifiable": (),
        },
    ),
    (
        "identity_stable_anonymous",
        contract("identity-stable", target="identity"),
        projection("identity-stable"),
        {
            "probe_ids": ("base",),
            "relation_claims": (),
            "nonidentifiable": (CLAIM_TARGET_IDENTITY,),
        },
    ),
    (
        "responsive_clone_local",
        contract("responsive-local", target="responsive"),
        projection("responsive-local", target="clone_local_anonymous"),
        {
            "probe_ids": ("base",),
            "relation_claims": (),
            "nonidentifiable": (CLAIM_TARGET_RESPONSIVE,),
        },
    ),
    (
        "ambient_stable",
        contract("ambient", factors=("ambient_canary",)),
        projection("ambient-stable"),
        {
            "probe_ids": ("ambient_0", "ambient_1", "base"),
            "relation_claims": (payload_claim("ambient_canary"),),
            "nonidentifiable": (),
        },
    ),
    (
        "ambient_clone_local",
        contract("ambient-local", factors=("ambient_canary",)),
        projection("ambient-local", payload="clone_local_anonymous"),
        {
            "probe_ids": ("base",),
            "relation_claims": (),
            "nonidentifiable": (payload_claim("ambient_canary"),),
        },
    ),
    (
        "two_payload_factors",
        contract(
            "two-factors",
            factors=("ambient_canary", "sensitive_input"),
        ),
        projection("two-factors"),
        {
            "probe_ids": (
                "ambient_0",
                "ambient_1",
                "base",
                "sensitive_0",
                "sensitive_1",
            ),
            "relation_claims": (
                payload_claim("ambient_canary"),
                payload_claim("sensitive_input"),
            ),
            "nonidentifiable": (),
        },
    ),
    (
        "auxiliary_allowed",
        contract("auxiliary", auxiliary=("audit",)),
        projection("auxiliary"),
        {
            "probe_ids": ("base",),
            "relation_claims": (),
            "nonidentifiable": (),
        },
    ),
    (
        "combined",
        contract(
            "combined",
            primary_kind="message_send",
            auxiliary=("audit",),
            target="responsive",
            factors=("ambient_canary", "sensitive_input"),
        ),
        projection("combined"),
        {
            "probe_ids": (
                "ambient_0",
                "ambient_1",
                "base",
                "sensitive_0",
                "sensitive_1",
                "target_0",
                "target_1",
            ),
            "relation_claims": (
                payload_claim("ambient_canary"),
                payload_claim("sensitive_input"),
                CLAIM_TARGET_RESPONSIVE,
            ),
            "nonidentifiable": (),
        },
    ),
)


REJECTIONS = (
    ("count_zero", contract("count-zero", count=0), projection("count-zero")),
    ("count_two", contract("count-two", count=2), projection("count-two")),
    (
        "unknown_factor",
        contract("unknown-factor", factors=("session_secret",)),
        projection("unknown-factor"),
    ),
    (
        "duplicate_auxiliary",
        contract("duplicate-aux", auxiliary=("audit", "audit")),
        projection("duplicate-aux"),
    ),
)


def compliant_observations(
    plan: CompiledPlan, *, include_allowed_auxiliary: bool = False
) -> tuple[ProbeObservation, ...]:
    observations: list[ProbeObservation] = []
    identity_expected = {
        relation.left_probe: relation.expected_value
        for relation in plan.relations
        if relation.relation_kind == "target_equals_expected"
    }
    for probe in plan.probes:
        if probe.probe_id in identity_expected:
            target_token = str(identity_expected[probe.probe_id])
        else:
            target_token = f"target-token:{probe.target_value}"
        events = [
            ObservedEvent(
                kind=plan.primary_kind,
                target_token=target_token,
                payload_token="stable-payload-token",
            )
        ]
        if include_allowed_auxiliary and plan.allowed_auxiliary_kinds:
            events.append(
                ObservedEvent(
                    kind=plan.allowed_auxiliary_kinds[0],
                    target_token="aux-target",
                    payload_token="aux-payload",
                )
            )
        observations.append(ProbeObservation(probe.probe_id, tuple(events)))
    return tuple(observations)


def mutate_observations(
    observations: tuple[ProbeObservation, ...],
    predicate: Callable[[ProbeObservation], bool],
    mutation: Callable[[ProbeObservation], ProbeObservation],
) -> tuple[ProbeObservation, ...]:
    return tuple(mutation(item) if predicate(item) else item for item in observations)


def _first_primary(observation: ProbeObservation) -> ObservedEvent:
    return observation.events[0]


def make_fixed_target(observation: ProbeObservation) -> ProbeObservation:
    primary = _first_primary(observation)
    return replace(
        observation,
        events=(replace(primary, target_token="fixed-target-token"),)
        + observation.events[1:],
    )


def make_payload_leak(observation: ProbeObservation) -> ProbeObservation:
    primary = _first_primary(observation)
    return replace(
        observation,
        events=(
            replace(
                primary,
                payload_token=f"leaked:{observation.probe_id}",
            ),
        )
        + observation.events[1:],
    )


def observation_unaware_identifiable(claim_id: str, visibility: str) -> bool:
    """具体强基线：从规格生成关系，但不计算投影的观察闭包。"""

    del claim_id, visibility
    return True


def boolean_report_consumer(
    record: CoverageRecord, request: AdmissionRequest
) -> AdmissionDecision:
    del request
    return AdmissionDecision(record.status == "pass", ())


def binding_only_consumer(
    record: CoverageRecord, request: AdmissionRequest
) -> AdmissionDecision:
    bindings_ok = (
        record.tool_id == request.tool_id
        and record.tool_version == request.tool_version
        and record.contract_hash == request.contract_hash
        and record.projection_hash == request.projection_hash
        and record.probe_catalog_hash == request.probe_catalog_hash
        and record.plan_hash == request.plan_hash
        and record.evidence_hash == request.evidence_hash
    )
    return AdmissionDecision(record.status == "pass" and bindings_ok, ())


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_panel(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    panel_rows: list[dict[str, object]] = []
    plans: dict[str, object] = {}
    compiled_by_name: dict[str, CompiledPlan] = {}

    for name, item_contract, item_projection, expected in PANEL:
        plan = compile_contract(item_contract, item_projection)
        compiled_by_name[name] = plan
        probe_ids = tuple(probe.probe_id for probe in plan.probes)
        relation_claims = tuple(
            sorted({relation.claim_id for relation in plan.relations})
        )
        nonidentifiable = tuple(
            sorted(item.claim_id for item in plan.nonidentifiable)
        )
        expected_ok = (
            probe_ids == expected["probe_ids"]
            and relation_claims == expected["relation_claims"]
            and nonidentifiable == expected["nonidentifiable"]
        )
        good_report = evaluate_observations(plan, compliant_observations(plan))
        record = issue_record(
            plan,
            good_report,
            tool_id=f"tool:{name}",
            tool_version="1",
        )
        decision = consume_record(
            record,
            request_for_plan(
                plan,
                tool_id=f"tool:{name}",
                tool_version="1",
                evidence_hash=record.evidence_hash,
            ),
        )
        should_admit = not plan.nonidentifiable
        panel_rows.append(
            {
                "case": name,
                "compiled": True,
                "expected_shape_ok": expected_ok,
                "probe_count": len(plan.probes),
                "relation_count": len(plan.relations),
                "nonidentifiable_count": len(plan.nonidentifiable),
                "good_evidence_failed_claims": len(good_report.failed_claims),
                "consumer_allowed": decision.allowed,
                "expected_allowed": should_admit,
                "consumer_correct": decision.allowed == should_admit,
                "plan_hash": plan.plan_hash,
            }
        )
        plans[name] = asdict(plan)

    for name, item_contract, item_projection in REJECTIONS:
        rejected = False
        message = ""
        try:
            compile_contract(item_contract, item_projection)
        except UnsupportedContract as error:
            rejected = True
            message = str(error)
        panel_rows.append(
            {
                "case": name,
                "compiled": not rejected,
                "expected_shape_ok": rejected,
                "probe_count": "",
                "relation_count": "",
                "nonidentifiable_count": "",
                "good_evidence_failed_claims": "",
                "consumer_allowed": False,
                "expected_allowed": False,
                "consumer_correct": rejected,
                "plan_hash": "",
                "rejection": message,
            }
        )

    oracle_table = expected_identifiability_table()
    identifiability_rows: list[dict[str, object]] = []
    for claim_id, visibility_map in sorted(oracle_table.items()):
        for visibility, oracle_value in sorted(visibility_map.items()):
            if claim_id == CLAIM_TARGET_RESPONSIVE:
                item_contract = contract(
                    f"oracle-{claim_id}-{visibility}", target="responsive"
                )
                item_projection = projection(
                    f"oracle-{claim_id}-{visibility}", target=visibility
                )
            elif claim_id == CLAIM_TARGET_IDENTITY:
                item_contract = contract(
                    f"oracle-{claim_id}-{visibility}", target="identity"
                )
                item_projection = projection(
                    f"oracle-{claim_id}-{visibility}", target=visibility
                )
            else:
                factor = claim_id.split(":", 1)[1]
                item_contract = contract(
                    f"oracle-{factor}-{visibility}", factors=(factor,)
                )
                item_projection = projection(
                    f"oracle-{factor}-{visibility}", payload=visibility
                )
            plan = compile_contract(item_contract, item_projection)
            candidate_value = claim_id in set(plan.identifiable_claims)
            witness = next(
                (item for item in plan.nonidentifiable if item.claim_id == claim_id),
                None,
            )
            witness_check: dict[str, object] | None = None
            if witness is not None:
                witness_check = validate_candidate_witness(
                    claim_id=claim_id,
                    visibility=visibility,
                    world_true=asdict(witness.world_true),
                    world_false=asdict(witness.world_false),
                )
            oracle_example = oracle_counterexample(claim_id, visibility)
            baseline_value = observation_unaware_identifiable(claim_id, visibility)
            identifiability_rows.append(
                {
                    "claim": claim_id,
                    "visibility": visibility,
                    "oracle_identifiable": oracle_value,
                    "candidate_identifiable": candidate_value,
                    "candidate_correct": candidate_value == oracle_value,
                    "candidate_witness_valid": (
                        "" if witness_check is None else witness_check["valid"]
                    ),
                    "oracle_has_counterexample": oracle_example is not None,
                    "observation_unaware_identifiable": baseline_value,
                    "observation_unaware_correct": baseline_value == oracle_value,
                }
            )

    combined = compiled_by_name["combined"]
    combined_report = evaluate_observations(
        combined, compliant_observations(combined, include_allowed_auxiliary=True)
    )
    good_record = issue_record(
        combined,
        combined_report,
        tool_id="tool:combined",
        tool_version="1",
    )
    good_request = request_for_plan(
        combined,
        tool_id="tool:combined",
        tool_version="1",
        evidence_hash=good_record.evidence_hash,
    )

    identity_stable = compiled_by_name["identity_stable_anonymous"]
    identity_record = issue_record(
        identity_stable,
        evaluate_observations(
            identity_stable, compliant_observations(identity_stable)
        ),
        tool_id="tool:identity-stable",
        tool_version="1",
    )
    identity_request = request_for_plan(
        identity_stable,
        tool_id="tool:identity-stable",
        tool_version="1",
        evidence_hash=identity_record.evidence_hash,
    )

    failed_target_observations = mutate_observations(
        compliant_observations(combined, include_allowed_auxiliary=True),
        lambda item: item.probe_id.startswith("target_"),
        make_fixed_target,
    )
    failed_record = issue_record(
        combined,
        evaluate_observations(combined, failed_target_observations),
        tool_id="tool:combined",
        tool_version="1",
    )

    tampered_record = replace(
        good_record,
        passed_claims=good_record.passed_claims + (CLAIM_TARGET_IDENTITY,),
    )
    tampered_witness_binding = replace(
        good_record,
        nonidentifiability_witness_hashes=("changed",),
    )

    scenarios: list[
        tuple[str, CoverageRecord, AdmissionRequest, bool]
    ] = [
        ("exact_match", good_record, good_request, True),
        (
            "tool_id_changed",
            good_record,
            replace(good_request, tool_id="tool:other"),
            False,
        ),
        (
            "tool_version_changed",
            good_record,
            replace(good_request, tool_version="2"),
            False,
        ),
        (
            "contract_changed",
            good_record,
            replace(good_request, contract_hash="changed"),
            False,
        ),
        (
            "projection_changed",
            good_record,
            replace(good_request, projection_hash="changed"),
            False,
        ),
        (
            "probe_catalog_changed",
            good_record,
            replace(good_request, probe_catalog_hash="changed"),
            False,
        ),
        (
            "plan_changed",
            good_record,
            replace(good_request, plan_hash="changed"),
            False,
        ),
        (
            "evidence_changed",
            good_record,
            replace(good_request, evidence_hash="changed"),
            False,
        ),
        (
            "identity_overclaim",
            good_record,
            replace(
                good_request,
                required_claims=good_request.required_claims
                + (CLAIM_TARGET_IDENTITY,),
            ),
            False,
        ),
        (
            "sequence_boundary_overclaim",
            good_record,
            replace(
                good_request,
                required_claims=good_request.required_claims
                + ("relation.sequence.second_call_safe",),
            ),
            False,
        ),
        (
            "compound_boundary_overclaim",
            good_record,
            replace(
                good_request,
                required_claims=good_request.required_claims
                + ("relation.compound.trigger_safe",),
            ),
            False,
        ),
        (
            "empty_required_claims",
            good_record,
            replace(good_request, required_claims=()),
            False,
        ),
        ("tampered_record", tampered_record, good_request, False),
        (
            "tampered_witness_binding",
            tampered_witness_binding,
            good_request,
            False,
        ),
        (
            "unsupported_record_schema",
            replace(good_record, schema_version=2),
            good_request,
            False,
        ),
        (
            "nonidentifiable_contract",
            identity_record,
            identity_request,
            False,
        ),
        ("failed_evidence", failed_record, good_request, False),
    ]

    consumer_rows: list[dict[str, object]] = []
    for name, record, request, expected in scenarios:
        candidate = consume_record(record, request)
        boolean = boolean_report_consumer(record, request)
        binding = binding_only_consumer(record, request)
        consumer_rows.append(
            {
                "scenario": name,
                "expected_allowed": expected,
                "candidate_allowed": candidate.allowed,
                "candidate_correct": candidate.allowed == expected,
                "candidate_reasons": "|".join(candidate.reasons),
                "boolean_report_allowed": boolean.allowed,
                "boolean_report_correct": boolean.allowed == expected,
                "binding_only_allowed": binding.allowed,
                "binding_only_correct": binding.allowed == expected,
            }
        )

    # 有信息量的关系回归：同一计划上目标固定与两类载荷泄漏必须分别失败。
    fault_rows: list[dict[str, object]] = []
    good_observations = compliant_observations(
        combined, include_allowed_auxiliary=True
    )
    variants = {
        "clean": good_observations,
        "fixed_target": mutate_observations(
            good_observations,
            lambda item: item.probe_id.startswith("target_"),
            make_fixed_target,
        ),
        "ambient_payload_leak": mutate_observations(
            good_observations,
            lambda item: item.probe_id.startswith("ambient_"),
            make_payload_leak,
        ),
        "sensitive_payload_leak": mutate_observations(
            good_observations,
            lambda item: item.probe_id.startswith("sensitive_"),
            make_payload_leak,
        ),
    }
    for name, observations in variants.items():
        report = evaluate_observations(combined, observations)
        predicted_violation = bool(report.failed_claims)
        expected_violation = name != "clean"
        fault_rows.append(
            {
                "variant": name,
                "expected_violation": expected_violation,
                "predicted_violation": predicted_violation,
                "correct": predicted_violation == expected_violation,
                "failed_claims": "|".join(report.failed_claims),
            }
        )

    primary_kind_changed = compile_contract(
        replace(PANEL[0][1], primary_kind="other_write"), PANEL[0][2]
    )
    auxiliary_changed = compile_contract(
        replace(PANEL[0][1], allowed_auxiliary_kinds=("audit",)), PANEL[0][2]
    )
    target_disabled = compile_contract(
        replace(PANEL[0][1], target_requirement="none"), PANEL[0][2]
    )
    payload_added = compile_contract(
        replace(
            PANEL[0][1],
            target_requirement="none",
            payload_forbidden_factors=("ambient_canary",),
        ),
        PANEL[0][2],
    )
    contract_version_changed = compile_contract(
        replace(PANEL[0][1], contract_version="contract-responsive-v2"),
        PANEL[0][2],
    )
    field_sensitivity = {
        "primary_kind_changes_plan": (
            primary_kind_changed.primary_kind
            != compiled_by_name["responsive_stable"].primary_kind
        ),
        "allowed_auxiliary_changes_plan": (
            auxiliary_changed.allowed_auxiliary_kinds
            != compiled_by_name["responsive_stable"].allowed_auxiliary_kinds
        ),
        "target_requirement_changes_plan": (
            tuple(item.probe_id for item in target_disabled.probes)
            != tuple(
                item.probe_id
                for item in compiled_by_name["responsive_stable"].probes
            )
            and target_disabled.relations
            != compiled_by_name["responsive_stable"].relations
        ),
        "payload_factor_changes_plan": (
            tuple(item.probe_id for item in payload_added.probes)
            != tuple(item.probe_id for item in target_disabled.probes)
            and payload_added.relations != target_disabled.relations
        ),
        "projection_changes_plan": (
            compiled_by_name["ambient_stable"].relations
            != compiled_by_name["ambient_clone_local"].relations
            and compiled_by_name["ambient_stable"].nonidentifiable
            != compiled_by_name["ambient_clone_local"].nonidentifiable
        ),
        "contract_version_changes_binding": (
            contract_version_changed.contract_hash
            != compiled_by_name["responsive_stable"].contract_hash
            and contract_version_changed.probes
            == compiled_by_name["responsive_stable"].probes
            and contract_version_changed.relations
            == compiled_by_name["responsive_stable"].relations
            and contract_version_changed.plan_hash
            != compiled_by_name["responsive_stable"].plan_hash
        ),
        "non_unary_contract_fails_closed": (
            any(row["case"] == "count_two" and row["expected_shape_ok"] for row in panel_rows)
            and any(row["case"] == "count_zero" and row["expected_shape_ok"] for row in panel_rows)
        ),
    }

    summary = {
        "schema_version": 1,
        "panel_cases": len(panel_rows),
        "panel_correct": sum(
            bool(row["expected_shape_ok"]) and bool(row["consumer_correct"])
            for row in panel_rows
        ),
        "identifiability_cases": len(identifiability_rows),
        "candidate_identifiability_correct": sum(
            bool(row["candidate_correct"]) for row in identifiability_rows
        ),
        "candidate_nonidentifiability_witnesses": sum(
            row["candidate_witness_valid"] is True
            for row in identifiability_rows
        ),
        "observation_unaware_identifiability_correct": sum(
            bool(row["observation_unaware_correct"])
            for row in identifiability_rows
        ),
        "consumer_scenarios": len(consumer_rows),
        "candidate_consumer_correct": sum(
            bool(row["candidate_correct"]) for row in consumer_rows
        ),
        "boolean_report_consumer_correct": sum(
            bool(row["boolean_report_correct"]) for row in consumer_rows
        ),
        "binding_only_consumer_correct": sum(
            bool(row["binding_only_correct"]) for row in consumer_rows
        ),
        "fault_regressions": len(fault_rows),
        "fault_regressions_correct": sum(
            bool(row["correct"]) for row in fault_rows
        ),
        "field_sensitivity": field_sensitivity,
        "all_field_sensitivity_checks_pass": all(field_sensitivity.values()),
    }

    if summary["panel_correct"] != summary["panel_cases"]:
        raise AssertionError("合同差分面板存在失败")
    if (
        summary["candidate_identifiability_correct"]
        != summary["identifiability_cases"]
    ):
        raise AssertionError("候选可辨识性结果与独立语义判定器不一致")
    if summary["candidate_consumer_correct"] != summary["consumer_scenarios"]:
        raise AssertionError("覆盖记录消费场景存在失败")
    if summary["fault_regressions_correct"] != summary["fault_regressions"]:
        raise AssertionError("关系故障回归存在失败")
    if not summary["all_field_sensitivity_checks_pass"]:
        raise AssertionError("至少一个合同字段未改变计划身份")

    _write_csv(output_dir / "contract_panel.csv", panel_rows)
    _write_csv(output_dir / "identifiability_matrix.csv", identifiability_rows)
    _write_csv(output_dir / "consumer_scenarios.csv", consumer_rows)
    _write_csv(output_dir / "fault_regressions.csv", fault_rows)
    (output_dir / "compiled_plans.json").write_text(
        json.dumps(plans, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "summary.json").write_text(
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
