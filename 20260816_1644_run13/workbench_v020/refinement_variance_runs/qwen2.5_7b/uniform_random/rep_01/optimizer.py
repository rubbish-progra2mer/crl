import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    best_point = None
    best_value = float('inf')
    evaluations = 0
    
    for _ in range(budget):
        point = np.random.uniform(bounds[0], bounds[1], dim)
        evaluations += 1
        
        try:
            value = f(point)
        except Exception as e:
            raise BudgetExhausted("Evaluation failed") from e
        
        if value < best_value:
            best_value = value
            best_point = point
    
    return {"best_point": best_point, "best_value": best_value, "evaluations": evaluations}
