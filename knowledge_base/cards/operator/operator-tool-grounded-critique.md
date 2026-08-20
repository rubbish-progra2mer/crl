<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-tool-grounded-critique","card_kind":"operator","paper_id":"P032","evidence_ids":["ev-p032-operator-core"],"source_refs":[{"path":"papers/P032_critic.pdf","sha256":"30a3161dbbb9531528bf410bd1df84eeb9ada8151f614789ae80ca86b7b32c7e"}]} -->
# Tool-Grounded Critique and Revision

## Intervention target
[CODEX_SYNTHESIS] The evidence available to an agent when deciding whether and how to revise an output.

## Before and after computation
[CODEX_SYNTHESIS] Intrinsic reflection re-reads the same answer. The changed computation invokes a task-relevant external tool, then conditions revision on returned validation evidence.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: draft output and tool interface. Output: tool feedback and revised output. Timing: after drafting and before final delivery.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] External observations can reveal errors unavailable from the model's unchanged internal context.

## Predicted observable signature
[CODEX_HYPOTHESIS] Benefits should track tool informativeness; a no-tool critique should underperform while harmful revisions remain measurable.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Corrections are non-monotonic, feedback and evaluator may share sources, and oracle-gated variants are not deployable.

## Source lineage
[CODEX_SYNTHESIS] Intrinsic reflection → external critique → verifier/stopping control.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p032-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] CRITIC; tool-interactive critiquing; external validation; feedback-conditioned revision; correction harm

