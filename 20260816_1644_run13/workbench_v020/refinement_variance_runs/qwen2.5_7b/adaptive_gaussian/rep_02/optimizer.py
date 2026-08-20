import numpy as np
from problems import BudgetExhausted

class AdaptiveGaussianOptimizer:
    def __init__(self, dim, bounds, seed=0):
        self.dim = dim
        self.bounds = bounds
        self.seed = seed
        np.random.seed(seed)
        self.incumbent = np.random.uniform(bounds[0], bounds[1], dim)
        self.best_fval = float('inf')
        self.best_x = self.incumbent.copy()
        self.step_size = 0.1 * (bounds[1] - bounds[0])
        self.success_count = 0
        self.stagnation_count = 0
        self.stagnation_threshold = 10
        self.evaluations = 0

    def optimize(self, f, budget):
        self.evaluations = 0
        while self.evaluations < budget:
            candidate = self.incumbent + self.step_size * np.random.randn(self.dim)
            candidate = np.clip(candidate, self.bounds[0], self.bounds[1])
            fval = f(candidate)
            self.evaluations += 1

            if fval < self.best_fval:
                self.best_fval = fval
                self.best_x = candidate.copy()
                self.incumbent = candidate.copy()
                self.success_count += 1
                self.stagnation_count = 0
                self.step_size *= 1.1
            else:
                self.success_count = 0
                self.stagnation_count += 1
                self.step_size *= 0.9

            if self.stagnation_count >= self.stagnation_threshold:
                self.incumbent = np.random.uniform(self.bounds[0], self.bounds[1], self.dim)
                self.best_fval = float('inf')
                self.best_x = self.incumbent.copy()
                self.success_count = 0
                self.stagnation_count = 0

        return {'x': self.best_x, 'fval': self.best_fval, 'evaluations': self.evaluations}

def optimize(f, dim, bounds, budget, seed):
    optimizer = AdaptiveGaussianOptimizer(dim, bounds, seed)
    return optimizer.optimize(f, budget)
