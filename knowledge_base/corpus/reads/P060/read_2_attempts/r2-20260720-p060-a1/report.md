# P060 独立二读报告

## Provenance

- Attempt：`r2-20260720-p060-a1`
- Invocation：`knowledge_base/corpus/reads/P060/read_2_attempts/r2-20260720-p060-a1/invocation.md`
- 论文：Kagitha et al., *Unifying Inference-Time Planning Language Generation*，Findings of ACL 2026，ACL Anthology `2026.findings-acl.415`。
- PDF：`knowledge_base/staging/plan05_sat_a1/P060_unifying_planning_language.pdf`
- PDF SHA-256：`5e3695206fd0e01347e348d606ebd206387f4fba3192ed24ea5133abdef36305`（实测与 invocation 匹配）。
- 冻结 prompt：仅从 invocation 内嵌 `Frozen prompt bytes` 读取；未另读 prompt source。Invocation 记录 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。
- 物理页数：44；已按物理页 1–44 顺序完整读取。
- 线程 provenance：`reused independent reader thread due platform thread cap`。本线程此前未接触 P060，但线程并非新建，故不声称 fresh thread。
- Canonical task/thread：`/root/plan05_card_source_audit_e`。
- Actual model/version：`unknown`（当前上下文不可观察精确版本）。
- 隔离：`procedural_blinding`；没有技术 file allowlist，不作技术隔离声明。

## 1. 方法改变了哪一步计算：IR taxonomy 与 pipeline

- [AUTHOR_FACT] 作者把规划 pipeline 按到最终 plan 前经过的 IR 数量分级：Level 0 `I→L` 是 direct planner；Level 1 `I→PDDL⇝L`；Level 2 `I→IR→PDDL⇝L`；Level 3 再增加一个 IR。PDDL 本身计入 level。定位：物理 p3，§3 `Level 0...Level 4`；p5，Table 1。
- [AUTHOR_FACT] 被评估的 IR 包括自由/结构化自然语言、Python simulator、PyPDDL 和 PDDL；PDDL 作为中间 IR 时对应 revision。新引入的 pipeline 在 Table 1 以 † 标出，包括 PyPDDL/PythonSim 与不同 Level 3 排序。定位：p3–p5，§3/Table 1。
- [AUTHOR_FACT] Level 1 direct PDDL 用一次 LLM 生成完整 domain/problem PDDL，再交给 symbolic planner；Level 2/3 增加 LLM 转译或 revision 调用。定位：p3–p5；p39、p41–p44 prompts。
- [READER_INTERPRETATION] changed computation 不是“更换 solver”，而是在 solver 前重排表示与纠错阶段：先生成某种 IR，再由 LLM/规则转成 PDDL，或让 PDDL 经 solver feedback 修订。
- [READER_INTERPRETATION] taxonomy 是组织框架，不是复杂度定律。“更高 level”同时改变调用次数、prompt、上下文长度和可用反馈，不能单凭 level 数字归因机制。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 输入 triplet 为自然语言 domain description `Dd`、problem description `Dp` 和 ground-truth PDDL domain header `DF'_G`；header 给出 action names 与 parameter signatures，用来固定 ontology。定位：p2，§2，`input I... triplet`。
- [AUTHOR_FACT] 输出目标是 plan `L`；formalizer 先产生 predicted domain/problem PDDL，经 `dual-bfws-ffparser` 求解，最终 plan 用 VAL 对 ground-truth domain/problem PDDL 验证。定位：p2–p3，§2；p5，§4 Metrics。
- [READER_INTERPRETATION] `DF'_G` 是实质信息边界：系统不从纯自然语言或观察中发现 action ontology，而是在已知动作名称/参数接口下做 Spec-to-Code。作者也明确把 World-to-Code 排除。定位：p12，Appendix D。
- [AUTHOR_FACT] PyPDDL prompt 附带 wrapper 文档和 domain-agnostic example；PythonSim 只要求生成可执行 simulator，但本文仍把它当 IR，再转成 PDDL。定位：p3，§3 `Python simulator`/`PyPDDL`。
- [AUTHOR_FACT] 所有 IR→PDDL 的 LLM stage 都再次获得原始 domain/problem descriptions；NL、PythonSim、PyPDDL 和 PDDL revision prompts 均如此。定位：p41–p44，Figures 49、51、53、55、57、58。
- [READER_INTERPRETATION] 因第二阶段同时看到原始输入，PyPDDL/PythonSim 的增益不能解释为“模型只依据 IR 成功翻译”；第二调用可忽略、修复或重新生成 IR 内容。
- [AUTHOR_FACT] solver-feedback revision 把先前 PDDL 和 solver feedback 输入下一次 LLM；没有 feedback 的 PDDL revision 只靠 LLM 自身修订。定位：p4 `PDDL→*PDDL`；p43–p44。
- [READER_INTERPRETATION] solver feedback 主要暴露 parser/solver 的语法或可解性信号，不提供 ground-truth 语义差异。一个语法合法且可产生 plan、但错误建模环境的 PDDL 仍可能得不到直接诊断。

## 3. 最强基线与最近组合基线

- [AUTHOR_FACT] 资源约束的一调用对照是 Level 0 direct plan 与 Level 1 direct PDDL；8 个 model×domain 主文组合中没有明确赢家，作者概括为 3 对 5。定位：p6，§5.1。
- [AUTHOR_FACT] 直接 PDDL 是所有多阶段 formalizer 的最近单阶段基线；PDDL→PDDL（有/无 solver feedback）是最近 revision 对照；PyPDDL→PDDL 与 deterministic Py2PDDL 是最近“同 IR、不同 transpiler”对照。定位：p5 Table 1；p6–p7，§5.2。
- [AUTHOR_FACT] 为匹配两次 LLM response，作者增加 `PDDL best-of-2`：独立采样两个 Level 1 PDDL，只要任一产生 valid plan 就计成功，并与单次 revision 的 PDDL→PDDL 比较。定位：p7，§5.2.1；p9，Fig. 6。
- [AUTHOR_FACT] sequential generation 和 documentation retrieval 等 contemporaneous PDDL techniques 被明确列为 out of scope；监督训练方法也不纳入。定位：p4，§3 `I→PDDL`。
- [READER_INTERPRETATION] 因而“系统性覆盖 most prior work”只能按作者的 IR 抽象理解；实验并未与所有最近强 pipeline 做 matched numerical comparison。

## 4. 模型、预算、prompt、oracle 与 matched-comparison 边界

### 4.1 共同条件

- [AUTHOR_FACT] 模型为 QwQ-32B、Qwen3-32B、gpt-oss-120b（117B total/5.1B active）和 GLM-4.5-Air-FP8（106B total/12B active）；用 vLLM、单张 H100、默认 temperature 0.4，报告三次运行均值与标准差。定位：p5，§4 Models。
- [AUTHOR_FACT] 四个 benchmark 各 100 个 domain/problem tuples；主文重点是 moderately templated descriptions，Natural 版本只在两个模型、两个域和关键 pipelines 上补测。定位：p4，§4 Datasets；p12–p13，Appendix A/Fig. 7。
- [READER_INTERPRETATION] 模型、硬件和数据集在同图内大体一致，但 pipeline 的 LLM 调用次数、prompt bytes、输出长度和 solver-feedback 可见性不同；Level 2/3 结果不是严格等计算预算比较。

### 4.2 best-of-2 ablation 的能力与缺口

- [AUTHOR_FACT] PDDL best-of-2 与单 revision 都使用两次 LLM response；除 QwQ-32B/BlocksWorld 外，revision 在 Fig. 6 所有展示实例中胜过 best-of-2。作者据此认为增益不只来自额外 compute。定位：p7，§5.2.1；p9 Fig. 6。
- [AUTHOR_FACT] best-of-2 为鼓励多样性使用 temperature 0.8，而其他实验默认 0.4，并表现出更高 run variance。定位：p7。
- [READER_INTERPRETATION] 这是有价值但不完全 matched 的消融：response 数相同，temperature 与 prompt/feedback结构不同；而“任一候选 valid 即成功”是评价期 union oracle，实际部署若无 ground-truth validator 不一定能知道该选哪一个。该 oracle 反而偏向 best-of-2，因此 revision 胜出仍是支持结构价值的证据，但不能称完全成本/决策匹配。
- [READER_INTERPRETATION] Fig. 6 只直接隔离 PDDL→PDDL revision，不隔离 PyPDDL→PDDL。PyPDDL 的收益仍可能混有第二调用、重新读取原始描述与更长 prompt 的效应。
- [OPEN_QUESTION] 论文没有报告各 pipeline 的实际 input/output tokens、wall-clock、solver/tool calls 或推理成本，也没有给 Level 3 对应的 matched best-of-3 对照。

### 4.3 评价 oracle 与任务简化

- [AUTHOR_FACT] plan accuracy 使用 ground-truth PDDL/VAL 判断 plan 是否在真实环境中正确；syntactic accuracy 是 solver 未返回 syntax error 的比例。定位：p5，§4 Metrics。
- [READER_INTERPRETATION] ground-truth PDDL 用于离线 evaluator 是合理基准，但不能被描述成部署时可用的 solver feedback；revision prompt 看到的是 solver feedback，不是 VAL 对 ground-truth 模型给出的语义差异。
- [AUTHOR_FACT] CoinCollector 原本部分可观察，本文将其转换为完全可观察，以与其余域统一。定位：p4，§4 Datasets。
- [AUTHOR_FACT] Appendix D 承认 action header 令 benchmark 偏 solver-facing，并明确当前贡献只评估 Spec-to-Code、不是从 raw observations 推断 dynamics/ontology。定位：p12。
- [READER_INTERPRETATION] 因此结果不能外推到无 action schema、部分可观察或必须主动发现动力学的规划场景。

## 5. 主要结果与负结果

### 5.1 level 与 direct PDDL

- [AUTHOR_FACT] Level 3 的 PDDL→PDDL→PDDL 在主文 8 个 model×domain 组合中的 6 个获得最高 plan accuracy；最佳 Level 2 pipeline 在 8/8 中胜 Level 0 和 Level 1。定位：p5–p6，§5.1/Fig. 2。
- [AUTHOR_FACT] 一调用条件下 direct planner 与 direct PDDL 无清晰赢家。定位：p6，`3 against 5 in 8...`。
- [READER_INTERPRETATION] “multi-stage formalizer consistently beats planner”必须保留“最佳 Level 2、所测 8 个组合、更多调用”条件，不能改写成 direct PDDL 本身稳定胜 planner。

### 5.2 IR 选择、PyPDDL 与 PythonSim

- [AUTHOR_FACT] Level 2 中 NL IR 相对 Level 1 持续伤害性能；PythonSim 类似但偶尔改善；PyPDDL 与 PDDL revision 持续改善。定位：p6，§5.2/Fig. 3。
- [AUTHOR_FACT] PyPDDL→PDDL 与带 solver feedback 的 PDDL revision 在 8 个组合中各胜对方 4 次；无 solver feedback 的 PDDL→PDDL 丧失 revision 优势。定位：p6。
- [AUTHOR_FACT] deterministic Py2PDDL transpilation 显著差于 LLM transpilation；QwQ-32B/BlocksWorld 示例为 16% 对 68%。作者把错误归因于生成 PyPDDL 不遵循 library 的非平凡数据结构约定。定位：p6–p8，§5.2/Fig. 4。
- [READER_INTERPRETATION] 该结果不支持“生成 Python/PyPDDL 后直接执行即可可靠获得 PDDL”；相反，它显示代码样式相近不足以保证 library/API 契合，LLM 第二阶段可能承担容错重写。
- [AUTHOR_FACT] Appendix PythonSim 示例含 `from typing import ... frozenset`，且 frozen dataclass `State` 包含 `Dict` 后被加入 `visited` set；按展示代码逐字执行存在 import/hashability 风险。定位：p30–p33，Figures 34–37。
- [READER_INTERPRETATION] 这与“Python simulator 是直接可执行形式 IR”的理想定义存在可复现性缺口，但本文主 pipeline 不执行 simulator，而是让 LLM 转译，所以该代码缺口未必直接等同于主指标失败。
- [AUTHOR_FACT] PyPDDL Appendix 跨页后 `@action(Block, Block) def stack` 的可见缩进与类内其他方法不一致。定位：p34–p35，Figures 38–39。
- [OPEN_QUESTION] 无源代码执行记录，无法判断上述 Python/PyPDDL 附录问题是 PDF 排版丢失、示例生成错误，还是实际实验输入同样错误。

### 5.3 grammar-constrained decoding

- [AUTHOR_FACT] 作者把 PDDL 3.1 BNF 转成 LALR(1)-compatible EBNF，并用 constrained decoding 保证“trivially syntactically correct”输出，但承认可能损害语义。定位：p12，Appendix B。
- [AUTHOR_FACT] grammar decoding 在 BlocksWorld 与标准 direct PDDL 接近（38% vs 36%），在 Logistics 为 0；作者称其 hit-or-miss，并把全面评估留待未来。定位：p12。
- [READER_INTERPRETATION] 这是明确负结果：语法合法不等于 domain/problem 语义正确，硬 grammar 约束可把模型稳定推向同类语义错误，不能作为 formalization 的通用修复。

### 5.4 complexity robustness

- [AUTHOR_FACT] complexity study 用 BlocksWorld 10–50 blocks、每档 10 个问题；比较 direct planner、direct PDDL、PyPDDL→PDDL 和 PDDL→PDDL。定位：p8，§5.3/Fig. 5。
- [AUTHOR_FACT] 所有方法随复杂度退化；direct planner 约在 20 blocks 时相对 10 blocks 减半，接近 50 时为零；direct PDDL 从 10 到 50 的 plan accuracy 损失不超过 20%。Level 2 小规模更好，但复杂度增大时下降更严重。定位：p9，§5.3。
- [READER_INTERPRETATION] “formalizer 更 robust”不等于性能不下降，也不等于多 IR 越多越 robust；该实验反而显示 accuracy 峰值与复杂度鲁棒性存在 tradeoff。

## 6. 作者明示限制与未测试边界

- [AUTHOR_FACT] 只实例化到 Level 3；已有工作使用更多 IR，作者承认当前框架实例不足以覆盖所有 contemporary insights。定位：p9，§7 Limitations。
- [AUTHOR_FACT] 只研究 PDDL；LTL、SMT、ASP、action languages 只在讨论中列出，没有实验。定位：p4，§3 `Non-PDDL Planning Languages`；p9 Conclusion。
- [AUTHOR_FACT] sequential generation、documentation retrieval 和 supervised training 不在实验范围。定位：p4。
- [AUTHOR_FACT] constrained decoding 只做有限补充实验，作者明确 defer comprehensive evaluation。定位：p12。
- [AUTHOR_FACT] Natural descriptions 只在两个模型、两个域、关键 pipelines 上验证。定位：p4、p12–p13。
- [AUTHOR_FACT] complexity stress test 仅 BlocksWorld，且 action ontology/header 仍给定。定位：p8、p12。
- [READER_INTERPRETATION] 未测试边界还包括真实长程/交互式执行、未知 ontology、部分可观察 dynamics、部署期无 ground-truth validator，以及不同 token/cost 预算下的 Pareto 前沿。

## 7. 可抽取的 Operator 候选

- [READER_INTERPRETATION] **IR-level pipeline decomposition**：把 formalization 显式分为 `I→IR→PDDL→solver`，并以 level/IR 类型描述 changed computation。证据：p3–p5。
- [READER_INTERPRETATION] **Syntax-aligned high-resource IR**：用 PyPDDL 作为 Python/PDDL 之间的形式 wrapper，再由 LLM或确定性工具转 PDDL。必须同时记录 deterministic transpiler 的负结果。证据：p3、p6–p8。
- [READER_INTERPRETATION] **Solver-feedback PDDL revision**：把上一版 PDDL 与 solver feedback重新交给 LLM修订；无 solver feedback 时优势消失。证据：p4、p6、p43–p44。
- [READER_INTERPRETATION] **Compute-matched structure ablation**：以同 response 数的 independent best-of-k 对照结构化 revision，用于区分“多调用”与“中间结构”。当前实现需保留 temperature/oracle 不完全匹配边界。证据：p7、p9。
- [READER_INTERPRETATION] **Grammar-constrained PDDL decoding** 不宜作为正向 Operator；当前证据应主要沉淀为 Failure，因为跨域表现灾难性不稳。证据：p12。

## 8. 可记录的 Failure 候选

- [AUTHOR_FACT] **Single-call formalization fragility**：最佳 Level 2 在 8/8 胜 Level 0/1；direct PDDL 与 planner 本身无明确赢家。定位：p6。
- [AUTHOR_FACT] **Distant NL IR hurts**：NL→PDDL 持续低于 direct PDDL。定位：p6。
- [AUTHOR_FACT] **Self-revision without external feedback loses advantage**：PDDL→PDDL 无 solver feedback 时不再体现 revision 优势。定位：p6。
- [AUTHOR_FACT] **Generated wrapper violates library conventions**：Py2PDDL deterministic route在示例组合 16% 对 LLM-transpile 68%，典型错误是把 `create_objs` 的对象集合当错误的数据结构访问。定位：p7–p8，Fig. 4。
- [AUTHOR_FACT] **Grammar legality can destroy semantics**：constrained decoding 在 Logistics 为零。定位：p12。
- [AUTHOR_FACT] **More IR can reduce robustness**：Level 2 小规模更强但复杂度增长时比 direct PDDL 退化更严重。定位：p9。
- [READER_INTERPRETATION] **IR attribution confound**：第二阶段持续看到原始描述；没有 IR-only 或 information-ablation 对照，故无法证明下游真正使用了 IR。
- [READER_INTERPRETATION] **Evaluation-feedback gap**：solver feedback不能发现所有语义错模；plan correctness需要 ground-truth environment validator，而该信息不进入 deployment-time revision。
- [AUTHOR_FACT] 摘要/引言末尾有一句称关键 pipeline“consistently outperforms LLM-as-formalizer”，与全文实际比较“最佳多阶段 formalizer胜 direct planner和 Level 1 formalizer”表述不一致。定位：p2 首栏末段；p6 §5.1。
- [READER_INTERPRETATION] 该句应视为论文文字错误，不能据此建立“formalizer 胜 formalizer”的事实。

## 9. 解析文本与可视 PDF

- [AUTHOR_FACT] PyMuPDF 对 44/44 物理页均抽取到非空文本；图像对象见 p1 与 p8。Table 1、Figures 1–58、正文和附录 prompts/code 均有页级定位。
- [READER_INTERPRETATION] p2、p5–p9、p14–p15 等双栏/密集图页的排序文本存在交错；本报告的数值只采用正文明确陈述、图注或可辨认表格文字，不从不可可靠解析的柱高臆测数值。
- [OPEN_QUESTION] 写入只允许 `report.md`，未生成临时 raster 页图；当前线程无可用像素级 PDF 视觉通道。因此不能声称完成逐像素图表核验。未发现抽取文字与图注/正文之间的实质冲突，但 Fig. 2/3/5/7–9 的精确柱高仍应由后续具备视觉通道者复核。

## 10. 总体二读结论

- [READER_INTERPRETATION] P060 最强的可复用结论不是“IR 越多越好”，而是：在给定 action header 的 Spec-to-Code 任务上，多阶段、syntax-aligned IR 或有 solver feedback 的 revision，常比单调用 direct PDDL 更可靠；但不同 IR、反馈与计算预算必须分开。
- [READER_INTERPRETATION] PyPDDL 的 LLM-transpile 结果有价值，但 deterministic Py2PDDL 失败、附录代码风险、第二阶段重复看到原始输入，共同阻止把增益直接归因于“可执行 Python wrapper 本身”。
- [READER_INTERPRETATION] matched best-of-2 支持 revision 结构不只是额外一次采样，但只覆盖两响应 PDDL revision，且 temperature、选择 oracle、tokens 和 Level 3 都未完全匹配。
- [READER_INTERPRETATION] 必须保留真实负结果：NL IR 持续有害、无 solver feedback 的自修订无优势、grammar decoding 在 Logistics 为零、所有方法随复杂度下降、更多 IR 的鲁棒性可能更差。

## 11. 可观察访问轨迹

1. 精确复核必要规则：工作区根 `AGENTS.md`、`crl_agent_v3/AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`；`paper-ingestion-and-evidence-builder/SKILL.md` 及其直接要求的三个 references。
2. 只读本 attempt `invocation.md`；统一 prompt 仅使用 invocation 内冻结 bytes，未读取单独模板文件。
3. 只读 invocation 指定 `P060_unifying_planning_language.pdf`；校验 SHA-256，使用受支持 `.venv` 的 PyMuPDF读取 metadata、物理页 1–44 全文，并逐页统计字符数与图像对象数。
4. 未枚举工作区；未读取 read_1、Cards、其他读者报告、其他论文读稿、Corpus Report、saturation/retrieval/blind 文件；未联网、未调用外部 API。
5. 写入仅通过 `apply_patch` 新建本 attempt 的 `report.md`；未修改其他文件。
