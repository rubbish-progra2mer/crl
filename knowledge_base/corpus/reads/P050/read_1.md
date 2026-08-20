# P050 Codex 首读：Agentic Verifier

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P050_agentic_verifier.pdf`
- PDF SHA-256：`81b1a3759a4de1b246240342435ef32f0f7d7265d17a938bd78086fe027b8654`
- 读取范围：全文（20 页），重点为主动反例生成、训练信号、Best@k 结果和 benchmark verifier 偏差。

## Changed computation

- [AUTHOR_FACT] 给定题目和一对候选程序，Verifier 多轮调用执行环境，生成满足约束且能使两个程序输出不同的输入 generator；最终以这些输入做 execution-based voting。
- [AUTHOR_FACT] 训练依次使用约 60K 成功轨迹 rejection fine-tuning，以及 10K queries、400 steps 的 GRPO；reward 只区分 invalid、相同输出、不同输出。
- [CODEX_SYNTHESIS] 可迁移机制是“评价者主动搜索最能区分候选假设的反例”，而不是在固定测试集上被动打分；代码任务只是实验载体。

## 关键结果与边界

- 两个 policy models、五个 coding benchmarks 上 Agentic Verifier 的 Best@8/64 总体最强；相对 vanilla 常见提升约 6–13 points，难题增益更大。
- 30B 训练 verifier 在 LiveCodeBench/OJBench 上超过 235B zero-shot verifier，支持任务化训练而非单纯更大模型。
- fixed benchmark tests 会把部分错误程序标为正确；主动生成输入可暴露候选间行为分歧，但“输出不同”本身不能判断哪一个正确。
- 训练对高质量 reference solutions、合成 tests、LLM validators 和 secure execution sandbox 依赖很强；validator 或 reference 错误会污染训练对。
- 大部分结果使用最多 512 test inputs；计算量显著增加，论文没有给出通用 Agent 任务上的外部有效性。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P050-E01 | method | §3.1, p.4 | pairwise counterexample search | [AUTHOR_FACT] 主动生成可区分输入。 |
| P050-E02 | training | §3.2–3.4, pp.5–6 | RFT + GRPO | [AUTHOR_FACT] 成功轨迹与稀疏执行 reward。 |
| P050-E03 | result | §4–5, pp.7–9 | five benchmarks | [AUTHOR_FACT] 跨模型/难度的 Best@k 增益。 |
| P050-E04 | limitation | §5.4, p.9 | imperfect benchmark verifiers | [AUTHOR_FACT+CODEX_SYNTHESIS] 分歧证据不等于正确性 oracle。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Active Discriminative Counterexample Search`
- Baseline：在固定或随机生成的测试输入上评价多个候选，增加数量但很少触及行为差异边界。
- Changed computation：评价者观察候选实现差异，主动提出并执行最可能使其分歧的有效输入，再用分歧证据缩小候选集或暴露 verifier 漏洞。
- 边界：必须有合法性检查；若没有可信 reference，反例只能证明不等价，不能自动指出正确候选。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Fixed Verifier False Positives Hide Behavioral Divergence`
- 现象：候选通过有限 benchmark tests 后被标为正确，但在有效输入空间仍与其他“正确”候选产生冲突输出。

## 首读裁决

`KEEP_FOR_SECOND_READ`。机制可迁移到 implement/评测设计，但正式 Card 必须与代码载体和大规模训练成本解耦。
