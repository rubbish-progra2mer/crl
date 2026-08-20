# P003 独立第三读全文核源报告

## 0. Provenance 与读取边界

- [AUTHOR_FACT] 本报告对应 invocation snapshot `r3-20260719-p003-a1/invocation.md`，Attempt ID 为 `r3-20260719-p003-a1`；canonical metadata 为 Zhou et al., *Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models*, ICML 2024 / PMLR 235。定位：invocation 顶部 metadata；短定位文本：“fresh independent third full-paper source checker”。
- [AUTHOR_FACT] 实际读取的项目研究输入只有三份：`P003_lats.pdf`、`second_read_prompt.md`、本 attempt 的 `invocation.md`。未枚举工作区，未读取 read_1、任何 read_2、Cards、其他读者报告或 blind query，未联网。PDF 实测 23 页，实算 SHA-256 为 `a6b84613eeeaa3beb979ac3e34cbb3575bceb7ccf6050a2c2fc677d5e3a3ab19`，与 invocation 一致。
- [AUTHOR_FACT] 为遵守运行环境强制技能流程，研究材料之外还读取了两份仅含通用工具规范、无项目内容的技能说明：`C:/Users/g/.codex/plugins/cache/openai-curated-remote/superpowers/6.1.1/skills/using-superpowers/SKILL.md` 与 `C:/Users/g/.codex/skills/pdf/SKILL.md`；另一次对不存在路径 `C:/Users/g/.codex/skills/.system/pdf/SKILL.md` 的读取尝试失败，未取得内容。这意味着本次是 invocation 所称的 `procedural_blinding`，不是可验证的文件级技术隔离。
- [AUTHOR_FACT] 实际工具链：Codex `functions.exec`、本地 PowerShell `shell_command`、Python 3、PyMuPDF（逐页文本/元数据/内存渲染）、Pillow（仅内存拼接缩略图）、`apply_patch`（唯一写入）。`pdfinfo` 调用因本机找不到命令而失败，之后未依赖它。没有生成落盘的中间文本或页面图像。
- [READER_INTERPRETATION] 模型身份在本会话可见为 Codex（GPT-5 系列）；更精确的部署版本不可见。canonical subtask/thread 为 `/root/p003_third_read`。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] LATS 将 CoT/ReAct 的单条自回归轨迹改为对“推理/动作”组合空间执行 MCTS 变体：每轮依次做 selection、expansion、evaluation、simulation、backpropagation、reflection，成功或达到 `k` 条轨迹预算时停止。定位：PDF p.2 Sec.1；p.5 Fig.2 / Sec.4.2；短定位文本：“search over a combinatorial space”“six operations in LATS”。
- [AUTHOR_FACT] expansion 不再只解码一个后继，而是在当前状态从同一个 `pθ` 采样 `n` 个动作，将每个动作送入环境并把返回 observation 组成子节点。定位：PDF p.4 Sec.4.1；p.5 “Expansion”；短定位文本：“sample n actions”。
- [AUTHOR_FACT] evaluation 在取得环境反馈后计算 `V(s)=λ·LM(s)+(1−λ)·SC(s)`：`LM(s)` 是同一 LM 对状态给出的 1–10 分式判断，`SC(s)` 奖励同一状态下重复采样到的动作。定位：PDF p.5 Eq.(2) / “Evaluation”；p.18–19 Sec.E.3；短定位文本：“after obtaining the environmental feedback”。
- [AUTHOR_FACT] selection 使用 UCT 平衡节点价值与访问次数；terminal reward 沿轨迹回传；失败终点还会生成 verbal reflection，并把失败轨迹与反思作为后续 agent/value-function 的上下文。定位：PDF p.4 Eq.(1)；p.5–6 “Backpropagation”“Reflection”；短定位文本：“learn from trial and error”。
- [READER_INTERPRETATION] 因而核心干预不是训练 `pθ`，而是在推理时把“下一步生成”包装成可回退、可分支、带外部反馈的状态搜索，并用同一 LM 同时承担 policy、heuristic evaluator 和 reflection generator。定位：PDF p.4 Sec.4.2；短定位文本：“repurposes pθ as an agent, state evaluator, and feedback generator”。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 抽象输入是自然语言 `x` 与预训练 LM `pθ`；在决策任务的时刻 `t`，policy 可见原始输入、此前动作与此前 observations。动作空间 `Â=A∪Z` 同时含环境动作与自由文本 thought。定位：PDF p.3 Sec.3.1；p.4 Sec.4.1；短定位文本：“space of permissible actions A”“reasoning traces Z”。
- [AUTHOR_FACT] 树节点定义为原始输入、截至当前的动作序列与 observation 序列；树和节点显式存入外部长时记忆。定位：PDF p.4 Sec.4.2；p.5 “Expansion”；短定位文本：“stored in an external long-term memory structure”。
- [AUTHOR_FACT] 干预发生在 inference time 的多个位置：扩展时采样候选；取得环境 observation 后再评分；到达终点后取得 objective reward 并回传；失败后生成 reflection 供下一轮上下文学习。定位：PDF p.5 Fig.2 与六个 operation 段落。
- [AUTHOR_FACT] 环境信息因任务而异：HotPotQA 提供 Wikipedia `search/lookup/finish` API、检索文本及答案正确性 oracle；programming 提供编译器和合成测试反馈；WebShop 提供网页文本、click/search 状态与自动 reward；Game of 24 没有外部工具，使用 CoT。定位：PDF p.6 Sec.5.1；p.7 Sec.5.2；p.8 Sec.5.3；p.15–17 Sec.D.1–D.4 / Table 12。
- [AUTHOR_FACT] programming 的每个 action 是完整程序，因此作者跳过 simulation；以内部测试通过比例作为回传 reward，搜索结束后选最高 value 的一个解，在真实测试集上计所谓 pass@1。定位：PDF p.7 Sec.5.2；短定位文本：“skip the simulation step”“select the solution with the highest value”。
- [OPEN_QUESTION] 除“遇到成功立刻停止”外，正文/Algorithm 1 没有对所有非 programming 任务统一写清预算耗尽时究竟返回哪一个节点/轨迹，以及并列 value 如何决胜。定位：PDF p.5 “Simulation”；p.15 Algorithm 1；短定位文本：“until the budget is reached”。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] HotPotQA reasoning-only（GPT-3.5，100 题）中，最强非 LATS 基线是 RAP `0.60 EM`，LATS(CoT) 为 `0.62`。定位：PDF p.6 Table 2。
- [AUTHOR_FACT] HotPotQA acting 中，与 LATS 结构最接近的是把 ReAct 接到 ToT/RAP：Table 3 报告 ToT(ReAct) `0.39`、RAP(ReAct) `0.54`，LATS(ReAct) `0.63`；LATS 自身的 CoT→失败后转 ReAct 组合为 `0.71`。定位：PDF p.6 Table 3；p.7 Sec.5.1；短定位文本：“simple adaptations of search algorithms”。
- [AUTHOR_FACT] HumanEval 的 GPT-3.5 组中最强非 LATS 基线是 Reflexion `68.1`，LATS 为 `83.8`；GPT-4 组中 Reflexion `91.0`，LATS `92.7`。MBPP 中最强非 LATS 基线 RAP `71.4`，LATS `81.1`。定位：PDF p.7 Tables 4–5。
- [AUTHOR_FACT] WebShop 的 prompting 基线中 Reflexion 为 score `64.2` / SR `35.0`；训练基线 fine-tuning 为 `67.5` / `45.0`；LATS 为 `75.9` / `38.0`。因此 LATS 的平均 score 高于这些基线，但 success rate 低于 fine-tuning。定位：PDF p.8 Table 6。
- [AUTHOR_FACT] Game of 24 中最接近的 MCTS reasoning 基线 RAP 为 `0.40`，LATS(CoT) 为 `0.44`。定位：PDF p.8 Table 7；p.17 Table 13。
- [READER_INTERPRETATION] “最强基线”依指标和资源口径而变：WebShop 若看平均 score 是 fine-tuning `67.5`，若看 SR 也是 fine-tuning `45.0`；HumanEval 则必须在同一 base model 组内比较，不能把 GPT-3.5 与 GPT-4 行直接混合。定位：PDF p.7 Table 4；p.8 Table 6。

## 4. 模型、token、tool-call、prompt 与 oracle 差异能否解释结果？

- [AUTHOR_FACT] 模型差异被部分控制但并未统一：HotPotQA、MBPP、WebShop、Game of 24 使用 GPT-3.5；HumanEval 同时报 GPT-3.5 与 GPT-4，且只在各自模型组内列基线。定位：PDF p.6–8 Tables 2–7。
- [AUTHOR_FACT] HotPotQA acting 明示使用 oracle：环境在收到答案后反馈正确性。作者称其用于聚焦“如何吸收高质量反馈”。定位：PDF p.6 Sec.5.1；短定位文本：“we use an oracle setup”。
- [READER_INTERPRETATION] 相同 `k` 不等于相同 LM 调用或 token 预算。LATS 每个扩展采 `n=5`，还调用 value prompt 与 reflection；ReAct(best of k) 只是多次轨迹采样。Table 9 只对 tree-search 方法给出成功时 token 数，ReAct/CoT-SC 的 token 栏为 “–”，所以不能据此完成对简单 prompting 基线的等 token 因果归因。定位：PDF p.6 Tables 2–3；p.9 Tables 9–10；短定位文本：“upon success”。
- [AUTHOR_FACT] 作者报告在成功样本上，LATS 与 ToT/RAP 同属 `O(kn)`，Table 9 token consumption 为 LATS `173,290`、ToT(ReAct) `210,215`、RAP(ReAct) `176,500`；Table 10 还报告 LATS 在不同 `k` 下成功所需平均节点较少。定位：PDF p.9 Tables 9–10。
- [OPEN_QUESTION] 原文没有清晰交代 Table 9 token 是否包含 agent、value、reflection 的全部输入/输出 token、环境 observation token 和失败轨迹；正文反而说明失败轨迹未计入该比较。定位：PDF p.9 “Sample complexity and token consumption”；短定位文本：“taking failed trajectories into account”。
- [AUTHOR_FACT] tool/oracle 可用性在 reasoning 与 acting 条件间不同：HotPotQA reasoning-only 不能检索，acting 可调用 Wikipedia API 并收到 terminal correctness；programming 的 acting 方法可看到内部测试/编译器反馈。定位：PDF p.6–7 Sec.5.1–5.2。
- [READER_INTERPRETATION] 因此 reasoning-only 与 acting 数字不构成纯“搜索算法”消融；更接近的归因证据是同一 ReAct 环境下的 ToT(ReAct)、RAP(ReAct)、LATS(ReAct) 及 LATS 组件消融。定位：PDF p.6 Table 3；p.8 Table 8。
- [AUTHOR_FACT] prompt 也不同：LATS 额外使用 value 与 reflection prompts，各方法在 HotPotQA 共有三条 few-shot examples；附录只完整列出 LATS 所用若干 prompt。定位：PDF p.6 Sec.5.1；p.18–23 Sec.E–G。
- [OPEN_QUESTION] 论文未提供跨方法完整 prompt/token/tool-call 审计，也未报告随机种子、重复运行、置信区间或显著性检验；100/50/397 等随机子集结果是否稳健，原文无法判断。定位：PDF p.6 Sec.5.1（100 题）；p.8 Sec.5.3（50 instructions）；p.16 Sec.D.2（MBPP 397）；p.17 Sec.D.4（50 games）。
- [READER_INTERPRETATION] HumanEval 的 `92.7 pass@1` 是从 `5` 个 expansion candidates × `8` iterations 中按内部 value 选出一个程序后再测 hidden tests，不是单次原始 LM 生成的 pass@1；公平性取决于各基线是否获得可比 search/test 预算。定位：PDF p.7 Table 4 / Sec.5.2；短定位文本：“sample 5 solutions”“8 iterations”。

## 5. 明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者明示两项主限制：相对 ReAct/Reflexion 计算成本更高；决策环境必须能回退到早期状态。定位：PDF p.9 Sec.6 “Limitations and future directions”；p.14 Sec.B。
- [AUTHOR_FACT] 作者进一步承认所测 benchmarks 相对现实交互环境较简单，某些环境不支持 rollback；Minecraft、更多 reasoning benchmarks、复杂环境与 multi-agent 被列为未来工作而非已验证范围。定位：PDF p.9 Sec.6；p.14 Sec.B；短定位文本：“relatively simple”“interesting avenues for future work”。
- [AUTHOR_FACT] WebShop 中 reflection 常常 generic、不能提供有效反馈并使 agent 陷入 local minima；ReAct(best of k) `59.1/32.0` 与 Reflexion `64.2/35.0` 的差距有限。定位：PDF p.8 Sec.5.3 / Table 6；短定位文本：“often generic”“stuck in local minima”。
- [AUTHOR_FACT] HotPotQA 的简单组合可失败：ToT(ReAct) `0.39` 低于 reasoning-only ToT `0.55`，RAP(ReAct) `0.54` 低于 reasoning-only RAP `0.60`。定位：PDF p.6 Tables 2–3；p.7 results discussion。
- [AUTHOR_FACT] LATS 消融的直接负向结果：No LM Heuristic `0.37`、DFS `0.42`、No Reflection `0.58`，完整 LATS(ReAct) `0.63`；`w=0.5` 为 `0.55`，`d=4` 为 `0.58`，`w=2.0` 仍为 `0.63`。定位：PDF p.8 Table 8；p.16 Table 11。
- [AUTHOR_FACT] 作者观察更深步骤常把 agent 推入 local minima 且很少改善成功；提高 exploration weight 到 `2.0` 没有提高最终准确率，只倾向更快收敛。定位：PDF p.14–15 Sec.C “Exploration weight”“Depth”。
- [AUTHOR_FACT] 安全边界仅作影响讨论：更强自主决策可能促进有害用途或执行 malware；论文没有相应安全实验。定位：PDF p.10 Impact Statement；短定位文本：“security risks”。

## 6. 可供后续抽取的机制与真实 Failure（本报告不生成 Card）

### 6.1 机制片段

- [READER_INTERPRETATION] 可抽取机制 O1：在可回退文本状态上做 inference-time branching，而不是延续单条 ReAct/CoT。证据：PDF p.3–5 Sec.3.2–4.2 / Fig.2。
- [READER_INTERPRETATION] 可抽取机制 O2：先执行候选动作取得外部 observation，再用 `LM score + self-consistency` 评估子节点。证据：PDF p.5 Eq.(2) / “Evaluation”。
- [READER_INTERPRETATION] 可抽取机制 O3：UCT selection + terminal reward backpropagation，使稀疏终局反馈影响后续分支。证据：PDF p.4 Eq.(1)；p.5 “Selection”“Backpropagation”。
- [READER_INTERPRETATION] 可抽取机制 O4：把失败轨迹与 verbal reflection 注入后续 policy/value context，形成无梯度的跨 trial 记忆。证据：PDF p.5–6 “Reflection”。
- [READER_INTERPRETATION] 可抽取机制 O5：任务特化接口——programming 跳过 simulation、用内部测试通过比例回传；HotPotQA 可先 CoT，失败后再切 ReAct。证据：PDF p.7 Sec.5.1–5.2。

### 6.2 原文直接支持的 Failure

- [AUTHOR_FACT] F1：把现成 search 直接套到 ReAct 并不保证受益，ToT(ReAct)/RAP(ReAct) 可低于其 reasoning-only 版本。定位：PDF p.6–7 Tables 2–3。
- [AUTHOR_FACT] F2：没有 LM heuristic 时，HotPotQA EM 从 `0.63` 降到 `0.37`；仅有 terminal binary reward 对搜索过于稀疏。定位：PDF p.8 Table 8；p.15 “LM value function”。
- [AUTHOR_FACT] F3：WebShop reflection 可能 generic 并陷入 local minima。定位：PDF p.8 Sec.5.3。
- [AUTHOR_FACT] F4：不能回退状态的环境不满足 LATS 的必要操作假设。定位：PDF p.9 Sec.6；p.14 Sec.B。
- [READER_INTERPRETATION] F5：当指标是 WebShop SR 时，LATS `38.0` 仍低于 fine-tuning `45.0`，说明平均属性匹配 score 的提升没有等比例转化为严格全条件成功。定位：PDF p.8 Table 6。

## 7. 原文内部不一致与未决复现问题

- [OPEN_QUESTION] HotPotQA 最大深度不一致：p.14 Sec.C 称主实验 `d=7`，p.16 Table 11 完整设置也写 `d=7`；但 p.15 Sec.D.1 写 “maximum depth limit of 6”。哪一项用于 Tables 2–3/8–11 无法由原文确定。
- [OPEN_QUESTION] programming 内部测试数量不一致：p.7 Sec.5.2 写 “number of generated tests at 4”；p.16 Sec.D.2 写 GPT-3.5 用 `6`、GPT-4 用 `4`。Table 4 的 GPT-3.5 数字究竟使用 4 还是 6 个内部 tests 未说明。
- [OPEN_QUESTION] HotPotQA 表间数值不一致：p.6 Table 3 与 p.8 Table 8 均给 ToT(ReAct) `0.39`；p.9 Table 9/10 给 `0.49`。p.6/8 给完整 LATS `0.63`，p.9 Table 10 在 `k=50` 给 `0.61`。没有注释说明是否来自不同 run、subset 或 stopping/cost 统计口径。
- [OPEN_QUESTION] p.5 prose 的 backpropagation 公式写成 `N(si)=N(si−1)+1` 且用前一节点量更新 `V(si)`，与 p.4 标准 MCTS 的“更新同一节点旧值”以及 p.15 Algorithm 1 的 `N(st+1)=N(st+1)+1` 不一致；需以代码或勘误确认哪些下标是排版错误。
- [OPEN_QUESTION] p.15 Algorithm 1 的函数签名 `LATS(s,pθ,pV,pref,d,k,n,w,a,b)` 与 Require 行的 `L,K,c,w,λ` 名称/数量不一致；伪代码还在 expansion loop 中写 `V(st)←V_t^(i)`，其究竟意在给 parent 还是第 `i` 个 child 赋值需要核验实现。
- [OPEN_QUESTION] p.19 Sec.E.4 标题为 “Reflection Prompt”，但可视 PDF 中正文与 p.18–19 Sec.E.3 value prompt 基本相同，仍要求最后输出 1–10 correctness score；这与 p.5–6 所述“总结错误并提出更优替代”的 reflection 功能不匹配。可能是附录复制/排版问题，不能据该页重建 HotPotQA reflection prompt。
- [OPEN_QUESTION] self-consistency 的动作等价判定没有操作化：自然语言 action 是按字符串完全相同、语义归并还是环境等价来计数，原文未说明。定位：PDF p.5 Eq.(2) 周围；短定位文本：“actions sampled multiple times”。

## 8. 解析文本与可视 PDF 核对

- [AUTHOR_FACT] 已逐页读取 PDF p.1–23 的解析文本，并对全部 23 页做了内存可视渲染核对；另以更高分辨率复核 p.5（Fig.2/公式）、p.9（Tables 9–10）、p.15（Algorithm 1）、p.17（Fig.4/Table 12）、p.19（Sec.E.4）。
- [READER_INTERPRETATION] 未发现页缺失、页序错乱、章节/图表标题错配或“解析文本声称存在但可视 PDF 不存在”的冲突。p.1 Fig.1、p.5 Fig.2、p.9 Tables 9–10、p.15 Algorithm 1、p.16 Fig.3/Table 11、p.17 Fig.4/Tables 12–13 均在可视页中存在。
- [READER_INTERPRETATION] 解析层会把双栏阅读顺序、表格列、算法缩进和代码排版扁平化，尤其是 p.9、p.15、p.17、p.19–23；本报告对这些页的数字/标题以可视渲染复核后的版面为准。上节列出的深度、测试数量、表格数值和 prompt 问题均直接存在于可视 PDF 内容本身，不是文本解析伪差异。

## 9. 边界声明

- [READER_INTERPRETATION] 本报告只回答统一核源问题并标示可复核证据，不与其他读者合并，不生成正式 Card，不进行 Candidate、novelty 或科研价值评价。
