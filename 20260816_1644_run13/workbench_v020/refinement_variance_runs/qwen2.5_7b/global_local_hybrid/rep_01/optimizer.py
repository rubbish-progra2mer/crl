import numpy as np
from problems import BudgetExhausted


def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    best_solution = None
    best_score = float('inf')
    local_searches = 3
    global_sampling_budget = int(budget * 0.8)
    local_search_budget = budget - global_sampling_budget

    # Global sampling phase
    for _ in range(global_sampling_budget):
        candidate = np.random.uniform(low, high, dim)
        score = f(candidate)
        if score < best_score:
            best_solution = candidate
            best_score = score

    # Local search phase
    for _ in range(local_searches):
        candidate = np.random.uniform(low, high, dim)
        if candidate not in [best_solution]:
            for _ in range(local_search_budget // local_searches):
                candidate = np.clip(candidate + np.random.normal(0, 0.1, dim), low, high)
                score = f(candidate)
                if score < best_score:
                    best_solution = candidate
                    best_score = score

    if best_solution is None:
        raise BudgetExhausted("No solution found within the budget.")

    return {"solution": best_solution, "score": best_score}
