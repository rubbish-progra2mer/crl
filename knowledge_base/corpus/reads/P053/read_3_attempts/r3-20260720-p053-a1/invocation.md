# Independent read-3 invocation

- Attempt ID: `r3-20260720-p053-a1`
- Reader role: fresh independent conflict and measurement checker
- Snapshot time before launch: `2026-07-20T00:39:43.0237741+08:00`
- PDF: `knowledge_base/staging/papers/P053_higher_order_planning_formalizers.pdf`
- PDF SHA-256: `224970784bd45edc3191b71c2aadd81e01f5869fcd004c4fa10bac4ed1217b19`
- Canonical metadata: arXiv:2603.23844 v2; Language Models as Higher-Order Planning Formalizers; 2026; arXiv preprint
- Prompt source: `knowledge_base/templates/second_read_prompt.md`
- Prompt SHA-256: `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- Read boundary: `procedural_blinding`；App 未提供可验证的文件级 allowlist，禁止工作区枚举。
- Tool/network permission: 本地 PDF 只读；不得联网；写入仅限本 attempt 的 `report.md`。
- Actual model/version: `unknown`（运行界面未暴露）
- Canonical task/thread: `/root/plan05_p053_third_reader`
- Completion time: `2026-07-20T01:04:39.1998613+08:00`
- Report: `report.md`; SHA-256 `01116b2087e13a5e7e755f7e9211cb54cc5197560adae6ea6a5d1250deafe8a3`
- Observable file-access/tool trace: 读者声明只读取 invocation、统一 prompt、指定 PDF 及必要 AGENTS/skill 指令；用 PowerShell/PyMuPDF 校验 SHA、逐页抽取并视觉复核，使用 apply_patch 写本报告；未联网、未枚举工作区、未读取禁区。技术级 trace 不可用。

## Exact request

你是论文 P053 的 fresh 独立第三读者。只允许读取指定 PDF、统一 prompt 和本 invocation；禁止枚举工作区，禁止读取 read_1、read_2、Cards、其他读者报告、其他论文读稿、Corpus Report 或任何 blind query。逐页独立检查全文，尤其攻击：higher-order representation 与额外 pattern-review prompt 是否被混淆；parser/ground-truth exact-match 是否替代真实 planner；synthetic fixed-domain scaling 能支持多窄的 Claim；最接近 Formalizer/D&C baseline 是否充分。按统一标签和精确页码/图表/短定位文本报告。只写本 attempt 的 `report.md`，不生成 Card/Evidence/manifest，不作 Candidate 评价。

## Frozen prompt bytes

```markdown
# CRL 独立二读请求模板

## 输入边界

第二读者只接收以下材料：

- 论文原文路径及 SHA-256；
- canonical metadata；
- 本文件中的统一问题清单。

不得接收首读 Card、首读结论、Operator/Failure 候选、预期分歧或其他读者报告。任务是独立核源，不是给论文打分、投票或评价 Candidate。

## 启动前冻结 invocation snapshot

每篇论文开始二读前，在该论文的 reads 目录保存不可由后续模板变化覆盖的 invocation snapshot，至少记录：

- exact request；
- 当次 `second_read_prompt.md` 原始 bytes 与 SHA-256；
- PDF 与 metadata 的 input manifest 及各自 SHA-256；
- 启动时间；
- 权限和 read scope。

返回后在同一 snapshot 补充 actual model/version（不可见则 `unknown`）、thread ID、path allowlist（若有）和可观察的 file-access/tool trace（不可见则 `unavailable`）。App 不支持文件级 allowlist 时标记 `procedural_blinding`；不得把 read-only 误称为技术隔离。二读报告必须引用该 snapshot。第三读复用同一 provenance 规则。

## 统一问题清单

1. 方法究竟改变哪一步计算？
2. 输入、输出、可用信息与干预时点分别是什么？
3. 最强基线与最接近组合基线是什么？
4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？
5. 作者明示限制、负向结果和未测试边界是什么？
6. 哪些内容可抽取为 Operator，哪些是真实可记录的 Failure？
7. 每项判断对应哪个页码、章节、图表和短摘录位置？
8. 解析文本与可视 PDF 是否冲突？

## 输出标签

- `[AUTHOR_FACT]`：作者明确报告且可定位的事实。
- `[READER_INTERPRETATION]`：读者对机制、边界或结果的解释。
- `[OPEN_QUESTION]`：原文无法解决或仍需核验的问题。

主 Codex 后续负责 reconciliation。第二读者不得自动合并首读、生成正式 Card 或作科研裁决。
```
