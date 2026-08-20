<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-experience-insight-update","card_kind":"operator","paper_id":"P018","evidence_ids":["ev-p018-insight-update-operations"],"source_refs":[{"path":"papers/P018_expel.pdf","sha256":"01e533d81fb4a5f91797c073a9b1929acbaa64da45a592b26563ca7d135024f3"}]} -->
# Cross-Task Experience Insight Update

## Intervention target
[AUTHOR_FACT] 从成功/失败经验中维护可 ADD、EDIT、UPVOTE、DOWNVOTE 的自然语言 insight 集。[[evidence:ev-p018-insight-update-operations]]

## Before and after computation
[CODEX_SYNTHESIS] Baseline 是每个任务从零开始；changed computation 是离线抽取跨任务规则，并在测试 prompt 中复用。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为训练任务轨迹及成败对比，输出为带重要性更新的 insights；抽取发生在测试前，推理时作为长期规则注入。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 反复支持的经验被保留，矛盾或局部规则可被降权/编辑，从而压缩跨任务失败模式。

## Predicted observable signature
[CODEX_HYPOTHESIS] 相比直接堆叠原始反思，筛选后的 insight 应更稳定且对相似新任务更有效。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 依赖经验质量、教师模型与跨任务共性；离线成本、数据相似性和提示长度必须公开。

## Source lineage
[CODEX_SYNTHESIS] ExpeL 是直接来源；与 Reflexion 的单任务 episodic retry 相邻但 intervention time 与知识粒度不同。

## Evidence ledger
[AUTHOR_FACT] `ev-p018-insight-update-operations` 定位到 PDF p.3 的四种维护操作。[[evidence:ev-p018-insight-update-operations]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] experiential learning；insight memory；cross-task rule extraction；ADD EDIT UPVOTE DOWNVOTE；经验规则记忆。

