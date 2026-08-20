# P043 Codex 首读：DeepResearch Bench

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P043_deepresearch_bench.pdf`
- PDF SHA-256：`8fbf30398f5e62f8839f0c9c8609bbb9e3cd0b57ae27d4bf33cb5db2007d1118`
- 读取范围：全文（31 页），重点为 RACE/FACT、人评验证与限制。

## 研究对象与方法

- [AUTHOR_FACT] 100 个 PhD-level tasks、22 fields；RACE 动态生成 dimension/criterion weights，以 Gemini Deep Research reference 做相对评分；FACT 抽取 statement–URL pairs 并验证网页支持。
- [CODEX_SYNTHESIS] 论文是 long-form research 评价从粗总分走向 task-adaptive criteria 与 citation support 的早期谱系节点，但其动态 judge-generated criteria 后来受到 P042/P044 的稳定性批评。

## 关键验证

- 50 个中文 tasks、四 agents、三名 domain expert；过滤掉 ICC<0 的任务后只剩 37 个用于 per-task correlation。
- RACE pairwise agreement 71.33%，human inter-agreement 68.44%；去 reference 后降至 66.56%，说明 reference 有用，但同样可能把 reference 风格/遗漏写入标尺。
- FACT 用 Gemini-2.5-Flash 验证 100 个 statement–URL pairs，support/not-support 与人工一致 96%/92%。样本规模有限，且不覆盖 claim extraction recall 的全部误差。
- reference 来自同一商业系统在特定日期的输出，且作者不能确认期间是否迭代；被评 Gemini 系统存在潜在 reference advantage。

## 与后续工作的冲突/边界

- P042 报告单 judge 与动态整体评分有高 variance，采用多 protocol/多 judge；P044 认为动态 criteria 不够可比，改为固定 expert taxonomy + task-specific guidance。
- 100 tasks 偏小、human evaluation throughput 有限、domain curation 有偏差；商业模型版本漂移。
- RACE absolute score 是 reference-relative，作者也要求关注排序而非绝对值；不可转为 CRL 自动科研分数。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P043-E01 | evaluation | §3, pp.4–6 | RACE/FACT | [AUTHOR_FACT] adaptive criteria + claim URL support。 |
| P043-E02 | evaluation | §4.3, pp.7–9 | human consistency | [AUTHOR_FACT] reference 与 criteria ablation。 |
| P043-E03 | limitation | App. A, p.17 | limitations | [AUTHOR_FACT] scale/domain/human throughput。 |
| P043-E04 | conflict | P042/P044 nearest prior | protocol critique | [CODEX_SYNTHESIS] 后续固定细粒度评价的动机。 |

## Card 草案（不进入正式 Cards）

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Reference-Relative Research Score Inherits Reference Blind Spots`
- 现象：target 与单一高质量 report 相比提高区分度，但 reference 的风格、覆盖和系统偏差成为隐含 ground truth。
- 约束：reference 只作对照，不得让它替代独立 claim evidence 与 task requirement。

## 首读裁决

`KEEP_FOR_SECOND_READ_AS_NEAREST_PRIOR`。主要用于谱系和冲突调和，不优先生成新 Operator。
