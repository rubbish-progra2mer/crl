<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-write-side-state-adjudication","card_kind":"operator","paper_id":"P030","evidence_ids":["ev-p030-failure-core","ev-p030-write-side-adjudication","ev-p030-authorized-readout"],"source_refs":[{"path":"papers/P030_stale_memory.pdf","sha256":"388f71f1eb952e7d7e7b19c2f25bfc744c47efa8ee00a548093b949432495109"}]} -->
# Write-Side State Adjudication for Conflicting Memory

## Intervention target
[CODEX_SYNTHESIS] Which memory claim has authority when new evidence implicitly invalidates old state.

## Before and after computation
[CODEX_SYNTHESIS] Old and new memories are both retrieved and the answer model must resolve them late. The changed computation adjudicates typed state during writes and constrains later readout to current state.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: existing state, new assertion, type and dependency relations. Output: updated authoritative state plus constrained readout. Timing: conflict resolution occurs before future retrieval/use.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Moving conflict resolution earlier should prevent stale facts from remaining equally available at decision time.

## Predicted observable signature
[CODEX_HYPOTHESIS] Downstream policy adaptation should improve even when raw retrieval recall is held constant.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] The evaluated system combines schemas, propagation search, and constrained readout; attention is not causal evidence.

## Source lineage
[CODEX_SYNTHESIS] Retrieval memory → stale-memory diagnosis → write-side authority control.

## Evidence ledger
[AUTHOR_FACT] The source separates the recognition/application failure from write-side state revision and readout grounded only in adjudicated state. [[evidence:ev-p030-failure-core]] [[evidence:ev-p030-write-side-adjudication]] [[evidence:ev-p030-authorized-readout]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] STALE; CUPMEM; implicit conflict; write-side adjudication; memory authority; policy adaptation
