from __future__ import annotations

import json
import re
from decimal import Decimal
from pathlib import Path

from .reviewer_protocol import (
    ROLE_WEIGHTS,
    ROLES,
    load_evaluator,
    role_score_basis_points,
)
from .reviewer_runtime import _invoke_role
from .workspace import _publish_once, _required_file, _sha256


FIXTURE_NAMES = ("weak", "medium", "strong", "unfair_baseline_trap")
_RUN_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,63}")


def calibration_root() -> Path:
    return Path(__file__).resolve().parents[1] / "evaluation" / "reviewer_calibration"


def run_calibration(
    run_id: str,
    *,
    timeout_seconds: float = 1800,
) -> dict[str, object]:
    if _RUN_ID.fullmatch(run_id) is None:
        raise ValueError("calibration run id must be 3-64 lowercase safe characters")
    root = calibration_root()
    destination = root / "results" / run_id
    if destination.exists():
        raise FileExistsError(f"calibration result already exists: {run_id}")
    destination.mkdir(parents=True)
    evaluator = load_evaluator()
    fixture_summaries: dict[str, dict[str, object]] = {}
    for fixture in FIXTURE_NAMES:
        packet = _required_file(root / f"{fixture}.md", within=root)
        fixture_root = destination / fixture
        fixture_root.mkdir()
        role_summaries: dict[str, dict[str, object]] = {}
        valid = True
        for role in ROLES:
            role_root = fixture_root / role
            role_root.mkdir()
            result = _invoke_role(role, packet, timeout_seconds=timeout_seconds)
            _publish_once(role_root / "events.jsonl", result["events"], within=destination)
            _publish_once(role_root / "stderr.bin", result["stderr"], within=destination)
            _publish_once(role_root / "raw_output.json", result["raw_output"], within=destination)
            valid = valid and result["valid"] is True
            role_score = None
            if result["valid"] is True:
                role_score = role_score_basis_points(role, result["output"]["scores"])
            report = {
                "schema_version": 1,
                "fixture": fixture,
                "fixture_sha256": _sha256(packet),
                "reviewer_role": role,
                "evaluator_version": evaluator["manifest"]["evaluator_version"],
                "evaluator_definition_sha256": evaluator["definition_sha256"],
                "valid": result["valid"],
                "invalid_reasons": result["invalid_reasons"],
                "runtime": result["runtime"],
                "events_sha256": _sha256(result["events"]),
                "stderr_sha256": _sha256(result["stderr"]),
                "raw_output_sha256": _sha256(result["raw_output"]),
                "role_score_basis_points": role_score,
                "output": result.get("output"),
            }
            _publish_once(
                role_root / "report.json", _json_bytes(report), within=destination
            )
            role_summaries[role] = {
                "valid": report["valid"],
                "role_score_basis_points": role_score,
                "scores": result["output"]["scores"] if result.get("output") else None,
            }
        numerator = None
        if valid:
            numerator = sum(
                int(role_summaries[role]["role_score_basis_points"])
                * ROLE_WEIGHTS[role]
                for role in ROLES
            )
        fixture_summary = {
            "fixture_sha256": _sha256(packet),
            "valid_triplet": valid,
            "overall_score_numerator": numerator,
            "overall_score_percent": _percent(numerator),
            "roles": role_summaries,
        }
        _publish_once(
            fixture_root / "summary.json",
            _json_bytes(fixture_summary),
            within=destination,
        )
        fixture_summaries[fixture] = fixture_summary

    acceptance = calibration_acceptance(fixture_summaries)
    summary = {
        "schema_version": 1,
        "calibration_run_id": run_id,
        "evaluator_version": evaluator["manifest"]["evaluator_version"],
        "evaluator_definition_sha256": evaluator["definition_sha256"],
        "one_fresh_triplet_per_fixture": True,
        "fixtures": fixture_summaries,
        "acceptance": acceptance,
    }
    _publish_once(destination / "summary.json", _json_bytes(summary), within=destination)
    return summary


def calibration_acceptance(
    fixtures: dict[str, dict[str, object]],
) -> dict[str, object]:
    missing = set(FIXTURE_NAMES) - set(fixtures)
    if missing:
        raise ValueError(f"missing calibration fixtures: {sorted(missing)}")
    valid = all(fixtures[name].get("valid_triplet") is True for name in FIXTURE_NAMES)
    scores = {
        name: fixtures[name].get("overall_score_numerator") for name in FIXTURE_NAMES
    }
    numeric = all(type(value) is int for value in scores.values())
    ordering = bool(
        numeric
        and scores["strong"] > scores["medium"] > scores["weak"]
    )
    unfair_not_above_medium = bool(
        numeric and scores["unfair_baseline_trap"] <= scores["medium"]
    )
    unfair_roles = fixtures["unfair_baseline_trap"].get("roles")
    emp_penalty = None
    adv_penalty = None
    if isinstance(unfair_roles, dict):
        emp = unfair_roles.get("EMP")
        adv = unfair_roles.get("ADV")
        if isinstance(emp, dict) and isinstance(emp.get("scores"), dict):
            emp_penalty = emp["scores"].get("baseline_fairness")
        if isinstance(adv, dict) and isinstance(adv.get("scores"), dict):
            adv_penalty = adv["scores"].get("confound_leakage_control")
    critical_penalties = (
        type(emp_penalty) is int
        and emp_penalty <= 1
        and type(adv_penalty) is int
        and adv_penalty <= 1
    )
    return {
        "all_triplets_valid": valid,
        "strong_gt_medium_gt_weak": ordering,
        "unfair_not_above_medium": unfair_not_above_medium,
        "unfair_emp_baseline_fairness": emp_penalty,
        "unfair_adv_confound_leakage_control": adv_penalty,
        "unfair_critical_dimensions_heavily_penalized": critical_penalties,
        "accepted": bool(
            valid and ordering and unfair_not_above_medium and critical_penalties
        ),
        "score_threshold_is_delivery_gate": False,
    }


def _percent(numerator: object) -> str | None:
    if type(numerator) is not int:
        return None
    return f"{Decimal(numerator) / Decimal(10000):.4f}"


def _json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
