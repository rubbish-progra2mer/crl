import numpy as np
from numpy.random import default_rng
from problems import BudgetExhausted

# Constants
MU = 5  # Number of parents
LAMBDA = 10  # Number of offspring
SIGMA_INIT = 0.1  # Initial standard deviation
SIGMA_MAX = 1.0  # Maximum standard deviation
SIGMA_MIN = 0.01  # Minimum standard deviation
REGULARIZATION = 1e-6  # Regularization term

class FullCovarianceESOptimizer:
    def __init__(self, dim, bounds, sigma=SIGMA_INIT):
        self.dim = dim
        self.bounds = bounds
        self.sigma = sigma
        self.mean = np.zeros(dim)
        self.cov = np.eye(dim) * sigma**2

    def sample_population(self):
        rng = default_rng()
        return rng.multivariate_normal(self.mean, self.cov, size=LAMBDA)

    def update_elites(self, population, fitness_scores):
        elites = population[np.argsort(fitness_scores)[:MU]]
        self.mean = np.mean(elites, axis=0)
        self.cov = np.cov(elites, rowvar=False) + REGULARIZATION * np.eye(self.dim)

    def adapt_scale(self):
        self.sigma *= 1.05 if np.all(self.cov > 0) else 0.95

    def optimize(self, f, budget):
        population = self.sample_population()
        fitness_scores = np.array([f(individual) for individual in population])
        best_index = np.argmin(fitness_scores)
        best_fitness = fitness_scores[best_index]
        best_individual = population[best_index]

        for _ in range(budget):
            population = self.sample_population()
            fitness_scores = np.array([f(individual) for individual in population])
            best_index = np.argmin(fitness_scores)
            best_fitness = min(best_fitness, fitness_scores[best_index])
            best_individual = population[best_index]

            self.update_elites(population, fitness_scores)
            self.adapt_scale()

        return {'best_fitness': best_fitness, 'best_individual': best_individual}

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    optimizer = FullCovarianceESOptimizer(dim, bounds)
    try:
        result = optimizer.optimize(f, budget)
    except BudgetExhausted:
        raise
    return result
