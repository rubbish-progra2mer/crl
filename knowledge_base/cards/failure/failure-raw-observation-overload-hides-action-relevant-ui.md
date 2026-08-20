<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-raw-observation-overload-hides-action-relevant-ui","card_kind":"failure","paper_id":"P079","evidence_ids":["ev-p079-action-conditioned-contextualization","ev-p079-ground-truth-action-retry","ev-p079-unseen-ui-boundary"],"source_refs":[{"path":"papers/P079_lcow.pdf","sha256":"2695ec5c912241fbdb56fc5f9ee3a4f60d1aaa23b511f35cff3d32908e97dead"}]} -->
# Lengthy Raw Observations May Obscure Action-Relevant UI

## Observed failure
[CODEX_HYPOTHESIS] 长 AXTree 中的无关元素与布局噪声可能使 policy 难以定位下一动作需要的 affordance；P079 以 next-action recoverability 构造训练目标，但未隔离验证 raw-observation overload 的因果。[[evidence:ev-p079-action-conditioned-contextualization]]

## Conditions and scope
[AUTHOR_FACT] 未见 Filter-List 类别时 contextualizer 没抽出隐藏 menu 所需元素，成功率没有提升。[[evidence:ev-p079-unseen-ui-boundary]]

## Failed intervention
[AUTHOR_FACT] 全零候选通过提供 ground-truth next action 重试。[[evidence:ev-p079-ground-truth-action-retry]] [CODEX_SYNTHESIS] 因此训练成功不能自动归因于无 oracle 的 observation compression。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 直接观察到的是 contextualizer 在未见 affordance 上漏掉必要元素并保持 0% success；这不证明 raw observation 本身隐藏了该元素。收益还可能来自 contextualizer 同时执行的 reasoning/planning，而论文没有 element fidelity metric 或 matched-total-compute baseline。[[evidence:ev-p079-unseen-ui-boundary]]

## Warning for future candidates
[CODEX_SYNTHESIS] 必须测试 unseen affordance、信息保留与 action accuracy，并把 contextualizer 的 reasoning/planning 贡献与单纯 token reduction 分开。

## Possible repair boundary
[CODEX_HYPOTHESIS] 用 task/history-conditioned subset 保留 action-relevant element IDs，但必须在无 ground-truth action 的新 UI 上验证。

## Evidence ledger
[CODEX_SYNTHESIS] training objective、oracle retry 与 unseen-UI failure 均绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] raw observation overload; AXTree noise; action relevant UI; unseen affordance; contextualization oracle
