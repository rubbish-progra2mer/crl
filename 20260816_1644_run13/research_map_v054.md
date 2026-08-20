# v054 研究地图

## 直接先行工作

- *Epistemic Transfer in AI-Assisted Verification: A Framework and Evaluation Protocol* 已把“撤去工具后对新主张的独立表现”定义为认知转移，并提出认知转移效应（ETE）与工具移除成本（TRC）。其四组设计直接比较答案优先、证据优先、主动练习和无练习，并要求延迟、无辅助、全新主张测试。
  - https://arxiv.org/abs/2608.08882
- *AI Assistance Reduces Persistence and Hurts Independent Performance* 通过 1,222 人的随机对照实验报告短时智能协助会降低坚持性和无辅助表现，并把长期能力脚手架列为设计目标。
  - https://arxiv.org/abs/2604.04721
- *How AI Impacts Skill Formation* 通过异步编程库学习实验发现，完全委托会损伤概念理解、代码阅读和调试能力，而保持认知参与的交互模式能保留学习结果。
  - https://arxiv.org/abs/2601.20245
- TRAVER 已将学生知识追踪与逐轮验证结合，用受控学生模拟和代码生成测试评价教学智能体。
  - https://aclanthology.org/2025.findings-acl.642/
- *Adjudicating Artifact-Faithfulness Claims in Tool-Using LLM Agents: A Trace-Local Protocol* 已把最终产物、模型的验证相关主张、确定性验证器和可重放轨迹绑定为局部裁决协议，直接覆盖“从轨迹产出可核验证据”的产物侧。
  - https://openreview.net/forum?id=40wuXQMQRU

## 候选差分审计

“核验残留物”若只是证据优先界面、要求用户先作答、逐步提示或隐藏最终答案，落入认知强制与教学脚手架；若只是把来源、验证器输出和轨迹切片装入证据包，落入轨迹局部产物忠实性。若用一个新的语言模型代替真实用户并测其后续任务表现，测到的是模型间上下文迁移，不是人的保留能力、坚持性或认知转移，无法识别目标因果量。

## 可执行性

权威协议要求数百至约两千名参与者、主动练习对照、工具移除探针及 7—14 天延迟测试。当前 Run 的本地模型和可验证任务环境不能替代这些因果条件。没有既新颖又可在当前资源内有效证伪的最小方法内核。

## 结论

v054 不注册正式假设，也不运行会把模型代理冒充人类证据的合成实验。
