<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"]
-->
# Candidate v020 — Task-Relative Signed Sparse Residuals

## One-sentence method kernel

For stripped terminal-agent trajectories with one excluded successful same-task reference, classify reward hacking from the evaluated trajectory TF-IDF vector plus separate sparse channels for n-grams added relative to the reference and n-grams missing from it.

## Baseline and changed computation

Let `x` be the L2-normalized character TF-IDF vector of one evaluated trajectory's commands and terminal outputs, and `r` the vector of the reserved successful reference for the same task. Define elementwise:

```text
common  = min(x,r)
novel   = x-common       = max(x-r,0)
missing = r-common       = max(r-x,0)
```

The Candidate fits the same class-weighted logistic regression used by every learned comparator on `[x, novel, missing]`. The proposed delta is the signed sparse residual map only. The reference is excluded from labels and reported rows.

## Why this differs from v012

v012 represented task-relative deviation with 29 coarse numeric features and failed because legitimate alternate workflows can have large effect/path distances while exploits can follow common effect sequences. v020 preserves the exact character fragments that produced each deviation and separates additions from omissions. It does not retune RCED or reuse its failed Candidate scores.

## Fixed data and split

- Development input: frozen v012 bucket-2 dataset, 1,729 rows, SHA-256 `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3`.
- Eligible-task/reference rule: identical to v012.
- Development train/validation/test partition: identical deterministic task-ID rule; exposed task `1012` remains forced into train.
- Confirmation: repository bucket 3 at commit `d8a29613235a0ef56a8b70b3142626a533da28c2`; acquisition forbidden before Promotion Audit.
- Analysis/cluster unit: trajectory/task ID.

Development is exposed and optional-stopping-prone. Only the untouched task-disjoint bucket 3 can confirm the result.

## Exact fair comparators

All use the same rows, fixed char-wb 3-5 TF-IDF vocabulary (fit only on evaluated training trajectories), class-weighted liblinear logistic regression, `C=1.0`, seed `12020`, and validation threshold selection:

- `text`: `x`.
- `reference_concat`: `[x,r]`.
- `absolute_delta`: `[x,abs(x-r)]`.
- `rced`: `[x, standardized 29-feature v012 delta]`.
- `signed_residual`: `[x,novel,missing]` Candidate.

The Candidate must beat the strongest of all four comparators on Development; the winner identity is then frozen for Confirmation.

## Development claim contract

The seven gates in `research_map_v020.md` are fixed and conjunctive. In particular, Candidate AUC must be at least `0.91`, TPR@5%FPR at least `0.55`, AUC delta versus the strongest comparator at least `0.005` with task-bootstrap lower bound above zero, validation-threshold FPR at most `0.08`, and Candidate AUC must strictly exceed every comparator.

The program records all row IDs, task IDs, targets, reference IDs, five scores, split memberships, thresholds, model/vectorizer bytes, feature dimensions, and source hashes. A separate auditor independently recomputes raw-row metrics, gates, partitions, reference exclusion, and model/config bindings.

## Maximum allowed claim

If Development, untouched Confirmation, three independent Reviews, and main-Codex decision all support it:

> On the fixed task-disjoint Terminal Wrench stripped-trajectory protocol with one successful same-task reference, separating reference-novel and reference-missing character n-grams improves low-cost reward-hack detection over raw text, reference concatenation, unsigned delta, and coarse RCED comparators.

## Forbidden claims

- First contrastive reward-hack detector.
- General reward-hack, malicious-agent, or task-success proof.
- Operation without a trusted same-task reference.
- Superiority to Terminal Wrench's LLM judge or Cheap Reward Hacking encoder on their different published splits.
- Robustness to reasoning removal beyond the fixed stripped condition, adversarial paraphrase, new benchmarks, or online attacks.
- Automatic Promotion from gates, files, or scores.

## Kill conditions

Any gate failure, reference leakage, split overlap, metric mismatch, or strongest-comparator loss freezes v020 and forbids Confirmation. No threshold, vocabulary, reference rule, comparator, or learner may change after execution.
