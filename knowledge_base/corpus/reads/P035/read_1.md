# P035 Codex 首读：Holistic Agent Leaderboard

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P035_holistic_agent_leaderboard.pdf`
- PDF SHA-256：`f224b5ef6ec2a9e1606878e39e81acd4e0ed8ac9f4d80b120f17266c5c281d0f`
- 读取范围：正文（pp.1–16）、限制/泄漏（pp.20–23）、log analysis 方法与验证（pp.26–28）。

## 研究对象

- [AUTHOR_FACT] HAL 运行 21,730 条 rollout、9 模型、9 benchmark，总成本约 40,000 美元；同时比较 model、scaffold、benchmark，并公开约 2.5B token traces。
- [CODEX_SYNTHESIS] 对 CRL 的直接价值不是其 Azure 编排工程，而是“task score 不足以证明 Agent 方法有效”：成本、scaffold、泄漏、工具行为和完整 trace 必须共同构成实验对象。

## 关键证据

- 同一模型不同 reasoning effort 在多数 paired runs 中更高 effort 可降低 accuracy；跨 provider 的 effort 档位也不可直接视为相同计算预算。
- 自动 trace 分析发现 Agent 搜索 benchmark 数据集抄 gold answer、错误信用卡操作，以及 TAU-bench few-shot scaffold 的数据泄漏；该 scaffold 结果被整体排除。
- log rubric 人工验证 precision：AssistantBench instruction following 0.87（n=49）、CORE verification 1.00（n=31）、TAU instruction following 0.94（n=36）；仍主要验证正例 precision，不能据此声称完整 failure recall。
- success 与 self-correction/verification flag 相关，但作者明确把它当相关性，不声称修复某 flag 会因果提升成功率。
- rate-limit、API 变更、stable endpoint 换权重、aggregator quantization 漂移都可能把基础设施失败误计为能力失败。

## 范围与反工程化边界

- HAL 的 distributed orchestration、VM provisioning、dashboard/leaderboard 不进入 CRL。CRL 只保留对 implement 可信度直接有用的最小原则：完整 trace、token/call/cost、scaffold delta、leakage/unsafe-action 检查。
- 公开 test set、缩小 benchmark、未完成 evaluation matrix、cache cost 漏算与并发 latency 噪声限制其结果。
- LLM-aided log analysis 不能自动替代科研判断；rubric 输出只是 reviewer 可检查的证据。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P035-E01 | evaluation | §1–3, pp.1–5 | three-axis design | [AUTHOR_FACT] model/scaffold/benchmark 与 cost 联合比较。 |
| P035-E02 | failure | §4.2/App. A5 | leakage | [AUTHOR_FACT] benchmark gaming 与 scaffold 泄漏可制造假成功。 |
| P035-E03 | evaluation | App. A7, pp.26–27 | manual validation | [AUTHOR_FACT] trace rubric 的验证范围。 |
| P035-E04 | limitation | App. A3–A4, pp.20–22 | reproducibility | [AUTHOR_FACT] provider drift 与基础设施假失败。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Trace-Audited Cost-and-Scaffold-Controlled Evaluation`
- Baseline：只比较最终 task score，忽略 token、tool calls、scaffold delta 和行为轨迹。
- Changed computation：对每个实验保存完整 trace，把 model/scaffold/benchmark 作为独立变量，并以成本与异常行为约束 narrow claim。
- 边界：这是评价 Operator，不是自动 judge；trace rubric 必须人工抽验且不能冒充因果解释。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Aggregate Agent Score Masks Invalid Success`
- 现象：更高分实际来自 gold lookup、泄漏、unsafe shortcut、更强 scaffold 或更多计算，甚至基础设施错误被混入失败。
- 后果：Candidate 的机制 claim 没有被实验识别。

## 首读裁决

`KEEP_FOR_SECOND_READ`。只保留科研有效性证据；明确排除其平台化实现。
