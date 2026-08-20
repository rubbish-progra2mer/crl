# P091 first read (W06) — MemStrata：相似度不可分辨矛盾/复述的结构性结果 + 确定性 supersession

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge (MemStrata)
- Author: Neeraj Yadav（单作者，MemStrata.dev — Called It Inc.，企业预印本）
- Identity: arXiv 2606.26511v1 (2026-06-25)；**正文自带草稿痕迹**（p.1 保留"Draft v2"与"For double-blind submission, anonymize…Regenerate every figure"等内部注记）——身份为未定稿 preprint，准入角色限 Failure/measurement 证据
- PDF: `knowledge_base/staging/w06_targeted/P091_memstrata.pdf`；SHA-256 `10349a31de86116b7e4cc5a8cb5e60766a55ab7dbab7894906841a6e3234171f`
- Parse check: 21 physical pages

## Canonical contribution

1. **相似度不可能性结果**（§3, §5.1, Table 1）：98 对标注样本上，cosine 区分 duplicate 与其余类 AUROC 0.5926；**contradict 对原句的平均 cosine（0.812）高于 duplicate（0.800）**（值翻转是最小编辑）；任意阈值下 duplicate 判定最高 precision 0.667。结论：写时 staleness 检测必须是结构性/确定性的，不能基于相似度。
2. **确定性 supersession 架构**（§4）：写路径对干净 (subject, relation, object) 三元组按归一化 (S,R) 键匹配，object 不同即 supersede（旧行关 valid_to、链 superseded_by），无 cosine 无 LLM；bi-temporal ledger 退休不删除；非三元组散文走 surprise-gate 回退。读路径无 LLM（~2.1s vs LLM rerank/verify ~16-18s）。
3. **Stale-fact-error 主结果**（§5.3, Table 3）：四个 marker-free 演化基准上，forced-answer 下 naive RAG 以 15–40% 概率答出被取代值（dependency_bump 15% 系"版本号更大=更新"的表面启发）；temporal_v6 ≈0%。相似度门控条件（v6/v6_no_verify）在弃答制下泄漏 stale 25–60%，比 RAG 更差。
4. **Marker-free 评测协议**（§4.5, B.1-B.2）：演化基准中新旧版本除变化值外逐字相同、禁止 outdated/legacy 等词；早期基准去掉 [OUTDATED] 标记使 reranker-RAG 掉 14 点——标记污染实测存在。

## Evidence and closest lineage

- 条件×基准矩阵（8×6，App.A.1）：静态 domain/locomo 上 temporal_v6 与 RAG 打平（0.82/0.30 vs 0.86/0.30）；四演化基准 0.95–1.00 vs RAG 0.20–0.47。
- 双向消融夹逼（D.1/D.1b）：lossy 合并变体静态崩塌（0.62/0.13）；去掉 supersession 使演化均值 0.99→0.33（≈naive RAG 0.32）且条件性捏造率 0.04→0.25（~6×，config_migration 达 0.56）——**并置新旧值且无法分辨会诱发捏造**，确定性 supersession 被隔离为唯一原因。
- 谱系：bi-temporal 数据库（Snodgrass 系）、temporal KG、GraphRAG 族（引 Zeng 2506.06331 的"图 RAG 收益在无偏评测下缩水"佐证表示丰富≠时效）；与 Self-RAG 型验证的差异（验证无时间信号）。

## Measurement and fairness boundaries

- **规模极小**：演化基准各 20–30 场景、静态 50/30 题；单 7B 回答模型（Qwen2.5-Coder-7B）+ 3B 判分（自我评分规避已做）；温度 0 单跑，无区间。
- **抽取是硬边界（作者自认，§7 + B.8）**：结构化单值模板上 supersession 键成功 ~97%；自由散文矛盾基准上仅 ~44%，该基准被隔离不计入主结果（其上 temporal_v6 0.62 < advanced_rag 0.74）——机制天花板由抽取层决定。
- 摄入顺序代理时间（无真实时间戳）；locomo 静态样本是 100 turn 截断版；单作者草稿态、数字待社区复核。

## Draft knowledge objects

### Operator draft: `Deterministic (S,R,O) Supersession over Bi-Temporal Ledger`

写时按归一化 (subject, relation) 键匹配、object 变更即退休旧值；读时只取 active 行。Intervention target = 写路径矛盾处理；predicted signature = 演化知识上 stale-fact-error→0 且静态召回不降、读延迟不变。前提 = 事实可被可靠抽取为单值三元组（散文场景 ~44% 即失效）。

### Failure draft: `Embedding Similarity Cannot Separate Contradiction from Duplicate`

值翻转矛盾比真复述更接近原句（0.812 vs 0.800，AUROC 0.59，max precision 0.667）；任何相似度阈值/门控做写时 supersession 都会泄漏 stale（端到端 25–60%）。

### Failure draft: `Co-Present Stale and Current Values Induce Fabrication`

无 supersession 时并置新旧值使条件性捏造率升 ~6×（0.04→0.25）——stale 不只是答错旧值，还制造无中生有。

### Failure draft (measurement): `Textual Staleness Markers Contaminate Evolution Benchmarks`

[OUTDATED] 型标记使基线虚高至多 14–18 点；marker-free 不变量应为演化评测的正确性属性。

## Draft Evidence locators

- Physical p.4 (§3)/p.6 (§5.1, Table 1): 不可能性结果与逐类 cosine。
- Physical pp.4-5 (§4.1-4.5): 写/读路径、ledger、marker-free 不变量。
- Physical pp.6-7 (Table 2-3): 主矩阵与 stale-fact-error（allow/forced 双制）。
- Physical p.8 (§7): 抽取边界自认；p.16 (B.8) 被隔离基准 44% vs 97%。
- Physical pp.19-20 (D.1/D.1b): 双向消融夹逼与捏造率放大。

All claims remain draft until independent read and reconciliation.
