import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    pop_size = 10
    elite_frac = 0.2
    sigma = 1.0
    alpha = 0.5
    beta = 0.1
    gamma = 0.01
    lambda_ = 0.1
    mu = 0.01

    # Initialize mean and covariance
    mean = np.random.uniform(low, high, dim)
    cov = np.eye(dim) * sigma

    for step in range(budget):
        try:
            # Sample population
            pop = np.random.multivariate_normal(mean, cov, pop_size)
            pop = np.clip(pop, low, high)
            scores = np.array([f(x) for x in pop])
            elite_idx = np.argsort(scores)[:int(elite_frac * pop_size)]
            elite = pop[elite_idx]
            elite_scores = scores[elite_idx]

            # Update mean
            mean = np.mean(elite, axis=0)

            # Update covariance
            cov = np.cov(elite.T)
            cov = (1 - alpha) * cov + alpha * np.eye(dim)
            cov = np.maximum(cov, np.eye(dim) * 1e-6)

            # Adapt scale
            scale = np.std(elite_scores)
            sigma = sigma * np.exp(beta * (np.log(scale) - np.log(sigma)))

            # Regularize covariance
            cov = (1 - gamma) * cov + gamma * np.eye(dim)

            # Adjust learning rate
            mu = mu * np.exp(lambda_ * (np.log(sigma) - np.log(mu)))

            # Check if we should stop
            if step + 1 >= budget:
                break
        except BudgetExhausted:
            break

    best_idx = np.argmin(scores)
    best_x = pop[best_idx]
    best_score = scores[best_idx]

    return {
        'x': best_x,
        'f': best_score,
        'iterations': step + 1,
        'budget': budget
    }
