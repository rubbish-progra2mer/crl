<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-cost-penalized-structured-clarification","card_kind":"operator","paper_id":"P072","evidence_ids":["ev-p072-structured-clarification-gate","ev-p072-unstructured-clarification-failure","ev-p072-compute-boundary"],"source_refs":[{"path":"papers/P072_structured_clarification.pdf","sha256":"def959b625902e0381ddbac6f25e042c8670f07435248e50a075fe8ef3945598"}]} -->
# Cost-Penalized Structured Clarification Gate

## Intervention target
[CODEX_SYNTHESIS] 干预 tool-calling Agent 在参数不完整时的 ask-versus-execute 决策，而不是优化问题措辞。

## Before and after computation
[AUTHOR_FACT] Before：自由文本策略缺少“问哪个、何时停”的标准。[[evidence:ev-p072-unstructured-clarification-failure]] After：以候选 tool call 的未知参数域形成结构化状态，用问题价值减重复方面成本决定追问或执行。[[evidence:ev-p072-structured-clarification-gate]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入是用户请求、tool schema、候选 calls 与已问方面；输出是一个澄清问题或当前最佳 call；时点在真正 tool invocation 之前。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 若失败来自 specification incompleteness，把停止标准绑定到可执行参数域会比通用 reflection/clarification prompt 更稳定。

## Predicted observable signature
[CODEX_HYPOTHESIS] 在匹配模型与 tool-call budget 下，关键参数缺失错误下降、重复问题下降；若只有措辞变化而 ask/execute 边界不变，则机制不成立。

## Preconditions and transfer risks
[AUTHOR_FACT] 少问用户并不等于少计算；在来源所报 ClarifyBench 配置中，系统仍使用约 22K tokens。[[evidence:ev-p072-compute-boundary]] [CODEX_SYNTHESIS] 还要求 schema 参数域可枚举且用户回答可更新它。

## Source lineage
[CODEX_SYNTHESIS] 来源 P072；迁移时应与 matched free-form clarification、domain-aware prompting 和相同调用预算比较。

## Evidence ledger
[CODEX_SYNTHESIS] 机制、失败对照与预算边界均有独立 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] cost penalized clarification; structured uncertainty; ask execute threshold; incomplete tool arguments; clarification stopping rule
