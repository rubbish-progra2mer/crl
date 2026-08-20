from __future__ import annotations

import math
import random as _random
from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence, Tuple

from .metrics import (
    bits_over_random,
    bor_ceiling,
    collapse_lambda,
    random_success_at_least_m,
    random_success_at_least_one,
)


@dataclass
class QueryRecord:
    """One retrieval event mined from a log.

    N is the pool size at query time, R the relevant count in the pool,
    K the depth used, and hit whether success occurred at that depth.
    m generalizes success to "at least m relevant items" (default 1).
    """

    N: int
    R: int
    K: int
    hit: bool
    m: int = 1
    qid: Optional[str] = None
    scores: Optional[Sequence[float]] = None

    @property
    def p_rand(self) -> float:
        if self.m <= 1:
            return random_success_at_least_one(N=self.N, R=self.R, K=self.K)
        return random_success_at_least_m(N=self.N, R=self.R, K=self.K, m=self.m)

    @property
    def lam(self) -> float:
        return collapse_lambda(N=self.N, R=self.R, K=self.K)


@dataclass
class AuditResult:
    """Aggregate chance-corrected audit over many QueryRecords."""

    n_queries: int
    p_obs: float
    p_rand_mean: float
    bor: float
    bor_ci: Tuple[float, float]
    bor_ceiling_mean: float
    lambda_mean: float
    frac_collapse_zone: float
    verdict: str
    per_query: list = field(default_factory=list, repr=False)

    def summary(self) -> str:
        lo, hi = self.bor_ci
        return "\n".join(
            [
                "BoR Audit",
                "=" * 58,
                f"queries analyzed          : {self.n_queries}",
                f"observed success (P_obs)  : {self.p_obs:.4f}",
                f"random baseline (P_rand)  : {self.p_rand_mean:.4f}",
                f"Bits-over-Random          : {self.bor:+.4f}  "
                f"[95% CI {lo:+.4f}, {hi:+.4f}]",
                f"BoR ceiling (mean)        : {self.bor_ceiling_mean:.4f}",
                f"lambda (mean)             : {self.lambda_mean:.4f}",
                f"collapse-zone queries     : {self.frac_collapse_zone:.0%}",
                "-" * 58,
                self.verdict,
            ]
        )


def audit(
    records: Iterable[QueryRecord],
    n_bootstrap: int = 2000,
    seed: int = 0,
) -> AuditResult:
    """Audit a log of retrieval events against their blind-draw baselines.

    P_obs is the mean hit rate, P_rand the mean per-query random baseline,
    and BoR = bits_over_random(P_obs, P_rand). The 95% CI is a bootstrap
    over queries.
    """
    recs = list(records)
    if not recs:
        raise ValueError("No query records to audit.")

    p_obs = sum(1 for q in recs if q.hit) / len(recs)
    p_rand_vals = [q.p_rand for q in recs]
    p_rand_mean = sum(p_rand_vals) / len(p_rand_vals)
    lambda_mean = sum(q.lam for q in recs) / len(recs)

    ceilings = [bor_ceiling(p) for p in p_rand_vals]
    finite = [c for c in ceilings if math.isfinite(c)]
    ceiling_mean = sum(finite) / len(finite) if finite else float("inf")

    frac_zone = sum(1 for p in p_rand_vals if p >= 0.95) / len(p_rand_vals)
    bor = bits_over_random(observed=p_obs, random_baseline=p_rand_mean)

    rng = _random.Random(seed)
    n = len(recs)
    boot = []
    for _ in range(n_bootstrap):
        s_hits = 0
        s_pr = 0.0
        for _ in range(n):
            q = recs[rng.randrange(n)]
            s_hits += q.hit
            s_pr += q.p_rand
        boot.append(
            bits_over_random(observed=s_hits / n, random_baseline=s_pr / n)
        )
    boot.sort()
    ci = (boot[int(0.025 * n_bootstrap)], boot[min(int(0.975 * n_bootstrap), n_bootstrap - 1)])

    return AuditResult(
        n_queries=n,
        p_obs=p_obs,
        p_rand_mean=p_rand_mean,
        bor=bor,
        bor_ci=ci,
        bor_ceiling_mean=ceiling_mean,
        lambda_mean=lambda_mean,
        frac_collapse_zone=frac_zone,
        verdict=_verdict(bor, p_obs, p_rand_mean, frac_zone),
        per_query=recs,
    )


def _verdict(bor: float, p_obs: float, p_rand: float, frac_zone: float) -> str:
    if frac_zone >= 0.5:
        return (
            f"COLLAPSE ZONE: {frac_zone:.0%} of queries have a random "
            f"baseline at or above 95%. Observed success ({p_obs:.0%}) is "
            f"mostly base rate; a blind draw scores {p_rand:.0%} here. "
            f"Reduce K or the success metric is decorative."
        )
    if math.isnan(bor):
        return (
            f"UNDEFINED: observed {p_obs:.0%} against a random baseline "
            f"of {p_rand:.0%}. The ratio carries no information either way."
        )
    if math.isinf(bor) and bor > 0:
        return (
            f"SELECTIVE: observed {p_obs:.0%} where the random baseline "
            f"is zero. Any success here is above chance and the bits are "
            f"unbounded."
        )
    if bor <= 0.0:
        return (
            f"AT/BELOW RANDOM: observed {p_obs:.0%} against a blind-draw "
            f"baseline of {p_rand:.0%}. No selectivity at this depth."
        )
    if bor < 1.0:
        return (
            f"WEAK: {bor:.2f} bits over random. Real but thin: less than "
            f"one doubling over blind luck."
        )
    return (
        f"SELECTIVE: {bor:.2f} bits over random, about {2 ** bor:.1f}x "
        f"better than a blind draw at this depth."
    )
