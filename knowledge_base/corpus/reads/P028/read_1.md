# P028 Codex 首读：Memory-R1

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P028_memory_r1.pdf`
- PDF SHA-256：`c206af4e792e9550f2aaec8a6c4d9b141d1ddcb587e781d7866870c8f3e4dd4f`
- 读取范围：问题/方法（pp.1–5）、主结果/消融（pp.6–9）、案例与训练构造（pp.11–13）、实现与扩展结果（pp.15–18）。

## Changed computation

- [AUTHOR_FACT] Memory Manager 对新对话信息与检索到的旧记忆选择 ADD/UPDATE/DELETE/NOOP；操作后的 bank 交给冻结 Answer Agent，以最终 QA exact match 训练 Manager（pp.3–5）。
- [AUTHOR_FACT] Answer Agent 从相似度检索的 60 条候选记忆中显式先选相关条目再回答，也以 exact match 做 PPO/GRPO；两 Agent 分阶段、交替冻结（pp.5, 15–17）。
- [CODEX_SYNTHESIS] 可迁移核心不是 CRUD 本身，而是把写入决策与下游可用性绑定；“存得像摘要”不等于“能支持未来问题”。

## Baseline、公平性与结果

- LoCoMo 训练仅 152 QA；测试 1307，排除 adversarial 子集；再 zero-shot 测 MSC/LongMemEval。比较 LoCoMo-RAG、A-Mem、Mem0、MemoryOS 及同架构 GPT-5 轨迹 SFT（p.5）。
- LLaMA-8B GRPO overall F1/B1/J 45.02/37.51/62.74，Memory-SFT 为 42.81/32.98/58.76；Qwen-7B GRPO 为 43.14/36.44/61.51（p.6）。并非所有 metric/type 上 RL 都优于 SFT或 PPO，例如 Qwen-7B J 低于 Memory-SFT。
- 去 Manager、Answer Agent、Distillation 均下降，但 Figure 5 的 ablation 组合/轴值有限；Answer Agent PPO 会提高 F1/B1 却使 J 从 59.4 降至 57.5，说明指标存在目标错配（p.7）。
- 以 LLM judge 做训练奖励会得到更冗长回答、J 更高而 F1/B1 更低；作者最后选择 EM 以保持短答案比较（p.8 Table 2）。这是 reward-induced style shift 的直接证据。
- 主要训练需 4×H100 80GB，14B 需 8×H100（p.15）；不是适合本机 commissioning 的轻量训练方案。

## 来源冲突与失败边界

- [SOURCE_CONFLICT] Appendix B.2 prose 称 temporal bank 由“previous 24 turns”构建，而紧邻 Algorithm 1 line 5 写“previous 50 turns”（p.13）。正式 Evidence 不得确定该窗口，二读必须核对代码/版本。
- [AUTHOR_FACT] 训练 Manager 时 reward 来自冻结 Answer Agent，因此 Manager 会适应该 Answer Agent 的能力/偏差；换下游模型后写入策略未必仍最优。
- [CODEX_SYNTHESIS] Exact match 只覆盖与现有 QA 相关的记忆，可能鼓励删除暂时无奖励、未来却重要的信息；152 QA 的高样本效率不等于覆盖通用 lifelong memory。
- 60 条候选与专门 Answer Agent 将 retrieval recall、selection 和 answer reasoning 混在一起；性能增益不能单独归因“记忆蒸馏”。
- 未否定：简单 reranker、更多 retrieved context 或更强 Manager 可贡献增益；论文的 latency 分析没有完整纳入写入所有历史的累计成本。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P028-E01 | mechanism | §3.1, p.4 | Eq.1–4 | “effect on downstream QA” | [AUTHOR_FACT] 写操作以最终可用性优化。 |
| P028-E02 | mechanism | §3.2, p.5 | Memory Distillation | “60 candidate memories” | [AUTHOR_FACT] 先宽召回再 learned selection。 |
| P028-E03 | result | §4.2, p.6 | Table 1 | “Memory-R1-GRPO” | [AUTHOR_FACT] 主表多指标结果。 |
| P028-E04 | reward_failure | §4.4, p.8 | Table 2 | “J-based reward ... verbose outputs” | [AUTHOR_FACT] 训练指标改变输出风格并损害其他指标。 |
| P028-E05 | conflict | Appendix B.2, p.13 | prose vs Algorithm 1 | “preceding 24 turns” / “previous 50 turns” | [SOURCE_CONFLICT] 训练窗口不一致，暂缓正式事实。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

Memory learning 的 Operator/Failure 来源；必须携带训练窗口冲突与下游 reward 依赖。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Downstream-Utility-Grounded Memory Operation`
- Baseline：LLM 依提示启发式决定 ADD/UPDATE/DELETE/NOOP。
- Changed computation：对候选写操作实际形成 memory state，以冻结回答器的终局正确性优化选择。
- 前提：未来任务分布由训练 QA 代表；reward 不奖励泄漏；候选记忆和写入成本一致。
- retrieval vocabulary：memory manager, learned CRUD, downstream utility, memory distillation, outcome reward。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Answer-Reward-Induced Memory Myopia`
- 条件：写入/删除仅由小规模当前 QA 的终局分数监督。
- 现象：策略可能保留对当前回答器有利的信息，删除暂未被问但未来有用的信息；输出还会适应具体 metric 风格。
- 替代解释：跨 benchmark zero-shot 增益说明部分策略可迁移，但不足以证明开放长期分布。
- 未否定：多任务/保留约束或反事实未来 query 可减少短视。

## 首读裁决

`KEEP_FOR_SECOND_READ`，且因来源自相冲突必须把代码/附录版本核验列为二读硬项。
