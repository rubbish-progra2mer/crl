import numpy as np
from random import Random
from copy import deepcopy
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    rng = Random(seed)
    best_x = None
    best_f = float('inf')
    for _ in range(rng.randint(1, 10)):  # Number of restarts
        x0 = [rng.uniform(bounds[0], bounds[1]) for _ in range(dim)]
        simplex = [x0]
        for _ in range(dim):
            x = np.array(x0)
            for i in range(dim):
                if rng.random() < 0.5:
                    x[i] = bounds[0]
                else:
                    x[i] = bounds[1]
            simplex.append(x.tolist())
        
        iter_count = 0
        while iter_count < budget:
            try:
                f_values = [f(x) for x in simplex]
                best_idx = np.argmin(f_values)
                best_f = min(best_f, f_values[best_idx])
                if best_x is None or f_values[best_idx] < f(best_x):
                    best_x = np.array(simplex[best_idx])

                # Reflection
                center = np.mean([simplex[i] for i in range(dim) if i != best_idx], axis=0)
                reflected = (1 + rng.random()) * center - simplex[best_idx]
                reflected_f = f(reflected)
                if reflected_f < f_values[best_idx] and reflected_f < f(simplex[best_idx]):
                    simplex[best_idx] = reflected.tolist()
                    continue

                # Expansion
                if reflected_f < f_values[0]:
                    expanded = 2 * reflected - simplex[best_idx]
                    expanded_f = f(expanded)
                    if expanded_f < reflected_f:
                        simplex[best_idx] = expanded.tolist()
                    else:
                        simplex[best_idx] = reflected.tolist()
                    continue

                # Contraction
                if np.any([f(x) < reflected_f for x in simplex if x != simplex[best_idx]]):
                    contracted = 0.5 * (center - simplex[best_idx])
                    contracted_f = f(contracted)
                    if contracted_f < reflected_f:
                        simplex[best_idx] = contracted.tolist()
                    else:
                        # Shrink
                        for i in range(dim):
                            simplex[i] = (1 - rng.random()) * simplex[i] + rng.random() * simplex[best_idx]
                else:
                    # Shrink
                    for i in range(dim):
                        simplex[i] = (1 - rng.random()) * simplex[i] + rng.random() * simplex[best_idx]

                iter_count += 1
            except BudgetExhausted:
                break

    return {'x': best_x, 'f': best_f}

if __name__ == "__main__":
    def test_f(x):
        return sum(x**2)

    result = optimize(test_f, 5, (-5, 5), 100, 42)
    print(result)
