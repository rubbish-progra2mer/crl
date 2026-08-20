# P020 独立二读核源报告

## 0. 边界与来源

- 本报告对应 frozen invocation snapshot：`r2-20260719-p020-a1/invocation.md`，Attempt ID 为 `r2-20260719-p020-a1`。
- 论文：*AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks*；本地 PDF SHA-256 实测为 `454906b0f931fd092ab25163c1ea3fd69e793eac570320ba257d174bee9b0c7c`，与 invocation 一致；共 38 个 PDF 页面。
- 本报告是 fresh 独立核源，只回答统一问题；不生成 Card，不评价 Candidate、novelty 或科研价值。
- 页码均指 PDF 的 1-based 页码。短定位文本仅用于定位，不代表额外推断。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] AgentTTS 改变的是**多阶段任务运行前及运行间的配置搜索/资源分配步骤**：在固定总预算下，为每个子任务选择模型与样本数（等价预算），而不是训练或修改基础模型参数。形式化目标是选择 `B -> {B1,...,Bn}`、模型 `Mi` 并最大化整体任务表现。[PDF p.3，Sec.3，Definition 1；定位：`allocate the computational budget among subtasks`]
- [AUTHOR_FACT] 单个子任务的执行采用 repeated sampling with fusion：同一模型生成 `k` 个样本，再由同一 LLM 通过 fusion prompt 聚合，见 Eq.(1)。[PDF p.3，Sec.3，Eq.(1)；定位：`same LLM is used for both generating solutions and performing fusion`]
- [AUTHOR_FACT] 方法的搜索循环为：初始化候选配置，交给 Environment 实际执行，接收表现反馈，生成 guidelines，再生成受预算约束的新候选；Archive 保存 trial、反馈和 guideline，终止时返回历史最佳 trial。[PDF p.6，Algorithm 1 与 Fig.2；PDF pp.6-7，Sec.5；定位：`feedback-driven interactions with the execution environment`]
- [AUTHOR_FACT] 初始化阶段用 Insight 1 比较各子任务在同一预算下的候选模型，同时将其他子任务固定为各自最大可用模型的一次推理；若大模型未显著优于小模型，则后续优先小模型。后续阶段把 Insight 2（寻找样本数拐点）与 Insight 3（跨子任务平衡）写入 guideline prompt。[PDF pp.6-7，Sec.5，Eq.(5)；PDF pp.33-34，Appendix A.7 prompts]
- [AUTHOR_FACT] 不同模型/任务/样本数先通过 FLOPs 近似转换为统一预算；预算单位是最小模型 3B 在基准 `(Np=128, Nd=64)` 上生成一次的成本，见 Eq.(4)/(12)。[PDF p.4，Theorem 1，Eq.(4)；PDF pp.24-25，Appendix A.2，Eq.(6)-(12)]
- [READER_INTERPRETATION] 因而核心增量是“带领域规则的 LLM 黑盒配置优化器”：它在配置空间中改变下一批要评估的 `(模型, 样本数)`，而实际子任务推理仍是既定的 repeated-sampling-plus-fusion 执行算子。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 搜索输入包括：固定的有序子任务集合、每个子任务的模型候选、总预算 `B`、任务描述、平均 prompt/generation 长度、评价指标及主指标；trial-generation prompt 还接收可用 sample 候选、预算函数、历史 trial 和已有 guidelines。[PDF p.3，Definition 1；PDF pp.33-34，Appendix A.7]
- [AUTHOR_FACT] 每轮可用信息包括 Archive 中的已试配置、训练集表现反馈和先前 guidelines；Environment 把 trial 转成可执行脚本，在实际任务平台运行并返回表现。[PDF pp.6-7，Fig.2、Algorithm 1 Lines 3/5/7/8；定位：`performance feedback is returned to the Agent`]
- [AUTHOR_FACT] 中间输出是自然语言 guideline 与一批严格预算可行的 JSON 配置；最终输出是 Archive 中表现最佳的 trial。[PDF p.6，Algorithm 1 Line 10；PDF pp.33-34，Appendix A.7，trial schema]
- [AUTHOR_FACT] 干预发生在每一批 trial 执行之前：首次由 Insight 1 产生初始化 trial，之后由上一轮反馈产生 guideline 和下一轮 trial。论文称各搜索方法在 50 个训练样本上执行 50 次搜索，随后把所选 trial 在 500 个测试样本上评估。[PDF p.8，Sec.6 Experimental Setup；PDF p.27，Appendix A.4]
- [READER_INTERPRETATION] 测试集结果按论文叙述不应反馈给搜索器；搜索器实际看到的是小训练集上的 trial 分数。不过，设计 insight 所用的 pilot 实验与最终评估使用同一组六个数据集，是否存在严格独立的 pilot split，原文没有说明。
- [OPEN_QUESTION] `batch_size` 在 prompt 中是占位符，但正文没有给出其具体值，也未清楚说明“50 iterations”“50 trials”与按 batch 生成候选之间的精确换算。[PDF p.8，Fig.3/实验设置；PDF p.34，trial-generation prompt]

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 基线包含 Random Search、Bayesian Optimization、LLM_ZS、MLCopilot 和 AgentHPO；图中的 `Best` 是先前 grid search 找到的最优 trial，只作为 benchmark。[PDF p.8，Fig.3 caption 与 Experimental Setup；PDF pp.35-36，Appendix A.9]
- [AUTHOR_FACT] 表 1 中，没有一个基线在所有数据集都独占最优。AgentHPO 是整体上最稳定的强基线之一：2Wiki 为 0.70/8.3h，Hotpot 为 0.74/36.3h，CWQ 为 0.78/37.4h，WebQSP 为 0.89/48.1h；其中后三项测试指标与 Ours 持平，但搜索时间更长。TaskBench 上 MLCopilot 与 Ours 同为 0.53，ChatDev 上 BO/MLCopilot 与 Ours 同为 0.75，但相应找到最优 trial 的时间记为 `–`。[PDF p.8，Table 1]
- [READER_INTERPRETATION] 若“最强基线”要求单一名称，AgentHPO 最合适；若按数据集，则应使用上面的逐任务并列关系，不能概括成某一基线全面最强。
- [AUTHOR_FACT] 结构上最接近的是适配后的 AgentHPO 与 MLCopilot：二者同样采用“反馈驱动的 guideline 生成 + guideline 驱动的候选生成”两阶段循环；区别主要在初始化知识来源和 AgentTTS 注入的三条 TTS insight。[PDF p.8，baseline description；PDF pp.35-36，Appendix A.9]
- [AUTHOR_FACT] 论文另有 `w/o Insight 1/2/3` 的单项消融，但没有报告“同时移除全部三条 insight、其余 prompt/循环完全相同”的一个统一近邻消融。[PDF p.9，Fig.4(d) 与 Ablation Studies]
- [OPEN_QUESTION] 因此，最接近的“组合基线”只能判为适配后的 AgentHPO/MLCopilot；原文不足以隔离“统一 AgentTTS 实现骨架”相对“三条 insight 文本”各自的净贡献。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] 论文写明使用 GPT-o3-mini 作为 LLM search agent，所有方法在 50 个训练样本上搜索、在 500 个测试样本上评估，并执行 50 次搜索；任务执行模型池和评价任务在方法间按实验设置共用。[PDF p.8，Sec.6 Experimental Setup]
- [READER_INTERPRETATION] 仅凭这句话不能确认所有 LLM 基线的 search-agent 版本、系统提示、temperature、最大输出 token、失败重试和 API 时间点完全相同；这些设置未逐基线列出。
- [AUTHOR_FACT] Prompt/可用信息差异是实验处理本身：LLM_ZS 仅接收任务描述、模型选择和总预算；MLCopilot 接收类似任务的历史；AgentHPO 接收结构化任务输入并依赖反馈；AgentTTS 额外接收三条 insight 指令及 Archive 历史。[PDF p.8；PDF pp.33-36，Appendices A.7/A.9]
- [READER_INTERPRETATION] 因此表现差异确实可能部分来自 prompt 长度、上下文信息量与历史信息质量；论文把它们视为方法组成，而不是控制到相同 token/context 后的纯搜索算法差异。
- [AUTHOR_FACT] 下游 repeated sampling 默认 temperature 为 0.9，其余 decoding 参数保持默认；只在 2Wiki 上追加了 0.1/0.5/0.9 温度实验。[PDF p.27，Appendix A.4；PDF p.10，Table 2]
- [OPEN_QUESTION] 未报告 search-agent 自身的 decoding 参数、每轮 prompt/input/output token 数、候选生成失败/JSON 修复次数、Environment tool-call 次数或各方法相等的 LLM token/API 预算，故无法排除 token 与 tool-call 开销差异。
- [READER_INTERPRETATION] FLOPs 预算推导 Eq.(6)-(12)只计 prompt encoding 与 `S` 次 decoding，没有显式计入 Eq.(1) 的 fusion 调用及其随候选数量增长的输入长度。若 fusion 成本未另计，高 `S` 配置的实际推理成本会被系统性低估。[PDF p.3，Eq.(1)；PDF pp.24-25，Eq.(6)-(12)]
- [OPEN_QUESTION] fusion 计算是否计入各 trial 的预算、搜索时间和 API-price 实验，原文没有明确说明。
- [AUTHOR_FACT] `Best` 来自 prior grid search，并在图中作为所有方法的 benchmark。[PDF p.8，Fig.3 caption]
- [OPEN_QUESTION] 原文未明确 grid-search oracle 是否仅用于事后画参考线，还是还影响 stopping criterion、超参数选择或“找到最优”的时间统计；也未说明 insight pilot 与最终 train/test split 的隔离方式。
- [AUTHOR_FACT] NeurIPS checklist 明示“不报告方差，因为计算开销高”。[PDF p.18，Checklist Q7；定位：`we do not report variance`]
- [READER_INTERPRETATION] 无多随机种子、误差条或显著性检验时，图 3/4 的早到达 trial 和表 1 的小幅差异可能受训练样本抽样、LLM 采样或搜索随机性影响。

## 5. 作者明示限制、负向结果与未测试边界

### 5.1 明示限制

- [AUTHOR_FACT] 方法假设子任务集合是静态且预先确定的；输入条件或用户交互导致的动态阶段，会使预定义子任务与预算分配困难，作者称其为“considerable challenge”。[PDF p.37，Appendix A.11]
- [AUTHOR_FACT] 统计层面没有方差、置信区间或显著性信息，理由是计算开销高。[PDF p.18，Checklist Q7]
- [AUTHOR_FACT] FLOPs 推导忽略 attention 相关项，作者称其通常小于总 FLOPs 的 1%；所有 budget lookup 还依赖平均 token 长度而非逐样本实际长度。[PDF p.25，Appendix A.2；PDF p.25，Table 4]
- [AUTHOR_FACT] 方法基于 repeated sampling；作者在 broader impact 中指出它可能放大并传播基础 LLM 的 hallucination，也面临 jailbreak、backdoor injection 和 membership inference 风险。[PDF pp.37-38，Appendix A.12]

### 5.2 负向结果

- [AUTHOR_FACT] 多个子任务的表现随样本数先升后振荡/下降；作者把 fusion 在候选变多时变复杂视为瓶颈，小模型在高采样下更易退化。[PDF p.5，Sec.4.2，Fig.1；PDF pp.29-31，Figs.9-14]
- [AUTHOR_FACT] 低质量上游检索会推迟下游 QA 的最优预算，并使小模型更难赶上大模型；在 Fig.1(d) 中，3B/8B 的峰值没有超过 70B 的最低表现。[PDF p.5，Fig.1(c-d) 讨论]
- [AUTHOR_FACT] 消融中，移除 Insight 1 未到达最优配置；移除 Insight 2 和 3 分别把最优 trial 推迟到第 29 和第 38 步。[PDF p.9，Fig.4(d)]
- [AUTHOR_FACT] 作者报告 BO 在非平滑景观中可能陷入局部最优，Random Search 对噪声较稳健但低效；表 1 多处 `–` 表示结果不可用或未找到最优 trial。[PDF p.8，Main Results 与 Table 1；PDF p.36，Appendix A.9]
- [AUTHOR_FACT] 完整案例中，低容量模型采用 70-90 次采样会出现显著性能退化，更多样本不保证更好。[PDF p.32，Fig.15]

### 5.3 未测试或证据很窄的边界

- [READER_INTERPRETATION] 未测试：动态/分支/循环工作流；未知阶段数的大规模工作流；除四类任务六个数据集之外的领域；不同 search-agent LLM；多随机种子；不同模型家族混配的系统性控制；含 verifier、Best-of-N 或 tree-search 的多阶段分配；真实用户交互或线上流量。
- [AUTHOR_FACT] 成本指标主要是 FLOPs，只在 2Wiki 上给出 API-price 例子；温度敏感性也只在 2Wiki、固定 Qwen2.5-72B 单次检索和 LLaMA-3 3B QA 下测试。[PDF p.10，Fig.7、Table 2；PDF p.26，Appendix A.3]
- [OPEN_QUESTION] 没有 wall-clock/能耗/并发吞吐作为统一预算的完整复现实验；H100 单卡设置也不能说明在批处理、模型并行或 API 服务条件下搜索排序是否保持。[PDF p.27，Appendix A.4]
- [OPEN_QUESTION] ChatDev 只报告最终 Consistency，作者也称其没有中间步骤指标，因此跨阶段因果解释在该任务上不可直接观测。[PDF p.27，Appendix A.4/A.5]

## 6. 可抽取的 Operator 与真实可记录的 Failure

以下仅是对论文机制/失败证据的独立核源分类，不是 Card 或科研评价。

### 6.1 Operator

1. [AUTHOR_FACT] **统一预算映射算子**：把 `(模型规模, 样本数, 任务平均 Np/Nd)` 映射到 3B 基准单位预算；Eq.(12) 给出近似函数。[PDF pp.24-25，Appendix A.2]
2. [AUTHOR_FACT] **重复采样-同模融合算子**：生成 `k` 个候选，再由同一 LLM fusion。[PDF p.3，Eq.(1)；PDF p.33，Fusion Prompt]
3. [AUTHOR_FACT] **等预算模型偏好初始化算子**：逐子任务比较候选模型，其他子任务固定为最大模型一次推理；大模型若无显著优势则偏向小模型。[PDF pp.6-7，Eq.(5)]
4. [AUTHOR_FACT] **反馈到 guideline 算子**：依据历史表现生成关于样本数拐点、子任务优先级与跨阶段平衡的文字 guideline。[PDF p.6，Algorithm 1 Line 5；PDF pp.33-34]
5. [AUTHOR_FACT] **预算约束候选生成算子**：让 LLM 依据任务、模型空间、预算函数、历史与 guideline 输出指定批量 JSON 配置，并用 `check_budget`/Environment 执行核验。[PDF p.34，Trial Generation Prompt；PDF p.35，Fig.16]
6. [AUTHOR_FACT] **Archive-Environment 闭环选择算子**：记录 trial/反馈/guideline，迭代执行并返回历史最优。[PDF pp.6-7，Algorithm 1、Fig.2]

### 6.2 Failure

1. [AUTHOR_FACT] **组合爆炸/穷举不可行**：三阶段、每阶段 2 个模型、预算约 1768 的 ChatDev 示例有 1,854,841 个有效配置。[PDF p.23，Appendix A.1，Listing 1]
2. [AUTHOR_FACT] **过采样融合退化**：超过拐点后性能振荡或下降，作者归因为 fusion 复杂度增加，且小模型更脆弱。[PDF p.5，Fig.1 与 Insight 2]
3. [AUTHOR_FACT] **上游劣化传导**：低质量检索提高下游任务难度、推迟其预算峰值，并改变适合的模型规模。[PDF p.5，Fig.1(b-d) 与 Insight 3]
4. [AUTHOR_FACT] **Insight 缺失导致搜索失败/延迟**：无 Insight 1 未找到最优；无 Insight 2/3 分别延迟至 trial 29/38。[PDF p.9，Fig.4(d)]
5. [AUTHOR_FACT] **非平滑景观下 BO 局部最优与随机搜索低效**。[PDF p.8，Main Results；PDF p.36，Appendix A.9]
6. [AUTHOR_FACT] **静态阶段假设在动态工作流失效**：运行时阶段不可预定义时，预算分配框架难直接应用。[PDF p.37，Appendix A.11]
7. [READER_INTERPRETATION] **核算缺口风险**：若 fusion 调用未计入 Eq.(12)，高样本数的“同预算”比较可能不再同成本。这是由公式覆盖范围推得的风险，论文未报告为已观测 failure。[PDF p.3 vs. pp.24-25]

## 7. 关键判断定位索引

| 判断主题 | 主要定位 |
|---|---|
| 问题定义与输入/输出 | PDF p.3，Sec.3，Definition 1、Eq.(1) |
| 三条经验 insight | PDF pp.5-6，Sec.4.2，Fig.1 |
| AgentTTS 搜索循环 | PDF pp.6-7，Sec.5，Algorithm 1、Fig.2、Eq.(5) |
| 主基线与主结果 | PDF p.8，Fig.3、Table 1 |
| 消融、训练集大小、解释案例 | PDF p.9，Fig.4、Fig.5 |
| 预算/温度/API-price 边界 | PDF p.10，Fig.6、Fig.7、Table 2 |
| Checklist：无方差 | PDF p.18，Checklist Q7 |
| Checklist：LLM usage 声明 | PDF p.22，Checklist Q16 |
| 穷举规模示例 | PDF p.23，Appendix A.1，Listing 1 |
| FLOPs 推导与 token 长度表 | PDF pp.24-26，Appendix A.2，Eq.(6)-(12)、Tables 3-9 |
| 数据、模型、指标、GPU/划分 | PDF pp.26-27，Appendix A.4 |
| 扩展 scaling 曲线 | PDF pp.28-31，Figs.8-14 |
| 完整搜索案例 | PDF p.32，Fig.15 |
| 完整 prompts | PDF pp.33-34，Appendix A.7 |
| 基线细节 | PDF pp.35-36，Appendix A.9 |
| 限制与 broader impact | PDF pp.37-38，Appendices A.11-A.12 |

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 已逐页提取 38 页文本，并检查覆盖全部 38 页的页面渲染缩略图；另对 PDF p.22（LLM checklist）、p.25（Table 4/预算表）、p.27（A.4 设置）做了更高分辨率页面核对。公式、表格标题、图注、checklist 答案与提取文本未发现实质性的“解析文本 vs 可视页面”冲突。
- [READER_INTERPRETATION] 多栏图（尤其 pp.29-32）的文本提取顺序会重复或打乱 panel 标签，不能仅凭抽取顺序恢复曲线；本报告的趋势判断依据正文解释、图注和可视页面共同核对，未对曲线逐像素数字化。
- [OPEN_QUESTION] 由于没有对所有曲线点进行图像数字化，正文未逐点列出的精确数值不能从本次核读中独立复算。

### 8.1 论文内容内部的不一致（不是解析错误）

1. [AUTHOR_FACT] Table 4 把 CWQ-R、WebQSP-R 的平均长度列为 `1024/64`，WebQSP-QA 为 `128/64`；A.4 正文却称两个 KGQA 数据集的 retrieval 都是 `2048/64`、QA 都是 `256/64`。[PDF p.25，Table 4；PDF p.27，Appendix A.4]
2. [AUTHOR_FACT] Table 4 把 TaskBench-Decomposition 列为 `1024/64`；A.4 正文称其为 `2048/64`。[PDF p.25，Table 4；PDF p.27，Appendix A.4]
3. [READER_INTERPRETATION] 上述长度直接进入预算函数，故不仅是排版差异，也会改变 normalized budget；需要作者/代码确认实际使用哪组数值。
4. [AUTHOR_FACT] A.4 对 retrieval-QA 的回答模型写成 LLaMA-3 `(3B, 8B, 72B)`，而主文、图例和预算表使用 70B/LLaMA-3.1-70B。[PDF p.27，Appendix A.4；PDF p.5，Fig.1；PDF pp.25-26，Tables 5-9]
5. [AUTHOR_FACT] Checklist Q16“Declaration of LLM usage”回答 `[NA]`，但核心方法明确把 LLM 作为 Agent，并在实验中使用 GPT-o3-mini 作为 search agent。[PDF p.22，Checklist Q16；PDF pp.6-8，Sec.5-6]
6. [READER_INTERPRETATION] Q16 的 `[NA]` 与正文方法描述存在明显语义冲突；这不是 PDF 解析问题，因为可视页面明确显示 `[NA]`。

## 9. Provenance、实际读取与可观察 trace

### 9.1 实际读取文件

研究输入（仅以下三项）：

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P020_agenttts.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P020/read_2_attempts/r2-20260719-p020-a1/invocation.md`

运行时指令文件（非研究输入；因系统要求使用 PDF skill 而读取）：

4. `C:/Users/g/.codex/skills/pdf/SKILL.md`
5. `C:/Users/g/.codex/plugins/cache/openai-curated-remote/superpowers/6.1.1/skills/verification-before-completion/SKILL.md`

未枚举工作区，未读取 read_1、Cards、其他报告、blind query 或其他项目研究文件；未联网。App 未提供可验证的文件级 allowlist，本次边界只能如 invocation 所述记为 `procedural_blinding`，不声称技术隔离或 read-only 隔离。

### 9.2 工具、模型与任务标识

- 工具：PowerShell `Get-Content`/`Test-Path`；Python 3；PyMuPDF 1.27.2.2（页数、metadata、逐页文本抽取与内存渲染）；Pillow（内存 contact sheet/JPEG）；`apply_patch`（仅写本报告）。
- 网络：未调用网络工具。
- Actual model/version：`unknown`（运行界面未暴露可核验的精确模型版本）。
- Canonical task identifier：`/root/p020_second_read`（当前协作任务可见标识）。
- Thread ID：`unavailable`。
- Attempt ID：`r2-20260719-p020-a1`。

### 9.3 可观察 file-access/tool trace

1. 读取 PDF skill 指令；提交前读取 verification-before-completion 指令。
2. 首次并行读取 prompt/invocation/pdfinfo 调用整体返回“找不到指定路径”；随后只对三个获准研究输入做 `Test-Path`，三者均为 `True`。
3. 首次 `Get-Content` 输出 prompt 出现终端编码乱码；随后用显式 UTF-8 读取 prompt 与 invocation。
4. 对 PDF 计算 SHA-256，读取 metadata 与页数：38 页，PyMuPDF 1.27.2.2。
5. 逐页抽取批次：pp.1-8、9-16、17-24、25-32、33-38。
6. 内存页面渲染核对批次：pp.1-4、5-10、11-16、17-22、23-28、29-34、35-38；追加高分辨率检查 p.22、p.25、p.27。所有渲染经 stdout/base64 直接送入可视检查，未写中间图片文件。
7. 仅写入本 `report.md`。
