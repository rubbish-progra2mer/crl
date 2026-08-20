# P016 独立二读核源报告

## 0. 身份、边界与结论摘要

- 本报告对应冻结的 invocation snapshot：`r2-20260719-p016-a1/invocation.md`，Attempt ID `r2-20260719-p016-a1`，启动时间 `2026-07-19T15:49:01+08:00`。
- [AUTHOR_FACT] 论文为 *Why Do Multi-Agent LLM Systems Fail?*，NeurIPS 2025 Datasets & Benchmarks，PDF 共 54 页。实算 PDF SHA-256 为 `6aff168d6e201217d3f79611f6ad024590a599a03b97ac2aeb0b0b128bac374c`，与 invocation 一致。统一提示词实算 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，也与 invocation 一致。
- [READER_INTERPRETATION] 本文的主贡献不是一个直接提升任务性能的新推理算法，而是三层工作：以人工 Grounded Theory 构建 14 类失败模式的 MAST；形成 1642 条带标注轨迹的 MAST-Data；以 few-shot o1 作为 LLM annotator 扩展标注。AG2 与 ChatDev 的 prompt/topology 干预是用于展示 MAST 诊断用途的附录案例研究，不应与主数据集/分类方法混为一个“方法”。定位：PDF pp.1–10，尤其 §3、§4、§5；附录 §H，pp.33–35。
- [AUTHOR_FACT] 关键核对结论：§H.3 文字声称两种 intervention 在 AG2 和 ChatDev 上都使不同 failure modes 减少，并称 topology 对两系统都更有效；图 10 的 AG2 数值却显示 prompt intervention 的三类失败计数全部增加，而 topology intervention 才明显减少。图 11 的 ChatDev 数值与文字一致，两种 intervention 都减少，且 topology 减少更多。定位：PDF p.34 §H.3 短定位“both of these interventions cause a decrease”；p.35 Figures 10–11。
- [READER_INTERPRETATION] 因而，关于“两个干预是否减少 failures”的统一答案是：**不能笼统回答都减少**。ChatDev：prompt 与 topology 均减少；AG2：topology 减少，但 prompt 按图 10 的失败计数反而增加。任务正确率与失败模式计数不是同一指标，AG2 prompt 可以提高正确率同时出现更多局部失败标签；这并不能挽救 §H.3 对“failure counts decrease”的直接文字—图表冲突。定位：PDF p.34 Table 5；p.35 Figures 10–11；p.36 §J.1 对“successful runs are not failure-free”的说明。

## 1. 统一问题 1：方法究竟改变哪一步计算？

- [AUTHOR_FACT] MAST 构建改变的是“如何从 MAS execution trace 识别并标准化失败”的分析/标注步骤。六位专家先对五个 MAS 的 150 条轨迹进行 Grounded Theory：open coding、constant comparative analysis、memoing、theorizing，直至理论饱和；之后三位专家在多轮 IAA 中迭代修改、增加、删除或合并 failure-mode 定义，最终得到 14 个 failure modes、3 个 categories。定位：PDF pp.5–6，§3.1–§3.2；短定位“theoretical saturation”“adjusting failure mode definitions”。
- [AUTHOR_FACT] LLM annotator 改变的是大规模标注计算：输入 execution trace、MAST 定义及人类标注 few-shot examples，让 OpenAI o1 输出 failure-mode 分类。few-shot 相比无 few-shot 的 o1，从 accuracy 0.89 / κ 0.58 提升到 accuracy 0.94 / κ 0.77；recall 0.77、precision 0.833、F1 0.80。定位：PDF p.6，§3.3，Table 2。
- [AUTHOR_FACT] AG2 的 prompt intervention 在原 prompt 中增加更清晰结构、缺失数据处理和显式 VERIFICATION section；topology intervention 改为 Problem Solver、Coder、Verifier 三角色，只有 Verifier 可在获得两条解法后终止。定位：PDF pp.33、38–41，§H.1、§L.1–§L.6。
- [AUTHOR_FACT] ChatDev 的 prompt intervention 强化角色层级、只有上级/CEO 可最终结束、测试者需检查 task-specific edge cases；topology intervention 把 DAG 改为 cyclic graph，只有 CTO 确认 reviews 满足后才终止，并设最大迭代上限。定位：PDF p.34 §H.2；pp.42–44 §M。

## 2. 统一问题 2：输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 人工 taxonomy 阶段输入是五个开源 MAS、编程和数学任务的 150 条完整轨迹；输出是经 IAA 精炼的 MAST 定义。初始分析平均每位专家超过 20 小时，三轮分歧解决约 10 小时，最终 κ=0.88。定位：PDF pp.5–6，§3.1–§3.2。
- [AUTHOR_FACT] LLM annotator 可用信息为完整 execution trace、MAST definitions、few-shot human examples；输出为 failure-mode labels 与理由。附录库接口还展示 `summary`、`task_completion`、`total_failures` 字段。定位：PDF p.6 §3.3；p.28 §C。
- [READER_INTERPRETATION] MAST/LLM annotator 是**执行后**对轨迹的诊断与标注；AG2/ChatDev 的 prompt、角色和 topology 修改发生在**执行前设计**，而 verifier/termination/cyclic review 在**执行中**改变信息流与终止条件。定位：PDF Figure 1 p.2；§H pp.33–35；§L–M pp.38–44。
- [AUTHOR_FACT] MAST-Data 的输出规模为 1642 条来自 7 个开源 MAS 的标注轨迹；任务覆盖 coding、math、general-agent。作者另发布 MAST-Data-human。定位：PDF pp.2–6，Table 1、§3.4。
- [OPEN_QUESTION] 论文未在 Table 5 或 Figures 10–11 附近完整披露每个干预配置的 token 数、LLM call 数、tool-call 数、平均轮次、失败计数归一化分母；因此无法从 PDF 单独判断干预后的失败计数差异是否同时伴随显著不同的计算预算。

## 3. 统一问题 3：最强基线与最接近组合基线

- [AUTHOR_FACT] 对 LLM annotator，直接基线是同一 o1 模型但不使用 few-shot：Table 2 的 `o1`；主配置是 `o1 (few shot)`。人类专家标签是校准/验证参照，不是普通模型基线。定位：PDF p.6，Table 2。
- [AUTHOR_FACT] 对 AG2/ChatDev 干预，matched baseline 是各框架原始实现；比较臂为 improved prompt 与 new topology。定位：PDF pp.33–34，§H.1–§H.2、Table 5。
- [AUTHOR_FACT] Figure 4 明示不同 MAS 使用的任务/benchmark 可能不同，结果用于展示系统特定 failure profile，不能作为 MAS 性能比较。Figure 5 同样说明不同 benchmark 上的性能不可直接比较。定位：PDF p.8 Figure 4 caption；p.26 Figure 5 caption。
- [READER_INTERPRETATION] 对“taxonomy/dataset 是否优于既有方法”，正文 Related Work 只做定性定位，没有一个覆盖相同七系统、相同轨迹、相同标签空间的组合基线实验；因此不存在可从本文报告中确认的“最强外部组合基线”。定位：PDF p.4 §2。
- [OPEN_QUESTION] few-shot o1 的示例数、选择规则及是否与某些测试轨迹/系统存在语义近邻关系，正文仅指向 prompt/examples，PDF 中没有足够信息完成泄漏审计。

## 4. 统一问题 4：模型、token、tool-call、prompt 或 oracle 差异

- [AUTHOR_FACT] 大规模 MAST-Data 混合 GPT-4 系、Claude 3、Qwen2.5、CodeLlama，并混合 coding、math、general-agent benchmark；无控制地跨行比较可能把模型、任务和系统设计差异混在一起。定位：PDF pp.1–3，Table 1；p.8 Figure 4 disclaimer。
- [AUTHOR_FACT] Appendix F 做了两个较受控比较：MetaGPT 内固定 framework/ProgramDev-v2，比 GPT-4o 与 Claude 3.7；固定 GPT-4o/ProgramDev-v2，比 MetaGPT 与 ChatDev。定位：PDF pp.30–31，Figures 8–9、§F。
- [READER_INTERPRETATION] 即使 Appendix F 固定了主要两项因素，PDF 仍未报告两模型的 token、sampling、调用次数、费用、工具权限是否完全匹配；只能称“控制了 framework/benchmark”或“控制了 model/benchmark”，不能称严格计算预算等价。
- [AUTHOR_FACT] AG2 topology 增加独立 Coder、Problem Solver、Verifier，Coder 可执行 Python，且 Verifier 控制终止；因此它与 baseline/improved-prompt 不只是 topology 名称不同，也潜在改变 LLM call、对话轮次、工具执行和 token 使用。定位：PDF pp.33、39–41。
- [AUTHOR_FACT] ChatDev topology 允许循环复审并设最大迭代；这也会改变执行步数/调用预算。定位：PDF p.34 §H.2。
- [OPEN_QUESTION] Table 5 的 ChatDev 两列未标模型、未给重复次数/误差项；正文虽在其他位置称 ChatDev prompt 改动保持 GPT-4o 与 user prompt 相同，但 topology 的具体调用预算及所有控制项未完整列出。定位：PDF p.7 FC1；p.34 Table 5。
- [AUTHOR_FACT] 论文使用 HE、HA、LA 三种来源：task completion 有 human evaluation，failure modes 有 human annotation 或 LLM annotation；Figures 10–11 明示 failure 分布由 automated LLM-as-a-Judge 得到。定位：PDF p.3 Table 1；p.35 captions。
- [READER_INTERPRETATION] failure 分布不是独立客观 oracle，而是 κ=0.77 的自动标注器输出；图中变化可能部分受到 judge 对不同长度、角色格式和 topology trace 的敏感性影响。论文未给 intervention plots 的人工复核率。
- [AUTHOR_FACT] Checklist p.20 声称“all of these LLMs are proprietary”且无需 GPU，但 Table 1、Appendix I 明确包含 Qwen2.5-Coder 与 CodeLlama 开源模型。两处文字不一致。定位：PDF p.20 Checklist item 8；pp.3、35–36 Table 1、§I/Table 6。

## 5. 统一问题 5：限制、负向结果和未测试边界

- [AUTHOR_FACT] 作者明确不声称 MAST 穷尽所有 MAS failure patterns。定位：PDF p.2 Introduction；p.7 §4；p.17 Checklist item 2。
- [AUTHOR_FACT] closed-source Manus 因底层模型与完整 agent trace 不透明，不能纳入 MAST-Data 的细粒度标注；仅做了部分人类任务正确性评估。定位：PDF p.27 §B.3。
- [AUTHOR_FACT] LLM annotator 虽 accuracy 0.94，但 recall 0.77、κ 0.77，不是无误差标签器；zero-shot o1 的 recall 0.62、κ 0.58。定位：PDF p.6 Table 2。
- [AUTHOR_FACT] AG2 的 negative/heterogeneous result：GPT-4 下 improved prompt 明显高于 baseline，但 new topology 只有小幅提升；Wilcoxon p=0.4，作者称不显著。GPT-4o 下 baseline 对 improved prompt 和 new topology 的比较 p=0.03。定位：PDF pp.33–34，§H.1、Table 5。
- [AUTHOR_FACT] 作者承认 tactical interventions 不普适、取决于 underlying LLM；ChatDev 改进仍“不构成 substantial improvements”，需要更综合的结构方案。定位：PDF pp.33–34，§H.1–§H.2。
- [AUTHOR_FACT] Table 5 的任务正确率：AG2/GPT-4 为 84.75±1.94（baseline）、89.75±1.44（prompt）、85.50±1.18（topology）；AG2/GPT-4o 为 84.25±1.86、89.00±1.38、88.83±1.51。ChatDev ProgramDev-v0 为 25.0、34.4、40.6；HumanEval 为 89.6、90.3、91.5。定位：PDF p.34 Table 5；已对可视表格核对。
- [OPEN_QUESTION] Table 5 未说明“±”究竟是标准差、标准误还是置信区间；ChatDev 无误差项和显著性检验。Checklist p.20 却称 Tables 2/5 报告 confidence intervals，而 Table 2 没有 CI，Table 5 也未定义 ±。该统计报告不足以支持更强的精确比较。
- [OPEN_QUESTION] 未测试边界至少包括：更多 closed-source MAS、无法获取完整 trace 的平台、视觉/实体多智能体任务、长期在线运行、安全对抗场景，以及 intervention 在 Table 5 以外的模型/benchmark 上的稳定性。

## 6. 统一问题 6：可抽取的 Operator 与真实可记录 Failure

以下仅作源内结构化区分，不生成 Card，也不评价 Candidate 或科研价值。

### 6.1 可抽取为 Operator 的论文内操作

- [AUTHOR_FACT] `Trace -> open coding/constant comparison/memoing/theorizing -> saturation`。定位：PDF p.5 §3.1。
- [AUTHOR_FACT] `多专家独立标注 -> 讨论分歧 -> 修改/增删/合并标签 -> 重复至高 IAA`。定位：PDF pp.5–6 §3.2。
- [AUTHOR_FACT] `Trace + MAST definitions + few-shot human examples -> o1 multi-label failure annotation + reason`。定位：PDF p.6 §3.3。
- [AUTHOR_FACT] `增加显式 verification prompt`、`拆分 Problem Solver/Coder/Verifier 并由 Verifier 终止`。定位：PDF pp.33、38–41 §H.1、§L。
- [AUTHOR_FACT] `强化 ChatDev 层级/edge-case prompts`、`DAG 改 cyclic review，CTO 确认后终止`。定位：PDF p.34 §H.2；pp.42–44 §M。
- [READER_INTERPRETATION] 上述 operator 分为“事后诊断标注 operator”和“事前/执行中系统干预 operator”；混用会把“测量失败”误说成“修复失败”。

### 6.2 真实可记录的 Failure

- [AUTHOR_FACT] 论文给出的 run-level failure 定义是 MAS 未达到 intended task objectives。定位：PDF p.2，短定位“does not achieve its intended task objectives”。
- [AUTHOR_FACT] MAST 的 14 个可记录 trace-level failure modes 是：
  - FC1 System Design：FM-1.1 Disobey task specification；1.2 Disobey role specification；1.3 Step repetition；1.4 Loss of conversation history；1.5 Unaware of termination conditions。定位：PDF pp.24–25 §A.1。
  - FC2 Inter-Agent Misalignment：FM-2.1 Conversation reset；2.2 Fail to ask for clarification；2.3 Task derailment；2.4 Information withholding；2.5 Ignored other agent’s input；2.6 Reasoning-action mismatch。定位：PDF pp.24–25 §A.2。
  - FC3 Task Verification：FM-3.1 Premature termination；3.2 No or incomplete verification；3.3 Incorrect verification。定位：PDF p.25 §A.3。
- [AUTHOR_FACT] Appendix N 给出轨迹短证据：重复/重置/角色违背（p.45 N.1）、停止条件不识别（pp.45–46 N.2）、任务跑偏（p.46 N.3）、不澄清（pp.46–47 N.4）、验证缺失/错误（pp.47–49 N.5–N.9）、reasoning-action mismatch（pp.49–51 N.10）、忽略他人输入（pp.51–52 N.11）、历史丢失（pp.52–53 N.12）、过早终止（pp.53–54 N.13）。
- [AUTHOR_FACT] 成功 run 也可能含 failure-mode occurrence；failed traces 只是总体频率更高。定位：PDF p.36 §J.1、Table 7。
- [READER_INTERPRETATION] 因此应分别记录 `最终任务失败` 与 `局部 failure-mode occurrence`。不能仅因自动 judge 给出某个 mode 就推断该 run 最终失败；也不能因最终成功就抹去局部失败。

## 7. 干预文字—表格—图形专项核对

### 7.1 AG2

- [AUTHOR_FACT] Table 5 显示 prompt 在 GPT-4/GPT-4o 的任务正确率都高于 baseline；topology 在两模型也高于 baseline，但 GPT-4 的小幅增益作者报告 p=0.4、不显著。定位：PDF pp.33–34。
- [AUTHOR_FACT] Figure 10 三类 failure counts（按图例 Original / Prompt Intervention / Topology Intervention）分别为：

  | AG2 failure category | Original | Prompt | Topology |
  |---|---:|---:|---:|
  | System Design Issues | 625 | 687 | 171 |
  | Inter-Agent Misalignment | 692 | 796 | 205 |
  | Verification Issues | 305 | 335 | 86 |
  | 合计（多标签计数） | 1622 | 1818 | 462 |

- [READER_INTERPRETATION] Prompt 相比 Original 是 `+196`（约 `+12.1%`），三类均增加；Topology 是 `-1160`（约 `-71.5%`），三类均减少。故 §H.3 的“both interventions decrease failures”对 AG2 prompt 不成立；“topology 更有效”与图一致。定位：PDF p.35 Figure 10 与 p.34 §H.3。

### 7.2 ChatDev

- [AUTHOR_FACT] Table 5 显示 prompt/topology 的 ProgramDev-v0 与 HumanEval 正确率都高于 baseline。定位：PDF p.34 Table 5。
- [AUTHOR_FACT] Figure 11 三类 failure counts 分别为：

  | ChatDev failure category | Original | Prompt | Topology |
  |---|---:|---:|---:|
  | System Design Issues | 424 | 372 | 355 |
  | Inter-Agent Misalignment | 447 | 403 | 376 |
  | Verification Issues | 209 | 176 | 169 |
  | 合计（多标签计数） | 1080 | 951 | 900 |

- [READER_INTERPRETATION] Prompt 相比 Original 为 `-129`（约 `-11.9%`），Topology 为 `-180`（约 `-16.7%`）；三类均下降。§H.3 关于 ChatDev 的文字与图一致，且 topology 的下降更大。
- [AUTHOR_FACT] Figure 11 的图内大标题仍写“(AG2)”，但图注写 ChatDev，周边 §H.3 也将 Figure 11 指向 ChatDev。定位：PDF p.35 Figure 11。
- [READER_INTERPRETATION] 这很可能是图内标题复制未改，但仅凭 PDF 应记录为标签冲突，不能静默替作者修正。

### 7.3 指标口径

- [AUTHOR_FACT] Figures 10–11 是 automated LLM-as-a-Judge 的 failure-mode **occurrence counts**，一个 trace 可有多个模式；Table 5 是 task accuracy。定位：PDF pp.34–35。
- [READER_INTERPRETATION] 因此 Table 5 的正确率提升与 Figure 10 的 AG2 prompt failure counts 上升可以同时发生；真正不可调和的是 §H.3 把 Figure 10 描述成“下降”。
- [OPEN_QUESTION] Figures 10–11 未在图注定义计数分母、是否汇总六次 repetitions、各配置实际 trace 数是否完全相同。未给人工复核或计数不确定性。

## 8. 统一问题 7：判断定位索引

| 判断主题 | PDF 定位 | 图表/短定位 |
|---|---|---|
| 数据规模与失败定义 | pp.2–3, Introduction | Table 1；“1642 annotated execution traces” |
| Taxonomy 构建 | pp.5–6, §3.1–3.2 | Figure 2；κ=0.88 |
| LLM annotator | p.6, §3.3 | Table 2；o1 vs o1 few shot |
| 14 个 failure modes | pp.7–8, §4；pp.24–25, §A | Figure 1、Appendix A |
| 不同系统不可直接比较 | p.8；p.26 | Figure 4/5 captions |
| 模型/架构受控比较 | pp.30–31, §F | Figures 8–9 |
| AG2 intervention | pp.33–34, §H.1；pp.38–41, §L | Table 5、prompt 全文 |
| ChatDev intervention | p.34, §H.2；pp.42–44, §M | Table 5、prompt 全文 |
| failure 分布冲突 | pp.34–35, §H.3 | Figures 10–11 |
| 成功轨迹也有局部 failure | p.36, §J.1 | Table 7 |
| 失败实例 | pp.45–54, §N | N.1–N.13 |

## 9. 统一问题 8：解析文本与可视 PDF 是否冲突

- [AUTHOR_FACT] 对 p.34 Table 5 做可视核对，表中数值与解析文本一致。
- [AUTHOR_FACT] 对 p.35 Figures 10–11 做可视核对并辅以 PDF word bounding boxes，柱上数值与本报告 §7 的转录一致。
- [AUTHOR_FACT] 实质冲突一：§H.3 文字声称 AG2 prompt 减少 failures，但 Figure 10 三类计数均上升。
- [AUTHOR_FACT] 标签冲突二：Figure 11 图内标题写“(AG2)”，图注与上下文写 ChatDev。
- [AUTHOR_FACT] 范围冲突三：Introduction p.2 称 7 个系统的 failure rate 详见 Figure 5；Figure 5 p.26 实际只画 6 个系统，图注也写 six，未画 OpenManus。
- [AUTHOR_FACT] 文档冲突四：Checklist p.20 称所有所用 LLM 都是 proprietary；Table 1 与 §I/Table 6 明列 Qwen2.5、CodeLlama 开源模型。
- [READER_INTERPRETATION] p.5 等含复杂矢量图的页面，按阅读顺序抽取的文本布局严重错乱，这是解析层布局问题；结合可见页面、caption 与后续正文后未据此提出额外语义冲突。
- [OPEN_QUESTION] 本次未进行外部代码、原始数据或论文仓库复算，因此图 10/11 柱值之外的生成过程与数据一致性仍未独立验证。

## 10. 实际读取、工具与可观察 trace

### 10.1 实际读取文件

研究核源输入实际仅使用以下三项指定文件：

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P016_mast_failures.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P016/read_2_attempts/r2-20260719-p016-a1/invocation.md`

另因上层执行规则要求，在开始 PDF 操作前读取了非研究内容的执行技能文件 `C:/Users/g/.codex/skills/pdf/SKILL.md`；它只提供 PDF 工具使用说明，未提供任何 P016 研究结论、首读信息或工作区内容。除此之外未读取 read_1、Cards、其他读者报告、blind query 或其他项目文件；未枚举工作区。

### 10.2 写入

- 唯一写入：本文件 `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P016/read_2_attempts/r2-20260719-p016-a1/report.md`。
- 未生成 Card，未生成 Candidate/novelty/科研价值评价文件，未生成临时页面图片。

### 10.3 使用工具

- PowerShell `Get-Content -LiteralPath ... -Raw -Encoding utf8`：读取 prompt 与 invocation；首次未显式指定 UTF-8 时出现 mojibake，随后以 UTF-8 重新读取。
- PowerShell `Get-FileHash -Algorithm SHA256`：校验 PDF、prompt、invocation。invocation 实算 SHA-256 为 `40a598bfbd...f0811`（snapshot 本身未预声明该值）。
- Python 3 + PyMuPDF (`fitz`)：只读打开指定 PDF；获取 54 页页数/metadata；按页 1–54 分块提取文本；提取 p.35 word-level bounding boxes；在内存中 rasterize p.34–35 关键表图及 p.26/p.30 图表进行可视核对。未把渲染页写入磁盘。
- 首次整本提取在 PDF p.1 因控制台 GBK 无法编码字符而以 `UnicodeEncodeError` 失败；设置 `PYTHONIOENCODING=utf-8` 后按页段完成 1–54 页读取。
- `apply_patch`：创建本报告。
- 网络工具：未使用；未联网。

### 10.4 模型、任务与隔离状态

- Actual model/version：Codex（系统上下文说明为 GPT-5-based）；精确模型版本/构建号不可见，`unknown`。
- Canonical task identifier：`/root/p016_second_read`。
- Thread ID：不可见，`unavailable`。
- 可验证 path allowlist：App 未提供，`unavailable`。
- 隔离状态：`procedural_blinding`。文件系统权限并非技术隔离；本报告不声称存在技术文件级隔离。
- 可观察 file-access trace：仅能据本次显式工具调用如上列出；操作系统/宿主层的完整审计日志不可见，`unavailable`。

