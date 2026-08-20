<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p094","card_kind":"paper","paper_id":"P094","evidence_ids":["ev-p094-sf-length-collapse","ev-p094-sf-guardrails","ev-p094-incremental-protocol"],"source_refs":[{"path":"papers/P094_memoryagentbench.pdf","sha256":"022d3771fd643d3bece04841e71331ef6963ff0eba43166849072caeb1b79508"}]} -->
# MemoryAgentBench: Incremental Multi-Turn Memory Evaluation

## Role in the knowledge base
[CODEX_SYNTHESIS] 重要评测载体：FactConsolidation 是带更新标注、多长度档、SH/MH 分档的选择性遗忘基准，并提供四能力框架（AR/TTL/LRU/SF）。ICLR 2026 正式发表。

## Problem and setting
[CODEX_SYNTHESIS] 既有基准要么一次性喂长上下文、要么只测技能执行；记忆 agent 的增量吸收、更新一致性、选择性遗忘缺少直接测量。

## Changed computation
[AUTHOR_FACT] 两阶段增量注入协议：逐 chunk 吸收 + 增量更新 + 后置多问。[[evidence:ev-p094-incremental-protocol]]

## Evidence-backed findings
[AUTHOR_FACT] SF 在显式序号护栏下仍随长度崩塌（o4-mini 80.0→14.0）。[[evidence:ev-p094-sf-length-collapse]] [[evidence:ev-p094-sf-guardrails]]
[CODEX_SYNTHESIS] 覆写提示消融（App. K.2/Table 19：激进/保守覆写策略 FC-MH 均 4.0，PDF 直核）排除指令缺失解释——作者结论 SF 非提示工程可解。
[CODEX_SYNTHESIS] 商业记忆代理 Overall 低于裸 4o-mini 参照；FC-MH 全线 ≤28%。

## Limitations and failure signals
[CODEX_SYNTHESIS] 主表两混杂（骨干不齐：长上下文代理用自家模型而 RAG/商业代理固定 4o-mini；chunk size 不齐：商业代理 4096 vs RAG 512）——跨行排名不作同配置结论；公平对照是附录 J 算力配平三档；GPT-4o 兼任 judge 与被测（轻度自评亲和）；FC 序号护栏与 marker-free 口径（P091）冲突。

## Lineage and baselines
[CODEX_SYNTHESIS] 长上下文基准 → 增量记忆评测；与 P092（冲突分型）、P091（marker-free 演化）构成三口径互补。采用 FC 时须评估序号护栏带来的提示泄漏，SH/MH 可作为预注册分层维度。

## Evidence ledger
[CODEX_SYNTHESIS] 长度崩塌、护栏、协议三条绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] MemoryAgentBench; FactConsolidation; EventQA; accurate retrieval; test-time learning; long-range understanding; selective forgetting; incremental injection; ICLR 2026; memory agent benchmark; incremental multi-turn evaluation; selective forgetting benchmark; fact consolidation dataset
