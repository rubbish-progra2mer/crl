# P030 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p030-a1/invocation.md`；只核读 invocation、统一问题和指定 SHA 的 37 页 PDF，未读取 read_1、Cards、其他报告/论文读稿或 blind query，未联网。
- [AUTHOR_FACT] 37 页正文、限制、构造 prompts、评测、人类验证、attention 分析、LightMem 案例与 CUPMEM 设计均逐页检查。
- [OPEN_QUESTION] 核读基于 PDF 文本层；关键表格和公式可连续提取，未逐页位图渲染，attention 曲线只按作者正文/图注作定性解释。

## 2. 论文对象与 changed computation

- [AUTHOR_FACT] STALE 含 400 个专家验证的 conflict scenarios、1,200 个 queries、约 100 个主题，输入上下文最高约 165k formatted tokens；Type I 是同属性隐式更新，Type II 是跨属性传播失效（§3、Table 5，物理页 3–6、26）。
- [AUTHOR_FACT] 三类 probes 分别测试 State Recognition、Premise Resistance、Implicit Policy Adaptation（§3，物理页 4–5）。
- [AUTHOR_FACT] CUPMEM 在写入时把证据映射到 typed temporal state schema，显式裁决 KEEP/STALE/REPLACE/UNKNOWN；对 Type II 扩展受影响 state regions，查询时只从授权后的 current-state basis 生成（§5、Appendix F，物理页 9、35–37）。
- [READER_INTERPRETATION] changed computation 不是增强 top-k retrieval，而是把“当前状态裁决”前移到 write time，并让 query readout 受 stale/unknown 状态约束。

## 3. 输入、输出与干预时点

- [AUTHOR_FACT] 写入输入为新 session 中的 state-relevant spans、旧 typed store 与固定 schema；输出为新增/细化/替换记录、STALE 归档或 UNKNOWN_CURRENT 标记（物理页 35–36）。
- [AUTHOR_FACT] 查询输入被解析为 intent、presupposed states、required state basis 和 action；verifier 输出 SUPPORTED/OUTDATED/UNRESOLVED，再生成最终回答（物理页 37）。
- [AUTHOR_FACT] schema 与 benchmark generation ontology 分开构建并在评测前固定，但仍是 LLM-assisted heuristic schema（物理页 35）。
- [READER_INTERPRETATION] Operator 的信息优势来自保留时间、状态类型、潜在受影响区域与写入期 LLM adjudicator；它不应被描述成纯检索改进。

## 4. 基线、结果与诊断

- [AUTHOR_FACT] Table 2 中最佳普通闭源模型 Gemini-3.1-Pro overall 55.2，Qwen3.5-27B 为 31.3；多数 memory frameworks 低于 18，GPT-4o-mini plain 为 8.7，CUPMEM 为 68.0（物理页 6–7、9）。
- [AUTHOR_FACT] 同 GPT-4o-mini backbone 下，只有 LightMem 17.8 高于 plain；其他外部 memory frameworks 提升有限或不一致（物理页 8）。
- [AUTHOR_FACT] LightMem 的新证据在 SR/PR top-20 中出现 77.5%，IPA 中 67.8%，但“已检索新证据仍失败”分别为 56.1%、99.0%、78.6%（Table 3，物理页 8–9）。
- [READER_INTERPRETATION] Table 3 强力支持 current-state adjudication gap：可见新证据不等于它成为支配后续行动的当前状态。
- [AUTHOR_FACT] attention 分析发现 query 对旧/新 session 的注意高于邻近噪声，而新 session 对旧 session 的直接 attention 较弱；作者明确称该分析为诊断而非因果（§4.3、Appendix E.4，物理页 8、31–33）。

## 5. 公平性、oracle 与成本

- [AUTHOR_FACT] benchmark 多阶段由 Qwen3.5-Plus、GPT-5.2、Gemini-3.1-Pro 等生成/验证，平均构造成本约 `$0.12`/instance；自动评测使用 Gemini-3.1-Flash-Lite judge（Appendix C，物理页 15）。
- [AUTHOR_FACT] memory baselines 都以 GPT-4o-mini 为 backbone；每实例成本约 LightMem `$0.02`、A-MEM `$0.38`、CUPMEM `$0.37`（物理页 15）。
- [AUTHOR_FACT] judge 在 240 responses 上与人工标签 agreement 95.83%，κ=0.9152；IPA agreement 较低 91.25%，且呈更保守的 false negatives（Table 7，物理页 30）。
- [READER_INTERPRETATION] CUPMEM 与 LightMem 在 backbone 上可比，但 CUPMEM 具有手工预定义 schema、额外写入期 adjudication 和接近 A-MEM 的较高成本；68.0 不能解释为零开销的单组件增益。
- [OPEN_QUESTION] 未看到去 schema、去 propagation search、去 constrained readout 的完整消融，故无法隔离三个组成部分的独立贡献。

## 6. 负向结果和作者边界

- [AUTHOR_FACT] PR 对多数模型几乎为零，Type II 普遍难于 Type I；重复调用小样本仍保持这些趋势（Table 2、Table 6，物理页 6–7、29）。
- [AUTHOR_FACT] 作者限定 STALE 为单次隐式状态转移、合成对话和固定 schema prototype；未覆盖反复更新、耦合属性、渐进 drift 或 schema-free open domain（Limitations，物理页 14）。
- [AUTHOR_FACT] distractor sessions 来自 LongMemEval 而非同 persona，作者承认生态效度可能降低（物理页 14）。
- [READER_INTERPRETATION] Failure 候选：`Updated memory is retrieved but lacks governing authority`；`Stale premise can override recognized current state`；`Propagation across attributes fails even with long context`。
- [READER_INTERPRETATION] 还应记录风险：错误的写入期 adjudication 可能过早废弃仍有效偏好，UNKNOWN_CURRENT 也可能过度阻断；Appendix H 明示错误状态更新与隐私风险（物理页 37）。

## 7. 可抽取资产与 Claim 边界

- [READER_INTERPRETATION] Evaluation Operator：`Three-probe stale-state evaluation: recognize, resist premise, adapt policy`。
- [READER_INTERPRETATION] Method Operator：`Write-side current-state adjudication with propagation-aware invalidation and constrained readout`。
- [READER_INTERPRETATION] 窄 Claim：在合成、专家复核的 STALE 与固定 typed schema 上，CUPMEM 相同 GPT-4o-mini backbone 显著高于 plain 和已测 memory frameworks，并改善 premise resistance。
- [READER_INTERPRETATION] 不支持：CUPMEM 已是通用长期记忆架构；attention 关系具有因果性；显式 schema 可扩展到任意用户状态；检索召回提高即可解决 stale memory。

## 8. 独立二读建议

`ACCEPT_WITH_NARROWING`。Failure/Evaluation 价值很高，CUPMEM Operator 也值得保留；必须绑定 synthetic one-shot、固定 schema、较高成本、LLM judge 与组件归因未隔离等边界。本建议仅供主 Codex reconciliation。
