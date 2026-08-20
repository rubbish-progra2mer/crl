<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-plan-cache-semantic-false-positives","card_kind":"failure","paper_id":"P071","evidence_ids":["ev-p071-plan-template-reuse","ev-p071-cache-false-positive-boundary"],"source_refs":[{"path":"papers/P071_agentic_plan_caching.pdf","sha256":"af2ec5f2b4431048ef71d4e090a43a6e9ed9104bcba6dd6d0826c8e26cbc3c8a"}]} -->
# Semantic Plan-Cache Hits Can Reuse the Wrong Computation

## Observed failure
[AUTHOR_FACT] query semantic caching 出现 false-positive hits，full-history reuse 也低于 plan-template approach。[[evidence:ev-p071-cache-false-positive-boundary]]

## Conditions and scope
[CODEX_SYNTHESIS] 绑定 plan/query reuse，不说明所有 semantic retrieval 都失败。

## Failed intervention
[CODEX_SYNTHESIS] 以表面目标相似度直接复用 answer/history，未区分可迁移 plan structure 与实例约束。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] false positive 可能来自 embedding similarity、阈值或历史噪声；当前 Evidence 不唯一识别来源。

## Warning for future candidates
[CODEX_SYNTHESIS] cache hit rate 不等于任务正确；需报告 wrong-hit、adaptation failure 与节省的真实 planning cost。

## Possible repair boundary
[AUTHOR_FACT] P071 抽取 abstract template 并用较小模型适配。[[evidence:ev-p071-plan-template-reuse]]

## Evidence ledger
[CODEX_SYNTHESIS] negative baselines 与 template alternative 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] plan cache false positive; semantic cache drift; wrong plan reuse; template adaptation
