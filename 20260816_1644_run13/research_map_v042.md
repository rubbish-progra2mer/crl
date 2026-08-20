# v042 研究地图

## 技能注入导致失败模式迁移

- SciDataBench（ACL ARR 2026 May）：300 个真实科学数据接口场景，分成知识发现、接口调用构造、预处理和研究问题回答四阶段。接口调用构造是普遍瓶颈；专门技能能显著提升知识型阶段，却不提高推理型阶段的通过率，并把部分模型推向提前退出、把另一模型推向无声错误。
  - https://openreview.net/forum?id=nP3Ye4rlGD
- SkillsInjector：直接以“注入更多技能可能降低任务完成率”为问题，联合优化技能选择、自适应上下文预算和技能集合感知呈现。
  - https://arxiv.org/abs/2605.29794
- AdaptMI：报告小模型在简单题上会因不必要技能示例产生认知负荷，并选择性注入技能。
  - https://openreview.net/forum?id=0nuohwdAvM

结论：现象真实，但按阶段、能力或难度路由技能已经被直接覆盖。

## 工具失败诱发替代探索

- *Do Tool Failures Help?*（ACL ARR 2026 May）报告适量工具失败可提高智能体表现，最优失败率依任务与模型推理能力而变。
  - https://openreview.net/pdf?id=F44stEMVFj
- *Failure makes the agent stronger*（Findings of ACL 2026）故意破坏正确工具调用、模拟错误反馈，并构造“错误调用→结构化反思→修正调用”的配对轨迹用于训练与评测。
  - https://aclanthology.org/2026.findings-acl.618/
- CausalFlow 与 Causal Agent Replay 已用反事实干预和重放定位或修复智能体失败。
  - https://arxiv.org/abs/2605.25338
  - https://arxiv.org/abs/2606.08275

结论：保留真实结果、另建失败条件影子分支的想法仍属于已有“故意失败反馈+反事实分支+修正”的组合，没有不可替代的新计算。

## 安全边界

所有噪声均指本地、非对抗性的工具可用性或错误反馈；未研究安全过滤绕过、攻击或对抗提示。
