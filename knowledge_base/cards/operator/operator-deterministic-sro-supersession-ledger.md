<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-deterministic-sro-supersession-ledger","card_kind":"operator","paper_id":"P091","evidence_ids":["ev-p091-supersession-rule","ev-p091-retain-fabrication"],"source_refs":[{"path":"papers/P091_memstrata.pdf","sha256":"10349a31de86116b7e4cc5a8cb5e60766a55ab7dbab7894906841a6e3234171f"}]} -->
# Deterministic (S,R,O) Supersession in a Bi-Temporal Ledger

## Intervention target
[CODEX_SYNTHESIS] memory write path 的时序有效性：新断言与既有事实值冲突时，谁保有回答权威。

## Before and after computation
[AUTHOR_FACT] Before：RAG 式全保留 + 读取时 LLM 裁决。After：事实以 (subject, relation, object) 键存储；新断言与同 (S,R) 键冲突时，确定性规则在 bi-temporal ledger 中 retire 旧值——无相似度阈值、无 LLM 调用。[[evidence:ev-p091-supersession-rule]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：抽取出的结构化断言与既有 ledger。输出：当前有效值 + 被 retire 的历史（可审计）。时点：写入时裁决，读取时只见当前值。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 把时序裁决从概率信号（相似度/LLM 判断）移到键匹配的确定性规则，消除两类失败源：阈值误判与读取时 co-present 混淆。

## Predicted observable signature
[AUTHOR_FACT] 消融实测：去掉 supersession 使 evolving accuracy 0.99→0.33、fabrication ×6——机制贡献在管线内被隔离。[[evidence:ev-p091-retain-fabrication]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 前提：断言可被抽取为 (S,R,O) 结构且 (S,R) 键可靠对齐——抽取器质量是新的单点故障；对无明确键结构的自由文本冲突不适用。静态知识侧保留 RAG 全召回。转移风险：基准为合成演化流，键对齐难度低于野生数据。

## Source lineage
[CODEX_SYNTHESIS] RAG 全保留 → STALE(P030) 写侧裁决诊断 → MemStrata 确定性 (S,R,O) supersession（写侧结构化节点占位者）；与 P095（读后装配层确定性 max）在管线位置上互补。

## Evidence ledger
[AUTHOR_FACT] supersession 规则定义与消融隔离分别绑定 exact Passage。[[evidence:ev-p091-supersession-rule]] [[evidence:ev-p091-retain-fabrication]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] subject relation object; supersession rule; bi-temporal ledger; deterministic conflict resolution; no similarity threshold; write-side adjudication; stale value retirement; write-time supersession; deterministic conflict resolution; retiring stale facts; subject relation object keys; temporal validity ledger; superseding contradicted values without an LLM
