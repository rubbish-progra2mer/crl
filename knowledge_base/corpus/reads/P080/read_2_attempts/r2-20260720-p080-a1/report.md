# P080 独立二读报告

## 1. 来源、阅读范围与结论

- source: `P080_autosearch.pdf`
- PDF SHA-256: `AB078EE4E0221166D92EA3856D028F92A9348899F8FA9D63EC8841764EDD8A86`
- 阅读范围：物理 PDF 第 1–21 页，逐页顺序阅读正文、公式、表格、图注、附录提示词与案例；论文印刷页码为 28059–28079。
- 论文：*AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning*，ACL 2026 Findings。
- 二读结论：**有条件准入**。准入内容是一个清楚、可复述的训练期 changed computation：用每步自生成中间答案与 gold answer 的逐步匹配，事后定位最早正确检索步，并据此塑造搜索深度奖励。不能把它扩大解释为在线时已知“最小充分深度”、无需 oracle 的逐样本最优停机，或在长搜索预算上已验证的普适规律。
- 第三读：**建议**。理由是训练 oracle 与推理时信息集存在关键差异，附录 Table 4 的 `OSR` 数值疑似实际复用了 `SD`，且论文没有方差/种子与等预算延迟核验；若后续要沉淀 Operator，这些点应由第三读专门复核。

## 2. Changed computation

### 2.1 原始 agentic RAG 计算

常规策略模型交替产生 reasoning、search query、retrieved observation，最终输出 answer。既有 RL 基线主要依赖终局正确性、逐步信息增益或外部模型/置信度来约束检索，但搜索步数常由固定上限或间接惩罚控制。（物理页 1–3）

### 2.2 AutoSearch 改变了什么

1. 在每个检索步 `t`，把问题与截至该步的完整搜索轨迹 `{q, s0, o0, ..., st, ot}` 再送给当前 policy，额外生成一个中间答案 `a_inter,t`。（物理页 4–5）
2. 训练时用 gold answer 对每个中间答案做 Exact Match，取首次 EM=1 的步为 `t_c`；从未答对则记为 `t_c=-1`。因此 `t_c` 是**基于整条 rollout 和 gold 的 hindsight 标注**，不是推理时直接观测的状态。（物理页 5）
3. 依据 `t_c` 将步划分为搜索不足、到达最早正确步前/当步的有效搜索、以及该步之后的过度搜索，并赋予分段 efficiency reward；未答对时给小的继续搜索激励，过度搜索给负奖励，较早达到 `t_c` 获得更高累计收益。（物理页 5，Figure 4）
4. 再叠加两类信号：格式/终局 EM 构成 base reward；当前中间答案 F1 相对历史最佳 F1 的增量构成 search-quality reward。（物理页 4–6）
5. 用 PPO 训练，retrieved observation token 被 mask，不进入 token-level policy loss；附加实验把累计 reward 当 outcome reward 用 GRPO，也得到相近结果。（物理页 6、8、13）

因此，真正的 changed computation 不是显式训练一个“问题复杂度预测器”，也不是部署时调用 gold 判停，而是：**训练阶段增加逐步自回答探针，用 gold 产生 hindsight stopping-depth supervision，再把它压入策略的搜索/停止行为。** 论文所称问题复杂度与模型能力是通过轨迹和当前 policy 的自回答表现被隐式体现的，并无独立估计模块。（物理页 3–5）

## 3. 输入、输出、信息可见性与时点

### 3.1 训练输入与信息

- 问题 `q_i`、每步 search query 和检索 observation、当前 policy、gold answer。
- 检索使用 2018 Wikipedia snapshot、E5 retriever，每次统一采样 top-3 文档；训练集为 NQ 与 HotpotQA 混合。（物理页 7）
- 中间答案探针在每次获得新 observation 后运行，能看到截至当前步的累计轨迹；`t_c` 的确定依赖 gold，并在 rollout 后对各步奖励进行 hindsight 归因。（物理页 4–5、14）
- terminal outcome reward 同样依赖 predicted answer 与 gold 的 EM；quality reward依赖 token-level F1 与 gold。（物理页 4–5）

### 3.2 推理输入与输出

- 推理时输入是用户问题、累计检索结果与策略自身状态；论文未描述部署时提供 gold answer，也没有在线计算 `t_c` 的 oracle。
- 输出仍是交替的 reasoning/search actions 与最终 answer；变化体现在训练后的 policy 学会用不同搜索深度结束轨迹。
- 训练中额外生成每步 intermediate answer 的计算成本没有被单独计入部署成本；论文也没有明确说明这些探针在推理时是否完全移除，但方法定义把它们用于 reward 计算，而主要推理指标只报告最终策略的搜索行为。（物理页 4–8）

### 3.3 测量输出

- Answer quality：Exact Match、word-level F1。
- Search cost：平均 Search Depth（SD）。
- Search Efficiency：`SE = EM / SD`，是比率代理，不是端到端 latency、token、FLOP 或货币成本。
- Over-Searching Ratio（OSR）：最终搜索步之前已可正确回答的样本比例；该量也依赖中间答案与 gold，不能作为无 oracle 的在线过搜检测器。（物理页 3、7）

## 4. 实验、强基线与主要结果

### 4.1 数据、模型与基线

- 六个 QA 数据集：NQ、TriviaQA、PopQA；HotpotQA、2WikiMultiHopQA、Bamboogle，覆盖 general/single-hop 与 multi-hop。（物理页 6–7）
- 主实验 backbone：Qwen2.5-3B-Base 与 Qwen2.5-7B-Base；固定深度诊断还比较 3B、7B、14B 能力差异。（物理页 3、7）
- 强基线：Search-R1、StepSearch、HiPRAG，并区分 base/instruct 版本；作者称在统一设置中独立复现基线。（物理页 6–7）
- 消融：去掉 base、efficiency、quality 三种 reward；另比较 PPO 与 GRPO。（物理页 8、13）

### 4.2 结果边界

- 3B 平均：AutoSearch EM 44.3、F1 52.4、SD 1.36、SE 35.6；表中最接近的 StepSearch-instruct 为 EM 37.0、F1 45.6、SD 1.82、SE 21.3。（物理页 6）
- 7B 平均：AutoSearch EM 48.0、F1 56.5、SD 1.27、SE 39.0；Search-R1-base 为 EM 46.8、F1 55.2、SD 2.36、SE 21.1。（物理页 6）
- 优势并非逐数据集、逐指标全胜。例如 7B HotpotQA 的 AutoSearch EM 42.7 低于 Search-R1-base 的 43.7；7B Bamboogle 的 AutoSearch EM 41.9 低于 StepSearch-base 的 42.7。应接受“平均 trade-off 改善”，不接受“所有任务精度都领先”。（物理页 6）
- Table 2 报告 AutoSearch 的 OSR 通常较低；但更低 OSR 与更短 SD、较高 EM 同时出现才有解释力，OSR 本身不区分因正确停机、未搜索或中间答案波动造成的差异。（物理页 7）
- 消融支持三类 reward 对平均 accuracy/depth 的互补作用；PPO/GRPO 结果接近。但消融只在 3B 设置报告，且没有误差条、重复运行或显著性检验。（物理页 8、13）
- 五个案例展示了较少搜索或更好证据整合，但属于选择性定性示例，不能替代总体因果分析。（物理页 14–15、17–21）

## 5. 预算、模型与 oracle 边界

- 训练共 1,005 optimization steps；actor/critic learning rate 分别为 `1e-6`/`1e-5`，warm-up ratio 为 0.285/0.015；总 batch 512、PPO mini-batch 256、actor/critic micro-batch 64/8；单节点 8×NVIDIA H20；总上下文上限 4,096 tokens。（物理页 12–13）
- 论文未报告 wall-clock、GPU-hours、能耗、每样本训练 token、每步 intermediate-answer 额外生成成本、端到端推理 token/latency 数值，也未给训练随机种子或多次运行方差。
- 主结论只在 Qwen2.5 3B/7B 训练上验证；固定深度的 14B 分析不是完整 AutoSearch 训练结果。不能外推到更大模型、其他模型族、动态网页检索或长上下文代理。
- 最关键 oracle：训练每步需要 gold answer 来计算 EM/F1、定位最早正确 `t_c` 并塑造 reward。部署时 policy 必须在没有 gold 的情况下从训练分布中内化停机行为；论文没有证明这种内化在 domain shift、答案别名、非短答案或不可精确匹配任务中仍能恢复“最小充分深度”。（物理页 4–5）
- 诊断与提示词把最大检索深度限制在 0–4；作者也在 Limitations 明确承认仅研究较低 maximum search steps。（物理页 9、14、16）

## 6. Failure、限制与可疑点

1. **训练/推理信息不对称**：最早正确步由 gold hindsight 得到；部署时没有该信号，因此“识别 minimal sufficient depth”只能理解为训练监督构造，不能理解为在线可验证判停。（物理页 4–5）
2. **EM/F1 代理脆弱**：答案别名、长生成、部分正确或语义等价会改变 `t_c`；F1 增量也可能把措辞变化当作检索质量变化。实验主要是短答案 QA，不能直接迁移到开放式研究代理。（物理页 5、7）
3. **OSR 不是因果冗余度**：它只看更早中间答案是否正确，不验证后续检索是否真的无信息价值，也不能衡量错误但有益的探索。（物理页 3、7）
4. **附录表疑似标注/复制错误**：物理页 13 的 Table 4 标为 F1 与 `OSR`，但 AutoSearch 的 `1.03/1.05/1.07/1.49/1.69/1.83` 与物理页 8 Table 3 的 SD 完全一致，且与物理页 7 Table 2 的 OSR `0.00/0.10/0.00/0.90/2.60/2.40` 不一致。该表不能直接作为 OSR 消融证据。
5. **等预算性不足**：只报告平均 search step 和比率 SE；不同方法的 reasoning token、query 长度、retrieved token、额外 judge/中间答案调用均未统一折算。Figure 6 的 search time/token 曲线缺少可复核数值与硬件说明。（物理页 7–8）
6. **统计不确定性缺失**：没有随机种子、重复训练、置信区间或显著性检验；尤其 7B 若干数据集差距很小，不能判定稳定领先。（物理页 6–8）
7. **搜索深度范围窄**：0–4 步下学到的策略可能只是短预算调度；长链 research、失败恢复、分支搜索与循环验证尚未覆盖。（物理页 9、16）
8. **复杂度/能力解释是隐式的**：论文没有独立测量 question complexity，也没有因果隔离 capability；二者由数据集、模型尺寸及自回答表现间接代理。（物理页 3–5）

## 7. 页码定位索引

- 研究问题、贡献、相关工作：物理页 1–2。
- 固定深度诊断、任务复杂度与模型尺寸效应：物理页 3。
- 三类 reward 总览、base reward、中间答案定义：物理页 4。
- `t_c`、efficiency reward、F1 quality reward：物理页 5。
- PPO/objective、主结果与数据设置：物理页 6–7。
- 消融、GRPO、训练动态、结论：物理页 8。
- 明示限制：物理页 9。
- 训练超参数、context、附加表：物理页 12–13。
- hindsight reward 图、固定深度提示词说明、案例分析：物理页 14–16。
- 完整案例：物理页 17–21。

## 8. 准入与第三读建议

- **准入：是，但限定范围。** 可准入为“训练期逐步自回答 + gold hindsight 深度奖励”的 changed-computation 证据，并保留其在短答案 QA、最多四步检索、Qwen2.5 3B/7B 与固定 Wikipedia/E5 环境内的适用边界。
- **不准入的扩大表述**：在线知道最小充分深度；不依赖 oracle；所有数据集均优于强基线；对长程 agentic research 已验证；真实总成本必然下降。
- **建议第三读：是。** 第三读应只核对三点：`t_c`/reward 的训练与推理边界；Table 4 的 OSR/SD 标注冲突；基线是否真正匹配 token、retrieval 与训练预算。若这三个问题不影响后续使用范围，才适合进一步抽取 Operator。

