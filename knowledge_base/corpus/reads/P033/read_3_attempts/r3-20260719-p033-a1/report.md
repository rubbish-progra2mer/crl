# P033 独立第三读报告

## Provenance 与边界

- Attempt：`r3-20260719-p033-a1`。
- 冻结 invocation：`knowledge_base/corpus/reads/P033/read_3_attempts/r3-20260719-p033-a1/invocation.md`。
- 原文：`knowledge_base/staging/papers/P033_self_refine.pdf`，61 个物理页；实测 SHA-256 为 `a07dfc5ada4ff818c77812dd581065a4e3e40f5736f2f36a97787a66da6e7825`，与 invocation 一致。
- 统一模板：`knowledge_base/templates/second_read_prompt.md`；实测 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，与 invocation 一致。
- 阅读方式：逐物理页解析并人工判断全文；对关键物理页 5、7、29、35 做了内存渲染视觉复核。以下 locator 中的页码均为 PDF 物理页码。

## 核心结论

1. `[AUTHOR_FACT]` SELF-REFINE 在测试时把一次生成改成同一底座模型依次执行 `INIT/GEN -> FEEDBACK -> REFINE`，并把历次输出与反馈追加进后续 refinement prompt；不更新模型参数。Locator：物理页 2–4，§2，Eq. (1)–(4)，Algorithm 1；短摘录锚点：“same underlying language model”。
2. `[READER_INTERPRETATION]` 因而被直接改变的是推理期计算图与可用上下文，而不是底座模型本身：新增了任务特定的反馈 prompt、refinement prompt、多次模型调用和迭代历史。该论文能支持“这一整套测试时协议相对单次生成有效”，不能仅凭主表把收益因果归于“self-feedback”这一单一因素。Locator：物理页 2–6，§2、§3.1、Table 1、Table 2。
3. `[AUTHOR_FACT]` 主实验覆盖 7 个任务、GPT-3.5/ChatGPT/GPT-4（代码任务另含 Codex），主要对照是同一底座模型的单次生成；主实验采样温度为 0.7，反馈与 refinement 即使对指令模型也使用 few-shot prompt，最多 4 轮。Locator：物理页 4–5，§3.1、Table 1。
4. `[READER_INTERPRETATION]` Table 1 的 21 个“模型×任务”绝对增量按表值复算平均约为 21.1 个百分点，与摘要“约 20% absolute on average”相符；但这只是跨异质指标的算术平均，不是统一量纲的单任务效应。Locator：物理页 1、5，Abstract、Table 1。
5. `[AUTHOR_FACT]` 主表没有任务级负增量，但 Math Reasoning 的增量为 0、0.2、0.2；作者将低增益归因于模型难以识别错误，ChatGPT 对 94% 实例反馈“everything looks good”。有外部正确性信号时数学任务才出现更大改善。Locator：物理页 5–6，Table 1、§3.3；物理页 29，Table 14；物理页 41，Appendix R。
6. `[AUTHOR_FACT]` 作者明确报告多维反馈任务并非逐轮单调改善：Acronym 示例总分 `11 -> 17 -> 12 -> 17`，一个维度改善时另一个维度可能退化。Locator：物理页 7–8，§4；物理页 29，Table 15、Appendix K.1。
7. `[READER_INTERPRETATION]` 因最终结果可按反馈模型分数挑选较优迭代，汇总终点分数会遮蔽中间轮次退化；论文没有给出 7 个任务统一的“样本级变好/不变/变坏”转移率。Locator：物理页 29，Table 15 后文字；物理页 39，Appendix P.2。

## 统一问题清单

### 1. 方法改变哪一步计算

- `[AUTHOR_FACT]` 初稿为 `y0=M(pgen||x)`；反馈为 `fbt=M(pfb||x||yt)`；修订使用输入、初稿、历次反馈和历次输出生成 `yt+1`。Locator：物理页 2–4，Eq. (1)、(2)、(4)，Algorithm 1。
- `[AUTHOR_FACT]` 反馈被要求“actionable”且“specific”，即指出具体修改动作与具体短语/问题。Locator：物理页 3–4，§2 FEEDBACK。
- `[READER_INTERPRETATION]` 操作符可描述为：`同模型自评 -> 将自然语言反馈注入下一轮 -> 保留历史的条件式重写`。这是从算法结构抽取的机制描述，不是对 Candidate 的评价。

### 2. 输入、输出、可用信息与干预时点

- `[AUTHOR_FACT]` 输入是任务输入 `x` 与任务特定 few-shot/instruction prompts；反馈模型看到 `x, yt`，refiner 还看到迭代历史；输出通常是最后一轮或任务特定选择规则选出的修订稿。Locator：物理页 2–4，§2；物理页 39，Appendix P.2。
- `[AUTHOR_FACT]` 干预发生在初始输出之后、每次 refinement 之前；没有训练或参数更新。Locator：物理页 1–4，Abstract、Figure 1、Algorithm 1。
- `[AUTHOR_FACT]` 可用监督并非完全空白：few-shot 示例中含人工或既有来源构造的反馈/修订。作者在不同任务中人工编写或整理部分 `fb` 与改进版本；代码优化使用既有慢/快程序及解释。Locator：物理页 44–45，Appendix V。
- `[READER_INTERPRETATION]` 所以“无需监督训练数据”不等于“协议完全不含人工任务知识”；任务 rubrics、示例反馈和改写示范是推理期监督信息。

### 3. 最强基线与最接近组合基线

- `[AUTHOR_FACT]` 主对照是相同 GPT-3.5、ChatGPT 或 GPT-4 的 Base 单次生成。Locator：物理页 4–5，§3.1、Table 1。
- `[AUTHOR_FACT]` 最接近机制消融包括 generic feedback 和 no feedback，但只报告 Code Optimization、Sentiment Reversal、Acronym Generation 三个任务，且所用底座并不统一。Locator：物理页 6，Table 2。
- `[AUTHOR_FACT]` 作者另以 ChatGPT 一次生成 `k=4` 个候选作为重采样对照，并进行 `1 vs. k` 人评；Figure 7 仅展示 Sentiment Reversal 与 Acronym Generation。Locator：物理页 8，§4 “Can we just generate multiple outputs”；物理页 29，Figure 7。
- `[AUTHOR_FACT]` Appendix H 还列出 PIE/Scalene 的 `BEST@16/@32` 等强基线；作者说明 SELF-REFINE 至多使用 4 个 samples，但该比较不是统一调用数的全任务对照。Locator：物理页 24–25，Tables 10–12。
- `[OPEN_QUESTION]` 原文没有提供跨全部 7 个任务、严格匹配 token 数、调用数、prompt 长度与最终选择器的同预算重采样/重写基线，因此无法从本文单独识别“反馈语义”相对于“更多计算与更多生成机会”的纯效应。

### 4. 结果是否可能来自预算、prompt、oracle 或评价差异

- `[AUTHOR_FACT]` Base 是一次生成，而 SELF-REFINE 增加多轮反馈与修订调用，并追加历史；论文没有把主实验统一成等 token 或等调用预算。Locator：物理页 3–5，Algorithm 1、§3.1。
- `[AUTHOR_FACT]` instruction-only 实验仍需“extensive prompt engineering”；数学任务的大幅增益主要来自修复初稿中遗漏的 `return`，当初始程序有效时不再改善。Locator：物理页 8、18，§4、Appendix E，Table 8。
- `[AUTHOR_FACT]` 数学附录使用 correct label 决定是否进入下一阶段；Oracle Feedback 只在当前答案错误时进入 REFINE。Locator：物理页 29，Appendix K.1；物理页 41，Appendix R。
- `[READER_INTERPRETATION]` 因此数学部分混有外部正确性/oracle 条件，不能与纯自反馈设置不加区分地解释。
- `[AUTHOR_FACT]` 多个开放生成任务使用 GPT-4 偏好评价；报告的人类相关性为 82%（Sentiment）、68%（Acronym）、71%（Dialogue）。物理页 5，§3.2。
- `[AUTHOR_FACT]` 人类 A/B 评价由作者执行；大部分实例仅一条标注，另对每数据集 50 个 GPT-4 输出样本做双标注。Locator：物理页 17，Appendix C。
- `[READER_INTERPRETATION]` 评价器、生成器、prompt rubric 与选稿分数之间存在共享模型/共享标准的可能；Claude-v2 复核 GPT-4 输出缓解但未消除这一问题。Locator：物理页 18–20，Appendix F、Table 9。

### 5. 停止条件、限制、负向结果与未测试边界

- `[AUTHOR_FACT]` 通用算法允许按固定迭代次数停止，或从反馈中提取任务特定停止标记；主实验一般最多 4 轮。Locator：物理页 3–4，Algorithm 1、§2 “Iterating”、§3.1。
- `[AUTHOR_FACT]` 具体实现不统一：Dialogue 最多 3 轮且从“除初稿外”的各轮中选反馈总分最高者；Sentiment 最多 4 轮并在达到目标情感时停止；Code Readability 因预算运行 5 轮；Math 使用正确标签控制迭代。Locator：物理页 36、39、41–42，Appendices O.2、P.2、R、S。
- `[OPEN_QUESTION]` Appendix K.1 称按所有迭代最大分数选择并指向“Algorithm 1 line 8”，但物理页 3 的 Algorithm 1 第 8 行只是 `end if`，且通用算法返回最后的 `yt`。这是停止/选择规则的内部文档不一致。Locator：物理页 3，Algorithm 1；物理页 29，Table 15 后段落。
- `[AUTHOR_FACT]` 弱模型 Vicuna-13B 难以按格式生成反馈，即使 oracle/hard-coded feedback 也常不遵循 refinement prompt，会重复输出或生成幻觉对话。Locator：物理页 8、26–27，§4、Appendix I、Figure 6。
- `[AUTHOR_FACT]` 失败样本人工分析中，失败主要来自错误反馈：错误定位占失败案例 33%，不当修复建议占 61%，好反馈执行错误占 6%。Locator：物理页 8–9，§4 Qualitative Analysis。
- `[AUTHOR_FACT]` Dialogue 分析还报告 incorrect feedback 25%、generic feedback 30%、incorrect scoring 10%；refinement 可能忽略反馈、引入新问题或对坏反馈不鲁棒。Locator：物理页 30–31，Tables 16–17。
- `[AUTHOR_FACT]` 作者明示边界包括底座需有足够 few-shot/指令遵循能力、主要模型闭源、只测试英语数据、未显式防止恶意提示导致有害文本。Locator：物理页 10，§6。

### 6. 可记录的 Operator 与 Failure

- `[READER_INTERPRETATION]` 可抽取 Operator：任务 rubric 驱动的自然语言自反馈；反馈条件式重写；历史累积；固定轮数/反馈标记停止；按模型自评分选择迭代输出。依据：物理页 2–4、29、39。
- `[AUTHOR_FACT]` 可记录 Failure：错误定位、不当修复建议、忽略反馈、引入新问题、多维指标间退化、弱模型格式/指令失败、数学错误自检失败。依据：物理页 6–9、27、29–31。
- `[READER_INTERPRETATION]` “平均提升”应与上述 failure 并列记录，不能覆盖任务级零增益、中间轮次退化或失败类型。

### 7. 表格与数字一致性核查

- `[AUTHOR_FACT]` Table 1 的 Constrained Generation 数值为 GPT-3.5 `16.0 -> 39.7`、ChatGPT `2.75 -> 33.5`、GPT-4 `4.4 -> 61.3`。Locator：物理页 5，Table 1。
- `[AUTHOR_FACT]` 声称重现 Table 1 并给置信区间的 Table 18，却给出 `28 -> 37`、`44 -> 67`、`15 -> 45`。Locator：物理页 35，Table 18。
- `[OPEN_QUESTION]` 两表的 Constrained Generation 数值不一致，原文没有解释是指标、数据切分还是实验版本变化；相关汇总主张需指定采用哪一表。
- `[OPEN_QUESTION]` Table 18 图注称 Wilson 95% interval，而紧随段落写 `alpha=99% confidence interval`；显著性星号的置信水平表述内部不一致。Locator：物理页 35，Table 18 caption 与正文。

### 8. 解析文本与可视 PDF

- `[AUTHOR_FACT]` 61 个物理页均成功抽取文本；关键页 5、7、29、35 的表格/曲线/图注经可视复核，主数值与上述 locator 一致。
- `[READER_INTERPRETATION]` 抽取文本对数学符号、箭头和多栏排版偶有顺序噪声，但在已视觉复核页未发现改变上述结论的解析—视觉冲突。
- `[OPEN_QUESTION]` 未对全部 61 页逐页做像素级视觉比对，因此不能声称未抽样页面绝无排版解析误差。

## 独立读者总判断

`[READER_INTERPRETATION]` 本文有直接证据支持：在其选定任务、prompt、评价器与追加计算预算下，完整 SELF-REFINE 协议相对同模型单次生成平均更好；它也直接记录了数学近零增益、弱模型失败、错误反馈与非单调退化。本文没有提供足以把全部收益独立归因于 self-feedback 的统一同预算设计，也没有统一的跨任务停止/选稿规则。该判断仅用于后续 reconciliation，不评价 Candidate。

## 实际访问、网络与工具声明

- 科研输入实际访问：本 attempt invocation、P033 PDF、统一模板；同一获准任务中的 P034 invocation/PDF 另行用于 P034 报告。未读取 read_1、任何 read_2、reconciliation、Cards、CORPUS_REPORT、blind query、其他论文读稿或其他报告。
- 程序性说明实际访问：本地 `pdf` 与 `evidence-quality-gate` 技能说明及其三份规则/格式/清单参考；它们未作为科研证据，也未改变冻结输入边界或输出路径。
- 工具：PowerShell `Get-Content`、`Get-FileHash`；Python `pypdf` 逐页文本抽取；PyMuPDF 内存渲染关键页；`apply_patch` 写入本报告。`pdfinfo` 曾尝试但因 Windows 路径解析失败，未产出页数；随后由 `pypdf` 取得页数。
- 网络：未调用任何联网工具、浏览器、搜索、API 或外部站点。
- 隔离：`procedural_blinding`，并非技术文件级 allowlist；未枚举工作区。
- 中间产物：未写入任何临时文本、图片、Card、Evidence 或 manifest；脚本只负责读取/抽取/哈希，科研判断由本读者完成。
