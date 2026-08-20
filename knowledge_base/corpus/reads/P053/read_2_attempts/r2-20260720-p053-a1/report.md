# P053 fresh 独立二读报告

## 0. 来源、边界与核查方式

- Invocation：`knowledge_base/corpus/reads/P053/read_2_attempts/r2-20260720-p053-a1/invocation.md`，Attempt ID `r2-20260720-p053-a1`。
- 论文：*Language Models as Higher-Order Planning Formalizers*，arXiv:2603.23844 v2，2026。
- PDF：`knowledge_base/staging/papers/P053_higher_order_planning_formalizers.pdf`；实测 SHA-256 为 `224970784bd45edc3191b71c2aadd81e01f5869fcd004c4fa10bac4ed1217b19`，与 invocation 一致。
- 统一 prompt SHA-256：`ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`（以 invocation 冻结正文为准）。
- 核查时间：`2026-07-20T00:49:31.8126046+08:00`；actual model/version：`unknown`；canonical task/thread：`/root/plan05_p053_second_reader`。
- 边界：`procedural_blinding`。未联网，未枚举工作区，未读取 read-1、Cards、其他读者报告、其他论文读稿、Corpus Report 或 blind 材料。
- 方法：校验哈希后，用 PyMuPDF 对 44 个物理页逐页抽取文本、检查页面尺寸/图片/矢量对象，并将全部页面内存渲染后逐页视觉复核；对主结果图与消融图做额外放大核查。除本报告外未写入其他文件。

## 1. 总结性结论

[AUTHOR_FACT] 论文提出的 Higher-Order Formalizer（下称 H-O Formalizer）不是让 LLM 搜索计划，而是把 formalization 阶段的输出从完整 grounded PDDL problem file 改为一个可执行的紧凑 Python generator；generator 执行后再生成完整 PDDL，后续交给 planner 或作者自建 parser。核心映射是 `Dn -> Rn -> In`。定位：物理页 4，§3.1，短定位文本 “outputs a higher-order generator program first”。

[READER_INTERPRETATION] 真正的 changed computation 是“让模型归纳并写出生成规则/循环”，把随实例规模增长的逐事实枚举移到确定性程序执行阶段；它没有消除 grounded instance 的下游展开，也没有消除 planner 的搜索复杂度。论文的主实验在 solver 超时/崩溃时改用 ground-truth problem-file parser exact comparison，因此主结果更直接证明“压缩模式下的 formalization fidelity”，而不是端到端求得计划的可扩展性。

[READER_INTERPRETATION] H-O 相对普通 Formalizer 的主结果并未干净隔离“高阶表示”这一变量：H-O 使用两阶段 pattern review，而普通 Planner/Formalizer 是单阶段；附录 prompt 还向 H-O 明示循环、对象构造、模运算、完整图构造等域特定算法骨架及错误检查清单。Figure 6 显示 pattern review 本身可带来很大增益，因此主图中的优势应视为“Python generator + 更强域特定提示 + 第二次反思调用”的联合效果。

[AUTHOR_FACT] 普通 Formalizer 的 scaling failure 不是普遍发生：在 BlocksWorld-Unravel 与 Transport-Unravel 中出现波动或退化，H-O 更强；在 OpenStacks-Unravel 与 ChildSnack-Unravel 中，G3F/DS-V4 普通 Formalizer 仍稳健，H-O 主要是匹配。定位：物理页 6，§4，短定位文本 “fluctuates or degrades in BlocksWorld and Transport” 与 “remains robust”。

## 2. 统一问题 1：方法究竟改变哪一步计算？

[AUTHOR_FACT] 普通 Formalizer 接收自然语言问题描述，直接输出 fully grounded PDDL problem instance；H-O Formalizer先输出 `Rn`（论文以 Python generator 为实例），再由 compiler/interpreter/lifted planner 展开为 `In`。定位：物理页 4，§3.1；Figure 1 在物理页 1 对比“explicitly enumerate many grounded fluents”与“compact program”。

[AUTHOR_FACT] 论文把普通 Formalizer 的模型侧空间描述为 ground fluent space `Fn`，把 H-O 的模型侧空间描述为 compact program space，并声称 `|Rn| << |Fn|`。定位：物理页 4，§3.1，短定位文本 “shifts Formalizer's burden”。

[AUTHOR_FACT] 实现上，模型生成 `<generator>...</generator>` 中的 Python 脚本；脚本执行产生 PDDL problem file。H-O 使用第二阶段 prompt，让模型回看首稿中的 repeating-pattern loops 后重新生成完整脚本。定位：物理页 6，§3.3；物理页 30–32、33–36、37–40、41–44，Listings 25、28、31、34。

[READER_INTERPRETATION] 计算变化可拆为两项，论文主结果却把它们一起改变：

1. 表示变化：PDDL 逐事实生成 -> 生成程序/循环；
2. 推理流程变化：单次生成 -> 首稿 + pattern review + 再生成。

[READER_INTERPRETATION] 下游仍需实际展开 `Rn` 为大型 `In`；而且程序化 planner 在大实例上仍会超时或崩溃。故方法转移的是 LLM 输出与状态跟踪负担，不是消除完整 grounding、求解或验证成本。定位：物理页 3，§2.2；物理页 11，Appendix E。

## 3. 统一问题 2：输入、输出、可用信息与干预时点

### 输入与可用信息

[AUTHOR_FACT] 各 pipeline 获得自然语言 domain description、自然语言 problem description，以及 ground-truth PDDL domain file；domain 固定，论文明确只研究 problem complexity scaling。定位：物理页 3，§2.2，短定位文本 “We assume the domain file as given”。

[AUTHOR_FACT] H-O prompt 额外要求输出 Python generator，并提供可执行 generator 示例和大量域特定约束。BlocksWorld 示例直接展示 odd/even stack 的构造循环；ChildSnack review 明示 residue class 与 child-to-table assignment 检查；OpenStacks review 明示 sliding-window/wraparound；Transport review 明示 fully connected roads、固定 package 起点与 capacity chain。定位：Listings 25/28/31/34，物理页 30–44。

[READER_INTERPRETATION] ground-truth domain file 不是 ground-truth problem file，因此不能简单称为答案泄漏；但 H-O prompt 中的域/模板特定算法与错误清单包含了大量本应从自然语言归纳的计算结构，形成强 scaffolding，尤其 Listing 25 的示例几乎直接给出 BlocksWorld-Unravel 初态的核心生成算法。

### 输出与干预时点

[AUTHOR_FACT] Planner 输出动作序列；普通 Formalizer 输出 PDDL problem file；H-O Formalizer 输出能生成 PDDL problem file 的 Python 程序。定位：物理页 2–4，§2–§3.1；Listings 21–34。

[READER_INTERPRETATION] H-O 干预发生在“自然语言 -> grounded problem representation”的 formalization 阶段，早于 programmatic planning。它不改变 domain action schemas，也不直接产生 plan。

### 下游与判定

[AUTHOR_FACT] 正常情况下作者使用 `dual-bfws-ffparser` planner 与 VAL validator；随着问题变大，planner 超时，因此作者自建 parser 对比 LLM 输出与 ground-truth PDDL problem file。定位：物理页 3，§2.2。

[AUTHOR_FACT] Appendix E 将 objects、initial state、goal state 的 perfect match 视为 valid plan；任何 mismatch 视为 invalid。作者称这些域中的问题都可解。定位：物理页 11，Appendix E，短定位文本 “perfect match ... implies a valid plan”。

[OPEN_QUESTION] parser 是否按集合语义消除事实顺序/格式差异、是否检查类型、重复事实、数值 fluent 与未被比较的 problem-file 字段，论文没有给出 parser 规范、测试或误判分析。

## 4. 统一问题 3：最强基线与最接近组合基线

[READER_INTERPRETATION] 最接近、也最重要的基线是“同一模型的普通 Formalizer”：输入仍是 NL domain/problem + ground-truth PDDL domain，输出改为直接 PDDL，并使用相同 ground-truth problem-file comparison。它与 H-O 的差异最接近目标 changed computation，但调用次数和 prompt 强度没有匹配。

[AUTHOR_FACT] 模型包括 Gemini 3 Flash（G3F）、DeepSeek-V4-Flash（DS-V4）与 Qwen2.5-Coder-32B-Instruct（Q25）。开放模型由 KANI、默认 temperature、单张 H100 运行。定位：物理页 4，§2.2 “Models”。

[AUTHOR_FACT] BlocksWorld-XXL 还比较 D&C Formalizer：一次调用生成 header，再把 problem description 分句，每句各调用一次生成一行 PDDL，最后合并。Q25 在 100 blocks 从普通 Formalizer 约 30% 提升到 D&C 的 100%。定位：物理页 4，§2.2；Figure 5a，物理页 7。

[READER_INTERPRETATION] D&C 是值得关注的组合基线，因为它同样通过改变生成分解缓解长输出/上下文负担；但论文只在 BlocksWorld-XXL 展示，没有在四个 Unravel 域与 H-O 正面对比，也没有按总调用数/token 对齐，因此不能判断“程序压缩”是否优于“多调用分解”。

[AUTHOR_FACT] Q25 的 pattern-review ablation 显示：OpenStacks 45% -> 55%，Transport 23% -> 66%，ChildSnack 41% -> 87%。定位：Figure 6，物理页 8。

[READER_INTERPRETATION] 缺失的关键组合基线是：普通 Formalizer + 同样两阶段 review；H-O 单阶段；H-O + 与普通 Formalizer等长度/调用预算；以及 D&C 在同一 Unravel 数据上的结果。没有这些 factorial comparisons，无法把主效应归因给 higher-order representation 本身。

## 5. 统一问题 4：模型、token、tool-call、prompt、oracle 差异

### 已报告预算事实

[AUTHOR_FACT] 普通 Planner/Formalizer 被描述为 single-stage；H-O 是 two-stage；D&C 是一次 header call 加“每句一次”调用。定位：物理页 4，§2.2；物理页 6，§3.3。

[AUTHOR_FACT] 开放模型只报告 KANI、default temperature、1 H100；每个实验只运行一次，单实例结果为 0/100。定位：物理页 4，§2.2；物理页 12，Appendix H。

[OPEN_QUESTION] 未报告可比的 input/output token 上限、总 token、wall-clock、API/tool-call 数、重试策略、解码停止条件、closed-model temperature/版本快照或经济成本。也未给出 generator 执行超时、异常处理和安全沙箱细节。

### 可导致混杂的具体差异

[READER_INTERPRETATION] H-O 至少多一次模型调用并重复原始任务 prompt；它既获得更多推理预算，也得到针对 repeating-pattern error 的定向反馈。Figure 6 的大幅增益证明该额外阶段不是可忽略因素。

[READER_INTERPRETATION] H-O prompt 比普通 Formalizer prompt 更强：除了输出格式，还明确要求循环、禁止 hard-code、给出域特定不变量与算法骨架。因而对比同时改变了输出语言、提示内容与推理轮数。

[READER_INTERPRETATION] 自建 parser + 已知可解数据构成 evaluation shortcut：perfect ground-truth match 足以推出存在有效计划，但不等于实际 planner 在给定资源内求出计划。论文自己的 planner 已在大问题上失败，因此“planning scalability”与“formalization exact-match scalability”必须分开。

[OPEN_QUESTION] Listing 25 的 BlocksWorld 第二阶段文字却写“target OpenStacks problem PDDL”（物理页 32）。这可能是论文排版/复制错误，也可能进入实际 prompt；论文未说明实际运行 prompt bytes 是否与附录完全一致，影响复现与解释。

## 6. 统一问题 5：限制、负向结果、未测试边界

### 作者明示限制

[AUTHOR_FACT] 只评估 fixed domain specification 的 classical symbolic planning；未覆盖 partial observability、stochastic、temporal 或 multi-agent settings。定位：物理页 9，§8 “Limitations”。

[AUTHOR_FACT] 实现依赖 Python generator 与 handcrafted prompting（包括 pattern-reflection）；未研究中间表示是否 optimal、minimal 或可跨域 transfer。定位：物理页 9，§8。

[AUTHOR_FACT] 作者提醒 Formalizer 与 H-O Formalizer 在真实环境仍可能 hallucinate。定位：物理页 12，Appendix F。

### 作者报告的负向/边界结果

[AUTHOR_FACT] 在 BlocksWorld-XXL，所有 Planner 到 30 blocks 均降至 20% 或以下；G3F 普通 Formalizer 到 100 blocks 仍为 100%，Q25 到 80 blocks 仍高于 70% 后急跌。Q25 错误中 14% 缺 init、64% 多 init、57% 缺 goal、21% 多 goal。定位：物理页 4，§2.2；Figure 5a，物理页 7。

[AUTHOR_FACT] 四个 Unravel 域中，Planner 几乎归零；OpenStacks 是例外，G3F/DS-V4 可用“先开足 stacks、批量开始、批量发货”的 brute-force plan 获得近乎完美结果。定位：物理页 6，§4。

[AUTHOR_FACT] 普通 Formalizer 在 BlocksWorld 与 Transport 波动/退化；在 OpenStacks 与 ChildSnack，frontier models 仍稳健。极端扩展中，OpenStacks 300 orders 时 G3F/DS-V4 为 90%/100%，ChildSnack 300 children 时为 80%/90%；1000-batch 只有 DS-V4 完成 OpenStacks，准确率 70%。定位：物理页 6，§4。

[READER_INTERPRETATION] “只有 DS-V4 完成”把完成性、资源预算与准确率纠缠在一起；论文未报告其他模型为何未完成、超时阈值或成本，不能将该扩展视为干净的模型质量比较。

[AUTHOR_FACT] Q25 无 pattern review 时的代码错误高度集中在循环：OpenStacks 90% 错误发生在 loop（80% 为 includes loop）；Transport 错误在 object appending 与 package/capacity loops；ChildSnack 100% 错误在 waiting loop。每域只随机取两个 batches，最多人工看 10 个错误。定位：物理页 8，§5 与 Listings 1–3。

[READER_INTERPRETATION] 该错误分析样本小，且“最多 10 个错误”不是全量审计；百分比不应外推为稳定总体分布。

### 数据与外推边界

[AUTHOR_FACT] Domains-Unravel 共 280 个 synthetic problems，四个域，每个规模/域 batch 含 10 个问题；除 BlocksWorld 外只变化一个主参数，其他参数固定在 low-medium difficulty。定位：物理页 5，§3.2；Table 1，物理页 11。

[AUTHOR_FACT] 为维持 plan complexity，BlocksWorld-Unravel 的 goal 仍被随机化并逐条枚举；保持常数长度的是 initial statement portion。定位：物理页 5–6，§3.2，短定位文本 “still randomize and enumerate the goal states” 与 “initial statement portion ... remains constant”。

[READER_INTERPRETATION] 因而论文验证的是特定“局部可压缩”模板，不是自然语言问题整体都具有常数描述长度；对于无规则、噪声、歧义、组合规则或需要从示例学习新生成器的任务，证据不足。

[OPEN_QUESTION] 未测试新域零样本迁移、模板外扰动、自然语言歧义/同义改写、错误 domain file、生成程序的安全性、语义等价但非 exact-match 的 PDDL、plan quality/optimality，以及当下游 grounding/planner 成为瓶颈时的端到端收益。

## 7. 统一问题 6：可抽取的 Operator 与真实 Failure（仅二读建议，不生成正式 Card）

### Operator 候选

[READER_INTERPRETATION] `Higher-order generator formalization`：让 LLM 输出可执行生成规则，把大规模事实枚举交给确定性程序；证据：Figure 1（物理页 1）、§3.1（物理页 4）、§3.3（物理页 6）。适用边界是输入确有简洁、可程序化的重复结构。

[READER_INTERPRETATION] `Pattern review / loop reflection`：首稿后专门审查循环、模运算、对象与事实构造，再完整重生 generator；证据：§3.3（物理页 6）、Figure 6（物理页 8）、Listings 25/28/31/34。

[READER_INTERPRETATION] `Sentence-wise D&C formalization`：header 单独生成，事实按自然语言句子拆分为多次原子生成后合并；证据：§2.2（物理页 4）、Listings 23–24（物理页 28–30）。它属于近邻替代 operator，不等同于 H-O。

### 真实可记录 Failure

[AUTHOR_FACT] `Ordinary Formalizer enumeration failure under compressed descriptions`：在部分 Unravel 域/模型随规模扩大出现波动或退化，错误体现为 initial/goal facts 缺失或额外生成。证据：§2.2（物理页 4）、§4（物理页 6）、Figure 5（物理页 7）。必须保留“仅部分域/模型”的边界。

[AUTHOR_FACT] `Generator loop/pattern error`：H-O 的紧凑程序会把一次 off-by-one、错误 residue class、对象类型拼接或 assignment rule 错误放大成大量 facts 错误。证据：§5（物理页 8）、Listings 1–3（物理页 8、10–11）。

[AUTHOR_FACT] `Downstream solver scaling failure`：大实例上 programmatic planner 会 timeout/crash，迫使评估退化为 parser exact comparison。证据：§2.2（物理页 3）、Appendix E（物理页 11）。

[READER_INTERPRETATION] 不应把“普通 Formalizer 普遍不扩展”记录为无条件 Failure，因为 G3F/DS-V4 在 OpenStacks/ChildSnack 及 300-scale extension 上反例明显；也不应把 H-O 写成消除 planning search 的 operator。

## 8. 统一问题 7：关键判断—定位索引

| 判断 | 标签 | 物理页 / 章节 / 图表 | 短定位文本 |
|---|---|---|---|
| H-O 输出 generator，再展开 PDDL | `[AUTHOR_FACT]` | p.4, §3.1 | “Dn -> Rn -> In” |
| 目标是减少模型枚举 grounded fluents | `[AUTHOR_FACT]` | p.1, Figure 1；p.4, §3.1 | “compact program” |
| H-O 使用两阶段 pattern review | `[AUTHOR_FACT]` | p.6, §3.3 | “two-stage prompts” |
| 普通 Formalizer 并非所有域都退化 | `[AUTHOR_FACT]` | p.6, §4；p.7, Figure 5 | “remains robust” |
| Q25 review 显著提升 | `[AUTHOR_FACT]` | p.8, Figure 6 | 45→55、23→66、41→87 |
| solver 大实例超时/崩溃，改用 parser | `[AUTHOR_FACT]` | p.3, §2.2；p.11, App. E | “times-out”; “crashes” |
| exact problem-file match 被计为 valid plan | `[AUTHOR_FACT]` | p.11, App. E | “perfect match ... implies a valid plan” |
| 数据为受控 synthetic、单主变量 | `[AUTHOR_FACT]` | p.5, §3.2；p.12, App. G | “synthetic” |
| 只跑一次且无方差估计 | `[AUTHOR_FACT]` | p.12, App. H | “Each experiment is run once” |
| H-O prompt 含强域特定算法提示 | `[AUTHOR_FACT]` | pp.30–44, Listings 25/28/31/34 | “Required: at least one loop” |
| 主结果混合表示变化与额外 review | `[READER_INTERPRETATION]` | p.6 §3.3 + p.8 Figure 6 | 单阶段 vs 两阶段 |
| 未证明端到端 planner scaling | `[READER_INTERPRETATION]` | p.3 + p.11 | solver failure 后改用 exact match |

## 9. 统一问题 8：解析文本与可视 PDF 是否冲突

[AUTHOR_FACT] 44 个物理页均已视觉复核。未发现会改变论文内容的 PDF 缺页、裁切、图表覆盖或公式渲染缺失。

[READER_INTERPRETATION] PyMuPDF 的 plain-text extraction 在双栏页存在阅读顺序交错，尤其物理页 1、4、8–11；Figure 5/6 的曲线与柱状值不能只依赖抽取文本，已用页面渲染复核。Appendix 的 Listings 13–44 以大段代码/提示为主，视觉页面与抽取文本在实质内容上吻合。

[OPEN_QUESTION] 物理页 32 的 “target OpenStacks” 出现在标题为 BlocksWorld 的第二阶段 prompt 中，视觉 PDF 与解析文本一致，因此这是原文中的真实不一致，不是 parser artifact；其是否进入实际实验 prompt 无法由论文解决。

## 10. 二读最终结论摘要

[READER_INTERPRETATION] 论文可靠地展示了一个有意义的计算重定位：对于规则性强、自然语言高度压缩的 planning instances，让模型写生成器比逐事实输出 grounded PDDL 更容易扩展。最可信的证据是 BlocksWorld/Transport 中同模型 H-O 相对普通 Formalizer 的曲线差异，以及 Q25 loop-error 分析。

[READER_INTERPRETATION] 但证据不足以把提升单独归因于 higher-order representation，更不足以支持一般性的端到端 planning scalability：H-O 同时得到第二次 review、域特定算法骨架与不同输出形态；预算未对齐；大实例用 parser exact match 代替实际求解；数据是高度规则化的 synthetic templates，且部分普通 frontier Formalizers 本身保持稳健。后续使用本论文时，应把 claim 收窄为“在已知固定域、可程序压缩的 problem formalization 上，generator representation 联合 pattern review 改善 exact formalization accuracy”，并把 prompt/预算/solver 边界一起保留。
