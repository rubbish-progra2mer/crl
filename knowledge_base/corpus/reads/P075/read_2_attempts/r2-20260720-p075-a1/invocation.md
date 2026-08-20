# Independent read-2 invocation

- Attempt ID: `r2-20260720-p075-a1`
- Reader role: fresh independent full-paper source checker
- Snapshot time before launch: `2026-07-20T03:23:29+08:00`
- PDF: `knowledge_base/staging/plan05_sat_a2/P075_memory_privacy.pdf`
- PDF SHA-256: `8c2cfcee69d60f4c20a959cd6b1a6a14d5f6e8d732792cf2a2b4864ac38a88cb`
- Canonical metadata: ACL Anthology 2025.acl-long.1227; Unveiling Privacy Risks in LLM Agent Memory; 2025; ACL Long
- Prompt source: `knowledge_base/templates/second_read_prompt.md`
- Prompt SHA-256: `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- Read boundary: `procedural_blinding`; no technical file allowlist.
- Tool/network permission: local PDF read only; no network; write only this attempt `report.md`.
- Actual model/version: `Codex subagent; exact model build not exposed to parent`
- Canonical task/thread: `/root/plan05_p026_second_reader`
- Completion time: `2026-07-20T03:39:10+08:00`
- Report: `report.md`; SHA-256 `a4322ebaf8adfbf4ff8d772f7b8c1f679f64215110f7a067ba1aeb3285faee9f`
- Observable file-access/tool trace: reader reported staging PDF + this invocation only; 20/20 physical pages, text plus visual verification; no network or prohibited workspace reads.
- Provenance correction: the original invocation text accidentally carried the future placeholder `03:35:00`; the file was actually frozen at `03:23:29` before launch. Only this timestamp and post-completion fields were corrected; the exact request and Frozen prompt bytes are unchanged.

## Exact request

你是 P075 的 fresh 独立第二读者。只读指定 PDF 与本 invocation 内 Frozen prompt；不得读 read_1/Cards/其他报告/Corpus/saturation/retrieval/blind。逐页核验 MEXTRA threat model、attacker knowledge levels、prompt generation、两类 agents/memory、leakage metrics、model/data/privacy Oracle、defenses/negative results 与黑盒外推边界；避免复制真实私人内容。只写本 attempt `report.md`。

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
