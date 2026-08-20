<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p044","card_kind":"paper","paper_id":"P044","evidence_ids":["ev-p044-evaluation-core"],"source_refs":[{"path":"papers/P044_deer.pdf","sha256":"bb262ad8999adb3feb46f3373db45815f31f16b714f02fe732c47625810cf42a"}]} -->
# DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation

## Role in the knowledge base
[CODEX_SYNTHESIS] Expert-report evaluation carrier with task-specific guidance and claim typing.

## Problem and setting
[CODEX_SYNTHESIS] Expert deep-research reports across multidisciplinary questions.

## Changed computation
[CODEX_SYNTHESIS] DEER combines granular rubrics, expert guidance, claim classification, semantic citation backtracking, and verification.

## Evidence-backed findings
[AUTHOR_FACT] The evidence supports a multi-layer report and claim evaluation protocol. [[evidence:ev-p044-evaluation-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Unknown-source claims are not all directly fact-checked; gold claim sets are small and task selection excludes hard-to-evaluate items.

## Lineage and baselines
[CODEX_SYNTHESIS] Refines generic LLM judging with task-specific evaluation cues.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p044-evaluation-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] DEER; expert guidance; claim taxonomy; semantic backtracking; information verification

