# Problem v013 — Does the reported adaptive-tool statistic equal the defined Bits-over-Random metric?

## Research question

For variable-depth tool-shortlist policies, does the success-weighted per-query ceiling reported as “BoR bits” in arXiv:2605.24660 equal the paper's own aggregate definition `log2(P_obs / P_rand)`? If not, does the substitution materially change policy ordering on a faithful BFCL reproduction and on an untouched BFCL version?

## Formal distinction

For query `i`, let:

- `h_i` be one when the gold tool appears in the presented top `K_i`, else zero;
- `N_i` be the candidate-tool count;
- `p_i = K_i / N_i` for a single relevant tool.

The target notebook statistic is:

```text
S_notebook = mean_i[h_i * (-log2(p_i))]
```

The paper-defined aggregate BoR, following the separate official auditor, is:

```text
S_defined = log2(mean_i[h_i] / mean_i[p_i])
```

`S_notebook` is the expected success-weighted chance ceiling. `S_defined` is the logarithm of a ratio of aggregate probabilities. The logarithm and the hit weighting do not commute, so the quantities are generally different even when every query has the same `N`.

## Why the distinction matters

The target paper presents the per-query reward as a deployable reward and reports its mean under the label “BoR bits.” If that mean is not the defined metric, then:

- optimizing the reward does not by itself establish maximization of defined BoR;
- reported policy order under “BoR bits” can differ from order under defined BoR;
- the empirical coverage, average depth, and downstream tool-choice results may remain valid, but the chance-corrected metric interpretation requires correction.

## Evaluation unit and scope

- Unit: one BFCL simple-query row evaluated under one frozen policy.
- Development: BFCL v3 simple at the fixed source commit and SHA.
- Confirmation: untouched BFCL v4 live simple at its fixed commit, acquired only after promotion.
- Policies: target-paper BoR-reward DQN, F1-reward DQN, and fixed `K ∈ {1,3,5,10,20,50}` where the corpus permits.
- Seeds: `42`, `123`, and `456` for both DQN policies.
- Scorer and split: faithful BM25 construction and target-notebook split.

The candidate does not evaluate downstream LLM tool choice and requires no API credentials.

## Falsifiable target

Development must show all of the following before Confirmation can be opened:

1. the implementation reproduces the notebook statistic exactly from frozen per-query rows;
2. at least one policy pair reverses order between `S_notebook` and `S_defined`;
3. the reversal is not confined to a single DQN seed;
4. a query bootstrap gives nonzero support for the observed metric difference;
5. the faithful replication stays within preregistered tolerances of the official preserved BM25 outputs.

Failure of any gate closes v013 without acquiring Confirmation.

## Claim boundary

If Development, untouched Confirmation, and three-review adjudication all pass, the strongest allowed claim is:

> In the fixed official BFCL tool-selection protocols, the reported mean success-weighted ceiling is not the paper-defined aggregate Bits-over-Random metric and can reverse policy rankings; consequently, those reported values do not establish that the BoR-reward policy maximizes defined BoR.

The claim does not deny the target paper's observed coverage, depth adaptation, or downstream choice-accuracy results, and it does not claim that aggregate BoR is by itself the correct utility objective.
