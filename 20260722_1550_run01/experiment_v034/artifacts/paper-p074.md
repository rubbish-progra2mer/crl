<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p074","card_kind":"paper","paper_id":"P074","evidence_ids":["ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"],"source_refs":[{"path":"papers/P074_toolgate.pdf","sha256":"7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d"}]} -->
# ToolGate: Contract-Grounded and Verified Tool Execution for LLMs

## Role in the knowledge base
[CODEX_SYNTHESIS] 提供“调用前 P gate + 返回后 Q gate + 验证后才 commit state”的 changed computation；并明确保证受 contract completeness 限制。

## Problem and setting
[CODEX_SYNTHESIS] 目标是防止不满足前提的调用或结构/语义不合约的返回污染 Agent 信任状态。

## Changed computation
[AUTHOR_FACT] precondition 决定工具是否合法可调用，postcondition 决定 runtime output 是否可写入 trusted state。[[evidence:ev-p074-contract-state-commit]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 核心超越普通 pre-call validator 的部分是 post-return verification 与 conditional state commit。

## Limitations and failure signals
[AUTHOR_FACT] ToolBench 约 25% 工具缺少结构化 response schema，来源实现将其 postcondition 默认设为 true。[[evidence:ev-p074-missing-schema-true-postcondition]]

## Lineage and baselines
[CODEX_SYNTHESIS] 最近基线应区分仅 schema/argument precheck、仅检索 rerank 与完整 P/Q commit gate，避免把额外 search computation 当作 contract 收益。

## Evidence ledger
[CODEX_SYNTHESIS] 一条 Evidence 固定 changed computation，一条固定 contract-relative 边界。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool contract; precondition gate; postcondition verification; trusted symbolic state; conditional commit; incomplete schema
