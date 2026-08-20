# P014 独立二读报告

## 0. Provenance 与读取边界

- [AUTHOR_FACT] 本报告对应冻结快照 `r2-20260719-p014-a1/invocation.md`，Attempt ID 为 `r2-20260719-p014-a1`；快照记录的论文为 *Instruct-of-Reflection: Enhancing Large Language Models Iterative Reflection Capabilities via Dynamic-Meta Instruction*，canonical ID 为 `ACL:2025.naacl-long.502`。
- [AUTHOR_FACT] 实际计算得到 PDF SHA-256 为 `57A01E87496308E3345839C48F085516DD2824EC5AAACF51B71F127C12F42BB7`，与 invocation 中的值一致。PDF 共 23 个物理页，页脚论文页码为 9956–9978。
- [AUTHOR_FACT] 本次实际读取的研究材料仅为：
  1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P014_instruct_of_reflection.pdf`；
  2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`；
  3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P014/read_2_attempts/r2-20260719-p014-a1/invocation.md`。
- [AUTHOR_FACT] 运行时还依据上层 PDF 处理规则读取了 `C:/Users/g/.codex/skills/pdf/SKILL.md`；该文件只包含通用 PDF 工具说明，不含 P014、其他论文、首读结论、Cards、Candidate、blind query 或其他读者信息。必须如实披露这一额外的非研究材料读取。
- [AUTHOR_FACT] 未枚举工作区，未读取 read_1、Cards、其他读者报告或 blind query，未联网。唯一写入目标是本 `report.md`。
- [AUTHOR_FACT] 实际工具轨迹：PowerShell/`shell_command` 读取提示词与 invocation（第一次沿终端默认编码显示乱码，随后以 UTF-8 显式重读）；`Get-FileHash` 核验 PDF；`pypdf` 获取元数据、页数并逐页提取 1–23 页；`PyMuPDF` 对 23 页做第二解析器核对，并重点复核页 4、8、13、21–23；`PyMuPDF + Pillow` 只在内存中渲染全 23 页缩略图和页 4、8、21、23 的可视图，不落盘。曾尝试调用 `pdfinfo`，因本机找不到该程序而失败，未由它取得任何 PDF 信息。
- [OPEN_QUESTION] 平台未提供可验证的文件级技术 allowlist 或 OS 级文件访问审计，因此本次隔离只能标为 `procedural_blinding`，不能声称技术隔离。平台可见任务名为 `/root/p014_second_read`；宿主 thread ID、底层库不可观察的内部系统调用以及精确部署构建号不可见。实际模型可表述为 Codex / GPT-5 系列，精确版本为 `unknown`。

## 1. 逐页覆盖记录

- [AUTHOR_FACT] PDF p.1（页脚 9956）：标题、摘要、§1、图 1；摘要称 IoRT 用 dynamic-meta instruction 和 refresh/stop/select 指令处理 redundant、drift、stubborn。
- [AUTHOR_FACT] PDF p.2（9957）：§1 余文与 §2.1；给出三类问题的定义，并强调不依赖 oracle labels。
- [AUTHOR_FACT] PDF p.3（9958）：§2.1–2.2、§3–3.1、图 2；比较 self-correct/CRITIC 在有无 oracle 评估下的迭代曲线。
- [AUTHOR_FACT] PDF p.4（9959）：§3.2、图 3、§4–4.1；给出四种迭代类型和不同模型的分布。
- [AUTHOR_FACT] PDF p.5（9960）：图 4、§4.1–4.2、式 (1)–(5)；描述 meta-memory、检索、生成、更新和反思响应。
- [AUTHOR_FACT] PDF p.6（9961）：§4.3、式 (6)–(7)、§5.1；定义 select/stop/refresh 与实验设置。
- [AUTHOR_FACT] PDF p.7（9962）：表 1、表 2、§5.2、§5.3 开头；给出数学与常识推理主结果和成本。
- [AUTHOR_FACT] PDF p.8（9963）：表 3、图 5、§5.3–§6；给出消融、调用量和随迭代变化的结果。
- [AUTHOR_FACT] PDF p.9（9964）：§6、§7、Limitations；讨论模型尺度、调用开销、误判和开放模型边界。
- [AUTHOR_FACT] PDF p.10–11（9965–9966）：References。
- [AUTHOR_FACT] PDF p.12（9967）：References 结束、附录 A、表 4–5、附录 C.1；给出评价方式、逐迭代转移比例和 meta-thought prompt。
- [AUTHOR_FACT] PDF p.13（9968）：表 6、附录 C.2；给出数据规模、few-shot 数和 refresh/self-reflect prompts。
- [AUTHOR_FACT] PDF p.14（9969）：附录 C.3；给出 select 与 refresh/stop prompts。
- [AUTHOR_FACT] PDF p.15–23（9970–9978）：附录 D，表 7–14；依次展示 stop、select、refresh 的 StrategyQA/GSM8K 案例。

## 2. 统一问题 1：方法究竟改变哪一步计算？

- [AUTHOR_FACT] IoRT 没有修改黑盒 LLM 的参数；它把静态链 `initial response → evaluation → revision` 改成 `initial response → evaluation → revision → instruction`，在每次反思后增加一个动态指令决策步骤。定位：PDF p.8，§6，短定位“dynamic iterative pipeline”。
- [AUTHOR_FACT] 第一阶段由 meta-thinker 从 meta-memory 中按问题嵌入余弦相似度检索 top-k `(question, meta-thought)` 对，生成当前问题的 meta-thought，并把新对加入 memory。定位：PDF p.5，§4.1，式 (1)–(4)，短定位“Retrieval / Generation / Updating”。
- [AUTHOR_FACT] 第二阶段先生成 basic/initial response；reflector 基于问题、basic response、抽取答案和 evaluation feedback 生成 reflective response。定位：PDF p.5，§4.2，式 (5)，短定位“Refresh and Self-Reflect”。
- [AUTHOR_FACT] 第三阶段先用不调用 LLM 的 self-consistency classifier 比较 basic answer 与 reflective answer 是否相等；不等时由 instructor 在 meta-thought 辅助下 select 较好响应，相等时由 instructor 决定 stop 或 refresh。定位：PDF p.6，§4.3，短定位“Does not use any LLM”及“Select / Stop / Refresh Instruction”。
- [READER_INTERPRETATION] 核心计算改动不是“反思生成器更强”，而是对两个候选答案做答案一致性门控，再让一个 LLM instructor 执行选择/停止/重启控制；meta-thought 是该控制器的附加判据。定位依据：PDF p.5 图 4；p.6 §4.3。
- [OPEN_QUESTION] §4.3 对 refresh 的状态更新写成“generate a new response to update `R^(i+1)_r`，而 `R^(i+1)_b = R^i_b`”，图 4 又呈现 refresh 后更新/重新生成的流程；论文没有给出完整伪代码来消除变量语义歧义。定位：PDF p.6，§4.3，短定位“Refresh Instruction”。

## 3. 统一问题 2：输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 外部输入是问题 `x`；最终输出是某一轮 instructor 选定/保留的响应 `R^i_o`，或达到最大迭代数 `N=4` 时的最后输出。若 stop，作者为了按轮评估把后续各轮都复制为该轮输出。定位：PDF p.5–6，§4.2–4.3，式 (5)–(7)；p.6 §5.1“maximum number of iterations to 4”。
- [AUTHOR_FACT] meta-thinker 可用当前问题、检索到的 top-k 问题/元思考对及手工初始化的 meta-memory；新生成的 meta-thought 会回写 memory。定位：PDF p.5，§4.1；p.13 表 6。
- [AUTHOR_FACT] reflector 可用问题、basic response、抽取的 basic answer 与自身生成的 evaluation feedback；数学任务中答案来自执行 PoT Python 代码，常识任务中答案通过正则从“so the answer is”之后抽取。定位：PDF p.5 §4.2；p.12 附录 A；p.13 附录 C.2。
- [AUTHOR_FACT] instructor 在答案不一致时可见问题、meta-thought、两份完整响应及两个抽取答案；答案一致时同样可见这些信息并决定 refresh/stop。定位：PDF p.6 §4.3；p.14 附录 C.3。
- [AUTHOR_FACT] 干预发生在每轮 reflective response 产生且答案被抽取之后、下一轮开始之前；图 4 说明重复步骤 8–14，直到 stop 或达到 `N`。定位：PDF p.5，图 4 caption。
- [READER_INTERPRETATION] 数学任务并非纯 intrinsic reflection，因为 reflector 能看到代码执行结果；但该结果不是“答案正确/错误”的 oracle label。常识任务没有同类工具执行反馈。定位依据：PDF p.3 §3.1；p.12 附录 A；p.13 prompts。
- [OPEN_QUESTION] meta-memory 在五次实验、不同测试样本、不同数据集或不同模型之间是否重置，论文未说明；因为它会持续加入当前测试问题的 meta-thought，结果可能依赖测试顺序和跨运行状态。定位：PDF p.5，§4.1“continuously evolves”；p.6 §5.1“五轮实验”。

## 4. 统一问题 3：最强基线与最接近组合基线

- [AUTHOR_FACT] 数学任务表 1 中，非 IoRT 的逐列最强结果并非单一方法：GSM8K 上分别为 Self-Contrast（GPT-3.5/GPT-4）、Multi-Agent（L-7B）、Self-Contrast（L-13B）、PoT+HSP（L-70B）；SVAMP 上分别为 Self-Contrast、PoT+HSP、PoT-SC(8)、PoT-SC(8)、PoT+HSP。定位：PDF p.7，表 1。
- [AUTHOR_FACT] StrategyQA 表 2 中，非 IoRT 的逐列最强结果分别为 CoT+HSP（GPT-3.5/GPT-4）、Multi-Agent（L-7B）、PS（L-13B）、Multi-Agent（L-70B）。定位：PDF p.7，表 2。
- [READER_INTERPRETATION] 组件上最接近的组合基线是数学的 PoT+HSP、常识的 CoT+HSP，因为它们同时使用相同初始推理范式与抽象提示，但把抽象知识用于初始作答而不是 instructor。流程上最接近的是 Self-Reflection 和 CRITIC（数学），而 Self-Contrast 是较强的多候选反思比较基线。定位依据：PDF p.6 §5.1；p.7 表 1–2、§5.2。
- [AUTHOR_FACT] IoRT 在数学十个模型×数据集单元中，相对 PoT 平均提高约 4.4%，相对 PoT+HSP 平均约 2.4%；CRITIC 相对 PoT 平均下降约 2.6%。StrategyQA 上 IoRT 相对 CoT 平均提高约 5.2%，相对 CoT+HSP 平均约 2.1%。定位：PDF p.7，§5.2，短定位“+4.4% / −2.6% / +2.4% / +5.2% / 2.1%”。
- [AUTHOR_FACT] 表 1 显示 IoRT 在 GPT-3.5/SVAMP 为 88.1，低于 Self-Contrast 的 89.0；在 GPT-4/GSM8K 为 95.4，与 Self-Contrast 95.4 持平，而不是全面严格胜出。定位：PDF p.7，表 1。
- [OPEN_QUESTION] 同页正文称 Self-Contrast 在“GSM8K with Llama2 7B”胜过 IoRT，但表 1 的对应值是 Self-Contrast 20.5、IoRT 24.0，方向相反；这是正文—表格的明确内部矛盾，需要原始实验表核验。定位：PDF p.7，§5.2，短定位“self-contrast outperforms our method”。

## 5. 统一问题 4：模型、token、tool-call、prompt、oracle 差异

- [AUTHOR_FACT] black-box LLM/reflector 使用 GPT-3.5-Turbo-0613、GPT-4-0613 或 Llama2-Chat 7B/13B/70B，但所有实验的 meta-thinker 和 instructor 都固定为 GPT-3.5-Turbo-0613。定位：PDF p.6，§5.1“GPT-3.5-Turbo-0613 serves as both”。
- [READER_INTERPRETATION] 因此 Llama2 行不是“只靠 Llama2”的增强：控制决策由 GPT-3.5 提供。若相应基线没有同等 GPT-3.5 调用，模型能力与方法结构无法完全分离。定位依据：PDF p.6 §5.1；p.9 Limitations。
- [AUTHOR_FACT] IoRT 数学平均调用数为 7.3；PoT/CoT 为 1、HSP 组合为 2、Self-Contrast 为 7.8、SC(8) 为 8、Self-Reflection/CRITIC 为 9。StrategyQA 仅报告 token：IoRT 3877，CoT 514，CoT+HSP 1018，CoT-SC(8) 4145，Multi-Agent 3922，Self-Reflection 5944。定位：PDF p.7，表 1–2。
- [READER_INTERPRETATION] 与 1–2 call 基线相比，增益可能部分来自更多采样/计算；与 Self-Contrast、SC、Self-Reflection 等高计算基线相比更接近，但论文没有逐模型、逐任务同时匹配 token、调用数和延迟。定位依据：PDF p.7 表 1–2；p.8 图 5。
- [AUTHOR_FACT] 数学任务采用 PoT 并执行代码；StrategyQA 采用 CoT 和正则答案抽取。IoRT、PoT/PoT+HSP 与 CRITIC 的数学设置更接近，跨“Text Describing Reasoning”和“Programming Language Reasoning”分组的直接比较仍含推理表示与工具差异。定位：PDF p.7 表 1 caption；p.12 附录 A。
- [AUTHOR_FACT] 表 1 caption 说明 CoT、CoT-SC(8)、Multi-Agent、Self-Contrast、Self-Reflection 的文本推理结果来自 Zhang et al. (2024)，不是全部在本文统一重跑。定位：PDF p.7，表 1 caption。
- [OPEN_QUESTION] 论文没有证明外部来源结果与本文运行在完全相同的模型快照、prompt、few-shot、温度、token 限额和评测脚本下；这限制了跨来源比较的严格性。定位：PDF p.6 §5.1；p.7 表 1 caption。
- [AUTHOR_FACT] IoRT 运行时不使用 ground-truth correctness oracle；self-consistency classifier 只比较两个抽取答案是否相等。图 2 中“w/ Oracle”是评估模拟：只累计错→对并忽略对→错。定位：PDF p.3，§3.1；p.6 §4.3。
- [READER_INTERPRETATION] “无 oracle”成立于控制器没有读取正确标签，但数学代码执行器仍提供外部执行反馈，且最终准确率、案例中的 ✓/✗ 当然由标准答案事后计算；两者不应混为一谈。定位依据：PDF p.3 §3.1；p.12 附录 A。
- [OPEN_QUESTION] 手工初始化 meta-thought、各任务不相同的 meta/refresh/reflect few-shot 数（数学 8/8/4，StrategyQA 6/5/3）以及 prompt 文案本身可能贡献增益；没有“相同调用预算 + 相同 GPT instructor + 随机/无信息 meta-thought”的完整对照。定位：PDF p.13，表 6；p.13–14 prompts。

## 6. 统一问题 5：限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者明示 IoRT 仍会误判；在 GPT-3.5 数学实验中，使用 oracle label 的最终迭代表现比 IoRT 高 1.6%。定位：PDF p.9，Limitations，短定位“exceeds our method by 1.6%”。
- [AUTHOR_FACT] 作者未用开源模型担任 meta-thinker/instructor，理由是其抽象推理和指导反思能力有限。定位：PDF p.9，Limitations。
- [AUTHOR_FACT] 静态反思存在真实负向结果：GSM8K/SVAMP 上 self-correct 与 CRITIC 无 oracle 时最多分别下降 2.4% 与 3.0%；表 5 中多轮的对→错比例常接近或超过错→对。定位：PDF p.3，图 2/§3.1；p.12，表 5。
- [AUTHOR_FACT] 消融 IoRT*（直接采用 reflective response、失去 select 保护）相对完整 IoRT 平均下降 4.4%；表 3 中还出现低于 initial 的单元，如 GPT-3.5/StrategyQA 65.9<66.8、L-7B/GSM8K 16.3<19.5、L-13B/StrategyQA 52.2<54.2。定位：PDF p.8，表 3/§5.3。
- [AUTHOR_FACT] 去掉 self-consistency 的 IoRT 平均准确率变化仅约 −0.51%，但必须跑满四轮；完整 IoRT 平均迭代 2.2。去掉 meta-thought 平均比完整 IoRT 低 2.1%，但仍比 initial 高 2.9%。定位：PDF p.8，§5.3。
- [READER_INTERPRETATION] 已测试边界很窄：仅 GSM8K、SVAMP、StrategyQA，输出类型仅数值或 T/F，模型为 2023 年快照 GPT 与 Llama2，固定温度 0.3、最大四轮；不能外推到开放式生成、长上下文、多工具代理、非英语、代码生成、安全任务或更新模型。定位依据：PDF p.6 §5.1；p.12–13 附录 A/表 6。
- [OPEN_QUESTION] 虽然每个数据集做五轮并报告平均值，但没有方差、置信区间或显著性检验；0.x–1.x 的差异是否稳定无法从论文判断。定位：PDF p.6，§5.1“five rounds”；p.7 表 1–2。

## 7. 统一问题 6：可抽取的 Operator 与真实 Failure

以下仅是二读核源层面的机制/失败定位，不生成 Card，也不作 Candidate 评价。

### Operator-like 机制

- [AUTHOR_FACT] `Meta-thought retrieve–generate–update`：检索相似问题的抽象解题知识，生成当前 meta-thought，并更新 memory。定位：PDF p.5，§4.1，式 (1)–(4)。
- [AUTHOR_FACT] `Answer-consistency gate`：不调用 LLM，仅判断 `A_b == A_r`，把控制流分为 select 与 stop/refresh 两支。定位：PDF p.6，§4.3。
- [AUTHOR_FACT] `Select`：答案不一致时，instructor 结合问题、两份响应、两答案和 meta-thought 选较优响应，并把它作为当前输出/下一轮基础。定位：PDF p.6，式 (6)；p.16–17、20–21，表 8–9、12–13。
- [AUTHOR_FACT] `Stop`：答案一致且 instructor 判断两者合理时提前终止，并复用该响应作为后续轮输出。定位：PDF p.6，式 (7)；p.15、19，表 7、11。
- [AUTHOR_FACT] `Refresh`：答案一致但 instructor 判断均未解题时，重新生成新思路以打破错误闭环。定位：PDF p.6 §4.3；p.18、22–23，表 10、14。
- [READER_INTERPRETATION] 三个控制 Operator 分别对应冗余（stop）、漂移（select）、顽固（refresh）；这是作者设计映射，不等于每次都能正确识别。定位依据：PDF p.2 §1；p.8 §6。

### 有数据或案例支持的 Failure

- [AUTHOR_FACT] `Redundant`：答案始终正确却继续反思，增加调用和延迟；图 3 中 GPT-3.5/GSM8K 的 redundant 占 50.4%，GPT-4 为 74.3%。定位：PDF p.4，图 3/§3.2。
- [AUTHOR_FACT] `Drift`：反思序列在正确/错误间变化，特别包括对→错；图 3 中 Llama2-7B/GSM8K drift 为 43.4%，表 5 给出每轮对→错比例。定位：PDF p.4，图 3；p.12，表 5。
- [AUTHOR_FACT] `Stubborn/invalid consistent`：始终坚持错误答案；图 3 中 GPT-3.5/GSM8K invalid-consistent 为 23.4%，GPT-4 为 20.0%。定位：PDF p.4，图 3/§3.2。
- [AUTHOR_FACT] `Invalid inconsistent`：持续变化却从未到达正确解；图 3 中 Llama2-7B/GSM8K 为 45.6%。定位：PDF p.4，图 3。
- [AUTHOR_FACT] `Instructor misjudgment`：作者明确承认 IoRT 仍有偶发误判，并以 oracle 比 IoRT 高 1.6% 量化上限差距。定位：PDF p.9，Limitations。
- [AUTHOR_FACT] `Reflector 破坏正确答案但 select 救回`：蜂蜇案例从正确 False 反思成错误 True，instructor 选回 CoT 0；公寓案例从正确 30.0 反思成错误 120.0，instructor 选回 Code 0。定位：PDF p.17 表 9；p.21 表 13。
- [OPEN_QUESTION] 表 13 的展示内容内部不一致：Code 1 与 Code 0 的可见代码相同且仍使用 `3/4`，但展示的抽取结果从 30.0 变成 120.0；instructor 又称 Code 1 使用 integer division。两个解析器和可视渲染均保留这一矛盾，需核查原始运行日志。定位：PDF p.21，表 13，短定位“Extract the Answer: 120.0”。
- [OPEN_QUESTION] 表 14 的 Code 2 使用可见的 `mod` 中缀写法，不是合法 Python；按展示公式，`cost_using_2 - cost_using_3 = 9 - 15 = -6`，却标为 `6.0 (✓)`，且没有可见 `abs`。两个解析器和可视渲染一致，需核查代码是否在排版时被改写或案例标签是否错误。定位：PDF p.23，表 14，短定位“Extract the Answer: 6.0”。

## 8. 统一问题 7–8：定位完整性与解析/可视冲突

- [AUTHOR_FACT] 上述判断均给出了 PDF 物理页、论文页脚页码、章节/图表/公式或短定位文本；页码以 PDF 物理页为主，避免仅用 proceedings 页码造成偏移。
- [AUTHOR_FACT] `pypdf` 在 PDF p.4 图 3 的图内字体上输出 `/uni...` 编码串；`PyMuPDF` 和可视渲染可恢复四个饼图及数值。因此这是第一解析器的字体映射失败，不是论文可视内容缺失。定位：PDF p.4，图 3。
- [AUTHOR_FACT] PDF p.8 表 3 的线性文本会把三列都抽成“IoRT”，但坐标与可视表头显示实际顺序为 `Initial | IoRT* | IoRT(w/o SC) | IoRT(w/o MT) | IoRT`；本报告按该顺序解释。定位：PDF p.8，表 3。
- [AUTHOR_FACT] 对 23 页进行了内存缩略图可视覆盖，并重点可视核查页 4、8、21、23；未发现页缺失、旋转、裁切或文本层与可视版面的大面积冲突。
- [OPEN_QUESTION] 除上面已确认的解析器字体/列顺序问题外，页 21 和页 23 的代码—输出矛盾在两种文本解析与可视渲染中均存在，不能归因于单一解析器；仍需作者代码或原始日志才能裁定。

## 9. 独立二读结论（非科研裁决）

- [READER_INTERPRETATION] IoRT 的可核源机制是：在静态反思后加入“答案一致性门控 + GPT-3.5 instructor + meta-thought”，用 select/stop/refresh 调节下一轮。主实验支持完整 IoRT 在三项封闭式推理任务上通常优于所列基线，并减少相对固定反思的调用量。
- [READER_INTERPRETATION] 证据解释必须保留四项边界：GPT-3.5 instructor 对所有基座模型的能力注入、调用/token 未完全匹配、部分基线结果来自外部论文、meta-memory 重置和测试顺序不明。
- [OPEN_QUESTION] 正文与表 1 的 Llama2-7B/Self-Contrast 比较矛盾，以及表 13–14 案例的代码/输出矛盾，均应在 reconciliation 时作为待核验 source conflict 保留，不能自动平滑掉。
