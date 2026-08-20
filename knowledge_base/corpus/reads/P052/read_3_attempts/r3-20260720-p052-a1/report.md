# P052 independent read-3 report

## Provenance 与访问披露

- Attempt：`r3-20260720-p052-a1`；本报告引用同目录 `invocation.md` 的冻结请求。
- 核验原文：`knowledge_base/staging/papers/P052_llmfp.pdf`，57 个物理页；实测 SHA-256 为 `e59c5c55b3befeeb4774a20990b8629f487e9fb1520cc2a953f041b7bb6fdaec`，与 invocation 一致。
- 统一提示：`knowledge_base/templates/second_read_prompt.md`；invocation 记录的 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。
- 阅读方式：逐物理页读取 PDF 内嵌文本层；另以内存渲染核对物理页 8、20、41、42 的主结果表、时间表、Formatter 与 Self Assess 示例，未创建临时文件。所核页面的视觉内容、图注和抽取文本未见冲突；其余页面未逐页像素渲染，复杂视觉布局是否含文本层未保留信息仍是 `[OPEN_QUESTION]`。
- 访问边界：`procedural_blinding`，不是技术文件级隔离。实际仅访问本 PDF、P051 指定 PDF、本 attempt 的 invocation、统一 prompt，以及必要的 AGENTS/CRL/技能指令；未联网，未读取 read_1/read_2、Cards、Evidence、reconciliation、audit、corpus report 或 blind 文件。
- 可观察工具轨迹：本地 SHA-256；PyMuPDF 1.28.0 页数、文本抽取与内存栅格化；写入仅为本文件。实际模型/version 与宿主 thread ID 对本读者不可见，记为 `unknown`；可见 agent task 为 `/root/plan05_p051_p052_third_reader`。

## 1. 方法改变的计算、输入输出与干预时点

- `[AUTHOR_FACT]` LLMFP 把直接规划改成五段：DEFINER 提取目标/决策变量/约束，FORMULATOR 生成变量 JSON 表示，CODE GENERATOR 写 Python/Z3，RESULT FORMATTER 把执行结果变成计划并作简短正确性说明，SELF ASSESS & MODIFICATION 检查前三步并替换首个被判错误的输出。定位：物理页 2，Figure 1；物理页 4–7，§3.1–3.6。
- `[AUTHOR_FACT]` 输入包括自然语言 task description、background information/API 和 query；输出是执行后格式化的计划。定位：物理页 4，§3 开头。短定位：`Task Description d`、`Background Information & API i`、`User Query q`。
- `[AUTHOR_FACT]` Code Generator 遇 runtime error 最多重新生成 5 次；Self Assess 最多循环 5 次。定位：物理页 7，§3.4、§3.6。
- `[READER_INTERPRETATION]` 真正增量不是“solver 变严谨”，而是把此前 task-specific formalization prompt 拆为一个跨任务的定义—变量表示—代码生成—同模型修订链；solver 仍只求解生成代码。

## 2. “zero-shot / task-agnostic”的真实边界

- `[AUTHOR_FACT]` 作者的 zero-shot 定义是：测试任务不需要 task-specific examples，且所有基线也以相同 task description、background/API、query 作为输入。定位：物理页 4，§3；物理页 8，§4.2 Baselines。
- `[AUTHOR_FACT]` FORMULATOR 并非无示例：单步多约束 prompt 固定含 Block Picking 与 TSP 两个示例；多步 prompt 固定含一个很长的 Logistics 示例。作者称这些示例未取自 9 个测试任务且跨任务不变。定位：物理页 6，§3.3；物理页 44–50，Appendix A.10.2。
- `[AUTHOR_FACT]` 不同任务类型使用不同 prompt 路径：多步问题省略 implicit-constraint Definer，并使用 objects/predicates/actions/update/goal 五段表示；单步问题使用另一组 6-field 变量表示。定位：物理页 5–6，§3.2–3.3；物理页 9–10 的 ablation 中多步 No Definer 标为 N/A。
- `[READER_INTERPRETATION]` 因而系统需要外部知道任务属于 single-step 还是 multi-step；“task-agnostic”更准确地表示“跨测试任务复用两套手工模板与固定跨域示例”，不是无需任务类型路由或无需人写形式化接口。
- `[AUTHOR_FACT]` 每个任务仍提供详细 domain engineering：完整目标、动作前置/后效、背景数组或 API、固定 output format；多步任务还提供 `update_data(solver)` 帮助更新未改变谓词。定位：物理页 27–34，Figures 4–12；尤其物理页 31–34 的四个多步任务。
- `[AUTHOR_FACT]` 论文明确要求 task description/query 清楚且详细；歧义或缺信息会使目标/约束定义困难。定位：物理页 10–11，Limitations。
- `[AUTHOR_FACT]` GPT-4o 与 Claude 的 prompt 并非完全相同；作者称 Claude 更自然地考虑约束、评估更严格，因此略作编辑，完整差异主要在代码/项目页而非论文正文。定位：物理页 43，Appendix A.10.2。
- `[OPEN_QUESTION]` 论文没有对“写 task description、动作语义、API、output format、任务类型路由”的人工小时作量化，也没有对完全未经作者整理的原始用户任务进行测试。

## 3. Same-model self-assessment：归因、可靠性与 harmful cases

- `[AUTHOR_FACT]` Self Assess 读取 task/query/API、Definer、Formulator、代码和 execution feedback，对三步给二元评分；若有错误，由该步骤自己生成修改。定位：物理页 7，§3.6；物理页 52，Self Assess & Modification Prompt。
- `[READER_INTERPRETATION]` 论文没有独立 critic 或不同模型交叉评审：同一 LLM family 既产生 formalization/code，又根据相同上下文与其执行结果判断自己的错误。因此它可修复明显 runtime/常识问题，但共享盲点不能由“自评通过”排除。
- `[AUTHOR_FACT]` 去掉 Self Assess 的 GPT-4o optimal rate 从五个多约束任务平均 79.1 降到 57.2，从四个多步任务平均 87.5 降到 75.1；各任务表中 Task Allocation 为 96.0 对 96.0，其余不高于完整系统。定位：物理页 9–10，§4.3 与 Table 3。
- `[READER_INTERPRETATION]` 该 ablation 表明“增加自评+最多 5 次后续循环的完整配置”有效，但没有隔离自评判断本身：额外 call、额外 token、再次代码生成和再次 solver 执行都同时增加，故不能把增益唯一归因于 same-model error diagnosis。
- `[AUTHOR_FACT]` 直接 harmful case：Gripper 中 solver 未找到解实际源于代码错误时，Self Assess 有时误判为 timestep 不足，并在原循环内再加循环，导致程序永远执行。定位：物理页 25，§A.6.9。
- `[AUTHOR_FACT]` 直接一致性反例：Coffee 示例的 Formatter 一方面输出正确的增量需求 39/26，另一方面按旧需求 30/20 写“constraint: No”；紧接着 Self Assess 仍把 Step 1–3 全评为 1。定位：物理页 41，Figure 19；物理页 42，Figure 20。短定位：`cafe2 needs 30 ... receives 39` 与三个 `Rating: 1`。
- `[READER_INTERPRETATION]` 该示例说明同模型自评可能忽略 formatter 自身的矛盾；即使本例最终计划数值正确，自评通过也不是端到端语义证书。
- `[OPEN_QUESTION]` 原文未报告 self-assessor 的 precision/recall、误修率、每轮“改善/不变/变坏”转移、无限运行触发率，也没有 independent-assessor、cross-model assessor 或等调用随机重试对照。

## 4. Matched budget 与基线解释

- `[AUTHOR_FACT]` Direct、CoT、Code、Code SMT 与 LLMFP 获得相同任务信息；基线也有 formatter。Code 可用任意 package/solver，Code SMT 明确使用 Z3；另有 o1-preview Direct。定位：物理页 8，§4.2 Baselines；物理页 43，baseline prompts。
- `[AUTHOR_FACT]` LLMFP 是多调用链，且可有 5 次 code regeneration 与 5 次 self-assessment loop；Direct/CoT prompt 是一次规划生成，Code/Code SMT 是一次代码生成再执行/格式化。定位：物理页 7，§3.4–3.6；物理页 43–52，Appendix A.10。
- `[AUTHOR_FACT]` 平均 wall time 显著不同：GPT-4o 的 LLMFP 在五个多约束任务平均 52.7s、四个多步任务平均 73.0s；对应 Direct GPT-4o 为 3.2s/2.7s，Code SMT GPT-4o 为 15.8s/10.3s。定位：物理页 20，Tables 8–10。
- `[AUTHOR_FACT]` Coffee 每题成本：LLMFP GPT-4o `$0.139`，Direct GPT-4o `$0.008`，CoT `$0.013`，Code `$0.023`，Code SMT `$0.024`，Direct o1-preview `$0.536`；LLMFP 九任务约 `$0.08–0.14/query`。定位：物理页 21，Tables 11–13。
- `[READER_INTERPRETATION]` “same input”不是 matched compute。主结果没有等 LLM-call、等 token、等美元、等 wall time、等 solver/retry 上限的对照；因此可比较的是系统级效果/成本点，而不是在固定预算下形式化分解的纯增益。
- `[OPEN_QUESTION]` 论文未报告各方法 token 数、精确 call 数、formatter 是否计入全部成本、solver timeout 对所有方法是否相同，也未给一个把 LLMFP 截断到 Direct/Code 同预算的曲线。
- `[AUTHOR_FACT]` 多步主表原先没有明确要求基线输出最优，而 LLMFP 可通过从短 horizon 递增证明更短步数无解；Appendix A.7 后来加入 explicit-optimal baselines，部分数值改变但仍低于 LLMFP。定位：物理页 26，§A.7、Table 14。
- `[READER_INTERPRETATION]` Appendix A.7 缓解了目标指令不匹配，但未解决调用/token/solver 预算不匹配。

## 5. 相对前代形式化框架的真正增量

- `[AUTHOR_FACT]` 前代 P051 使用 3 个 TravelPlanner 查询—步骤示例、几乎覆盖全部步骤的代码示例、训练集调 prompt 与模型特定补丁，然后让 LLM 生成 Z3 代码。定位：P051 物理页 4–6、24–34。
- `[AUTHOR_FACT]` P052 明确把 P051 列为 formal verification planning 先行工作，同时主张此前方法依赖 task-specific examples；LLMFP 改用 generic Definer、fixed task-agnostic Formulator examples、zero-example Code Generator 与 Self Assess。定位：P052 物理页 3–4，§2；物理页 5–7，§3.2–3.6；P052 物理页 11 的 Hao et al. 引用。
- `[READER_INTERPRETATION]` 可证的真正增量有三项：一是把“测试域专用步骤/代码 demonstrations”换成跨域目标—变量—约束表示；二是统一覆盖单步多约束与多步状态转移；三是增加基于 execution feedback 的自动回溯修订。九任务结果与 No Formulator/No Self Assess ablation 支持这些系统组件的经验价值。
- `[READER_INTERPRETATION]` 未改变的核心是 LLM 负责语义 formalization、外部 solver 负责搜索；solver guarantee 仍条件化于正确编码。P052 也没有消除手工 task description/API/output format、固定示例、任务类型模板或模型特定 prompt 调整，因此不应把增量表述成“无 task engineering”。
- `[AUTHOR_FACT]` 添加单个 task-specific Formulator 示例可把 Coffee 七类查询平均 optimal rate 从 61.2 提到 85.4，尤其歧义 Set 3 从 11.8 到 70.6。定位：物理页 10，§4.4、Table 4。
- `[READER_INTERPRETATION]` 该结果同时说明通用化是实质改进，也显示在歧义 query 上 domain example 仍提供很大的剩余收益；zero-shot 不是“无需域知识”的同义词。

## 6. Solver guarantee、失败与运行边界

- `[AUTHOR_FACT]` 作者称 SMT sound and complete，在编码正确时可保证优化计划；多步任务通过从较小 timestep 开始验证无解来找最短计划。定位：物理页 7，§3.7；物理页 19，§A.3；物理页 26，§A.7。
- `[READER_INTERPRETATION]` 保证对象是生成的 SMT 模型，不是自然语言任务。失败例反复显示“solver 严格优化错误模型”：Sokoban 未把未提及 adjacency 设为 false；Coffee 漏 conservation；Warehouse 覆写 API；Blocksworld 未初始化未提及谓词。定位：物理页 17，Sokoban；物理页 24–25，§A.6。
- `[AUTHOR_FACT]` Workforce 的 solver 最长运行 15 分钟，部分难题因此找不到最优解；更大数据库/可行计划很多时 solver 变慢。定位：物理页 24，§A.6.2；物理页 10–11，Limitations。
- `[AUTHOR_FACT]` 其他明确失败包括：Coffee/Facility/Workforce 的歧义 query 被反向解释；Task Allocation Formulator 写错 robot finish time；Warehouse Code Generator 把给定 `get_distance` 覆写为常数 1；Gripper 的误修可无限执行。定位：物理页 24–25，§A.6.1–A.6.9。
- `[OPEN_QUESTION]` 论文未统一报告每任务 timeout、runtime error、错误但可执行 formalization、self-assessor false pass 的计数；optimal rate 无法直接分解这些机制。

## 7. 可复用机制与可记录失败（仅本次阅读层）

- `[READER_INTERPRETATION]` 可复用机制：以目标/变量/约束 schema 降低一步生成完整 solver 程序的难度；把 execution feedback 送回最早错误步骤作局部重建；对多步任务显式编码 closed-world 初始化、action precondition/effect、frame update 和 goal horizon。依据：物理页 5–7、44–52。
- `[READER_INTERPRETATION]` 可记录失败：同模型共享盲点、错误 API 覆写、closed-world 漏初始化、歧义 query 方向翻转、solver 超时、误把代码错误当 horizon 不足并造成无限循环。依据：物理页 17、24–25、41–42。
- `[OPEN_QUESTION]` 没有外部语义 oracle 时，self-assessment 能否稳定发现“可运行、可满足、但语义错误”的模型仍未解决。

## 8. 逐页覆盖摘要与非裁决声明

- 物理页 1–13：摘要、方法、主实验、ablation、限制、参考文献；物理页 14：目录。
- 物理页 15–26：任务复杂度、Sokoban、迭代/成功率、时间成本、基线与 LLMFP 失败、显式最优基线。
- 物理页 27–34：9 个任务的完整 task description、background/API 与 query 示例；物理页 35–42：Coffee 的基线与 LLMFP 全阶段输出，包括 formatter/self-assess 矛盾。
- 物理页 43–52：baseline、Definer、两类 Formulator、Code Generator、Formatter、Self Assess 的 prompt；物理页 53–56：切换 MILP 的 prompt 差异与输出；物理页 57：paraphrase 实验。
- 本报告只做独立核源与边界解释，不作论文准入、Card 写入、Candidate 评价或最终科研裁决。
