# v161 失败归因

## 类型

`CONTINUAL_SKILL_UTILITY_ATTRIBUTION_CLOSED_BY_PAIRED_VALIDATION_LIBRARY_MAINTENANCE_AND_SKILL_COMPOSITION_PRIORS`

## 直接原因

- ContinualSkillBench 已用纯上下文学习条件证明顺序收益不能直接归因给显式技能；
- 通过同任务有／无技能配对执行隔离候选技能贡献，已由 HDSO 以可证伪验证协议直接实现；
- 按效用、兼容性和验证状态维护、合并或删除技能已有 SkillOps；
- 技能子集、数量与顺序的联合路由已有 SkillComposer；
- 用顺序任务结果联合优化技能生成和调用已有 SAGE。

## 非原因

- 不是否认顺序经验在 14/15 个模型—领域组合上的归一化收益；
- 不是把技能库规模、调用频率或自动质量分误当作因果效用；
- 不是因缺少本机模型而放弃可改变新颖性判断的实验；
- 不是安全控制、Prior collision 或 Run 终局。

## 决定

不注册实验或 Seed。将纯上下文学习对照与技能因果效用分离原则纳入负记忆；Run 保持 `ACTIVE`，下一版寻找不同的决策结构。
