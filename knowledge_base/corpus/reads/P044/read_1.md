# P044 Codex 首读：DEER

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P044_deer.pdf`
- PDF SHA-256：`bb262ad8999adb3feb46f3373db45815f31f16b714f02fe732c47625810cf42a`
- 读取范围：全文（45 页），重点为 expert taxonomy、guidance ablation、claim back-tracking、human validation 与限制。

## Changed evaluation

- [AUTHOR_FACT] 以 80 个跨 20 domains 的标准构建 7 dimensions/25 subdimensions/101 fixed rubric items；每任务另有 domain expert 编写并交叉复核的 mandatory guidance。
- [AUTHOR_FACT] 信息核验不仅看 inline citation，还将 claim 分为 A–F；对可验证的 A–C 通过语义 back-tracking 找前文来源，再验证 claim support、coverage、source quality/diversity。
- [CODEX_SYNTHESIS] 固定共享 rubric 保证跨任务可比，task expert guidance 给出内容锚点，claim-level evidence verification 防止写得像专家但来源不支撑。

## 关键结果与边界

- 45 reports、每篇两位领域专家；从 Vanilla→Dimensions→Granular→Expert Guidance，最终 Pearson/Spearman/pairwise 为 0.73/0.71/0.84；inter-evaluator Krippendorff α 从 0.46 提至 0.55。
- 仅加 granular rubric 会使相关性和一致性下降；说明“schema 越细越严谨”是错误，expert guidance 才恢复有效性。
- claim extraction binary verifiable F1 约 0.79–0.81，六分类 F1 仅约 0.59–0.69；错误会传播到 support/coverage 指标。
- 平均自动评价成本约 $0.5–$1/report，仍需要付费 API；CRL 后续如实际使用必须先获用户授权。
- 任务从 HLE QA 经专家改写，Expert Guidance 又源于原题答案/理由；适合 benchmark judging，但对开放科研 Candidate 不可能拥有同等 expert oracle。
- 作者明确 DEER 不能替代 human oversight；当前只做 text reports，正好符合 CRL 范围。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P044-E01 | evaluation | §4.2–4.3, pp.4–5 | taxonomy/guidance | [AUTHOR_FACT] fixed rubric + expert task guidance。 |
| P044-E02 | evaluation | §4.4, pp.5–6 | claim back-tracking | [AUTHOR_FACT] 显式/隐式 claim 来源核验。 |
| P044-E03 | negative_result | §6.3–6.4, pp.7–8 | ablations | [AUTHOR_FACT] granular rubric 单独加入反而变差。 |
| P044-E04 | limitation | §7, p.9 / App. | judge/oracle/error propagation | [AUTHOR_FACT+CODEX_SYNTHESIS] 自动评价边界。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Shared Rubric plus Task-Evidence Guidance Evaluation`
- Baseline：动态生成 criteria 或用一组宽泛维度让 judge 自行选择关注点。
- Changed evaluation：共享固定维度保证可比；task-specific evidence/guidance 只锚定本任务必查内容；claim support 另由外部证据链核验。
- 边界：开放科研中 guidance 不能来自答案 oracle；Reviewer 只能从独立论文/实验 artifact 构建窄 Claim 检查项。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Granular Rubric Without Domain Anchor`
- 现象：检查项数量增加，但 judge 不知道哪些细节对本任务关键，导致一致性与人类相关性下降。

## 首读裁决

`KEEP_FOR_SECOND_READ`。与 P042/P043 组成评测协议谱系，直接约束 reviewer 设计但不生成自动评分器。
