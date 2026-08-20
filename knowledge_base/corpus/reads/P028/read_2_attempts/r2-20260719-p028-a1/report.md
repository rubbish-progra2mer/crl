# P028 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p028-a1/invocation.md`；只核读 invocation、统一问题及指定的 20 页 PDF，未读取其他读稿或知识资产，未联网。
- [AUTHOR_FACT] 正文与附录逐页检查，专门复核了 temporal-memory 构造、LoCoMo 统计、PPO/GRPO 与 compute 设置。
- [OPEN_QUESTION] 本次使用 PDF 文本层；关键冲突来自同一解析页内的正文与算法文本，不依赖位图判断，但其余复杂图形未逐页位图复核。

## 2. 方法改变的计算

- [AUTHOR_FACT] Memory-R1 包含 Memory Manager 与 Answer Agent：前者对 memory 执行 ADD/UPDATE/DELETE/NOOP，后者从检索的 60 条 memories 中提炼证据并作答（方法，物理页 3–5）。
- [AUTHOR_FACT] 两个 agent 分开用 PPO/GRPO 训练；Manager 由下游 exact-match QA reward 驱动，Answer Agent 也以 exact match 学习 memory utilization（方法/算法，物理页 4–6）。
- [READER_INTERPRETATION] changed computation 是把 memory write policy 与 memory read/distill policy 都变成任务回报训练的决策过程，而非只优化 embedding retrieval。

## 3. 输入、输出与干预时点

- [AUTHOR_FACT] Manager 输入当前对话/临时 memory 与已有 memory bank，输出 CRUD 动作；Answer Agent 输入 query 与 top-60 retrieval，输出压缩证据和答案（物理页 3–6）。
- [AUTHOR_FACT] 训练/测试使用 LoCoMo，并在 MSC、LongMemEval 做 zero-shot；LoCoMo 报告 152/81/1307 的 train/validation/test 规模（实验设置，物理页 6–8）。
- [AUTHOR_FACT] 训练使用 LLaMA/Qwen 的 3B/7B/14B 变体；多数设置为 4 张 H100，14B 为 8 张 H100（附录设置，物理页 14–15）。

## 4. 结果与归因边界

- [AUTHOR_FACT] Table 1 报告 Memory-R1 在 LoCoMo 多数组合明显优于非 RL memory baselines，并有跨数据集结果（物理页 7–9）。
- [AUTHOR_FACT] 并非所有 RL 配置都胜过 SFT：例如某 Qwen PPO 汇总值 59.53 低于 SFT 61.13，GRPO 61.51 仅略高（Table 1）。
- [AUTHOR_FACT] temporal memory 构造与部分 SFT trajectories 使用 GPT-4o-mini / GPT-5 作为外部模型（设置/附录，物理页 6–7、13–16）。
- [READER_INTERPRETATION] 主结果来自 learned CRUD、learned readout、外部 temporal memory、模型规模与训练算法的组合；不能把全部提升归因于 Manager CRUD。

## 5. 原文内部冲突

- [AUTHOR_FACT] 物理页 13 的实现说明写 temporal memory bank 使用 preceding 24 turns；同页 Algorithm 1 第 5 行写 previous 50 turns。
- [OPEN_QUESTION] 24 与 50 无法同时描述同一 temporal-memory 窗口，原文未解释是不同阶段、笔误或版本差异；该参数直接影响可复现输入与信息预算。
- [AUTHOR_FACT] 主文物理页 5 将 LoCoMo 会话描述为约 600 turns、26k tokens，附录物理页 12 则给出平均约 300 turns、9k tokens。
- [OPEN_QUESTION] 两组统计是否采用不同格式/切分/过滤口径没有被定义清楚。

## 6. 成本、oracle 与公平性

- [AUTHOR_FACT] Answer Agent 每题可看到 60 条 retrieval；训练使用 4–8 张 H100，并借助 GPT 系列模型生成中间资产（设置/附录）。
- [READER_INTERPRETATION] 与不使用 external temporal-memory teacher 或不同 retrieval count 的基线比较时，需保留信息量和教师差异。
- [OPEN_QUESTION] 未给出端到端 token、API 与 GPU 小时成本，也未在统一开销下比较 learned manager/readout。

## 7. 负向结果、资产与 Claim

- [READER_INTERPRETATION] Operator 候选：`Downstream-reward-trained memory CRUD`；`RL-trained evidence distillation over retrieved memories`。
- [READER_INTERPRETATION] Failure 候选：`RL does not consistently beat SFT across model/algorithm combinations`；`Memory-window ambiguity blocks reproducibility`。
- [READER_INTERPRETATION] 在参数冲突解决前，可暂存机制描述，但不宜形成带精确配置的强实证 Claim。
- [READER_INTERPRETATION] 不支持：所有 RL memory agent 都优于 SFT；结果只来自 CRUD；无需外部教师；当前文本足以完整复现。

## 8. 独立二读建议

`NEED_THIRD_READ`。第三读应优先查明 24/50 turns 与 600/300 turns 两组冲突，必要时核对作者代码或版本记录；在冲突解决前不生成正式强 Claim。本建议仅供主 Codex reconciliation。
