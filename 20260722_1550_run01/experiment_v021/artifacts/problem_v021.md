# Problem v021 — Capacity-Matched Test of Signed Task-Relative Residuals

The v020 target problem and action-surface scope remain unchanged. The unresolved identification problem is whether the observed gain comes from separating reference-novel from reference-missing n-grams, or merely from giving L2 logistic regression a third duplicated feature block.

v021 therefore asks whether `[x,novel,missing]` still beats:

- `[x,abs,abs]`, which preserves reference-difference magnitude and three-block regularization but removes direction; and
- `[x,x,x]`, which preserves three-block regularization but removes reference difference.

All earlier raw-text, reference-concat, absolute-delta, and RCED comparators remain. A loss to either new control falsifies the signed-direction claim and forbids Confirmation.
