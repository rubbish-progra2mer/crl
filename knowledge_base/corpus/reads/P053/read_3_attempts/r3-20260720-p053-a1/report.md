# P053 fresh independent read-3 report

## 1. Provenance 与边界

- Invocation：`knowledge_base/corpus/reads/P053/read_3_attempts/r3-20260720-p053-a1/invocation.md`
- Attempt ID：`r3-20260720-p053-a1`
- 角色：fresh independent conflict and measurement checker
- PDF：`knowledge_base/staging/papers/P053_higher_order_planning_formalizers.pdf`
- 实测 PDF SHA-256：`224970784bd45edc3191b71c2aadd81e01f5869fcd004c4fa10bac4ed1217b19`，与 invocation 一致。
- 统一 prompt 实测 SHA-256：`ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，与 invocation 一致。
- 隔离：`procedural_blinding`，不是可验证的文件级技术隔离。本读只使用 invocation、统一 prompt 与指定 PDF；未读取 read_1、read_2、Cards、其他读者报告、其他论文读稿、Corpus Report、blind 材料，未联网。
- 解析与核查：用 PyMuPDF 1.28.0 按物理页 1–44 抽取文本，并逐页检查可视页面；没有生成中间研究文件。
- 输出边界：本文件只作独立核源，不生成 Card/Evidence/manifest，不作 Candidate 评价。

## 2. 核心结论

1. `[AUTHOR_FACT]` H-O Formalizer 改变的是**问题形式化的输出表示**：模型不再直接枚举 grounded PDDL instance，而是先生成一个 Python generator，再由执行器展开为 PDDL，最后交给 planner 或比较器。定位：物理页 4，§3.1，短定位“`Dn ↦ Rn ↦ In`”；物理页 6，§3.3，短定位“generate Python programs that produce PDDL problem files upon execution”。它没有改变底层规划搜索算法。

2. `[READER_INTERPRETATION]` 论文的主要 H-O 对比混合了两个干预：一是 higher-order generator representation，二是只给 H-O pipeline 的第二阶段 pattern-review prompt。物理页 6 明说 H-O 使用 two-stage prompts，而 Planner/Formalizer 是 single-stage；物理页 8、Figure 6 又显示 pattern review 本身把 Q25 的准确率从 45%/66%/23% 提高到 55%/87%/41%（OpenStacks/Transport/ChildSnack）。因此 Figure 5 中 H-O 相对 Formalizer 的差异不能仅归因于表示变化。

3. `[AUTHOR_FACT]` 当 programmatic planner 随规模增大而 timeout/crash 时，作者用自写 parser 比较生成 PDDL 与 ground-truth problem file；完全匹配就计为 valid plan，任何 mismatch 计为 invalid。定位：物理页 3，§2.2，短定位“we write our own parsers”；物理页 11，Appendix E，短定位“a perfect match ... implies a valid plan”。

4. `[READER_INTERPRETATION]` 上述替代指标测量的是严格的 instance-formalization exact match，不是实际 planner 产生且经 VAL 验证的 plan accuracy。它可以在固定 domain 且实例保证可解时作为“存在可行计划”的充分代理，但不能证明端到端规划链在大实例上可运行；相反，planner timeout/crash 已经暴露了该链的未解决瓶颈。Planner 与 Formalizer/H-O 还因此接受了不同的最终 oracle：前者验证动作序列，后两者在大规模时核对 ground-truth PDDL。

5. `[READER_INTERPRETATION]` 证据可支持的窄 Claim 是：在四个**合成、固定 domain、强规则模板、主要单参数扩展**的数据族上，让所测 LLM 输出生成器程序，配合二阶段 pattern review，通常比一次性显式枚举 PDDL 更能维持 ground-truth instance exact-match accuracy。证据不支持把结论外推为通用 planning scalability、真实工业任务可扩展性、未知 domain formalization、跨 domain transfer，或实际 solver scalability。

6. `[READER_INTERPRETATION]` 最接近的控制与基线不足：缺少 single-stage H-O、Formalizer + pattern review 的正交对照；D&C Formalizer 只在 BlocksWorld-XXL 上报告，未在四个 unraveling domain 上报告；没有与 lifted planner、模板/DSL compiler、已有 code-as-intermediate-representation 或 generalized-planning program generation 方法进行实证比较。因此“表示变化”与“第二次模型调用/额外提示/额外 token”不能被因果分离，最近方法谱系也只停留在 related-work 文字说明。

## 3. 统一问题清单

### 3.1 方法究竟改变哪一步计算？

- `[AUTHOR_FACT]` 常规 Formalizer：`Dn → In`，LLM 直接输出 grounded PDDL problem；H-O Formalizer：`Dn → Rn → In`，LLM 输出 compact generator program，程序展开 PDDL。物理页 4，§3.1。
- `[AUTHOR_FACT]` 下游 planner/domain file 不变；作者通常使用 `dual-bfws-ffparser`，用 VAL 验证 planner 输出。物理页 3，§2.2。
- `[READER_INTERPRETATION]` 真正改变的是**serialization/formalization computation**：把重复事实的枚举从 LLM token generation 移到确定性程序执行。它没有减少展开后 `In` 的大小，也没有改变 planner 对展开后实例的搜索；论文实际还因 solver timeout 转而采用 parser exact match。
- `[OPEN_QUESTION]` 论文没有形式化定义所生成 Python 程序的允许语言、语义等价关系、最小性或安全执行边界。“higher-order”在实验中具体实现为 Python source generator，而不是经过独立验证的通用 lifted representation。

### 3.2 输入、输出、可用信息与干预时点

- `[AUTHOR_FACT]` 输入包括 NL domain description、NL problem description、ground-truth PDDL domain file，以及 pipeline-specific prompt；domain file 被假定已给出且固定。物理页 3，§2.2；物理页 6，§3.3。
- `[AUTHOR_FACT]` Planner 输出 action sequence；Formalizer 输出 PDDL problem file；H-O Formalizer 第一稿输出 Python generator，第二阶段在看到自己第一稿后检查 repeating patterns，再重生成完整 generator；执行 generator 后得到 PDDL。物理页 3–4、6；Listings 22、25–34（物理页 28–44）。
- `[AUTHOR_FACT]` H-O prompt 不只是更换输出格式，还明确要求循环、禁止硬编码完整 fact lists，并包含 domain-specific correctness constraints。定位：物理页 30–32（BlocksWorld）、33–36（ChildSnack）、37–40（OpenStacks）、41–44（Transport）。
- `[READER_INTERPRETATION]` 干预发生在 formalization 输出生成时，但第二阶段让 H-O 多看到一次自身草稿并多获得一次完整 prompt。因而 model calls、token budget、纠错机会与输出表示同时变化。
- `[OPEN_QUESTION]` PDF 未报告每个 pipeline 的实际 input/output/reasoning token、最大 token、延迟、生成器执行失败率、总 tool/model-call 数、成本，亦未说明 closed models 的精确 decoding 参数。

### 3.3 最强基线与最接近组合基线

- `[AUTHOR_FACT]` 直接基线是同模型的 Planner、Formalizer；BlocksWorld-XXL 另有 D&C Formalizer。物理页 4，§2.2 与 Figure 5a（物理页 7）。
- `[AUTHOR_FACT]` D&C 先调用一次生成 header，再按 NL description 的句子逐句调用模型生成一个 PDDL fact，最后合并。物理页 4，短定位“one sentence at a time”；Listings 23–24（物理页 28–30）。
- `[READER_INTERPRETATION]` 最关键但缺失的组合对照是：
  1. single-stage H-O；
  2. two-stage/pattern-review regular Formalizer；
  3. 在四个 unraveling domains 上运行 D&C Formalizer，并报告调用数、token、成本；
  4. deterministic template/DSL compiler upper bound；
  5. lifted planning 或不完整展开的 planner；
  6. 已有 code intermediate representation / generalized planning program generation 的实现级对照。
- `[AUTHOR_FACT]` Related Work 提到 Kagitha et al. 的 code intermediate representations、Silver et al. 与 Stein et al. 的 solver-code/generalized-planning 程序，但只作概念区别，没有实验比较。物理页 8，§6。
- `[OPEN_QUESTION]` 作者没有说明为什么 D&C 未进入 unraveling benchmarks，也没有量化其按句调用在 compact description 上是否不适用或成本过高。

### 3.4 可能的 model、token、tool-call、prompt 与 oracle 差异

- `[AUTHOR_FACT]` 模型为 Gemini 3 Flash、DeepSeek-V4-Flash、Qwen2.5-Coder-32B-Instruct；open models 通过 KANI、default temperature、单张 H100 运行。物理页 4，§2.2。
- `[AUTHOR_FACT]` H-O 使用两阶段 prompting；Planner/Formalizer 使用单阶段。物理页 6，§3.3。
- `[AUTHOR_FACT]` Figure 6 的 H-O ablation 直接证明 pattern review 是有效干预：Q25 在三域均提高。物理页 8。
- `[READER_INTERPRETATION]` 因此 Figure 5 的差异至少可能来自：程序表示、第二次调用、额外上下文/输出 token、针对已观察错误编写的 domain-specific review instructions，以及 generator 执行；缺少 factorial control 不能拆分贡献。
- `[AUTHOR_FACT]` ChildSnack 第二阶段明确把“previous generation”的主要错误总结写进 prompt，并要求保留 exact instance-specific facts；Transport/OpenStacks 也逐项列出易错规则。物理页 36、40、43–44。
- `[READER_INTERPRETATION]` 这些不是通用“反思”措辞，而是接近 benchmark/domain-specific error checklist 的强监督，可能显著降低固定模板上的错误；其可迁移性未测。
- `[AUTHOR_FACT]` BlocksWorld 的第二阶段 prompt 出现域名错写：在“Prompt for LLM-as-Higher-Order-Formalizer”中要求检查是否“exactly reproduce the target OpenStacks problem PDDL”。物理页 32，Listing 25。
- `[OPEN_QUESTION]` 该错写是否实际用于全部 BlocksWorld 运行、是否影响结果，PDF 无法判定。
- `[READER_INTERPRETATION]` Planner 用动作序列 + ground-truth simulation/VAL；大规模 Formalizer/H-O 用 PDDL-vs-ground-truth parser。这是 outcome oracle 不一致，不应把两者共同称作同一种实测 plan accuracy 而不加限定。

### 3.5 限制、负向结果与未测试边界

- `[AUTHOR_FACT]` 作者明示仅测试 fixed-domain classical symbolic planning；未测 partially observable、stochastic、temporal、multi-agent。物理页 9，Limitations。
- `[AUTHOR_FACT]` H-O 依赖 Python generator 与 handcrafted prompts/pattern-reflection；未研究 representation 的 optimality、minimality、transferability，也未研究更原则化 IR、learned compiler、与 lifted planning 的紧密集成。物理页 9。
- `[AUTHOR_FACT]` Domains-Unravel 共 280 个合成实例，四域主要只改变一个参数，其余参数固定在低到中等难度；模板具有规则化关系。物理页 5–6，§3.2；物理页 11，Table 1。
- `[AUTHOR_FACT]` 主实验规模最高 100；扩展到 300/1000 只做 OpenStacks 与 ChildSnack，且 1000-batch 仅 DS-V4 完成 OpenStacks、准确率 70%。物理页 6，§4。
- `[AUTHOR_FACT]` 各实验只运行一次；单实例结果为 0/100，图中百分比是批内聚合。物理页 12，Appendix H。
- `[READER_INTERPRETATION]` default temperature 下单次采样没有重复运行、方差或置信区间，无法区分随机波动与规模趋势，尤其每个规模仅 10 个实例时。
- `[AUTHOR_FACT]` 常规 Formalizer 在 BlocksWorld 与 Transport 会波动或下降；Planner 在多数 unraveling 域接近归零，但 G3F/DS-V4 的 OpenStacks Planner 通过“open sufficient stacks → bulk start → bulk ship”的暴力可行策略接近满分，未做有意义优化。物理页 6，§4。
- `[AUTHOR_FACT]` Q25 常规 Formalizer 在 BlocksWorld-XXL 的错误包含 missing/extra init 与 missing/extra goals；H-O ablation 的错误集中于 loop/object typing/waiting assignment。物理页 4、8、10–11。
- `[OPEN_QUESTION]` PDF 没有报告 parser 的规范化规则、语义等价处理、代码测试、误报/漏报审计；也没有报告 generated Python 的异常、超时、安全性与复现次数。

### 3.6 可抽取 Operator 与真实 Failure（仅作为独立读者建议）

- `[READER_INTERPRETATION]` Operator：将重复 grounded facts 的显式 token 枚举改成 compact executable generator，由循环/规则在 LLM 输出后展开；证据位置物理页 4，§3.1，及 Figure 1（物理页 1）。
- `[READER_INTERPRETATION]` Operator：在 generator 初稿后增加 domain-specific pattern-review，再完整重生成；证据位置物理页 6，§3.3，及 Listings 25/28/31/34。
- `[READER_INTERPRETATION]` Operator：D&C Formalizer 把长描述拆成 header call + sentence/fact calls；证据位置物理页 4，§2.2，Listings 23–24。
- `[AUTHOR_FACT]` Failure：直接 Planner 随规模增加迅速崩溃；unraveling benchmark 中除 OpenStacks 特例外近零。物理页 4、6–7。
- `[AUTHOR_FACT]` Failure：regular Formalizer 在 compact-to-large mapping 下并非稳定扩展，BlocksWorld 与 Transport 有波动/退化。物理页 6–7。
- `[AUTHOR_FACT]` Failure：loop 的 off-by-one/modulo、typed-object 构造、child-to-table assignment 会成批制造 missing/extra facts。物理页 8、10–11。
- `[READER_INTERPRETATION]` Failure：实际 planner 在大实例 timeout/crash，导致论文无法用统一的真实规划执行指标评估所声称的端到端 planning pipeline。物理页 3、11。

### 3.7 Claim 边界

- `[AUTHOR_FACT]` 数据不是开放世界 NL；每域由作者设计“realistic scenario with an easily describable pattern”，固定多个参数，只轮换/反转赋值以制造批内差异。物理页 5，§3.2。
- `[READER_INTERPRETATION]` 因此 strongest defensible claim 应同时限定：synthetic、fixed known domain、handcrafted compact patterns、作者给定 domain PDDL、所测三模型、所测规模、PDDL exact match、H-O + two-stage pattern review。
- `[READER_INTERPRETATION]` “decouples token output from combinatorial explosion”只对 generator source 的输出长度成立；展开后的 PDDL 与 planner input 仍然增长，论文也未报告 token-length scaling 曲线或端到端 wall-clock/memory scaling。
- `[OPEN_QUESTION]` 论文没有测试 pattern 不在 prompt/error checklist 中、多个参数同时变化、噪声/歧义 NL、未知 domain、动态约束、非规则目标、跨 domain generator reuse 或真实工业输入。

## 4. Parser / ground-truth exact-match 的测量审计

- `[AUTHOR_FACT]` §2.2 先说 BlocksWorld 保证 solvable，因此 generated problem file 与 ground truth 完全匹配就计为 valid plan；Appendix E 又将相同逻辑扩展表述为“our domains’ problems are always solvable”。物理页 3、11。
- `[READER_INTERPRETATION]` 若 parser 确实验证 objects/init/goal 的集合精确相等且 fixed domain 完全相同，则该条件足以说明生成了与 ground truth 相同的 planning instance；但它仍没有执行 planner，也没有产生 plan。
- `[READER_INTERPRETATION]` “任何 mismatch 都 invalid”会把语义等价但非字面/集合等价的形式化判错；反过来，若 parser 未检查 metric、numeric fluent、domain binding 或类型细节，也可能漏错。PDF 没给 parser specification，二者都无法排除。
- `[READER_INTERPRETATION]` planner timeout/crash 不应只被当作换指标的工程细节：它直接限制“完整 H-O planning pipeline scales”的 Claim。当前实验更准确的术语应是 `formalization exact-match accuracy under guaranteed-solvable fixed-domain instances`。
- `[OPEN_QUESTION]` 表述“plan accuracy, the percentage that can be executed to achieve the goal state”（物理页 3）是否把 parser-accepted formalization 与真实执行验证混合汇总，图注与附录没有逐点注明哪些样本由 planner/VAL、哪些由 parser 判定。

## 5. Higher-order representation 与 pattern review 的冲突审计

- `[AUTHOR_FACT]` H-O 主方法默认包含 pattern-reflection stage，不是附加可选分析。物理页 6。
- `[AUTHOR_FACT]` Figure 6 只在 Q25、OpenStacks/Transport/ChildSnack 上比较“Q25”与“Q25 Pattern Review”；未含 BlocksWorld、frontier models 或 regular Formalizer + review。物理页 8。
- `[READER_INTERPRETATION]` Figure 6 能证明 review prompt 对 H-O generator 有增益，却不能证明剩余增益来自 representation；需要 2×2 设计：direct PDDL vs generator × one-stage vs two-stage review。
- `[READER_INTERPRETATION]` 第二阶段 prompt 包含作者从先前错误中总结出的具体失败模式，尤其 ChildSnack 的 residue/table assignment、OpenStacks 的 wraparound/count chain、Transport 的对象分组和道路事实。这使实验同时测试“程序表示 + benchmark-aware checklist”。
- `[OPEN_QUESTION]` review prompt 的制定数据是否与评测实例/批次隔离、是否迭代看过测试错误、是否对所有模型固定，PDF 未交代。物理页 8 只说错误分析随机抽两个 batches、每域最多分析 10 个错误。

## 6. 逐页核查记录与视觉冲突

| 物理页 | 核查内容 |
|---:|---|
| 1 | 标题、摘要、Introduction、Figure 1；确认 direct grounded enumeration 与 compact generator 的概念图。 |
| 2 | planning instance/space 定义、Planner 与 inference-time scaling；确认 H-O 动机延续。 |
| 3 | Formalizer 定义、evaluation protocol、planner/VAL 与 parser substitution、BlocksWorld-XXL。 |
| 4 | 模型、Figure 5a 文字结果、D&C、unraveling 定义与 `Dn ↦ Rn ↦ In`。 |
| 5 | 四域合成数据、fixed/main-varying parameters、批内 rotate/reverse 规则。 |
| 6 | H-O 输入与二阶段 prompt、Figure 5 结果、300/1000 扩展。 |
| 7 | Figure 5a–e 全图；视觉确认三种 pipeline、三/四模型曲线与 Q25 Pattern Review 图例。 |
| 8 | Figure 6、Q25 error analysis、Related Work、Conclusion。 |
| 9 | Limitations 与 references 起始。 |
| 10 | references 结束、Listings 2–3 起始。 |
| 11 | Listings 2–3、Table 1、Figure 7、Appendix D/E；确认 solver crash 与 parser exact-match 说明。 |
| 12 | risks、synthetic data、single-run statistics、artifact statement。 |
| 13 | BlocksWorld domain 与 5-block 描述。 |
| 14 | BlocksWorld-XXL 100-block enumerative description。 |
| 15 | 100-block goal与 BlocksWorld-Unravel compact description 起始。 |
| 16 | compact description 结束、ChildSnack domain 起始。 |
| 17 | ChildSnack domain 与 problem file 起始。 |
| 18 | ChildSnack problem file 与 NL domain description。 |
| 19 | ChildSnack compact problem、OpenStacks domain 起始。 |
| 20 | OpenStacks grounded actions。 |
| 21 | OpenStacks domain/problem file。 |
| 22 | OpenStacks NL descriptions、Transport domain 起始。 |
| 23 | Transport actions 与 problem file 起始。 |
| 24 | Transport fully connected road facts。 |
| 25 | Transport road facts 续。 |
| 26 | Transport road facts、vehicles/packages。 |
| 27 | Transport goals/NL descriptions、regular Formalizer prompt 起始。 |
| 28 | regular Formalizer/Planner prompts、D&C header prompt 起始。 |
| 29 | D&C header/body prompts。 |
| 30 | D&C body prompt、BlocksWorld H-O prompt 起始。 |
| 31 | BlocksWorld generator example 与 H-O constraints。 |
| 32 | BlocksWorld H-O constraints、二阶段 prompt 的“target OpenStacks”错写、ChildSnack Planner prompt。 |
| 33 | ChildSnack regular Formalizer 与 H-O prompt 起始。 |
| 34 | ChildSnack H-O generator example。 |
| 35 | ChildSnack H-O constraints 与 second-stage 起始。 |
| 36 | ChildSnack domain-specific error checklist、OpenStacks Planner prompt。 |
| 37 | OpenStacks regular Formalizer 与 H-O prompt 起始。 |
| 38 | OpenStacks H-O generator example。 |
| 39 | OpenStacks H-O constraints。 |
| 40 | OpenStacks second-stage checklist、Transport Planner/Regular Formalizer 起始。 |
| 41 | Transport regular Formalizer constraints 与 H-O prompt 起始。 |
| 42 | Transport H-O generator example。 |
| 43 | Transport H-O constraints 与 domain-specific second-stage checklist。 |
| 44 | Transport second-stage prompt 结束。 |

- `[AUTHOR_FACT]` 可视 PDF 中 Figure 5、Figure 6、Figure 7、Table 1 和 Listings 均存在，页序与正文引用一致。
- `[READER_INTERPRETATION]` 未发现会改变上述科研判断的解析文本/可视 PDF 冲突。PyMuPDF 在物理页 2、4、6–7 的若干位置没有抽出 stylized benchmark 名称，但物理页 5 正文可抽出 `Domains-Unravel dataset`；这属于局部文本抽取缺失，不应以抽取空白作为论文原文缺词的证据。

## 7. Reconciliation 建议（不作裁决）

- `[READER_INTERPRETATION]` 后续综合时应把论文结果标为“generator-based formalization exact match”，不要无条件写成“planner scalability”。
- `[READER_INTERPRETATION]` 任何关于 H-O 表示优越性的表述都应附带 two-stage pattern-review confound，并引用 Figure 6 的独立增益。
- `[READER_INTERPRETATION]` 对 synthetic scaling 的引用必须保留 fixed-domain、single-main-parameter、handcrafted-pattern、single-run、guaranteed-solvable 与 parser-oracle 边界。
- `[OPEN_QUESTION]` 若该论文将承担关键机制或基线判断，需另行核验作者代码中的 parser semantics、实际 prompt 调用链、seed/temperature/token budgets、测试批次与 prompt-error-analysis 的隔离，以及是否有真实 planner 运行的逐实例标记；本 fresh read 不越界读取这些材料。
