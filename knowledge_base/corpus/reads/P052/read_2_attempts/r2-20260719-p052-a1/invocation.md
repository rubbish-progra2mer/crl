# Independent read-2 invocation

- Attempt ID: `r2-20260719-p052-a1`
- Reader role: fresh independent full-paper source checker
- Snapshot time before launch: `2026-07-19T23:51:33.5601750+08:00`
- PDF: `knowledge_base/staging/papers/P052_llmfp.pdf`
- PDF SHA-256: `e59c5c55b3befeeb4774a20990b8629f487e9fb1520cc2a953f041b7bb6fdaec`
- Canonical metadata: OpenReview 0K1OaL6XuK / arXiv:2410.12112; Planning Anything with Rigor: General-Purpose Zero-Shot Planning with LLM-based Formalized Programming; 2025; ICLR
- Prompt source: `knowledge_base/templates/second_read_prompt.md`
- Prompt SHA-256: `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- Read boundary: `procedural_blinding`；App 未提供可验证的文件级 allowlist，禁止工作区枚举。
- Tool/network permission: 本地 PDF 只读；不得联网；写入仅限本 attempt 的 `report.md`。
- Actual model/version: `unknown`（运行界面未暴露）
- Canonical task/thread: `/root/plan05_p051_p052_second_reader`
- Completion time: `2026-07-20T00:05:48.7984452+08:00`（controller observed）
- Report: `report.md`; SHA-256 `1cde5290a17ddd4985f4226d3d1bfbb66114a890461658a77c2345ba4eb3b1e0`
- Observable file-access/tool trace: 读者声明科研内容仅访问两篇指定 PDF 各自的 invocation 与统一 prompt；另读取必要的 AGENTS/skill 指令。使用 PowerShell hash、严格 UTF-8 读取、PyMuPDF、apply_patch 与编码检查；未联网、未读取禁区。技术级 trace 不可用。

## Exact request

你是论文 P052 的 fresh 独立第二读者。只允许读取指定 PDF、统一 prompt 和本 invocation；禁止枚举工作区，禁止读取 read_1、Cards、其他读者报告、其他论文读稿或任何 blind query。逐页检查全文，按统一问题输出带标签、页码/章节/图表/短定位文本的报告。重点独立核验 zero-shot/task-agnostic 边界、same-model self-assessment 的归因、matched budget、formalization failure 与成本，但不得接收或迎合首读结论。只写本 attempt 的 `report.md`，不生成 Card/Evidence/manifest，不作 Candidate 评价。

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
