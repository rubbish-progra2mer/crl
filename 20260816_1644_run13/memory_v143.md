# v143 当前记忆

## 新增负记忆

- 不把“原种子通过率 + 固定难度偏移 + 距 0.5 最近”称为已落地的学习前沿；必须观察材料化后目标策略表现。
- 金标准答案通过生成测试只认证任务内部一致性，不能认证任务对当前策略的难度或训练价值。
- 下游训练增益若同时改变动作选择、技能子图、制品编辑掩码和提示，不能单独归因于混合整数规划选择器。
- 同候选池关闭求解器、动作置乱和动作边际匹配是必要组件对照，但本身是评价修补，不是方法贡献。
- 用经验动作效果、学习进展、策略遗憾或优先级回放修复固定偏移时，必须先对照自动目标生成、无监督环境设计、ACCEL 和 PLR。
- StructAgent 的验证状态陈旧回到 v012；最小充分状态回到 v124；BoardroomAI 的影响传播回到依赖闭包与 Matrix；MOOSEDev 的集合完备/否定/替代回到结构化知识查询。
- 公开仓库复核只能陈述看到了什么：截至 2026-08-17，三条公开分支路径与一般终端合成文件中未发现 FORGE 选择器；不得外推为代码绝对不存在。

## 诊断与状态

- `crl-active-diagnosis` 事实包位于 `workbench_v143/diagnosis/v143-frontier-convergence-20260817/`，`FACTS_SHA256=875c3141d1d9b165e03e2b8f44e70fae4e6ff12424ead66e6b68fd5b105a1a63`。
- FTS Recall 为 `READY`，无污染和陈旧源；semantic Recall 未请求，状态单独为 `DEGRADED / semantic_index_missing`。
- v143 无实验、Seed、Reviewer、Formal 或 Review-support 证据。
- v029 外部执行边界保持原样；Run 保持 `ACTIVE / AUTONOMOUS`。
