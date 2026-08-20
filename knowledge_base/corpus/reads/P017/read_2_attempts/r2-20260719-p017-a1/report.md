# P017 独立二读核源报告

> 本报告是 fresh read-2 的全文核源结果，不是 Card，不评价 Candidate、novelty 或科研价值。统一问题与标签来自本 attempt 的 `invocation.md` 所冻结的 `second_read_prompt.md`。

## 0. 输入与核读范围

- [AUTHOR_FACT] Canonical metadata：`ACL:2025.emnlp-main.623`；题名 *Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems*；EMNLP 2025 Main。定位：invocation snapshot；PDF p.1 页眉与标题。
- [AUTHOR_FACT] PDF 共 15 页，印刷页码 12347–12361；SHA-256 实测为 `f94767d936354030dc25f10db92a2f6f85f49b7d7163ac45b253e047ca67bd8b`，与 invocation 一致。
- [AUTHOR_FACT] 统一二读提示 SHA-256 实测为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，与 invocation 一致；invocation 本身实测 SHA-256 为 `01f40926b6655186fc02eb36c2bd20cf4d16a0d91097afc833f4b301c6ae1abd`。
- [READER_INTERPRETATION] 核读覆盖 PDF p.1–15：正文、References、Limitation、Appendix A–D、Figure 1–5、Table 1–4、Algorithm 1、公式与页脚；文本逐页抽取，并对每页进行可视渲染核查，对关键图表另作较高分辨率的内存裁剪核查。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] 被改变的核心步骤是：在多智能体实际对话开始前，针对当前查询动态生成通信拓扑，而非使用固定 Chain/Tree/Complete/Random 图。EIB-LEARNER 先把每个 agent 的角色/提示描述与查询编码为节点特征，再用两个 GNN 分别在 Full 与 Chain 邻接上模拟传播，得到 `M_dense` 与 `M_sparse`，最后由 query-aware gate 加权融合为 `M_final` 并采样离散拓扑。定位：PDF p.6–7，§4.1–4.2，Eq. (7)–(10)；Figure 3；PDF p.15，Algorithm 1。短定位文本：`Adaptive Dual-View Fusion`。
- [AUTHOR_FACT] 离散图产生后，agent 按拓扑排序依次执行；每轮每个 agent 接收查询和邻居输出，进行 K 轮通信，最后由聚合 agent 给出输出。定位：PDF p.2–3，§2，Eq. (2)–(4)；PDF p.7，§5.1；PDF p.15，Algorithm 1。本文实验固定 `K=3`，并指定 summarizer agent 汇总对话历史。
- [AUTHOR_FACT] 图生成器以最终任务效用为 reward，用 policy gradient 优化，因为下游 LLM 推理得到的效用不可微。定位：PDF p.7，§4.2 `Model Optimization`，Eq. (11)。
- [READER_INTERPRETATION] 因而它并未改变基础 LLM 的参数或单个 agent 的内部生成规则；主要干预点是“谁在何时能看到谁的输出”，并通过查询条件化的图采样改变后续上下文传播路径。
- [OPEN_QUESTION] Eq. (9) 使用内积解码 `Z^T Z`，天然给出对称系数矩阵；但 §2 把目标定义为 DAG，Algorithm 1 又直接从 `M_final` 采样后做拓扑排序。正文未说明如何把对称 mask 定向、如何屏蔽环或保证采样图无环。定位：PDF p.2–3，§2；p.6–7，Eq. (9)–(10)；p.15，Algorithm 1。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 拓扑学习器输入包括查询 `Q`、预定义 agent roles 及其 prompt 文本描述；NodeEncoder 为 `all-MiniLM-L6-v2`，维度 384。定位：PDF p.6，Eq. (7)；p.7，§5.1。
- [AUTHOR_FACT] 学习器输出为 query-specific 通信图 `G`；实际 MAS 输出为 summarizer agent 聚合 K=3 轮历史得到的最终答案。定位：PDF p.3，Eq. (3)–(4)；p.7，§4.2 与 §5.1。
- [AUTHOR_FACT] 图学习阶段可用信息只明确写到角色/角色提示描述和当前 query embedding；未声称提前知道 agent 对当前题的真实正确率。定位：PDF p.5–6，§4.1，尤其“without prior knowledge of agent reliability”附近。
- [AUTHOR_FACT] CAPE/TCTE 分析不是 EIB 推理流程本身，而是独立的反事实分析：对固定拓扑，强制单个 agent 产生操纵后的输出，再看最终正确性是否翻转。错误传播实验从原本答对的 500 题出发，注入错误；洞见传播实验从原本答错的 500 题出发，注入正确答案。定位：PDF p.3–5，§3.1、§3.2.1–3.2.2，Eq. (5)–(6)，Figure 2。
- [READER_INTERPRETATION] CAPE 干预发生在 agent 输出形成处、最终聚合之前；EIB 的拓扑干预发生在多轮对话开始前。二者不能混为同一训练信号：正文把 CAPE/TCTE 用于机制分析，而 EIB 训练使用最终任务 reward。
- [OPEN_QUESTION] §3.1 的形式定义写成直接 `do(O_i := Ō_i)`，但实验操作写成“修改 system prompt 以产生错误/正确输出”。若实际是 prompt 注入而不是硬替换输出，则内容长度、解释风格和指令效应可能与答案正确性一起变化，干预并非只改变一个变量。定位：PDF p.3，Definition 3.1；p.4–5，§3.2.1–3.2.2。
- [OPEN_QUESTION] §2 对边方向的文字定义存在方向不一致：p.2 说 `(v_i,v_j)` 表示 `v_i` 接收 `v_j`，p.3 的邻居集却写为 `{v_j | (v_j,v_i) in E}`。这会影响复现时邻接矩阵和消息方向。定位：PDF p.2，`Communication Topology`；p.3，Eq. (2)。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] Table 1 的六数据集平均最强外部基线是 G-designer：90.04%；EIB-LEARNER 为 91.38%，作者报告平均提升 1.34 个百分点。定位：PDF p.7–8，§5.2，Table 1。
- [AUTHOR_FACT] 固定拓扑/非自动设计基线中，Table 1 最强平均值是 LLM-Debate 87.53%，Random 为 85.33%，Chain 为 84.53%，Complete 为 82.16%。定位：PDF p.8，Table 1。
- [READER_INTERPRETATION] 与“组合机制”最接近的内部对照是 `w/o Fusion`：它仍保留 dense/sparse 两个分支，但用直接相加替代 query-aware fusion。三数据集平均为 88.37%，完整模型为 91.08%，差 2.71 个百分点。定位：PDF p.8，§5.3，Table 2。
- [AUTHOR_FACT] 另外两个结构消融为 `w/o Dense`（平均 87.51）和 `w/o Sparse`（平均 89.31）；去掉 dense 分支降幅最大，GSM8K 从 95.20 降至 91.10。定位：PDF p.8，Table 2。
- [OPEN_QUESTION] Table 2 只有 MMLU、GSM8K、HumanEval，不能直接确认相同的组合收益是否覆盖 AQuA、MultiArith、SVAMP。定位：PDF p.8，§5.3，Table 2。

## 4. 模型、token、tool-call、prompt、oracle 差异能否解释结果？

- [AUTHOR_FACT] 主实验声明统一使用 GPT-4o、OpenAI API、K=3 和 summarizer agent；而 §3 的传播机制分析明确使用 6 个 GPT-3.5 实例，Appendix B 的扩展性表也使用 GPT-3.5。定位：PDF p.4，§3.2 `Experimental Settings`；p.7，§5.1；p.13，Table 3 caption。
- [READER_INTERPRETATION] Table 1 内部比较若确实遵循“throughout all experiments”的统一 GPT-4o 设置，模型差异不太可能单独解释同表结果；但 §3 的 GPT-3.5 因果现象与 §5 的 GPT-4o 性能证据属于不同模型条件，不能自动视为同一机制在同一模型上的闭环验证。
- [AUTHOR_FACT] Figure 4 标注的 token 总量显示 EIB 并非最低：MMLU 上 EIB 约 `2.3e5`、G-designer `2.2e5`；GSM8K 上 EIB `8.8e6`、G-designer `8.2e6`。EIB 的准确率更高，作者据此称成本“comparable”。定位：PDF p.8–9，§5.4，Figure 4a–b。
- [READER_INTERPRETATION] 相比 Complete Graph 和 LLM-Debate，EIB 的通信 token 明显更低；但相对最强基线 G-designer，它用的是略多而非更少的 token，因此性能增益不能描述成在严格相同 token 预算下得到。
- [OPEN_QUESTION] 正文未明确 Figure 4 的 token 计数是否包含拓扑学习器训练、NodeEncoder/GNN 推理、重试或只统计 LLM 通信；纵轴指数在可视图中也未完整写清，精确值主要依赖点旁注释。定位：PDF p.8–9，§5.4，Figure 4。
- [AUTHOR_FACT] 洞见传播实验向 agent 注入正确答案，属于 oracle intervention；它用来测量传播能力，不是实际部署时可用的信息。定位：PDF p.4–5，§3.2.2。
- [OPEN_QUESTION] 作者没有逐基线给出完整角色提示、summarizer 提示、采样温度、最大 token、停止条件和随机种子，也未报告统计方差/置信区间。故仍不能排除 prompt、采样和预算细节对小幅差异（尤其 1.34 个百分点）有贡献。定位：PDF p.7，§5.1；p.8，Table 1。
- [OPEN_QUESTION] 文中没有报告 tool-call 型 agent 流程；HumanEval 的 Pass@1 必然涉及代码判定，但正文未交代执行器调用是否计入通信成本或是否对所有方法完全一致。定位：PDF p.7，§5.1；p.14，Table 4。
- [OPEN_QUESTION] §3.2 写“for each topology”构造各自的 500 个原答对和 500 个原答错题集。若不同拓扑使用的是不同题目子集，Figure 2 的跨稀疏度 TCTE/accuracy 曲线会混入样本构成差异；正文未说明是否固定同一题集。定位：PDF p.4，§3.2 `Experimental Settings`。

## 5. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 明示限制一：评估只覆盖 general reasoning、math reasoning、code generation；作者建议未来扩展到真实世界决策和开放域对话。定位：PDF p.9，`Limitation`。
- [AUTHOR_FACT] 明示限制二：固定的预定义 agent roles 和人工 prompts 可能限制对陌生或演化场景的适应性。定位：PDF p.9，`Limitation`。
- [AUTHOR_FACT] 传播分析只在 MMLU、6 个 GPT-3.5 agents 上完成；主实验 agent 数为 MMLU 6、HumanEval 5、数学任务 4；扩展性附录只测试 5、7、9 agents。定位：PDF p.4，§3.2；p.7，§5.1；p.13，Appendix B、Table 3。
- [AUTHOR_FACT] 负向结果：Chain 抑制错误传播但也抑制正确洞见；Full 墠强洞见传播但更易传播错误。作者报告 Chain 相对 Full 的错误 TCTE 最多降低 19%，Full 的洞见 TCTE 相对 Chain 增加 10.5%。定位：PDF p.4–5，§3.2.1–3.2.2，Figure 2a–b。
- [AUTHOR_FACT] 负向结果：AgentDrop/AgentPrune 在 Figure 2c 中没有优于中等稀疏度 Random graph。定位：PDF p.5，§3.2.4，Figure 2c。
- [AUTHOR_FACT] 负向结果：Table 1 中 SC(CoT) 在 GSM8K 比 Vanilla 低 0.70；Complete 在 GSM8K 低 2.20、在 SVAMP 低 2.54。定位：PDF p.8，Table 1。
- [AUTHOR_FACT] 鲁棒性只测试向单个 agent 注入 adversarial system prompt；简单 Chain/Tree 最多下降 11.8%，EIB 下降 1.24%。定位：PDF p.8–9，§5.5，Figure 4c。
- [OPEN_QUESTION] 未测试边界包括：多 agent 同时受攻击、非 prompt 类攻击、动态加入/退出 agents、循环通信图、K 非 3、其他基础模型、开放式长文本质量指标、真实工具环境与跨分布角色集合。正文没有提供这些条件下的结论。

## 6. 可抽取为 Operator 的内容与真实 Failure

以下仅按统一问题做可抽取性核源，不生成 Card。

### Operator 候选

- [AUTHOR_FACT] `CAPE`：固定图上对单 agent 输出做反事实替换，记录最终答案正确性是否翻转。定位：PDF p.3，Definition 3.1，Eq. (5)。
- [AUTHOR_FACT] `TCTE`：对各 agent 的 CAPE 按 `1/sqrt(degree)` 加权平均，衡量拓扑对局部干预的总体敏感性。定位：PDF p.3–4，Definition 3.2，Eq. (6)。
- [AUTHOR_FACT] 稀疏度扫描：从 Full 随机删边到 Chain 测错误传播；从 Chain 加边到 Full 测洞见传播。定位：PDF p.4–5，§3.2.1–3.2.2。
- [AUTHOR_FACT] 双视图传播模拟：以 Chain 作为 sparse view、Full 作为 dense view，分别运行 GNN。定位：PDF p.6，§4.1，Figure 3。
- [AUTHOR_FACT] 查询感知融合：MLP+softmax 从 query embedding 产生 dense/sparse 权重，融合两个 connectivity masks。定位：PDF p.7，Eq. (10)。
- [AUTHOR_FACT] Bernoulli edge sampling + policy-gradient task reward：从融合 mask 采样图，再由不可微的最终任务效用更新图学习器。定位：PDF p.7，Eq. (11)；p.15，Algorithm 1。

### 可记录 Failure

- [AUTHOR_FACT] Dense topology 的局部错误易扩散并翻转最终答案。定位：PDF p.4，Finding 1，Figure 2a。
- [AUTHOR_FACT] Sparse topology 会阻断有益洞见进入最终决策。定位：PDF p.5，Finding 2，Figure 2b。
- [AUTHOR_FACT] 只追求稀疏的 learned topology 在该分析中未必优于中等稀疏随机图。定位：PDF p.5，§3.2.4，Figure 2c。
- [AUTHOR_FACT] 去掉任一 dense/sparse/fusion 模块均使三任务平均准确率下降，其中去 dense 降幅最大。定位：PDF p.8，§5.3，Table 2。
- [AUTHOR_FACT] 简单固定拓扑在单 agent prompt injection 下出现明显性能下降。定位：PDF p.8–9，§5.5，Figure 4c。
- [READER_INTERPRETATION] 上述 Failure 都是在特定模型、任务、agent 数和攻击设置中观测到的，不能扩写成对所有 MAS 的普遍定律。

## 7. 关键结论的页码、章节、图表与定位索引

|判断|标签|定位|
|---|---|---|
|稠密图增强错误传播|[AUTHOR_FACT]|PDF p.4，§3.2.1，Figure 2a，`Finding 1`|
|稠密图增强正确洞见传播|[AUTHOR_FACT]|PDF p.5，§3.2.2，Figure 2b，`Finding 2`|
|中等稀疏度对应更高任务准确率|[AUTHOR_FACT]|PDF p.5，§3.2.3，Figure 2a–b，`Insight`|
|双 GNN 分别使用 Full/Chain 视图|[AUTHOR_FACT]|PDF p.6，§4.1，Figure 3，Eq. (8)–(9)|
|query-aware gate 融合两张 mask|[AUTHOR_FACT]|PDF p.7，§4.2，Eq. (10)|
|EIB 平均 91.38，G-designer 90.04|[AUTHOR_FACT]|PDF p.8，Table 1|
|去 dense/sparse/fusion 都退化|[AUTHOR_FACT]|PDF p.8，§5.3，Table 2|
|EIB token 略高于 G-designer、准确率更高|[AUTHOR_FACT]|PDF p.8–9，§5.4，Figure 4a–b|
|单 agent prompt attack 下 EIB 下降 1.24%|[AUTHOR_FACT]|PDF p.8–9，§5.5，Figure 4c|
|5/7/9 agents 的扩展性结果|[AUTHOR_FACT]|PDF p.13，Appendix B，Table 3|
|数据集测试规模与指标|[AUTHOR_FACT]|PDF p.14，Appendix C，Table 4|
|完整图生成与执行伪代码|[AUTHOR_FACT]|PDF p.15，Algorithm 1|

## 8. 解析文本与可视 PDF 是否冲突？

- [READER_INTERPRETATION] 对 PDF p.1–15 的抽取文本与逐页可视渲染核对后，正文段落、Figure 1–4、Table 1–4 和 Algorithm 1 的主要标签/数值没有发现由解析顺序造成的实质冲突。双栏页面的抽取顺序偶有图中文字先于正文、公式空格丢失，但可视核查可恢复结构。
- [AUTHOR_FACT] 原文本身存在 Figure 5 的 case 对应冲突：Appendix D（PDF p.13）称 HumanEval 为 case A、GSM8K 为 case B；可视 Figure 5（PDF p.14）却明确标注 `GSM8K (case A)` 与 `Humaneval (case B)`。这不是解析器造成的冲突。作者意图无法由原文确定。
- [OPEN_QUESTION] Figure 5 的正确 case 映射需作者或代码/补充材料确认；本报告不自行修正。
- [AUTHOR_FACT] Algorithm 1 可视文本末尾的注释写为 `Update G-Designer parameters`，而算法标题、损失和上下文均为 EIB-LEARNER。定位：PDF p.15，Algorithm 1。
- [READER_INTERPRETATION] 该注释像是文字沿用错误，但原文未说明；不应把它静默改写为 EIB 参数更新证据。
- [OPEN_QUESTION] Algorithm 1 同时用 `alpha` 表示学习率和 dense/sparse gate 权重，且未交代 DAG 约束步骤；这两点降低伪代码可复现性。定位：PDF p.7，Eq. (10)–(11)；p.15，Algorithm 1。

## 9. Provenance 与可观察 trace

- Invocation snapshot：`D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P017/read_2_attempts/r2-20260719-p017-a1/invocation.md`；Attempt ID `r2-20260719-p017-a1`。
- 实际模型/版本：Codex；系统上下文仅说明其基于 GPT-5，更细的可核验模型版本 `unknown`。
- 任务标识：`/root/p017_second_read`；独立可见 thread ID：`unavailable`。
- 文件级 path allowlist：`unavailable`。本次按 invocation 执行 `procedural_blinding`；这不是技术隔离，也不声称存在系统强制的 read-only 沙箱。
- 实际研究输入文件：
  1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P017_information_propagation_topologies.pdf`
  2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
  3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P017/read_2_attempts/r2-20260719-p017-a1/invocation.md`
- 运行规范文件访问（非研究证据输入）：`C:/Users/g/.codex/skills/pdf/SKILL.md`。这是平台要求的 PDF 处理技能说明；其内容未用于论文事实判断。
- 可观察工具 trace：通过 `functions.exec` 调用本地 `shell_command`；使用 PowerShell `Get-Content`/`.NET UTF-8 ReadAllText` 读取两份 markdown，`Get-FileHash` 校验 PDF、prompt 和 invocation；使用 Python `pypdf` 读取页数、metadata、逐页文本与图像对象计数；使用 Python `PyMuPDF (fitz)` + `Pillow` 在内存中渲染 15 页及关键图表裁剪，并以 base64 直接返回视觉检查，未写临时图像；曾读取可用工具元数据以寻找不落盘的 PDF 可视方案。工具精确内部版本：`unavailable`。
- 网络：未调用联网工具，未发起论文检索或外部页面访问。
- 工作区边界：未枚举工作区；未读取 read_1、Cards、其他读者报告、blind query 或其他项目文件。
- 写入：仅本文件 `report.md`。

