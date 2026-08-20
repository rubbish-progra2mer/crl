# P001 fresh independent read-3 全文核源报告

## 0. Provenance 与边界

- Invocation snapshot：`r3-20260719-p001-a1/invocation.md`；本报告引用其中冻结的 exact request、canonical metadata 与 prompt bytes。
- [AUTHOR_FACT] 输入 PDF 的实测 SHA-256 为 `f285b0971ae4a790e402fb93966bed3adde2cf0a04977d08b2b40d6ab0cace69`，与 invocation 记录一致。
- [AUTHOR_FACT] PDF 共 33 个物理页；页脚论文页码亦为 1--33，因此下文 `p.N` 同时指 PDF 物理页与论文印刷页。
- [READER_INTERPRETATION] 本报告只做独立全文核源与机制/边界拆解，不生成 Card，不评价 Candidate、novelty 或科研价值。

## 1. 逐页覆盖记录

| 页 | 实际检查内容 |
|---|---|
| p.1 | 标题、摘要、Introduction 起始 |
| p.2 | Figure 1；CoT/Act/ReAct 对照；动机 |
| p.3 | 贡献；Section 2 形式化与总体方法 |
| p.4 | Section 2 特性；3.1 setup；3.2 起始 |
| p.5 | Table 1、Figure 2；基线、混合策略、微调 |
| p.6 | Table 2；HotpotQA/FEVER 结果与失败分析 |
| p.7 | Figure 3；Section 4；ALFWorld、WebShop 设置 |
| p.8 | Tables 3--4；决策任务结果；ReAct-IM |
| p.9 | Related Work；Conclusion 起始 |
| p.10 | Conclusion；reproducibility、ethics；参考文献起始 |
| p.11 | 参考文献 |
| p.12 | 参考文献 |
| p.13 | 参考文献结束 |
| p.14 | Appendix A；Table 5、Figure 4；human-in-the-loop 起始 |
| p.15 | Figure 5；微调细节；ReAct-IM 细节 |
| p.16 | HotpotQA prompts：Original、Act 起始 |
| p.17 | HotpotQA prompts：Act、CoT、ReAct 起始 |
| p.18 | HotpotQA ReAct prompts 续 |
| p.19 | HotpotQA ReAct prompts 结束 |
| p.20 | FEVER prompts：Original、Act、CoT 起始 |
| p.21 | FEVER prompts：CoT、ReAct |
| p.22 | Table 6：WebShop Act/ReAct prompts |
| p.23 | Table 7：ALFWorld Act prompt（含内部不一致，见 §8） |
| p.24 | Table 8：ALFWorld ReAct prompt |
| p.25 | Table 9：ReAct-IM prompt；trajectory appendix 起始 |
| p.26 | FEVER 三个对照轨迹 |
| p.27 | FEVER 第四轨迹；ALFWorld trajectories 起始 |
| p.28 | ReAct ALFWorld trajectory；Act 失败说明 |
| p.29 | Act ALFWorld trajectory；ReAct-IM 失败说明 |
| p.30 | ReAct-IM ALFWorld trajectory |
| p.31 | Table 10：WebShop Act/ReAct trajectory |
| p.32 | Appendix E；成功、假阳性、推理错误样例 |
| p.33 | 搜索错误、幻觉、标签歧义样例 |

## 2. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] 一般代理原本按 `π(a_t | c_t)` 从环境上下文选择动作；ReAct 将动作空间从 `A` 扩为 `Â = A ∪ L`，其中语言空间 `L` 中的 thought 不改变外部环境、也不产生环境 observation，而是把 thought 写回上下文供后续推理或行动使用。定位：p.3，Section 2，短定位文本 “augment the agent's action space”。
- [READER_INTERPRETATION] 因而核心计算变化不是更换环境转移函数，而是在每个环境动作前后允许一次“上下文内的语言状态更新”：`c_t -> (c_t, thought) -> action -> observation`。该中间语言状态承担目标分解、计划更新、观测摘要、常识注入、异常恢复和进度跟踪。定位：p.3，Section 2，列举 “decomposing task goals”“track progress”“handle exceptions”。
- [AUTHOR_FACT] 在知识密集任务中，作者让模型密集交替生成 Thought、Action、Observation；在长时程决策任务中，thought 稀疏且异步出现，由模型自行决定何时思考或行动。定位：pp.3--4，Section 2，短定位文本 “alternate the generation” 与 “appear sparsely”。
- [AUTHOR_FACT] 主实验以冻结的 PaLM-540B 为基础，通过少量人工轨迹做 in-context prompting；附录另报告 GPT-3 `text-davinci-002`，并对 PaLM-8B/62B 做 3,000 条正确生成轨迹的微调实验。定位：p.3 Section 2；p.5 Section 3.2 “using 3,000 trajectories”；p.14 Table 5。
- [READER_INTERPRETATION] ReAct 的最小可分离干预是“在同一动作/观察轨迹上加入可自由生成的 thought token”；知识任务中的 Wikipedia 工具接入是另一项同时存在但可由 ReAct-vs-Act 对照部分隔离的干预。定位：p.5 Section 3.2 “Act ... removes thoughts”；pp.7--8 Section 4。

## 3. 输入、输出、可用信息与干预时点

### 3.1 通用接口

- [AUTHOR_FACT] 时刻 `t` 的输入是上下文 `c_t=(o_1,a_1,...,o_t)`；输出可以是环境动作 `a_t∈A`，也可以是语言 thought `â_t∈L`。thought 只更新上下文；环境动作才触发 observation。定位：p.3，Section 2，公式段。
- [AUTHOR_FACT] 可用信息包括任务输入、此前动作与环境观测、此前 thought，以及冻结 LLM 的参数内知识；不同任务的外部环境分别为 Wikipedia API、ALFWorld 文本环境和 WebShop 页面环境。定位：pp.3--4 Sections 2--3；p.7 Section 4。
- [READER_INTERPRETATION] 干预发生在解码时的轨迹生成层：prompt 用示范规定 Thought/Action/Observation 的语法和行为模式，模型在运行中把外部反馈再次纳入下一次生成，而不是事后重排一个已完成答案。定位：p.2 Figure 1；pp.16--25 Appendix C prompts。

### 3.2 知识密集任务

- [AUTHOR_FACT] HotpotQA 与 FEVER 采用 question-only 设置，模型不接收 supporting paragraphs；内部知识或外部检索是可用信息来源。定位：p.4 Section 3.1，短定位文本 “question-only setup”。
- [AUTHOR_FACT] Wikipedia API 的动作是 `search[entity]`（实体页首 5 句或相似实体）、`lookup[string]`（下一条含该字符串的句子）和 `finish[answer]`。作者明确称该 action space 弱于 SOTA retriever。定位：p.4 Section 3.1 “Action Space”。
- [AUTHOR_FACT] HotpotQA/FEVER 分别使用 6/3 个随机训练案例，人工编写 dense Thought-Action-Observation demonstrations；作者称更多示例没有提升。定位：p.4 Section 3.2 及脚注 2。
- [AUTHOR_FACT] `ReAct -> CoT-SC` 在 ReAct 未于 HotpotQA 7 步或 FEVER 5 步内返回答案时回退到 CoT-SC；`CoT-SC -> ReAct` 在 `n` 个 CoT 样本的多数答案少于 `n/2` 时回退到 ReAct。定位：p.5 Section 3.2 “Combining Internal and External Knowledge”。

### 3.3 决策任务

- [AUTHOR_FACT] ALFWorld 输入为高层目标与文本化房间状态，输出为导航/交互动作；ReAct 的 sparse thoughts 用于目标分解、子目标完成跟踪、下一子目标选择及物品位置常识。定位：p.7 Section 4 “ALFWorld”；pp.23--25 Tables 7--9。
- [AUTHOR_FACT] ALFWorld 每个 task type 人工标注 3 条训练轨迹，并用其中 2 条的 6 种排列构造 prompts；评估为 134 个 unseen games。定位：p.7 Section 4。
- [AUTHOR_FACT] WebShop 输入为用户购物约束及网页 observation，输出包括 search、选择商品/选项和 buy；评价为 500 条 test instructions 的平均属性覆盖分数与完全满足约束的成功率。定位：p.7 Section 4 “WebShop”；p.22 Table 6。

## 4. 最强基线与最接近组合基线

### 4.1 HotpotQA / FEVER

- [AUTHOR_FACT] Table 1 的 PaLM-540B 结果为：Standard `28.7/57.1`，CoT `29.4/56.3`，CoT-SC `33.4/60.4`，Act `25.7/58.9`，ReAct `27.4/60.9`，`CoT-SC -> ReAct` `34.2/64.6`，`ReAct -> CoT-SC` `35.1/62.0`（前者为 HotpotQA EM，后者为 FEVER Acc）。定位：p.5 Table 1。
- [READER_INTERPRETATION] 不含 ReAct 的最强 prompting 基线是 CoT-SC；最接近的机制对照是 Act（同样调用 Wikipedia 工具，仅移除 thought）。CoT 是 reasoning-only 对照，而不是同工具预算对照。定位：p.5 Section 3.2 “Baselines”。
- [AUTHOR_FACT] 混合方法中，HotpotQA 最好的是 `ReAct -> CoT-SC` 35.1，FEVER 最好的是 `CoT-SC -> ReAct` 64.6；监督式任务专用 SoTA 为 67.5/89.5，但作者承认 prompting 方法仍显著落后。定位：p.5 Table 1；p.6 Section 3.3 末段。
- [READER_INTERPRETATION] “最接近组合基线”是 CoT-SC 本身加上两个方向的 gated fallback；论文没有报告同 token、同 sample、同 tool-call 预算的纯组合控制项。定位：pp.5--6 Figure 2 与混合策略段。

### 4.2 ALFWorld / WebShop

- [AUTHOR_FACT] ALFWorld 总成功率：Act best-of-6 45，ReAct average 57，ReAct best-of-6 71，ReAct-IM average 48，ReAct-IM best-of-6 53，BUTLER best-of-8 37。定位：p.8 Table 3。
- [READER_INTERPRETATION] ALFWorld 最接近 ReAct 的两项对照分别是 Act（移除 thoughts）与 ReAct-IM（保留 dense 外部反馈式 thoughts，但限制内部推理类型）。定位：pp.7--8 Section 4；p.15 Appendix B.2。
- [AUTHOR_FACT] WebShop：Act `Score 62.3 / SR 30.1`，ReAct `66.6 / 40.0`，IL `59.9 / 29.1`，IL+RL `62.4 / 28.7`，Human Expert `82.1 / 59.6`。定位：p.8 Table 4。
- [READER_INTERPRETATION] WebShop 的最近控制基线是 Act，因为 Table 6 左右两列的任务、页面信息和动作空间相同，右列主要增加 thought；按 SR 看 Act 也是非 ReAct 自动方法中最高者。定位：p.22 Table 6。

## 5. 模型、token、tool-call、prompt 与 oracle 差异

- [AUTHOR_FACT] 知识任务的 Standard/CoT 不访问 Wikipedia，而 Act/ReAct 访问 API；因此 ReAct 对 Standard/CoT 的差异同时包含外部信息访问。定位：pp.4--5 Sections 3.1--3.2。
- [READER_INTERPRETATION] ReAct-vs-Act 更能隔离 thought 的作用，但仍未隔离额外生成 token、上下文长度、解码时延和潜在更多/不同检索动作；论文未给每题 token、tool-call 或 wall-clock 预算。定位：p.5 baseline 构造；全文未见成本表。
- [AUTHOR_FACT] CoT-SC 以温度 0.7 采样 21 条 CoT 轨迹并多数投票；主 ReAct/Act 示例和决策任务采用 greedy decoding。定位：p.5 Section 3.2；p.8 Table 3 caption；p.14 Table 5。
- [READER_INTERPRETATION] 因此 CoT-SC、单轨 ReAct 及二者混合的推理计算预算并不等价；Figure 2 虽按 CoT-SC sample 数展示曲线，但没有折算 ReAct 的 token/tool 成本。定位：pp.5--6 Figure 2。
- [AUTHOR_FACT] ALFWorld 的 ReAct/Act prompts 来自相同随机训练轨迹，Act 被描述为删除 thoughts，且 6 个 prompt 排列均报告 average/best；BUTLER 则用 `10^5` expert trajectories/type 且 beam search。定位：p.7 setup；p.8 Table 3 caption。
- [READER_INTERPRETATION] ALFWorld 的 ReAct-vs-Act 设计相对受控，但 best-of-6 是按同一批 134 个 unseen games 的结果择优；原文未说明另有 prompt-selection split，因此 best 数字可能包含选择优势。定位：pp.7--8。
- [OPEN_QUESTION] Table 7 的可视 Act prompt 实际含一条 `think:`，与表题 “No thoughts are provided” 及正文“without thoughts”冲突；无法仅凭论文判断这是排版遗留、真实实验 prompt 污染，还是示例误标。定位：p.23 Table 7，短定位文本 “Now I clean a lettuce”。
- [AUTHOR_FACT] WebShop 的 IL/IL+RL 使用 1,012 条人工轨迹，IL+RL 另用 10,587 条训练 instructions；ReAct/Act 为 one-shot prompting。定位：pp.7--8。
- [READER_INTERPRETATION] 训练数据量对 ReAct 有利于“少样本”叙述，但并不自动使方法预算可比：预训练模型规模、prompt token 和在线页面交互成本均未与 IL/RL 统一。
- [AUTHOR_FACT] 微调实验只保留由各方法生成且最终答案正确的 3,000 条轨迹。定位：p.5 Section 3.2 “Finetuning”。
- [READER_INTERPRETATION] 这构成 correctness-filtered bootstrap；若比较微调方法，需要知道各方法生成候选池大小、过滤率与轨迹质量是否匹配，原文未报告。
- [OPEN_QUESTION] Wikipedia API 的语料版本、检索时间戳、缓存与每次任务的最大总 tool calls 未完整给出；Figure 4 甚至依赖“up-to-date”页面，因此复现实验可能受外部状态影响。定位：p.4 API 描述；p.14 Figure 4。
- [OPEN_QUESTION] 论文未报告多随机种子置信区间或显著性检验；“significantly”主要基于点估计与 prompt permutations，无法从原文判断统计不确定度。定位：p.8 Results。

## 6. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] ReAct 在 HotpotQA 略低于 CoT（27.4 vs. 29.4），且 Table 2 的失败样本中 reasoning error 占 47%，search-result error 占 23%；作者还观察到重复生成旧 thought/action 的循环。定位：p.6 Table 2 与 A--C 分析。
- [AUTHOR_FACT] CoT 的主要失败为 hallucination（作者标注的失败样本中 56%），而 ReAct 的结构约束提高 groundedness 但降低推理步骤组织的灵活性。定位：p.6 Table 2 与段 B。
- [AUTHOR_FACT] 小模型少样本 prompting 时 ReAct 最差；微调 3,000 条后才成为四方法中最好。定位：p.6 末段；p.7 Figure 3。
- [AUTHOR_FACT] WebShop 各方法仍远低于 human expert；作者指出更多商品探索与 query reformulation 对 prompting 方法仍困难。定位：p.8 Table 4 及其后段。
- [AUTHOR_FACT] Conclusion 明示：大动作空间复杂任务需要更多 demonstrations，容易超过 in-context input length；更多高质量人工标注、多任务训练和 RL 组合留作未来。定位：pp.9--10 Section 6。
- [AUTHOR_FACT] 主实验模型 PaLM 当时不可公开访问；作者以完整 prompts、GPT-3 实验和代码缓解可复现性问题。定位：p.10 “Reproducibility Statement”。
- [AUTHOR_FACT] Ethics Statement 指出连接外部环境可能检索私密/不当信息或执行有害动作；本实验通过限定 Wikipedia/WebShop 且禁止真实购买/编辑降低风险。定位：p.10。
- [READER_INTERPRETATION] 未测试边界至少包括：开放网页写操作、隐私数据环境、真实购买/机器人危险动作、长于本文 horizon 的开放任务、多模型/多尺寸系统性复现、严格成本匹配以及大规模 human-in-the-loop 安全评估。定位依据：pp.9--10 Conclusion/Ethics；p.14--15 仅单例 human edit。
- [OPEN_QUESTION] “interpretability/trustworthiness/controllability”主要由轨迹检查、50+50 正误样本的人类标签和单个人工 thought-edit 例子支撑；未见盲化用户研究、校准指标或干预副作用统计。定位：p.3 贡献；p.6 Table 2；pp.14--15 Figure 5。

## 7. 可抽取的 Operator 与真实可记录的 Failure

以下仅是本读者按统一问题清单做的临时机制抽取，不是 Card 或科研裁决。

### 7.1 Operator

- [READER_INTERPRETATION] **Language-state insertion**：在环境动作空间中插入不改变环境的自由语言 thought，并写回上下文。证据：p.3 Section 2，`Â=A∪L`。
- [READER_INTERPRETATION] **Dense reason-act-observe loop**：知识任务按 Thought -> Action -> Observation 密集闭环迭代。证据：pp.3--5；pp.16--21 prompts。
- [READER_INTERPRETATION] **Sparse asynchronous deliberation**：长时程决策中仅在关键位置输出 thought，由模型自行选择干预时点。证据：pp.3--4；pp.22--25 prompts。
- [READER_INTERPRETATION] **Explicit retrieval action interface**：用 search/lookup/finish 将检索变成可观察的序列动作。证据：p.4 Section 3.1。
- [READER_INTERPRETATION] **Confidence/timeout gated fallback**：用步数超限或 CoT 多数不足阈值在 ReAct 与 CoT-SC 间切换。证据：p.5 Section 3.2。
- [READER_INTERPRETATION] **Correct-trajectory bootstrap**：筛选正确的 ReAct/Act/CoT/Standard 生成轨迹，微调较小模型。证据：pp.5--7 Figure 3；p.15 Appendix B.1。
- [READER_INTERPRETATION] **Thought editing as online policy steering**：人类直接删改中间 thought，后续动作随新上下文改变。证据：pp.14--15 Figure 5。

### 7.2 Failure

- [AUTHOR_FACT] **Repetitive loop / recovery failure**：ReAct 会重复此前 thought/action；Act 轨迹在错误清洗动作后反复执行失败序列。定位：p.6 段 B；pp.28--29 D.2.2，短定位文本 “Nothing happens”。
- [AUTHOR_FACT] **Non-informative retrieval derailment**：空结果或无用结果使 ReAct 难以恢复和改写 query；作者标注为 23% 的 ReAct 失败样本。定位：p.6 Table 2；p.33 “Failure: Search error”。
- [AUTHOR_FACT] **Reasoning-structure error**：ReAct 的结构约束可使其在复杂问题中按实体列表机械搜索，未完成真正组合推理。定位：p.6；p.32 “Failure: Reasoning error”。
- [AUTHOR_FACT] **Hallucinated thought / false belief**：CoT 可编造事实；ReAct 或 ReAct-IM 的 thought 也可错误表示状态并诱导后续动作。定位：p.6 Table 2；p.15 Figure 5；pp.29--30 D.2.3。
- [AUTHOR_FACT] **Subgoal-state loss**：Act 缺少 thought 时会忘记当前状态/子目标；ReAct-IM 会误判子目标完成或下一子目标。定位：p.8 Results 与 ReAct-IM 分析；pp.28--30。
- [AUTHOR_FACT] **Label staleness / ambiguity**：HotpotQA 可能含过期答案；EM 也把语义可接受但字符串不匹配的答案记错。定位：p.6；p.14 Figure 4；p.33 “Failure: Label ambiguity”。
- [READER_INTERPRETATION] **Prompt-format contamination risk**：Act 示例含 thought 的 p.23 内部不一致意味着“移除 thought”的消融实现需要从实际实验 prompt 重新核验。证据：p.23 Table 7。

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 已对 33 页逐页执行文本层解析，并对每页做内存栅格渲染检查；所有页均可打开，正文、表格、附录和页序连续，无缺页。
- [READER_INTERPRETATION] 普通正文页的解析文本与可视内容语义一致；主要解析问题出现在多栏表格/图形的阅读顺序，而不是原文内容缺失。
- [AUTHOR_FACT] p.2 Figure 1、p.14 Figure 4、p.15 Figure 5 的图内字体映射使解析文本呈现类似替换字母的乱码；可视渲染显示原图本身可读。因此这些图的细节以图注、周边正文与可视图为准，不把乱码当作作者文本。定位：p.2 Figure 1；p.14 Figure 4；p.15 Figure 5。
- [AUTHOR_FACT] p.5 Table 1/Figure 2 与 p.8 Tables 3--4 的解析文本会交错两栏和图例；经可视渲染复核后，本报告 §4 的数值按视觉表格重建。
- [AUTHOR_FACT] p.1 左侧 arXiv 版本戳在解析时插入摘要行中，但可视 PDF 中它只是页边竖排戳，不属于摘要正文。
- [AUTHOR_FACT] p.23 Table 7 的 “No thoughts are provided” 与表内一条 `think:` 同时存在于可视 PDF，故这不是解析器伪影，而是原文内部不一致。定位：p.23 Table 7。
- [OPEN_QUESTION] 除 p.23 的内容不一致外，未发现会改变本报告机制判断或表格数值的视觉/解析冲突；图内极小文字未逐字符转录，故不能声称完成逐字符 OCR 等价核验。

## 9. 仍需主 Codex reconciliation 时保留的问题

- [OPEN_QUESTION] 实验实际使用的 ALFWorld Act prompt 是否真的完全移除了 thoughts？需要核对公开代码/运行日志，但本次 blind scope 禁止联网及读取其他材料。
- [OPEN_QUESTION] 若按公平预算比较，ReAct、Act、CoT-SC 和混合策略各自的平均生成 token、环境步数、tool calls、失败超时和延迟是多少？论文未提供。
- [OPEN_QUESTION] best-of-6 prompt 选择是否使用独立 selection set，以及对 134 个 games 的置信区间是多少？原文未解决。
- [OPEN_QUESTION] 3,000 条正确轨迹微调的候选生成数、过滤率、任务覆盖和各方法数据难度是否匹配？原文未解决。
- [OPEN_QUESTION] Wikipedia 检索快照与 API 实现版本为何，Figure 4 的动态知识结果能否按同一输入重现？原文未解决。

## 10. 实际访问范围与工具记录

- 实际读取的任务内容文件仅为：
  1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P001_react.pdf`
  2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
  3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P001/read_3_attempts/r3-20260719-p001-a1/invocation.md`
- 实际写入仅为本 `report.md`，通过 `apply_patch` 创建。
- 完成写入后仅重读本 `report.md` 做存在性、标签覆盖与边界声明验证；它是本任务输出，不是额外研究输入。
- 未枚举工作区；未读取 read_1、任何 read_2、Cards、其他读者报告、blind query 或其他论文；未联网。
- 可观察工具轨迹：PowerShell `Get-Content` 读取两个 Markdown 输入，`Get-FileHash` 校验 PDF，`Get-Command`/Python `importlib` 只检查本地 PDF 工具可用性；尝试 `pdfinfo` 但包装器报“找不到路径”，未取得 PDF 内容；随后使用本地 Python `fitz/PyMuPDF` 直接逐页解析文本、页数、目录、版面块，并使用 `fitz + PIL` 在内存中逐页渲染 JPEG 供视觉检查；`view_image` 直接打开 PDF 的尝试无法处理，因此未依赖该结果；最终仅用 `apply_patch` 写报告，并以 PowerShell 重读输出做结构验证。
- 工具/运行时会正常加载其自身可执行文件和库；上述“仅三个输入”指研究内容文件访问范围，不把运行工具自身谎称为不存在。
- Actual model/version：接口未向本读者暴露精确模型版本，记为 `unknown`。
- Canonical subtask/thread：`/root/p001_third_read`。
