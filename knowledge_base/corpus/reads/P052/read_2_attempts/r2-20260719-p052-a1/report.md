# P052 独立二读报告

## Provenance 与边界

- [AUTHOR_FACT] 本报告对应 frozen invocation `r2-20260719-p052-a1`，引用路径为 `knowledge_base/corpus/reads/P052/read_2_attempts/r2-20260719-p052-a1/invocation.md`；其中指定 PDF 为 `P052_llmfp.pdf`，SHA-256 为 `e59c5c55b3befeeb4774a20990b8629f487e9fb1520cc2a953f041b7bb6fdaec`，prompt SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。（invocation，首部 manifest，短定位：“Independent read-2 invocation”）
- [READER_INTERPRETATION] 我按 invocation 的 `procedural_blinding` 边界独立阅读了该 PDF 的全部 57 个 PDF 页面；没有读取 read_1、Card、Evidence、其他论文读稿、其他读者报告或 blind query/judgment/result，也没有联网。
- [OPEN_QUESTION] 运行界面未暴露可核验的实际基础模型版本或平台 thread ID；actual model/version 记为 `unknown`，本代理任务路径为 `/root/plan05_p051_p052_second_reader`，技术级文件访问 trace 不可用，只能披露下文可观察操作。

## 1. 方法改变的计算步骤

- [AUTHOR_FACT] LLMFP 将自然语言规划分成五步：DEFINER 提取目标/决策变量/约束，FORMULATOR 生成变量 JSON，CODE GENERATOR 写 Z3 代码，RESULT FORMATTER 将执行结果转成固定格式，SELF ASSESS & MODIFICATION 评估三步并从首个错误步骤重新执行。（PDF p.2–7，Fig. 1、§3.1–3.6，短定位：“five steps”“modifies the first incorrect step”）
- [AUTHOR_FACT] Code Generator 遇到 runtime error 最多重新生成 5 次；Self Assess & Modification 最多循环 5 次。（PDF p.7，§3.4、§3.6，短定位：“maximum re-generation times to be 5”“maximum number of loops to be 5”）
- [READER_INTERPRETATION] 核心计算干预不是新 solver 算法，而是把一次性“直接规划”改造成结构化形式化流水线，并用执行结果驱动同一 LLM 的多轮修订；solver 负责在给定编码上搜索，LLM 负责决定编码表达什么。
- [READER_INTERPRETATION] 可供主 Codex 后续抽取的机制而非本报告裁决：`goal/constraint definition→typed variable representation→code generation→solver execution` 的分解，以及 `execution feedback→step-wise self-assessment→局部回滚` 的修订回路。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 用户输入包括自然语言任务描述 `d`、背景信息/API `i` 与用户查询 `q`；任务描述给问题设置与目标，背景信息提供数值或 API，查询给初始/目标状态或新增/修改约束。（PDF p.4，§3，短定位：“Natural Language Task Description”“Background Information & API”“User Query”）
- [AUTHOR_FACT] 实验还给各方法相同的期望输出格式/formatter；9 个任务的输入附录展示了详细任务定义、具体数据结构或辅助 API，以及示例查询。（PDF p.8、p.27–34、p.43，§4.2、Appendix A.8、A.10.1，短定位：“same input information”“Expected output format”）
- [AUTHOR_FACT] 单步任务的 DEFINER 在看到任务描述和背景信息后生成目标/变量/约束；FORMULATOR 再结合查询；多步任务 FORMULATOR 直接按 objects/predicates/actions/update/goal 组织，任务动作的 precondition/effect 由输入明确给出。（PDF p.5–6，§3.2–3.3、Fig. 2，短定位：“implicit constraints”“five sections”）
- [READER_INTERPRETATION] “只给任务描述、什么也没有”的引言愿景并非实验的字面输入条件；实测系统还获得背景数值/API、明确动作语义、查询、输出格式，以及通用提示中的 solver/变量建模说明。

## 3. Zero-shot / task-agnostic 的实际边界

- [AUTHOR_FACT] 作者定义 zero-shot 为测试任务不需要 task-specific examples；FORMULATOR 仍包含固定的示例：单步任务用 Block Picking 与 TSP 两个示例，多步任务用 Logistics 示例，这些示例跨所有测试任务保持不变。（PDF p.6、p.44–50，§3.3、Appendix A.10.2，短定位：“not task-specific examples”“fixed for all the planning tasks”）
- [AUTHOR_FACT] Code Generator 不含示例，但 prompt 明确要求 Python/Z3 语法、变量字段含义、`Optimize()` 初始化和优化目标位置；Claude 的提示因模型特性做了少量编辑。（PDF p.7、p.43、p.50–52，§3.4、Appendix A.10.2，短定位：“with no examples”“edit the prompts a little”）
- [AUTHOR_FACT] 9 个主任务含 5 个多约束任务与 4 个多步任务；Coffee/Workforce/Facility 来自既有 MILP benchmark，Task Allocation/Warehouse 由作者创建，多步任务来自规划 benchmark。（PDF p.7、p.15–16，§4.1、Appendix A.1，短定位：“9 planning problems”）
- [AUTHOR_FACT] 在 Coffee 的每类查询向 FORMULATOR 加一个 task-specific 示例后，平均 optimal rate 从 61.2% 升至 85.4%，提升 24.2%；作者将大幅提升尤其归因于含糊的 “Why” 查询。（PDF p.10，§4.4、Table 4，短定位：“improves … by 24.2%”）
- [AUTHOR_FACT] Blocksworld 任务描述经 LLM 随机改写后，Claude 3.5 Sonnet 在 50 题上得到 92% optimal rate；作者限定前提为改写后仍有充分信息。（PDF p.57，Appendix A.10.4、Table 15，短定位：“as long as they have adequate information”）
- [READER_INTERPRETATION] 论文支持的是“固定跨任务模板与固定跨任务示例，在给出详细任务规范/API 后，对未提供该任务示例的 9+1 个域进行迁移”；它不证明任意任务、无 API 工程、无格式工程或含糊/缺信息输入下的 task-agnostic 规划。
- [OPEN_QUESTION] 固定示例与测试任务在结构上接近（例如 TSP 示例与 Warehouse 路径优化、Logistics 示例与多步状态更新）；论文没有做“移除所有示例但保持其他预算一致”或“换成结构不相似示例”的对照，无法量化 task-agnostic 示例的迁移贡献。
- [OPEN_QUESTION] 作者承认 LLMFP 需要清晰详细的任务描述与查询；未测试开放世界、未知动作语义、工具/API 缺失、严重歧义或输入事实不完整时的 zero-shot 边界。（PDF p.10–11，Limitations，短定位：“needs clear and detailed task descriptions and queries”）

## 4. Same-model self-assessment 的归因

- [AUTHOR_FACT] Self Assess prompt 同时获得任务、查询、API、前三步输出和 execution feedback，要求对三步分别二元打分并自行修改错误步骤；没有外部 critic 或不同模型评审者。（PDF p.7、p.51–52，§3.6、Appendix A.10.2，短定位：“assess whether any steps 1-3 are correct”）
- [AUTHOR_FACT] 移除 Self Assess & Modification 后，GPT-4o 在五个多约束任务的平均 optimal rate 从 79.1% 降至 57.2%，四个多步任务从 87.5% 降至 75.1%。（PDF p.9–10，§4.3、Table 3，短定位：“No Self Assess & Modification”）
- [AUTHOR_FACT] Figure 19 的 Coffee Formatter 先写 cafe2 的 light/dark 需求为旧值 30/20、收到 39/26，然后错误地把“收到量≥需求量”判断为 “No”；紧接着又称计划符合约束且符合常识。Figure 20 的 Self Assess 随后把 Step 1–3 全部评为 1。（PDF p.41–42，Figs. 19–20，短定位：“No, cafe2 needs 30 … receives 39”“Rating: 1”）
- [READER_INTERPRETATION] 上述公开示例是 same-model assessment 不能可靠发现自身语义/逻辑错误的直接证据：formatter 的判断内部矛盾，自评仍全通过。它不否定平均消融增益，但限制“自评等价于独立验证”的解释。
- [READER_INTERPRETATION] No-Self ablation 同时移除了错误检测、最多 5 轮额外 LLM 调用、额外 token 和重新求解机会；因此 Table 3 只能把增益归因于整套“多轮自评+修改预算”，不能单独归因于 same-model 判断质量。
- [OPEN_QUESTION] 论文没有 matched-call/matched-token 对照，例如用同等 5 轮预算做无自评重采样、独立模型评审或基于形式规则的 critic；因而无法区分自评内容、额外计算与多次采样带来的贡献。
- [OPEN_QUESTION] 没有报告 self-assessor 的错误发现 precision/recall、误修率、漏检率或按步骤的混淆矩阵；只给最终 optimal rate，无法判断修订链中有多少错误被正确定位。

## 5. 基线、公平性与 matched budget

- [AUTHOR_FACT] 基线为 Direct、CoT、Code、Code SMT，均使用 GPT-4o 与 Claude 3.5 Sonnet，并另加 Direct o1-preview；作者称所有基线均为 zero-shot、接收与 LLMFP 相同的任务描述、背景/API、查询，并配 formatter。（PDF p.8，§4.2 Baselines，短定位：“same input information”“provide all baselines with formatters”）
- [AUTHOR_FACT] GPT-4o 的 9 任务平均 optimal rate 为 83.7%，Claude 3.5 Sonnet 为 86.8%；Direct o1-preview 在五个多约束任务平均 29.7%，四个多步任务平均 68.1%。（PDF p.8–9，Tables 1–2、§4.2，短定位：“Optimal rate (%)”）
- [AUTHOR_FACT] 对多步基线显式加入“最优”要求后，部分方法提高、部分下降，但 LLMFP 仍高于所有表中基线。（PDF p.26，Appendix A.7、Table 14，短定位：“explicit optimal requirements”）
- [READER_INTERPRETATION] 同输入/同模型比较改善了模型差异控制，尤其 LLMFP vs Code SMT；但 LLMFP 是多阶段、多调用、最多 5 次代码重生成和 5 次自修复，而基线 prompt 展示为单次主要调用，故并非 matched inference budget。
- [OPEN_QUESTION] 论文没有报告 token 数、LLM 调用数、tool-call 数、solver 调用数或统一 wall-clock 截止下的 matched-budget accuracy；因此性能差不能仅归因于形式化分解本身。
- [OPEN_QUESTION] Optimal rate 的 ground-truth/evaluator 细节未在本 PDF 中完整定义；尤其自然语言 “Why” 查询的期望方向被作者称为对人也含糊，评价结果部分依赖数据集既定解释。（PDF p.10、p.24，§4.4、Appendix A.6.1/A.6.3，短定位：“confusing even for humans”）

## 6. Formalization failure 与 solver guarantee

- [AUTHOR_FACT] 作者将 SMT 的 soundness/completeness 和最优性保证限定于正确编码：文中多次使用 “given correct input” 或 “if the formulation and generated codes are correct”。（PDF p.7、p.19、p.23、p.26，§3.7、Appendix A.3/A.5.4/A.7，短定位：“given correct input”“with correct encoding”）
- [AUTHOR_FACT] LLMFP 的作者分析记录：Coffee 漏掉烘焙/运输流守恒隐式约束；Task Allocation FORMULATOR 产生错误 robot finish time；Warehouse Code Generator 覆盖 `get_distance` API 并固定返回 1；Blocksworld/Mystery Blocksworld 未把未提及谓词初始化为 False。（PDF p.24–25，Appendix A.6.1/A.6.4–A.6.7，短定位：“fails to consider all implicit constraints”“overwrites the provided API”“unmentioned states”）
- [AUTHOR_FACT] Workforce 有些困难查询超过 15 分钟 solver 上限；Gripper 中 Self Assess 有时误判为 timestep 不足并在原循环内加循环，导致程序永远执行。（PDF p.24–25，Appendix A.6.2/A.6.9，短定位：“maximum solver runtime … 15 minutes”“execute forever”）
- [AUTHOR_FACT] Sokoban 的主要失败是只把提及的相邻位置设为 True，却没把未提及位置设为 False，使 solver 可伪造邻接关系以缩短计划；更大地图也使 SMT 变慢。（PDF p.17，Appendix A.1、Table 5 后，短定位：“fails to initialize unmentioned positions to be False”）
- [READER_INTERPRETATION] 这些失败表明 solver 能严格优化错误世界模型；形式化层的 omission、API corruption 和 closed-world 初始化错误是端到端保证的主要断点。
- [READER_INTERPRETATION] 可供后续记录的真实失败信号包括：隐式约束漏建、查询方向反转、变量值/类型错误、覆盖可信 API、closed-world false 初始化遗漏、solver 超时，以及自修复引入不终止循环。这些是论文明确展示的 failure modes，不是本报告对 Candidate 的评价。
- [OPEN_QUESTION] 论文没有独立语义验证器来证明 DEFINER/FORMULATOR/Code 与自然语言等价，也没有报告形式化错误中哪些被 benchmark evaluator 漏过；“optimal”仅能相对于最终编码与 evaluator 理解。
- [OPEN_QUESTION] 作者称可换用任意 solver，只需改提示要求；附录只给 Coffee 上的 Gurobi 示例，没有跨 9 任务的 solver 替换实验，因此 solver-agnostic 泛化仍是演示性主张。（PDF p.53–56，Appendix A.10.3，短定位：“Coffee example”）

## 7. 成本与运行时间

- [AUTHOR_FACT] GPT-4o 上，LLMFP 在五个多约束任务平均 52.7 秒/题，在四个多步任务平均 73.0 秒/题；多数基线更快，但多约束任务上 Direct o1-preview 平均 76.0 秒。（PDF p.20，Appendix A.4、Tables 8–10，短定位：“Average wall time (s) per query”）
- [AUTHOR_FACT] GPT-4o LLMFP 各任务平均成本为 0.081–0.140 美元/题，作者概括约 0.1 美元；Coffee 上 LLMFP 为 0.139 美元，Direct GPT-4o 为 0.008、Direct o1-preview 为 0.536。（PDF p.21，Appendix A.4、Tables 11–13，短定位：“Average cost ($) per query”）
- [READER_INTERPRETATION] Coffee 同题成本显示 LLMFP 约为 Direct GPT-4o 的 17 倍，但低于不同模型 o1-preview；这说明“成本不高”依赖参照系，不能代替 matched-model/matched-budget 性价比分析。
- [OPEN_QUESTION] 成本只系统报告 GPT-4o，未给 Claude 3.5 Sonnet；也未分成功/失败、重生成次数或自修复轮数报告 token/费用分布，均值可能掩盖长尾。
- [OPEN_QUESTION] Table 10 各组件平均时间之和与 Tables 8–9 的方法总时间并非所有任务都显然一致，论文未说明并行、失败重试或统计口径；因此不宜从组件表反推精确调用预算。

## 8. 解析文本与可视 PDF 核对

- [READER_INTERPRETATION] PyMuPDF 逐页解析覆盖 PDF p.1–57；对 PDF p.8（Tables 1–2）、p.20（Tables 8–10）、p.24（LLMFP failure cases）与 p.41（Figure 19 Formatter 矛盾）进行了内存渲染视觉抽查，关键数值、标题和矛盾文本与解析结果一致。
- [READER_INTERPRETATION] 数学式、代码缩进及少量 “≥/≤” 字符在文本解析中出现布局/编码退化，但视觉核对支持本报告引用的表格与 Figure 19 逻辑矛盾；本报告未依赖退化字符来重建可执行代码。
- [OPEN_QUESTION] 未对 57 页逐页做像素级 OCR 对照；“无其他冲突”只表示逐页文本阅读加关键页视觉抽查未发现实质差异。

## 9. 可观察访问与工具披露

- [READER_INTERPRETATION] 实际读取的科研材料仅为：P052 PDF、P052 本 invocation、统一 `second_read_prompt.md`；另外为遵守执行规则读取了工作区两级 `AGENTS.md`、`pdf` 与 `encoding-safe-edit` 的 `SKILL.md`。P051 材料仅用于独立完成另一份 P051 报告，未用于本篇结论。
- [READER_INTERPRETATION] 实际工具：PowerShell `Get-FileHash` 验证 SHA-256；`.NET UTF8Encoding(false,true)` 读取 Markdown；本地 Python 3 + PyMuPDF (`fitz`) 获取页数、逐页文本与内存 PNG；`shell_command` 执行只读命令；`apply_patch` 创建本报告。曾尝试本地 `pdfinfo`，其包装器无法解析路径，未产生研究结论；未使用网络、OCR、外部 API 或其他代理。

