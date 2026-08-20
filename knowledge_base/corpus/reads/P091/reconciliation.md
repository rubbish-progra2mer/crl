# P091 reconciliation — MemStrata

Disposition: `FAILURE_AND_MEASUREMENT_ADMISSION_WITH_COCONSTRUCTION_AND_MISSING_BASELINE_BOUNDARIES`
Read 1: `corpus/reads/P091/read_1.md`
Accepted read-2: `corpus/reads/P091/read_2_attempts/r2-20260727-p091-a1/`
  - report SHA-256: `1dbd0c2793298e1acae88ce642af59c151b4ae16c22aee202653cd2f1ab42261`（17,133 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**——两读无事实冲突；read_2 新增边界均有原文逐字锚。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜核心不可能性结果**：98 对上 cosine AUROC 0.5926、contradict 均值 0.8119 > duplicate 0.7998、任意阈值 max precision 0.667（§5.1 Table 1）。
2. **AGREE｜机制与主结果**：确定性 (S,R,O) supersession + bi-temporal ledger + 读路径无 LLM；静态打平（0.82/0.30 vs 0.86/0.30）、演化 0.95–1.00 vs RAG 0.20–0.47；stale-fact-error forced 制 15–40% vs ~0%；D.1/D.1b 双向消融夹逼（去 supersession 0.99→0.33 且捏造 0.04→0.25）。
3. **AGREE｜marker-free 不变量**：去 [OUTDATED] 使基线掉 14–18 分而 temporal 仅 −4；单测强制。
4. **ACCEPT-BOUNDARY（read-2 新增）｜基准-抽取器共构**：抽取 prompt（C.1）的 few-shot 首例与 code_mutation 基准首场景 state-A 句**逐字相同**——~97% 抽取成功率在该模板族上可能被 few-shot 覆盖抬高（自由散文上实测塌到 ~44% 与此一致）。引用抽取率必须连同此共构。
5. **ACCEPT-BOUNDARY（read-2 新增）｜缺时序元数据 RAG 基线**："RAG cannot avoid by construction" 严格只对**无时间元数据的 naive/rerank RAG** 成立；未测 timestamped-chunk RAG 或 recency 加权检索等给基线顺序信号的廉价变体；也未实测任何外部记忆系统（Mem0/MemGPT 只在相关工作）。普适口径按此收窄。
6. **ACCEPT-BOUNDARY（read-2 新增）｜"no LLM" 口径**：仅指键比较与读路径；写路径的三元组抽取是 LLM prompt、散文回退走相似度+LLM gate。
7. **ACCEPT-DEFECT（read-2 新增）**：(a) 自称 "We release the harness…" 但 PDF 内无任何仓库 URL——发布物不可核验；(b) A.1 中 no_memory 条件报非零活动事实数（统计瑕疵，原文无解释）；(c) code_mutation stale 实为 0.033 非严格 0（作者以 ~0% 概括）；(d) "ties RAG" 是宽松措辞（domain 差 4 分）；(e) SWE-bench 引用疑残留。
8. **AGREE｜作者自认限制**：抽取是硬边界（97% vs 44%、隔离基准上反输 advanced_rag 0.62 vs 0.74）；摄入顺序代理时间；单 judge 噪声；单 7B/数十条每基准；correctness judge prompt 未印出（stale 判定实现无法从 PDF 核实，OPEN）。

## Frozen source role

- **准入角色**：Failure/negative evidence 来源（相似度不可分辨矛盾/复述；相似度门控泄漏 stale 25–60%；并置新旧值诱发捏造 ~6×；有损合并毁静态召回）；measurement risk 来源（marker 污染不变量；表面版本号启发式；弃答掩盖 stale 承诺→forced-answer 协议）；写侧结构化 supersession 节点占位者。
- **不是什么证据**：不证对带时序元数据 RAG 或外部记忆系统的优势（未测）；不证自由文本场景可用性（抽取 44%、隔离基准反输）；抽取成功率数字不脱离共构引用；所有数字为未同行评审单机自测、无外部可核验发布物——证据等级低于正式发表来源，不得用于任何数值外推。
- 状态：草稿态单作者 preprint（正文自带匿名化指示残留），Card 中引用一律注明该身份。
