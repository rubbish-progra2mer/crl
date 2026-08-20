# P020 — Codex 首读

- PDF：`knowledge_base/staging/papers/P020_agenttts.pdf`
- PDF SHA-256：`454906b0f931fd092ab25163c1ea3fd69e793eac570320ba257d174bee9b0c7c`
- 读取时间：`2026-07-19T17:20:00+08:00`
- 读取范围：逐页检查 1–38 页；正文 1–10 页、参考文献 11–15 页、NeurIPS checklist 16–22 页、成本推导/数据/模型与完整 budget tables 23–28 页、补充 scaling 曲线 29–31 页、完整搜索案例与 prompts 32–35 页、基线/限制/影响 35–38 页；关键图表和 prompts 另作可视核对。

## 方法与输入输出

- [AUTHOR_FACT] AgentTTS 解决静态 multi-stage pipeline 的离散模型选择与每阶段 repeated-sampling budget allocation；每个候选配置指定各 subtask 的 model 和 sample count，总预算由归一化 inference-FLOPs 或 API price 约束。
- [AUTHOR_FACT] 每个 subtask 的多个 samples 由同一 LLM 使用 temperature 0.9 生成，再由同一 LLM 按 fusion prompt 汇总；方法不使用独立 verifier/reward model。
- [AUTHOR_FACT] 搜索 Agent 使用 GPT-o3-mini。Archive 保存 candidate、performance feedback 与 LLM 生成的 guidelines；Environment 在 50 个 training samples 上实际执行候选；迭代 50 trials 后返回 training performance 最佳配置，再在 500 个 disjoint test samples 上评估。
- [AUTHOR_FACT] 初始阶段以同一 target subtask 的 equal maximum budget 比较模型大小，其他 stages 固定最大模型 single-pass；若大模型优势不显著，则优先小模型。后续 prompt 明示“先增长后饱和”“subtasks 相互依赖”和低方差时 mutation/crossover/random exploration 三类先验。
- [READER_INTERPRETATION] AgentTTS 的实际干预是把人工总结的三条 search priors 写入 prompt，并让通用 LLM 根据小样本实验史提出下一批离散配置；核心不是自动发现 TTS 定律，而是 prior-conditioned black-box optimization。

## 三条 empirical insights 的证据边界

- [AUTHOR_FACT] Insight 1：同一 subtask 内不同 model size 的 compute-performance tradeoff 不同；例中 retrieval 偏好 Qwen2.5-72B 单样本，QA 在有限预算下常偏好 Llama-3 3B/8B 多样本。
- [AUTHOR_FACT] Insight 2：重复 samples 增加后，fusion performance 会波动、饱和或下降；2Wiki 示例中 QA 的最佳 sample count 随 model/retrieval quality 变化。
- [AUTHOR_FACT] Insight 3：上游 retrieval F1 被分成约 0.8/0.6/0.35 条件后，下游 QA 的最佳 model/sample budget 随输入质量变化。
- [READER_INTERPRETATION] Insight 1–3 是有用的搜索模式，但其原始 pilot curves 就来自与最终评测相同的六个 datasets/task types；论文没有 leave-one-dataset 或 leave-one-task-type transfer 来证明它们能在未参与总结的新 pipeline 上保持搜索优势。
- [AUTHOR_FACT] Appendix A.5 先在各 subtask 上比较多个 model families，再为 retrieval 选 Qwen、其他 stages 选 Llama；ChatDev 因无中间指标被排除该分析。
- [READER_INTERPRETATION] Candidate family selection 和三条 priors 均利用了额外的 dataset-specific pilot experiments。它们可以作为方法开发知识，但其成本不应从“search efficiency”总叙述中隐去。

## 成本定义与近似

- [AUTHOR_FACT] FLOPs normalization 把最小模型 3B、prompt 128、decode 64、1 sample 定义为 budget 1；先计一次 shared prompt encoding，再按 samples 线性累加 decode FLOPs，并忽略作者称通常低于 1% 的 attention terms。
- [AUTHOR_FACT] 预算使用每个 subtask 的平均 prompt/decode lengths，而不是逐实例实际 lengths；main search 以 H100 80GB 执行，parallel samples 假设可共享 prompt encoding。
- [READER_INTERPRETATION] 这是透明、可复算的 proxy，但不等于实际 wall-clock、显存占用或服务价格；batching efficiency、KV cache、kernel utilization 和实际输出长度会改变真实成本。
- [AUTHOR_FACT] API-price 补充实验只在 2Wiki QA 上用 Together AI 单价重画曲线，并再次展示 search trace；因此“跨 cost metrics 泛化”证据目前限于一个任务。
- [SOURCE_AMBIGUITY] Problem definition 写 `ΣB_i=B`，算法与案例实际接受未用满预算的配置（例如 used budget 876/900）；可执行约束显然更接近 `ΣB_i≤B`。

## 主结果与公平比较

- [AUTHOR_FACT] 所有搜索方法在同一 50-sample training set 上最多 50 trials；Figure 3 的虚线 Best 是“prior grid search”找到的 training optimum。Table 1 的 time 是找到 optimum 的时间；“–”表示不可用或未在预算内找到 optimum。
- [AUTHOR_FACT] Test results：2Wiki AgentTTS 0.72 vs LLM baselines 0.70；Hotpot 0.74 与 AgentHPO 并列；CWQ 0.78 与 MLCopilot/AgentHPO 并列；WebQSP 0.89 与两基线并列；TaskBench 0.53 与 MLCopilot 并列；ChatDev 0.75 与 BO/MLCopilot 并列。
- [READER_INTERPRETATION] AgentTTS 的主要支持是更少 trials/更短 time 达到已知 training optimum；六个 test metrics 中只有 2Wiki 明确高于表内下一最佳值，其余多为并列。不能把它写成在所有任务上稳定提高 final task quality。
- [AUTHOR_FACT] 作者在 checklist 明确回答“Experiment statistical significance: No”，理由是计算成本高，未报告 variance；所有 main curves/tables 无 error bars、置信区间或多随机种子。
- [READER_INTERPRETATION] 2Wiki test 的 2-point 差异来自 500 samples 且无重复/区间，不能严谨称 statistically significant；论文摘要/正文中的 “significantly outperforms”只能按口语“明显”理解，非统计显著。
- [SOURCE_CONCERN] Prior grid search、six-dataset pilot curves、model-family screening 的计算没有计入 AgentTTS 的 Table 1 search time；若 Claim 是方法首次面对任务时的 total search cost，该比较低估了建立先验的离线成本。
- [READER_INTERPRETATION] 若三条 insights 被视为一次性、跨任务可复用的研究知识，则应在 unseen task-type transfer 中验证；论文未提供。若视为本任务 pilot knowledge，则必须把 pilot cost计入。

## LLM 作用是否被隔离

- [AUTHOR_FACT] AgentHPO、MLCopilot、LLM-ZS、AgentTTS 均用同一 GPT-o3-mini 搜索 agent；AgentTTS 的独特输入是三条定向 TTS priors 和结构化初始化。
- [AUTHOR_FACT] Ablation 仅在 2Wiki、budget 900 上逐一删除 Insight 1/2/3；删除后到最优的 trial 变慢或失败。
- [READER_INTERPRETATION] Ablation 支持三条 prompt priors 有用，但没有“同样三条规则 + 非 LLM deterministic/evolutionary controller”的基线。因此无法区分增益来自 LLM planning，还是来自简单 search heuristic 获得了更强领域先验。
- [AUTHOR_FACT] MLCopilot 获得 similar-task search history，AgentHPO 获得结构化 task/model/budget，但作者明确指出它们没有 AgentTTS 的 tailored insights。
- [READER_INTERPRETATION] 这是一种 prior-advantaged comparison，而非完全信息对称比较；合理的窄 Claim 是“给 GPT-o3-mini 注入这三条经验规则，比所适配基线更快”，而非“LLM agent 本身发现了更优分配”。
- [SOURCE_CONFLICT] NeurIPS checklist 的 LLM usage 项回答 `[NA]`，称核心方法没有重要/原创/非标准 LLM component；但正文把 GPT-o3-mini Agent 的 guideline/candidate generation 定义为核心框架。至少在信息披露口径上存在明显张力。

## 负向与未测试边界

- [AUTHOR_FACT] Test-time scaling 并非单调；更多 samples 可因小模型能力和 fusion bottleneck 使性能下降。Temperature table 也呈明显非单调：同 sample count 的最佳 temperature 在 0.1/0.5/0.9 间变化。
- [AUTHOR_FACT] 作者唯一正式 limitation 是只支持预定义、静态 stages，无法直接处理运行时由输入或交互动态决定的 subtask graph。
- [READER_INTERPRETATION] Training set 仅 50 samples，objective surface 含采样噪声；一次 50-trial trace 可能把偶然高分配置当 best。无多 seed 是搜索效率 Claim 的关键限制，不只是展示细节。
- [READER_INTERPRETATION] ChatDev 的 Consistency 是需求文本与 code semantic embedding cosine similarity，不是 functional correctness、test pass 或 user value；它只支持搜索该 proxy metric 的结论。
- [AUTHOR_FACT] Repeated-sampling fuser 明示候选可能 biased/incorrect，但没有可信 verifier；作者在 broader impact 中承认 scaling 可放大/传播 hallucination 与安全风险。

## 可抽取候选（尚非正式 Card）

- Operator：`Insight-Conditioned Multi-Stage Budget Search`——将 stage-specific model preference、diminishing return、cross-stage dependence 写入 LLM optimizer prompt，用真实小样本执行反馈迭代候选。
- Operator：`Equivalent-Compute Model/Sample Allocation`——把不同模型、stage token profile 与 sample count 映射到共同预算单位，在固定总预算下比较大模型少采样与小模型多采样。
- Failure：`Offline Pilot Cost Omitted from Search-Efficiency Claim`——同数据集 pilot curves、model-family screening 和 grid optimum 提供强先验，却未计入在线搜索时间。
- Failure：`Prior Advantage Mistaken for LLM Planning Advantage`——方法比基线获得更具体的领域规则，且缺少同规则的非 LLM controller，不能隔离 LLM 推理的因果贡献。
- Failure：`Noisy Small-Set Optimum Without Repeated Search`——50-sample objective、temperature sampling、无 variance/seed，使“更快到最优”可能依赖一次轨迹噪声。

## 未解决问题

- `[OPEN_QUESTION]` 每个“trial”是单一配置还是 batch candidates；Table 1 time 是否包含 initial candidates 和 GPT-o3-mini latency/cost，PDF没有给出完整计数分解。
- `[OPEN_QUESTION]` Preliminary pilot curves、family screening 和 prior grid search 的总 H100/API cost，以及是否与 50-sample search 使用完全相同实例。
- `[OPEN_QUESTION]` 在全新 task type、未做 dataset-specific pilot 时，三条 insights 是否仍比通用 HPO priors有额外价值。
- `[OPEN_QUESTION]` 相同 priors 交给简单 rule-based/evolutionary search 后是否可达到同等或更高效率。
- `[OPEN_QUESTION]` 500-test-set结果和搜索 trace 在不同 random seeds/temperature generations 下的稳定性。
