from __future__ import annotations

import math

import numpy as np
import torch

from program import (
    state_vector,
    target_terminal_reward,
    terminal_utility,
    updated_coverage_dual,
    updated_ratio,
)


def test_state_has_no_gold_dependent_feature() -> None:
    scores = np.asarray([3.0, 2.0, 1.0], dtype=np.float32)
    first = {"scores": scores, "n": 3, "gold_rank": 1}
    second = {"scores": scores, "n": 3, "gold_rank": 3}
    assert np.array_equal(state_vector(first, 2), state_vector(second, 2))


def test_target_rewards_match_official_equations() -> None:
    assert target_terminal_reward("target_bor_dqn", 1.0, 2, 0.25) == 2.0
    assert target_terminal_reward("target_bor_dqn", 0.0, 2, 0.25) == 0.0
    assert target_terminal_reward("target_f1_dqn", 1.0, 3, 0.25) == 0.5


def test_candidate_and_ratio_utilities() -> None:
    hit = torch.tensor([1.0, 0.0])
    chance = torch.tensor([0.1, 0.2])
    depth = torch.tensor([1.0, 2.0])
    candidate = terminal_utility(
        "coverage_constrained_chance_dqn", hit, chance, depth, 0.5
    )
    ratio = terminal_utility("unconstrained_ratio_dqn", hit, chance, depth, 4.0)
    assert torch.allclose(candidate, torch.tensor([0.4, -0.2]))
    assert torch.allclose(ratio, torch.tensor([0.6, -0.8]))


def test_controller_updates() -> None:
    assert math.isclose(updated_coverage_dual(0.05, 0.8, 0.9, 0.1, 1.0), 0.06)
    assert updated_coverage_dual(0.0, 1.0, 0.9, 0.1, 1.0) == 0.0
    assert math.isclose(updated_ratio(0.8, 0.1), 8.0)
