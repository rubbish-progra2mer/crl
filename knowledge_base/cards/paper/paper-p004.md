<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p004","card_kind":"paper","paper_id":"P004","evidence_ids":["ev-p004-failure-core"],"source_refs":[{"path":"papers/P004_travelplanner.pdf","sha256":"a7c7edd67c90e9997e940aaa7b435d46a8b201ed119c125b341b01b215454133"}]} -->
# TravelPlanner: A Benchmark for Real-World Planning with Language Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] Failure/evaluation anchor for multi-constraint real-world planning.

## Problem and setting
[CODEX_SYNTHESIS] Travel itineraries must satisfy hard, commonsense, and environment constraints while using a closed tool sandbox.

## Changed computation
[CODEX_SYNTHESIS] The contribution changes evaluation, not the agent: plans are checked against structured constraints and tool-grounded records.

## Evidence-backed findings
[AUTHOR_FACT] TravelPlanner makes constrained-plan validity and delivery failures observable. [[evidence:ev-p004-failure-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] The benchmark does not identify a universally effective planning operator; extraction and domain design can affect measured success.

## Lineage and baselines
[CODEX_SYNTHESIS] Strong carrier for testing whether a planning method improves constraint satisfaction rather than answer fluency.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p004-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] TravelPlanner; constrained planning; hard constraints; commonsense constraints; plan validity

