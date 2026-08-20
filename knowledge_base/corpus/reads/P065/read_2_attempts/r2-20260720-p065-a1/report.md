# P065 独立二读报告

## 0. 读取身份、边界与完整性

- `[AUTHOR_FACT]` 论文：Lang Feng、Zhenghai Xue、Tingcong Liu、Bo An，*Group-in-Group Policy Optimization for LLM Agent Training*，NeurIPS 2025，arXiv:2505.10978（PDF p.1，标题页）。
- `[AUTHOR_FACT]` 本次唯一论文源为 `knowledge_base/staging/plan05_sat_a1/P065_gigpo.pdf`；实测 SHA-256 为 `f6a4d4559c41048be67a0e4a062f9957996fc79e6a80f65fe66f1140fac82dcd`，与 invocation 冻结值一致；PDF 共 27 页。
- `[READER_INTERPRETATION]` Provenance: reused independent reader thread due platform thread cap
- `[READER_INTERPRETATION]` 本报告只读取本 attempt 的 `invocation.md`、其中内嵌冻结统一 prompt、指定 PDF 与已在同一复用线程中完成复核的必要规则；未读取 read_1、Cards、其他报告、其他论文读稿、Corpus/saturation/retrieval 文件，未联网。
- `[READER_INTERPRETATION]` 已按 PDF p.1–27 顺序提取每页文本并逐页执行内存视觉渲染复核；每页文本均非空，公式、表格、图、算法和附录案例未见 parsed text 与视觉 PDF 的实质冲突。

## 1. 一句话技术结论

- `[AUTHOR_FACT]` GiGPO 在同一批 `N` 条完整 episode rollout 上计算两层相对 advantage：episode/macro advantage 比较整条轨迹总回报；step/micro advantage 把轨迹中重复出现的同一环境状态作为 anchor，将该状态后的动作及其 discounted return 组成局部组；两者以 `A=AE+ωAS` 相加后进入 clipped policy objective（PDF p.4–6，§4.1–4.3，Eq. 2–9；Figure 1–2）。
- `[READER_INTERPRETATION]` 该方法真正改变的是**已有 rollout 的离线重分组与 advantage 赋值**，而不是采样过程：它不为每个 state 追加分支 rollout，也不引入 critic；micro signal 仍是 Monte Carlo return 相对值，受后续动作、折扣距离、状态别名及重复次数影响，并非单步动作的因果效果（PDF p.5–6，§4.2）。
- `[READER_INTERPRETATION]` 方法适用性高度依赖可重复、可稳定匹配的环境状态。离散、确定、可回退且常有循环的 ALFWorld/WebShop 最符合假设；连续、噪声、部分可观测或几乎不重复的状态空间会使 step group 稀疏、错误合并或直接退化为 episode-only GRPO（PDF p.10，§6）。

## 2. 冻结问题逐项回答

### Q1. 方法究竟改变哪一步计算？

- `[AUTHOR_FACT]` Vanilla trajectory-level GRPO 对同一 task/初始状态下的 `N` 条完整轨迹只计算一个 episode 相对 advantage，并把它作为整条轨迹的宏观信号（PDF p.3–5，§3、§4.1，Eq. 1–3；Figure 1 左）。
- `[AUTHOR_FACT]` GiGPO 在 rollout 完成后枚举轨迹组内所有 distinct environment states `U`；对每个 anchor `s̃`，把所有满足 `s_t^(i)=s̃` 的 `(a_t^(i),R_t^(i))` 聚为 `GS(s̃)`，其中 `R_t^(i)=Σ_{k=t}^T γ^{k-t}r_k^(i)`（PDF p.5–6，§4.2，Eq. 4–7）。
- `[AUTHOR_FACT]` 对每个局部组，作者以组均值和 `Fnorm`（`std` 或固定 1）标准化 discounted return 得到 `AS`，再与所属轨迹的 `AE` 相加：`A(a_t^(i))=AE(τ_i)+ωAS(a_t^(i))`（PDF p.6，§4.3，Eq. 7–8）。
- `[AUTHOR_FACT]` 最终目标是按 step 求和的 clipped importance-ratio objective，另加相对 reference policy 的 KL penalty；GiGPO 的伪代码只比 GRPO 多出 anchor grouping、`AS` 计算与 advantage 合并（PDF p.6，Eq. 9；PDF p.17，Algorithm 1）。
- `[READER_INTERPRETATION]` 因而 GiGPO 是 advantage estimator/credit assignment 层的改动；rollout policy、environment interaction、actor 更新框架与 GRPO 保持同型。

### Q2. 输入、输出、可用信息与干预时点

- `[AUTHOR_FACT]` policy 输入为当前环境状态 `s_t` 和 task prompt `x`，输出为 textual action `a_t`；环境返回即时 reward `r_t` 与下一状态（PDF p.3，§3，Problem setup）。
- `[AUTHOR_FACT]` 每轮训练先从同一 task `x` 初始化 `N` 个 identical environments，完成至多 `T` 步的整批 on-policy rollout；GiGPO 的新增计算只在全部轨迹采集完毕后发生（PDF p.4，§4；PDF p.17，Algorithm 1 lines 5–13）。
- `[AUTHOR_FACT]` episode signal 使用整条轨迹 total return；step signal使用动作发生时点之后的 discounted return，因此读取该动作之后直至 episode 结束的全部 reward（PDF p.4–6，Eq. 2–7）。
- `[AUTHOR_FACT]` ALFWorld/WebShop prompt 实际包含 task description、step count、最近 2 轮 observation/action、current observation 与 admissible actions；Search 使用 full interaction history（PDF p.18–19，§E.2，Figure 8–10）。
- `[OPEN_QUESTION]` anchor key 所称“environment state”究竟是 current observation、完整 simulator state，还是包含历史与 step count 的实际 policy conditioning state，论文未给出实现级定义。若只匹配 observation，则被分在同一 anchor 下的动作可能来自不同历史/隐藏状态；若匹配完整 prompt，重复率又可能远低于 Figure 5（PDF p.5，Eq. 4；PDF p.18–19，Figure 8–10）。
- `[OPEN_QUESTION]` Eq. 7 在同一 anchor 内仍用统一下标 `R_t^(j)`，但 Eq. 4 允许状态在不同轨迹、不同时间步出现；这应理解为每个 occurrence 自己的 `R_{t'}^(j)`，论文记号未显式处理不同时间索引。

### Q3. 最强基线与最接近组合基线

- `[AUTHOR_FACT]` ALFWorld/WebShop 的 RL 基线为 PPO、RLOO、GRPO；提示基线为 Qwen2.5、ReAct、Reflexion，另列 GPT-4o 与 Gemini-2.5-Pro（PDF p.7–8，§5.1–5.2，Table 1）。
- `[AUTHOR_FACT]` 与 GiGPO 在架构和 rollout 上最接近的基线是 GRPO：Qwen2.5-1.5B 上 GRPO 的 ALFWorld/WebShop success 为 72.8/56.8，GiGPOw/o std 为 86.1/67.4；Qwen2.5-7B 上为 77.6/66.1 对 90.2/75.2（PDF p.8，Table 1）。
- `[AUTHOR_FACT]` 若只看最强既有 RL 数值，7B 的 PPO 在 ALFWorld/WebShop 达 80.4/68.7，高于同规模 GRPO，但使用额外 critic；1.5B 中 GRPO 是两任务最强非 GiGPO RL 基线（PDF p.8，Table 1）。
- `[AUTHOR_FACT]` 最接近的**组合**基线是 DAPO；作者把 DAPO 的 dynamic sampling 与 clip-higher 同时接入 GiGPO，得到 GiGPOdynamic。Qwen2.5-1.5B WebShop success 为 GRPO 56.8、DAPO 66.1、GiGPOdynamic 75.0（PDF p.19–20，§E.4，Table 4）。
- `[AUTHOR_FACT]` Search QA 的完整平均强基线在 3B 是 Search-R1 32.5，在 7B 是 ZeroSearch 39.1；GiGPO 分别为 42.1 与 47.2。StepSearch 缺少单跳结果，不能形成完整平均对照（PDF p.8，Table 2）。
- `[READER_INTERPRETATION]` 因果上应优先比较 GiGPO 对 GRPO，以及 GiGPOdynamic 对 DAPO；闭源模型、prompt-only agent 或使用 critic 的 PPO 只能说明系统级表现，不是对 micro advantage 的单变量检验。

### Q4. 模型、token、tool-call、prompt、oracle 与 rollout/cost matching

- `[AUTHOR_FACT]` ALFWorld/WebShop 的所有 RL 方法使用相同超参数；group-based 方法均为 16 组×8 rollout=128 environments，PPO 也用 128 environments。ALFWorld 最大 50 步、prompt/response 为 2048/512；WebShop最大 15 步、4096/512；rollout temperature 均为 1.0（PDF p.7，§5.1；PDF p.17–18，§E.1）。
- `[AUTHOR_FACT]` ALFWorld/WebShop 使用 rule-based reward：成功 10、失败 0、invalid action -0.1；Search QA 使用成功 1、失败 0、invalid -0.01，最多 4 turn，group size 5（PDF p.17–18，§E.1）。
- `[AUTHOR_FACT]` Search QA 按 Search-R1 设置，retriever 为 E5；采用 similarity-based GiGPO，以 longest matching subsequence similarity `>0.9` 合并状态（PDF p.7，§5.1）。
- `[AUTHOR_FACT]` 作者明确称 GiGPO 不增加任何 LLM rollout：anchor grouping 是已有轨迹上的 hashmap 分组，`AS` 是简单算术；Figure 6 报告 rollout 221.97s、old prob 24.99s、ref prob 25.96s、update 89.86s、episode advantage 0.05s、grouping 0.01s、step advantage 0.53s（PDF p.10，§5.6，Figure 6）。
- `[READER_INTERPRETATION]` “无额外 rollout”在算法结构上成立；但“identical rollout cost”只表示相同 rollout 配置，并未报告各训练后 policy 的实际 episode 长度、生成 token 或 wall-clock rollout 时间。不同 policy 可能提前成功、失败或循环，故 realized inference cost 未被直接等配证明。
- `[AUTHOR_FACT]` 作者声称 GiGPO 与 GRPO 有相同 GPU memory usage，并且特有时间开销 `<0.002%`（PDF p.1–2，Abstract/Introduction；PDF p.10，§5.6）。
- `[READER_INTERPRETATION]` Figure 6 的数值与 `<0.002%` 冲突：GiGPO 特有 grouping+AS 为 `0.54s`，共享部分连同 AE 为 `362.83s`，故 `0.54/362.83≈0.001488`，即 **0.1488%**，约为声称上限 0.002% 的 **74.4 倍**。若作者本意是“比例 `<0.002`”而不是“百分比 `<0.002%`”，则数值成立，但论文单位写错。
- `[READER_INTERPRETATION]` “same GPU memory”没有峰值显存表或 GRPO 并排实测；可从不含 critic、不加 rollout 推断增量很小，但不能从现有实验验证为严格相同。
- `[READER_INTERPRETATION]` ALFWorld/WebShop 的 matched RL 对照较强，因为模型、prompt budget、环境数、温度、训练迭代与 reward 都被明确对齐；Search QA 对 Search-R1/ZeroSearch/StepSearch 的训练 compute、prompt 和实际 tool-call budget未逐项并列，因而 QA 增益的算法归因较弱。
- `[AUTHOR_FACT]` Search 7B 在“最多 3 次 tool call”下，单跳平均约 0.9 次、多跳约 1.6 次；作者将其与 OTC 的约 1.0/1.7 次比较，但 OTC 不在 Table 2 性能主表中（PDF p.8–9，§5.3）。
- `[OPEN_QUESTION]` Search 的“max turn=4”与文中“at most 3 tool calls”如何映射，以及所有 QA 基线是否共享相同限制，没有完整说明。

### Q5. 作者限制、负向结果和未测试边界

- `[AUTHOR_FACT]` 作者明示的主要限制是 anchor group 依赖 state matching；复杂环境中的噪声或细微差异会使 identical state 难以检测。作者称无重复状态时 `AS=0`，GiGPO 退化为 GRPO，并建议未来使用 embedding 或 domain-specific structural equivalence（PDF p.10，§6）。
- `[AUTHOR_FACT]` `Fnorm` 没有统一最优：困难/不平衡任务中 `std` 可能放大梯度、固定 1 更好；其他任务两者相近，reward variance 稳定时 `std` 仍可能有益（PDF p.8，§5.2）。
- `[AUTHOR_FACT]` `ω` 的 WebShop sensitivity 显示最佳 success 在 `ω=0.8`（68.3），主设置 `ω=1.0` 为 67.4；`ω=1.4` 降至 56.3，甚至低于 `ω=0` 的 56.6，说明过强 micro signal 会压制有用的 episode guidance（PDF p.20，§E.5，Table 5）。
- `[AUTHOR_FACT]` Figure 5 中 singleton step groups 始终占约 20.7%–34.2%，即相当比例的状态没有可比较的重复 occurrence（PDF p.9，§5.5，Figure 5）。
- `[READER_INTERPRETATION]` 未测试边界包括：连续控制、高维随机 observation、部分可观测/隐藏状态、跨 task anchor、非平稳环境、近似匹配误合并、不同 anchor size 的偏置、长 trajectory 的 Monte Carlo 方差，以及真实线上 agent 的延迟/成本。
- `[READER_INTERPRETATION]` ALFWorld/WebShop 只报告三随机种子均值±波动，没有显著性检验；QA 只给单一分数、无 seed/置信区间；因此小差值的稳健性未被量化（PDF p.8，Table 1–2）。

### Q6. 可抽取的 Operator 与真实 Failure

- `[READER_INTERPRETATION]` **Operator O1：episode-group reuse。** 在相同 task/初始状态的一批完整 rollout 内，同时复用全轨迹 return 计算 macro signal，并复用重复 state occurrence 计算 micro signal，无需额外分支采样（PDF p.4–6，Figure 1–2）。
- `[READER_INTERPRETATION]` **Operator O2：anchor-state retrospective grouping。** 以可哈希的 state 为 key，把跨轨迹/跨时间的 occurrence 聚合，再比较该状态后的 discounted return（PDF p.5–6，Eq. 4–7）。
- `[READER_INTERPRETATION]` **Operator O3：hierarchical additive advantage。** 用 `AE+ωAS` 同时保留 episode coherence 与局部动作排序，并可叠加 DAPO 等单轮 group-RL 技术（PDF p.6，Eq. 8–9；PDF p.19–20，§E.4）。
- `[READER_INTERPRETATION]` **真实 Failure F1：成本百分比算术/单位错误。** Figure 6 支持约 0.149% 增量，而非 `<0.002%`；这是论文内部可复算的数值冲突（PDF p.10，Figure 6）。
- `[AUTHOR_FACT]` **真实 Failure F2：state-repeat 缺失。** 作者承认没有重复 state 时无法形成有效 `AS`，方法退化为 GRPO（PDF p.10，§6）。
- `[AUTHOR_FACT]` **真实 Failure F3：micro 权重过大导致性能下降。** `ω=1.4` 的 WebShop success 56.3，低于 `ω=0.8` 的 68.3，也略低于无 step signal 的 `ω=0` 56.6（PDF p.20，Table 5）。
- `[OPEN_QUESTION]` **潜在 Failure P1：singleton+std 未定义。** Eq. 7 对 group size 1 使用 `std=0` 会出现 `0/0`，正文/算法未给 epsilon、丢弃或置零规则；但 Figure 5 显示 singleton 很常见。作者“无重复时 AS=0”的结论需要未披露的实现 guard（PDF p.6，Eq. 7；PDF p.9，Figure 5；PDF p.10，§6）。
- `[READER_INTERPRETATION]` **潜在 Failure P2：时间与后续策略混杂。** 同一 state 的 `R_t` 同时受当前 action、后续 policy 和距终奖的折扣长度影响；Figure 3 甚至明确用“较早 occurrence 折扣更多”产生排序。因此 `AS` 是局部条件下的 return association，不是当前 action 的独立因果贡献（PDF p.6，Figure 3）。
- `[READER_INTERPRETATION]` **潜在 Failure P3：loop occurrence 过度加权。** 同一 trajectory 可在同一 anchor 出现多次，Eq. 4 将每次都作为组成员；会循环的失败轨迹可能以大量相关样本主导局部均值/方差。Figure 5 的早期 `|GS|≥50` 直接证明此类大重复组存在，但论文未做去重或按 trajectory 重加权消融（PDF p.5，Eq. 4；PDF p.9，Figure 5）。
- `[READER_INTERPRETATION]` **潜在 Failure P4：state aliasing。** Search 用 LCS>0.9 近似合并文本状态；表面相似但语义/隐藏状态不同的页面可能被误视为同一 decision state。论文只报告阈值，没有误合并率或 threshold ablation（PDF p.7，§5.1）。

### Q7. 核心证据定位表

| 主题 | 标签与证据 | 精确定位 |
|---|---|---|
| episode advantage | `[AUTHOR_FACT]` 相同 task/初始状态下完整轨迹 total return 的组内相对值。 | PDF p.4–5，§4.1，Eq. 2–3 |
| anchor grouping | `[AUTHOR_FACT]` 跨 trajectory/time 汇总完全相同 state 的 occurrence。 | PDF p.5，§4.2，Eq. 4 |
| step return | `[AUTHOR_FACT]` 从当前 occurrence 到 episode 终点的 discounted return。 | PDF p.5–6，Eq. 5–7 |
| 合并 objective | `[AUTHOR_FACT]` `A=AE+ωAS` 后进入 clipped policy objective。 | PDF p.6，§4.3，Eq. 8–9 |
| rollout matching | `[AUTHOR_FACT]` group RL 都用 16×8=128 environments，PPO 也用 128。 | PDF p.17–18，§E.1 |
| reward 边界 | `[AUTHOR_FACT]` ALF/WS 成功10、失败0、invalid -0.1；Search 成功1、失败0、invalid -0.01。 | PDF p.17–18，§E.1 |
| 主 matched baseline | `[AUTHOR_FACT]` GiGPO 与 GRPO 在相同模型/预算下比较。 | PDF p.7–8，§5.1–5.2，Table 1 |
| 组合 baseline | `[AUTHOR_FACT]` DAPO 对 GiGPOdynamic。 | PDF p.19–20，§E.4，Table 4 |
| group 动态 | `[AUTHOR_FACT]` singleton 约20.7%–34.2%，早期存在大量≥50的大组。 | PDF p.9，§5.5，Figure 5 |
| 成本冲突 | `[AUTHOR_FACT]` grouping 0.01s、AS 0.53s、共享/AE 362.83s；正文却称 `<0.002%`。 | PDF p.10，§5.6，Figure 6 |
| state-repeat 限制 | `[AUTHOR_FACT]` 无重复 state 时退化为 GRPO。 | PDF p.10，§6 |
| ω 负向边界 | `[AUTHOR_FACT]` `ω=1.4` 明显劣于 `ω=0.8`。 | PDF p.20，§E.5，Table 5 |

### Q8. parsed text 与 visual PDF 是否冲突？

- `[READER_INTERPRETATION]` 27/27 页完成顺序 parsed-text 核验与逐页视觉渲染；标题、正文、Eq. 1–14、Figure 1–11、Table 1–5、Algorithm 1、prompt 与案例均未发现解析错位造成的事实冲突。
- `[READER_INTERPRETATION]` 成本问题不是解析冲突：视觉版 PDF p.10 的 Figure 6 清楚显示 `221.97, 24.99, 25.96, 89.86, 0.05, 0.01, 0.53`，正文也清楚写 `<0.002%`；矛盾来自作者的百分比计算或单位。
- `[READER_INTERPRETATION]` PDF p.4–6 的密集公式/图、p.8 的两张大表、p.9–10 的动态图与成本图、p.16–20 的附录公式/算法/表格均已视觉单独核对，与 parsed text 一致。

## 3. 逐页覆盖账本

| PDF 页 | 覆盖内容与核验结果 |
|---:|---|
| 1 | `[AUTHOR_FACT]` 标题、摘要、引言起始；文本/视觉一致。 |
| 2 | `[AUTHOR_FACT]` 问题动机、GiGPO 两层结构、贡献与相关工作起始；文本/视觉一致。 |
| 3 | `[AUTHOR_FACT]` 相关工作、problem setup、group-based RL 预备知识；文本/视觉一致。 |
| 4 | `[AUTHOR_FACT]` Figure 1、episode group、Eq. 2–3；文本/视觉一致。 |
| 5 | `[AUTHOR_FACT]` Figure 2、anchor grouping、Eq. 4–5；文本/视觉一致。 |
| 6 | `[AUTHOR_FACT]` Eq. 6–9、Figure 3、hierarchical objective；文本/视觉一致。 |
| 7 | `[AUTHOR_FACT]` benchmarks、baselines、训练设置、主结果叙述；文本/视觉一致。 |
| 8 | `[AUTHOR_FACT]` Table 1–2、normalization 与 QA/tool-call 结果；文本/视觉一致。 |
| 9 | `[AUTHOR_FACT]` Figure 4–5、消融与 step-group 动态；文本/视觉一致。 |
| 10 | `[AUTHOR_FACT]` Figure 6 成本分解、结论和作者限制；文本/视觉一致。 |
| 11 | `[AUTHOR_FACT]` 参考文献；文本/视觉一致。 |
| 12 | `[AUTHOR_FACT]` 参考文献；文本/视觉一致。 |
| 13 | `[AUTHOR_FACT]` 参考文献；文本/视觉一致。 |
| 14 | `[AUTHOR_FACT]` 参考文献；文本/视觉一致。 |
| 15 | `[AUTHOR_FACT]` 参考文献结束；文本/视觉一致。 |
| 16 | `[AUTHOR_FACT]` verl-agent、Broader Impacts、unbiasedness 起始；文本/视觉一致。 |
| 17 | `[AUTHOR_FACT]` Eq. 11–14、Algorithm 1、ALFWorld 训练细节；文本/视觉一致。 |
| 18 | `[AUTHOR_FACT]` WebShop/Search 训练细节与 Figure 8 prompt；文本/视觉一致。 |
| 19 | `[AUTHOR_FACT]` Figure 9–11、VLM 结果叙述、orthogonality 起始；文本/视觉一致。 |
| 20 | `[AUTHOR_FACT]` Table 3–5、DAPO 组合和 `ω` sensitivity；文本/视觉一致。 |
| 21 | `[AUTHOR_FACT]` ALFWorld 完整轨迹 steps 1–3；文本/视觉一致。 |
| 22 | `[AUTHOR_FACT]` ALFWorld 轨迹 steps 4–6；文本/视觉一致。 |
| 23 | `[AUTHOR_FACT]` ALFWorld 轨迹 steps 7–10；文本/视觉一致。 |
| 24 | `[AUTHOR_FACT]` WebShop 轨迹 steps 1–2；文本/视觉一致。 |
| 25 | `[AUTHOR_FACT]` WebShop 轨迹 steps 3–5 起始；文本/视觉一致。 |
| 26 | `[AUTHOR_FACT]` WebShop 结尾与 Search 轨迹 steps 1–2；文本/视觉一致。 |
| 27 | `[AUTHOR_FACT]` Search 轨迹 step 3 与答案；文本/视觉一致。 |

## 4. 关键未决问题

1. `[OPEN_QUESTION]` anchor state 的精确 serialization/key 是什么；是否包含 task、step count、最近历史、可用动作和隐藏 simulator state？
2. `[OPEN_QUESTION]` `|GS|=1` 且 `Fnorm=std` 时如何避免除零；是否丢弃、置 `AS=0`、加 epsilon，还是使用总体 std？
3. `[OPEN_QUESTION]` 同一 trajectory 对同一 anchor 的多次 occurrence 是否去重或重加权；若不处理，loop-heavy trajectory 会贡献高度相关的重复样本。
4. `[OPEN_QUESTION]` `std` 是 population standard deviation 还是 sample standard deviation；小 group 的尺度会显著不同。
5. `[OPEN_QUESTION]` Appendix C 只证明 `Fnorm=1` 的 episode `AE` 与 RLOO 成比例；step `AS` 在 occurrence sampling、相关样本和近似 state matching 下是否仍有任何 unbiasedness 保证？
6. `[OPEN_QUESTION]` Figure 5 是否排除所有轨迹必然共享的 initial state；“group size 6–8 表明策略一致”的解释是否控制了正常路径上的公共状态？
7. `[OPEN_QUESTION]` Search 的 LCS>0.9 state grouping 误合并率、漏合并率和阈值敏感性如何；论文没有 ablation。
8. `[OPEN_QUESTION]` Figure 6 的 `<0.002%` 是否原意为无单位比例 `<0.002`；若不是，成本百分比应更正为约 `0.149%`。
9. `[OPEN_QUESTION]` “identical GPU memory”与“identical LLM rollout cost”是否有 GRPO 并排峰值显存、token、episode length 和 wall-clock 原始数据支持？

## 5. 独立阅读结语

- `[READER_INTERPRETATION]` GiGPO 最可复用的机制是：从已付费的完整 rollout 中回收重复 state occurrence，构造无需额外采样的局部相对 return 信号，再与 trajectory-level signal 联合优化。
- `[READER_INTERPRETATION]` 其最可靠的实证来自 ALFWorld/WebShop 对 GRPO 的 matched 设置以及 episode/step 两项消融；QA 和闭源/提示基线更适合作为系统性能参照，而非严格算法归因。
- `[READER_INTERPRETATION]` 其核心边界不是“有没有额外 rollout”，而是重复状态是否真代表相同决策条件、singleton/近似匹配如何处理，以及 Monte Carlo micro return 能否避免时间、后续 policy 与循环频次混杂。
- `[READER_INTERPRETATION]` 可确认的论文内部冲突只有成本百分比/单位；其余关键问题属于实现未披露或方法适用边界，不能在二读中冒充已验证失败。
