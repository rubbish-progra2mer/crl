# P049 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P049/read_2_attempts/r2-20260719-p049-a1/invocation.md`
- 论文：*Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents*
- PDF SHA-256：`352a4f39ae64d07722a7e63bfed3d9afad20f7529c406ee764af37d3503b40c8`
- [AUTHOR_FACT] 已读取全部 12 个物理页。

## 1. changed computation 与干预时点

- [AUTHOR_FACT] 系统在工具执行前把 provisional tool call 交给独立 reviewer；Progressive Feedback 最多 N 轮反馈—修订并在 reviewer 接受时停止。另有 Best-of-N Selector 和 Grader：基础 agent 以 0.3–1.0 温度生成 N 个候选，由 reviewer 直接选或打 0–1 分。（物理页 2–3，§2.1；图 2）
- [AUTHOR_FACT] 输入是完整对话、工具文档和待执行响应；输出为 reviewer 的 error 布尔值/反馈，或候选选择。干预在实际 tool side effect 之前。（物理页 1–3）
- [READER_INTERPRETATION] 机制价值在 pre-execution veto/revision，能避免事后状态恢复；但 reviewer 没有外部执行结果，只能基于上下文、政策与 schema 审查。

## 2. 基线、模型与主结果

- [AUTHOR_FACT] 基础 tool agent 固定为 `gpt-4o-2024-11-20`、temperature 0、seed 42；reviewer 比较 GPT-4o、o3-mini，GEPA 阶段换 GPT-5 mini，reasoning effort medium。（物理页 3，§3.2）
- [AUTHOR_FACT] BFCL Non-Live 基线 relevance suite 90.9、irrelevance 84.9；GEPA 配置 `4o-r2-5-mini-v3-gepa` 为 92.5/90.4。BFCL Live 上该 GEPA 配置 relevance 78.5，低于 baseline 79.2，虽 simple/irrelevance 提升。（物理页 6，表 5；物理页 10，表 6–7）
- [AUTHOR_FACT] tau2 三域、3 次 benchmark runs 的 baseline 平均 48.7；最佳 `4o-r5-4o-v1` 平均 55.8，但 airline 从 42.0 降至 40.7、retail 从 62.9 降至 62.6，增益主要来自 telecom 41.2→64.0。（物理页 5，表 3；物理页 10，表 8）
- [AUTHOR_FACT] Best-of-N selection 的 v1 平均 47.3，低于 48.7 baseline；domain-specific v2-tau 的 progressive feedback 52.9，也低于 generic v1 的 55.8。（同上）

## 3. Helpfulness/Harmfulness 指标问题

- [AUTHOR_FACT] 论文把 Helpfulness 写为“base agent 错且 reviewer 修正的 test cases 百分比”，Harmfulness 为“base 正确但 reviewer 弄错的 test cases 百分比”，比值为二者相除；另又解释 o3-mini 为“36.8% of base errors corrected、11.7% new errors”。（物理页 4–6，§4.1、表 2）
- [READER_INTERPRETATION] 若二者都以全部 test cases 为分母，约 90% baseline accuracy 下 Helpfulness 不可能为 36.8%；数值显然更像分别以 base-error 与 base-correct 子集为分母。不同分母的 36.8/11.7 直接相除得到“3.1:1”不能代表总体净收益，因为还必须乘以错误/正确基率。
- [OPEN_QUESTION] 原文没有给出该 dedicated experiment 的计数、混淆矩阵或无歧义公式，无法复算 3.1:1；后续使用前应要求分母与样本数。

## 4. prompt 优化、泄漏与成本

- [AUTHOR_FACT] GEPA 从人工 v2 prompt 收集 reviewer 失败案例、用 LLM 反思并迭代到收敛，prompt 从 358 增至 1,599 tokens；只在 BFCL 做，未扩展 tau2。（物理页 6，§4.4.3）
- [OPEN_QUESTION] 文中没有报告 GEPA 的训练/验证/独立测试拆分；若失败案例来自同一 BFCL Non-Live 评测集，表 5 的增益可能含测试集 prompt overfitting。
- [AUTHOR_FACT] BFCL 平均延迟从 1.27s 到 7.87s（6.2×），tau2 episode 从 158.7s 到 384.3s（2.4×）；BFCL reviewer 平均 1.33 calls/item，tau2 约 0.96 calls/turn。（物理页 7、12，图 5/表 9）
- [READER_INTERPRETATION] 和 baseline 相比使用额外模型、最多 5 轮/5 候选及更长 prompt，准确率增益是明显追加推理预算下的结果；跨配置也混入 reviewer 模型升级。

## 5. 负向结果、限制与候选

- [AUTHOR_FACT] reviewer 会过度怀疑工具调用；初版有 23% 冗余迭代，显式提示后降到 8%。tau2 失败分布中 policy violation/context error 下降，但 tool selection/argument error 上升，over-verbalization 增加 17 个百分点。（物理页 4–5，图 3、表 4）
- [AUTHOR_FACT] 作者明示只测 GPT-4o base 和少数 reviewer；GEPA 与 H/H 指标只用于 BFCL；开源/小模型、tau2 自动优化与多轮 partial-credit 尚未验证。（物理页 8，Limitations）
- [READER_INTERPRETATION] Operator 候选：不可逆 tool call 前的独立 reviewer + 有上限的 progressive revision；同时记录 conditional correction/degradation 的完整混淆矩阵，而非仅比值。
- [READER_INTERPRETATION] Failure 候选：reviewer 误把中间 tool-only response 当不完整；domain prompt 不迁移；selector 可低于 baseline；延迟 2.4–6.2×；提示调优可能评测集过拟合。
- [READER_INTERPRETATION] 建议保留 pre-execution reviewer 的 changed-computation 和 tau2 telecom 增益，但不得用“3:1”直接宣称净正收益，也不得把 GEPA 增益视为已完成留出验证。

## 6. 可视核验

- [AUTHOR_FACT] 图 4/表 2 的 36.8、11.7、3.1:1 与正文一致；问题来自指标分母表述，而非 PDF 解析冲突。

