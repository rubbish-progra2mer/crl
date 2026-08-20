# Independent read-2 invocation

- Attempt ID: `r2-20260720-p071-a1`
- Reader role: fresh independent full-paper source checker
- Snapshot time before launch: `2026-07-20T02:03:43.1189862+08:00`
- PDF: `knowledge_base/staging/plan05_sat_a1/P071_agentic_plan_caching.pdf`
- PDF SHA-256: `af2ec5f2b4431048ef71d4e090a43a6e9ed9104bcba6dd6d0826c8e26cbc3c8a`
- Canonical metadata: NeurIPS 2025 / arXiv:2506.14852; Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents; 2025; NeurIPS
- Prompt source: `knowledge_base/templates/second_read_prompt.md`
- Prompt SHA-256: `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- Read boundary: `procedural_blinding`；App 未提供可验证的文件级 allowlist，禁止工作区枚举。
- Tool/network permission: 本地 PDF 只读；不得联网；写入仅限本 attempt 的 `report.md`。
- Actual model/version: `unavailable`
- Canonical task/thread: `/root/plan03_blind_evaluator_v1`；因平台线程容量限制复用独立 reader thread，不声称全新空线程。
- Completion time: `2026-07-20T02:58:30.9866645+08:00`
- Report: `report.md`; SHA-256 `4d7b63f9dc73f2dd251282cff3bad8f99bffb9da47f5ff3369b5c25d3bf04429`
- Observable file-access/tool trace: reader 最终只读取 canonical `papers/P071_agentic_plan_caching.pdf` 与本 invocation 内 Frozen prompt，逐页核验 27/27 页；canonical 与 staging 记录的 PDF SHA 相同；未联网、未访问禁止材料，只写本 attempt 的 `report.md`。技术级 file allowlist 不可用，边界为 procedural blinding。

## Exact request

你是论文 P071 的 fresh 独立第二读者。只允许读取必要的两级 AGENTS/CRL 环境规则、指定 PDF、统一 prompt 和本 invocation；禁止枚举工作区，禁止读取 read_1、Cards、其他读者报告、其他论文读稿、Corpus Report、saturation review/disposition 或任何 retrieval/blind 文件。逐页检查全文，按统一问题输出带标签、页码/章节/图表/短定位文本的报告。重点独立核验 plan template extraction/matching/adaptation、成功轨迹、质量/成本/延迟、数据依赖与更长上下文混杂，不得接收或迎合首读结论。只写本 attempt 的 `report.md`，不生成 Card/Evidence/manifest，不作 Candidate 评价。

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
