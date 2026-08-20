# PLAN_05 Card source audit E 报告

- Audit ID：`plan05-audit-e`
- 角色：fresh independent source-to-Card auditor；不是 Commissioning Reviewer，不评价 Candidate。
- 审计边界：仅审计 invocation 冻结的 3 张 Card、canonical `evidence.json` 与 P053/P054/P055 PDF；未联网。
- 冻结性检查：invocation 列出的 7 个 SHA-256 均与本地实际文件匹配。
- 判定口径：`PASS` 表示原文直接支撑或综合明确保持在来源边界内；`NARROW` 表示核心方向可保留但措辞、条件或评估边界必须收窄；`REJECT` 表示当前冻结来源不支持该主张。

## 1. `operator-higher-order-generative-formalization.md`

### 1.1 AUTHOR_FACT

| 判定 | Card 段落 | Evidence ID | PDF 页/短定位 | 核查与最小修订建议 |
|---|---|---|---|---|
| PASS | `Before and after computation`：“普通 Formalizer 直接输出完整 grounded instance；改变后……generator program……生成 PDDL problem file” | `ev-p053-higher-order-generator`; `ev-p053-python-to-pddl-pipeline` | P053 物理 p4，§3.1，`Instead of directly outputting...`; p6，§3.3，`generate Python programs that produce PDDL problem files` | 两段原文共同直接支撑表示改变和 Python→PDDL 执行链。无需修改。 |

### 1.2 CODEX_SYNTHESIS / HYPOTHESIS 边界攻击

| 判定 | Card 段落 | Evidence ID | PDF 页/短定位 | 核查与最小修订建议 |
|---|---|---|---|---|
| PASS | `Intervention target` | `ev-p053-higher-order-generator` | P053 p4，§3.1，`|Dn| << |In|` 与 `explicitly emit...facts` | “短描述—大 grounded instance—避免逐项枚举”是原文定义的 compression gap，没有扩写成普遍 Agent planning 规律。 |
| PASS | `Inputs outputs information and timing` | `ev-p053-python-to-pddl-pipeline`; `ev-p053-higher-order-generator` | P053 p3，§2.2，Formalizer→PDDL→planner；p6，§3.3，NL domain/problem + ground-truth domain file→Python→PDDL | 输入、IR、最终 grounded instance 及 solver 前时序均可回溯。“可信”是对原文 `ground-truth PDDL domain files` 的保守改写。 |
| PASS | `Mechanism hypothesis` | `ev-p053-higher-order-generator` | P053 p4，§3.1，`|Rn| << |Fn|` 与从枚举转向 generation rule | 已标为 `[CODEX_HYPOTHESIS]`，且只提出可检验的输出复杂度机制，没有冒充作者实验结论。 |
| NARROW | `Predicted observable signature` 末句“论文当前系统没有隔离 review” | `ev-p053-pattern-review-confound` | P053 p6，§3.3，H-O 为 two-stage、Planner/Formalizer 为 single-stage；p8，§5/Fig. 6，Q25 另有去除 pattern review 的 ablation | 主 H-O vs Formalizer 比较确实没有 matched-review 隔离，但论文并非完全没有 review ablation：p8 单独报告 Q25 pattern-review ablation。最小改为：“主 H-O/普通 Formalizer 对比未匹配 review；论文另在 Q25 上消融 pattern review，但未给出四臂 matched-budget 分解。” |
| PASS | `Preconditions and transfer risks` 中 parser/planning 边界 | `ev-p053-parser-evaluation-boundary` | P053 p3，§2.2，planner timeout 后用 parser 比较 generated 与 ground-truth PDDL，并在 BlocksWorld 可解假设下计作 valid plan | Card 正确保留了“文件 exact match 不等于实际 planner 在该规模完成搜索”的边界。无需修改。 |
| NARROW | `Source lineage` | 当前 Card 无对应 Evidence；冻结 PDF 可核 P054→P053，但不可核 P051/P052 | P054 p2/Fig. 1：NL→完整 Domain/Problem PDDL→planner；P053 p4，§3.1：改为 generator representation | “P054 complete PDDL Formalizer→P053 generator”有源；“与 P051/P052 相邻”在本 Card 没有 Evidence 引用，且不在本审计可读来源内。最小删除 P051/P052 句，或以后添加可回溯 Evidence 再恢复。 |
| PASS | `Evidence ledger` | `ev-p053-higher-order-generator`; `ev-p053-python-to-pddl-pipeline`; `ev-p053-pattern-review-confound` | P053 p4、p6、p8 | 把 representation change 作为 Operator、把 pattern review 作为混杂而非第二 Operator，是保守拆分；但应同时采用上面的 ablation 限定。 |
| PASS | `Retrieval vocabulary` | 不适用（检索词，不是事实主张） | 与 P053 p3–p4、p6、p9 术语一致 | 无需修改。 |

## 2. `failure-grounded-formalization-output-expansion.md`

### 2.1 AUTHOR_FACT

| 判定 | Card 段落 | Evidence ID | PDF 页/短定位 | 核查与最小修订建议 |
|---|---|---|---|---|
| PASS | `Observed failure` | `ev-p053-higher-order-generator` | P053 p4，§3.1，compact `Dn` 对应更大的 `In`；普通 Formalizer 必须显式产生大量 facts | 原文定义包含 objects/fluents/initial/goal 等 grounded instance 成分，并明确把枚举负担放在普通 Formalizer 上。无需修改。 |
| PASS | `Evidence and alternative explanations` | `ev-p053-pattern-review-confound` | P053 p6，§3.3，two-stage pattern reflection 与普通 Formalizer 的 single-stage 不同；p8/Fig. 6，pattern review 提升 Q25 | “改进可能同时来自表示压缩与额外检查预算”是由明确设计差异和单独 review 增益支持的混杂判断。无需修改；可补一句“主比较未 matched review”。 |

### 2.2 CODEX_SYNTHESIS / HYPOTHESIS 边界攻击

| 判定 | Card 段落 | Evidence ID | PDF 页/短定位 | 核查与最小修订建议 |
|---|---|---|---|---|
| PASS | `Conditions and scope` | `ev-p053-higher-order-generator` | P053 p4–p5，§3.1–3.2，unraveling problems 由紧凑规则展开；p9，§8 限于 fixed-domain classical symbolic planning | Card 没有把 failure 混成 solver 搜索失败或一般语言遗漏，范围合理。 |
| NARROW | `Failed intervention` 前半：“仅提高 context window……增加无结构 reflection” | `ev-p053-parser-evaluation-boundary` 只直接支撑 planner timeout；没有直接支撑这些干预“失败” | P053 p4 报告 D&C 缓解 context overload；p8/Fig. 6 报告 pattern review 增益；p3 报告 planner timeout | “不改变输出展开位置”是结构判断，但标题下容易被读成“这些手段无效”，而论文反而观察到 D&C/review 有益。最小改为：“这些手段即使提高准确率，也不单独证明已消除输出展开瓶颈；planner 仍可能 timeout。” |
| PASS | `Warning for future candidates` | `ev-p053-pattern-review-confound`; `ev-p053-parser-evaluation-boundary` | P053 p3、p6、p8 | parser/planning 与 representation/review 两个混杂均被正确分开；四臂设计是明确的审计建议，不是伪装成作者实验。 |
| PASS | `Possible repair boundary` | `ev-p053-higher-order-generator` | P053 p4，compiler/interpreter/lifted planner；p9，未来更 principled IR/compilation | 已标为 hypothesis，且核心是改变中间表示或展开位置。`constraint template` 是举例而非已验证结论。 |
| PASS | `Evidence ledger` | `ev-p053-higher-order-generator`; `ev-p053-parser-evaluation-boundary` | P053 p5 数据构造；p9，§8 limitations | fixed-domain、synthetic、规则展开和不外推到所有 Agent planning 均保守。 |
| PASS | `Retrieval vocabulary` | 不适用 | 与 P053 的 compression gap、generator、planner timeout 术语一致 | 无需修改。 |

## 3. `failure-constraint-shift-breaks-formalization.md`

### 3.1 AUTHOR_FACT

| 判定 | Card 段落 | Evidence ID | PDF 页/短定位 | 核查与最小修订建议 |
|---|---|---|---|---|
| NARROW | `Observed failure` 第一事实：“在 CoPE 中，一个短约束就显著降低 direct planning 与 formalization 表现” | `ev-p055-constraint-performance-drop` | P055 p7，§6，作者概括 one-line constraints 显著削弱 planning/formalization；p6/Fig. 2–3，存在 `+25`、`+0` 等非下降单元 | 来源支持 CoPE 的总体/多数设置结论，但不支持“任意一个约束、每个方法/模型/单元都下降”。作者的“over all cases”紧接的是 planning，不宜平移成 formalization 全表普遍规律。最小改为：“在 CoPE 的总体结果中，作者报告短约束显著削弱 direct planning 与 formalization；但并非每个模型×方法×形式体系单元都下降。” |
| PASS | `Observed failure` 第二事实：自然描述遗漏 `clear` | `ev-p054-natural-language-implicit-predicate-failure` | P054 p7，§5.3，Natural BlocksWorld 未显式给 `clear`，模型常遗漏，导致 unsolvable PDDL 或 incorrect plans | Card 准确保留了 implicit predicate、具体例子与后果。无需修改。 |
| PASS | `Conditions and scope` | `ev-p055-constraint-formalism-taxonomy` | P055 p4，§3/Table 1 后：四类 constraint；不同 formalism 需不同修改；四类并集不被任一 formalism trivialize | 原文直接支撑。Card 的“没有单一 formalism 平凡覆盖全部类别”准确，不等于声称不能表达。 |
| NARROW | `Evidence and alternative explanations` 第一事实：“formalizer 最多获得三次错误驱动代码修订” | `ev-p055-three-revision-budget` | P055 p5，§5：Revision 可 `up to 3 tries`，基于执行返回的 error message（如有）；随后又称 Formalizer 有 3 attempts 写出 syntactically correct PDDL，`not re-plan` | 核心预算边界正确，但“3 次 revision”可能被误读为“初次生成之外再修 3 次”，且并非每次都有错误消息。最小改为：“Revision 条件下 formalizer 最多有 3 次代码尝试/修订机会，按执行错误消息（如有）再生成；这是语法修复，不是重新规划。” |
| PASS | `Evidence and alternative explanations` 第二事实：“主实验每域只用 100 个代表配对” | `ev-p055-representative-subset-boundary` | P055 p5，§4：完整组合 10,000；手工将每个 constraint 配一个 representative problem，得到每域 100 | 精确保留了从完整组合到 representative subset 的边界。可把“100 个代表配对”写成“100 个 constraint–problem 手工配对”以更清楚，但非必须。 |
| PASS | `Evidence and alternative explanations` 第三事实：plan correctness 假阳性与 20 样本抽查 | `ev-p055-plan-correctness-false-positive-boundary` | P055 p10，§8 Limitation：正确 plan 可能来自不忠实 code；只分析来自所有 datasets/methods 的 20 samples | Card 没有接受论文由 20 个零假阳性样本推出“negligible”的扩张。为最完整保留边界，可加“20 个 pooled samples（跨所有 datasets/methods），不是每组 20 个”。 |

### 3.2 CODEX_SYNTHESIS / HYPOTHESIS 边界攻击

| 判定 | Card 段落 | Evidence ID | PDF 页/短定位 | 核查与最小修订建议 |
|---|---|---|---|---|
| PASS | `Failed intervention` | `ev-p055-plan-correctness-false-positive-boundary`; `ev-p054-natural-language-implicit-predicate-failure` | P055 p10；P054 p7 | “solver 只能验证实际写入模型”准确解释了遗漏约束/隐式 predicate 时的验证边界，没有声称 solver 本身错误。 |
| NARROW | `Warning for future candidates` | `ev-p055-plan-correctness-false-positive-boundary`; `ev-p055-three-revision-budget`; `ev-p055-constraint-formalism-taxonomy` | P055 p4、p5、p10 | solver/syntax/final-plan accuracy 不足以单独证明 faithfulness，以及应报告 formalism/toolchain/revision/category，均有来源或直接逻辑支撑；但本 Card 引用链没有直接支撑“必须公开 horizon”。最小删除 `horizon`，或以后另加可回溯 Evidence。 |
| PASS | `Possible repair boundary` | 相关 Evidence 仅界定问题；本段明确标为 hypothesis | P055 p4、p7、p10 | “constraint coverage / semantic decomposition / 独立规格核查”是窄研究假设，没有冒充作者已验证方法；也明确排除环境反馈学习/执行恢复外推。 |
| PASS | `Evidence ledger` | `ev-p054-natural-language-implicit-predicate-failure`; `ev-p055-constraint-performance-drop`; `ev-p055-plan-correctness-false-positive-boundary` | P054 p7；P055 p6–p7、p10 | 该段主动写明“不声称所有表格单元都下降”和“不把 20 样本零假阳性扩写成可靠 evaluator”，恰好修复了两个最危险的来源越界。建议把相同限定上移到 `Observed failure`，避免读者只看首段时误读。 |
| PASS | `Retrieval vocabulary` | 不适用 | 与 P054/P055 原文术语一致 | 无需修改。 |

## 4. 总体结论

### 4.1 AUTHOR_FACT 汇总

- 共核查 9 个独立 AUTHOR_FACT 原子项：7 个 `PASS`，2 个 `NARROW`，0 个 `REJECT`。
- 两个 `NARROW` 分别是：P055 降幅不能扩成每个 constraint/表格单元的普遍下降；P055 “三次 revision”必须保留 `up to 3 tries`、错误触发和 `not re-plan` 语义。同一 20-sample 事实判为 `PASS`，但仍建议显式写成跨 datasets/methods 的 pooled 20 samples。
- P054 implicit-`clear` Failure 为直接、准确、可定位的作者失败事实。
- P053 generator representation、Python→PDDL pipeline、pattern-review 混杂与 parser/planning 边界均有直接原文支持。

### 4.2 综合层结论

- 无需整体拒绝任何 Card；核心 source-to-Card 关系成立。
- 必须收窄 4 个综合段落：P053 主比较与单独 Q25 review ablation 的关系、P051/P052 无 Evidence 的 lineage、把 context/review 放在 `Failed intervention` 下造成的“无效”暗示、P055 warning 中无当前来源支撑的 `horizon`。
- representation gain 不能与额外 pattern-review 预算合并归因；parser exact match 不能替换实际端到端 planner scalability；P055 下降只可作为 CoPE 范围内的总体/多数设置现象；100 representative pairs、最多 3 次代码尝试/修订、pooled 20-sample faithfulness 抽查都必须继续保留。

## 5. 可观察访问轨迹

1. 规则读取（精确路径、`Get-Content -Raw -Encoding UTF8`）：工作区根 `AGENTS.md`、`crl_agent_v3/AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`；`evidence-quality-gate/SKILL.md` 及其 3 个 references；`paper-ingestion-and-evidence-builder/SKILL.md` 及其 3 个 references；本地 `pdf/SKILL.md`。
2. 冻结任务读取：仅 `knowledge_base/corpus/card_audits/plan05-audit-e/invocation.md`。
3. 冻结内容读取：仅 invocation 列出的 3 张 Card 与 `knowledge_base/corpus/evidence.json`；没有枚举 Cards、reads、reconciliation、Corpus Report、blind query 或既有 audit。
4. 完整性检查：仅对 invocation 列出的 7 个冻结输入运行 `Get-FileHash -Algorithm SHA256`；全部匹配。
5. PDF 核源：用受支持环境 `D:\Desktop\crl_judge\crl_agent_v3\.venv\python.exe` 与 PyMuPDF 只读打开 P053/P054/P055；访问的物理页为 P053 p3–p9、P054 p2/p5–p8、P055 p4–p8/p10。主要结论定位于 P053 p3/p4/p6/p8/p9、P054 p2/p7、P055 p4/p5/p6/p7/p10。
6. 解析异常如实记录：第一次 P053 文本输出因控制台 GBK 无法编码数学符号而失败；改设进程级 `PYTHONIOENCODING=utf-8` 后成功。曾尝试把 P055 p6 在内存中渲染为 JPEG/PNG 供图像通道目视复核，但图像通道未能处理；未生成临时文件。图表相关判断因此只使用 PDF 页内可提取的箭头数值、图注与相邻正文，不臆测未读取的曲线高度。
7. 网络：未调用任何网络搜索、下载或外部 API。
8. 写入：仅通过 `apply_patch` 新建本报告；未修改 Card、Evidence、manifest 或其他文件。
