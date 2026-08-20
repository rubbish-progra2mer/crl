# P073 独立二读报告

## Provenance 与读取边界

- Attempt：`r2-20260720-p073-a1`
- 引用的冻结 invocation：`knowledge_base/corpus/reads/P073/read_2_attempts/r2-20260720-p073-a1/invocation.md`
- canonical PDF `knowledge_base/papers/P073_probecal.pdf` 在本次启动时不存在；实际读取路径为 `knowledge_base/staging/plan05_sat_a2/P073_probecal.pdf`。
- 实际 PDF SHA-256：`2c56eb776ba9caf9dbe0663fdabbafc2941c10c08394494df158c5980090cc53`，与 invocation 冻结值一致。
- PDF 共 25 个物理页，对应论文印刷页 16781–16805；解析文本逐页覆盖 25/25。视觉核对覆盖物理页 1–9、12–25；物理页 10–11 为 References，仅做解析文本核对。
- 未读取 read_1、Cards、其他 read_2、saturation、retrieval、blind 或其他论文；未联网。
- 技术隔离状态：`procedural_blinding`，不是文件级技术 allowlist。
- Actual model/version：`unknown`（runtime 未暴露精确 serving version）。可见 task path：`/root/plan05_card_source_audit_e`；产品 thread ID 不可见。
- 可观察工具轨迹：读取冻结 invocation；检查 canonical/staging 精确路径并计算 staging PDF SHA-256；用本地 PDF 解析器按物理页 1–25 提取文本；以内存渲染核对关键图表和附录表；仅写本报告。

## 一、结论摘要

[AUTHOR_FACT] PROBECAL 使用语言模型内部 embedding 和执行结果的二元监督训练一个 MLP，估计给定 prompt 或 execution trace 的成功概率，再用估计概率选择 prompt、对候选 trace 的答案做置信加权聚合。（物理页 2 Figure 1；物理页 4 §3）

[READER_INTERPRETATION] 方法真正改变的是 **候选生成之前的 prompt 分配** 与 **候选生成/执行之后的 trace reranking**。它不改变工具本身，不直接修复已生成代码，也不是无监督或零样本校准；其关键资源是带 ground-truth answer 的代表性训练题目、由这些题目产生的多条候选执行及可访问的 LLM hidden embedding。

[AUTHOR_FACT] 论文在 MATH 子类与 TabMWP 上报告 accuracy 与 15-bin ECE；主要模型是 `CodeLlama-7B-Instruct-hf`，另测 Mistral-7B、CodeLlama-13B-Instruct、Llama3-8B-Instruct。GPT-4o-mini 只用于展示原始 logit 仍失准，没有展示 PROBECAL 在闭源模型上的训练/收益。（物理页 5–9 §4–§5.3；物理页 22 Tables 14–16）

[READER_INTERPRETATION] 论文支持的最稳妥结论是：在所测程序生成式 tool-use、同数据集监督、可读内部 embedding、既定候选池下，一个小型监督式 outcome probe 可改善若干 prompt/trace 选择结果。它不支持跨领域零样本 probe transfer、闭源 API 普适应用、真实异构工具生态、在线错误恢复或未标注部署校准。

## 二、逐页覆盖

| 物理页 | 印刷页 | 核验内容 | 解析/视觉状态 |
|---:|---:|---|---|
| 1 | 16781 | Abstract、问题定义、两类 miscalibration、PROBECAL 总述 | 文本+视觉一致；注意正文同时出现 `PROBECAL` 与 `PROBCAL` 拼写。 |
| 2 | 16782 | Figure 1；tool-agent 形式化；candidate program/trace；主要贡献摘要 | 文本+视觉一致；Figure 1 清楚显示 execution-result supervision、MLP 与 prompt/trace selection。 |
| 3 | 16783 | Figure 2；prompt design 与 trace selection 两类场景 | 文本+视觉一致。 |
| 4 | 16784 | §3 reward estimation；prompt/trace calibration；weighted training | 文本+视觉一致；公式与段落顺序无冲突。 |
| 5 | 16785 | LLM logit、temperature scaling、数据集、agent 类型、实现细节 | 文本+视觉一致。 |
| 6 | 16786 | Table 1；ECE、baseline 和 main-results 起始 | 文本+视觉一致；表格脚注对 baseline ECE 的定义非常关键。 |
| 7 | 16787 | Table 2；main results、消融、TS/WEIGHT/SORT/E.S.L. | 文本+视觉一致。 |
| 8 | 16788 | train/test shift、其他模型、训练集大小、verbal confidence、闭源诊断 | 文本+视觉一致。 |
| 9 | 16789 | Table 3；Related Work、Conclusion、Limitations | 文本+视觉一致。 |
| 10 | 16790 | References | 解析覆盖；未做视觉细读。 |
| 11 | 16791 | References | 解析覆盖；未做视觉细读。 |
| 12 | 16792 | Table 4 数据规模；附录 B–D 路由与 calibration-curve 定义 | 文本+视觉一致。 |
| 13 | 16793 | Table 5 Mistral dynamic；Figures 3–4 static curves | 文本+视觉一致。 |
| 14 | 16794 | Table 6 static 全数据集结果 | 文本+视觉一致；揭示组合方法并非每个子任务/预算都最优。 |
| 15 | 16795 | Table 7 static variants I | 文本+视觉一致。 |
| 16 | 16796 | Table 8 static variants II | 文本+视觉一致。 |
| 17 | 16797 | Table 9 dynamic 全数据集结果 | 文本+视觉一致；同样存在 prompt-only/trace-only 优于组合的单元格。 |
| 18 | 16798 | Table 10 dynamic variants I | 文本+视觉一致。 |
| 19 | 16799 | Table 11 dynamic variants II | 文本+视觉一致。 |
| 20 | 16800 | Table 12 static train/test ECE | 文本+视觉一致；固定宽表解析未发现列反转。 |
| 21 | 16801 | Table 13 dynamic train/test ECE | 文本+视觉一致。 |
| 22 | 16802 | Tables 14–16：训练规模、其他模型、verbal confidence；Figure 5 | 文本+视觉一致。 |
| 23 | 16803 | Figures 6–8 | 视觉核对曲线/直方图布局与附录说明一致。 |
| 24 | 16804 | Figures 9–11 | 视觉核对一致。 |
| 25 | 16805 | Figure 12 | 视觉核对一致。 |

## 三、方法究竟改变哪一步计算

### 3.1 监督数据与 representation

[AUTHOR_FACT] 对每个训练问题，作者使用不同 candidate prompts 或采样多条 execution traces，收集 language-agent embedding `ϕ` 与最终 reward `r`。问答场景中，最终结果与 ground-truth answer 匹配时 `r=1`，否则 `r=0`；MLP 学习 `P(r|ϕ)`。（物理页 4 §3，短摘录位置：“reward r equals 1 if the final result matches the ground truth answer”）

[AUTHOR_FACT] 主要实验的 embedding dimension 为 4096；校准器实现为具有 256、256、80 单元的三个 hidden layers 的 MLP，训练 10 epochs，Adam，学习率 `1e-4`；训练集再按 9:1 分 train/validation，并按 validation minimum loss 选模型。（物理页 5 §4.3）

[OPEN_QUESTION] 原文没有说明 embedding 来自哪一层、哪个 token、何种 pooling，也没有给出 prompt embedding 与 trace embedding 的精确序列边界。正文称“three-layer MLP”，实现段又称“three hidden layers”，若加输出层则层数口径不同。这些信息不足以从 PDF 独立复现 representation/probe。

### 3.2 Prompt calibration

[AUTHOR_FACT] 对问题 `q`，方法按 probe 的 estimated reward 为不同 prompt 分配选择概率；作者将其联系到 Boltzmann exploration。（物理页 4 §3 “Prompt Selection Calibration”）

[OPEN_QUESTION] 论文只说“select each prompt proportional to the estimated reward”，没有给出实际归一化公式、Boltzmann temperature、零概率处理或训练/推理采样伪代码。无法从 PDF 判断实现是直接按概率归一化，还是 `exp(score/temperature)`。

### 3.3 Trace calibration

[AUTHOR_FACT] 候选 trace `z_i` 生成后，方法按最终答案 `a` 聚合 `P(\hat r|a,z_i,q)`，选择累计 calibrated confidence 最大的答案；这相当于 confidence-weighted majority voting。（物理页 4 §3 “Execution Trace Selection Calibration”）

[READER_INTERPRETATION] 该干预发生在 candidate programs 已经生成、且为了取得 answer 已经执行之后。它减少的是错误 candidate 被最终采用的概率，不减少候选生成或工具执行本身，也不提供执行中的 step-level uncertainty 或恢复动作。

### 3.4 Prompt+Trace 组合、reweight 与 temperature scaling

[AUTHOR_FACT] 正样本权重设为同一问题中 negative count / positive count，负样本权重为 1，以处理成功样本稀少。（物理页 4 §3.1）

[AUTHOR_FACT] E.S.L. 用 token probabilities 的 `exp(sum log p_i)`；SORT 使用排序后第二小 token probability。Temperature scaling 在 validation NLL 上学习 `T`，只缩放 logits，不改变 argmax class。（物理页 5 §3.1）

[AUTHOR_FACT] Table 1 脚注称组合 ECE 使用 PROBECAL-PROMPT 与 PROBECAL-TRACE “logits”的平均值和 label 计算。（物理页 6 Table 1）

[OPEN_QUESTION] 正文混用 probability、confidence、logit；没有给出组合方法在最终答案选择时究竟平均 pre-sigmoid logits 还是 post-sigmoid probabilities。该歧义会影响 calibration 数值与复现。

## 四、数据、labels、模型与预算

[AUTHOR_FACT] TabMWP 使用 500 个 train questions 训练校准器、500 个 test questions 评价。MATH 分为 Precalculus 198/156、Geometry 474/237、Count & probability 483/291、Number 780/497、Algebra 1065/881、Prealgebra 814/636、Intermediate 607/503（train/test）。（物理页 5 §4.1；物理页 12 Table 4）

[AUTHOR_FACT] static agent 使用 Primitive 与 Instance prompts；dynamic TroVE 对每题使用 import existing tools、create new tools、primitive-only 三个 prompts，每个 prompt 采样 `K` 次，形成 `3K` answers 后 self-consistency。（物理页 5 §4.2）

[AUTHOR_FACT] 主结果中 static 的样本数从 1 到 10，dynamic 从 1 到 20；结果平均 5 runs，每个 run 又平均 10 次采样 `T` answers 的实例。（物理页 7 §4.4）

[OPEN_QUESTION] 预算口径不闭合：TroVE 定义是三种 prompt 各采样 `K` 次（总计 `3K`），实验段却称从多种 prompts 采样总计 `T` answers，附录列名为 `# Samples`。PDF 未说明表中 1/5/10/20 是总候选数、每 prompt 数，还是每方法不同的有效候选数。因此无法严格确认 token、LLM call 与 tool execution budget 完全匹配。

[OPEN_QUESTION] 没有报告训练校准器时每个训练问题生成多少 prompts/traces、总 LLM tokens、总程序执行数、embedding 抽取成本、MLP 参数/训练设备或 end-to-end latency。作者只说训练“within minutes”，并在 Limitations 承认外部校准模型增加计算开销。（物理页 5 §4.3；物理页 9 Limitations）

[READER_INTERPRETATION] test-time 不使用 test ground-truth label，因此不是直接 answer oracle；但整个方法需要同分布的 labeled calibration questions 和执行结果，是 supervised in-domain outcome modeling。该监督成本必须与无监督 self-consistency/logit baselines 分开核算。

[OPEN_QUESTION] PDF 没有 prompt 原文、few-shot exemplars、tool library 的 train/test 重合分析或 contamination test。未发现作者报告直接 split leakage，但也无法排除 prompt/example/tool overlap 对结果的贡献。

## 五、基线与最接近组合基线

[AUTHOR_FACT] 基线包括：

1. `INSTANCE` / `TROVE`：uniform prompt sampling + 无 confidence weighting 的 self-consistency；
2. `INSTANCE-SAMPLE` / `TROVE-SAMPLE`：按训练集中各 prompt 生成 positive answers 的总数分配 prompt sampling，再用普通 self-consistency；
3. `SORT` / `E.S.L.`：uniform prompt sampling + LLM token-logit confidence-weighted majority；
4. TS、WEIGHT、SORT、E.S.L. 作为 PROBECAL variants；
5. verbal confidence 仅在 CodeLlama-13B、TabMWP、size-50 setting 中比较。（物理页 6 §4.3；物理页 7 §4.5；物理页 22 Table 16）

[READER_INTERPRETATION] 最接近的组合基线是“training positive-count prompt prior + LLM-logit trace weighting”，但表中没有明确列出把这两者同时组合的单一 baseline。也没有 linear/logistic probe、仅用 surface/execution features 的监督 reranker、同参数 MLP 不用 hidden embedding、跨域冻结 probe 等对照。因此性能增益可证明“监督式 embedding outcome predictor 有用”，但不能隔离为 MLP 深度、hidden representation 或 calibration 专有机制的贡献。

## 六、实际 calibration metric 与可比性

[AUTHOR_FACT] 主 calibration metric 是 15-bin Expected Calibration Error：按每个 confidence bin 的样本占比加权 `|accuracy-confidence|`；同时报告 task accuracy。（物理页 6 §4.3）

[AUTHOR_FACT] Table 1 明确：`INSTANCE`、`INSTANCE-SAMPLE`、`TROVE`、`TROVE-SAMPLE` 的 ECE 以全 1 confidence vector 对 label 计算，即把每个 prompt/trace 当作同等且 confidence=1；PROBECAL-PROMPT&TRACE 的 ECE 则以两个 probe logits 的平均值计算。（物理页 6 Table 1 脚注）

[READER_INTERPRETATION] 因此 Table 1 的 ECE 并不是 matched confidence estimator 的公平横向比较。baseline 的 0.690/0.823/0.788/0.851 很大程度上等于“始终置信 1”与错误率的差，而不是 self-consistency vote fraction、empirical prompt success rate 或温度校准后的 baseline confidence。该表能证明 probe 输出比全 1 向量更接近频率，但不能单独证明优于所有合理 baseline calibration 方法。

[OPEN_QUESTION] 论文没有报告 NLL、Brier score、adaptive/classwise ECE、bin sensitivity、置信区间或显著性检验。固定 15 bins 且不同方法 confidence construction 不同，限制 calibration 结论强度。

## 七、主要结果与事实核对

[AUTHOR_FACT] Table 1 中，dynamic TabMWP：PROBECAL-PROMPT&TRACE 在 `Acc@5` 为 45.87，对 TROVE 36.69（+9.18 percentage points）；`Acc@10` 为 50.93，对 42.00（+8.93 points），支持正文“over 7%”的局部陈述。（物理页 6 Table 1）

[AUTHOR_FACT] static TabMWP `Acc@10`：组合方法 57.31，INSTANCE 51.79；static Algebra `Acc@10`：31.23 对 28.96。相应 ECE 报告为 0.035/0.026，但 baseline ECE 使用全 1 confidence，需按上一节限制解释。（物理页 6 Table 1）

[AUTHOR_FACT] Mistral-7B dynamic TabMWP `Acc@20`：组合方法 66.56，TROVE 61.07；但 Count `Acc@20`：组合 29.87，TROVE 29.97，组合略低。（物理页 13 Table 5）

[AUTHOR_FACT] CodeLlama-13B static TabMWP、size 500：组合 71.14，INSTANCE 65.66；Llama3-8B：组合 78.48，INSTANCE 75.20。size 50 时组合 67.07，INSTANCE 65.66；TRACE 单独为 67.72，反而高于组合。（物理页 22 Tables 14–15）

[READER_INTERPRETATION] 这些结果是同数据集内重新训练/选择 probe 的模型扩展，不是一个固定 probe 在新模型或新领域上的 transfer。

## 八、负向结果、内部张力与 Failure 线索

[AUTHOR_FACT] Temperature scaling 对 accuracy 与 ECE 通常影响很小；作者观察到 train/test distribution shift，低 train ECE 不保证低 test ECE，TS 也未显著改善 test ECE 或 accuracy。（物理页 7–8 §4.5；物理页 20–21 Tables 12–13）

[AUTHOR_FACT] E.S.L. 与 SORT 作为 probe 输入时表现会波动，E.S.L. 可显著降低性能。例如 dynamic Geometry `Acc@20`：标准组合 9.61，而组合 E.S.L. 为 6.53。（物理页 7 §4.5；物理页 18 Table 10）

[AUTHOR_FACT] verbal confidence 在 CodeLlama-13B/TabMWP/size-50 的 `Acc@10` 为 64.68，低于 INSTANCE 65.66。（物理页 22 Table 16）

[AUTHOR_FACT] 附录显示组合方法不是每个 dataset/budget 的最优项：static Count `Acc@10` 中 PROMPT 29.01 高于组合 28.69；static Geometry `Acc@10` 中 TRACE 11.94 高于组合 11.89；dynamic Prealgebra `Acc@20` 中 TRACE 34.45 高于组合 34.25；Mistral Count `Acc@20` 中 TROVE 29.97 高于组合 29.87。（物理页 13–14 Tables 5–6；物理页 17 Table 9）

[READER_INTERPRETATION] 因而正文“PROBECAL-PROMPT&TRACE achieves the highest performance across all datasets in all tool-using scenarios”（物理页 7 §4.4）与完整附录存在张力。最多可说它在 Table 1 展示的 TabMWP/Algebra 选定预算中最优，且整体经常较强；不能说所有 dataset、budget、base model 都最优。

[OPEN_QUESTION] 所有 sampling 结果虽称平均 5 runs × 10 sampling instances，但表中没有标准差、置信区间、paired tests 或随机种子。诸如 0.01–0.5 point 的差异不能据此认定为稳定改善。

可记录的 Failure 线索：

- [AUTHOR_FACT] 原始 LLM token probabilities 和 verbal confidence 在所测 tool-use setting 中可严重失准，且简单 TS 无法稳定修复 train/test shift。
- [AUTHOR_FACT] 把 E.S.L./SORT 与 probe representation 组合并不保证改善，某些任务显著退化。
- [READER_INTERPRETATION] prompt+trace 双重校准不是单调增益；prompt-only 或 trace-only 可在特定任务/预算更好。
- [READER_INTERPRETATION] 用全 1 confidence 定义 self-consistency baseline ECE 会夸大 calibration gap，属于评价口径 Failure，而不是 agent 本身的自然置信度失败。

## 九、作者明示限制与未测试边界

[AUTHOR_FACT] 作者明示外部 calibration model 带来计算开销，并提醒恶意工具可导致负面后果。（物理页 9 Limitations）

[AUTHOR_FACT] 论文明确说当前输出“completely operated by external tool execution, such as code generation”，把与 UALA 等混合 reasoning/tool-switch 框架的结合留作未来工作。（物理页 9 Related Work）

[READER_INTERPRETATION] 未测试边界包括：真实 API/搜索/视觉工具的非确定性、多轮 stateful agent、工具返回分布漂移、在线更新、跨数据集冻结 probe、跨模型 probe transfer、closed-source hidden representation、工具执行成本优化、安全拒答，以及 calibration 失败后的恢复策略。

[AUTHOR_FACT] GPT-4o-mini 只报告 Count & probability 上 500-output-length 的原始 E.S.L. ECE 0.5149 与 SORT ECE 0.1183；没有训练或应用 PROBECAL。（物理页 8 §5.3）

[READER_INTERPRETATION] 因此“closed-source LLM 也适用 PROBECAL”不成立；该实验只支持“闭源模型的可见 token confidence 仍可能失准”。

## 十、可抽取 Operator 与不可越界内容

### 可抽取 Operator

1. **Supervised embedding reward probe for prompt routing**
   - 输入：问题、tool prompt、可访问的 LLM embedding；训练时另需 ground-truth execution reward。
   - 输出：prompt expected-success probability；在生成候选前改变 prompt sampling allocation。
   - 边界：需要同分布 labels、hidden representation 与额外 probe training；采样归一化细节原文不完整。

2. **Supervised embedding reward probe for trace reranking**
   - 输入：问题、候选 execution traces、候选答案与 trace embedding。
   - 输出：按答案聚合的 calibrated reward score；在候选生成和执行后、最终答案提交前发生。
   - 边界：不减少候选 tool calls，不提供 step-level credit，不修复执行。

3. **Class-imbalance reweighted probe training**
   - 正样本权重为 negative/positive count，负样本权重 1。
   - 作者结果仅显示边际、非普遍改善；不能单独抽成已验证的主要机制。

### 不应抽成强结论

- 不应把 PROBECAL 描述为无监督校准、在线学习或 oracle-free；训练明确使用 ground-truth outcome labels。
- 不应声称组合方法在所有任务、预算和模型上最佳。
- 不应把低 ECE 直接等价为公平超越 self-consistency baseline，因为 confidence construction 不一致。
- 不应声称闭源模型可直接应用 hidden-embedding probe。
- 不应把同域 test improvement 外推为跨域或长期分布漂移下的 transfer。

## 十一、Reconciliation 前必须保留的 Open Questions

1. embedding 的 layer/token/pooling、prompt/trace 序列边界是什么？
2. 每个训练问题实际生成多少候选，probe-training 总 token/tool-execution budget 是多少？
3. dynamic `#Samples` 是总候选 `T` 还是每 prompt 的 `K`；三 prompt 的真实总调用数是否为 `3K`？
4. prompt selection 的概率归一化和 Boltzmann temperature 是什么？
5. PROMPT&TRACE 最终组合的是 logits 还是 probabilities；训练与推理是否一致？
6. 为什么 baseline ECE 使用全 1 vector，而不是 self-consistency vote confidence 或 empirical prompt success probability？
7. 是否存在与 MLP probe 同监督预算的 linear probe、surface-feature reranker 或 cross-domain frozen-probe 对照？
8. 运行方差、随机种子、置信区间和显著性如何？
9. prompt exemplars、工具库与 train/test 是否有内容重合或 contamination？
10. 在真实失败工具、非确定性 API、多轮 state 与分布漂移下，校准是否仍成立？

## 十二、最终二读判断

[READER_INTERPRETATION] P073 提供了一个清楚、可操作的 **监督式 prompt/trace outcome-probe reranking** 机制，并在多个程序生成数学子任务和若干开源模型上显示有意义的 accuracy/ECE 改善。最可信的证据是 matched dataset 内的 probe 与 self-consistency/logit 选择比较，以及 TS、weight、logit-input 的附录消融。

[READER_INTERPRETATION] 证据强度受到四个关键限制：监督 label 与隐藏 embedding 依赖、候选生成预算口径不清、baseline ECE 构造不对齐、以及无方差/显著性且附录存在非单调和负向结果。后续 reconciliation 应保留这些边界，不得把论文压缩成“通用工具 Agent 校准器”或“组合方法普遍最优”。
