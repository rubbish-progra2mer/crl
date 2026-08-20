# P010 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P010_longmemeval.pdf`；SHA-256：`c6c6d75072d316d7b040dbbbb9caf7607821e6dd34d986e6f6c7e3e1721179f7`
- 主 Codex 首读：`knowledge_base/pilot/reads/P010/read_1.md`；SHA-256：`489e2db37dd8f2d7c5630f4a4b09c344871cfe65197a4e6315085ed85b44c6fc`
- 二读 `r2-20260719-p010-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P010/read_2_attempts/r2-20260719-p010-a1/invocation.md`；SHA-256：`a4626b05fedb4d6b580293a44a1ac62604c82d345c53d7518548b39f4c881b79`。Report：`knowledge_base/pilot/reads/P010/read_2_attempts/r2-20260719-p010-a1/report.md`；SHA-256：`7deeff2f0f306149c5968760427c6f1e73150f13e969e6e3aef98ecd2fa0b90b`。
- 其他二读 attempts：无。第三读 attempts：无；本文是 memory failure/operator/evaluation 的近期分析论文，不是唯一直接祖先，计划不超过两个 Operator/Failure Cards；两读无关键冲突或视觉解析冲突。
- 独立性：`procedural_blinding`；二读者声明未读取首读、Cards、其他报告或 blind query。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：论文把 memory assistant 分为 indexing/retrieval/reading 三阶段与 value/key/query/reading 四个控制点。方法性改变包括 round 粒度、原 value+fact 的 key expansion、可 abstain 的时间范围过滤、JSON+Chain-of-Note reading；它们是可分别消融的组件，不是单一端到端 architecture。核点：PDF pp.7–10 §4–5、Figure 4、Tables 3–4、Figure 6。

### Baseline — `AGREE`

Long-context direct reading 是无显式 memory 操作的 baseline；evidence-only oracle 只诊断 reader，不是可部署上界。每个控制点的最近 baseline 分别是相同 value 下 `K=V`、无 query expansion，以及 NL/JSON×Direct/CoN。§5.2–5.4 默认叠加 JSON+CoN 和时间排序，不能把跨节结果当纯单变量。核点：PDF pp.6、8–10、26–28。

### 公平性与预算 — `AGREE`

Figure 5 对 retrieved-token 做控制，但索引抽取、fact expansion、GPT-4o 时间解析、storage/latency/cost 未统一报告；reader 能力显著改变最优 token budget。商业系统只用 97 个更短、筛过题型的问题，不可与完整 benchmark 等价。Judge 使用 GPT-4o 且少数题型人机一致率约 0.90。核点：PDF pp.6、8–10、20–21。

### 主要结果 — `AGREE`

Table 3 中 round `K=V` Recall@10 .692，`V+fact` .784，GPT-4o Top-10 QA .670→.720；该结果支持“保留原文、用 fact 扩 key”，不支持以 fact 替换 value。弱时间解析器会造成 false-positive pruning；JSON+CoN 只在 oracle retrieval 组合中最稳，不在 full-history/所有 reader 上普遍改善。核点：PDF pp.6、9–10、27–28。

### Limitation — `AGREE`

500 问历史是 LLM 辅助+人工编辑的受控合成分布；无真实长期自然日志同规模验证。没有删除、跨用户隔离、poisoning defense 或长期 index drift 实验。Figure 5 纯曲线无逐点表；没有置信区间/多 seed。核点：PDF pp.4–6、11、17–19、26–28。

### Operator — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Index–Retrieve–Read Failure Decomposition`：用 annotated evidence recall 和 oracle reading 分离 retrieval 与 reading，避免从最终 QA 反推唯一故障。Round/value、fact-key、temporal filter、CoN 作为该 Paper Card 中的具体干预证据，不拆成更多正式 Operator Cards。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Correct Recall Still Produces Wrong Reading`：best design 下，即使 top-10 recall 正确仍有约 15%–19% 全部实例生成错误，说明 retrieval-only 优化不能消除 reading failure。压缩损失与 false temporal pruning 作为同一 Paper Card 的其他负向边界。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：数据 artifacts、抽取器 error rate、全组件联合边际贡献、完整成本和时间排序单独消融均未解决。
- CORE disposition：`ACCEPT`。它提供 memory 流水线故障定位 Operator 与直接负向 Evidence。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先创建 Evidence。
