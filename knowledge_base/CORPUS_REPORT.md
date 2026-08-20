# CRL 共享论文知识库概况

更新时间：2026-07-31（Asia/Shanghai）

## 当前资产

- 99 篇外部论文，3995 个 Passage，224 条 Evidence。
- 228 张 Markdown Card：Paper 99、Operator 66、Failure 63。
- `knowledge.sqlite` 保存 Paper、Passage 与 Evidence；`passages.npz` 是 Passage 向量索引；`cards_fts.sqlite` 是可从 Markdown Card 全量重建的全文索引。
- 知识权威顺序是：外部原文及其 SHA-256 → reconciliation → Evidence → Card。检索排名不构成科学证据。

## 使用边界

知识库服务于主 AI 研究者的文献理解、失败排查、方法迁移和最近工作判断，不生成科研结论，也不充当正式 Run 的启动门。Failure、Operator、Paper/Evidence 是并列、互补的知识入口，完整保留，由主研究者自主决定查询顺序、深度和组合方式。

共享库只保存外部论文及其客观派生知识。任何科研运行中的候选、实验结论、路线、审查意见、失败记忆、决策、状态或复制件都不得进入共享库。

## 2026-07-31 精确清洗

本次维护保留了全部 99 篇论文 PDF、`knowledge.sqlite` 中的 Paper/Passage/Evidence、`passages.npz` 和有价值的论文阅读材料；删除了明确来自科研运行的候选清单、评测历史和叙述，并把受影响 Card 与 manifest 角色改写为只描述论文自身机制、失败、边界和谱系。

清洗后 228 张 Card 全部通过来源、Evidence、新鲜度、UTF-8 与结构校验，全文索引已重建。v011 内容清洗回放结果为 calibration 20/20（critical 8/8）、blind replay 17/18（critical 5/5）。这只是知识检索回归，不是机器验收。
