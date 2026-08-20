# P009 独立第二读报告

## 0. 身份、边界与 provenance

- 本报告对应冻结快照：`r2-20260719-p009-a1/invocation.md`，Attempt ID 为 `r2-20260719-p009-a1`，启动时间为 `2026-07-19T17:28:00+08:00`。
- [AUTHOR_FACT] 论文 canonical metadata：*MemGPT: Towards LLMs as Operating Systems*，arXiv:2310.08560，PDF 共 13 个物理页；PDF 内页码与物理页码 1–13 一致。PDF SHA-256 实测为 `9F674BCFF69C86F11C813DFAD613D8841F5F8ED17979E3C4DF06A91DF7762E0`，与 invocation 一致。
- Prompt SHA-256 实测为 `FFB7C12E663F44318D8EDA1C270CBC26AD66665FD803247A2AB66A8F23FA333A`，与 invocation 一致。
- Actual model/version：OpenAI Codex（GPT-5 系列）；更细部署版本不可见。Canonical collaboration task path：`/root/p009_second_read`；宿主 thread ID 不可见。
- Path enforcement：`procedural_blinding`。App 未提供可验证的文件级 allowlist，因此不能把本次边界称为技术隔离。
- 本次没有联网，没有读取首读、Cards、其他报告或 blind query，没有生成 Card，也没有作 Candidate 评价或科研 Reviewer 裁决。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] MemGPT 不改底层 Transformer 权重或注意力计算；它把固定上下文 LLM 包装为一个具有“主上下文—外部上下文”层级、队列管理器和函数执行器的系统。LLM 的提示 token 是主上下文，外部数据只有被显式移入主上下文后才参与下一次推理。[物理页2/印刷页2，§2、§2.1，定位：“must always be explicitly moved into main context”]
- [AUTHOR_FACT] 主上下文被拆为只读 system instructions、可由函数修改的 working context，以及保存滚动消息历史的 FIFO queue；FIFO 首项保存被逐出消息的递归摘要。[页2，§2.1，定位：“split into three contiguous sections”]
- [AUTHOR_FACT] 每次新消息到达时，队列管理器追加消息、拼接 prompt、触发 LLM 推理，并把输入消息和 LLM 输出写入 recall storage。到达 warning token count（例示 70%）时插入 memory-pressure 警告；到达 flush token count（例示 100%）时逐出一定消息（例示 50%）并重写递归摘要。[页2–3，§2.2，定位：“warning token count”；“flushes the queue”]
- [AUTHOR_FACT] LLM completion 被解析为函数调用；参数通过校验后执行，结果或运行时错误再反馈给 LLM。检索支持分页，避免一次检索撑爆上下文。[页3，§2.3，定位：“parsed by MemGPT”；“implement pagination”]
- [AUTHOR_FACT] 函数可携带 `request_heartbeat=true`，要求函数执行完立即再次推理，从而在向用户返回前串联多次检索/编辑。[页3–4，Fig.3、§2.4，定位：“Function chaining allows”]
- [READER_INTERPRETATION] 因而被改变的不是单次 LLM 的 token-to-token 映射，而是**推理前后的上下文组装、外部存储读写、溢出处理和多轮工具控制流**：同一固定窗口 LLM 被置于一个能自我选择何时查、写、逐出、再推理的闭环中。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 输入事件可为用户消息、系统消息（含容量警告）、用户交互状态、定时事件；事件先被解析为纯文本并加入主上下文，随后触发推理。[页4，§2.4，定位：“events trigger LLM inference”]
- [AUTHOR_FACT] 单次 LLM 输入是拼接后的主上下文：system instructions + working context + FIFO queue；外部 recall/archive storage 不能被模型直接注意，须经函数检索后作为消息回填。[页2–3，§2.1、Fig.3，定位：“Prompt Tokens”；“Read via Functions”]
- [AUTHOR_FACT] 单次 LLM 输出是 completion string，可被解释为函数调用或面向用户的回复。函数输出、错误和分页结果又成为后续推理可见输入。[页3，§2.3，定位：“output string is parsed”；“fed back to the processor”]
- [AUTHOR_FACT] 系统可用信息包括：working context 中显式保存的事实；FIFO 中近期消息和递归摘要；recall storage 中完整消息记录；archival storage 中任意长度文本对象；函数 schema、自然语言说明和 token-limit 警告。[页2–3，§2.1–2.3]
- [AUTHOR_FACT] 干预发生在四类时点：外部事件到达时；warning threshold 触发时；flush threshold 触发时；LLM 主动发函数调用并用 heartbeat 请求继续推理时。[页3–4，§2.2–2.4]
- [READER_INTERPRETATION] 最终用户级输出不是一次 completion 的必然直接产物，而可能是“事件→推理→函数→回填→再推理”的可变长度轨迹。论文未把最大链长、最大工具调用数或统一停止预算写成实验控制变量。

## 3. 最强基线与最接近组合基线

### 3.1 对话任务

- [AUTHOR_FACT] DMR 的固定上下文基线是相同基础 LLM 不加 MemGPT，并向其提供过去五次会话的有损摘要；MemGPT 可访问完整历史，但必须通过分页 recall search 调入上下文。[页5，§3.1.1，Table 2 后文，定位：“lossy summarization”；“full conversation history”]
- [AUTHOR_FACT] Table 2 中，固定基线的最高 Accuracy/ROUGE-L(R) 是 GPT-3.5 Turbo 的 38.7%/0.394；对应 MemGPT 版本为 66.9%/0.629。GPT-4 与 GPT-4 Turbo 的对应 MemGPT 版本分别达到 92.5%/0.814 与 93.4%/0.827。[页5，Table 2]
- [READER_INTERPRETATION] DMR 最接近的组合基线是“相同基础 LLM + 递归式有损会话摘要”，因为它也试图延长历史，但没有可查询的完整 recall store。它仍不是等信息量基线。
- [AUTHOR_FACT] opener 实验以 MSC persona 和人工 opener 作相似度参照；Table 3 中 MemGPT(GPT-4) 的 SIM-1/SIM-3 最高（0.868/0.843），Human 的 SIM-H 为 1.000。该表未报告一个“不带 MemGPT、只看固定窗口历史”的独立 LLM opener 基线。[页5–6，§3.1.2，Table 3]

### 3.2 文档 QA

- [AUTHOR_FACT] 固定上下文与 MemGPT 使用同一 OpenAI `text-embedding-ada-002` 表示和 cosine-similarity retriever；固定基线在 LLM 推理前独立取 top-K 文档，MemGPT 则把整个 embedding 文档集装入 archival storage，并可多次搜索和翻页。[页6，§3.2.1，定位：“both ... use the same retriever”]
- [AUTHOR_FACT] 为把固定上下文基线推到默认长度之外，作者截断各检索文档段以塞入相同数量的文档，且报告截断加剧时准确率下降。Fig.5 只给曲线，没有数值表；正文称 MemGPT(GPT-4) 与 MemGPT(GPT-4 Turbo) 在该任务结果相同。[页6–7，Fig.5、§3.2.1]
- [READER_INTERPRETATION] 最接近组合基线是“相同向量检索器 + 固定 top-K reader + 超窗时段落截断”。论文没有实验比较 FLARE、迭代 RAG 或其他同样允许主动多次检索的组合系统；这些只在 Related Work 出现。[页8，§4，定位：“FLARE”；“interleave retrieval”]

### 3.3 嵌套 KV

- [AUTHOR_FACT] 固定基线在约 8k token 上下文中获得全部 140 个 UUID 键值对，并被明确要求递归 lookup；作者称 GPT-4 Turbo 是较强固定基线，但 GPT-4/GPT-4 Turbo 到 3 层嵌套时均降为 0。[页7–8，Fig.7、§3.2.2；页13，§6.1.6]
- [READER_INTERPRETATION] 这里的最接近基线是“全量 KV 在上下文内 + 明示 nested lookup 的基础 LLM”；它与 MemGPT 的主要差别是后者以工具查询逐跳取得记录并可链式调用。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] 作者做了同基础模型的成对比较（GPT-3.5、GPT-4、GPT-4 Turbo），并明确观察到底层模型的函数调用能力影响 MemGPT：文档 QA 中 GPT-3.5 版显著退化；nested KV 中 MemGPT(GPT-4 Turbo) 反而弱于 MemGPT(GPT-4)。[页4，§3 Implementation details；页7，Fig.7 与 §3.2.1]
- [READER_INTERPRETATION] 成对模型控制能排除一部分“仅因换模型”的解释，但不能排除 tool-use 能力与方法交互；作者自己把 GPT-3.5 的退化归因于 limited function calling capabilities。[页7，§3.2.1]
- [AUTHOR_FACT] DMR 中 MemGPT 可查询完整会话历史，固定基线只有有损摘要；document QA 中 MemGPT 可反复查询整个存储，固定基线只得到预取 top-K，超窗后还被截断。[页5，§3.1.1；页6–7，§3.2.1]
- [READER_INTERPRETATION] 因此信息量、token 分配和检索轮次是机制组成部分，也是归因混杂项。现有结果不能把收益进一步拆成“外部存储容量”“主动检索策略”“递归摘要质量”“更多工具调用”各自贡献。
- [AUTHOR_FACT] 提示词不对称：DMR 的 MemGPT persona 要求用 core memory 和 conversation search 作 best guess，基线被要求信息不足时返回 `NO ANSWER`；文档 MemGPT 被告知答案“ALWAYS”在 archival memory 且要持续搜索，基线仅在给定文档列表内回答；KV MemGPT 更被全大写要求“DO NOT STOP SEARCHING UNTIL”确认 value 不再是 key。[页11–13，§6.1.1、§6.1.4、§6.1.6]
- [READER_INTERPRETATION] 上述 prompt/oracle 差异可能提高 MemGPT 的搜索坚持度，尤其与作者记录的“未执行足够 lookup”直接相关；论文没有提供 prompt-matched 消融。
- [AUTHOR_FACT] DMR QA 由另一个 LLM 生成，正确性用 GPT-4 judge；文档 QA 也由 LLM judge 判定答案及证据文本是否匹配。DMR judge 被要求“generous with your grading”。[页5，§3.1.1；页7，§3.2.1；页11–13，§6.1.2、§6.1.5]
- [OPEN_QUESTION] judge 的具体重复性、人工复核比例、盲化方式和对不同回答风格的偏差未报告。MemGPT 回答更长，而 DMR 又使用 ROUGE-L recall 并采用宽松 judge，verbosity 是否带来系统性优势无法由本文解决。[页5–6，§3.1.1–3.1.2]
- [OPEN_QUESTION] 各方法的平均 prompt/completion token、工具调用次数、检索页数、延迟和费用未报告，因而无法判断收益是否在相同推理预算下成立。

## 5. 作者明示限制、负向结果和未测试边界

- [AUTHOR_FACT] 文档 QA 受 embedding similarity search 限制；gold document 常落在前十余条之外。MemGPT 理论上可继续分页，但实测常在遍历完结果库前停止。[页7，§3.2.1，定位：“often stop paging”]
- [AUTHOR_FACT] 文档 QA 的 MemGPT(GPT-3.5) 因函数调用能力有限而显著退化，并以 GPT-4 最好。[页7，§3.2.1，末段]
- [AUTHOR_FACT] Nested KV：GPT-3.5 固定基线在 1 层嵌套即为 0%；GPT-4 与 GPT-4 Turbo 到 3 层为 0%；MemGPT(GPT-4) 不随层数下降，但 MemGPT(GPT-4 Turbo/GPT-3.5) 从 2 层开始下降，作者归因为没有完成足够 lookup。[页8，§3.2.2]
- [AUTHOR_FACT] 实验范围有限：document QA 仅从 NaturalQuestions-Open 抽 50 个问题；nested KV 为 140 对、0–4 层、30 个排序配置；对话为 MSC 五次会话并新增第六次单 QA。[页5，§3.1.1；页7–8，§3.2.1–3.2.2]
- [AUTHOR_FACT] Appendix 明言文中 MemGPT prompts 为简写，完整实现细节和 exact prompts 不在 PDF 内。[页11，§6.1，定位：“edited for brevity”]
- [READER_INTERPRETATION] 论文没有报告置信区间、显著性检验、独立重复运行、工具失败率、内存写错/污染率、冲突事实处理正确率或摘要累积误差。
- [OPEN_QUESTION] 未测试边界至少包括：对抗性/错误外部记忆、恶意 prompt 注入、隐私删除与持久存储治理、长链工具错误恢复、跨数据库一致性、并发事件、真实多年会话、百万 token 真实法律/金融文档、开源基础模型以及等成本/等延迟比较。结论只应外推到本文给出的两个领域与具体合成/半合成设置。
- [READER_INTERPRETATION] §5 把其他领域、不同数据库/缓存层和更好的控制流/内存策略列为未来方向，这也反向说明这些并未在本文验证。[页8，§5，定位：“future exploration”]

## 6. 可抽取的 Operator 与真实可记录的 Failure

这里仅做独立源内抽取，不生成正式 Card。

### 6.1 Operator

- [AUTHOR_FACT] **分层上下文分页**：把有限 prompt 作为 main context，把 recall/archive 作为 external context，借助函数在层间搬运信息。[页2–3，§2、Fig.3]
- [AUTHOR_FACT] **可写工作记忆**：以 append/replace 等函数把稳定事实、偏好和人物状态写入 working context。[页2，§2.1；Fig.1、Fig.4]
- [AUTHOR_FACT] **压力感知逐出**：warning threshold 先通知模型保存重要信息，flush threshold 再逐出并更新递归摘要。[页3，§2.2]
- [AUTHOR_FACT] **完整消息日志 + 按需 recall**：所有输入/输出长期写入 recall storage，离开窗口后仍可搜索并分页回填。[页2–3，§2.2；Fig.2]
- [AUTHOR_FACT] **主动 archival retrieval**：模型自行构造查询、翻页和组合多条检索结果。[页6–7，§3.2.1；Fig.6]
- [AUTHOR_FACT] **heartbeat 函数链**：函数完成后立即再推理，支持多跳查询后再 yield。[页3–4，Fig.3、§2.4]
- [AUTHOR_FACT] **事件/中断控制流**：用户、系统、交互状态和定时事件均可触发推理。[页4，§2.4]

### 6.2 实证记录到的 Failure

- [AUTHOR_FACT] **检索提前停止**：MemGPT 在文档 QA 中常未遍历完检索结果就停止分页。[页7，§3.2.1]
- [AUTHOR_FACT] **弱函数调用模型退化**：MemGPT(GPT-3.5) 在文档 QA 显著降级，作者归因于 limited function calling capabilities。[页7，§3.2.1]
- [AUTHOR_FACT] **多跳深度失败**：固定 GPT-3.5 在一层 nested KV 即归零，GPT-4/4 Turbo 到三层归零；MemGPT(GPT-4 Turbo/GPT-3.5) 从两层开始下降，原因是调用 lookup 次数不足。[页8，§3.2.2；Fig.7]
- [AUTHOR_FACT] **截断导致证据丢失**：固定基线为容纳更多文档而缩短段落时，gold snippet 被省略概率增加，准确率下降。[页7，§3.2.1；Fig.5]
- [READER_INTERPRETATION] §2.3 所举“working context 已满仍添加”会产生 runtime error，但论文只说明系统会把错误反馈给模型，没有给出该错误的实测发生率或任务后果，因此不能把它当作已量化的实验 Failure。[页3，§2.3]

## 7. 定位索引与逐页检查记录

本报告所有判断均使用“物理页/印刷页 + 章节/图表 + 短定位文本”。逐页覆盖如下：

| 页 | 已核对内容 | 关键定位 |
|---|---|---|
| 1 | 摘要、动机、虚拟内存类比、函数调用总览 | Abstract；§1 “illusion of an infinite context” |
| 2 | Fig.1/2；主/外部上下文；主上下文三区；queue manager 开头 | §2–2.2 “three contiguous sections” |
| 3 | Fig.3；warning/flush；函数执行器；分页与错误回填 | §2.2–2.3 “request_heartbeat=true” |
| 4 | Table 1；事件控制流；函数链；实验与模型 endpoint | §2.4、§3 “events trigger” |
| 5 | DMR 与 opener 的数据、指标、Table 2/3、摘要基线 | §3.1.1–3.1.2 “lossy summarization” |
| 6 | Fig.5/6；document QA 设置、相同 retriever | §3.2.1 “same retriever” |
| 7 | Fig.7/8；50 问题；提前停止；截断；GPT-3.5 退化 | §3.2.1 “often stop paging” |
| 8 | Nested KV 负向结果；Related Work；Conclusion | §3.2.2 “failing to perform enough lookups” |
| 9 | References（前半） | References |
| 10 | References（后半） | References |
| 11 | prompts 简写声明；DMR persona/baseline/judge prompt | §6.1–6.1.3 “edited for brevity” |
| 12 | DMR 生成 prompt；document MemGPT/baseline prompt；judge 开头 | §6.1.3–6.1.5 “ALWAYS be in your archival memory” |
| 13 | document judge 结尾；KV MemGPT/baseline prompt | §6.1.5–6.1.6 “DO NOT STOP SEARCHING” |

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 已对 13 个物理页逐页提取文本，并以内存渲染方式检查全部页面的可视缩略图；页序、双栏结构、章节分布、Table 1–3、Fig.1–8 和 Appendix 布局与解析文本总体一致，未发现实质内容冲突。
- [READER_INTERPRETATION] 解析存在版面顺序伪影但不构成论文内容冲突：页2 的 Fig.1/2 图内对话被抽取两次；页4、页6–7 的图内文本会插入正文阅读顺序；页7 的 “Nesting Level” 首字母被抽成异常 glyph；连字有 `ﬁ/ﬂ` 形式。报告中的数值与结论均以正文、表格标题和可视布局交叉核对，未把这些伪影当作重复证据。
- [OPEN_QUESTION] 本次可视核验为全页缩略图结构检查，足以发现页缺失、图表/正文大范围错配和明显渲染冲突，但不等价于逐像素 forensic comparison；曲线 Fig.5/7 中未印为表格的精确坐标不作人工估读。

## 9. 实际读取文件、工具与 trace 可见性

### 实际读取文件

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P009_memgpt.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P009/read_2_attempts/r2-20260719-p009-a1/invocation.md`
4. 非研究材料、为遵守 PDF 任务所读取的技能说明：`C:/Users/g/.codex/skills/pdf/SKILL.md`

除上述文件外未读取其他文件；未枚举工作区。唯一写入是本 `report.md`。

### 实际使用工具

- Codex `functions.exec` 调度本地 `shell_command` 与 `apply_patch`。
- PowerShell/.NET：UTF-8 `ReadAllText`、`Get-FileHash`、`Get-Command`。
- `pdftotext` 检测为不可用；`pdfinfo` shim 调用失败，未用于论文判断。
- Python 本地库：`pypdf 6.9.1` 逐页文本与 metadata；`PyMuPDF/fitz 1.27.2.2` + Pillow 在内存中渲染可视缩略图；未落地中间图像或文本。
- 仅检测了 `pdfplumber 0.11.9` 的可用性，未用它读取论文内容。
- 网络：未使用。

### Observable trace

- 系统级、可独立审计的完整 file-access/tool trace：`unavailable`。
- 可观察范围仅限本任务会话中实际返回的命令输出、哈希、逐页文本和内存渲染结果，以及本节的自报工具记录；这不构成文件级技术隔离证明。
