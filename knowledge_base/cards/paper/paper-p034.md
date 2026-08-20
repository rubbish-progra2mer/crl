<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p034","card_kind":"paper","paper_id":"P034","evidence_ids":["ev-p034-failure-core"],"source_refs":[{"path":"papers/P034_refinebench.pdf","sha256":"ee5c4d93ddf6c0741f0d08042b6aca2e0f08c3d3bd70e6cc6c90378bbc2d8c7f"}]} -->
# RefineBench: Evaluating Refinement Capability of Language Models via Checklists

## Role in the knowledge base
[CODEX_SYNTHESIS] Narrow negative benchmark for repeated self-refinement.

## Problem and setting
[CODEX_SYNTHESIS] Checklist-derived tasks with minimal self-refinement prompts and guided feedback controls.

## Changed computation
[CODEX_SYNTHESIS] The benchmark measures transitions across repeated revisions instead of only final aggregate accuracy.

## Evidence-backed findings
[AUTHOR_FACT] The evidence shows that later revisions can corrupt initially correct answers. [[evidence:ev-p034-failure-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] The result is prompt-, model-, domain-, and evaluator-specific and does not refute all external or targeted feedback.

## Lineage and baselines
[CODEX_SYNTHESIS] Constrains Self-Refine claims and motivates verification/stopping gates.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p034-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] RefineBench; correct-to-incorrect transition; refinement degradation; checklist feedback; stopping

