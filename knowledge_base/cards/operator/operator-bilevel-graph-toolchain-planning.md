<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-bilevel-graph-toolchain-planning","card_kind":"operator","paper_id":"P048","evidence_ids":["ev-p048-operator-core"],"source_refs":[{"path":"papers/P048_naviagent.pdf","sha256":"d7578b55678c89f2ffb78741c5faab8adf7c70e7e4160d2cd5fafea522e192ab"}]} -->
# Bilevel Graph-Conditioned Toolchain Planning

## Intervention target
[CODEX_SYNTHESIS] Separation of high-level interaction decisions from low-level API-chain construction.

## Before and after computation
[CODEX_SYNTHESIS] A monolithic planner emits a complete API sequence. The changed computation selects direct/clarify/retrieve/execute modes while a graph layer constructs and revises toolchains.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: user request, tool/parameter graph, current execution state. Output: interaction mode and feasible tool path. Timing: mode selection precedes graph execution and can recur.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Decoupling may reduce high-level search while preserving structured feasibility at the tool layer.

## Predicted observable signature
[CODEX_HYPOTHESIS] Benefits should remain when model calls and tool descriptions are matched, with gains localized to dependency-heavy tasks.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Evidence is limited by synthetic chains, unequal calls, external judges, and weakly specified dynamic recovery.

## Source lineage
[CODEX_SYNTHESIS] Planner-executor split → graph retrieval → bilevel tool orchestration.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p048-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] NaviAgent; bilevel planning; tool graph; parameter dependency; toolchain construction

