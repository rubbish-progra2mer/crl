<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p032","card_kind":"paper","paper_id":"P032","evidence_ids":["ev-p032-operator-core"],"source_refs":[{"path":"papers/P032_critic.pdf","sha256":"30a3161dbbb9531528bf410bd1df84eeb9ada8151f614789ae80ca86b7b32c7e"}]} -->
# CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing

## Role in the knowledge base
[CODEX_SYNTHESIS] Direct source for tool-grounded self-correction.

## Problem and setting
[CODEX_SYNTHESIS] Question answering, code, mathematics, and toxicity tasks where external tools can validate outputs.

## Changed computation
[CODEX_SYNTHESIS] CRITIC calls a task-appropriate tool after generation and conditions revision on returned feedback.

## Evidence-backed findings
[AUTHOR_FACT] The evidence distinguishes external validation from intrinsic introspection. [[evidence:ev-p032-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Corrections are non-monotonic; some settings share feedback and evaluator sources, and oracle variants are not deployable.

## Lineage and baselines
[CODEX_SYNTHESIS] Contrasts with intrinsic self-correction and precedes verifier-gated refinement.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p032-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] CRITIC; tool-interactive critiquing; external feedback; validation then revision; non-monotonic correction

