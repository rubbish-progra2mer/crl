<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p047","card_kind":"paper","paper_id":"P047","evidence_ids":["ev-p047-evaluation-core"],"source_refs":[{"path":"papers/P047_tau2_bench.pdf","sha256":"0817e3fd33915326180d548caa900dcc5cba42ded27688105d8ce2f7e73aad84"}]} -->
# tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment

## Role in the knowledge base
[CODEX_SYNTHESIS] Evaluation carrier for dual-control conversational agents.

## Problem and setting
[CODEX_SYNTHESIS] Agent and user each have private observations and tools that modify a shared dynamic world.

## Changed computation
[CODEX_SYNTHESIS] Tau2-Bench makes both participants active controllers and validates state transitions.

## Evidence-backed findings
[AUTHOR_FACT] The evidence captures coordination and information asymmetry absent from single-control tasks. [[evidence:ev-p047-evaluation-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Dual control is implemented in one domain; user-simulator errors and oracle plans limit interpretation.

## Lineage and baselines
[CODEX_SYNTHESIS] Extends tau-bench terminal-state evaluation with user-side action.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p047-evaluation-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] tau2-Bench; dual control; shared environment; user tools; Dec-POMDP

