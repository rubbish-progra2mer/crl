import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    pop_size = min(10, dim + 1)
    pop = np.random.uniform(low, high, (pop_size, dim))
    best = pop[np.random.randint(pop_size)]
    evals = 0

    def crossover(a, b, c):
        return np.where(np.random.rand(dim) < 0.9, c, a)

    def mutate(a, b, c):
        return a + np.random.rand() * (b - c)

    def restart():
        nonlocal pop, best
        pop = np.random.uniform(low, high, (pop_size, dim))
        best = pop[np.random.randint(pop_size)]

    for _ in range(budget):
        if evals >= budget:
            raise BudgetExhausted
        for i in range(pop_size):
            a, b, c = np.random.choice(pop, 3, replace=False)
            mutant = mutate(a, b, c)
            trial = crossover(mutant, best, a)
            trial = np.clip(trial, low, high)
            trial_score = f(trial)
            evals += 1
            if trial_score < f(best):
                best = trial
        if np.random.rand() < 0.1:
            restart()
    return {'solution': best, 'score': f(best)}
