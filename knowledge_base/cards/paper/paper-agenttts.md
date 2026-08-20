<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-agenttts","card_kind":"paper","paper_id":"P020","evidence_ids":["ev-p020-compute-allocation-search","ev-p020-diminishing-compute-return"],"source_refs":[{"path":"papers/P020_agenttts.pdf","sha256":"454906b0f931fd092ab25163c1ea3fd69e793eac570320ba257d174bee9b0c7c"}]} -->
# AgentTTS

## Role in the knowledge base
[CODEX_SYNTHESIS] 近期 test-time compute allocation、planning/search 与 efficiency 的交叉来源。

## Problem and setting
[CODEX_SYNTHESIS] 多阶段复杂任务，各 subtask 可选不同模型与采样预算，以总 FLOPs 衡量成本。

## Changed computation
[AUTHOR_FACT] 用 Agent 搜索多阶段任务的 compute-optimal allocations。[[evidence:ev-p020-compute-allocation-search]]

## Evidence-backed findings
[AUTHOR_FACT] 额外 compute 超过某点后收益递减或消失，上游分配还会改变下游需求。[[evidence:ev-p020-diminishing-compute-return]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Model pool、搜索 prior、配置试验成本与预算口径共同影响结果，不能当作纯 policy improvement。

## Lineage and baselines
[CODEX_SYNTHESIS] Random search、BO、LLM_ZS、AgentHPO 与 MLCopilot 是实验 baseline，AgentHPO/MLCopilot 是最近控制；固定模型与 uniform scaling 只是概念对照。ToT 搜索 thought，AgentTTS 搜索配置，二者 intervention object 不同。

## Evidence ledger
[AUTHOR_FACT] p.2 同时支持 allocation search 与 diminishing-return boundary。[[evidence:ev-p020-compute-allocation-search]] [[evidence:ev-p020-diminishing-compute-return]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] AgentTTS；test-time scaling；compute-optimal allocation；model routing；multi-stage budget；测试时计算优化。
