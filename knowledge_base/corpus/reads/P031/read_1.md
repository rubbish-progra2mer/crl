# P031 Codex 首读：Agent Memory Characterization

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P031_agent_memory_characterization.pdf`
- PDF SHA-256：`b9d840d861da993e05ecc9e2295e9754ee9289ebc595270f6af18c55e57b8782`
- 读取范围：全文（12 页），重点复核方法、三阶段成本分解、准确率—成本前沿与限制。

## 研究对象与 Changed computation

- [AUTHOR_FACT] 论文不是提出新 memory agent，而是把 10 个系统统一拆为 construction、retrieval、generation 三阶段，并比较 long-context、flat RAG、structure-augmented RAG、agentic control-flow 四类范式。
- [CODEX_SYNTHESIS] 它改变的不是 Agent 决策，而是研究者对 memory implement 的评估对象：从“只看 QA accuracy / query latency”改为“把写入构建、存储、查询和生成的全生命周期代价一起计入”。

## 关键结果、基线与公平性

- LongMemEval_S_* 上，Mem0 每 query 小于 0.1 秒，而 long-context GPT-4.1-mini 约 38 秒；但这排除了预构建成本。
- 本地 Qwen3-32B、300 queries 的端到端比较中，BM25 为 47.0 accuracy、582 kJ；Letta 为 27.7、15,429 kJ。按正确答案归一化后跨度超过 47 倍。
- MemoryAgentBench 宏平均中，BM25 55.8% 反而最高；结构化/agentic 系统支付更高 construction cost，却未在聚合准确率上超过它。作者同时提醒该集合偏 recall-heavy，不能把 BM25 胜出外推到所有任务。
- construction 的中位 decode token 仅占 4.6%，主要负载是 embedding 与 prefill；某些严格结构输出系统在较小 construction LLM 上不是平滑退化，而是整个 memory store 失效。

## 失败边界与未否定项

- 结果来自固定系统实现、有限数据集与特定模型/硬件；它证明成本常被漏算，不证明复杂 memory 在需要 mutation、conflict resolution 或 long-range reasoning 的任务上无价值。
- API 与本地模型混合实验、不同系统原始配置和 judge accuracy 仍限制完全公平比较。
- 论文偏系统测量；不得把 admission control、GPU scheduling 等部署建议误写成 Agent 科研 Operator。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P031-E01 | evaluation | §3–4, pp.4–6 | three-phase profiler | [AUTHOR_FACT] 全生命周期分解。 |
| P031-E02 | negative_result | §4.2, p.6 | Table 3 / Figure 4 | [AUTHOR_FACT] construction energy 与每正确答案能耗跨度。 |
| P031-E03 | negative_result | §4.5, p.8 | frontier | [AUTHOR_FACT] 复杂 memory 未在宏平均 accuracy 超过 BM25。 |
| P031-E04 | limitation | §4.4, pp.7–8 | model sensitivity | [AUTHOR_FACT] 硬结构契约造成能力门槛。 |

## Card 草案（不进入正式 Cards）

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Query-Only Memory Evaluation Hides Lifecycle Cost`
- 条件：比较 memory implement 时只报告回答准确率和查询时延，忽略 construction、storage、写入新鲜度和调用结构。
- 现象：复杂系统看似“低延迟且更智能”，但完整生命周期的时间、能耗或每正确答案成本可能高一个数量级，甚至 accuracy 不及简单检索。
- 边界：复杂能力可能在非 recall-heavy 任务中值得其成本；需要能力匹配和 cost-matched 比较，而不是一律否定。

## 首读裁决

`KEEP_FOR_SECOND_READ`。定位为 cost-aware evaluation 的 Failure / Paper 来源；除非二读发现明确的 Agent 决策变化，不建立 Operator Card。
