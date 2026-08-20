<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p060","card_kind":"paper","paper_id":"P060","evidence_ids":["ev-p060-formal-ir-solver","ev-p060-ir-result-and-nl-failure"],"source_refs":[{"path":"papers/P060_unifying_planning_language.pdf","sha256":"5e3695206fd0e01347e348d606ebd206387f4fba3192ed24ea5133abdef36305"}]} -->
# Unifying Inference-Time Planning Language Generation

## Role in the knowledge base
[CODEX_SYNTHESIS] inference-time planning 中 formal IR + symbolic solver 的机制来源，并提供 natural-language IR 负向对照。

## Problem and setting
[AUTHOR_FACT] LLM 输出 formal intermediate representation，再由 symbolic solver 执行。[[evidence:ev-p060-formal-ir-solver]]

## Changed computation
[CODEX_SYNTHESIS] 在生成答案前插入 syntax-aligned IR，把可枚举/约束计算交给 solver。

## Evidence-backed findings
[AUTHOR_FACT] 增加一层 IR 后，Level 2 在论文报告的 8/8 个设置中优于 Level 0/1；四类 IR 中 natural-language IR 持续伤害，而 PyPDDL/PDDL 持续改善结果。[[evidence:ev-p060-ir-result-and-nl-failure]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 结果依赖任务能否忠实映射到 IR；形式执行正确不等于自然语言规格正确。

## Lineage and baselines
[CODEX_SYNTHESIS] natural-language CoT/plan → formal IR solver → syntax-aligned multi-IR refinement。

## Evidence ledger
[CODEX_SYNTHESIS] solver 计算和 NL-IR 负向结果由两条 Evidence 支撑。

## Retrieval vocabulary
[CODEX_SYNTHESIS] formal intermediate representation; symbolic solver; inference-time planning language; natural-language IR failure
