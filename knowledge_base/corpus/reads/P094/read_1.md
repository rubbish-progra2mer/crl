# P094 first read (W06) — P094 MemoryAgentBench：四能力增量评测 + FactConsolidation 选择性遗忘载体

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions (MemoryAgentBench)
- Authors: Yuanzhe Hu; Yu Wang; Julian McAuley（UCSD；前两人共同一作/通讯）
- Identity: arXiv 2507.05257v4 (2026-06-28)；**ICLR 2026 正式发表**（每页页眉 "Published as a conference paper at ICLR 2026"）
- PDF: `knowledge_base/staging/w06_targeted/P094_memoryagentbench.pdf`
- PDF SHA-256: `022d3771fd643d3bece04841e71331ef6963ff0eba43166849072caeb1b79508`
- Parse check: 33 physical pages

## Canonical contribution

以记忆/认知科学四能力框架组织记忆代理评测：**AR 精确检索 / TTL 测试时学习 / LRU 长程理解 / SF 选择性遗忘**；把长上下文数据集重构为逐 chunk 增量注入的多轮形态（区分"记忆=压缩蒸馏"与"长上下文=全量保留"），并新建两个数据集：EventQA（小说事件时序多选，全自动流水线）与 **FactConsolidation**（自 MQUAKE 反事实编辑对构造：真事实在前、矛盾改写在后，拼接成 6K/32K/64K/262K 上下文；SH 直接回忆 + MH 多跳推理；prompt 显式护栏"事实按序号索引、新事实序号更大、冲突取最新"）。2071 题、上下文 103K–1.44M。

## Evidence and closest lineage

- 被测代理三类：长上下文（GPT-4o/4o-mini/Claude-3.7/GPT-5-mini/GPT-4.1-mini）、RAG（BM25/BMX、Text-Embed-3、Qwen3-Embedding、GraphRAG/RAPTOR/HippoRAG-v2 等结构增强）、Agentic Memory（MemGPT、MIRIX、A-MEM 等；默认骨干 GPT-4o-mini）。
- 主结果（Table 3）：**SF 是全场最弱能力**——FC-MH 上长上下文模型 2–28%（GPT-4o 5.0、Claude-3.7 2.0、GPT-5-mini 28.0）；整体最好长上下文代理 GPT-5-mini 60.6 平均。
- FactConsolidation 效度检验（Table 5）：6K 短上下文下 GPT-4o SH 92.0 / o4-mini MH 80.0——**任务本身可解**；32K 即崩（o4-mini MH 80→14）——失败源于长程记忆一致性而非任务不可解。
- 消融：chunk 越小 AR 越好但 LRU 变差（Fig.2）；top-k 增大普遍助益（Fig.3）；骨干升级对 RAG 边际、对 Agentic Memory 显著（MIRIX +9.7，Table 4）。
- 谱系表（Table 1）：LongMemEval 覆盖 AR 但无 TTL/LRU/SF；本基准四能力全覆盖 + 三类代理全覆盖。

## Measurement and fairness boundaries

- SF 评测**依赖 prompt 护栏**（"newer facts have larger serial numbers"、指令冲突取最新）——测的是"有显式时序线索时的冲突消解"，比 MemStrata 的 marker-free 不变量弱一档：序号即文本时序标记，MemStrata 会将其视为污染源。两者测量哲学的冲突值得在卡中显式记录。
- FactConsolidation 源自 MQUAKE 反事实（维基三元组改写），非会话式自然更新；每上下文多题共享注入（省资源但引入题间相关）。
- 商业/结构代理只测代表子集（预算自认限制）；指标无区间。

## Draft knowledge objects

### Failure draft: `Selective Forgetting Collapses with Context Length Even with Explicit Recency Guardrails`

即便 prompt 明示"序号更大=更新、冲突取最新"，FC-MH 从 6K 的 80%（o4-mini）跌到 32K 的 14%；262K 下主流代理 2–28%。长程更新一致性是当前记忆代理最弱能力。

### Operator draft: `Incremental Multi-Turn Reconstruction of Long-Context Benchmarks`


## Draft Evidence locators

- Physical pp.1-3: 四能力定义、memory vs long-context 区分、LongMemEval 局限声明。
- Physical pp.5-6: Table 2 数据集总览；FactConsolidation 构造（MQUAKE、长度档、SH/MH）；护栏 prompt 说明（p.7 §3.3）。
- Physical p.8: Table 3 主结果（FC-SH/MH 列）。
- Physical pp.9-10: 消融（chunk/top-k/骨干）与 Table 5 效度检验。

All claims remain draft until independent read and reconciliation.
