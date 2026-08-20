# Research Problem v035

## Setting

Input is an interaction history, tool metadata and two plausible next actions.
Exactly one action is preferred by the benchmark. The evaluation target is
pairwise classification accuracy, not task execution success.

## Failure under study

Plausible action pairs often share tool names, arguments, explanatory text or
interaction context while differing in only one operational field. A small
judge that reads the full pair may overweight shared content, verbosity or
presentation. A pointwise judge may discard the fact that the decision turns
on a specific contrast.

## Question

Can deterministic localization of the non-shared operational fields, grounded
in the frozen history and implicated tool contracts, improve an
order-symmetric frozen Qwen3-0.6B judge over matched full-input controls on
multi-source ToolPRMBench Development and untouched ToolSandbox
Confirmation?

## Scope

This is not:

- a new reward-model training method;
- an executable verifier or formal contract checker;
- a general solution to LLM-judge bias;
- a claim that pairwise evaluation dominates pointwise evaluation;
- a claim about downstream Agent task success.

The strongest possible Claim is limited to pairwise next-action judgment under
the fixed data, model, projections, controls and gates.
