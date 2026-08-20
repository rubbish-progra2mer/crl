<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-grounded-formalization-output-expansion","card_kind":"failure","paper_id":null,"evidence_ids":["ev-p053-higher-order-generator","ev-p053-pattern-review-confound","ev-p053-parser-evaluation-boundary"],"source_refs":[{"path":"papers/P053_higher_order_planning_formalizers.pdf","sha256":"224970784bd45edc3191b71c2aadd81e01f5869fcd004c4fa10bac4ed1217b19"}]} -->
# Grounded Formalization Output Expansion

## Observed failure
[AUTHOR_FACT] 一个简短描述可指代远大的 grounded planning instance，迫使普通 Formalizer 从紧凑输入显式输出大量 objects、fluents 与 goals。[[evidence:ev-p053-higher-order-generator]]

## Conditions and scope
[CODEX_SYNTHESIS] Failure 出现在规则性强但 expansion ratio 高的 text-to-formal tasks；它不同于 solver 搜索失败，也不同于自然语言规格遗漏。

## Failed intervention
[CODEX_SYNTHESIS] 提高 context window、分段生成或增加 pattern review 即使提高准确率，也不单独证明已经消除输出展开瓶颈；即使生成文件正确，外部 planner 仍可能因 grounded instance 规模 timeout。[[evidence:ev-p053-parser-evaluation-boundary]]

## Evidence and alternative explanations
[AUTHOR_FACT] P053 的 H-O 系统同时增加第二次 pattern-review prompt，因此观察到的改进可能同时来自表示压缩与额外检查预算。[[evidence:ev-p053-pattern-review-confound]]

## Warning for future candidates
[CODEX_SYNTHESIS] 不得把 parser exact match 当作端到端 planning success；不得用额外 review calls 偷换 representation gain。实验至少需要 `ordinary formalizer`、`ordinary + matched review`、`generator` 和 `generator + matched review`。

## Possible repair boundary
[CODEX_HYPOTHESIS] 有价值的修复应改变中间表示或展开位置，例如 generator/compiler IR、lifted representation 或约束模板；如果只是更长 prompt、更多 tokens 或后处理重试，则没有命中此 Failure。

## Evidence ledger
[CODEX_SYNTHESIS] Source 支持的窄边界是 fixed-domain、synthetic、可规则展开的 formalization，不外推到所有 Agent planning。[[evidence:ev-p053-higher-order-generator]] [[evidence:ev-p053-parser-evaluation-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] description-to-formal compression gap; grounded enumeration; output-length failure; generator program; planner timeout; representation bottleneck
