import math

from bor import (
    bits_over_random,
    collapse_lambda,
    random_recall_baseline,
    random_success_at_least_one,
)


def test_random_success_zero_when_k_zero():
    assert random_success_at_least_one(N=100, R=10, K=0) == 0.0


def test_random_success_one_when_k_covers_all_irrelevant_plus_one():
    assert random_success_at_least_one(N=100, R=10, K=91) == 1.0


def test_observed_equals_random_has_zero_bor():
    assert bits_over_random(0.25, 0.25) == 0.0


def test_recall_baseline_is_k_over_n():
    assert random_recall_baseline(N=100, K=10) == 0.1


def test_case2_numbers_are_close():
    p10 = random_success_at_least_one(N=400_000, R=20_000, K=10)
    p100 = random_success_at_least_one(N=400_000, R=20_000, K=100)

    assert math.isclose(p10, 0.401, abs_tol=0.002)
    assert math.isclose(p100, 0.994, abs_tol=0.002)


def test_lambda():
    assert collapse_lambda(N=400_000, R=20_000, K=100) == 5.0