<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p098","card_kind":"paper","paper_id":"P098","evidence_ids":["ev-p098-nonbinding-blindness","ev-p098-constraint-injection","ev-p098-diff-leak-550","ev-p098-open-problem"],"source_refs":[{"path":"papers/P098_constraint_injection.pdf","sha256":"f73aaa44ab843311d0676030081b8f1b9e18f9e9bb0bb0b9a87c761917b43ab3"}]} -->
# Constraint Injection: Beyond Objective Equivalence on VRP

## Role in the knowledge base
[CODEX_SYNTHESIS] 目标等价验证路线的重要最近工作，提供非绑定约束双向失明与 decoupled metrics open problem 的逐字引语锚。

## Problem and setting
[AUTHOR_FACT] SFT 过滤与 RL 奖励共同止于目标等价，对非绑定约束错误双向失明。[[evidence:ev-p098-nonbinding-blindness]]

## Changed computation
[AUTHOR_FACT] INJ：目标常数化 + 带标签探针解注入 + solver 可行性判定 vs 标签；同一验证器作拒绝采样过滤与 GRPO 奖励（0.2/0.5/0.3 权重）。[[evidence:ev-p098-constraint-injection]]

## Evidence-backed findings
[AUTHOR_FACT] 最干净证据 = 消融：仅去 INJ（无注入臂数据反而更大）SFT -2.86 / GRPO -4.00；550/7347 教师样本过 DIFF 挂 INJ——泄漏实测。[[evidence:ev-p098-diff-leak-550]]

## Limitations and failure signals
[AUTHOR_FACT] 评测口径自认：Pass@1 压缩约束级反馈，细粒度约束违规剖面指标 open problem。[[evidence:ev-p098-open-problem]]
[CODEX_SYNTHESIS] 主表对 frontier 胜负不作能力结论（B1/B2 主场分布 + 教师蒸馏混杂：Gemini 既是教师又是最强基线，合并 AVG 仍落后 95.00 vs 93.00）；εobj 未报数值；单次训练无方差；契约失配弃样规模未报；TSPTW 泛化缺口 -8.40。

## Lineage and baselines
[CODEX_SYNTHESIS] ORLM/OptMATH（SFT 线）、SIRL/OR-R1（RL 线）均止于执行/目标等价；与 P096/P097 构成认证侧三近邻。本文可支持机制与失败量化，不宜用来外推不同设定下的主表胜负。

## Evidence ledger
[CODEX_SYNTHESIS] 四条 evidence 分别锚定失明定义、INJ 实现、泄漏量化、open problem 自认。

## Retrieval vocabulary
[CODEX_SYNTHESIS] VRPCoder; constraint injection; dual-verified rejection sampling; GRPO; vehicle routing; objective equivalence blindness; probe synthesis; attack operators; constraint injection as a training signal; vehicle routing code generation; dual verifier for optimization programs
