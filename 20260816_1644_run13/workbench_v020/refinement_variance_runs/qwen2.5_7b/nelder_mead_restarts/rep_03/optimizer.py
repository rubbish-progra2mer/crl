import numpy as np
from random import Random
from copy import deepcopy

class BudgetExhausted(Exception):
    pass

def optimize(f, dim, bounds, budget, seed):
    rng = Random(seed)
    x = rng.uniform(bounds[0], bounds[1], dim)
    simplex = [deepcopy(x) for _ in range(dim + 1)]
    for i in range(dim + 1):
        simplex[i] += rng.uniform(-1e-6, 1e-6)  # Perturb each point slightly

    reflections = []
    expansions = []
    contractions = []
    shrinks = []

    for _ in range(budget):
        values = [f(s) for s in simplex]
        indices = np.argsort(values)
        best, worst = simplex[indices[0]], simplex[indices[-1]]

        # Center of simplex without the worst point
        center = np.mean(simplex[:dim], axis=0)

        # Reflection
        reflection = 2 * center - worst
        reflections.append(reflection)
        if f(reflection) < values[indices[1]]:
            simplex[-1] = reflection
            continue

        # Expansion
        expansion = 2 * reflection - worst
        expansions.append(expansion)
        if f(expansion) < f(reflection):
            simplex[-1] = expansion
            continue

        # Contraction
        contraction = 2 * center - worst
        contractions.append(contraction)
        if f(contraction) < values[indices[-1]]:
            simplex[-1] = contraction
            continue

        # Shrink
        for i in range(dim):
            simplex[i] = (simplex[i] + worst) / 2
        shrinks.append(simplex[i])

    # Best solution found
    return {'solution': best, 'function_value': f(best)}

# Example usage
if __name__ == "__main__":
    def black_box_function(x):
        return sum(xi**2 for xi in x)

    result = optimize(black_box_function, 5, (-5.0, 5.0), 100, seed=42)
    print(result)
