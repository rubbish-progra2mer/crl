<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"]
-->
# Candidate v021 — Task-Relative Signed Sparse Residuals with Capacity-Matched Controls

## Candidate identity

The scientific Candidate is byte-equivalent in computation to v020:

```text
common  = min(x,r)
novel   = x-common
missing = r-common
signed_residual = [x,novel,missing]
```

v021 changes only the fair comparator set after the main Codex found a pre-Confirmation identification defect in v020.

## New mandatory controls

- `triple_text = [x,x,x]` matches 90,000-dimensional three-block regularization without reference information.
- `duplicated_absolute = [x,abs(x-r),abs(x-r)]` matches 90,000-dimensional three-block regularization and unsigned reference distance without signed direction.

The four v020 comparators remain. All seven methods use the same exposed Development bytes, split, reference rows, char-wb 3-5 TF-IDF vocabulary, class-weighted liblinear logistic regression, C=1, seed 12020, validation threshold rule, and task-cluster bootstrap.

## Frozen gates and Confirmation

Every v020 gate is unchanged but the strongest-comparator set expands from four to six. Candidate must strictly beat both capacity controls and every earlier comparator, retain AUC at least `0.91`, low-FPR TPR at least `0.55`, and delta at least `0.005` with positive task-bootstrap lower bound.

Only a positive main-Codex audit of fresh v021 Development may authorize the still-unacquired Terminal Wrench bucket-3 Confirmation. Confirmation uses the same frozen seven models, thresholds, and strongest-comparator identity without refitting.

## Maximum claim

If all later stages pass:

> On the fixed task-disjoint Terminal Wrench stripped-trajectory protocol with one successful same-task reference, signed reference-novel/reference-missing n-gram channels improve reward-hack detection over raw, concatenated, coarse, unsigned, and capacity-matched duplicated controls.

No first-contrastive, general detector, online safety, task-success, or cross-benchmark claim is allowed.
