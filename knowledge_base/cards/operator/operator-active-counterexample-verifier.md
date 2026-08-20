<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-active-counterexample-verifier","card_kind":"operator","paper_id":"P050","evidence_ids":["ev-p050-operator-core"],"source_refs":[{"path":"papers/P050_agentic_verifier.pdf","sha256":"81b1a3759a4de1b246240342435ef32f0f7d7265d17a938bd78086fe027b8654"}]} -->
# Active Counterexample-Seeking Verifier

## Intervention target
[CODEX_SYNTHESIS] Test inputs used to distinguish candidate implementations at inference time.

## Before and after computation
[CODEX_SYNTHESIS] Random inputs or fixed generated tests weakly separate programs. The changed computation iteratively proposes executable inputs that maximize behavioral divergence.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: problem plus pairs or sets of candidate programs and execution outputs. Output: discriminative test inputs and consistency evidence. Timing: after candidate generation, before reranking.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Active search should spend execution budget on regions where candidates disagree rather than redundant random cases.

## Predicted observable signature
[CODEX_HYPOTHESIS] At matched sandbox-call and token budgets, generated inputs should produce more informative divergences and better reranking.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Divergence proves non-equivalence but not correctness; generated validators and majority outputs are not formal truth.

## Source lineage
[CODEX_SYNTHESIS] Execution reranking → random differential testing → agentic counterexample search.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p050-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Agentic Verifier; counterexample input; behavioral divergence; execution reranking; active test generation

