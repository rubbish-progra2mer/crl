# P097 独立二读报告（fresh reader, W06 扩充波次）

- 读者：r2-20260727-p097-a1（独立二读，未接触 read_1 或任何 Card/reconciliation）
- 日期：2026-07-27
- 论文：ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization
- canonical metadata（任务给定）：ReLoop, arXiv 2602.15983v2 (2026-04-29), preprint

## 0. 文件核验

- [AUTHOR_FACT] 实测 SHA-256 = `8563653b872e78822f024b4d2f11532f75354e98c729ed26ac5bbf9675724c66`，与任务指定值完全一致（python hashlib 对 staging/w06_targeted/P097_reloop.pdf 全文件计算）。
- [AUTHOR_FACT] 物理页数 = 39（PyMuPDF page_count）；印刷页码 1–39 与物理页一一对应（p.1 印 "1"，p.36 印 "36"，p.39 印 "39"）。
- [AUTHOR_FACT] p.1 右侧 arXiv 印记逐字为 "arXiv:2602.15983v2  [cs.SE]  29 Apr 2026"，p.1 页脚有 "Preprint." 字样——与 canonical metadata（2602.15983v2, 2026-04-29, preprint）一致。
- [AUTHOR_FACT] PDF 元数据 title 与首页标题一致；作者 6 人（Lian, Sun, Chen, Zhang, Qin, Teo），Northwestern/温州/CityU HK/NUS 联合署名（p.1）。
- [READER_INTERPRETATION] p.37–39 含完整 NeurIPS Paper Checklist，说明该 preprint 按 NeurIPS 投稿格式准备；正文 9 页 + 参考文献（p.10–11）+ 附录 A–H（p.12–36）。
- 视觉抽查页：p.5（Table 2）、p.7（Table 4）、p.8（Table 5/6）、p.9（Table 7）、p.36（Table 23），150 dpi 渲染逐一与抽取文本比对（见第 8 题）。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] ReLoop 不改模型权重、不改解码方式（全部 greedy, temperature 0）、不改求解器；它改变两处："Structured generation decomposes code production into a four-stage reasoning chain (understand, formalize, synthesize, verify)"，以及生成之后加一个外部验证-修复回路 "Behavioral verification detects errors that survive generation by testing whether the formulation responds correctly to solver-based parameter perturbation"（p.1, Abstract）。
- [AUTHOR_FACT] 生成侧：把单次直接代码生成替换为单次 LLM 调用内的四阶段链 x →understand→ U →formalize→ M →synthesize→ Ĉ →verify→ C（Eq. 1, §3.2, p.4），其中 Stage 2 要求显式变量类型推理（"can you order 2.7 pallets?"，p.4），Stage 4 在同一生成调用内自查完备性（p.5）。
- [AUTHOR_FACT] 验证侧：L1 执行验证（阻断层：AST 语法/运行/求解器状态；FATAL 触发带诊断的再生成，最多 N=3 次；INFEASIBLE 附 IIS、UNBOUNDED 附 unbounded ray，§3.3.1, p.5）；L2 行为测试（非阻断，CPT+OPT：对 LLM 抽取的候选约束/目标项施加极端参数扰动，用目标值变化率 r 判定缺失，§3.3.2, p.5–6）；WARNING 触发定向修复并带回归回滚（τr=4%），§3.4, p.6。
- [AUTHOR_FACT] 架构两原则："Only L1 blocks output—L2 provides diagnostics but never discards a valid solution"；"Conservative repair—only high-confidence issues (WARNING) trigger repair"（§3.3, p.5）。完整过程由 Algorithm 1（Appendix E, p.23）形式化：Phase 1 生成+L1 循环，Phase 2 L2 诊断+修复循环（含 skip guard、safety check、regression rollback）。
- [READER_INTERPRETATION] 本质上这是"提示结构 + 执行外环"级别的干预：一个 prompt-level 分解算子加一个 solver-in-the-loop 的验证-修复外循环，二者均无需训练。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 输入："Let x denote a natural-language optimization problem description containing all parameter values."（§3.1, p.3）。评测时每个实例是 data-embedded prompt（"Each instance is presented as a data-embedded prompt with JSON data inline", §4, p.7）。
- [AUTHOR_FACT] 输出：Algorithm 1 的 Ensure 行——"Verified code C, objective z*, solution x*, status, diagnostics D"（p.23）。L2 只产诊断/警告，不会丢弃 L1 已得的可行解（p.5）。
- [AUTHOR_FACT] 可用信息：无 ground truth——L2 是 "an external semantic signal that bypasses LLM self-review and requires no ground truth"（Abstract, p.1）；外部信号 = 求解器对扰动的响应、IIS 约束集、unbounded ray 变量、语法 traceback；L2 抽取阶段 LLM 可见 data 键名列表但不见数值（"provides the list of available data parameter keys (but not values)", E.4, p.30）。
- [AUTHOR_FACT] L2 验证所用 LLM 与生成 LLM 相同（"the constraint/objective extraction uses the same LLM that generates the code", G.1, p.35）。
- [AUTHOR_FACT] 干预时点：(a) 生成时（CoT prompt）；(b) 执行后（L1，FATAL 再生成 ≤N=3）；(c) 得到可行解后（L2 扰动测试 + 修复循环 ≤N=3；Algorithm 1 两个循环, p.23）。扰动因子按类型：capacity ×0.001、demand ×100、其他 ×0.01；cost ×0.001、revenue ×100（§3.3.2 p.6；E.4/E.5 p.31–32）。阈值：r<5% WARNING、5–30% INFO、>30% 或 infeasible PASS（Table 2, p.5；E.4, p.31）。
- [AUTHOR_FACT] 扰动的实现前提：代码通过 data["key"] 访问运行时数据字典（Stage 3, p.5 "it is essential for L2's perturbation testing"）；抽取失败则回退自包含代码 + AST 源码扰动（E.2 p.28；E.4 p.31 "falls back to AST-based source-code perturbation"）。
- [READER_INTERPRETATION] 干预全部发生在推理期、单实例内、无跨实例记忆；额外成本为 "∼3× base cost in LLM tokens"（§5.1, p.7）。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 论文自设三配置：Base（直接生成/SFT-RL 模型用其自有格式）、CoT（四阶段结构化）、ReLoop（CoT + L1–L2 + 修复, N=3）（§5.1, p.7）。消融表 Table 7（p.9）给出递增链：Direct → +CoT → +CoT+L1 → +CoT+L1+L2。
- [READER_INTERPRETATION] 最接近的组合基线是 +CoT+L1（结构化生成 + 执行恢复、无行为验证）：它隔离 L2 的净贡献（MAMO 上 Claude 75.4→79.8 = +4.4pp；RetailOpt 严格精度 31.1→31.1 = 0）。
- [AUTHOR_FACT] 模型侧对照为 5 模型三范式：Claude Opus 4.6、DeepSeek-V3.2（671B MoE）、Qwen3-32B、OptMATH-Qwen2.5-32B（Offline SFT）、SIRL-Qwen2.5-32B（solver-feedback Online RL）（§5.1, p.7）。
- [AUTHOR_FACT] 跨基准 Base 数字来源混合："we cite baseline Acc% from Chen et al. [10] (SIRL Table 1) for models where published results are available: DeepSeek-V3.2, Qwen3-32B, OptMATH-32B, and SIRL-32B. We run CoT and +ReLoop configurations ourselves."（G.3, p.35）——即 MAMO/IndustryOR 上 4/5 模型的 Base 为引用而非复跑；GPT-4 (49.3/33.0)、DeepSeek-R1 (67.9/45.0)、OpenAI-o3 (51.2/44.0) 仅文字引用、未接 ReLoop（p.35）。
- [READER_INTERPRETATION] 缺失的基线：无任何显式修复/自改进基线（Self-Refine、Reflexion、OptiMUS、Chain-of-Experts 等）在相同预算下的实验对比——Table 1（p.3）只做性质对比（Detects Silent Failures / External Signal / No Ground Truth / Iterative Repair），非实验对比；也没有等 token 预算的多次采样对照（见第 4 题）。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] token/调用不对等是明示的：ReLoop "adds ∼3× base cost in LLM tokens"（§5.1, p.7）；L1/L2 各至多 3 次再生成/修复调用（Table 19, p.28），且安全重试 "does not consume the repair budget"（E.6, p.34）；Base 为单次调用。
- [READER_INTERPRETATION] 因此 Exec% 增益（OptMATH 2.6→17.9、DeepSeek 53.2→97.4）在机制上部分等价于"带诊断反馈的重试预算"；论文没有等预算对照（如 Base + 3 次盲重试或 pass@3）来分离"重试次数"与"诊断质量"的贡献。这是本文最主要的混杂来源。
- [READER_INTERPRETATION] Acc 侧部分免疫：+CoT 与 Direct 同为单次调用（Table 7, p.9），Claude +8.5pp（22.6→31.1）不含重试预算差异；L2 的 +4.4pp（MAMO）是 +CoT+L1 之上的增量，含额外调用但受回滚保护。
- [AUTHOR_FACT] prompt 差异：RetailOpt 的 prompt 自带 "structure cues"——变量索引约定、与参考 MILP 对齐的易腐流入等式、聚合产能约束（C.1, p.17–18），且 "fully unscaffolded prompts produce near-zero accuracy on compositional retail problems for all tested models"（p.18）。
- [READER_INTERPRETATION] 该脚手架与 ground-truth 求解器（URS）的建模约定同源对齐（r=1 为最老库存、holding cost 仅 k≥2 等），意味着 RetailOpt 的正确性度量部分测的是"能否遵循给定约定"；同一 prompt 下跨模型/跨配置比较仍公平，但绝对准确率不可外推到无脚手架场景。
- [AUTHOR_FACT] oracle 差异：L2 自身不用 ground truth；但正确性评测依赖 Gurobi 11.0 对手工参考公式的 ground truth（"Ground-truth optimal values are computed by Gurobi 11.0 applied to hand-crafted formulations", §4, p.7），判定 = 状态匹配 + 相对误差 < ε（D.2, p.22）；Exec% 把 infeasible/unbounded/运行错误都计失败（D.3, p.22）。
- [AUTHOR_FACT] 作者自曝一处可比性风险：OptMATH 在 MAMO 的异常高 Base "may also reflect potential training–evaluation overlap"（footnote 2, p.8）。
- [READER_INTERPRETATION] 另一可比性弱点：MAMO/IndustryOR 的 4 个 Base 数字直接引自 SIRL 论文（G.3, p.35），其评测 harness（代码提取、超时、解析）与本文自跑的 CoT/ReLoop 不保证逐项一致；若有差异，Base→ReLoop 的增量会被污染。ε=1e-6 声称沿用 Chen et al. 协议（p.7, p.34）。
- [AUTHOR_FACT] 模型差异：每行内 Base/CoT/ReLoop 同一模型（Table 21, p.35：温度 0、max tokens 8192、API/vLLM BF16）；L2 抽取与生成同 LLM（p.35），不存在借更强验证模型的问题。
- [AUTHOR_FACT] 全部结果 single-run pass@1、无误差条；checklist #7 明答 "No"，理由是 greedy 决定性 + 20 实例复跑一致（p.38；G.4, p.35），并承认 "LLM API behavior can drift over time"（p.38）。
- [READER_INTERPRETATION] 综合判断：核心定性结论（CoT 助强模型、L1 救执行、L2 只对局部缺陷有效）方向可信——消融链内部一致且负向结果如实报告；但各增量的绝对幅度受"重试预算不对等 + 引用 Base + 单次运行"三重影响，不应按点值引用。

## 5. 作者明示限制、负向结果和未测试边界

- [AUTHOR_FACT] Limitations 段（§6, p.9–10）：(1) "Structured generation assumes format compatibility: CoT disrupts SFT models' learned patterns (84 crashes, 65 regressions on OptMATH/MAMO)"；(2) "L2 shares the generating LLM for constraint extraction, creating potential failure correlation"；(3) τr "is calibrated for localized defects, conservatively holding major structural omissions to the L1 baseline"；(4) "Three failure modes remain beyond scope: coefficient magnitude errors, formulation equivalence errors, and unrepresented problem structures."（p.10）。
- [AUTHOR_FACT] 负向结果（作者明确报告）：
  - DeepSeek 上 CoT 使执行崩塌 91.1%→53.2%（§5.2, p.7–8；Table 7, p.9）。
  - OptMATH 在 MAMO 上 CoT 使 Base 56.2%→30.0%，"84 instances crash and 65 previously correct solutions are destroyed"（§5.3, p.8）。
  - RetailOpt 上 L2 对严格精度零贡献（Claude 31.1→31.1，Table 7, p.9），因错误 "predominantly structural"（p.9）。
  - Claude ReLoop 后仍 "two-thirds remain silent failures"（§5.2, p.7；Exec 100 vs Acc 31.1）。
  - F3（Resource）与 F5（Feasibility Stress）全模型 0%；F6 上 Claude 增益为零（Table 23 及讨论, p.36）。
  - IndustryOR 偏差双峰："34% have deviations below 1% ... and 47% exceed 10% ..., leaving almost no instances in the correctable range"（§5.4, p.9）。
  - 三个 32B 模型在 RetailOpt 严格准确率全 0（Table 5, p.8；Table 23, p.36）。
- [AUTHOR_FACT] 未测试边界（作者明说）："cross-model verification is left for future work"（G.1, p.35）；无统计显著性/误差条（checklist #7 = No, p.38）。
- [READER_INTERPRETATION] 作者未讨论的边界：仅 Gurobi 一种求解器；仅 greedy pass@1（未测 pass@k/采样温度）；L2 阈值敏感性只有一句话（"accuracy varies by <1% across τℓ∈[1%, 10%] and τh∈[20%, 50%]", §3.3.2, p.6，无表格支撑）；RetailOpt 由作者自建自评（ground truth 与 prompt 脚手架同源）。
- [OPEN_QUESTION] NeurIPS checklist #2（p.37）列出的四条 limitation 含 "(ii) linear L2 overhead in tested parameters"，但 §6 Limitations 正文四点中并无此条——checklist 与正文轻微不一致；开销 3× 只出现在 §5.1 与 checklist #8。

## 6. 可抽取 Operator 与真实可记录 Failure

Operator（可迁移操作，均可定位）：
- [AUTHOR_FACT] OP1 四阶段结构化生成：单次调用内 understand/formalize/synthesize/verify + 显式变量类型推理 + 生成内自查；§3.2 p.4–5，完整 prompt 在 E.2 p.29（"STEP 1: UNDERSTAND THE PROBLEM ... STEP 4: VERIFY COMPLETENESS"）。
- [AUTHOR_FACT] OP2 行为验证 = 极端参数扰动 + 分级阈值：capacity ×0.001 / demand ×100 / cost ×0.001 / revenue ×100；r<5% WARNING、5–30% INFO、>30% 或诱发 infeasible 为 PASS（扰动诱发 infeasible 视为强 PASS，footnote 1, p.4）；§3.3.2 p.5–6、E.4–E.5 p.30–32。核心可迁移思想："instead of interpreting sensitivity, we test whether it exists"（§2, p.3）。
- [AUTHOR_FACT] OP3 诊断特异的执行恢复：INFEASIBLE→IIS 最小冲突约束集喂回 LLM，UNBOUNDED→unbounded ray 变量，语法→traceback（§3.3.1, p.5；L1 再生成 prompt E.3, p.30）。
- [AUTHOR_FACT] OP4 保守修复防回归三件套：safety check（禁 data 重定义/变异、禁 os/subprocess 导入，E.6 p.33–34）、regression guard（目标偏移 >4% 或状态劣化即回滚，§3.4 p.6）、INFO 项显式 "DO NOT FIX"（repair prompt p.33："Below items are NORMAL in 80%+ of cases"）。
- [AUTHOR_FACT] OP5 数据-代码分离作为可验证性设计：强制 data["key"] 访问模式使运行时扰动可行；抽取失败回退自包含 + AST 源码扰动双策略（Stage 3 p.5；E.2 p.28；E.4 p.31）。
- [AUTHOR_FACT] OP6 基准构造法：38 archetype × 5 变体；确定性种子 seed = uint32_le(SHA256("{name}|{v}")[:4])，demand/storage ×U(1±0.15)（B.3, p.16–17）；组合式设计矩阵（Table 10, p.16）；F5 用"遗漏即 infeasible"的不对称做诊断信号（B.1, p.16）。
- [READER_INTERPRETATION] OP2 的适用前提必须一并记录：仅当缺陷是"局部可扰动"的（缺约束/缺目标项）才有效；对内部自洽的错误分解无效（"structural silent failures ... that perturbation cannot detect", §5.2, p.8）。

Failure（论文中真实发生且有数字/证据）：
- [AUTHOR_FACT] F-1 结构化 CoT 使 DeepSeek 执行率 91.1→53.2："produces intermediate mathematical notation that fails to translate into valid Gurobi syntax"（§5.2, p.7–8）。
- [AUTHOR_FACT] F-2 CoT 与窄域 SFT 格式冲突：OptMATH/MAMO 56.2→30.0，84 崩溃 + 65 个原本正确的解被毁（§5.3, p.8；Limitations p.9–10）。
- [AUTHOR_FACT] F-3 扰动检测对结构性静默失败失效：RetailOpt 严格精度 L2 增量为 0（Table 7, p.9）；Claude 三分之二仍为静默失败（p.7–8）。
- [AUTHOR_FACT] F-4 修复 LLM 会伪造数据："we observed repair LLMs fabricating values that corrupt the problem"（§3.4, p.6）——safety check 的动因。
- [AUTHOR_FACT] F-5 IndustryOR 双峰失效区：<1% 偏差占 34%（扰动测不到）、>10% 占 47%（3 轮修不好），可修复中间带几乎为空（§5.4, p.9）。
- [AUTHOR_FACT] F-6 替代方向反转为高频建模错误：pilot 中 "∼35% error rate across four frontier LLMs"（A.7 D4, p.15）。
- [AUTHOR_FACT] F-7 多资源耦合与可行性压力超出全部被测模型能力：F3/F5 全 0%（Table 23 及讨论, p.36）。
- [READER_INTERPRETATION] F-1/F-2 合并成一个可复用教训：结构化提示不是免费的——对基座模型是增益、对格式敏感的 SFT/中档模型可能是净伤害，应按模型类别先做格式兼容性检查。

## 7. 判断-定位对照表（物理页码 / 章节 / 图表 / 逐字定位语）

| # | 判断 | 物理页 | 章节/图表 | 逐字定位语 |
|---|------|--------|-----------|------------|
| 1 | 90 点可行-正确差距 | p.1, p.7 | Abstract; §5.2 Table 5 | "a feasibility–correctness gap reaching 90 percentage points" |
| 2 | 四阶段生成定义 | p.4 | §3.2 Eq.(1) | "We decompose generation into four stages executed in a single LLM call" |
| 3 | 扰动敏感性性质 | p.3–4 | §3.1 Property 1 | "the objective must change substantially" |
| 4 | 严重度矩阵 | p.5 | Table 2 | "Severity matrix across verification layers" |
| 5 | 扰动因子 | p.6, p.31–32 | §3.3.2; E.4/E.5 | "capacity ×0.001, demand ×100, other ×0.01" |
| 6 | 阈值缓冲不对称 | p.5–6 | §3.3.2 | "a deliberate preference for under-detection over over-repair" |
| 7 | 回归回滚 τr=4% | p.6, p.28 | §3.4; Table 19 | "rolls back any repair that ... shifts the objective by >τr = 4%" |
| 8 | RetailOpt 构成 | p.6–7 | §4; Table 4 | "38 × 5 = 190 instances" |
| 9 | 主结果 | p.8 | Table 5 | "Main results on RetailOpt-190 (pass@1, greedy decoding, N =3)" |
| 10 | 跨基准结果 | p.8 | Table 6 | "Cross-benchmark generalization (Acc%, ϵ=10−6, pass@1)" |
| 11 | 消融链 | p.9 | Table 7 | "Each row adds one component; L2 = CPT + OPT" |
| 12 | +8.5pp / +4.4pp 归因 | p.9 | §5.4 | "primary accuracy driver (+8.5pp; 20 corrected, 4 regressed)"；"largest single accuracy contributor for Claude (+4.4pp; 11 corrected, 2 regressed)" |
| 13 | 3× token 成本 | p.7 | §5.1 | "ReLoop adds ∼3× base cost in LLM tokens" |
| 14 | Base 数字系引用 | p.35 | G.3 | "we cite baseline Acc% from Chen et al. [10] (SIRL Table 1)" |
| 15 | 同 LLM 验证 | p.35 | G.1 | "cross-model verification is left for future work" |
| 16 | 单次运行无误差条 | p.35, p.38 | G.4; checklist #7 | "All results are single-run (pass@1)" |
| 17 | prompt 脚手架 | p.17–18 | C.1 | "fully unscaffolded prompts produce near-zero accuracy" |
| 18 | 数据泄漏疑虑 | p.8 | footnote 2 | "may also reflect potential training–evaluation overlap" |
| 19 | 每族结果 | p.36 | Table 23 | "Per-family results on RetailOpt-190 (Acc%, ϵ = 10−4)" |
| 20 | 修复伪造数据 | p.6 | §3.4 | "repair LLMs fabricating values that corrupt the problem" |
| 21 | 替代方向 35% 错误率 | p.15 | A.7 D4 | "∼35% error rate across four frontier LLMs" |
| 22 | 评测判定标准 | p.7, p.22 | §4 Evaluation; D.2 | "feasibility status matches ground truth" |
| 23 | Exec% 定义 | p.22 | D.3 | "Infeasibility, unboundedness, and runtime errors all count as execution failure" |
| 24 | 求解器设置 | p.26, p.35 | Table 17; G.2 | "TimeLimit 60 seconds ... Threads 1 ... Seed 0" |

- [READER_INTERPRETATION] 内部一致性抽验通过：Table 23 各族×实例数汇总与 Table 5 总量吻合（Claude Base 43/190=22.6%、ReLoop 59/190≈31.1%；DeepSeek Base 1/190≈0.5%）；+8.5pp = 31.1−22.6，+4.4pp = 79.8−75.4，均可复算。

## 8. 解析文本与可视 PDF 是否冲突（就抽查页回答）

- [AUTHOR_FACT] 抽查 p.5（Table 2 严重度矩阵）、p.7（Table 4 scenario families）、p.8（Table 5/6 全部数字）、p.9（Table 7 消融数字）、p.36（Table 23 每族数字）共 5 页的 150 dpi 渲染图，与 PyMuPDF 抽取文本逐项比对：所有数值、阈值、粗体位置一致，未发现冲突。
- [READER_INTERPRETATION] 抽取文本对多列表格做了线性化（单元格逐个流式输出，如 Table 5 数字逐行排开），需按视觉版面重组才能正确对应列名；本报告所有表格数字均以视觉版面核对后为准。数学符号在抽取文本中有轻微乱序/连字问题，但不影响数值判读。
- [OPEN_QUESTION] 一处正文内部（非文本-视觉）疑似不一致，两种呈现相同、故非解析问题：§5.3（p.8）称 IndustryOR "contains longer real-world problems"，而 Table 22（p.35）给出 IndustryOR 平均 ∼267 tokens < MAMO-ComplexLP 的 ∼459 tokens；"longer" 或指推理链而非 prompt 长度，原文无法裁决。

## 9. 其他 OPEN_QUESTION 汇总

- [OPEN_QUESTION] 等预算对照缺失：Base + 盲重试（同样 ≤3 次、无诊断）能恢复多少 Exec%？原文无此实验，L1 诊断反馈的净价值无法与重试预算分离。
- [OPEN_QUESTION] 引用的 SIRL Base 数字与本文自跑 pipeline 的 harness（代码提取、超时、状态解析）是否逐项对齐，原文未描述比对过程。
- [OPEN_QUESTION] 阈值敏感性声明（"accuracy varies by <1%", p.6）无支撑表格或附录实验，扫描范围与数据无法核验。
- [OPEN_QUESTION] Claude Opus 4.6 在 MAMO/IndustryOR 的 Base 数字来源（自跑还是引用）未逐字写明；按 G.3 列举的四个被引模型推断为自跑，但原文未明说。
- [OPEN_QUESTION] p.1 给出 GitHub 仓库（github.com/junbolian/ReLoop）而 checklist #5（p.37）称 "will be released under a permissive license upon acceptance"——代码/基准当前实际可用性本读未核验（任务限定不访问外部资源）。
