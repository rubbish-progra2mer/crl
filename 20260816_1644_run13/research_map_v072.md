# v072 研究图谱

## 错误级联与验证放置

- *GraphTracer* 已用信息依赖图而非时间顺序追踪多轮深度搜索中的根因与症状。
  - https://arxiv.org/abs/2510.10581
- *From Spark to Fire* 已把多智能体协作抽象为有向依赖图，建模错误传播并给出早期放大风险判据。
  - https://arxiv.org/abs/2603.04474
- *Delayed Verification Destabilizes Multi-Agent LLM Belief* 已研究有限验证预算下的纠正者放置，给出图上的超模目标和近似规则。
  - https://arxiv.org/abs/2606.27409
- *Trajectory Graph Copilot* 已在执行前用轨迹图诊断潜在动作错误。
  - https://arxiv.org/abs/2607.27443

因此“依赖图—传播风险—关键节点验证”的主链不是空白。

## 人机修复成本

- *HAS-Bench* 将人和语言模型智能体表示为具有角色、权限、通信路径和行动权的参与者，同时测澄清、反馈利用、控制校准、主动性与交互成本。
  - https://arxiv.org/abs/2607.04329
- *Know Your Mistakes* 用问责模型预测对话状态错误，并把用户确认摩擦轮次作为纠错机制。
  - https://aclanthology.org/2025.acl-long.1399/
- *Human-Guided Harm Recovery for Computer Use Agents* 已以用户偏好刻画恢复质量并构建恢复基准。
  - https://openreview.net/forum?id=joefYuOHWS

因此“任务成功之外计入用户修复负担”已有直接评价和方法。

## 信息不足与推理失败的反事实区分

- *SciDataBench* 已按知识发现、API 调用、预处理和回答分阶段评分，并通过阶段定向技能注入观察知识瓶颈被关闭后失败质量如何迁移。
  - https://openreview.net/forum?id=nP3Ye4rlGD
- *Action Boundary Blindness* 使用替换测试：强制正确动作类型后若失败仍持续，则归为执行边界问题；否则归为规划/工具选择问题。
  - https://aclanthology.org/2026.acl-long.1711/
- *REFLECT* 对候选错误步骤施加诊断特定补丁并受控重放，以结果翻转作为归因证据。
  - https://arxiv.org/abs/2606.09071

因此“补足信息或替换局部步骤—重放—根据翻转归因”的计算已经被直接实现。

## 结论

三条残余路径都已有问题级与方法级直接工作。局部合成实验只能复现依赖图验证、用户摩擦或干预式归因，不注册假设。
