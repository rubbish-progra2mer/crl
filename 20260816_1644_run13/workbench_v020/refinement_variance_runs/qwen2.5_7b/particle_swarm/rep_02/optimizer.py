import random
import numpy as np
from problems import BudgetExhausted

class Particle:
    def __init__(self, dim, bounds):
        self.position = np.random.uniform(bounds[0], bounds[1], dim)
        self.best_position = self.position.copy()
        self.velocity = np.zeros(dim)
        self.best_score = float('inf')

class Optimizer:
    def __init__(self, dim, bounds, inertia_min=0.4, inertia_max=0.9, cognitive=2.0, social=2.0):
        self.dim = dim
        self.bounds = bounds
        self.inertia_min = inertia_min
        self.inertia_max = inertia_max
        self.cognitive = cognitive
        self.social = social
        self.particles = [Particle(dim, bounds) for _ in range(10)]  # 10 particles for this example
        self.global_best_position = np.zeros(dim)
        self.global_best_score = float('inf')

    def optimize(self, f, budget, seed):
        np.random.seed(seed)
        t = 0
        stagnation_counter = 0

        while t < budget:
            for particle in self.particles:
                # Update velocity and position
                for i in range(self.dim):
                    r1, r2 = random.random(), random.random()
                    inertia = self.inertia_min + t * (self.inertia_max - self.inertia_min) / budget
                    particle.velocity[i] = (self.inertia_min + inertia) * particle.velocity[i] + self.cognitive * r1 * (particle.best_position[i] - particle.position[i]) + self.social * r2 * (self.global_best_position[i] - particle.position[i])
                    particle.position[i] += particle.velocity[i]

                    # Bounding the position
                    particle.position[i] = np.clip(particle.position[i], self.bounds[0], self.bounds[1])

                # Evaluate the function
                score = f(particle.position)
                if score < particle.best_score:
                    particle.best_score = score
                    particle.best_position = particle.position.copy()

                # Update global best
                if score < self.global_best_score:
                    self.global_best_score = score
                    self.global_best_position = particle.position.copy()

            # Check for stagnation
            if self.global_best_score == self.particles[0].best_score:
                stagnation_counter += 1
            else:
                stagnation_counter = 0

            if stagnation_counter >= budget // 10:
                # Restart if stagnation persists
                self.restart_particles()
                stagnation_counter = 0

            t += 1

        return {'best_position': self.global_best_position, 'best_score': self.global_best_score}

    def restart_particles(self):
        for particle in self.particles:
            particle.best_position = np.random.uniform(self.bounds[0], self.bounds[1], self.dim)
            particle.best_score = float('inf')
            particle.position = np.random.uniform(self.bounds[0], self.bounds[1], self.dim)
            particle.velocity = np.zeros(self.dim)

def optimize(f, dim, bounds, budget, seed):
    optimizer = Optimizer(dim, bounds)
    try:
        return optimizer.optimize(f, budget, seed)
    except BudgetExhausted:
        return {'best_position': optimizer.global_best_position, 'best_score': optimizer.global_best_score}
