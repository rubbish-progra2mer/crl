import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    best_x = np.random.uniform(low, high, dim)
    best_f = float('inf')
    evaluations = 0

    def nelder_mead(f, x0, bounds, max_iter=100, tol=1e-6):
        n = len(x0)
        centroid = np.mean(x0, axis=0)
        reflect = centroid + np.random.uniform(0, 1, n) * (centroid - x0)
        reflect = np.clip(reflect, bounds[0], bounds[1])
        reflect_f = f(reflect)
        nonlocal evaluations
        evaluations += 1

        if reflect_f < f(x0[0]):
            expand = centroid + np.random.uniform(1, 2, n) * (centroid - x0)
            expand = np.clip(expand, bounds[0], bounds[1])
            expand_f = f(expand)
            evaluations += 1
            if expand_f < reflect_f:
                return expand
            else:
                return reflect
        elif reflect_f < f(x0[-1]):
            return reflect
        else:
            contract = centroid + np.random.uniform(0, 0.5, n) * (centroid - x0)
            contract = np.clip(contract, bounds[0], bounds[1])
            contract_f = f(contract)
            evaluations += 1
            if contract_f < f(x0[-1]):
                return contract
            else:
                shrink = np.random.uniform(0, 0.5, n) * (x0[0] - x0[-1]) + x0[-1]
                shrink = np.clip(shrink, bounds[0], bounds[1])
                return shrink

    for _ in range(10):  # 10 restarts
        if evaluations >= budget:
            break
        x = np.random.uniform(bounds[0], bounds[1], dim)
        for _ in range(100):  # 100 iterations per restart
            if evaluations >= budget:
                break
            if evaluations >= budget:
                break
            try:
                x = nelder_mead(f, x, bounds)
                current_f = f(x)
                evaluations += 1
                if current_f < best_f:
                    best_f = current_f
                    best_x = x
            except BudgetExhausted:
                break

    return {'x': best_x, 'f': best_f, 'evaluations': evaluations}
