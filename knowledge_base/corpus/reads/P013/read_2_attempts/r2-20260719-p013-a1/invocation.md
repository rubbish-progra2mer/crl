# Independent read-2 invocation

- Attempt ID: `r2-20260719-p013-a1`
- Reader role: fresh independent full-paper source checker
- Launch time: `2026-07-19T15:40:10+08:00`
- PDF: `knowledge_base/staging/papers/P013_intrinsic_self_correction_limits.pdf`
- PDF SHA-256: `d172f0b3e933544f5165250338e3e989036e8d826fea34093e6aed4adb5b042a`
- Canonical metadata: canonical_id=ICLR:8b4add8b0aa8749d80a34ca5d941c355; title=Large Language Models Cannot Self-Correct Reasoning Yet; year=2024; venue=ICLR 2024; version=ICLR proceedings
- Prompt source: `knowledge_base/templates/second_read_prompt.md`
- Prompt SHA-256: `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- Read boundary: `procedural_blinding`；App 未提供可验证的文件级 allowlist，禁止工作区枚举。
- Tool/network permission: local PDF read only；不得联网，写入仅限本 attempt 的 `report.md`。
- Actual model/version: Codex（GPT-5 系列上下文；精确内部版本不可见，记为 `unknown`）
- Canonical task/thread: `/root/p013_second_read`
- Returned report: `knowledge_base/pilot/reads/P013/read_2_attempts/r2-20260719-p013-a1/report.md`
- Returned report SHA-256: `795d43a5f4a1807111d755cb5e3330712c51e6ac748ede2b219804315b250ca9`
- Observable file-access/tool trace: 读者声明只读取 PDF、冻结 prompt 与本 invocation，只写入本 attempt 的 `report.md`；使用 PowerShell `Get-Content`/`Get-FileHash`、Python `pypdf`、PyMuPDF 与 Pillow；`pdfinfo` 路径调用失败、`pdftotext` 不可用；可视页以内存渲染，未生成中间文件，未联网。平台未提供 OS 级访问审计或技术性 path allowlist，故仅为 `procedural_blinding`。

## Exact request

你是论文 P013 的 fresh 独立第二读者。只允许读取：D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P013_intrinsic_self_correction_limits.pdf、D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md、以及本 invocation；禁止枚举工作区，禁止读取 read_1、Cards、其他读者报告或任何 blind query。逐页检查全文，按统一问题输出带 [AUTHOR_FACT]/[READER_INTERPRETATION]/[OPEN_QUESTION] 标签、页码/章节/图表/短定位文本的报告。只写 D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P013/read_2_attempts/r2-20260719-p013-a1/report.md，不生成 Card，不作 Candidate 评价。

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
