<!-- crl-v3-evidence-ids
["ev-p039-aggregate-score-masking","ev-p080-fixed-depth-under-over-search","ev-p080-gold-supervised-minimal-depth"]
-->
# Research Map v013

## Evidence-backed motivation

- `ev-p039-aggregate-score-masking` supports the general risk that aggregate task scores can hide distinct tool-use failure mechanisms.
- `ev-p080-fixed-depth-under-over-search` supports the need to vary search depth across task/model conditions.
- `ev-p080-gold-supervised-minimal-depth` supports learned supervision for the earliest sufficient search depth.

These formal sources motivate adaptive depth and metric disaggregation. They do not establish the newly observed BoR inconsistency; that observation is bound to the fixed v013 target-paper PDF, notebooks, official metric library, and BFCL bytes.

## Nearest source relationship

The closest source is not merely adjacent work; it is the exact target paper and its official notebook. The second closest source is the same authors' separate official `bits-over-random` package, which computes the aggregate ratio as defined. v013's contribution is the byte-addressed consistency audit joining these two official artifacts and measuring ordinal consequences on the target protocol.

## Failure

The target paper defines:

```text
BoR = log2(P_obs / P_rand)
```

but its single-tool RL reward and reported notebook metric use:

```text
mean_i[hit_i * -log2(K_i / N_i)]
```

The latter is neither an unbiased per-query decomposition nor an algebraic estimator of the former. It rewards only successes by their individual ceiling and assigns failure zero. This can prefer a higher-coverage, deeper policy even when the defined aggregate ratio prefers a more selective shallower policy.

## Intervention

For every frozen policy/query row:

1. retain query ID, policy, seed, gold rank, selected `K`, `N`, and hit;
2. recompute the target notebook reward;
3. aggregate rows by policy and seed;
4. compute both `S_notebook` and `S_defined`;
5. enumerate all deterministic pairwise order comparisons under both metrics;
6. flag strict ordinal reversals and ties;
7. bootstrap complete query IDs so all policies for one query remain coupled;
8. independently verify fixed-K arithmetic from gold ranks.

The experiment does not change policy outputs after seeing either metric.

## Changed-computation claim

v013 changes the evaluation computation from a mean of success-weighted per-query ceilings to the defined logarithm of an aggregate observed/chance ratio. It is not:

- a prompt change;
- a new retriever;
- another RCED or TPPA variant;
- threshold retuning;
- an alternative data split;
- a claim based on file existence or a script-generated PASS label;
- a fixture sanity check.

## Main scientific risks

- Development uses a benchmark and author outputs already read during selection; only Confirmation is untouched.
- Exact DQN trajectories can vary with PyTorch/platform details even at fixed seeds. Primary metric identities operate on frozen produced rows; reproduction tolerances therefore cover policy-level means rather than require bit-identical weights.
- A ranking reversal shows metric non-equivalence and interpretive consequence, not that either policy is universally better.
- Aggregate BoR can favor very selective low-coverage policies. v013 does not promote it as a complete deployment utility.
- BFCL v3 and v4 live-simple are two benchmark versions, not broad task-family generalization.
- The target paper is a recent preprint and may be revised after the fixed source bytes.

## Candidate Promotion Audit Before Development

The target failure is directly observable in frozen source code and finite arithmetic. The proposed audit changes a material evaluation computation rather than relabeling an existing score. The discrepancy has a precise null condition: if all evaluated policies have identical hit/depth distributions or happen to preserve the same ordering, ordinal impact may vanish even though the formulas differ.

The nearest fair comparator is the target notebook statistic on exactly the same policy/query rows. The defined metric is implemented two ways: a local direct formula and the fixed official `bits-over-random` audit primitives. Fixed-K rows provide an analytic control independent of DQN training.

Development exposure is explicitly disclosed. Promotion requires faithful protocol reproduction, exact row-level recomputation, an ordinal consequence beyond one seed, and coupled-query uncertainty analysis. The allowed claim is correspondingly limited to the fixed metric interpretation. On this basis, the main Codex authorizes implementation and one frozen Development experiment, but not Confirmation.

## Development contract

Development uses the fixed BFCL v3 simple file and reproduces the target notebook's BM25 registry, `70/30` shuffled split under seed `42`, DQN architecture, reward definitions, seeds, and training episode count. It records all per-query policy rows before calculating either aggregate score.

The exact one-shot Experiment Plan must freeze:

- source and input hashes;
- BM25 tokenization and implementation;
- train/test IDs;
- DQN hyperparameters and seeds;
- fixed-K policies;
- metric equations;
- bootstrap resamples/seed;
- reproduction tolerances;
- promotion gates;
- prospective Confirmation commit/path;
- compute/time budget.

## Development promotion gates

All gates must pass:

1. **Row integrity:** exactly one row per `(query_id, policy, seed)` for DQN policies and one per `(query_id, fixed_k)` for fixed policies; all `1 <= K <= N`, `hit == (gold_rank <= K)`, and values finite.
2. **Recomputation identity:** maximum absolute error between stored target reward and `hit * -log2(K/N)` is `<= 1e-12`.
3. **Independent defined-metric identity:** direct `log2(mean(hit)/mean(K/N))` and the separately imported fixed official metric primitive differ by `<= 1e-12` for every nondegenerate policy.
4. **Faithful reproduction:** each three-seed target-policy mean found fraction and mean K is within `0.03` and `1.0`, respectively, of the fixed official notebook output; each fixed-K found fraction is within `0.01`.
5. **Fixed-K control:** the preregistered `K=1` versus `K=3` pair reverses strict order between notebook and defined metrics on Development.
6. **Learned-policy consequence:** at least two of the three seeds contain a strict order reversal involving a learned policy and a fixed-K policy.
7. **Aggregate consequence:** the policy maximizing the notebook statistic is not the policy maximizing defined BoR.
8. **Bootstrap support:** for the preregistered reversed fixed-K pair, a coupled-query bootstrap with `20,000` resamples yields at least `0.95` probability that each metric's signed pairwise difference has its observed, opposite sign.

No gate may be lowered after execution. Development failure forbids Confirmation.

## Untouched Confirmation contract

After a positive main-Codex Promotion Audit, acquire only `BFCL_v4_live_simple.json` from the fixed Gorilla commit. Apply the frozen Development implementation, tokenization, trained DQN weights, policy evaluation, metric equations, fixed-K set, and bootstrap procedure without refitting or threshold selection.

Confirmation gates:

1. Development and Confirmation line hashes are disjoint.
2. All row-integrity and both metric-identity checks pass.
3. At least one strict policy-pair order reversal appears.
4. The aggregate maximizing policy differs under the two metrics.
5. A preregistered fixed-K reversal has coupled-bootstrap sign support of at least `0.90` in both directions.

If the exact `K=1`/`K=3` pair does not reverse in Confirmation, the implementation may report other pairs but may not substitute one post hoc for gate 5; v013 fails unless the frozen Plan prospectively defines a deterministic pair-selection rule before Confirmation is acquired.

## Review and decision boundary

Only a complete frozen Review Packet containing implementation, Plan, inputs, environment capture, raw Development and Confirmation rows, raw stdout/stderr, metrics, audits, and hashes may open three independent Reviewer calls. Reviewer votes or scores cannot substitute for the main Codex's final evidence adjudication.
