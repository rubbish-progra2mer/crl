import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    best_x = np.random.uniform(low, high, dim)
    best_f = f(best_x)
    for _ in range(budget - 1):
        try:
            x = np.random.uniform(low, high, dim)
            f_val = f(x)
            if f_val < best_f:
                best_f = f_val
                best_x = x
        except BudgetExhausted:
            break
    return {'x': best_x, 'f': best_f}
