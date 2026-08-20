<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p051","card_kind":"paper","paper_id":"P051","evidence_ids":["ev-p051-formalization-pipeline","ev-p051-solver-guarantee-boundary","ev-p051-omitted-constraint-failure","ev-p051-cost-boundary"],"source_refs":[{"path":"papers/P051_formal_verification_planning.pdf","sha256":"ba9261d6d8fbf2b43817e57c29aa6ffacc0b14ef038e6c86a33f8780490bd365"}]} -->
# Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools

## Role in the knowledge base
[CODEX_SYNTHESIS] TravelPlanner 机制链中把自然语言规划转成可执行约束模型、再交给 SMT solver 搜索的强基线。

## Problem and setting
[CODEX_SYNTHESIS] 多日旅行规划需要同时满足硬约束、常识约束、环境可用性和预算约束。

## Changed computation
[AUTHOR_FACT] LLM 先生成形式化步骤与调用 solver 的代码，再由 solver 求解编码后的问题。[[evidence:ev-p051-formalization-pipeline]]

## Evidence-backed findings
[AUTHOR_FACT] 论文把形式保证限定在已经编码且可满足的约束系统；solver 为该系统生成形式验证的计划。[[evidence:ev-p051-solver-guarantee-boundary]]

## Limitations and failure signals
[AUTHOR_FACT] LLM 遗漏 all-different 约束时，solver 会重复选择同一对象以优化分数。[[evidence:ev-p051-omitted-constraint-failure]] [AUTHOR_FACT] 该多调用管线还报告了显著成本和时延。[[evidence:ev-p051-cost-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] P004 的结构化约束失败 → 直接语言规划/搜索 → 自然语言到形式模型 → solver-backed planning；P052 进一步把专用形式化示例改造成跨任务分解。

## Evidence ledger
[AUTHOR_FACT] 本卡所引事实均锚定准入 PDF、当前 Passage SHA 与精确引用区间。[[evidence:ev-p051-formalization-pipeline]] [[evidence:ev-p051-solver-guarantee-boundary]] [[evidence:ev-p051-omitted-constraint-failure]] [[evidence:ev-p051-cost-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] formal verification planning; SMT solver; TravelPlanner; constraint encoding; solver-backed plan; formalization fidelity
