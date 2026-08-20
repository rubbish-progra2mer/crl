<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-milestone-dag-trajectory-evaluation","card_kind":"operator","paper_id":"P037","evidence_ids":["ev-p037-evaluation-core","ev-p037-minefield-violation"],"source_refs":[{"path":"papers/P037_toolsandbox.pdf","sha256":"3449baed1d8e0f4c07dbc859621899685eed8a6a0445a1ae8909c178e6b6173e"}]} -->
# Milestone-DAG Multi-Path Trajectory Evaluation

## Intervention target
[CODEX_SYNTHESIS] Evaluation of stateful tool trajectories that may have multiple valid action orders.

## Before and after computation
[CODEX_SYNTHESIS] A trace must match one reference sequence or is judged only at the final response. The changed computation aligns achieved milestones under DAG ordering and checks minefields.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: interaction trace, milestone DAG, minefield conditions, environment state. Output: path-aware progress and violation measures. Timing: after a rollout.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Partial progress and alternative valid paths become observable without treating one reference as the only solution.

## Predicted observable signature
[CODEX_HYPOTHESIS] Semantically equivalent action orders should receive similar credit while state violations remain detectable.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Human milestones encode process priors; simulator errors and inaction can inflate submetrics.

## Source lineage
[CODEX_SYNTHESIS] Exact trajectory match → terminal state checks → milestone-DAG multi-path scoring.

## Evidence ledger
[AUTHOR_FACT] The source defines path-aware milestone-DAG matching and minefields that zero the trajectory score when prohibited events occur. [[evidence:ev-p037-evaluation-core]] [[evidence:ev-p037-minefield-violation]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] ToolSandbox; milestone DAG; minefield; multi-path evaluation; stateful trajectory
