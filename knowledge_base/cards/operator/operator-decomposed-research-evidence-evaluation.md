<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-decomposed-research-evidence-evaluation","card_kind":"operator","paper_id":null,"evidence_ids":["ev-p042-evaluation-core","ev-p043-evaluation-core","ev-p044-evaluation-core"],"source_refs":[{"path":"papers/P042_live_research_bench.pdf","sha256":"579b9728b76cfd242e9c94d9ff2985e196bbc72b5a741030e4f308ede04a4f69"},{"path":"papers/P043_deepresearch_bench.pdf","sha256":"8fbf30398f5e62f8839f0c9c8609bbb9e3cd0b57ae27d4bf33cb5db2007d1118"},{"path":"papers/P044_deer.pdf","sha256":"bb262ad8999adb3feb46f3373db45815f31f16b714f02fe732c47625810cf42a"}]} -->
# Decomposed Research-Report Evidence Evaluation

## Intervention target
[CODEX_SYNTHESIS] Whether a long research report satisfies its task and whether individual claims are supported by accessible sources.

## Before and after computation
[CODEX_SYNTHESIS] A single LLM judge emits one holistic score. The changed computation separates report dimensions, statement/claim extraction, citation association, source support, and task-specific expert guidance.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: research task, report, citations, fetched source content, optional expert guidance. Output: dimension scores plus claim-level support records. Timing: after report generation.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Separating task fulfillment from evidence support exposes a mechanism that improves prose while weakening factual grounding.

## Predicted observable signature
[CODEX_HYPOTHESIS] Candidate comparisons should report narrow claim-support and task-fulfillment deltas, not only one overall judge preference.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Reference/judge family dependence, dynamic web content, proprietary budgets, preprocessing, and uncovered uncited claims remain measurement risks.

## Source lineage
[CODEX_SYNTHESIS] Holistic judge → checklist dimensions → statement-source support → task-specific expert guidance.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p042-evaluation-core]] [[evidence:ev-p043-evaluation-core]] [[evidence:ev-p044-evaluation-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] DeepEval; FACT; DEER; claim-level verification; citation support; expert guidance; deep research evaluation

