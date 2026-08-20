# P004 fresh independent read-2 report

## 0. 读取身份、范围与来源

- 本报告对应 frozen invocation：`r2-20260719-p004-a1`，canonical task 为 `/root/p004_second_read`；invocation 文件 SHA-256 为 `dd6942d62c3d0b2defd402c121af42c461de0bd556c679953ef937c6cbe80f20`。
- [AUTHOR_FACT] 论文为 **TravelPlanner: A Benchmark for Real-World Planning with Language Agents**，PMLR 235 / ICML 2024；PDF 共 24 页。定位：PDF p.1，标题、作者与页脚 “Proceedings of the 41st International Conference on Machine Learning”。
- [AUTHOR_FACT] PDF SHA-256 实测为 `a7c7edd67c90e9997e940aaa7b435d46a8b201ed119c125b341b01b215454133`，与 invocation 一致；`second_read_prompt.md` SHA-256 实测为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，与 invocation 一致。
- [READER_INTERPRETATION] 本文的主要贡献是一个任务、环境、数据集与评测管线，不是一个新的可训练规划方法。因此下文“改变哪一步计算”按基准对被测 agent 的输入—交互—输出—判定链条来回答。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] TravelPlanner 把以往“单目标、固定 ground truth、预定义动作集”的规划评测，改成部分可观测的真实旅行场景：agent 先调用工具收集信息，再生成满足多类约束的完整行程。定位：PDF p.1，§1，短定位 “single-objective optimization with fixed ground truths”；PDF p.2，Figure 1 与其后正文 “partially observable environment”；PDF p.3，§3.1。
- [AUTHOR_FACT] 评测计算链为：自然语言计划 → 抽取 transportation / restaurants / attractions / accommodations 等关键字段 → 结构化计划 → 预定义脚本检查。作者明确用 GPT-4-Turbo 完成关键字段抽取。定位：PDF p.5，§3.4，脚注 1，短定位 “use GPT-4-Turbo for this extraction process”；抽取 prompt 见 PDF pp.17–18，§B.3.5。
- [AUTHOR_FACT] 计划判定由 Delivery Rate、Commonsense Constraint Pass Rate、Hard Constraint Pass Rate、Final Pass Rate 构成；commonsense 与 hard constraint 又分别计算 micro 与 macro，公式 (1)–(2) 给出聚合方式。定位：PDF p.5，§3.4，公式 (1)、(2)。
- [AUTHOR_FACT] 除完整 two-stage 设置外，作者增加 sole-planning 消融：用人工标注计划预先确定目的城市，并直接给 agent 详细且必要的信息，从而移除工具调用。定位：PDF p.6，§3.5，短定位 “human-annotated plans to pre-determine the destination cities”。
- [READER_INTERPRETATION] 因而真正改变的不是 LLM 内部推理公式，而是三处外部计算：①任务状态从全给定变为经工具暴露；②目标从单一正确答案变为多约束可行性；③自然语言输出先经 LLM parser 再由脚本判定。该链条把信息获取、记忆、规划和评测解析器共同纳入最终分数。
- [OPEN_QUESTION] 论文未报告 GPT-4-Turbo 抽取器相对人工结构化结果的准确率，也未说明抽取失败如何计入各项 constraint pass rate；因此无法由原文分离“规划错误”与“评测解析错误”。定位：PDF p.5 脚注 1、pp.17–18 §B.3.5；原文只给 prompt，未见 parser 验证实验。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 输入 query 由出发城市、目的地/州、日期、3/5/7 天、人数、预算及若干 hard constraints 组成；难度 Easy/Medium/Hard 对应预算，以及逐步加入 cuisine、room type、room rule、transportation preference。定位：PDF pp.4–5，§3.3 “Query Construction”；生成 prompt 见 p.17，§B.3.4。
- [AUTHOR_FACT] 输出是逐日完整行程，至少覆盖 current city、transportation、breakfast、attraction、lunch、dinner、accommodation，并须满足环境、commonsense 与 hard constraints。定位：PDF p.2，Figure 1；PDF p.4，Table 1；PDF pp.15–18，§B.3.2–B.3.5。
- [AUTHOR_FACT] two-stage 可用信息来自静态闭合 sandbox 中六个搜索工具：CitySearch、FlightSearch、DistanceMatrix、RestaurantSearch、AttractionSearch、AccommodationSearch；NotebookWrite 保存被选条目，只有写入 Notebook 的信息可交给 Planner。定位：PDF p.4，Table 2 与 §3.3 “Environment Setting”；PDF p.12，Table A.2；PDF pp.14–15，§B.3.1，短定位 “Only the data stored in Notebook can be seen by Planner”。
- [AUTHOR_FACT] 环境约束在每次搜索调用后以无结果/可用结果反馈；信息收集最多 30 步，三次连续失败或重复动作触发 early stop。定位：PDF p.3，§3.2；PDF p.5，§3.4 “30 steps”；PDF p.7，Figure 2 图注。
- [AUTHOR_FACT] planning 阶段的干预包括：Direct 直接生成；ZS-CoT 增加 “Let’s think step by step”；ReAct 交替 Thought/Action/Observation 并提供每日整段计划的 CostEnquiry；Reflexion 再由 reflection model 对此前错误尝试给高层反馈。定位：PDF p.13，§B.1 “Planning Strategy”；具体 prompts 见 pp.15–17，§B.3.2–B.3.3。
- [READER_INTERPRETATION] 可观察干预时点依次是：query 合成与预算回标 → 工具选择/参数化 → Notebook 记忆写入 → Planner 生成 → GPT-4-Turbo 字段抽取 → 脚本约束检查。sole-planning 在第二、三步之前注入人工选定城市和“必要信息”，因此它不是仅关闭 tool-call 的轻量消融，而是改变了 agent 可用信息的质量与覆盖率。
- [OPEN_QUESTION] “detailed and necessary information” 的精确选择规则、信息量/token 数、排序方式及是否对各模型完全相同，正文未量化。定位：PDF p.6，§3.5。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 以 Final Pass Rate 为主，Table 3 中最强结果是 sole-planning 的 Direct GPT-4-Turbo：validation 4.4%，test 4.4%；完整 two-stage 中最强是 GPT-4-Turbo + ReAct，validation/test 均为 0.6%。定位：PDF p.6，Table 3。
- [AUTHOR_FACT] rule-based Greedy Search 的 Final Pass Rate 为 0%，但 test hard-constraint micro/macro 为 52.4%/31.8%，后者高于 Direct GPT-4-Turbo 的 44.3%/23.1%；因此不同指标下不存在单一支配者。定位：PDF p.6，Table 3；greedy 细节见 p.13，§B.1。
- [AUTHOR_FACT] 同为 GPT-4-Turbo、同为 sole-planning 的 Reflexion 补充实验在 validation 上 Final Pass Rate 为 3.3%，低于 Direct GPT-4-Turbo 的 4.4%；但其 hard-constraint micro/macro 为 52.4%/40.0%，高于 Direct 的 47.1%/22.2。定位：PDF p.14，Table B.3；对照 p.6，Table 3。
- [READER_INTERPRETATION] 与本文完整任务最接近的“组合基线”是 two-stage ReAct + GPT-4-Turbo，因为它同时经历工具交互和最终规划；与纯规划能力最接近的是 sole-planning Direct GPT-4-Turbo。Greedy Search 是成本优化规则基线，但不是 LLM+搜索的混合规划器。
- [OPEN_QUESTION] 论文没有评测“LLM 负责语言/约束解析 + 显式搜索或约束求解器负责可行性”的真正组合基线，也未将 greedy 的候选生成与 LLM 的自然语言规划组合；因此无法判断 0.6%/4.4% 相比更接近任务结构的 neuro-symbolic 或 solver-backed baseline 有多大差距。定位：PDF p.6 §4.1、Table 3；p.13 §B.1。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] two-stage 中作者统一采用 ReAct 工具框架、改变 foundation LLM；候选模型限定为可处理超过 8K 输入者，并使用各自官方 instruction format。定位：PDF p.6，§4 与 §4.1。
- [AUTHOR_FACT] 所有实验为 zero-shot；最大信息收集步数是 30。定位：PDF p.6，§4 末句；PDF p.5，§3.4。
- [READER_INTERPRETATION] **模型差异可解释部分结果。** Table 3 的跨模型比较不是仅比较 planner 能力，还同时改变模型规模、训练、上下文实现和官方 instruction format；论文没有等 token 或等推理成本控制。
- [AUTHOR_FACT] 除 Direct 外，主要 planning strategy 实验用 GPT-3.5-Turbo，理由是控制成本；GPT-4-Turbo + Reflexion 仅在 validation 补充。定位：PDF p.13，§B.1，短定位 “other strategies are evaluated using GPT-3.5-Turbo”；p.14 Table B.3。
- [READER_INTERPRETATION] **策略比较受交互预算和 prompt 结构影响。** Direct、ZS-CoT、ReAct、Reflexion 获得的额外 thought/action/feedback 不同；ReAct/Reflexion 使用 CostEnquiry，Direct 不使用。论文给了 prompt，但未给每种策略的平均 token、调用次数、延迟或美元成本，故不能把差异纯归因于“规划策略”。定位：PDF p.13 §B.1；pp.15–17 §B.3.2–B.3.3。
- [AUTHOR_FACT] sole-planning 直接提供人工标注计划所确定的目的城市和必要信息；two-stage 必须自己调用工具并把条目写入 Notebook。定位：PDF p.6，§3.5；p.14 §B.3.1。
- [READER_INTERPRETATION] **mode gap 含 oracle/info-quality 差异。** p.7 将两种模式差距解释为同时处理 information collection 与 planning 的困难，但 sole-planning 还获得人工筛选的信息与城市，因此“最大超过 30%”不能单独识别 multitasking/cognitive-capacity 的因果效应。定位：PDF p.7，§4.2 “largest gap reaching over 30%”。
- [READER_INTERPRETATION] **评测器也引入模型差异。** 所有自然语言计划经 GPT-4-Turbo 解析后才脚本评分；若被测模型输出风格与 parser prompt 的示例格式匹配程度不同，得分可能包含格式可解析性差异，而非只含计划可行性。定位：PDF p.5 脚注 1；pp.17–18 §B.3.5。
- [AUTHOR_FACT] 数据并非完整保留现实语义：餐馆被随机分配到城市并随机赋 cuisine，住宿被随机分配并随机赋 room rules；Flight price 用 distance 乘随机因子，taxi/self-driving 价格亦为公式生成。定位：PDF pp.12–13，§A.3。
- [READER_INTERPRETATION] **随机数据构造可能改变任务性质。** 分数更直接衡量对该闭合 sandbox 的检索、记忆和约束一致性，而不等同于对真实旅行市场的常识规划能力。
- [OPEN_QUESTION] 原文未报告随机种子、多次运行方差、采样参数、每个模型的确切 token 使用、工具调用预算是否除统一 30 步外完全相等、API 模型快照日期，也未给显著性区间。定位：PDF pp.6–8 §4–§5；附录 prompts pp.14–18，未见这些项目。

## 5. 明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 核心负向结果：完整 two-stage 中 GPT-4-Turbo 最终通过率仅 0.6%，其他模型为 0%；即使给全信息，现有策略仍难完成多约束计划。定位：PDF p.2，§1 主要发现；p.6 Table 3；pp.6–7 §4.2。
- [AUTHOR_FACT] 作者明示未测试 ToT 与 GoT，理由是复杂搜索空间下成本过高，且作者预期其复杂任务收益有限。定位：PDF p.6，§4.1 “We do not include ToT and GoT”。
- [AUTHOR_FACT] 作者仅考虑上下文能力超过 8K 的模型，并全部采用 zero-shot；这排除了短上下文模型、训练/微调与基于 feedback 的学习。定位：PDF p.6，§4、§4.1。
- [AUTHOR_FACT] 作者承认“commonsense”定义因人而异，目前标准基于作者共识，鼓励扩展维度。定位：PDF p.9，Impact Statement，短定位 “everyone’s definition of commonsense may be different”。
- [AUTHOR_FACT] 环境约束没有单独计分，作者认为其影响已反映在 Within Sandbox 与 Complete Information。定位：PDF p.5，§3.4。
- [AUTHOR_FACT] sandbox 是静态、闭合环境；FlightSearch 只取 2022-03-01 至 2022-04-01 的数据。定位：PDF p.4，§3.3 “static and closed sandbox”；p.12，§A.3。
- [AUTHOR_FACT] 人工计划由 20 名研究生标注，作者逐条检查并按人工计划成本重新校准预算；每个 query 至少有一个可行解，但未声称穷举所有解。定位：PDF p.5，§3.3 “Human Annotation” 与 “Quality Control”。
- [READER_INTERPRETATION] 未测试边界包括：动态价格/库存、开放网络信息、超出该时间窗与城市集合的泛化、非旅行任务、few-shot/训练后 agent、明确 backtracking/constraint solver、人与 agent 协作，以及 parser 的人工复核。原文对这些没有结果，不能外推。
- [OPEN_QUESTION] 没有独立人类成功率/错误率基线；“人工平均 12 分钟”只报告标注耗时，不能用来建立 agent-vs-human 可行性差距。定位：PDF p.6，Table 3 图注。

## 6. 可抽取的 Operator 与真实记录的 Failure

### 6.1 可抽取为 Operator 的内容

- [READER_INTERPRETATION] **Tool-grounded information collection operator**：按 query 主动选择搜索工具、读取环境反馈，并把后续规划所需条目写入 Notebook。定位：PDF p.2 Figure 1；p.4 §3.3；pp.14–15 §B.3.1。
- [READER_INTERPRETATION] **Memory bottleneck / Notebook operator**：只允许 Planner 看见被 NotebookWrite 选中的信息，用显式工作记忆限制替代无限上下文堆积。定位：PDF p.4 §3.3；p.14 §B.3.1。
- [READER_INTERPRETATION] **Oracle-information ablation operator**：以人工标注计划确定城市并直接提供必要信息，隔离（但不纯粹识别）planning 与 information collection。定位：PDF p.6 §3.5。
- [READER_INTERPRETATION] **Plan normalization operator**：用 GPT-4-Turbo 把自然语言计划抽成固定 JSON schema，再由确定性约束脚本核验。定位：PDF p.5 §3.4；pp.17–18 §B.3.5。
- [READER_INTERPRETATION] **Constraint-wise micro/macro verifier**：逐约束计分与整计划全约束通过两种聚合并存，避免高平均通过率掩盖“一项失败即不可行”。定位：PDF p.5，公式 (1)–(2)。
- [READER_INTERPRETATION] **Cost-feedback and reflective revision operator**：CostEnquiry 为完整单日子计划提供环境成本，Reflexion 追加高层错误反馈。定位：PDF p.13 §B.1；pp.16–17 §B.3.3。

### 6.2 作者实际观察并可定位的 Failure

- [AUTHOR_FACT] 工具阶段的真实错误类型包括 Max Step Limit、Argument Error、Invalid Action Dead Loop、Same Action Dead Loop；GPT-4-Turbo 的 invalid-action 与 same-action dead-loop 占其工具错误 37.3% 与 6.0%。定位：PDF p.7，Figure 2 与 §5.1。
- [AUTHOR_FACT] agent 工具调用/写入 Notebook 的数量低于 reference，且行程越长差距更明显，导致信息不全、虚构或遗漏。定位：PDF p.7，Table 5；PDF p.8，§5.2。
- [AUTHOR_FACT] 多约束整体失败：micro 尚可而 macro 很低；Budget 与 Minimum Nights Stay 等全局约束尤弱。定位：PDF p.7，§4.2 与 Table 4；PDF p.8，§5.2 “global planning scenarios”。
- [AUTHOR_FACT] 日期固着/不能自纠：2022 query 被持续用 2023 日期搜索，最终无结果或直接规划。定位：PDF p.8，Figure 3 左与 §5.3；PDF p.21，Figure C.2。
- [AUTHOR_FACT] 信息混淆导致 hallucination：在 sole-planning 中把同一航班号用于去程和返程。定位：PDF p.8，Figure 3 中与 §5.3。
- [AUTHOR_FACT] reasoning-action disconnect：Reflexion 口头要求降低成本，实际随机换到可能更贵的条目。定位：PDF p.8，Figure 3 右与 §5.3；更完整成本失败见 p.24，Figure C.7。
- [AUTHOR_FACT] 其他可复核实例包括：未形成往返闭环且漏餐/住宿（p.21 Figure C.1）、返程早班机后仍在出发城市安排活动（p.22 Figure C.3）、重复餐馆（p.22 Figure C.4）、违反儿童/最少住宿夜数（p.23 Figure C.5）。
- [READER_INTERPRETATION] 上述 failure 是作者在数据/轨迹中实际展示的错误，不应扩大为“所有 LLM 必然如此”；Figure 2 的百分比是错误分布而不是每个任务发生率。

## 7. 位置索引与关键短定位文本

以下索引汇总前述判断的主要核源点；各条已经在对应问题下给出标签。

| PDF 页 | 章节/图表 | 短定位文本或对象 | 支撑内容 |
|---:|---|---|---|
| 1–2 | Abstract, §1, Figure 1 | “1225… intents”, “six tools”, “partially observable” | 基准目标、规模、两阶段流程 |
| 3–4 | §3.1–3.3, Table 1–2 | “three types of constraints”, “static and closed sandbox” | 约束类型、环境、工具 |
| 5 | §3.3–3.4, Eq. (1)–(2) | “GPT-4-Turbo for this extraction process” | 标注、解析器、指标 |
| 6 | §3.5–4.2, Table 3 | “human-annotated plans…”, “zero-shot” | sole-planning、基线与主结果 |
| 7 | Figure 2, Table 4–5, §5.1–5.2 | “three consecutive failed attempts” | 工具错误、逐约束表现、工具数量 |
| 8 | Figure 3, §5.2–5.3 | “incorrect dates”, “information confusion”, “align… reasoning” | 三类核心失败机制 |
| 9 | Impact Statement | “definition of commonsense may be different” | 作者明示主观边界 |
| 12–13 | §A.2–A.3, §B.1 | “randomly assign”, “control the cost” | 数据合成、策略实现与模型混杂 |
| 14–18 | §B.3.1–B.3.5 | Tool-use / planning / extraction prompts | prompt 与信息流复核 |
| 19–20 | §C.1 | annotated plan | 人工 reference 示例 |
| 21–24 | Figure C.1–C.7 | case analyses | 额外真实失败与一个 feasible case |

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 已对 PDF 1–24 页逐页提取文本，并把 1–6、7–12、13–18、19–24 四组页面以内存 contact sheet 方式逐页视觉核对；未发现会改变实验数字、章节归属或本文主要判断的“解析文本—可视页面”实质冲突。
- [READER_INTERPRETATION] 文本层会丢失二维布局：p.2 Figure 1 的流程图被线性化；p.6 Table 3、p.7 Figure 2/Table 4–5 的列与百分比关联必须依赖可视表格/图形复核；pp.21–24 彩色 case box 的视觉分区也不会完整保留在纯文本中。本报告中的表格数字与错误类别已对照渲染页，而非只依赖线性文本顺序。
- [AUTHOR_FACT] p.14–18 prompt 框在文本抽取时出现控制字符/断词，p.20 的示例字符串含异常 Unicode 字形；可视 PDF 同样显示为排版/编码瑕疵，没有发现它们造成主结果数字变化。
- [OPEN_QUESTION] 论文自身存在工具命名不完全一致，但这不是解析器与视觉页冲突：p.2 Figure 1 的示例调用出现 `TransportationSearch`，工具箱和 p.12 Table A.2 列的是 `FlightSearch`/`DistanceMatrix`；pp.14–15 prompt 使用 `GoogleDistanceMatrix`，正文表格多写 `DistanceMatrix`。原文没有解释这些名称是否是别名。

## 9. 实际读取文件、使用工具与 trace 可见性

### 实际读取的研究文件（仅以下三项）

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P004_travelplanner.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P004/read_2_attempts/r2-20260719-p004-a1/invocation.md`

未枚举工作区，未读取 read_1、Cards、其他报告、blind query，未联网，未生成 Card，未评价 Candidate，未运行科研 Reviewer。

### 实际使用的工具

- `shell_command`：PowerShell `Get-Content` 读取两份 Markdown；`Get-FileHash` 核验三份输入；本地 Python + PyMuPDF 获取 PDF 页数并逐页抽取文本。
- `pdfinfo`：曾尝试读取该 PDF 的元数据，但本环境命令不可用/返回 “The system cannot find the path specified”；未据此形成任何事实判断。
- Node REPL + 本地 Python（PyMuPDF、Pillow）：不落地中间图像，在内存中渲染 24 页并组成四张 contact sheet 做视觉核对。
- 调用编排层：用于展示 shell 输出、内存图像和一次工具目录查询；工具目录查询没有读取工作区文件。

### Provenance / trace

- Actual model/version：`Codex（GPT-5 系列）`；精确 serving model/version 对本 reader 不可见，记为 `unknown`。
- Canonical task：`/root/p004_second_read`；平台内部 UUID/thread ID 不可见，记为 `unknown`。
- Path allowlist：平台未提供可验证的文件级 allowlist；本轮为 `procedural_blinding`，不得表述为技术隔离。
- Observable file-access/tool trace：本会话中上述命令与工具调用可观察；平台级、系统完整文件访问审计 trace 为 `unavailable`。
- 唯一持久写入：本 `report.md`。
