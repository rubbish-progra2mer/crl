# Nearest Prior v037

## Toolformer

Toolformer is the nearest likelihood-based tool-use ancestor. It samples API
calls, executes them and retains calls whose result lowers loss on subsequent
natural-text tokens, then finetunes the language model. ECDS does not execute a
call, predict downstream text or train. It measures evidence-induced
likelihood change on aligned differential positions of two already proposed
actions.

Frozen PDF SHA-256:
`6d7483d94653008e40c2058a1c22441c92e3713dae278b6361e8efc447c99522`.

## ToolRM

ToolRM trains generative and discriminative pairwise tool-action reward models
from preference data. ECDS is training-free, separately scores each action and
contains no pairwise verdict label. Generic tool-action evaluation and
likelihood-based preference are not novel.

Frozen PDF SHA-256:
`9679fe106dfc881cfdaf7e77cd6b38c871da2e503b4964f91f2fe0a8293f714f`.

## ToolPRMBench

ToolPRMBench supplies the pairwise step-judgment carrier. ECDS claims neither
the task nor its data.

Frozen PDF SHA-256:
`f7ac155d9862f0def0b1f5c09e992dc7b626fdf90601a8cb2e8a9bcbd6712455`.

## Collision ceiling

Sequence likelihood, differential tokens and counterfactual subtraction are
not individually novel. The only testable contribution is their fixed
composition under matched controls, multi-source Development and untouched
Confirmation. Even a pass supports only next-action ranking, not Agent utility.
