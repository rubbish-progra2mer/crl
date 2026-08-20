# P013 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P013_intrinsic_self_correction_limits.pdf`
- PDF SHA-256：`d172f0b3e933544f5165250338e3e989036e8d826fea34093e6aed4adb5b042a`
- 读取时间：`2026-07-19T15:42:00+08:00`
- 读取范围：逐页检查 1–17 页；正文 1–9 页，参考文献 9–12 页，完整 prompts 与正/负/不变案例及 constrained-generation 对照 13–17 页。

## 研究对象与定义边界

- [AUTHOR_FACT] 论文把 intrinsic self-correction 严格定义为：不借助 human、gold answer、tool、external model/knowledge 的外部反馈，仅由模型根据自身已有输出生成 critique 并重答 reasoning task。
- [AUTHOR_FACT] 它审计三类常见归因：oracle label 控制停止、multi-agent debate 相对等 response self-consistency、feedback prompt 比 initial prompt 含更多任务要求。
- [READER_INTERPRETATION] 本文核心不是提出新解题 Operator，而是一组科研 Failure/evaluation Operators。标题中的“cannot … yet”只覆盖所测 2023-era models、reasoning benchmarks 与最多两轮的 intrinsic setting，不能外推 grounded reflection、style/safety correction 或后续模型。

## 设置与公平性控制

- GSM8K 1319 test、CommonSenseQA 1221 dev、HotPotQA 100-question Reflexion subset。GPT-3.5 用完整集；GPT-4/4-Turbo/Llama-2 因成本只随机采 200（HotPot 100），未报告重复 sampling CI。
- GPT-3.5/GPT-4 temperature=1，GPT-4-Turbo/Llama-2 temperature=0；最多两轮，每轮总 calls 从 1→3→5（feedback+revision 各一 call）。不同 decoding 条件跨模型不可直接比较“稳定性”。
- Oracle setting 使用 gold correctness 决定是否停止：初答正确则不改，错误才迭代。Intrinsic setting 去除 label，由模型自行决定 retain/change。因此 oracle gain 已机械排除 correct→incorrect transitions。
- Debate 复现 GPT-3.5-0301、3 agents、2 rounds；比较相同“初始 agents 数”与相同总 responses。3/6/9 response self-consistency 用 majority vote。
- Prompt audit 把 constrained-generation 的 `ALL concepts` 约束前移到 initial instruction，然后再应用原 feedback/refine，检验 gain 是否只是迟到的任务说明。

## 主要结果与窄 Claim

- Oracle Table 2：GPT-3.5 GSM8K/CSQA/HotPot 75.9/75.8/26.0→84.3/89.7/29.0；GPT-4 95.5/82.0/49.0→97.5/85.5/59.0。它证明有真实 correctness oracle 时 retry 有用，不证明模型能自判。
- Intrinsic Table 3：GPT-3.5 五 calls 后 74.7/41.8/25.0，均不高于 75.9/75.8/26.0；GPT-4 89.0/80.0/43.0，不高于 95.5/82.0/49.0。Table 4 GPT-4-Turbo/Llama-2 亦下降，多组 feedback prompts 无法逆转。
- Transition Figure 1：GPT-3.5 GSM8K correct→incorrect 8.8% > incorrect→correct 7.6%；CSQA 39.8% vs 5.8%。GPT-4 更常不变，但仍可能破坏正确答案。关键失败是 verifier discrimination，而不是完全不会生成另一答案。
- Debate Table 7：3-response debate round1 83.2 vs SC3 82.5；总 6 responses 时 SC6 85.3 > debate 83.2，总 9 时 SC9 88.2 > debate round2 83.0。若不等总生成数，容易把 sampling/selection gain 误称 critique gain。
- Constrained Table 8：原 prompt 44.0→self-correct 67.0（作者复现 53.0→61.1）；明确 `ALL` 的一次 initial prompt 81.8，再加原 self-correction 降至 75.1。说明 feedback 中新增 task constraint 是主要混杂。

## 失败边界与限制

- [AUTHOR_FACT] Intrinsic critique 会受“请找问题”类 prompt 驱动，常把正确答案改错；CSQA 的 distractors 都表面相关时尤其严重。
- [AUTHOR_FACT] 论文明确不否定 external tool/verifier/human feedback；code executor、calculator、search 或训练 critique model 可提供额外信息，属于不同 setting。
- [AUTHOR_FACT] 论文也不覆盖所有域：style、preference 或 safety criteria 可能更易由 LLM 自评；结论聚焦 reasoning correctness。
- [AUTHOR_FACT] HotPot sample 仅 100，作者因此不做 transition statistics；其单次 10-point GPT-4 oracle change 不应被当稳定总体估计。
- [READER_INTERPRETATION] “正确初答应已是 prompt/decoder 下最优”是作者直觉解释，不是形式证明；新的 stochastic search、latent verifier 或训练变化可能改变结论。
- [READER_INTERPRETATION] Self-consistency 本身依赖可规范化答案与 majority，复杂 agent trajectory/开放输出没有直接可用的等价 voting baseline；等 token/call 原则保留，但具体 baseline 需按任务设计。
- [READER_INTERPRETATION] 该审计针对同模型自评。独立强 verifier/critic 即使不是环境 oracle，也属于 external feedback；其可靠性应单独测，不应被标签为 intrinsic。

## 可抽取候选（尚非正式 Card）

- Evaluation Operator：`Feedback-Provenance Separation`——明确区分 intrinsic critique、oracle correctness、tool execution、human/other-model feedback，分别报告，禁止混称 self-correction。
- Evaluation Operator：`Equal-Response/Token Correction Baseline`——按总 responses/calls/tokens 对齐 self-consistency、best-of-N 或 search，隔离额外 compute。
- Evaluation Operator：`Initial-Prompt Information Parity`——feedback 中的任务约束必须也出现在强 initial baseline，避免“迟到说明”伪装成迭代收益。
- Failure：`Intrinsic Critique Flips Correct Reasoning`——无新信息的 problem-seeking prompt 对正确输出施加改变偏置，correct→incorrect 抵消甚至超过修正。
- Failure：`Oracle-Gated Retry Masquerades as Self-Verification`——gold correctness 只让错误样本 retry，机械保护正确样本，使 gain 不能证明自判能力。
- Failure：`Debate Gain Collapses Under Equal Sampling Budget`——交互 critique 在相同总 responses 下不及简单 majority，收益来自采样而非辩论计算。

## 未解决问题

- `[OPEN_QUESTION]` 当前更强模型在相同 prompts/temperature/完整数据集上是否仍复现，本文不能回答。
- `[OPEN_QUESTION]` 若用独立且 calibration 明确的 verifier，但不访问 gold/tool，属于何种“external”层级及净收益，本文未系统研究。
- `[OPEN_QUESTION]` 开放式 agent trajectories 的等预算 baseline 如何定义，不能直接套用答案 majority。
- `[OPEN_QUESTION]` 多轮中正确性置信度、abstain/retain gate 是否能减少 correct→incorrect，论文只测固定 prompts。
