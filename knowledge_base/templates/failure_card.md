<!-- Replace this line with one valid CRL_CARD_META JSON object; see ../CARD_SCHEMA.md. -->
# Failure Card

## Observed failure

只记录论文或可审计实验真正观察到的负向结果、无效机制或边界，不把猜测写成事实。

## Conditions and scope

写明模型、任务、工具、预算、数据和比较条件，防止将局部失败外推为普遍结论。

## Failed intervention

写清失败方法实际改变了什么计算，以及它可能根本没有改变什么。

## Evidence and alternative explanations

把直接 Evidence、作者解释、Codex 综合和仍然成立的替代解释分开；人工写明 canonical failure condition、aliases、与相近 Card 的 same-mechanism/refinement/contradiction 关系及 Evidence family 依赖。

## Warning for future candidates

给出未来 Candidate 必须回答的问题；该警告不是黑名单或自动拒绝规则。

## Possible repair boundary

只有 Evidence 支持时才记录可能修复方向；没有支持时明确保持未知。

## Evidence ledger

逐项列出负向结果、比较公平性和适用边界对应的 evidence_id。

## Retrieval vocabulary

列出失败现象、失败 computation 和混杂因素的常见改写；必须保留适用条件，不得把局部失败扩成通用关键词黑名单。
