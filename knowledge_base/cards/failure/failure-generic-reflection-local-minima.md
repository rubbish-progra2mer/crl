<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-generic-reflection-local-minima","card_kind":"failure","paper_id":"P003","evidence_ids":["ev-p003-generic-reflection-local-minimum"],"source_refs":[{"path":"papers/P003_lats.pdf","sha256":"a6b84613eeeaa3beb979ac3e34cbb3575bceb7ccf6050a2c2fc677d5e3a3ab19"}]} -->
# Generic Reflection Can Trap Search in Local Minima

## Observed failure
[AUTHOR_FACT] 在 LATS 的 WebShop 设置中，生成的 reflections 经常过于通用、不能提供有用反馈，并使 Agent 倾向陷入 local minima。[[evidence:ev-p003-generic-reflection-local-minimum]]

## Conditions and scope
[CODEX_SYNTHESIS] 该结果来自文本 WebShop、有限样本和固定迭代预算；它说明没有可操作错误定位的 verbal feedback 可能无效，不证明所有 reflection 都有害。

## Failed intervention
[CODEX_SYNTHESIS] 失败干预是把失败轨迹压缩为通用语言反思后再次注入搜索，却没有给出能区分下一动作的具体状态、证据或约束。

## Evidence and alternative explanations
[AUTHOR_FACT] 原文把问题描述为 reflection generic、not useful，并观察到 local-minimum tendency。[[evidence:ev-p003-generic-reflection-local-minimum]]

## Warning for future candidates
[CODEX_SYNTHESIS] 不能把“生成了 critique”当作 changed computation；必须说明 critique 如何改变候选动作、价值判断、剪枝或执行分支，并与等迭代搜索比较。

## Possible repair boundary
[CODEX_HYPOTHESIS] 若反馈绑定具体 state/action error，并在提交动作前进入 value、selection 或 pruning，可能比仅追加通用反思更可检验。

## Evidence ledger
[AUTHOR_FACT] `ev-p003-generic-reflection-local-minimum` 定位 PDF p.8 对 generic reflection、无用反馈与 local minima 的直接描述。[[evidence:ev-p003-generic-reflection-local-minimum]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] generic reflection；non-actionable critique；local minimum；verbal feedback failure；reflection without changed action selection；通用反思无效。
