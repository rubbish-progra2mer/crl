from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


Atom = tuple[Fraction, Fraction, int]


def fraction_record(value: Fraction) -> dict[str, object]:
    return {"fraction": str(value), "float": float(value)}


def weighted_isotonic_fit(atoms: list[Atom]) -> dict[Fraction, Fraction]:
    """对相同预测分数聚合后执行加权池相邻违反者算法。"""
    grouped: dict[Fraction, tuple[int, Fraction]] = {}
    for true_score, predicted_score, weight in atoms:
        old_weight, old_sum = grouped.get(predicted_score, (0, Fraction(0)))
        grouped[predicted_score] = (old_weight + weight, old_sum + weight * true_score)

    blocks: list[dict[str, object]] = []
    for predicted_score in sorted(grouped):
        weight, target_sum = grouped[predicted_score]
        blocks.append(
            {
                "xs": [predicted_score],
                "weight": weight,
                "target_sum": target_sum,
                "mean": target_sum / weight,
            }
        )
        while len(blocks) >= 2 and blocks[-2]["mean"] > blocks[-1]["mean"]:
            right = blocks.pop()
            left = blocks.pop()
            merged_weight = int(left["weight"]) + int(right["weight"])
            merged_sum = Fraction(left["target_sum"]) + Fraction(right["target_sum"])
            blocks.append(
                {
                    "xs": list(left["xs"]) + list(right["xs"]),
                    "weight": merged_weight,
                    "target_sum": merged_sum,
                    "mean": merged_sum / merged_weight,
                }
            )

    fitted: dict[Fraction, Fraction] = {}
    for block in blocks:
        for predicted_score in block["xs"]:
            fitted[Fraction(predicted_score)] = Fraction(block["mean"])
    return fitted


def build_atoms(replication: int) -> list[Atom]:
    return [
        (Fraction(1, 4), Fraction(1, 10), replication),
        (Fraction(1, 4), Fraction(1, 2), replication),
        (Fraction(3, 4), Fraction(1, 2), replication),
        (Fraction(3, 4), Fraction(9, 10), replication),
    ]


def conditional_calibrated_means(fitted: dict[Fraction, Fraction]) -> dict[Fraction, Fraction]:
    return {
        Fraction(1, 4): (fitted[Fraction(1, 10)] + fitted[Fraction(1, 2)]) / 2,
        Fraction(3, 4): (fitted[Fraction(1, 2)] + fitted[Fraction(9, 10)]) / 2,
    }


def gradient(mean_low: Fraction, mean_high: Fraction) -> Fraction:
    return (-mean_low + mean_high) / 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    replications = (1, 10, 1000, 1_000_000)
    audits: list[dict[str, object]] = []
    reference_fit: dict[Fraction, Fraction] | None = None
    reference_residuals: dict[Fraction, Fraction] | None = None
    for replication in replications:
        fitted = weighted_isotonic_fit(build_atoms(replication))
        calibrated_means = conditional_calibrated_means(fitted)
        residuals = {level: calibrated_means[level] - level for level in calibrated_means}
        if reference_fit is None:
            reference_fit = fitted
            reference_residuals = residuals
        audits.append(
            {
                "replication": replication,
                "effective_anchor_weight": 4 * replication,
                "fit": {str(x): fraction_record(y) for x, y in fitted.items()},
                "conditional_calibrated_mean": {
                    str(level): fraction_record(value) for level, value in calibrated_means.items()
                },
                "conditional_residual": {
                    str(level): fraction_record(value) for level, value in residuals.items()
                },
                "same_as_population_reference": fitted == reference_fit and residuals == reference_residuals,
            }
        )

    assert reference_fit is not None
    assert reference_residuals is not None
    true_gradient = gradient(Fraction(1, 4), Fraction(3, 4))
    raw_world_gradient = gradient(Fraction(3, 10), Fraction(7, 10))
    calibrated_means = conditional_calibrated_means(reference_fit)
    calibrated_gradient = gradient(
        calibrated_means[Fraction(1, 4)], calibrated_means[Fraction(3, 4)]
    )

    assumptions = {
        "true_and_predicted_scores_bounded_unit_interval": True,
        "phi_strictly_monotone_on_levels": Fraction(3, 10) < Fraction(7, 10),
        "positive_level_separation": Fraction(7, 10) - Fraction(3, 10) == Fraction(2, 5),
        "positive_balanced_anchor_coverage": Fraction(1, 2) > 0,
        "noise_conditionally_zero_mean": (Fraction(-1, 5) + Fraction(1, 5)) / 2 == 0,
        "noise_bounded": max(abs(Fraction(-1, 5)), abs(Fraction(1, 5))) <= 1,
        "raw_bias_bound_is_one_twentieth": max(
            abs(Fraction(3, 10) - Fraction(1, 4)),
            abs(Fraction(7, 10) - Fraction(3, 4)),
        )
        == Fraction(1, 20),
    }
    expected_fit = {
        Fraction(1, 10): Fraction(1, 4),
        Fraction(1, 2): Fraction(1, 2),
        Fraction(9, 10): Fraction(3, 4),
    }
    expected_residuals = {
        Fraction(1, 4): Fraction(1, 8),
        Fraction(3, 4): Fraction(-1, 8),
    }
    assertions = {
        "all_stated_assumptions_hold": all(assumptions.values()),
        "population_isotonic_fit_matches_preregistration": reference_fit == expected_fit,
        "nonvanishing_conditional_residuals_match_preregistration": (
            reference_residuals == expected_residuals
        ),
        "replication_does_not_change_fit_or_residual": all(
            audit["same_as_population_reference"] for audit in audits
        ),
        "true_gradient_is_one_quarter": true_gradient == Fraction(1, 4),
        "raw_world_gradient_is_one_fifth": raw_world_gradient == Fraction(1, 5),
        "calibrated_gradient_is_one_eighth": calibrated_gradient == Fraction(1, 8),
        "calibration_increases_absolute_gradient_bias": (
            abs(calibrated_gradient - true_gradient)
            > abs(raw_world_gradient - true_gradient)
        ),
    }
    payload = {
        "experiment": "wmrl-isotonic-overlap-counterexample",
        "distribution": {
            "true_levels": [fraction_record(Fraction(1, 4)), fraction_record(Fraction(3, 4))],
            "phi": "1/10 + 4*r/5",
            "phi_at_levels": [fraction_record(Fraction(3, 10)), fraction_record(Fraction(7, 10))],
            "noise_support": [fraction_record(Fraction(-1, 5)), fraction_record(Fraction(1, 5))],
            "atoms": [
                {
                    "true_score": fraction_record(true_score),
                    "predicted_score": fraction_record(predicted_score),
                    "probability": fraction_record(Fraction(1, 4)),
                }
                for true_score, predicted_score, _ in build_atoms(1)
            ],
        },
        "assumptions": assumptions,
        "replication_audit": audits,
        "gradient_witness": {
            "score_function_low_high": [-1, 1],
            "true_gradient": fraction_record(true_gradient),
            "raw_world_gradient": fraction_record(raw_world_gradient),
            "calibrated_gradient": fraction_record(calibrated_gradient),
            "raw_absolute_bias": fraction_record(abs(raw_world_gradient - true_gradient)),
            "calibrated_absolute_bias": fraction_record(abs(calibrated_gradient - true_gradient)),
        },
        "assertions": assertions,
        "all_assertions_passed": all(assertions.values()),
        "interpretation_boundary": (
            "只检验目标论文 Lemma 11 的已写假设是否足以保证正文等距回归目标的逐轨迹系统误差消失；"
            "不评价真实任务经验结果，也不自动形成新方法。"
        ),
    }
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if not payload["all_assertions_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
