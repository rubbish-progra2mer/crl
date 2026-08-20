<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p071","card_kind":"paper","paper_id":"P071","evidence_ids":["ev-p071-plan-template-reuse","ev-p071-cache-false-positive-boundary"],"source_refs":[{"path":"papers/P071_agentic_plan_caching.pdf","sha256":"af2ec5f2b4431048ef71d4e090a43a6e9ed9104bcba6dd6d0826c8e26cbc3c8a"}]} -->
# Agentic Plan Caching

## Role in the knowledge base
[CODEX_SYNTHESIS] test-time reusable plan template 的机制来源，以及 semantic-cache false-positive 的负向锚点。

## Problem and setting
[AUTHOR_FACT] APC 从已完成 plan 抽取 reusable template，按目标语义检索后由较小模型适配。[[evidence:ev-p071-plan-template-reuse]]

## Changed computation
[CODEX_SYNTHESIS] 从复用完整历史或答案改为复用去实例化的 plan skeleton，再针对当前目标适配。

## Evidence-backed findings
[AUTHOR_FACT] plan caching 存在 cost/performance trade-off；query semantic cache 有 false-positive hit，full-history reuse 也较差。[[evidence:ev-p071-cache-false-positive-boundary]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 复用依赖任务结构相似性与安全匹配阈值；命中率不能替代适配后任务正确率。

## Lineage and baselines
[CODEX_SYNTHESIS] answer/query cache and full-history reuse → abstract plan-template reuse → small-model adaptation。

## Evidence ledger
[CODEX_SYNTHESIS] template pipeline 与 false-positive/复用边界各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] agentic plan caching; reusable plan template; test-time memory; semantic cache false positive; plan adaptation
