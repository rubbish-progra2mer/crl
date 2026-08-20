# P018 — Codex 首读

- PDF：`knowledge_base/staging/papers/P018_expel.pdf`
- PDF SHA-256：`01e533d81fb4a5f91797c073a9b1929acbaa64da45a592b26563ca7d135024f3`
- 读取时间：`2026-07-19T16:20:00+08:00`
- 读取范围：逐页检查 1–38 页；正文 1–10 页、参考文献 10–12 页、方法背景与实验细节 13–15 页、prompt 16–18 页、完整 insight 示例 18–22 页、行为案例 23–35 页、补充统计 35–38 页；对关键图表和图内文字另作可视检查。

## 方法实际改变的计算

- [AUTHOR_FACT] ExpeL 有三个阶段：在训练任务上用 Reflexion 最多重试 `Z` 次收集成功/失败 trajectories；从同任务 success/failure pairs 与跨任务 success groups 抽取自然语言 insights；测试时把全部 insights 和按 task embedding 检索的 top-k 成功 trajectories 拼入 ReAct prompt，单次作答。
- [AUTHOR_FACT] Experience retrieval 使用 Faiss kNN、`all-mpnet-base-v2` task embedding，只检索训练池中的成功轨迹；它改变的是 evaluation prompt 中的 in-context demonstrations。
- [AUTHOR_FACT] Insight extraction 由 `gpt-4-0613` 迭代执行 ADD、EDIT、UPVOTE、DOWNVOTE；新 insight 初始 count=2，降到 0 时删除。输入是成功/失败轨迹对或 `L` 个成功轨迹，输出是持续更新的规则列表。
- [AUTHOR_FACT] Evaluation policy、experience gathering reflection 默认使用 `gpt-3.5-turbo-0613`（超长时 reflection 使用 16k 版本），所有 evaluation agents 使用同一 `gpt-3.5-turbo-0613`、temperature 0、greedy decoding。
- [READER_INTERPRETATION] “Learning”发生在外部自然语言 memory/prompt construction，而非参数更新；核心干预是规则抽象与成功轨迹检索的组合，并非单一 reflection。
- [READER_INTERPRETATION] Insights 的 count/update 是 LLM 对批次顺序敏感的文本维护过程，不是由独立 reward 或统计检验校准的置信度。

## 数据、基线与协议

- [AUTHOR_FACT] 任务为 HotpotQA、ALFWorld、WebShop；HotpotQA/FEVER 使用 Wikipedia Docstore API。作者称使用 four-fold validation，并又描述“train on one half, evaluate on the other half, and vice versa”。评测集为 HotpotQA 100、ALFWorld 134、WebShop 100 个 ReAct/Reflexion 使用过的任务。
- [SOURCE_AMBIGUITY] “four-fold”与“两半互换”的具体 fold 构造、训练池大小、重复方式在 PDF 中没有完全展开，不能仅据此重建严格的数据拆分。
- [AUTHOR_FACT] 主基线是 Act、ReAct，另引 ReAct+Reflexion 的多轮结果；组件比较包括 insights-only 与 retrieve-only。Imitation Learning 数字取自 ReAct 论文，不是同一新运行。
- [AUTHOR_FACT] WebShop 被改为固定平均价格约束，并把每页 items 从 3 扩为 10；虽然所有本论文 agent 可共享修改环境，但数字不宜与原始 WebShop 配置直接等同比较。
- [AUTHOR_FACT] Prompt/fewshot 来自 ReAct/Reflexion，但 WebShop 额外增加到两个 fewshot examples。
- [AUTHOR_FACT] 所有实验运行于单机 i9-9900K、64GB RAM、RTX 2080 Ti；API 调用发生在 2023-07-10 至 2023-08-10。

## 主要结果及其窄解释

- [AUTHOR_FACT] Figure 5 success rates：HotpotQA Act 29、ReAct 28、insights-only 36、retrieve-only 31、ExpeL 39；ALFWorld Act 28、ReAct 40、insights-only 50、retrieve-only 55、ExpeL 59；WebShop IL 29、Act 34、ReAct 35、insights-only 37、retrieve-only 38、ExpeL 41。图中误差箭头为跨 folds 标准误。
- [AUTHOR_FACT] 与 Reflexion 多次尝试的横线比较：HotpotQA ExpeL 39 接近 Reflexion R3 40；ALFWorld ExpeL 单次 59 高于 Reflexion R3 54；WebShop ExpeL 41 位于 Reflexion 的较低区间，低于其后续重试值。
- [READER_INTERPRETATION] 主结果支持“训练任务经验经抽象与检索后，可改善同分布未见任务的单次 prompting 表现”；它不支持零训练数据的自我改进，也不等同于测试任务上的在线学习。
- [AUTHOR_FACT] HotpotQA→FEVER transfer：Act 58±0.0、ReAct 63±0.4、无 target demos 的 insight adaptation 65±1.7、使用 target task demos 的 ExpeL Transfer 70±0.7；target demos 同时用于调整 insights 和执行时 fewshot。
- [READER_INTERPRETATION] Transfer 发生在共享 Wikipedia search API 和相似检索技能的两个任务间；结果支持有限的同工具机制迁移，不足以证明跨无关 domain 的普适 transfer。
- [AUTHOR_FACT] ALFWorld retry 表：ExpeL+Reflexion R0 59.0，R1/R2/R3 为 60.4/63.4/64.2；retrieve-only 为 54.5/57.5/59.7/60.4，ReAct+Reflexion 为 40.3/47.8/52.2/54.4。R1–R3 从 R0 failed checkpoints 继续。

## 预算与公平性

- [AUTHOR_FACT] Appendix Table 6 的平均 total tokens 显著不同：HotpotQA ReAct 1319.75、ExpeL 4310.06；ALFWorld 2051.49 对 2856.7；WebShop 2575.41 对 3291.31。Insights-only/retrieve-only 也普遍高于 ReAct。
- [AUTHOR_FACT] ExpeL 在 HotpotQA 的 action/observation 数不比 ReAct 更多（4.8/4.87 vs 5.18/5.19），但 prompt context 带来约 3.27 倍 total tokens；论文没有 equal-token 或 context-length-matched baseline。
- [READER_INTERPRETATION] 因而主提升无法排除“更多、且由训练任务与 GPT-4 产生的上下文”这一资源优势；这不是伪结果，但 Claim 必须写成 memory-augmented prompting 在其额外预算下有效，不能写成同预算策略改进。
- [AUTHOR_FACT] Insights 由 GPT-4 生成，而 evaluation policy/主 ReAct 基线为 GPT-3.5；论文没有计入/对齐离线 GPT-4 insight-extraction 成本。
- [READER_INTERPRETATION] Ours 同时拥有 insights 与 retrieved trajectories，组件消融支持两者各自有用，但没有一个 total-token matched concatenated-control 来排除纯上下文容量效应。

## 负向结果与机制边界

- [AUTHOR_FACT] HotpotQA ablation：ReAct 28.0±1.4，hand-crafted insights 32.0±1.1，`insights with reflections` 29.0±0.4，GPT-3.5-generated insights 32.0±0.4，完整 GPT-4 ExpeL 39.0±1.7。
- [AUTHOR_FACT] 作者解释，将 raw reflections 额外加入 insight construction 反而有害，可能因为 reflection hallucinations 污染抽象过程。
- [READER_INTERPRETATION] 这是可记录的真实负向证据：并非更多 reflection/memory 一定更好；未经 success/failure 对比和跨样本规则维护的反思可能向长期记忆传播错误。
- [AUTHOR_FACT] ALFWorld retrieval ablation：reasoning similarity 48.5±2.1，random 42.5±0.8，task similarity 59.0±0.3，ReAct 40.0±0.3。作者认为逐步变化的 reasoning-retrieved fewshots 可能造成 instability。
- [READER_INTERPRETATION] Task-level stable retrieval 优于 trajectory 内动态 reasoning retrieval 的结果，提示 memory injection 的一致性可能比局部语义相似度更重要；但仅在 ALFWorld 单设置验证。
- [AUTHOR_FACT] 作者限制包括：只研究文本 observation、依赖 closed-source API、insight 列表尚未超过 context limit，真正 lifelong setting 需要额外 retrieval；prompting 缺少 RL 式理论保证。
- [READER_INTERPRETATION] 所展示“emergent abilities”来自人工挑选的成功案例，并明确省略 irrelevant/non-representative steps；只能作为机制例示，不能作为新能力发生率或因果归因证据。
- [READER_INTERPRETATION] Figure 16/17 的“回看 observation 后猜对”、Figure 18/19 的 world prior/self-correction，都有可能由拼入的具体规则或 retrieved demonstration 直接诱导；论文没有逐项删除对应 insight 来验证单条规则因果作用。

## 可抽取候选（尚非正式 Card）

- Operator：`Dual-Level Experiential Memory Injection`——从训练任务轨迹同时形成跨任务自然语言规则与按任务相似度检索的成功示例，在 inference prompt 中并用。
- Operator：`Contrastive Experience-to-Rule Maintenance`——把同任务失败/成功对与跨任务成功集合交替输入，以 ADD/EDIT/UPVOTE/DOWNVOTE 维护可复用规则。
- Failure：`Unfiltered Reflection Contaminates Long-Term Insights`——把反思文本直接加入规则抽取使 HotpotQA 从完整方法 39 降至 29，接近 ReAct 28；潜在原因是 hallucinated reflection 被长期化。
- Failure：`Dynamic Reasoning-Similarity Retrieval Destabilizes Context`——随轨迹最新 reasoning 动态替换 examples，在 ALFWorld 明显低于稳定的 task-similarity retrieval。
- Failure：`Experience Gain Confounded by Context/Teacher Budget`——离线 GPT-4 抽取及更长 prompt 未做 equal-budget 对照，限制了对机制效率的归因。

## 未解决问题

- `[OPEN_QUESTION]` four-fold validation 与 half-swap 的精确构造、随机种子及各 training experience pool 的确切规模。
- `[OPEN_QUESTION]` Full ExpeL、insights-only 与 retrieve-only 的离线 API token/call 总成本，以及是否跨 folds 完全独立生成 memory。
- `[OPEN_QUESTION]` 逐条 insight 的输入来源、更新顺序和 count 历史未在 PDF 中完整给出，无法复核规则是否由 test-adjacent manual choices 影响。
- `[OPEN_QUESTION]` “emergent ability”案例的选择协议和发生频率未报告；只能保留为案例观察。
