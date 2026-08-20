<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p075","card_kind":"paper","paper_id":"P075","evidence_ids":["ev-p075-retrieve-to-action-leakage","ev-p075-measured-memory-extraction","ev-p075-session-isolation-boundary"],"source_refs":[{"path":"papers/P075_memory_privacy.pdf","sha256":"8c2cfcee69d60f4c20a959cd6b1a6a14d5f6e8d732792cf2a2b4864ac38a88cb"}]} -->
# Unveiling Privacy Risks in LLM Agent Memory

## Role in the knowledge base
[CODEX_SYNTHESIS] 高优先级负向知识：Agent memory 的风险位于 query-controlled retrieval 到 workflow-aligned action 的完整链，而不只是数据库能否直接读取。

## Problem and setting
[AUTHOR_FACT] 攻击设计把检索到的历史示例指定为任务对象，并把输出适配到目标 Agent 已允许的 workflow channel。[[evidence:ev-p075-retrieve-to-action-leakage]]

## Changed computation
[CODEX_SYNTHESIS] 本来源不提供正向 Operator；它展示当前 query 同时改变 retrieval neighbourhood 与 Agent 对 retrieved demonstrations 的处理方式。

## Evidence-backed findings
[AUTHOR_FACT] 静态 200-record memory、30 prompts 下，来源报告从 EHRAgent/RAP 分别提取 50/26 条历史 queries。[[evidence:ev-p075-measured-memory-extraction]]

## Limitations and failure signals
[AUTHOR_FACT] 被测框架没有 session control，多用户可共享 memory；user/session isolation 仅作为未来方向。[[evidence:ev-p075-session-isolation-boundary]] [CODEX_SYNTHESIS] 实证范围限于 GPT-4o 驱动的两个 single-agent 与 static memory，不可直接外推到多 Agent 或动态记忆系统。

## Lineage and baselines
[CODEX_SYNTHESIS] 最近对照是缺少 workflow aligner 的直接索取；未来防御研究必须同时控制正常任务能力、实际调用次数、retrieval exposure 与 session ownership。

## Evidence ledger
[CODEX_SYNTHESIS] 机制、测量与关键部署前提各有 Evidence；不保存攻击字符串或私人样例。

## Retrieval vocabulary
[CODEX_SYNTHESIS] agent memory privacy; retrieval exposure; workflow aligned leakage; shared session memory; cross user demonstrations
