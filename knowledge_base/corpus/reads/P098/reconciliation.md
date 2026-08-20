# P098 reconciliation — Constraint Injection (VRPCoder)

Disposition: `KEY_ANCHOR_ADMISSION_WITH_HOME_FIELD_AND_TEACHER_DISTILLATION_BOUNDARIES`
Read 1: `corpus/reads/P098/read_1.md`
Accepted read-2: `corpus/reads/P098/read_2_attempts/r2-20260727-p098-a1/`
  - report SHA-256: `bbf013f0b3ddd51895a67d64d8f14da45537d54f9bd7c88a3c25daccc35c8e6e`（20,987 B，已对盘复核）
Other attempts: none
Reconciler: main Codex, 2026-07-27

## Source reconciliation

2. **AGREE｜最干净证据 = 消融**：两臂共享底模/LoRA/解码/提示词/Cgold/DIFF，唯一差异 INJ 有无，且无注入臂数据更大（7347 vs 6797）——+2.86（SFT）/+4.00（GRPO）平均增益基本排除模型/token/prompt/oracle 混杂；分布外基准（B2/B4）增益最大。read-2 注记："更大数据=更保守"仅在数据同质时成立，但这 550 个含缺陷样本恰是 DIFF-only 管线的现实反事实，对照恰当。
3. **ACCEPT-BOUNDARY（read-2 新增，重要）｜主场分布混杂**：Benchmark 1/2 由论文自己的合成管线（同一教师、同 60 场景池、同措辞风格）生成，**B1 评测题还经过与训练数据相同的双验证过滤器**——B1/B2 对 VRPCoder 是主场、对 frontier 基线是客场；外部来源的 B3（+1.35）/B4（−8.40）信号更弱且混合。主表胜出不外推为一般 VRP 建模能力优势。
4. **ACCEPT-BOUNDARY（read-2 新增）｜教师蒸馏混杂与 headline 选择性**：训练数据由 Gemini-3.1-Pro Preview + Claude Opus 4.6 生成，而 Gemini 同时是最强评测基线——"学生超教师"主要发生在教师自家分布上，实为"教师输出经 Cgold 双验证过滤的再蒸馏"；按合并 AVG，Gemini 95.00 仍 > VRPCoder-GRPO 93.00（摘要"三基准胜出"表述准确但选择性）。OR-LLM 基线 78+ 分差距可能部分是分布/格式失配（用其原提示词；B3 上 0.00 类极端值），论文无归因实验。
5. **ACCEPT-BOUNDARY（read-2 新增）｜INJ 的契约前提与不可判定类**：可注入性依赖提示词强制的变量命名/arc-first 索引契约 + 教师 node_id_map 回译；构建失败/格式不支持/节点匹配不可靠/求解状态未决一律记验证失败弃样——**INJ 不是全覆盖判定器**，契约失配的实际规模未报告（OPEN）；单个 s+ 对伪过约束的覆盖强度未量化；实例规模极小（客户 4–12），规模外推未测。
6. **ACCEPT-GAP（read-2 新增）｜未报告项**：训练期 DIFF 容差 εobj 数值全文未给（与评测 10⁻³ 是否同值不明）；B.1 允诺的逐 profile 数据流统计表不存在；单次训练/评测无方差/种子重复——消融增益稳定性不可评估；B4 落后归因 TSPTW 缺席方向合理但无按变体拆分佐证。
7. **AGREE｜失败量化（read-2 补强）**：550/7347（≈7.5%）教师生成样本过 DIFF 但挂 INJ——纯目标等价过滤放行约束缺陷的**实测规模**（全文最有价值的非构造性失败记录）；Fig.1 钉子案例系作者构造性说明而非训练日志自然样本（引用时注明）；修复退化封堵（同车绑定防拆路掩盖超载）本身是一条一般性教训。

## Frozen source role

- **不是什么证据**：主表对 frontier 的胜负不作能力结论（主场分布+教师蒸馏+提示词协议三重混杂；合并 AVG 仍落后 Gemini）；不证对不服从命名契约的自由格式代码可用；不证规模外推（客户 4–12）；消融点值无方差佐证，按方向引用；OR-LLM 基线差距不作跨系统能力比较。
- 状态：preprint（v1，北航+百度）；代码/数据可用性未核验。
