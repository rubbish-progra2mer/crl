# PLAN_05 Card Source Audit F

## 审计身份与边界

- 本报告是一次性、独立的知识源 grounding 审计；不是研究 Reviewer，不评分、不排名、不投票，也不生成 Candidate。
- 执行线程 provenance：`reused independent reader thread due platform thread cap`。平台线程容量限制导致复用独立读者线程；本次审计仍只使用 invocation 明列的 42 张 Card、这些 Card 引用的 35 条 Evidence，以及 Card metadata 引用的 16 份 PDF。
- 未联网；未读取 read_1、read_2、reconciliation、saturation、calibration、blind、旧 audits 或 Candidate 材料。
- `knowledge_base/corpus/evidence.json` 的 SHA-256 为 `092c1f1dd85cc3a6bdd13b37e81dc37443827bd79697085d1004f885230c7496`，与 invocation 一致。
- 42/42 张 Card 的 metadata 可解析；共有 35 条唯一 Evidence；所有 `[AUTHOR_FACT]` 行均带 Evidence 引用；16/16 份 PDF 的 SHA-256 均与各 Card `source_refs` 一致。

判定口径：`ACCEPT` 表示 Card 文本、引用和边界无需 source 修订；`REVISE` 表示存在可定位且可局部修复的文本、引用定位或 source metadata 问题；`REJECT` 仅用于核心内容无法由允许来源支撑的情形。

## Paper Cards

| Card | 结论 | 可定位理由与必要动作 |
|---|---|---|
| `paper-p026.md` | ACCEPT | P026 p7 §3.2.2 明确把每次 policy-LLM 调用抽取为 input/output/reward transition；p9 §3.3.1 明确当前实现把同一 final return 赋给 episode 内所有 action。Card 对机制和 credit 边界的区分准确。 |
| `paper-p056.md` | REVISE | 核心事实受支持：P056 p1 支持 node prompt 与 edge/connectivity 优化，p5 §3.2 支持同一 20 个 Mini Crosswords 用于优化和评估，p17 支持 DyLAN 的轻微精度优势及更高复杂度/成本。但 `ev-p056-dylan-cost-quality.section="References"` 错误；该页实际为 Appendix D.1。修正 Evidence section 后可接受。 |
| `paper-p057.md` | ACCEPT | P057 p4 §3 支持 archive-conditioned agent code search；p6 §4.1 明确 ARC 搜索 25 iterations，并用 held-out test data 评价全部 discovered agents。Card 已把重复使用 test data 与 discovery budget 作为边界，而未把其当独立泛化证明。 |
| `paper-p058.md` | REVISE | P058 p6–7 §4 支持 MCTS 对完整 executable workflow 的 selection/expansion/evaluation/backpropagation 及 validation-driven 选择。Card 中“二读还发现部分超参数叙述不一致”不由 metadata 中的 PDF/Evidence locator 直接承载，且依赖本审计禁止读取的 provenance。删除该句，或改为带 PDF 页码与具体冲突值的独立 source 观察。 |
| `paper-p059.md` | REVISE | P059 p3 §2.1 的形式化定义是 orchestrator 每步选择单个 `a_t ∈ A` 激活，不是选择“参与者集合”。将“选择激活哪些 Agent”“参与者集合”改为“选择下一名激活 Agent”；p10 的 compact/cyclic 关联可保留，但继续注明其与 controller、异质能力和 terminal outcome 混杂。 |
| `paper-p060.md` | REVISE | P060 p6 跨 §5.1–§5.2 的直接结果是：增加一层 IR 后 Level 2 在 8/8 设置优于 Level 0/1；四类 IR 中 NL 持续伤害，而 PyPDDL/PDDL 持续改善。“第二种 syntax-aligned IR”容易误读为某一固定的第二类型，应改成上述精确定义。`ev-p060-ir-result-and-nl-failure.section="Introduction"` 也应改为 `§5.1–§5.2`。Lineage 中 P051/P052 不在本 Card `source_refs`，应删除或补齐正式 source 依赖。 |
| `paper-p062.md` | REVISE | P062 p4 §3.1 支持统一 STM/LTM/language-memory action policy，但 task specification `T` 在训练时包含 expected answer `A_q`；Card 未披露这一 training-only oracle boundary。p6 还明确同一 trajectory advantage 广播到所有先前 memory/reasoning steps。补写 `A_q` 边界；并把两条 Evidence 的 `section="Front Matter"` 分别改为 `§3.1` 与 `§3.4–§3.5`。 |
| `paper-p063.md` | REVISE | P063 p4 §3.2、p6 §4.2、p20 Appendix 分别支持 dynamic link generation、主要使用 `k=10` 且按类别调整、以及 prompt 允许更新邻居内容/标签。Card 中“二读发现多处公式、prompt、k 与成本叙述不一致”没有本 Card metadata 可定位的直接 source 记录；删除该概括，或逐项增加 PDF locator 和具体冲突。 |
| `paper-p064.md` | REVISE | P064 p2 的 experience-following 是当前 query 与 retrieved record 的高 **input similarity** 导致高 output similarity；Card 的“retrieved execution similarity”改变了自变量。改为“高输入/查询相似度的 retrieved record 可诱发错误复制与放大”。`ev-p064-evaluator-reliability` 位于 p5 §3.2–§3.3，不是 Introduction；另应删除或直接定位“二读发现表格数值不一致”。 |
| `paper-p065.md` | REVISE | P065 p5 §4.2 支持对完全相同 environment states 下的 action 与 discounted return 分组且不增加 rollout；p9 §5.5 的 recurrence 比例只来自 ALFWorld。Card 把它写成“Agent Lightning uniform return 的直接后继”，但本 Card 只声明 P065 source，未声明 P026；应改成不具名的 trajectory-level uniform-return baseline，或补 P026 source/evidence。删除未定位的“二读……开销比例算术不一致”；“规范 state”改为“完全相同 environment state”。 |
| `paper-p066.md` | REVISE | P066 p1 Abstract 支持 single-turn 强而 memory、dynamic decision-making、long-horizon reasoning 仍困难；p4 §3.3 支持 Base/Missing Parameters/Missing Functions/Long Context 四类 multi-turn 评价。核心结论可保留；但 Card 中“二读发现 extra/duplicate prediction、嵌套值比较和 multi-turn 聚合……”没有 source locator，应删除或逐项加 PDF 定位。 |
| `paper-p067.md` | REVISE | P067 p6 §3.2 和 p7 §4.2 支持：AgentHarm 分开测 refusal、malicious-task success 与 benign capability；在所测 universal jailbreak/template 条件下，jailbroken agents 保留基本 agentic competencies。Card 的“Agentic misuse 可保持”过度泛化，应限定为“在 AgentHarm 的所测模型、任务与 jailbreak 条件下”。 |
| `paper-p068.md` | REVISE | P068 p2 Figure 1/Introduction 支持 challenger disagreement → evidence proposal → auditor adjudication → revise then score；p6 §6.3–§7.1 支持 hidden micro-gold 60.8%→90.9%。两条 Evidence 的 section 分别误标为 `Front Matter` 与 `Related Work`，应按上述位置修正。Card 中“二读发现完整方法成本显著更高及同族模型共演化”应改成带具体 PDF locator 的 source observation，或保留为明确 hypothesis/待控 confound，不能以禁止材料 provenance 入库。 |
| `paper-p069.md` | REVISE | P069 p1 Abstract/§1 支持描述编辑使 GPT-4.1、Qwen2.5-7B 的 usage 超过 10 倍；p3 §2.1.2 支持相同描述/参数下 first-tool order bias。核心事实准确，但 Evidence section 均误标为 `Front Matter`：分别改为 `Abstract/§1` 与 `§2.1.1–§2.1.2`。 |
| `paper-p070.md` | REVISE | P070 p3 §3.1 支持六阶段 token/latency attribution；p9 Conclusion/Limitations 支持在所测轻量至中等工具中 orchestration/synthesis 占主导，并明确重型 I/O 可改变瓶颈。Card 中“二读发现表格 total/percentage 内部不一致”无直接 locator；删除或给出具体页、表、字段与算术关系。 |
| `paper-p071.md` | ACCEPT | P071 p2 §1 直接支持 plan-template extraction、semantic-target retrieval 与小模型 adaptation；p7 §4.2 支持 semantic-cache false positives、full-history 的准确率/成本劣化及总体 cost-performance trade-off。Card 边界与 PDF 一致。 |

## Operator Cards

| Card | 结论 | 可定位理由与必要动作 |
|---|---|---|
| `operator-transition-decomposed-agent-training.md` | ACCEPT | 输入/输出/reward transition、训练时机和“不把 transition decomposition 误当局部 credit”均由 P026 p7、p9 支持；changed computation 清楚。 |
| `operator-utility-optimized-agent-graph.md` | ACCEPT | P056 p1、p5 支持 node/edge optimization、pre-deployment search 与同集评价边界；输入、输出和 discovery budget 表述可执行。 |
| `operator-archive-conditioned-agent-code-search.md` | ACCEPT | P057 p4、p6 支持从 archive 条件化生成/修改 agent code，并用有限 search/evaluation budget 选择。Card 没有把 held-out test 的重复使用包装成独立泛化。 |
| `operator-mcts-executable-workflow-refinement.md` | ACCEPT | P058 p6–7 支持完整 workflow 作为搜索对象、validation feedback、selection/expansion/evaluation/backpropagation 及部署前搜索预算。 |
| `operator-state-conditioned-agent-activation.md` | REVISE | P059 p3 §2.1 的 action 是单个被激活 agent；Card 的“active agents”“下一激活子集”“roster”误写为 subset selection。输入仍是当前 state，但输出应改为“下一名 agent identity”，预算变化也按逐步单 agent activation 表述。 |
| `operator-syntax-aligned-formal-ir-planning.md` | REVISE | changed computation 与 P060 p1、p6 一致；但其引用的 `ev-p060-ir-result-and-nl-failure.section` 应从 Introduction 改为 `§5.1–§5.2`。Source lineage 指向 P051/P052，却未在 metadata 声明且不在本次 allowlist；删除该具名依赖或补齐正式 source。 |
| `operator-unified-language-memory-action-policy.md` | REVISE | P062 p4 支持 task state/STM/LTM 输入及 hybrid action 输出，p6 支持 broadcast credit；但必须披露训练 state 的 `T` 含 expected answer `A_q`，以免把训练 oracle 偷渡成部署输入。同步修正两条 Evidence section。 |
| `operator-dynamic-linked-memory-evolution.md` | ACCEPT | P063 p4 §3.2 支持生成 memory links，p20 Appendix prompt 支持基于新记忆更新邻居内容/标签；Card 明确这是 write-side persistent rewrite，并披露额外 LLM call 与 provenance-loss 风险。 |
| `operator-anchor-state-relative-credit.md` | REVISE | P065 p5 §4.2 的输入不是泛称“规范 state/action/outcome”，而是完全相同 environment state 下的 action 与 discounted return；输出为该 anchor group 的 relative advantage。按此改写即可；不额外 rollout 与 ALFWorld recurrence 边界准确。 |
| `operator-capability-preserving-agent-safety-evaluation.md` | ACCEPT | P067 p6–7 支持离线比较 harmful-task success、refusal 和 retained benign/basic agentic capability；Card 已注明 sandbox、task coverage 与“测量修复而非防御”的边界。 |
| `operator-evidence-audit-before-score.md` | REVISE | P068 p2 的计算角色应分开：challenger 读取 current benchmark state 并在 disagreement 时提交 verdict/rationale/evidence；auditor 比较 challenger proposal 与 incumbent rationale；accepted revision 形成新版本后再评分。Card 的统一输入“claim、gold 与外部证据”会把可修订 current label 误写成 oracle gold，也遗漏 disagreement-only gate。同步修正两条 Evidence section。 |
| `operator-stagewise-mcp-cost-attribution.md` | ACCEPT | P070 p3 §3.1 明确六阶段、token 与 latency instrumentation；p9 明确所测部署的 bottleneck 与 heavy-tool regime-shift 边界。Card 正确描述为 profiling operator，而非任务质量提升机制。 |
| `operator-adaptive-plan-template-reuse.md` | ACCEPT | P071 p2 支持完成后抽取 structured plan template、按 semantic target 检索并由 lightweight model 适配；p7 支持 false-positive、long-history、recurrence 与 accuracy-cost 风险。输入、输出、时机、预算均具体。 |

## Failure Cards

| Card | 结论 | 可定位理由与必要动作 |
|---|---|---|
| `failure-uniform-terminal-return-erases-step-credit.md` | ACCEPT | P026 p9 直接观察到同一 final return 广播给 episode 内所有 actions；Card 将“局部 credit 不可识别”标为 synthesis，并未捏造成作者的因果实验结论。 |
| `failure-same-set-agent-graph-evaluation.md` | ACCEPT | P056 p5 明确同一 20 题用于 optimization/evaluation；Card 用“可适配 evaluation instances”而非“必然过拟合”保持了窄推断。 |
| `failure-reused-selection-feedback-in-agent-search.md` | ACCEPT | P057 p6 与 P058 p7 分别支持在 search 中重复使用 held-out test/validation feedback；Card 正确限定为 selection-induced optimism 风险，没有宣称已观察到特定泛化跌幅。 |
| `failure-natural-language-ir-hurts-formal-planning.md` | REVISE | P060 p6 §5.2 直接支持在该论文 8 个 LLM-domain settings 中 NL IR 持续伤害；Card 的窄范围正确。仅需把关联 Evidence section 从 Introduction 修正为 `§5.1–§5.2`。 |
| `failure-unified-memory-policy-retains-terminal-credit-smearing.md` | REVISE | P062 p6 直接支持同一 trajectory advantage 广播到先前 memory/reasoning actions，Card 对“改变控制权但未识别 step-specific causal credit”的区分准确。需修正两条 P062 Evidence section，并在适用边界中披露训练 `T` 含 expected answer `A_q`，避免 credit 结论与 training oracle 混淆。 |
| `failure-retrieved-experience-propagates-stored-errors.md` | REVISE | P064 p2 的条件是 retrieved record 与当前 query 的高 **input similarity**，随后出现 output imitation/error propagation。把“execution-similar memory”“表面执行相似性召回”改为“input/query-similar retrieved record”；`ev-p064-evaluator-reliability.section` 改为 `§3.2–§3.3`。 |
| `failure-anchor-state-credit-needs-state-recurrence.md` | ACCEPT | P065 p9 §5.5 的 `<35%` singleton / `>65%` recurrent-state 观察明确限定在 ALFWorld；Card 把它作为机制前提而不是普遍失败结论，范围诚实。 |
| `failure-single-turn-tool-score-overstates-agent-competence.md` | ACCEPT | P066 p1 与 p4 支持 single-turn 表现不能覆盖 memory、动态决策、长程推理以及四类 multi-turn 状态能力；Card 没有把 benchmark 差距扩展成所有 Agent 的普遍失败。 |
| `failure-chatbot-refusal-does-not-establish-agent-safety.md` | REVISE | P067 p7 的观察仅来自 AgentHarm 所测模型、benign set 与 universal jailbreak/template 条件；将 Observed failure 限定到这些条件。其“capability-preserving trajectory evaluation 是测量修复，不是自动防御”边界可保留。 |
| `failure-one-shot-expert-gold-is-brittle.md` | REVISE | P068 p6 支持 hidden micro-gold 从 60.8% 到 90.9%，且 Card 已限定 Deep Research benchmark。需把 `ev-p068-one-shot-gold-brittle.section` 改为 `§6.3–§7.1`、`ev-p068-audit-then-score.section` 改为 `Figure 1/Introduction`；并明确 audit 只处理 challenger 与 current benchmark 的 disagreement，不是对所有标签重审。 |
| `failure-tool-description-and-order-bias.md` | REVISE | P069 p1、p3 直接支持描述编辑 usage 偏置与 identical-tool first-order bias，且 Card 正确没有推导任务正确率必然下降。修正两条 Evidence section；删除“二读确认”这一未由 source metadata 承载的 provenance，改为独立 PDF 观察。 |
| `failure-light-tool-runtime-bottleneck-overreach.md` | REVISE | P070 p9 Limitations 直接限定 lightweight-to-moderate tools，并说明 heavy I/O 可造成 regime shift；核心 failure 边界准确。删除或精确定位“二读发现部分汇总表数值不一致”，不能只引用被禁止的读稿 provenance。 |
| `failure-plan-cache-semantic-false-positives.md` | ACCEPT | P071 p7 §4.2 直接支持 semantic-cache false-positive hits 及 full-history 的更差准确率/更高成本；Card 以适用条件和可能修复边界表述，没有把 APC 结果外推为普遍缓存定律。 |

## 必须统一修正的 Evidence locator

以下 9 条 Evidence 的 `page_start/page_end` 和 passage 内容可定位，但 `section` 与 PDF 页内实际章节不一致：

| Evidence | 当前 section | 应改为 |
|---|---|---|
| `ev-p056-dylan-cost-quality` | `References` | `Appendix D.1` |
| `ev-p060-ir-result-and-nl-failure` | `Introduction` | `§5.1–§5.2` |
| `ev-p062-unified-memory-action-policy` | `Front Matter` | `§3.1 Problem Formulation` |
| `ev-p062-broadcast-advantage` | `Front Matter` | `§3.4–§3.5` |
| `ev-p064-evaluator-reliability` | `Introduction` | `§3.2–§3.3` |
| `ev-p068-audit-then-score` | `Front Matter` | `Figure 1 / Introduction` |
| `ev-p068-one-shot-gold-brittle` | `Related Work` | `§6.3–§7.1` |
| `ev-p069-description-induced-preference` | `Front Matter` | `Abstract / §1 Introduction` |
| `ev-p069-identical-tool-order-bias` | `Front Matter` | `§2.1.1–§2.1.2` |

## 审计结论

- `ACCEPT`: 17
- `REVISE`: 25
- `REJECT`: 0

没有发现核心机制完全无法由允许 PDF/Evidence 支撑的 Card。所有 `REVISE` 均可通过收窄措辞、补齐训练/适用条件、纠正 changed computation、删除未声明的“二读发现” provenance，或修正 Evidence section metadata 完成；在这些修订落地前，不应把相关 Card 视为 source-grounding 已闭环。
