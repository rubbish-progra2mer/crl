# P019 独立第二读核源报告

## 0. 任务与来源快照

- [AUTHOR_FACT] 本报告对应 invocation snapshot `r2-20260719-p019-a1`，启动时间为 `2026-07-19T15:59:05+08:00`；canonical metadata 为 `ACL:2025.findings-acl.604`，题名 *STeCa: Step-level Trajectory Calibration for LLM Agent Learning*，Findings of ACL 2025。（定位：`invocation.md` 顶部清单）
- [AUTHOR_FACT] 实际核验的 PDF 共 18 个物理页，文件大小 563,161 bytes；实算 SHA-256 为 `f0957a2acf89227b77922ee4d5a9de10759cc6ad89778077f048c178a0184703`，与 invocation 一致。统一提示词实算 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，也与 invocation 一致。
- [READER_INTERPRETATION] 下文“PDF 页”指文件物理页；括号内另列论文印刷页码，避免把 PDF 第 1 页误写为印刷页 1。
- [READER_INTERPRETATION] 本报告仅做独立核源、机制拆解、边界与失败记录，不生成 Card，不对 Candidate、创新性或科研价值作判断。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] STeCa 的前置步骤仍是用专家 ReAct 轨迹进行 SFT；每个 action 单元同时包含 CoT rationale 与环境动作，得到 base agent `π_base`。（定位：PDF 页 3–4，印刷页 11599–11600，§3 与 §3.1；短定位：“Warm-up via Supervised Fine-tuning”，式 (4)）
- [AUTHOR_FACT] 方法的第一项新增计算是在探索/数据构造时，用 Monte Carlo rollout 的终局奖励期望估计每个动作的 step reward：从给定历史继续采样 `N` 条后续轨迹，再平均 outcome reward。（定位：PDF 页 2–3，印刷页 11598–11599，§2 “Step-level Reward Acquisition”，式 (1)）
- [AUTHOR_FACT] 方法随后比较相邻步骤的 step reward。base agent 在专家前缀后产生探索动作；若探索动作的 step reward 相对前一专家动作下降超过阈值条件，则把该探索动作标为 deviated action。正文给出的判据是 `r_step(s_t, â_{t+1}) - r_step(s_{t-1}, a_t) < δ`。（定位：PDF 页 4，印刷页 11600，§3.2 “Deviated Action Detection…”，式 (5)）
- [AUTHOR_FACT] 检出第一处偏差后，方法把“此前专家前缀 + 偏差动作 + 对应 ground-truth action”交给 off-the-shelf LLM（实例为 GPT-4o），生成能导向 ground-truth action 的 reflective thought；该校准步再接上专家后缀，组成 calibrated trajectory。（定位：PDF 页 4–5，印刷页 11600–11601，§3.2 “Calibrated Trajectory Collection…”；PDF 页 15，印刷页 11611，Figure 7）
- [AUTHOR_FACT] 方法不是等整条失败轨迹结束后再处理；作者称其在检测到第一个 deviated action 时立即构造校准轨迹，并停止不必要的后续探索。（定位：PDF 页 5，印刷页 11601，§3.2；短定位：“immediately when detecting the first deviated action”）
- [AUTHOR_FACT] 最后的新增计算是混合三类数据做 reward-weighted policy-gradient training：校准轨迹 `D_c`、成功探索轨迹 `D_e`、失败位置对应的专家后缀 `D_s`；用 nDTW 轨迹偏离距离形成 `r_c/r_s/r_e`，再进入总目标式 (10)。（定位：PDF 页 5，印刷页 11601，§3.3，式 (7)–(10)）
- [READER_INTERPRETATION] 因而，最准确的改变位置是“训练前的数据构造与训练目标”，而不是测试时额外挂接一个显式 MC 控制器：训练期先定位首个 reward drop，用 oracle 辅助反思生成纠正样本，再用距离加权的混合目标训练策略。
- [OPEN_QUESTION] 论文把该能力称作 real-time/timely calibration，但附录测试设置只描述普通 ReAct 推理、one-shot prompt、greedy decoding；没有说明测试时运行式 (1)/(5) 的 MC 检测器。论文证据因此支持“训练数据在首个偏差处即时构造”，但不能直接证明推理时存在一个显式在线 detector。（定位：PDF 页 4–5，§3.2–3.3；PDF 页 13–15，印刷页 11609–11611，Appendix C、E.1）

## 2. 输入、输出、可用信息与干预时点

### 2.1 基本任务接口

- [AUTHOR_FACT] 任务被形式化为 POMDP `(U,S,A,O,T,R)`；给定自然语言任务 `u`，策略在历史交互 `e_{t-1}` 上产生 action `a_t`，环境返回 observation `o_t`，直到成功或达到最大步数；最终 outcome reward 在 `[0,1]`。（定位：PDF 页 2，印刷页 11598，§2 “Task Formulation”）
- [AUTHOR_FACT] 训练与测试的 agent action 使用 ReAct 风格，先生成 rationale/thought 再执行 action；推理阶段用一个 one-shot 示例，greedy decoding，temperature 0。（定位：PDF 页 4，§3.1；PDF 页 13–15，Appendix C、E.1，Figure 6）

### 2.2 偏差检测接口

- [AUTHOR_FACT] 输入包括专家子轨迹/环境状态、base agent 的探索动作、MC 后续 rollout 与环境给出的终局 reward；实现设置为 `N=5`、MC temperature 1、`δ=0`。（定位：PDF 页 3–4，§2、§3.2；PDF 页 6，印刷页 11602，Implementation Details）
- [AUTHOR_FACT] 输出是每步 reward 估计以及“deviated / non-deviated”二元判定；step reward 只用于检测 deviated actions，作者明确说不直接将其作为更广泛的优化信号。（定位：PDF 页 4，§3.2，式 (5) 后；PDF 页 9，Limitations (2)）
- [READER_INTERPRETATION] 式 (5) 比较的是两个不同时间/状态上的 MC 估计；`N=5` 时估计方差可能较高，但正文未报告置信区间、重复采样稳定性或误检率。因此它更像 reward-drop heuristic，而非已校准的偏差概率。

### 2.3 反思校准接口

- [AUTHOR_FACT] 反思模型可见：历史轨迹、已被标成不优的最后一步、该步的 ground-truth action；提示还显式告知“last step is not optimal”。输出是能引出 ground-truth action 的 reflective thought。（定位：PDF 页 4，§3.2；PDF 页 15，Appendix E.2，Figure 7）
- [AUTHOR_FACT] 校准轨迹在纠正步之后直接使用 expert trajectory 的剩余后缀；偏差轨迹也被保留进 `D_c` 的定义。（定位：PDF 页 4–5，§3.2，式 (6)）
- [READER_INTERPRETATION] 这不是探索 agent 在无答案条件下自主找回轨迹，而是 oracle-assisted calibration data construction：ground-truth action 与 expert suffix 都属于训练期额外可用信息。

### 2.4 训练输出与测试干预

- [AUTHOR_FACT] 训练输出是经 SFT warm-up 后再做 1 epoch reinforced training 的 LLM agent；主实验 base model 为 Llama-2-7B-Chat，另测 Mistral-7B 与 Llama-3-8B-Instruct。（定位：PDF 页 6–7，§4.1、§5.1；PDF 页 13–14，Appendix C）
- [AUTHOR_FACT] 测试时所有方法按 ReAct 格式从任务/历史生成 thought-action，使用 greedy decoding；论文未写测试时调用 GPT-4o 反思或 MC rollout。（定位：PDF 页 13–15，Appendix C、E.1）
- [OPEN_QUESTION] 训练得到的模型究竟以何种可观察内部信号“识别”测试时偏差，论文没有给出显式触发规则、校准动作标记或推理时 reflection call trace；Figure 9 只展示案例中的 “Self-reflection” 文本。（定位：PDF 页 16，印刷页 11612，Figure 9）

## 3. 最强基线与最接近的组合基线

- [AUTHOR_FACT] Table 1 中最强的非 STeCa 主基线是 IPR：四个 split 为 67.6/61.9/70.3/74.7，平均 68.6；STeCa 为 69.6/63.6/74.3/76.1，平均 70.9。作者把平均相对提升报告为 3.4%。（定位：PDF 页 6，印刷页 11602，Table 1、§4.2）
- [AUTHOR_FACT] 机制最邻近的两类成分分别由不同基线覆盖：IPR 使用 step reward 扩增 sub-trajectory preference pairs；E2CL 使用 planning/feedback/correction data 做监督微调。Table 1 的 E2CL 平均为 68.2。（定位：PDF 页 13，印刷页 11609，Appendix B；PDF 页 6，Table 1）
- [READER_INTERPRETATION] 论文没有提供一个同时结合“IPR 式 step-level 定位 + E2CL 式 correction/reflection + 与 STeCa 相同数据量和训练目标”的完整组合基线；因此无法从 Table 1 单独分离三者叠加的边际贡献。
- [AUTHOR_FACT] 在相同 STeCa 收集数据上，作者另给两种训练变体：SFT+DPO 平均 70.0、去掉 reward tuning 的 SFT 平均 69.6，均低于完整方法 70.9。（定位：PDF 页 6，Table 1、§4.2）
- [READER_INTERPRETATION] 这两项是训练目标消融，能部分支持 reward-weighted training 的作用，但它们不是上述“最接近组合基线”，也没有控制 GPT-4o oracle、MC rollout 成本或样本规模。

## 4. 模型、token、tool-call、prompt 与 oracle 差异

- [AUTHOR_FACT] 主 tuning-based 对比使用 Llama-2-7B-Chat 作为基础模型；Table 2 又在 ALFWorld 上分别用 Mistral-7B 与 Llama-3-8B-Instruct 比较 SFT/IPR/STeCa，STeCa 在列出的 seen/unseen 分数上均最高。（定位：PDF 页 6–7，Table 1、Table 2、§5.1）
- [AUTHOR_FACT] STeCa 的反思训练样本由 GPT-4o 生成；用 base agent 自己生成反思时，Table 3 四个 split 从 69.6/63.6/74.3/76.1 降至 66.0/61.1/71.4/73.3。（定位：PDF 页 7，印刷页 11603，Table 3、§5.2）
- [READER_INTERPRETATION] 这项负向结果说明成绩对外部强模型生成的反思质量敏感，因而“STeCa mechanism”与“GPT-4o teacher quality”并未被完全解耦。
- [AUTHOR_FACT] MC 版本每个待估动作采样 5 条后续轨迹；GPT-4o annotation 与 reward-model prediction 是另两种 step reward 获取变体，Table 3 中均低于 MC，但 GPT-4o annotation 接近 MC。（定位：PDF 页 6–7，Implementation Details、Table 3；PDF 页 14–15，Appendix D.1、E.3）
- [READER_INTERPRETATION] MC 方案显然增加环境 rollout/tool interaction 数；论文没有报告各方法的总 rollout、环境 step、LLM token、GPT-4o 调用数、训练样本数或等成本控制。性能差异可能部分来自额外计算与 oracle 信息，而不仅是目标函数。
- [AUTHOR_FACT] reflection prompt 不只改变措辞，还直接给 ground-truth action 并声明前一步错误；这比一般无 oracle 的自反思提示拥有更强信息。（定位：PDF 页 15，Figure 7）
- [AUTHOR_FACT] 主表把 GPT-3.5-Turbo/GPT-4 的 prompting-only 结果与 7B tuning-based agents 并列；这些比较在模型、是否训练及数据接口上均不同。（定位：PDF 页 6，Table 1）
- [OPEN_QUESTION] 论文未报告 prompt token 长度、context truncation、各 baseline 的 one-shot 示例是否完全相同、GPT-4o 反思样本数量及 teacher 版本快照，因此无法排除 token/prompt/teacher-version 差异。
- [OPEN_QUESTION] nDTW 的局部 action 距离只写成“such as L2 or cosine distance”，没有说明自然语言 thought-action 的表示、embedding 模型或实际采用哪一种距离；该实现细节会直接影响式 (7)–(9) 的 reward。（定位：PDF 页 3，印刷页 11599，§2 “Normalized Dynamic Time Warping”，式 (2)–(3)）

## 5. 作者明示限制、负向结果与未测试边界

### 5.1 明示限制

- [AUTHOR_FACT] MC sampling 需要大量采样迭代，带来显著计算开销；作者将其列为第一项限制。（定位：PDF 页 9，印刷页 11605，Limitations (1)）
- [AUTHOR_FACT] step rewards 当前只用于识别/评估 deviated actions，未充分用于更广泛的决策或优化。（定位：PDF 页 9，Limitations (2)）
- [AUTHOR_FACT] 框架聚焦检测到第一处偏差后立即校准，没有显式处理多个 deviated actions 的多步校准。（定位：PDF 页 9，Limitations (3)）

### 5.2 真实负向或无增益结果

- [AUTHOR_FACT] 自生成反思显著低于 GPT-4o 反思，具体四个 split 见 Table 3 的 66.0/61.1/71.4/73.3 对 69.6/63.6/74.3/76.1。（定位：PDF 页 7，Table 3）
- [AUTHOR_FACT] GPT-4o annotation 与 reward-model prediction 都没有超过 MC sampling；reward model 在 VirtualHome seen/unseen 为 68.2/61.8，在 ALFWorld 为 74.0/73.3。（定位：PDF 页 7，Table 3）
- [AUTHOR_FACT] SFT+DPO 与无 reward tuning 变体的平均分分别是 70.0、69.6，低于完整方法的 70.9。（定位：PDF 页 6，Table 1、§4.2）
- [AUTHOR_FACT] 去掉任一训练损失都下降；其中去掉 exploration loss 的降幅最大，VirtualHome/ALFWorld unseen 从 63.6/76.1 降至 60.5/71.2。（定位：PDF 页 17，印刷页 11613，Table 6、§G.3）
- [AUTHOR_FACT] `δ=0` 最好；`δ=-0.01/0.05/0.1` 在两数据集均略低。（定位：PDF 页 17–18，Table 7、§G.4）
- [AUTHOR_FACT] VirtualHome 短任务（≤7 步）上 STeCa 与 SFT 同为 76.2，没有优势；中等长度 7–13 步只比 IPR 高 0.6 个百分点（60.0 对 59.4）。（定位：PDF 页 18，印刷页 11614，Table 9、§G.5）

### 5.3 未测试或证据不足边界

- [AUTHOR_FACT] 主实验是 VirtualHome 与 ALFWorld，补充实验加入 ScienceWorld；均为模拟交互环境。主数据过滤到 3–20 步，平均/最大 turn 为 10.1/20 与 11.5/20。（定位：PDF 页 5、13，§4.1、Appendix A，Table 4；PDF 页 17–18，§G.1、Table 8）
- [READER_INTERPRETATION] 未展示真实设备、开放网页、非封闭工具生态、超过 20 步很多的轨迹、连续/高维动作、非二值稀疏终奖或安全关键场景；不能从本文数据外推这些边界。
- [OPEN_QUESTION] 主结果表只给单点分数，没有训练多 seed 的均值/方差、置信区间或显著性检验；“significantly”在统计意义上是否成立无法由报告数字核验。（定位：PDF 页 6–8，Table 1–3、Figure 4–5）
- [READER_INTERPRETATION] Figure 3 支持“离完成越近，平均 MC reward 总体越高”的趋势，但可视曲线有局部波动；正文“monotonically increase”的严格单调表述强于图中可直接确认的证据。（定位：PDF 页 7，Figure 3；续文 PDF 页 8，§5.3）
- [OPEN_QUESTION] 偏差检测的 precision/recall、误检/漏检、MC 方差，以及检测位置相对真实首错位置的误差均未报告；因此式 (5) 的 detector 质量尚不能单独评估。

## 6. 可抽取的 Operator 与可记录 Failure（仅核源描述）

### 6.1 Operator

- [READER_INTERPRETATION] **Reward-drop detector**：在专家前缀后探索一步，以 MC outcome expectation 估计相邻 step rewards，用阈值 `δ` 标出首次下降。（证据：PDF 页 3–4，式 (1)、(5)，Figure 2）
- [READER_INTERPRETATION] **Oracle-guided reflection splice**：把偏差动作、ground-truth action 与历史交给强 LLM，生成 reflective thought，并拼接 expert suffix 构造校准轨迹。（证据：PDF 页 4–5，§3.2；PDF 页 15，Figure 7）
- [READER_INTERPRETATION] **First-deviation early stop/calibration**：检出首个偏差即校准，不继续完成该探索轨迹。（证据：PDF 页 5，§3.2）
- [READER_INTERPRETATION] **Trajectory-distance reward shaping**：用 nDTW 偏离距离分别奖励大偏差校准、困难专家后缀，并惩罚成功轨迹中的不必要绕行。（证据：PDF 页 5，式 (7)–(9)）
- [READER_INTERPRETATION] **Three-source reinforced mixture**：联合 `D_c/D_s/D_e` 进入 reward-weighted policy-gradient objective。（证据：PDF 页 5，式 (10)）
- [READER_INTERPRETATION] **Deviated-history stress test**：从含偏差历史的状态继续执行，并与移除偏差动作的条件对照，测校准恢复能力。（证据：PDF 页 8，§5.4、Figure 5；PDF 页 14，Appendix D.2）

### 6.2 Failure

- [AUTHOR_FACT] **弱反思生成器失败**：base agent self-generation 反思在四个 split 全部下降。（PDF 页 7，Table 3）
- [AUTHOR_FACT] **替代 reward 获取不胜 MC**：GPT-4o annotation 与 reward model 均未超过 MC；reward model 降幅更明显。（PDF 页 7，Table 3）
- [AUTHOR_FACT] **简单训练目标不胜完整 reward tuning**：SFT+DPO 和仅 SFT 均低于完整 STeCa。（PDF 页 6，Table 1）
- [AUTHOR_FACT] **移除任一数据/损失组件均下降**：尤其无 exploration loss 时 unseen 成功率下降较多。（PDF 页 17，Table 6）
- [AUTHOR_FACT] **阈值偏离 0 均下降**：正阈值可能过滤校准机会，负阈值可能容忍次优动作；后半句是作者解释。（PDF 页 17–18，§G.4、Table 7）
- [AUTHOR_FACT] **短任务无增益**：≤7 步 VirtualHome 上与 SFT 完全持平。（PDF 页 18，Table 9）
- [AUTHOR_FACT] **案例中的 SFT/IPR 未恢复**：Figure 9 的 ALFWorld 个案中，SFT 和 IPR 沿偏差继续并失败，STeCa 反思后成功；这只是单个可视案例，不是失败率统计。（PDF 页 16，Figure 9）

## 7. 关键判断—定位索引

| 判断 | 标签 | PDF 页（印刷页） | 章节/图表/式 | 短定位文本 |
|---|---|---:|---|---|
| MC 终奖期望生成 step reward | [AUTHOR_FACT] | 3（11599） | §2，式 (1) | “expected value of these outcome rewards” |
| 相邻 reward drop 检测偏差 | [AUTHOR_FACT] | 4（11600） | §3.2，式 (5) | “step-level reward comparison” |
| GPT-4o 获知 ground-truth action | [AUTHOR_FACT] | 4、15（11600、11611） | §3.2，Figure 7 | “ground-truth action” |
| 首个偏差处立即校准 | [AUTHOR_FACT] | 5（11601） | §3.2 | “first deviated action” |
| 三类轨迹与 TDD reward | [AUTHOR_FACT] | 5（11601） | §3.3，式 (7)–(10) | “trajectory deviation distance” |
| IPR 是主表最强非 STeCa 基线 | [AUTHOR_FACT] | 6（11602） | Table 1 | Average 68.6 |
| GPT-4o 反思质量敏感 | [AUTHOR_FACT] | 7（11603） | Table 3，§5.2 | “Self-generation” |
| 多偏差未处理 | [AUTHOR_FACT] | 9（11605） | Limitations (3) | “does not explicitly address multi-step calibration” |
| 测试为普通 ReAct greedy decoding | [AUTHOR_FACT] | 13–15（11609–11611） | Appendix C、E.1，Figure 6 | “greedy decoding” |
| 长任务优势更大、短任务持平 | [AUTHOR_FACT] | 18（11614） | Table 9，§G.5 | “≤7 / 7–13 / >13” |

## 8. 解析文本与可视 PDF 的一致性检查

- [AUTHOR_FACT] 已逐页提取并阅读 18/18 个物理页；另以 PDF 内存渲染复查 18 页全页缩略图，并重点查看 Figure 2、Table 1、Figure 4–5、Figure 9、Table 5–9 所在页。主要标题、正文、图注、表值、脚注与附录在可视页和解析文本之间未发现实质冲突。
- [READER_INTERPRETATION] 双栏 PDF 的文本抽取在 Figure 1–2、Table 1、Figure 4–5 与 Figure 6–8 处存在阅读顺序交错，数学花体字符也有 Unicode 替代符；上述位置均以可视版式重新确定左右栏、图表归属和公式顺序。本报告没有把抽取顺序当作原始排版顺序。
- [AUTHOR_FACT] 发现两处属于原文内部标记/表述不一致、而非 parser-versus-visual 冲突：其一，正文与 Table 3 称 “GPT-4o Annotation”，Appendix D.1 却写 “utilize GPT-4 for annotation”；其二，§G.3 开头列 `L_Ds`，Table 6/图注写 success-guided loss `L_Db`，而正文方法的数据集符号是 `D_s`。（定位：PDF 页 7、14、17，Table 3、Appendix D.1、§G.3/Table 6）
- [AUTHOR_FACT] Table 2 正文称 Mistral-7B unseen “17.1% improvement over SFT”，表值是 75.3 对 58.2，即差 17.1 个百分点；若按相对百分比则约为 29.4%。原文此处把“百分点差”写成“% improvement”的含义不清。（定位：PDF 页 7，Table 2、§5.1）
- [OPEN_QUESTION] 以上原文不一致应在后续 reconciliation 中保留为待澄清项，不宜由第二读者擅自修正为某一版本。

## 9. Provenance、实际读取文件与可观察 trace

- Invocation 引用：`r2-20260719-p019-a1`；invocation 文件实算 SHA-256：`8fac2e0fe1e719395c0074d360605f0a79c707de643bde245b6a49eebd98fd77`。
- 实际读取的研究输入文件：
  1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P019_steca.pdf`
  2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
  3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P019/read_2_attempts/r2-20260719-p019-a1/invocation.md`
- 额外读取的运行级说明文件：`C:/Users/g/.codex/skills/pdf/SKILL.md` 与 `C:/Users/g/.codex/plugins/cache/openai-curated-remote/superpowers/6.1.1/skills/verification-before-completion/SKILL.md`。前者是系统强制的通用 PDF 工具说明，后者是交付前验证规范；二者都不是工作区研究材料，且未读取其中引用的其他文件。为保持 trace 诚实，在此显式列出。
- 未读取：read_1、Cards、其他读者报告、blind query、其他项目文件；未枚举工作区；未联网。
- 实际工具：PowerShell `Get-Content`（提示词/invocation 首次读取，控制台出现编码错显）；Python UTF-8/JSON 重新读取两份文本；Python `hashlib` 做 SHA-256；PyMuPDF (`fitz`) 做 18 页逐页文本提取、页数/页框/图像与绘图对象检查及内存渲染；Pillow 做内存 JPEG 全页/拼图检查；`apply_patch` 仅写本 `report.md`。
- 失败工具尝试：曾尝试调用本地 `pdftoppm` 做替代渲染，但系统未安装该命令，返回 `FileNotFoundError`；没有产生输出文件，也没有据此形成论文判断。
- 可观察 file-access/tool trace：上述命令级操作在本任务工具日志中可见；更底层系统调用 trace、完整 thread ID 与可验证的文件级 allowlist 均 `unavailable`。
- Read boundary：`procedural_blinding`。App 未提供可验证的文件级技术隔离；本报告不把程序性只读约束声称为技术隔离。
- Actual model/version：模型界面仅可知为 Codex（based on GPT-5）；精确 serving model/version `unknown`。
- Canonical task/agent identifier：`/root/p019_second_read`；底层 thread ID `unavailable`。
- 网络：未调用网络工具，`network access observed: none`。
- 写入：只写入 `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P019/read_2_attempts/r2-20260719-p019-a1/report.md`；未生成 Card 或其他项目文件。
