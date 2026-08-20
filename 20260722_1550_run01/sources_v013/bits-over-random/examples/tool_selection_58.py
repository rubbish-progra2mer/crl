from bor import bor_ceiling, collapse_lambda, random_success_at_least_one

N = 58
R = 4  # typical relevant tools for a task

for K in [5, 20, 58]:
    p_rand = random_success_at_least_one(N=N, R=R, K=K)
    ceiling = bor_ceiling(p_rand)
    lam = collapse_lambda(N=N, R=R, K=K)

    print(f"K={K}")
    print(f"  random baseline: {p_rand:.3f}")
    print(f"  BoR ceiling:     {ceiling:.3f} bits")
    print(f"  lambda:          {lam:.3f}")