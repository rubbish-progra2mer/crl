#!/usr/bin/env python3
"""Threshold-free statistics, pure stdlib. Single source of truth for the harnesses.

Every function here is deliberately simple enough to audit by reading. No scipy,
no sklearn — a reviewer reproduces these numbers from a bare Python install.

Design notes that matter for how the results should be read:

* AUROC is the normalised Mann-Whitney U, ties credited 0.5. It answers "does ANY
  operating point separate these classes", which is the question a catch-rate at
  one threshold cannot answer.
* ``oracle_best_threshold`` sweeps BOTH polarities and says which one won. This
  matters: when AUROC < 0.5 the discriminating direction is the inverted one, and
  a one-sided sweep silently reports the trivial predict-everything point as the
  ceiling. A ceiling only reachable by inverting a gate's sense is a finding
  about sign, not an available repair.
* The percentile bootstrap DEGENERATES under perfect separation (every resample
  is also perfectly separated, so the interval collapses). Use
  ``exact_permutation_p`` there instead; ``summarise`` picks correctly.
"""

from __future__ import annotations

import math
import random

DEFAULT_SEED = 20260726
DEFAULT_BOOTSTRAP_ITERS = 4000
DEFAULT_PERM_ITERS = 20000


# --------------------------------------------------------------------------- AUROC


def auroc(pos: list[float], neg: list[float]) -> float:
    """P(score_pos > score_neg), ties credited 0.5. NaN if either side is empty."""
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    for p in pos:
        for n in neg:
            wins += 1.0 if p > n else (0.5 if p == n else 0.0)
    return wins / (len(pos) * len(neg))


def bootstrap_ci(
    pos: list[float],
    neg: list[float],
    iters: int = DEFAULT_BOOTSTRAP_ITERS,
    seed: int = DEFAULT_SEED,
) -> tuple[float, float]:
    """Percentile bootstrap CI for AUROC. Meaningless under perfect separation."""
    rng = random.Random(seed)
    vals = []
    for _ in range(iters):
        rp = [rng.choice(pos) for _ in pos]
        rn = [rng.choice(neg) for _ in neg]
        vals.append(auroc(rp, rn))
    vals.sort()
    return vals[int(0.025 * iters)], vals[int(0.975 * iters)]


def exact_permutation_p(pos: list[float], neg: list[float]) -> float | None:
    """Exact two-sided p, for PERFECT separation only (AUROC 0 or 1).

    Under the null all C(n+m, n) label assignments are equally likely and exactly
    one separates completely in each direction. Returns None otherwise — use the
    bootstrap there.
    """
    a = auroc(pos, neg)
    if a not in (0.0, 1.0):
        return None
    return 2.0 / math.comb(len(pos) + len(neg), len(pos))


def oracle_best_threshold(pos: list[float], neg: list[float]):
    """Best balanced accuracy over ALL thresholds AND BOTH polarities.

    Returns ``(best_ba, best_threshold, polarity)`` where polarity is
    ``"ge"`` (positive when score >= t — the direction a gate normally ships) or
    ``"lt"`` (positive when score < t — the INVERTED direction).
    """
    best = (0.0, None, None)
    for t in sorted(set(list(pos) + list(neg))):
        ba_ge = (
            sum(p >= t for p in pos) / len(pos) + sum(n < t for n in neg) / len(neg)
        ) / 2.0
        if ba_ge > best[0]:
            best = (ba_ge, t, "ge")
        ba_lt = (
            sum(p < t for p in pos) / len(pos) + sum(n >= t for n in neg) / len(neg)
        ) / 2.0
        if ba_lt > best[0]:
            best = (ba_lt, t, "lt")
    return best


def deployed_direction_ceiling(pos: list[float], neg: list[float]) -> float:
    """Best balanced accuracy restricted to the ``>=`` direction a gate ships."""
    if not pos or not neg:
        return float("nan")
    return max(
        (sum(p >= t for p in pos) / len(pos) + sum(n < t for n in neg) / len(neg)) / 2.0
        for t in sorted(set(list(pos) + list(neg)))
    )


def summarise(
    label: str,
    pos: list[float],
    neg: list[float],
    pos_name: str = "positive",
    neg_name: str = "negative",
    seed: int = DEFAULT_SEED,
) -> dict:
    """One measure, fully characterised. Picks bootstrap vs exact p correctly."""
    a = auroc(pos, neg)
    ba, t, polarity = oracle_best_threshold(pos, neg)
    rec = {
        "measure": label,
        "n_positive": len(pos),
        "n_negative": len(neg),
        "positive_class": pos_name,
        "negative_class": neg_name,
        "auroc": round(a, 4),
        "auroc_inverted_direction": round(1.0 - a, 4) if a == a else None,
        "oracle_best_balanced_accuracy": round(ba, 4),
        "oracle_best_threshold": round(t, 6) if t is not None else None,
        "oracle_best_polarity": polarity,
        "oracle_best_balanced_accuracy_DEPLOYED_DIRECTION_ONLY": round(
            deployed_direction_ceiling(pos, neg), 4
        ),
    }
    p_exact = exact_permutation_p(pos, neg)
    if p_exact is None:
        lo, hi = bootstrap_ci(pos, neg, seed=seed)
        rec["ci95_bootstrap"] = [round(lo, 4), round(hi, 4)]
        rec["ci95_excludes_chance"] = bool(hi < 0.5 or lo > 0.5)
        rec["exact_permutation_p"] = None
    else:
        rec["ci95_bootstrap"] = None  # degenerate under perfect separation
        rec["ci95_excludes_chance"] = None
        rec["exact_permutation_p"] = p_exact
    return rec


def fmt(rec: dict, indent: str = "    ") -> str:
    """One-line-ish human rendering of a summarise() record."""
    ci = rec["ci95_bootstrap"]
    if ci:
        tail = f"CI95 [{ci[0]:.3f}, {ci[1]:.3f}]" + (
            "" if rec["ci95_excludes_chance"] else " (touches chance)"
        )
    else:
        tail = f"exact p={rec['exact_permutation_p']:.2e} (perfect separation)"
    pol = "" if rec["oracle_best_polarity"] == "ge" else "  <-- INVERTED polarity"
    return (
        f"{indent}{rec['measure']:<44s} n={rec['n_positive']:>2d}/{rec['n_negative']:<2d} "
        f"AUROC={rec['auroc']:.4f}  {tail}\n"
        f"{indent}{'':<44s} ceiling: deployed={rec['oracle_best_balanced_accuracy_DEPLOYED_DIRECTION_ONLY']:.4f} "
        f"both={rec['oracle_best_balanced_accuracy']:.4f}{pol}"
    )


# ------------------------------------------------------- two-sample permutation


def permutation_test_mean_diff(
    a: list[float],
    b: list[float],
    iters: int = DEFAULT_PERM_ITERS,
    seed: int = DEFAULT_SEED,
) -> dict:
    """Two-sided permutation test on |mean(a) - mean(b)|.

    Used for the pilot's BALANCE check, where a NON-significant result is the
    desired outcome: it says the confounder is comparable across the classes the
    design means to separate. A non-significant p is weak evidence of balance,
    never proof of it — so the observed difference is reported alongside, and at
    pilot n the honest reading is the effect size, not the p-value.
    """
    if not a or not b:
        return {"observed_diff": None, "p_two_sided": None, "n_a": len(a), "n_b": len(b)}
    rng = random.Random(seed)
    obs = abs(sum(a) / len(a) - sum(b) / len(b))
    pool = list(a) + list(b)
    na = len(a)
    hits = 0
    for _ in range(iters):
        rng.shuffle(pool)
        d = abs(sum(pool[:na]) / na - sum(pool[na:]) / (len(pool) - na))
        if d >= obs - 1e-15:
            hits += 1
    return {
        "observed_diff": round(obs, 6),
        "p_two_sided": round((hits + 1) / (iters + 1), 5),
        "n_a": len(a),
        "n_b": len(b),
        "mean_a": round(sum(a) / len(a), 6),
        "mean_b": round(sum(b) / len(b), 6),
    }


# ------------------------------------------------------------------------ kappa


def cohens_kappa(rater_a: list[str], rater_b: list[str]) -> dict:
    """Cohen's kappa for two raters over the same items.

    Present so the annotator-agreement step (Gate 3) has a committed
    implementation before the annotator arrives, rather than being improvised
    after the labels land.
    """
    if len(rater_a) != len(rater_b) or not rater_a:
        return {"kappa": None, "n": 0, "note": "unequal or empty"}
    n = len(rater_a)
    cats = sorted(set(rater_a) | set(rater_b))
    observed = sum(x == y for x, y in zip(rater_a, rater_b)) / n
    expected = sum(
        (rater_a.count(c) / n) * (rater_b.count(c) / n) for c in cats
    )
    if expected == 1.0:
        return {"kappa": None, "n": n, "note": "chance agreement is 1.0; kappa undefined"}
    return {
        "kappa": round((observed - expected) / (1 - expected), 4),
        "observed_agreement": round(observed, 4),
        "expected_agreement": round(expected, 4),
        "n": n,
        "categories": cats,
    }


# ------------------------------------------------------------------- self-check


def _self_check() -> None:
    """Verify auroc against a brute-force reference and the known edge cases."""
    rng = random.Random(7)
    for _ in range(200):
        p = [rng.random() for _ in range(rng.randint(2, 9))]
        n = [rng.random() for _ in range(rng.randint(2, 9))]
        ref = sum(
            1.0 if x > y else (0.5 if x == y else 0.0) for x in p for y in n
        ) / (len(p) * len(n))
        assert abs(auroc(p, n) - ref) < 1e-12
    assert auroc([1, 2, 3], [4, 5, 6]) == 0.0
    assert auroc([4, 5, 6], [1, 2, 3]) == 1.0
    assert auroc([1, 1], [1, 1]) == 0.5
    # perfect separation in the inverted direction still has a ceiling of 1.0,
    # reached with polarity "lt" -- the bug this module exists to not repeat.
    ba, _, pol = oracle_best_threshold([1, 2, 3], [4, 5, 6])
    assert ba == 1.0 and pol == "lt", (ba, pol)
    assert abs(deployed_direction_ceiling([1, 2, 3], [4, 5, 6]) - 0.5) < 1e-12
    assert cohens_kappa(["a", "b", "a"], ["a", "b", "a"])["kappa"] == 1.0
    print("harness.lib.stats self-check: PASS")


if __name__ == "__main__":
    _self_check()
