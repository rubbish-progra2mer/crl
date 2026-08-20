# P011 fresh 独立二读报告

- Attempt：`r2-20260719-p011-a1`
- 论文：*On Memory Construction and Retrieval for Personalized Conversational Agents*（ICLR 2025）
- 本报告引用的冻结 snapshot：`read_2_attempts/r2-20260719-p011-a1/invocation.md`，SHA-256=`ca0d60c1a7733c1250b78c5d4b9ea2f6e50dc54f932e4deb201c67cdd3871df5`
- PDF 核验：SHA-256=`998ab05ece554a83870b1baf5762f314837165e99f22ef2af8ffd7ba473c5004`，与 invocation 一致；共 35 个 PDF 页面，页脚编号 1–35。
- 任务边界：独立核源；不生成 Card，不评价 Candidate，不与任何其他读者结论合并。

## 一、方法究竟改变哪一步计算？

- [AUTHOR_FACT] SECOM 首先改变**记忆构建的粒度**：把每个会话 `c_i` 划分为连续、无重叠、主题一致的 segments，并令每个 segment 成为一个 memory unit，而非把单 turn 或整 session 当作 memory unit。定位：PDF p4，§2.1–2.2，Eq. (1)，短定位文本：“construct a segment-level memory bank”。
- [AUTHOR_FACT] SECOM 还改变**检索前的 memory 表示**：对 memory bank 的每个单元先用 LLMLingua-2 压缩，再由原检索器检索；公式写为 `f_R(u*, f_Comp(M), N)`。定位：PDF p5，§2.3，Eq. (2)，短定位文本：“denoise memory units … before retrieval”。
- [AUTHOR_FACT] 主流程中的检索器和生成器接口没有被重新定义：给定当前请求 `u*` 与预算 `N`，检索 `N` 个单元，将其按时间顺序作为上下文，再由 `f_LLM` 生成响应。定位：PDF p4，§2.1，短定位文本：“take the retrieved N memory units in time order”。
- [READER_INTERPRETATION] 因而核心计算变化是两段前处理的组合：`会话→主题段` 与 `原始段→压缩段`；它不是新的生成解码算法，也不是新的 BM25/MPNet 相似度函数。定位：PDF p4–5，§2.1–2.3，Eq. (1)–(2)。

## 二、输入、输出、可用信息与干预时点

| 阶段 | 输入与可用信息 | 输出 | 干预时点 | 核源 |
|---|---|---|---|---|
| 记忆构建 | 完整历史 `H={c_i}`；每个 session 内的有序 user-agent turns；zero-shot 模式不使用分割标注 | 连续 topical segments 与 segment-level bank | 当前问题到来前，可离线执行 | [AUTHOR_FACT] PDF p4，§2.1–2.2，Eq. (1)；p16，Fig. 6 |
| 有限标注反思分割 | 带真值边界的训练会话；按 WindowDiff 选出的 top-100 hard examples；既有 rubric/examples | 10 条 rubric 与代表例，拼入后续分割 prompt | 仅在有分割标注的 segmentation benchmark 训练/迁移阶段 | [AUTHOR_FACT] PDF p5，§2.2；p15，§A.1；p17，Fig. 7；p23，Fig. 8 |
| 记忆去噪 | 已构建 memory units；LLMLingua-2，75% compression rate，`xlm-roberta-large` | 压缩后的 memory units | 检索前 | [AUTHOR_FACT] PDF p5，§2.3、Implementation Details，Eq. (2) |
| 检索 | 当前请求 `u*`、压缩 bank、预算 `N`；BM25 或 MPNet+FAISS | top-`N` memory units | 响应生成前 | [AUTHOR_FACT] PDF p4–5，§2.1、§3 |
| 生成 | 当前请求与按时间重排的已检索上下文；主实验 GPT-35-Turbo，鲁棒性实验 Mistral-7B-Instruct-v0.3 | 最终 response `r*` | 最后一步 | [AUTHOR_FACT] PDF p4–5，§2.1、§3 |

- [AUTHOR_FACT] QA 主实验使用 zero-shot segmentation；作者明确说 LOCOMO 与 Long-MT-Bench+ 不使用 rubric。定位：PDF p5，§3 “We employ zero-shot segmentation for QA benchmarks”；p15，§A.1 “do not use any rubric”。
- [READER_INTERPRETATION] main QA 推断时没有显式使用测试答案或检索真值边界作为 SECOM 输入；但问答数据构造、GPT-4 评分和分割模型均涉及 GPT-4，不能据此推断整个评测链完全独立。定位：PDF p5，§3 Datasets & Evaluation；p18，§A.4；p20，§A.7。

## 三、最强基线与最接近组合基线

- [AUTHOR_FACT] 按 Table 1 的主指标 GPT4Score，LOCOMO 上最强非 SECOM 方法是 ConditionMem（65.92），最强简单粒度基线是 Turn-Level(BM25)（65.58）；SECOM(BM25, GPT4-Seg) 为 71.57。定位：PDF p6，Table 1，LOCOMO 行。
- [AUTHOR_FACT] 按同表 GPT4Score，Long-MT-Bench+ 上最强非 SECOM 方法是 MemoChat（85.14），最强简单粒度基线是 Turn-Level(MPNet)（84.91）；SECOM(MPNet, GPT4-Seg) 为 88.81。定位：PDF p6，Table 1，Long-MT-Bench+ 行。
- [READER_INTERPRETATION] **结构上最接近的外部组合基线**是 MemoChat：它同样在 segment level 操作记忆，但用经过调优的 LLM 负责记忆构建与检索；它没有构成“同一分割器 + 同一检索器 + 仅去掉压缩”的严格配对。定位：PDF p6，§3 Baselines，短定位文本：“operates memories at segment level”。
- [READER_INTERPRETATION] **最接近的内部因果对照**是 `SECOM −Denoise`（Table 2），它只拿掉压缩去噪；粒度的内部对照则是对 turn/session/segment 都施加 compression 的 Figure 5。定位：PDF p7，Ablation Study on Granularity；p8，Table 2。
- [OPEN_QUESTION] “最强基线”会随指标、检索器和数据集而变化；论文没有预注册唯一主指标，也没有报告置信区间或显著性检验，因此不能把单一排名解释为统计显著优胜。定位：PDF p5，§3 Evaluation Metrics；p6，Table 1。

## 四、结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] 主表内 SECOM 与 turn/session 共享 GPT-35-Turbo 响应生成器，并分别使用同类 BM25/MPNet 检索器；作者还说明主结果中的 turn/session 基线也使用 compression denoising。定位：PDF p5，§3 Implementation Details；p6，§3 Baselines，短定位文本：“denoising-enhanced turn-level and session-level baselines”。
- [READER_INTERPRETATION] 因此，SECOM 对相同 retriever 的 turn/session 差异较难完全归因为响应模型或压缩开关；Figure 5 与 Table 2 是最有诊断力的配对证据。定位：PDF p7，Fig. 5；p8，Table 2。
- [AUTHOR_FACT] 不同外部基线采用不同记忆生成、摘要、检索机制；MemoChat 还调优 LLM。定位：PDF p6，§3 Baselines。
- [READER_INTERPRETATION] 与 SumMem/RecurSum/ConditionMem/MemoChat 的端到端差异仍是复合差异，可能混入 model、prompt、memory tokenization、调用次数与实现质量，不能只归因于“segment+compression”。定位：PDF p6，Table 1 与 Baselines。
- [AUTHOR_FACT] Table 1 标称 LOCOMO/Long-MT-Bench+ 检索预算分别为 4k/1k tokens，但 Long-MT-Bench+ 的 session-level 实际上下文为约 3,680–4,118 tokens，turn/segment 约 820–1,047 tokens；MemoChat 为 1,615 tokens。定位：PDF p6，Table 1 表题及 `# Tokens` 列。
- [OPEN_QUESTION] 标称 1k token 预算如何约束不可切分的整 session、不同方法超预算时如何处理，原文未说明。这个差异没有明显偏袒 SECOM（session 获得更多 token 仍更差），但会妨碍严格的等预算归因。定位：PDF p6，Table 1。
- [AUTHOR_FACT] Long-MT-Bench+ 的长程问题部分由 GPT-4 生成，原始 LOCOMO 主实验 QA 也由 GPT-4 生成；GPT4Score 又由 GPT-4-0125 打分，分割器主版本为 GPT-4-0125。定位：PDF p5，§3 Datasets & Evaluation；p15，§A.1；p20，§A.7；p27，Fig. 12。
- [READER_INTERPRETATION] 同一模型家族参与数据生成、分割和裁判，存在风格同源或 judge 偏好这一未隔离因素；官方 LOCOMO QA 的 Table 6 与十人 human evaluation 提供了部分缓解，但没有完全排除。定位：PDF p18，Table 6、§A.4–A.5；p21–22，§A.10、Table 10。
- [AUTHOR_FACT] segmentation transfer 的 reflection 以 ground-truth segmentation 与 WindowDiff 选 top-100 hard examples；这属于训练期监督信息，不用于作者所述的 main QA zero-shot segmentation。定位：PDF p5，§2.2；p15，§A.1。
- [OPEN_QUESTION] Table 5 报告了总 input/output tokens 与 latency，但没有给出各阶段 API/tool-call 数、离线构建成本的摊销方式、硬件与并发设置。定位：PDF p15，Table 5、§A.2。

## 五、作者明示限制、负向结果与未测试边界

### 作者明示/可直接定位的限制与负向结果

- [AUTHOR_FACT] 作者承认开放域会话分割标注难、边界具有歧义，人工标注也困难。定位：PDF p4，§2.2，短定位文本：“ambiguous nature of segmentation points”。
- [AUTHOR_FACT] Figure 3 只显示 compression rate 超过 50% 时，在给定设置下检索 recall 持续改善；没有报告低于 50% 的区间。定位：PDF p3，Fig. 3 及正文。
- [AUTHOR_FACT] 去掉 denoise 后，LOCOMO GPT4Score 从 69.33 降至 59.87（−9.46），Long-MT-Bench+ 从 88.81 降至 87.51（−1.30）；压缩作用具有明显数据集差异。定位：PDF p7–8，Ablation、Table 2。
- [AUTHOR_FACT] GPT-4 zero-shot 分割可能过细；Figure 11 的例子从真值 2 段切成预测 5 段，WindowDiff=0.80。定位：PDF p26，Fig. 11，短定位文本：“favors a more fine-grained segmentation”。
- [AUTHOR_FACT] 小分割模型会降级：Long-MT-Bench+ 上 RoBERTa-Seg GPT4Score=81.52，低于 Turn-Level(MPNet)=84.91 与 MemoChat=85.14；Mistral-Seg=86.32，GPT-4-Seg=88.81。定位：PDF p22，Table 11。
- [AUTHOR_FACT] 在官方 LOCOMO QA 的 Mistral 生成设置中，MemoChat 因经常无法生成构建 memory bank 所需的有效 JSON 而不适用。定位：PDF p18，Table 6 表注。
- [READER_INTERPRETATION] 论文没有独立的 `Limitations` 章节；上述是正文/附录中散落的限制或负向观测，不能替代完整风险清单。定位：PDF p10，§5 后直接进入 References；p15 起为 Appendix。

### 原文未覆盖或不足以解决的边界

- [OPEN_QUESTION] 未单独测量压缩 memory 的事实保真、否定词/数字/时间更新保留率；端到端 QA 上升不能证明所有压缩单元语义无损。定位：PDF p3，Fig. 3；p5，§2.3；p8，Table 2。
- [OPEN_QUESTION] 未测试在线持续写入、记忆冲突/过期、删除与遗忘、隐私、安全注入、跨语言、真实用户长期使用或多模态会话。论文实验均基于静态基准历史。定位：PDF p5，§3 Datasets；p20–21，§A.7、§A.9。
- [OPEN_QUESTION] Long-MT-Bench+ 是把五个连续 session 合并并由 GPT-4 生成更多问题；它与自然发生的长期关系型对话之间的外部效度未验证。定位：PDF p5，§3；p20，§A.7、Table 7。
- [OPEN_QUESTION] CoQA/Persona-Chat 附加实验聚合相邻样本且只抽取子集；未报告随机种子、多次抽样方差。定位：PDF p20–21，§A.9、Tables 8–9。
- [OPEN_QUESTION] 人评只说明 10 位标注者与五个维度，未在本文页内报告样本量、盲法、标注者一致性或不确定区间。定位：PDF p21–22，§A.10、Table 10。
- [OPEN_QUESTION] 多张表使用“significant”描述优势，但未见统计检验、置信区间或多重比较控制。定位：PDF p6–8，Main Results/Ablations；p10，Conclusion。

## 六、可抽取的 Operator 与真实可记录的 Failure

以下只做独立证据抽取，不作 Candidate 评价。

### Operator

1. [AUTHOR_FACT] **连续主题分段算子**：为 turn 加索引/role，令 LLM 一次性输出覆盖全部 turns、连续且不重叠的 JSONL 边界。定位：PDF p4，§2.2，Eq. (1)；p16，Fig. 6。
2. [AUTHOR_FACT] **有限标注反思算子**：按 WindowDiff 选 hard examples，分 mini-batches 让 LLM 反思错误、更新 rubric，并保留代表例。定位：PDF p5，§2.2；p15，§A.1；p17，Fig. 7；p23–25，Figs. 8–10。
3. [AUTHOR_FACT] **压缩去噪算子**：用 LLMLingua-2 以 75% compression rate 先压缩全部 memory units，再执行 BM25/MPNet 检索。定位：PDF p5，§2.3，Eq. (2)、Implementation Details。
4. [AUTHOR_FACT] **检索后时间重排算子**：先按相关性取 top-`N`，再按时间顺序拼接给生成器。定位：PDF p4，§2.1。
5. [READER_INTERPRETATION] **直接保留原对话内容算子**：segment retrieval 后直接拼接 segment，避免先摘要再取回造成的细节损失。定位：PDF p3，Introduction，短定位文本：“bypassing summarization”。

### Failure

1. [AUTHOR_FACT] **turn-level 碎片化/关键词缺失导致漏取与误取**：Figure 1 标出 false negative/false positive；Figure 13 中只取回标题 turn 却缺失完整故事，生成器声称没有故事。定位：PDF p2，Fig. 1；p28–29，Fig. 13。
2. [AUTHOR_FACT] **session-level 过粗导致无关内容干扰**：Figure 14 中目标不等式已在 session 内，模型仍声称未提供第二个不等式。定位：PDF p2，Fig. 1；p30–31，Fig. 14。
3. [AUTHOR_FACT] **摘要记忆丢失回答所需细节**：RecurSum 丢失“两项奥斯卡/给导演的启示”，ConditionMem 还错误丢弃有用 turns，二者回答成 `Free Solo`。定位：PDF p7，Main Results；p32–33，Fig. 15；p34–35，Fig. 16。
4. [AUTHOR_FACT] **无 compression 时检索/端到端性能下降**：LOCOMO GPT4Score −9.46，Long-MT-Bench+ −1.30。定位：PDF p8，Table 2。
5. [AUTHOR_FACT] **zero-shot GPT-4 过分割**：示例 WindowDiff=0.80。定位：PDF p26，Fig. 11。
6. [AUTHOR_FACT] **轻量分割器性能折损**：RoBERTa-Seg 在 Long-MT-Bench+ 低于最强 turn-level 与 MemoChat。定位：PDF p22，Table 11。
7. [AUTHOR_FACT] **基线的结构化输出失败**：Mistral 不能稳定完成 MemoChat 的有效 JSON “Memo Writing”。定位：PDF p18，Table 6 表注。

## 七、页级核查清单

| PDF 页 | 逐页检查内容 | 关键定位 |
|---:|---|---|
| 1 | 标题、摘要、研究动机 | Abstract；§1 开始 |
| 2 | turn/session/summary/segment 的语义差异 | Fig. 1；“fragmentary”“irrelevant”“information loss” |
| 3 | 粒度与压缩的预备实验、贡献 | Figs. 2–3 |
| 4 | 三阶段形式化；分段定义与 zero-shot 方案 | §2.1–2.2；Eq. (1) |
| 5 | reflection、压缩公式、实现、数据与评测 | §2.2–2.3；Eq. (2)；§3 |
| 6 | 主结果、预算、八类基线 | Table 1；Baselines |
| 7 | pairwise、粒度 ablation、压缩 ablation 引入 | Fig. 4；Fig. 5 |
| 8 | 去噪 ablation；Mistral 生成；分割评测设置 | Tables 2–3；Eq. (3) |
| 9 | 三个分割数据集结果；memory/segmentation related work | Table 4；§4.1 |
| 10 | chunking/denoising related work；结论 | §4.2–4.3；§5 |
| 11 | References | Conneau–Kim |
| 12 | References | Kim–Mishra |
| 13 | References | Pan–LangChain |
| 14 | References | LangChain–Zhong |
| 15 | References 结束；分割细节、成本、prefix analogy | §A.1–A.3；Table 5 |
| 16 | zero-shot segmentation prompt | Fig. 6；Eq. (4) |
| 17 | reflection rubric 生成 prompt | Fig. 7 |
| 18 | 官方 LOCOMO QA；评测 prompt 说明 | Table 6；§A.4–A.6；Eq. (5) |
| 19 | case-study 引言续页 | §A.6 |
| 20 | 数据构造、DCG、额外数据集 | Table 7；§A.7–A.9；Eq. (6) |
| 21 | CoQA/Persona-Chat 结果；human eval 与小模型引入 | Tables 8–9；§A.10–A.11 |
| 22 | 人评与分割器大小结果 | Tables 10–11 |
| 23 | 带 reflection 的 segmentation prompt | Fig. 8 |
| 24 | TIAGE 学得的 rubric | Fig. 9 |
| 25 | SuperDialSeg 学得的 rubric | Fig. 10 |
| 26 | GPT-4 zero-shot 过分割实例 | Fig. 11；WindowDiff=0.80 |
| 27 | GPT-4 单样本与 pairwise 评测 prompt | Fig. 12 |
| 28 | turn-level case 前半：历史、问题、错误回答 | Fig. 13 上半 |
| 29 | segment-level 对照与正确回答 | Fig. 13 下半 |
| 30 | session-level case 前半：无关内容与错误回答 | Fig. 14 上半 |
| 31 | segment-level 对照与正确回答 | Fig. 14 下半 |
| 32 | RecurSum case 前半：摘要丢失细节 | Fig. 15 上半 |
| 33 | segment-level 对照与正确回答 | Fig. 15 下半 |
| 34 | ConditionMem case 前半：摘要/丢弃有用 turn | Fig. 16 上半 |
| 35 | segment-level 对照与正确回答 | Fig. 16 下半 |

## 八、解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] PyMuPDF 文本层成功覆盖全部 35 页；页脚 1–35、章节顺序、Tables 1–11、Figures 1–16、Eqs. (1)–(6) 均能在解析文本中定位。
- [READER_INTERPRETATION] 对 1–35 页逐页进行了**内存渲染**版面复核，未发现页缺失、页序错乱、标题/表图不存在或跨页案例对应错误。重要表格数值以文本层逐项读取，渲染图用于确认版面与图表存在性。
- [READER_INTERPRETATION] 文本解析会线性化双栏、表格、公式与图内标签，尤其 p2–3、p6–9、p16–17、p23–35；这属于阅读顺序/视觉语义损失，不是已确认的内容冲突。p28–35 的颜色高亮在文本层不会保留颜色含义，但可视页确有彩色强调。
- [OPEN_QUESTION] 本轮渲染为适合逐页核查的缩略级 raster，不构成逐像素印刷质量审计；细小图例颜色、线条精确坐标与字体嵌入未单独验证。
- [OPEN_QUESTION] invocation 的 canonical title 带前缀 `SeCom:`，而 PDF 可视首页题名为 `On Memory Construction and Retrieval for Personalized Conversational Agents`；这可能只是 canonical 命名规范差异，PDF 内未解释。定位：invocation metadata；PDF p1 标题。

## Provenance、实际读取文件与可观察 trace

### 实际读取文件

仅读取了以下三份输入：

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P011_secom.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P011/read_2_attempts/r2-20260719-p011-a1/invocation.md`

未枚举工作区；未读取 read_1、Cards、其他读者报告或 blind query；未联网。

### 工具与文件访问 trace

- `shell_command` + PowerShell：对上述三个明确路径执行 `Get-Item` 元数据检查；对 prompt/invocation 执行一次 `Get-Content -Raw`。该次控制台编码导致中文 mojibake，随后以 UTF-8 重新读取核对。
- `shell_command` + Python：用 `Path.read_bytes()` 读取 prompt 与 invocation，核验 UTF-8 内容和 SHA-256；prompt SHA-256=`ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。
- `shell_command` + Python/PyMuPDF (`fitz`)：读取 PDF metadata、页数和 1–35 页文本层，分四批输出逐页内容；用 `hashlib` 核验 PDF SHA-256。
- `shell_command` + Python/PyMuPDF：将 1–35 页逐页直接渲染到内存并编码为 JPEG 供可视复核；未写入临时图片。
- 曾尝试本地 `pdfinfo`，命令因系统找不到路径而失败；之后未依赖其结果。
- 为验证工具返回值封装，执行过一次不访问文件的 `Write-Output 'probe'`。
- 写入仅为本报告 `report.md`；没有生成其他产物。
- 首次写入后仅对本报告执行一次 `Get-Item` 元数据检查；该次检查确认文件存在、当时长度为 19,404 bytes，未回读报告正文。

### 平台可观察性限制

- Actual model/version：`Codex（系统明示基于 GPT-5）`；更细的模型 build/version 未向本代理暴露，记为 `unknown`。
- Canonical task：`/root/p011_second_read`；独立的底层 thread ID 未向本代理暴露，记为 `unknown`。
- Path allowlist：平台没有向本代理提供可验证的文件级 allowlist，故严格按 invocation 执行 `procedural_blinding`；不声称存在技术隔离。
- 平台未提供 syscall 级或全局 file-access 审计日志；以上 trace 是本代理可观察并实际发起的工具调用，无法证明平台内部不存在不可见访问。
