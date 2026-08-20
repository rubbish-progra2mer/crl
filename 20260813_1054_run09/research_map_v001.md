# 研究地图与证据边界

## 已核对的共享知识库证据

- `P074` ToolGate：`ev-p074-contract-state-commit` 表明其用前置条件约束调用、用后置条件约束结果是否进入可信符号状态；`ev-p074-missing-schema-true-postcondition` 表明约四分之一缺少结构响应模式的 ToolBench 工具被设为 `Q=True`。这支持“静态契约可能留下不可验证空洞”，但不证明本候选有效。
- `P030` STALE：`ev-p030-failure-core` 与 `ev-p030-recognition-application-gap` 区分了识别状态已过期和在下游行为中实际采用新状态；`ev-p030-write-side-adjudication` 与 `ev-p030-authorized-readout` 已覆盖写侧裁决和受权状态读出。因此本候选不能把“阻止旧状态进入下游”作为新贡献。
- `P079` LCoW：`ev-p079-action-conditioned-contextualization` 已用下一动作可恢复性选择观测子集；这使“只保留动作相关观察”本身不是新颖点。
- `P073` Uncertainty Calibration：`ev-p073-internal-confidence-misalignment` 表明文本相似的执行轨迹可具有不同正确性；`ev-p073-execution-supervised-probe` 已用执行结果监督校准探针。候选不能依赖语言模型置信度作为真值。
- `P098` Constraint Injection：`ev-p098-nonbinding-blindness` 与 `ev-p098-constraint-injection` 说明单次目标等价可漏掉非约束性错误，而已知标签的反事实约束探针可揭露它们。这是“构造可区分错误分支的探针”机制来源，但其对象是优化模型而非在线工具状态。
- `P101` Distilled Test Suites：`ev-p101-neighbor-distillation` 用单点修改的邻居查询定义覆盖并蒸馏小测试集。这是“用少量测试分离语义分支”的机制来源，但其对象是离线文本到结构化查询评价。

## 实时最近工作碰撞检索（2026-08-13）

以下只核对了公开摘要、可检索正文片段或论文页面，不等同于逐页完整阅读：

- ToolGate（arXiv:2601.04688）：霍尔式工具契约和可信状态提交。https://arxiv.org/abs/2601.04688
- Agent-BRACE（arXiv:2605.11436）：原子自然语言主张加序数置信度的显式信念状态，并由策略模型使用。https://arxiv.org/abs/2605.11436
- Context Gathering Decision Process（arXiv:2605.07042）：把主动上下文搜索形式化为部分可观测马尔可夫决策过程，并维护谓词信念状态。https://arxiv.org/abs/2605.07042
- Agent-Authored World Modeling（arXiv:2606.25421）：从策略当前决策需要构造世界模型训练目标。https://arxiv.org/abs/2606.25421
- SenseAct（ICLR 2026 Agents in the Wild workshop）：在图形界面动作后做类型条件化后置条件检查，并在符号状态不足时选择性调用视觉模型。https://openreview.net/forum?id=0DznNQFW4g
- NesyProAct（OpenReview 公开稿）：以神经符号动作、前置条件、后动作不变量和最小修复组织网页智能体。https://openreview.net/pdf?id=9xteuRjHr7

## 当前尚未发现的精确组合

当前检索未发现把“写后潜在状态分支”先按下游动作或终局约束取商，再在可用只读工具中选择最小分支分离探针的文本与工具型大语言模型智能体方法。这只是本轮检索事实，不是新颖性证明；后续仍需围绕主动诊断、测试选择、部分可观测规划和程序监控做更窄检索。

## 关键未决问题

1. 决策类由语言模型声明会不会过于不稳定，导致方法只是换一种自评？
2. 分支库若由研究者预定义，是否在实验中泄露故障分布？
3. 与“固定写后读”和“全量读回”相比，复杂调度是否只在刻意设计的成本结构下有利？
4. 未见故障不在分支库中时，是否会出现错误确定性？
