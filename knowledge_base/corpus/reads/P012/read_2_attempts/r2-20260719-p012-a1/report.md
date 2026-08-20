# P012 独立二读报告

## 0. 身份、边界与 provenance

- 本报告对应 invocation snapshot：`r2-20260719-p012-a1/invocation.md`，Attempt ID 为 `r2-20260719-p012-a1`；论文为 *Reflexion: Language Agents with Verbal Reinforcement Learning*（NeurIPS 2023）。
- [AUTHOR_FACT] 指作者在论文中明确写出、且本读者能定位的事实；[READER_INTERPRETATION] 是本读者对机制或证据边界的解释；[OPEN_QUESTION] 是仅凭本文不能解决或文本内部仍有歧义的问题。
- 本报告是 fresh 独立核源，不合并首读，不生成 Card，不评价 Candidate。
- PDF 实际 SHA-256 为 `efba04cd48b779131fc4c3c58ae49e8523ded534f9225a7c57c7bdad0823803d`，与 invocation 一致。PDF 共 19 页，页面印刷页码亦为 1–19。
- 实际模型可见信息：Codex（基于 GPT-5）；更细部署版本不可见。协作任务标识：`/root/p012_second_read`。
- 隔离性质：`procedural_blinding`。平台未提供可验证的文件级 allowlist，故不能把本次读取称为技术隔离。

## 1. 逐页核查覆盖

以下每页均同时做了解析文本读取与可视渲染检查。

| PDF 页 | 主要内容与定位 | 核查结论 |
|---:|---|---|
| 1 | 标题、摘要、§1 Introduction；短定位 “not by updating weights” | [AUTHOR_FACT] 摘要陈述以语言反馈和 episodic memory 改进后续试次；可视页与正文解析一致。 |
| 2 | Figure 1、引言续；短定位 “semantic gradient signal” | [AUTHOR_FACT] 三类任务示例与三种反馈来源被概述。图内文本的解析层出现字符编码乱码，但可视图正常，见 §8。 |
| 3 | §2 Related work、§3 开头及相关工作对照表 | [AUTHOR_FACT] 作者把 Actor、Evaluator、Self-Reflection 分成三个模块；可视页与解析一致。 |
| 4 | Figure 2、Algorithm 1、Actor/Evaluator/Self-reflection/Memory | [AUTHOR_FACT] 算法图和模块输入输出可定位；可视页确认伪代码确实写作 “or”，见问题 2 的开放项。 |
| 5 | §3 末、§4、§4.1 ALFWorld | [AUTHOR_FACT] 记忆上限通常为 1–3；ALFWorld 设置、基线重试和结果文字均可定位。 |
| 6 | Figure 3、§4.2 HotPotQA、Figure 4 | [AUTHOR_FACT] ALFWorld 失败类型曲线及 HotPotQA 四种设置可定位；图线、图例与解析正文相符。 |
| 7 | §4.2 结果/消融、§4.3 Programming、Table 1 | [AUTHOR_FACT] HotPotQA episodic-memory 消融和编程 benchmark 结果可定位。 |
| 8 | Table 2、Table 3、编程分析与消融 | [AUTHOR_FACT] false-positive 测试问题及两项受损版本的结果可定位。 |
| 9 | §5 Limitations、§6、§7、§8 | [AUTHOR_FACT] 局部最优、记忆结构、代码测试边界、安全风险和隔离执行建议可定位。 |
| 10 | References [6]–[23] | [AUTHOR_FACT] 参考文献页；无新增实验主张。 |
| 11 | References [24]–[31] | [AUTHOR_FACT] 参考文献页；无新增实验主张。 |
| 12 | Appendix A、Table 4、Table 5 | [AUTHOR_FACT] 额外模型结果显示 starchat-beta 无增益，不同较强模型均有不同幅度增益。 |
| 13 | Appendix B、Figure 5 | [AUTHOR_FACT] ALFWorld 两轮轨迹展示失败、反思与第二轮成功。 |
| 14 | §B.1 WebShop Limitation、Figure 6、§C 开头 | [AUTHOR_FACT] WebShop 在四轮内无显著改善，作者明确归因于探索多样性不足。 |
| 15 | §C.1–C.5（部分） | [AUTHOR_FACT] 编程 Actor、自反思与消融 prompt 形式可定位。 |
| 16 | §C.5 续行 | [AUTHOR_FACT] 页面确实只有 prompt 结构的四行续文；稀疏不是解析丢页。 |
| 17 | §D.1、Figure 7 | [AUTHOR_FACT] HotPotQA ReAct 两轮完整示例；示例反思与实际搜索动作有内部矛盾，见问题 5。 |
| 18 | §D.2、§D.3 | [AUTHOR_FACT] CoT 与 CoT(GT) 两轮反思示例；可视页与解析一致。 |
| 19 | §D.4.1、§D.4.2 | [AUTHOR_FACT] EPM 消融 prompt 示例；§D.4.1 的数字与结论内部不一致，见问题 5。 |

## 2. 统一问题 1：方法究竟改变哪一步计算？

- [AUTHOR_FACT] Reflexion 不更新 LLM 权重，而是把策略参数化为 `θ = {M_a, mem}`；每轮轨迹 `τ_t` 先由 Evaluator 评分，再由 Self-Reflection 模型把 `{τ_t, r_t}` 放大为语言经验 `sr_t`，追加到 `mem`，下一轮 Actor 在该记忆条件下重新生成轨迹。定位：PDF p.1 摘要与 §1，短定位 “not by updating weights”；p.4 Figure 2/Algorithm 1；p.5 §3 “The Reflexion process”。
- [READER_INTERPRETATION] 真正被改变的计算不是梯度更新或模型参数，而是**跨试次的推理上下文构造与下一轮策略条件分布**：`mem` 把失败轨迹压缩为语言提示，改变后续 Actor 的输入，从而改变动作/答案/代码生成。
- [AUTHOR_FACT] 短期记忆是当前 trajectory history，长期记忆是历次 self-reflection；长期记忆受最大容量 `Ω` 限制，通常为 1–3。定位：PDF p.4 “Memory”；p.5 短定位 “usually set to 1-3”。
- [OPEN_QUESTION] 本文没有给出把语言记忆引起的改变分解为“错误定位、计划更新、额外采样/重试、上下文增长”各自独立贡献的统一因果估计；只在部分任务做了组件消融。

## 3. 统一问题 2：输入、输出、可用信息与干预时点

### 3.1 通用模块

- [AUTHOR_FACT] Actor 输入状态观测、短期轨迹历史和长期反思记忆，输出文本与动作；Evaluator 输入生成轨迹并输出任务分数/奖励；Self-Reflection 输入稀疏奖励、当前轨迹与持久记忆，输出具体语言反馈。定位：PDF p.3 §3 “Actor”；p.4 “Evaluator”“Self-reflection”“Memory”及 Figure 2。
- [AUTHOR_FACT] 干预发生在一轮尝试完成并被评价之后、下一轮开始之前；成功或达到 trial 边界时停止。定位：PDF p.4 Algorithm 1；p.5 §3 “After the first trial”。
- [OPEN_QUESTION] Algorithm 1 可视页和解析文本都写成 `while M_e not pass or t < max trials do`（PDF p.4）。按通常程序语义，`or` 会使循环直到“已通过且达到上限”才退出，与正文所述“until ... correct”及实验中的最大轮数边界不完全一致；需要代码或作者澄清这里是否应为 `and`。

### 3.2 各任务的可用信息

- [AUTHOR_FACT] ALFWorld：Actor 为 ReAct；环境只直接表示任务是否完成。自评触发器有 LLM 二分类或手写启发式（同一动作/响应超过 3 个 cycle，或动作数超过 30）；基线在触发后跳过反思、重置环境并重试，Reflexion 则先反思并更新记忆。记忆保留最近 3 条反思。定位：PDF p.5 §4.1，短定位 “more than 3 cycles”“exceeds 30”。
- [AUTHOR_FACT] HotPotQA：CoT 设置可获得问题，CoT(GT) 还获得数据集的 ground-truth context；ReAct 可以调用 Wikipedia API 检索。轮间用 exact match 产生二元成功信号，记忆为 3 条经验。CoT 用 6-shot，ReAct 用 2-shot，self-reflection 用 2-shot。定位：PDF p.6 §4.2。
- [AUTHOR_FACT] 编程：输入自然语言函数描述；Actor 生成实现。模型先以 CoT 生成测试及自然语言说明，用 AST 过滤语法有效测试，最多采样 6 个测试执行；测试反馈和一条反思经验用于下一轮实现。定位：PDF p.7 §4.3；p.15 §C.2–C.3。
- [READER_INTERPRETATION] 因而三类任务共享“尝试—评价—语言反思—记忆—重试”骨架，但 Evaluator 可用信息差异很大：环境完成信号、答案 exact match、Wikipedia 工具返回、编译器/解释器日志和自生成测试不能视为同一种监督强度。

## 4. 统一问题 3：最强基线与最接近组合基线

- [AUTHOR_FACT] ALFWorld 的直接同构基线是 ReAct-only：使用相同 GPT-3、相同两条 domain few-shot 轨迹，并在自评触发后重置重试但不写反思。ReAct + Reflexion 完成 130/134 个任务，正文称相对强基线绝对提升 22%。定位：PDF p.5 §4.1 “In the baseline runs”与 “Results”；p.6 Figure 3。
- [READER_INTERPRETATION] ALFWorld 最接近的组合基线不是静态单次 ReAct，而是“ReAct + 相同失败检测 + reset/retry、但跳过 reflection”。它较好隔离反思记忆，但全文未报告 token/tool-call 等预算匹配。
- [AUTHOR_FACT] HotPotQA 的基线包括 ReAct-only、CoT-only、CoT(GT)-only；最接近反思机制的组合消融是 `CoT(GT) EPM`，仅把最近一条 trajectory 放入 episodic memory。加入 self-reflection 相对 EPM 再带来 8 个百分点。定位：PDF p.6 Figure 4(c)；p.7 §4.2 “Analysis”。
- [READER_INTERPRETATION] CoT(GT) 是“推理能力”隔离设置，但因获得 ground-truth context，不应当作无 oracle 的整体 QA 基线；整体检索问答更直接的比较是 ReAct-only 与 ReAct + Reflexion。
- [AUTHOR_FACT] 编程 Table 1 同时列出先前方法/模型 SOTA、GPT-4 单次生成基线和 Reflexion。HumanEval Python 为 80.1（GPT-4）对 91.0（Reflexion）；MBPP Python 为 80.1 对 77.1，是明确反例。定位：PDF p.7 Table 1。
- [AUTHOR_FACT] 编程最接近的组件基线见 Table 3：base 0.60；去掉 test generation、保留 self-reflection 为 0.52；保留 test generation、去掉 self-reflection 为 0.60；完整 Reflexion 为 0.68。定位：PDF p.8 Table 3。

## 5. 统一问题 4：模型、token、tool-call、prompt 或 oracle 差异

- [AUTHOR_FACT] 额外模型实验表明模型能力是强调节变量：starchat-beta 在 HumanEval Python 上 baseline 与 Reflexion 都为 0.26；作者称指定自我纠正是更强、更大模型的 emergent quality。定位：PDF p.12 Appendix A、Table 4。
- [READER_INTERPRETATION] 因此不能把“Reflexion 普遍有效”与“强模型具备可用自诊断能力”分开看；弱模型零增益是直接证据。
- [AUTHOR_FACT] 不同任务使用不同 shot 数、不同 Actor（CoT/ReAct）、不同评估器和不同工具：HotPotQA ReAct 用 Wikipedia API，而 CoT(GT) 获得真值上下文；编程 Reflexion 额外生成并执行最多 6 个测试。定位：PDF p.4 “Evaluator”；p.6 §4.2；p.7 §4.3。
- [READER_INTERPRETATION] 论文的部分比较控制了基础模型和主要 prompt，但总体没有 token、延迟、API 调用次数、环境交互次数或总推理成本的统一预算匹配。Reflexion 多出评估、反思、记忆上下文和多轮重试，因此性能增益不能解释为等计算预算下的纯算法增益。
- [AUTHOR_FACT] HotPotQA 用环境 exact-match 对答案给二元成功信号；CoT(GT) 直接获得 ground-truth context，但作者称不给 ground-truth answer。定位：PDF p.6–7 §4.2，短定位 “without access to the ground truth answer”。
- [READER_INTERPRETATION] exact-match 成败属于由真值答案导出的 oracle-like 反馈，即使未泄露答案文本；CoT(GT) 的上下文本身是更强 oracle 信息。两者与开放环境中的内部自评不可直接等同。
- [OPEN_QUESTION] 全文没有报告按成功任务归一化的 token/tool-call/编译执行成本，也未给出“相同总尝试次数 + 同等上下文长度 + 无反思摘要”的全面控制；性能—成本前沿仍未知。

## 6. 统一问题 5：限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者明确承认 Reflexion 可能陷入非最优局部极小值，长期记忆仅为有界滑动窗口；建议未来尝试向量数据库或 SQL 等结构。定位：PDF p.9 §5，短定位 “non-optimal local minima”。
- [AUTHOR_FACT] WebShop 上，100 个环境的 two-shot ReAct + Reflexion 在四轮后因无改善而终止，反思也“不 helpful/intuitive”；作者结论是需要高多样性与探索的任务超出其能力。定位：PDF p.14 §B.1、Figure 6。
- [AUTHOR_FACT] MBPP Python 的 Reflexion 77.1 低于 GPT-4 单次基线 80.1。作者把这一负向结果联系到内部测试的 false positive：MBPP Python 为约 16.3%，HumanEval Python 为约 1.4%；错误实现通过内部测试会被过早提交。定位：PDF p.7 Table 1；p.8 Table 2 及其后分析。
- [OPEN_QUESTION] Table 2 把 TP/FN/FP/TN 定义为事件，但数值按列呈现为条件比例（例如 TP+FP=1、FN+TN=1），没有清楚写出每列分母；这些数值不应被直接当作标准联合 confusion matrix 频率。定位：PDF p.8 Table 2 与短定位 `P(not pass@1 generation correct | tests pass)`。
- [AUTHOR_FACT] 不生成测试、只做无依据反思时，HumanEval Rust 困难子集从 0.60 降到 0.52，作者观察到对正确实现产生 harmful edits；有测试但无语言反思则仍为 0.60、无增益。定位：PDF p.8 Table 3 与 “Ablation study”。
- [AUTHOR_FACT] 代码测试的明示未覆盖/困难边界包括非确定性生成器、与 API 交互的 impure function、硬件相关输出、并行或并发行为。定位：PDF p.9 §5。
- [AUTHOR_FACT] 方法依赖 LLM 自评或启发式能力，且作者明确说没有 formal guarantee for success。定位：PDF p.2 §1，短定位 “not having a formal guarantee”。
- [OPEN_QUESTION] Appendix D.1 的反思叙述与轨迹不一致：Trial 1 实际已经 `Search[Gorden Kaye]`，但反思称未来应搜索 Gorden Kaye；真正成功的 Trial 2 搜索的是 Sam Kelly。定位：PDF p.17 Figure 7。该例无法支持其文字所述的具体纠错路径，尽管第二轮答案确实标记为正确。
- [OPEN_QUESTION] Appendix D.4.1 的 Trial 2 同时写 Jonny Craig 和 Pete Doherty 都参加过 7 个乐队，却立即得出 Jonny “more bands” 并标记正确；反思又引入“past/current”区分但未给数量证据。定位：PDF p.19 §D.4.1。该例存在内部算术/比较不一致。
- [READER_INTERPRETATION] 除正文已列边界外，全文没有系统测试长期记忆扩展、噪声/对抗性反馈、反思累积错误、跨任务迁移、真实成本或安全约束下的表现。

## 7. 统一问题 6：可抽取的 Operator 与真实 Failure（仅核源，不生成 Card）

### 7.1 可抽取为 Operator 的机制

- [AUTHOR_FACT] **反馈语言化**：把标量/二元奖励与失败轨迹转成可操作的自然语言经验。定位：PDF p.1 §1；p.4 “Self-reflection”。
- [AUTHOR_FACT] **持久反思记忆重条件化**：将 `sr_t` 追加到有界 `mem`，下一轮 Actor 同时读取短期轨迹和长期经验。定位：PDF p.4 Figure 2/Algorithm 1；p.5 §3。
- [AUTHOR_FACT] **评价器可插拔**：可使用 exact match、手写失败启发式、LLM 自评、外部环境反馈或自生成测试。定位：PDF p.2 §1；p.4 “Evaluator”。
- [AUTHOR_FACT] **失败触发的 reset/retry**：评价后反思、重置环境并进入下一 trial，直至通过或达到任务边界。定位：PDF p.4 Algorithm 1；p.5 §4.1。
- [AUTHOR_FACT] **测试驱动的代码自修复**：生成测试、AST 过滤、执行测试、对失败做语言解释，再改写实现。定位：PDF p.7 §4.3；p.15 §C.2–C.5。
- [READER_INTERPRETATION] 这些是论文中可复现描述的计算操作；本报告不把它们提升为正式 CRL Operator Card，也不判断其研究价值。

### 7.2 真实可记录的 Failure

- [AUTHOR_FACT] **探索多样性不足**：WebShop 四轮无显著提升且反思无帮助。定位：PDF p.14 §B.1、Figure 6。
- [AUTHOR_FACT] **弱模型无自修正增益**：starchat-beta baseline=0.26、Reflexion=0.26。定位：PDF p.12 Table 4。
- [AUTHOR_FACT] **测试 false positive 导致过早接受错误代码**：MBPP Python 低于 GPT-4 基线。定位：PDF p.7 Table 1；p.8 Table 2。
- [AUTHOR_FACT] **无测试支撑的反思会伤害正确实现**：消融为 0.52，低于 0.60 baseline。定位：PDF p.8 Table 3 及分析。
- [AUTHOR_FACT] **只有测试反馈、没有独立语言反思时无增益**：self-reflection omission 为 0.60，与 baseline 相同。定位：PDF p.8 Table 3。
- [AUTHOR_FACT] **ReAct-only 的长期 hallucination failure**：ALFWorld 曲线收敛到约 22% hallucination rate 且无长期恢复。定位：PDF p.6 Figure 3 及其前分析。
- [READER_INTERPRETATION] Appendix p.17 与 p.19 的示例内部不一致应单独记录为“报告/示例证据质量问题”，不宜与方法运行失败混为一类。

## 8. 统一问题 7–8：定位完整性与解析文本/可视 PDF 冲突

- [AUTHOR_FACT] 本报告的重要机制、基线、结果与限制均在前述条目中附有 PDF 页码、章节/图表和短定位文本；主要证据集中于 p.1–9、p.12–19。
- [READER_INTERPRETATION] 19 页解析文本与可视 PDF 未发现会改变论文结论的实质冲突。
- [AUTHOR_FACT] 唯一明显的解析层异常在 PDF p.2 Figure 1：图内嵌字体被 `pypdf` 提取为控制/错码字符；可视渲染显示三列任务、trajectory、evaluation、reflection、next trajectory 均正常。Figure 1 caption 与其下正文解析正常。因此报告关于该图的判断依据可视页与相邻正文，不依据乱码图内文本。
- [AUTHOR_FACT] PDF p.16 在可视页上本来就只有 §C.5 prompt 结构的四行续文，解析得到 113 个字符与页面稀疏内容相符，不是漏提取。
- [AUTHOR_FACT] p.17 与 p.19 的不一致同时存在于可视页和解析文本，故是论文示例内部问题，不是解析错误。
- [OPEN_QUESTION] 数学公式与图表的精确排版语义未做独立 OCR/结构化表格复原；不过 Figure 2、Algorithm 1、Tables 1–5 和 Figures 3–7 均已视觉检查，未见数值或标签被遮挡。

## 9. 实际读取文件、工具与可观察 trace

### 9.1 实际读取文件

研究内容读取严格限于：

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P012_reflexion.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P012/read_2_attempts/r2-20260719-p012-a1/invocation.md`

此外，因运行时的强制技能规则，实际还读取了两份通用工具说明文件：

4. `C:/Users/g/.codex/skills/pdf/SKILL.md`
5. `C:/Users/g/.codex/plugins/cache/openai-curated-remote/superpowers/6.1.1/skills/using-superpowers/SKILL.md`

后两者不含 P012、其他读者、Card、blind query 或工作区研究内容；仍在此如实披露，避免把实际 trace 误报为只有三次文件访问。未读取 read_1、Cards、其他读者报告、blind query 或其他论文，未枚举工作区。

### 9.2 工具与操作

- PowerShell `Get-Content`：读取 prompt 与 invocation。第一次沿终端默认编码显示为乱码，随后显式 UTF-8 重读；报告依据 UTF-8 内容。
- PowerShell `Get-FileHash -Algorithm SHA256`：核对 PDF hash。
- `pdfinfo`：曾尝试读取 PDF 信息，但本机找不到该工具，调用失败；未产生输出文件。
- Python `pypdf`：只读打开 PDF，读取 metadata、19 页页数，并分段逐页提取全部文本。
- Python `PyMuPDF`：检查本地版本并在内存中渲染 PDF 页面。
- Node REPL + Python 子进程：把 p.1–4、5–8、9–12、13–16、17–19 组成内存 contact sheet 返回视觉检查；未写临时图片。
- 工具能力目录：仅查询可用工具描述以寻找无需落盘的 PDF 可视化路径；未调用 Adobe/网络服务。
- 曾尝试把 shell 返回的 base64 PNG 直接作为图像交给界面，两次均无法处理；随后改为 Node REPL 内存图像返回。两次失败尝试未落盘。
- `apply_patch`：唯一文件写入为本 `report.md`。
- 网络：未调用 web 搜索、网页打开、下载或任何外部 connector。

### 9.3 平台无法观察或证明的 trace

- 平台没有向本读者提供可审计的 OS 文件访问日志、文件级 allowlist 命中记录或底层缓存记录，故这些 trace 为 `unavailable`。
- 本读者只能报告自己发起并在对话中可见的工具调用，不能证明宿主平台、PDF 库或其他进程在底层没有额外缓存/读取行为。
- 没有可见的精确部署 build/version；因此只能报告“Codex（基于 GPT-5）”。
- 未把 `procedural_blinding` 误称为技术隔离或可验证 read-only sandbox。
