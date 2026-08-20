<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p052","card_kind":"paper","paper_id":"P052","evidence_ids":["ev-p052-decomposed-formalization","ev-p052-result-self-assessment","ev-p052-fixed-cross-task-examples","ev-p052-implicit-constraint-failure","ev-p052-self-diagnosis-nontermination"],"source_refs":[{"path":"papers/P052_llmfp.pdf","sha256":"e59c5c55b3befeeb4774a20990b8629f487e9fb1520cc2a953f041b7bb6fdaec"}]} -->
# Planning Anything with Rigor: General-Purpose Zero-Shot Planning with LLM-based Formalized Programming

## Role in the knowledge base
[CODEX_SYNTHESIS] P051 的直接泛化后继：用跨任务分解替代测试任务专用示例，同时保留形式求解边界。

## Problem and setting
[CODEX_SYNTHESIS] 九类多约束和多步规划任务，输入仍包括详细任务描述、背景信息或 API 与输出格式。

## Changed computation
[AUTHOR_FACT] 管线把问题定义、变量/约束表示和 solver 代码生成分开执行。[[evidence:ev-p052-decomposed-formalization]] [AUTHOR_FACT] 求解结果随后被格式化，并由同一模型做有界的步骤自评与修改。[[evidence:ev-p052-result-self-assessment]]

## Evidence-backed findings
[AUTHOR_FACT] Formulator 使用两个固定且不随测试任务变化的跨任务示例；这里的 task-agnostic 不等于没有任务说明或领域接口。[[evidence:ev-p052-fixed-cross-task-examples]]

## Limitations and failure signals
[AUTHOR_FACT] Definer 可能遗漏隐式守恒约束，使 solver 优化语义不完整的模型。[[evidence:ev-p052-implicit-constraint-failure]] [AUTHOR_FACT] 同模型自诊断也可能误判代码错误并引入不终止循环。[[evidence:ev-p052-self-diagnosis-nontermination]]

## Lineage and baselines
[CODEX_SYNTHESIS] P051 专用形式化 demonstrations → P052 Definer/Formulator/Code Generator 分解；最接近的强对照是使用同一 Z3 工具的一步 Code-SMT，而不是无工具直接生成。

## Evidence ledger
[AUTHOR_FACT] 本卡所引事实均锚定准入 PDF、当前 Passage SHA 与精确引用区间。[[evidence:ev-p052-decomposed-formalization]] [[evidence:ev-p052-result-self-assessment]] [[evidence:ev-p052-fixed-cross-task-examples]] [[evidence:ev-p052-implicit-constraint-failure]] [[evidence:ev-p052-self-diagnosis-nontermination]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] LLMFP; decomposed formalization; Definer; Formulator; Code-SMT; implicit constraint; task-agnostic planning
