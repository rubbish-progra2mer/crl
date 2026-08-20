# P016 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P016_mast_failures.pdf`
- PDF SHA-256：`6aff168d6e201217d3f79611f6ad024590a599a03b97ac2aeb0b0b128bac374c`
- 读取时间：`2026-07-19T15:50:00+08:00`
- 读取范围：逐页检查 1–54 页；正文 1–10 页，参考文献 11–23 页，taxonomy/system/dataset/correlation 24–31 页，strategy/intervention/model/benchmark/cost 32–37 页，AG2/ChatDev prompts 38–44 页，13 组 failure examples 45–54 页。

## 研究对象与数据生成链

- [AUTHOR_FACT] MAST 不是自动修复方法，而是从 5 个 MAS 的 150 traces 由 6 名专家按 Grounded Theory 开放编码得到的 14-mode taxonomy，分 System Design、Inter-Agent Misalignment、Task Verification 三类。
- [AUTHOR_FACT] 定义通过三轮 IAA：每轮 3 experts 独立标 5 条、讨论修订，最终平均 Cohen κ=.88；另在两种 unseen MAS/benchmarks 做一轮得到 κ=.79。公开 MAST-Data-human 总共 21 triple-annotated traces。
- [AUTHOR_FACT] 大规模 1642 traces 的 failure labels 主要由 OpenAI o1 few-shot annotator生成；在 held-out human labels 上 accuracy .94、recall .77、precision .833、F1 .80、κ=.77。Prevalence 图与跨系统分布因此是模型标注统计，不是 1642 条全人工 root-cause adjudication。
- [READER_INTERPRETATION] 知识库应把 MAST 当 failure vocabulary 与 trace-inspection checklist，不把它程序化成自动科研 ontology/score。其 value 在于促使 Codex逐 trace区分表面相似原因，而非计数即裁决。

## 覆盖、分母与比较边界

- 7 frameworks 涵盖 coding、math、GAIA/general agent；模型含 GPT-4/4o/4o-mini、Claude3.7、Qwen2.5-Coder、CodeLlama。各 configuration trace 数从 30 到 206，benchmark与模型不统一。
- Figure 5 的 41–86.7% failure rates来自不同 systems+benchmarks，作者明确不可横向当 MAS ranking。Figure 4 只画每 system前30条共210 traces 的 profiles，也不是1642完整分布。
- 一个 trace 可有多个 failure modes；Figure 1 的 mode/category percentages 是 failure occurrence组成，不是独立 task failure probability。Appendix Table 8 category rate甚至可大于1（每trace多次/多label）。
- 14 modes包含行为与推断 root cause混合：如 loss history、ignored input、withholding可能共享表面症状。Fine-mode最高相关 .63，作者承认 LLM annotator可能混淆。
- “System design issue”并不排除 model limitation；正文明确列 architecture、poor user prompt、LLM instruction-following三种可能来源。Taxonomy category不能单独证明因果归属。

## 主要发现与窄解释

- 全集图示占比约 FC1 44.2%、FC2 32.3%、FC3 23.5%；高频 modes包括 step repetition 15.7%、reasoning-action mismatch 13.2%、unaware termination 12.4%、disobey task 11.8%。这些是annotator-observed prevalence，不是统计显著因果效果。
- 同 ProgramDev-v2+MetaGPT 时 GPT-4o相对Claude减少FC1/FC2；同 GPT-4o+ProgramDev-v2 时 MetaGPT相对ChatDev减少FC1/FC2但FC3更多。固定两因素之一支持 architecture/model都影响 profile，但没有随机化framework components。
- Successful traces仍可被标 verification failures，failed traces通常更多 modes。小表样本（ChatDev success 10、fail20；MetaGPT success12、fail18可由百分步长推断）说明某 mode非充分/必要失败条件。
- MAST建议 multi-level verification：低级compile/test与高级task objective并列。Chess case展示代码/浅tests通过却规则不完整，support“有 verifier ≠ verification正确”。
- Open-source 400 traces 中 CodeLlama failure counts普遍远高Qwen，但模型大小/能力不同；只说明此配置差距，不分离 model规模、instruction tuning与framework交互。

## Intervention证据与冲突

- AG2 GSM-Plus 200随机题、baseline/improved prompt/new 3-role topology、GPT-4/4o、6 repeats。GPT-4 prompt 84.75→89.75，topology85.50且p=.4不显著；GPT-4o prompt89.00、topology88.83相对84.25，Wilcoxon p=.03。Tactical fix依赖model。
- ChatDev在ProgramDev-v0 32 tasks由25.0→34.4→40.6，HumanEval 89.6→90.3→91.5；没有reported repeats/CI/significance。所谓 +15.6 是ProgramDev-v0 absolute gain，不是跨任务保证。
- [SOURCE_CONFLICT] Appendix H.3 文字称两 interventions “decrease across different failure modes”且 topology更有效；Figure 10 的 AG2 prompt counts在多数 modes/category反而高于Original（如FC1 625→692、FC2 687→796、FC3 171→205），只有topology明显下降。文字与图对prompt intervention冲突，正式 Card必须保留未解决状态。
- [READER_INTERPRETATION] Intervention后的 failure counts由同一 o1 annotator产生且配置可能有不同有效 trace/turn长度；未给normalized denominator/annotator盲化。不能用这些counts强因果证明某prompt“修复某mode”。Task accuracy evidence相对更直接。

## 失败边界与限制

- [AUTHOR_FACT] MAST不声称 exhaustive；taxonomy来自特定7 frameworks、以coding/math居多，closed-source Manus因无完整traces未纳入primary dataset。
- [AUTHOR_FACT] LLM annotator recall .77、F1 .80，意味着稀有/相似 modes会漏标或混标；0.8% information withholding等小比例不能精确排序。
- [AUTHOR_FACT] Existing verifiers常只看compile、TODO等表面条件；verification itself会 incorrect，添加reviewer不等于获得ground truth。
- [AUTHOR_FACT] Prompt/role/topology tactical changes效果不一致，作者明确认为需更深的verification、communication、uncertainty、state/memory等研究，但这些是future strategies，不是本文已验证结果。
- [READER_INTERPRETATION] IAA κ=.88基于最终每轮仅5 traces的小集合，不能证明所有1642长trace上human annotation同等稳定；公开human set 21条仍很小。
- [READER_INTERPRETATION] 每trace平均超15,000 lines，而o1输入处理、截断策略与exact prompt未在PDF完整呈现；长trace中的early failure可否稳定可见是关键开放点。
- [READER_INTERPRETATION] “theory of mind collapse”“organization design primacy”等是作者解释/研究假设，MAST observations本身不足以排除base model或benchmark artifact。

## 可抽取候选（尚非正式 Card）

- Evaluation Operator：`Stage-Localized Multi-Agent Failure Trace Audit`——按pre/execution/post逐步定位spec/state、information flow、verification，而非只看最终success。
- Evaluation Operator：`Multi-Level Objective Verification`——低级syntax/tool execution与高级task constraints/real behavior分别验证，记录verifier自身错误。
- Failure：`Reasoning–Action/Message Mismatch`——agent内部已发现正确依据，却传递/执行了不同内容，单纯增加context无效。
- Failure：`Superficial Verification Accepts Objective-Incomplete Output`——compile或浅tests通过但任务规则/edge cases缺失。
- Failure：`Termination Governance Failure`——不会停止与过早停止分别造成loop或不完整交付，终止权限/条件需要显式且可核验。
- Failure：`Inter-Agent Information Flow Breakdown`——withholding、ignored input、failure-to-clarify须依trace证据区分，不能仅按最终缺信息自动分类。
- Failure：`Taxonomy Annotator Confuses Correlated Root Causes`——相似表象与长trace使自动labels漏标/混标，频率不得替代人工科研判断。

## 未解决问题

- `[OPEN_QUESTION]` LLM annotator对每个mode的per-class precision/recall、长trace截断和prompt exact bytes，PDF未完整披露。
- `[OPEN_QUESTION]` Figure 1 prevalence的精确分母是mode occurrences还是trace-level binary aggregation，图注与正文不足以完全复算。
- `[OPEN_QUESTION]` Figure 10 prompt intervention文字与柱状counts为何相反，需要代码/data核对；本Pilot只以PDF标记冲突。
- `[OPEN_QUESTION]` Human IAA set与o1 calibration/validation examples是否严格不重叠、few-shot如何选取，论文描述不足。
