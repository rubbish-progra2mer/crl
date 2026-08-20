import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    x = np.random.uniform(low, high, dim)
    best_x = x
    best_f = f(x)
    step_size = 1.0
    num_evals = 1
    num_success = 0
    num_stagnant = 0
    max_stagnant = 10

    while num_evals < budget:
        try:
            for _ in range(10):
                perturbation = np.random.randn(dim) * step_size
                candidate = x + perturbation
                candidate = np.clip(candidate, low, high)
                candidate_f = f(candidate)
                num_evals += 1
                if candidate_f < best_f:
                    best_f = candidate_f
                    best_x = candidate
                    num_success += 1
                    num_stagnant = 0
                    step_size *= 1.1
                else:
                    num_stagnant += 1
                if num_stagnant >= max_stagnant:
                    step_size *= 0.9
                    num_stagnant = 0
            if num_success > 0:
                x = best_x
                num_success = 0
            else:
                x = np.random.uniform(low, high, dim)
        except BudgetExhausted:
            break

    return {
        'x': best_x,
        'f': best_f,
        'num_evals': num_evals,
        'success': num_success > 0
    }
