# P029 Codex 首读：MemFail

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P029_memfail.pdf`
- PDF SHA-256：`7649a407d54058c425fa7f6ea1dc8551288e16bac24ff0e1bad1e0ec90315d8d`
- 读取范围：形式化与任务（pp.1–5）、评测与发现（pp.5–9）、完整结果/错误分解（pp.19–22）、生成与判分提示（pp.27–35）。

## Changed computation / evaluation object

- [AUTHOR_FACT] 把记忆系统拆为 Summarize、Store、Retrieve 三操作，并在知道所有 memory store 与 retrieved set 的条件下按顺序诊断 storage、summary、retrieval、reasoning failure（pp.3–6）。
- [AUTHOR_FACT] 五个合成 diagnostic 分别施压：条件限定保真、共存事实、误导 persona、长链 retrieval 与分散条件摘要（pp.4–6）。
- [CODEX_SYNTHESIS] 对 CRL 的核心 Operator 是“按信息生命周期定位失败”，而不是只用最终 QA accuracy 给整个 memory 模块一个分数。

## Baseline、公平性与结果

- 同一 gpt-5-mini 作为所有系统外部 test-taker 与 grader；四个 memory framework 使用各自内部模型。100 条人工复核中回答正确 98%，错误类型分类 98.4%（p.6）。
- k 从 4 增到 20 只在 retrieval-bottleneck（尤其共存事实）较有帮助；summary failure 不因更多召回而修复（pp.6–7）。
- 更强内部模型在多数任务不改善且可退化；更多 token 对 summary-bottleneck 有利，对 retrieval-bottleneck 可污染 embedding（pp.7–8）。图表给出趋势与 Wilson interval，但正文较少给精确总体数值，正式 Card 应保存窄趋势而非虚构均值。
- StructMem 图结构在 long-hop/conditional 较强、coexisting retrieval 很弱；Mem0 短事实存储好、长 persona 因 tool-call 数不足出现 storage failure（p.8）。这支持“架构诱导特定 failure signature”。

## 失败边界与未否定项

- 全数据由多种 LLM 生成、结构化过滤并人工逐项核对；它是隔离机制的 diagnostic，不预测真实部署频率（p.9）。
- grader 可见全部 stored/retrieved memories，这是诊断 oracle，只用于归因、不能给被测 Agent 使用；形式上公平但不属于可部署机制。
- `get_all_memories()` 不适用于隐式参数记忆/权重记忆，benchmark 主要覆盖显式外部 memory（p.9）。
- Long-Hop 用刻意正交的 synthetic anchor，降低世界知识捷径，却可能高估真实语言中语义关联与实体歧义的差异。
- 未否定：强模型可改善 reasoning failure；本结论只说当前主要错误常在 memory architecture，不能表述为模型能力永远无关。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P029-E01 | taxonomy | §3.2, p.3 | four failure modes | “summary ... storage ... retrieval ... reasoning” | [AUTHOR_FACT] 明确的生命周期失败分类。 |
| P029-E02 | mechanism | §5.1, pp.5–6 | Phase 3 Grading | “conditional on storage” | [AUTHOR_FACT] 分层诊断防止重复归因。 |
| P029-E03 | negative_result | §6 Q1, pp.6–7 | Figure 1 | “scales poorly with k” | [AUTHOR_FACT] 更多召回不是通用修复。 |
| P029-E04 | negative_result | §6 Q2, p.7 | Figure 2 | “stronger models do not improve accuracy” | [AUTHOR_FACT] 当前系统的架构瓶颈观察。 |
| P029-E05 | failure | §6 Q4, p.8 | architecture findings | “fails to issue enough tool calls” | [AUTHOR_EXPLANATION] Mem0 长输入 storage failure 解释。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

Failure-first memory 诊断强来源；Paper/Failure 优先级高于提出的 mixture-of-memories future idea。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Conditional Memory-Lifecycle Failure Localization`
- Baseline：只报告 memory-augmented QA 最终准确率。
- Changed computation：依次核验原信息是否被存、条件是否保真、是否被召回、召回后是否用对，使每个问题只落到最早失败环节。
- 前提：系统能导出 memory store；诊断器可访问完整状态但不反馈给被测 Agent。
- retrieval vocabulary：summary failure, storage failure, retrieval failure, conditional diagnosis, memory failure signature。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Memory-Architecture Trade-off Hidden by Aggregate Accuracy`
- 条件：不同 task 混合成一个端到端均值。
- 现象：图/向量/原子事实系统在不同 failure 上相互反转；均值掩盖具体可修机制。
- 替代解释：合成任务配比会改变均值与排名。
- 未否定：部署最终仍需端到端指标，但必须与条件失败分解并列。

## 首读裁决

`KEEP_FOR_SECOND_READ`。其负向知识密度高；二读应攻击 synthetic validity、grader oracle 与错误分类条件。
