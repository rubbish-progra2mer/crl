<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-selective-forgetting-collapses-with-context-length","card_kind":"failure","paper_id":"P094","evidence_ids":["ev-p094-sf-length-collapse","ev-p094-sf-guardrails"],"source_refs":[{"path":"papers/P094_memoryagentbench.pdf","sha256":"022d3771fd643d3bece04841e71331ef6963ff0eba43166849072caeb1b79508"}]} -->
# Selective Forgetting Collapses with Context Length Despite Explicit Recency Guardrails

## Observed failure
[AUTHOR_FACT] FactCon-MH 上 o4-mini 在 6K 版本得 80.0、32K 版本崩至 14.0——任务本身可解，失败随历史长度出现而非任务不可行。[[evidence:ev-p094-sf-length-collapse]]

## Conditions and scope
[AUTHOR_FACT] 评测 prompt 含显式护栏：事实带序号索引、"newer facts have larger serial numbers"、被明确要求以最新事实解冲突——失败不能归因于缺少更新指令。[[evidence:ev-p094-sf-guardrails]]
[CODEX_SYNTHESIS] ICLR 2026 正式发表；两阶段增量注入协议；SF 为合成冲突流（作者自认并辩护）。

## Failed intervention
[CODEX_SYNTHESIS] 依赖长上下文模型 + 显式 recency 规则完成选择性遗忘；提示工程消融（激进/保守覆写策略）都救不了（Table 19），排除"换个 prompt 就好"的解释。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 主表跨行混杂（骨干不齐 + chunk size 配置不齐）不影响本失败：6K/32K 对照为同模型同任务；FactCon 由 MQUAKE 反事实编辑对构造（§3.1），先验答案即为被更新掉的旧值，先验解释不成立。序号护栏使该口径与 marker-free 口径（P091）不可直接比较——护栏在场仍崩即为下界证据。

## Warning for future candidates
[CODEX_SYNTHESIS] 将 FactConsolidation 用于无标记记忆研究时须评估并移除可能泄漏更新顺序的护栏；任何“长上下文足以处理更新”的候选方法都必须面对该测量。

## Possible repair boundary
[CODEX_HYPOTHESIS] 未被本文排除的组合：chunk=512 + 强骨干 + 更深检索的联合单元未测全；结构化 supersession（P091）与装配层确定性择新（P095）是绕开长程注意的两条已占位路线。

## Evidence ledger
[CODEX_SYNTHESIS] 长度崩塌与护栏在场分别绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] selective forgetting; FactConsolidation; context length collapse; serial number guardrail; recency instruction; memory update failure; 6K 32K; o4-mini; failing to overwrite outdated facts; memory update failure at long context; forgetting collapses as history grows; ignoring newest-fact instructions; updating memory with conflicting facts
