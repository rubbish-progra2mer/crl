# P022 Codex 首读：MOC

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P022_moc.pdf`
- PDF SHA-256：`ba1d15b954937e17f660891e1f3b52bde6d19aa7d4f4759ca3ca98703975ea83`
- 读取范围：问题与形式化（pp.1–3）、Multi-Order Communication 与合并算法（pp.4–6）、主结果/消融/成本/限制（pp.7–9）、数据与提示细节（pp.14–17）。

## Changed computation

- [AUTHOR_FACT] 传统 DAG MAS 只把直接前驱输出拼给目标 Agent；MOC 按最短可达 hop 收集 K 阶上游原始回复，按 far-to-near 与拓扑顺序组织，使目标 Agent 可重新核对远端来源（pp.3–5）。
- [AUTHOR_FACT] 当消息数超预算时，语义—拓扑合并器先找高相似、顺序向前的消息对，用小模型生成五个长度受限的合并候选，再按对两条原消息 embedding 相似度之和选一个，保留后位锚点（pp.5–6）。
- [CODEX_SYNTHESIS] 方法把“连哪些 Agent”和“沿边传什么”分开；可迁移核心是增加未经中间 Agent 改写的证据感受野，再在明确预算下做有来源边界的去重。

## Baseline、公平性与结果

- 主比较是在相同随机 DAG、相同 Agent 数与骨干下的 Vanilla MAS vs `+MOC`，覆盖 Gemma-2-27B、Qwen2.5-32B；另测 DeepSeek-V3.2 和 G-Designer 图（pp.6–9）。该同拓扑比较有解释力。
- Gemma 七 Agent 在四种 edge density 上平均相对提升 0.89%–2.30%；Qwen HumanEval 的最大相对提升 3.68%，但并非所有单项都升（p.7）。
- K=2 比 K=1 稳定，K=3 在密图出现回落；说明更大感受野不是单调增益（p.8 Figure 3a）。
- 合并减少目标 Agent 输入，但自身蒸馏开销很大：七 Agent 单样本约 80 秒几乎全部来自 distillation；G-Designer HumanEval 的 Agent 输入 token 增加 40.1%，且该数还排除了 consolidation 成本（p.8）。
- DeepSeek-V3.2 设置 temperature=1，而本地骨干为 temperature=0；表4仅单次总量式结果，不能把小幅增益严格归因于 MOC 的稳定效应。

## 失败边界与未否定项

- [AUTHOR_FACT] K=3 在较密图可能因冗余下降；作者也承认固定 K、错误/恶意上游消息传播是限制（pp.8–9）。
- [CODEX_SYNTHESIS] embedding 相似与合并候选的 embedding 保真不保证逻辑、数字或少数派证据保真；“五候选择优”还引入隐藏推理成本与小模型偏差。
- [CODEX_SYNTHESIS] MOC 可能以更多总 token/延迟换目标 Agent 的更短上下文。因此正确对照必须同时报告：目标 Agent token、合并器 token、模型调用数、端到端延迟与准确率。
- 未否定：无蒸馏的原始多阶暴露在短消息/小 K 时可能已足够；自适应 K、来源信任与非语义去重可能比固定合并更合适。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P022-E01 | failure | §1, p.2 | Restricted Evidence Receptive Field | “raw upstream responses from multiple hop distances” | [AUTHOR_FACT] 论文要解决的中间改写与证据范围问题。 |
| P022-E02 | mechanism | §4.1, pp.4–5 | Eq.6–11 | “assigned to its shortest reachable order” | [AUTHOR_FACT] K 阶消息的身份与排序规则。 |
| P022-E03 | mechanism | §4.2, pp.5–6 | Eq.13–16, Algorithm 1 | “later message v as the anchor” | [AUTHOR_FACT] 合并保持拓扑次序的操作定义。 |
| P022-E04 | negative_result | §5.3, p.8 | Figure 3(a) | “K = 3 does not consistently bring additional gains” | [AUTHOR_FACT] 感受野扩张非单调。 |
| P022-E05 | cost | §5.3, p.8 | Table 3 | “overhead is dominated by the distillation stage” | [AUTHOR_FACT] 目标上下文节省不等于端到端便宜。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

Multi-agent communication 的强 Operator 来源，也是“更多上游消息/更多 Agent 不保证更好”的 Failure 来源。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Source-Preserving Multi-Order Message Exposure`
- Baseline：目标 Agent 只看直接前驱已经改写过的回复。
- Changed computation：同时暴露按 hop 与拓扑排序的远端原始回复；在超过预算时才做顺序保持的显式合并。
- 前提：拓扑为可追踪 DAG；消息身份和来源未在合并前丢失；总成本被完整测量。
- retrieval vocabulary：multi-order communication, evidence receptive field, semantic attenuation, topology-aware consolidation, source verification。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Communication Receptive-Field Saturation`
- 条件：高阶消息在密图或长消息条件下大量重复、冲突或含噪。
- 现象：K 增大后性能不再上升甚至下降；目标上下文或合并成本膨胀。
- 替代解释：固定 K/阈值、蒸馏器或骨干能力可能造成回落，而非多阶证据本身无效。
- 未否定：任务自适应 K 与可信来源选择可能保留增益。

## 首读裁决

`KEEP_FOR_SECOND_READ`。二读需重点核实端到端成本口径、合并信息损失与随机 DAG 复现实验。
