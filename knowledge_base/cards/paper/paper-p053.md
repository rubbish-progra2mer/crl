<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p053","card_kind":"paper","paper_id":"P053","evidence_ids":["ev-p053-higher-order-generator","ev-p053-python-to-pddl-pipeline","ev-p053-pattern-review-confound","ev-p053-parser-evaluation-boundary"],"source_refs":[{"path":"papers/P053_higher_order_planning_formalizers.pdf","sha256":"224970784bd45edc3191b71c2aadd81e01f5869fcd004c4fa10bac4ed1217b19"}]} -->
# Language Models as Higher-Order Planning Formalizers

## Role in the knowledge base
[CODEX_SYNTHESIS] P054/P055 完整 PDDL formalizer 谱系的表示层后继：用可执行生成器处理短描述对应巨大 grounded instance 的 compression gap。

## Problem and setting
[AUTHOR_FACT] 固定 classical-planning domain 中，简短自然语言规则可能展开为远大的 objects、fluents、initial state 与 goal state，普通 Formalizer 必须显式输出这些 grounded facts。[[evidence:ev-p053-higher-order-generator]]

## Changed computation
[AUTHOR_FACT] 模型先生成紧凑的 higher-order program，再由执行器把程序展开成 PDDL problem file，之后才交给 planner 或 parser。[[evidence:ev-p053-higher-order-generator]] [[evidence:ev-p053-python-to-pddl-pipeline]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 该机制把模型侧计算从“大量事实枚举”改成“重复规则编码”，因此最有价值的可迁移点是表示与输出复杂度，而不是再增加一次自由语言 reasoning。

## Limitations and failure signals
[AUTHOR_FACT] 完整系统还加入了普通 Formalizer/Planner 没有的第二阶段 repeating-pattern review，表示变化与额外 prompting 未被隔离。[[evidence:ev-p053-pattern-review-confound]] [AUTHOR_FACT] 大实例中 planner timeout 后，部分结果以生成文件和 ground truth 的 exact parser comparison 代替 planner 完成。[[evidence:ev-p053-parser-evaluation-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] P054 complete PDDL formalizer → P055 constraint stress → P053 compact generator representation。closest comparison 必须至少包含普通 Formalizer、`Formalizer + same review` 与匹配预算的生成器版本；只和 direct Planner 比较不足以识别机制。

## Evidence ledger
[CODEX_SYNTHESIS] 正式 Claim 只覆盖规则可程序化展开的固定域 formalization；不据此声称一般 Agent planning、真实任务或端到端大实例 solver scalability 已解决。[[evidence:ev-p053-higher-order-generator]] [[evidence:ev-p053-python-to-pddl-pipeline]] [[evidence:ev-p053-pattern-review-confound]] [[evidence:ev-p053-parser-evaluation-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] higher-order formalizer; generator program; grounded PDDL expansion; compression gap; unraveling problem; representation scaling; pattern-review confound
