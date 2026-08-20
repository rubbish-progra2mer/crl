# P048 Codex 首读：NaviAgent

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P048_naviagent.pdf`
- PDF SHA-256：`d7578b55678c89f2ffb78741c5faab8adf7c70e7e4160d2cd5fafea522e192ab`
- 读取范围：全文主体及关键附录（35 页），重点为 bilevel decision、静态/动态图 ablation 与评测定义。

## Changed computation

- [AUTHOR_FACT] 高层 Agent 在直接回答、澄清、工具链检索、执行之间决策；低层工具图以 API/参数节点及结构/行为边表达依赖，通过图搜索提供候选子图。
- [AUTHOR_FACT] DeepSeek-V3 ToolBench ablation：ReAct TSR 34.5，单加 Graph+Alpha 45.7，单加 Bilevel 42.4，Bilevel+Graph+Unpruned 50.3，加入 heuristic search 55.2。
- [CODEX_SYNTHESIS] 在 CRL 允许范围内可抽取的是“先决定是否/为何进入工具执行，再在显式依赖子图中规划”的静态双层结构；动态图反馈、API 故障恢复和路径重组被明确排除。

## 关键结果与边界

- ToolBench 多 backbone 上均报告 TSR 提升；50 个 RapidAPI、303 queries 的 live evaluation 也有 4.3–12.0 point 增益。
- TSR 由 LLM 对 ground truth 比较，TCR 只表示产生最终输出；二者不能自动等同真实任务完成。
- Qwen2.5-14B 另经 3,500+ 生成样本 SFT；不同变体同时改变 graph、search、训练与恢复动作，完整系统提升不能归因于单一 operator。
- 核心方法的大部分适应性来自历史成功统计、动态图更新和执行失败后的 rerouting，属于用户排除方向，不能曲解为正式知识库研究目标。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P048-E01 | method | §3.1–3.2, pp.3–4 | bilevel / graph | [AUTHOR_FACT] 高层动作选择与低层依赖图。 |
| P048-E02 | result | §4.4, pp.8–9 | component ablation | [AUTHOR_FACT] 静态图、双层结构和搜索分别带来增益。 |
| P048-E03 | limitation | §4.1 / §5 | TSR judge / coupled components | [AUTHOR_FACT+CODEX_SYNTHESIS] 指标与归因边界。 |
| P048-E04 | scope_exclusion | §3.2.4–3.3 | graph evolution/recovery | [CODEX_SYNTHESIS] 排除反馈学习与执行恢复部分。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Bilevel Intent-to-Dependency-Subgraph Planning`
- Baseline：单层 Agent 在大工具列表中逐步选择下一调用，意图判断与工具链搜索混在同一决策。
- Changed computation：高层先选择直接答复/澄清/检索工具链，只有需要执行时才把任务约束投影到静态 API-参数依赖子图中搜索。
- 边界：仅保留静态结构；不包含在线边权学习、故障探测、rerouting 或恢复。

## 首读裁决

`KEEP_FOR_SECOND_READ_WITH_SCOPE_BOUNDARY`。二读需要确认静态 ablation 足以独立支撑上述窄 Operator。
