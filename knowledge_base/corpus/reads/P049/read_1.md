# P049 Codex 首读：Reinforced Agent

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P049_reinforced_agent.pdf`
- PDF SHA-256：`352a4f39ae64d07722a7e63bfed3d9afad20f7529c406ee764af37d3503b40c8`
- 读取范围：全文（12 页），重点为预执行 reviewer、helpfulness/harmfulness、跨 benchmark 结果与延迟。

## Changed computation

- [AUTHOR_FACT] 主 Agent 先产生 provisional tool call，独立 reviewer 在调用执行前审查；可用 progressive feedback 修订，或在 best-of-N candidates 中选择/评分。
- [AUTHOR_FACT] Progressive feedback 在 tau2 平均从 48.7% 升至 55.8%，但 airline/retail 不一定提升，主要增益来自 telecom；best-of-N selection 甚至可低于 baseline。
- [CODEX_SYNTHESIS] 有价值的机制不是“多一个 Agent”，而是在不可逆工具动作前引入职责独立、可测量误伤率的 veto/修订点。

## 关键结果与边界

- BFCL 上 o3-mini reviewer helpfulness 36.8%、harmfulness 11.7%，比值 3.1:1；GPT-4o v2 为 34.9%/12.9%。
- reviewer 会把正确 tool-only response 误判为不完整；明确提示后冗余 review loop 从 23% 降到 8%。tau2 中 over-verbalization failure 增加 17 个百分点。
- BFCL 平均延迟从 1.27s 到 7.87s（6.2×）；tau2 从 158.7s 到 384.3s（2.4×）。这不是免费提升。
- base 仅 GPT-4o；GEPA 优化和 helpfulness/harmfulness 只在 BFCL 系统评测，未在 tau2 验证；benchmark-specific prompt 迁移会失效。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P049-E01 | method | §2.1, pp.2–3 | progressive reviewer | [AUTHOR_FACT] 预执行独立审查。 |
| P049-E02 | result | §4.2–4.3, pp.4–5 | BFCL/tau2 | [AUTHOR_FACT] 提升不均匀且存在误伤。 |
| P049-E03 | failure | §4.2, pp.4–5 | over-skepticism | [AUTHOR_FACT] reviewer 破坏正确动作。 |
| P049-E04 | cost | §4.5, p.7 | latency | [AUTHOR_FACT] 6.2×/2.4× 延迟。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Independent Pre-Execution Tool-Call Review`
- Baseline：主 Agent 生成的工具调用直接进入环境，错误只能事后恢复。
- Changed computation：在执行前冻结 provisional action，由不同职责的 reviewer 只检查工具相关性、参数和 policy precondition；拒绝时返回具体修订意见。
- 边界：必须同时报告 reviewer helpfulness、harmfulness、额外调用和延迟；不能以 reviewer 自信替代环境证据。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Reviewer Over-Skepticism Breaks Valid Actions`
- 现象：reviewer 将“尚未执行所以没有结果”误当成工具调用不完整，修订本来正确的动作并增加无关文本。

## 首读裁决

`KEEP_FOR_SECOND_READ`。强机制证据，但二读必须防止把 benchmark-specific reviewer prompt 当通用审查能力。
