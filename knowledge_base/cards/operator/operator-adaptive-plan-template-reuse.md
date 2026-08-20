<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-adaptive-plan-template-reuse","card_kind":"operator","paper_id":"P071","evidence_ids":["ev-p071-plan-template-reuse","ev-p071-cache-false-positive-boundary"],"source_refs":[{"path":"papers/P071_agentic_plan_caching.pdf","sha256":"af2ec5f2b4431048ef71d4e090a43a6e9ed9104bcba6dd6d0826c8e26cbc3c8a"}]} -->
# Adaptive Reuse of Abstract Plan Templates

## Intervention target
[CODEX_SYNTHESIS] 新任务开始时的 planning computation，不缓存最终答案。

## Before and after computation
[CODEX_SYNTHESIS] plan from scratch/full-history replay → retrieve abstract completed-plan template and adapt with a smaller model。[[evidence:ev-p071-plan-template-reuse]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为新目标、template cache 与 similarity；输出为适配计划；test time 增加检索/小模型调用并减少大模型 planning。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 复用结构而非实例值，可保留可迁移 decision skeleton 并降低历史污染。

## Predicted observable signature
[CODEX_HYPOTHESIS] 对结构相似但实体不同的任务更有效；错误 match 时性能下降，且严格阈值呈成本—覆盖折中。

## Preconditions and transfer risks
[AUTHOR_FACT] semantic query cache 有 false positives，full-history reuse 也较差。[[evidence:ev-p071-cache-false-positive-boundary]]

## Source lineage
[CODEX_SYNTHESIS] semantic answer/query cache → full-history memory → P071 abstract plan template adaptation。

## Evidence ledger
[CODEX_SYNTHESIS] template changed computation 与 false-positive boundary 有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] plan template cache; test-time memory; plan skeleton adaptation; semantic cache false positive
