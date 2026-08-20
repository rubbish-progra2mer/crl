# P034 Codex 首读：RefineBench

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P034_refinebench.pdf`
- PDF SHA-256：`ee5c4d93ddf6c0741f0d08042b6aca2e0f08c3d3bd70e6cc6c90378bbc2d8c7f`
- 读取范围：正文（pp.1–11）、limitations（p.17）、完整 self/guided 结果与 meta-evaluation（pp.21–23）。

## 研究对象与 Changed computation

- [AUTHOR_FACT] 1,000 个问题、11 domains、平均 9.9 个 checklist item；区分 self-refinement（无反馈）与 guided refinement（回传未满足 checklist），最多五轮。
- [CODEX_SYNTHESIS] 论文提供了拆分实验：固定同一 refinement interface，只改变外部缺陷定位是否可见，从而测量“自发现问题”与“执行给定修复”两种能力。

## 关键结果

- self-refinement 中，最强模型初始也只有约 29–31 Pass；五轮增益通常很小，部分下降。例如 DeepSeek-R1 -0.1，GPT-5 +1.7，Gemini 2.5 Pro +1.8。
- guided refinement 差异巨大：GPT-4.1 Pass 23.4→95.5，Claude Opus 4.1 18.7→98.4；较小模型仍明显受限。
- DeepSeek-R1 在第 2→3 轮出现 19.1% correct→incorrect，同时仅 8.1% incorrect→correct；多轮不是单调安全的。
- checklist 有人工适当性 96.1%；GPT-4.1 evaluator 与人工二元判断约 90% 一致，因此 judge 仍有约一成误差空间。

## 与 Self-Refine 的表面冲突调和假设

- [CODEX_SYNTHESIS] P033 的大收益集中于可润色/约束任务，常由 preference metrics 评价；数学正确性几乎不增益。P034 使用更难、更多 free-form 与 exact-match 问题，并显式比较无反馈/有 checklist feedback。两者共同支持“执行具体反馈通常强于自主发现缺陷”，而不是简单互相否定。
- 二读须检查版本时间、模型设置、prompt、Pass/Acc 定义与评价模型是否造成额外差异。

## 失败边界

- benchmark 不能证明模型在所有 domain 都不能自修正；作者明确承认 task difficulty、prompt scaffolding、token limit 和推理配置会改变趋势。
- checklist 与 evaluator 使用 reference-derived criteria，guided setting 接近强外部提示；它不是现实中总能获得的免费反馈。
- 部分原始材料含图表的文本化描述，但本文评价输入为文本；不把它扩成多模态研究方向。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P034-E01 | evaluation | §3, pp.4–6 | protocol | [AUTHOR_FACT] self/guided 受控拆分。 |
| P034-E02 | negative_result | §4–5, pp.7–11 | self-refinement | [AUTHOR_FACT] 多数模型五轮无稳定增益。 |
| P034-E03 | mechanism | App. E.3, p.22 | guided results | [AUTHOR_FACT] 缺陷 checklist 可见时显著改善。 |
| P034-E04 | limitation | App. B, p.17 | scope | [AUTHOR_FACT] prompt/task/inference 依赖。 |

## Card 草案（不进入正式 Cards）

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Iterative Refinement Without Defect Localization`
- 条件：模型只被要求再次改进，却没有独立指出未满足的条件或错误位置。
- 现象：同一错误被重复、已正确部分回退，更多轮只增加 token 而非改进。
- 未否定：目标缺陷可验证、checklist 与 reference-independent feedback 可用时，refinement execution 很强。

## 首读裁决

`KEEP_FOR_SECOND_READ`。是 P033/P032 Operator 的关键负向边界，优先级高于再做一张泛化 “reflection works” Card。
