# P039 Codex 首读：ToolFailBench

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P039_toolfailbench.pdf`
- PDF SHA-256：`6588af66fd477d9764c20c52c2adb7d92fcbf6a788fe09713bc71916862d3009`
- 读取范围：全文（18 页），重点为 trap/control 构造、两步 protocol、failure taxonomy、主结果与限制。

## 研究对象

- [AUTHOR_FACT] 1,000 个单轮任务：750 个 tool-required parametric traps 与 250 个 no-tool controls；把 Tool-Skip、Result-Ignore、Output-Fabrication、Unnecessary-Tool-Use 分开。
- [CODEX_SYNTHESIS] 它验证的是 tool loop 的“调用后证据服从性”，不是开放 Agent 的完整 planning 能力。

## 关键结果与公平性

- 最佳 Grok-4.3 CTUR 86.33%，仍未饱和；强模型不是调用最多，而是在需要时调用并忠实使用结果。
- Llama-3.1-70B CTUR 62.58%，但 UTR 77.73%、control accuracy 8.91%；Qwen2.5-72B control accuracy 98.00%，同尺度差 89 个百分点。
- 所有模型同一任务、tool schema、temperature=0、max_tokens=1024；两阶段先 `tool_choice=auto`，若调用后再强制 `tool_choice=none` 输出答案，便于拆分 selection 与 integration。
- label 为 rule classifier + 两个 LLM judges 多数票；虽报告 rule-only 和一致性，judge 仍可能共享 blind spot。

## 边界

- mock return 故意违背 plausible prior，是强控制诊断；不能直接推断内部来源就是记忆而非随机 hallucination。
- 单轮固定两步不覆盖 multi-tool planning、长期状态或错误恢复；绝对发生率不能外推到真实 Agent。
- prompt 明确要求 tool output 是 source of truth，可能高估一般场景中的服从性；另一方面仍有 RI，说明 failure 真实存在。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P039-E01 | evaluation | §3–4, pp.2–4 | trap/control protocol | [AUTHOR_FACT] 调用与调用后使用分解。 |
| P039-E02 | negative_result | §5, p.5 | Table 2 | [AUTHOR_FACT] aggregate 相似、failure profile 相反。 |
| P039-E03 | limitation | §6, p.7 | limitations | [AUTHOR_FACT] 单轮/域/judge 边界。 |

## Card 草案（不进入正式 Cards）

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Tool Called but Evidence Not Used`
- 条件：工具执行成功且返回受控值，但模型最终答案回退到 parametric prior、泛化措辞或编造结构字段。
- 现象：function-call accuracy 正常，最终 factual/action claim 仍错误。
- 替代解释：输出解析与格式规则可能造成假阳性，需保留 trace 与 rule/judge 分歧。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Post-Call Evidence-Faithfulness Decomposition`
- Changed evaluation：分别测 tool selection、result integration、fabrication 与 no-tool discipline，不用单一 pass rate 混合它们。

## 首读裁决

`KEEP_FOR_SECOND_READ`。Failure 价值高；不可把诊断 benchmark 当成开放 implement 成功证明。
