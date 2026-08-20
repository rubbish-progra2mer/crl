<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p050","card_kind":"paper","paper_id":"P050","evidence_ids":["ev-p050-operator-core"],"source_refs":[{"path":"papers/P050_agentic_verifier.pdf","sha256":"81b1a3759a4de1b246240342435ef32f0f7d7265d17a938bd78086fe027b8654"}]} -->
# Scaling Agentic Verifier for Competitive Coding

## Role in the knowledge base
[CODEX_SYNTHESIS] Test-time verifier source using active counterexample search.

## Problem and setting
[CODEX_SYNTHESIS] Competitive-programming candidates can be executed on generated inputs and reranked.

## Changed computation
[CODEX_SYNTHESIS] The verifier actively proposes inputs that maximize behavioral divergence among candidate programs.

## Evidence-backed findings
[AUTHOR_FACT] The evidence supports active discriminative test generation rather than random sampling. [[evidence:ev-p050-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Output disagreement does not reveal which program is correct; validators and majority outputs are not formal truth, and compute is unequal.

## Lineage and baselines
[CODEX_SYNTHESIS] Transfers search and verifier mechanisms into a code testbed.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p050-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Agentic Verifier; counterexample search; discriminative input; execution reranking; behavioral divergence

