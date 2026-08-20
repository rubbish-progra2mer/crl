import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    pop_size = min(10, dim + 1)
    pop = np.random.uniform(low, high, (pop_size, dim))
    best = pop[np.random.randint(pop_size)]
    best_f = f(best)
    evals = 1

    def crossover(a, b, target):
        return np.where(np.random.rand(dim) < 0.8, a, b)

    def diversity(pop):
        return np.sum(np.std(pop, axis=0))

    def restart(pop):
        return np.random.uniform(low, high, (pop_size, dim))

    for _ in range(budget - 1):
        if evals >= budget:
            raise BudgetExhausted
        for i in range(pop_size):
            a, b, c = np.random.choice(pop_size, 3, replace=False)
            mutant = pop[a] + 0.5 * (pop[b] - pop[c])
            mutant = np.clip(mutant, low, high)
            trial = crossover(mutant, pop[i], pop[i])
            trial_f = f(trial)
            evals += 1
            if trial_f < f(pop[i]):
                pop[i] = trial
                if trial_f < best_f:
                    best = trial
                    best_f = trial_f
        if diversity(pop) < 0.1:
            pop = restart(pop)
    
    return {
        "best": best.tolist(),
        "best_f": best_f,
        "evaluations": evals
    }
