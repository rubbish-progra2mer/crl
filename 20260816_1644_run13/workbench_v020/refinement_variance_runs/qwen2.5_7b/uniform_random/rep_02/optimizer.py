import numpy as np
from problems import BudgetExhausted


def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    
    low, high = bounds
    best_point = None
    best_value = float('inf')
    
    for _ in range(budget):
        point = np.random.uniform(low, high, dim)
        value = f(point)
        
        if value < best_value:
            best_value = value
            best_point = point
    
    return {'best_point': best_point, 'best_value': best_value}
