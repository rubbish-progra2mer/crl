<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-outcome-trained-execution-state-planner","card_kind":"operator","paper_id":"P021","evidence_ids":["ev-p021-operator-core"],"source_refs":[{"path":"papers/P021_agentflow.pdf","sha256":"33e04a3fa3ac197e69c2fffd5f53a274c80872a515a6269bc98ae7d4105f7095"}]} -->
# Outcome-Trained Planner over Explicit Execution State

## Intervention target
[CODEX_SYNTHESIS] The planner inside a tool-integrated loop, not the executor, verifier, or final answer generator.

## Before and after computation
[CODEX_SYNTHESIS] A frozen or offline-trained planner acts under deployment-state shift. The changed computation updates the planner on policy while tool results and verifier feedback change the current state.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: task plus current knowledge/memory/tool feedback state. Output: next planned action. Timing: before each execution step; training signal arrives from terminal outcome.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] On-policy exposure should align planning decisions with the state distribution produced by the active scaffold.

## Predicted observable signature
[CODEX_HYPOTHESIS] Improvement should concentrate on multi-turn replanning after tool/verifier observations, not merely on longer answers.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Sparse terminal reward is broadcast across turns, external judges add information, and unequal budgets prevent attributing all system gains to planner learning.

## Source lineage
[CODEX_SYNTHESIS] ReAct execution loop → offline planner tuning → in-flow outcome-trained planner.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p021-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Flow-GRPO; in-flow planner; explicit execution state; on-policy agent planning; sparse trajectory reward

