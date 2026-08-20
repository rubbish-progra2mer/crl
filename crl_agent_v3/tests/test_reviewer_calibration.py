from __future__ import annotations

from crl_v3.reviewer_calibration import calibration_acceptance


def _fixture(score: int, *, emp: int = 2, adv: int = 2) -> dict[str, object]:
    return {
        "valid_triplet": True,
        "overall_score_numerator": score,
        "roles": {
            "EMP": {"scores": {"baseline_fairness": emp}},
            "ADV": {"scores": {"confound_leakage_control": adv}},
        },
    }


def test_calibration_acceptance_uses_only_frozen_semantic_anchors() -> None:
    result = calibration_acceptance(
        {
            "weak": _fixture(20),
            "medium": _fixture(50),
            "strong": _fixture(80),
            "unfair_baseline_trap": _fixture(45, emp=0, adv=1),
        }
    )
    assert result["accepted"] is True
    assert result["score_threshold_is_delivery_gate"] is False


def test_unfair_pretty_result_cannot_pass_without_critical_penalties() -> None:
    result = calibration_acceptance(
        {
            "weak": _fixture(20),
            "medium": _fixture(50),
            "strong": _fixture(80),
            "unfair_baseline_trap": _fixture(45, emp=3, adv=3),
        }
    )
    assert result["unfair_not_above_medium"] is True
    assert result["unfair_critical_dimensions_heavily_penalized"] is False
    assert result["accepted"] is False
