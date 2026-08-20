# P024 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p024-a1/invocation.md`；只核读 invocation、统一问题和指定的 31 页 PDF，未读取其他知识资产，未联网。
- [AUTHOR_FACT] 正文和附录逐页检查，重点核对 reasoning/factual 表、agents/rounds 消融、agreeability 与 token 表。
- [OPEN_QUESTION] 采用 PDF 文本层核读，未逐页位图渲染；表格值可提取且未发现明显错位，图中连续曲线仅作定性理解。

## 2. 方法改变的计算

- [AUTHOR_FACT] 多个同模型 agent 先独立作答，随后每轮看到其他 agents 的回答并修订自己答案，最终在有分歧时以多数答案汇总（方法，物理页 2–4）。
- [AUTHOR_FACT] 主要配置为 3 agents、2 rounds；agents 是同一基础模型的独立对话副本（设置，物理页 4–5）。
- [READER_INTERPRETATION] changed computation 是迭代式 peer-answer exposure；它增加独立采样和交叉条件化，但并未引入独立知识源或真正异质审稿人。

## 3. 结果与最接近基线

- [AUTHOR_FACT] Table 1 中单体在 arithmetic/GSM8K/chess 为 67.0/77.0/91.4，debate 为 81.8/85.0/122.9；Reflection 在 GSM8K 为 75.0，低于单体 77.0（物理页 5–6）。
- [AUTHOR_FACT] Table 2 中 debate 在 biography/MMLU/chess 为 73.8/71.1/45.2；Reflection 的 MMLU 为 57.7，低于单体 63.9（物理页 6–7）。
- [AUTHOR_FACT] majority-vote 也是关键近邻基线，在 Table 1 为 75.0/81.0/105.0，通常弱于完整 debate（物理页 5–6）。
- [AUTHOR_FACT] 增加 agents/rounds 在部分任务继续增益，但并非所有设定单调改善；较长上下文会恶化表现（消融与附录）。

## 4. 成本与替代解释

- [AUTHOR_FACT] 附录 Table A9 显示 debate 生成 token 远高于 single：例如 arithmetic 548 对 95.6，GSM8K 524 对 111.5，MMLU 527.7 对 91.7，validity 306 对 39（物理页 24–25）。
- [READER_INTERPRETATION] 优势可能部分来自约 5–8 倍生成预算和多次独立采样；与 single/reflection 的质量差不能直接等同于“讨论机制”的纯效应。
- [READER_INTERPRETATION] Majority 基线削弱了“仅因多样采样”的解释，但没有形成严格等 token、等调用次数的对照。
- [OPEN_QUESTION] 原文未报告统一 dollar/latency 预算下的 Pareto 比较。

## 5. 负向结果与边界

- [AUTHOR_FACT] 作者观察到模型具有 agreeability：后轮会接受其他 agent 的答案；错误共识可能被复制，长上下文也会带来退化（分析/案例与附录）。
- [AUTHOR_FACT] Reflection 在部分任务低于 single，表明同一模型自我修订不是稳定提升机制（Table 1–2）。
- [READER_INTERPRETATION] 可记录 Failure：`Homogeneous peers can converge on correlated error`；`Debate gain may be paid for by large sampling/token expansion`；`Self-reflection can degrade without new evidence`。
- [OPEN_QUESTION] 论文年代和模型较早，未验证现代 tool-using agent、异质模型或真实长程行动轨迹。

## 6. 可抽取资产与 Claim

- [READER_INTERPRETATION] Operator 候选：`Iterative peer-answer exposure before final aggregation`。
- [READER_INTERPRETATION] 窄 Claim：在论文所测早期语言模型和若干推理/事实任务中，3-agent 2-round debate 通常优于单体、reflection 和简单 majority。
- [READER_INTERPRETATION] 不支持：同质 debate 是成本有效的普遍提升；共识等同于正确；多轮一定优于单轮；该机制可直接替代独立 Reviewer。

## 7. 独立二读建议

`ACCEPT_WITH_NARROWING`。作为 multi-agent/reflection 早期机制和负向边界来源有价值；所有正式 Claim 必须附带同质性、token 放大和旧模型边界。本建议仅供主 Codex reconciliation。
