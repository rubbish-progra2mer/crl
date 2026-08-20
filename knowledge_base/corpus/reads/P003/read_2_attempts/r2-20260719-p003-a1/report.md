# P003 独立二读报告

## 0. 身份、范围与来源

- 本报告对应 invocation snapshot：`r2-20260719-p003-a1`，即 `knowledge_base/pilot/reads/P003/read_2_attempts/r2-20260719-p003-a1/invocation.md`。
- [AUTHOR_FACT] 论文为 Zhou et al., *Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models*，PMLR 235 / ICML 2024。PDF 共 23 页；实测 SHA-256 为 `a6b84613eeeaa3beb979ac3e34cbb3575bceb7ccf6050a2c2fc677d5e3a3ab19`，与 invocation 一致。（PDF p.1，标题页；invocation input manifest）
- [READER_INTERPRETATION] 本报告是 fresh 独立核源，只回答统一问题，不生成 Card，不对 Candidate 作评价，也不与任何其他读者结论合并。

## 1. 方法究竟改变哪一步计算？

### 1.1 核心计算改动

- [AUTHOR_FACT] LATS 不再让 LM 以 CoT 或 ReAct 单轨自回归地产生一条轨迹，而是把 LM 包在一个 MCTS 变体中；每个节点存放原始输入、截至当前的动作序列和环境观察序列，形式写为 `s=[x,a_{1:i},o_{1:i}]`。（PDF p.4，Sec. 4.2，定位：“frames decision-making as a tree search”）
- [AUTHOR_FACT] 每轮依次执行 selection、expansion、evaluation、simulation、backpropagation、reflection，直到成功或达到轨迹/计算预算。（PDF p.5，Fig. 2 及 Sec. 4.2，定位：“six operations in LATS”）
- [AUTHOR_FACT] Expansion 从当前状态用基础 LM `pθ` 采样 `n` 个候选动作；环境实际执行每个动作并返回观察，形成子节点，而不是仅由 LM 预测下一状态。（PDF pp.4–5，Sec. 4.1–4.2，定位：“environment receives each action”）
- [AUTHOR_FACT] Evaluation 在环境反馈之后给子节点赋值。值函数混合两项：LM 对状态的 1–10 评分与同一状态动作的自一致性分数，`V(s)=λ·LM(s)+(1−λ)·SC(s)`。（PDF p.5，Eq. 2，定位：“after obtaining the environmental feedback”）
- [AUTHOR_FACT] Selection 使用含访问计数和探索权重的 UCT；terminal reward 沿轨迹回传以更新节点值与访问次数。（PDF pp.4–5，Eq. 1、Backpropagation；PDF p.15，Algorithm 1）
- [AUTHOR_FACT] 失败终止时，LM 根据失败轨迹与最终 reward 生成文字反思；失败轨迹和反思进入外部记忆，在后续 action generator 与 value function 的上下文中复用。（PDF pp.5–6，Reflection，定位：“stored in the memory”）
- [READER_INTERPRETATION] 因而最小机制差异不是“多采样”本身，而是：**在真实环境反馈之后评估分支，并用 UCT、终局回传和失败反思决定后续从哪个历史状态继续搜索**。

### 1.2 任务特化

- [AUTHOR_FACT] 无外部反馈的纯推理任务用 CoT 作为基础 prompt；交互任务用 ReAct 式 thoughts+actions 空间。（PDF p.4，Sec. 4.1，定位：“In environments without feedback”）
- [AUTHOR_FACT] Programming 中一个 action 就是一份完整程序；作者跳过 simulation，用合成测试通过率直接作为回传 reward，搜索结束后选 value 最高的程序，再在真实测试套件上计算 pass@1。（PDF p.7，Sec. 5.2，定位：“skip the simulation step”）
- [AUTHOR_FACT] HotPotQA 另有 CoT→ReAct 的混合版本：先内部推理，失败后切换到带检索工具的 ReAct。（PDF p.7，Sec. 5.1，定位：“first prompting with a CoT-based prompt”）

## 2. 输入、输出、可用信息与干预时点

### 2.1 通用接口

- [AUTHOR_FACT] 输入是自然语言序列 `x` 和预训练 LM `pθ`；输出 `y` 可以是推理答案或完成交互任务的最终动作/轨迹。（PDF p.3，Sec. 3.1，定位：“our goal is to generate a final output y”）
- [AUTHOR_FACT] 交互状态可用信息包括原始输入、历史 thoughts/actions、环境 observations、访问计数、节点值、失败轨迹与反思；这些以文本作为模块间接口，不需要参数训练。（PDF pp.2, 4–6，Sec. 1、4.1–4.2）
- [AUTHOR_FACT] 干预发生在：(a) 每个状态扩展时采样多个 action；(b) action 后收到 observation 再评分；(c) simulation 到 terminal 后取得客观 reward；(d) 失败后产生 reflection；(e) reward 回传后改变后续 UCT selection。（PDF p.5，Fig. 2 与六个操作）
- [AUTHOR_FACT] 搜索可在成功时提前终止，否则在 `K/k` 轨迹或深度限制耗尽后停止。（PDF p.5，Sec. 4.2；PDF p.15，Algorithm 1）
- [OPEN_QUESTION] 对非 Programming 任务，预算耗尽但无成功时最终输出节点/轨迹的精确选择规则未在 Algorithm 1 中清晰写出；正文主要描述成功即停止和失败继续搜索。（PDF pp.5, 15，Simulation / Algorithm 1）

### 2.2 各环境可用信息

- [AUTHOR_FACT] HotPotQA action space 为 free-form thoughts 加 `search[entity]`、`lookup[string]`、`finish[answer]`；Wikipedia API 返回检索观察。作者采用 oracle setup，在提交答案后由环境给出 correctness feedback。（PDF p.6，Sec. 5.1；PDF pp.15–16，Sec. D.1）
- [AUTHOR_FACT] Programming observation 是 LM 合成的内部测试套件执行结果与编译器输出；最终评价才使用真实测试套件。（PDF p.7，Sec. 5.2；PDF p.16，Sec. D.2）
- [AUTHOR_FACT] WebShop action 是 search/click/think，observation 是结构化网页反馈与反思；reward 由购买商品与指令属性/选项的词汇及语义匹配自动计算。（PDF pp.8, 16–17，Sec. 5.3、D.3、Table 12）
- [AUTHOR_FACT] Game of 24 没有外部工具反馈，用 CoT、LM value 与 self-consistency 进行内部搜索。（PDF pp.8, 17，Sec. 5.4、D.4）

## 3. 最强基线与最接近组合基线

### 3.1 HotPotQA

- [AUTHOR_FACT] 内部推理表中，最强非 LATS 基线为 RAP 0.60 EM；LATS(CoT) 为 0.62。CoT、CoT-SC、ToT 分别为 0.34、0.38、0.55。（PDF p.6，Table 2）
- [AUTHOR_FACT] 交互检索表中，最强非 LATS 基线为 RAP(ReAct) 0.54，其次 Reflexion 0.51；LATS(ReAct) 0.63，`n=10` 为 0.65，CoT+ReAct 混合版本为 0.71。（PDF p.6，Table 3）
- [READER_INTERPRETATION] 最接近“组合基线”是 ToT(ReAct) 和 RAP(ReAct)，因为它们同样把搜索算法与 ReAct 环境交互结合；但它们不是 LATS 六操作的完整复现。
- [AUTHOR_FACT] ToT(ReAct)=0.39、RAP(ReAct)=0.54，均低于各自在 reasoning-only 表中的 ToT=0.55、RAP=0.60；作者据此认为直接拼接搜索与 ReAct 不充分。（PDF pp.6–7，Tables 2–3 与 Results）

### 3.2 Programming

- [AUTHOR_FACT] HumanEval / GPT-3.5 中最强非 LATS 基线是 Reflexion 68.1 pass@1，LATS(ReAct) 83.8；GPT-4 中 Reflexion 91.0、LATS 92.7、Base LM 80.1。（PDF p.7，Table 4）
- [AUTHOR_FACT] MBPP / GPT-3.5 中最强非 LATS 基线是 RAP 71.4，Reflexion 70.0，LATS 81.1。（PDF p.7，Table 5）
- [READER_INTERPRETATION] Programming 的最接近组合基线是 RAP（树搜索）与 Reflexion（测试反馈+反思）两条线，但论文没有展示“RAP + 同等测试反馈 + 同等反思记忆”的完全资源匹配组合。

### 3.3 WebShop 与 Game of 24

- [AUTHOR_FACT] WebShop 的 prompting 基线中 Reflexion 最强：score 64.2、SR 35.0；LATS 为 75.9、38.0。训练方法中 Fine-tuning 为 67.5、45.0，Expert 为 82.1、59.6。（PDF p.8，Table 6）
- [READER_INTERPRETATION] 若以 average score 为主，LATS 强于论文列出的训练基线；若以 success rate 为主，Fine-tuning 45.0 高于 LATS 38.0，Expert 也明显更高。因此“最强基线”依赖指标，不能只复述 score。
- [AUTHOR_FACT] Game of 24 中最强非 LATS 基线为 RAP 0.40 success rate，LATS(CoT) 为 0.44。（PDF p.8，Table 7）

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

### 4.1 已控制或部分控制的因素

- [AUTHOR_FACT] 主要 GPT-3.5 表在同一模型名下比较；HumanEval 另报告 GPT-4。HotPotQA 每个方法用三个 few-shot examples，涉及 sampling 的方法使用 `k=50`；WebShop 的 LATS、ReAct(best of k)、Reflexion 均设 `k=30`。（PDF pp.6–8，Secs. 5.1–5.3）
- [AUTHOR_FACT] HotPotQA 的 Table 9 报告树搜索方法同为 `O(kn)` sample complexity；成功样本上的 token consumption 为 ToT(ReAct) 210,215、RAP(ReAct) 176,500、LATS 173,290。（PDF p.9，Table 9）
- [AUTHOR_FACT] 同表把 ReAct(best `k=250`) 0.42 与 LATS(`n=5,k=50`) 0.63 并列，以相同最大候选数量级作一项对照，但 ReAct/CoT-SC 的 token consumption 栏为 “-”。（PDF p.9，Table 9）
- [AUTHOR_FACT] WebShop 作者称在相同 iteration 数下比较并得到 LATS 改善；环境和 action space 共享预构造接口。（PDF p.8，Sec. 5.3 / Table 6 caption）

### 4.2 尚未排除的混杂

- [READER_INTERPRETATION] LATS 每个 expansion 采 `n` 个 action，还额外调用 LM 做 value 和 reflection；单轨 ReAct/Reflexion 的 LM call 结构不同。即使 `k` 相同，也不等价于 token、tool-call、wall-clock 或总 LM inference 次数相同。
- [OPEN_QUESTION] 论文未给出所有基线的完整 token/tool-call 分解；Table 9 只统计树搜索方法成功时的平均 token，并明确对 ReAct/CoT-SC 留空，也没有将失败轨迹的实际 token 纳入表中。（PDF p.9，Table 9 与 “upon success”）
- [OPEN_QUESTION] “GPT-3.5”“GPT-4”的具体模型快照、温度、top-p、停止条件和随机种子在全文/附录可见内容中没有统一完整披露，因而模型版本与 decoding 差异无法完全复核。（PDF pp.6–9 Tables 2–10；pp.17–23 prompts）
- [AUTHOR_FACT] 各方法使用不同 prompt 设计；附录分别给出 LATS acting/reasoning、value、reflection prompts。Value prompt要求输出 1–10 correctness score，反思 prompt包含失败轨迹。（PDF pp.17–23，Secs. E–G）
- [READER_INTERPRETATION] Prompt 差异是方法组成的一部分，但实验没有把“相同搜索、仅换 prompt”与“相同 prompt、仅换搜索”完全析因；因此不能把所有增益唯一归因于 MCTS。
- [AUTHOR_FACT] HotPotQA 使用答案 correctness oracle，作者明确称其用于聚焦“如何利用高质量反馈”，且认为基线也处于该设置。（PDF p.6，Sec. 5.1，定位：“oracle setup”）
- [READER_INTERPRETATION] 该 oracle 对受控比较有价值，但限制了对无 correctness oracle 场景的外推；LATS 在 Table 8 中对 LM heuristic、DFS、reflection 的消融并不能消除 oracle 本身带来的任务简化。
- [AUTHOR_FACT] Programming 的内部测试由 LM 合成，最终才用真实测试评估；测试反馈质量可能直接影响搜索价值。（PDF p.7，Sec. 5.2）
- [OPEN_QUESTION] 是否对所有 Programming acting/search 基线使用完全相同的合成测试、测试生成模型与失败输出格式，正文没有逐基线给出足够细的资源审计信息。
- [READER_INTERPRETATION] WebShop 与 Fine-tuning/IL+RL 的训练成本和推理成本并不等价；Table 6 是性能参照，不是 compute-matched 对照。

## 5. 作者明示限制、负向结果和未测试边界

### 5.1 明示限制

- [AUTHOR_FACT] 第一项主限制是相对 ReAct/Reflexion 更高的计算成本；作者建议在困难任务或性能优先时使用 LATS。（PDF pp.9, 14，Sec. 6 与 Appendix B，定位：“higher computational cost”）
- [AUTHOR_FACT] 第二项主限制是决策环境必须能回退到早先状态；该假设并非所有真实环境都满足。（PDF pp.9, 14，Sec. 6 与 Appendix B，定位：“requires the agent to be able to revert”）
- [AUTHOR_FACT] 作者承认所用 benchmarks 相比真实复杂交互环境“relatively simple”，并把 Minecraft、更复杂环境、更多 reasoning benchmarks 和 multi-agent 扩展列为未来工作。（PDF pp.9, 14，Sec. 6 / Appendix B）
- [AUTHOR_FACT] Impact Statement 提到更强自主决策可能助长有害用途、执行恶意软件及安全风险。（PDF p.10，Impact Statement）

### 5.2 明示负向或削弱结果

- [AUTHOR_FACT] WebShop 中作者发现 reflection 往往泛化、不能给出有效反馈，并会使 agent 陷入 local minima；ReAct(best of k) 59.1 与 Reflexion 64.2 的差距相对有限。（PDF p.8，Sec. 5.3，定位：“often generic”）
- [AUTHOR_FACT] HotPotQA 中去掉 reflection 后从 0.63 降至 0.58；作者指出该 0.05 增益小于 Reflexion 相对 ReAct 的 0.19，可能因为 search 与 reflection 改善的是重叠问题。（PDF p.8，Sec. 5.4 / Table 8）
- [AUTHOR_FACT] HotPotQA 去掉 LM heuristic 后为 0.37，换 DFS 为 0.42；完整 LATS 为 0.63。Appendix 另报 `w=0.5` 为 0.55、`d=4` 为 0.58、`w=2.0` 为 0.63。（PDF pp.8, 14, 16，Tables 8、11）
- [AUTHOR_FACT] Game of 24 去掉 self-consistency（`λ=1`）从 0.44 降至 0.40。（PDF p.17，Table 13）
- [AUTHOR_FACT] WebShop 上 LATS 的 success rate 38.0 低于 Fine-tuning 45.0，也远低于 Expert 59.6。（PDF p.8，Table 6）
- [AUTHOR_FACT] Appendix 的 WebShop 失败示例包含买入超预算商品、错误判断产品属性、invalid action 与未能返回搜索页；这些是 prompt 中展示的具体失败轨迹，不是总体失败率分解。（PDF pp.21–23，Secs. G.2–G.3）

### 5.3 未测试或报告不足的边界

- [AUTHOR_FACT] 实际评测子集为 HotPotQA 100 题、WebShop 50 instructions、Game of 24 50 games、MBPP 随机 397 题；HumanEval 用全部 164 题。（PDF pp.6–8, 15–17，Secs. 5、D）
- [OPEN_QUESTION] 文中没有为主要结果给出置信区间、显著性检验或多随机种子方差；小子集结果的稳定性无法由本 PDF 判断。
- [OPEN_QUESTION] 对不可回退、部分可回退、状态具有不可逆副作用、环境反馈噪声大或延迟的系统，LATS 的表现未做实验验证；作者只把它们作为限制/未来方向讨论。（PDF pp.9, 14）
- [OPEN_QUESTION] 多 agent、真实开放互联网、长时程 embodied 环境和训练外新工具接口未在本论文中验证。（PDF pp.9, 14）
- [OPEN_QUESTION] HotPotQA 深度设置存在内部口径差异：Appendix B 称主实验 `d=7`，Table 11 也列完整设置 `d=7`；Appendix D.1 又称对所选 100 题使用 maximum depth 6。原文未解释两者是否对应不同 run。（PDF pp.14–16，Appendix B/C/D.1，定位：“maximum depth of d=7” / “maximum depth limit of 6”）
- [OPEN_QUESTION] Programming 内部测试数量也有口径差异：正文 Sec. 5.2 称 generated tests 设为 4；Appendix D.2 称 GPT-3.5 用 6 个内部测试、GPT-4 用 4 个。若正文包括 GPT-3.5 主表，则需作者澄清。（PDF pp.7, 16，Sec. 5.2 / D.2）

## 6. 可抽取机制单元（Operator）与真实可记录 Failure

以下只做来源抽取，不作 Candidate 价值判断。

### 6.1 可抽取机制单元

- [READER_INTERPRETATION] **环境反馈后的分支价值评估**：先执行 action 得 observation，再让 LM 评分，而不是仅凭内部 world model 预测。（依据：PDF pp.4–5，Sec. 4.2）
- [READER_INTERPRETATION] **LM score 与同状态自一致性融合**：用可调 `λ` 混合语义价值和重复采样频率信号。（依据：PDF p.5 Eq. 2；p.17 Table 13）
- [READER_INTERPRETATION] **UCT 驱动的语言 agent 分支选择与终局 reward 回传**：访问计数、探索项、节点价值共同决定重访/扩展历史状态。（依据：PDF pp.4–5 Eq. 1；p.15 Algorithm 1）
- [READER_INTERPRETATION] **失败轨迹+文字反思的跨 trial 外部记忆**：terminal failure 后生成语义诊断并注入后续 agent/value context。（依据：PDF pp.5–6 Reflection）
- [READER_INTERPRETATION] **可回退环境的文本状态重放**：复制历史 context/observation/action 以恢复任意节点，避免学习 world model。（依据：PDF pp.3–4，Sec. 3.2 / 4.2）
- [READER_INTERPRETATION] **先内部推理、失败后启用工具**：HotPotQA 的 CoT→ReAct 分阶段策略。（依据：PDF p.7，Sec. 5.1）
- [READER_INTERPRETATION] **完整解作为 action 的任务适配**：Programming 跳过 simulation，以合成测试通过率直接回传。（依据：PDF p.7，Sec. 5.2）

### 6.2 有直接论文证据的 Failure

- [AUTHOR_FACT] **泛化反思导致局部最优**：WebShop 反思经常不提供有用反馈，agent 容易卡住。（PDF p.8，Sec. 5.3）
- [AUTHOR_FACT] **简单搜索×ReAct 拼接失效**：ToT(ReAct) 与 RAP(ReAct) 在 HotPotQA 分别 0.39、0.54，低于其 reasoning-only 的 0.55、0.60。（PDF pp.6–7，Tables 2–3）
- [AUTHOR_FACT] **稀疏终局 reward 下无 LM heuristic 的搜索显著退化**：去掉 evaluation 后 0.37，完整 LATS 0.63；作者解释仅靠完成轨迹 reward 信号稀疏且常为 binary。（PDF pp.8, 15–16，Tables 8、11 与 Appendix C）
- [AUTHOR_FACT] **弱探索或浅深度退化**：`w=0.5` 为 0.55、`d=4` 为 0.58，相对完整 0.63 下降。（PDF pp.14, 16，Appendix C / Table 11）
- [AUTHOR_FACT] **无 self-consistency 的纯推理搜索下降**：Game of 24 的 `λ=1` 为 0.40，混合值为 0.44。（PDF p.17，Table 13）
- [AUTHOR_FACT] **具体 WebShop 执行错误**：附录失败轨迹展示超预算购买、属性误判和 invalid action。（PDF pp.21–23，Secs. G.2–G.3）
- [READER_INTERPRETATION] “不可回退环境”与“更高计算成本”应记录为适用前提/限制，不应伪装成论文已实测的 failure；论文未给出这两类场景的失败实验。

## 7. 关键判断定位索引

| 判断 | 页码 / 章节 / 图表 | 短定位文本 |
|---|---|---|
| MCTS 包装 LM agent | p.4, Sec. 4.2 | “adapting MCTS to language agents” |
| 六操作 | p.5, Fig. 2 | “selection, expansion, evaluation, simulation, backpropagation, and reflection” |
| post-observation value | p.5, Evaluation | “after obtaining the environmental feedback” |
| 混合值函数 | p.5, Eq. 2 | `λ * LM(s) + (1-λ) * SC(s)` |
| 反思记忆 | pp.5–6, Reflection | “failed trajectories and corresponding reflections” |
| HotPotQA oracle | p.6, Sec. 5.1 | “oracle setup” |
| Programming 跳过 simulation | p.7, Sec. 5.2 | “skip the simulation step” |
| WebShop generic reflection | p.8, Sec. 5.3 | “often generic” / “local minima” |
| 成本与回退限制 | p.9, Sec. 6；p.14, App. B | “higher computational cost”; “revert to earlier states” |
| 算法全貌 | p.15, Algorithm 1 | `LATS(s,pθ,pV,pref,...)` |
| WebShop 具体失败轨迹 | pp.21–23, G.2–G.3 | “accidentally bought a product that was $100”; “Invalid action!” |

## 8. 解析文本与可视 PDF 一致性

- [AUTHOR_FACT] 已逐页检查 PDF p.1–23 的解析文本，并将全部 23 页在内存中渲染为页面图像核对版面；未发现“可视 PDF 表达一个结论而解析文本表达相反结论”的实质冲突。
- [READER_INTERPRETATION] 双栏正文的解析顺序总体可辨，但局部会把左右栏相邻段落拼接；因此本报告以页码、章节、表图编号和短定位词交叉定位，而没有依赖单一连续文本顺序。（典型：PDF pp.1–9、14–17）
- [READER_INTERPRETATION] 公式、上标、撇号、破折号和代码字体存在字符级解析噪声；例如标题页破折号、Eq. 1/Algorithm 1 的上下标、Programming prompt 的 Python 空格与引号均不能把解析文本当作精确源码。（PDF pp.1, 4–5, 15, 19–20）
- [READER_INTERPRETATION] Fig. 2 的流程图、Fig. 3 的曲线及 Fig. 4 的示例轨迹内部细节不能由纯文本完整恢复；解析主要保留 caption 与邻近正文。表格数值则可由解析文本与可视布局相互核对。（PDF p.5 Fig. 2；p.16 Fig. 3；p.17 Fig. 4；Tables 2–13）
- [OPEN_QUESTION] 本次核对使用低分辨率内存渲染联系图检查全页结构，并对 p.1 单页单独渲染；没有做像素级/OCR 双引擎逐字符比对。因此“无实质冲突”不等于证明每个字形完全一致。

## 9. Provenance、实际读取文件与工具

### 实际读取的文件（仅以下三项）

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P003_lats.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P003/read_2_attempts/r2-20260719-p003-a1/invocation.md`

未读取 read_1、Cards、其他读者报告、blind query 或工作区其他研究材料；未联网。

### 实际使用的工具与可观察操作

- PowerShell `Get-Content -Raw -Encoding UTF8`：读取 prompt 与 invocation。
- PowerShell `Get-FileHash -Algorithm SHA256`：核对指定 PDF 哈希。
- `pdfinfo.cmd`：曾尝试读取指定 PDF 元信息，但运行失败并返回 “The system cannot find the path specified”；未据此产生页数结论。
- Python `PyMuPDF` (`fitz`)：打开指定 PDF，确认 23 页，逐页抽取 p.1–23 文本与页面结构统计，并在内存中渲染页面。
- Python `Pillow`：仅在内存中组合 PDF 页面联系图；没有写出中间图像文件。
- Codex 图像输出：查看内存生成的页面图像，核对可视布局。
- `apply_patch`：唯一写操作，仅创建本 `report.md`。

Actual model/version：`unknown`（运行时未提供可核验的精确模型版本）。Canonical task：`/root/p003_second_read`。文件级强制 allowlist：`unavailable`；本次按 invocation 执行 `procedural_blinding`。完整系统级 file-access/tool trace：`unavailable`；上列为本读者在会话中实际可观察并执行的操作。
