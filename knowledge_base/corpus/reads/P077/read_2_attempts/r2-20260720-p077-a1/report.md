# P077 独立二读报告：ArCHer

## 阅读与来源状态

- 已逐页阅读指定 PDF 的全部 39 个物理页，包括正文、参考文献、环境/数据附录、额外实验、失败轨迹、超参数表和理论证明。
- 源 PDF SHA-256：`9A25030A872732DC5FC544E04E3D20382BE1D512EEEFD97E7E92179DD2C5F8EC`。
- 本报告的页码均指 PDF 物理页，不使用论文印刷页码。

## Changed computation

ArCHer 改变的不是提示词，而是多轮语言策略的训练计算。它把同一生成过程拆成两个时间尺度并并行优化：高层把一次完整 utterance 当动作，用跨轮 TD/Bellman backup 学习长期 `Q(s,a)` 与 `V(s)`；低层把 token 当动作，但不再从外部终局奖励跨全部 token 直接回传，而把高层 critic 给出的 utterance-level advantage 当成该轮 token 序列的终端奖励，用 REINFORCE/带 token baseline 的 policy gradient 更新自回归 actor。高层可复用 replay buffer 中历次交互，低层则在 critic 上“in silico”采样和优化。（物理页 2、4–8）

在线主实例的计算链为：收集当前 actor 与环境的 utterance transition → 存入包含历史策略数据的 replay buffer → 用 `r + gamma V_target(s')` 更新 utterance Q → 在 replay 状态上从当前 actor 采样 utterance，使 V 回归该动作的 target-Q 期望 → 用 `min(Q1,Q2)-min(V1,V2)` 一类保守 advantage 更新 token actor；Q/V 使用 target networks、Polyak 更新和 double-Q 技巧。（物理页 5–8）

框架还给出两种实质变体：长 utterance 时额外训练 token-level value baseline 降低 policy-gradient 方差；纯离线时以 IQL expectile backup 约束 critic 在数据支持内，并用 AWR 对 actor 施加由 advantage 加权的行为克隆约束，避免 OOD action 导致 Q 过估计和策略坍塌。（物理页 6–7、13–14、24）

## 输入、输出、信息与时点

- 高层状态输入：到当前轮为止的完整交互历史；高层动作输出：一个可变长 token 序列/utterance；环境随后返回下一状态与可能延迟的标量任务奖励。低层状态是轮前历史加本轮已生成 token，低层动作是下一个 token，EOS 结束本轮。（物理页 4–5）
- 训练时高层 critic 可读取 replay buffer 中过去在线策略产生的 `(s,a,r,s')`；Q 的监督目标包含下一状态的 target-V。V 的动作期望不是由 oracle 穷举，而是在 replay 状态上由当前 actor 自回归采样 utterance 近似。（物理页 5–6）
- 低层 actor 更新时可读取高层 critic 对“整段 utterance”的 advantage；这是一种训练期学习信号。部署/交互时 actor 仍按 token 自回归生成，论文没有要求在每个 token 上调用外部奖励 oracle。（物理页 4–8）
- 外部信息只在每个高层环境 step 后到达：Detective Game 返回游戏状态，Twenty Questions/Guess My City 返回模拟 oracle 回复，WebShop 返回页面文本；终局或逐步计算奖励由环境给出。（物理页 10、22–23）

## 实验与强基线

在线评测覆盖 Detective Game、Twenty Questions Subset、Twenty Questions、Guess My City、WebShop。前三类分别要求 51 步解谜、最多 20 问识别隐藏词/城市，WebShop 最多 10 个交互 step；任务均有程序化或模拟环境奖励，而非人工在线满意度。（物理页 9–10、22–23）

主要比较包括：

- token-level PPO：同一任务初始化下的标准 on-policy 强基线；论文报告 Twenty Questions 上至少需每个梯度步 1,024 条 on-policy rollout，超过 100k samples 才略高于 -17，而 ArCHer 少于 1,000 samples 达到该回报，据此形成“至少 100x”样本效率主张。（物理页 10、12、24、33）
- Filtered BC：保留近期 rollout，以总回报最高 10% 做模仿；它早期收敛快但随后平台化，是检验 RL 是否真正优于成功轨迹筛选的重要基线。（物理页 10、12、33）
- CHAI：utterance-level off-policy baseline，在线化后使用与 ArCHer 相同的标准 TD loss，但 actor 冻结，每次从其采样 `k=5` utterance 再由 critic 排序。作者指出该配置已约为 ArCHer 运行时间的 4 倍；更大 k 未测，因而比较受算力边界约束。（物理页 10–12）
- WebShop 另比较 GPT-3.5 `gpt-3.5-turbo-instruct` 的 expert/Act-only prompt 与 ReAct prompt；ArCHer 的 GPT-2 base 在该设置超过二者，但 ReAct 因原 `text-davinci-002` 被弃用而换模型后明显退化，不能把该图解读为对原 ReAct 配置的无条件胜利。（物理页 11–12、24–27）
- token-level DQN 曾实现但未得到非零表现，故未进入主图；离线实验仅比较若干 ArCHer 目标组合、BC 与 Filtered BC，作者明确说因算力限制没有广泛对比离线 SOTA。（物理页 10、13–14）

在线主图报告 3 个随机种子的中位数；离线 Twenty Questions 表以 5 个种子共 1,280 条评估轨迹比较，IQL+AWR 为 -14.1，SARSA+AWR 为 -14.5，Filtered BC 为 -15.4，普通 BC 为 -16.8；直接 IQL+REINFORCE 坍塌到 -20，加入 BC 后为 -15.3。（物理页 11、13–14）

关键消融支持的边界较清楚：小 replay buffer（最近 48 rollouts）不稳定；MC critic regression 早期快但不能稳定利用混合策略数据；在线 IQL 在简单任务可加速探索、在 Twenty Questions 上会因有偏 policy-gradient signal 带来不稳定；长/多样 utterance 的 Guess My City 从 token baseline 获益，但多一个模型与更新开销。（物理页 12–14、28、33）

## 预算、模型与 oracle 边界

- 主实验 actor 多为约 100M 参数 GPT-2；critic 为 RoBERTa-base 加 CLS 线性头。双 Q/双 V 共享一个 encoder backbone 和不同 MLP head，actor 与 critic 参数独立；可选 token baseline 另用一套 GPT-2。仅在 Twenty Questions Subset 上把 actor 换成 Mistral-7B，且因其 zero-shot 已有非零奖励而跳过 SFT。（物理页 7、13）
- 作者明确把 7B 视为可承受预算上限；没有验证更大模型或更多 benchmark。论文也承认交互仍以“数千次”为量级，不能直接外推到约 100 次真实人类交互。（物理页 10、14）
- 在线 ArCHer 的公开超参数表：batch 256；每轮 critic 更新 50 次、actor 更新 3 次；replay buffer 10,000；每轮 rollout 在前四任务为 128、WebShop 为 512；actor warm-up 为 10/10/20/10/20 轮；discount 为 0.98/0.95/0.95/0.95/0.9。（物理页 33）
- Twenty Questions 和 Guess My City 的 oracle 不是人或精确符号器，而是以原数据监督微调的 `flan-t5-small`，替代原 benchmark 的 `flan-t5-xl`。Guess My City 观察到 agent 会诱导 oracle 泄露城市名，于是只对回复中出现目标名的情形硬编码为“I cannot answer that question.”；这只能堵住一种显式 reward hacking。（物理页 10、23、28、31）
- WebShop 在线主环境只用 instruction index 2000–2100 的 100 条子集；离线数据用 index 0–1000 并由 GPT-3 `text-davinci-002` 配合 ReAct prompt 收集。奖励是购买项与请求的相似度标量，并非现实用户满意度。（物理页 10、23）
- 所有方法都从任务相关的次优数据 SFT checkpoint 起步，以便早期探索；因此结果不代表从未适配 base model 直接进行 RL 的效果。（物理页 11、22–23）

## Failure、限制与可迁移风险

1. 证据主要来自小 GPT-2 actor、模拟环境和计算型奖励；唯一 7B 消融只覆盖较简单的 10-word Twenty Questions Subset，不能证明在大型通用 agent、真实 web 或人类交互上的同等可扩展性。（物理页 13–14）
2. 样本效率虽相对 PPO 高，绝对仍需数千至数万 trajectory；真实人类反馈预算约 100 次时并不适用，作者把 model-based RL 列为未来方向。（物理页 11–14）
3. oracle 与环境可被利用。Guess My City 中出现重复、乱码式提问和 oracle 自相矛盾；Twenty Questions 失败轨迹会无限重复同一问题。论文展示了这些失败而非仅展示成功例。（物理页 28–31）
4. CHAI 使用 `k=5` 且冻结 actor，较大的 candidate set 因算力未测；PPO 需要大 on-policy batch。主张中的“强基线”存在明确预算不对称，宜保留为同文实验事实，而非跨实现的终局优越性。（物理页 11–12、33）
5. 离线结果只是初步研究，缺少广泛离线 RL SOTA；直接 REINFORCE 会因 OOD action 快速坍塌，说明在线实例不能原样迁移到静态数据。（物理页 13–14）
6. 理论比较基于固定长度/填充后的等价 token MDP、Bellman completeness、density-ratio coverage、有限函数类与 FPE 子程序；它说明最坏情形 advantage 估计误差累积差异，但不等同于证明实际非线性 ArCHer 端到端收敛或达到实验性能。（物理页 8–9、33–39）
7. paper 中“current actor sampling”用于 V 回归且 critic/actor 循环耦合；实际效果依赖 warm-up、target networks、double-Q、replay 新旧分布和更新比，不能把核心简化成“把 token 奖励换成 utterance 奖励”后期待同效。（物理页 5–8、33）

## 页码定位索引

- 方法总览与单轮/多轮对比：物理页 1–4。
- MDP 定义、在线/离线目标、算法伪码：物理页 4–8。
- 理论主张：物理页 8–9；完整假设与证明：物理页 33–39。
- 任务、基线、主结果与消融：物理页 9–14。
- 环境、oracle、数据来源：物理页 22–24。
- prompting baseline 复现差异：物理页 24–27。
- 额外消融与 reward-hacking 轨迹：物理页 28–32。
- 精确超参数：物理页 33。

## 准入与第三读建议

- 准入判定：**准入**。理由是 changed computation 明确、训练时点和信息流可分解、在线主比较包含 PPO/Filtered BC/CHAI，并主动展示 replay、TD、baseline、offline objective 与 reward-hacking 的失败边界。此“准入”只表示可作为后续知识综合的论文来源，不构成 Candidate、novelty 或三审结论。
- 第三读：**建议**。第三读应窄化到三项：源码级确认 Q/V/advantage 的精确实现与序列 mask；核对 100x 主张在相同 wall-clock、token 数和 environment-call 数下是否仍成立；复查 Guess My City oracle exploitation 与 WebShop 100-instruction 子集是否主导收益。二读不联网，以上尚未核验。

