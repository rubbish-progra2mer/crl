# P077 独立定向三读报告

## 读取与来源

- 论文：*ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL*。
- 来源：`knowledge_base/staging/plan05_sat_a3/P077_archer.pdf`。
- SHA-256：`9a25030a872732dc5fc544e04e3d20382be1d512eeefd97e7e92179dd2c5f8ec`（读取前本地复核一致）。
- 阅读范围：物理页 1–39，逐页阅读全文；未联网，遵守 `procedural_blinding`。

## Changed computation 核对

ArCHer 真正改变的是训练计算的时间尺度分工，而不是简单给 token-level PPO 换一个 reward。高层把一次完整 utterance 当 action，以历史交互为 state，用 replay buffer 上的 off-policy TD 学习 utterance-level `Q(s,a)`；Q 的 Bellman target 是 `r + γ V̄(s')`。另一个 `V(s)` 回归当前 actor 自回归采样 utterance 在延迟 Q 下的期望值（物理页 5–6，式 1–2）。低层仍是 token-level actor，但将高层 utterance advantage 作为整个 utterance 结束时的终端回报，对该 utterance 内全部 token 做 REINFORCE 更新（物理页 6，式 3；算法总表见物理页 8）。这使低层 actor 更新可以“in silico”进行而不增加环境交互，环境数据则被高层 replay 反复复用（物理页 5、8）。

可选的低层 baseline `Ṽ(s_c,a_{1:i-1})` 不是高层 `V(s)`：它对 token prefix 回归 utterance advantage 的 Monte-Carlo return，再从同一个 utterance-level advantage 中逐 token 相减以降方差（物理页 6，式 4–5）。离线变体又改为高层 IQL 与 actor AWR（物理页 7）。因此必须区分三类量：高层 Q、高层 V，以及可选的低层 token-prefix baseline。

实现边界并未完全闭合。主实验以 GPT-2 为 actor、RoBERTa-base 加线性头为 critic；训练两套 Q/V 头并共享同一 encoder backbone，actor 与 critic 参数独立，可选低层 baseline 再用独立 GPT-2（物理页 7）。论文只写 advantage “using a minimum over Q1, Q2 and V1, V2”，没有给出双 Q/双 V 组合的明确代数式，也未说明是 `min(Q)-min(V)`、配对差值后取最小，还是其他实现。因此 Q/V/advantage 的概念边界清楚，但双估计器的精确实现边界不能仅凭本文复原。

## “100x”与预算公平性

“100x”只被物理页 12 的一个阈值比较直接支持：Twenty Questions 上，PPO 用超过 100k 个样本才达到略高于 -17 的平均回报，ArCHer 用少于 1k 个样本达到同一回报；相关图的横轴明确标为 trajectories（物理页 11–12、24）。因此可接受的表述是“在该任务和该回报阈值上，按收集轨迹数至少约 100x”。

不能把它扩张为以下等价性：

- 不是等 environment steps/calls。每条轨迹最多 20 个问题但可提前终止，论文未报告两方法在对应阈值前累计的实际 turn 数或 oracle 调用数（物理页 10、23）。
- 不是等生成 token 数。没有累计输入/输出 token、序列长度或解码开销统计。
- 不是等训练计算。PPO 每次更新需 1024/2048 条 on-policy 轨迹，ArCHer 每轮 128 条；两者 batch、actor update、critic update、epoch 数也不同（物理页 24、33）。ArCHer还额外训练 Q/V critic 并从 actor 采样 utterance 来拟合 V。
- 不是等 wall-clock。论文没有给出 ArCHer 与 PPO 达到该阈值的时间；唯一明确的相对运行时是 CHAI 在 `k=5` 时约为 ArCHer 的 4 倍（物理页 11），不能外推到 PPO。

公平性方面，论文声明算法无关的模型架构、学习率等尽量一致，并让所有方法从同一类次优 SFT checkpoint 初始化（物理页 11）；在线曲线报告三种子中位数（物理页 11）。但上述相同项不足以把“trajectory sample efficiency”转换为 token/FLOP/wall-clock efficiency。

## Oracle、reward hacking 与评测边界

Twenty Questions 与 Guess My City 的 oracle 不是人或规则真值，而是为节省计算、在公开数据上训练的 `flan-t5-small`；原基准使用 `flan-t5-xl`（物理页 10、23）。Guess My City 允许自由问答，作者明确观察到 agent 会诱导 oracle 直接输出城市名，随后只增加“若回复中出现城市名，则替换为固定拒答”的补丁（物理页 23）。这只堵住字面泄露，不保证 oracle 不以别名、矛盾回答、错误肯定或其他可利用模式泄露信息。

附录的实际轨迹进一步显示问题未消失：模型产生畸形重复问题，oracle 却返回肯定；另一个例子反复询问 London 并不断得到肯定（物理页 31）。作者也承认自由回答 oracle 的漏洞、幻觉和 OOD 回复会使对话陷入无意义重复（物理页 28、31）。因此 Guess My City 的回报改善不能干净归因于更好的信息搜寻策略，必须保留 oracle exploitation 的替代解释。Twenty Questions 成功轨迹较自然，但失败轨迹也会重复同一问题（物理页 29–30）。WebShop 使用 0–1 稠密相似度奖励并允许部分匹配得分（物理页 23、32），故“成功”也不等于严格满足全部购买约束。

## 争议结论

1. “ArCHer 100x more sample efficient than PPO”可在“Twenty Questions、达到约 -17、以轨迹计数”这一窄合同下成立；作为跨任务、等调用、等 token、等算力或等时间结论不成立。
2. “learns strategic behavior rather than exploiting the environment”证据不足。附录展示自然策略，但也展示 oracle 可利用轨迹；作者的字面城市名过滤不能排除更广泛 reward hacking。
3. “advantage 的实现可由论文完整复现”不成立；单 Q/V 定义与低层 baseline 角色可复原，双 Q/双 V 的具体组合仍欠规格。
4. 理论结果比较的是满足强假设的拟合策略评估误差，不能自动证明主实验中的神经实现或 100x 曲线；理论与实证应分开引用（物理页 8–9、34–39）。

## 准入裁决

**有限准入。** 准入：（a）utterance-level off-policy TD critic + token-level on-policy actor 的 changed computation；（b）在 Twenty Questions 指定阈值上按轨迹数观察到至少约 100x 的窄样本效率现象；（c）off-policy replay 与可选 token baseline 的消融方向。拒绝准入：（a）等 environment call/token/FLOP/wall-clock 的 100x；（b）无 reward hacking 的机制归因；（c）精确双 Q/双 V advantage 实现已经由本文闭合。任何后续引用必须同时携带轨迹口径、单任务阈值和 oracle 漏洞边界。

