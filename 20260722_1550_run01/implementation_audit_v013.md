# v013 Main-Codex Implementation Audit

## Scope

The main Codex personally reviewed:

- `implementation_v013/audit.py`
- `implementation_v013/independent_audit.py`
- `implementation_v013/test_metric_logic.py`
- the fixed target notebook's BM25 cell;
- the fixed `rank-bm25==0.2.2` wheel source;
- the fixed official `bits-over-random` metric implementation.

This audit authorizes freezing an Experiment Plan. It does not report a Development result and does not authorize Confirmation, Reviewers, or Delivery.

## Frozen implementation identities at audit time

| Artifact | Lines / bytes | SHA-256 |
|---|---:|---|
| `implementation_v013/audit.py` | 814 lines | `EA92265ABF4B6D2FE8B6838F424B17E383F8361C0FC65658FE25FCC96B82F9E8` |
| `implementation_v013/independent_audit.py` | 436 lines | `990A33893A98AF7C4996D89A754CB67861729840E729C8A424E382CA3E1212DE` |
| `implementation_v013/test_metric_logic.py` | 48 lines | `9AE5104A273C9045C33B7E420B5DFA5444E7C289911C7CFAE1D78D6A6EC78CFD` |
| `sources_v013/dependencies/rank_bm25-0.2.2-py3-none-any.whl` | 8,584 bytes | `7BD4A95571ADADFC271746FA146A4BCFD89C0CF731E49C3D1AD863290ADBE8AE` |

## Faithfulness audit

The implementation matches the fixed official BM25 cell on:

- query extraction from `question[0]`;
- first-function tool identity;
- tool description construction from name, description, and property names;
- insertion-ordered registry;
- lowercase whitespace tokenization;
- `rank-bm25` 0.2.2 `BM25Okapi`;
- stable descending score sort;
- one shuffle with seed `42`;
- `70/30` train/test split;
- maximum depth `min(N, 100)`;
- state vector and seven normalizations;
- DQN shape `7 → 64 → 64 → 2`;
- replay size `20,000`, batch `64`, Adam learning rate `1e-3`, gamma `0.95`;
- terminal BoR and F1 rewards;
- intermediate step cost `0.005`;
- epsilon schedule `0.5 → 0.1 → 0.03`;
- target update every 500 episodes;
- `15,000` episodes;
- seeds `42`, `123`, and `456`;
- fixed K values `1, 3, 5, 10, 20, 50`.

The author notebook evaluates each deterministic trained policy five identical times. The v013 implementation freezes one row per query/policy/seed instead; this removes duplicate identical rows without changing any mean, standard deviation over query rows, or policy ordering.

## Metric audit design

- `audit.py` writes raw query-level rows before aggregate interpretation.
- It computes the notebook statistic and paper-defined aggregate from the same rows.
- It freezes trained state dictionaries for possible untouched Confirmation.
- `independent_audit.py` does not import metric aggregation code from `audit.py`.
- The independent entry point recomputes hit validity, reward identity, group metrics, pairwise reversals, maxima, reproduction tolerances, and the paired fixed-K bootstrap.
- It separately imports `bits_over_random` from the fixed official repository and compares that value against the direct aggregate formula.
- Its output explicitly states that mechanical checks do not authorize scientific promotion.

## Side-effect audit

Static search found:

- no network client;
- no subprocess or package installer;
- no deletion, rename, or replacement operation;
- no Reviewer, Decision, Delivery, or system-status write;
- output writes are limited to the caller-provided experiment directory and independent report path;
- model loading for Confirmation requires an explicit frozen model directory.

The shared environment remains unchanged. The fixed BM25 wheel is loaded directly from the Run source directory.

## Executed checks

1. Formula tests:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe -m pytest -q implementation_v013/test_metric_logic.py
exit code: 0
result: 2 passed in 1.39s
```

2. Syntax compilation:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe -m py_compile implementation_v013/audit.py implementation_v013/independent_audit.py
exit code: 0
```

3. Fixed official metric import:

```text
bits_over_random(observed=0.6, random_baseline=1/370)
exit code: 0
observed: 7.794415866350106
```

Generated `__pycache__` and `.pyc` files were removed after the checks. A recursive read-only scan then found none in the Run.

## Residual risks accepted before Development

- PyTorch version and CPU numerical behavior can shift learned policy means relative to the author's Colab, so the Plan uses prospectively fixed reproduction tolerances.
- The source notebook does not pin the `rank-bm25` version. v013 fixes the latest published version used by the package name at selection time, `0.2.2`, and records its wheel hash.
- Development is exposed replication data; untouched evidentiary weight must come from the prospectively fixed BFCL v4 file.
- The scripts compute mechanical gate fields, but the main Codex must read raw rows and decide whether any apparent reversal supports the bounded claim.

## Audit conclusion

The implementation is specific to the v013 experiment, changes no CRL infrastructure, and contains no automated scientific promotion path. It is sufficiently faithful and auditable to freeze exactly one Development Plan.
