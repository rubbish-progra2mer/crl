# P001 独立第二读报告

## 0. Provenance 与读取边界

- [AUTHOR_FACT] 本报告对应 invocation snapshot：`read_2_attempts/r2-20260719-p001-a1/invocation.md`，Attempt ID 为 `r2-20260719-p001-a1`，启动时间为 `2026-07-19T15:02:25.2917326+08:00`；reader role 为 `fresh independent full-paper source checker`。
- [AUTHOR_FACT] invocation 给出的 canonical metadata 为：`arXiv:2210.03629 / ICLR 2023`，题名 *ReAct: Synergizing Reasoning and Acting in Language Models*，venue/year 为 ICLR 2023/2023。
- [AUTHOR_FACT] 本次重新计算得到 PDF SHA-256 为 `f285b0971ae4a790e402fb93966bed3adde2cf0a04977d08b2b40d6ab0cace69`，prompt SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，均与 invocation snapshot 一致。
- [AUTHOR_FACT] PDF 共 33 个物理页，页脚印刷页码也是 1–33，因此下文“第 n 页”同时指 PDF 物理页与印刷页；未发现页码错位。
- [READER_INTERPRETATION] 本次采用 procedural blinding：App 没有提供可验证的文件级技术隔离，独立性依靠严格遵守 invocation 的路径边界，不能表述为技术强制的 read-only 隔离。
- [OPEN_QUESTION] Actual model/version 在当前 agent 可见信息中没有可验证的具体版本标识，记为 `unknown`；canonical task 可见为 `/root/p001_second_read`，但底层 thread ID 不可见。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] 第 3 页，§2，定位文本“augment the agent’s action space to A-hat = A union L”：一般 agent 原本根据上下文 `c_t=(o_1,a_1,...,o_t)` 产生环境动作；ReAct 把动作空间从环境动作 `A` 扩为 `A ∪ L`，其中 `L` 是语言空间。
- [AUTHOR_FACT] 第 3 页，§2，定位文本“does not affect the external environment”与“update the context”：语言动作（thought/reasoning trace）不改变外部环境、也不产生环境 observation，而是被追加进上下文，供后续推理或行动使用。
- [READER_INTERPRETATION] 计算上的关键改变不是增加一个独立训练出的规划器，而是在同一自回归 LM 轨迹中插入可见语言状态，使下一 token/动作同时条件于历史 observation、action 与显式 thought；外部工具返回的信息再进入下一轮上下文。
- [AUTHOR_FACT] 第 3–4 页，§2，定位文本“alternate the generation of thoughts and actions”与“appear sparsely”：知识推理任务使用较密集的 Thought–Action–Observation 交替；长时程决策任务让模型自行决定 thought 的稀疏、异步出现位置。
- [AUTHOR_FACT] 第 3 页，§2，定位文本“frozen large language model, PaLM-540B”与“few-shot in-context examples”：论文主设置冻结 PaLM-540B，以人写的 action/thought/environment-observation 轨迹作为少样本上下文；这不是主结果中的参数更新。
- [AUTHOR_FACT] 第 5–7 页，§3.2–3.3 与 Figure 3，论文另做参数微调变体：用 ReAct 生成且答案正确的 3,000 条轨迹微调 PaLM-8B/62B，解码完整 trajectory。
- [READER_INTERPRETATION] 因而可把论文方法拆为两个层次：核心 ReAct operator 是“显式语言思考动作 + 环境动作的闭环交替”；3,000 条轨迹微调和 ReAct/CoT-SC fallback 是建立在核心 operator 上的独立增强，不应混成一个不可分的算法包。

## 2. 输入、输出、可用信息与干预时点

### 2.1 HotpotQA / FEVER

- [AUTHOR_FACT] 第 4 页，§3.1 “question-only setup”：输入仅为 HotpotQA 问题或 FEVER claim，不提供 supporting paragraphs；模型须依靠内部知识或主动检索。
- [AUTHOR_FACT] 第 4 页，§3.1 “Action Space”：Wikipedia API 提供 `search[entity]`（页面首五句或近似实体）、`lookup[string]`（当前页面下一个包含该字符串的句子）与 `finish[answer]`；作者明说该 API 比先进 lexical/neural retriever 弱。
- [AUTHOR_FACT] 第 4–5 页，§3.2；附录 Tables/Prompts 第 16–21 页：ReAct 输入上下文包含问题/claim、few-shot 演示及运行中累计的 thought、action、observation；输出是 HotpotQA 最终字符串答案或 FEVER 的 SUPPORTS/REFUTES/NOT ENOUGH INFO。
- [READER_INTERPRETATION] 干预发生在每个检索/推理回合：模型先生成 thought 或 action，API observation 随即追加；因此信息可用性随轨迹推进而改变，而不是一次性 retrieval-then-answer。
- [AUTHOR_FACT] 第 5 页，§3.2 “ReAct→CoT-SC / CoT-SC→ReAct”：混合方法还在 ReAct 达到步数上限（HotpotQA 7、FEVER 5）或 CoT-SC 多数票不足 `n/2` 时切换方法。

### 2.2 ALFWorld

- [AUTHOR_FACT] 第 7 页，§4 “ALFWorld”：输入是文本化房间观察与高层任务；动作是导航、拿取、清洗、放置等文本命令。一个任务可有 50 多个位置，专家可能需 50 多步。
- [AUTHOR_FACT] 第 7 页，§4：每种 task type 随机标注 3 条训练轨迹；每个实际 prompt 取其中 2 条，共构造 6 个排列；在 134 个未见 evaluation games 上按 task type 评估。
- [AUTHOR_FACT] 第 7 页，§4，定位文本“sparse thoughts”：thought 用于分解目标、跟踪完成情况、确定下一子目标，以及利用常识推测物体位置；环境 observation 在每个动作后可用。
- [AUTHOR_FACT] 第 14–15 页，Figure 5：作者展示人工可在轨迹运行中删除或添加 thought 文本以改变后续行为；作者同时明确系统性 human-in-the-loop 研究留待未来。

### 2.3 WebShop

- [AUTHOR_FACT] 第 7–8 页，§4 “WebShop”：输入为自然语言购物要求，环境含 1.18M 商品与结构化/非结构化网页文本；动作包括搜索、选择商品、选择选项及购买。评估在 500 条 test instructions 上报告 attribute coverage 平均 score 与全部满足要求的 success rate。
- [AUTHOR_FACT] 第 22 页 Table 6 与第 31 页 Table 10：ReAct 相比 Act 额外生成 `think[...]`，环境对 thought 返回 `OK`，随后模型继续点击/购买；最终环境输出任务得分或成功结果。
- [READER_INTERPRETATION] 这里的 thought 既是内部显式状态，也是一次被环境接口接受的特殊 action；它增加了 token 与 action-turn 数量，不能把 ReAct/Act 差异解释为仅改变“内容语义”而完全不改变计算预算。

## 3. 最强基线与最接近组合基线

### 3.1 知识密集任务

- [AUTHOR_FACT] 第 5 页，§3.2：Standard 删除 thought/action/observation；CoT 删除 action/observation；CoT-SC 以温度 0.7 采样 21 条 CoT 并多数投票；Act 仅删除 thought、保留检索 action 与 observation。
- [READER_INTERPRETATION] 对“显式 reasoning 是否有增益”的最近、最受控基线是 Act，因为它沿用同一批 ReAct 演示轨迹并保留同一 API；Standard/CoT 则同时改变工具可用性，不能单独归因 thought。
- [AUTHOR_FACT] 第 5 页 Table 1：PaLM-540B 上，HotpotQA EM 为 Standard 28.7、CoT 29.4、CoT-SC 33.4、Act 25.7、ReAct 27.4、CoT-SC→ReAct 34.2、ReAct→CoT-SC 35.1；FEVER accuracy 对应为 57.1、56.3、60.4、58.9、60.9、64.6、62.0。
- [AUTHOR_FACT] 第 6 页，§3.3 “perform best”：论文的最强 prompting 结果是 HotpotQA 的 ReAct→CoT-SC 和 FEVER 的 CoT-SC→ReAct；二者都不是纯 ReAct，而是内部知识投票与外部检索的组合。
- [AUTHOR_FACT] 第 5 页 Table 1：监督式 domain-specific SOTA 为 HotpotQA 67.5、FEVER 89.5，显著高于所有 prompting 结果。

### 3.2 ALFWorld

- [AUTHOR_FACT] 第 7 页，§4：Act 使用同一批轨迹但移除 thoughts，是最近受控基线；BUTLER 是每类任务用 `10^5` expert trajectories 训练的 imitation-learning agent；ReAct-IM 是以密集外部反馈式 thought 替代 ReAct 稀疏内部推理的 ablation。
- [AUTHOR_FACT] 第 8 页 Table 3：overall success rate 为 Act best-of-6 45、ReAct average 57、ReAct best-of-6 71、ReAct-IM average 48、ReAct-IM best-of-6 53、BUTLER best-of-8 37；ReAct 在 Pick-2 类别的 best-of-6 为 41，与 Act 的 41 相同，并非每一列都严格胜出。
- [READER_INTERPRETATION] 检验“稀疏、可变内部 reasoning 相对密集状态反馈”的最近组合基线是 ReAct-IM；检验“有无 thought”的最近基线是 Act。BUTLER 训练数据、模型与解码均不同，更适合做外部性能参照而非因果对照。

### 3.3 WebShop

- [AUTHOR_FACT] 第 8 页 Table 4：Act score/SR 为 62.3/30.1，ReAct 为 66.6/40.0，IL 为 59.9/29.1，IL+RL 为 62.4/28.7，human expert 为 82.1/59.6。
- [READER_INTERPRETATION] WebShop 最近受控基线是同样 one-shot 环境交互的 Act；IL/IL+RL 分别使用 1,012 条人轨迹与额外 10,587 条训练指令，训练范式不同。

## 4. 模型、token、tool-call、prompt 与 oracle 差异能否解释结果？

- [AUTHOR_FACT] 第 3 页脚注 1、第 14 页 Table 5：相同 ReAct prompting 下，GPT-3 `text-davinci-002` 在 500 个 HotpotQA 子集上为 30.8（PaLM-540B 29.4），在 134 个 ALFWorld 任务上为 78.4（PaLM-540B 70.9）。
- [READER_INTERPRETATION] 模型本身明显影响绝对性能；主表中 ReAct/Act 使用同一 PaLM-540B 可部分控制这一点，但跨工作比较（BUTLER、IL/RL、监督 SOTA）不能排除 model/training-data 差异。
- [AUTHOR_FACT] 第 5 页，CoT-SC 使用 21 个温度采样并多数投票；ReAct/Act 主轨迹采用 greedy decoding。第 8 页 Table 3 注明 BUTLER 使用 beam search，而其他方法 greedy。
- [READER_INTERPRETATION] CoT-SC 与单轨迹 ReAct 的采样/token 预算不等；Figure 2 虽展示随 CoT-SC sample 数变化的曲线，并声称混合方法用 3–5 samples 达到 21-sample CoT-SC，但未给出总生成 token、延迟或 API-call 等成本匹配实验。
- [AUTHOR_FACT] 第 4–5 页：Standard/CoT 没有 Wikipedia API，Act/ReAct 有；混合方法还根据失败步数或投票置信度调用另一方法。
- [READER_INTERPRETATION] Standard/CoT 与 ReAct 的差异包含 oracle/tool access；只有 Act 与 ReAct 更接近控制 tool access。即便 ReAct 对 Act，thought 也增加输入/输出 token、上下文长度和在 WebShop/ALFWorld 中的 `think` 回合，论文没有等 token 或等 turn 对照。
- [AUTHOR_FACT] 第 7 页：ALFWorld 六个 prompt 来自同三条标注轨迹的两两排列；Table 3 报告 best-of-6，同时也仅为 ReAct/ReAct-IM 给出 average。第 8 页正文称优势在六个 controlled trials 上均存在。
- [OPEN_QUESTION] 论文未清楚说明“best prompt”是否借助 evaluation-game 表现选择；若在同一 134 个 evaluation games 上择优，则 best-of-6 含测试集选择效应。Act 未在 Table 3 报告 average，也使平均性能的完全对称比较不可恢复。
- [AUTHOR_FACT] 第 23 页 Table 7 的 caption 明写“An Act prompt ... No thoughts are provided”，但表内实际包含一行 `> think: Now I clean a lettuce (1)...`；该行在可视 PDF 中确实存在，并非文本解析伪影。
- [OPEN_QUESTION] Table 7 的 thought 是实际 Act prompt 泄漏还是附录排版/转录错误，原文无法判定；在澄清前，“ALFWorld Act 完全移除 thought”的实现一致性存在疑问。
- [AUTHOR_FACT] 第 5 页，微调只保留 ReAct（以及各 baseline）生成且最终答案正确的 3,000 条轨迹。
- [READER_INTERPRETATION] 这一步使用答案正确性筛选，属于训练数据构造中的 outcome oracle；可证明所选 bootstrap 管线有效，但不能与未经正确性筛选、同 token 数的数据直接等价比较。
- [AUTHOR_FACT] 第 14 页 Figure 4：作者展示 HotpotQA label 过时而 ReAct 从当前 Wikipedia 得到更新答案的案例。
- [READER_INTERPRETATION] 数据标签时间与 Wikipedia snapshot/API 内容也是 measurement 差异来源；exact match 会把某些事实更新算作“错误”，同时 API 实时性可能让工具方法拥有与静态标签不一致的信息。
- [OPEN_QUESTION] 原文未报告严格等 prompt 长度、等生成 token、等 wall-clock、等 API-call、等检索结果 oracle、等演示标注成本的消融，因此不能排除一部分增益来自额外计算/信息预算。

## 5. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 第 6 页，§3.3：ReAct 在 HotpotQA 上低于 CoT（27.4 vs 29.4），其交替结构约束被作者认为会降低推理步骤的灵活性；ReAct 的 reasoning error 在抽样失败案例中占 47%，并出现重复生成先前 thought/action 的循环。
- [AUTHOR_FACT] 第 6 页 Table 2 与正文：无信息 search result 占 ReAct 抽样 error cases 的 23%，会使后续推理偏离且难以恢复；作者把改善 decoding（如 beam search）留作未来。
- [AUTHOR_FACT] 第 6 页 Table 2：在人工抽查的 HotpotQA 轨迹中，成功案例 false positive 为 ReAct 6%、CoT 14%；失败案例类别中 CoT hallucination 为 56%，ReAct hallucination 记为 0%，但 ReAct 有 reasoning/search errors。
- [READER_INTERPRETATION] Table 2 的百分比来自分别随机抽取 50 个 correct 与 50 个 incorrect trajectory/方法的分层样本，不是总体端到端发生率；不能把“0% hallucination”推广为 ReAct 永不幻觉。
- [AUTHOR_FACT] 第 4 页脚注 2：作者称增加 HotpotQA/FEVER few-shot examples 不提高性能；第 5 页脚注 3：增加超过 7/5 的步骤也不提高 ReAct 表现。
- [AUTHOR_FACT] 第 6–7 页 Figure 3：PaLM-8B/62B 仅 prompting 时，ReAct 在四方法中最差；需 3,000 条筛选轨迹微调后才成为最好。第 15 页 §B.1 还称 Standard/CoT 微调不久即退化。
- [AUTHOR_FACT] 第 8 页：ALFWorld Act 会丢失子目标/当前环境状态；ReAct-IM 会误判子目标是否完成、缺少高层分解和常识位置推理。第 28–30 页给出 Act 与 ReAct-IM 陷入重复动作的具体失败轨迹。
- [AUTHOR_FACT] 第 8 页：WebShop 所有方法显著低于 human expert；作者指出人类会进行更多商品探索和 query reformulation，而 prompting 方法仍难做到。
- [AUTHOR_FACT] 第 9–10 页 Conclusion：复杂、大动作空间任务需要更多 demonstrations，容易超过 in-context input-length limit；学习更多高质量人工 annotation、multi-task training 与 RL 组合均是未来工作。
- [AUTHOR_FACT] 第 10 页 Reproducibility：主实验使用当时未公开的 PaLM；作者用附录 prompts、GPT-3 实验与代码缓解，但主模型本身不可访问。
- [AUTHOR_FACT] 第 10 页 Ethics：连接外部环境可能查询不当/隐私信息或执行有害动作；论文实验只允许 Wikipedia/WebShop 等受限网站与无真实危险的动作（不能真购买、不能编辑 Wikipedia）。
- [OPEN_QUESTION] 未测试边界包括真实开放网页、可写/可购买/物理执行的高风险 action space、隐私攻击、恶意 observation/prompt injection，以及长于本文 horizon 或超出上下文窗口的任务。
- [AUTHOR_FACT] 第 14–15 页 Figure 5：人工 thought editing 只有个案演示，作者明说更系统的研究留待未来。
- [OPEN_QUESTION] 论文没有报告 thought 的事实忠实性校准、人工编辑失败率、编辑者盲法/成本、跨 annotator 稳定性，也没有验证可读 reasoning 是否忠实反映模型内部因果过程。

## 6. 可抽取的 Operator 与真实可记录的 Failure

以下仅是源文中可定位的抽取项，不生成 Card，也不作 Candidate 评价。

### 6.1 Operator 抽取项

- [AUTHOR_FACT] **语言动作扩空间 operator**：把 `A` 扩为 `A ∪ L`，thought 不触发外部状态变化而更新上下文。定位：第 3 页 §2，“augment the agent’s action space”“does not affect the external environment”。
- [AUTHOR_FACT] **密集 Thought–Action–Observation operator**：知识推理任务按多轮 thought/action/observation 交替。定位：第 3–5 页 §2、§3.2；第 17–21 页完整 prompts。
- [AUTHOR_FACT] **稀疏异步 reasoning operator**：长时程决策中由模型决定何时 `think`，用于目标分解、进度跟踪、常识位置推断与异常恢复。定位：第 3–4、7 页 §2/§4；第 24 页 Table 8。
- [AUTHOR_FACT] **工具定向检索 operator**：用 thought 选择/改写 `search`、`lookup`，把 observation 回填下一轮。定位：第 4 页 §3.1；第 18、21 页 prompt 示例。
- [AUTHOR_FACT] **双路径 fallback operator**：超过 ReAct 步数上限则转 CoT-SC，或 CoT-SC 多数不足半数则转 ReAct。定位：第 5 页 §3.2。
- [AUTHOR_FACT] **人工 thought-edit operator**：运行中删除错误 thought、插入提示以改写后续 policy。定位：第 14–15 页 Figure 5。
- [AUTHOR_FACT] **正确轨迹 bootstrap operator**：筛选答案正确的生成轨迹，再微调小模型输出完整轨迹。定位：第 5–7 页 §3.2、Figure 3；训练步数见第 15 页 §B.1。

### 6.2 真实 Failure 抽取项

- [AUTHOR_FACT] **ReAct 重复循环/next-action reasoning error**：无法跳出重复 thought/action。定位：第 6 页 §3.3B；第 32 页 “Failure: Reasoning error”。
- [AUTHOR_FACT] **检索无信息后难恢复**：空或无用 search result 使 reasoning 偏离。定位：第 6 页 §3.3C（23% of sampled error cases）；第 33 页 “Failure: Search error”。
- [AUTHOR_FACT] **CoT 幻觉事实/错误传播**：人工样本中 CoT 失败的 hallucination 类为 56%。定位：第 6 页 Table 2；第 33 页 hallucination 示例。
- [AUTHOR_FACT] **Act 缺少状态跟踪导致动作循环**：拿到 knife 后未先移动到 sink 就清洗，之后重复失败序列。定位：第 28–29 页 §D.2.2。
- [AUTHOR_FACT] **ReAct-IM 错误子目标信念**：thought 将未清洗 knife 当作 clean，随后反复放置。定位：第 29–30 页 §D.2.3。
- [AUTHOR_FACT] **False positive / label ambiguity**：ReAct 可基于错误实体/事实得到形式上匹配答案，或输出语义正确但与标签字符串不匹配。定位：第 6 页 Table 2；第 32–33 页 §E.1。
- [AUTHOR_FACT] **小模型纯 prompting 学不会联合行为**：PaLM-8B/62B prompting 的 ReAct 最差。定位：第 6–7 页 Figure 3 及正文。
- [AUTHOR_FACT] **工具 grounding 仍可能与 benchmark label 冲突**：更新后的网页事实与过时 label 不一致。定位：第 14 页 Figure 4。
- [READER_INTERPRETATION] 可记录 Failure 应保留具体条件（模型、task、prompting/finetuning、抽样分母、是否工具可用）；否则会把“ReAct 在某抽样下的 failure mode”错误泛化成所有 ReAct 实现的固有定律。

## 7. 逐页覆盖与定位索引

- [AUTHOR_FACT] 第 1 页：题名、摘要、§1 开头；定位“generate both reasoning traces and task-specific actions in an interleaved manner”。
- [AUTHOR_FACT] 第 2 页：Figure 1 与 §1；四种 prompting 及 QA/ALFWorld 轨迹对比。
- [AUTHOR_FACT] 第 3 页：§1 贡献、§2 形式化；`A ∪ L`、frozen PaLM-540B、dense/sparse thought 区分。
- [AUTHOR_FACT] 第 4 页：§2 特性、§3.1、§3.2 开头；question-only、Wikipedia API、演示数。
- [AUTHOR_FACT] 第 5 页：Table 1、Figure 2、baseline、fallback、finetuning 设置。
- [AUTHOR_FACT] 第 6 页：Table 2、§3.3；ReAct/CoT 对比、失败模式、Figure 3 讨论。
- [AUTHOR_FACT] 第 7 页：Figure 3、§4；ALFWorld/WebShop 设置与训练/评估规模。
- [AUTHOR_FACT] 第 8 页：Tables 3–4；ALFWorld/WebShop 结果与 ReAct-IM ablation。
- [AUTHOR_FACT] 第 9 页：§5、§6 开头；相关工作与方法边界。
- [AUTHOR_FACT] 第 10 页：Conclusion、Reproducibility、Ethics、References 开头。
- [AUTHOR_FACT] 第 11–13 页：References；未发现新增实验结论。
- [AUTHOR_FACT] 第 14 页：Appendix A.1–A.3，Table 5、Figure 4、human edit 引入。
- [AUTHOR_FACT] 第 15 页：Figure 5、§B.1–B.2；人工编辑个案、微调步数、ReAct-IM 定义。
- [AUTHOR_FACT] 第 16–19 页：§C.1 HotpotQA 的 Original/Act/CoT/ReAct 完整 prompts。
- [AUTHOR_FACT] 第 20–21 页：§C.2 FEVER 的 Act/CoT/ReAct prompts。
- [AUTHOR_FACT] 第 22 页：§C.3 Table 6，WebShop Act/ReAct prompt 对照。
- [AUTHOR_FACT] 第 23–25 页：§C.4 Tables 7–9，ALFWorld Act/ReAct/ReAct-IM prompts；第 23 页存在 caption 与 `think` 行不一致。
- [AUTHOR_FACT] 第 26–27 页：§D.1 FEVER trajectories；含 ReAct/Act/CoT 正负例。
- [AUTHOR_FACT] 第 27–30 页：§D.2 ALFWorld trajectories；ReAct 成功、Act 与 ReAct-IM 循环失败。
- [AUTHOR_FACT] 第 31 页：§D.3 Table 10，WebShop Act/ReAct 输出对照。
- [AUTHOR_FACT] 第 32–33 页：§E.1 success/failure-mode examples；true/false positive、reasoning/search/hallucination/label ambiguity。

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 逐页检查了全部 33 页的解析文本，并以页面渲染检查每页布局；正文段落、章节号、页码与主要表格数值未发现实质性内容冲突。
- [AUTHOR_FACT] 第 2 页 Figure 1、第 14 页 Figure 4、第 15 页 Figure 5 的图内文本使用特殊字体/嵌入编码：文本抽取会产生大量字符替换与错序，但可视 PDF 图像正常；涉及这些图的判断以可视页面、figure caption 及相邻正文交叉核对。
- [AUTHOR_FACT] 第 5 页 Table 1/Figure 2、第 8 页 Tables 3–4、第 22 页 Table 6、第 31 页 Table 10 为多栏布局，线性文本抽取会交错列顺序；数值与轨迹配对以可视表格版面核对。
- [AUTHOR_FACT] 第 23 页 Table 7 caption/内容矛盾同时存在于可视 PDF 与解析文本，故是源文内部不一致，不是解析错误。
- [OPEN_QUESTION] 未进行像素级 PDF 与出版源/作者代码的版本比对，也未联网核验网页或代码；因此只能确认本地给定 PDF 内部的解析—可视一致性，不能确认其与外部版本完全相同。

## 9. 实际读取文件与工具记录

### 实际读取的文件

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P001_react.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P001/read_2_attempts/r2-20260719-p001-a1/invocation.md`

未枚举工作区；未读取 read_1、Cards、其他读者报告、blind query 或其他文件；未联网。

### 实际使用的工具

- `functions.exec`：编排已明确路径的本地只读调用。
- `shell_command` / PowerShell `Get-Content -Encoding UTF8`：读取两个指定 Markdown 文件。
- `shell_command` / `Get-FileHash`：计算指定 PDF 与 prompt 的 SHA-256。
- `shell_command` / Python + PyMuPDF (`fitz`)：读取 PDF 页数、逐页抽取 1–33 页文本、在内存中渲染页面/联系表；Pillow 仅在内存中拼接渲染图，没有写临时文件。
- `shell_command` / Python + `pypdf`：独立确认 PDF 页数为 33。
- `view_image`：曾直接尝试查看指定 PDF，工具无法处理 PDF；随后使用上述内存渲染进行可视核查。
- `apply_patch`：唯一写入动作，仅创建本 `report.md`。

完整的底层 file-access/tool trace：`unavailable`。以上是本 agent 在当前任务中可观察并如实记录的调用；App 未提供可验证的系统级完整访问审计。
