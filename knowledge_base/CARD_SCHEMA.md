# CRL Card Schema v1

## 权威边界

认识论依据依次为：原始来源及其 SHA-256、后续独立阅读 reconciliation、冻结的 Evidence JSON、Markdown Card、派生检索结果。当前 `KnowledgeStore`/`knowledge.sqlite` 只提供 Paper、Passage 和 Evidence 的运行时查询接口；排名不是证据。

Markdown Card 是 Card 内容的唯一权威。`cards_fts.sqlite` 只能由 Markdown 全量重建，可以删除，不能成为第二套 Card 真值数据库。Failure、Operator、Paper 三类 Card 是并列、互补的浏览入口，不存在固定科研行动优先级，也不形成数据库权重、黑名单、自动 Gate 或统一分数。

## 第一行元数据

每张正式 Card 的第一行必须是唯一一行 JSON 注释：

```text
<!-- CRL_CARD_META {JSON object} -->
```

JSON object 必须精确包含以下六个字段，不得增加或省略：

| 字段 | 机械约束 |
|---|---|
| `schema_version` | integer，固定为 `1` |
| `card_id` | string，匹配 `[a-z0-9][a-z0-9._-]{2,127}`，且等于文件名 stem |
| `card_kind` | `paper`、`operator` 或 `failure` |
| `paper_id` | string 或 null；Paper Card 必须引用现有 Paper |
| `evidence_ids` | 非空、无重复的 string array；每项必须引用当前 Evidence |
| `source_refs` | 非空 object array；每项只含 `path` 和 64 位小写 `sha256` |

`source_refs.path` 必须是相对 `knowledge_base/` 的 POSIX 路径：不得是绝对路径，不得包含 `..` 或反斜杠。文件必须存在且哈希一致。Card 引用的每项 Evidence，其论文全文 SHA-256 都必须由至少一个 SourceRef 覆盖。

## 正文契约

元数据之后的第一个非空行是唯一 H1 标题。Card kind 必须与父目录名一致，固定章节必须逐字出现一次。

正文事实与推断只能使用以下标签：

- `[AUTHOR_FACT]`：作者明确陈述、展示或报告的事实；同一非空段落或列表项必须含 Evidence token。
- `[AUTHOR_INTERPRETATION]`：作者对结果或机制的解释；同一非空段落或列表项必须含 Evidence token。
- `[CODEX_SYNTHESIS]`：历史兼容标记，表示当时的 AI 研究者基于已列 Evidence 的综合，不得伪装成作者结论。`codex_note` 等既有字段同样只作兼容保留，不因模型命名调整重写 Card。
- `[CODEX_HYPOTHESIS]`：尚待实验检验的可证伪推断，不得写成知识事实。

Evidence token 的唯一格式为 `[[evidence:<evidence_id>]]`。正文 token 集合必须与 metadata 的 `evidence_ids` 集合完全相同。格式工具只校验引用存在、新鲜度、来源哈希、章节和标签；不判断自然语言是否被 Evidence 语义支持，也不计算质量、新颖性或重要性。

## 三类 Card 职责

### Failure Card

保存真实观察到的失败、无效机制和适用边界，帮助主 AI 研究者避免重复踩坑。它与 Operator、Paper Card 并列互补；Failure 命中只是警告和反例，不能自动否决未来方法。

Failure Card 只接受按正式论文准入流程进入共享知识库的外部来源。CRL 自有 Run 的实验、Candidate、Decision、Memory、Ledger、失败结论及其复制件不得进入共享 Paper/Evidence/Card 或定位索引；这些证据只保留在各自 Run 内，不跨 Run 检索或复用。

### Operator Card

方法生成的核心资产。必须说明干预目标、Baseline 与 Changed Computation、输入输出、可用信息、发生时点、预算变化、预测机制签名、前提和迁移风险。

### Paper Card

来源解释层。说明论文角色、问题设定、实际 changed computation、证据支持的发现、限制、谱系和基线；不能用论文摘要替代原始来源。

## 运行时知识流

三路知识流是给主 AI 研究者使用的高价值检索方法，不是脚本状态机。可以从 Failure、Operator 或 Paper 任一路进入，也可以并行或交叉查询，随后回到 Evidence 和原始页面核对来源、边界与谱系；主研究者根据当前问题决定顺序、深度和组合方式。

Failure 命中只提供警告和反例，Operator 命中只提供 changed-computation 组件，Paper/Evidence 用于复核事实。脚本不得因为某一路未调用、候选数量不足或未按固定顺序执行而判定 Run 不合格，也不得自动生成、排序、淘汰候选方法或替代科研判断。

禁止把三路结果合并成 `failure_weight`、`operator_score` 或统一自动分数。需要比较不同入口时，可执行独立查询并由主 AI 研究者阅读；检索顺序本身不代表科学优先级。

## 固定章节

Paper Card：`Role in the knowledge base`、`Problem and setting`、`Changed computation`、`Evidence-backed findings`、`Limitations and failure signals`、`Lineage and baselines`、`Evidence ledger`、`Retrieval vocabulary`。

Operator Card：`Intervention target`、`Before and after computation`、`Inputs outputs information and timing`、`Mechanism hypothesis`、`Predicted observable signature`、`Preconditions and transfer risks`、`Source lineage`、`Evidence ledger`、`Retrieval vocabulary`。

Failure Card：`Observed failure`、`Conditions and scope`、`Failed intervention`、`Evidence and alternative explanations`、`Warning for future candidates`、`Possible repair boundary`、`Evidence ledger`、`Retrieval vocabulary`。

## 明确禁止

不得建设知识图谱或图数据库运行时，不得为 Card 建立 embedding/vector index、Reranker、学习排序、自动标签器、自动 Candidate 生成器、科研评分器或自动推理系统。不得用近重复论文数量冒充独立机制证据数。
