import numpy as np
from problems import BudgetExhausted

def optimize(f, dim, bounds, budget, seed):
    np.random.seed(seed)
    low, high = bounds
    n_points = min(20, budget // 2)
    samples = np.random.uniform(low, high, (n_points, dim))
    scores = np.array([f(x) for x in samples])
    best_idx = np.argmin(scores)
    best_point = samples[best_idx]
    best_score = scores[best_idx]
    
    remaining = budget - n_points
    if remaining <= 0:
        return {'best_score': best_score, 'best_point': best_point.tolist(), 'evaluations': n_points}
    
    local_steps = min(5, remaining // 2)
    local_points = []
    for _ in range(local_steps):
        if remaining <= 0:
            break
        idx = np.random.choice(n_points)
        x = samples[idx] + np.random.normal(0, 0.1, dim)
        x = np.clip(x, low, high)
        local_points.append(x)
        remaining -= 1
    
    local_scores = []
    for x in local_points:
        try:
            local_scores.append(f(x))
        except BudgetExhausted:
            break
    
    all_points = np.vstack([samples, np.array(local_points)])
    all_scores = np.hstack([scores, np.array(local_scores)])
    best_idx = np.argmin(all_scores)
    best_point = all_points[best_idx]
    best_score = all_scores[best_idx]
    total_evaluations = n_points + len(local_scores)
    
    return {'best_score': best_score, 'best_point': best_point.tolist(), 'evaluations': total_evaluations}
