# P023 fresh 独立第三读核源报告

## 0. Provenance 与边界

- Invocation snapshot：`knowledge_base/corpus/reads/P023/read_3_attempts/r3-20260719-p023-a1/invocation.md`，Attempt ID `r3-20260719-p023-a1`。
- 原文：`knowledge_base/staging/papers/P023_masrouter.pdf`；实测 SHA-256 `1bf45eaa68515ae2a6d3de2e2240ac321fef37a46ba831718aacee52bb12f457`，与 invocation 一致。
- 统一提示：`knowledge_base/templates/second_read_prompt.md`；实测 SHA-256 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，与 invocation 一致。
- Canonical metadata：MasRouter: Learning to Route LLMs for Multi-Agent Systems；ACL 2025 Long；DOI `10.18653/v1/2025.acl-long.757`。
- 实际模型/版本：`unknown`（运行界面未提供可核验版本）；canonical task/thread：`/root/plan05_third_reader_conflicts`。
- 阅读方法：对 24 个物理页逐页读取原始 PDF 的文本对象；对争议相关页的原始版面进行内存渲染复核，未创建临时文件。
- 边界声明：未读取 `read_1`、任何 `read_2`、reconciliation、Cards、CORPUS_REPORT、其他报告/读稿或 blind query；未枚举工作区；未联网；未作 Candidate 评价。

## 1. 方法改变的计算步骤

- [AUTHOR_FACT] MasRouter 把单一 LLM 路由扩展为一个级联的多智能体系统路由：先选择协作模式，再决定 agent 数量与角色，最后为每个 agent 选择 LLM。Locator：物理页 2，Introduction，MASR 定义段；物理页 4，Section 4 与 Figure 2；短摘录位置：“collaboration mode determination, role allocation, and LLM routing”。
- [AUTHOR_FACT] 搜索空间写为 `S=(M,R,T)`；一个 MAS 实例包含所选 LLM、角色和协作模式，agent 数量为 `k`。Locator：物理页 3，Section 3.1，Definition 1、Equation (1)。
- [AUTHOR_FACT] 控制器分解为 `Fθ = Fθm ◦ Fθr ◦ Fθt`：`Fθt` 选协作模式，`Fθr` 级联生成角色，`Fθm` 以多项分布进行 LLM 分配。Locator：物理页 4，Equation (5)；物理页 4–5，Sections 4.1–4.3，Equations (6)–(11)。
- [AUTHOR_FACT] agent 数量由查询隐变量计算为 `k=ceil(δ(H)·γ)`；为保持可微，训练时以取整前值并用 Gamma 函数近似多项式系数。Locator：物理页 5，Sections 4.1、4.3，Equation (12)。
- [READER_INTERPRETATION] 核心 changed computation 不是“给固定 agent 换一个模型”，而是对协作拓扑、角色序列、agent 数量和每个 agent 的模型进行联合、分阶段的条件选择。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 推理时输入是查询 `Q`，以及预定义的 LLM 池 `M`、角色池 `R`、协作模式池 `T`；输出是针对该查询构造的 MAS `S`。Locator：物理页 3，Definition 2、Equation (2)；物理页 4，Section 4 开头。
- [AUTHOR_FACT] 协作模式模块使用查询的文本编码和候选协作模式表示；角色模块使用查询、已选协作模式及先前角色；LLM 路由模块使用查询、协作模式和已选角色。Locator：物理页 4–5，Equations (6)–(11)。
- [AUTHOR_FACT] 候选 LLM 池为 gpt-4o-mini、Claude-3.5-Haiku、Gemini-1.5-Flash、Llama-3.1-70B；DeepSeek-V3 用于 inductive 能力实验。协作模式池包括 CoT、Reflexion、self-consistency、LLM debate、Macnet Chain/Complete Graph；角色池含 26 个角色，并包含编译器或 Wikipedia 访问能力。Locator：物理页 6，Section 5.1 “LLM Backbones”“Implementation Details”；物理页 21–24，Appendix E profiles。
- [AUTHOR_FACT] 训练循环对每个 `Q∈D` 重复 `K` 次采样构造 MAS、执行并计算 `R=U(S;Q,a)-λC(S;Q)`，再以 policy gradient 更新参数。Locator：物理页 15，Appendix B，Algorithm 1；物理页 4、6，Equations (3)、(13)。
- [READER_INTERPRETATION] 干预发生在回答生成前的系统组装阶段；训练反馈发生在所采样 MAS 执行并得到性能/成本后。

## 3. 基线与比较口径

- [AUTHOR_FACT] Table 1 比较了 vanilla 单模型、CoT/ComplexCoT/self-consistency、固定多智能体拓扑、动态 MAS、单 LLM router，共 20 个基线；MasRouter 的五数据集平均值为 85.93。Locator：物理页 6–7，Section 5.1 与 Table 1。
- [AUTHOR_FACT] Table 1 中 AFlow 的最高列平均值为 84.20；作者正文把 RouterDC 称为 SOTA LLM routing method，并报告 MasRouter 平均高 3.51%。Locator：物理页 6–7，Section 5.2 与 Table 1。
- [READER_INTERPRETATION] 若按“动态构造多智能体工作流”接近程度，AFlow/AgentPrune 更接近；若按“从模型池路由”接近程度，RouterDC 更接近。论文未提供一个同时匹配协作模式、角色与 LLM 三路选择的组合基线。
- [OPEN_QUESTION] “最接近组合基线”无法由原文唯一确定；表中不存在把同一模式池、角色池和 LLM 池交给另一种联合路由器的严格对照。

## 4. 训练/验证/测试 query、划分与 oracle reward：争议专项核查

### 4.1 Query 来源与数量

- [AUTHOR_FACT] 实验使用 MMLU、GSM8K、MATH、HumanEval、MBPP；MATH 仅说明从不同难度层次分层抽样 519 个问题。Locator：物理页 6，Section 5.1 “Dataset and Benchmarks”。
- [AUTHOR_FACT] Algorithm 1 的输入是 benchmark `D`，并直接写 `for query Q∈D`。Locator：物理页 15，Appendix B，Algorithm 1 lines 1–2。
- [OPEN_QUESTION] 原文未说明五个 benchmark 分别采用官方 train、validation、test 中的哪一部分，也未给出除 MATH 519 外的训练/验证/测试 query 数量。
- [OPEN_QUESTION] 原文未给出训练、验证、测试的划分比例、划分规则、固定 query ID 或防止交叉污染的说明；全文检索也没有 `split` 命中。
- [OPEN_QUESTION] Table 1 的报告集是否与用于 policy-gradient 优化的 `D` 完全隔离，原文无法判定。

### 4.2 Oracle answer 与 reward 使用范围

- [AUTHOR_FACT] 优化目标首先把 benchmark `D` 定义为查询 `Q` 与对应 oracle answer `a` 的集合；utility `U(S;Q,a)` 衡量 MAS 性能，cost `C(S;Q)` 衡量调用/API/token 成本。Locator：物理页 4，Section 3.2 “Optimization Objective”，Equation (3)。
- [AUTHOR_FACT] Equation (4) 以得到答案 `a` 的条件似然表示回答质量；Section 4.4 说优化目标最大化正确解概率并最小化 token expenditure。Locator：物理页 4，Equation (4)；物理页 6，Section 4.4，Equation (13)。
- [AUTHOR_FACT] Algorithm 1 明确计算 `R=U(S;Q,a)-λC(S;Q)` 并据此更新 `θ`。Locator：物理页 15，Algorithm 1 最后两步。
- [READER_INTERPRETATION] 原文明确支持“训练奖励依赖 oracle answer `a`/正确性反馈”，但没有把 `U` 的数据集特定判分函数、验证时选择规则和最终测试时是否禁用 oracle 分别写清。
- [OPEN_QUESTION] oracle reward 的使用范围是否只限训练 query、是否参与超参数选择/验证、是否在报告集上继续更新，原文没有可定位说明；不得据此断言存在或不存在测试泄漏。

### 4.3 随机种子与重复实验

- [AUTHOR_FACT] 方法含随机潜变量采样和多项采样；实验把温度设为 1。Locator：物理页 5，Equations (7)、(10)；物理页 6，Section 5.1；物理页 15，Algorithm 1。
- [AUTHOR_FACT] 消融中的 `w/o Fθt/Fθr/Fθm` 用随机选择替换对应模块。Locator：物理页 8，Section 5.5 与 Table 3。
- [OPEN_QUESTION] 原文没有报告随机种子、独立重复次数、均值/标准差、置信区间或显著性检验；全文对 `seed`、`repeat` 均无命中。
- [OPEN_QUESTION] Table 1–3 与 Figure 3–5 的单点结果是否来自单次运行、最佳运行或多次平均，原文无法判定。

## 5. 可能的模型、token、tool-call、prompt 与 oracle 差异

- [AUTHOR_FACT] Table 1 的固定/动态 MAS 多以单一 gpt-4o-mini 或 Gemini-1.5-Flash运行，而 MasRouter 和单 LLM routers 使用 LLM Pool。Locator：物理页 7，Table 1 与 caption。
- [READER_INTERPRETATION] 因此 MasRouter 的结果同时包含“路由策略”和“可选择不同模型”的作用；Table 1 不是所有方法在同一个固定 backbone 下的纯路由器比较。
- [AUTHOR_FACT] 角色池包含编译器与 Wikipedia 访问角色，Appendix E 还给出不同角色的 MessageAggregation、PostProcess 和 prompt profile。Locator：物理页 6，Section 5.1；物理页 21–24，Appendix E。
- [OPEN_QUESTION] 原文没有逐基线说明是否共享完全相同的角色提示、工具权限、tool-call 次数上限、终止条件与后处理，因此工具/prompt 差异无法排除。
- [AUTHOR_FACT] 成本项可包含 LLM calls、API cost、token cost；λ 控制性能—成本权衡。Locator：物理页 4，Equation (3) 后解释。
- [OPEN_QUESTION] Table 1 的准确率比较是否在相同 token 预算或相同调用预算下完成，原文没有统一预算约束；成本另在 Figure 3、Tables 10–12 报告。
- [OPEN_QUESTION] oracle 差异的主要未决点见 Section 4.2：训练/验证/测试各阶段的可见性未分开陈述。

## 6. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者假设 LLM pool 中每个模型均可靠；被攻击或投毒的模型可能误导其他 agent，鲁棒识别属于未来工作。Locator：物理页 9，Limitations。
- [AUTHOR_FACT] 作者称用 MasRouter 收集的数据微调大模型 router 可进一步提升性能，但因时间限制没有详细讨论。Locator：物理页 9，Limitations。
- [AUTHOR_FACT] 去掉 LLM router 带来最大性能下降；去掉成本项对性能影响不大，但在 GSM8K/MATH 上成本分别上升 54.09%/41.62%。Locator：物理页 8，Section 5.5，Table 3。
- [AUTHOR_FACT] `γ` 从 6 增至 10 只带来边际性能增益，却使单 query 成本约为 1.5 倍；较大 `λ` 降低 17.78% 成本但约损失 1.3% 性能。Locator：物理页 8，Sensitivity Analysis，Figure 5。
- [OPEN_QUESTION] 未测试边界还包括未披露划分条件下的跨 query 泛化、被投毒模型鲁棒性、严格等预算比较，以及随机性稳定性。

## 7. 可供后续抽取的机制与真实失败事实（非正式 Card）

- [READER_INTERPRETATION] 可抽取机制：查询条件化的级联控制器依次选择协作模式、角色与 LLM；动态 agent 数量；以性能减成本的策略梯度联合优化。依据：物理页 4–6，Sections 4.1–4.4；物理页 15，Algorithm 1。
- [AUTHOR_FACT] 可记录负向事实：移除 LLM 路由导致最大消融性能下降；移除成本项显著增加成本；agent 上限超过 6 后收益趋于边际；较强成本惩罚有性能代价。依据：物理页 8，Table 3、Figure 5。
- [READER_INTERPRETATION] 训练/测试边界、oracle 范围和随机复现信息缺失应记录为证据缺口，不应改写成已观察到的性能失败或泄漏结论。

## 8. PDF 版面与解析核验

- [AUTHOR_FACT] 物理页 4 的 Equation (3)、物理页 6 的实验设置、物理页 15 的 Algorithm 1 经过原始页面内存渲染复核；关键数字与公式同逐页文本对象一致。
- [READER_INTERPRETATION] 双栏和 Figure 2 导致物理页 4 的线性文本顺序交错，但未改变本报告采用的公式、数据集或算法结论；所有 locator 以物理页为准，并同时给出 PDF 中的印刷页码（15549–15572）可回查。
- [OPEN_QUESTION] 未对 24 页逐页做独立 OCR 或像素级字符比对，因此不能宣称不存在任何细小排版/字形解析差异；争议相关页未见会改变结论的视觉冲突。

## 9. 独立第三读结论

- [READER_INTERPRETATION] 原文清楚支持 MasRouter 的级联联合路由机制和 oracle-dependent 训练奖励，但不支持确定训练/验证/测试 query 的来源与隔离方式。
- [READER_INTERPRETATION] 原文也不支持任何关于随机种子、多次重复或统计稳定性的明确说法。
- [OPEN_QUESTION] 最关键的未决事实是：用于 policy-gradient 更新的 `D` 与最终报告集之间如何划分，以及 oracle reward 在训练、验证和测试各阶段的精确使用范围。

## 10. 可观察访问、网络与工具声明

- 文件访问：科研内容仅来自本报告第 0 节列出的 PDF、统一提示与本 attempt invocation；另按系统要求读取项目 `AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md` 和本地 `pdf` 技能说明等非科研操作规约，并回读本报告做编码/内容校验。未读取任何被禁止的科研资产。
- 网络：未使用；未发起任何 web/search/download 请求。
- 工具：使用 PowerShell 精确路径读取与 SHA-256 校验；使用项目 `.venv` 中 PyMuPDF 1.28.0 对原 PDF 逐页抽取文本、定位关键词并在内存中渲染关键页面；使用 `apply_patch` 仅写入本 `report.md`。
- 隔离性质：`procedural_blinding`，不是技术文件级 allowlist。
