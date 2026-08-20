import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    inertia = 0.9
    inertia_decay = 0.995
    cognitive = 1.5
    social = 1.5
    particles = 20
    max_iter = 100
    stagnation = 10

    # Initialize particles
    positions = np.random.uniform(low, high, (particles, dim))
    velocities = np.random.uniform(-1, 1, (particles, dim))
    personal_best = positions.copy()
    personal_best_scores = np.array([f(pos) for pos in positions])
    global_best = positions[np.argmin(personal_best_scores)]
    global_best_score = np.min(personal_best_scores)
    evaluations = 0

    for iter in range(max_iter):
        if evaluations >= budget:
            raise BudgetExhausted()
        for i in range(particles):
            if evaluations >= budget:
                raise BudgetExhausted()
            r1 = np.random.rand(dim)
            r2 = np.random.rand(dim)
            velocities[i] = inertia * velocities[i] + cognitive * r1 * (personal_best[i] - positions[i]) + social * r2 * (global_best - positions[i])
            positions[i] = np.clip(positions[i] + velocities[i], low, high)
            score = f(positions[i])
            evaluations += 1
            if score < personal_best_scores[i]:
                personal_best[i] = positions[i]
                personal_best_scores[i] = score
                if score < global_best_score:
                    global_best = positions[i]
                    global_best_score = score
        if evaluations >= budget:
            raise BudgetExhausted()
        if np.all(np.abs(personal_best_scores - np.min(personal_best_scores)) < 1e-6):
            stagnation_count = 0
        else:
            stagnation_count += 1
        if stagnation_count >= stagnation:
            # Restart
            positions = np.random.uniform(low, high, (particles, dim))
            velocities = np.random.uniform(-1, 1, (particles, dim))
            personal_best = positions.copy()
            personal_best_scores = np.array([f(pos) for pos in positions])
            global_best = positions[np.argmin(personal_best_scores)]
            global_best_score = np.min(personal_best_scores)
            stagnation_count = 0

    result = {
        'position': global_best,
        'score': global_best_score,
        'evaluations': evaluations
    }
    return result
