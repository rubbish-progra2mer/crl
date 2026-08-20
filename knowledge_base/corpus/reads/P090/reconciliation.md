# P090 reconciliation — MemGAS

Disposition: `OPERATOR_AND_FAILURE_ADMISSION_WITH_UNABLATED_FILTER_AND_METRIC_STYLE_BOUNDARIES`
Read 1: `corpus/reads/P090/read_1.md`
Accepted read-2: `corpus/reads/P090/read_2_attempts/r2-20260727-p090-a1/`
  - invocation SHA-256: 见目录内文件（含 runtime provenance 补全）
  - report SHA-256: `f7e985e40a621865b2c7092c2d318df876e326d0f56ac6d9752327ab89c8717e`（21,177 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**——两读在机制、主数字、公平性控制上无事实冲突；二读新增项均为原文自带缺陷或边界，双通道（文本+视觉）已自证，无需第三读裁决。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜机制链**：四粒度元数据（Eq.1-2）→ GMM accept/reject 关联图 → 熵倒数粒度路由（Eq.3-4）→ 加权种子 PPR（Eq.5）→ LLM 冗余过滤。两读定位一致（read_1 pp.3-5；read_2 §1 各条含逐字锚）。
2. **AGREE｜training-free 与公平性控制**：统一 gpt-4o-mini-2024-07-18、共享生成提示词、温度 0、统一 top-3、Contriever 编码底座（p.6）。
3. **AGREE｜核心结果**：LongMemEval-s 4o-J 60.20/F1 20.38/R@10 94.47；Table 7 knowledge-update 行（turn 41.67 / router 51.39 / oracle 72.22）；建库成本 Table 8（52.9M in/5.2M out）；同预算 Table 10 下仍最高。
4. **ACCEPT-BOUNDARY（read-2 新增）｜过滤步未消融**：Table 3 只拆 GMM/PPR/MA/Router，无 "w/o LLM-Filter" 行，而查询感知过滤是多数基线不具备的组件——**MemGAS 的增益是含过滤步的 bundle 级主张**，不得归因给路由/图结构单一组件。
5. **ACCEPT-BOUNDARY（read-2 新增）｜指标风格放大**：词面指标增幅（F1 +48%）远大于判定指标（4o-J +8.7%）；过滤指令"保留原 token"利于抽取式短答风格。引用本文数字优先 GPT4o-J 口径。
6. **ACCEPT-BOUNDARY（read-2 新增）｜user-user 载体失利**：LoCoMo（唯一 user-user 语料）4o-J 上 MemGAS 41.07 **低于** HippoRAG 2 (45.62，表内加粗) 与 SeCom (44.21)；且朴素 Combination 在 4o-J 口径下 2/4 数据集反超完整方法（Table 5）。read_1 未标出此点，采纳 read_2。
7. **ACCEPT-DEFECT（read-2 新增，双通道确认为原生缺陷）**：(a) Table 10 两块 Input Tokens 均印 "8,000"（正文为 8,000/16,000 两档）；(b) Fig.15/16 的 After Filter 输出框互换；(c) §D.1 正文把 HippoRAG 2 输入 token 误作输出（实际输出优势 ~2× 非 ~20×）；(d) 跨表数值不一致（LoCoMo 4o-J Table 1=41.07 vs Table 5=40.08；Table 2 vs Table 6 检索行小差）——**引用 LoCoMo 数字必须注明表号**；(e) 附录 H 称 PPR "not a contribution" 与正文归属表述不一致。
8. **OPEN（两读一致遗留）**：多粒度命中折算 session 级 Recall/NDCG 的口径未写明（复现前须查代码）；Combination 基线实现无公式；超参 (α=15, λ=0.2) 是否全数据集统一未明说。

## Frozen source role

- **不是什么证据**：不证 user-user 对话载体上的优势（LoCoMo 判定指标失利）；不证输出 token "20×" 节省（正文误写）；不证过滤步之外单组件的独立贡献；不含任何时序有效性能力。
- 状态：preprint（ICLR 模板无接收标注），数字引用须带表号。
