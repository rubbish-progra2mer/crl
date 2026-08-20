<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p030","card_kind":"paper","paper_id":"P030","evidence_ids":["ev-p030-failure-core"],"source_refs":[{"path":"papers/P030_stale_memory.pdf","sha256":"388f71f1eb952e7d7e7b19c2f25bfc744c47efa8ee00a548093b949432495109"}]} -->
# STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?

## Role in the knowledge base
[CODEX_SYNTHESIS] Core negative evidence for stale or conflicting memory.

## Problem and setting
[CODEX_SYNTHESIS] Agents must recognize an implicit update, resist obsolete premises, and make later actions follow current state.

## Changed computation
[CODEX_SYNTHESIS] STALE separates recognition from policy application; CUPMEM adjudicates state at write time with typed constraints.

## Evidence-backed findings
[AUTHOR_FACT] The evidence shows that retrieving an update does not guarantee it gains decision authority. [[evidence:ev-p030-failure-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Attention analysis is diagnostic, and the full CUPMEM result combines multiple extra computations.

## Lineage and baselines
[CODEX_SYNTHESIS] Moves memory research beyond retrieval recall toward state conflict resolution.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p030-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] STALE; stale memory; implicit conflict; premise resistance; decision authority; write-side adjudication

