# P099 独立二读报告（fresh 二读者，W06 扩充波次）

- 论文：Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization
- canonical metadata 对照：arXiv 2605.26457v1 (cs.SE, 2026-05-26)，preprint。实测 PDF 第 1 页左侧竖排水印为 "arXiv:2605.26457v1 [cs.SE] 26 May 2026"，页脚为 "Preprint."，与 canonical 一致。[AUTHOR_FACT]（物理页 p.1，标题页，逐字定位："arXiv:2605.26457v1 [cs.SE] 26 May 2026"）
- 实测 SHA-256：4865494ceedf3da946cc5970d1815b5b534ac0f6793a50dfdf196dca6ec4560d（与任务给定值一致）
- 实测文件字节数：1,892,061 字节
- 实测物理页数：58 页（pymupdf page_count；物理页码与印刷页码一致，p.11 印刷页码即 "11"）
- 抽查方式：pymupdf 全文抽取（58 页全部读毕）；另对 p.1（标题页）、p.8（Figure 4 + 数据统计）、p.10（Figure 5，含 300dpi 局部放大）、p.11（Table 1）、p.37（Table 4）做了视觉 Read 抽查。

标签纪律说明：每条内容陈述恰用一个标签 [AUTHOR_FACT] / [READER_INTERPRETATION] / [OPEN_QUESTION]，并给出物理页码 + 章节/图表 + 短逐字定位语。

---

## 1) 方法究竟改变哪一步计算？

1.1 [READER_INTERPRETATION] 这是一篇基准 + 环境 + 评测器论文，不改动模型训练或解码；它改变的计算步骤是"规格忠实性(specification faithfulness)的评测计算"：从（i）与专家参考规格比对或（ii）LLM 判官打分，改为对生成规格在具体测例上做确定性的接受/拒绝判定。（依据 p.2–3, §1；p.6, §2.2）

1.2 [AUTHOR_FACT] 具体机制一：作者扩展 Verus 的 exec_spec 机制，把生成的逻辑规格编译成可执行 Rust 函数以便在具体输入上运行。（p.3, §1，"extending Verus's exec_spec mechanism (§2.2) to compile each generated specification into a Rust function"）

1.3 [AUTHOR_FACT] 具体机制二：每个测例先做符号检查（把测例作为 Verus 断言插入并跑验证器，completeness 用 assert(pre_spec(x))/assert(post_spec(x,y))，soundness 用取反断言），验证失败或超时才回退到运行时检查（编译成可执行函数 fs 并比对布尔输出）。（p.6, §2.2，"we use a symbolic check followed by a runtime check"）

1.4 [AUTHOR_FACT] 具体机制三：新增 exec_spec_unverified 宏，生成可执行代码但省去"可执行代码与原规格对应性"的证明，理由是对应性证明可能在可执行代码足以用于测试时仍失败，构成不必要的失败模式；溢出/死循环等错误在运行期以 panic 形式显现。（p.7, §2.2 与 p.24, App C.1，"produces executable Rust code without the correspondence proof"）

1.5 [AUTHOR_FACT] exec_spec 的类型/构造覆盖也被扩展：支持 Seq/Set/Multiset/Map 等 vstd 核心规格类型、其核心方法子集（如 Seq::subrange、Set::contains）、以及多变量有界量词。（p.7, §2.2 与 p.26, App C.3，"sequences, sets, multisets, and maps"）

1.6 [AUTHOR_FACT] 另一处被改变的计算是"任务本身"：agent 在交互环境（Verus、bash、文件系统）中填写 pre_spec/post_spec 两个规格洞，而非一次性生成；环境与 Harbor 集成。（p.3, §1，"integrates with Harbor"；p.10, §3.2）

1.7 [READER_INTERPRETATION] 汇总：论文没有提出新的规格生成方法；它改变的是评测端的判定函数（reference/LLM-judge → 四桶测例 + 符号/执行两级判定，Fig 6 六种 resolution 类别），以及数据端的测例来源（官方测试 + 人写 hacks 经平台裁决路由入四桶，Fig 4）。（p.8 Fig 4；p.13 Fig 6）

## 2) 输入、输出、可用信息与干预时点分别是什么？

2.1 [AUTHOR_FACT] 输入（每个任务给 agent）：非正式 Codeforces 题面 sI、固定 In1/Out 类型的 Verus 骨架 solve.rs（含待填的 pre_spec/post_spec 空体）、来自 completeness 桶的 3 个样例测例（soundness 桶不给样例）、一个别的题的完整规格 worked example、Verus 文档（含 exec_spec 指南）、Verus 源码、评测器源码、以及 Verus 专家撰写的详细任务提示（App H 全文）。（p.10–11, §3.2 "Additional materials"；p.10，"three sample testcases drawn from the completeness buckets, and no sample testcases from the soundness buckets"）

2.2 [AUTHOR_FACT] 输出：pre_spec 与 post_spec 的函数体（允许自定义 helper spec/proof 函数），另有四个可选的 *_proof 证明辅助函数体；不得改动类型定义、check_* 包装器结构、__PASTE__ 标记与断言行。（p.10, §3.2；p.22, App B.2 骨架；p.54, App H §2 "you may edit"）

2.3 [AUTHOR_FACT] 可用信息/反馈通道：agent 可随时运行 verus_gym_specgen_check，在可见样例测例上得到含 Verus 错误信息的反馈（写入 /home/attempts）；最终评分用隐藏测例套件，规格须通过全部四桶（可见+隐藏）所有测例才算正确。（p.10, §3.2，"A separate, larger set of testcases is hidden from the agent"）

2.4 [AUTHOR_FACT] 干预时点/终止条件：rollout 在 agent 调用 submit、预算耗尽或超 75 分钟超时时结束；每题预算 $2.5；SWE-AGENT 框架下另有每题 400 次 API 调用上限（Table 1 的分组标签只把 "max 400 steps" 标在开源模型组）。（p.10, §3.2；p.11, Table 1 题注 "a budget of $2.5 per problem"；p.30–31, App F，"a limit of 400 API calls per problem"）

2.5 [OPEN_QUESTION] App F（p.30–31）写 "For SWE-AGENT, we additionally impose a limit of 400 API calls per problem"（未限定开源），而 Table 1（p.11）仅在开源组标注 "max 400 steps, $2.5 cost cap"；闭源模型是否同样受 400 步上限约束，原文两处表述不一致，无法在文内裁决。

2.6 [AUTHOR_FACT] 评测端的输入是提交的规格 + 具体测例（由 parser R 从 Codeforces 原始文本转换成的类型化 Verus/Rust 值，须通过字节级 round-trip P(R(t)) == t）；输出是每测例六类 resolution 之一（compile-or-syntax-error / accept-via-symbolic / reject-via-symbolic / accept-via-exec / reject-via-exec / indeterminate-during-exec），再按桶极性映射为对/错。（p.7, §3.1，"Treproduced = P(R(t)) == t"；p.13, Fig 6 及其题注）

## 3) 最强基线与最接近组合基线是什么？

3.1 [AUTHOR_FACT] 被评模型层面：六个模型统一在 SWE-AGENT 下评测；最强为 gemini-3.1pro（Pass@1 0.778），其后 gpt5.3-codex 0.578、opus4.6 0.511；开源 deepseek-v4pro 0.243、glm-5.1 0.215、kimi-k2.6 0.255。（p.11, Table 1 与 §4.2；视觉抽查确认表内全部 24 个数值与解析文本一致）

3.2 [AUTHOR_FACT] 评测方法层面的对照基线是 LLM-as-a-judge：用 gpt5.3-codex 判断它自己生成的规格（给题面 + 少量原始测例及其 Verus 表示 + 待评规格），在 527 个 compile-clean 规格上与本文评测器比对；判官把 191 个评测器判错的规格中的 49 个（25.7%）标为正确。（p.12, §4.3 与 p.37, F.7 + Table 4，"it marked 49 of 191 incorrect but compilable specifications as correct"）

3.3 [AUTHOR_FACT] 另一个内部对照是"只用 completeness 测例评测"（Pass@1-Comp. 列）：加入 soundness 测例后 gpt5.3-codex 从 77% 降到 58%、gemini-3.1pro 82%→78%、opus4.6 59%→51%。（p.12, §4.3，"pass@1 drops from 77% to 58% for gpt5.3-codex"）

3.4 [READER_INTERPRETATION] 没有"最接近组合基线"的实证比较：论文未在同一任务集上运行参考规格比对法（如 VERINA 式）或"LLM 判官 + 测例"混合评测；与相关工作的对比仅为 Table 2（p.14）的八维定性勾选表。LLM-judge 基线也只覆盖 gpt5.3-codex 自评这一配置，未测跨模型判官或带工具判官。

3.5 [AUTHOR_FACT] 与普通代码生成的对照（非基线而是能力对照）：在 gpt5.3-codex 规格失败且每输入唯一正确输出、且有代码生成记录的 187 题上，同一模型用 Python 解出 153 题（81.8%）。（p.11, §4.2 与 p.36, F.6，"code-generation success rate of 81.8% on this subset"）

## 4) 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

4.1 [AUTHOR_FACT] 作者自己指出预算型评测受 API 层细节影响：API 延迟决定 75 分钟墙钟内能完成的交互轮数；美元预算消耗依赖各家 prompt-cache 定价与缓存命中率。（p.31, App F，"dollar-budget consumption depends partly on prompt-cache behavior"）

4.2 [READER_INTERPRETATION] 因此跨模型 Pass@1 排名部分混杂了非能力因素：同样 $2.5 在不同定价下对应不同 token 量；延迟高的模型有效交互轮数更少；若 400 步上限确实只施加于开源组（见 2.5），则闭源/开源对比还叠加步数不对称。这些不影响"任务对所有模型都难"的定性结论，但影响模型间量的比较。

4.3 [AUTHOR_FACT] prompt 与工具对所有模型一致：同一 SWE-AGENT 脚手架、同一 App H 专家提示、同一工具集（文件系统、shell、verus_gym_specgen_check、submit）；作者称材料与提示旨在让失败更多反映规格化难度而非 Verus 语法不熟。（p.11, §3.2，"rather than unfamiliarity with Verus syntax"）

4.4 [AUTHOR_FACT] 但作者也承认部分模型差距来自能否停留在 Verus/exec_spec 支持的语言片段内：弱模型多个桶被 compile/syntax error 主导。（p.12, §4.3 与 p.33, F.2 + Figure 15，"dominated by compile/syntax errors in several buckets"）

4.5 [READER_INTERPRETATION] oracle 层面：四桶标签来自 Codeforces 平台产物（validator/checker 裁决 + hack 元数据的 regex 过滤，p.27–28, App D Stage 3），并经字节级 round-trip 转换；这条链路可信度较高，但仍是有限测例近似（作者明言，见 5.2），且 "Incorrect as per Benchmark testcases" 本身是近似真值——Table 4 题注用 "as approximated by benchmark testcases" 自我限定（p.37）。

4.6 [READER_INTERPRETATION] F.6 的"代码易、规格难"对照存在任务不对等：代码生成用 Python 且按官方测例判分，规格生成用 Verus 且按四桶（含对抗 hacks）判分；语言熟悉度与测试强度都不同，81.8% 与 57.8% 不是同一把尺子上的读数。作者的措辞（"many failures are not explained by an inability to solve the underlying Codeforces problem"）限定得当，但更强的解读需谨慎。

4.7 [AUTHOR_FACT] 判官实验的设置差异：判官是静态一次性分类（prompt 内给题面+少量测例+规格），没有执行工具；且是自评（同模型）。（p.37, F.7，"We asked gpt5.3-codex to act as a judge for specifications generated by the same model"）

4.8 [READER_INTERPRETATION] 因此"判官漏检 26%"证明的是"无执行的 LLM 判断会漏掉可执行测试能抓的错"，不排除更强判官配置（跨模型、带执行工具、多数投票）能缩小差距——这些配置未测。

## 5) 作者明示限制、负向结果和未测试边界是什么？

5.1 [AUTHOR_FACT] 明示限制一：只覆盖单文件竞赛式问题；仓库级、多文件真实软件的规格化未涉及。（p.15, §6 Limitations，"This work focuses on single-file competition-style problems."）

5.2 [AUTHOR_FACT] 明示限制二：忠实性评测仍是近似——有限测试套件能暴露很多规格错误但不能排除所有错误。（p.15, §6，"they cannot rule out all possible errors"）

5.3 [AUTHOR_FACT] 负向结果一：LLM 判官在 25.7% 的可编译错误规格上误判为正确（49/191）。（p.37, Table 4）

5.4 [AUTHOR_FACT] 负向结果二：gpt5.3-codex 三次独立运行 0.578/0.559/0.566，pass@3=0.756（439/581）但 pass3 仅 202/581=34.8%，规格生成跨尝试脆弱。（p.35, F.4，"only 202 of 581 problems (34.8%) are solved by all three attempts"）

5.5 [AUTHOR_FACT] 负向结果三：最容易档（rating 600–900）最好的模型也只到 0.90；难度上升性能单调下降（gemini 至 2400–2700 档为 0.50，gpt5.3-codex 同区间 0.73→0.27）。（p.32, F.1 与 p.33, Figure 14，"solves only 90%"）

5.6 [AUTHOR_FACT] 数据边界（构建期过滤）：排除浮点问题（Verus 不支持浮点推理）、排除早于 hack 系统的老赛题、丢弃截断/重复测例、regex 过滤句法性无效 hack、每桶不足 5 例的题被剔除、每桶超 200 例随机抽 200；源头 10k 题最终取样 581 题。（p.27–29, App D，"We collect 10k problems"；"If any bucket exceeds 200 test cases, we randomly sample 200 from it."）

5.7 [AUTHOR_FACT] F.8 的测例预算分析是均匀子抽样下的回溯计算（桶间独立性假设），非重新跑基准；结论是小预算已近饱和、post-completeness 桶饱和最慢（m≈50–75）。（p.37, F.8，"an exact retrospective calculation under uniform subsampling"）

5.8 [READER_INTERPRETATION] 未测试边界（原文未做）：非 Codeforces 域的规格化；参考规格评测与本评测器在同题上的头对头；判官换模型/加工具；开源模型在更高预算下的表现；exec_spec 不支持片段（如 int/nat 作字段、非有界量词）对可表达规格空间的影响只以 "≥86% 的题至少有一个模型写出全通过的 exec_spec 兼容规格"（p.12, §4.3）做了单向佐证。

5.9 [AUTHOR_FACT] 覆盖性佐证原文：至少 86% 的基准题存在某个被评模型写出的 exec_spec 兼容且全测例通过的规格。（p.12, §4.3，"for at least 86% of benchmark problems"）

## 6) 哪些内容可抽取为 Operator，哪些是真实可记录的 Failure？

Operator 候选（均为我的抽象，锚定作者事实）：

6.1 [READER_INTERPRETATION] Op-可执行规格评测：把面向验证器的逻辑谓词编译为可执行代码，使"规格是否接受具体测例"变成确定性运行时判定；两级流水（先符号证明、失败再执行）兼得可证明性与可判定性。（锚定 p.6 §2.2、p.13 Fig 6）

6.2 [READER_INTERPRETATION] Op-去证明化降噪：当生成物只用于测试而非并入已验证系统时，砍掉对应性证明（exec_spec_unverified）以消除评测器自身的伪失败模式。这个"按用途裁剪保证强度"的手法可迁移到其他形式化评测。（锚定 p.7 §2.2、p.24 App C.1）

6.3 [READER_INTERPRETATION] Op-人类对抗产物再利用：把平台上人写 hacks 按平台裁决（validator/checker）自动路由进 pre/post × sound/complete 四桶，获得 LLM 难以自产的贴身反例；作者引 Sinha et al. 2025 支持"LLM 难造反例"。（锚定 p.8 §3.1 + Fig 4）

6.4 [READER_INTERPRETATION] Op-字节级 round-trip 转换验收：agent 写 parser R 与 printer P，仅当 P(R(t)) == t 字节相等才接受转换，防止评错具体测例；失败反馈回 agent 迭代。（锚定 p.7–8 §3.1、p.9 Fig 3）

6.5 [READER_INTERPRETATION] Op-四桶分解：把"规格忠实"拆成 pre/post × soundness/completeness 四个可分别测量的方向，并用 Pass@1 与 Pass@1-Comp 之差量化 soundness 测试的必要性。（锚定 p.5–6 §2.1、p.11 Table 1、p.12 §4.3）

6.6 [READER_INTERPRETATION] Op-回溯子抽样预算审计：用超几何公式 1−C(P,k)/C(T,k) 离线估计更小测例预算的漏检率，论证测试套件规模是否够用。（锚定 p.37 F.8）

真实可记录的 Failure（作者报告的具体失败）：

6.7 [AUTHOR_FACT] F-规格失败三模式：遗漏输入假设（1028C 漏 "n−1 个矩形有公共点"，gpt5.3-codex 与 gemini-3.1pro 都中招，p.47–48 G.3 + Table 8）；接受错误输出（1051B 用"非同偶"替代 gcd=1，接受 (3,6)，p.40–41 G.1 + Table 5；1027C 漏最优性、kimi 只查形状/越界值，p.42–45 G.2 + Table 6/7）；拒绝正确输出（2074D gemini 的区间并规格拒绝正确计数 13，opus4.6 用更简单的按列刻画通过，p.49–51 G.4 + Table 9）。（§4.3 "Failure modes" p.14 总括）

6.8 [AUTHOR_FACT] F-过度规格化是独立失败模式：2074D 上"更复杂的规格"本身导致 post-completeness 失败，与欠规格化相对。（p.35, F.3，"over-specification is itself a failure mode distinct from under-specification"）

6.9 [AUTHOR_FACT] F-判官假接受：49 例评测器有具体反例而判官仍判对。（p.37 Table 4）

6.10 [AUTHOR_FACT] F-片段逃逸：deepseek-v4pro/glm-5.1/kimi-k2.6 多个桶被 compile/syntax error 主导。（p.12 §4.3、p.34 Figure 15）

6.11 [AUTHOR_FACT] F-符号可证但语义错：gpt5.3-codex 在 soundness 桶有一条不小的"符号解析但判定与桶标签相反"带，即 Verus 能证明其规格行为、且该行为与预期裁决相悖——是规格的具体语义错误而非评测器无法解析。（p.33–34, F.2，"concrete semantic failures in the generated specification"）

6.12 [AUTHOR_FACT] F-原版 exec_spec 的对应性证明会在可执行代码本可用于测试时失败（作者作为动机记录的工具链失败模式）。（p.7 §2.2，"the correspondence proof may fail even when the executable code is sufficient"）

## 7) 每项判断对应哪个物理页码、章节、图表和短逐字定位语？

（正文各条已内嵌锚点；此处再给核心数字的集中对照表。物理页码=印刷页码。）

- 581 任务、六模型、77.8%/51.1–57.8%/21.5–25.5%、判官漏 26%：p.1 Abstract，"solves 77.8% of tasks"。
- 四桶定义 τpre-comp/τpre-sound/τpost-comp/τpost-sound：p.6 §2.1，"four buckets of testcases"。
- 符号→执行两级检查：p.6 §2.2，"a symbolic check followed by a runtime check"。
- exec_spec_unverified 设计：p.7 §2.2 与 p.24 App C.1。
- 构建 agent = gpt5.3-codex inside SWE-AGENT；round-trip 验收：p.7 §3.1，"(gpt5.3-codex inside SWE-AGENT)"。
- hack 路由规则：p.8 Fig 4 与 p.27 App D Stage 3。
- 每桶均值 21/80/55/78、每桶至少 5 例：p.8 "Dataset statistics"。
- 每桶中位数 12/97/29/93：p.10 Figure 5 题注。
- 3 个样例仅出自 completeness 桶；隐藏测例；75 分钟：p.10 §3.2。
- Table 1 全部数值、$2.5/题：p.11（已视觉核对）。
- soundness 消融 77→58 / 82→78 / 59→51：p.12 §4.3。
- ≥86% 覆盖性佐证：p.12 §4.3。
- 六类 resolution 决策树：p.13 Figure 6。
- 相关工作八维对照：p.14 Table 2。
- 限制（单文件、有限测试）：p.15 §6 Limitations。
- 10k 题源、无浮点、regex 过滤句法 hack、200 上限、581 取样：p.27–29 App D。
- rating 800–2700、中位 1200、均值 1289：p.29 App E 与 p.30 Figure 10。
- $2.5 + 400 API 调用 + Modal/Docker 4CPU/8GB + API 延迟与缓存告诫：p.30–31 App F。
- 难度分层（0.90→0.50 等）：p.32 F.1 与 p.33 Figure 14。
- 解析分布 Figure 15：p.34。
- pass@3 0.756 / pass3 34.8%：p.35 F.4。
- 三模型并集 486/581、共同核 214、gemini 独解 84：p.35–36 F.5 与 Figure 16。
- 245 错误规格、197 唯一输出、187 有代码运行、153 解出 81.8%：p.36 F.6。
- Table 4 混淆矩阵 310/49/26/142，54 个不编译者被排除：p.37 F.7（已视觉核对）。
- F.8 回溯子抽样公式与收敛点：p.37–39，Figure 17/18。
- 案例研究 1051B/1027C/1028C/2074D：p.40–51，App G，Table 5–9，Listing 1–7。
- App H 完整提示（工作区布局、可编辑范围、评测流程说明）：p.52–58。

## 8) 解析文本与可视 PDF 是否冲突（就抽查过的页面回答）？

8.1 [READER_INTERPRETATION] 就我视觉抽查的 p.1、p.8、p.10（含 Figure 5 放大）、p.11、p.37 而言，pymupdf 解析文本与渲染页面无冲突：Table 1 的 24 个数值、Table 4 的四格数值与百分比、标题页水印与作者名单、Figure 5 题注中位数均逐一吻合。多栏图表（Fig 2、Fig 3、Table 5–9）的文本抽取存在阅读顺序交错，但内容无缺失或讹变。

8.2 [AUTHOR_FACT] 视觉抽查发现一处论文内部（非解析层）小不一致：p.8 正文写每题平均 "21 pre-sound"，而 p.10 Figure 5 的 pre_sound 面板标注 "Mean: 20"（其余三桶 80/55/78 与图内 80/55/78 一致）。（p.8 "Dataset statistics" vs p.10 Figure 5 面板标注，放大图核实）

8.3 [OPEN_QUESTION] Figure 5 显示两个 soundness 桶 Max: 200（与 App D "超 200 抽 200" 一致），但两个 completeness 桶 Max: 100 且直方图在 100 处堆积（pre_complete 约 290 题、post_complete 约 285 题贴在 100），暗示 completeness 桶实际存在 100 的上限或来源侧截断；正文只写了 200 的上限（p.29），未解释 100 这个值。无法在文内裁决是"官方测试恰好不超 100"还是存在未记载的额外抽样上限。

8.4 [READER_INTERPRETATION] Figure 5 右上角有排版残留小字 "last update: 2026-05-25 12:54 UTC"（图产状态戳），不影响内容，但表明图为自动流水线产出。（p.10，放大图可见）

8.5 [OPEN_QUESTION] 摘要与 §1 说开源模型区间 "21.5–25.5%"，Table 1 开源三行为 0.243/0.215/0.255——区间端点取的是 glm-5.1 与 kimi-k2.6，deepseek 0.243 在区间内，表述一致；但 "51.1–57.8%" 描述"其他前沿模型"仅含 opus4.6 与 gpt5.3-codex 两个点。此为表述粒度问题而非矛盾，记录备查。（p.1 Abstract vs p.11 Table 1）

---

报告完。本报告基于对 58 页全文抽取与上述页面的视觉抽查独立完成，未读取任何被禁材料。
