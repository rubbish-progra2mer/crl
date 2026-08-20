# P015 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P015_should_we_be_going_mad.pdf`
- PDF SHA-256：`8d0330933f495a3804842e8c8b0f778d8529fefeaf8d2a2dbf89d94f97bd0e70`
- 读取时间：`2026-07-19T15:43:00+08:00`
- 读取范围：逐页检查 1–23 页；正文 1–9 页，参考文献 10–11 页，跨数据 cost/time/token plots 12–15 页，完整 configuration/cost table 16–18 页，metrics 与 debate/agent prompts 19–23 页。

## 研究对象与 changed computation

- [AUTHOR_FACT] 论文统一实现 Society-of-Mind、Multi-Persona、ChatEval、Self-Consistency、Ensemble Refinement、Medprompt subcomponents 与 single-agent，在多选 QA 上扫描 agents、rounds、agent/debate prompts、summarization、sampling等配置，同时记录 accuracy、USD cost、latency、tokens、calls。
- [AUTHOR_FACT] 新增的 agreement modulation 只在 prompt 中要求 agent “X% of the time agree”，改变 Multi-Persona devil/其他 debate agents 的初始同意先验，继而改变最终 consensus/accuracy。
- [READER_INTERPRETATION] 最重要资产是负向科研控制：MAD 是高度敏感的 test-time ensemble/protocol family，必须与同调用的独立采样/聚合比较。Agreement instruction 是调节候选相关性/多样性的 Operator，不是事实 verifier。

## 设置与比较边界

- 主大规模实验用 GPT-3.5-Turbo，覆盖 MedQA 1273、PubMedQA 500、medical MMLU 123、CosmosQA 抽 500、CIAR 50、GPQA 448、Chess short 1000。GPT-4/Mixtral 只在 MedQA 做后续较小扩展。
- Medprompt 实现有意移除了 original kNN exemplar lookup，因为它需要 train/test split；保留 question randomization、few-shot CoT ensembling。本文“Medprompt”不是论文完整版本。
- “Best performance”Table 2 是每 system×dataset 从大量 configurations 中取最高，括号是 median；这不是预注册单一 protocol。K-fold-like audit 才用同类别另两个 datasets 选 hyperparameters，再算 held-out 第三个。
- Debate systems 与 SC/ER 的 calls、prompt history、summarizer/judge并非总是一一相等；论文用 cost/tokens/calls curves展示 Pareto，而非给每个 cell 强制等 compute。

## 主要结果与窄解释

- Table 2 没有 system 跨七数据集统治：Medprompt 在 MedQA .65、PubMedQA .77、Cosmos .48领先或并列；SC 在 MMLU .78、CIAR .56；single agent 在 GPQA .33；Multi-Persona 在 Chess .33。原始 MAD 不是普遍优势。
- MedQA broad sweep 中 SoM 最好 configuration .61，Medprompt总体最好且更便宜；Multi-Persona 通常比 Medprompt 低约 7 points。成本增加与 accuracy 有趋势但高度配置依赖。
- Held-out-category hyperparameter selection 中 medical 上除 Multi-Persona 外多数 ensemble/debate超过 single，SC/Medprompt最好；non-medical 上仅 Multi-Persona/SC超过 single。跨 task transfer 不稳定。
- Figure 4：SoM 从 first agent到 final有明显平均 gain，ChatEval较小，Multi-Persona反而降低；devil 强制反对会把正确初答改坏，final protocol gain不能只看最终 accuracy。
- Agreement modulation 的最优方向因 dataset 相反：MedQA/PubMedQA偏高 agreement，counter-intuitive CIAR偏低；不存在统一“多样性越高越好”。
- 在 376 USMLE subset 上，Multi-Persona调 agreement 约提升 15%、SoM约5%、ChatEval几乎不受影响；把 90% intensity 应用于 full MedQA 后报告 GPT-3 类新最好值。
- GPT-3.5 上 agreement hyperparameter 可迁移至 GPT-4 MedQA，但不迁移至 Mixtral 8x7B；protocol超参依赖 backbone architecture/behavior。

## 失败边界与限制

- [AUTHOR_FACT] MAD 原始实现一般 calls/tokens/cost更高，却不可靠超过 Medprompt/self-consistency；更多交互不是独立机制证据。
- [AUTHOR_FACT] Debate hyperparameters和agent prompt可引起高 variance；最佳设置常 dataset-specific，new dataset上不保证超过 single-agent。
- [AUTHOR_FACT] Multi-Persona的刻意 dissent可降低整体 performance；答案改变只有在变得更准确时才有价值，consensus/diversity本身不是质量指标。
- [AUTHOR_FACT] API model updates、variable latency和大规模成本限制 reproducibility；GPT-4 preliminary/generalization实验规模较小。
- [READER_INTERPRETATION] 论文先在 376-question USMLE subset 选择 90% agreement，再报告 full MedQA表现；若该 subset属于 full test set（文字如此暗示），full result含 tuning examples，不能作为完全 held-out SOTA证据。
- [READER_INTERPRETATION] 调 agreement prompt 的 `X%`不是逐题可校准概率约束，仅是语言诱导；observed first-round agreement虽变化，但机制不保证精确实现强度。
- [READER_INTERPRETATION] Multiple-choice majority/consensus 易定义；开放式 Agent research review没有 canonical answer，不能直接把 MAD协议移植为 Reviewer投票。独立异议价值需靠证据而非agreement optimum。

## 可抽取候选（尚非正式 Card）

- Evaluation Operator：`Compute–Accuracy Pareto Audit for Multi-Agent Protocols`——同时报告 calls/tokens/time/cost，并与同预算独立采样、SC、ER和single强prompt比较。
- Evaluation Operator：`First-to-Final Answer Transition Audit`——记录初答正确性、任一agent正确、答案改变、最终正确，识别debate是在修正还是破坏。
- Operator：`Task-Calibrated Agreement Prior`——通过agent prompt调节候选相关性/反对强度，但超参必须在独立validation task上选且按backbone重估。
- Failure：`Forced Dissent Corrupts Correct Initial Answers`——devil/contrarian角色把反对当目标，导致Multi-Persona低于首个agent。
- Failure：`MAD Advantage Disappears under Strong Cheap Baselines`——原协议被SC/Medprompt或single强prompt追平/超过。
- Failure：`Protocol Hyperparameter Overfitting`——从大量agents/rounds/prompts中报告dataset最佳，夸大可迁移性能。

## 未解决问题

- `[OPEN_QUESTION]` 376 USMLE subset与full MedQA的确切包含关系、调参/最终评估是否去重，PDF未明确。
- `[OPEN_QUESTION]` 各系统相同总tokens/calls下的统一accuracy表未给出，只能从scatter/Pareto判断。
- `[OPEN_QUESTION]` API版本的精确snapshot、随机种子与每配置重复次数在正文不完整。
- `[OPEN_QUESTION]` agreement modulation在开放生成、tool-use trajectory和真实协作任务上是否仍有效，未测试。
