# P064 独立二读报告

## 0. 身份、冻结输入与读取边界

- paper_id：`P064`
- attempt_id：`r2-20260720-p064-a1`
- 论文：*How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior*（ACL 2026 Long；ACL Anthology `2026.acl-long.27`）
- 冻结 PDF：`knowledge_base/staging/plan05_sat_a1/P064_experience_following_memory.pdf`
- PDF SHA-256：`2c3992d238f5d6dec4ed96faae0a82e3b88edc6e37b26d8622a2b780f2160400`
- invocation SHA-256：`2987257f673ac4771a6f9f198b5a56b44b006e837347c0adca3243edb75f5625`
- 统一 prompt SHA-256：`ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- 完成时间：`2026-07-20T02:29:58+08:00`
- 执行身份：`/root/plan03_blind_evaluator_v1`；具体模型产品名/版本在当前上下文中不可验证，记为 `unknown`。
- read boundary：`procedural_blinding`，不是技术文件隔离。
- provenance：`reused independent reader thread due platform thread cap`

[AUTHOR_FACT] 本报告以冻结 invocation 及统一 prompt 为任务依据，逐页读取并核验指定 PDF 全部 23 个物理页。文本层使用 PyMuPDF 分批读取，视觉层使用 pdfjs-dist 与 Canvas 在内存中逐页渲染，未生成中间文件。

[READER_INTERPRETATION] 本线程此前存在与 P064 无关的独立盲读上下文，故不是全新空线程；本次是线程首次接触 P064，未读取或利用 P064 的 read_1、Cards、其他报告、Corpus/saturation/retrieval 材料或其他论文读稿，也未联网或枚举工作区。

[AUTHOR_FACT] 可观察访问轨迹仅包括：本 attempt 的 `invocation.md`、统一 `second_read_prompt.md`、指定 `_memory.pdf`，以及对目标 `report.md` 是否存在的精确检查。任务最初给出的、不存在的 `P064_experience_following.pdf` 路径曾发生一次失败的精确哈希尝试；主任务随后明确更正为 invocation 中的 `_memory.pdf`，该失败尝试没有读取到文件内容。

[READER_INTERPRETATION] 本次只生成此二读报告，不创建 Card、Evidence 或 manifest，不作 Candidate 评价，也不与首读自动调和。

## 1. 方法究竟改变哪一步计算

[AUTHOR_FACT] 标准执行循环先从包含 query–execution 对的 episodic memory `D` 中，按当前 query 与历史 query 的输入相似度检索 top-K 记录 `ξK`，再把这些记录作为 in-context demonstrations 生成当前执行轨迹 `e`。（物理页 3，§2.2，定位：`Memory Reading`、`D={(q_i,e_i)}`、`ξ_K`）

[AUTHOR_FACT] 论文系统操纵的第一步是任务完成后的**记忆添加决策**：trajectory evaluator `π(q,e)` 决定是否把当前 query–execution 对写入 memory。四个对照为 fixed memory（从不添加）、add-all（全部添加）、coarse automatic evaluator 选择性添加、strict human/oracle evaluator 选择性添加。（物理页 3–4，§3–3.1，定位：`π_fixed=0`、`π_all=1`、coarse、strict）

[AUTHOR_FACT] 第二步是**记忆删除决策**。periodical deletion 依据时间窗中的检索频率删除低频记录；论文提出的 history-based deletion 要求记录至少被检索 `n` 次，再按这些检索所关联的后续任务平均 utility 是否低于阈值 `β` 删除；combined deletion 对两种规则取 OR。（物理页 6，§4.1，定位：`φ_per`、`φ_hist`、`φ_comb`）

[READER_INTERPRETATION] 论文的主要新计算不是新的 agent 推理器或记忆表征，而是把“未来任务执行反馈”累积为每条记忆的经验效用，并用于回溯删除。experience-following、error propagation 与 misaligned experience replay 是由受控比较得到的行为现象/失败机制，不应与 history-based deletion 这个干预算子混为一项方法。

## 2. 输入、输出、可用信息与干预时点

[AUTHOR_FACT] agent 输入是当前任务 query `q` 与检索出的 K 条历史 query–execution demonstrations；输出是当前执行轨迹 `e`。四个 agent 的任务、输入、输出、检索特征及 K 均不同：RegAgent/EHRAgent/AgentDriver/CIC-IoT Agent 的 K 分别为 6/4/1/3。（物理页 3、12–13，§2.2、附录 A.1，表 3）

[AUTHOR_FACT] 添加发生在当前任务执行完成后。coarse evaluator 使用当前 query、execution/结果及 agent-specific prompt 作判断；strict evaluator 在论文实验中由 ground truth 比较模拟。删除发生在后续执行已经多次检索某条记录之后，history-based rule 可用这些未来任务的 evaluator utility；资源约束变体在每次任务后先做周期删除，若仍超容量，再删除平均 utility 最低的一条。（物理页 4、6、9、12–18，§3.1、§4.1、§5.2、附录 A）

[READER_INTERPRETATION] history-based deletion 的信息具有延迟性：记录必须先被检索并影响若干后续任务，才获得删除证据。因此它不能在记录首次写入时辨认所有有害经验，且早期伤害可能已进入后续记忆。

[OPEN_QUESTION] 文中把 future task evaluations 称作“free quality labels”，但真实部署是否免费取决于环境能否产生可信反馈；在无标准答案、无自动执行验证或 evaluator 调用昂贵时，这一假设并不成立。（物理页 1–2、6，摘要/贡献、§4.1）

## 3. Experience-following、错误传播与错误经验回放

[AUTHOR_FACT] 论文把 experience-following 定义为：当前任务与被检索记录的**输入相似度**越高，当前执行与记录执行的**输出相似度**往往越高。作者对每个 test stream 累积平均两类相似度，并在四个 agent 及不同 backbone 上观察相关趋势。（物理页 2、5、19–20，§3.3，图 3、9、12，表 4–5）

[AUTHOR_FACT] RegAgent 在记忆扩张且检索到高度相似 demonstrations 时，正文报告 Pearson `r≈1`；附录在 Qwen 与不同 retrieval K 下给出的相关系数约为 0.69–0.95，说明强度会随模型、添加策略和 K 改变。（物理页 5、20，§3.3，表 4–5）

[READER_INTERPRETATION] 这些实验建立的是输入/输出相似度随记忆演化的关联，而非“相似经验必然因果导致复制”的完全隔离证明；记忆容量、记录质量与最近邻相似度同时变化。各 agent 又使用不同的输入/输出相似度定义，跨 agent 的相关系数并不是同一测量尺度。

[OPEN_QUESTION] AgentDriver 的附录把 output similarity 描述为 predicted trajectory 与 ground-truth trajectory 的 RBF kernel，而正文定义要求比较当前执行与被检索记录的执行；这两种对象并不显然相同，需要作者澄清实际实现。（物理页 5、13，§3.3 与附录 A.1，定位：AgentDriver output similarity）

[AUTHOR_FACT] error propagation 实验固定每个任务检索到的 demonstrations，但在 error-free 变体中用 ground-truth output 替换 LLM execution。add-all 与 coarse addition 的实际执行和 error-free 变体之间差距随时间扩大；AgentDriver 的 strict addition 后期逐渐接近并在约 2000 次执行后超过该变体。（物理页 5–6，§3.4，图 4）

[READER_INTERPRETATION] 该对照支持“错误执行被写回、再次检索、再传播”的反馈环，但 error-free 并非可靠的全局最优上界：作者脚注明示 AgentDriver ground-truth trajectory 仍可能 suboptimal，且替换输出会改变可复用经验的分布。因此“超过 error-free”不能解释为超过真实最优轨迹。（物理页 6，§3.4 脚注 2）

[AUTHOR_FACT] misaligned experience replay 指某些记录即使通过初始质量筛选，作为未来任务 demonstration 时仍持续产生低 utility；history-based deletion 用后续执行反馈识别这类记录。RegAgent 中被删记录整体误差高于保留记录，strict addition 下误差不超过 1 的记录中，误差大于约 0.5 的部分仍较容易传播误差。（物理页 7–8，§4.3，图 6）

[AUTHOR_FACT] 这一现象并非所有 evaluator 都表现为“保留即更优”：使用 GPT-4o-mini evaluator 的 AgentDriver 中，附录明确报告保留记忆的平均 ground-truth 质量反而低于删除记录。（物理页 22，附录 B.7，图 16 后段）

[READER_INTERPRETATION] 这项反例说明 history-based utility 与记录 intrinsic correctness 可以错位；它可能保留对当前任务流有用但本身不够正确的轨迹，也可能被 noisy evaluator 错误引导。misaligned replay 的缓解能力因此依赖 evaluator 和任务分布，不能被视为普遍保证。

## 4. 最强基线与最近组合基线

[AUTHOR_FACT] 添加实验的最近受控基线是 fixed memory 与 add-all；三档 coarse evaluator 是可自动化的选择性添加对照；strict addition 在四个 agent 上取得表 1 最高性能，但它通过 ground truth 模拟人类，是 oracle reference 而非可直接部署的公平基线。（物理页 4，§3.1–3.2，表 1）

[AUTHOR_FACT] 表 1 中 fixed/add-all/strict 的结果分别为：RegAgent 67.53/55.48/70.95，EHRAgent 16.75/13.05/38.50，AgentDriver 40.11/32.32/51.00，CIC-IoT 71.50/59.90/85.40。add-all 同时把 memory size 扩张至 4100/2411/2125/1050，且四项性能均低于 fixed。（物理页 4，表 1）

[READER_INTERPRETATION] add-all 是验证“相似经验回放会传播错误”的关键负对照：它与其他添加方案从同一初始 memory 出发，又不做质量筛选。但它既改变噪声比例也大幅改变 memory size/最近邻分布，因此不能单独量化每个因素的贡献。

[AUTHOR_FACT] 对 history-based deletion，最近组合基线是：相同添加 evaluator 下的 no deletion、periodical deletion，以及 periodical OR history 的 combined deletion。strict evaluator 下 history deletion 相对 no deletion在 EHRAgent/AgentDriver/CIC-IoT 上由 38.67/51.00/85.40 变为 42.06/51.81/89.60，但 RegAgent 从 70.95 降至 69.80；combined 的记忆最小，却在部分任务进一步降分。（物理页 7，§4.2，表 2）

[AUTHOR_FACT] RegAgent 的 size-matched 补充对照从两种最终 memory 各抽 1000 条高频记录，再在 1000 个 fresh test cases 上固定 memory 评估，history deletion 为 74.4，strict-only 为 72.8。（物理页 21，附录 B.6，表 7）

[READER_INTERPRETATION] 该 size-matched 结果较好地隔离了 RegAgent 的质量/容量混杂，但只覆盖一个 synthetic agent 和一个抽样规模；三个 real agents 没有同等的 size-matched 对照。

[OPEN_QUESTION] 论文引用了多种既有 memory management 方法，却没有与外部 SOTA 系统作端到端 head-to-head；因此“最强基线”只能指本文内部 controlled variants，不能据此声称优于现有完整记忆系统。（物理页 3、9，§2.2、Limitations）

## 5. 模型、token、tool-call、prompt 与 oracle 混杂

[AUTHOR_FACT] 大多数主实验固定 agent backbone 为 GPT-4o-mini；C1/C2 evaluator 分别使用 GPT-4o-mini/GPT-4.1-mini，C3 是在独立训练集 300 条正确 judge data 上微调的 GPT-4.1-mini。附录又在 GPT-4o、DeepSeek-V3、Qwen3-32B/14B 上验证部分趋势。（物理页 3–4、19–20，§3.1，附录 B.2，表 4）

[READER_INTERPRETATION] 同一 agent 内的主要添加对照大体控制了生成 backbone 与任务 prompt，因此性能差异不像纯“换强 agent 模型”。但 evaluator 的模型、微调标签、prompt 和阈值均变化，所谓 evaluator-quality effect 同时包含模型能力、监督数据和判定标准差异。

[AUTHOR_FACT] strict evaluator 全部依赖 ground truth：RegAgent 按真实数值误差阈值，EHRAgent 用 exact match，AgentDriver 用预测轨迹到 ground truth 的 3 秒平均 L2 阈值，CIC-IoT 用字符串匹配。论文因实际逐条人工判断不可行而明确称这是 human/oracle 的模拟。（物理页 4、12–13，§3.1、附录 A.1）

[READER_INTERPRETATION] strict 结果属于在线有标签反馈上界，不能与无标签部署等同；同一 test stream 上使用当前样本 ground truth 决定写入/删除，并影响后续 test samples，实质上是 sequential supervised adaptation。C3 也不是纯零监督，因为使用了 300 条带正确性标签的 judge data。

[AUTHOR_FACT] 四个 agent 的 retrieval K、embedding/feature、输出相似度、任务 prompt、工具环境和指标均不同；AgentDriver 还把原方法的 top-3 后由 LLM 二次筛选简化成 top-1 vector retrieval。（物理页 12–18，附录 A.1–A.4，表 3）

[READER_INTERPRETATION] 这种异质性有利于观察现象是否跨任务出现，却削弱精确的横向数值可比性。论文没有报告 token、trajectory-evaluator 调用数、tool-call、embedding/retrieval 成本、wall-clock 或存储成本；memory size 不是总计算成本。history-based 方法还需持续记录每条经验的检索和 utility 历史。

[OPEN_QUESTION] 需要补充相同总 evaluator 调用预算、相同 memory size、相同检索成本和相同可获得反馈下的比较；还需说明重复运行次数、随机种子、任务顺序方差及统计置信区间。正文和表格主要呈现单条趋势/点估计，未见显著性检验。

## 6. 作者限制、负向结果与未测试边界

[AUTHOR_FACT] 作者明示只研究 task-agnostic 的 addition/deletion，没有覆盖 structural transformation、merging、summarization、reflection；对不同 agent 架构的外推需要额外细粒度分析。论文亦明确没有理论保证，结论来自经验实验。（物理页 9，Limitations）

[AUTHOR_FACT] add-all 在四个 agent 上全部劣于 fixed；部分 coarse addition 曲线持平或下降，fixed 有时优于 coarse。作者指出直接使用 vanilla LLM trajectory evaluator 可能比制作一个小而高质量的微调数据集产生更严重的负面影响。（物理页 4–5，§3.2，表 1、图 2/8）

[AUTHOR_FACT] coarse C1 下 history/combined deletion 并不稳定：AgentDriver 的 no-del/history 为 36.92/34.00，CIC-IoT 为 74.00/73.70，RegAgent 为 63.18/62.10；combined 进一步降至 35.62/68.80/59.32。GPT-4o-mini evaluator 在 EHRAgent 上带来增益，却在 AgentDriver 上退化。（物理页 7，§4.2，表 2、图 5）

[AUTHOR_FACT] strict evaluator 下 periodical deletion 在四个 agent 的性能均不高于 no deletion；strict history deletion 在 RegAgent 的原始非配平比较也略低于 no deletion。Qwen3-32B 上 strict+history 为 68.4，低于 strict-only 的 72.9；Qwen3-14B 则为 73.6 对 72.9。（物理页 7、20，表 2、表 4）

[AUTHOR_FACT] 删除超参数存在明显敏感性：RegAgent history deletion 将 `β` 从 0.5 改为 0.6 时 SR 从 69.8 降至 62.0；period 从 500 改为 100 时 periodic deletion 从 67.7 降至 53.2。（物理页 20，附录 B.3，表 6）

[AUTHOR_FACT] task distribution shift 是把同一测试集的 embedding/input vectors 用 GMM 聚成三组后重排，并非引入全新任务族；resource-constraint 实验只覆盖 EHRAgent 与 AgentDriver。CIC-IoT 的 1000 个测试样本来自该数据集 training split。（物理页 8–9、13、18–19、23，§5、附录 A.1/A.5/B.8）

[READER_INTERPRETATION] 尚未测试或证据不足的边界包括：真正的新概念/新环境分布、不可获得 ground truth 的开放式任务、反馈强延迟或非平稳时的 history utility、真实 memory 存储与检索预算、长期超过数千步的累积、对抗/隐私敏感记忆、更多 agent 架构，以及 evaluator 自身分布漂移。

## 7. Operator 候选（仅供主 Codex 后续裁决）

1. [READER_INTERPRETATION] **O1：trajectory-evaluator-gated addition。** 任务后用 `π(q,e)` 筛选是否写入经验，避免 add-all 噪声反馈环。（物理页 3–4，§3.1）
2. [READER_INTERPRETATION] **O2：future-utility history deletion。** 对每条被检索经验累计后续任务 utility，达到最小观察次数后按均值阈值删除。（物理页 6，§4.1）
3. [READER_INTERPRETATION] **O3：frequency OR utility combined deletion。** 同时清除长期低频与高频但低效用记录，以性能换容量。（物理页 6–7，§4.1–4.2）
4. [READER_INTERPRETATION] **O4：小规模高质量 judge supervision。** 用 300 条独立标注轨迹微调 evaluator，以改善选择性添加/删除的稳定性。（物理页 4–5、7，§3.1–3.2、§4.2）
5. [READER_INTERPRETATION] **O5：硬容量下的最低平均 utility 淘汰。** 每次执行后先周期删除，仍超限时只移除 utility 最低记录。（物理页 8–9，§5.2）

## 8. Failure 候选（仅供主 Codex 后续裁决）

1. [READER_INTERPRETATION] **F1：add–retrieve–imitate 的错误传播环。** 错误轨迹写回后因输入相似被再次检索并复现，形成累积退化。（物理页 5–6，§3.3–3.4，图 4）
2. [READER_INTERPRETATION] **F2：通过入库筛选但对未来任务有害的 misaligned replay。** 单条执行看似正确不代表是有效 demonstration。（物理页 7–8，§4.3，图 6）
3. [READER_INTERPRETATION] **F3：noisy evaluator 的双重放大。** 同一错误 judge 同时控制 addition 与 history deletion，可把坏记录留下并删除好记录。（物理页 7、22，§4.2、附录 B.7）
4. [READER_INTERPRETATION] **F4：add-all 造成 memory bloat 与全面性能下降。** 四个 agent 均出现。（物理页 4，表 1）
5. [READER_INTERPRETATION] **F5：容量—质量—最近邻相似度混杂。** 更大 memory 同时改变候选覆盖、噪声量和检索相似度，原始分数难归因。（物理页 4–5、7、21，表 1–2、表 7）
6. [READER_INTERPRETATION] **F6：strict/oracle feedback 的不可部署边界。** ground truth 模拟 human evaluator，掩盖了真实反馈缺失问题。（物理页 4、12–13，§3.1、附录 A.1）
7. [READER_INTERPRETATION] **F7：删除规则超参数脆弱。** `β`、周期和最小检索次数变化可显著降分。（物理页 20，表 6）
8. [READER_INTERPRETATION] **F8：utility correctness 错位。** 被保留经验可能比被删经验的 ground-truth 质量更低。（物理页 22，图 16、附录 B.7）

## 9. 解析文本与视觉 PDF 核对

[AUTHOR_FACT] 文本层和视觉层均覆盖物理页 1–23。视觉核对确认：表 1/图 2 位于物理页 4，图 3–4 位于页 5，删除公式位于页 6，表 2/图 5 位于页 7，限制位于页 9，agent 与 evaluator 细节位于页 12–18，补充结果位于页 19–23。

[READER_INTERPRETATION] 未发现影响结论的解析文本—视觉版式冲突；本报告引用的表格数值与放大后的视觉表格相符。公式文本存在常见的符号/换行归一化，式义和阈值以视觉页为准。

[OPEN_QUESTION] 论文自身存在两处可见的跨表数值不一致，并非文本解析错误：EHRAgent C1 addition 在表 1 为 26.19，表 2 对应 coarse/no-del 为 25.91；strict addition 在表 1 为 38.50，表 2 对应 strict/no-del 为 38.67。正文没有说明这是重跑、随机波动还是转录差异。（物理页 4、7，表 1–2）

## 10. 独立性声明

[READER_INTERPRETATION] 本报告只在冻结输入下记录作者事实、独立解释、开放问题及 Operator/Failure 候选，并给出物理页、章节、图表与短定位文本；未接收或迎合首读结论，未生成正式 Card/Evidence，未执行 Candidate、novelty/prior-work 或科研裁决。
