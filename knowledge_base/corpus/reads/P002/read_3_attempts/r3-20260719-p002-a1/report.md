# P002 fresh 独立第三读报告

## 0. Provenance 与边界

- Invocation：`r3-20260719-p002-a1`；角色为 fresh independent third full-paper source checker。本报告引用并遵循指定的 `invocation.md` 与冻结版 `second_read_prompt.md`。
- 论文：*Tree of Thoughts: Deliberate Problem Solving with Large Language Models*，NeurIPS 2023；本地 PDF 共 14 页。重新计算的 PDF SHA-256 为 `6939cadebd84c8cdcc6ff3c2082b75851a86e2ef82008848d0af692f80521fa7`，与 invocation 一致。
- 实际模型可见信息：Codex（GPT-5）；更精确的服务端 model/version 对本读者不可见。Canonical subtask：`/root/p002_third_read`；独立 thread ID 不可见。
- 隔离性质：`procedural_blinding`，不是可验证的文件级技术隔离。实际工作区内容读取仅限以下三项：指定 PDF、`knowledge_base/templates/second_read_prompt.md`、本 attempt 的 `invocation.md`。未枚举工作区，未读取 read_1、任何 read_2、Card、其他读者报告或 blind query，未联网。
- 可观察工具轨迹：PowerShell `Get-Content`（首次默认解码出现中文乱码，随后显式 UTF-8 重读）；本地命令可用性探测（`pdfinfo`、`pdftotext`、`mutool`、`qpdf`、`gswin64c`、`tesseract` 均不可用，Python 可用）；Python 仅对指定 PDF 做 SHA-256；PyMuPDF/PyPDF 模块探测；PyMuPDF 逐页文本抽取、页数/元数据读取、14 页逐页内存栅格化；对图 1、2、4、6 做内存裁切复核；Pillow 仅用于一次未落盘的内存拼图尝试。工具运行时加载了系统 Python/PyMuPDF/Pillow 包文件，但没有把它们作为研究材料读取。除本 `report.md` 外未写入其他文件。
- 报告约束：这里只做独立核源与统一问题回答；不生成 Card，不合并其他读者结论，不作 Candidate、novelty 或科研价值评价。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] ToT 把一次连续、从左到右的 CoT 生成改写为对显式状态树的搜索：节点状态为 `s=[x,z1...i]`，每个节点保存输入和迄今 thought 序列；局部生成多个下一 thought，随后用 LM 评价状态，再由搜索程序决定继续、剪枝或回溯。（PDF p.3，§3，定位：“search over a tree”与“four questions”）
- [AUTHOR_FACT] 一个具体 ToT 实例包含四个可独立设计的部件：thought decomposition、thought generator、state evaluator、search algorithm。thought 的粒度按任务变化，可以是一行中间算式、一个写作计划或一个填词答案。（PDF p.3，§3；Table 1，PDF p.5；定位：“A specific instantiation ... four questions”）
- [AUTHOR_FACT] 生成器有两种实现：从 CoT prompt 独立采样 `k` 个 thought，或用 propose prompt 在同一上下文中顺序提出 `k` 个不重复候选；前者用于 Creative Writing，后者用于 Game of 24 与 Crosswords。（PDF p.3，§3 “Thought generator”；Figures 2/4/6，PDF pp.5/7/8）
- [AUTHOR_FACT] 评价器也有两种实现：逐状态产生数值/类别 value，或把多个状态放在一起投票选出最有希望者；评价可以重复采样并聚合。（PDF pp.3–4，§3 “State evaluator”，定位：“Value each state independently”与“Vote across states”）
- [AUTHOR_FACT] BFS 每一步扩展候选并保留 value 总和最大的 `b` 个状态；DFS 按候选优先级深入，遇到阈值剪枝或终点后回溯。论文实现 Game of 24/Creative Writing 用 BFS，Crosswords 用 DFS。（PDF p.4，Algorithms 1–2，§3 “Search algorithm”）
- [READER_INTERPRETATION] 因而核心干预点不是训练参数，也不是单纯把 prompt 写得更长，而是“在一个中间语义单元生成后、生成后续单元前”插入分支、LM 自评与外部搜索控制；token 级解码器仍是同一个基础 LM。
- [OPEN_QUESTION] Algorithm 2 的伪代码在评价新状态时写成 `V(pθ,{s′})(s)`，同时参数表写 `vth` 而判断行写 `vthres`；正文语义显然指向评价 `s′`，但论文未说明这是排版笔误还是实现细节。（PDF p.4，Algorithm 2，定位：“if V ... > vthres”）

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 通用输入是任务实例 `x` 及 prompt 中的指令/少样例；生成器可见当前状态 `s=[x,z1...i]`，独立 value 评价器可见单一状态，vote 评价器可见一组候选状态；最终输出由所选末端/最优状态继续生成。（PDF pp.2–4，§2–§3；Algorithm 1 返回行）
- [AUTHOR_FACT] Game of 24 输入为四个数，输出为每个输入数恰用一次且等于 24 的算式；ToT 在三次中间算式之间干预，每步提出候选、以 `sure/maybe/impossible` 三次评价并做 `b=5` BFS。（PDF p.5，Table 1、Figure 2、§4.1 “Task/ToT Setup”）
- [AUTHOR_FACT] Creative Writing 输入为四个随机句子，输出为四段连贯文字且各段分别以给定句子结束；ToT 先采样 5 个计划并投票 5 次保留 1 个，再基于该计划采样 5 篇文章并投票 5 次保留 1 个。（PDF pp.6–7，§4.2、Figure 4，定位：“depth 2”与“sample 5 votes”）
- [AUTHOR_FACT] Mini Crosswords 输入 5 个横向、5 个纵向 clue，输出 5×5 字母板；程序把已有 thought 转为剩余 clue 的字母约束，LM 提案并给置信度，评价器检查每个剩余 clue 是否仍可填，DFS 最多搜索 100 步。（PDF pp.7–8，§4.3、Figure 6）
- [AUTHOR_FACT] Crosswords 的最终输出不是全局验证后的最优状态，而是“最深探索状态”（并列时取最先探索者）；这使搜索轨迹到最终答案之间又多了一层启发式选择。（PDF p.8，§4.3 “ToT setup”，定位：“render the deepest explored state”）
- [READER_INTERPRETATION] 可用信息不只原始输入与先前自然语言 thought，还包括任务代码产生的结构化状态：Game of 24 的剩余数字、Crosswords 的交叉字母约束、搜索队列与阈值。这些程序化转换属于 ToT 系统的一部分，不能只按单次 prompt 比较理解结果。
- [AUTHOR_FACT] 主实验未调用外部检索或环境工具；Crosswords 反而明确把“大规模检索的专门管线”排除在研究目标之外，并指出外部检索可能缓解稀有词知识不确定性。（PDF pp.7–8，§4.3 及脚注 2）

## 3. 最强基线与最接近组合基线

### 3.1 Game of 24

- [AUTHOR_FACT] 标准基线结果为 IO 7.3%、CoT 4.0%、CoT-SC (`k=100`) 9.0%；带最多 10 次、且使用算式正确性 ground-truth 反馈的 IO+Refine 达 27%。按表中非 oracle 基线，IO+Refine 最强。（PDF pp.5–6，§4.1 “Baselines”；Table 2）
- [AUTHOR_FACT] 论文另报 oracle “best of 100”：IO 33%、CoT 49%；这是从 100 个样本中按答案正确性选最优的分析上界，不是无标签部署基线。ToT 为 `b=1` 45%、`b=5` 74%。（PDF p.6，Table 2、Figure 3(a)）
- [READER_INTERPRETATION] 最接近的组合基线是 CoT-SC（多路径采样后聚合）与 IO+Refine（生成—反馈—再生成），但前者只在最终答案聚合、后者依赖真实正确性反馈；二者都没有“thought 级分支 + LM 状态评价 + 系统搜索”的完整组合。

### 3.2 Creative Writing

- [AUTHOR_FACT] IO 与 CoT 均为 zero-shot；CoT 先计划再写，因而是最接近 thought 分解的基线。IO、CoT 每题生成 10 个样本；IO+Refine 最多 5 次。（PDF p.6，§4.2 “Baselines”）
- [AUTHOR_FACT] GPT-4 连贯性均分为 IO 6.19、CoT 6.93、ToT 7.56；IO+Refine 为 7.67，数值上高于未 refine 的 ToT；ToT+Refine 为 7.91，但这是 ToT 的扩展而非独立基线。（PDF pp.6–7，§4.2 Results、Figure 5(a)）
- [AUTHOR_FACT] 盲式作者子集比较只覆盖 CoT 与 ToT：100 对中偏好 ToT 41、偏好 CoT 21、相似 38。（PDF pp.6–7，§4.2、Figure 5(b)）

### 3.3 Mini Crosswords 与附加任务

- [AUTHOR_FACT] Crosswords 主基线仅 IO 与 CoT；CoT 在 letter/word/game 上为 40.6%/15.6%/1 场（20 场中），略强于 IO 的 38.7%/14%/0 场。ToT 为 78%/60%/4 场。（PDF pp.7–8，Table 3 与 Results）
- [READER_INTERPRETATION] `-prune`、`-backtrack` 与 `+best state` 是 ToT 内部消融/上界，不应冒充独立组合基线；其中 `+best state` 使用 oracle 轨迹状态选择。
- [AUTHOR_FACT] 附录的 100 题子集上，GSM8K 的 CoT/ToT 为 86/90，StrategyQA 为 82/83；在这些 GPT-4+CoT 已很强或受外部知识限制的任务上，增益很小。（PDF pp.13–14，§B.1、Table 4）

## 4. 模型、token、tool-call、prompt 与 oracle 差异

- [AUTHOR_FACT] 主实验除另有说明外使用 Chat Completion 模式 GPT-4、temperature 0.7，实验发生在 2023-05-05 至 2023-05-16。（PDF p.5，§4 开头与脚注 1）
- [OPEN_QUESTION] 论文没有给出可复现的 GPT-4 模型快照标识、随机种子或全部 API 采样轨迹；仅凭“GPT-4”与日期不能排除服务端版本变化。（PDF p.5，脚注 1；Appendix A 只给外部代码/轨迹链接，PDF p.13）
- [AUTHOR_FACT] Game of 24 中 ToT 每题约 5.5k completion/1.4k prompt tokens、成本 `$0.74`；CoT best-of-100 为 6.7k/2.2k、`$0.47`，IO best-of-100 为 1.8k/1.0k、`$0.13`。（PDF p.14，§B.3、Table 7）
- [AUTHOR_FACT] Creative Writing 中 ToT 每题约 4k completion/2.9k prompt tokens、`$0.32`，CoT 为 0.9k/0.4k、`$0.07`；作者总结 ToT 可需要 CoT 的 5–100 倍生成 token。（PDF p.14，§B.3、Table 8 与后文）
- [READER_INTERPRETATION] 因此主结果不能解释为“在等 token、等调用次数、等 prompt 下仅替换搜索结构”的净效应。ToT 同时改变 prompt 类型、调用次数、候选数量、上下文组织、LM 自评以及外部控制流；论文给了成本尺度分析，但没有完整的等预算对照。
- [AUTHOR_FACT] Game of 24 的 IO+Refine 明确使用真实算式正确性反馈；IO/CoT best-of-k 也由 oracle 正确性挑选。Crosswords `+best state` 从 DFS 轨迹中用 oracle 选最佳状态。（PDF pp.5–6，§4.1；PDF p.8，§4.3 “Oracle and ablation studies”）
- [READER_INTERPRETATION] 这些 oracle 结果适合作为诊断上界，不能与无需真实标签选择的 ToT 主运行当作同一信息条件。
- [AUTHOR_FACT] Creative Writing 自动评价由 GPT-4 zero-shot 打 1–10 分，每个输出采 5 个分数；人工评价者是“作者子集”，并做顺序随机化与盲比较。（PDF p.6，§4.2 “Task setup”）
- [OPEN_QUESTION] 论文未给出作者评价者人数、个体一致性、冲突处理，也未测试评价模型是否对由相近 GPT-4 prompt 生成的 ToT 文本存在方法偏好；人工对照又只比较 CoT 与 ToT，不能校准 IO+Refine。
- [AUTHOR_FACT] GPT-3.5 的 Game of 24 为 IO 6%、CoT 3%、ToT 19%，且需把 proposal prompt 从 1-shot 改为 3-shot；GPT-4 生成+GPT-3.5 评价为 64%，反向组合为 31%。（PDF pp.13–14，§B.2、Table 5）
- [READER_INTERPRETATION] GPT-3.5 对照同时改变了模型与 proposal few-shot 数，不能作为纯模型替换实验；但 64% 对 31% 的混合实验确实支持该任务更受 thought generation 质量制约。

## 5. 明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者明示：ToT 对 GPT-4 已擅长的许多任务可能没有必要；主文只研究三个相对简单、专门挑战 GPT-4 的任务；ToT 比采样法消耗更多资源。（PDF p.9，§6 “Limitations and future directions”）
- [AUTHOR_FACT] 未测试的搜索包括 A*、MCTS 等更高级算法；本文只实现 BFS/DFS，也只用 off-the-shelf LM，没有训练或微调 ToT 式决策能力。（PDF pp.4、9，§3 与 §6）
- [AUTHOR_FACT] Game of 24 的 CoT 4.0% 低于 IO 7.3%，且约 60% CoT 样本在第一步、约前三个词后就已不可达 24；ToT `b=1` 也只有 45%，增至 `b=5` 才达 74%。（PDF p.6，Table 2、Figure 3(b)）
- [AUTHOR_FACT] Crosswords 的 LM evaluator 会把实际可解状态判为 impossible 并错误剪枝；无剪枝搜索找到 4/20 个正确解，但最终启发式只输出其中 1 个，且其中 3 个是有剪枝 ToT 在 100 步内找不到的。（PDF p.8，§4.3 “Oracle and ablation studies”）
- [AUTHOR_FACT] Crosswords oracle best state 解出 7/20，而主输出只解出 4/20；`-backtrack` 的 word 成功率仅 20%，说明最终状态选择、剪枝与回溯均仍是显著失败来源。（PDF p.8，Table 3 与消融段）
- [AUTHOR_FACT] StrategyQA 上 ToT 仅比 CoT 高 1 点，作者把瓶颈归因于外部知识而非推理；Crosswords 脚注也指出稀有/废词知识可由检索补足。（PDF pp.8、14，脚注 2 与 §B.1）
- [AUTHOR_FACT] 作者提示未来与外部环境或人交互的应用可能增加危害，例如促进有害用途。（PDF p.10，“Broader Impact”）
- [OPEN_QUESTION] 论文没有测试真实世界长时任务、含噪声/动态反馈环境、不同语言、不同 prompt 作者、不同供应商模型、检索增强、严格等计算预算或独立外部人工评测；这些边界不能由三个主任务外推。

## 6. 可抽取的 Operator 与真实可记录 Failure（仅供核源，不生成 Card）

### 6.1 来源支持的 Operator 片段

- [AUTHOR_FACT] **任务自适应 thought decomposition**：把过程拆成可生成且可评价的语义单元。（PDF p.3，§3.1；Table 1，p.5）
- [AUTHOR_FACT] **多候选 thought generation**：独立采样或同上下文顺序 proposal。（PDF p.3，§3.2）
- [AUTHOR_FACT] **LM state evaluation**：独立 value、跨候选 vote，并可重复采样聚合。（PDF pp.3–4，§3.3）
- [AUTHOR_FACT] **BFS top-b 保留**：逐层扩展并只保留最有希望的 `b` 个状态。（PDF p.4，Algorithm 1）
- [AUTHOR_FACT] **DFS 阈值剪枝与回溯**：按优先级深入，不可行则剪子树并回到父状态。（PDF p.4，Algorithm 2；Figure 6，p.8）
- [AUTHOR_FACT] **sample–vote 两阶段选择**：先在写作计划间投票，再在文章间投票。（PDF pp.6–7，§4.2、Figure 4）
- [AUTHOR_FACT] **refinement 作为 thought generation 变体**：作者提出新 thought 可由旧 thought 迭代改写而来。（PDF pp.6–7，§4.2 Results）

### 6.2 论文实证支持的 Failure 片段

- [AUTHOR_FACT] **早期不可逆错误**：CoT 在 Game of 24 中约 60% 于第一步已失败。（PDF p.6，Figure 3(b)）
- [AUTHOR_FACT] **自评误剪正确路径**：Crosswords evaluator 可能把真实可解状态判为 impossible。（PDF p.8，消融段）
- [AUTHOR_FACT] **轨迹有解但输出启发式漏解**：无剪枝找到 4 个解却只输出 1 个；oracle best state 与主结果也有 7/20 对 4/20 的差距。（PDF p.8，Table 3 与消融段）
- [AUTHOR_FACT] **弱模型 generation 瓶颈**：Game of 24 中 GPT-3.5 generation+GPT-4 evaluation 仅 31%，反向为 64%。（PDF p.14，§B.2）
- [AUTHOR_FACT] **外部知识瓶颈**：StrategyQA 增益很小，Crosswords 稀有词导致错误评价。（PDF pp.8、14）
- [AUTHOR_FACT] **资源放大**：ToT 需要约 5–100 倍 CoT 生成 token，Creative Writing 成本约 5 倍。（PDF p.14，§B.3）
- [READER_INTERPRETATION] 上述项目是论文明确观测到的机制/失败来源；是否提升为正式 Operator/Failure、如何命名和去重，应留给后续 reconciliation，而不是由本报告裁决。

## 7. 关键判断—页码/章节/图表/短定位索引

| 判断 | 标签 | 核源位置 | 短定位文本 |
|---|---|---|---|
| 显式维护 thought 树 | [AUTHOR_FACT] | PDF p.2，§1，Figure 1 | “actively maintains a tree of thoughts” |
| 四组件实例化 | [AUTHOR_FACT] | PDF p.3，§3 | “answering four questions” |
| 独立 value / 跨状态 vote | [AUTHOR_FACT] | PDF pp.3–4，§3 | “Value each state independently” / “Vote across states” |
| BFS/DFS 控制流 | [AUTHOR_FACT] | PDF p.4，Algorithms 1–2 | “Breadth-first search” / “Depth-first search” |
| 三任务输入、输出、thought 粒度 | [AUTHOR_FACT] | PDF p.5，Table 1 | “Task overview” |
| Game of 24 74% | [AUTHOR_FACT] | PDF p.6，Table 2 | “ToT (ours) (b=5) 74%” |
| CoT 第一阶段大量失败 | [AUTHOR_FACT] | PDF p.6，Figure 3(b) | “around 60% ... first step” |
| 写作 sample–vote | [AUTHOR_FACT] | PDF p.7，Figure 4 | “samples 5 different plans” |
| 写作自动/人工结果 | [AUTHOR_FACT] | PDF p.7，Figure 5 | “21 / 38 / 41” |
| Crosswords DFS、剪枝、回溯 | [AUTHOR_FACT] | PDF p.8，Figure 6、Table 3 | “pruned if any ... impossible” |
| oracle best state 差距 | [AUTHOR_FACT] | PDF p.8，§4.3 | “solves 7/20 games” |
| 主限制与未来边界 | [AUTHOR_FACT] | PDF p.9，§6 | “only explores three relatively simple tasks” |
| GPT-3.5 与混合模型诊断 | [AUTHOR_FACT] | PDF pp.13–14，Tables 5–6、§B.2 | “bottleneck is thought generation” |
| token/成本差异 | [AUTHOR_FACT] | PDF p.14，Tables 7–8、§B.3 | “5-100 times more generated tokens” |

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 已对 PDF 1–14 页全部做文本抽取和内存栅格化逐页核对；正文段落、公式、表格数值、章节标题、页码与图注的版面对应关系一致，未发现缺页、页序错乱或正文数值在解析层与可视层相互矛盾。
- [AUTHOR_FACT] Figure 1（p.2）、Figure 2（p.5）、Figure 4（p.7）、Figure 6（p.8）内部使用的部分嵌入字体在 PyMuPDF 文本层被抽成异常 Unicode 字符；可视渲染中这些标签为正常英文、数字与流程框。该现象是解析层字体映射故障，不是论文视觉内容本身的冲突。相关结论均以可视图、图注和相邻正文交叉核对，没有依赖乱码字符串。
- [AUTHOR_FACT] PDF p.14 的 Table 8 内容明确是 Creative Writing 的 IO/CoT/ToT token 与成本，但可视图注写成 “Cost analysis on Game of 24.”；文本抽取层也同样如此。这是原稿图注命名不一致，不是解析器制造的冲突。（PDF p.14，Table 8）
- [OPEN_QUESTION] 除上述字体映射故障与 Table 8 图注不一致外，低层 PDF 字形到字符的语义映射不能仅靠抽取器保证；若后续需要逐字引用图内 prompt，应以更高分辨率人工转录复核，而不应复制当前乱码文本层。

## 9. 独立读者结语

- [READER_INTERPRETATION] 本文的实证支持对象是一个“任务化 thought 粒度 + 多候选生成 + LM 自评 + BFS/DFS 控制”的组合系统。主任务上有明显改进，但等预算、等 prompt、oracle 信息、评价者独立性和模型快照等问题没有被完全控制。
- [READER_INTERPRETATION] 最明确、可复核的负向证据集中在：CoT 早期错误、Crosswords 自评误剪、最终状态选择漏解、弱模型 thought generation 瓶颈，以及显著资源放大。以上均保留为来源判断，不延伸到 Candidate、novelty 或科研价值裁决。
