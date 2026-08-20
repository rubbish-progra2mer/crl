from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize_scalar


SEED = 20260816
M = 4
N_DRAWS = 4000
MARGIN = 0.02


def patterns(m: int) -> np.ndarray:
    return np.array(list(itertools.product((0, 1), repeat=m)), dtype=float)


def subsets(m: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    for order in (1, 2, 3):
        out.extend(itertools.combinations(range(m), order))
    return out


def design_matrix(cells: np.ndarray, subs: list[tuple[int, ...]]) -> np.ndarray:
    rows = [np.ones(len(cells))]
    for subset in subs:
        rows.append(cells[:, subset].prod(axis=1))
    return np.vstack(rows)


def expected_log_growth(values: np.ndarray, probs: np.ndarray, p0: float) -> tuple[float, float]:
    lower = float(values.min())
    upper_lambda = (1.0 - 1e-10) / max(p0 - lower, 1e-12)

    def loss(lam: float) -> float:
        factors = 1.0 + lam * (values - p0)
        if np.any(factors <= 0):
            return float("inf")
        return -float(np.dot(probs, np.log(factors)))

    result = minimize_scalar(loss, bounds=(0.0, upper_lambda), method="bounded")
    return -float(result.fun), float(result.x)


def main() -> None:
    rng = np.random.default_rng(SEED)
    cells = patterns(M)
    subs = subsets(M)
    a = design_matrix(cells, subs)
    c = np.zeros(len(cells))
    c[-1] = 1.0

    rows = []
    for _ in range(N_DRAWS):
        concentration = 10 ** rng.uniform(-1.0, 0.7)
        probs = rng.dirichlet(np.full(len(cells), concentration))
        b = a @ probs
        fit = linprog(c, A_eq=a, b_eq=b, bounds=(0.0, None), method="highs")
        if not fit.success:
            continue
        floor = float(fit.fun)
        observed = float(probs[-1])
        gap = observed - floor
        if not (0.25 <= floor <= 0.85 and gap <= 0.08 and floor > MARGIN + 0.05):
            continue

        dual = np.asarray(fit.eqlin.marginals, dtype=float)
        witness = a.T @ dual
        if np.max(witness - c) > 1e-7:
            raise RuntimeError("dual witness violates pointwise domination")
        p0 = floor - MARGIN
        direct_growth, direct_lambda = expected_log_growth(c, probs, p0)
        witness_growth, witness_lambda = expected_log_growth(witness, probs, p0)
        rows.append(
            {
                "floor": floor,
                "observed": observed,
                "identification_gap": gap,
                "p0": p0,
                "witness_min": float(witness.min()),
                "witness_max": float(witness.max()),
                "witness_variance": float(np.dot(probs, (witness - floor) ** 2)),
                "direct_variance": observed * (1.0 - observed),
                "witness_growth": witness_growth,
                "direct_growth": direct_growth,
                "growth_ratio": witness_growth / direct_growth if direct_growth > 0 else None,
                "witness_lambda": witness_lambda,
                "direct_lambda": direct_lambda,
                "probs": probs.tolist(),
                "dual": dual.tolist(),
            }
        )

    ratios = np.array([r["growth_ratio"] for r in rows], dtype=float)
    better = ratios > 1.0
    summary = {
        "seed": SEED,
        "m": M,
        "draws": N_DRAWS,
        "retained": len(rows),
        "margin": MARGIN,
        "moment_orders": [1, 2, 3],
        "fraction_witness_faster": float(better.mean()) if len(rows) else None,
        "growth_ratio_quantiles": {
            str(q): float(np.quantile(ratios, q)) for q in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)
        } if len(rows) else {},
        "best_cases": sorted(rows, key=lambda r: r["growth_ratio"], reverse=True)[:10],
        "worst_cases": sorted(rows, key=lambda r: r["growth_ratio"])[:10],
    }
    out = Path(__file__).with_name("dual_witness_sweep.json")
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in summary.items() if k not in {"best_cases", "worst_cases"}}, indent=2))


if __name__ == "__main__":
    main()
