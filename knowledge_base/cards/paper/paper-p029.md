<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p029","card_kind":"paper","paper_id":"P029","evidence_ids":["ev-p029-failure-core"],"source_refs":[{"path":"papers/P029_memfail.pdf","sha256":"7649a407d54058c425fa7f6ea1dc8551288e16bac24ff0e1bad1e0ec90315d8d"}]} -->
# MemFail: Stress-Testing Failure Modes of LLM Memory Systems

## Role in the knowledge base
[CODEX_SYNTHESIS] Failure-localization framework for external-memory systems.

## Problem and setting
[CODEX_SYNTHESIS] Memory systems decomposed across storage, retrieval, and answer generation under controlled stress tests.

## Changed computation
[CODEX_SYNTHESIS] MemFail evaluates lifecycle operations separately instead of reporting only final QA accuracy.

## Evidence-backed findings
[AUTHOR_FACT] The evidence supports stage-specific failure diagnosis and architecture-specific failure profiles. [[evidence:ev-p029-failure-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Synthetic tasks and oracle diagnostic views are not deployable runtime operators.

## Lineage and baselines
[CODEX_SYNTHESIS] Extends memory-stage decomposition with explicit negative tests.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p029-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MemFail; memory lifecycle failure; storage error; retrieval error; answer reasoning error

