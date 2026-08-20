<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p036","card_kind":"paper","paper_id":"P036","evidence_ids":["ev-p036-failure-core"],"source_refs":[{"path":"papers/P036_tau_knowledge.pdf","sha256":"f6fbe657daa349b1495bef6fecd7b1a3c845da3bf296d2589eedb45e051613bd"}]} -->
# tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge

## Role in the knowledge base
[CODEX_SYNTHESIS] Evaluation carrier for knowledge discovery and use inside conversational agents.

## Problem and setting
[CODEX_SYNTHESIS] Procedural documents, tool discovery, database state, and user interaction are jointly required.

## Changed computation
[CODEX_SYNTHESIS] The benchmark contrasts retrieval interfaces with gold documents and full context to separate access from use.

## Evidence-backed findings
[AUTHOR_FACT] Even gold documents leave a large failure gap, so retrieval is not the only bottleneck. [[evidence:ev-p036-failure-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Gold context is an oracle analysis condition; simulator and interface differences affect absolute scores.

## Lineage and baselines
[CODEX_SYNTHESIS] Tests whether memory/retrieval methods change downstream decision computation.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p036-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] tau-Knowledge; gold documents; knowledge use; procedural reasoning; tool discovery

