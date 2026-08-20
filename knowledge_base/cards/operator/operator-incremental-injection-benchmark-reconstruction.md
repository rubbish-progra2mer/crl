<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-incremental-injection-benchmark-reconstruction","card_kind":"operator","paper_id":"P094","evidence_ids":["ev-p094-incremental-protocol","ev-p094-sf-guardrails"],"source_refs":[{"path":"papers/P094_memoryagentbench.pdf","sha256":"022d3771fd643d3bece04841e71331ef6963ff0eba43166849072caeb1b79508"}]} -->
# Incremental Multi-Turn Injection Reconstruction of Long-Context Benchmarks

## Intervention target
[CODEX_SYNTHESIS] 记忆 agent 评测协议：把一次性长上下文数据集改造成增量吸收流，使"边看边存边更新"成为被测对象。

## Before and after computation
[AUTHOR_FACT] After：全部 agent 逐 chunk 接收输入、吸收进记忆并增量更新，看完全部 chunk 后才回答问题；每 chunk 前置记忆化指令，各数据集配任务理解指令。[[evidence:ev-p094-incremental-protocol]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：任意长文档/对话数据集 + 切分粒度。输出：两阶段（注入/查询）评测流 + 一上下文多问摊销。时点：评测协议层，与被测系统无关。
[AUTHOR_FACT] 竞争力护栏（如 SF 的序号规则）作为协议一部分显式声明。[[evidence:ev-p094-sf-guardrails]]

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 增量注入使记忆构建成本、更新一致性、跨 chunk 整合暴露为可测行为；一次性喂入会掩盖全部三者。

## Predicted observable signature
[CODEX_SYNTHESIS] 同一数据同一骨干下，增量协议应使记忆系统间分差拉开（构建/更新策略开始起作用）；配算力配平三档（附录 J 同族）可判断差异来自架构还是信息预算。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 前提：数据可切分且问题不依赖切分边界。转移风险：离散 chunk 非真流式（作者自认）；chunk size 本身是强混杂（512 vs 4096 在 AR 上显著）——协议使用者必须配平或 sweep。

## Source lineage
[CODEX_SYNTHESIS] 静态长上下文基准（LongBench 系）→ 增量注入改造（本文），可作为长期记忆第二评测载体的构造方法。

## Evidence ledger
[AUTHOR_FACT] 协议定义与护栏声明绑定 exact Passage。[[evidence:ev-p094-incremental-protocol]] [[evidence:ev-p094-sf-guardrails]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] incremental injection; two-phase protocol; chunked absorption; memory agent evaluation; amortized multi-question; compute-matched tiers; MemoryAgentBench; chunk-by-chunk injection; incremental memory evaluation; converting long-context datasets to streams; inject then query protocol; absorbing input piece by piece
