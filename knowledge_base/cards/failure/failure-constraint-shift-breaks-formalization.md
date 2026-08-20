<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-constraint-shift-breaks-formalization","card_kind":"failure","paper_id":null,"evidence_ids":["ev-p054-natural-language-implicit-predicate-failure","ev-p055-constraint-formalism-taxonomy","ev-p055-representative-subset-boundary","ev-p055-three-revision-budget","ev-p055-constraint-performance-drop","ev-p055-plan-correctness-false-positive-boundary"],"source_refs":[{"path":"papers/P054_planning_formalizer_limits.pdf","sha256":"f1e766c715ddaef8b671a9176c75c65759ddf09316dffd8ea32eab4a2c05a5a1"},{"path":"papers/P055_planner_formalizer_constraints.pdf","sha256":"0d21a03ded6ae892d0818ec8e0f453b3ca0fc1c4cb3e30ae2c3b182c40868207"}]} -->
# Constraint Shift Breaks Planning Formalization

## Observed failure
[AUTHOR_FACT] 在 CoPE 的总体结果中，作者报告短约束显著削弱 direct planning 与 formalization；但并非每个模型、方法与形式体系的表格单元都下降。[[evidence:ev-p055-constraint-performance-drop]] [AUTHOR_FACT] 更自然的基础描述还会因遗漏 `clear` 等隐式 predicate 产生 unsolvable PDDL 或错误计划。[[evidence:ev-p054-natural-language-implicit-predicate-failure]]

## Conditions and scope
[AUTHOR_FACT] initial、goal、action、state 四类 constraint 在 PDDL、PDDL3、LTL、SMT 中需要不同修改，没有单一 formalism 平凡覆盖全部类别。[[evidence:ev-p055-constraint-formalism-taxonomy]]

## Failed intervention
[CODEX_SYNTHESIS] “把请求翻译成任意一种 formal language 再交 solver”并不自动保证局部约束被忠实编码；形式 solver 只能验证实际写入的模型。

## Evidence and alternative explanations
[AUTHOR_FACT] 在 Revision 条件下，formalizer 最多有三次代码尝试/修订机会，按执行错误消息（如有）再生成；这是语法修复，不是重新规划。主实验每域只用 100 个 constraint–problem 手工代表配对。[[evidence:ev-p055-three-revision-budget]] [[evidence:ev-p055-representative-subset-boundary]] [AUTHOR_FACT] plan correctness 还可能把未忠实表达约束的代码判为成功，论文只在跨 datasets/methods 合并抽样的 20 个样本上检查这一假阳性。[[evidence:ev-p055-plan-correctness-false-positive-boundary]]

## Warning for future candidates
[CODEX_SYNTHESIS] 不能用 solver success、syntax pass 或 final-plan accuracy 单独证明 constraint faithfulness；必须公开 formalism/toolchain、revision calls 和 evaluation false-positive 风险，并按 constraint category 报告。

## Possible repair boundary
[CODEX_HYPOTHESIS] 值得研究的改进应改变 constraint coverage、semantic decomposition 或独立规格核查的计算，并在 matched budget 下减少类别化遗漏；错误反馈重试本身不作为新 Operator，也不扩展到环境反馈学习/执行恢复方向。

## Evidence ledger
[CODEX_SYNTHESIS] 本 Failure 连接 P054 的 implicit-semantics omission 与 P055 的 explicit constraint shift；它不声称所有表格单元都下降，也不把 20 个样本的零假阳性扩写成可靠 evaluator。[[evidence:ev-p054-natural-language-implicit-predicate-failure]] [[evidence:ev-p055-constraint-performance-drop]] [[evidence:ev-p055-plan-correctness-false-positive-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] constraint faithfulness; semantic omission; PDDL constraint; formalizer robustness; specification shift; plan-correctness false positive; matched revision budget
