import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    best_x = None
    best_f = np.inf
    evaluations = 0

    def coordinate_search(x, step_size, max_steps=100):
        nonlocal evaluations
        for _ in range(max_steps):
            if evaluations >= budget:
                raise BudgetExhausted
            for i in range(dim):
                for delta in [-step_size, step_size]:
                    new_x = np.copy(x)
                    new_x[i] += delta
                    if (new_x >= low).all() and (new_x <= high).all():
                        evaluations += 1
                        f_val = f(new_x)
                        if f_val < best_f:
                            best_f = f_val
                            best_x = new_x
                            if f_val < 1e-8:  # Early exit if near minimum
                                return
        return

    for _ in range(10):  # Number of random restarts
        if evaluations >= budget:
            break
        x = np.random.uniform(low, high, dim)
        evaluations += 1
        f_val = f(x)
        if f_val < best_f:
            best_f = f_val
            best_x = x
            if f_val < 1e-8:
                break
        step_size = 0.1
        coordinate_search(x, step_size)
        step_size *= 0.9  # Reduce step size on failure

    return {
        'x': best_x,
        'f': best_f,
        'evaluations': evaluations
    }
