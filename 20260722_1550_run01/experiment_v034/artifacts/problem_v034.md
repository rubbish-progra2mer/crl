# Problem v034

## Bounded question

Can deterministic tool-contract evidence projections plus a calibrated
weakest-obligation score improve a frozen 0.6B model's pairwise next-action
judgment across held-out ToolPRMBench sources?

## Observable failure

Tool-use actions can be locally plausible while failing exactly one mandatory
condition: using the wrong interaction mode or tool, violating an argument
schema, inventing a value, or ignoring a prerequisite and prior state.
Holistic reward judgments and mean aggregation can allow strong surface
plausibility on other dimensions to mask that single failure.

## Falsifiable hypothesis

Under leave-one-source-out Development over GTA, BFCL and ToolTalk, the minimum
cross-source empirical percentile of five fixed pointwise obligation log odds
will improve pairwise accuracy over every mandatory comparator. The comparator
set includes the same model's holistic score, every individual obligation, raw
minimum, calibrated mean and product, pairwise majority, an
other-source-selected single obligation and a supervised linear ensemble using
the same five logits.

## Exclusions

The experiment does not execute tools, reconstruct environment state, prove
correctness, generate rubrics, train or fine-tune the language model, identify
causal error types, measure search performance, or establish online safety. It
does not claim that 0.6B is a strong general judge. A failure is a negative
result for the fixed computation, not permission to tune prompts, obligations,
aggregation, thresholds or model size.
