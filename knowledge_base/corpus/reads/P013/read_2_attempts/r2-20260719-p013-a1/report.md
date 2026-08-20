# P013 独立二读报告

## 0. 身份、范围与 provenance

- [AUTHOR_FACT] 论文题名为 *Large Language Models Cannot Self-Correct Reasoning Yet*，ICLR 2024 conference paper；论文 PDF 共 17 页。定位：PDF p.1，标题区，短定位文本“LARGE LANGUAGE MODELS CANNOT SELF-CORRECT REASONING YET”。
- [AUTHOR_FACT] 本报告引用冻结的 invocation snapshot：`knowledge_base/pilot/reads/P013/read_2_attempts/r2-20260719-p013-a1/invocation.md`，Attempt ID 为 `r2-20260719-p013-a1`；其中给出的 PDF SHA-256 为 `d172f0b3e933544f5165250338e3e989036e8d826fea34093e6aed4adb5b042a`。本次本地复算得到同一 SHA-256。
- [READER_INTERPRETATION] 本次是 fresh independent read-2，只做全文核源和统一问题回答；未生成 Card，未进行 Candidate 评价，也未尝试与其他读者结论合并。
- [OPEN_QUESTION] 平台没有提供可验证的文件级 allowlist 或 OS 级文件访问审计，因此只能声明并报告 `procedural_blinding`，不能把它描述为技术隔离。

## 1. 逐页检查台账

- [AUTHOR_FACT] PDF p.1：摘要与引言开头定义 intrinsic self-correction，即仅依赖模型自身能力、不借助外部反馈；摘要称在 reasoning 场景中性能有时会在自纠后下降。定位：Abstract，短定位文本“without the crutch of external feedback”。
- [AUTHOR_FACT] PDF p.2：引言指出三类评估问题——oracle label、与推理成本不等价的基线、初始 prompt 不充分；Section 2 将后文未特别说明的 “self-correction” 限定为 intrinsic self-correction。定位：Introduction / Background and Related Work，短定位文本“all references to ‘self-correction’ ... pertain to intrinsic self-correction”。
- [AUTHOR_FACT] PDF p.3：Table 1 将 RCI/Reflexion 对应到 oracle labels，将 Multi-Agent Debate 对应到对 self-consistency 的不公平比较，将 Self-Refine 对应到 sub-optimal prompt design；Section 3.1 给出数据、模型、采样和三步提示流程。定位：Table 1、Section 3.1，短定位文本“a three-step prompting strategy”。
- [AUTHOR_FACT] PDF p.4：Table 2 显示 oracle-gated correction 相对标准提示提升；Table 3 显示 GPT-3.5/GPT-4 的 intrinsic correction 在所列 benchmark/round 上不提升并通常下降；正文明确指出 oracle label 用来阻止已正确答案继续被修改。定位：Tables 2–3、Section 3.2，短定位文本“no (further) self-correction will be performed”。
- [AUTHOR_FACT] PDF p.5：Tables 4–6 给出 GPT-4-Turbo、Llama-2 与多种反馈 prompt；所列 self-correct 结果均低于各自 standard prompting。脚注说明 HotpotQA 样本太小，省略其答案变化分析。定位：Tables 4–6、footnote 1，短定位文本“sample size ... is quite small”。
- [AUTHOR_FACT] PDF p.6：Figure 1 将两轮后变化分为 No Change、Correct→Incorrect、Incorrect→Correct、Incorrect→Incorrect；Figure 2 给出成功/失败示例。正文的直觉解释是，附加反馈 prompt 可能把模型从初始 prompt 下的较优响应推开。定位：Figures 1–2、Section 3.3，短定位文本“bias the model away”。
- [AUTHOR_FACT] PDF p.7：Table 7 在 GSM8K 上比较 debate 与相同 response 数的 self-consistency；9 responses 时分别为 83.0 与 88.2。Table 8 与 Section 5 开始展示 constrained generation 的 prompt-design 对照。定位：Tables 7–8、Sections 4–5。
- [AUTHOR_FACT] PDF p.8：Section 5 将“必须覆盖全部概念”的约束前置到初始 prompt 后，Standard Prompting (ours) 为 81.8，高于在原方案结果上报告的 self-correct 数值；在强初始 prompt 上继续 self-correct 得 75.1。Section 6 开始讨论外部执行器/工具/验证器反馈的潜力。定位：Table 8、Sections 5–6，短定位文本“includes *ALL* of the above concepts”。
- [AUTHOR_FACT] PDF p.9：作者建议按相当推理成本比较、初始与反馈 prompt 投入相同设计努力；Section 7 明示研究聚焦 reasoning，style/safety 等其他领域可能存在有效自纠。Reproducibility Statement 给出模型入口、kernel/access time 与 Appendix prompt。定位：Sections 6–7、Reproducibility Statement。
- [AUTHOR_FACT] PDF p.10：参考文献页，无新增实验主张；包含被论文讨论的 self-debug、multi-agent debate、external-tool critiquing 等来源。定位：References。
- [AUTHOR_FACT] PDF p.11：参考文献页，无新增实验主张；包含 Self-Refine、Reflexion、Llama 2 等来源。定位：References。
- [AUTHOR_FACT] PDF p.12：参考文献结束，无新增实验主张；包含 self-consistency、HotpotQA 等来源。定位：References。
- [AUTHOR_FACT] PDF p.13：Appendix A Figure 3 展示 GSM8K 的成功自纠案例，初始错误答案 18 被改为正确答案 24。定位：Figure 3，短定位文本“changes an incorrect answer to a correct one”。
- [AUTHOR_FACT] PDF p.14：Figure 4 展示失败案例，初始正确答案 75 被改成错误答案 37.50。定位：Figure 4，短定位文本“changes a correct answer to an incorrect one”。
- [AUTHOR_FACT] PDF p.15：Figure 5 展示答案保持不变的 GSM8K 案例，前后均为 260。定位：Figure 5，短定位文本“does not change the answer”。
- [AUTHOR_FACT] PDF p.16：Figure 6 展示 CommonSenseQA 中正确选项 E（puncture wound）被改成错误选项 D（competition）。定位：Figure 6，短定位文本“changes a correct answer to an incorrect one”。
- [AUTHOR_FACT] PDF p.17：Figures 7–8 对照原 constrained-generation 初始 prompt 与作者加入全部概念约束的初始 prompt；Figure 7 caption 明确指出该约束原先只在 feedback/refine 中隐含。定位：Figures 7–8，短定位文本“not explicitly mentioned in the prompt for initial response generation”。

## 2. 统一问题 1：方法究竟改变哪一步计算？

- [AUTHOR_FACT] 论文的核心工作不是提出一个新的自纠算法，而是重新控制并比较既有自纠设置。基础自纠流程改变的是首次生成之后的推理：先生成初答，再让模型审阅初答并产出反馈，最后让模型依据反馈重新回答原问题；最多两轮。定位：PDF p.3，Section 3.1 “Prompts”，短定位文本“initial generation ... produce feedback ... answer ... again”。
- [AUTHOR_FACT] oracle 版本在每次答案生成后用 ground-truth correctness 决定是否停止；若答案已正确便不再自纠。intrinsic 版本去掉该 label，由模型自身决定保留或改变答案。定位：PDF p.3–4，Sections 3.1–3.2，短定位文本“use the correct label to determine when to stop”。
- [AUTHOR_FACT] debate 实验把单模型单响应改成 3 个同模型实例、2 轮 debate，让多个生成彼此影响并形成最终答案；对照 self-consistency 则独立生成多份答案后按计数多数投票。定位：PDF p.7，Section 4，短定位文本“3 agents and 2 rounds of debate”。
- [AUTHOR_FACT] constrained-generation 对照改变的是信息进入模型的时点：把原先只在 feedback/refine 中显现的“覆盖全部概念”要求直接加入首次生成 prompt。定位：PDF p.8、p.17，Section 5、Figures 7–8。
- [READER_INTERPRETATION] 因而论文检验的不是“更多计算是否有用”这一单一问题，而是区分三种机制：外部 oracle 门控、同一模型的内生 review/revise、以及多样本选择/共识。其主要贡献是拆分这些机制的归因。

## 3. 统一问题 2：输入、输出、可用信息与干预时点

- [AUTHOR_FACT] reasoning 实验输入为 GSM8K 数学题、CommonSenseQA 多选常识题、HotpotQA closed-book 多跳问答；输出分别按任务答案准确率或 HotpotQA exact match 评估。定位：PDF p.3，Section 3.1 “Benchmarks”。
- [AUTHOR_FACT] 初始生成只接收任务 prompt；反馈步骤接收/审阅前一生成；修订步骤重新回答原问题并利用反馈。作者称详细 prompt 在 Appendix A，并对 GSM8K/CommonSenseQA 加入格式指令以便自动评估。定位：PDF p.3，Section 3.1 “Prompts”。
- [AUTHOR_FACT] intrinsic setting 可用信息不含人工或外部正确性反馈；oracle setting 额外拥有 ground-truth correctness，并在每轮后用于停止门控。定位：PDF p.2、p.4，Section 2、Section 3.2。
- [AUTHOR_FACT] 每轮 intrinsic correction 包含 feedback 与 revised answer 两次新增调用，因此 Table 3–6 的总调用数为初始 1、round 1 后 3、round 2 后 5。定位：PDF p.4–5，Tables 3–6，“# calls”。
- [AUTHOR_FACT] debate 的可用信息包括其他 agent 的回答/批评；self-consistency 的选择只利用答案计数。干预发生在初始多响应之后；Table 7 以 3、6、9 个 responses 对齐比较。定位：PDF p.7，Section 4、Table 7。
- [AUTHOR_FACT] constrained-generation 的输入是 20–30 个 concepts，输出是包含这些概念的 coherent sentence/paragraph，论文实验指标为 concept coverage。定位：PDF p.8，Section 5，短定位文本“use concept coverage as the metric”。
- [OPEN_QUESTION] 正文未给出每个设置的实际输入 token、输出 token、停止长度、总延迟或价格；仅有 calls/responses，不能确认各方法在总 token 成本上严格等价。

## 4. 统一问题 3：最强基线与最接近组合基线

- [AUTHOR_FACT] Section 3 对 intrinsic correction 的直接基线是相同模型/任务的 Standard Prompting（1 call）。例如 GPT-4 在 GSM8K 上 standard 为 95.5，round 1/2 为 91.5/89.0；GPT-4-Turbo 为 91.5、88.0、90.0。定位：PDF p.4–5，Tables 3–4。
- [READER_INTERPRETATION] 该 standard baseline 在 prompt/task 上最接近，但不是成本匹配基线；3/5 calls 的 intrinsic correction 在 Section 3 没有同时对比 3/5 独立样本 self-consistency。因此它足以检验“自纠是否胜过单次初答”，不足以单独判断“相同计算预算下的最佳策略”。
- [AUTHOR_FACT] Section 4 的最接近组合基线是相同 response 数的 self-consistency。3 responses 时 debate 83.2、self-consistency 82.5；6 responses 时 85.3 对 83.2；9 responses 时 88.2 对 83.0。最强列示结果是 9-response self-consistency 88.2。定位：PDF p.7，Table 7。
- [AUTHOR_FACT] Section 5 的最接近 prompt-control baseline 是作者的 strengthened Standard Prompting (ours)，将完整任务约束前置；其 81.8 高于在该强初答上继续应用 self-correct 后的 75.1。定位：PDF p.7–8，Table 8、Section 5。
- [OPEN_QUESTION] Table 8 同时列出 44.0/67.0 与 53.0/61.1 两组带星号/来源差异的 standard/self-correct 数值，但表内没有清楚命名这两组各自对应“原论文报告”还是“作者复现”的哪一种实验条件；正文只说既引用原结果又用 `gpt-3.5-turbo-0613` 复现。精确行级映射需要额外实验日志，原文不足以消歧。

## 5. 统一问题 4：模型、token、tool-call、prompt、oracle 差异能否解释结果？

- [AUTHOR_FACT] oracle 差异能直接解释 Table 2 与 Tables 3–6 的方向差异，因为 oracle 正确性用于阻止正确答案被进一步改坏；作者把这点视为此前改善的关键来源。定位：PDF p.4、p.6，Section 3.2–3.3，短定位文本“prevent the model from altering a correct answer”。
- [AUTHOR_FACT] prompt 差异能解释 constrained-generation 的大幅提升：将全部概念约束放入初始 prompt 后，单次生成达到 81.8，并且再加原 self-correction 降到 75.1。定位：PDF p.7–8，Table 8、Section 5。
- [AUTHOR_FACT] 调用/响应预算可以解释部分 debate 相对 single-prompt 的提升；当按相同 response 数与 self-consistency 比较时，debate 在 6/9 responses 下更差。定位：PDF p.7，Table 7、Section 4。
- [AUTHOR_FACT] 模型与解码条件并不统一：GPT-3.5-Turbo 为 `gpt-3.5-turbo-0613`，另有 GPT-4（2023-08-29 访问）、`gpt-4-1106-preview`、`Llama-2-70b-chat`；GPT-3.5/GPT-4 temperature=1，GPT-4-Turbo/Llama-2 temperature=0。GPT-3.5 用完整评测集，其他模型因成本每数据集随机抽 200（HotpotQA 100）。定位：PDF p.3，Section 3.1 “Test Models and Setup”。
- [READER_INTERPRETATION] 因为温度、样本量、模型版本同时变化，跨模型退化幅度不能被解释为纯模型能力差；可靠的判断应主要使用同一模型、同一数据与同一 prompt 家族内的前后对照。
- [AUTHOR_FACT] Table 7 的 debate 使用 `gpt-3.5-turbo-0301`，而 Section 3 使用 `gpt-3.5-turbo-0613`；因此 Table 7 的 Standard Prompting 76.7 与 Table 3 的 75.9 不应直接当作同一实验重复。定位：PDF p.3、p.7，Sections 3.1、4。
- [READER_INTERPRETATION] 论文没有在 Section 3 将 3/5-call correction 与等 token/等 call 的独立采样、best-of-N（需要 verifier）或 self-consistency 系统比较；核心结论“intrinsic review/revise 未提高单次初答”有直接证据，但“任何同预算多调用策略都无效”不由这些实验支持。
- [OPEN_QUESTION] 论文未报告随机种子、每个随机抽样子集的题目 ID、置信区间/显著性检验、精确 token 数或 API 端非确定性；小幅差异（例如 91.5→91.0）是否稳定不能从原文判定。
- [AUTHOR_FACT] intrinsic reasoning 实验没有外部工具反馈；代码执行器、搜索、计算器、训练 verifier 等只在 Discussion 中作为外部反馈成功方向引用。定位：PDF p.8，Section 6 “Leveraging external feedback for correction”。

## 6. 统一问题 5：作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 明示负向结果：Tables 3–6 中，所列模型/benchmark/feedback prompt 的 intrinsic correction 均未超过其 standard prompting；多种场景会把正确答案改错。定位：PDF p.4–6，Tables 3–6、Figure 1。
- [AUTHOR_FACT] 明示负向结果：相同 response 数时，multi-agent debate 在 6 与 9 responses 下低于 self-consistency；作者把提升归因于多样本 consistency/selection，而非 self-correction。定位：PDF p.7，Section 4、Table 7。
- [AUTHOR_FACT] 明示负向结果：完整约束已经进入初始 prompt 后，继续 self-correct 从 81.8 降至 75.1。定位：PDF p.7–8，Table 8、Section 5。
- [AUTHOR_FACT] 明示限制：研究聚焦 LLM reasoning；作者明确承认 style alignment、safety 等其他域可能存在成功自纠。定位：PDF p.9，Section 7，短定位文本“strategies that could enhance ... in other domains”。
- [AUTHOR_FACT] 明示限制：HotpotQA 源研究/本实验使用 100 题，作者因样本小而不做 Figure 1 类答案变化统计。定位：PDF p.3、p.5，Section 3.1、footnote 1。
- [AUTHOR_FACT] 成本限制：GPT-3.5 外的模型只随机测试每数据集 200 题（HotpotQA 100），且最多测试两轮自纠。定位：PDF p.3，Section 3.1。
- [READER_INTERPRETATION] 标题中的 “cannot ... yet” 应读作对特定时期模型、特定 reasoning 数据、特定 prompt 与最多两轮流程的经验性结论，不是对未来模型或所有可能 intrinsic algorithms 的理论不可能性证明。
- [OPEN_QUESTION] 未测试边界包括：更多轮数、训练过的专用自评器、非英语推理、分布外/长上下文任务、过程级而非答案级验证、开放权重模型的更多规模、token 严格等预算、以及除 concept coverage 外的生成质量维度。
- [READER_INTERPRETATION] Constrained Generation 以 concept coverage 为指标，但任务描述同时要求 coherent sentence/paragraph；因此 81.8 的提升不能单独证明连贯性也提升。

## 7. 统一问题 6：可抽取的 Operator 与真实 Failure（仅作读者标注）

### 可抽取 Operator

- [AUTHOR_FACT] `Intrinsic review → feedback → revise`：初答后由同一 LLM 检查并生成反馈，再据此重答，无外部反馈，最多两轮。定位：PDF p.2–3，Sections 2、3.1。
- [AUTHOR_FACT] `Oracle-gated correction`：每轮后由 ground-truth correctness 决定停止，正确即停止。定位：PDF p.3–4，Section 3.2。
- [AUTHOR_FACT] `Multi-agent debate / model-driven consensus`：3 个同模型实例、2 轮交互，以模型整合多份生成。定位：PDF p.7，Section 4。
- [AUTHOR_FACT] `Self-consistency / count-based majority vote`：独立采样多响应并按答案计数投票，用作等 response 基线。定位：PDF p.7，Section 4、Table 7。
- [AUTHOR_FACT] `Constraint front-loading / prompt consolidation`：把 feedback 阶段才出现的可形式化任务约束前置到初始 prompt。定位：PDF p.8、p.17，Section 5、Figures 7–8。
- [READER_INTERPRETATION] `External verifier/tool feedback` 可作为论文讨论的后续 Operator 类别，但不是本文 intrinsic 主实验实际执行的 Operator；应与实验证据分开记录。定位：PDF p.8，Section 6。

### 真实可记录 Failure

- [AUTHOR_FACT] `Correct → Incorrect`：模型无法可靠判断自己原推理是否正确，反馈 prompt 会诱发无根据的改答。Figure 4 从 75 改成 37.50；Figure 6 从 E 改成 D。定位：PDF p.6、p.14、p.16，Section 3.3、Figures 4/6。
- [AUTHOR_FACT] `Incorrect → Incorrect` 与 `No Change`：Figure 1 明确将二者列为答案变化类别；GSM8K 的 GPT-3.5 有 74.7% 保持初答。定位：PDF p.4–6，Section 3.3、Figure 1，短定位文本“74.7% ... retains its initial answer”。
- [AUTHOR_FACT] `Distractor-induced flip`：CommonSenseQA 错误选项常与问题表面相关，review prompt 可能把模型偏向另一个选项，造成高 correct→incorrect。定位：PDF p.4，Section 3.3。
- [READER_INTERPRETATION] `Oracle masking`：oracle-gated 设置通过禁止正确样本继续修改，遮蔽了 intrinsic 机制最关键的误改风险；这是一种评估归因 Failure，而非模型单独的 Failure。
- [AUTHOR_FACT] `Budget-mismatched attribution`：把多响应 debate 与单次或仅 3-response self-consistency 比较，会把采样/选择收益误归因于 debate；等 responses 后优势消失。定位：PDF p.7，Section 4。
- [AUTHOR_FACT] `Task-information leakage across stages`：初始 prompt 漏掉明确约束，feedback 才补充任务信息，使提升无法区分来自“更完整指令”还是“自纠”。定位：PDF p.8、p.17，Section 5、Figure 7。
- [READER_INTERPRETATION] `Prompt-induced displacement`：在没有新增任务证据时，附加 review prompt 改变条件分布，可能把初始较优答案推离；这是作者直觉解释而非被独立机制实验严格识别的因果结论。定位：PDF p.6，Section 3.3 “Intuitive Explanation”。

## 8. 统一问题 7：定位充分性

- [READER_INTERPRETATION] 上述每项核心判断均给出 PDF 页码、章节/表/图及短定位文本；正文印刷页码与 PDF 页序均为 1–17，一致，无需另做页码换算。
- [OPEN_QUESTION] Figure 1 的完整扇区百分比依赖图内视觉标签，文本抽取未保留全部标签；若后续需要逐扇区录入精确数值，应以原 PDF 图像人工转录并二次复核，不应从当前解析文本推断。

## 9. 统一问题 8：解析文本与可视 PDF 是否冲突

- [AUTHOR_FACT] 已对 PDF p.1–17 逐页做文本抽取，并把所有页面分批直接在内存中渲染核对；没有发现页缺失、倒置、表格数值与正文主张相冲突或附录示例内容不一致。
- [AUTHOR_FACT] PDF p.3 的 Table 1 在解析文本中被排到该页正文与页脚之后，但在可视版面中位于页面顶部；这是读取顺序差异，不是内容冲突。
- [AUTHOR_FACT] PDF p.6 的 Figure 1/2 图内内容主要是嵌入图像：解析文本能取得 caption，却没有完整取得饼图标签、百分比和示例框文字；可视渲染确认这些元素实际存在。
- [AUTHOR_FACT] PDF p.13–17 的附录示例文本可被解析，且与可视版面中的 Figures 3–8 对应；未见语义冲突。
- [READER_INTERPRETATION] 因此当前结论是“存在文本层遗漏与版面顺序偏差，但未发现实质冲突”；不能把“解析成功”误当成对所有图内数值的机器可读保证。

## 10. 实际读取文件、工具与不可观察 trace

- [READER_INTERPRETATION] 实际读取且仅读取以下三份任务输入：
  1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P013_intrinsic_self_correction_limits.pdf`
  2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
  3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P013/read_2_attempts/r2-20260719-p013-a1/invocation.md`
- [READER_INTERPRETATION] 实际写入仅本文件：`D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P013/read_2_attempts/r2-20260719-p013-a1/report.md`。未枚举工作区，未读取 read_1、Cards、其他读者报告或 blind query，未生成中间图片或文本文件，未联网。
- [READER_INTERPRETATION] 工具 trace：PowerShell `Get-Content` 读取两份 Markdown；`Get-FileHash` 复算 PDF SHA-256；本机 `pdfinfo` 包装器曾被调用但在读页前因路径错误失败，`pdftotext` 不可用；随后以 Python `pypdf` 分页抽取 p.1–17 文本，以 PyMuPDF (`fitz`) + Pillow 将 p.1–17 分批渲染为内存图像，并额外渲染 p.6 Figure 1/2 区域核对；最终用 `apply_patch` 写入本报告。所有渲染数据经标准输出进入当前会话，未落盘。
- [OPEN_QUESTION] 平台不可观察/不可证明的 trace：精确内部模型版本、底层运行时或库加载所触及的系统文件、OS 级文件访问日志、技术性 path allowlist、其他进程的文件访问、以及命令包装器内部未暴露的行为。当前可见 agent 身份为 Codex（GPT-5 系列上下文；精确内部版本不可见），canonical task 为 `/root/p013_second_read`；这些陈述不构成平台级审计证明。

