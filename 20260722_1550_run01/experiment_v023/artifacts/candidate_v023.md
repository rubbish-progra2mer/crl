<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p079-action-conditioned-contextualization","ev-p079-unseen-ui-boundary"]
-->
# Candidate v023 — Action–Observation Role Factorization (AORF)

## Changed computation

Let a single training-only char-wb TF-IDF vocabulary map the complete mixed trajectory, commands alone and terminal outputs alone to `x`, `c`, and `o`. The Candidate is:

```text
AORF(x,c,o) = [x,c,o]
```

This permits a linear detector to weight the same lexical coordinate differently when it was issued by the agent versus observed from the environment, while retaining the conventional mixed surface.

## Mandatory controls

In addition to mixed, commands-only, outputs-only and `[c,o]` baselines, three exact 90,000-dimensional controls are mandatory:

- `[x,x,x]`: generic three-block L2 capacity;
- `[x,c,c]`: mixed plus duplicated action evidence;
- `[x,o,o]`: mixed plus duplicated observation evidence.

AORF must strictly exceed every comparator. The same shared vocabulary, learner, C, seed, data, thresholds and task-cluster bootstrap apply to all eight methods.

## Data boundary

Only already touched buckets 2+3 are Development. No same-task reference is selected or removed. Bucket 0 is the predesignated untouched Confirmation and may be acquired only after a positive written main-Codex Development audit. Bucket 1 is unused.

## Maximum claim

Only if Development, bucket-0 Confirmation, independent audits, three fresh Reviews and main-Codex Decision all pass:

> On the fixed task-disjoint Terminal Wrench stripped command/output protocol, assigning independent shared-vocabulary coefficient roles to issued commands and observed terminal feedback improves reference-free reward-hack detection over mixed, role-only, concatenated, and capacity-matched single-role duplication controls.

No sequence modeling, causal state verification, general detector, online safety, per-task dominance, cross-benchmark or first-ever role-separation claim is allowed.
