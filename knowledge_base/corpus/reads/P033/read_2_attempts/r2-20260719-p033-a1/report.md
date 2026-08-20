# P033 独立二读报告

- Attempt：`r2-20260719-p033-a1`
- PDF SHA-256：`a07dfc5ada4ff818c77812dd581065a4e3e40f5736f2f36a97787a66da6e7825`
- 阅读范围：物理页 1–61，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`
- 第三读触发建议：`YES_IF_CORE_ANCHOR`

## 1. 正向机制：究竟改变什么

- [AUTHOR_FACT] Self-Refine 使用同一个 LLM 依次生成初稿、反馈和修订，把历次输出追加到上下文，最多迭代 4 次；各任务使用人工编写的 few-shot 提示，temperature 为 0.7。（物理页 2–4，§2–§3，定位词 “FEEDBACK”“REFINE”“maximum of four”）
- [READER_INTERPRETATION] 改变的计算是显式分离“产出—诊断—改写”并保留迭代历史，不是参数学习；正向机制应收窄为“具体、可操作反馈驱动的再生成”。
- [AUTHOR_FACT] 七类任务覆盖对话、代码、文本改写和数学等，实验使用 GPT-3.5、ChatGPT、GPT-4 等不同能力模型。（物理页 4–5，§3，定位词 “seven tasks”）

## 2. 正向证据

- [AUTHOR_FACT] 主结果在偏好、格式约束、代码修订等任务上报告较大提升；但数学几乎不变：GPT-3.5 为 64.1→64.1、ChatGPT 74.8→75.0、GPT-4 92.9→93.1。（物理页 5，主表，定位词 “Math Reasoning”）
- [AUTHOR_FACT] 具体反馈通常优于泛化反馈或无反馈；多轮收益往往前几轮最大，之后递减。（物理页 6–7，反馈消融与迭代曲线，定位词 “specific feedback”“diminishing”）
- [AUTHOR_FACT] 指令遵循代码任务的收益很大一部分来自修复遗漏的 return statement；对已经有效的程序没有同等改善。（物理页 7–8，代码分析，定位词 “return statements”）
- [READER_INTERPRETATION] 可接受的正向 Claim 是：当错误可由模型定位、评价目标可从提示中表达且修订能力足够时，显式反馈循环能提升偏好或约束满足。

## 3. 负向证据与真实失败

- [AUTHOR_FACT] 数学任务中 ChatGPT 在 94% 的反馈里认为答案“看起来没问题”；加入外部正确性反馈后某项分析提升超过 5 分。（物理页 6，数学分析，定位词 “94%”“external feedback”）
- [AUTHOR_FACT] 70 个定性失败样本中，33% 为错误定位错误，61% 为不恰当修复，6% 为没有正确执行一条本来有效的反馈。（物理页 8、30–31，错误分析/案例，定位词 “33%”“61%”“6%”）
- [AUTHOR_FACT] 多维目标的多轮修订可能非单调，Vicuna 等较弱模型并未稳定受益。（物理页 7–8，迭代/模型分析，定位词 “non-monotonic”“Vicuna”）
- [READER_INTERPRETATION] 核心 Failure 是“同模型自反馈无法可靠检测隐藏的正确性错误，并可能在多目标修订中回归”；这与“反思普遍有效”的宽 Claim 直接冲突。

## 4. Baseline、oracle 与评测混杂

- [AUTHOR_FACT] 多项开放式任务依赖 GPT-4-as-judge；人评多为每样本单标注，另取每任务 50 项双标并报告中等到较高一致性。（物理页 8–10、附录评测说明，定位词 “GPT-4”“50”）
- [AUTHOR_FACT] 附录的数学推进分析使用正确标签决定何时继续，表 14 明确属于 oracle 条件。（物理页 41 及相邻附录，定位词 “oracle”）
- [AUTHOR_FACT] 提示包含任务专用示例、rubric 和输出格式；部分任务差异不显著。（物理页 32–61，prompts/统计附录，定位词 “confidence interval”）
- [READER_INTERPRETATION] 不能把 oracle-gated 数学曲线、GPT-4 judge 偏好和普通非 oracle 自修正混为同一证据；提示本身也是重要干预。
- [OPEN_QUESTION] 在固定总 token/调用预算下，Self-Refine 相比 best-of-N、一次更长生成或独立 critic 的优势仍未完全隔离。

## 5. 可抽取内容与裁决边界

- [READER_INTERPRETATION] Operator 候选：`对可外显评价维度生成具体反馈，再由具备相应能力的模型修订，设置有限轮数与回归检查`。
- [READER_INTERPRETATION] Failure 候选：`自反馈把错误答案误判为正确`；`错误定位导致不恰当修补`；`多轮修订非单调`；`弱模型不能通过流程补足能力缺口`。
- [READER_INTERPRETATION] 窄 Claim：Self-Refine 对偏好/约束型任务有条件正向信号，但不证明无外部反馈的通用正确性提升，更不等同于 agent 的持续自我学习。
- [OPEN_QUESTION] 本文是 self-refinement 经典锚点且正负证据并存；若主 Codex 要把它作为多个 Operator 的关键来源或与 P034 形成冲突裁决，应启动第三读，否则可按收窄结论入库。

## 6. 作者限制、解析与访问

- [AUTHOR_FACT] 作者限制包括闭源模型、英文任务、对指令遵循能力的依赖以及潜在安全风险。（物理页 10，Limitations，定位词 “closed-source”“English”“safety”）
- [AUTHOR_FACT] 解析覆盖物理页 1–61，未发现影响结论的文本—可视版冲突；复杂图表建议在正式摘录前目视复核。
- [AUTHOR_FACT] 实际模型/版本 `unknown`；程序性盲化。冻结后只读指定 PDF 和 invocation 内统一 prompt；使用本地 PowerShell、`Get-FileHash`、Python/PyMuPDF；未联网。冻结前仅用 `rg` 定位指定路径，未打开论文。只写本报告。
