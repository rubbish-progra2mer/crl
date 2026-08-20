# Research Map v034

## Fixed data boundary

Development is the immutable union of three ToolPRMBench files at repository
commit `b43164fbb2cd2963e1906a6fe62a86e7ce05973e`:

- `prmbench_GTA.json`: 118 pairs;
- `prmbench_bfcl.json`: 111 pairs;
- `prmbench_tooltalk.json`: 86 pairs.

There are 315 pairs and 630 pointwise actions. Each file is one source domain.
For each held-out source, empirical calibration and any learned control use
only the other two sources. Every pair receives exactly one out-of-source
prediction.

Pair clusters are `source + task` for GTA and ToolTalk and
`source + sample_id` for BFCL, yielding 195 Development clusters. Pair order is
irrelevant: pointwise scores are computed before chosen/rejected comparison.

`prmbench_ToolSandbox.json` is the predesignated untouched Confirmation. It may
be acquired only after a positive written main-Codex Promotion Audit.

## Frozen model and answer likelihood

All methods use official `Qwen/Qwen3-0.6B` at revision
`c1899de289a04d12100db370d81485cdf75e47ca` in BF16 evaluation mode on the
shared RTX 5060 Ti environment. No generation, sampling, fine-tuning, external
API or second model is allowed.

The tokenizer's exact answer tokens are:

```text
Yes = 9454
No  = 2753
```

Thinking is disabled through the model's native chat template. For prompt
`x`, the pointwise validity logit is:

```text
L(x) = log p(Yes | x) - log p(No | x)
```

Only the next-token logits are used. A prompt is deterministically limited to
12,288 tokens by retaining fixed head and tail portions of its evidence
sections; the action and obligation instruction are never truncated.

## Deterministic evidence compiler

The compiler reads only each frozen row's `history`, `functions` and candidate
action. It normalizes JSON with sorted keys and compact separators, detects a
structured call when present, extracts its tool name, and selects a matching
schema by exact `name`, `api_name` or `api_names`. GTA embeds its tool
description in the system history; when no separate `functions` object exists,
that frozen system content is the schema carrier.

No label, `rationale`, `error type`, `possible_answer`, model name, chosen
position or rejected position enters a prompt.

Five obligation prompts are fixed:

1. `mode`: history, action, available tool names/descriptions; decide whether
   tool call versus natural-language response is the correct next mode;
2. `tool`: history, action, available names/descriptions; decide whether the
   selected tool exists and is the functionally appropriate next operation;
3. `arguments`: action and exact matched schema; decide names, required fields,
   types, enums and explicit schema constraints;
4. `grounding`: history, action and matched schema; decide whether argument
   values and factual assertions are supported by prior user/tool evidence and
   preserve required exact content;
5. `progress`: history, action and matched schema; decide prerequisites,
   ordering, response to prior failure, non-repetition and progress toward the
   request.

If an obligation is genuinely inapplicable, its fixed instruction requires
`Yes`; it may not invent an error merely because no tool call is present.

A sixth `holistic` prompt receives the union of full history, full tool
metadata and action and asks whether the action is the correct next step. It is
a mandatory same-model baseline.

## Candidate calibration and score

For held-out source `s`, let `T` be all 2-action points from the other two
sources. For obligation `k`, convert logit `l` to a midrank empirical
percentile:

```text
F_k(l) = (count_T(L_k < l) + 0.5 * count_T(L_k = l)) / |T|
```

No Development label enters `F_k`. The Candidate, Contract-Calibrated
Conjunctive Bottleneck (`CCCB`), is:

```text
CCCB(action) = min_k F_k(L_k(action))
```

For every pair, the higher pointwise score wins; exact ties receive `0.5`
accuracy credit.

## Mandatory comparators

All use the same frozen rows and model:

1. `holistic`;
2. five individual obligation logits;
3. `raw_min`: minimum of the five raw logits;
4. `calibrated_mean`: arithmetic mean of the five percentiles;
5. `calibrated_product`: sum of `log(max(F_k, 1e-6))`;
6. `pair_majority`: majority of the five pointwise obligation comparisons,
   with tied votes split;
7. `selected_single`: choose the best individual obligation by pair accuracy
   on the other two labeled sources, fixed-name tie-break, then apply it to the
   held-out source;
8. `linear_ensemble`: fixed-C logistic regression on signed five-logit pair
   differences from the other two sources, augmented by their negations with
   opposite labels, then applied to the held-out source.

The linear control uses `C=1`, L2 penalty, `liblinear`, intercept, no feature
scaling and seed `3401`. No hyperparameter or threshold search is allowed.

## Metrics and independent audit

Primary metric is pairwise accuracy with exact ties worth `0.5`. A
2,000-resample cluster bootstrap over the 195 fixed clusters estimates
Candidate-minus-strongest-comparator accuracy, seed `3401`. The strongest
comparator is selected by overall Development accuracy with deterministic name
tie-break.

Raw output must contain all 315 pair identities, source, cluster, both action
scores, all six next-token logit pairs, percentiles, all method decisions and
chosen/rejected orientation. The independent auditor must load the model from
the frozen local snapshot and recompute every prompt, token boundary, logit,
percentile, learned control, decision, slice, bootstrap and summary from source
bytes rather than trusting the program.

## Fixed Development gates

Every gate is conjunctive:

- Candidate accuracy `>= 0.60`;
- Candidate-minus-strongest accuracy `>= 0.03`;
- cluster-bootstrap lower bound `> 0`;
- Candidate strictly beats every mandatory comparator overall;
- Candidate accuracy is at least `0.50` on each of GTA, BFCL and ToolTalk;
- all three source deltas versus the frozen strongest comparator are
  nonnegative;
- at least two source deltas are strictly positive;
- action-swap recomputation changes no pointwise score and reverses every
  non-tied pair decision exactly;
- all source/model/prompt/output/environment/capture and independent-audit
  bytes are current.

Scripts may report gates but cannot authorize Confirmation.

## Conditional Confirmation

Only after all Development gates and a positive main-Codex Promotion Audit may
the frozen acquisition script download the repository's
`prmbench_ToolSandbox.json` at the same commit. For Confirmation, each
obligation's empirical calibration distribution is frozen from all 630
Development action points. The selected-single identity is chosen once from
all 315 Development pairs, and the fixed-C linear control is fitted once on all
Development pair differences plus their negations. These full-Development
states and the Development strongest-comparator name are written before
Confirmation acquisition and then applied without fitting or selection.

Confirmation requires:

- Candidate accuracy `>= 0.58`;
- Candidate-minus-frozen-strongest accuracy `> 0`;
- cluster-bootstrap lower bound `>= 0`;
- Candidate strictly beats every frozen mandatory comparator;
- exact pointwise/model/data/capture and independent-audit integrity.

A positive written main-Codex Confirmation Audit is required before a formal
Review Packet can be frozen.

## Claim ceiling

Only if Development, untouched Confirmation, independent audits, three fresh
leaf Reviews and the main-Codex Decision all pass:

> On the fixed ToolPRMBench source-holdout protocol with Qwen3-0.6B, fixed
> schema/history-derived obligation projections and the minimum of
> other-source empirical obligation percentiles improve pairwise next-action
> accuracy over holistic, single-obligation, soft-aggregation, voting,
> source-selected and supervised-linear controls.

No generic PRM, rubric-decomposition novelty, formal correctness, executable
state verification, unseen-benchmark, larger-model, search-improvement or
online-safety claim is allowed.
