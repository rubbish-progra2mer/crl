# P080 独立定向第三读报告

## 读取边界与来源

- 论文：*AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning*。
- 原始文件：`knowledge_base/staging/plan05_sat_a3/P080_autosearch.pdf`。
- SHA-256：`ab078ee4e0221166d92ea3856d028f92a9348899f8fa9d63ec8841764edd8a86`。
- 已逐页读取 PDF 物理页 1–21，包括正文、公式、表格、限制、训练细节、固定深度提示词和五个案例。
- 本报告是 fresh third reader 在 procedural blinding 下的独立判断；未联网，未读取任何既有读审、调和、Cards、Evidence、审计、Candidate、calibration 或 blind 材料。

## 结论先行

AutoSearch 确实实现了一个可辨认的 changed computation：训练时在每次检索后生成中间答案，用 gold answer 的 Exact Match 找到该轨迹中“首次答对”的深度，再以该 hindsight 深度奖励此前检索、惩罚其后检索；同时用 gold token-F1 的逐步增益奖励搜索质量。但这不是 oracle-free 的自我判断。论文所谓 minimal sufficient depth 在训练期明确依赖 gold EM/F1 oracle，部署时只是由经此监督训练的策略隐式内化停止行为。

因此，本篇可有限准入为：

1. “gold-supervised hindsight search-depth shaping” 的窄 Operator 证据；
2. oracle 依赖、parametric-memory/污染未排除、训练成本未计入净节省、最大深度过低和比较公平性不足的 Failure/边界证据。

不得将其准入为“无需 gold 的自适应充分性判定”“已证明端到端净成本下降”或“已验证长程 agentic search”的证据。

## 机制核对

### 1. minimal sufficient depth 直接依赖 gold Exact Match

- PDF 物理页 4–5：每个检索步由当前策略根据累积轨迹生成 intermediate answer；随后定义
  `t_c = min {t | EM(a_inter,t, a_gold) = 1}`。若整条轨迹都未答对，则设 `t_c = -1`。
- PDF 物理页 5：search efficiency reward 以该 `t_c` 把步骤分为有效搜索、过度搜索和未答对轨迹，并给出不同奖励。换言之，“最早充分”不是由模型置信度、证据覆盖或停止判别器直接识别，而是由 gold answer 的事后正确性判定提供。
- PDF 物理页 4：base outcome reward 的最终答案正确性同样用 `EM(a_pred, a_gold)`。
- PDF 物理页 5：search quality reward 是当前中间答案相对历史最佳的 gold token-F1 增益，即仍直接访问 `a_gold`。

论文把 intermediate answer 称为 self-evaluation signal，但“答案由自己生成”不等于“正确性由自己评价”。正确性、首次答对深度和质量增益都由外部 gold oracle 决定。更准确的机制表述应是：训练期 gold-supervised hindsight credit assignment，推理期执行由此训练出的搜索策略。

### 2. 未答对轨迹的形式化表述存在不一致

- PDF 物理页 5 先设未答对时 `t_c=-1`，随后文字又以 `t_c>T` 描述 under-search；这与前述取值不一致。
- 同页公式及图 4 对 `t_c<0` 的轨迹给予每步小正奖励，因此其实际意图似乎是让未答对轨迹在固定上限内继续搜索。

该不一致不否定整体 operator，但会影响严格复现；需要以实现代码核对具体分支，本文 PDF 本身不足以消除歧义。

### 3. 该机制只在很低的深度范围内成立

- PDF 物理页 3：机制动机实验把搜索深度固定为 0、1、2、3、4。
- PDF 物理页 14、16：附录明确说明并给出 exactly 0–4 searches 的五套提示词。
- PDF 物理页 9：作者在 Limitations 中明确承认研究聚焦于“relatively low maximum search steps”，更宽深度范围尚待研究。

因此“minimal sufficient”只是 0–4 次检索上限内、相对于该模型和 benchmark 的截断最早答对点。对于在第 4 步后才可解决的问题，实验不能区分“真正不充分”与“搜索上限太低”，也不能支撑 long-horizon agentic search 的一般结论。

## parametric memory 与 contamination 替代解释

论文没有给出 benchmark contamination audit、去记忆化测试、答案扰动、时间切分、实体替换或仅依据检索证据的可支持性核查。以下案例进一步说明 retrieval causality 未被建立：

- PDF 物理页 18，Case 2：AutoSearch 的检索结果列出 Danielle Savre、Katie Wright、Katie Holmes，并未提供 Katie Sagona 是 child actor 的证据；模型仍输出 gold “child actor”。此外，问题文本本身已包含“was a child acting ...”这一强答案提示。
- PDF 物理页 19，Case 3：展示的检索结果只明确支持 Sharqliyya 在叙利亚，未展示 Umm Al-Tuyour 与 Hama Governorate 的证据；模型却断言三者都在叙利亚。
- PDF 物理页 20，Case 4：展示结果未给出 California State Polytechnic University, Pomona 为公立大学的证据，模型仍回答两校都是 public universities。
- PDF 物理页 17–20 的 AutoSearch 轨迹反复声称“I don’t have any pre-existing knowledge”，这只是模板化生成文本，不能作为排除参数记忆的证据。

这些现象与“更好的检索带来答案”相容，但同样与参数记忆、问题泄漏式提示、benchmark 熟悉度或无证据猜测相容。由于训练集混合 NQ 与 HotpotQA，且主表同时在 NQ/HotpotQA 上评估（PDF 物理页 7），至少部分结果还是 in-domain；论文虽也报告其他数据集，却未排除这些替代解释。故不能把低 `t_c` 自动解释为“所需外部证据已在该深度获得”。

## 预算、训练成本与推理节省

### 已报告事实

- PDF 物理页 6：采用 PPO，包含 actor/value 网络，并在训练损失中 mask 外部 observation token。
- PDF 物理页 13：训练共 1,005 个 optimization steps，单节点 8×NVIDIA H20，总 batch size 512，PPO minibatch 256，actor/critic micro-batch 分别为 64/8；总上下文上限 4,096 tokens。
- PDF 物理页 4–5：训练 rollout 的每个检索步都额外生成中间答案，并计算多路奖励。
- PDF 物理页 6–8：推理效率主要以 Search Depth、`SE=EM/SD`、训练曲线中的 search time 与 token length 描述；主表平均搜索深度约 1–3.5。

### 未报告或未纳入

- 没有总 GPU-hours、训练 wall-clock、训练 token 数、检索调用总量、功耗、硬件成本或相对 baseline 的完整训练成本。
- 没有给出节省一次推理所对应的真实货币/延迟/能耗，也没有训练成本的 amortization break-even query count。
- `SE=EM/SD` 只把搜索次数作为成本代理，未覆盖生成 token、检索结果长度、PPO actor/critic 开销及训练期逐步 intermediate-answer 生成。
- Figure 6 给出趋势图，但没有足够的数值化端到端成本账本。

因此可接受的结论是“在作者设定中，平均检索步数较少且 EM/F1 较高”；不可接受的结论是“计入训练与全链路资源后，总成本已被证明更低”。

## 强基线与公平性核对

- PDF 物理页 6–7：主表比较 Search-R1、StepSearch、HIPRAG；作者称这些结果由其独立复现，并使用 Qwen2.5 3B/7B、2018 Wikipedia、E5 retriever、top-k=3。
- 正面之处是同时报告 EM/F1、Search Depth、Search Efficiency 和 OSR，而不是只报告单一准确率。
- 但 PDF 未给出各 baseline 的逐项训练预算、优化步数、超参数、随机种子、重复次数、方差或显著性检验，也未明确证明各方法获得相同的总训练 compute、检索调用预算和调参预算。
- 3B 表含 HIPRAG-base 与 HIPRAG-instruct，7B 表只列 HIPRAG-instruct；AutoSearch 与各方法在 base/instruct 初始化和训练设置上的完全同配关系无法仅由主表审计。
- Related Work 中讨论了 R1-Searcher++、Search Wisely、ReARTeR 等效率导向方法（PDF 物理页 2、12），但主实验未纳入这些更贴近“减少冗余检索”的 comparator。
- 未报告评测样本数、独立重复或置信区间。OSR 又以“在最终步前曾答对”为定义（PDF 物理页 7），因此同样会把参数记忆或偶然早期命中计为 over-searching 证据。

故“包含若干强基线”成立，但“强基线比较已充分公平、可审计”不成立。

## 争议结论与可接受表述

| 论文式结论 | 第三读裁决 |
|---|---|
| self-answering 识别 minimal sufficient depth | 需改写。中间答案是 self-generated，但充分性由 gold EM oracle 识别。 |
| 机制按题目复杂度和模型能力自适应 | 有行为证据，但题目复杂度未被独立测量；低深度也可由参数记忆/benchmark 熟悉度造成。 |
| 避免 over-searching 且不损害质量 | 在所测 0–4 深度和指标下获得支持；不外推到长程搜索或真实全链路成本。 |
| 更高 efficiency | 只支持“EM/搜索步数”这一代理指标；不支持计入 8×H20 训练后的净效率。 |
| 机制可作为 oracle-free stopping operator | 不支持。gold 只在训练时使用，但 operator 的学习信号仍是 gold-supervised。 |

## 准入建议

- Failure 证据：`准入`。可用于记录“以早期正确答案定义充分深度会依赖 gold oracle，并可能把参数记忆/污染误当检索充分性”“低最大深度不足以验证长程自适应”“仅用搜索步数会漏算训练和生成成本”。
- Operator 证据：`有限准入`。名称应固定为“gold-supervised hindsight intermediate-answer reward for search-depth shaping”；适用边界限定为有训练答案、固定浅深度、离线 RL 的 QA 设置。
- 不准入：oracle-free minimal-sufficient-depth detector、真实部署净节省、长程 agentic search、已排除 contamination 的检索因果主张。
- 总体裁决：`LIMITED_ADMISSION`。论文具有机制价值，但必须携带 oracle、成本、深度、替代解释与公平性边界，不能以作者的宽表述直接下游复用。

