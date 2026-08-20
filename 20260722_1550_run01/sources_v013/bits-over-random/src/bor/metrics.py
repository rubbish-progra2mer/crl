from __future__ import annotations

import math


def _check_counts(N: int, R: int, K: int) -> None:
    if N <= 0:
        raise ValueError("N must be positive.")
    if R < 0 or R > N:
        raise ValueError("R must satisfy 0 <= R <= N.")
    if K < 0 or K > N:
        raise ValueError("K must satisfy 0 <= K <= N.")


def _log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def random_success_at_least_one(N: int, R: int, K: int) -> float:
    """Probability that a blind draw of K items hits at least one relevant item."""
    _check_counts(N, R, K)

    if K == 0 or R == 0:
        return 0.0
    if K > N - R:
        return 1.0

    log_no_hit = _log_choose(N - R, K) - _log_choose(N, K)
    return -math.expm1(log_no_hit)


def random_success_at_least_m(N: int, R: int, K: int, m: int) -> float:
    """Probability that a blind draw of K items hits at least m relevant items."""
    _check_counts(N, R, K)

    if m <= 0:
        return 1.0
    if m > R or m > K:
        return 0.0

    upper = min(R, K)
    terms = [
        _log_choose(R, x) + _log_choose(N - R, K - x) - _log_choose(N, K)
        for x in range(m, upper + 1)
    ]

    peak = max(terms)
    return math.exp(peak) * sum(math.exp(t - peak) for t in terms)


def random_recall_baseline(N: int, K: int) -> float:
    """Expected recall from a blind draw of K items."""
    if N <= 0:
        raise ValueError("N must be positive.")
    if K < 0 or K > N:
        raise ValueError("K must satisfy 0 <= K <= N.")
    return K / N


def enrichment_factor(observed: float, random_baseline: float) -> float:
    """Observed success divided by random success."""
    if observed < 0:
        raise ValueError("observed must be non-negative.")
    if random_baseline < 0:
        raise ValueError("random_baseline must be non-negative.")

    if random_baseline == 0:
        if observed == 0:
            return float("nan")
        return float("inf")

    return observed / random_baseline


def bits_over_random(observed: float, random_baseline: float) -> float:
    """log2(observed / random_baseline)."""
    ef = enrichment_factor(observed, random_baseline)

    if ef == 0:
        return float("-inf")
    if math.isnan(ef) or math.isinf(ef):
        return ef

    return math.log2(ef)


def bor_success_at_one(observed: float, N: int, R: int, K: int) -> float:
    """BoR for Success@K where success means at least one relevant item."""
    p_rand = random_success_at_least_one(N=N, R=R, K=K)
    return bits_over_random(observed=observed, random_baseline=p_rand)


def bor_ceiling(random_baseline: float) -> float:
    """Best possible BoR if observed success is 1.0."""
    return bits_over_random(observed=1.0, random_baseline=random_baseline)


def collapse_lambda(N: int, R: int, K: int) -> float:
    """Expected relevant hits under random drawing, K * R / N."""
    _check_counts(N, R, K)
    return K * R / N