# P051 independent read-3 report

## Provenance 与访问披露

- Attempt：`r3-20260720-p051-a1`；本报告引用同目录 `invocation.md` 的冻结请求。
- 核验原文：`knowledge_base/staging/papers/P051_formal_verification_planning.pdf`，50 个物理页；实测 SHA-256 为 `ba9261d6d8fbf2b43817e57c29aa6ffacc0b14ef038e6c86a33f8780490bd365`，与 invocation 一致。
- 统一提示：`knowledge_base/templates/second_read_prompt.md`；invocation 记录的 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。
- 阅读方式：逐物理页读取 PDF 内嵌文本层；另以内存渲染核对物理页 7 的四张结果表与物理页 16 的时间/成本表，未创建临时文件。所核关键表格的视觉内容与抽取数字未见冲突；其余页面未逐页像素渲染，因此复杂版面是否存在未被文本层保留的信息仍是 `[OPEN_QUESTION]`。
- 访问边界：`procedural_blinding`，不是技术文件级隔离。实际仅访问本 PDF、本 attempt 的 invocation、统一 prompt，以及必要的 AGENTS/CRL/技能指令；未联网，未读取 read_1/read_2、Cards、Evidence、reconciliation、audit、corpus report 或 blind 文件。
- 可观察工具轨迹：本地 SHA-256；PyMuPDF 1.28.0 页数、文本抽取与内存栅格化；写入仅为本文件。实际模型/version 与宿主 thread ID 对本读者不可见，记为 `unknown`；可见 agent task 为 `/root/plan05_p051_p052_third_reader`。

## 1. 方法改变的计算、输入输出与干预时点

- `[AUTHOR_FACT]` 方法把直接生成旅行计划改成四段计算：LLM 先把自然语言查询转成约束步骤，再把步骤转成 Python/Z3 代码，执行 SMT/Optimize，最后把求解结果解析成自然语言计划；不可满足时再基于 unsat core、信息检索和用户反馈修改约束/代码。定位：物理页 3，Figure 1；物理页 4，§3.2；物理页 5，§3.3.3–3.4。短定位：`Query to Steps`、`Steps to Codes`、`get_unsat_core`。
- `[AUTHOR_FACT]` 输入并非只有终端用户查询：Query-Step 使用 3 个手工 TravelPlanner 示例；Step-Code 示例覆盖“几乎全部”示例步骤，足以示范 API 与 SMT 调用而无需另给 API 文档。定位：物理页 4–5，§3.3.1–3.3.2；完整 prompt 位于物理页 24–34，Appendix G.1。短定位：`three human-crafted examples`、`cover almost all`。
- `[AUTHOR_FACT]` 作者在 TravelPlanner 训练集上选择 3 个示例并用其他训练查询调 prompt；不同模型还接受不同解释、示例和禁用写法。定位：物理页 6，§5.1 Implementation；物理页 34，§G.1.3。短定位：`tune the prompt`、`add more explanations or examples`。
- `[READER_INTERPRETATION]` 主要 Operator 是“让 LLM 生成可执行形式化模型，再把组合搜索交给 solver”；真正的干预发生在 solver 之前的语义抽取/代码生成，以及 unsat 后的约束修订。它不是 solver 对原始自然语言直接作证明。

## 2. Formalization fidelity 与 solver guarantee

- `[AUTHOR_FACT]` 论文称 SMT solver sound and complete，因而在“constraints are satisfiable”时保证找到解，并把输出称为 formally verified plan。定位：物理页 2，§1；物理页 5，§3.3.3。短定位：`guarantees to find a solution if there exists one`。
- `[READER_INTERPRETATION]` 该保证只对“生成代码实际编码出的约束系统”成立；它不覆盖 NL→步骤、步骤→代码是否忠实、是否漏掉隐含约束、API 数据是否正确，也不覆盖达到 30 分钟截止前能否完成。论文自己的非满分通过率与代码失败例支持这一边界：TravelPlanner 最佳 test final pass 为 93.9%，新任务出现漏掉 distinct、API 参数错误、站点 ID/索引混淆。定位：物理页 7，Table 1；物理页 23，§F.3。
- `[AUTHOR_FACT]` 代码示例实际初始化 `Optimize()`，而正文多处笼统称 SMT solver；TravelPlanner 目标主要是满足全部约束，四个新任务还评价 optimal rate。定位：物理页 30，Appendix G.1.2；物理页 7，Tables 1–2。
- `[OPEN_QUESTION]` 原文没有给出独立的 formalization-fidelity 检查器、NL 规范与生成代码的等价性证明、或人工逐约束编码审计率；因此无法从 solver 的 soundness/completeness 推出端到端语义保证。
- `[OPEN_QUESTION]` 原文未说明 Z3 返回 `unknown`、Optimize 未证最优、异常退出与 30 分钟超时在评测脚本中如何严格区分；“complete”表述没有显式附带资源无界条件。

## 3. TravelPlanner 基线、模型与预算公平性

- `[AUTHOR_FACT]` 主表比较 Greedy Search、TwoStage(GPT-4)、Direct(GPT-4)、validation-only Direct(o1-preview)，以及 Ours 的 Mistral-Large、Claude-3、GPT-4；test 表没有 o1-preview。定位：物理页 6，§5.1 Baselines；物理页 7，Table 1。
- `[AUTHOR_FACT]` 正文称 LLM-Modulo 是当时最强工具框架，GPT-4-Turbo/o1-preview 分别达 20%/65%，但 Table 1 未把 LLM-Modulo 纳入同表重跑。定位：物理页 1–2，Introduction；物理页 7，Table 1。
- `[AUTHOR_FACT]` 作者为“输入公平”移除了 Ours 的额外 NL→JSON 阶段，因为基线只有自然语言输入；加回 JSON 后 validation/test 还能进一步提高。定位：物理页 4，§3.3.1；物理页 6，§5.1；物理页 19，Table 8。
- `[READER_INTERPRETATION]` 这只匹配了输入表示的一项，并未匹配计算预算。Ours 使用多个 LLM 阶段、按约束类型的多次 Step-Code 调用、长手工示例、Z3 最长 30 分钟；Direct 是预收集信息后的直接生成，TwoStage 是另一工具流程。Table 1 因而证明各“系统配置”的效果差异，不隔离 formalization 本身在等 call/token/time/oracle 条件下的因果增益。
- `[OPEN_QUESTION]` 原文没有报告各方法相同的 LLM call 数、输入/输出 token、API/tool-call 数、solver wall-clock 上限、重试数或美元预算，也没有同一基础模型、同一 token/call/tool 预算的 LLM-Modulo 对照。
- `[OPEN_QUESTION]` o1-preview 因运行时间长未用于 TwoStage 或 Ours，Claude-3 的 Ours 与 GPT-4/o1-preview 基线属于跨模型比较；不能据此把全部差距唯一归因于形式化机制。定位：物理页 6，§5.1 Baselines。

## 4. 人工 prompt/API 成本与运行成本

- `[AUTHOR_FACT]` 作者明确承认从头设计 instruction steps 与对应代码“time-consuming”；终端用户只需自然语言，但这把成本转移到离线系统设计者。定位：物理页 9，§7 Prompt Designing。
- `[AUTHOR_FACT]` 完整 Query-Step prompt 占物理页 24–29，含 3 个详细 TravelPlanner 示例；Step-Code prompt 占物理页 29–34，逐类示范 City/Date/Transportation/Flight/Driving/Restaurant/Attraction/Accommodation/Budget 的 API 与 Z3 代码。交互修复还另有 4/6 个检索 API、允许修改字段、最小修改规则和 15-iteration 指令。定位：物理页 35–41，§G.2。
- `[AUTHOR_FACT]` GPT-4 在 180 个 validation 查询上的平均 API 成本为每题 `$0.74`；179 个交付查询平均总耗时 `245.66s`，其中 LLM Step-Code `166.66s`、SMT `38.39s`。交互修复成功子集的平均成本为每轮 `$0.65`，平均 `33.68s/iteration`，硬预算模拟用户平均 2.22 轮。定位：物理页 16，§B.1–B.2，Tables 6–7。
- `[READER_INTERPRETATION]` 这些数字量化了线上 API/时延，却没有量化 3 个示例、近全 API/solver 代码示范、训练集 prompt 调整和模型特定补丁的人工小时；“end-user autonomy”不等于“task engineering cost 为零”。

## 5. 超时、形式化失败与负向边界

- `[AUTHOR_FACT]` 每题 solver 上限 30 分钟。Limitations 称 1180 题中 1.3% 因超过该上限找不到计划；Appendix B 对 validation 另报告 180 题中 1 题超时。定位：物理页 6，§5；物理页 9，§7 Solver Runtime；物理页 16，§B.1。
- `[OPEN_QUESTION]` 论文未在同一张分解表中说明 1.3% 对 validation/test 的具体计数，也未把 delivery failure 细分为 solver timeout、LLM 代码错误、API 错误和其他 runtime error。Table 1 的未交付比例明显依模型而变。定位：物理页 7，Table 1。
- `[AUTHOR_FACT]` Mistral-Large 对训练示例未覆盖的 `no shared room` 产生错误形式化，另有 runtime 与偶发代码生成错误；模型需要额外示例并被要求不要用循环/索引变量。定位：物理页 34，§G.1.3–G.1.4。
- `[AUTHOR_FACT]` 跨任务失败直接包括：Block Picking 漏掉 all-different 导致重复取高分块；Task Allocation 错调 `Max` 引发 runtime error；Warehouse 把站点 ID 当列表索引、或同时把首尾变量设为 origin，导致非最优或冲突。定位：物理页 22–23，§F.3。
- `[AUTHOR_FACT]` 数据库本身可能不安全或不正确，系统不能识别；更大数据库、更多约束、极少可行解时 solver 可能很慢。定位：物理页 9，§7 Risky Data / Solver Runtime。

## 6. 可复用机制与可记录失败（仅本次阅读层）

- `[READER_INTERPRETATION]` 可复用机制：把结构化 decision variables、显式约束、目标、外部数据 API 和 solver 调用组成可执行形式化；unsat core 可作为交互修复的定位信号。依据：物理页 3–5，Figure 1 与 §3.2–3.4。
- `[READER_INTERPRETATION]` 可记录失败：语义漏约束、值域/索引混淆、模型特定 prompt 脆弱、生成代码 runtime error、solver timeout、错误数据库被形式化后仍会被“严格”求解。依据：物理页 9、22–23、34。
- `[OPEN_QUESTION]` unsat core 只解释已编码约束；若自然语言要求被漏掉或误译，它不能暴露该遗漏。论文没有测该类“错误形式化但 solver 成功”的独立发生率。

## 7. 逐页覆盖摘要与非裁决声明

- 物理页 1–9：摘要、方法、数据、主实验、交互修复、限制；物理页 10–12：参考文献；物理页 13–14：目录。
- 物理页 15–23：约束清单、成本/时延、示例输出、附加指标、迭代曲线、新任务定义与失败分析。
- 物理页 24–34：完整 satisfiable-planning prompts、代码示例、模型特定改动与失败；物理页 35–41：交互修复/消融 prompts；物理页 42–50：新约束说明、paraphrase 示例及完整 unseen-constraint 输出步骤。
- 本报告只做独立核源与边界解释，不作论文准入、Card 写入、Candidate 评价或最终科研裁决。
