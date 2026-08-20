# Research Map v032

## Fixed data boundary

Development is the immutable union of Terminal Wrench buckets 1, 2 and 3 at
repository commit `d8a29613235a0ef56a8b70b3142626a533da28c2`. It contains
4,256 unique rows, 250 tasks, three generator families and five source
datasets. Existing per-bucket manifests bind every source byte.

For generator `m` and task fold
`f = SHA256(task_id)[1] mod 3`, the held-out rows have generator `m` and fold
`f`. Training rows have a different generator and a different task fold. Every
Development row receives exactly one out-of-fold score.

Bucket 0 is the predesignated untouched Confirmation. It may be acquired only
after a positive written main-Codex Promotion Audit.

## Shared representation

For each training bundle:

1. deterministically extract the task description from the frozen prompt and
   form the full stripped action surface from commands plus terminal outputs;
2. fit one char-wb TF-IDF vocabulary on the union of training task and action
   texts only;
3. fit a 64-coordinate randomized Truncated SVD on that same training union,
   with fixed seed and iteration count;
4. L2-normalize task and action latent rows.

No held-out task, held-out generator or label enters this representation fit.

## Conditional normal-action map

Let normalized latent task and action vectors be `t` and `a`.

The Candidate map `W_success` is a fixed-alpha multi-output ridge regression
from `t` to `a`, fitted only on successful (`target=0`) training rows. Each
task contributes total sample weight one, so tasks with more baseline
trajectories cannot dominate.

The Candidate feature is:

```text
innovation_success = abs(a - W_success(t))
candidate = [direct_action_tfidf, z(innovation_success)]
```

The feature scaler and supervised class-balanced logistic detector are fitted
on the same allowed training rows. Only the map is success-only; the final
detector uses the legitimate and exploit labels available in Development.

## Mandatory methods

All methods use the same rows, bundle split, fixed hyperparameters and direct
action vocabulary:

1. `direct_action`: direct action/terminal char TF-IDF;
2. `task_concat`: one char TF-IDF over `TASK ... ACTION ...`;
3. `latent_additive`: direct text plus `[t,a]`;
4. `identity_innovation`: direct text plus `abs(a-t)`;
5. `all_row_innovation`: direct text plus `abs(a-W_all(t))`, where `W_all`
   uses every training row with equal total weight per task;
6. Candidate `successful_innovation`: direct text plus
   `abs(a-W_success(t))`.

`all_row_innovation` is the equal-capacity closest composition. Candidate
attribution requires strictly beating it. `latent_additive` controls access to
the same task and action latents without a conditional residual.

## Fixed Development gates

Primary metrics are AUC and TPR at empirical 5% FPR over all doubly held-out
rows. The strongest comparator is selected by Development AUC with a
deterministic name tie-break. A 2,000-resample task-cluster bootstrap estimates
Candidate-minus-strongest AUC.

Every gate is conjunctive:

- Candidate AUC `>= 0.88`;
- Candidate TPR@5%FPR `>= 0.55`;
- Candidate-minus-strongest AUC `>= 0.005`;
- task-cluster bootstrap lower bound `> 0`;
- Candidate strictly beats all five comparators in AUC;
- all three generator deltas are nonnegative;
- at least two generator deltas are positive;
- at least four of five source deltas are nonnegative;
- all representation, mapping, feature, prediction, metric, environment,
  capture and independent-audit bytes are current.

Scripts may report gates but cannot authorize Confirmation.

## Conditional Confirmation

After and only after a positive main-Codex Promotion Audit, acquire repository
bucket 0 with the frozen config and acquisition script. Exact Development and
Confirmation task IDs must be disjoint.

The frozen full Development bundle for each target generator scores that
generator's Confirmation rows without fitting. The Development strongest
comparator remains fixed.

Confirmation requires:

- Candidate AUC `>= 0.86`;
- Candidate TPR@5%FPR `>= 0.50`;
- Candidate AUC strictly exceeds every comparator;
- Candidate-minus-frozen-strongest AUC `> 0`;
- task-bootstrap lower bound `>= 0`;
- all generator deltas nonnegative and at least two positive;
- at least four source deltas nonnegative;
- exact data/model/output/audit/capture integrity.

A positive written main-Codex Confirmation Audit is required before freezing a
Review Packet.

## Claim ceiling

Only if Development, untouched Confirmation, independent audits, three fresh
leaf Reviews and the main-Codex Decision all pass:

> On the fixed Terminal Wrench stripped serious-exploit protocol, under held-out
> task and held-out generator evaluation, augmenting a supervised action-text
> detector with absolute innovation from an equal-task-weight successful-only
> cross-task task-to-action map improves detection over direct text,
> task/action concatenation, raw latent, identity-residual and all-row
> conditional controls.

No generic anomaly detector, task-alignment guarantee, causal localization,
state verification, online intervention, unseen-domain, per-task dominance or
first-ever claim is allowed.

