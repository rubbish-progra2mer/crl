import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    best_x = np.random.uniform(low, high, dim)
    best_f = float('inf')
    evaluations = 0

    def coordinate_search(x, step_size):
        nonlocal evaluations
        for i in range(dim):
            for delta in (-1, 1):
                new_x = x.copy()
                new_x[i] += delta * step_size
                if (new_x >= low).all() and (new_x <= high).all():
                    evaluations += 1
                    if evaluations >= budget:
                        raise BudgetExhausted
                    f_val = f(new_x)
                    if f_val < best_f:
                        best_f = f_val
                        best_x = new_x
        return best_f

    step_size = 1.0
    for _ in range(budget // 10):
        try:
            x = np.random.uniform(low, high, dim)
            evaluations += 1
            if evaluations >= budget:
                raise BudgetExhausted
            f_val = f(x)
            if f_val < best_f:
                best_f = f_val
                best_x = x
            coordinate_search(x, step_size)
            step_size *= 0.9
        except BudgetExhausted:
            break

    return {
        'x': best_x,
        'f': best_f,
        'evaluations': evaluations,
        'budget': budget
    }
