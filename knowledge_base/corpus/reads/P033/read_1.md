# P033 Codex 首读：Self-Refine

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P033_self_refine.pdf`
- PDF SHA-256：`a07dfc5ada4ff818c77812dd581065a4e3e40f5736f2f36a97787a66da6e7825`
- 读取范围：正文（pp.1–10）、任务/评测与分析附录、人工偏好与失败案例。

## Changed computation

- [AUTHOR_FACT] 同一 LLM 依次作为 generator、feedback provider、refiner；把历史输出与反馈追加进 prompt，最多四轮或由任务停止条件终止，无参数更新。
- [CODEX_SYNTHESIS] 真正作用变量是“可执行、具体的反馈”，不是 reflection 标签或多轮本身。

## 结果与对照

- 七任务上报告 5–40 个百分点提升，但任务异质：多项使用 GPT-4 preference 或 human A/B；数学推理几乎不变（GPT-4 92.9→93.1，ChatGPT 74.8→75.0）。
- 数学任务中 ChatGPT 对 94% 实例反馈“everything looks good”；若外部信号指出答案错误，增益才超过 5%。
- actionable feedback、generic feedback、no feedback 对代码优化为 27.5 / 26.0 / 24.8；sentiment reversal 为 43.2 / 31.2 / 0。
- 首轮收益最大，后续边际递减；多 aspect 任务可能一个维度改善、另一维度退化。
- 对 35 个失败案例的人工分析中，33% 因反馈错定位，61% 因建议了错误修复，只有 6% 是 refiner 未正确执行好 feedback。
- instruction-only 设置需要大量 prompt engineering；弱模型即使给 oracle feedback 也可能不遵循 refinement prompt。

## 失败边界与公平性

- 主结果未系统控制额外 sampling/token；虽然作者做人类 1-vs-4 初始样本比较，它仍不是统一成本匹配评估。
- preference judge 可能偏好更长、更润色的回答；大幅提升不能直接等同事实正确性或 Agent task success。
- few-shot 示例包含如何反馈和如何修正，不能把结果解释成模型自发发现研究缺口。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P033-E01 | mechanism | §2, pp.2–4 | Algorithm 1 | [AUTHOR_FACT] feedback/refine loop。 |
| P033-E02 | negative_result | §3.3, p.6 | math analysis | [AUTHOR_FACT] 无错误识别时数学几乎不增益。 |
| P033-E03 | ablation | §4, p.6 | Table 2 | [AUTHOR_FACT] specific feedback 优于 generic/no feedback。 |
| P033-E04 | failure | §4, p.8 | qualitative analysis | [AUTHOR_FACT] 失败主要源于错误反馈。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Actionable Feedback-Conditioned Refinement`
- Baseline：直接再次生成或只给“请改进”一类 generic instruction。
- Changed computation：先输出针对具体缺陷与动作的 feedback，再以该 feedback 和完整迭代历史条件化修订。
- 前提：feedback accuracy 单独评估；token/call matched；保留原本正确项；最终质量由独立 verifier 判断。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Self-Feedback Bottleneck in Iterative Refinement`
- 现象：refiner 能执行反馈，但 critic 找不到真实错误或建议错误修复，导致停滞、表面改写或正确性回退。

## 首读裁决

`KEEP_FOR_SECOND_READ`。必须与 P032、P034 冲突调和，不能单独把“平均约 20%”写入正式知识。
