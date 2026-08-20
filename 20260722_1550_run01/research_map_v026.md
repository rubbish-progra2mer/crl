<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"]
-->
# Research Map v026

## Failure and intervention

Terminal Wrench establishes real action-visible reward-hacking trajectories, while contract/state evidence shows why successful-looking terminal interaction need not establish the intended postcondition. v021 showed that a single successful same-task lexical reference can help on one split but remained heterogeneous on Confirmation. v025 showed that an additive verifier-relative partition is weaker than position-free anchor vocabulary. The v026 intervention replaces both with an episodic cross-generator support computation.

## Fixed setting

Development is the immutable union of exposed Terminal Wrench buckets 1, 2 and 3 at commit `d8a29613235a0ef56a8b70b3142626a533da28c2`. Their original acquisition phases remain bound per manifest (Development for buckets 1/2 and v022 Confirmation for bucket 3); v026 changes only their role to exposed Development and does not rewrite source metadata. Bucket 0 remains untouched Confirmation. Tasks must have at least one successful baseline from each of all three generator families, so that every training query retains a support after both its own and the bundle-target generator are excluded. The 22 prospectively identified ineligible Development tasks are fixed before scoring; 228 tasks and 4,072 rows remain.

For target generator `m` and task fold `f = SHA256(task_id)[1] mod 3`, held-out queries have generator `m` and fold `f`. Training queries and supports have folds other than `f` and generators other than `m`; references from `m` are forbidden. Held-out query supports are successful baselines of the same held-out task from generators other than `m`. Every eligible row is scored exactly once by the bundle that holds out both its task fold and generator.

## Shared representation and methods

One training-only char-wb TF-IDF vocabulary (3–5 grams, min-df 2, max 20,000) is fit on stripped action text from allowed training rows. Let `q` be a query vector, `r` a successful support vector, and `d=abs(q-r)`. Every fitted method uses class-weighted liblinear logistic regression, C=1, seed 12026. Pair sample weights sum to one per query, and pair-model class weights are computed from query-class counts so support multiplicity changes neither a query's total loss weight nor the global regularization scale.

Methods are:

1. `direct=[q]`;
2. `triple_query=[q,q,q]`, the 60,000-coordinate capacity control;
3. `consensus_no_abs=[q,r,r]`, trained over all allowed supports and mean-aggregated per query;
4. `single_support=[q,r,d]`, using the lexicographically first allowed support at inference and the same frozen Candidate pair model;
5. Candidate `cross_model_consensus=[q,r,d]`, trained over every allowed support and mean-aggregated per query.

The Candidate's unique supported delta over `single_support` is multi-support consensus; over `consensus_no_abs` it is the explicit absolute deviation block; over `triple_query` it is cross-generator same-task support information.

## Development analysis and gates

Primary metrics over all doubly held-out OOF rows are AUC and TPR at empirical 5% row FPR. The strongest comparator is the largest AUC among the four controls with deterministic name tie-break. A 2,000-resample task-cluster bootstrap evaluates Candidate-minus-strongest AUC. The main Codex must inspect all raw rows, task/fold/target-generator/source/support-count slices, pair counts, corrections, regressions and original source bindings.

All Development evidence gates are conjunctive: Candidate AUC `>=0.88`; TPR@5%FPR `>=0.55`; AUC delta versus strongest `>=0.005`; bootstrap lower bound `>0`; Candidate strictly exceeds all four comparators; Candidate-minus-strongest AUC is nonnegative for every held-out generator and positive for at least two; eligible tasks are at least 90% of all source tasks; all query/support/task/model/source/model/capture/audit bindings are current. Gate booleans cannot authorize Confirmation.

## Conditional untouched Confirmation

Only a positive written main-Codex Promotion Audit may acquire bucket 0. Three full Development bundles are frozen, one per target generator, and each excludes that generator from training queries/supports. Confirmation rows use the matching target-generator bundle and successful same-task supports from the other two generators, with no fitting, support reselection, comparator reselection or gate change.

Confirmation gates are Candidate AUC `>=0.86`; TPR@5%FPR `>=0.50`; Candidate strictly beats all controls; delta versus the frozen Development strongest comparator `>0` with task-bootstrap lower bound `>=0`; per-generator deltas are nonnegative and at least two are positive; eligible tasks are at least 90% of all source tasks; Development/Confirmation tasks are disjoint; all bytes are current. A positive main Confirmation Audit is required before Review.

## Prior collision and claim ceiling

D²4FAD and UniVAD establish few-normal-support transfer; LOTTERY establishes reference-dependent aggregation; Trajectory Guard establishes lightweight task/trajectory anomaly learning. The only open contrast is their absence of this exact real action-trajectory, cross-generator-support, jointly held-out task/generator computation and control ladder. No generic few-shot anomaly, Siamese, support weighting, reference-only testing, causal, universal or first-ever claim is allowed.
