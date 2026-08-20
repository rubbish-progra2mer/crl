# P034 独立第三读报告

## Provenance 与边界

- Attempt：`r3-20260719-p034-a1`。
- 冻结 invocation：`knowledge_base/corpus/reads/P034/read_3_attempts/r3-20260719-p034-a1/invocation.md`。
- 原文：`knowledge_base/staging/papers/P034_refinebench.pdf`，44 个物理页；实测 SHA-256 为 `ee5c4d93ddf6c0741f0d08042b6aca2e0f08c3d3bd70e6cc6c90378bbc2d8c7f`，与 invocation 一致。
- 统一模板：`knowledge_base/templates/second_read_prompt.md`；实测 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，与 invocation 一致。
- 阅读方式：逐物理页解析并人工判断全文；对关键物理页 4、8、9、11 做了内存渲染视觉复核。以下 locator 中的页码均为 PDF 物理页码。

## 核心结论

1. `[AUTHOR_FACT]` REFINEBENCH 是一个 1,000 题、11 个领域、两种任务类型（free-form/exact match）的五轮 refinement 基准；每题平均 9.9 个二值 checklist items。Locator：物理页 4–7，§3、Tables 1–2、§4.1。
2. `[AUTHOR_FACT]` self-refinement 的目标模型不接收显式反馈，只收到“若绝无可改则 `[TERMINATE]`，否则继续改写”的通用提示；guided refinement 则把上一轮未通过的 checklist items 启发式改写成反馈并交给目标模型。Locator：物理页 5，§3.2；物理页 25，Appendix G.1。
3. `[READER_INTERPRETATION]` 因此该 benchmark 的 self-refinement 更准确地说是“无缺陷定位信息的重复修订”；guided refinement 是“由参考答案派生 checklist、GPT-4.1 判错、再把失败项送回”的强定向反馈条件。两者之差包含额外信息，不是同信息条件下两种内生算法的纯比较。
4. `[AUTHOR_FACT]` 以严格全项通过指标 `Pass` 看，Gemini-2.5-Pro 从 29.5 到 31.3（+1.8），GPT-5 从 27.5 到 29.1（+1.7），DeepSeek-R1 从 8.1 到 7.9（表中记 -0.1）；多数模型无明显提升或下降。Locator：物理页 7–8，§4.2、Table 3。
5. `[AUTHOR_FACT]` 更细的 checklist item 比例 `Acc` 揭示了主文 `Pass` 摘要掩盖的退化：Gemini-2.5-Pro 为 `72.5 -> 71.4`（-1.1），DeepSeek-R1 为 `44.8 -> 34.5`（-10.3）；不少 instruction-tuned 模型也下降。Locator：物理页 21，Table 7。
6. `[READER_INTERPRETATION]` 论文能直接反证的是：在这一题集、这一通用自改 prompt、这些推理配置、最多五轮、以 GPT-4.1/checklist 评分时，重复无指导修订通常不能稳定提高。它不能反证带自生成 critique、不同 scaffold、验证器、搜索、工具反馈、训练后 critic 或其他停止/选稿策略的一般 self-refinement。
7. `[AUTHOR_FACT]` 论文限制段明确写明，这些趋势“不必然意味着 LMs 缺乏 self-refine 能力”，结果可能随领域、难度、prompt scaffold 与推理配置变化。Locator：物理页 17，Appendix B。

## 统一问题清单

### 1. 任务定义与被改变的计算

- `[AUTHOR_FACT]` 第 1 轮由输入查询 `x1` 生成初答 `y1`；后续轮由当前查询 `xt` 与上一答案 `yt-1` 生成修订 `yt`。每轮随后由独立 evaluator LM 对 checklist 逐项判 Yes/No，最多到第 5 轮。Locator：物理页 4–5，Figure 2、§3.2。
- `[AUTHOR_FACT]` self-refinement 中 `ft` 为空，目标模型自行决定停止或继续；guided 中未通过项形成下一轮反馈；partial-guided 只暴露按比例选出的部分 items。Locator：物理页 5，§3.2 “Providing Feedback”。
- `[READER_INTERPRETATION]` 可抽取的 benchmark Operator 是：`上一答条件式修订 -> 外部 checklist 逐项判定 -> 可选地把失败条件回注 -> 最多五轮/模型自报停止`。

### 2. 输入、输出、可用信息、干预时点

- `[AUTHOR_FACT]` 目标模型始终看到原问题和上一轮回答；self 条件看不到 checklist 或失败项，guided 条件在下一轮看到失败 checklist 的命令式改写。Locator：物理页 4–5，Figure 2、§3.2；物理页 25，Appendix G.1。
- `[AUTHOR_FACT]` evaluator GPT-4.1 看到 query、完整 model answer 与完整 checklist，只输出逐项 Yes/No。Locator：物理页 5，§3.2；物理页 25–26，Appendix G.2。
- `[AUTHOR_FACT]` 全 checklist“criteria”实验把完整评价标准给目标模型，但不提供如何修正；两例模型的 Pass5 明显上升：LLaMA-3.1-70B-Instruct 从无 criteria 的 4.6 到 48.2，Gemini-2.5-Pro 从 31.3 到 75.8。Locator：物理页 8–9，Table 4。
- `[READER_INTERPRETATION]` 这支持“缺陷/目标维度定位是瓶颈”这一局部解释，但证据仅来自两个模型且 criteria 本身由参考答案派生；不能把它视为普遍因果定律。

### 3. 评价者信息与 checklist 来源

- `[AUTHOR_FACT]` 多数题原本没有 checklist；作者以 GPT-4o、GPT-4.1、Claude-Sonnet-3.7 结合原题和参考答案生成，再人工审阅迭代。随后用 GPT-4.1 对参考答案回测，过滤其判 No 的 items，过滤率 1.1%。Locator：物理页 5，§3.1 Steps 2–3。
- `[AUTHOR_FACT]` 人工 checklist 质量评估覆盖 100 个样本、854 items，96.1% 被判为 appropriate。Locator：物理页 5，§3.1；物理页 21–23，Appendix E.4、Figure 11。
- `[AUTHOR_FACT]` response appropriateness 的人工评估对每个 sampled instance 随机抽一个 checklist item，并随机抽取 18 个模型之一的输出；meta-evaluation 中 GPT-4.1 与人工判断一致率为 90%，高于另五个 evaluator LMs。Locator：物理页 21–23，Appendix E.4–E.5、Table 9。
- `[READER_INTERPRETATION]` 90% 一致率是有力但不完美的验证；剩余 evaluator 误差足以影响严格的 `Pass`，因为任一 item 判错都会改变整题是否全通过。
- `[READER_INTERPRETATION]` GPT-4.1 同时参与 checklist 生成候选、reference-answer 过滤和最终评价，形成共享评价器的依赖；人工抽检缓解但没有对全部 9,898 items 与全部多轮输出建立金标准。

### 4. 指标与迭代退化

- `[AUTHOR_FACT]` `Acc_t=100*Nc/N` 衡量每题通过 checklist item 的比例；`Pass_t` 只有全部 N 项都正确才记 1，再跨实例平均。Locator：物理页 7，§4.1。
- `[AUTHOR_FACT]` Table 7 显示很多模型即使 `Pass` 变化很小，`Acc` 仍显著下降；例如 LLaMA-3.1-70B-Instruct 的 `Acc` 为 `35.0 -> 29.1`，GPT-4.1 为 `67.9 -> 64.2`。Locator：物理页 21，Table 7。
- `[AUTHOR_FACT]` DeepSeek-R1 的转移分析显示第 2->3 轮有 19.1% 从 correct 转为 incorrect，只有 8.1% 从 incorrect 转为 correct；后续错误保持超过 64%。Locator：物理页 11，§5.3、Figure 9。
- `[READER_INTERPRETATION]` 这构成直接的“修订会破坏先前正确内容”证据，且比仅看最终平均增量更能说明迭代退化。
- `[AUTHOR_FACT]` DeepSeek-R1 从第 1 轮到第 2 轮平均 reasoning tokens 下降 69.7%，作者的关键词分析认为后续自纠/验证模式减少。Locator：物理页 10–11，§5.3、Figure 8。
- `[READER_INTERPRETATION]` 关键词计数只支持行为表征的相关性，不足以证明 token 下降导致性能下降；论文限制段也要求更精确分析。Locator：物理页 17，Appendix B。

### 5. 缺陷定位条件与 guided refinement

- `[AUTHOR_FACT]` guided feedback 直接来自 evaluator 判为未满足的 checklist items，并将诸如问句“Does the response...”启发式改为“The response should...”。Locator：物理页 5，§3.2；物理页 25，Appendix G.1。
- `[AUTHOR_FACT]` guided 条件下多数大模型到第 5 轮接近高 Pass；例如 Claude-Opus-4.1 达 98.4，o3-mini 达 98.2，Gemini-2.5-Pro 达 94.7。Locator：物理页 8，Table 3；物理页 22，Table 8。
- `[AUTHOR_FACT]` 50% partial-guided 分析显示模型更能修复已提供 feedback 的 items，对未提供 items 仍困难。Locator：物理页 8–9，§5.1、Figure 4。
- `[OPEN_QUESTION]` Figure 4 给趋势图但正文未在同处报告每一类 known/unknown items 的完整数值表、抽样方式与不确定区间；“能纳入反馈但难自找缺陷”的强度需要代码/数据级复核。
- `[READER_INTERPRETATION]` guided 的近满分体现对非常具体、逐项且由参考答案派生的反馈之遵循能力；它不等价于真实用户提供的模糊、错误、不完整或彼此冲突的反馈。

### 6. 停止条件与预算差异

- `[AUTHOR_FACT]` self-refinement prompt 允许模型输出 `[TERMINATE]`，协议最大 5 轮；大多数模型平均在第 3–4 轮附近停止，即使最佳 Pass5 仍低于 32。Locator：物理页 9，Figure 6 与§5.2；物理页 25，Appendix G.1。
- `[OPEN_QUESTION]` 原文未清楚说明模型提前 `[TERMINATE]` 后，Table 3/7 中后续 turn 分数是沿用、重评还是以其他方式填充；该实现细节影响逐轮曲线解释。
- `[AUTHOR_FACT]` 统一推理设置为 top-p 0.9、temperature 1.0、max tokens 10,000；reasoning models 设 10,000 tokens，OpenAI 系列 reasoning effort 为 medium。Evaluator 为 top-p 1.0、temperature 0、max tokens 10,000。Locator：物理页 20，Appendix E.1。
- `[READER_INTERPRETATION]` 相同上限不等于相同实际 token/延迟/成本；不同模型会提前停止且输出长度不同。论文的同模型跨轮趋势比跨模型绝对高低更接近受控比较。
- `[AUTHOR_FACT]` 作者报告 Gemini-2.5-Pro 每样本 evaluator 成本/延迟：self 为 `$0.038/51.1s`，guided 为 `$0.028/22.9s`。Locator：物理页 10，§5.2。

### 7. 外部有效性与未测试边界

- `[AUTHOR_FACT]` 题目分布并不均衡：Math 32%，Humanities/Social Science 19%，Law 14%；总计 11 domains。Locator：物理页 6，Figure 3；物理页 18，Table 5。
- `[AUTHOR_FACT]` 非文本图表被 GPT-4o/GPT-4.1/Claude-Sonnet-3.7 转成文字或 markdown，再由作者人工核对。Locator：物理页 4–5，§3.1 Step 1。
- `[READER_INTERPRETATION]` 因此 benchmark 测的是文字化材料理解，不直接覆盖原生视觉输入下的 refinement。
- `[AUTHOR_FACT]` 论文自身限制包括领域、难度、prompt scaffold 与 inference configuration 依赖；DeepSeek 分析主要依赖关键词搜索。Locator：物理页 17，Appendix B。
- `[AUTHOR_FACT]` 污染分析只用 Min-K% Prob 在 LLaMA2-13B 上检测，报告问题/参考答案污染率 0.1%/0.5%。Locator：物理页 19–20，Appendix D.4。
- `[READER_INTERPRETATION]` 该单模型检测不能建立 34 个被测前沿模型均无污染；尤其 benchmark 来源含公开考试与既有公开数据，污染结论应限于所用检测器与代理模型。
- `[OPEN_QUESTION]` 未测试的关键边界包括：自生成结构化 critique、独立 critic、工具/检索/执行反馈、多候选搜索与 reranking、不同温度/更高 token、训练后的自纠模型，以及超出五轮的策略。

### 8. 内部报告问题与 locator 风险

- `[OPEN_QUESTION]` 物理页 9 把线性回归结果写为 `R^2=-0.477`；常规定义下带截距 OLS 的 `R^2` 不应为负，且负号更像相关系数。未提供回归细节前，不应把该数值解释为标准决定系数。
- `[AUTHOR_FACT]` Table 3/7 的 DeepSeek-R1 `Pass` 从 8.1 到 7.9，而表中 delta 记 -0.1；按显示的一位小数直接相减为 -0.2，可能来自未四舍五入底层值。Locator：物理页 8、21，Tables 3、7。
- `[READER_INTERPRETATION]` 因表中数值已四舍五入，delta 应优先视作作者从未舍入数值计算，而不是自行断言算术错误。

### 9. 解析文本与可视 PDF

- `[AUTHOR_FACT]` 44 个物理页均成功抽取文本；先前批量输出中物理页 5 有一处工具显示截断，已单页重新完整抽取。关键页 4、8、9、11 经可视复核，协议图、主表、停止/域分析图和转移图与上述结论一致。
- `[READER_INTERPRETATION]` 解析文本对多栏表格、数学符号和图中文字存在列拼接噪声，因此数字判断以表头、正文说明与关键页视觉复核交叉确认。
- `[OPEN_QUESTION]` 未对全部 44 页逐页做像素级视觉比对，不能声称未抽样页面绝无排版解析误差。

## 独立读者总判断

`[READER_INTERPRETATION]` REFINEBENCH 提供了强而具体的负向证据：在无显式缺陷定位、一个极简继续修订 prompt、最多五轮、GPT-4.1/checklist 评分的设置中，多数模型不能稳定提高，且可破坏原本正确的 checklist items；同时，定向失败项反馈可大幅改善结果。它不构成对“一般 self-refinement”或所有自反馈算法的反证。该边界既由实验设计决定，也被作者在 Limitations 中明示。该判断仅用于后续 reconciliation，不评价 Candidate。

## 实际访问、网络与工具声明

- 科研输入实际访问：本 attempt invocation、P034 PDF、统一模板；同一获准任务中的 P033 invocation/PDF 另行用于 P033 报告。未读取 read_1、任何 read_2、reconciliation、Cards、CORPUS_REPORT、blind query、其他论文读稿或其他报告。
- 程序性说明实际访问：本地 `pdf` 与 `evidence-quality-gate` 技能说明及其三份规则/格式/清单参考；它们未作为科研证据，也未改变冻结输入边界或输出路径。
- 工具：PowerShell `Get-Content`、`Get-FileHash`；Python `pypdf` 逐页文本抽取；PyMuPDF 内存渲染关键页；`apply_patch` 写入本报告。`pdfinfo` 曾尝试但因 Windows 路径解析失败，未产出页数；随后由 `pypdf` 取得页数。
- 网络：未调用任何联网工具、浏览器、搜索、API 或外部站点。
- 隔离：`procedural_blinding`，并非技术文件级 allowlist；未枚举工作区。
- 中间产物：未写入任何临时文本、图片、Card、Evidence 或 manifest；脚本只负责读取/抽取/哈希，科研判断由本读者完成。
