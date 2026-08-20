# P037 Codex 首读：ToolSandbox

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P037_toolsandbox.pdf`
- PDF SHA-256：`3449baed1d8e0f4c07dbc859621899685eed8a6a0445a1ae8909c178e6b6173e`
- 读取范围：正文（pp.1–10）及 scenario、metric、prompt/user-simulator 细节。

## 研究对象

- [AUTHOR_FACT] ToolSandbox 用可变 world state、on-policy user simulator、milestones 与 minefields 评价任意轨迹，不要求复现单一预定动作序列。
- [CODEX_SYNTHESIS] 其可迁移贡献主要是“结果等价 + 中间禁止条件”的评价对象，而非其 sandbox 工程。

## 关键结果

- GPT-4o 平均 73.0；但 Insufficient Information 仅 42.0。弱模型因几乎不调用工具反而在该列取得虚高分，说明单一子指标会奖励退化策略。
- 多工具、多用户轮、state dependency 随模型变小下降更快；较大模型在 state dependency 上也可能因错误并行调用而不及较小模型。
- distraction/name/description/type scrambling 的影响随模型而变，说明 tool schema 表面信息是重要混杂项。
- 状态依赖、canonicalization、insufficient information 是可区分的 failure；最终 task score 会把它们混在一起。

## 边界

- state dependency 中大量恢复/重试行为属于用户明确排除的“环境反馈学习与执行恢复”研究方向，不从中生成该方向 Operator；仅保留它作为 tool evaluation 的实验载体。
- user simulator 有非忽略的 hallucination/instruction-following error；作者也承认 milestone/minefield 人工编写难扩展。
- 外部 web-backed tool 影响复现；没有 token/cost-matched 模型比较。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P037-E01 | evaluation | §2–3, pp.2–6 | milestones/minefields | [AUTHOR_FACT] 任意轨迹的状态评价。 |
| P037-E02 | failure | §4, pp.7–8 | Table 5 | [AUTHOR_FACT] 分解后的 failure profile。 |
| P037-E03 | limitation | §7, p.10 | limitations | [AUTHOR_FACT] simulator、authoring、external service。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Outcome-Equivalent Milestone-and-Minefield Evaluation`
- Baseline：要求 Agent 命中唯一 reference trajectory 或只看最终自然语言回答。
- Changed evaluation：对 world-state milestones 做拓扑匹配，同时检查禁止状态/调用，使多条合法轨迹都可得分而危险捷径被拒绝。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Single Tool Score Rewards Degenerate Inaction`
- 现象：不调用工具的弱系统在“避免不必要/不可行调用”上得高分，却不能完成正常任务。
- 约束：任何 abstention/safety 指标必须与正常 utility 联合报告。

## 首读裁决

`KEEP_FOR_SECOND_READ`。保留评价机制与负向指标解释；不引入环境恢复研究方向。
