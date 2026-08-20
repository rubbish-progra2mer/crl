<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p009","card_kind":"paper","paper_id":"P009","evidence_ids":["ev-p009-operator-core"],"source_refs":[{"path":"papers/P009_memgpt.pdf","sha256":"9f674bcff69c86f11c813dcfad613d8841f5f8ed17979e3c4df06a91df7762e0"}]} -->
# MemGPT: Towards LLMs as Operating Systems

## Role in the knowledge base
[CODEX_SYNTHESIS] Direct ancestor for explicit context and memory tier control.

## Problem and setting
[CODEX_SYNTHESIS] Long documents and multi-session conversations that exceed the underlying model context window.

## Changed computation
[CODEX_SYNTHESIS] MemGPT introduces virtual context management that pages information across limited in-context memory and external storage.

## Evidence-backed findings
[AUTHOR_FACT] The source frames long-context handling as hierarchical storage control rather than one-shot retrieval. [[evidence:ev-p009-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Paging policies, model prompting, and storage organization are coupled; it is not evidence that more stored text alone helps.

## Lineage and baselines
[CODEX_SYNTHESIS] Precedes later learned memory CRUD, compression, and state-adjudication mechanisms.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p009-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MemGPT; virtual context management; paging; memory tiers; context overflow

