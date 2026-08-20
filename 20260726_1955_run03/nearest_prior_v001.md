# Main Codex Nearest Prior Record

## Frozen before review

本文是主 Codex 的私有最近先行记录（v001），在 Review Packet 冻结前预提交：本文 bytes 的 SHA-256 将记入 RUN_LEDGER 与 Packet commitment 区；正文不进入共同 Packet。写入时间：2026-07-26T22:10+08:00（初稿，冻结前可修订，冻结即锁定）。

## Search views

- **Changed computation（中性）**："对 LLM 生成的可执行约束模型，在其可行集内对每个参考条件做对抗搜索，量化被解级成功掩盖的静默漏约束质量"。
- **关键组件**：solver 反例查询（SAT/SMT 标准能力）；参考条件的 harness 侧编码；逐约束 enforcement 判定；掩盖/捕获分类。
- **完整 pipeline**：NL 约束规格 → LLM 形式化 → solver → 解级认证 →（错误触发修复）。
- **组件组合与可运行基线**：探针式规格验证在相邻载体的既有实现及其可运行性。

## Exact searches

全部在 2026-07-26（Asia/Shanghai）执行，开放网络 WebSearch/WebFetch：

1. "testing LLM generated formal specifications unit tests counterexample validation omitted constraints autoformalization 2025 2026" → 2510.23350（Alloy）、2605.26457（Verus-SpecGym）、2606.29493（Lean 基准缺陷）。
2. "mutation testing metamorphic validation LLM translated constraints SMT solver planning specification faithfulness audit" → SMT solver 测试（OOPSLA21 型变异）、2607.03223（Round-trip mutation）。
3. "LLM planning formalization faithfulness verification PDDL SMT model errors natural language constraints 2025 2026" → 2606.29700（planner-in-the-loop）、2606.00981、2503.18971（survey）、NL-PDDL-Bench、ACL 2025 formalizer limits（=P054）。
4. "LLM optimization modeling formalization validation solver probe enforcement missing constraint silent failure audit OR NL4OPT" → ReLoop 2602.15983、Constraint Injection 2606.04816、OptArgus 2605.11738、ORPilot 2605.02728、OptiRepair 2602.19439、ConstraintBench 2602.22465。
5. "'under-constrained' OR 'missing constraints' LLM generated planning model SMT PDDL detection without ground truth silent success false positive" → CaStL 2410.22225、2510.05486（=P055 lineage）、2606.29700。
6. "TravelPlanner SMT formalization audit constraint enforcement verification faithfulness solver success masks omission" → 只命中 P051（2404.11891）本身与综述页，无 enforcement 审计工作。
7. "vacuity detection model checking coverage metrics formal verification" → Kupferman & Vardi（vacuity detection in temporal model checking）、Chockler-Kupferman-Vardi（coverage metrics, FMSD 2006）、Kupferman "Sanity Checks in Formal Verification"（CONCUR 2006）、Beer et al. 2001。
8. "Zhong Yu Klein test suite evaluation text-to-SQL semantic accuracy distilled test suites 2020" → EMNLP 2020（arXiv 2010.02840），代码公开（taoyds/test-suite-sql-eval），Spider 官方指标。
9. 深读：2606.04816 全文（HTML）；2602.15983 全文（HTML）；2510.23350 摘要页。

全文可得性：2606.04816、2602.15983 HTML 全文已读；2510.23350 摘要级（正文 Springer 付费，标 unresolved 到摘要边界）；经典 vacuity/coverage 文献读到作者页 PDF 摘要级。

## Component collisions

- **solver 反例查询**：标准能力，无归属问题。
- **"检查通过但成分未起作用"**：模型检测的 vacuity detection / coverage metrics（Kupferman-Vardi 系）是概念级祖先。差异：vacuity/coverage 审计的是"给定 spec 与给定 model 的检查过程"；本 kernel 审计的是"LLM 生成的 model 相对外部参考条件的 enforcement"，参考条件不在被审对象内部。计算对象与信息可得性不同，非同一 family。
- **P050 active counterexample verifier**（KB 内）：借用的搜索结构来源，作用对象是候选程序区分，非规格 enforcement；已在 Research Map 以 Operator 迁移形式披露。

## Composition collisions

- **Zhong-Yu-Klein 2020（distilled test suites）**：同一认识论（单实例执行成功掩盖语义错误查询；用对抗构造暴露），载体 NL→SQL，暴露手段是蒸馏数据库测试套件（对 gold query 高覆盖）。差异：需要 gold query 生成测试套件；不给逐约束 enforcement 判定；不研究 slack 结构与修复盲区。**认识论最近祖先，计算不同（数据库蒸馏 vs 生成模型可行集内 SAT 探针），载体不同**。
- **2510.23350（Alloy + LLM 测试用例）**：LLM 从 NL 生成测试用例验证 Alloy 域模型；定性检测主张；无掩盖率量化、无 slack、无 solver 对抗探针（测试来自 LLM，引入生成保真风险）。
- **Verus-SpecGym 2605.26457**：可执行规格对具体 case 的 accept/reject 作忠实性信号，载体为程序验证规格评测环境；非规划、无掩盖分解。
- **ReLoop 2602.15983**：**当前最强组合碰撞**。已量化 OR 库存载体上 91.1% solver-feasible vs 0.5% formulation-correct 的 feasibility–correctness gap；行为验证 = 数据参数极端扰动的敏感性启发式（阈值分级），约束抽取复用同一 LLM（自认 failure correlation）；修复环内嵌。差异：(a) 其 gap 以"formulation correctness（对 gold 公式）"为真值，我以"参考条件的证书级 enforcement 判定（SAT witness + 检查器复核）"为真值，无 LLM 参与检测；(b) 无逐约束 enforcement 剖面（其 L2 是启发式存在性测试，承认漏掉 structural 错误）；(c) 无 slack-luck 机制分析与可控收紧反事实；(d) 无错误触发修复盲区的显式量化（其 L1 即错误触发，文中定性承认 "solver feedback catches syntax errors, not missing constraints"）；(e) 载体为 Gurobi 代码生成，非 NL agent 规划基准。
- **Constraint Injection 2606.04816**：训练方法（SFT+GRPO，VRPCoder 8B）——用可行/单约束违反探针做训练信号；探针需按域手工设计 attack operators 与 gold 规格；评测仍是 Pass@1（objective equivalence）；其 Limitations 明文把"反映独立约束违规剖面的更细粒度解耦评测指标"列为 open problem。本 kernel 恰是该 open problem 的测量端实现，且不训练。
- **OptArgus 2605.11738 / OptiRepair 2602.19439 / ORPilot 2605.02728**：多 Agent 幻觉检测 / 闭环修复 / 生产工具，OR 载体；检测均含 LLM 判断环节；无证书级 enforcement 分解。

## Full-pipeline collisions

- **P051（2404.11891）**：被审计范式的旗舰（NL→SMT→solver→解级认证 93.3% val）；其 unsat-core 修复只在 UNSAT 分支触发；论文自报的失败分析（block picking all-different 遗漏）证明遗漏在其管线真实发生。无 enforcement 审计。
- **P052 LLMFP**：分解式形式化 + 五轮同模型自评；自评误诊有作者事实（Gripper 不终止）。
- **2606.29700 planner-in-the-loop**：VAL/planner 错误信号反馈修复——错误触发家族，静默 SAT 分支无信号。
- **P055/CoPE**：认证指标的假阳性通道由作者自认（"no feasible alternative"、20 样本零假阳性、简化域）；是本 kernel 直接反驳的占用者论断。

## Comparator roles and relative differences

- **nearest（认识论）**：Zhong-Yu-Klein 2020。**nearest（量化 + 相邻载体）**：ReLoop。**nearest（探针构造）**：Constraint Injection。**current-strongest 可运行竞争分解**：无——在带逐约束参考检查器的 NL agent 规划载体上，未检得任何可运行的 enforcement/masking 分解实现（absence-of-evidence，检索日 2026-07-26，检索式见上）。
- **collision verdict**：无未解决碰撞。三个最近邻都不计算"解级认证的掩盖率 + 逐约束证书级剖面 + slack 机制 + 修复盲区"这组量；两个最近邻（ReLoop 定性承认修复盲区、Constraint Injection 明文列为 open problem）反而为本 kernel 的空缺提供占用者自证。
- **风险标注**：若 Reviewer 找到 2026 年 6-7 月更新的、在规划载体上运行探针审计的工作，本 verdict 需重开；检索已尽当前可达面。

## Closest-composition conclusion

不存在可直接运行于本载体的外部竞争分解，因此 Promotion Development 的 comparator 采用**内部臂矩阵**（run02 先例）：在同一批冻结的 F1 形式化产物上，实测 (A1) 解级认证信号、(A2) 错误信号集合（UNSAT/异常——错误触发修复家族的触发面）、(A3) 同模型 self-check（P052 家族的自评计算）、(A4) 选项消融行为测试（ReLoop-CPT 在本载体的忠实改编：删除全部合规选项重解 / 数值参数极端缩放）、(A5) enforcement 探针（唯一 delta）。A2/A3/A4 是三个已占用检测家族的载体内改编，构成组件级与组合级近邻的可运行代理；证书级真值由 A5 的 witness + 参考检查器复核提供。预注册 Confirmation Plan 沿用同一臂矩阵。若 Reviewer 认为 A4 改编不忠实于 ReLoop 原方法，应把 A4 结论限缩为"该类行为测试的一个实例"而非对 ReLoop 的直接比较——本记录预先承认该限缩。
