# P034 独立二读报告

- Attempt：`r2-20260719-p034-a1`
- PDF SHA-256：`ee5c4d93ddf6c0741f0d08042b6aca2e0f08c3d3bd70e6cc6c90378bbc2d8c7f`
- 阅读范围：物理页 1–44，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`
- 第三读触发建议：`YES_IF_CORE_SELF_REFINEMENT_EVIDENCE`

## 1. 方法与计算干预

- [AUTHOR_FACT] RefineBench 包含 1,000 个问题、11 个领域，每题配平均 9.9 项可核对 checklist；比较无反馈 self-refinement、完整 checklist 引导和部分 checklist 引导。（物理页 1–5，摘要/§2–§3，定位词 “1,000”“11 domains”“9.9”）
- [AUTHOR_FACT] 模型先作答，再在最多五轮中自我修订；guided 条件向模型提供具体遗漏标准，partial-guided 只提供部分标准。（物理页 5–8，实验设计，定位词 “self”“guided”“partial”）
- [READER_INTERPRETATION] 干预点是把“是否存在问题”的模糊自省，替换为“针对外部给定缺口清单的定向修订”；这直接区分问题发现能力与修复能力。

## 2. 正向与负向结果

- [AUTHOR_FACT] 表 3 的 pass 指标中，自我修订从第 1 到第 5 轮大多持平或下降；例外包括 Gemini-2.5-Pro 29.5→31.3、GPT-5 27.5→29.1，而 DeepSeek-R1 8.1→7.9。（物理页 8，表 3，定位词 “Turn 1”“Turn 5”）
- [AUTHOR_FACT] 完整 accuracy 表显示部分模型下降更明显，例如 Gemini 的 accuracy 72.5→71.4，尽管 pass 增加；GPT-5 的 accuracy 增加 5.2 个点。（物理页 21，完整结果表，定位词 “Accuracy”）
- [AUTHOR_FACT] 只提供 checklist 标准、不提供参考解答，Gemini 提升 44.5 点，Llama-70B 提升 43.6 点；partial-guided 模型主要修复被明确指出的条目，对未指出问题改善有限。（物理页 8–10，guided/partial-guided 分析，定位词 “44.5”“43.6”）
- [READER_INTERPRETATION] 强正向证据指向“外部缺口定位能显著释放修复能力”；强负向证据指向“模型通常不能自行发现缺口”。这不是自我改进普遍成功，而是诊断与修复能力分离。

## 3. 数据、评测与潜在混杂

- [AUTHOR_FACT] checklist 由 GPT-4o、GPT-4.1、Claude 等生成后经作者人工审查；回译和 GPT-4.1 过滤后移除 1.1%，领域专家检查的 854 个 checklist 项中 96.1% 被判适当。（物理页 4–6，benchmark construction，定位词 “96.1%”“1.1%”）
- [AUTHOR_FACT] 主 evaluator 为 GPT-4.1；对 100 个随机 checklist-item/response 组合报告约 90% meta-accuracy。（物理页 6–7、附录 evaluator validation，定位词 “90%”）
- [READER_INTERPRETATION] checklist、reference 与 evaluator 共享模型来源，仍可能存在共模偏差；90% 的小样本验证不足以把剩余标签误差视为可忽略。
- [AUTHOR_FACT] Min-K% 污染检测只在 Llama2-13B 上执行，报告问题 0.1%、参考答案 0.5% 的低风险比例。（物理页 16–17，contamination，定位词 “Min-K%”“0.1%”“0.5%”）
- [READER_INTERPRETATION] 该检测不能排除其他被测闭源模型或训练语料中的污染。
- [AUTHOR_FACT] evaluator 成本约为 self 条件每样本 0.038 美元/51.1 秒，guided 约 0.028 美元/22.9 秒；该表并未给出所有目标模型的完整生成成本。（物理页 10，成本表，定位词 “$0.038”“51.1s”）

## 4. 质量异常、限制和失败

- [AUTHOR_FACT] 论文报告终止长度与表现的关系时写作 “R2=-0.477”；通常意义下 R² 不应为负，原文可能意指相关系数或 adjusted R²。（物理页 9–10，termination analysis，定位词 “R2=-0.477”）
- [READER_INTERPRETATION] 这是需要作者澄清的统计记号异常，相关论断不宜直接作为强证据。
- [AUTHOR_FACT] 附录示例中的个别参考答案存在明显算术/符号不一致，例如计算机科学样例的分项和总数文本不一致，工程样例的推导与最终符号不一致。（物理页 27–36，样例/reference，短定位 “375”“223245”“18800”）
- [READER_INTERPRETATION] 这些是 benchmark 标签质量的实质风险，尤其会影响 checklist 驱动的精细比较；不应因总体人工抽检率较高而忽略。
- [AUTHOR_FACT] 作者明确指出结果受领域、难度、prompt 和推理配置影响，观察趋势不证明模型缺乏相应能力。（物理页 17，Limitations，定位词 “do not prove”“domain”“prompt”）

## 5. 可抽取内容

- [READER_INTERPRETATION] Operator 候选：`把独立诊断器输出的具体遗漏项作为局部修订目标；对未指出项保持不变并做回归检查`。
- [READER_INTERPRETATION] Failure 候选：`无反馈自我修订平均不改善且可退化`；`修复能力显著高于问题发现能力`；`partial feedback 导致只修显式条目`；`共享 evaluator/checklist 来源带来共模偏差`。
- [READER_INTERPRETATION] 窄 Claim：在 RefineBench 的 checklist 任务上，外部、具体诊断显著提高修订，而无反馈 self-refinement 的平均收益很弱；不能外推成通用的自我改进失败或成功。
- [OPEN_QUESTION] 由于本文可能成为反对“再加一轮 reflection”的关键负向锚点，若用于多个 Operator 或与 P033 做强冲突裁决，建议第三读重点核验参考答案错误、指标定义和统计记号。

## 6. 解析与访问声明

- [AUTHOR_FACT] 解析覆盖物理页 1–44；表格和样例文本可读，未发现 OCR 造成上述数值异常，异常来自原文排版内容本身。正式引用复杂表格前仍建议目视复核。
- [AUTHOR_FACT] 实际模型/版本 `unknown`；程序性盲化。冻结后只读指定 PDF 与 invocation 内统一 prompt；使用本地 PowerShell、`Get-FileHash`、Python/PyMuPDF；未联网。冻结前仅用 `rg` 定位指定路径，未读论文。只写本报告。
