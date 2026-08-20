# P100 first read (W06) — P100 Tool Shortlist Size：把展示深度 K 本身作为评测与学习对象（BoR）

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: How Many Tools Should an LLM Agent See? A Chance-Corrected Answer
- Authors: Vyzantinos Repantis; Ameya Gawde; Harshvardhan Singh; Joey Blackwell II（Meta Platforms，Preprint 自标）
- Identity: arXiv 2605.24660v2 (2026-06-07)，cs.IR，13pp
- PDF: `knowledge_base/staging/w06_targeted/P100_tool_shortlist_size.pdf`
- PDF SHA-256: `4db89bfac79bc90dd5b532d04ac1012ed1691657a45379bbbb2312682847164c`
- Parse check: 13 physical pages

## Canonical contribution

把工具检索的**展示深度 K 当作一等评测对象**：应用 chance-corrected 的 Bits-over-Random（BoR = log2(Pobs/Prand)，Prand 由超几何分布给出，Rq=1 时 = K/N），并把它直接用作**逐查询深度选择的 RL 奖励**（MDP：逐个查看排序候选，STOP/CONTINUE 二元动作；STOP 命中时奖励 −log2(Prand(k))——短列表命中天然更值钱，深度惩罚是度量结构的数学后果而非工程惩罚项，"self-pruning"）。RL agent 刻意极简（DQN/表格 Q），定位为度量探针非生产架构。

## Evidence and closest lineage

- BFCL（370 工具池化重构）：BoR agent 90.3±2.4% 覆盖 @K=7.4 ≈ FK=50 的 90.8%（深度 1/7）。
- ToolBench（3,251 工具，N=50 候选集）：**分难度桶的清晰分离**——easy（gold 排 1）K=2.5/100%；medium K=4.8/74.4%；hard（gold 排 6-20）K=5.7/16.7%（FK=5、F1 消融、FK=1 全部 0%）；聚合覆盖 FK=5 反而更高（64.7 vs 61.9）——均匀深度吃掉 easy/medium、hard 全灭的权衡被量化。
- F1 深度惩罚消融：与查询/注册表无关的固定惩罚不产生自适应（K≈1.5 各桶不动）。
- **scorer 质量负结果**（§4.2）：BM25 在 MetaTool 仅 33% found@1 时 BoR agent 膨胀到 K=80.7（1.04 bits）——弱 scorer 下无处可停；同奖励换 MiniLM/BGE 得 K≈2.3——**深度策略由 scorer 判别力决定**；BoR 曾标出其他指标漏掉的坏 scorer。
- 下游验证（§4.3，Claude Sonnet 4.6）：短自适应列表也改善 LLM 选择：93.1% vs 固定 5 工具 87.1%；medium 桶 76.8% vs 60.9%——**少展示提升选择质量**的直接证据。
- 谱系：Kratzwald/Taguchi/DPS/DynamicRAG（深度/截断线）、Less-is-More/ToolRerank/RAG-MCP（工具过滤线）、BEDROC/enrichment factor（化学信息学 chance-correction 传统被接入 IR）。

## Measurement and fairness boundaries

- 只测"正确工具是否被展示"（覆盖），执行正确性超范围；训练用 oracle Rq、推断假设 Rq=1；候选集多为构造（gold+hard distractors）非全注册表；RL 超参逐条件微调（step_cost/γ 例外被如实列出）；单 LLM 下游验证。

## Draft knowledge objects

### Operator draft: `Chance-Corrected Depth Reward (BoR) for Per-Query Shortlist Sizing`

以 −log2(Prand(k)) 为 STOP 奖励，使深度惩罚内生于随机基线上升；changed computation = 检索深度从固定超参变为逐查询决策变量。Predicted signature = 深度随难度桶单调上升、弱 scorer 下策略退化为全展示。前提 = scorer 有判别力、Rq 已知或可设 1。

### Failure draft: `Fixed Shortlist Depth Trades Hard-Query Coverage for Aggregate Numbers`

固定 K=5 聚合覆盖更高但 gold 排 6+ 的查询 0% 命中；均匀深度把失败集中在难查询上，聚合指标掩盖该结构（评测陷阱：deep-vs-fixed 对比必须分难度桶报告）。

## Draft Evidence locators

- Physical pp.1-2: BoR 定义、贡献与 scope 声明。
- Physical pp.4-5: MDP/奖励/self-pruning、doubling rule。
- Physical pp.5-6: BFCL/MetaTool/ToolBench 结果与难度桶分析。
- Physical pp.6-7: scorer 质量负结果（K=80.7）、Fig.1/2。
- Physical p.7+: 下游 tool-choice 验证（93.1 vs 87.1）。

All claims remain draft until independent read and reconciliation.
