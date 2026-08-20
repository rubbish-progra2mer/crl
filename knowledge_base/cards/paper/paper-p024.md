<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p024","card_kind":"paper","paper_id":"P024","evidence_ids":["ev-p024-operator-core"],"source_refs":[{"path":"papers/P024_multiagent_debate.pdf","sha256":"80ecf57b31f248e6ce234412618aa6001d19630a9de0cf18c24cb60ae3a8054d"}]} -->
# Improving Factuality and Reasoning in Language Models through Multiagent Debate

## Role in the knowledge base
[CODEX_SYNTHESIS] Direct ancestor for peer-answer exposure and iterative multi-agent critique.

## Problem and setting
[CODEX_SYNTHESIS] Multiple model instances independently answer, inspect peers, revise, and aggregate.

## Changed computation
[CODEX_SYNTHESIS] Debate adds cross-trajectory peer responses before final revision and majority aggregation.

## Evidence-backed findings
[AUTHOR_FACT] The source establishes peer-exposure computation, not independent evidence verification. [[evidence:ev-p024-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Token cost is substantially higher and consensus may converge to a shared error.

## Lineage and baselines
[CODEX_SYNTHESIS] Ancestor for debate controllers, topology studies, and contribution diagnostics.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p024-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] multiagent debate; peer critique; iterative revision; majority vote; consensus error

