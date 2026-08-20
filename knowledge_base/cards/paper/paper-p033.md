<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p033","card_kind":"paper","paper_id":"P033","evidence_ids":["ev-p033-operator-core"],"source_refs":[{"path":"papers/P033_self_refine.pdf","sha256":"a07dfc5ada4ff818c77812dd581065a4e3e40f5736f2f36a97787a66da6e7825"}]} -->
# Self-Refine: Iterative Refinement with Self-Feedback

## Role in the knowledge base
[CODEX_SYNTHESIS] Canonical source for same-model iterative feedback and refinement.

## Problem and setting
[CODEX_SYNTHESIS] Seven heterogeneous generation tasks using one model as generator, feedback provider, and refiner.

## Changed computation
[CODEX_SYNTHESIS] Self-Refine repeatedly feeds the model's critique and revision history back without updating parameters.

## Evidence-backed findings
[AUTHOR_FACT] The evidence defines the full iterative protocol. [[evidence:ev-p033-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] No unified equal-budget baseline isolates self-feedback; task prompts, stopping, selectors, and occasional oracle information vary.

## Lineage and baselines
[CODEX_SYNTHESIS] Stronger positive prior than generic reflection, but bounded by intrinsic-correction negatives and RefineBench.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p033-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Self-Refine; self-feedback; iterative refinement; same-model critic; stopping rule

