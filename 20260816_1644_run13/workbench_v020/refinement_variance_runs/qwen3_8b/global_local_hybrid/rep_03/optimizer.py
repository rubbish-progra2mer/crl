import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    n_samples = min(100, budget // 2)
    n_local_searches = min(5, budget // 2)
    n_local_steps = min(100, budget // 2)
    best_points = []
    evaluations = 0

    # Initial random sampling
    for _ in range(n_samples):
        if evaluations >= budget:
            raise BudgetExhausted
        x = np.random.uniform(low, high, dim)
        try:
            score = f(x)
            evaluations += 1
            best_points.append((score, x))
        except BudgetExhausted:
            raise

    # Select top candidates for local search
    best_points.sort()
    best_points = best_points[:n_local_searches]

    # Local search from each candidate
    for score, x in best_points:
        if evaluations >= budget:
            raise BudgetExhausted
        for _ in range(n_local_steps):
            if evaluations >= budget:
                raise BudgetExhausted
            step = np.random.normal(0, 0.1, dim)
            new_x = x + step
            new_x = np.clip(new_x, low, high)
            try:
                new_score = f(new_x)
                evaluations += 1
                if new_score < score:
                    x = new_x
                    score = new_score
            except BudgetExhausted:
                raise

    best_score, best_x = min(best_points)
    return {
        'score': best_score,
        'x': best_x,
        'evaluations': evaluations
    }
