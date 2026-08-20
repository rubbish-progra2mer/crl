# Problem v032

## Bounded question

Can a successful-only, cross-task task-to-action normal map expose rewarded
serious exploits that a direct supervised action-text detector and an ordinary
task/action concatenation detector miss?

## Observable failure

Terminal Wrench contains legitimate successful trajectories and real rewarded
serious exploits for the same broad task population. Its stripped variant
removes explicit hack reasoning but preserves task descriptions, commands and
terminal outputs. Earlier Run versions show that direct lexical detection is
strong, while fixed operation-role relevance and ordinary task concatenation do
not reliably capture task-specific abnormality.

## Falsifiable hypothesis

Across held-out task folds and held-out generator families, the absolute
innovation relative to a normal-action map learned only from successful
training trajectories will improve AUC over every mandatory comparator,
including direct text, task concatenation, raw latent addition, an identity
task/action residual and an all-row conditional map.

## Exclusions

The experiment does not infer intent, identify a causal exploit step, verify
environment state, use exploit categories, use reasoning traces, use a
same-task successful support, or establish online safety. A failure is a
negative result for this fixed computation, not permission to retune it.

