<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-action-preserving-observation-contextualization","card_kind":"operator","paper_id":"P079","evidence_ids":["ev-p079-action-conditioned-contextualization","ev-p079-ground-truth-action-retry","ev-p079-unseen-ui-boundary"],"source_refs":[{"path":"papers/P079_lcow.pdf","sha256":"2695ec5c912241fbdb56fc5f9ee3a4f60d1aaa23b511f35cff3d32908e97dead"}]} -->
# Next-Action-Supervised Observation Contextualization

## Intervention target
[CODEX_SYNTHESIS] tool/web Agent 在每次决策前读取的长 observation，而非动作模型本身。

## Before and after computation
[CODEX_SYNTHESIS] 原始 AXTree 全量输入 → 基于任务与历史产出 reasoning 加 action-relevant subset，再供 policy 选择动作；训练用多 Agent next-action matching 选择监督目标。[[evidence:ev-p079-action-conditioned-contextualization]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为任务、动作历史与当前 AXTree；输出在每个 policy decision 前生成，是带 element IDs 的 refined observation。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 直接优化下一动作可恢复性，比无条件摘要更能保留决策相关 UI，同时减少 observation noise。

## Predicted observable signature
[CODEX_HYPOTHESIS] 在相同 policy 与 action budget 下减少 observation tokens，同时保持或提升 next-action accuracy；损失应集中在未见 affordance。

## Preconditions and transfer risks
[AUTHOR_FACT] 零分候选会用 ground-truth next action 重试。[[evidence:ev-p079-ground-truth-action-retry]] [AUTHOR_FACT] 未见 Filter-List UI 上没有提升。[[evidence:ev-p079-unseen-ui-boundary]] [CODEX_SYNTHESIS] contextualizer 同时生成 reasoning/planning，论文未报告 element-level fidelity；每个动作增加一次 contextualizer 调用，训练依赖强 teacher/judge，且没有 matched-total-compute baseline。

## Source lineage
[CODEX_SYNTHESIS] 从 P079 原样抽象；它不同于纯 context compression，因为 contextualizer 也生成 reasoning。

## Evidence ledger
[CODEX_SYNTHESIS] action-conditioned target、oracle retry 与 transfer failure 均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] observation contextualizer; AXTree compression; action-relevant context; next-action recoverability; unseen affordance failure
