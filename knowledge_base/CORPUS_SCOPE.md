# CRL v3 Production Agent Research Corpus Scope

当前范围版本：2026-07-31（Asia/Shanghai）  
知识截止：以各论文实际摄取时点为准，并在 `CORPUS_REPORT.md` 汇总。

## 1. 目标与停止规则

本知识库服务于一个窄目标：帮助主 AI 研究者从可核验的大语言模型智能体研究证据中理解论文、识别 Failure/Gap、迁移 changed-computation Operator，并形成值得进行本机小实验的研究实现。知识库不直接生成 idea，也不替代主研究者的科研判断。

固定论文篇数不是完成门槛。正式停止依据是：全文与复核质量、九个机制簇的机制覆盖、负向知识与强基线覆盖、谱系完整性、互补搜索波次的检索饱和，以及独立 blind-spot 审计是否仍发现会改变 implement space 的高影响遗漏。实际篇数只作结果披露。

Failure、Operator、Paper Card 是并列、互补的正式浏览入口，不设科研行动优先级。认识论权威顺序仍为原 PDF/散列与 reconciliation > Evidence > Card 综合 > 检索分数。

## 2. 准入范围

只准入文本与工具型 LLM Agent 的机制研究：

- reasoning/planning；
- test-time search、verification 与 compute allocation；
- tool use 与 action interface；
- memory、context 与 long-horizon state；
- reflection 与 self-improvement；
- multi-agent control 与 information flow；
- agent learning 与 credit assignment；
- evaluation、reliability、verifiability 与 safety；
- efficiency、cost，以及作为机制实验载体的 Deep Research。

主体年份为 2022–执行日，越接近执行日的工作占比应越高。更早论文只在其是定义性祖先、不可替代强基线或关键负向证据时准入。CCF-A/CCF-B、领域顶会和正式 proceedings 优先；优秀 arXiv、企业技术报告、公开 benchmark/evaluation 若提供不可替代的机制或失败证据，也可在明确版本与证据边界后准入。

SWE/code、文本 Web/API 与 Deep Research 只作为机制实验载体。每个此类条目必须说明它验证了哪项 changed computation、Failure 或 measurement risk；只有应用性能而无可迁移机制价值的条目不进入正式 manifest。

## 3. 排除范围

- 机器人、具身、多模态 Agent；
- 传统控制或非 LLM Agent 任务；
- “环境反馈学习与执行恢复”作为独立研究方向；
- 只有摘要、搜索 snippet 或不可核验元数据的条目；
- 纯应用系统、无机制隔离的 leaderboard paper；
- 仅以更强模型、更多 token/tool calls、额外 oracle/verifier 或 prompt 优势取得提升且无法隔离方法差异的工作；
- 与已录取版本重复、但没有独立机制或负向证据的版本。

范围外工作如是其他机制的直接祖先，只能有限准入，并在 Card 中明确 transfer boundary；不能借此扩大研究方向。

## 4. 正式准入条件

一篇论文进入 production manifest 前必须同时满足：

1. canonical identity、版本关系、合法可访问全文和 PDF SHA-256 已确认；
2. 主 AI 研究者首读覆盖问题、方法、实现、实验、消融、限制和相关附录；
3. 存在有效的独立二读、逐项 reconciliation；关键 anchor、冲突或多 Operator 依赖时完成条件性三读；
4. Evidence locator 能回到原 PDF，且区分作者事实、作者解释与 `[CODEX_SYNTHESIS]`；
5. 至少承担一种明确角色：canonical Operator、Failure/negative evidence、直接祖先/强基线、measurement risk 或不可替代实验载体；
6. 对应 Card 的事实字段只来自 reconciliation 后的 Evidence；
7. 没有阻断性 `UNRESOLVED`，也没有未披露的预算、oracle、模型、prompt 或 benchmark contamination 风险。

未完成上述条件的候选只留在 `staging/`，不参与正式检索或 Gap 形成。

## 5. 机制覆盖矩阵

| Stable slug | Agent computation stage | 优先补充的 Failure / limitation | 可迁移 Operator 目标 | 强基线 / 直接祖先要求 | evaluation / measurement 风险 | 可用实验载体 | Pilot 起点与当前空白 |
|---|---|---|---|---|---|---|---|
| `planning_reasoning` | 任务分解、计划形成、action selection | 长推理/显式计划在等预算下无益；计划错误传播 | 改变候选计划的生成、选择或修订计算 | direct policy、ReAct、tree/search 类 closest-composition | extra compute、prompt length、model scale | SWE、Web/API、可判定文本任务 | 已有 interleaving/tree search；缺等 verifier/采样预算归因 |
| `test_time_search_verification` | 候选生成后、执行前或中间状态的验证与选择 | verifier 错误、搜索收益来自采样量、固定深度的 under/over-search | evidence/consistency-grounded verifier；选择性 search/compute | direct sampling、Self-Consistency、fixed-depth、faithful adaptive compute | hidden oracle、gold-hindsight label、unequal samples | 工具计划、SWE、Deep Research | 已有 search/allocation；P080 补 adaptive depth，P081 补 independent-sampling baseline；开放工具 plan verifier 仍是运行时 nearest-prior 问题 |
| `tool_use_action_interface` | tool selection、argument construction、output interpretation、action commit | wrong tool/arguments、generic-tool distractor、raw-observation overload、likelihood/Agent utility 错位 | validated specialized tool creation/retrieval；action-preserving contextualization；显式 action interface | ReAct、Toolformer、CRAFT、强 function-calling agent、等 tool-call/token comparator | original-instance validation、ground-truth action retry、single-call/cost、model/tool advantage | τ-bench/BFCL 类文本 API、SWE、文本 Web | P078/P079/P082 已补 action-space、observation-side 与 self-supervised tool lineage；严格等预算收益消融留给具体 Candidate |
| `memory_context_long_horizon` | memory write、index、retrieve、read、decision context | stale/irrelevant memory、context competition、reading overload、write contamination | 分离 write/retrieve/read，改变决策时可见信息 | no-memory、full-context、fixed-k、strong memory pipeline | truncation confound、gold retrieval、session-ID/cost semantics | LongMemEval 类长历史文本交互 | 已有 stage decomposition/overload；缺 irrelevant retrieval 的直接因果证据 |
| `reflection_self_improvement` | 失败后 critique、policy/experience update、stop decision | generic/intrinsic critique、重复采样、外部 instructor 归因 | grounded critique、selective reflection、停止/更新门控 | no-reflection、resampling、Reflexion/ExpeL closest composition | extra context/token、oracle feedback、survivorship | SWE、Web/API、文本推理 | 已区分多种 reflection；缺 trajectory stop 判据 |
| `multi_agent_information_flow` | agent 间 message routing、aggregation、coordination | correlated error、重复采样、debate cost、跨 prompt/environment/agent trust surface | topology/routing、evidence diversity、selective aggregation | Self-Consistency、ensemble、single-agent matched-budget | aggregate token、role prompt、majority-vote advantage、simulated adversarial tools | 协作推理、SWE、Deep Research | 已有 MAD/MAST、routing/topology 与 P081 matched baseline；P083 补 adversarial coordination Failure，不虚构 defense Operator |
| `agent_learning_credit_assignment` | trajectory 后的局部 credit、experience update、policy adaptation | outcome credit 错配、token-local high variance、oracle trajectory、污染经验 | localized credit、step/decision attribution；受限的 utterance-critic/token-actor baseline | ArCHer、Agent Lightning、GiGPO、outcome-only update | trajectory-vs-token cost、simulated oracle、online feedback、data leakage | logged SWE/Web/API trajectories | P077 补 hierarchical temporal-credit canonical baseline；环境反馈学习仍按 Scope 排除，离线 delayed credit 需在具体研究中重新核源 |
| `evaluation_reliability_safety` | 评测定义、重复运行、uncertainty、安全审计 | benchmark artifact、leakage、低可靠性、单一终态与单 Agent 分数掩盖系统风险 | terminal+process measurement、repeat reliability、stagewise trust-surface audit | 当前强 benchmark、TAMAS、closest composition、matched model/budget | contamination、weak baseline、hidden oracle、metric gaming、simulated tools/monitor false positive | τ-bench/BFCL、SWE、Deep Research | 已有终态/重复/安全；P083 补多 Agent adversarial surfaces 与失败轻量防御证据 |
| `efficiency_cost_deep_research` | test-time compute、tool calls、latency、source acquisition 与 synthesis | 更多预算偷换、固定深度、成本不完整、质量—成本割裂、收益递减 | uncertainty/need-aware allocation、adaptive retrieval depth、可审计资源控制 | static matched-budget、Self-Consistency、fixed-depth、random/margin/entropy allocation | gold-hindsight stopping、token vs character、parallelism、cached calls、provider price | Deep Research、Web/API、SWE | P080 补 quality/depth trade-off，P081 补 independent-compute baseline；完整开放 Web Deep Research 联合评测由正式 Run 按 Candidate 检索 |

上表九项是稳定机制族。当前 `corpus/manifest.json` 还保留两个历史标签，以避免在没有独立知识库维护授权时改写 Paper 身份：`efficiency and cost` 归入 `efficiency cost and human deep-research interaction`，`multi-agent coordination` 归入 `multi-agent control and information flow`。因此只读结构审计会看到九个稳定族、十一个现有标签和两个已声明别名；别名不代表新增研究方向。

每个机制簇都必须同时搜索成功方法、失败/消融、强基线、最近组合和评测陷阱。论文数量、相近 Card 数量或同一 Evidence family 的多篇工作不能冒充独立支持。

## 6. 搜索入口族与来源优先级

需要系统检索时，建议先写清要补的 Failure/Operator/lineage/measurement 空白，再按科研需要组合以下入口；这是一种高价值方法，不是每轮必须执行的脚本门槛：

1. mechanism 与 changed-computation 词；
2. failure、limitation、ablation、negative result、benchmark artifact；
3. anchor 的 backward/forward citation lineage；
4. 2025–执行日的 ICLR/ICML/NeurIPS/ACL-family/AAAI 等目录、arXiv 与可信企业报告 recent scan；需要关注最近 6 个月 preprint，因为正式 proceedings 往往滞后；
5. strong baseline 与 benchmark 的引用者；
6. 组件组合、完整 pipeline 和 closest-composition 的最近先行；
7. safety、reliability、cost、verifiability 的横向审计。

来源优先级：官方 proceedings/OpenReview/ACL Anthology/PMLR/NeurIPS/ICLR/出版社或作者项目页 > arXiv 原文与官方代码 > Semantic Scholar 等候选发现服务。候选发现服务和摘要永远不能替代全文。

## 7. 独立知识库维护

知识库扩充不是正式 Run 的启动门，也不按时间、候选数量或碰撞计数自动触发。当前阶段扩充能力暂停：正式 Run 中发现的重要新论文只把来源、引用和必要证据保存在该 Run，不写入 staging、manifest、数据库或共享 Card。未来是否恢复独立知识库维护，或恢复 Run 中临时摄取，必须由用户另行明确授权。

未来用户明确恢复独立知识库维护后，维护方向与规模由主 AI 研究者根据预期科研收益判断。Failure、Operator、三路查询、谱系与评测陷阱等厚知识机制继续保留，但不得为了扩充而扩充。届时每次摄取仍遵守第 4 节的来源、独立阅读、reconciliation 和 Evidence 绑定标准；新论文与既有 Card 冲突时，由主研究者阅读并修订相应知识，不建立自动科研裁决器。

共享知识库只接收外部论文及其客观 Paper、Passage、Evidence 和 Card。任何 Run 的实验、候选、路线、审查意见、决策、失败结论、状态或复制件都不得进入共享库；跨 Run 只共享本 Scope 准入的论文知识。

## 8. 饱和与硬停止

只有在互补入口的后续波次主要返回重复、范围外或不改变 canonical computation、Failure condition、独立反证、谱系、strong baseline、measurement risk 与 implement space 的内容，并且独立 blind-spot 审计没有未解决高影响遗漏时，才能提出检索饱和。

任一正式论文缺全文/SHA/独立二读/reconciliation，任一关键 Operator/Failure 无 Evidence，存在版本重复或高影响盲点，均禁止进入 production retrieval freeze。达到任何篇数不改变该规则。
