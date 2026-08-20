# P036 Codex 首读：τ-Knowledge

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P036_tau_knowledge.pdf`
- PDF SHA-256：`f6fbe657daa349b1495bef6fecd7b1a3c845da3bf296d2589eedb45e051613bd`
- 读取范围：全文（29 页），重点为 benchmark 构造、retrieval/gold/long-context 对照、error analysis 与限制。

## 研究对象

- [AUTHOR_FACT] τ-Banking 含 698 个文档、约 194K token、97 个任务；平均每任务需 18.6 个文档和 9.52 次 tool call，部分工具只能从文档中发现。
- [CODEX_SYNTHESIS] 该工作把 knowledge access 的评价从“query 找到文档”推进到“文档是否改变长程、policy-compliant 的行动序列”。其核心价值是分离 retrieval failure 与 knowledge-use failure。

## 关键结果与诊断

- 最佳非 gold 配置为 GPT-5.2 high + terminal，pass^1 25.52%；最佳 pass^4 仅 13.40%。
- gold documents 直接放入上下文后，最佳 Claude-4.5-Opus 仍只有 39.69% pass^1；说明 retrieval 并非唯一瓶颈。
- 无知识库平均 pass^1 约 2%；完整 200K context 最高约 12%。这同时证明知识必要、全塞上下文也不能替代 targeted search + correct use。
- terminal 平均优于 dense/sparse，但需要更多 search/shell calls 和更长时间，且收益集中在近期高 reasoning 模型；不能视为无成本检索改进。
- error analysis：约 23% 与搜索低效/过早假设有关，14.5% 涉及跨产品复杂依赖，5% 违反隐式动作顺序，4% 过信用户未验证陈述。

## 公平性与边界

- corpus 由 latent structured specification 生成并经人工审核，利于精确 gold，但不是自然企业知识分布；可能低估真实文档矛盾和历史漂移。
- user simulator 的 194 个抽样轨迹有 4 个 task-critical error；低但非零。
- gold documents 是强诊断 oracle，只用于拆瓶颈，不能作为 deployable Agent 的主结果。
- terminal 配置开放更多搜索自由度；必须同时报告 token、shell calls 与 latency。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P036-E01 | evaluation | §3–6, pp.3–7 | Gold vs retrieval | [AUTHOR_FACT] knowledge access/use 分离。 |
| P036-E02 | negative_result | §6, pp.6–8 | Table 2 / ablations | [AUTHOR_FACT] gold 仍低、full-context 更低。 |
| P036-E03 | failure | §7, pp.8–9 | error analysis | [AUTHOR_FACT] assumptions/order/verification failures。 |
| P036-E04 | limitation | §8, pp.9–10 | limitations | [AUTHOR_FACT] simulator、API latency 与 unrestricted search 边界。 |

## Card 草案（不进入正式 Cards）

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Retrieved Knowledge Without Action Integration`
- 条件：必要文档已进入上下文，但 Agent 未将多文档约束、动态状态和工具结果合成为动作前提。
- 现象：document recall 看似充分，仍出现错误产品选择、错误动作顺序或未验证用户主张。
- 未否定：更强检索可修复 access gap；但 gold 对照显示它不能单独修复 utilization gap。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Gold-Access Knowledge-Use Decomposition`
- Changed evaluation：用 gold-document 条件消除检索瓶颈，再与真实 retrieval 和 no-KB 条件比较，区分 access 与 use。
- 边界：评价 Operator，不是 Candidate 自动生成器；gold 结果不可冒充正式 Agent 能力。

## 首读裁决

`KEEP_FOR_SECOND_READ`。作为 knowledge→decision 证据链与诊断实验的核心来源。
