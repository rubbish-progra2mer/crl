import random
import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    best_point = None
    best_value = float('inf')
    
    for _ in range(budget):
        # Generate a random point within the given bounds
        point = np.random.uniform(bounds[0], bounds[1], dim)
        
        try:
            # Evaluate the function at the random point
            value = f(point)
        except Exception as e:
            raise BudgetExhausted("Evaluation failed: " + str(e))
        
        # Update the best point if the new value is better
        if value < best_value:
            best_value = value
            best_point = point
    
    # Return the best point found
    return {'x': best_point.tolist(), 'value': best_value}
