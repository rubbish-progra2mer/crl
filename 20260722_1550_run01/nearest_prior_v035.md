# Nearest Prior v035

## ToolPRMBench

ToolPRMBench defines the exact carrier: interaction history, tool metadata, a
correct next action and a plausible rejected action. It evaluates general and
tool-specialized process reward models. v035 does not claim the benchmark,
pairwise task or tool-specific evaluation.

Frozen PDF SHA-256:
`f7ac155d9862f0def0b1f5c09e992dc7b626fdf90601a8cb2e8a9bcbd6712455`.

## ToolRM

ToolRM is the closest tool-specific learned evaluator. It builds pairwise
preference data, trains generative and discriminative critics, randomizes
response order and evaluates both orders. It consumes the full context and
candidate responses. v035 does not train a reward model and cannot claim
generic pairwise critique, position control or tool-call matching.

Frozen PDF SHA-256:
`9679fe106dfc881cfdaf7e77cd6b38c871da2e503b4964f91f2fe0a8293f714f`.

## PRePair

PRePair independently reasons about each full response before making a final
pairwise choice. It directly collides with any broad pointwise-before-pairwise
Claim. v035 instead compiles a symmetric, deterministic representation of only
the fields that differ. Independent full pointwise scoring is mandatory as a
control.

Frozen PDF SHA-256:
`8735b209a569f7b6d06b90b3c3dc970013ae0bbc23849032fe7ec6ff417549b9`.

## Pairwise or Pointwise

This work formalizes distracted evaluation and reports that pairwise
preferences are more vulnerable than absolute scores to irrelevant
assertiveness, prolixity and sycophancy perturbations. It motivates but does
not instantiate tool-action field localization. v035 must beat a pointwise
control; a gain over full pairwise alone is insufficient.

Frozen PDF SHA-256:
`1257158555afd20ec4c52e9ae37d26ee70c4448b6070f64a54592b8021d7412e`.

## SCOPE

SCOPE's Bidirectional Preference Entropy scores both response orders and
aggregates aligned probabilities before conformal selection. Therefore
bidirectional probability aggregation and order invariance are prior art and
serve only as a required control in v035. v035 makes no conformal-risk Claim.

Frozen PDF SHA-256:
`7211f2e58739ff480279d3cbeddc8877c6bf41f0f023ed1b04d4bc727f936a08`.

## Collision judgment

Every component except the exact field-difference evidence projection is
covered by prior work. The only potentially supportable contribution is the
complete fixed projection under matched-model controls, cross-source
Development and untouched ToolSandbox Confirmation. Failure against full
pointwise, full pairwise or evidence-free difference scoring is a direct
method-level falsification.

