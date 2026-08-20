<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-objective-equivalence-passes-nonbinding-errors","card_kind":"failure","paper_id":"P098","evidence_ids":["ev-p098-nonbinding-blindness","ev-p098-diff-leak-550","ev-p098-open-problem"],"source_refs":[{"path":"papers/P098_constraint_injection.pdf","sha256":"f73aaa44ab843311d0676030081b8f1b9e18f9e9bb0bb0b9a87c761917b43ab3"}]} -->
# Objective Equivalence Passes Non-Binding Constraint Errors into Training Data

## Observed failure
[AUTHOR_FACT] 目标等价对约束集结构性失明：候选可伪增或缺失约束而仍匹配参考最优值——只要受影响约束在被测实例上非绑定；两个失败模式（spurious over-constraint / silent constraint omission）都能通过可执行性与差分测试过滤、进入 SFT 数据并获得正 RL 奖励。[[evidence:ev-p098-nonbinding-blindness]]
[AUTHOR_FACT] 实测泄漏规模：7347 个教师样本中 550 个（≈7.5%）过差分测试但挂约束注入。[[evidence:ev-p098-diff-leak-550]]

## Conditions and scope
[CODEX_SYNTHESIS] VRP 端到端 Gurobi 代码生成的训练管线（拒绝采样过滤 + GRPO 奖励）；泄漏率测于其自建教师生成分布（Gemini-3.1-Pro + Claude Opus 4.6 教师）。

## Failed intervention
[CODEX_SYNTHESIS] DIFF/answer-agreement 作为唯一接受信号——单实例最优值比对无法约束"未被该实例激活"的约束结构。

## Evidence and alternative explanations
[AUTHOR_FACT] 作者自认评测口径同病：Pass@1 本质是目标等价度量，把约束级多维反馈压成二元信号，"decoupled evaluation metrics ... remain an open problem"。[[evidence:ev-p098-open-problem]]
[CODEX_SYNTHESIS] 550/7347 是单教师分布单次统计（无方差）；Fig.1 钉子案例系构造性说明非训练日志自然样本。

## Warning for future candidates
[CODEX_SYNTHESIS] 任何以答案一致性做过滤、奖励或评测的候选方法都必须回答非绑定约束盲区；作者明确将更细粒度的 decoupled constraint-violation profiles 列为开放问题。

## Possible repair boundary
[CODEX_HYPOTHESIS] 带标签探针注入已用于训练信号；认证时点的逐约束 enforcement 剖面仍未被本文覆盖；软约束或目标罚项机制缺少确定性可行性标签，仍属开放边界。

## Evidence ledger
[CODEX_SYNTHESIS] 非绑定失明定义、550 泄漏量化、open problem 自认三条绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] objective equivalence; non-binding constraint; spurious over-constraint; silent constraint omission; differential testing leak; 550 of 7347; rejection sampling; constraint-violation profile; matching the reference optimum while constraints are wrong; contaminated training data via objective equivalence; differential testing leaks constraint errors; blindness to non-binding constraints
