# PLAN_05 Card Source Audit G

## 审计身份、边界与 provenance

- 本报告是 13 张 A2 Card 的一次性 source-grounding audit；不是研究 Reviewer，不评分、不排名、不投票，不生成 Candidate，也不启动三审。
- 严格读取范围：invocation 明列的 13 张 Card、这些 Card 引用的 13 条唯一 Evidence，以及 Card metadata 指向的 P072–P076 PDF。
- 未联网；本轮未打开 read_1、read_2、reconciliation、saturation、calibration/blind、prior audits 或 Candidate artifacts。
- `knowledge_base/corpus/evidence.json` 的实际 SHA-256 为 `ddcf22a35a67dd95c9319dec27ca62257e02399febc594dbf8130e9571a82aab`，与 invocation 一致。
- P072–P076 五份 canonical PDF 均存在，5/5 SHA-256 与 Card `source_refs` 一致。
- 13/13 Card metadata 可解析；13 条唯一 Evidence 均存在；全部 `[AUTHOR_FACT]` 均带 Evidence 引用。
- Blinding 是 `procedural_blinding`，不是技术文件隔离。平台复用了同一 task path；本轮没有读取任何 read_2 文件，但运行上下文此前执行过 P073/P076 的二读任务。因此本报告不能声称具有跨任务的记忆级 fresh isolation；以下每项结论均在本轮重新以允许的 Card、Evidence 和 PDF 定位核验。
- 唯一写入：本 `report.md`。

判定口径：`ACCEPT` 表示 Card 文本及其 Evidence package 无需 source 修订；`REVISE` 表示存在可局部修复的措辞、Evidence span/section、监督/预算或适用边界问题；`REJECT` 仅用于核心内容无法由允许来源支撑的情形。

## 逐 Card 处置

### Paper Cards

| Card | 结论 | Source 核验 | 最小可执行修改 |
|---|---|---|---|
| `paper-p072.md` | REVISE | P072 p2 Introduction 直接支持自由文本 clarification 缺少参数关系、重要性、可行性以及“问什么/何时停”的标准；p5 Figure 3、§4.2–§5.1 支持候选 call、结构化 belief、candidate questions、cost-penalized EVPI 与 ask/execute gate；p8 §8.1 支持约 22K tokens。核心内容成立。问题是 `ev-p072-unstructured-clarification-failure.section="Front Matter"` 与 `ev-p072-structured-clarification-gate.section="Related Work"` 均错；22K 也应限定为所报 ClarifyBench/实验配置，不能写成方法恒定成本。 | 1) 两条 Evidence section 分别改为 `Introduction`、`Figure 3 / §4.2–§5.1`；2) 将“仍约使用 22K tokens”改为“在来源所报 ClarifyBench 配置中约 22K tokens”。 |
| `paper-p073.md` | REVISE | P073 p3 Figure 2/§2.1 确有一正确一错误、文本形式相近而 uncertainty 相近的例子；p2 Figure 1 与 p4 §3 支持 embedding + execution-result supervision 的 MLP，并用于 prompt/trace selection。Card 的监督、数学/表格代码任务与非 oracle-free 边界准确。问题是两条 Evidence 的 exact span 不完整：`ev-p073-internal-confidence-misalignment` 未包含“一正确一错误”，`ev-p073-execution-supervised-probe` 当前 span 只含 MLP/监督句，未含“用于选择 prompt/trace”；前者 section 还误标为 Introduction。 | 扩展第一条 Evidence span 至 Figure 2 caption；扩展第二条至 Figure 1 caption 中“select the most suitable prompt and execution trace”的前句，或拆成独立 selection Evidence；把第一条 section 改为 `Figure 2 / §2.1`。Card 文本无需扩大。 |
| `paper-p074.md` | ACCEPT | P074 p4 §3.2 直接支持 P/Q contract、P 约束合法调用、Q 约束结构/类型/语义并定义 verified state update；同页明确约 25% ToolBench tools 无 structured response schema 时默认 `Q=True`。Card 没有把 contract existence 偷换成完整语义保证，并提醒 search computation 与 contract effect 分离。无需修改。 | 无。 |
| `paper-p075.md` | REVISE | P075 p4 §3.1 支持 locator + workflow aligner，把 retrieved history 变成 Agent 正常 code/web action 的任务对象；p5 §4.1–§4.2/Table 1 支持 GPT-4o、两个 single-agent、static 200-record memory、30 prompts、50/26 extracted queries；p9 Limitations 支持无 session control 及 isolation 未测试。Card 的机制与数值准确，但没有保留“只测 single-agent、默认 GPT-4o”的关键 transfer boundary；三条 Evidence section 均不精确，其中两条明显误标 Introduction。 | 在 Limitations 增加“实证限于 GPT-4o 驱动的两个 single-agent 与 static memory”；Evidence section 改为：`ev-p075-retrieve-to-action-leakage → §3.1`、`ev-p075-measured-memory-extraction → §4.1–§4.2 / Table 1`、`ev-p075-session-isolation-boundary → Limitations`；并把 session Evidence span 扩至“isolation 留作 future work”，或删去 Card 中超出当前 span 的该半句。 |
| `paper-p076.md` | REVISE | P076 p5 §4 支持 false error/status、inter-agent trust、adaptive error handling 与 front-line metadata laundering；p8 §6.5 支持 sub-agent refusal/warning 与系统级执行并存；p11 Ethics Statement 支持 controlled lab、未攻击生产 live services。Card 对 capability 依赖、未验证 defense、不能说与 prompt injection 无关的边界准确。问题是 Evidence section 元数据：metadata 条目误标 `2.1 Agentic AI`，controlled-lab 条目误标 `8 Discussion`。 | 分别改为 `§4 Control-flow hijacking in multi-agent systems` 与 `Ethics Statement`；可把 refusal 条目从宽泛 `6 Results` 精化为 `§6.5 Life finds a way`。Card 文本无需改。 |

### Operator Cards

| Card | 结论 | Source 核验 | 最小可执行修改 |
|---|---|---|---|
| `operator-cost-penalized-structured-clarification.md` | REVISE | 输入为 user request/tool schema/candidate calls/history，输出 question 或 best call，发生在 invocation 前；P072 p5–6 明确支持 unknown parameters、EVPI−redundancy cost、stopping coefficient、execution threshold 与 max steps。Card changed computation 可执行且 hypothesis/observable signature 有边界。问题仅在两条 linked Evidence section 错标，以及 22K 成本缺少实验设置限定。 | 同步修正 P072 两条 Evidence section；把 22K 改为“来源所报 ClarifyBench 配置”；在预算句保留“较少用户问题不等于较少模型计算”。 |
| `operator-execution-supervised-prompt-trace-calibration.md` | REVISE | P073 p4 §3 显示训练时以 `(embedding, execution reward label)` 学 `P(r|ϕ)`；推理时 prompt score 在候选生成前分配 prompt，trace score 在候选程序生成并执行后聚合答案。Card 的“输入为 embedding 与离线标签”把训练输入和推理输入写在一起，容易把 label 误解为 test-time oracle；也未说明 offline label generation 本身需要多候选生成/执行预算。两条 Evidence span/section 另有上述问题。 | 将 Inputs/Outputs 拆成：`训练输入=embedding+ground-truth execution outcome；推理输入=unlabeled candidate embedding`；明确 trace rerank 在 candidates 已生成/执行后，不能减少这些 tool calls；补充 offline candidate-generation/execution budget；按 paper-p073 行修正 Evidence spans/section。 |
| `operator-contract-gated-tool-state-commit.md` | REVISE | P074 p4–5 §3.2–§3.4 支持 typed state、document/schema-derived P/Q、pre-call filtering、post-return verification 与 conditional commit。Operator 的 I/O/timing 和 `Q=True` coverage 风险准确。但 `[AUTHOR_FACT] Before：tool call/result 由自然语言推理直接接受` 不在所引 `ev-p074-contract-state-commit` exact span；该句来自 p1 Introduction。Card 还应明确 P/Q 是从官方文档/interface 提取，不是推理时由 LLM 生成，以固定 contract source/oracle boundary。 | 把 Before 半句改为 `[CODEX_SYNTHESIS]`，或新增/扩展 Evidence 至 p1 Introduction；在 Inputs 增加“P/Q 由 tool documentation/schema 预先提取”；保留 `Q=True` 与 contract-relative verification 边界。 |

### Failure Cards

| Card | 结论 | Source 核验 | 最小可执行修改 |
|---|---|---|---|
| `failure-free-form-clarification-no-stop-value.md` | REVISE | Observed failure 与 P072 p2 Introduction 逐项一致；P072 p5–6 支持替代 gate，p8 支持 22K token 边界。Card 已把范围限于 schema-grounded parameter ambiguity，未外推到开放对话。问题是 linked Evidence section 错标及成本未限定实验配置。 | 修正两条 P072 Evidence section；把 Possible repair 中 22K 改为“来源所报 ClarifyBench 配置约 22K”。 |
| `failure-internal-tool-confidence-not-execution-success.md` | REVISE | P073 p3 Figure 2 支持一正确一错误 traces 获得相近 uncertainty；Card 用“不等于所有 log probabilities 都无信息”保持了窄推断，并明确 supervised repair 的 label/embedding 依赖。当前 Evidence span 未包含 correct/incorrect caption，section 也错。 | 扩展 `ev-p073-internal-confidence-misalignment` 至 Figure 2 caption 并把 section 改为 `Figure 2 / §2.1`；扩展 supervised-probe span 或把“替代原始 confidence”改成只陈述其已直接包含的 MLP mapping/training supervision。 |
| `failure-incomplete-tool-contracts-false-verified-state.md` | ACCEPT | P074 p4 明确约 25% ToolBench tools 默认 `Q=True`；Card 清楚区分 source-observed implementation gap 与尚未实测的 semantic false-commit accident rate，并把 unknown/isolation 标为 hypothesis。Evidence 与 PDF 均足够，范围准确。 | 无。 |
| `failure-retrieved-memory-laundered-through-actions.md` | REVISE | P075 p4–5 支持 workflow-aligned retrieval leakage 与 50/26 数值，p9 支持无 session control；Card 已把 isolation/sanitization/output filter 标成未验证。但 scope 未写 single-agent/GPT-4o，且 Evidence sections/spans 有上述缺口。 | Conditions 增加“两个 GPT-4o single-agent、static memories”；修正三条 Evidence section；扩展 session Evidence span 至 future-isolation 句，或删去未在当前 span 内的 future-work 表述。 |
| `failure-untrusted-agent-metadata-privileged-control-flow.md` | REVISE | P076 p5、p8、p11 分别直接支持 metadata laundering、refusal non-composition、controlled-lab boundary；Card 还诚实保留 capability prerequisites、orchestrator-specific templates、缺 matched controls 与未验证 repairs。核心 Failure 可接受。仅 linked Evidence section 有两处错误。 | 把 metadata Evidence section 改为 `§4`，controlled-lab Evidence 改为 `Ethics Statement`；可把 refusal Evidence 精化为 `§6.5`。 |

## Evidence package 的统一修订清单

### Section metadata

| Evidence | 当前 section | 最小修订 |
|---|---|---|
| `ev-p072-unstructured-clarification-failure` | `Front Matter` | `Introduction` |
| `ev-p072-structured-clarification-gate` | `Related Work` | `Figure 3 / §4.2–§5.1` |
| `ev-p073-internal-confidence-misalignment` | `Introduction` | `Figure 2 / §2.1 Misalignment Scenarios` |
| `ev-p075-retrieve-to-action-leakage` | `Introduction` | `§3.1 Attacking Prompt Design` |
| `ev-p075-measured-memory-extraction` | `Introduction` | `§4.1–§4.2 / Table 1` |
| `ev-p075-session-isolation-boundary` | `Conclusion` | `Limitations` |
| `ev-p076-metadata-control-flow-laundering` | `2.1 Agentic AI` | `§4 Control-flow hijacking in multi-agent systems` |
| `ev-p076-controlled-lab-boundary` | `8 Discussion` | `Ethics Statement` |

`ev-p072-compute-boundary.section="Results"` 与 `ev-p076-refusal-not-system-safety.section="6 Results"` 是正确但过宽的父章节；可分别精化为 `§8.1 Agent Inference Experiments` 与 `§6.5 Life finds a way`，不构成事实错误。

### Exact span completeness

1. `ev-p073-internal-confidence-misalignment`：当前 `source_content` 从“textual formats are similar”起，没包含 Figure 2 caption 中“一条错误、一条正确”。Card 的 `[AUTHOR_FACT]` 使用了后者，需向前扩 span。
2. `ev-p073-execution-supervised-probe`：当前 span 只包含 MLP inputs/outputs 与 execution supervision，没包含同一 Figure 1 caption 中“据此选择 prompt 与 execution trace”。需向前扩 span或拆分 selection Evidence。
3. `ev-p075-session-isolation-boundary`：当前 span 只到“multiple users may share the same session”，而 Cards 还声称 user/session isolation 是 future work。需扩至后续 isolation/future-work 句，或收窄 Card。

## Source-boundary 结论

- `ACCEPT`：2
- `REVISE`：11
- `REJECT`：0

没有 Card 的核心机制或 Failure 完全脱离 P072–P076 原文。修订集中在 Evidence locator/span、P073 training-vs-inference oracle 边界、P075 single-agent/session ownership 边界、以及 P074 Before/source provenance。完成上述局部修改后，无需启动新审计循环；主 Codex 可按 invocation 的 one-pass disposition 处理。
