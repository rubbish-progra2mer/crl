# P021 Codex 首读：AgentFlow

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P021_agentflow.pdf`
- PDF SHA-256：`33e04a3fa3ac197e69c2fffd5f53a274c80872a515a6269bc98ae7d4105f7095`
- 读取范围：问题与系统定义（pp.1, 4–6）、实验与消融（pp.7–10）、训练算法与理论边界（pp.17–19）、评测与工具细节（pp.20–23, 27–30）。

## Changed computation

- [AUTHOR_FACT] AgentFlow 把工具型 Agent 拆为 Planner、Executor、Verifier、Generator 四个模块，以显式演化 Memory 串联；只训练 Planner，其他模块保持冻结（pp.4–7）。
- [AUTHOR_FACT] Flow-GRPO 在当前 Planner 策略下运行完整多轮系统，把同一个最终结果奖励广播给轨迹内每一轮，再用组归一化优势、PPO clipping 和 KL 约束更新 Planner（pp.5–6, 17）。
- [CODEX_SYNTHESIS] 真正改变的不是“多一个 reviewer”，而是 Planner 的训练分布：由离线模仿静态轨迹改为在 Executor/Verifier/Memory 的实时闭环状态上做 on-policy 更新。奖励广播只是可计算近似，不能表述为识别了哪一步真正有功。

## Baseline、公平性与结果

- 基线包括同骨干的冻结 AgentFlow、GPT-4o Planner、GPT-4o 轨迹 SFT、AutoGen、搜索/代码工具 RL 模型和基础模型（pp.7–9, 20–21）。作者统一了部分搜索与代码工具，并报告三次运行均值及标准差，但不同系统的提示、实际 tool call/token、模块调用成本并未完全等价（pp.20–23）。
- Flow-GRPO 相对冻结 Qwen2.5-7B Planner 在六项训练策略消融任务平均提高 17.2 个百分点；离线 SFT 相对冻结版本平均下降 19.0 个百分点（p.9 Table 3）。
- 主表覆盖十个任务；作者报告搜索、agentic、数学、科学四组均有提升（pp.7–8）。但训练数据混合 Search-R1 与 DeepMath，部分测试与训练域邻近；GPT-4o 与 7B AgentFlow 的“规模胜出”也混入工具与系统结构差异，不能作为纯模型能力比较。
- 增加最大轮数 3→10 同时增加平均实际轮数并改善四项任务（p.10），因此性能包含额外推理/工具预算；不能把全部增益归因于更好的单步策略。

## 失败边界与未否定项

- [AUTHOR_FACT] 冻结 Planner 的案例会重复错误 Python 调用；训练后案例转向直接传入数值并成功（p.9）。这是案例证据，不是错误循环总体发生率。
- [AUTHOR_FACT] 奖励由 GPT-4o rubric 判断语义/数值/选项等价（pp.6, 20）；不是所有任务都由可执行 verifier 给出，故“verifiable”有 LLM judge 误差边界。
- [CODEX_SYNTHESIS] 同一最终奖励赋给所有轮会把成功轨迹中的无效动作一并强化，论文证明的是目标重写与局部优化形式，不是因果信用正确性；这与后续细粒度 credit assignment 工作构成直接张力。
- 未否定：离线训练在覆盖真实闭环状态、使用更合适的轨迹级目标时可能有效；更强静态 Planner 仍带来 5.8 点平均增益；方法尚未证明迁移到不可自动判分的开放研究任务。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P021-E01 | mechanism | §3.1, pp.4–5 | Eq.2 前后 | “four specialized modules” | [AUTHOR_FACT] 四模块与显式 Memory 定义。 |
| P021-E02 | mechanism | §3.2, p.6 | Eq.4–7 | “every action within a rollout receives the same global reward” | [AUTHOR_FACT] 轨迹奖励广播是核心更新信号。 |
| P021-E03 | result | §4.4, p.9 | Table 3 | “SFT ... 19.5” | [AUTHOR_FACT] 表中平均值显示离线 SFT 明显低于冻结与 Flow-GRPO。 |
| P021-E04 | failure | §4.3, p.9 | Figure 7 | “stuck in error loops” | [AUTHOR_FACT] 冻结系统重复工具调用错误的条件性案例。 |
| P021-E05 | fairness | Appendix C.1, p.20 | Evaluation Details | “increase the maximum number of turns ... 10” | [AUTHOR_FACT] 评测允许的推理轮数边界。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

Agent learning / tool-use 中“闭环 Planner 训练”强来源，同时也是“全轨迹奖励广播并非因果 credit”的对照来源。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`In-Flow Planner Policy Optimization`
- Baseline：冻结或在闭环外用静态轨迹训练 Planner。
- Changed computation：用当前完整 Agent 系统生成 on-policy 多轮状态，只更新 Planner，并以最终任务结果做组相对策略更新。
- 前提：任务存在廉价且可信的终局判分；Executor/Verifier/Memory 接口在训练与评测间稳定。
- retrieval vocabulary：in-the-flow optimization, planner policy, multi-turn tool use, trajectory reward, offline SFT collapse。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Trajectory Reward Broadcast Masks Turn Contribution`
- 条件：多轮轨迹仅有最终奖励，且同一优势广播到每个动作。
- 现象：成功轨迹中的有效、冗余和偶然动作得到同号更新，无法据此识别真正关键步骤。
- 替代解释：组内相对优势与 on-policy 状态匹配本身可能足以带来性能改善。
- 未否定：额外 counterfactual/process signal 可改善 credit；本文没有直接比较这些方案。

## 首读裁决

`KEEP_FOR_SECOND_READ`。Operator 与 Failure 都可能影响多个 Agent-learning 候选；需要独立二读重点攻击奖励可验证性、预算公平性和理论“等价”措辞。
