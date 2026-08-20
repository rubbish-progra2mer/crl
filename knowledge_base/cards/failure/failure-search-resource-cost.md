<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-search-resource-cost","card_kind":"failure","paper_id":"P002","evidence_ids":["ev-p002-search-resource-cost"],"source_refs":[{"path":"papers/P002_tree_of_thoughts.pdf","sha256":"6939cadebd84c8cdcc6ff3c2082b75851a86e2ef82008848d0af692f80521fa7"}]} -->
# Search Improvement Lacks Equal-Budget Isolation

## Observed failure
[AUTHOR_FACT] ToT search requires more resources, including GPT-4 API cost, than sampling methods。[[evidence:ev-p002-search-resource-cost]]

## Conditions and scope
[CODEX_SYNTHESIS] 结论限于显式 thought search 与其比较设置，不表示所有搜索都不值得。

## Failed intervention
[CODEX_SYNTHESIS] 现有结果同时改变 branch 数、evaluator calls 与搜索控制流，当前 Evidence 因而不能单独识别搜索结构在等预算下的贡献。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 更强 evaluator、更多候选和更长推理都可能贡献；来源也说明可用模块化 trade-off 调整成本。

## Warning for future candidates
[CODEX_SYNTHESIS] 至少报告 token、model calls、API cost 等适用预算，并尽可能做固定预算对照，分开候选数量、evaluator 与回溯贡献。

## Possible repair boundary
[CODEX_HYPOTHESIS] 选择性展开或便宜 verifier 可能改善成本，但需在固定预算下验证。

## Evidence ledger
[AUTHOR_FACT] `ev-p002-search-resource-cost` 定位到 PDF p.9 的资源限制。[[evidence:ev-p002-search-resource-cost]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] tree search cost；more samples confound；verifier calls；fixed-budget search；equal test-time compute；matched model token sampling and verifier budgets；搜索预算混杂。
