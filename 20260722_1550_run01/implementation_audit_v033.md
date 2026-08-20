# v033 Main-Codex Implementation Audit

Disposition: `READY_TO_FREEZE_ONE_SHOT_DEVELOPMENT`.

No subagent or Reviewer participated. No v033 scientific metric has been
computed.

## Execution-only lineage

v032 was not executed. Its Plan contained one unresolved explanatory count and
was frozen as a preparation failure before any capture or output path existed.

v033 preserves the v032 scientific design and exact executable code:

- program SHA-256
  `4875b8c7ecde6772fa25e8b86587fe6d59f210a5505763a8ebc38fb4f2a3cc39`;
- independent auditor SHA-256
  `7a0055e44f84eae95d9a185d00b904f2a5439c1392f185bfeceb1f1cd39c9067`;
- test SHA-256
  `56fc6c5c89be3d8cda5c00bb3bd654d170d055e7ae7dd9efb92c4aba956d37c7`.

Only the config experiment identity and Candidate SHA binding changed. Ridge
alpha, SVD dimension/iterations, seed, vocabulary, folds, controls, gates,
datasets and source manifests are unchanged.

## Rechecked implementation

I re-read the complete v033 Candidate, Research Map, config, program and
auditor. The following invariants remain true:

- all nine OOF bundles exclude the complete target generator and held-out task
  fold;
- the shared latent representation uses training text without labels;
- `successful_map` receives only `target=0` rows with total sample weight one
  per task;
- `all_map` uses all training rows with the same per-task normalization;
- the Candidate is the direct text detector plus absolute successful-map
  innovation;
- five mandatory comparators include equal-capacity all-row innovation;
- bucket 0 cannot be acquired by the scientific program and is accepted only
  as a config-bound future Confirmation input;
- the auditor does not import the program and independently refits all OOF and
  full bundles.

The exact dense feature count is fixed by the implementation:

```text
4,256 rows × (128 latent-additive + 64 identity + 64 all-row + 64 successful)
= 1,361,920 values
```

## Executed checks

From `D:\Desktop\crl\20260722_1550_run01` with the shared Python 3.11.15
interpreter:

- v033 `py_compile`: exit `0`;
- v033 targeted pytest: exit `0`, `5 passed in 2.30s`;
- generated `implementation_v033/__pycache__` was resolved inside the intended
  directory and deleted.

The earlier structural preflight remains byte-applicable: 4,256 unique rows,
250 tasks, three generators, five sources, and both classes in every one of the
nine generator×fold cells.

## Freeze judgment

The only remaining risk is the preregistered scientific hypothesis. No
same-version hyperparameter or gate repair is authorized after execution.
v033 is ready for one publish-once Plan with the exact count `1,361,920`.
