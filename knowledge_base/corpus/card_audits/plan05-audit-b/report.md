# PLAN_05 Operator Card 独立核源 B 组报告

## 审计身份与边界

- task/thread identity：`/root/plan05_card_source_audit_b`
- 角色：未参与本组 Card 写作的独立核源读者
- 报告写入时间：2026-07-19T23:43:30+08:00（Asia/Shanghai）
- 审计对象：指定的 7 张 Operator Card
- 审计动作：核对 Card metadata、`evidence.json` 中的绑定 Evidence、原始 PDF 字节 SHA 与相关原文上下文；没有修改 Card、Evidence 或 PDF。
- 明确未执行：Candidate 生成、Reviewer 三审、novelty/prior-work 审查、Commissioning、联网扩展文献。

## 共同完整性检查

- `knowledge_base/corpus/evidence.json` SHA-256：`14595b5d45f8861752e6ef188505e761ca87f16885becfb46bfbd2e1667ea257`
- 7 张 Card 的 metadata 均可读，引用的 9 个 Evidence ID 均存在。
- 9 个 `source_refs.sha256` 均与 `knowledge_base/papers/` 中对应 PDF 的实际 SHA-256 完全一致。
- 9 个 Evidence 的 `fulltext_sha256` 均与对应 PDF 的实际 SHA-256 完全一致。
- Card 中科研内容均使用 `[CODEX_SYNTHESIS]` 或 `[CODEX_HYPOTHESIS]`；没有发现把综合或假设伪装成 `[AUTHOR_FACT]` 的正文陈述。Evidence ledger 的 `[AUTHOR_FACT]` 只承担来源绑定说明。

## 逐卡结论

### 1. `operator-hidden-state-tool-necessity-gate.md`

- Card SHA-256：`478e67c4440270f138f679d6cfd7fa9dfdbb7f31b67907b0841cc2e36535de03`
- Evidence：`ev-p041-operator-core`
- 原始来源：`P041_tool_call_necessity.pdf`，SHA-256 `a05f71b904209ea49cbc9cd13434255aab4037f96640477810fb78a61b701ba0`
- 证据判断：Evidence 直接支持“最后输入 token 的跨层 hidden states 中可线性解码 tool necessity”以及 forced no-tool 标签构造；原文还明确说明真实方法是 `PROBE&PREFILL`：阈值化 probe 结果后预填 steering sentence，模型随后继续生成。
- 问题：Card 把真实的“probe + soft/hard prefill steering”写成“gates tool access”。这会把可被模型覆盖的软引导误写成工具访问门禁，也漏掉 intervention identity 中关键的 prefill 动作。Evidence 本身也只覆盖 probe/标签，不足以支撑当前写法。
- 结论：**REVISION_REQUIRED**
- 最小修订：
  1. 将标题/Intervention target 改为“Hidden-State Tool-Necessity Probe with Prefill Steering”一类不暗示硬门禁的表述；
  2. 将 Before/After 改为“读取最后输入 token 的跨层 hidden states → 线性 probe/阈值 → 预填工具需要或无需工具的 steering sentence → 正常生成”，明确工具仍可访问且 soft prefill 可被覆盖；
  3. Output 写成 probe 概率/二值判断及其对应 prefill，而不是只写二值门控；
  4. 新增一条来自论文第 2 页或方法节的 Evidence，直接绑定 `PROBE&PREFILL`，保留现有 Evidence 用于 hidden-state/标签事实。

### 2. `operator-milestone-dag-trajectory-evaluation.md`

- Card SHA-256：`d61230628397c893db7ca52c9538e918ffc37ff5ee8329a1e2971d3b4f2a69cc`
- Evidence：`ev-p037-evaluation-core`
- 原始来源：`P037_toolsandbox.pdf`，SHA-256 `3449baed1d8e0f4c07dbc859621899685eed8a6a0445a1ae8909c178e6b6173e`
- 证据判断：现有 Evidence 直接支持 milestone DAG、拓扑序约束以及在多种映射中取最佳平均相似度。原始 PDF 第 4–5 页另外支持 Minefield、世界状态/消息轨迹匹配和违规后总分归零。
- 问题：Card 的 changed computation 与输出把 Minefield 违规检查作为核心组成，但 metadata 只绑定了不含 Minefield 的 Evidence。Card 科研内容本身与 PDF 一致，缺口是 Card → Evidence 的直接支撑不完整。
- 结论：**REVISION_REQUIRED**
- 最小修订：新增一条来自原始 PDF 第 4–5 页的 Minefield Evidence（应包含“must NOT occur”及违规计分规则），并把该 Evidence ID 加入 Card metadata/Evidence ledger；Card 正文无需扩写。

### 3. `operator-decomposed-research-evidence-evaluation.md`

- Card SHA-256：`764af077c05664a69bb0232840a65bc02bd8e9ca174f610e9ee14e4aa372c808`
- Evidence：`ev-p042-evaluation-core`、`ev-p043-evaluation-core`、`ev-p044-evaluation-core`
- 原始来源：P042/P043/P044，三份 PDF SHA 均与 metadata 一致。
- 证据判断：三条 Evidence 分别直接锚定多维报告评估、FACT 的事实/引用可信度分解，以及 expert-guided judge 与 claim-level verification 的组合。原始上下文进一步支持 statement-URL 提取、网页内容支持判断、任务特定 Expert Evaluation Guidance、隐式引用回溯和 claim-level 量化结果。
- intervention identity：支持。
- before/after：支持；“单一整体分数 → 分维度/分声明/分来源支撑”与三篇原文一致。
- 输入输出与时点：支持；均为报告生成后的评价，输入包含任务、报告、引用及取回来源，输出包含维度分数和 claim-level 支撑结果。
- 风险边界：Card 以 `[CODEX_SYNTHESIS]` 表述 judge/reference 依赖、动态网页、预处理和未覆盖声明，未把这些推断伪装成作者事实；原文上下文能解释这些边界。
- 结论：**PASS**

### 4. `operator-smt-preexecution-policy-guard.md`

- Card SHA-256：`960cede9f270231dac4d8f87a6fd5d6bd11144a2ceed47efa2b0e70393857975`
- Evidence：`ev-p046-operator-core`
- 原始来源：`P046_solver_aided_verification.pdf`，SHA-256 `0b29985358a4735f7e2ad032225cf5299080be4ef33cf8539f2550c8bbf06807`
- 证据判断：Evidence 直接支持在执行前拦截 planned tool call、用 Z3 检查 formal constraints、阻断违规调用。原始 PDF 第 2–3 页进一步支持从对话/参数提取可观察状态、SAT/UNSAT 输出、最小 unsat core 反馈及最多三次 replanning。
- intervention identity、before/after、输入输出与时点：支持。
- 风险边界：Card 明确把保证限制在人工审阅的 policy encoding 与抽取状态内；这与论文对自动形式化失败、语义完整性和约束紧致性的讨论一致。
- 标签：综合、假设与来源事实区分正确。
- 结论：**PASS**

### 5. `operator-bilevel-graph-toolchain-planning.md`

- Card SHA-256：`63635105cce05afd8db69402f06a023fa887792d9f26e9698fd762ecacf4be69`
- Evidence：`ev-p048-operator-core`
- 原始来源：`P048_naviagent.pdf`，SHA-256 `d7578b55678c89f2ffb78741c5faab8adf7c70e7e4160d2cd5fafea522e192ab`
- 证据判断：Evidence 直接支持高层决策与 graph-based toolchain construction/execution 解耦，以及高层选择 interaction mode、低层动态构造和修订 toolchain。原始 PDF 方法节支持 direct/clarify/retrieve/execute 四动作空间、历史/观察/裁剪图输入和 TWNM 图搜索。
- intervention identity、before/after、输入输出与时点：支持。
- 风险边界：simulated benchmark、不同方法调用步数、LLM-based TSR 判断和动态恢复验证范围均能从实验设置或方法边界追溯；Card 以综合标签呈现，没有扩大为作者结论。
- 结论：**PASS**

### 6. `operator-bounded-preexecution-reviewer.md`

- Card SHA-256：`51af09117a8233ab374d218f15d27d91619862157c4379bf6b3924ef04a24f0c`
- Evidence：`ev-p049-operator-core`
- 原始来源：`P049_reinforced_agent.pdf`，SHA-256 `352a4f39ae64d07722a7e63bfed3d9afad20f7529c406ee764af37d3503b40c8`
- 证据判断：现有 Evidence 直接支持 reviewer 在执行前检查 provisional tool call 并在发现错误时给出修订反馈。原始 PDF 第 1–3 页支持 execution agent/reviewer agent 的职责分离，以及“直到批准或最多 N 轮”的 progressive feedback；第 7/12 页支持 2.4–6.2× latency。
- 问题：Card 标题与核心 IO 强调“independent/bounded”，但唯一绑定 Evidence 的摘录既没有明确职责分离，也没有最大 N 轮。正文与原始 PDF 一致，缺口是 Evidence 绑定不足。
- 结论：**REVISION_REQUIRED**
- 最小修订：新增一条来自第 1–3 页的 Evidence，直接包含“primary execution agent / secondary review agent separation”与“until approval or maximum iterations N”；把新 Evidence 加入 metadata/Evidence ledger。Card 正文无需扩写。

### 7. `operator-active-counterexample-verifier.md`

- Card SHA-256：`ef06600ccabf67f1708049c00e5164ee2eb25f1b48949aff72407030b7b7c7b9`
- Evidence：`ev-p050-operator-core`
- 原始来源：`P050_agentic_verifier.pdf`，SHA-256 `81b1a3759a4de1b246240342435ef32f0f7d7265d17a938bd78086fe027b8654`
- 证据判断：Evidence 直接支持主动推理程序行为并搜索能暴露候选差异的高区分度输入。原始 PDF 第 2–7 页支持多轮执行交互、输入生成器、候选执行输出和 reranking 时点；第 5/9 页支持 validator、majority/consensus 与不完美 benchmark verifier 的边界。
- intervention identity、before/after、输入输出与时点：支持。
- 风险边界：“差异不等于正确性，validator/majority 不是形式真值”是对原文实验机制的保守综合，标签正确。
- 结论：**PASS**

## 总结

- PASS：4 张（decomposed research evaluation、SMT guard、bilevel graph planning、active counterexample verifier）。
- REVISION_REQUIRED：3 张。
  - P041：存在 intervention identity 实质性误写，必须把“硬门禁”改回“probe + prefill steering”。
  - P037、P049：正文与原始 PDF 基本一致，但 Card metadata 的 Evidence 链没有直接覆盖其标题/核心计算中的 Minefield 或 bounded independent reviewer，需最小补证。
- 在上述 3 张完成最小修订并重做对应单卡核源前，本组不应整体标记为 source-audit PASS。

## 实际读取文件与范围

### Card（全文）

- `knowledge_base/cards/operator/operator-hidden-state-tool-necessity-gate.md`
- `knowledge_base/cards/operator/operator-milestone-dag-trajectory-evaluation.md`
- `knowledge_base/cards/operator/operator-decomposed-research-evidence-evaluation.md`
- `knowledge_base/cards/operator/operator-smt-preexecution-policy-guard.md`
- `knowledge_base/cards/operator/operator-bilevel-graph-toolchain-planning.md`
- `knowledge_base/cards/operator/operator-bounded-preexecution-reviewer.md`
- `knowledge_base/cards/operator/operator-active-counterexample-verifier.md`

### Evidence

- `knowledge_base/corpus/evidence.json`：只读取并审计上述 7 张 Card 绑定的 9 个 Evidence 对象。

### 原始 PDF（相关页与相邻上下文）

- `knowledge_base/papers/P041_tool_call_necessity.pdf`：摘要、引言、Probe 设定、PROBE&PREFILL 方法及相关附录结果页。
- `knowledge_base/papers/P037_toolsandbox.pdf`：第 1–6、16–19 物理页。
- `knowledge_base/papers/P042_live_research_bench.pdf`：第 6–7 物理页。
- `knowledge_base/papers/P043_deepresearch_bench.pdf`：第 4–6 物理页。
- `knowledge_base/papers/P044_deer.pdf`：第 3–6 物理页。
- `knowledge_base/papers/P046_solver_aided_verification.pdf`：第 1–3 物理页。
- `knowledge_base/papers/P048_naviagent.pdf`：摘要、方法与实验设置/消融相关页（第 1–11 物理页内的相关上下文）。
- `knowledge_base/papers/P049_reinforced_agent.pdf`：摘要、方法、误差/延迟与限制相关页（第 1–5、7–10、12 物理页）。
- `knowledge_base/papers/P050_agentic_verifier.pdf`：第 1–10 物理页。

## 未读范围

- 没有读取任何 blind query、blind judgment 或 blind result 文件。
- 没有读取或审计本任务指定范围之外的 Card。
- 没有对上述 PDF 做无关章节的逐页全文复读；只读取足以核对 intervention identity、before/after、输入输出时点和风险边界的原文及相邻上下文。
- 没有读取外部网页、代码仓库或第三方二手材料；本报告只以当前 admitted PDF、绑定 Evidence 和 Card 为依据。
