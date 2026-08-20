# P072 独立二读报告

## 1. Provenance、读取边界与覆盖

- Invocation snapshot：`knowledge_base/corpus/reads/P072/read_2_attempts/r2-20260720-p072-a1/invocation.md`；本报告遵循其中冻结的 exact request 与 Frozen prompt。Invocation 实际 SHA-256 为 `98ec8b615153ab7a61764117ab7ffed40d4543e926dd79431c2d3e66fb7acfe1`，其中记录的统一 prompt SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。
- Invocation 指定的 canonical 路径 `knowledge_base/papers/P072_structured_clarification.pdf` 不存在；实际且唯一读取的论文路径为 `D:\Desktop\crl_judge\crl_agent_v3\knowledge_base\staging\plan05_sat_a2\P072_structured_clarification.pdf`。
- 实际 PDF SHA-256：`def959b625902e0381ddbac6f25e042c8670f07435248e50a075fe8ef3945598`，与 invocation 冻结值完全一致。
- 覆盖范围：PDF 物理页 1–28，共 28/28 页；对应文集页 40811–40838。正文、参考文献、附录 A–C、算法、工具域表和人工标注说明均已覆盖。
- 核验方式：按物理页连续提取文本并阅读，同时对 1–28 页逐页渲染缩略图做可视检查；表 2–5、图 4–7、公式 (1)–(13)、算法 1–2及附录中的交叉引用结合可视页面复核。未发现文本解析与可视 PDF 在实质内容上的冲突；文本提取会打散公式、表格和图例，因此下面的数值与公式关系以可视版面复核为准。
- 权限事实：本次是 `procedural_blinding`，不是技术文件隔离。未联网、未枚举工作区、未读取 read_1、Card、其他 read_2、saturation、retrieval 或 blind 文件；除本报告外未写入其他文件。实际模型的可验证产品版本、canonical task/thread ID 均未向读者暴露，记为 `unknown/unavailable`。

## 2. 论文究竟改变了哪一步计算

### 2.1 推理时 SAGE-Agent

- `[AUTHOR_FACT]` 输入包括用户请求、工具集合及 schema、对话/观测历史和由 LLM 生成的候选工具调用；候选参数取具体值或 `<UNK>`。工具 schema 被形式化为工具名、参数集、参数域和必需参数集合。（物理页 4–6，§4–5；物理页 26，算法 1）
- `[AUTHOR_FACT]` 候选调用的分数由参数确定度相乘得到：已指定参数取 1，未指定的有限域参数取 `1/|D|`，连续/无限域参数取小常数 `epsilon`；工具先验设为均匀，参数被假定条件独立。用户回答通过参数域交集更新 belief。（物理页 4–6，公式 (1)–(2)；物理页 12）
- `[AUTHOR_FACT]` 当需要澄清时，LLM 同时生成候选问题及其所针对的工具参数 aspect；系统以“最佳候选确定度的期望提升”定义 EVPI，再减去重复询问成本 `lambda * sum n_a(t)`，选择净分最高的问题。（物理页 5–6，公式 (3)–(5)）
- `[AUTHOR_FACT]` 实际实现不是直接求一个已给定响应模型下的标准 EVPI，而是模拟“完美消歧”：对问题覆盖的未知 aspect，以相应域大小乘回候选分数，再计算期望最大值。（物理页 6，§5.2 Step 3）
- `[AUTHOR_FACT]` 停止/执行触发包括：最佳候选分数达到执行阈值、最佳问题净收益低于 `alpha * max pi_c`、或达到最大步数；执行失败后，正文称可生成修正调用或错误专用问题并重新进入选择环节。（物理页 6，§5.2；物理页 12，§A.2）
- `[READER_INTERPRETATION]` 因而真正的计算改动是：在 ReAct 的 Reason 与 Act 之间插入“schema 域大小构造的完整度分数 → LLM 生成问题 → 完美消歧近似 EVPI − 重复 aspect 成本 → ask/execute 阈值”的控制器。它主要度量 specification completeness，不是从预测正确率校准得到的模型 epistemic uncertainty。

### 2.2 训练时 uncertainty-weighted GRPO

- `[AUTHOR_FACT]` 训练使用 When2Call 的约 9K 条样本，动作空间为 AskQuestion、CallTool、Decline、DirectAnswer；基础模型为 Qwen2.5 3B/7B，训练一轮 GRPO，并使用 LoRA。（物理页 6–7，§6–7；物理页 14–16，附录 B）
- `[AUTHOR_FACT]` appendix 的 certainty 对工具调用取候选调用分数，对 ASK 取 `1 - pi_c`，其他动作取 1；候选调用分数仍是参数确定度乘积。（物理页 16，公式 (10)–(13)）
- `[READER_INTERPRETATION]` 该奖励没有直接评估问题的信息增益或回答后的实际改进；它更接近“根据 `<UNK>`/参数域完整度重加权动作分类奖励”。参数只要被填入就获确定度 1，即使其值错误，因此该量本身不是校准置信度。

## 3. ClarifyBench、用户模拟器与评测边界

- `[AUTHOR_FACT]` ClarifyBench 覆盖文档、车辆、股票、旅行、文件系统五个域和 92 个工具，含 Explicit、Ambiguous、Infeasible 三类请求；用户模拟器持有真实意图，并回答 agent 的澄清问题。（物理页 3–4，§3；物理页 17–19，附录 C.1–C.3）
- `[AUTHOR_FACT]` 数据来自 DocPilot 的成功调用与 BFCL-v3。Ambiguous 样本通过最多遮蔽 3 个参数并用 GPT-4o 生成 5 个候选查询构造；Infeasible 样本通过手写 API 错误规则破坏工具调用，再由 LLM 生成查询。用户意图 prompt 也由 LLM 根据 ground-truth 调用和 utterance 总结。（物理页 3–4，§3.2；物理页 17、25，附录 C.2.1、C.6）
- `[AUTHOR_FACT]` 两名研究生标注者给每个候选按自然度、忠实度、可执行性等维度评分，并选最高者；最高分选择的一致性 Cohen's kappa 为 0.76。（物理页 4、19、28）
- `[AUTHOR_FACT]` 用户模拟器 prompt 明确向模拟器提供当前请求的 ground truth、用户意图和上下文，同时要求只回答当前具体问题、不泄露未来意图。作者另称从三类任务随机抽取 600 条交互轨迹做 post-hoc 人工检查，98.8% 的模拟器响应满足一致性与适当范围。（物理页 17–19、25，附录 C.2.2、C.5）
- `[READER_INTERPRETATION]` 模拟器是一个持有当前轮真值、服从提示且合作式回答的 oracle-like 用户。98.8% 验证支持其对既定 prompt 的一致性，却不能证明其覆盖真实用户的含糊、拒答、误解、信息缺失或偏好变化。
- `[OPEN_QUESTION]` 98.8% 的分母究竟是 600 条轨迹、轨迹中的全部回复，还是某个回复子集，原文没有清楚说明；C.5 也未报告该 post-hoc 检查的标注者人数、盲法或一致性。
- `[OPEN_QUESTION]` 表 2 报告总样本 716，但 Explicit 241 + Ambiguous 213 + Infeasible 198 = 652，差 64。逐域也存在同一缺口（例如 Documents 总数 181，而三类合计 146）。论文未解释剩余样本类别，导致各 split 的实际分母不完全可恢复。（物理页 4，表 2）

## 4. 基线、匹配程度与主要结果

- `[AUTHOR_FACT]` 推理实验将所有方法放在共同 ReAct scaffold 上，比较 ReAct + `ask_question()`、ProCOT、Active Task Disambiguation、Domain-aware ReAct，以及仅凭 `<UNK>` 触发问题的 SAGE heuristic ablation；GPT-4o 与 Qwen2.5-14B-Instruct 均以 temperature 0.5 运行。SAGE 使用 `lambda=0.5, alpha=0.1, epsilon=1e-4`。（物理页 6–7，§7、表 3）
- `[READER_INTERPRETATION]` 最接近的组合基线是 Domain-aware ReAct，因为它同样获得显式 schema 上下文；最接近的机制消融是 SAGE heuristic，因为保留候选/未知参数触发、移除 EVPI 选择。不存在跨所有 split 和指标都固定为同一个“最强基线”。
- `[AUTHOR_FACT]` GPT-4o 的 Ambiguous Coverage：SAGE 59.73，Domain-aware ReAct 55.70；平均问题数分别 1.39 与 2.56。Explicit Coverage 为 71.67 对 68.11；Infeasible Coverage 为 67.33，而外部基线中 Active Task Disambiguation 为 65.27。（物理页 7，表 3）
- `[AUTHOR_FACT]` Qwen2.5-14B 的 Ambiguous Coverage：SAGE 54.56，ProCOT 52.45，Domain-aware ReAct 51.10；Explicit 为 64.62，外部基线最高 ProCOT 61.76；Infeasible 为 61.84，外部基线最高 Domain-aware ReAct 55.76。（物理页 7，表 3）
- `[AUTHOR_FACT]` heuristic ablation 通常比完整 SAGE 低约 1–3 个点并多问约 0.2–0.4 个问题；`lambda` 消融只在每个 split 70 个 GPT-4o 样本上进行，作者称从 0 增至 0.5 可减少 18–27% 问题且其他指标变化小于 3%。（物理页 8，图 5及 §8.1）
- `[READER_INTERPRETATION]` 表 3 的标准差普遍很大（许多单元约 20–35），且未报告显著性检验、置信区间或逐域结果；因此数个百分点的差异不能仅凭该表解释为稳健胜出。

## 5. 模型、token、tool-call、prompt 与 oracle 差异

- `[AUTHOR_FACT]` 同一基础模型内的主表比较控制了模型名称和 temperature；训练实验也明确声明评测时不使用 SAGE scaffold 或 reward。（物理页 7，§7）
- `[AUTHOR_FACT]` 资源图显示简单基线约使用 14–18K tokens、14–16 次 LLM calls；Active Task Disambiguation 约 24K tokens、40 calls；SAGE 约 22K tokens，并称相对 Active Task Disambiguation 减少 54% calls。（物理页 8，图 4）
- `[READER_INTERPRETATION]` 因此“少问用户”不能等同于“计算更省”：SAGE 的 token 用量高于简单 ReAct/ProCOT/Domain-aware ReAct，54% calls 降幅的参照主要是昂贵的 Active Task Disambiguation。对用户问题数、LLM 调用数和 token 成本应分开报告。
- `[AUTHOR_FACT]` 工具参数域并非全部直接来自 API 枚举；附录称用 Qwen2.5-7B-Instruct 分析所有工具参数，产出 finite、estimated finite、numeric range、string 等域类型、大小和代表值。（物理页 14，附录 B.2）
- `[READER_INTERPRETATION]` SAGE 的效果可能部分来自额外的 schema/domain augmentation、候选与问题生成 prompt，以及多次 LLM 调用，而不只来自 EVPI 公式。论文没有给出足够细的 per-method prompt、候选数、最大轮数、上下文长度和相同 domain annotations 的配对证明来完全拆开这些因素。
- `[READER_INTERPRETATION]` benchmark 的 Ambiguous 查询由 GPT-4o 生成，同时 GPT-4o 又是一个被测模型；这形成同模型家族的生成/评测耦合风险。论文没有报告人写查询、真实用户查询或跨生成模型查询上的单独结果。
- `[OPEN_QUESTION]` 自然语言回答到参数域约束的 `UPDATE`/`O_b` 如何实现、使用何模型、其准确率与失败处理均未具体报告。该模块若获得 ground truth 或强 LLM 推断能力，会构成关键 oracle/模型边界。（物理页 5、12、26）

## 6. 明确可见的负向结果与未覆盖边界

- `[AUTHOR_FACT]` BFCLv2/When2Call 单轮表中，SAGE 的 ToolCall F1 低于 ReAct：GPT-4o 为 0.65 对 0.75，Qwen2.5-14B 为 0.59 对 0.72；主要伴随 ToolCall recall 从 0.79 降至 0.55、从 0.85 降至 0.48。SAGE 的 AskQuestion/Decline 指标更好，显示其收益包含偏向保守调用的权衡。（物理页 8，表 4）
- `[AUTHOR_FACT]` Qwen2.5-14B 的 Ambiguous TMR 中，完整 SAGE 为 78.14，略低于 heuristic ablation 的 78.23；不是所有单元都由完整方法最好。（物理页 7，表 3）
- `[AUTHOR_FACT]` uncertainty-weighted GRPO 的最大提升集中在 Direct Prompting：3B 从 base 36.5、普通 GRPO 55.0 到 65.2；7B 从 36.7、45.1 到 62.9。但在 Log Probability 评测上，它低于普通 GRPO：3B 为 35.9 对 38.4，7B 为 36.2 对 38.2。（物理页 9，图 6）
- `[AUTHOR_FACT]` 每个训练设置运行三次，但论文报告“best-performing model/setting”，未报告三次均值、方差或选择准则的完整结果。（物理页 7，§7(B)）
- `[AUTHOR_FACT]` 作者明示限制包括依赖可用于增强 schema 的工具描述、ClarifyBench 仍是模拟环境、模型范围仅覆盖 GPT-4o/Qwen2.5-14B 推理与 Qwen2.5-3B/7B 训练，并继承基础模型局限。（物理页 9，§10）
- `[READER_INTERPRETATION]` 未测试边界还包括真实用户、非合作或无法回答的用户、schema 错误/陈旧、未见工具域、不同语言、连续域校准、长对话状态漂移、高风险不可逆工具调用，以及真实执行后的端到端任务成功率。

## 7. 理论与复现审计

- `[READER_INTERPRETATION]` 论文把 `pi_c` 称为概率，但公式 (2) 只给出正比关系，实际评分又直接使用参数乘积；候选集合由 LLM 临时生成，而理论定义声称枚举全部可行 completion。对大域、连续域和组合工具调用，这两者并不等价。（物理页 4–6）
- `[OPEN_QUESTION]` 标准 EVPI 公式需要 `P(r | q, B)`，但论文没有给出或学习该响应分布；实现采用“完美解决目标参数”的域大小乘法近似。该近似如何归一化、如何处理一个回答只部分缩小域、用户拒答或回答有噪声，原文未解决。（物理页 5–6，公式 (3)、§5.2）
- `[READER_INTERPRETATION]` 成本项只惩罚重复询问过的 aspect。首次询问任何数量的新 aspect 成本均为 0，所以它是 redundancy cost，不是一般性的用户负担、时间或打扰成本；“ask/stop cost”不能解读为完整交互成本模型。（物理页 5，公式 (4)）
- `[READER_INTERPRETATION]` 附录 Proposition 1 的“`pi=1` 当且仅当所有参数已指定”在未指定参数域大小为 1 时不成立，而且“已指定”不等于“值正确”。（物理页 11，§A.1）
- `[READER_INTERPRETATION]` Proposition 2 把 `max` 错称为 concave；其 Jensen 不等式方向实际依赖 `max` 的 convex 性。随后又直接把本文的 EVPI 边际量替换成 entropy reduction 来声称 submodularity，没有建立两者等价，因此 submodularity 证明不成立。有限终止证明还假定 EVPI 持续下降或成本持续增长，而算法每步重新生成候选/问题，未证明这些条件；算法本身已有 `Tmax` 才是直接的有限上界。（物理页 11–12，§A.1）
- `[READER_INTERPRETATION]` 正文称执行失败后重新进入询问环，而算法 1 的执行分支写的是执行并直接 return；伪代码没有展示 error recovery 的实际控制流。（物理页 6、12、26）
- `[OPEN_QUESTION]` 正文 §6.2 写成 `R_category = Cert * r_base`，但附录公式 (9)–(11) 表示只对 `r_cls` 加权，总奖励仍含未加权的 `r_fmt` 与 `r_tool`。这会改变训练目标，属于关键复现歧义。（物理页 6、15–16）
- `[READER_INTERPRETATION]` appendix 的 `r_tool` 还给“no tool call or wrong tool name”列出 0.5，而“only one has a tool call”为 0；分支语义和正文“正确识别 tool/non-tool”表述不完全一致。ASK/REFUSE 标签来自问号或拒绝关键词启发式，未报告标签审计，可能引入训练噪声。（物理页 14、16）
- `[OPEN_QUESTION]` epsilon 也有内部不一致：主实验写 `1e-4`，图 7 标注的 Default 却是 `0.001`。此外 appendix 仍有 `Figure ??`、Travel 的 `Table ??`，训练表中的 batch size 写作 `8 (logs)`；GRPO 的 group size、采样配置等也未完整呈现。（物理页 7、13、16、19）

## 8. 可抽取的机制与真实 Failure 证据种子

以下仅是供主 Codex reconciliation 的独立证据种子，不生成正式 Card，也不作 Candidate 裁决。

- `[AUTHOR_FACT]` Operator 种子 O1：把工具参数 schema 映射成有限域/连续域确定度，并以参数确定度乘积形成候选调用的结构化完整度分数。（物理页 4–6，公式 (1)–(2)）
- `[AUTHOR_FACT]` Operator 种子 O2：对 LLM 生成的问题使用完美消歧近似 EVPI，减去重复 aspect 成本，再由相对阈值决定 ask 或 execute。（物理页 5–6，公式 (3)–(5)）
- `[AUTHOR_FACT]` Operator 种子 O3：把同一参数完整度信号用于 GRPO 动作分类奖励，使高不确定时 ASK 权重更高、参数完整时 TOOLCALL 权重更高。（物理页 6、16）
- `[AUTHOR_FACT]` Failure 证据 F1：普通 ReAct 在含糊请求上可能过早执行；表 3 的 Coverage/TMR/PMR 与提问数共同提供间接实验对照。（物理页 7，表 3）
- `[AUTHOR_FACT]` Failure 证据 F2：Active Task Disambiguation 在单轮评测中 AskQuestion recall 高但 precision 低，呈现过度询问；SAGE 则以降低 ToolCall recall 换取更高 Decline/AskQuestion 表现。（物理页 8，表 4）
- `[AUTHOR_FACT]` Failure 证据 F3：重复询问同一参数 aspect 会增加用户负担，论文用重复计数惩罚并在小规模 lambda 消融中观察到问题数下降。（物理页 5、8）
- `[READER_INTERPRETATION]` F1–F3 的证据仍受模拟用户、自动构造查询、schema/domain 辅助和未匹配计算预算限制；不能直接外推到真实用户或高风险工具执行。

## 9. 独立二读结论

- `[READER_INTERPRETATION]` 论文的可核实贡献是一个实用的 schema-completeness 控制器及相应模拟 benchmark，而不是已经被证明校准的 Bayesian uncertainty/POMDP 求解器。最有说服力的结果是同基础模型下 Coverage 与用户提问数的联合改善，以及训练后 Direct Prompting 的大幅提高。
- `[READER_INTERPRETATION]` 结论必须同时保留四项边界：EVPI 是完美消歧启发式而非已估计响应模型；用户模拟器持有 ground truth；SAGE 的 token 成本高于简单基线；负向结果包括 ToolCall recall/F1 和 Log Probability 指标下降。
- `[OPEN_QUESTION]` 在把该工作升级为更强机制证据前，最需要补的是：解释表 2 的 64 个样本缺口；公开/固定 `UPDATE`、domain augmentation 与 per-method prompts；按三次训练均值方差报告；在真实或带噪用户上验证；并用相同 token/LLM-call 预算与相同 schema 信息重新比较。
