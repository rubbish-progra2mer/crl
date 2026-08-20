# P088 Reconciliation

- Disposition: `DIRECT_OPERATOR_ADMISSION_WITH_THEORY_DEPLOYMENT_AND_SCALE_BOUNDARY`
- Read 1 SHA-256: `ef8dd73665749188cd2438fc4c59ab78125797a75e7fb56972c9c23feba3227f`
- Accepted read-2: `read_2_attempts/r2-20260720-p088-a1/`
- Read-2 invocation SHA-256: `49ea219c1138707c973fb87fe44a39f4a3cdc1e9ff3e57f4d690a91257a9ea83`
- Read-2 report SHA-256: `56af1fdeee931dd0ce98371706ebfc67548c5e8bdacb525aeefdec45caae12b4`
- Other attempts: none
- Read 3: not triggered; both reads agree on the objective, residual mechanism, direct-prior role and deployment limits. The proposition-number typo does not affect the admitted computation.

## Source reconciliation

- `AGREE`: NNN replaces independent query–item scores with a non-negative elastic-net reconstruction of the query from the full corpus embedding matrix, ranking the support by learned coefficient magnitude.
- `RESIDUAL_CHANGED_COMPUTATION`: selecting an item explains part of the query vector; subsequent correlated items compete against the remaining residual, making the returned set jointly dependent rather than independently top-k.
- `DIRECT_PRIOR`: this is a direct method-level prior for joint-set retrieval, residualized sparse decoding, redundancy suppression and complementary tool-set recovery. The same non-negative reconstruction/support computation is an exact or near-exact collision.
- `THEORY_BOUNDARY`: Theorem 1 is a per-query existence statement. Its hyperparameters may depend on the corpus, true target set and query; it does not provide one deployable parameter pair for all queries or guarantee finite-step FISTA recovery.
- `DEPLOYMENT_MISMATCH`: experiments select one global parameter pair on validation data. The theorem cannot be used as a guarantee for that shared-parameter system, and the frozen version is hyperparameter-sensitive.
- `RESULT_BOUNDARY`: NNN-FIX is strong on the ToolBank datasets but is not uniformly better on every dataset/metric; NNN-TR is more consistent but additionally changes representation training through unrolled optimization. Single point estimates lack repeated-seed uncertainty.
- `MECHANISM_SIGNATURE_BOUNDARY`: larger relevant-set size is consistent with the residual account, but it also covaries with task difficulty and metric ceilings; the source does not directly measure residual mediation.
- `SCALE_BOUNDARY`: FISTA repeatedly multiplies by the full corpus matrix, with `O(dNT)` inference and unrolled-training activation cost. Evaluated corpora contain at most 1,651 items, with no ANN-scale latency or resource comparison.
- `LABEL_BOUNDARY`: Recall/Completeness evaluate recovery of labeled target sets. They do not establish general diversity, alternative-tool validity, executability or downstream answer correctness.

## Frozen source role

Operator source and mandatory closest-composition comparator for jointly decoding complementary tool/document sets through non-negative residual reconstruction. It does not establish a scalable ANN replacement, global-parameter guarantee or end-to-end Agent success.
