<!-- crl-v3-evidence-ids
["ev-p039-aggregate-score-masking","ev-p080-fixed-depth-under-over-search","ev-p080-gold-supervised-minimal-depth"]
-->
# Research Map v019

## Observed Failure and boundary

- [AUTHOR_FACT] P080 reports that fixed search depth can under-search difficult cases and over-search easy cases. [[evidence:ev-p080-fixed-depth-under-over-search]]
- [AUTHOR_FACT] P080 uses hindsight success to supervise the earliest sufficient search depth. [[evidence:ev-p080-gold-supervised-minimal-depth]]
- [AUTHOR_FACT] P039 shows that aggregate tool-use scores can collapse distinct failure modes. [[evidence:ev-p039-aggregate-score-masking]]
- [CODEX_SYNTHESIS] The fixed target BoR paper defines an aggregate success/chance ratio but trains with a different success-weighted per-query ceiling. The prior v013 run established the non-equivalence on frozen rows. That fact motivates the target failure but does not establish that v019's constrained objective works.

The boundary is tool presentation, not downstream argument correctness or execution. A policy with high defined BoR but low coverage is not accepted as useful merely because its selectivity ratio is large.

## Intervention stage

The intervention occurs after BM25 has produced a complete tool ranking and before a shortlist is passed to an LLM. The policy reads the same seven target state features and emits the same binary `STOP` or `CONTINUE` action. Only the training utility and its slow control variable change.

## Operator shortlist and source recheck

1. **Published per-query chance surrogate.** Success at K receives `-log2(K/N)` and failure receives zero. This creates adaptive behavior but is not the aggregate ratio it is named after.
2. **Unconstrained ratio optimization.** Generic cost-aware RL optimizes average reward over average cost through an auxiliary `reward - rho * cost` computation. On the exposed Development fixed policies, the aggregate ratio favors `K=1` despite 0.60 coverage. It is retained only as a mechanism ablation.
3. **Coverage-constrained chance exposure.** Treat `K/N` as terminal cost and gold presentation as terminal success; update a slow dual variable to keep training coverage at 0.90 while the DQN minimizes exposure. This is the selected kernel.
4. **Order counterbalancing.** Killed because current permutation-invariance and position-calibration methods already occupy that computation.

## Competing method kernels

### Kernel A — unconstrained aggregate-ratio control

- Failure: published surrogate is not the aggregate ratio.
- Changed computation: terminal utility `hit - rho*(K/N)` with a slow ratio estimate.
- Direct falsifier: collapse toward `K=1` or materially reduced coverage.

### Kernel B — coverage-constrained chance-exposure control

- Failure: the current reward hides the operational coverage requirement inside a non-equivalent per-query score.
- Changed computation: terminal utility `lambda*hit - K/N`; update `lambda` from the training coverage residual against a fixed 0.90 demand.
- Direct falsifier: no reduction in mean K at matched coverage, instability across seeds, or failure to preserve coverage on untouched data.

## Natural-language disposition

Kernel A is retained only as a no-constraint ablation because the exposed fixed-K rows already show the metric's low-coverage optimum. Kernel B is kept because it changes the actual stop decision objective, has a direct final-outcome test, reuses a real pipeline without new dependencies, and is not equivalent to prompt editing, threshold-only evaluation, or another retrieval reranker.

## Candidate Promotion Audit — before Development

The Target Failure is visible in the joint result variables `(coverage, mean K, defined BoR)`: the target surrogate can produce a policy that is neither an optimizer of defined BoR nor an explicit solver of the paper's stated high-coverage/low-depth tradeoff. The Candidate changes the DQN's terminal utility and a slow training-time dual that controls the `STOP` boundary. This can affect the final shortlist because every action value is trained against chance exposure under an explicit coverage residual; it is not a validity or formatting proxy.

The closest component prior is cost-aware ratio/constrained RL. The closest full pipeline is the official target adaptive tool-depth DQN. The nearest recent adjacent pipeline uses offline RL with an explicit correctness-versus-step-cost reward for adaptive policy retrieval. v019 borrows all of those ideas and claims only the fixed-pipeline empirical delta: explicit coverage control plus chance exposure in place of the target per-query surrogate.

Pre-implementation review also found that v013's local target-labelled DQN was not a valid comparator because its state included a gold-dependent `found` feature and its split/training details differed from the target BFCL notebook. v019 therefore compares only against a fresh official-state reproduction executed in the same frozen program and budget. This necessary rerun repairs comparator validity; it does not repair or reinterpret v013.

Development is justified because the Candidate computation has not been run, the target metric mismatch is present in frozen source bytes, the official comparator code is fixed, the implementation requires no new model or environment mutation, and a prospective BFCL version remains unread. Positive Development will not automatically authorize Confirmation; the main Codex must inspect raw per-query corrections, coverage losses, dual trajectories, official-baseline reproduction, and comparator fairness first.

## Unique narrow Gap

The remaining gap is whether a slow coverage dual applied to the target STOP/CONTINUE DQN can preserve presented-gold coverage while lowering chance exposure on real BFCL rankings, relative to the same fixed target policy rows. The experiment does not seek a new general constrained-RL algorithm.
