# P016 fresh independent read-3 report

## 0. Provenance、访问边界与核验方式

- [AUTHOR_FACT] 本报告对应 invocation `r3-20260719-p016-a1`；论文 canonical metadata 为 *Why Do Multi-Agent LLM Systems Fail?*，NeurIPS 2025 Datasets & Benchmarks，PDF SHA-256 为 `6aff168d6e201217d3f79611f6ad024590a599a03b97ac2aeb0b0b128bac374c`。定位：`invocation.md` 顶部 manifest。
- [AUTHOR_FACT] 实际重新计算的 PDF SHA-256 与 prompt SHA-256 分别为 `6AFF168D6E201217D3F79611F6AD024590A599A03B97AC2AEB0B0B128BAC374C`、`FFB7C12E663F44318D8EDA1C270CBC26AD66665FD803247A2AB66A8F23FA333A`，与 invocation 一致。
- [READER_INTERPRETATION] 本次科研内容访问遵守 procedural blinding：只读取指定 PDF、统一 prompt 与本 invocation；没有枚举工作区，没有读取 `read_1`、任何 `read_2`、Cards、其他报告或 blind query，也没有联网。另因上层运行规范强制要求 PDF 任务先读取技能说明、提交前读取完成验证说明，读取了 `C:/Users/g/.codex/skills/pdf/SKILL.md` 与 `C:/Users/g/.codex/plugins/cache/openai-curated-remote/superpowers/6.1.1/skills/verification-before-completion/SKILL.md`；二者均为工具/验收说明，不含 P016、其他读者结论或任何科研内容。此额外访问在这里如实披露，因此不能声称存在技术文件级隔离。
- [READER_INTERPRETATION] 可观察工具轨迹：PowerShell `Get-Content -Encoding UTF8` 读取 prompt/invocation；`Get-FileHash` 校验输入；Python 通过本地 PyMuPDF 逐页提取 54 页文本，并用 PyMuPDF/Pillow 在内存中生成 6 组页面接触图和关键页裁剪图作视觉核对；没有生成或写入临时文件；最终仅通过 `apply_patch` 写本 `report.md`。`pdfinfo` 调用因本机不可用而失败，未产生内容或文件。实际模型/版本在当前界面不可见，记为 `unknown`；本任务标识为 `/root/p016_third_read`。
- [READER_INTERPRETATION] 页码均指 PDF 物理页（同时与页脚页码一致）。全文 54 页均检查；正文为 PDF 页 1–10，参考文献 11–16，NeurIPS checklist 17–23，附录 24–54。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] 论文的核心产物不是一个直接替换 MAS 推理步骤的求解算法，而是“采集执行轨迹 → 建立失败分类法 → 标注轨迹 → 分析/干预系统”的诊断流水线。作者先用 Grounded Theory 分析 150 条轨迹形成 MAST，再用人工一致性迭代标准化定义，最后用 LLM-as-a-Judge 扩展到 1642 条轨迹。定位：PDF p.2，Introduction，短定位“Grounded Theory”；p.5–6，§3.1–3.4，Figure 2。
- [AUTHOR_FACT] MAST 把失败划分为 14 个 failure modes、3 个 failure categories，并映射到 pre-execution、execution、post-execution 阶段。定位：PDF p.2，Figure 1；p.7–8，§4；p.24–25，Appendix A。
- [AUTHOR_FACT] 可扩展标注所改变的计算是：向 OpenAI o1 输入一条 MAS execution trace、MAST definitions 和来自人工标注数据的 few-shot examples，输出所观察到的 failure-mode 分类；数据发布时还为每条被识别的模式给出 reason。定位：PDF p.6，§3.3，短定位“execution trace, the MAST definitions, and few-shot examples”；p.6，§3.4，短定位“provides a corresponding reason”。
- [AUTHOR_FACT] o1 无 few-shot 时 Table 2 报告 Accuracy 0.89、Recall 0.62、Precision 0.68、F1 0.64、κ 0.58；加入 few-shot 后为 0.94、0.77、0.833、0.80、κ 0.77。定位：PDF p.6，Table 2。
- [AUTHOR_FACT] 两组干预另行改变 MAS 的 pre-execution/workflow 计算：AG2 增加结构化 verification prompt，或改为 Problem Solver、Coder、Verifier 三角色且仅 Verifier 可终止；ChatDev 则强化角色层级/边界，或把 DAG 改为 cyclic graph，并由 CTO 满足 review 后终止、另设最大迭代数。定位：PDF p.33–34，§H.1–H.2；具体 prompt 在 p.38–44，Appendix L–M。
- [READER_INTERPRETATION] 因而应区分三类“方法”：MAST 是标签/诊断表示；LLM annotator 是把轨迹映射为标签的分类器；Appendix H 的 prompt/topology changes 才是对运行中 MAS 计算流程的干预。把三者合称为单一性能提升方法会混淆诊断、标注与系统改造。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] Taxonomy 构建输入为来自 HyperAgent、AppWorld、AG2、ChatDev、MetaGPT 的 150 条轨迹，覆盖 programming 与 math；6 名人工专家使用 theoretical sampling、open coding、constant comparative analysis、memoing、theorizing，直到 theoretical saturation。定位：PDF p.5，§3.1。
- [AUTHOR_FACT] 标准化阶段每轮由 3 名专家独立标注从上述集合随机选出的 5 条轨迹，再讨论分歧、调整/增删/合并模式；共 3 轮，最终平均 Cohen’s κ=0.88。定位：PDF p.5–6，§3.2。
- [AUTHOR_FACT] LLM annotator 可用的信息包含完整 execution trace、MAST definitions、few-shot examples；其输出是每个 failure mode 是否检测到、summary、task completion、total failures（库示例），而 MAST-Data 中每个标注另有文字理由。定位：PDF p.6，§3.3–3.4；p.28，Appendix C 的 `produce_taxonomy` 示例。
- [AUTHOR_FACT] 作者把 failure 定义为“MAS 未实现预期 task objectives”的实例，但 Appendix J 又显示 failure-mode 标注也会出现在最终成功的 trace 中。定位：PDF p.2，Introduction，短定位“does not achieve its intended task objectives”；p.36，§J.1，短定位“Successful runs are not failure-free”。
- [READER_INTERPRETATION] 这里存在层级差异：task-level failure 是最终目标未达成；failure-mode occurrence 是轨迹中的局部异常行为，未必导致最终失败。后续使用数据时不能把某个 mode 出现直接等同于 task failure。
- [AUTHOR_FACT] AG2 干预发生在任务开始前的 system prompt、agent specialization 和 termination policy；ChatDev 干预发生在角色 prompt 与 orchestration topology/termination policy。它们不在同一 trace 完成后再修正答案。定位：PDF p.33–34，§H.1–H.2；p.38–44，Appendix L–M。
- [OPEN_QUESTION] 论文没有完整说明 LLM annotator 的精确 o1 版本、temperature/采样参数、最大上下文/截断策略、每种 mode 的判定阈值，以及 few-shot 样例的固定选择规则；仅说细节见 Appendix N，但 Appendix N（p.45–54）实际主要给 14 类中的若干 trace examples，并未给出完整 annotator prompt 或推理配置。
- [OPEN_QUESTION] “完整 execution trace”是否始终能装入 o1 上下文不清楚。作者称每条初始轨迹平均超过 15,000 行（p.2），但没有报告截断、分块、摘要或超长输入处理。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 对 LLM annotator，最直接基线是同一 o1、不带 few-shot；目标配置是 o1 + few-shot。Table 2 的五项指标均由后者更高。定位：PDF p.6，Table 2。
- [AUTHOR_FACT] 对 AG2，baseline 是原 MathChat（Student + 可执行 Python 的 Assistant）；两个比较条件分别为 improved prompt 和三角色 new topology。六次重复下，GPT-4 的准确率为 baseline 84.75±1.94、prompt 89.75±1.44、topology 85.50±1.18；GPT-4o 为 84.25±1.86、89.00±1.38、88.83±1.51。定位：PDF p.33–34，§H.1，Table 5。
- [AUTHOR_FACT] AG2 中 GPT-4 的 new-topology 小增益 Wilcoxon p=0.4，作者称不显著；GPT-4o 下 baseline 对 prompt 与 topology 的比较 p=0.03。定位：PDF p.33–34，§H.1。
- [AUTHOR_FACT] 对 ChatDev，baseline 与 improved prompt、new topology 比较；ProgramDev-v0 为 25.0、34.4、40.6，HumanEval 为 89.6、90.3、91.5。定位：PDF p.34，Table 5。作者在正文用 +9.4% 和 +15.6% 指代 ProgramDev-v0 上相对 baseline 的百分点增幅。定位：PDF p.3、p.8–9。
- [READER_INTERPRETATION] 就“最接近组合基线”而言，new topology 并非只多一个 agent：AG2 同时改变角色数、工具分工、对话规则与终止权限；ChatDev 同时改变图结构、review 循环、CTO 权限和最大迭代截止。因此它们是 bundled intervention，而不是单因子 topology baseline。
- [AUTHOR_FACT] Figure 5 的六个 MAS 使用不同 benchmark，作者明确写“not directly comparable”；Figure 4 也明确只用于展示 system-specific failure profiles，不用于跨 MAS 性能比较。定位：PDF p.26，Figure 5 caption；p.8，Figure 4 caption。
- [AUTHOR_FACT] 较可控的两个对比是：Figure 8 固定 MetaGPT 与 ProgramDev-v2、改变 GPT-4o/Claude-3.7-Sonnet；Figure 9 固定 GPT-4o 与 ProgramDev-v2、改变 MetaGPT/ChatDev。定位：PDF p.30，Figures 8–9 与 §F。

## 4. 模型、token、tool-call、prompt 与 oracle 差异能否解释结果？

- [AUTHOR_FACT] 作者对部分比较主动控制一个主要变量：Figure 8 固定 framework/benchmark 比模型，Figure 9 固定 model/benchmark 比 framework；§4 的 ChatDev role intervention 声称使用同一 user prompt 与 GPT-4o。定位：PDF p.7，§4，短定位“same user prompt and LLM”；p.30，§F。
- [READER_INTERPRETATION] 这只能降低模型或 framework 混杂，不能排除 token budget、API 版本、sampling、并行度、tool-call 数、运行时环境、测试 oracle 与 trace length 的影响，因为论文未给出这些量的配平或消融。
- [AUTHOR_FACT] Table 1 的主数据混合 GPT-4o、GPT-4、GPT-4o-mini、Claude-3.7-Sonnet、Qwen2.5-Coder-32B、CodeLlama-7B，并混合 ProgramDev、SWE-Bench Lite、Test-C、GSM-Plus、OlympiadBench、MMLU、GAIA；完成评估与 failure 标注又混合 HE/HA/LA。定位：PDF p.3，Table 1。
- [READER_INTERPRETATION] 因此全体 1642 traces 的 failure prevalence 适合描述这份采样混合物，但不能单凭总占比推出某个模型或某种 MAS 设计的因果失败率。
- [AUTHOR_FACT] 作者报告 annotator 成本随 trace 长度明显变化，跨 MAS 平均单条/单组成本口径文字为“average cost across all MAS frameworks is $1.8”，表中从 AppWorld 0.3740 到 OpenManus 4.1409。定位：PDF p.37，§K，Table 9。
- [OPEN_QUESTION] Table 9 的“average cost”货币单位和归一化口径不够清楚：正文写“average cost across all MAS frameworks is $1.8”且“normalized by the number of traces”，表题却为“Average failure cost by MAS framework”。无法判断是每条 trace、每个 failed trace，还是每个配置的平均 API 花费。
- [OPEN_QUESTION] 干预实验没有报告 token、turn、tool-call 或 wall-clock budget。循环 topology 允许更多迭代，三角色 topology 也可能增加调用；性能增益是否部分来自更多推理/验证预算，原文不能排除。
- [OPEN_QUESTION] ProgramDev-v0 的人工/自动成功判定 oracle 细则没有在本 PDF 中给出；HumanEval 与 ProgramDev-v0 的 oracle 强度显然不同，但 Table 5 没有说明是否统一执行环境、测试覆盖与失败判定。

## 5. 明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者两次明确表示 MAST 不穷尽所有 failure patterns，只是统一理解的第一步。定位：PDF p.2，Introduction，短定位“do not claim it covers every potential failure pattern”；p.7，§4，短定位“do not claim MAST is exhaustive”。
- [AUTHOR_FACT] 失败根因在 MAS 中复杂且可能由个体模型行为与系统设计叠加；缺少标准定义使跨系统一致标注困难。定位：PDF p.4–5，§3 与 Figure 2 前段。
- [AUTHOR_FACT] fine-grained modes 之间最高相关约 0.63，作者指出相似症状可能让自动评价器混淆不同根因。定位：PDF p.29，Appendix E，Figure 7。
- [AUTHOR_FACT] 闭源 Manus 因未披露底层模型且不给完整内部 trace，无法可靠做 MAST 细粒度标注，因此不纳入 primary MAST-Data；作者只人工评估其 ProgramDev task correctness，报告 60% success。定位：PDF p.27，§B.3。
- [AUTHOR_FACT] 战术干预有明确负向/有限结果：GPT-4 下 AG2 new topology 的小增益不显著（p=0.4）；ChatDev 虽改善但作者称不构成 substantial improvements；总体完成率仍低，单点修补不能解决全部 modes。定位：PDF p.33–34，§H.1–H.2；p.9，§5.3。
- [AUTHOR_FACT] 作者认为显式 verifier 有帮助但不是“silver bullet”；现有 verifier 常做编译、TODO 等表面检查，不能保证高层任务正确。定位：PDF p.8，§4 FC3。
- [AUTHOR_FACT] 研究覆盖 7 个 open-source frameworks，领域主要为 coding、math、general-agent tasks；开放模型仅在 ChatDev/MetaGPT 的 400 traces 上另行分析。定位：PDF p.3，Table 1；p.35–36，Appendix I，Table 6。
- [READER_INTERPRETATION] 未测试边界包括：更多自然语言、具身、多模态或真实组织协作任务；长期在线学习/记忆；不同 verifier/oracle；不同上下文长度与调用预算；闭源系统内部 failure dynamics；MAST 之外的新 failure modes。
- [AUTHOR_FACT] NeurIPS checklist 声称 Table 2 与 Table 5 报告 confidence intervals。定位：PDF p.20，checklist item 7。
- [READER_INTERPRETATION] 该说法与可见表格不完全一致：Table 2 只有点估计，无误差条/区间；Table 5 只有 AG2 四列中的两列数据带“±”，ChatDev 两列没有区间，而且正文未定义“±”是标准差、标准误还是置信区间，也未说明区间计算法。
- [OPEN_QUESTION] 人工标注样本口径需要澄清：Introduction 称 `MAST-Data-human` 为 21 条、每条 3 位专家标注（p.2）；Table 1 的前 7 个系统各 30 条均标 `HA`（p.3），合计 210 条。`HA` 是否表示至少一名人类标注、而非三专家共标，原文未明确。
- [OPEN_QUESTION] §3.4 写“two new MAS (OpenManus and Magentic-One) with two new benchmarks (MMLU and GAIA)”（p.6），但 Table 1 将 OpenManus 配 ProgramDev、Magentic-One 配 GAIA、AG2 配 MMLU；验证组合与样本数需要更清晰的对应表。
- [OPEN_QUESTION] 同一段又写最终框架包括初始 5 个、验证 2 个以及 Manus（p.6），但 §B.3 明确 Manus 不进入 primary MAST-Data（p.27）。这里很可能把 OpenManus/Manus 写混，无法仅由本文确定最终 7 个框架的叙述是否一致。
- [OPEN_QUESTION] Checklist item 12 称“不使用 existing assets”（PDF p.22），但正文明确使用多种现有 MAS、benchmark 与闭源/开源模型；这可能是 checklist 填写口径错误。

## 6. 可抽取的 Operator 与真实可记录的 Failure

### 6.1 Operator（诊断/干预操作，不等同于失败）

- [AUTHOR_FACT] Taxonomy-construction operator：theoretical sampling → open coding → constant comparison → memoing → theorizing → saturation。定位：PDF p.5，§3.1。
- [AUTHOR_FACT] Label-standardization operator：三专家独立标注随机 trace → 讨论分歧 → 修改定义/增删合并 mode → 重复三轮至 κ=0.88。定位：PDF p.5–6，§3.2。
- [AUTHOR_FACT] Scalable-annotation operator：`trace + MAST definitions + few-shot examples → o1 judge → mode flags/reasons`。定位：PDF p.6，§3.3–3.4；p.28，Appendix C。
- [AUTHOR_FACT] Prompt-role operator：明确角色职责、汇报关系、任务边界、edge cases 与 verification section。定位：PDF p.32–34，§G.1、§H；p.38–44，Appendix L–M。
- [AUTHOR_FACT] Termination-control operator：仅 Verifier/上级/CTO 在满足条件后终止，并设置最大迭代上限。定位：PDF p.33–34，§H.1–H.2。
- [AUTHOR_FACT] Topology operator：AG2 从两角色协作改为 Problem Solver/Coder/Verifier；ChatDev 从 DAG 改为 cyclic review workflow。定位：PDF p.33–34，§H.1–H.2。
- [AUTHOR_FACT] Verification operator：外部知识、生成过程测试输出、低层与高层多级检查；这些在正文中部分是建议而非均已实验。定位：PDF p.8，§4 FC3；p.32–33，§G，Table 4。
- [READER_INTERPRETATION] Appendix G 的 standardized protocols、RL、confidence thresholds、memory/state management 是作者提出或引用的策略方向；除 Appendix H 的两组战术干预外，本文没有对这些 structural strategies 做直接实验，不能记作已验证算子效果。

### 6.2 Failure（论文定义并在 trace 中给出实例的局部失败模式）

- [AUTHOR_FACT] FC1 System Design Issues：FM-1.1 Disobey task specification；FM-1.2 Disobey role specification；FM-1.3 Step repetition；FM-1.4 Loss of conversation history；FM-1.5 Unaware of termination conditions。定位：PDF p.24，Appendix A.1；实例 p.45–46、p.48–49、p.52–53。
- [AUTHOR_FACT] FC2 Inter-Agent Misalignment：FM-2.1 Conversation reset；FM-2.2 Fail to ask for clarification；FM-2.3 Task derailment；FM-2.4 Information withholding；FM-2.5 Ignored other agent’s input；FM-2.6 Reasoning-action mismatch。定位：PDF p.24–25，Appendix A.2；实例 p.45–52。
- [AUTHOR_FACT] FC3 Task Verification：FM-3.1 Premature termination；FM-3.2 No or incomplete verification；FM-3.3 Incorrect verification。定位：PDF p.25，Appendix A.3；实例 p.47–49、p.51–54。
- [AUTHOR_FACT] Figure 1 在 1642 traces 上报告 mode prevalence：1.1 11.8%、1.2 1.50%、1.3 15.7%、1.4 2.80%、1.5 12.4%；2.1 2.20%、2.2 6.80%、2.3 7.40%、2.4 0.80%（正文 p.7 写 0.85%）、2.5 1.90%、2.6 13.2%；3.1 6.20%、3.2 8.20%、3.3 9.10%。定位：PDF p.2，Figure 1；p.7–8，§4。
- [READER_INTERPRETATION] 上述百分比是 annotator 在该数据混合物中的标签出现分布，不是互斥 task-failure 概率；单 trace 可有多个 mode，成功 trace 也可含 mode。证据：PDF p.29，Figure 7 的 mode correlations；p.36，§J.1。
- [AUTHOR_FACT] Appendix N 给出可核源实例，例如：AG2 在给定答案已包含于题面时转而求另一个量（FM-2.3，p.46）；把“20 fish”误作 `$20` 成本且未核验（FM-3.2，p.47）；HyperAgent 声称 edit 已应用但执行器发现 `mode` 参数仍不存在（FM-3.1，p.53–54）。
- [READER_INTERPRETATION] “作者对成因的解释/改进建议”不应直接记作 Failure。例如 p.8 将 FC2 联系到 theory-of-mind collapse 是机制解释；真正可记录的 Failure 仍应落到具体 trace 中可观察的 withholding、ignored input、reasoning-action mismatch 等行为。

## 7. 关键判断的页码、章节、图表与短定位文本索引

| 判断 | 定位 | 短定位文本 |
|---|---|---|
| 数据规模与 failure 定义 | p.2，Introduction | “1642 annotated execution traces”；“does not achieve its intended task objectives” |
| MAST 的 14 modes / 3 categories | p.2，Figure 1；p.7–8，§4；p.24–25，Appendix A | “14 distinct failure modes” |
| Grounded Theory 构建流程 | p.5，§3.1，Figure 2 | “open coding”；“theoretical saturation” |
| 人工一致性迭代 | p.5–6，§3.2 | “three such rounds”；“κ = 0.88” |
| LLM annotator 输入与效果 | p.6，§3.3，Table 2 | “execution trace, the MAST definitions, and few-shot examples” |
| 泛化验证 | p.6，§3.4 | “Cohen’s Kappa score of 0.79” |
| 跨系统结果不可直接比较 | p.8，Figure 4 caption；p.26，Figure 5 caption | “rather than to serve as a performance comparison”；“not directly comparable” |
| 模型与架构的受控比较 | p.30–31，Figures 8–9，§F | “Effect of Underlying LLM”；“Effect of MAS Framework” |
| AG2/ChatDev 干预与准确率 | p.33–35，§H，Table 5，Figures 10–11 | “baseline, improved prompt, and new topology” |
| 成功 trace 也可含 failure mode | p.36，§J.1，Table 7 | “Successful runs are not failure-free” |
| Annotator 成本 | p.37，§K，Table 9 | “highly depends on the length of the traces” |
| 精确 prompt 干预文本 | p.38–44，Appendix L–M | “Verification Steps”；“authority to make final decisions” |
| 每类 failure 的 trace 例子 | p.45–54，Appendix N | “Where it went wrong” |

## 8. 解析文本与可视 PDF 是否冲突？

- [READER_INTERPRETATION] 54 个物理页均完成文本层读取与视觉缩略核对；关键图页 p.5、p.29–30、p.35 另作较高分辨率/裁剪检查。未发现缺页、旋转、整页扫描无文本层或正文段落在视觉版面中消失。
- [READER_INTERPRETATION] 图表页的文本层存在阅读顺序破碎，但这属于布局解析问题而非论文内容冲突：p.5 Figure 2、p.8 Figure 4、p.29 Figures 6–7、p.30 Figures 8–9、p.35 Figures 10–11 的坐标轴/图例/数字在纯文本提取中交错；视觉 PDF 中图表本身完整。因此这些页的图题、柱形关系和表格应以视觉版面为准。
- [AUTHOR_FACT] p.35 Figure 11 的可视内部图题写的是“Failure Mode Distribution Comparison: Intervention Comparison (AG2)”，但同图下方 caption 写“interventions on ChatDev”；这一不一致在可视裁剪和文本层中都出现，并非解析器伪影。
- [READER_INTERPRETATION] Figure 11 很可能沿用了 Figure 10 的 AG2 内部标题模板，但本文没有勘误说明；使用 Figure 11 时应按 caption 与 §H.3 将其理解为 ChatDev，同时保留标题冲突记录。
- [READER_INTERPRETATION] p.20 checklist 关于 Table 2/Table 5 confidence intervals 的陈述，与 p.6/p.34 可见表格不完全一致；这是论文内部陈述—表格冲突，不是解析文本—视觉 PDF 冲突。
- [OPEN_QUESTION] Figure 10/11 的大量柱值由 LLM annotator 产生，但图中样本数、每种配置的 trace 数、是否跨六次重复聚合及误差条定义没有在 caption 或 §H.3 完整说明，无法从视觉图或文本层恢复。

## 9. 本读者结论边界

- [READER_INTERPRETATION] 本报告只回答统一核源问题并区分 Operator、Failure、解释与开放问题；未生成 Card，未与其他读者结果 reconciliation，未进行 Candidate、novelty 或科研价值评价。
