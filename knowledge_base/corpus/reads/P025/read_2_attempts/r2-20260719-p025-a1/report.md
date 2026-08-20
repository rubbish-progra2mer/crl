# P025 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p025-a1/invocation.md`；只读取 invocation、统一问题和指定的 27 页 PDF，未读取首读/Card/其他报告，未联网。
- [AUTHOR_FACT] 正文、理论、训练设置、消融和附录实现页均逐页检查。
- [OPEN_QUESTION] 使用 PDF 文本层，未逐页位图渲染；公式和表格文本连续，图形趋势未做像素级复核。

## 2. 方法改变的计算

- [AUTHOR_FACT] 论文诊断 ReMA 式 multi-agent RL 中 reasoning agent 变“懒”：多轮 GRPO 的 `1/T` 归一化会使长轨迹单步梯度缩小（理论与诊断，物理页 3–6）。
- [AUTHOR_FACT] Dr. MAMR 移除该轮数归一化，并加入基于反事实遮蔽/语义聚类的 causal influence reward 以及 restart reward；实验取 `α=β=0.1`（方法，物理页 6–9）。
- [AUTHOR_FACT] 遮蔽后的输出用 Qwen embedding 聚类，相似阈值约 0.9；restart 行为另有 SFT cold start（设置与附录，物理页 10–12、18–19）。
- [READER_INTERPRETATION] changed computation 同时包含梯度重标定、跨 agent 贡献奖励与故障重启，不是单一算子；主结果不能自动归因到其中任一项。

## 3. 理论边界

- [AUTHOR_FACT] 理论给出的梯度大小关系依赖轨迹长度及条件 `κ < T_L/T_S`（理论节，物理页 5–6）。
- [READER_INTERPRETATION] 该结论说明一种可能的优化偏置，不等于证明 `1/T` 在所有模型/任务中因果导致 lazy agent；它也没有排除奖励稀疏、角色冗余等原因。
- [OPEN_QUESTION] 原文没有单独在广泛设置中只移除 `1/T` 并控制其余奖励项，从而验证该理论机制的外部普适性。

## 4. 结果、基线与消融

- [AUTHOR_FACT] Table 1：7B 的 GRPO/ReMA/Dr. MAMR 平均为 55.08/51.97/58.43；14B 为 58.05/57.24/62.49（物理页 10–11）。
- [AUTHOR_FACT] 个别任务不单调，例如 14B MATH500 的 Dr. MAMR 80.4 略低于 GRPO 80.6，GSM8K 93.69 低于 94.5（Table 1）。
- [AUTHOR_FACT] 消融表显示移除各组成部分会降低总体表现；附录中的 process reward 尝试仍未阻止 collapse（物理页 12–13、20–22）。
- [READER_INTERPRETATION] 结果支持复合方法在所测数学 multi-agent 框架内有效，并支持“过程奖励本身不必然解决 lazy behavior”；不支持每个子算子均独立充分。

## 5. 成本、oracle 与公平性

- [AUTHOR_FACT] 训练 batch 128、每步 128 rollouts，使用 GPT-4o 生成 adversarial noisy reasoning；restart 数据使用 SFT cold start（设置/附录）。
- [OPEN_QUESTION] 未给出完整 GPU 数、训练时长与 dollar 成本，因此 128-rollout 方案的个人可复现实用性不明。
- [READER_INTERPRETATION] GPT-4o 噪声与 restart cold start 是额外教师/数据资源；与“完全从 base 纯 RL”表述需严格分开。

## 6. 负向结果和适用边界

- [AUTHOR_FACT] ReMA 在报告设置中可低于普通 GRPO，且不同任务仍有 Dr. MAMR 小幅退化（Table 1）。
- [READER_INTERPRETATION] Failure 候选：`Per-turn normalization can favor shorter/less active agent trajectories`；`Process reward alone may not prevent role collapse`。
- [READER_INTERPRETATION] restart 属于执行恢复机制；若 CRL 研究范围排除环境反馈/执行恢复，应只吸收 lazy-agent/credit 部分，不将 restart 作为核心方向。
- [OPEN_QUESTION] 未测试工具型开放环境、非数学任务、异质 agents，以及没有强模型合成噪声时的表现。

## 7. 可抽取资产与 Claim

- [READER_INTERPRETATION] Operator 候选：`Length-debiased multi-agent policy gradient`；次级候选为 `Counterfactual influence reward across agent messages`。
- [READER_INTERPRETATION] 窄 Claim：在论文的数学 multi-agent RL 设置中，移除轮数归一化并联合 contribution/restart rewards 的复合方案优于列出的 GRPO/ReMA 平均表现。
- [READER_INTERPRETATION] 不支持：Shapley 式奖励或 restart 单独产生全部增益；理论已证明普遍因果；方法成本适合个人常规训练。

## 8. 独立二读建议

`ACCEPT_WITH_NARROWING`。保留 normalization-induced laziness Failure 和训练 credit Operator；把 restart 标记为范围外/次要组成，并保留复合归因与算力缺失问题。本建议仅供主 Codex reconciliation。
