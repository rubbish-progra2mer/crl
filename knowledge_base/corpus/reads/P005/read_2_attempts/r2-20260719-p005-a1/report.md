# P005 独立第二读报告

## 0. Provenance 与边界

- Attempt：`r2-20260719-p005-a1`
- 论文：*ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs*，ICLR 2024。
- 本报告引用的冻结快照：`knowledge_base/pilot/reads/P005/read_2_attempts/r2-20260719-p005-a1/invocation.md`。
- [AUTHOR_FACT] PDF 实测 SHA-256 为 `76f7d1a6acd0c8d86d0bd41340dd12976643b9bbcaed3008a2357ef2d492ff8a`，与 invocation 一致；PDF 共 23 个物理页。
- 独立性：未联网；未读取任何 `read_1`、Card、其他读者报告、blind query；未生成 Card，未评价 Candidate，未运行科研 Reviewer。
- 实际读取的研究文件仅有：
  1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P005_toolllm.pdf`
  2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
  3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P005/read_2_attempts/r2-20260719-p005-a1/invocation.md`
- 为遵循系统操作规范，另读取了两份非研究材料：`C:/Users/g/.codex/skills/pdf/SKILL.md` 与 `C:/Users/g/.codex/skills/encoding-safe-edit/SKILL.md`；它们不含 P005、首读或候选信息。
- 实际模型/版本：Codex（GPT-5 系列）；精确后端 build 不可见，记为 `unknown`。Canonical agent task：`/root/p005_second_read`；产品级 thread ID 不可见，记为 `unknown`。
- 使用工具：PowerShell `Get-FileHash`；本地 Python `pypdf`（逐页文本解析）、PyMuPDF/`fitz` 与 Pillow（内存渲染，不落盘）；`apply_patch`（仅写本报告）。尝试调用 `pdfinfo`，环境中不可用，未据此得出任何内容结论。
- 可观察 trace：当前任务 transcript 中的工具调用级 trace 可观察；App/OS 提供的独立文件访问审计、可验证 path allowlist 均 `unavailable`。因此隔离性质仍是 invocation 所述 `procedural_blinding`，不是技术性 read-only/allowlist 隔离。

> 页码均指 PDF 物理页（也与正文印刷页码一致）。下文每项实质判断均给出章节/图表和短定位文本。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] ToolLLM 不是单一算法，而是把工具学习链路改成“API 收集与过滤 → ChatGPT 生成指令 → ChatGPT+DFSDT 标注真实 API 调用路径 → 监督微调 ToolLLaMA → API 检索 → ToolEval 评估”。定位：p. 2–3，Fig. 1，§1；短定位词：“three phases”“API retriever”“ToolEval”。
- [AUTHOR_FACT] 最明确的计算级改变是：将 CoT/ReACT 的单一路径、不可回撤决策，替换为带回撤/重启的深度优先决策树搜索（DFSDT）。每个状态下模型基于历史动作和真实 API 返回生成下一动作；若当前分支无望，则调用 give-up/restart，回到分叉状态，并把先前子节点动作提供给模型，要求生成不同动作。定位：p. 5–6，Fig. 4，§2.3；p. 22–23，§A.8；短定位词：“expand a new node”“different from all of them”。
- [AUTHOR_FACT] 实际实现并非经典 DFS 的“生成多个子节点、排序再扩展”，而是省略子节点排序、采用 pre-order traversal；无回撤时退化为 ReACT。定位：p. 13–14，§A.4；短定位词：“skip the sorting process”“degrades to ReACT”。
- [AUTHOR_FACT] DFSDT 同时用于训练数据的解路径标注和推理策略；ToolLLaMA 虽由 DFSDT 产生的数据训练，但推理时既可用 ReACT，也可用 DFSDT。定位：p. 6，§2.3；p. 14，§A.4。
- [READER_INTERPRETATION] 因而核心机制不是改变单次 LLM forward 的网络结构，而是改变 forward 之间的控制流、可见历史和分支选择；模型参数层面的改变主要来自 ToolBench 上的监督微调。依据：p. 6，§2.3；p. 7、13，§3.2、§A.3。

## 2. 输入、输出、可用信息与干预时点

| 环节 | 输入与可用信息 | 输出 | 干预时点与定位 |
|---|---|---|---|
| 指令生成 | [AUTHOR_FACT] 抽样 API 文档、3 个随机 in-context seeds；单工具 seeds 共 12 个，多工具 seeds 共 36 个。 | 指令与相关 API 对，初始近 20 万条。 | 生成数据时一次性干预。p. 4–5，§2.2；p. 16–22，§A.7；定位词：“three in-context seed examples”。 |
| 解路径标注 | [AUTHOR_FACT] 原始指令、抽样 API 的文档/函数字段、此前 `action,response` 历史；分支扩展时额外提供此前候选动作。API 返回是真实在线调用结果。 | 多轮 Thought、API 名、参数、API 响应，最终 `give_answer` 或 `give_up_and_restart`；仅保留 pass 路径，共 126,486 对。 | 每轮 API 调用前选择动作；分支失败后触发回撤/重启。p. 5–6，§2.3；p. 22–23，§A.8。 |
| API 响应处理 | [AUTHOR_FACT] API 响应若超过 1024 tokens，按 ChatGPT 预先生成的 schema 删除不重要字段；仍超长则只保留前 1024 tokens。 | 压缩后的 observation。 | 每次长响应进入后续推理之前。p. 13，§A.2；定位词：“only retain the first 1024 tokens”。 |
| ToolLLaMA 训练 | [AUTHOR_FACT] ChatGPT 风格的多轮输入/输出；因作者不知道 ChatGPT 如何组织 function-call 字段，ToolLLaMA 将函数信息直接拼入 prompt。LLaMA-2 7B 上训练 2 epochs，最大长度 8192。 | 预测下一动作/最终回答的 ToolLLaMA。 | 参数训练阶段。p. 7，§3.2；p. 13，§A.3。 |
| 主实验推理 | [AUTHOR_FACT] 用户指令，加上 oracle ground-truth API 集；唯一例外是 ToolLLaMA-DFSDT-Retriever，接收检索器 top-5 API。 | 多轮 API 调用路径与最终回答/放弃。 | 推理前选择 API 集；每步由 ReACT 或 DFSDT 控制。p. 7–8，§3.2，Table 4。 |
| ToolEval | [AUTHOR_FACT] Pass 输入为指令与一条路径，输出 Pass/Fail/Unsure；Win 输入为同一指令的两条路径，输出 win/lose/tie。每例调用 ChatGPT 至少 4 次，多数投票。 | pass rate 与 win rate。 | 整条执行路径完成后。p. 6，§3.1；p. 14–15，§A.5。 |

- [READER_INTERPRETATION] “可用信息”在不同模型之间并不完全同构：ChatGPT 使用原生 function field，ToolLLaMA 使用串接 prompt；不同模型也可能具有不同上下文窗口和函数调用实现。定位：p. 2，§1；p. 13，§A.3。
- [OPEN_QUESTION] 主实验没有给出每个模型完全统一的 token 上限、单路径最大 tool-call 数、DFSDT 分支数/深度和停止预算的完整表，因此无法仅由本文确认所有模型在每个例子上的有效计算预算相同。定位：p. 6，§3.1 仅称 “limited budgets”；p. 7，§3.1 仅对 DFSDT 与 ReACT@N 说明总成本对齐。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 主实验 Table 4 中，按六个 ToolBench 切分的平均值，最强外部模型基线是 GPT-4+DFSDT：Pass 71.1、Win 70.4。ToolLLaMA+DFSDT 为 66.7/60.0，ToolLLaMA+DFSDT-Retriever 为 67.3/63.1，ChatGPT+DFSDT 为 64.8/64.3。定位：p. 8，Table 4，§3.2。
- [READER_INTERPRETATION] 对“ToolLLaMA 是否学会工具使用”最接近的组合基线是同为 oracle API、同为 DFSDT 控制的 ChatGPT+DFSDT 与 GPT-4+DFSDT；对“DFSDT 是否优于线性推理”最接近的是 ReACT@N，而不是只跑一次的 ReACT。依据：p. 7，Table 3；p. 8，Table 4。
- [AUTHOR_FACT] ReACT@N 将 ReACT 重复运行到总 OpenAI API 成本与 DFSDT 相同；ChatGPT 上平均 Pass 为 ReACT 35.3、ReACT@N 44.5、DFSDT 63.8。定位：p. 7，Table 3，§3.1；定位词：“total costs reach the same level”。
- [AUTHOR_FACT] API 检索实验中更强的传统基线是 OpenAI `text-embedding-ada-002`，其平均 NDCG@1/@5 为 49.6/45.4；BM25 为 18.5/17.0；作者的 BERT-base dense retriever 为 78.0/84.9。定位：p. 7，Table 2，§3.1。
- [AUTHOR_FACT] OOD APIBench 的最强对照取决于检索条件：Gorilla-RS+Oracle 在三域 AST 与 hallucination 上总体强于 ToolLLaMA+Oracle；例如 TorchHub 为 93.01 AST、6.99 hallucination，对应 ToolLLaMA+Oracle 的 85.88、14.12。定位：p. 9，Table 5，§3.3。
- [READER_INTERPRETATION] 因此“ToolLLaMA 与 ChatGPT 相当”只适用于 Table 4 的特定 ToolBench/ToolEval/策略组合；不能外推为对最强 GPT-4 基线或 APIBench 最强 Gorilla-RS+Oracle 的全面持平。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] Table 4 除 `ToolLLaMA-DFSDT-Retriever` 外全部使用 oracle ground-truth API；Retriever 版本改为 top-5 检索 API，且其结果有时更高。定位：p. 7–8，§3.2，Table 4；定位词：“all methods use the oracle API retriever”。
- [READER_INTERPRETATION] oracle API 会把“从 16k API 中发现工具”和“在已给 API 上规划”混在不同实验条件中；Table 4 的大多数结果主要衡量后者，而非端到端检索能力。
- [AUTHOR_FACT] DFSDT 比单次 ReACT 消耗更多 OpenAI API calls；作者只在 ChatGPT 的 Table 3 以 ReACT@N 做总成本层面的对齐。定位：p. 7，§3.1；p. 13–14，§A.4。
- [READER_INTERPRETATION] Table 4 中“DFSDT 普遍更强”可能同时包含搜索算法与更多 tool/model calls 的增益；Table 3 的 ReACT@N 缓解但没有消除“自适应树搜索 vs 多次独立重启”的计算结构差异。
- [AUTHOR_FACT] ToolLLaMA 的训练上下文扩为 8192；数据生成使用 `gpt-3.5-turbo-16k`；ChatGPT 原生 function-call 字段与 ToolLLaMA 的 prompt 串接不同。定位：p. 2，§1；p. 7，§3.2；p. 13，§A.3。
- [READER_INTERPRETATION] 模型家族、上下文长度、function-call 序列化和 prompt 接口均未做严格同构控制，因而不能把跨模型差异全部归因于 ToolBench 微调或 DFSDT。
- [AUTHOR_FACT] 训练指令、解路径和自动评估都由 ChatGPT 深度参与；Win Rate 还以 ChatGPT-ReACT 为比较锚点。定位：p. 2–3，§1；p. 6，§3.1；p. 8，Table 4。
- [READER_INTERPRETATION] 同一教师/生成器/评估器的重用可能带来风格或偏好耦合；87.1%/80.3% 人机一致率证明相关性较高，但不足以排除这种偏差。定位：p. 15，§A.5。
- [AUTHOR_FACT] ToolEval 的 Win 规则奖励“尝试更多潜在有用 API”，而 DFSDT 的设计恰好扩展更多路径；Pass 规则在若干可解/不可解情形中也会把充分尝试后的放弃或拒答记为 Pass。定位：p. 14–15，§A.5；定位词：“greater number of APIs is better”。
- [READER_INTERPRETATION] 这套 metric 定义可能结构性偏好探索型策略，因此 Pass/Win 提升不完全等价于最终答案事实正确性提升。
- [OPEN_QUESTION] 论文未报告在统一 token、统一有效 API 响应、统一 tool-call 次数、统一序列化 prompt、统一非 ChatGPT evaluator 下重跑 Table 4 的结果，故无法从本文消除上述替代解释。

## 5. 明示限制、负向结果与未测试边界

### 作者明示或直接报告

- [AUTHOR_FACT] RapidAPI 会随时间变化，且一条指令可能有无限多正确路径，作者认为固定 ground-truth solution path 不可行。定位：p. 6，§3.1；定位词：“temporal variability”“infinite potential solution paths”。
- [AUTHOR_FACT] ToolEval 与人工的一致率并非 100%：Pass 87.1%，Win 80.3%；作者还明确指出人类专家也常不同意，并称公平工具评估仍“有很长的路”。定位：p. 15，§A.5。
- [AUTHOR_FACT] 长 API 响应可能因有限上下文无法直接输入；压缩后仍超 1024 tokens 时只保留前 1024 tokens。定位：p. 13，§A.2。
- [AUTHOR_FACT] 经典 DFS 的子节点排序需要约 `O(n log n)` 次 LLM/API 比较，成本过高；作者据经验省略排序。定位：p. 13–14，§A.4。
- [AUTHOR_FACT] APIBench 不测试 prompts 不含任何 API 描述的 zero-shot setting，因为三个测试域的 API 在训练中从未出现。定位：p. 15，§A.6。
- [AUTHOR_FACT] Vicuna 与 Alpaca 在 Table 4 全部切分的 Pass/Win 均为 0。定位：p. 8，Table 4，§3.2。
- [AUTHOR_FACT] 多工具检索更难：作者检索器的 NDCG@1 从 I1 的 84.2 降到 I2 的 68.2（I3 为 81.7）；作者也明确称 I1 比 I2/I3 更简单。定位：p. 7，Table 2，§3.1。
- [AUTHOR_FACT] APIBench 上 ToolLLaMA+Our Retriever 在 TensorHub 同时弱于 Gorilla-RS+BM25（AST 40.59 vs 41.90；hallucination 6.48 vs 2.77）；ToolLLaMA+Oracle 也没有超过 Gorilla-RS+Oracle。定位：p. 9，Table 5，§3.3。

### 读者据实验设计识别的边界

- [READER_INTERPRETATION] 训练数据只保留 DFSDT 已通过的路径，且 API 从 53,190 过滤到 16,464；这提高可用性，但形成“可调用 API + 已成功路径”的选择边界。定位：p. 4，§2.1；p. 6，§2.3；p. 13，§A.1。
- [READER_INTERPRETATION] 指令由 API 组合反向合成，并被明确要求每题调用 2–5 个 API、至少 30 词；这与自然用户流量的分布可能不同。定位：p. 16–17、22，§A.7。
- [OPEN_QUESTION] 未测试真实用户自发请求、长期 API 漂移后的鲁棒性、恶意/不可信 API 响应、权限与隐私风险、调用副作用、失败后的状态回滚，以及大于当前搜索预算的长程任务。
- [OPEN_QUESTION] 文中没有独立 safety/limitations 实验，也没有报告响应压缩的信息保真定量指标；“human evaluation 保留重要信息”未给出样本量和一致率。定位：p. 13，§A.2。

## 6. 可抽取的 Operator 与真实可记录的 Failure

以下仅作论文内机制/失败证据的独立核源，不生成 Candidate，也不作价值裁决。

### Operator

- [AUTHOR_FACT] **层级约束 API 组合采样**：用 RapidAPI category/collection 的局部相关性，采 2–5 个工具、每工具至多 3 个 API，生成 I2/I3 多工具指令。定位：p. 5，§2.2，Fig. 3。
- [AUTHOR_FACT] **带失败回撤的 DFSDT 控制器**：保留状态与此前子动作，在 `give_up_and_restart` 后生成不同分支；采用 preorder DFS、成功即停。定位：p. 6，§2.3；p. 13–14，§A.4；p. 22–23，§A.8。
- [AUTHOR_FACT] **真实 observation 驱动的多轮路径标注**：动作格式含 thought/API/parameters，下一步读取真实 API response。定位：p. 5–6，§2.3。
- [AUTHOR_FACT] **API 响应 schema 压缩器**：按 API 固定格式删除低价值键，并设置 1024-token 截断。定位：p. 13，§A.2。
- [AUTHOR_FACT] **指令—API 双塔检索器**：Sentence-BERT/BERT-base 对指令和文档编码，以正/负 API 做对比学习，推理取 top-5。定位：p. 6–8，§3.1–3.2，Table 2。
- [AUTHOR_FACT] **多次判决+多数投票的路径 evaluator**：Pass/Win 各调用 ChatGPT 至少 4 次，再聚合。定位：p. 14–15，§A.5。

### Failure

- [AUTHOR_FACT] **线性轨迹错误传播**：CoT/ReACT 的错误动作会继续传播，出现错误调用、幻觉 API 或循环。定位：p. 6，§2.3；定位词：“error propagation”。
- [AUTHOR_FACT] **单路径探索不足**：CoT/ReACT 只探索一个方向，复杂任务 pass 低；同成本 ReACT@N 仍低于 DFSDT。定位：p. 6–7，§2.3、§3.1，Table 3。
- [AUTHOR_FACT] **通用对话 SFT 不迁移到工具域**：Vicuna/Alpaca 在该评测中全为 0。定位：p. 8，Table 4。
- [AUTHOR_FACT] **多工具检索退化**：I2 的 NDCG 显著低于 I1；作者明确解释多工具检索更难。定位：p. 7，Table 2。
- [AUTHOR_FACT] **自动评估不完全一致**：相对人工仍有 12.9 个百分点的 Pass 不一致和 19.7 个百分点的 Win 不一致。定位：p. 15，§A.5（由作者报告的一致率直接换算）。
- [AUTHOR_FACT] **OOD 最强设定未胜**：在 APIBench 的 Gorilla-RS+Oracle 对照下，ToolLLaMA+Oracle 三域均未取得更优的 AST/hallucination 组合。定位：p. 9，Table 5。
- [READER_INTERPRETATION] **搜索/评估耦合失败风险**：Win 规则奖励更多 API 探索，可能把更高搜索成本误当作更高答案质量。定位：p. 15，§A.5；p. 7，§3.1。
- [READER_INTERPRETATION] **成功路径选择偏差**：只保留 pass 路径会隐藏 DFSDT 无法标注的任务类型和失败频率；126,486 是成功保留量，不是对全部近 20 万指令的无条件成功证明。定位：p. 5–6，§2.2–2.3。

## 7. 判断—页码/章节/图表/短定位索引

上文已经逐项附定位。为便于 reconciliation，核心索引如下：

| 判断簇 | 主要位置 | 短定位文本 |
|---|---|---|
| 总体链路 | p. 2–3，Fig. 1，§1 | “three phases” |
| DFSDT 改变控制流 | p. 5–6，Fig. 4，§2.3；p. 13–14，§A.4；p. 22–23，§A.8 | “expand a new node” |
| Retriever | p. 6–7，Table 2，§3.1 | “NDCG@1 and NDCG@5” |
| 同成本推理基线 | p. 7，Table 3，§3.1 | “ReACT@N” |
| ToolBench 主结果与 oracle 条件 | p. 7–8，Table 4，§3.2 | “ground-truth (oracle) APIs” |
| OOD 结果 | p. 8–9，Table 5，§3.3 | “OOD generalization” |
| 响应压缩 | p. 13，§A.2 | “first 1024 tokens” |
| ToolLLaMA prompt/训练差异 | p. 13，§A.3 | “concatenate this information” |
| ToolEval 规则与一致率 | p. 14–15，§A.5 | “Pass, Fail, and Unsure” |
| 未测试 APIBench zero-shot | p. 15，§A.6 | “do not consider the zero-shot setting” |
| 合成指令约束 | p. 16–22，§A.7 | “two to five APIs” |

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 已对 23/23 个物理页逐页解析文本，并在内存中逐页渲染可视页面；另外单页放大核对了标题页、Table 2/3（p. 7）、Table 4（p. 8）、Table 5（p. 9）及 Table 6/附录提示页（p. 16）。
- [READER_INTERPRETATION] 未发现文本层与可视 PDF 在章节顺序、正文主张、页码、图表标题或关键数值上的语义冲突。
- [AUTHOR_FACT] 可观察的解析问题集中在双栏/表格：`pypdf` 会把 Table 1–6 的列、页脚页码与正文交错输出，正文个别词的空格也丢失。报告中的表格数值据可视表格与对应正文交叉核对，不使用串列后的原始文本顺序推断列归属。
- [OPEN_QUESTION] 由于本任务没有做 OCR 与字体对象级逐字比对，不能声称所有字符字形 100% 一致；但对本报告所引用的机制、边界和数值，未观察到可影响结论的冲突。

## 独立读者收束

- [READER_INTERPRETATION] 本文最扎实的可复用机制证据是“失败可回撤、先前子动作可见、差异化分支扩展”的 DFSDT 控制流，以及与 ReACT@N 的成本近似对照。
- [READER_INTERPRETATION] 最需要 reconciliation 保留的限定是：Table 4 大量使用 oracle API，DFSDT 与 ReACT 的计算预算并非在所有模型上完整同构，且数据生成、训练教师与评估器都高度依赖 ChatGPT。
- 本报告不包含论文打分、Candidate 价值判断、正式 Card 或 Reviewer 裁决。
