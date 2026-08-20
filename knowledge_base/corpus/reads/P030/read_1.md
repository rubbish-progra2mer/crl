# P030 Codex 首读：STALE

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P030_stale_memory.pdf`
- PDF SHA-256：`388f71f1eb952e7d7e7b19c2f25bfc744c47efa8ee00a548093b949432495109`
- 读取范围：问题与形式化（pp.1–5）、构造/评测/结果（pp.6–10）、限制/成本（pp.14–15）、judge 验证与案例（pp.27–34）、CUPMEM 细节（pp.35–37）。

## Changed computation / evaluation object

- [AUTHOR_FACT] STALE 把“新证据未显式否定旧信息、却使旧 belief 失效”分为同属性 Type I 与跨属性传播 Type II；分别用 State Resolution、Premise Resistance、Implicit Policy Adaptation 三种 query 探测（pp.2–6）。
- [AUTHOR_FACT] CUPMEM 在写入时把候选映射到类型化 state slot，显式把旧项标为 ACTIVE/STALE/UNKNOWN_CURRENT；Type II 通过受 schema 约束的 affected-region 搜索找可能被间接影响的旧项，query 只从裁决后状态读出（pp.9, 35–37）。
- [CODEX_SYNTHESIS] 关键转变是从“时间衰减/相似度 retrieval”到“写侧当前状态裁决”。召回到新证据不代表它获得了控制 downstream decision 的权威。

## Baseline、公平性与结果

- 400 个专家复核 conflict、每个三 probe，共 1200 query；长上下文最多 150K。Plain LLM 用完整历史，memory framework 统一 GPT-4o-mini backbone；每个 probe 独立调用，memory 固定（pp.6–7）。
- 最强 plain Gemini-3.1-pro overall 55.2%；Qwen3.5-27B 31.3%；LightMem 17.8%，其他 memory framework 多低于 10。CUPMEM 同 GPT-4o-mini 为 68.0（p.7 Table 2）。
- Premise Resistance 是普遍最弱维度：Gemini pro Type I SR 92 但 PR 30；Qwen-27B 76→4。Type II 普遍更难（p.7）。
- LightMem 新证据在 SR/PR top-20 中出现 77.5%，但 PR 仍 99% failure；old memory top-1 84.5%。这直接隔离了“召回可见但没有 current-state authority”（pp.8–9 Table 3）。
- CUPMEM 每实例约 $0.37，接近最贵 baseline A-MEM $0.38，远高于 LightMem $0.02（p.15）；68% 不能称低成本胜出。

## 失败边界与未否定项

- benchmark 与 CUPMEM 共用“latent state/implicit invalidation”概念；尽管作者声称 schema 独立于生成 ontology，预定义 10 domain/local slots 仍是强 scaffolding，可能有 benchmark-fit 优势（pp.14, 35）。
- 所有冲突为一次性、合成、专家编辑；不能外推多次反转、模糊状态或真实用户不确定表达（p.14）。
- judge 对 240 响应与人工一致 95.83%，但 IPA false-negative 16.67%；自动分数可能低估开放式正确策略（pp.29–30）。
- 把旧项标 stale 的错误代价未在主结果中单独报告；过度裁决可能错误废弃仍共存或暂时有效的偏好。
- [CODEX_SYNTHESIS] CUPMEM 使用 LLM adjudicator/common-sense propagation，强提升可能来自额外模型调用与 schema，不是单一“写侧标记”组件；需要 cost-matched 与错误 update precision baseline。
- 未否定：query-time reranking/contradiction check 可能在较低成本下修复部分 PR；论文证明当前 retrieval-only baseline 不足，不证明 write-time schema 是唯一解。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P030-E01 | failure | §3.2–3.3, pp.4–5 | Axiom 1/2 | “without syntactic negation” | [AUTHOR_FACT] implicit invalidation 定义。 |
| P030-E02 | evaluation | §3.5, p.6 | SR/PR/IPA | “query ... presupposes mo remains true” | [AUTHOR_FACT] premise resistance 独立探针。 |
| P030-E03 | negative_result | §4.4, pp.8–9 | Table 3 | “Failure despite new evidence ... 99.0%” | [AUTHOR_FACT] 可见性不等于使用权威。 |
| P030-E04 | mechanism | §5, p.9 | write-side adjudication | “blocked before query time” | [AUTHOR_FACT] stale state 在写侧退休。 |
| P030-E05 | limitation | Appendix A/C, pp.14–15 | Method/Cost | “targeted prototype” | [AUTHOR_FACT] schema 与成本边界。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

Memory update/safety 的强 Failure 与 evaluation source；CUPMEM 是有潜力但高 scaffolding/high-cost 的 Operator 来源。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Write-Side Current-State Adjudication`
- Baseline：旧、新 observation 都留在向量库，query-time top-k 临时决定。
- Changed computation：新证据写入时主动搜索直接/间接受影响的旧 state，标记 ACTIVE/STALE/UNKNOWN，再约束 query 只用授权 current basis。
- 前提：state 更新证据足够；共存事实与替代事实可区分；错误 retirement 被测量；额外 LLM/cost 公平报告。
- retrieval vocabulary：implicit conflict, stale memory, current-state adjudication, premise resistance, propagated invalidation。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Retrieved Update Without Decision Authority`
- 条件：旧、新证据并列召回，排序偏向 query 表面前提，且无显式 current-state 状态。
- 现象：模型能在直接问询时承认更新，却在带旧前提的任务中继续按旧状态行动。
- 替代解释：长上下文 attention、基础模型 instruction-following 或 query framing 也会影响失败。
- 未否定：低成本 premise verifier 或时序 reranker 可能部分修复。

## 首读裁决

`KEEP_FOR_SECOND_READ`。二读须专门审查 schema leakage、过度 stale 标记、cost-matched baseline 与合成分布外推。
