# P017 — Codex 首读

- PDF：`knowledge_base/staging/papers/P017_information_propagation_topologies.pdf`
- PDF SHA-256：`f94767d936354030dc25f10db92a2f6f85f49b7d7163ac45b253e047ca67bd8b`
- 读取时间：`2026-07-19T16:45:00+08:00`
- 读取范围：逐页检查 1–15 页；正文 1–9 页，参考文献 10–12 页，附录实验细节、伪代码、扩展结果与案例 13–15 页。

## 研究对象与机制

- [AUTHOR_FACT] 论文研究有向无环图通信拓扑如何影响 LLM 多智能体系统中的信息传播；系统执行 `K` 轮，最后由指定 summarizer 汇总答案。
- [AUTHOR_FACT] CAPE 通过干预单个 agent 的输出，测量最终答案正确性是否翻转；TCTE 对各节点 CAPE 按 `1/sqrt(degree)` 加权后取平均。
- [AUTHOR_FACT] 两类定向干预分别是：对原本答对的问题，用 system prompt 强制某个 agent 产生错误；对原本答错的问题，直接注入正确答案作为 insight。
- [READER_INTERPRETATION] 这套量度观察的是“人为注入后最终 correctness 是否翻转”，不是自然运行中消息内容的实际因果中介，也没有直接测量信息沿每条边传播的语义过程。
- [READER_INTERPRETATION] TCTE 的 degree 权重是作者设计的汇总量；它可以用于同一实验协议内比较，但不应被记录成普适的自然传播定律。

## 因果分析实验

- [AUTHOR_FACT] 因果分析使用 6 个 GPT-3.5 agents 和 MMLU；每种拓扑分别准备 500 个原本正确的问题用于错误干预，以及 500 个原本错误的问题用于正确 insight 干预。
- [AUTHOR_FACT] 论文从 fully connected graph 随机删除边直到 chain，并反向从 chain 增加边；结果显示中等稀疏度可能在阻断错误和传播正确 insight 之间取得折中。
- [READER_INTERPRETATION] 错误由 prompt 强制、insight 直接给出正确答案，二者都是 oracle/artificial intervention。它们适合做传播压力测试，不能直接证明自然失败时系统能够识别并注入同等质量的信息。
- [OPEN_QUESTION] 正文关于“for each topology”构造原本正确/错误集合的表述，未充分说明跨拓扑曲线是否使用完全相同的题目；若各拓扑按自身初始正确性条件筛选，则跨拓扑比较同时受到选择条件变化影响。
- [AUTHOR_FACT] 对完全图随机删边及从链增加边会生成不同具体图；论文没有报告对随机图采样重复次数、方差或置信区间。

## EIB-Learner

- [AUTHOR_FACT] EIB-Learner 对 sparse-chain view 与 dense-complete view 分别使用 GNN，节点特征包含角色和 query 表示；内积得到边 mask，再由 query gate 融合两种拓扑并采样 Bernoulli graph，以任务 reward 做 policy-gradient 优化。
- [AUTHOR_FACT] 训练目标是下游任务正确性 reward；并未使用 CAPE/TCTE 的 error/insight 干预标签直接监督边选择。
- [READER_INTERPRETATION] “error isolation / insight broadcast”主要由 sparse/dense architectural priors 与作者解释连接到 EIB；学习器并没有显式识别某条真实消息是错误还是正确 insight。
- [AUTHOR_FACT] 主实验使用 GPT-4o，3 轮通信及固定 summarizer；MMLU 6 agents、HumanEval 5 agents、数学任务 4 agents。每个实验只用 `B∈{40,60}` 个 query samples 优化拓扑。
- [OPEN_QUESTION] 论文没有足够明确地说明这 40/60 个优化样本与最终测试集合是否严格不重叠，以及超参数是否在独立 validation set 上选择。

## 主要结果与公平边界

- [AUTHOR_FACT] 主表中 EIB-Learner 六项平均 91.38，G-Designer 90.04，绝对差 1.34；没有报告多次独立训练、置信区间或显著性检验。
- [AUTHOR_FACT] 三项 ablation 平均值为：完整 EIB 91.08，移除 dense view 87.51，移除 sparse view 89.31，移除 fusion 88.37。
- [AUTHOR_FACT] 测试规模分别为 MMLU 153、GSM8K 1319、MultiArith 600、SVAMP 1000、AQuA 254、HumanEval 164。
- [AUTHOR_FACT] Token 图显示 EIB 与 G-Designer 消耗相近但并非始终更低：例如 MMLU 约 2.3e5 对 2.2e5，GSM8K 约 8.8e6 对 8.2e6。
- [READER_INTERPRETATION] 因此支持的窄结论是“在论文所测设置中，query-conditioned topology learner 相对若干拓扑基线取得小幅平均提升”；不支持“以更低成本稳定胜出”或“已隔离所有 compute/token 差异”。
- [AUTHOR_FACT] Prompt-injection robustness 实验只向一个 agent 注入干扰，EIB 报告平均下降 1.24；论文没有给出完整攻击 prompt、重复采样统计或置信区间。
- [AUTHOR_FACT] Appendix scalability 改用 GPT-3.5、MMLU 1000 题及 5/7/9 agents；EIB 相对 G-Designer 的绝对提升约为 1.39/1.32/1.81。
- [SOURCE_AMBIGUITY] 正文称 scalability 中最高可有 5.11% improvement，但附录表中相对 G-Designer 的逐列绝对差并不达到 5.11；该数字可能使用了不同参照或相对百分比，不能在 Card 中无参照复述。

## 限制与失败边界

- [AUTHOR_FACT] 作者承认角色与 prompts 手工固定，实验集中在 reasoning、math、code，尚未覆盖更开放的动态环境。
- [READER_INTERPRETATION] 因果章节建立了针对人工干预的敏感性证据，但没有证明 learned topology 的真实性能增益由 CAPE/TCTE 所描述的中介机制导致。
- [READER_INTERPRETATION] Query-conditioned graph learning的比较还混合了额外优化样本、GNN/政策梯度训练与拓扑选择能力；需要把它与静态拓扑的差异写清，不能归因成单一“稀疏优于稠密”。
- [READER_INTERPRETATION] 案例图只给出结果性叙述，没有完整 trajectory/messages 来证明某条边确实完成了所声称的错误隔离或正确信息广播。
- [READER_INTERPRETATION] 在小优化集、单次结果和无误差条的条件下，1–2 个点的优势应作为 Pilot 中的有限实证，不宜升级为稳定普适规律。

## 可抽取候选（尚非正式 Card）

- Evaluation Operator：`Paired Harmful/Helpful Propagation Stress Test`——分别在原本正确与原本错误样本上注入错误和 oracle insight，观察拓扑对两类传播的非对称影响；必须显式标注 oracle 性质。
- Operator：`Query-Conditioned Sparse/Dense Topology Fusion`——以 query 表示在 sparse 与 dense 通信先验之间逐边融合，改变本轮 agent 的可通信结构。
- Failure：`Dense Error Amplification / Sparse Insight Blocking`——高连通图放大被注入错误，过稀图又阻断被注入的正确 insight，表明单一固定连通度可能无法兼顾两者。
- Failure：`Oracle Intervention Mistaken for Natural Causal Mechanism`——由强制错误/直接正确答案得到的翻转率，被过度解释为自然消息传播或 learned topology 的真实因果中介。

## 未解决问题

- `[OPEN_QUESTION]` 500/500 分析集合是否在所有拓扑间共享同一题目与同一初始条件，还是按各拓扑分别筛选。
- `[OPEN_QUESTION]` 40/60 optimization queries 与评测题的拆分、随机种子、重复训练及 validation protocol。
- `[OPEN_QUESTION]` 5.11% scalability claim 的明确参照与计算方式。
- `[OPEN_QUESTION]` EIB edge probabilities、最终采样图和真实消息内容之间是否有可复核的逐案例 correspondence。
