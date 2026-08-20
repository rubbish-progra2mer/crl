<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-trace-failure-taxonomy","card_kind":"operator","paper_id":"P016","evidence_ids":["ev-p016-mast-taxonomy"],"source_refs":[{"path":"papers/P016_mast_failures.pdf","sha256":"6aff168d6e201217d3f79611f6ad024590a599a03b97ac2aeb0b0b128bac374c"}]} -->
# Trace-Level Multi-Agent Failure Taxonomy Audit

## Intervention target
[AUTHOR_FACT] 将多代理 execution trace 的失败分为 system design、inter-agent misalignment 与 task verification 三类。[[evidence:ev-p016-mast-taxonomy]]

## Before and after computation
[CODEX_SYNTHESIS] Baseline 是只看终局 accuracy；changed computation 是回到 trace 标注失败发生的协作环节，再选择局部修复。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为完整多代理轨迹，输出为可多标签的 failure modes；诊断发生在执行后，不改变当次 policy。相比只记终局 accuracy，诊断增加完整轨迹存储与人工/LLM annotator 成本；该成本不计入当次 policy execution，但必须单独报告。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 结构化 trace 诊断能区分模型能力不足、信息错配与验证缺失，减少只改 prompt 的盲目修补。

## Predicted observable signature
[CODEX_HYPOTHESIS] 针对命中类别的修复应优先降低对应 occurrence，但 accuracy 与 occurrence 可能不同步。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Taxonomy 依赖轨迹可见性、标注定义与系统范围；标签频率不是因果效应或自动 ontology。

## Source lineage
[CODEX_SYNTHESIS] MAST 是直接来源；本 Card 将其作为 Codex 诊断 Operator，不构建程序化知识图谱。

## Evidence ledger
[AUTHOR_FACT] `ev-p016-mast-taxonomy` 定位到 PDF p.1 的 14 modes/3 categories。[[evidence:ev-p016-mast-taxonomy]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MAST；multi-agent failure taxonomy；trace diagnosis；inter-agent misalignment；task verification；多代理失败归因。
