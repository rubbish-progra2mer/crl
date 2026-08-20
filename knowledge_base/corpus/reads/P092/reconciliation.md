# P092 reconciliation — MemConflict

Disposition: `MEASUREMENT_COMPOSITION_ADMISSION_WITH_NO_NAIVE_BASELINE_AND_COCONSTRUCTION_BOUNDARIES`
Read 1: `corpus/reads/P092/read_1.md`
Accepted read-2: `corpus/reads/P092/read_2_attempts/r2-20260727-p092-a1/`
  - report SHA-256: `c866338f19b6385c216f64c49a2dcc52cbdb4c496552f0f49fa805018d9b6d24`（24,013 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**——两读事实一致；read_2 的新增项全部为原文可定位的边界/空缺。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜框架与指标**：三类冲突（dynamic/static/conditional）fitness-for-use 形式化；两级协议 AA + SEH@K/SRS + UOCS/CRS 诊断；EUG = SEH@3 − AA 的利用缺口分解；冲突后立即发问的查询时点（区别于"全会话后统一问"）。
2. **AGREE｜数据与主结果**：12 实例/均 52.3 会话/204k tokens/124.3 查询（dynamic 90.8/static 16.7/conditional 16.9，宏平均聚合）；MemOS 平均最强（AA 0.554/SEH@3 0.671）；CRS 全员 ≤0.2501；static 最难；距离/长历史/implicit/干扰项四向敏感性齐降；LangMem dynamic 利用失败 53.9% > 检索失败。
3. **ACCEPT-GAP（read-2 新增，重要）｜无朴素对照基线**：全文没有 full-context、朴素 RAG-over-raw-history 或 recency 启发式基线——六系统相对"什么都不做的简单方案"的增益不可知。**该基准作为证据源的结构性空缺**，任何引用其系统排名的结论都不含"相对朴素方案"的信息。
4. **ACCEPT-BOUNDARY（read-2 新增）｜构造-评测同源**：数据 LLM 生成 + 判分 LLM 辅助（同为 gpt-5.0-mini，无版本号）；人工核验只有定性描述，无人数/覆盖率/一致率；无方差/显著性；static/conditional 每实例仅 ~16.7 查询——表内四位小数差异的稳健性未知。
5. **ACCEPT-BOUNDARY（read-2 新增）｜白盒可比性**：各系统记忆粒度不同，"gold memory item 命中"依赖 LLM 语义匹配，粒度差异可能造成 SEH/SRS 跨系统偏置（无校准实验）；各系统按默认配置接入，token/tool-call 预算未报告。
6. **AGREE｜作者自认限制**：受控模拟非自然交互；三类困难之外未建模；白盒协议对不透明系统难适用。
7. **ACCEPT-NOTE（read-2）**：ACM 模板占位符（J.ACM 2018/DOI XXXXXXX/2007-2009 收稿行）不得用作出版信息；Op-8 设计建议三件套（时间状态编码/conflict-aware rerank/生成前验证）是**未实证的假设性建议**，引用须标注；效率表（Mem0 加库 40216s vs MemOS 1356s）无硬件/并发条件说明。

## Frozen source role

- **准入角色**：最近外部组合（记忆冲突的白盒检索/排序评测协议 SEH@K/SRS/EUG + 三类冲突构造 + 冲突距离/干扰项操纵算子）；Failure 来源（六系统冲突处理强弱不均、CRS 全线低迷、"答案对≠识别矛盾"、"证据在场≠被用"）；measurement risk 来源（构造-评测同源、无朴素基线、白盒粒度偏置）。
- **不是什么证据**：不证六系统相对朴素方案（full-context/naive RAG/recency）的优势——该对照不存在；系统间四位小数差异不作数值引用（无方差）；Op-8 建议不作已验证 Operator；出版信息以 arXiv 水印为准。
- 状态：preprint（ACM 模板投稿态），judge 模型无版本锚。
