<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"]
-->
# Research Map v021

## Frozen Candidate

`signed_residual = [x,max(x-r,0),max(r-x,0)]`.

## Comparator-complete ladder

All use identical rows, vocabulary, logistic learner, C, class weights, seed, threshold selection, and bootstrap:

1. `text = [x]`.
2. `reference_concat = [x,r]`.
3. `absolute_delta = [x,abs(x-r)]`.
4. `rced = [x, standardized coarse delta]`.
5. `triple_text = [x,x,x]`.
6. `duplicated_absolute = [x,abs(x-r),abs(x-r)]`.
7. Candidate `signed_residual = [x,novel,missing]`.

The strongest of all six comparators is fixed from v021 Development before Confirmation.

## Unchanged Development gates

Candidate AUC `>=0.91`; TPR@5%FPR `>=0.55`; AUC delta versus the enlarged strongest comparator `>=0.005`; task-bootstrap lower bound `>0`; frozen-threshold FPR `<=0.08`; frozen-threshold TPR `>=0.45`; Candidate AUC strictly exceeds every comparator; reference/split/audit error `<=1e-12`.

## Promotion boundary

v020's positive metrics are motivating evidence only. v021 requires its own captured fit, raw rows, model bundle, audit, case readback, and main-Codex judgment. Bucket-3 acquisition remains forbidden until that judgment is positive.
