import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    best_x = None
    best_fval = float('inf')
    num_evals = 0

    for _ in range(10):  # Number of restarts
        x = np.random.uniform(bounds[0], bounds[1], dim)
        step_size = 0.1
        num_evals_this_restart = 0

        for i in range(dim):
            x_best = x.copy()
            fval_best = f(x)
            num_evals_this_restart += 1
            num_evals += 1

            for sign in [-1, 1]:
                x[i] += sign * step_size
                fval = f(x)
                num_evals_this_restart += 1
                num_evals += 1

                if fval < fval_best:
                    x_best[i] = x[i]
                    fval_best = fval

            if fval_best < best_fval:
                best_fval = fval_best
                best_x = x_best
                num_evals_this_restart = 0  # Reset counter if a better solution is found

            # Reduce step size if no improvement
            if num_evals_this_restart == 10:
                step_size *= 0.5
                num_evals_this_restart = 0

            if num_evals >= budget:
                raise BudgetExhausted()

    return {'x': best_x, 'fval': best_fval}
