# P002 独立二读报告

## 0. 来源与边界

- 审计记录：本报告对应 invocation snapshot：`read_2_attempts/r2-20260719-p002-a1/invocation.md`，Attempt ID 为 `r2-20260719-p002-a1`；角色是 fresh independent full-paper source checker。
- 审计记录：实际读取的 PDF SHA-256 为 `6939cadebd84c8cdcc6ff3c2082b75851a86e2ef82008848d0af692f80521fa7`，与 invocation 记录一致；PDF 共 14 页。
- 审计记录：canonical metadata 为 *Tree of Thoughts: Deliberate Problem Solving with Large Language Models*，NeurIPS 2023，official proceedings。
- [READER_INTERPRETATION] 本报告只做独立核源与机制/边界梳理，不生成 Card，不合并其他读者结论，也不评价 Candidate。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] ToT 改变的是**推理时的中间解搜索与选择过程**：不再只采样一条连续、从左到右的 CoT，而把状态写成 `s=[x,z1...zi]`，显式维护由“thought”构成的树。定位：PDF p.3，§3，短定位文本 “frames any problem as a search over a tree”。
- [AUTHOR_FACT] 一个具体 ToT 实例包含四个环节：thought decomposition、thought generation、state evaluation、search algorithm。定位：PDF pp.3–4，§3，短定位文本 “answering four questions”。
- [AUTHOR_FACT] thought generator 有两种实现：从当前状态独立采样 `k` 个后继，或在同一 propose prompt 中顺序提出 `k` 个不同后继。定位：PDF p.3，§3 条目 2；Figure 2/4/6。
- [AUTHOR_FACT] state evaluator 也有两种实现：逐状态给 value/classification，或在一组状态间 vote；可多次采样后聚合。定位：PDF p.4，§3 条目 3，短定位文本 “Value each state independently” 与 “Vote across states”。
- [AUTHOR_FACT] 搜索器使用 BFS 或 DFS：BFS 每层保留最优 `b` 个状态；DFS 按估值优先展开，在低于阈值时剪枝并回溯。定位：PDF p.4，Algorithm 1、Algorithm 2、§3 条目 4。
- [READER_INTERPRETATION] 因而核心计算改动不是训练新模型，而是把一次自回归解码改造成“LM 生成候选—LM 评估候选—外部搜索控制器选择/剪枝/回溯”的闭环。定位依据：PDF pp.3–4，§3；p.9，§6 “off-the-shelf LM”。

## 2. 输入、输出、可用信息与干预时点

### 2.1 通用接口

- [AUTHOR_FACT] 输入是问题 `x`；树状态包含 `x` 与此前 thoughts；输出由最终选中状态再经生成器产生。定位：PDF p.3，§3 状态定义；p.4，Algorithm 1 返回行。
- [AUTHOR_FACT] 方法不要求额外训练；本体依赖预训练 LM、任务化 thought decomposition、generation/evaluation prompts 和搜索过程。定位：PDF p.4，§3 “No extra training is needed”。
- [READER_INTERPRETATION] 干预发生在完整答案生成之前和各 thought 边界处，而不是 token 级每一步：每次扩展后先评估，再保留、剪枝或回溯。定位依据：PDF pp.3–4，§3 与 Algorithms 1–2。

### 2.2 Game of 24

- [AUTHOR_FACT] 输入为 4 个数；输出为每个数恰用一次且等于 24 的合法算式；thought 是三步中间算式。定位：PDF p.5，Table 1、§4.1 “Task Setup”。
- [AUTHOR_FACT] 可用信息是当前剩余数字与此前中间算式；同一个 propose prompt 在三步上复用，BFS 每步保留 `b=5`，value prompt 将状态判为 sure/maybe/impossible，每个 thought 的 value 采样 3 次。定位：PDF p.5，§4.1 “ToT Setup”；Figure 2。
- [READER_INTERPRETATION] 干预点是每生成一条中间算式之后；搜索器依据 LM 对“剩余数字还能否到 24”的近似前瞻决定是否继续。定位依据：PDF pp.4–5，§3 evaluator 与 §4.1。

### 2.3 Creative Writing

- [AUTHOR_FACT] 输入是 4 个随机句子；输出是 4 段连贯文章，每段必须依次以一个输入句结尾；中间 thought 是短写作计划。定位：PDF pp.5–6，Table 1、§4.2 “Task setup”。
- [AUTHOR_FACT] ToT 先采样 5 个计划并用 5 次 vote 选一个，再基于所选计划采样 5 篇文章并以同样方式 vote；树深为 2、breadth limit `b=1`。定位：PDF p.6，§4.2 “ToT setup”；p.7，Figure 4。
- [READER_INTERPRETATION] 这里的主要干预点有两个：计划生成后选择一次，文章生成后再选择一次；它更接近分阶段 best-of-5，而非多层宽搜索。定位依据：PDF pp.6–7，§4.2、Figure 4。

### 2.4 Mini Crosswords

- [AUTHOR_FACT] 输入为 5 条横向和 5 条纵向 clue；输出是 5×5、共 25 个字母的棋盘；thought 是待填 clue 的候选单词。定位：PDF p.7，Table 1、§4.3 “Task setup”。
- [AUTHOR_FACT] 当前已填词被转成剩余 clue 的字母约束；LM 多次提出“填哪一条 clue、填什么词”并给置信度，聚合后形成 DFS 次序；若任一剩余 clue 被判 impossible，则剪枝并回溯。定位：PDF pp.7–8，§4.3 “ToT setup”；Figure 6。
- [AUTHOR_FACT] 搜索最多 100 步；最终简单输出达到的最深状态（并列时取最先探索者）。定位：PDF p.8，§4.3，短定位文本 “limit DFS search steps to 100”。
- [AUTHOR_FACT] 本实验刻意不使用检索，作者说明外部 retrieval/web interaction 可缓解罕见词知识不确定性。定位：PDF pp.7–8，§4.3 与 footnote 2。

## 3. 最强基线与最接近组合基线

### 3.1 Game of 24

- [AUTHOR_FACT] 普通单法结果为 IO 7.3%、CoT 4.0%、CoT-SC(`k=100`) 9.0%；IO+Refine(`k=10`) 为 27%；ToT `b=1` 为 45%、`b=5` 为 74%。定位：PDF p.6，Table 2。
- [AUTHOR_FACT] 论文另报 oracle “best of 100”：IO 33%、CoT 49%；作者明确称其为 oracle setup。定位：PDF p.6，§4.1 “Results”、Table 2。
- [READER_INTERPRETATION] 若“最强基线”要求可部署、无答案 oracle，则表中最强是 IO+Refine 27%，但它使用方程正确性的 ground-truth feedback；若只比较同模型下的采样上限，最强是 CoT best-of-100 49%，不能与无 oracle 的选择规则等同。定位依据：PDF pp.5–6，§4.1 “Baselines/Results”。
- [READER_INTERPRETATION] 最接近的组合基线不是单一一个：CoT-SC 提供多链采样与聚合，IO+Refine 提供迭代反馈；两者都缺少 ToT 的局部树扩展加状态级搜索。定位依据：PDF p.3，§2；p.5，§4.1。

### 3.2 Creative Writing

- [AUTHOR_FACT] GPT-4 连贯性均分：IO 6.19、CoT 6.93、ToT 7.56；IO+Refine 7.67、ToT+Refine 7.91。定位：PDF pp.6–7，§4.2 “Results”、Figure 5(a)。
- [AUTHOR_FACT] 作者子集的盲序成对判断中，ToT 胜 CoT 41 次、相当 38 次、CoT 胜 ToT 21 次。定位：PDF pp.6–7，§4.2、Figure 5(b)。
- [READER_INTERPRETATION] 最强表内配置是 ToT+Refine 7.91；最强非 ToT 基线是 IO+Refine 7.67，且高于纯 ToT 7.56。最接近组合基线是 CoT 的“先计划再写”与 iterative-refine，但论文未给“CoT+vote”或等调用预算的完整因子基线。定位依据：PDF pp.6–7，§4.2。

### 3.3 Mini Crosswords

- [AUTHOR_FACT] IO/CoT 的字母、单词、整局成功率分别为 38.7/14/0 和 40.6/15.6/1；ToT 为 78/60/20。定位：PDF p.7，Table 3。
- [AUTHOR_FACT] oracle best state 为 82.4/67.5/35；去掉 pruning 为 65.4/41.5/5；去掉 backtracking 为 54.6/20/5。定位：PDF p.7，Table 3；p.8 “Oracle and ablation studies”。
- [READER_INTERPRETATION] 最接近组合基线是 CoT（按 h1..5、v1..5 依次填词），但它没有改写决策或回溯；`-backtrack` 是更直接的机制消融，对回溯贡献的证据强于只与 CoT 比较。定位依据：PDF pp.7–8，§4.3。

## 4. 模型、token、tool-call、prompt 与 oracle 差异

- [AUTHOR_FACT] 主实验除另述外均为 Chat Completion 模式 GPT-4、temperature 0.7，运行时间为 2023-05-05 至 2023-05-16。定位：PDF p.5，§4 开头及 footnote 1。
- [OPEN_QUESTION] 原文没有给出精确 GPT-4 model snapshot/version，因此无法核验所有调用是否锁定同一后端版本。定位：PDF p.5 只写 “GPT-4”。
- [AUTHOR_FACT] ToT 显著增加计算：Game of 24 每题 completion/prompt tokens 为 5.5k/1.4k、成本 $0.74；IO best-of-100 为 1.8k/1.0k、$0.13；CoT best-of-100 为 6.7k/2.2k、$0.47。定位：PDF p.14，Appendix B.3，Table 7。
- [AUTHOR_FACT] Creative Writing 中 ToT 使用约 5 倍 completion tokens 和费用：IO 0.9k/0.4k、$0.06；CoT 0.9k/0.4k、$0.07；ToT 4k/2.9k、$0.32。定位：PDF p.14，Appendix B.3，Table 8。
- [AUTHOR_FACT] 作者概括 ToT 可能需要比 CoT 多 5–100 倍生成 token。定位：PDF p.14，Appendix B.3。
- [READER_INTERPRETATION] 因此主结果不能解释为“只改变搜索拓扑”的纯因果效应：生成次数、评估次数、prompt 类型和任务化分解同时变化。Game of 24 的 best-of-100 成本表缓解了部分预算疑问，但不能替代等 tool-call、等 prompt-token、等 oracle 的完整控制。定位依据：PDF pp.3–6、p.14。
- [AUTHOR_FACT] Game of 24 的 IO+Refine 每轮接收方程是否正确的 ground-truth feedback；IO/CoT best-of-k 也由真实成功判据 oracle 选样本。定位：PDF pp.5–6，§4.1。
- [READER_INTERPRETATION] 这两类结果应与 ToT 的 LM heuristic selection 分开看，不能把 27% 或 49% 当作同信息条件的普通基线。定位依据：PDF pp.5–6，§4.1。
- [AUTHOR_FACT] Creative Writing 的自动指标由 GPT-4 零样本打 1–10 分，每个输出取 5 个分数平均；人评由“subset of the authors”完成盲序成对比较。定位：PDF p.6，§4.2 “Task setup”。
- [READER_INTERPRETATION] 生成器与自动评估器同属 GPT-4，可能存在同模型偏好；作者人评降低了这一风险，但评审者并非独立外部标注者，且只直接比较 CoT 与 ToT。定位依据：PDF p.6，§4.2。
- [AUTHOR_FACT] GPT-3.5 的 Game of 24 实验把 proposal prompt 从 1-shot 改为 3-shot；其 ToT 为 19%，而 GPT-4 ToT 为 74%。定位：PDF p.14，Appendix B.2、Table 5。
- [READER_INTERPRETATION] 该跨模型差异同时含模型与 prompt-shot 数差异，不能视作严格模型替换实验。定位依据：PDF p.14，Appendix B.2。
- [AUTHOR_FACT] Crosswords 的 `+best state` 是 oracle；普通 ToT 最终输出规则会遗漏搜索途中已得到的正确状态。定位：PDF p.8，§4.3 “Oracle and ablation studies”。

## 5. 明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者明确说 ToT 对 GPT-4 已擅长的任务可能没有必要；主文只研究三个相对简单、刻意挑战 GPT-4 的任务。定位：PDF p.9，§6 “Limitations and future directions”。
- [AUTHOR_FACT] Appendix 的 GSM8K/StrategyQA 上 ToT 只比 CoT 小幅提高：90 对 86、83 对 82；作者认为 StrategyQA 瓶颈是外部知识而非推理。定位：PDF pp.13–14，Appendix B.1、Table 4。
- [AUTHOR_FACT] ToT 比采样法消耗更多资源；更高级搜索如 A*、MCTS 未在本文实验，留作未来工作。定位：PDF p.4，§3 条目 4；p.9，§6；p.14，Appendix B.3。
- [AUTHOR_FACT] 本文只使用 off-the-shelf LM；ToT 风格微调未测试。定位：PDF p.9，§6。
- [AUTHOR_FACT] Creative Writing 中 IO+Refine 7.67 高于未加 refine 的 ToT 7.56；这是表内真实负向/边界结果。定位：PDF p.7，§4.2、Figure 5(a)。
- [AUTHOR_FACT] Game of 24 中 CoT 4.0% 低于 IO 7.3%，CoT-SC 也只有 9.0%；约 60% CoT 样本在第一步即失败。定位：PDF p.6，Table 2、Figure 3(b)、“Error analysis”。
- [AUTHOR_FACT] Crosswords 中 evaluator 会把已经正确的罕见/旧词状态误判为 impossible 并剪枝；不剪枝时能搜索到 4/20 个正确解，却只由输出 heuristic 交付 1 个，其中 3 个是带剪枝 ToT 在 100 步内找不到的。定位：PDF p.8，§4.3 “Oracle and ablation studies”、footnote 2。
- [AUTHOR_FACT] 去掉 backtracking 后单词成功率降至 20%，整局仅 5%；作者据此强调回溯重要。定位：PDF pp.7–8，Table 3 与 §4.3。
- [OPEN_QUESTION] 未测试边界包括：更深/更宽的长期任务、真实世界编码/数据分析/机器人决策、带外部检索的知识不确定性、非 GPT 系列模型的大规模比较，以及在固定总预算下的最优搜索配置。定位依据：PDF pp.8–9，§5–6；p.14，Appendix B.3。
- [AUTHOR_FACT] Broader Impact 提醒：未来与外部环境或人交互可能放大有害使用；同时作者认为显式高层语言状态可能提高可解释性与人类对齐机会。定位：PDF p.10，Broader Impact。

## 6. 可抽取的 Operator 与真实可记录的 Failure

### 6.1 Operator 候选（仅独立核源，不生成正式 Card）

- [AUTHOR_FACT] **Task-aware thought decomposition**：按问题结构确定可生成且可评估的中间单元。定位：PDF p.3，§3 条目 1，短定位文本 “small enough” / “big enough”。
- [AUTHOR_FACT] **Independent sample / sequential propose**：按 thought 空间开放度选择独立采样或同上下文去重式提案。定位：PDF p.3，§3 条目 2。
- [AUTHOR_FACT] **State value / pairwise-set vote**：对状态单独赋值，或在状态集合中投票。定位：PDF p.4，§3 条目 3。
- [AUTHOR_FACT] **Repeated-evaluation aggregation**：重复 value/vote，用更多成本换稳定 heuristic。定位：PDF p.4，§3 条目 3 末段。
- [AUTHOR_FACT] **BFS top-b retention**：逐层保留 `b` 个最有希望状态。定位：PDF p.4，Algorithm 1。
- [AUTHOR_FACT] **DFS threshold pruning and backtracking**：按候选次序深搜，低价值剪枝并回溯。定位：PDF p.4，Algorithm 2；p.8，Figure 6。
- [AUTHOR_FACT] **Constraint serialization**：把当前状态转成剩余数字或字母约束，供下一次 proposal/evaluation。定位：PDF p.5，Figure 2；pp.7–8，Figure 6。
- [AUTHOR_FACT] **Refinement as thought generation**：作者把从旧 thought refine 出新 thought 视作第三类 generation。定位：PDF p.7，§4.2 末段。

### 6.2 Failure 候选

- [AUTHOR_FACT] **Early irreversible CoT failure**：约 60% Game of 24 CoT 样本第一步后已无解。定位：PDF p.6，Figure 3(b)、“Error analysis”。
- [AUTHOR_FACT] **False-negative pruning under knowledge uncertainty**：Crosswords 对罕见/旧词作 impossible 误判，会剪掉正确子树。定位：PDF p.8，§4.3、footnote 2。
- [AUTHOR_FACT] **Final-state heuristic misses discovered solution**：不剪枝实验曾找到 4/20 个正确解，普通输出 heuristic 只输出 1 个。定位：PDF p.8，§4.3。
- [AUTHOR_FACT] **No-backtracking degradation**：`-backtrack` 单词正确率仅 20%，明显低于完整 ToT 的 60%。定位：PDF p.7，Table 3；p.8，§4.3。
- [AUTHOR_FACT] **Weak marginal gain when base task is easy/knowledge-limited**：GSM8K 和 StrategyQA 只比 CoT 高 4 和 1 个百分点。定位：PDF pp.13–14，Table 4、Appendix B.1。
- [AUTHOR_FACT] **Resource escalation**：ToT 可能需要 CoT 的 5–100 倍生成 token。定位：PDF p.14，Appendix B.3。
- [READER_INTERPRETATION] 上述 Failure 都是原文直接报告的误差、消融退化或资源边界；“ToT 一定优于 CoT/Refine”不是可记录事实，因为 Creative Writing 的 IO+Refine 高于纯 ToT，且易任务增益很小。定位依据：PDF p.7、pp.13–14。

## 7. 逐页核查索引

- [AUTHOR_FACT] p.1：标题、摘要、§1 Introduction；报告 CoT 4% 与 ToT 74% 的 Game of 24 摘要结果。
- [AUTHOR_FACT] p.2：Figure 1；§1 结尾与 §2 Background 开头；定义 IO，并提出维护/探索备选与前瞻/回溯。
- [AUTHOR_FACT] p.3：§2 的 CoT、CoT-SC 定义；§3 的状态、thought decomposition、generator 与 evaluator 开头。
- [AUTHOR_FACT] p.4：evaluator 两类策略、Algorithms 1–2、BFS/DFS 及框架性质；§4 开头。
- [AUTHOR_FACT] p.5：Table 1、Figure 2；§4.1 Game of 24 的任务、基线与 ToT 配置。
- [AUTHOR_FACT] p.6：Table 2、Figure 3；Game of 24 结果/误差；§4.2 Creative Writing 的任务、基线、ToT 与结果。
- [AUTHOR_FACT] p.7：Figures 4–5、Table 3；Creative Writing 结果续；§4.3 Crosswords 的任务、基线和 ToT 配置开头。
- [AUTHOR_FACT] p.8：Figure 6；Crosswords 的搜索、结果、oracle/剪枝/回溯消融；§5 开头。
- [AUTHOR_FACT] p.9：§5 Related Work 后半；§6 Discussion 的限制与结论。
- [AUTHOR_FACT] p.10：Broader Impact、Acknowledgements、References [1]–[13]。
- [AUTHOR_FACT] p.11：References [14]–[33]。
- [AUTHOR_FACT] p.12：References [34]–[44]。
- [AUTHOR_FACT] p.13：Appendix A 代码/提示/轨迹链接；Appendix B、Table 4–6、B.1 的 zero-shot ToT 配置。
- [AUTHOR_FACT] p.14：B.1 结果续、B.2 GPT-3.5、B.3 成本与效率、Tables 7–8。

## 8. 解析文本与可视 PDF 冲突检查

- 审计记录：页级文本提取覆盖 PDF 14/14 页；正文段落、章节标题、算法、表格数值与图注均可提取。
- 审计记录：PDF pp.2、5、7、8 的 Figure 1/2/4/6 内部使用了特殊字体/矢量文本，解析输出出现字符映射乱码；相邻正文与图注仍可读，Tables 1–8 的关键数值可提取。
- [READER_INTERPRETATION] 目前没有发现正文、表格与图注之间的实质结论冲突；但这不等于完成了像素级视觉验真。
- [OPEN_QUESTION] 当前工具链的内存图像回传未成功，无法对每个图内的所有细字做完整可视核对；因此“完整可视 PDF trace”记为 `unavailable`，不能声称已排除所有排版/颜色编码层面的冲突。

## 9. 实际读取文件与工具记录

实际读取的研究文件仅有：

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P002_tree_of_thoughts.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P002/read_2_attempts/r2-20260719-p002-a1/invocation.md`

另外按系统要求读取了工具操作说明：`C:/Users/g/.codex/skills/pdf/SKILL.md`；它不是研究证据来源。

实际使用的工具/方式：`shell_command` 调用 Python `pypdf` 做 PDF 页数、metadata 与 14 页逐页文本提取，Python `hashlib`/PowerShell `Get-FileHash` 尝试做 SHA-256 核验（最终由 Python 成功核验），Python `PyMuPDF` 尝试内存渲染关键页（图像回传未成功），以及 `apply_patch` 写入本报告。未联网，未枚举工作区，未读取 read_1、Cards、其他读者报告或 blind query。

可观察的完整 file-access/tool trace：`unavailable`。以上仅是本读者能够如实列出的显式调用记录；App 未提供可验证的文件级 allowlist，边界属于 `procedural_blinding`，不是技术隔离。
