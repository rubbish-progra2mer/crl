# PLAN_05 Card 来源独立审计 D

## 结论

**NEEDS_REVISION**

两张 Card 的文件来源、Evidence、passage、字符区间和 SHA-256 机械链路完整，但正文仍有来源归因和精确引用问题。问题集中在：把 P051 的重复选择错误归因给 solver；使用未被本卡 Evidence 覆盖的 P004 谱系、P052 基线定义和五轮上限；把论文中的 `Code_SMT` 基线扩写成未被当前证据精确证明的 “one-shot/一步生成”；以及数条 Evidence 的结构化 `section` 与原始 PDF 标题不一致。修正前不应把这两张 Card 视为来源审计通过。

本报告只是 Card 来源审计，不是 Commissioning Reviewer，不评价任何 Candidate、novelty 或方法潜力。

## 审计范围与隔离

仅审查：

- `knowledge_base/cards/operator/operator-decomposed-solver-backed-formal-planning.md`
- `knowledge_base/cards/failure/failure-solver-guarantee-stops-at-formalization.md`

仅使用：

- `knowledge_base/corpus/evidence.json`
- `knowledge_base/knowledge.plan05_final_scratch.sqlite`
- `knowledge_base/papers/P051_formal_verification_planning.pdf`
- `knowledge_base/papers/P052_llmfp.pdf`

未读取 P051/P052 的 `read_1`、`read_2`、`read_3`、`reconciliation`，未读取 Corpus Report、其他审计报告或任何 blind 材料。

审计输入 SHA-256：

- Operator Card：`124b3a6745a6ee2400cfe48e89e4b97831e7871f4819c4bd3ad889fc763b1b82`
- Failure Card：`8462a8670d338ab1c4e2e1a1e48ff4651063d5b416e0ed27e9bd947ffb545692`
- canonical `evidence.json`：`8151019097a16d0e28677315ccefa88631b7d1ef8fab40444abd7041b632edc3`
- scratch SQLite：`55a9e002eda7058996765f15accceea018837072d2afd1fb133076d8b37fee79`

## 机械来源链核查

### PASS 项

1. 两张 Card 的 `source_refs` 都只指向 P051、P052；实际 PDF SHA-256 与 Card、SQLite `papers.fulltext_sha256`、9 条相关 Evidence 的 `fulltext_sha256` 完全一致：
   - P051：`ba9261d6d8fbf2b43817e57c29aa6ffacc0b14ef038e6c86a33f8780490bd365`
   - P052：`e59c5c55b3befeeb4774a20990b8629f487e9fb1520cc2a953f041b7bb6fdaec`
2. 两张 Card 共引用 9 个不同 Evidence ID。9 个 ID 均在 canonical `evidence.json` 与 scratch SQLite 中存在，二者全部共享字段逐项一致。
3. 9 条 Evidence 的 `source_content_sha256` 重新按 UTF-8 计算均匹配；对应 passage 的 `text_sha256` 重新计算均匹配。
4. 每条 Evidence 的 `passage_text_sha256` 均等于当前 passage 的 `text_sha256`；`quote_start`/`quote_end` 均在边界内，切片结果逐字等于 `source_content`。
5. Card 正文中的 Evidence 引用均包含于各自元数据 `evidence_ids`，元数据中列出的 Evidence 也都在正文出现。

### 来源元数据需修正

以下 Evidence 的物理页、locator、原文片段和 SHA 均正确，但 `section` 字段继承了过粗或错误的 passage section，与 PDF 可见标题不一致：

- `ev-p051-solver-guarantee-boundary`：记录为 `Related Work`，原文为 §3.3.3 `SMT Solver`（P051 物理页 5）。
- `ev-p051-cost-boundary`：记录为 `Conclusion`，原文为 Appendix B.1 `Satisfiable Plan Solving`（P051 物理页 16）。
- `ev-p051-omitted-constraint-failure`：记录为 `Conclusion`，locator 指向 Appendix F.3，原文确为附录失败分析（P051 物理页 23）。
- `ev-p052-implicit-constraint-failure`：记录为 `REFERENCES`，原文为 Appendix A.6.1 `Coffee`（P052 物理页 24）。
- `ev-p052-self-diagnosis-nontermination`：记录为 `REFERENCES`，原文为 Appendix A.6.9 `Gripper`（P052 物理页 25）。

必要修改：修正 canonical Evidence 与相应 passage 的 section/分段元数据，同时保持 PDF、物理页、精确片段、字符区间及重新计算后的哈希一致。locator 已给出正确小节不能消除结构化 `section` 的错误。

## Operator Card 审计

### 被现有引用精确支持

- P051 的自然语言查询 → 形式化步骤 → 可执行 SMT 代码 → solver 调用流程，由 `ev-p051-formalization-pipeline` 支持。
- P051 的保证只在生成代码已经编码问题后成立，且表述为约束可满足时由 sound and complete SMT solver 找到方案，由 `ev-p051-solver-guarantee-boundary` 支持。
- P051 的多次 LLM 调用、平均成本与时延边界，由 `ev-p051-cost-boundary` 支持。
- P052 的 DEFINER → FORMULATOR → CODE GENERATOR 分解，由 `ev-p052-decomposed-formalization` 支持。
- P052 的固定格式结果转换、自评并修改首个判错步骤，由 `ev-p052-result-self-assessment` 支持。
- P052 FORMULATOR 使用非测试任务特定且跨任务固定的示例，由 `ev-p052-fixed-cross-task-examples` 支持；但完整页还说明多步任务会换成一个固定的多步任务示例，因此不应写成所有任务类别共用完全相同示例。

### 必要修改

1. **删除或补证 P004 谱系节点。** `Source lineage` 写有“P004 约束失败 → P051…”，但本 Card 的 `source_refs` 和 `evidence_ids` 都没有 P004。按当前两篇来源的审计边界，应删除该节点；若保留，必须新增可回溯到 P004 原文的 Evidence 和 SourceRef 后再审。
2. **为“最多五轮”的有界性补 Evidence，或删除“有界”表述。** 当前 `ev-p052-result-self-assessment` 的精确片段没有轮数上限；P052 物理页 7 §3.6 才写明 `maximum number of loops to be 5`。建议把正文改为“固定格式的结果转换，并进行最多 5 轮的自评与修改”，同时引用覆盖 §3.6 上限的 Evidence。当前“有界的结果格式化与同模型自评”既缺精确引用，也容易把“有界”错误修饰到结果格式化。
3. **不要把 `Code_SMT` 自动扩写成 “one-shot/一步生成”。** P052 物理页 8 §4.2 将基线定义为提示 LLM 生成使用 Z3 的 Python 代码，且说明它与 LLMFP 使用相同输入信息；当前 Card 没有引用该页 Evidence，原文此处也未用 “one-shot” 一词。应改用作者的精确基线名 `Code_SMT`，或新增能明确证明单次生成语义的原文 Evidence。
4. **为命名基线补引用。** `Predicted observable signature` 使用 `direct planning` 和 `Code-SMT`，`Before and after computation` 也定义了相同基线，但现有 6 条 Evidence 没有基线定义。应新增 P052 物理页 8 §4.2 的基线 Evidence；若不新增，则把表述泛化为不依赖论文特定基线身份的假设。
5. **缩窄 Evidence ledger 的 AUTHOR_FACT 措辞。** “两篇直接谱系论文”这一谱系身份并非 6 个被引 Evidence 的内容。可改成 `[CODEX_SYNTHESIS] 本卡把 P051 与 P052 视为直接方法谱系；下列 Evidence 分别支持流程、保证边界、分解、自评与成本`；若要保留 `[AUTHOR_FACT]` 的直接谱系说法，应加入 P052 对 Hao et al. (2024)/P051 前身工作的明确引用 Evidence。

## Failure Card 审计

### 被现有引用精确支持

- P051 的 all-different 遗漏及最终计划重复选择相同 block，由 `ev-p051-omitted-constraint-failure` 支持。
- P052 DEFINER 遗漏隐式物料守恒约束，导致形式模型允许无来源供给/加工并压低成本，由 `ev-p052-implicit-constraint-failure` 支持。
- P051 对已编码且可满足约束系统的 solver 保证边界，由 `ev-p051-solver-guarantee-boundary` 支持。
- P052 在 Gripper 中把代码生成错误误诊为 timestep 不足、再嵌套一层循环并造成永久执行，由 `ev-p052-self-diagnosis-nontermination` 支持。
- “自然语言意图与编码模型不自动等价”作为 `[CODEX_SYNTHESIS]`，与上述保证边界和两类遗漏失败一致；repair boundary 明确标为 `[CODEX_HYPOTHESIS]`，没有伪装成作者结论。

### 必要修改

1. **纠正 P051 失败的主体归因。** Card 写成“solver 重复选择同一对象”，但 P051 原文写的是 LLM 生成代码未显式检查 block index 全异，并称 LLM 在两份计划中重复选择高分 block。应改为：`P051 的 LLM 生成代码遗漏 all-different 约束，所得计划重复选择同一 block`。若要描述 solver 角色，应另以 `[CODEX_SYNTHESIS]` 写成“solver 优化了语义不完整但形式可满足的编码模型”，不能把作者原文直接改写为 solver 主动选择。
2. **补充基线定义 Evidence 或删除论文特定基线要求。** `Warning for future candidates` 要求与 `direct planning`、`one-shot Code-SMT` 比较，但本 Card 的 4 条 Evidence 都不定义这些基线。P052 物理页 8 §4.2 可支持 `Direct`、`Code_SMT`、相同模型族和相同输入信息；它不直接支持 “one-shot” 措辞，也没有证明预算已相等。建议引用新增的 §4.2 Evidence，并将“one-shot Code-SMT”改为作者原名 `Code_SMT`；“申明预算”可保留为 Codex 的未来实验纪律，但不得写成作者已采用等预算比较的事实。
3. **把 Evidence ledger 的综合边界改标为综合。** “两篇论文共同支撑‘solver 正确、形式化仍可能错误’”是跨 Evidence 的推断，不是任一所引片段逐字给出的作者结论。建议将该句标为 `[CODEX_SYNTHESIS]`，并把可直接归于作者的四项事实分别保留为 `[AUTHOR_FACT]`。

## 修改后复验条件

只有在以下事项全部完成后，本审计结论才可改为 PASS：

1. 修正 Failure Card 对 P051 重复选择的主体归因。
2. 删除 P004 谱系节点，或补齐 P004 的 SourceRef 与精确 Evidence。
3. 为 P052 §3.6 的五轮上限和 §4.2 的 Direct/Code_SMT 基线定义补建并引用 Evidence，或删除相关精确事实。
4. 删除未经精确证明的 “one-shot/一步生成” 扩写，除非另有直接 Evidence。
5. 将跨论文归纳从 `[AUTHOR_FACT]` 调整为 `[CODEX_SYNTHESIS]`，或拆成逐条可直接归于作者的事实。
6. 修正列出的 Evidence/passage `section` 元数据并重新核对哈希与字符区间。

本审计未改动任何 Card、Evidence、SQLite 或 PDF。
