<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p011","card_kind":"paper","paper_id":"P011","evidence_ids":["ev-p011-failure-core"],"source_refs":[{"path":"papers/P011_secom.pdf","sha256":"998ab05ece554a83870b1baf5762f314837165e99f22ef2af8ffd7ba473c5004"}]} -->
# On Memory Construction and Retrieval for Personalized Conversational Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] Mechanism/failure anchor for memory-unit granularity.

## Problem and setting
[CODEX_SYNTHESIS] Personalized long-term conversation memory constructed from turns, sessions, summaries, or coherent segments.

## Changed computation
[CODEX_SYNTHESIS] SECOM segments conversations and compresses each segment before retrieval.

## Evidence-backed findings
[AUTHOR_FACT] The source reports that memory-unit granularity affects both retrieval accuracy and semantic quality. [[evidence:ev-p011-failure-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Segmentation and compression are combined, so improvements cannot be assigned to granularity alone.

## Lineage and baselines
[CODEX_SYNTHESIS] Refines static retrieval memory and motivates failure cards about fragmentation and lossy summaries.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p011-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] SECOM; memory granularity; turn memory; session memory; segment memory; compression denoising

