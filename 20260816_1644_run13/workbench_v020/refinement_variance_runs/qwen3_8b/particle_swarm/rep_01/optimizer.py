import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    particles = np.random.uniform(low, high, (dim,))  # Initial position
    velocities = np.random.uniform(-1, 1, (dim,))
    personal_best = particles.copy()
    global_best = particles.copy()
    best_score = float('inf')
    inertia = 0.9
    inertia_decay = 0.995
    cognitive = 1.5
    social = 1.5
    stagnation_threshold = 10
    stagnation_count = 0

    for step in range(budget):
        try:
            for i in range(dim):
                # Update velocity
                r1 = np.random.rand()
                r2 = np.random.rand()
                velocities[i] = inertia * velocities[i] + cognitive * r1 * (personal_best[i] - particles[i]) + social * r2 * (global_best - particles[i])
                # Update position
                particles[i] += velocities[i]
                # Ensure position is within bounds
                particles[i] = np.clip(particles[i], low, high)
            # Evaluate new position
            current_score = f(particles)
            # Update personal best
            if current_score < f(personal_best):
                personal_best = particles.copy()
            # Update global best
            if current_score < best_score:
                best_score = current_score
                global_best = particles.copy()
                stagnation_count = 0
            else:
                stagnation_count += 1
            # Decay inertia
            inertia *= inertia_decay
            if stagnation_count >= stagnation_threshold:
                # Restart by reinitializing particles
                particles = np.random.uniform(low, high, (dim,))
                velocities = np.random.uniform(-1, 1, (dim,))
                personal_best = particles.copy()
                global_best = particles.copy()
                best_score = float('inf')
                stagnation_count = 0
        except BudgetExhausted:
            break

    result = {
        'best_position': global_best,
        'best_score': best_score
    }
    return result
