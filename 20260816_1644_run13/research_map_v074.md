# v074 研究图谱

## 计划锚定

- *WebAnchor* 直接定义 `plan anchor`：长程网页推理中首个推理步骤对后续行为产生不成比例的影响，并用两阶段强化学习分别优化首步规划与按计划执行。
  - https://arxiv.org/abs/2601.03164

这精确覆盖“自生成计划反过来锁定执行”的核心现象。

## 计划—执行失配与修订

- *PIVOT* 将计划和执行轨迹作为可优化对象，经过 PLAN、INSPECT、EVOLVE、VERIFY 四阶段，用环境反馈产生文本梯度并单调接收改进轨迹。
  - https://arxiv.org/abs/2605.11225
- *Devil’s Advocate* 在执行前预测失败和替代方案、执行后检查子目标对齐，并在必要时回溯修订。
  - https://aclanthology.org/2024.findings-emnlp.53/
- *PilotRL* 分别训练全局计划质量、执行器计划遵循以及计划在环境变化下的自适应修订。
  - https://openreview.net/pdf/895bb06b77441ebfe940b4ef8784d5cfc5bc7a92.pdf

## 陈旧计划和约束执行

- *SyncPlan* 显式加入等待、死锁检测与轻量计划陈旧检测器，当环境变化使假设失效时触发重规划。
  - https://arxiv.org/abs/2608.01652
- *RunAgent* 把自然语言计划解释为含 IF、GOTO、FORALL 的智能体语言，并在每步推导、验证约束和纠错。
  - https://arxiv.org/abs/2605.00798

## 结论

首步计划锚定、计划—执行失配、环境反馈修订、计划陈旧检测和自然语言计划约束执行均有直接工作。删除旧计划、增加“可修订”标签或加入重规划提示不会形成新计算，不注册实验。
