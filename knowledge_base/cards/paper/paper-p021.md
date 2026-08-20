<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p021","card_kind":"paper","paper_id":"P021","evidence_ids":["ev-p021-operator-core"],"source_refs":[{"path":"papers/P021_agentflow.pdf","sha256":"33e04a3fa3ac197e69c2fffd5f53a274c80872a515a6269bc98ae7d4105f7095"}]} -->
# In-the-Flow Agentic System Optimization for Effective Planning and Tool Use

## Role in the knowledge base
[CODEX_SYNTHESIS] Agent-learning operator source for training a planner inside an active tool/verifier flow.

## Problem and setting
[CODEX_SYNTHESIS] Long-horizon tool-integrated tasks with an evolving execution state and sparse outcome rewards.

## Changed computation
[CODEX_SYNTHESIS] Flow-GRPO updates the planner on policy while executor, verifier, and solution generator remain in the loop.

## Evidence-backed findings
[AUTHOR_FACT] The evidence supports in-flow planner optimization over explicit execution state. [[evidence:ev-p021-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Trajectory reward is broadcast across turns; external judges and unequal system budgets prevent clean system-level attribution.

## Lineage and baselines
[CODEX_SYNTHESIS] Combines ReAct-style execution with outcome-trained planning; closest baselines are frozen and SFT planners in the same scaffold.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p021-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Flow-GRPO; in-the-flow optimization; outcome-trained planner; sparse reward; tool-integrated planning

