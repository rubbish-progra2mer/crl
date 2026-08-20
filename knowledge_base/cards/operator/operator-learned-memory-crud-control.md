<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-learned-memory-crud-control","card_kind":"operator","paper_id":"P028","evidence_ids":["ev-p028-operator-core"],"source_refs":[{"path":"papers/P028_memory_r1.pdf","sha256":"c206af4e792e9550f2aaec8a6c4d9b141d1ddcb587e781d7866870c8f3e4dd4f"}]} -->
# Outcome-Trained Memory CRUD and Use Control

## Intervention target
[CODEX_SYNTHESIS] What an agent stores, updates, deletes, ignores, and later uses.

## Before and after computation
[CODEX_SYNTHESIS] A heuristic memory pipeline writes and retrieves entries with fixed rules. The changed computation learns explicit ADD/UPDATE/DELETE/NOOP control and a separate answer-time selector.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: recent interaction, current memory bank, and candidate retrieved memories. Output: memory operation and evidence-conditioned answer. Timing: write control precedes storage; use control precedes answering.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Outcome learning can optimize memory state and downstream evidence use jointly rather than only retrieval similarity.

## Predicted observable signature
[CODEX_HYPOTHESIS] Gains should persist under matched retrieval candidates and should appear in update/delete decisions, not only larger context.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Training compute, external model assets, conflicting context-window descriptions, and coupled manager/answer learning limit transfer claims.

## Source lineage
[CODEX_SYNTHESIS] Virtual memory paging → heuristic memory CRUD → outcome-trained write/read control.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p028-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Memory-R1; learned memory management; ADD UPDATE DELETE NOOP; memory manager; answer agent

