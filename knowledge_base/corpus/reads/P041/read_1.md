# P041 Codex 首读：LLM Agents Already Know When to Call Tools

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P041_tool_call_necessity.pdf`
- PDF SHA-256：`a05f71b904209ea49cbc9cd13434255aab4037f96640477810fb78a61b701ba0`
- 读取范围：正文（pp.1–10）、benchmark、OOD、ablation 与 Search-o1 附录定位。

## Changed computation

- [AUTHOR_FACT] 对输入最后一个 token 的多层 hidden states 训练 L2 logistic probe，预测该模型在当前任务上是否需要工具；再用一句 prefill 引导直接回答或调用工具。
- [CODEX_SYNTHESIS] 变化不是再增加显式 reasoning，而是从 pre-generation representation 读取 decision signal，并在生成第一个 action 前改变路由。

## 关键结果

- WHEN2TOOL 含 18 个环境、计算/知识边界/执行可靠性三类、easy/medium/hard 三档；tool necessity label 来自同一模型强制 no-tool 时是否成功。
- 六模型 probe AUROC 0.894–0.957；Reason-then-Act 在 Llama 上可使 accuracy 从 79.5→31.2、83.1→47.9，但 probe 仍高于 0.9。
- Probe&Prefill 平均减少 48% tool calls、accuracy 下降 1.7%；hard task 每省一次调用的 accuracy cost 明显低于 prompt/reasoning baselines。
- Search-o1 上报告减少 20–56% API calls 且 accuracy 不降；该外部载体验证比合成环境更重要，二读必须复核其 exact protocol 与统计不确定性。

## 公平性与未否定项

- 需要访问 hidden states，因此不适用于只开放 API logits/文本的闭源模型；“兼容任何 serving”只对可取得表示的部署成立。
- tool-necessity 是 model-conditional label；probe 可能主要学习 environment/difficulty 模板，而不是一般自知能力。OOD 仅为同类别 held-out environments，不能称跨真实域通用。
- synthetic hard tasks 常被构造为不使用工具必错，边界比真实任务清晰；Search-o1 结果需承担主要外推证据。
- prefill 会把 probe 错误直接注入生成；hard prefill 更是强制路由，必须单独报告 false-skip 与 false-call。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P041-E01 | mechanism | §4–5, pp.6–8 | probe & prefill | [AUTHOR_FACT] 表示读取后改变第一步 action。 |
| P041-E02 | negative_result | §3, pp.4–6 | prompt/RTA | [AUTHOR_FACT] 显式 reasoning 不能稳定校准调用。 |
| P041-E03 | evaluation | §5.2–5.3, pp.7–9 | tradeoff / transfer | [AUTHOR_FACT] calls–accuracy 前沿。 |
| P041-E04 | limitation | App. D/G | OOD/Search-o1 | [CODEX_SYNTHESIS] 外推与开放权重边界。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Pre-Generation Tool-Necessity Probe Routing`
- Baseline：prompt 告知“少用工具”或先口头 reasoning，再由原生成策略自行决定。
- Changed computation：从 prompt encoding 的 hidden state 解码 task/model-conditional need，阈值化后在 action generation 前 prefill route。
- 前提：open-weight/hidden-state access；calibration set 与 deployment task 相符；false-skip cost 明确；与相同 token/call budget 比较。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Verbalized Tool Self-Assessment Loses Latent Signal`
- 现象：模型内部表示可区分需要/不需要工具，但要求它用自然语言解释后再行动，反而抑制必要调用或只叙述意图不发出合法 call。

## 首读裁决

`KEEP_FOR_SECOND_READ`。implement 潜力高，但必须严格审计 model-conditional label、模板泄漏与 Search-o1 外推。
