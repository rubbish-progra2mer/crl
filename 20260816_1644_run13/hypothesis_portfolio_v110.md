# v110 假设组合

## H1：成功轨迹的因果必要动作过滤

- 状态：`KILLED_BY_BEHAVIOR_CALIBRATION_INTERVENTION_CREDIT_AND_RUN_MEMORY`
- 原因：冗余/不足调用的行为校准、成功轨迹伪步骤信用、动作干预与后端补偿归因均已直接覆盖。

## H2：观测支持的动作优势

- 状态：`KILLED_BY_DIRECT_OBSERVATION_SUPERVISION`
- 原因：SOAR 已把环境观测令牌接入优势，目标正是避免只学习成功动作而不理解工具后果。

## H3：失败对比驱动的能力课程

- 状态：`KILLED_BY_DIRECT_CAPABILITY_TARGETED_TRAINING`
- 原因：TRACE 已从成功/失败轨迹识别能力缺口、合成环境、训练能力适配器并路由；在线错误裂变和失败专门智能体也已覆盖邻近实现。

## H4：回放删减式逐步信用

- 状态：`KILLED_BY_STEP_LEVEL_INTERVENTION_AND_ERROR_LOCALIZATION`
- 原因：首错干预、首个不可恢复错误定位、轨迹遗忘定位和层级优势已经占据核心计算。

## 实验决定

不注册轨迹删减探针。小规模确定性轨迹可以演示某步非必要，却不能改变直接训练方法与 Run 内干预归因的归属。
