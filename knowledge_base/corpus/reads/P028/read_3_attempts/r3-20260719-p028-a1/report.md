# P028 fresh 独立第三读核源报告

## 0. Provenance 与边界

- Invocation snapshot：`knowledge_base/corpus/reads/P028/read_3_attempts/r3-20260719-p028-a1/invocation.md`，Attempt ID `r3-20260719-p028-a1`。
- 原文：`knowledge_base/staging/papers/P028_memory_r1.pdf`；实测 SHA-256 `c206af4e792e9550f2aaec8a6c4d9b141d1ddcb587e781d7866870c8f3e4dd4f`，与 invocation 一致。
- 统一提示：`knowledge_base/templates/second_read_prompt.md`；实测 SHA-256 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，与 invocation 一致。
- Canonical metadata：Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning；ACL 2026 Long，`ACL:2026.acl-long.583`。
- 实际模型/版本：`unknown`（运行界面未提供可核验版本）；canonical task/thread：`/root/plan05_third_reader_conflicts`。
- 阅读方法：对 20 个物理页逐页读取原始 PDF 的文本对象；对 LoCoMo 规模和 temporal-memory window 所在争议页进行内存渲染复核，未创建临时文件。
- 边界声明：未读取 `read_1`、任何 `read_2`、reconciliation、Cards、CORPUS_REPORT、其他报告/读稿或 blind query；未枚举工作区；未联网；未作 Candidate 评价。

## 1. 方法改变的计算步骤

- [AUTHOR_FACT] Memory-R1 含两个分别经 RL 微调的 agent：Memory Manager 对外部记忆执行 `ADD/UPDATE/DELETE/NOOP`；Answer Agent 对 RAG 取回的候选记忆执行 memory distillation 并回答。Locator：物理页 1–2，Abstract/Introduction；物理页 3–4，Section 3 与 Figure 2。
- [AUTHOR_FACT] Memory Manager 策略接收新信息 `x` 与当前/检索记忆 `Mold`，输出操作 `o` 和更新内容 `m'`。Locator：物理页 3–4，Section 3.1，Equation (1)。
- [AUTHOR_FACT] Answer Agent 接收问题 `q` 和候选记忆集 `Mret`，输出答案 `y`；每题按相似度 RAG 检索 60 条候选记忆后再蒸馏。Locator：物理页 4–5，Section 3.2，Equation (5)。
- [AUTHOR_FACT] 两个 agent 均分别用 PPO 或 GRPO 微调，奖励来自最终答案与 gold answer 的 exact match；Memory Manager 训练时 Answer Agent 冻结，Answer Agent 训练时 Memory Manager 固定。Locator：物理页 4–5，Sections 3.1–3.2，Equations (2)–(6)；物理页 16–17，Appendix E/F 交界处的两阶段训练说明。
- [READER_INTERPRETATION] 核心 changed computation 有两处：把记忆写入/合并/删除决策变为 outcome-driven policy；把“直接消费全部检索结果”改为学习式记忆筛选与回答。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 多会话对话由多个 session 组成；session 是不同时间发生的交互，每个 session 含若干 turn，正文把 turn 定义为“两位用户的一次来回交换”。Locator：物理页 3，Section 3 开头。
- [AUTHOR_FACT] 在每个新对话 turn，LLM 先抽取值得记忆的信息，再从 memory bank 检索相关项，Memory Manager 决定操作并更新记忆。Locator：物理页 3–4，Section 3 与 Figure 2；物理页 19，Algorithms 3、5。
- [AUTHOR_FACT] 回答阶段按问题从已构造的 memory bank 取回候选，Answer Agent 先输出选中的相关记忆，再给最终答案。Locator：物理页 4–5，Section 3.2；物理页 15–16，Algorithm 2、Figure 11；物理页 19，Algorithm 4。
- [AUTHOR_FACT] Algorithm 2 进一步说明每位对话参与者各检索 top 30，共 60 条。Locator：物理页 15，Algorithm 2 lines 7–8。
- [READER_INTERPRETATION] Memory Manager 的干预点是逐 turn 更新外部记忆；Answer Agent 的干预点是问题到达后的检索结果过滤和答案生成。

## 3. 基线与比较口径

- [AUTHOR_FACT] 主实验基线包括 LoCoMo RAG、A-Mem、Mem0、MemoryOS 与 Memory-SFT。所有基线由作者用 LLaMA-3.1-8B-Instruct 和 Qwen-2.5-7B-Instruct 重实现，推理温度为 0，最大 token limit 为 2048。Locator：物理页 5，Section 4.1 “Baselines”。
- [AUTHOR_FACT] Memory-SFT 使用与 Memory-R1 相同的架构和训练数据，但把 RL 换成对 GPT-5 trajectories 的行为克隆。Locator：物理页 5，Section 4.1 “Baselines”。
- [READER_INTERPRETATION] 因此 Memory-SFT 是最接近的受控训练目标基线；MemoryOS 是正文计算相对提升时采用的 strongest external baseline。Locator：物理页 6，Table 1 后正文。
- [OPEN_QUESTION] “最强基线”取决于是否把作者自建的 Memory-SFT 算作基线以及采用 F1、BLEU-1 还是 J；Table 1 中不同定义不应被合并成一个无条件排名。

## 4. LoCoMo turn/token statistics：所有原文口径与冲突

| 来源 | 原文报告 | 阶段/口径判断 |
|---|---|---|
| 物理页 3，Section 3 开头 | session 是不同时间的交互；turn 是两位用户的一次 back-and-forth exchange | [AUTHOR_FACT] 这是本文对 session/turn 的显式方法定义。 |
| 物理页 5，Section 4.1 “Dataset and Model” | LoCoMo 对话“about 600 turns, 26k tokens” | [AUTHOR_FACT] 位于主实验数据集介绍，描述 LoCoMo 长对话规模。 |
| 物理页 12，Appendix B.1 “Test Data” | 对话“averaging 300 turns and 9k tokens”，最多 35 sessions | [AUTHOR_FACT] 位于附录测试数据介绍，也描述 LoCoMo 对话规模。 |

- [READER_INTERPRETATION] 两组数字都明确指向 LoCoMo conversations，而原文没有标注一个是 utterance 数、另一个是 back-and-forth turn 数，也没有说明一个是原始全集、另一个是过滤后子集。
- [READER_INTERPRETATION] 物理页 3 对 turn 的显式定义使“600 utterances≈300 exchanges”成为可能的外部解释，但这不是论文自己给出的消歧；本报告不采用该解释来消除冲突。
- [OPEN_QUESTION] `600/26k` 与 `300/9k` 是否来自不同预处理版本、不同数据子集、不同 turn 计数单位或简单笔误，原文无法判定。
- [AUTHOR_FACT] 上述四个关键数字均经原始页面内存渲染确认，与解析文本一致；不是抽取错位造成的冲突。

## 5. Temporal-memory window：所有原文定义与冲突

| 来源 | 原文报告 | 阶段/口径判断 |
|---|---|---|
| 物理页 13，Appendix B.2，Algorithm 1 line 5 | 对每个 turn `t`，由 GPT-4o-mini 使用“previous 50 turns”构造 temporal memory bank | [AUTHOR_FACT] 标题为 Memory-R1 Training 的数据构造算法；输出是 Memory Manager 训练 tuple。 |
| 物理页 13，Appendix B.2 “Memory Manager Training Data” | 对每个 turn `t`，GPT-4o-mini 从“preceding 24 turns”构造 temporal memory bank | [AUTHOR_FACT] 同页同节的 Memory Manager 训练数据正文。 |
| 物理页 13，Appendix B.2 “Answer Agent Training Data” | 每题在 temporal memory bank 上 RAG 取回 60 条候选记忆 | [AUTHOR_FACT] 这是 Answer Agent 候选检索数量，不是 turn-window 长度。 |
| 物理页 15，Algorithm 2 lines 7–8 | 每个参与者 top 30，共 60 条候选记忆 | [AUTHOR_FACT] 这是 60 条的组成口径，仍不是 24/50 turn window。 |

- [READER_INTERPRETATION] `previous 50 turns` 与 `preceding 24 turns` 都描述 Memory Manager training-data construction，而非清楚区分训练/验证/测试、Memory Manager/Answer Agent 或原始/过滤阶段。
- [OPEN_QUESTION] 原文没有版本标记、脚注或定义说明两种窗口各自适用范围；因此不能把 24 和 50 解释成不同阶段后同时成立。
- [AUTHOR_FACT] 同一物理页 13 的左右栏版面分别清楚显示 24 与 50；两处均经内存渲染确认，不是双栏文本解析串列导致的误读。

## 6. 数据划分、训练数据与 reward 使用范围

- [AUTHOR_FACT] LoCoMo 排除 adversarial subset，采用 `1:1:8` train/validation/test split，共 `152/81/1307 questions`。Locator：物理页 5，Section 4.1 “Dataset and Model”。
- [AUTHOR_FACT] 只在 LoCoMo 上训练，对 MSC 与 LongMemEval 做 zero-shot evaluation。Locator：物理页 5、7，Sections 4.1、4.3。
- [AUTHOR_FACT] Memory Manager 与 Answer Agent 分别从 LoCoMo 多轮对话构造训练集；前者没有显式操作标签，以 downstream answer exact match 作学习信号；后者使用 question、60 retrieved memories 和 gold answer。Locator：物理页 13，Appendix B.2；物理页 15，Algorithm 2。
- [OPEN_QUESTION] `152/81/1307` 明确以 questions 计数，但原文没有说明对应 dialogue/session 是否也隔离；同一对话上下文能否跨 train/validation/test，无法由原文判断。
- [OPEN_QUESTION] 24/50-turn 冲突使 Memory Manager 训练 tuple 的精确构造不可复现；不能由其他表述多数来选择一个窗口。

## 7. 可能的模型、token、tool-call、prompt、oracle 差异

- [AUTHOR_FACT] 作者称所有基线使用同一两种 backbone、温度 0、最大 2048 tokens；RL 训练使用温度 1.0，validation/testing 使用 greedy decoding 温度 0。Locator：物理页 5，Section 4.1；物理页 15，Appendix D。
- [AUTHOR_FACT] Memory Manager 训练数据中的 temporal memory bank 由 GPT-4o-mini 预构造；Memory-SFT trajectories 来自 GPT-5。Locator：物理页 13，Appendix B.2/Algorithm 1；物理页 5，Memory-SFT baseline。
- [READER_INTERPRETATION] 因此即使被评估 backbone 相同，训练监督生成器/数据构造器仍包含外部强模型；这些条件与纯 heuristic baselines 不完全等价。
- [AUTHOR_FACT] Answer Agent 看到每题 60 条候选记忆并进行 distillation；论文另比较 Base、Base+Reranker、Memory-R1 的准确率与延迟。Locator：物理页 4–5，Section 3.2；物理页 8，Figure 8。
- [OPEN_QUESTION] 各外部 baseline 是否使用完全一致的 memory extraction prompt、相同 memory bank 内容、同样 60 条候选与相同检索实现，原文没有逐项证明。
- [AUTHOR_FACT] 训练 reward 使用 gold answer exact match；评估还包含 token-level F1、BLEU-1 和单独 LLM-as-a-Judge。Locator：物理页 4–5，Equations (4)–(6)，Section 4.1。
- [AUTHOR_FACT] 以 J 值作训练 reward 会提高 J 但降低 F1/BLEU-1，因为输出更长；作者最终采用 EM reward。Locator：物理页 8，Table 2 与 Reward Design Analysis。
- [READER_INTERPRETATION] 这是明确的 reward/metric alignment 影响：结果会随奖励模型和答案长度口径变化，不应只归因于记忆机制。
- [OPEN_QUESTION] LLM-as-a-Judge 所用具体模型在已核读原文中未给出，故 J 的模型依赖无法定量排除。

## 8. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 评估集中在对话型数据；多模态扩展超出本文范围。Locator：物理页 9，Limitations。
- [AUTHOR_FACT] Memory Manager 与 Answer Agent 分开训练以在稀疏奖励下保持稳定，但过程不够直接；端到端多智能体 RL 被列为未来方向。Locator：物理页 9，Limitations。
- [AUTHOR_FACT] 去掉 RL Memory Manager、RL Answer Agent 或 memory distillation 均降低部分指标；具体消融数值见 Figure 5。Locator：物理页 7，Section 4.4 与 Figure 5。
- [AUTHOR_FACT] J-based reward 的输出冗长，导致 F1/BLEU-1 较差并妨碍与长度受控基线的直接比较。Locator：物理页 8，Reward Design Analysis 与 Table 2。
- [OPEN_QUESTION] 未测试/未澄清边界包括多模态、端到端联合训练、question split 的 dialogue 隔离、精确 temporal window，以及 LoCoMo 规模统计口径。

## 9. 可供后续抽取的机制与真实失败事实（非正式 Card）

- [READER_INTERPRETATION] 可抽取机制：以最终 QA 正确性驱动记忆 CRUD/NOOP 决策；对固定候选记忆进行学习式 distillation；两个 agent 分阶段冻结训练。依据：物理页 3–5，Section 3；物理页 16–19，Algorithms 3–5。
- [AUTHOR_FACT] 可记录负向事实：vanilla manager 在两个真实案例中把互补事实误判为冲突并进行 DELETE/ADD；原始 Answer Agent 被无关 mountaineering 记忆干扰而答错。Locator：物理页 11–12，Appendix A.1–A.2。
- [AUTHOR_FACT] 可记录负向事实：J-based reward 与 lexical-overlap metrics 出现明显错配；分开训练虽稳定但增加流程复杂度。Locator：物理页 8–9，Reward Design Analysis、Limitations。
- [READER_INTERPRETATION] 24/50 与 600/26k 对 300/9k 是来源冲突/复现缺口，不应改写成模型性能 Failure。

## 10. PDF 版面与解析核验

- [AUTHOR_FACT] 物理页 5 的 `600 turns/26k tokens`、物理页 12 的 `300 turns/9k tokens`、物理页 13 的 24-turn 正文与 50-turn Algorithm 1 均经原始页面内存渲染复核，与解析文本一致。
- [READER_INTERPRETATION] 物理页 13 为双栏版面，线性抽取会交错左右栏；本报告分别依据版面中的 Appendix B.2 正文和 Algorithm 1 定位，未把相邻栏内容合并。
- [OPEN_QUESTION] 未对 20 页逐页做独立 OCR 或像素级字符比对，因此不能宣称不存在任何细小字形解析差异；争议相关数字未见视觉冲突。

## 11. 独立第三读结论

- [READER_INTERPRETATION] 原文明确支持 Memory-R1 的双 agent、两阶段 RL 机制，以及 LoCoMo question 级 `152/81/1307` 划分。
- [READER_INTERPRETATION] 原文同时、不可消歧地给出两套 temporal-memory window（24 与 50 turns）和两套 LoCoMo 对话规模（约 600/26k 与平均 300/9k）。它们没有被来源明确指派到不同阶段或统计口径。
- [OPEN_QUESTION] 在没有作者勘误、代码配置或版本说明的情况下，精确训练窗口和 LoCoMo turn/token 统计均应保持 unresolved，不应按多数表述或便利性裁决。

## 12. 可观察访问、网络与工具声明

- 文件访问：科研内容仅来自本报告第 0 节列出的 PDF、统一提示与本 attempt invocation；另按系统要求读取项目 `AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md` 和本地 `pdf` 技能说明等非科研操作规约，并回读本报告做编码/内容校验。未读取任何被禁止的科研资产。
- 网络：未使用；未发起任何 web/search/download 请求。
- 工具：使用 PowerShell 精确路径读取与 SHA-256 校验；使用项目 `.venv` 中 PyMuPDF 1.28.0 对原 PDF 逐页抽取文本、定位关键词并在内存中渲染关键页面；使用 `apply_patch` 仅写入本 `report.md`。
- 隔离性质：`procedural_blinding`，不是技术文件级 allowlist。
