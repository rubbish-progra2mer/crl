# P024 Codex 首读：Multiagent Debate

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P024_multiagent_debate.pdf`
- PDF SHA-256：`80ecf57b31f248e6ce234412618aa6001d19630a9de0cf18c24cb60ae3a8054d`
- 读取范围：机制与 consensus（pp.1–4）、实验/分析/限制（pp.5–9）、复现实验、消融与成本（pp.12–15）。

## Changed computation

- [AUTHOR_FACT] 多个同类模型实例先独立回答；每一轮把其他 Agent 的回答与推理拼入当前 Agent 上下文，要求其更新自己的答案；重复数轮，末轮不一致时取多数答案（pp.1–4）。
- [CODEX_SYNTHESIS] 相比独立采样+多数投票，改变的是采样间的信息耦合：每条推理链能读取并修正其他链，但也因此失去独立性，产生从众与错误传播风险。

## Baseline、公平性与结果

- 主要设置使用 GPT-3.5、三 Agent、两轮；与单 Agent、一次 reflection、六个独立 Agent 的 majority 比较，后者大致匹配生成调用数（pp.4–5, 14）。
- Arithmetic/GSM8K 中 Debate 为 81.8/85.0，独立 majority 为 75.0/81.0；MMLU 为 71.1 vs 67.0（pp.5–6）。结果支持“交互超过纯采样”的窄主张。
- 论文还报告 GPT-4、Llama-7B、不同数据 split、prompt paraphrase、reasoning-chain 消融；只给最终答案低于给答案+推理（p.14 Table A7）。
- 成本并非严格相同：例如 MMLU 的 debate 生成 token 527.7，高于 majority 422.31；Chess reasoning 的 debate 199.5，远高于 majority 49.2（p.15 Table A9）。调用数近似不等于 token/上下文成本匹配。
- Biography 使用 ChatGPT judge，并在 100 个判断上人工准确 93/100（p.13）；这不是完全 oracle-free 的事实评测。

## 失败边界与未否定项

- [AUTHOR_FACT] 更“顺从”的短提示更快形成 consensus，却可能牺牲正确性；作者明确观察到 Agent 很 agreeable，且定性案例会收敛到错误答案（pp.4, 12–13）。
- [AUTHOR_FACT] 长 debate 受上下文处理能力与成本限制（p.9）；更多轮数/Agent 的提升主要在算术等小任务分析，不能外推为任意复杂 Agent 任务。
- [CODEX_SYNTHESIS] consensus 是行为相关性指标，不是真实性证据；一旦所有 Agent 共享同一误解，反复交流会放大而不是抵消误差。
- 未否定：角色/模型异质性、保留独立意见、外部证据或 adversarial critic 可能降低从众；本文并未比较真正独立且证据约束的 Reviewer。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P024-E01 | mechanism | §2.1, p.3 | Figure 2 后 | “responses from other agents are concatenated” | [AUTHOR_FACT] 交互式更新而非独立投票。 |
| P024-E02 | result | §3.1, p.5 | Table 1 | “3 agents and two rounds” | [AUTHOR_FACT] 主结果的调用结构。 |
| P024-E03 | failure | §2.2, p.4 | Consensus in Debates | “language model agents were relatively agreeable” | [AUTHOR_FACT] 从众是已观察机制。 |
| P024-E04 | negative_result | Appendix A.1, p.12 | prompt effect | “faster consensus at the expense of worse performance” | [AUTHOR_FACT] 一致速度与正确性可冲突。 |
| P024-E05 | cost | Appendix A.4, p.15 | Table A9 | “Average number of generated tokens” | [AUTHOR_FACT] 各策略的 token 并未统一。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

Multi-agent reflection/debate 祖先与强 baseline；同时是“Reviewer 必须独立且不能以共识替代证据”的 Failure 来源。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Cross-Trajectory Critique Update`
- Baseline：独立生成后直接多数投票，或同一实例只反思自己的答案。
- Changed computation：每个实例在保留自身轨迹的同时读取其他实例的完整推理并再生成。
- 前提：实例初始差异足够；共享信息不含隐藏答案；总 token/轮数作为公平预算记录。
- retrieval vocabulary：multiagent debate, cross-agent critique, majority baseline, consensus, reasoning-chain exchange。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Consensus Without Independent Evidence`
- 条件：同源模型共享偏差，更新提示鼓励采纳其他回答，且没有外部证据或独立裁决。
- 现象：consensus 快速上升但可能收敛到共同错误；更顺从不等于更正确。
- 替代解释：部分错误源于上下文长度、提示措辞或任务歧义，而非 debate 必然失败。
- 未否定：程序化 verifier、来源绑定或真正独立 skeptic 可使交互有效。

## 首读裁决

`KEEP_FOR_SECOND_READ`。作为祖先/基线必留；二读应复核成本匹配和 consensus 误用边界。
