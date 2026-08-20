# v165 失败归因

## 类型

`SKILL_DESCRIPTION_REPAIR_COLLIDES_WITH_FULL_BODY_RERANKING_QUERY_CONDITIONAL_UTILITY_AND_SAME_CAPABILITY_RESOLUTION_PRIORS`

## 直接原因

- SkillReducer 已生成／压缩路由描述并重构技能正文；
- SkillRouter 已证明完整正文是决定性路由信号，并发布正文检索—重排基准和模型；
- SkillResolve-Bench 已直接建模同能力候选歧义、易混淆负例、契约画像和家族内代表选择；
- R3-Skill 已把查询条件化兼容性和拒绝负例用于两阶段技能检索训练；
- SkillReranker 已把任务和技能分解为执行状态与状态转移描述再重排；
- 因而“规范修复后检测排序反转并按不确定性升级正文”的候选没有新的不可替代计算。

## 非原因

- 不是本地资源不足：现有环境具备轻量稀疏／语义检索实验所需核心库；
- 不是已经看到公开数据上的正负结果：除说明、任务轻量元数据和文件清单外，没有读取技能数据记录或运行评估；
- 不是恶意技能、描述攻击、提示注入或安全过滤研究；
- 不是 v029 外部安全边界、科研反证、Run 终局或用户终止。

## 决定

不注册实验或 Seed。将“合规修复可能改变路由可分性”保留为评价消融，而非论文主张；v166 离开技能描述、技能检索和正文重排方法族，Run 保持 `ACTIVE`。
