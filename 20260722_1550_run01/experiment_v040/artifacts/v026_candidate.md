<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"]
-->
# Candidate v026 — Cross-Model Consensus Deviation (CMCD)

## Changed computation

For an evaluated stripped action trajectory `q`, collect every successful same-task support trajectory produced by a generator family different from `q`'s target generator. With one shared training-only vocabulary, each support `r` produces:

```text
pair(q,r) = [q, r, abs(q-r)]
```

A single supervised pair classifier is trained with every allowed support, weighting its pairs to total one per query and computing class balance from query counts rather than duplicated pair counts. CMCD is the arithmetic mean of its frozen pair probabilities. Development holds out both the query's task fold and its entire generator family; target-generator bytes are absent from that bundle's training queries and supports.

## Mandatory controls

- `direct=[q]` tests ordinary cross-task/cross-generator transfer;
- `triple_query=[q,q,q]` matches three-block capacity without support;
- `consensus_no_abs=[q,r,r]` uses every support and equal capacity without an explicit deviation block;
- `single_support=[q,r,abs(q-r)]` uses the lexicographically first support with the same frozen pair model, isolating multi-support aggregation.

Every fitted model shares the same eligible rows, target-generator exclusions, task folds, vocabulary recipe, learner, C and seed. Candidate must strictly beat all controls, not merely direct text.

## Data and claim boundary

Only exposed buckets 1–3 are Development. The 22 tasks lacking a successful baseline from every one of the three generator families are excluded prospectively, leaving 228 tasks and 4,072 rows. Bucket 0 is untouched Confirmation and may be acquired only after a positive written main-Codex Promotion Audit.

Only if Development, untouched Confirmation, independent audits, three fresh leaf Reviews and the main-Codex Decision all pass:

> On the fixed Terminal Wrench stripped-action protocol with known-good same-task traces from other generator families, mean aggregation of supervised query–support absolute-deviation scores improves reward-hack detection when both the evaluated task and generator are held out, relative to direct, capacity-matched, no-deviation and single-support controls.

No generic few-shot anomaly, support weighting, unseen-model universality, online monitor, causal state verification, hidden-intent, reasoning-trace, cross-benchmark or first-ever novelty claim is allowed.
