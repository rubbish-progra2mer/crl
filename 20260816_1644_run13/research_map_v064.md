# v064 研究图谱

## 1. 动态修订与残留约束

- [AgentChangeBench](https://openreview.net/forum?id=ZCi58UP9uR) 已直接评估对话中途目标切换。
- [EvolIF](https://aclanthology.org/2026.acl-long.433/) 已覆盖多轮演化指令与约束组。
- [Residual Drift Dominates Contradiction](https://openreview.net/pdf?id=B9gtT1hhEm) 已使用显式账本研究多轮约束残留漂移。

因此“约束墓碑/目标修订账本”没有清晰新差分。

## 2. 局部编辑与未授权污染

- [SCALPEL](https://openreview.net/forum?id=pdFNHe3Yzz) 已用“必须改变/必须不变”的可执行反事实奖励训练外科式结构编辑。
- [LEDGER](https://openreview.net/pdf?id=5akZa6boHV) 已覆盖依赖感知长文档编辑与局部修改不污染无关内容。
- [Overeager Coding Agents](https://arxiv.org/abs/2605.18583) 已把良性任务中的范围外动作作为授权问题系统评价。

因此修改足迹/语义局部性不是空白。

## 3. 已授权行动的过度确认

- [Aligning Agents via Planning](https://aclanthology.org/2026.acl-long.1062/) 的轨迹级奖励已显式包含过度拒绝和无必要工具调用。
- [What Benchmarks Don't Measure: Abstention Competence](https://openreview.net/pdf?id=0yKgijjdct) 直接研究何时应执行、确认或弃权。
- [MCPGAUGE](https://openreview.net/forum?id=Q2SgxaVhaC) 联合衡量主动性、合规、有效性和开销。

因此双向授权校准已有直接评价框架。

## 4. 自动后置条件与任务验证器

- [Verified Tool Calls](https://arxiv.org/abs/2608.02645) 明确覆盖超时后派发、延迟可见、部分成功与陈旧冲突，并指出后置条件需要逐任务工程。
- [SpecMind](https://openreview.net/forum?id=NH2xIXmQ4q) 已直接进行交互式多轮后置条件推断。
- [VeriAct](https://arxiv.org/abs/2604.00280) 已用反例与验证反馈迭代修复不完整或过度约束的形式规约。
- [Recursive Synthetic Terminal Tasks](https://arxiv.org/abs/2608.05466) 已联合递归保持指令、环境、参考解和验证器一致。
- [Proxy State-Based Evaluation](https://aclanthology.org/2026.acl-industry.87/) 已以结构化代理状态评价多轮工具智能体目标完成。

“从近失状态反例合成工具任务后置条件”被规约合成与智能体验证器两侧夹住，剩余仅为应用迁移。
