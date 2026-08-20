# W06 Card source audit A disposition

- Audit ID: `w06-audit-a`
- Report SHA-256: `a40e8d9cd6d4078a01873301e4d00aa890ee76fff9ca51e80674f3364474925d`
- Decision: `ACCEPT_WITH_SINGLE_ROUND_NARROWING`
- Atomic totals: 88 PASS / 11 NARROW / 0 REJECT（99 原子项）

## Disposition

主 Codex 按审计意见完成一轮收窄（不循环审计），全部 11 处 NARROW 逐条采纳，修订即审计给出的最小精确修正：

1. `paper-p090`：写侧机制改为 "LLM 生成 summary/keyword，raw session 及其 turn 切分共同构成四粒度"（Eq.1 精确语义）；"路由单项贡献未隔离" 收窄为 "仅在 LongMemEval-s 消融（Table 3 w/o Router）中被量化，跨基准主表增益仍系管线级"。
2. `operator-entropy-routed-multi-granularity-retrieval`：同上路由消融收窄。
3. `failure-cosine-cannot-separate-contradiction-from-duplicate`：0.5926 归位为 duplicate-vs-其余类 AUROC，contradiction-vs-duplicate 表述携带作者圆整值 0.59。
4. `failure-answer-accuracy-without-conflict-recognition`：judge 表述改为 "LLM 辅助匹配＋人工校验（§3.6）"。
5. `operator-support-evidence-whitebox-retrieval-metrics`：EUG 三处（intervention target / before-after / vocabulary）统一改为 Evidence Utilization **Gap**（SEH@3−AA，利用缺口诊断）。
6. `paper-p093`："5 偏差电池" 改为 "4 偏差 + 答案在场因素构成五个单因素设定"。
7. `failure-dense-retriever-surface-bias-collapse`：ColBERT v2 覆盖面按 Fig.1 修正（仅 ReasonIR-8B 为 foil-only）。
8. `operator-paired-single-factor-bias-decomposition`：t 区间 −20.96~−42.25 归位为 foil 组合比较（Table 4），单因素设定不再挂该区间。

未修订项：审计确认全部机械层完好（11/11 evidence quote 与 sqlite passage 切片逐字节一致、passage/PDF SHA 全匹配）、无捏造数字、invocation 点名的过度声明风险方向全部已在卡内对冲。`ev-p091-retain-fabrication` 的 section 字段标 "References" 而实际为附录 D（p.20）系 chunker 分节跟踪的已知机械性状（页码正确、quote 绑定精确）；evidence 记录一经导入即冻结，不回改，此状况记录于本处置与 CORPUS_REPORT §13。

修订后 12 张卡全部重过 `manage_cards.py validate`；重建的 cards FTS 索引以修订后字节为准（见 v010 评测冻结快照）。一轮修订后不触发循环审计。
