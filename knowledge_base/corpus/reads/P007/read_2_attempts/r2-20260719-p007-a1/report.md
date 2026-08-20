# P007 独立二读报告

## 0. Provenance 与读边界

- [AUTHOR_FACT] 本报告对应 frozen invocation snapshot：`r2-20260719-p007-a1/invocation.md`，Attempt ID 为 `r2-20260719-p007-a1`；canonical metadata 为 ICLR 2025 论文 *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*。（定位：invocation，`Independent read-2 invocation` / `Canonical metadata`）
- [AUTHOR_FACT] 实际核验 PDF 的 SHA-256 为 `e2d45d573e1fce753ead1a44cc468ad386dd384e2668450d0a9c0e2c7920ada0`，与 invocation manifest 一致；PDF 共 53 个物理页。（定位：invocation 的 `PDF SHA-256`；本轮本地哈希与页数检查）
- [READER_INTERPRETATION] 本次是 fresh 独立核源：未读取 read_1、Cards、其他读者报告、blind query，未联网，未生成 Card，未评价 Candidate，也未运行科研 Reviewer。（定位：invocation，`Read boundary`、`Exact request`；本轮自我可观察工具调用）
- [AUTHOR_FACT] 实际模型为 GPT-5 系 Codex；精确部署版本在本会话不可见，记为 `unknown`。canonical task/thread 为 `/root/p007_second_read`。（定位：本会话可见运行身份；精确版本不可见）
- [AUTHOR_FACT] App 未提供可验证的文件级 allowlist，因此隔离性质是 `procedural_blinding`，不是技术 read-only 隔离。（定位：invocation，`Read boundary`）

## 1. 方法究竟改变哪一步计算？

- [READER_INTERPRETATION] 这篇论文的主要贡献是改变**代理评测计算**，不是提出一个提升代理能力的新 agent update rule：它把“用户一次性给齐信息、代理独自操作环境”的静态评测，改成工具—代理—模拟用户的动态闭环，并把领域政策放入代理可用上下文。（定位：PDF p.1，§1，短定位文本：`interact with ... users and programmatic APIs`；PDF p.3，§3，短定位文本：`POMDP`）
- [AUTHOR_FACT] 单任务被形式化为 POMDP；状态分成数据库状态与用户状态，动作分成数据库 API 动作与对用户的自然语言动作。数据库转移由 Python 函数确定性执行，用户转移通过 LM 采样而具有随机性。（定位：PDF p.3，§3，短定位文本：`S = Sdb ⊗ Suser`、`transition ... deterministic`；PDF p.4，§3，短定位文本：`transition Tuser ... is stochastic`）
- [AUTHOR_FACT] 终局奖励改为 `r = r_action × r_output ∈ {0,1}`：一部分比较最终数据库是否等于唯一标注目标数据库，另一部分检查面向用户的回复是否包含必要输出。（定位：PDF p.4–5，§3 `Reward`，Figure 2d；短定位文本：`final database is identical`、`contain all necessary information`）
- [AUTHOR_FACT] 论文新增 `pass^k`（文中写作 pass-hat-k）来估计同一任务的 k 次 i.i.d. 试验是否**全部**成功，并与至少一次成功的 `pass@k` 对照；默认主指标为 `pass^1 = E[r]`。（定位：PDF p.5，§3 `Pass^k metric`，公式；短定位文本：`all k i.i.d. task trials are successful`）
- [READER_INTERPRETATION] 因而“改变的计算步骤”可分成三层：交互式轨迹生成、终局状态/输出判定、跨重复试验的一致性聚合；论文没有在被测模型参数上做训练更新。（定位：PDF p.3–5，§3；PDF p.7，§5 `Methods`）

## 2. 输入、输出、可用信息与干预时点分别是什么？

- [AUTHOR_FACT] 代理输入包括：领域政策（FC 设置中作为 system prompt）、可调用工具及其定义、此前代理—用户对话、每次工具调用返回的数据库观察；代理不能直接看到数据库，只能经 API 读写。（定位：PDF p.2，Figure 1a；PDF p.3，§3 `Databases and APIs`；PDF p.7，§5 `Methods`；短定位文本：`system prompt is set to be the domain policy`）
- [AUTHOR_FACT] 代理看不到 task annotation；该标注只用于用户模拟和评测。用户模拟器输入为隐藏的用户 instruction 和迄今完整的代理—用户对话，但看不到代理与 API 工具之间的交互历史。（定位：PDF p.4，§3，Figure 2d；短定位文本：`Task annotation is not visible to the agent`、`cannot see ... agent and API tools`）
- [AUTHOR_FACT] 每个 task instance 的隐藏部分包含用户身份、意图、偏好以及 ground-truth 写动作，并可选包含用户问题的 ground-truth outputs；作者声称 instruction 被写成在领域政策下只产生一个结果。（定位：PDF p.4，§3 `Task instances`，Figure 2d；短定位文本：`guarantees only one possible outcome`）
- [AUTHOR_FACT] 代理每轮可输出自然语言用户响应或单个工具调用，并可在会话任意时点调用工具；用户输出 `###STOP###` 时 episode 结束，随后使用最终数据库和代理对用户消息计算奖励。（定位：PDF p.4，§3 `User simulation` / `Task instances`；短定位文本：`call tools at any point`、`episode finishes`）
- [AUTHOR_FACT] 主实验把每个任务限制为最多 30 个 agent actions（工具调用或用户回复）；代理温度为 0.0，用户温度为 1.0；主表每任务至少运行 3 次。（定位：PDF p.7，§5 `Methods`；短定位文本：`at most 30 agent actions`、`at least 3 trials per task`）
- [READER_INTERPRETATION] 干预点有两类：代理在会话内通过提问、告知与 API 写动作改变轨迹/数据库；评测器只在 episode 终点判定单次成功，再在重复试验后计算 pass^k。（定位：PDF p.3–5，§3；PDF p.7，§5）

## 3. 最强基线与最接近组合基线是什么？

- [AUTHOR_FACT] Table 2 的最强被测组合是 `gpt-4o + native function calling`：retail 61.2、airline 35.2、加权平均 48.2；表注说明除 Llama-3 使用 text-ReAct 外，其余为 function calling，平均值按 domain 加权而非按任务数加权。（定位：PDF p.7，Table 2；短定位文本：`gpt-4o 61.2 35.2 48.2`、`weighted by domains`）
- [READER_INTERPRETATION] 对“agent 接口/推理格式”贡献最接近的组合基线是同模型下的 FC、text-ReAct 与 Act-only；Figure 3 在 τ-retail 上显示 FC 一致优于文本格式方法，ReAct 又优于 Act-only。（定位：PDF p.7，Figure 3，§5.1 `Method comparison`；短定位文本：`function calling consistently outperforms`）
- [AUTHOR_FACT] 最接近的政策信息消融是从 FC agent system prompt 中删除 domain policy：gpt-4o 从 61.2→56.8（retail）、33.2→10.8（airline）；gpt-3.5 从 20.0→14.5、10.8→9.6。（定位：PDF p.8–9，Table 3，§5.2；短定位文本：`policy is not provided`）
- [AUTHOR_FACT] 最接近的用户模拟组合对照固定 gpt-4o FC agent，比较 vanilla `llm`、`react`、`verify`、`reflection`；平均 3 次 airline 试验中 reflection 的 Acc 最高（0.406），但四种策略相近。（定位：PDF p.9，Table 4，§5.3；短定位文本：`reflection performing the best`）
- [OPEN_QUESTION] 论文没有给出一个同时严格匹配模型、prompt tokens、工具调用额度、推理 token 和用户采样轨迹的“组合基线”；因此 FC vs ReAct/Act 只能视作最接近而非完全受控的接口比较。（定位：PDF p.7，§5 `Methods` / Figure 3；原文只给 30 actions 上限与温度，未报告上述逐项匹配）

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] Table 2 明确更换了 agent model，因此跨行结果本来就同时反映模型能力差异；Llama-3 还因不支持原生 FC 而使用 text-ReAct，接口也不同。（定位：PDF p.7，Table 2 表注与 §5 `Models`；短定位文本：`except Llama-3 via text-ReAct`）
- [READER_INTERPRETATION] Figure 3 的 FC、ReAct、Act 比较同时改变了原生 tool-call 通道、输出格式与提示：ReAct 被要求生成 `Thought ... Action ...`，Act 只生成 action，而 FC 由模型原生决定用户消息或工具调用。因此差异可能包含 prompt/interface/tool-call 适配效应，不能纯归因于“显式 reasoning”。（定位：PDF p.7，§5 `Methods`；短定位文本：`text-formatted ReAct`、`natively supported function calling`）
- [AUTHOR_FACT] 论文仅统一了 30 个 agent actions 上限，并未报告各模型/方法实际输入 token、输出 token、tool-call 数的配平；成本分析只给出 gpt-4o FC + gpt-4 用户在 retail 的单项估算，并指出 95.9% agent 价格来自输入。（定位：PDF p.7，§5 `Methods`；PDF p.8，§5.1 `Cost analysis`；短定位文本：`95.9% / 4.1%`）
- [OPEN_QUESTION] 由于没有逐方法 token/tool-call/latency 配平数据，不能排除上下文长度、原生函数调用训练、API 版本或实际工具调用次数对排名的贡献。（定位：PDF p.7–8，§5；原文未给该控制）
- [AUTHOR_FACT] ground-truth task annotation 对代理隐藏，统一的终局 oracle 用于奖励计算；从论文描述看，没有证据表明某一 agent baseline 获得了额外的 ground-truth oracle。（定位：PDF p.4，Figure 2d，§3；短定位文本：`used only for user simulation and evaluation`）
- [READER_INTERPRETATION] oracle 仍可能通过数据构造产生间接偏置：作者反复运行 gpt-4-turbo FC 来润色 user instruction，且在讨论中承认 task curation 存在 implicit bias。（定位：PDF p.5，§4 Stage III；PDF p.10，§6；短定位文本：`use the gpt-4-turbo FC agent to tune`）
- [AUTHOR_FACT] 同一任务的用户 prompt 与数据库转移固定，主要随机性来自用户/代理消息采样；用户温度 1.0、代理温度 0.0。（定位：PDF p.5，§3 `Pass^k metric`；PDF p.7，§5 `Methods`）
- [OPEN_QUESTION] 原文没有拆分 pass^k 下降中“用户模拟随机性”和“代理自身非确定性/API 非确定性”的份额；因此不能从 pass^k 曲线单独定位不一致性的来源。（定位：PDF p.5，§3；PDF p.7–8，Figure 4，§5.1）

## 5. 作者明示限制、负向结果和未测试边界是什么？

- [AUTHOR_FACT] 作者明确承认 `r=1` 可能只是成功的必要而非充分条件：代理即使未取得显式用户确认就执行 return，也可能通过当前 rule-based reward。（定位：PDF p.5，§3 `Reward`；短定位文本：`necessary but not sufficient`）
- [AUTHOR_FACT] 用户模拟限制包括 instruction 的 typo/ambiguity、instruction 不含全部领域知识，以及模拟 LM 的推理、计算、长上下文记忆或指令对齐能力有限。（定位：PDF p.9–10，§6 `Directions for improvement`；短定位文本：`typos or ambiguities`、`limited capacity`）
- [AUTHOR_FACT] 作者提出但未在当前版本完成的改进包括：更系统的唯一结果检查、更复杂的领域政策、更多成功指标（例如用 LM 检查规则是否遵循）、替代数据策划与用户模拟方法。（定位：PDF p.10，§6；短定位文本：`More evaluation metrics can be added`）
- [AUTHOR_FACT] 数据策划需要困难的人工标注，并因使用 gpt-4-turbo FC 调整用户 system prompt 而存在 implicit bias。（定位：PDF p.10，§6；短定位文本：`manual annotation process ... difficult`、`implicit bias`）
- [AUTHOR_FACT] 当前仅构造 retail 115 题与 airline 50 题；域本身是现实域的简化，医疗、税务、法律等更复杂域被列为未来方向。（定位：PDF p.6，Table 1，§4.1–4.2；短定位文本：`simplified compared to real-world domains`）
- [AUTHOR_FACT] 小模型 7B/13B 未测试；self-reflection 被认为在一次真实客服机会中不现实，planning 被认为可能过慢，因此未作为主要 agent 方法评测。（定位：PDF p.7，§5 `Models` / `Methods`；短定位文本：`We do not test small models`、`might be too slow`）
- [AUTHOR_FACT] 负向结果包括：给 FC agent 增加 `think` function 没有提升；text-ReAct/Act 落后于 native FC；gpt-4o retail 的 pass^8 降到 25% 以下；最强模型在 airline 也只到 35.2% pass^1。（定位：PDF p.7–8，Figure 3、Figure 4、Table 2，§5.1；短定位文本：`did not boost performance`、`pass^8 drops to <25%`）
- [AUTHOR_FACT] 在 115 条 gpt-4o FC retail 轨迹的一次抽样中，40 条失败；其中 4 条归因于 user instruction typo/ambiguity 并被修复，剩余 36 条被人工归因于 agent。（定位：PDF p.8，§5.2 `Failure breakdown`，Figure 5）
- [AUTHOR_FACT] 对 4 种 user strategy 的失败轨迹抽样审查显示，用户模拟导致的错误均不超过 4%；但该结论基于每种策略从失败轨迹中随机抽 50 条、airline 全域 3 次试验。（定位：PDF p.9，Table 4，§5.3）
- [OPEN_QUESTION] 论文未用真实人类用户验证模拟对话的外部效度，也未验证简化政策/数据库下的排名能否迁移到真实客服系统。（定位：PDF p.2–4，§1/§3 明示 LM-simulated users；PDF p.10，§6 仅讨论模拟器限制）

## 6. 哪些内容可抽取为 Operator，哪些是真实可记录的 Failure？

### 6.1 可核源的 Operator

- [READER_INTERPRETATION] `Interactive TAU loop`：把隐藏数据库、API、政策、LM 用户与 agent 组成逐轮闭环，使信息收集与授权在轨迹中发生。（定位：PDF p.2，Figure 1；PDF p.3–4，§3）
- [READER_INTERPRETATION] `Policy-conditioned tool agent`：以领域政策约束 agent，并只允许其经工具观察/修改数据库；部分约束由 API 检查，部分必须由 agent 自己遵守。（定位：PDF p.3，§3 `Domain policy`；短定位文本：`Some restrictions are implemented ... and others not`）
- [READER_INTERPRETATION] `Unique-goal end-state evaluator`：人工保证唯一目标结果，再用最终数据库相等性与必要输出检查替代轨迹级人工打分。（定位：PDF p.4–6，Figure 2d，§3 `Reward`、§4 Stage III、§4.2 `Faithful rule-based evaluation`）
- [READER_INTERPRETATION] `Repeated-trial reliability aggregator`：以 pass^k 聚合同一语义任务在随机对话变化下连续成功的概率。（定位：PDF p.5，公式；PDF p.7，Figure 4）
- [READER_INTERPRETATION] `Policy-removal diagnostic`：移除 system-prompt policy，观察性能降幅以探测模型是否实际利用领域规则。（定位：PDF p.8–9，Table 3，§5.2）
- [READER_INTERPRETATION] `Manual failure taxonomy`：从失败轨迹中人工区分错误参数/信息、错误决策、复合请求部分解决，用于定位数据库推理、规则遵循与长期跟踪问题。（定位：PDF p.8–9，Figure 5、Figure 6，§5.2）

### 6.2 可记录的 Failure

- [AUTHOR_FACT] `Evaluator false positive / coverage gap`：未获显式确认却执行写动作，仍可能得到 `r=1`。（定位：PDF p.5，§3 `Reward`）
- [AUTHOR_FACT] `Wrong argument` 占 36 条 agent failures 的 33.3%；`Wrong info` 占 22.2%，二者合计约 55%。（定位：PDF p.8，Figure 5 可视图例与环图；§5.2 `Failure 1`）
- [AUTHOR_FACT] `Wrong decision` 占 25.0%，表现为未理解或未遵守领域规则而选错工具类型。（定位：PDF p.8，Figure 5；§5.2 `Failure 2`）
- [AUTHOR_FACT] `Partially resolve` 占 19.4%，表现为复合请求只完成一部分；Figure 6 还显示 ground-truth 写动作越多，retail 任务越难。（定位：PDF p.8–9，Figure 5、Figure 6；§5.2 `Failure 3`）
- [AUTHOR_FACT] Task 0 展示“一次 exchange”规则遗漏：agent 先交换键盘，导致订单状态改变，第二个恒温器交换报 `non-delivered order`。（定位：PDF p.25–30，§C.2.1；短定位文本：`only one exchange per order is possible`）
- [AUTHOR_FACT] Task 7 展示错误参数：用户要求更暗且电源偏好 AC>battery>USB，agent 最终选择了 medium brightness 的 AC 灯，而标注目标是 low brightness 的 AC 灯。（定位：PDF p.31–36，§C.2.2；短定位文本：`fails ... to find the desired exchange item option`）
- [AUTHOR_FACT] Task 42 展示复合请求部分解决：agent 只修正含 jigsaw 的订单地址和用户地址，没有修正另一个 pending order 的错误地址。（定位：PDF p.37–44，§C.2.3；短定位文本：`only fixes the jigsaw order address`）
- [AUTHOR_FACT] 较弱 agent 会幻觉不存在的 ID：每个 retail task 的此类 tool calls，gpt-4o FC 为 0.46，gpt-3.5 FC / Act 为 2.08 / 6.34。（定位：PDF p.8，§5.2 `Failure 1`）
- [READER_INTERPRETATION] 上述 Failure 可以作为核源事实记录，但这些例子与人工比例只描述当前数据、模型和抽样，不应自动外推成普遍因果结论。（定位：PDF p.8–9，§5.2 的抽样范围；PDF p.31–44，附录例子）

## 7. 页码、章节、图表和短定位文本如何对应？

- [AUTHOR_FACT] 机制定义集中在 PDF p.3–5 的 §3：POMDP、数据库/API、用户模拟、任务实例、奖励和 pass^k；关键图为 Figure 2，关键公式在 p.5。（短定位文本：`Tool-Agent-User Interaction`、`r = r_action × r_output`）
- [AUTHOR_FACT] 构造与规模集中在 PDF p.5–6 的 §4 和 Table 1；更完整 API/政策见 p.12–19 的 Appendix B 与 Table 5。（短定位文本：`Manual task annotation and validation`、`Retail policies`、`Airline policies`）
- [AUTHOR_FACT] 主模型/方法结果集中在 PDF p.7–9 的 §5：Table 2、Figure 3、Figure 4、Figure 5、Table 3、Figure 6、Table 4。（短定位文本：`MAIN RESULTS`、`RESEARCH CHALLENGE ANALYSIS`、`USER SIMULATION METHODS`）
- [AUTHOR_FACT] 作者限制集中在 PDF p.9–10 的 §6；额外按任务成功率结果见 PDF p.12 的 Figure 7。（短定位文本：`Directions for improvement`、`Average Rewards by Task`）
- [AUTHOR_FACT] 三个失败实例分别位于 PDF p.25–30（§C.2.1）、p.31–36（§C.2.2）、p.37–44（§C.2.3）；成功 airline 轨迹位于 p.48–53（§D.2）。（短定位文本：`WRONG DECISION`、`WRONG ARGUMENT`、`PARTIALLY SOLVE COMPOUND REQUESTS`、`SUCCESSFUL TRAJECTORY`）
- [READER_INTERPRETATION] 本报告其余每项判断已在条目内嵌物理 PDF 页码、章节/图表及短定位文本；页码指 PDF viewer 的 1–53 物理页，恰与印刷页码一致。（定位：逐页可视核对）

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 已逐页对照 53 个物理页的解析文本与可视渲染；未发现缺页、页序错乱、整页渲染失败，正文、表格、图、公式、政策代码和附录轨迹均可见。（定位：PDF p.1–53，逐页解析与逐页 fit-to-page 可视检查）
- [READER_INTERPRETATION] 未发现会改变论文结论的文本—视觉语义冲突，但解析文本会丢失二维关联。最重要的例子是 Figure 5：线性抽取先列百分比再列标签，无法安全配对；可视图明确映射为 Wrong argument 33.3%、Wrong info 22.2%、Wrong decision 25.0%、Partially resolve 19.4%。（定位：PDF p.8，Figure 5）
- [AUTHOR_FACT] Figure 3/4/6/7 的柱、曲线与任务难度分布不能由纯文本完整恢复；表格数值和图注可抽取，但曲线形状必须以可视 PDF 为准。（定位：PDF p.7，Figure 3/4；p.9，Figure 6；p.12，Figure 7）
- [AUTHOR_FACT] 解析结果存在排版噪声：`τ-bench`、`pass^k` 被拆分或替换符号，双栏/公式被线性化，附录 JSON 长行出现换行标记，代码缩进与语法着色丢失；可视 PDF 中对应内容排版正常。（定位：PDF p.1、p.5、p.13–22、p.25–53）
- [AUTHOR_FACT] PDF p.44 与 p.53 内容稀疏是原文轨迹只剩 `user: ###STOP###` 或收尾语句所致，不是抽取缺失。（定位：PDF p.44、p.53）
- [OPEN_QUESTION] 视觉核对能确认当前 PDF 的显示与解析对应，但不能验证发布源代码、在线仓库或后续版本是否与论文完全一致；本次禁止联网且未读取任何外部材料。（定位：invocation，`Tool/network permission`）

## 9. 实际读取文件、工具与 trace

- [AUTHOR_FACT] 实际读取的研究文件仅有：
  1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P007_tau_bench.pdf`
  2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
  3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P007/read_2_attempts/r2-20260719-p007-a1/invocation.md`
- [AUTHOR_FACT] 另读取了执行所需的非研究技能说明 `C:/Users/g/.codex/skills/pdf/SKILL.md`；未把它作为论文证据。（定位：本轮自我可观察文件访问）
- [AUTHOR_FACT] 使用的工具/方式：PowerShell `Get-Content`、`Get-FileHash`；Python `pypdf` 页数/逐页文本抽取；仅绑定 `127.0.0.1` 的临时本地 PDF viewer；Playwright 对同一 PDF 逐页 fit-to-page 内存截图核对；`apply_patch` 写入本报告。没有互联网请求。（定位：本轮自我可观察工具调用）
- [AUTHOR_FACT] 本地 viewer 已停止；Playwright 初次打开 PDF 自动产生的两个已知 trace 文件已删除。除本 `report.md` 外，本轮未保留其他输出文件。（定位：本轮自我可观察清理调用）
- [AUTHOR_FACT] 平台级、不可篡改的完整 file-access/tool trace 对本 reader 为 `unavailable`；可用的只有本报告列出的自我可观察调用记录，不能将其声称为技术审计日志。（定位：invocation，`Observable file-access/tool trace`）

