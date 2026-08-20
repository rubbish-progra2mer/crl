# P042 Codex 首读：LiveResearchBench

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P042_live_research_bench.pdf`
- PDF SHA-256：`579b9728b76cfd242e9c94d9ff2985e196bbc72b5a741030e4f308ede04a4f69`
- 读取范围：正文（pp.1–10）、judge alignment、evaluation prompts、systems/cost 与错误案例附录。

## 研究对象

- [AUTHOR_FACT] 100 个动态、用户导向、多面且 search-intensive 的 expert-curated tasks；DeepEval 把 coverage、presentation、consistency、analysis depth、citation association/accuracy 分开。
- [CODEX_SYNTHESIS] 对 CRL 最重要的不是用该 benchmark 直接做本机实验，而是它证明 long-form research 的单一总分会混合“搜得多、覆盖全、引用对、分析深”这些不同机制。

## 评价机制与结果

- 单一 0–10 holistic judge 在预实验中与人类一致率低于 60%，跨 runs 的 analysis depth 可差 50+ 分；论文因此按维度分别采用 checklist、pointwise issue finding、position-swapped pairwise 与 citation rubric tree。
- 主评测用 Gemini 2.5 Pro 与 GPT-5 独立评价后取平均；各 protocol 的人类 preference agreement 报告约 85.9–100%，但这是抽样 preference agreement，不是逐 claim 完全正确率。
- 17 systems 中没有同时统治 coverage、depth、citation、coherence；长报告与多 Agent 都不自动更好。
- 论文观察多数系统更像 deep searcher：收集和组织信息强，但 source synthesis 与 analysis depth 弱；所有抽查强系统仍有 unsupported-citation errors。
- 配置以“maximize performance”为目标，最大 output tokens 与失败重试未跨系统严格 cost-match；绝对系统排名不能直接解释为架构因果。

## 边界

- checklist 初稿由 GPT-5 生成并由专家验证；judge 模型与部分被评系统同族，仍可能存在风格/模型偏差。
- live web 增强时效性也降低完全复现；商业系统在评测期间可能更新。
- pairwise depth 依赖 baseline report；win rate 是相对量，不能跨不同 baseline 直接比较。
- 论文建议 memory/compression/synthesis，但其评测未因果证明某具体机制会修复 failure。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P042-E01 | evaluation | §3–4, pp.5–7 | protocol selection | [AUTHOR_FACT] 按评价对象选择 judge protocol。 |
| P042-E02 | negative_result | §5, pp.8–10 | Obs. 1–9 | [AUTHOR_FACT] 长度/多 Agent/更多检索不自动改善。 |
| P042-E03 | failure | §5, p.10 | deep searcher | [AUTHOR_FACT] coverage 与 synthesis/depth 分离。 |
| P042-E04 | limitation | §5/App. C | model/cost/live-web | [CODEX_SYNTHESIS] 排名与因果边界。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Object-Matched Multi-Protocol Research Evaluation`
- Baseline：一个 LLM 一次整体打分，混合所有维度。
- Changed evaluation：coverage 用 task checklist，consistency/citation association 用逐项找错，depth 用换位 pairwise，citation support 用可访问网页逐 claim 核验。
- 边界：不同维度不自动合成科研真值；Codex/Reviewer 仍做最终解释。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Deep Search Mistaken for Deep Research`
- 现象：更多页面、更多 Agent 与更长报告提高覆盖或引用数量，却没有跨来源论证、批判比较和可靠 citation support。

## 首读裁决

`KEEP_FOR_SECOND_READ`。是 Knowledge→Gap 与 Reviewer 评价的核心证据，但不引入其大规模 benchmark 平台。
