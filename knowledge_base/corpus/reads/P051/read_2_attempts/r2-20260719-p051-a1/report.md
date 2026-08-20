# P051 独立二读报告

## Provenance 与边界

- [AUTHOR_FACT] 本报告对应 frozen invocation `r2-20260719-p051-a1`，引用路径为 `knowledge_base/corpus/reads/P051/read_2_attempts/r2-20260719-p051-a1/invocation.md`；其中指定 PDF 为 `P051_formal_verification_planning.pdf`，SHA-256 为 `ba9261d6d8fbf2b43817e57c29aa6ffacc0b14ef038e6c86a33f8780490bd365`，prompt SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。（invocation，首部 manifest，短定位：“Independent read-2 invocation”）
- [READER_INTERPRETATION] 我按 invocation 的 `procedural_blinding` 边界独立阅读了该 PDF 的全部 50 个 PDF 页面；没有读取 read_1、Card、Evidence、其他论文读稿、其他读者报告或 blind query/judgment/result，也没有联网。
- [OPEN_QUESTION] 运行界面未暴露可核验的实际基础模型版本或平台 thread ID；actual model/version 记为 `unknown`，本代理任务路径为 `/root/plan05_p051_p052_second_reader`，技术级文件访问 trace 不可用，只能披露下文可观察操作。

## 1. 方法改变的计算步骤

- [AUTHOR_FACT] 框架将原先由 LLM 直接生成完整计划的步骤，改为：自然语言查询→LLM 生成形式化步骤→LLM 生成 Python/Z3 代码→执行 SMT 求解→LLM 将结果转回自然语言；若不可满足，则读取 unsat core、收集信息、提出约束修改并再次求解。（PDF p.3–5，Fig. 1、§3.2–3.4，短定位：“Query to Steps”“Steps to Codes”“get_unsat_core”）
- [AUTHOR_FACT] Query-Step 由三个手工 TravelPlanner 示例教授，步骤按目的地、日期、交通、航班、餐饮、景点、住宿、预算等主题拆分；Step-Code 示例几乎覆盖示例步骤中的全部 API 与 SMT 调用。（PDF p.4–5，§3.3.1–3.3.2，短定位：“three human-crafted examples”“cover almost all the steps”）
- [READER_INTERPRETATION] 真正新增的计算干预是把组合搜索与约束满足交给求解器，同时把“从自然语言到约束代码”的语义建模留给 LLM；因此方法的严谨性由两段组成：形式化是否忠实，以及求解器是否正确求解该形式化。论文的强保证只直接覆盖后者。
- [READER_INTERPRETATION] 可供主 Codex 后续抽取的机制而非本报告裁决：`NL→步骤→代码→SMT` 的分层形式化，以及 `unsat core→信息收集→最小约束修改→再求解` 的交互修复回路。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] TravelPlanner 输入是自然语言约束，涉及起点、目的地、旅行天数/日期、人数、预算及交通、餐饮、住宿偏好；输出逐日指定城市、交通、景点、餐厅与住宿。（PDF p.3–4，§3.1，短定位：“Given a natural language description”“output plan should satisfy C”）
- [AUTHOR_FACT] 框架可调用 CitySearch、FlightSearch、DistanceSearch、RestaurantSearch、AttractionSearch、AccommodationSearch 等封闭数据库 API；失败修复阶段还使用 FlightCheck/DrivingCheck 等检查或搜索 API。（PDF p.4–5、p.31–38，§3.3.2、§3.4、Appendix G，短定位：“information collection APIs”）
- [AUTHOR_FACT] 求解器执行点位于 LLM 已生成代码之后；只有在代码执行得到不可满足原因后，交互修复才发生。（PDF p.4–5，§3.2–3.4，短定位：“execute the code”“proceeds to interactive plan repair”）
- [AUTHOR_FACT] 作者说明所有信息来自所用数据库，系统不能区分数据库中的不安全或错误信息。（PDF p.9，§7 Risky Data，短定位：“does not have the capability to distinguish unsafe or incorrect information”）
- [READER_INTERPRETATION] 输出计划的形式正确性只相对于被编码的约束和数据库快照成立，不等价于对现实世界安全性、数据真实性或用户自然语言原意的端到端证明。

## 3. Formalization fidelity 与 solver guarantee 边界

- [AUTHOR_FACT] 作者在 §3.3.3 称 SMT solver sound and complete，并称“若解存在则保证找到”；正文结论则使用“almost guarantees”，而 TravelPlanner 实验为 solver 设置每题 30 分钟上限。（PDF p.5、p.6、p.8–9，§3.3.3、§5、§6–7，短定位：“guarantees to find a solution if there exists one”“30 minutes”“almost guarantees”）
- [AUTHOR_FACT] 1180 个 TravelPlanner 查询中，1.3% 因超过 30 分钟而未找到计划；验证集 180 题中有 1 题超时，其余 179 题求解器平均 38.39 秒。（PDF p.9、p.16，§7 Solver Runtime、Appendix B.1、Table 6，短定位：“1.3%”“179 out of 180”“38.39 seconds”）
- [AUTHOR_FACT] 新任务失败分析明确记录形式化/代码错误：Block Picking 漏掉 all-different，导致重复选择高分块；Task Allocation 错用 `Max` 参数产生运行错误；Warehouse 把起终点变量与站点变量混淆产生冲突，或把站点 ID 误当列表索引而得到非最优解。（PDF p.22–23，Appendix F.3，短定位：“fails to take this into account”“runtime errors”“incorrect distance”）
- [AUTHOR_FACT] Mistral-Large 的主要失败包括未见过的 “no shared room” 语义被错误翻译，以及偶发代码生成错误和运行时问题。（PDF p.34，Appendix G.1.4，短定位：“not shared room exists”“code generation errors”）
- [READER_INTERPRETATION] “sound and complete”不能推出端到端计划必然正确：只有在约束集合忠实、代码无误、API 数据正确且求解未被超时截断时，solver 的结论才具有相应保证。论文自己的失败案例直接证明 LLM 形式化层可漏约束、反转语义、产生索引错误或运行错误。
- [OPEN_QUESTION] 论文没有给出独立的形式化语义等价检查器、人工双审协议或逐约束覆盖证明；因而无法从文中确定 93% 以上通过样本中是否仍存在 benchmark evaluator 未覆盖的语义偏差。
- [OPEN_QUESTION] 文中将 Z3 `Optimize()` 用于优化（Appendix G 代码），但“sound and complete”表述主要以 satisfiability solver 为对象；在优化、启发式预筛选和 30 分钟超时并存时，最优性/完备性的精确适用条件没有被形式化陈述。

## 4. 基线、比较公平性与替代归因

- [AUTHOR_FACT] TravelPlanner 主要基线包括 Greedy Search、TwoStage (GPT-4)、Direct (GPT-4) 和验证集上的 Direct (o1-preview)；作者没有用 o1-preview 跑 TwoStage 或本框架，理由是其运行时间长。（PDF p.6，§5.1 Baselines，短定位：“do not evaluate Two-Stage or our framework with o1-preview”）
- [AUTHOR_FACT] Table 1 中验证/测试最终通过率：Ours (Claude-3) 为 93.3%/93.9%，Ours (GPT-4) 为 93.3%/90.2%，Direct (GPT-4) 为 4.4%/4.4%；Direct (o1-preview) 只报告验证集 10.0%。（PDF p.7，Table 1，短定位：“Final Pass Rate”）
- [AUTHOR_FACT] 为与仅用自然语言输入的基线比较，主结果去掉了 NL→JSON 步骤；加回 JSON 后，验证集 GPT-4/Claude/Mistral 的最终通过率为 98.9%/98.3%/84.4%，GPT-4 测试集为 97.0%。（PDF p.4、p.6、p.19，§3.3.1、§5.1、Appendix D.1/Table 8，短定位：“For fairness”“Ours+JSON”）
- [AUTHOR_FACT] 新领域实验在每个任务中加入“一份 travel planning 示例”和“几行新问题描述”，并提供任务专用 API 描述；比较对象是 TwoStage (GPT-4o)，两者各测 25 个场景。（PDF p.8、p.21–22，§5.2.3、Appendix F.1–F.2，短定位：“one example from travel planning and a few lines of new problem description”）
- [READER_INTERPRETATION] 同模型的 Direct (GPT-4) 与 Ours (GPT-4) 结果支持“分层形式化+solver”优于直接生成，但并未隔离多轮 prompt、更多 token、更多 API 调用、solver 搜索和离线 prompt 调优各自的贡献。
- [READER_INTERPRETATION] 以 Ours (Claude-3) 对比 Direct (o1-preview) 或 LLM-Modulo (o1-preview) 不是严格同模型比较；而新领域所谓 zero-shot 仍获得任务描述、任务 API 与额外提示文字，结论应理解为“无该任务训练示例的迁移”，而非“无任务工程/无任务知识”。
- [OPEN_QUESTION] 论文没有报告各方法 matched token budget、matched tool-call budget、matched wall-clock budget 或 matched prompt length；也没有给出全部基线的成本，因此不能排除资源预算差异的替代解释。
- [OPEN_QUESTION] Greedy/TwoStage/Direct 的部分结果来自既有论文，而当前框架提示在 TravelPlanner 训练集上调优；文中没有提供一次统一重跑、相同模型版本和相同 API 快照下的完整比较。

## 5. 主要结果、负向结果与未测边界

- [AUTHOR_FACT] 主 TravelPlanner 测试集 1000 题上，最佳报告最终通过率为 Claude-3 的 93.9%；Mistral-Large 为 67.8%，且 delivery rate 为 69.9%。（PDF p.6–7，§5.1、Table 1，短定位：“Test (#1000)”）
- [AUTHOR_FACT] 四个新任务 Block Picking、Task Allocation、TSP、Warehouse 的 optimal rate 分别为 92%、92%、100%、72%；Warehouse 是最弱的新领域。（PDF p.7–8，Table 2、§5.2.3，短定位：“Optimal”）
- [AUTHOR_FACT] 不可满足查询修复在 10 次迭代下平均成功率为 UnsatChristmas 78.6%、修改版 TravelPlanner 85.0%；20 次迭代升至 81.6% 和 91.7%。（PDF p.7–8、p.20，Tables 3–4、Appendix E，短定位：“Ours-20”）
- [AUTHOR_FACT] 作者明示限制包括从头设计步骤/代码提示很耗时、SMT 随规模增大变慢、可能需要启发式或其他 solver、以及数据库风险。（PDF p.9，§7，短定位：“time-consuming to formulate”“Solver Runtime”“Risky Data”）
- [READER_INTERPRETATION] 可供后续记录的真实失败信号包括：自然语言语义误编码、遗漏约束、错误 API/索引使用、代码执行失败、solver 超时，以及基于不安全数据生成形式上可满足但现实有风险的计划。这些是论文明确展示的 failure modes，不是本报告对 Candidate 的评价。
- [OPEN_QUESTION] 未测试边界包括更大/动态数据库、开放世界实时数据、对抗或含糊查询、数据库事实错误、比 3/5/7 天更长的 TravelPlanner 组合，以及在严格资源上限下的规模扩展。

## 6. 成本与运行时间

- [AUTHOR_FACT] Appendix B 报告 TravelPlanner 验证集 GPT-4 平均每题成本 0.74 美元；179 个交付题平均总时长 245.66 秒，其中 NL-JSON 5.45 秒、JSON-Step 35.16 秒、Step-Code 166.66 秒、SMT 38.39 秒。（PDF p.16，Appendix B.1、Table 6，短定位：“$0.74 per query”“245.66 seconds”）
- [AUTHOR_FACT] UnsatChristmas 中 hard-budget 模拟用户的 23 个成功查询，GPT-4 平均每迭代 0.65 美元、33.68 秒，成功修改平均需 2.22 次迭代。（PDF p.16，Appendix B.2、Table 7，短定位：“$0.65 per iteration”“2.22 per query”）
- [READER_INTERPRETATION] 交互修复的典型成功案例若按报告均值估算，仅 LLM 迭代成本约为 0.65×2.22≈1.44 美元；这是读者基于作者均值的乘积，不是作者直接报告的总体均价，且不包含失败查询的完整消耗。
- [OPEN_QUESTION] Table 6 的阶段列表包含 NL-JSON，但主公平比较明确去掉 NL→JSON；论文没有澄清 0.74 美元/245.66 秒对应主版 Ours 还是 Ours+JSON，也没有报告 Claude/Mistral、全部失败题或所有基线的同口径成本。

## 7. 解析文本与可视 PDF 核对

- [READER_INTERPRETATION] PyMuPDF 逐页解析覆盖 PDF p.1–50；对 PDF p.7（Tables 1–4）、p.16（Tables 6–7）与 p.23（Appendix F.3 失败案例）进行了内存渲染视觉抽查，表中数字、标题与失败叙述未发现与解析文本冲突。
- [READER_INTERPRETATION] 附录代码页的解析文本丢失部分缩进并把少量排版箭头拆开，因此本报告不依赖解析后的精确 Python 语法来做代码可执行性判断；方法语义、表格数值和作者叙述可稳定定位。
- [OPEN_QUESTION] 未对 50 页逐页做像素级 OCR 对照；“无冲突”只表示逐页文本阅读加关键页视觉抽查未发现实质差异。

## 8. 可观察访问与工具披露

- [READER_INTERPRETATION] 实际读取的科研材料仅为：P051 PDF、P051 本 invocation、统一 `second_read_prompt.md`；另外为遵守执行规则读取了工作区两级 `AGENTS.md`、`pdf` 与 `encoding-safe-edit` 的 `SKILL.md`。P052 材料仅用于独立完成另一份 P052 报告，未用于本篇结论。
- [READER_INTERPRETATION] 实际工具：PowerShell `Get-FileHash` 验证 SHA-256；`.NET UTF8Encoding(false,true)` 读取 Markdown；本地 Python 3 + PyMuPDF (`fitz`) 获取页数、逐页文本与内存 PNG；`shell_command` 执行只读命令；`apply_patch` 创建本报告。曾尝试本地 `pdfinfo`，其包装器无法解析路径，未产生研究结论；未使用网络、OCR、外部 API 或其他代理。

