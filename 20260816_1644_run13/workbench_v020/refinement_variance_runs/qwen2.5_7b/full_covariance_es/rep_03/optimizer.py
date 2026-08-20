import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    dim = dim
    low, high = bounds
    population_size = 10
    sigma = 0.1
    lambda_ = 5 * dim
    mu = int(lambda_ / 2)
    alpha = 0.1
    beta = 0.2
    rho = 0.05

    # Initialize population
    X = np.random.uniform(low, high, (population_size, dim))
    F = np.array([f(x) for x in X])

    for generation in range(int(budget)):
        # Select elites
        elites_indices = np.argsort(F)[:mu]
        X_elites = X[elites_indices]
        F_elites = F[elites_indices]

        # Update mean
        mean = np.mean(X_elites, axis=0)

        # Update covariance
        cov = np.cov(X_elites, rowvar=False)
        cov += rho * np.eye(dim)  # Regularization

        # Sample new population
        X_new = np.random.multivariate_normal(mean, cov, lambda_ - mu)
        X_new = np.vstack((X_elites, X_new))

        # Evaluate new population
        F_new = np.array([f(x) for x in X_new])
        F = np.concatenate((F_elites, F_new))

        # Adapt scale
        sigma *= np.exp(alpha * (np.mean(F_elites) - np.mean(F)))

        # Replace population
        X = X_new
        F = F

        if generation % 100 == 0:
            print(f"Generation {generation}, Best score: {np.min(F_elites)}")

    # Return the best solution found
    best_index = np.argmin(F_elites)
    best_solution = X_elites[best_index]
    best_score = F_elites[best_index]

    if generation >= budget - 1:
        raise BudgetExhausted

    return {"solution": best_solution, "score": best_score}
