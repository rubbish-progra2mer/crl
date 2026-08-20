import math

from bor import QueryRecord, audit
from bor.metrics import random_success_at_least_one


def test_collapse_zone_verdict():
    # Case 2 numbers: N=400k, R=20k (5%), K=100 -> p_rand ~ 0.994
    recs = [QueryRecord(N=400_000, R=20_000, K=100, hit=True) for _ in range(50)]
    result = audit(recs, n_bootstrap=200)
    assert result.p_obs == 1.0
    assert result.p_rand_mean > 0.99
    assert result.frac_collapse_zone == 1.0
    assert "COLLAPSE ZONE" in result.verdict
    assert result.bor < 0.05


def test_selective_verdict_and_ci():
    # Perfect retriever at low density: BoR should equal the ceiling.
    recs = [QueryRecord(N=1_000, R=10, K=10, hit=True) for _ in range(100)]
    result = audit(recs, n_bootstrap=200)
    p_rand = random_success_at_least_one(N=1_000, R=10, K=10)
    assert math.isclose(result.bor, -math.log2(p_rand), rel_tol=1e-9)
    lo, hi = result.bor_ci
    eps = 1e-9
    assert lo - eps <= result.bor <= hi + eps
    assert "SELECTIVE" in result.verdict


def test_at_or_below_random():
    recs = [QueryRecord(N=100, R=10, K=10, hit=(i % 2 == 0)) for i in range(100)]
    # p_obs = 0.5; p_rand for N=100,R=10,K=10 is ~0.67 -> below random
    result = audit(recs, n_bootstrap=200)
    assert result.bor < 0
    assert "AT/BELOW RANDOM" in result.verdict


def test_empty_raises():
    try:
        audit([])
    except ValueError:
        pass
    else:
        raise AssertionError("audit([]) should raise ValueError")


def test_nan_verdict_undefined():
    recs = [QueryRecord(N=50, R=0, K=10, hit=False) for _ in range(20)]
    result = audit(recs, n_bootstrap=50)
    assert math.isnan(result.bor)
    assert "UNDEFINED" in result.verdict


def test_infinite_bor_zero_baseline():
    recs = [QueryRecord(N=50, R=0, K=10, hit=True) for _ in range(20)]
    result = audit(recs, n_bootstrap=50)
    assert math.isinf(result.bor) and result.bor > 0
    assert "unbounded" in result.verdict
