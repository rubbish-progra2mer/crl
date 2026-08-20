# P027 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p027-a1/invocation.md`；只核读 invocation、统一问题和指定的 13 页 PDF，未读取首读、Cards、其他报告或 blind query，未联网。
- [AUTHOR_FACT] 13 页正文/附录逐页检查，重点核对数据生成过滤、对照、三次运行和额外 token 表。
- [OPEN_QUESTION] 核读基于 PDF 文本层，未逐页位图渲染；表格解析未见明显字段错位。

## 2. 方法改变的计算

- [AUTHOR_FACT] CSO 从 policy 的失败轨迹逐步取状态，由强 expert 为每一步生成 5 个替代动作；process reward model 分别评价原动作与替代动作（方法，物理页 3–5）。
- [AUTHOR_FACT] 论文按 policy 分数 `<0.45` 且 expert 分数 `>0.65` 筛选，随后让 policy 从替代动作继续执行，并只保留最终 gold verification 成功的分支；成功替代动作与原动作形成 DPO preference pair（算法，物理页 4–6）。
- [READER_INTERPRETATION] changed computation 位于训练数据构造，而非部署时 agent loop：用“失败局部状态 + 专家反事实动作 + 最终 oracle 验证”产生 step-level 偏好。

## 3. 输入、输出与信息边界

- [AUTHOR_FACT] 输入是失败 rollout 的中间状态、原 policy action、gold task outcome、expert 与 PRM；输出是通过验证的 chosen/rejected action pair，供两轮 DPO 训练（方法/设置，物理页 4–7）。
- [AUTHOR_FACT] expert 为 Claude-3.7，且 PRM 也由同类闭源强模型提供；训练模型是 CK-Pro-8B，初始 SFT 数据约 47k（实验设置，物理页 6–7）。
- [READER_INTERPRETATION] 该 Operator 需要训练期 oracle answer 和强教师，不是无需外部监督的 autonomous self-improvement。

## 4. 基线、结果与消融

- [AUTHOR_FACT] 在 GAIA-Text 103 题和 XBench 100 题上，基础模型为 35.9/23.0，CSO 为 49.5/29.0；结果按三次运行报告（Table 1，物理页 7–8）。
- [AUTHOR_FACT] StepDPO 为 38.9/25.0，IPR 为 44.6/24.0，构成更接近的数据优化基线（Table 1）。
- [AUTHOR_FACT] PRM+verification 得到 671 pairs；去 PRM 为 1967，去 verification 为 4126；去 PRM 的 GAIA 结果 48.5，接近完整方法 49.5（消融，物理页 8–9）。
- [READER_INTERPRETATION] 最终验证是强质量过滤；PRM 主要提高数据选择精度/效率，但其独立效果从结果上不强。

## 5. 成本与替代解释

- [AUTHOR_FACT] 额外生成 token 每轮约 168M，StepDPO 约 141M，ETO 约 212M；该口径不等于包含共享 rollout、API 价格和 wall-clock 的总成本（成本分析，物理页 9–10）。
- [READER_INTERPRETATION] 强 expert 本身可能贡献动作质量，gold verification 则提供任务级 oracle；提升不能被描述成小模型仅凭自身失败自主学会。
- [OPEN_QUESTION] expert 与 PRM 来自相关模型可能造成相关偏差；没有独立 PRM 来源消融。
- [OPEN_QUESTION] 未给出闭源调用的完整货币成本、失败任务探索成本及个人硬件复现成本。

## 6. 负向结果与边界

- [AUTHOR_FACT] 去 PRM 会保留更多 pairs 而效果仅小幅下降，说明分数阈值并非全部增益来源（消融表）。
- [READER_INTERPRETATION] Failure 候选：`Training-time self-improvement claim hides expert and gold-oracle dependence`；`Same-source expert and critic can share blind spots`。
- [OPEN_QUESTION] 没有 gold outcome、无法可靠执行工具、或 expert 不能访问同一状态时，方法是否仍成立未测试。

## 7. 可抽取资产与 Claim

- [READER_INTERPRETATION] Operator 候选：`Verified counterfactual step optimization from failed trajectories`。
- [READER_INTERPRETATION] 窄 Claim：在有 gold verifier 与 Claude expert 的两个文本 agent benchmark 上，将验证成功的局部替代动作制成 DPO pairs 可提高 8B agent 表现。
- [READER_INTERPRETATION] 不支持：无 oracle 自我改进；PRM 是必要组件；token/费用比其他训练方案更优；可直接迁移到开放式科研任务。

## 8. 独立二读建议

`ACCEPT_WITH_NARROWING`。适合作为“失败轨迹到局部偏好数据”的训练算子，但必须在 Card 中醒目标注 gold verifier、强 expert、闭源 PRM 与成本边界。本建议仅供主 Codex reconciliation。
