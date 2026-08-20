from bor import bor_success_at_one, collapse_lambda, random_success_at_least_one

N = 400_000
R = 20_000  # 5% money-shaped documents

for K, observed in [(10, 0.82), (100, 1.00)]:
    p_rand = random_success_at_least_one(N=N, R=R, K=K)
    bor = bor_success_at_one(observed=observed, N=N, R=R, K=K)
    lam = collapse_lambda(N=N, R=R, K=K)

    print(f"K={K}")
    print(f"  observed success: {observed:.3f}")
    print(f"  random baseline:  {p_rand:.3f}")
    print(f"  BoR:              {bor:.3f} bits")
    print(f"  lambda:           {lam:.3f}")