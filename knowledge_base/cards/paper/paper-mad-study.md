<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-mad-study","card_kind":"paper","paper_id":"P015","evidence_ids":["ev-p015-agreement-prior","ev-p015-debate-cost-nondominance"],"source_refs":[{"path":"papers/P015_should_we_be_going_mad.pdf","sha256":"8d0330933f495a3804842e8c8b0f778d8529fefeaf8d2a2dbf89d94f97bd0e70"}]} -->
# Should We Be Going MAD?

## Role in the knowledge base
[CODEX_SYNTHESIS] Multi-agent debate 的强负向/成本 baseline，并提供 agreement-prior 控制机制。

## Problem and setting
[CODEX_SYNTHESIS] 多种 MAD 与非辩论 prompting protocols 在多选 QA 上比较 accuracy、time、tokens 与 API cost。

## Changed computation
[AUTHOR_FACT] 新干预在角色 prompt 中写入目标 agreement percentage。[[evidence:ev-p015-agreement-prior]]

## Evidence-backed findings
[AUTHOR_FACT] 额外计算不保证更好结果，表现依赖 hyperparameters 与 system design。[[evidence:ev-p015-debate-cost-nondominance]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 协议同时改变信息共享、轮数和 prompt；原论文部分表格结果口径冲突，相关数字不用于 Card Claim。

## Lineage and baselines
[CODEX_SYNTHESIS] Self-consistency、ensemble refinement 与 Medprompt 是关键非辩论强 baseline；原始 Multi-Persona 是 agreement modulation 的最近控制。

## Evidence ledger
[AUTHOR_FACT] p.6 支持 agreement prompt；p.4 支持 compute non-dominance。[[evidence:ev-p015-agreement-prior]] [[evidence:ev-p015-debate-cost-nondominance]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MAD；multi-agent debate；agreement modulation；cost accuracy tradeoff；self-consistency baseline；多代理辩论。

