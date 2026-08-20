<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-debate-cost-nondominance","card_kind":"failure","paper_id":"P015","evidence_ids":["ev-p015-debate-cost-nondominance"],"source_refs":[{"path":"papers/P015_should_we_be_going_mad.pdf","sha256":"8d0330933f495a3804842e8c8b0f778d8529fefeaf8d2a2dbf89d94f97bd0e70"}]} -->
# Multi-Agent Debate Does Not Reliably Dominate Under Cost

## Observed failure
[AUTHOR_FACT] 论文报告额外计算并不保证更好结果，表现取决于 hyperparameters 与 system design。[[evidence:ev-p015-debate-cost-nondominance]]

## Conditions and scope
[CODEX_SYNTHESIS] 范围是所测多选 QA、MAD protocols 与模型；不能外推为所有 multi-agent collaboration 无效。

## Failed intervention
[CODEX_SYNTHESIS] 单纯增加 agents、rounds 与相互可见答案，没有必然改变错误相关性或信息质量。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] Prompt、聚合、角色先验、调用数和数据集同时变化；协议级非占优不等于每个组件无效。

## Warning for future candidates
[CODEX_SYNTHESIS] 需要等 token/call 强 ensemble baseline，并测独立信息、相关错误和首答被破坏。

## Possible repair boundary
[CODEX_HYPOTHESIS] 只有路由独立证据或动态控制交互时，multi-agent 计算才可能超越独立采样聚合。

## Evidence ledger
[AUTHOR_FACT] `ev-p015-debate-cost-nondominance` 定位到 PDF p.4 的成本—结果边界。[[evidence:ev-p015-debate-cost-nondominance]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MAD non-dominance；multi-agent debate cost；self-consistency baseline；correlated errors；多代理辩论不占优。

