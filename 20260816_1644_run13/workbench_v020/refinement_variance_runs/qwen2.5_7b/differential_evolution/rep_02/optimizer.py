import numpy as np
from random import Random
from copy import deepcopy

class BudgetExhausted(Exception):
    pass

def optimize(f, dim, bounds, budget, seed):
    rng = Random(seed)
    population_size = 10
    mutation_factor = 0.8
    crossover_probability = 0.9
    restart_threshold = 50
    restart_budget = 10

    # Initialize population
    population = np.array([rng.uniform(bounds[0], bounds[1], dim) for _ in range(population_size)])
    fitness = np.array([f(x) for x in population])

    # Main loop
    for evals in range(budget):
        # Mutation
        new_population = np.zeros_like(population)
        for i in range(population_size):
            a, b, c = sorted(rng.sample(range(population_size), 3))
            new_population[i] = population[a] + mutation_factor * (population[b] - population[c])

        # Crossover
        for i in range(population_size):
            if rng.random() < crossover_probability:
                for j in range(dim):
                    if rng.random() < 0.5:
                        new_population[i][j] = population[i][j]

        # Selection
        for i in range(population_size):
            if f(new_population[i]) < fitness[i]:
                population[i] = new_population[i]
                fitness[i] = f(new_population[i])

        # Diversity-preserving restart
        if evals % restart_threshold == 0:
            if np.random.rand() < 0.1:
                population = np.array([rng.uniform(bounds[0], bounds[1], dim) for _ in range(population_size)])
                fitness = np.array([f(x) for x in population])

        if evals == budget - 1:
            raise BudgetExhausted("Budget exhausted")

    # Find the best solution
    best_index = np.argmin(fitness)
    return {"solution": population[best_index].tolist(), "fitness": fitness[best_index]}
