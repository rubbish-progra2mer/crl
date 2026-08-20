<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p013","card_kind":"paper","paper_id":"P013","evidence_ids":["ev-p013-intrinsic-self-correction-degrades","ev-p013-oracle-free-equal-budget-boundary"],"source_refs":[{"path":"papers/P013_intrinsic_self_correction_limits.pdf","sha256":"d172f0b3e933544f5165250338e3e989036e8d826fea34093e6aed4adb5b042a"}]} -->
# Large Language Models Cannot Self-Correct Reasoning Yet

## Role in the knowledge base
[CODEX_SYNTHESIS] Core negative evidence for intrinsic self-correction without external feedback.

## Problem and setting
[CODEX_SYNTHESIS] Reasoning tasks comparing initial answers, repeated self-correction, and equal-response alternatives.

## Changed computation
[CODEX_SYNTHESIS] The evaluated intervention asks a model to reconsider its own output without adding an external verifier or new evidence.

## Evidence-backed findings
[AUTHOR_FACT] The source reports no reliable improvement and occasional degradation without oracle labels, including under equal-response comparisons. [[evidence:ev-p013-intrinsic-self-correction-degrades]]

## Limitations and failure signals
[CODEX_SYNTHESIS] It does not refute tool-grounded critique, external feedback, stronger selectors, or all task domains.

## Lineage and baselines
[CODEX_SYNTHESIS] Contradicts broad claims that generic self-reflection is sufficient and sets a strong baseline boundary for reflection methods.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p013-intrinsic-self-correction-degrades]] [[evidence:ev-p013-oracle-free-equal-budget-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] intrinsic self-correction; no external feedback; equal response budget; oracle-free refinement; degradation

