# P019 — Codex 首读

- PDF：`knowledge_base/staging/papers/P019_steca.pdf`
- PDF SHA-256：`f0957a2acf89227b77922ee4d5a9de10759cc6ad89778077f048c178a0184703`
- 读取时间：`2026-07-19T16:45:00+08:00`
- 读取范围：逐页检查 1–18 页；正文 1–9 页、参考文献 10–12 页、数据/实现 13–14 页、完整 prompts 与案例 14–16 页、补充实验 17–18 页；关键表格、曲线、prompt 与案例另作可视核对。

## 方法实际做了什么

- [AUTHOR_FACT] STeCa 先用带 GPT-4o 生成 rationale 的 expert trajectories 对 7B/8B base model 做 3 epochs SFT，得到 base agent；再从 expert prefix 的状态让 base agent探索，用 `N=5` Monte Carlo rollouts 的终局 reward 估计每步 completion probability。
- [AUTHOR_FACT] 若 explored action 后的 MC step reward 相比前一 expert action 的 step reward 下降超过阈值 `δ`（主实验 δ=0），则把该 explored action 标成 deviated action；step reward只用于离线构造数据，不在最终 inference 时运行。
- [AUTHOR_FACT] 检测到第一个 deviated action 后，prompt 明确告诉 GPT-4o“上一动作不最优”，并直接提供该步 ground-truth expert action，请其生成能导向 ground-truth action 的 reflective thought；随后拼接 expert suffix 构造 calibrated trajectory。
- [AUTHOR_FACT] 训练数据还包括 base agent 自主探索成功的 trajectories、对应 expert trajectories，以及 failed cases 的 expert sub-trajectories。最终用 policy-gradient 风格加权 log-likelihood，将 trajectory deviation distance 纳入 reward。
- [READER_INTERPRETATION] 论文题目中的“timely/real-time calibration”主要指训练数据在首次检测到 deviation 时截断并校准；部署后的 agent 没有一个在线 MC detector 或 GPT-4o reflection module，而是通过离线蒸馏过的参数直接继续规划。
- [READER_INTERPRETATION] Reflection 不是从错误轨迹自主发现正确动作，而是对已给 ground-truth action 生成解释性 rationale；应记录为 oracle-guided calibration-data synthesis，而不是 intrinsic self-correction。

## Step reward 与 deviation 判据边界

- [AUTHOR_FACT] Step reward 是从某一 prefix 开始、由当前 policy 继续 rollout 的终局成功率估计；主实验每步只采样 5 条、temperature=1。
- [AUTHOR_FACT] 检测时比较的是相邻时间点/状态上的两个 completion estimates：前一 expert action 与下一 explored action。Figure 3 在 expert trajectories 上显示越接近终点，MC reward 通常越高。
- [READER_INTERPRETATION] 该判据将“离终点更近带来的自然 completion-probability 上升”作为参照。`δ=0` 时，一个合理但暂未提高 5-sample 估计的动作也可能被标成 deviation；论文没有报告 detector precision/recall 或相对于人工步骤标签的误报率。
- [READER_INTERPRETATION] 对 expert prefix 的逐步单分支偏离以及 ground-truth suffix 的可得性，是训练期强 oracle；它适合自动制造校准数据，不直接适用于无 expert trajectory 的开放任务。
- [AUTHOR_FACT] GPT-4o step-reward annotation 与 learned reward model variants 均低于 MC，但 GPT-4o variant 接近：MC 平均四格为 69.6/63.6/74.3/76.1，GPT-4o 为 69.1/62.5/74.1/74.9，RM 为 68.2/61.8/74.0/73.3。
- [AUTHOR_FACT] 作者承认 MC sampling 计算昂贵，只有限利用 step rewards，且当前只处理第一次 deviation，不显式处理多个 deviated actions。

## 数据、基线与主结果

- [AUTHOR_FACT] 主数据为 ALFWorld 2,851 train/274 test、13 actions、平均/最大 10.1/20 turns；VirtualHome 4,920 train/494 test、40 actions、平均/最大 11.5/20 turns。测试分 seen task types 与 unseen task variations。
- [AUTHOR_FACT] VirtualHome 数据过滤为环境可执行、最终状态成功、3–20 步的 expert plans；所有 expert action 前的 rationale 由 GPT-4o 根据任务和 expert trajectory 生成。
- [AUTHOR_FACT] Llama-2-7B 主表平均：SFT 63.3、IPR 68.6、STeCa 70.9；四格 STeCa 为 VirtualHome 69.6/63.6、ALFWorld 74.3/76.1。论文没有给出多次训练方差、置信区间或显著性检验。
- [AUTHOR_FACT] STeCa with SFT+DPO 为 70.0，`w/o RT`（只用收集数据中的 optimal trajectories 做 SFT）为 69.6，均明显高于原始 SFT 63.3，但只比完整 STeCa 低 0.9/1.3。
- [READER_INTERPRETATION] 这表明大部分增益可能来自新增的高质量/困难 expert-derived trajectories，本方法的 trajectory-distance reinforced weighting 提供的是较小的附加收益；不能把 70.9−63.3 全部归因于“学会实时校准”。
- [AUTHOR_FACT] 不同 backbone 的 ALFWorld 对比：Mistral-7B STeCa 73.3/75.3 vs IPR 71.4/73.9；Llama-3-8B 74.9/77.0 vs IPR 72.3/75.8。相对 IPR 的绝对优势为 1.2–2.6 点。
- [AUTHOR_FACT] ScienceWorld 补充实验 STeCa 77.3/68.9 vs IPR 75.0/66.8；VirtualHome 按任务长度分组中，短任务与 SFT 同为 76.2，中任务 60.0 vs IPR 59.4，长任务 48.9 vs IPR 42.2。
- [READER_INTERPRETATION] 长任务分组支持优势随 horizon 增大，但没有报告各组样本数或区间；不能从单个分组表推断连续的稳定 scaling law。

## Teacher、预算与评测污染风险

- [AUTHOR_FACT] GPT-4o 同时用于生成所有 expert rationales、生成 ground-truth-conditioned reflective thoughts；base-agent self-generated reflection variant 明显下降到 66.0/61.1/71.4/73.3。
- [READER_INTERPRETATION] 完整方法的 reflection质量依赖强教师且带 ground truth；自生成 ablation 说明较弱 base agent 并不具备同等校准数据生成能力。Claim 必须保留 teacher/oracle 条件和离线成本。
- [AUTHOR_FACT] 所有训练使用 8×A6000 48GB；MC 每个 candidate step 5 rollouts。论文没有报告总 rollout 数、GPU-hours、GPT-4o token/call 成本或与 IPR 的等预算对齐。
- [SOURCE_CONCERN] Appendix D.2 称 calibration analysis 的“seen test set”从 `Dc` 随机选 100 条；`Dc` 在方法中正是用于 reinforced training 的 calibration dataset。PDF 未说明这 100 条先从训练中剔除。
- [READER_INTERPRETATION] 因此 Figure 4 的 seen calibration result 可能存在直接训练样本复用，不能作为独立泛化证据；unseen set 是另从 unseen scenarios 构造，相对更有解释力。主 Table 1 held-out task evaluation 不因这一点自动失效。
- [AUTHOR_FACT] `δ` 的定义处写 `δ≥0`，但 Appendix Table 7 实际测试 `δ=-0.01`；数值结果存在，形式约束与实验范围不一致。

## 源内不一致与案例边界

- [SOURCE_CONFLICT] Figure 9 案例中 Observation 2 明确写 cabinet 2 有 `pan 1`，紧接的 Thought 3 却声称 cabinet 2 没有 pan、只有 saltshaker；这是案例中被标为 deviation 的直接前因，且可视页面与解析文本一致。
- [READER_INTERPRETATION] 该案例很好地说明 observation→thought mismatch，但其历史 deviation 是评测数据预先选定/构造的；“autonomously identifies”是训练后行为解释，不代表 inference 时显式运行 detector。
- [SOURCE_AMBIGUITY] nDTW 定义中正文同时出现索引/归一化表达不严谨：Equation 2 的说明混用 `d(x_i,y_i)` 与 `y_j`；Equation 3 写 `D(x−1,y−1)` 而非明确的末端索引。动作表示及距离函数实际选择也未在 PDF 中清楚报告。
- [SOURCE_CONFLICT] Appendix G.3 正文称成功引导项为 `L_Ds`，Table 6 行/表注却写 `L_Db`；属于符号错误，不能据表自动创建一个新 loss。
- [READER_INTERPRETATION] Figure 5 把四个方法各自一对（有/无 deviation）聚成散点并连接，只能展示汇总关联；不能证明 trajectory deviation distance 对 success 的逐样本因果关系。

## 可抽取候选（尚非正式 Card）

- Operator：`First-Deviation Oracle-Calibrated Trajectory Synthesis`——在 expert prefix 上采样探索，检测首个 completion-probability下降点，用 ground-truth action + teacher reflection + expert suffix制造校准轨迹。
- Operator：`Outcome-Rollout Step Reward for Offline Error Localization`——以多个 continuation 的终局成功率估计当前 action 对未来成功的影响，仅用于离线定位训练数据中的疑似 deviation。
- Failure：`Ground-Truth Rationalization Mistaken for Self-Reflection`——teacher 已获知动作错误及正确 action，生成的是解释/蒸馏数据，而非未知答案条件下的自主纠错。
- Failure：`Adjacent Completion-Probability Drop Conflates Progress and Action Quality`——在有限 MC 样本与不同剩余 horizon 下比较相邻值，可能把噪声或暂时不增益的合理动作标为 deviation。
- Failure：`Calibration Evaluation Reuses Training Calibration Pool`——seen calibration analysis 从 `Dc` 抽样且未说明 holdout，导致训练记忆与真实恢复能力混淆。

## 未解决问题

- `[OPEN_QUESTION]` `Dc` 中被用作 Figure 4 seen evaluation 的 100 条是否在 reinforced training 前严格移除。
- `[OPEN_QUESTION]` Deviated-action detector 对人工/环境 ground truth 的 precision、recall、false-positive rate；5-rollout uncertainty 未报告。
- `[OPEN_QUESTION]` 实际 nDTW action representation、distance 函数与归一化实现，以及公式符号错误是否只属排版。
- `[OPEN_QUESTION]` 各方法使用的新增 trajectory 数、rollout/GPT-4o 预算是否对齐。
- `[OPEN_QUESTION]` 主结果与消融是否有多随机种子；PDF 仅报告单点值。
