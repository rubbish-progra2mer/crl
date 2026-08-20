<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-tool-description-and-order-bias","card_kind":"failure","paper_id":"P069","evidence_ids":["ev-p069-description-induced-preference","ev-p069-identical-tool-order-bias"],"source_refs":[{"path":"papers/P069_tool_preferences.pdf","sha256":"bf2fb1bba7d9d028348bc9d8991d3ed01f78437c834fa4106d3abae048cbbac5"}]} -->
# Tool Description and Order Can Dominate Selection

## Observed failure
[AUTHOR_FACT] 仅改 description 可造成超过十倍 usage 差异，functionally identical tools 仍有 order-sensitive selection。[[evidence:ev-p069-description-induced-preference]] [[evidence:ev-p069-identical-tool-order-bias]]

## Conditions and scope
[CODEX_SYNTHESIS] PDF 中的 functionally identical control 直接表明 selection/provider fairness 不稳定；它不等同于任务正确率下降或真实工具执行损失。

## Failed intervention
[CODEX_SYNTHESIS] 通过更长、更积极或位置更靠前的 schema 获得调用份额，却没有改变工具能力。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] combined edits 同时改变长度、cue、示例与信誉表达，缺少 token-matched 因子消融；名称后缀也可能残留身份混杂。

## Warning for future candidates
[CODEX_SYNTHESIS] tool routing 实验必须 counterbalance order/description，并报告真实执行 outcome、cost 与 side effects。

## Possible repair boundary
[CODEX_HYPOTHESIS] 对称描述与交叉顺序是最低控制，不代表已解决 preference bias。

## Evidence ledger
[CODEX_SYNTHESIS] description effect 与 identical-tool order effect 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool description bias; order effect; functionally identical tools; provider selection fairness
