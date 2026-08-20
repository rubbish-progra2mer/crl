# P095 first read (W06) — P095 Deterministic Freshness：装配层瓶颈论 + extract-then-max 配方

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution
- Authors: Vikas Reddy; Sumanth Challaram（独立/IIT-KGP，双作者小团队 preprint）
- Identity: arXiv 2606.01435v1 (2026-05-31)，cs.AI；开源（自称 ~50 行编排 + Langfuse traces + 单命令复现）
- PDF: `knowledge_base/staging/w06_targeted/P095_deterministic_freshness.pdf`
- PDF SHA-256: `60f5542186d6e629e00885922dd57ee18e55f7775932c6991c2d76796c75b4a1`
- Parse check: 29 physical pages

## Canonical contribution

**装配层瓶颈论**：MAB FactConsolidation 上所有已发表记忆系统（含专为时序设计的 Zep/Graphiti 7.0%、最强 HippoRAG-v2 54.0%、FC-MH 全员 ≤7%）都输给一个极简配方——fact 级 BM25 检索 → LLM 只做**语义候选抽取**（明令不比较序号、逐字抽取全部匹配项）→ Python `max(serial)` 确定性择新。matched-setup 对照（同骨干/同检索/同 chunk/同 TOP_K/每格 n=100）：LLM-judgment 管线 67.2% vs extract-then-max 78.0%（+10.8pp，262K 处 +21pp）。多跳 CAR 管线 = Self-Ask 分解 + 逐 hop 确定性择新：FC-MH 30.2%（gpt-4o-mini）/51.5%（gpt-4o）vs 已发表最好 7%。结论：冲突消解瓶颈在 assembly（检索后聚合）而非 storage（图/海马体/agentic/类型化）。

## Evidence and closest lineage

- 机制归因：两个 LLM 失败模式——**prior-override**（真实世界实体的训练先验压过显式"新者胜"规则）与**serial-comparison drift**（候选池随上下文变大后序号追踪漂移：LLM-judgment 64K→262K 从 75% 跌到 61%）；结构化抽取消除两者。§5.4 条件化于"事实确已检回"的子集，把退化定位到检索后判断。
- 互补性分析（§5.5）：21% 题只有 max(serial) 解出、10.5% 只有 LLM-judgment 解出、11.5% 双双失败（检索上限下界）。
- **LongMemEval knowledge-update 交叉检验（§5.7，n=45）**：机制从 max(serial) 移植为 max(timestamp) 后**只打平** LLM judgment（57.8% vs 64.4%，CI 重叠）；输掉的是 Yes/No、historical（"previous"）、aggregation 型问题——max() 对这些是错误算子。作者据此把论旨收窄为"确定性聚合是 current-value 冲突的正确原语，须与问题类型感知组合"。
- 谱系：Self-Ask/IRCoT 分解线（贡献不在分解在逐 hop 择新）；temporal-rag（明确反对其"分歧留给 LLM"设计）；Grofsky 2025（单例 recency 有效）；Memanto（"图复杂度非必要"论的延伸）；知识编辑先验文献（LLM 难以用 prompt 压过时序先验）。

## Measurement and fairness boundaries

- 作者自认（§1.6 honest limits）：matched 对照**联动变化** resolver+prompt 格式+温度（0.7 vs 0.0），+10.8pp 是管线级效应，resolver 单独贡献未隔离；假设数据带显式版本标记（序号/时间戳）；MQUAKE 反事实构造未必覆盖真实冲突形态；三骨干（4o-mini/4o/o4-mini）均 OpenAI 系——**无跨家族**；LongMemEval 检验 n=45 CI 宽。
- fact 级 chunking 本身是与 MAB 默认 chunk-512 的偏离（保序号为索引键），既是方法组件也是混杂。

## Draft knowledge objects

### Operator draft: `Extract-Candidates-Then-Deterministic-Max Assembly`

LLM 职责收窄为语义候选抽取（禁止择优），时效裁决交给确定性代码。Intervention target = 检索后装配步；predicted signature = 增益随上下文长度增大、prior-override 消失、天然产生校准弃答。前提 = 显式版本标记存在；对非 current-value 问题类型需组合处理。

### Failure draft: `LLM Judgment Cannot Reliably Apply Explicit Freshness Rules`

规则写进 prompt（"newer facts have larger serial numbers"）仍系统性失败：训练先验覆盖上下文值 + 长上下文序号漂移；存储架构再复杂也不修此病（Zep 7.0% 为极端例）。

## Draft Evidence locators

- Physical pp.1-3: 摘要与 §1.2 matched-setup 表（67.2 vs 78.0、Δ 随长度扩大）。
- Physical pp.4-5: 三 findings 表、§1.4 装配瓶颈论、Zep 收窄声明。
- Physical p.6: §1.6 honest limits 全清单。
- Physical pp.7-8: 相关工作定位（temporal-rag 引语、Grofsky delta、先验文献）。
- Physical pp.9-10: SH-conflict 伪代码与 CAR 定义。

All claims remain draft until independent read and reconciliation.
