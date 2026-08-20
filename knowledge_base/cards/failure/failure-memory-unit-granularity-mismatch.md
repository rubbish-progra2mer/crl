<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-memory-unit-granularity-mismatch","card_kind":"failure","paper_id":"P011","evidence_ids":["ev-p011-failure-core"],"source_refs":[{"path":"papers/P011_secom.pdf","sha256":"998ab05ece554a83870b1baf5762f314837165e99f22ef2af8ffd7ba473c5004"}]} -->
# Memory Unit Granularity Creates Retrieval and Semantic Loss

## Observed failure
[AUTHOR_FACT] Turn-, session-, and summary-level memory units exhibit different retrieval and semantic-quality failures. [[evidence:ev-p011-failure-core]]

## Conditions and scope
[CODEX_SYNTHESIS] Personalized long-term conversations stored as external memory and retrieved for response generation.

## Failed intervention
[CODEX_SYNTHESIS] A fixed memory unit either fragments related information or merges too much unrelated/noisy context.

## Evidence and alternative explanations
[CODEX_SYNTHESIS] Compression, retrieval model, and segmentation quality also contribute; granularity is not the only causal variable.

## Warning for future candidates
[CODEX_SYNTHESIS] Do not propose another memory store without specifying the unit of storage and testing retrieval plus downstream use.

## Possible repair boundary
[CODEX_HYPOTHESIS] Task-adaptive or coherent segmentation is plausible, but must be compared with turn/session/summary baselines under equal context.

## Evidence ledger
[AUTHOR_FACT] The cited passages bind this failure to admitted PDF bytes and current Passage SHA values. [[evidence:ev-p011-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] memory granularity; fragmentation; session memory; summary loss; segment retrieval

