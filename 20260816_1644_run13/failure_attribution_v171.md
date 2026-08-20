# v171 失败归因

## 类型

`WITNESS_CARRYING_INSTRUCTION_GC_CLOSED_BY_RATIONALE_PRESERVATION_SKILL_ATTRIBUTION_AND_COVER_MINIMIZATION_PRIORS`

## 直接原因

- 保存规则添加原因并把它与执行提示隔离，目标论文已直接实现并给出因果效果；
- 通过删减或联盟采样估计规则边际贡献，SkillReducer 和 SkillShapley 已覆盖；
- 在硬覆盖约束下寻找最短结构，SkillZip 已覆盖；
- 用失败见证矩阵求最小保留集，是经典回归测试选择／集合覆盖的直接迁移。

## 非原因

- 不是灾难性记忆缺少证据；真实仓库风险曲线和合成评论干预都很强；
- 不是见证绑定没有工程价值；它能提高可审计性与可删除性；
- 不是资源、安全控制或环境阻止了实验；本版因先行覆盖而不重复实验；
- 不是 Run 终局或用户终止。

## 决定

不注册实验或 Seed。v172 转向不依赖提示／技能压缩的新 frontier，Run 保持 `ACTIVE`。
