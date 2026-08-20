# P015 fresh 独立第三读核源报告

## 0. 身份、输入与访问边界

- Attempt：`r3-20260719-p015-a1`；角色：fresh independent third full-paper source checker。
- Canonical metadata：PMLR:v235/smit24a，*Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs*，ICML 2024。
- [AUTHOR_FACT] 指定 PDF 的实测 SHA-256 为 `8d0330933f495a3804842e8c8b0f778d8529fefeaf8d2a2dbf89d94f97bd0e70`；统一 prompt 的实测 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，均与 invocation 声明一致。
- 实际模型/版本：Codex（系统说明其基于 GPT-5；更细版本在本任务中不可见）；任务标识：`/root/p015_third_read`。
- 研究输入仅为 invocation、统一 prompt、指定 PDF。未枚举工作区，未读取 read_1、read_2、Cards、其他报告或 blind query，未联网。
- 工具过程：PowerShell 定点读取与哈希；`pypdf` 读取元数据并逐页抽取文本；`PyMuPDF`/Pillow 将 23 页渲染到系统临时目录；图像查看工具逐页核对；`apply_patch` 写本报告。系统要求使用 PDF 技能，因而另读取了系统插件目录中的 `pdf/SKILL.md`（仅为工具操作规范，不是研究证据或论文输入）。本次属于 `procedural_blinding`，并非可验证的文件级技术隔离。
- PDF 共 23 页，PDF 页码与页脚印刷页码 1–23 一致。第 17–18 页是旋转 90° 的横向 Table 3；核查时已旋正查看。临时渲染图不属于研究输出，将在完成后删除。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] 论文比较的 MAD 系统改变的是**推理时**的生成与信息传递：多个 LLM 实例/调用在多轮中生成答案，并把其他代理的答案、完整历史或摘要放回后续上下文；作者明确说无需梯度更新。定位：PDF p.2，§2，短定位文本 “entirely using in-context prompting” 与 “no gradient-based parameter updates”。
- [AUTHOR_FACT] 新提出的干预是 agreement modulation：在辩论开始时通过提示词指定代理应同意其他代理的比例，原文模板为 “you should agree with the other agents X% of the time”，并把 X 称为 agreement intensity。定位：PDF p.6，§3 “Improving MAD via agreement modulation”。
- [AUTHOR_FACT] 主要试验载体是 Multi-Persona：angel 接收问题，devil 的 system prompt 被改写以调节不同意程度，judge 管理并输出最后答案。定位：PDF p.2 “Multi-Persona”；p.6 “we modulate the disagreement using the ‘devil’’s system prompt”；p.20–21，Appendix A.5–A.6，`MP MAD`、`ANGEL`、`DEVIL`。
- [READER_INTERPRETATION] 因而论文的新方法没有改训练、权重、检索器或外部工具，而是改变“后续推理调用看到什么社会性先验/上下文”这一计算环节；其作用路径是提示词 → 首轮实际一致率 → 多轮答案演化/最终共识 → 准确率。该路径由 Figure 5–6 支持，但不是因果机制的完全识别。
- [OPEN_QUESTION] “X% of the time”到底是针对题目级事件、单轮事件、答案相同还是论证立场相同，论文未给形式化定义或校准算法；X 与实际首轮 agreement 并非一一对应（Figure 5 右），故 prompt 强度不是已校准的概率控制器。定位：PDF p.6–7，Figure 5。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 输入是多项选择任务：MedQA（4-answer 版本）、PubMedQA（问题、context、答案）、临床 MMLU、CosmosQA、CIAR、GPQA、Chess-short，共 7 个数据集；输出最终被解析为选项字母并据此计算 accuracy。定位：PDF p.3–4，§3 数据集列表；p.20–23，Appendix A.5–A.6 多处 “capital letter answer”。
- [AUTHOR_FACT] 论文正文一处写“三个 medical + three other reasoning datasets”，但实际列出 CosmosQA、CIAR、GPQA、Chess 四个非医疗数据集，Table 2 也有 7 个数据集列。定位：PDF p.3–5，§3 与 Table 2。
- [AUTHOR_FACT] 可用信息按协议不同：SoM 向代理提供其他代理答案并可先摘要；ChatEval 可按顺序共享全部历史、同步生成，或同步生成后摘要；ER 先采样多个 reasoning paths，再把它们拼成 student reasonings 供聚合调用；Self-Consistency 的各路径彼此独立，只按多数答案汇总；Multi-Persona 的 angel/devil 输出交给 judge，judge 可提前结束。定位：PDF p.2，§2；p.3，Table 1；p.20–21，Appendix A.5–A.6。
- [AUTHOR_FACT] agreement modulation 在辩论“at the outset”施加；在 Multi-Persona 中具体改 devil 的 system prompt，而不是辩论结束后重排答案。定位：PDF p.6，§3。
- [READER_INTERPRETATION] judge 的最终 JSON/字母解析属于输出聚合阶段；完整历史、摘要和其他代理答案属于中间可用信息。不同协议的信息集并不相同，因此结果不是在完全相同的条件信息下仅替换一个“辩论算子”。
- [OPEN_QUESTION] Appendix A.6 的 ER CoT prompt 写有 “referring to authoritative sources as needed”，但正文只描述 LLM API 调用，未说明启用浏览、检索或其他 tool。现有 PDF 不能确认代理是否仅凭参数知识回答；也不能把 “API calls” 自动解释为 tool calls。定位：PDF p.3，§3；p.21，Appendix A.6 `ER CoT`。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 不存在跨全部数据集统一最强系统。Table 2 的逐数据集最高值为：MedQA Medprompt 0.65；PubMedQA Medprompt 0.77；MMLU Self-Consistency 0.78；CosmosQA Medprompt 0.48；CIAR SoM 与 Self-Consistency 并列 0.56；GPQA Single Agent 0.33；Chess Multi-Persona 0.33。定位：PDF p.5，Table 2 “Best performance achieved”。
- [AUTHOR_FACT] 作者把 Medprompt 描述为总体表现最好且成本较低的非辩论策略；但本论文实现省略 kNN/训练集检索，只保留 question randomization 与 few-shot CoT ensembling。定位：PDF p.2 “we do not employ the kNN approach”；p.4 “Medprompt strategy ... performs the best overall”；p.5，Table 2。
- [READER_INTERPRETATION] 对 agreement modulation 最接近的控制不是 Medprompt，而是**未加入 agreement-intensity 提示的原始 Multi-Persona**：angel/devil/judge、轮数与基础模型最相近，主要差别正是 devil 的一致倾向提示。SoM 与 ChatEval 是次近的 MAD 结构基线；Medprompt、Self-Consistency、ER 是较强的非辩论/组合推理基线。
- [OPEN_QUESTION] Table 3 与主结果无法直接对上：例如 Table 3（PDF p.17）列出 Single Agent/SIMPLE 的 MedQA `Score 0.76`、多项 ChatEval 为 0.67–0.71、原始 Multi-Persona 为 0.68–0.72；但 Table 2（p.5）给相应系统的最佳 MedQA 仅 0.60、0.60、0.58，Figure 1/10 的纵轴与点也约在 0.52–0.65。可视 PDF 与解析文本都确认这些 Table 3 数字，故这是**论文内部结果表不一致**，不是文本抽取误差。PDF 未说明 Table 3 是否来自不同子集、不同模型或错误版本，基线强弱应优先标注此未决冲突。定位：PDF p.3 Figure 1；p.5 Table 2；p.12 Figure 10；p.17–18 Table 3。

## 4. 模型、token、API、prompt 与 oracle 差异

- [AUTHOR_FACT] 主实验使用 `3.5-turbo`；作者称其为 GPT-3，并以性能/成本平衡作为选择理由。GPT-4 与 Mixtral 8x7B 只在 MedQA 上另行评估。定位：PDF p.3，§3 “with the 3.5-turbo engine”；p.7–9 “Evaluating using other APIs”、Figures 8–9。
- [AUTHOR_FACT] 比较中同时变化了代理数、轮数、reasoning/aggregation 次数、agent prompt、round summarization、sampling 参数及系统特定超参数；Figure 1 和 Appendix A.1 还显示成本、时间、token 与 API 调用数差异。定位：PDF p.3–4，§3 Results；p.12–15，Figures 10–16；p.17–18，Table 3。
- [AUTHOR_FACT] few-shot CoT 的医疗示例与解释来自临床专家；完整 Medprompt 的 kNN 部分被删除。定位：PDF p.2 脚注 1及 Medprompt 段。
- [READER_INTERPRETATION] 因此准确率差异可能来自协议、prompt 内容、few-shot 知识、采样参数、上下文长度、调用预算共同变化；论文展示 trade-off，但没有把各系统严格配成等 token、等 API 调用或等美元预算的单因素实验。Figure 1/10–16 只能显示相关关系，不能消除这些混杂。
- [AUTHOR_FACT] Table 2 选择每个系统在每个数据集上的最高配置；另一个 K-fold 分析用同类别两个 held-out 数据集的平均准确率选择配置后再评目标数据集。定位：PDF p.4–5 “best-performing configurations”；p.5 “Is MAD simply sensitive to hyperparameters?”；Figure 3。
- [READER_INTERPRETATION] Table 2 的“逐数据集最好配置”具有事后 oracle 选择性质，不等同于新数据集上可用的预注册配置；Figure 3 的跨数据集选择更接近外推测试，但论文没有给折叠、候选空间、方差或显著性细节。
- [AUTHOR_FACT] agreement 强度先在 376 道 USMLE/MedQA 子集上扫描，再把 90% prompt 用于 full MedQA；作者报告 Multi-Persona 在子集上约提升 15%、SoM 约提升 5%，ChatEval 几乎不受影响。定位：PDF p.6–7，Figures 5–6 及其前后正文。
- [OPEN_QUESTION] 该 376 题子集是否包含在后续 full MedQA 评分中、90% 是否因查看该子集结果而选择、以及是否有独立测试集，PDF 没有交代；若重叠，则 full-set 结果不是完全独立于调参的评估。
- [AUTHOR_FACT] GPT-3.5 上选出的 agreement 设置可迁移到 GPT-4，但不能良好迁移到 Mixtral 8x7B。定位：PDF p.9，Figure 9 后正文。
- [OPEN_QUESTION] 论文未报告随机种子级重复、置信区间或显著性检验；Figure 2 等箱线图是**跨配置**的性能分布，不应自动当作重复运行的不确定性。定位：PDF p.5，Figure 2；p.12–15，Figures 10–16。
- [OPEN_QUESTION] API 的精确模型快照、价格表日期、并发/重试策略与解析失败处理细节未完整给出；作者自己承认模型更新和推理时延可变。定位：PDF p.9，Limitations；p.19，Appendix A.3–A.4。

## 5. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 原始实现下，MAD 不可靠地优于 Medprompt、Self-Consistency 等非辩论/集成方法；它通常需要更多 API 调用、tokens 与成本。定位：PDF p.1 Abstract；p.4 Results；p.9 Conclusions。
- [AUTHOR_FACT] 增加成本/API 使用并不保证更好结果；性能高度依赖数据集、系统和超参数。定位：PDF p.4 “additional computing does not guarantee better results”；p.5 Figure 3 前后。
- [AUTHOR_FACT] Multi-Persona 的辩论过程平均会比第一代理的初始答案更差；作者归因于 devil 被设计为反驳，即使初始答案正确也会施压改变。定位：PDF p.5–6，Figure 4 与 “even if the initial response was correct”。
- [AUTHOR_FACT] agreement modulation 的方向依赖数据集：MedQA/PubMedQA 偏好高一致，CIAR 呈相反趋势；ChatEval 几乎无法通过同一提示机制调节。定位：PDF p.6–7，Figures 5–6。
- [AUTHOR_FACT] 主实验受 API 调用时延波动、不可预见模型更新、财务与时间成本限制；作者建议未来用开源模型和自有基础设施扩展。定位：PDF p.9，Limitations。
- [AUTHOR_FACT] 医疗问答可能产生错误且过度自信的预测，造成误导或误诊风险。定位：PDF p.9，Impact Statement。
- [READER_INTERPRETATION] 明确未覆盖或覆盖很弱的边界包括：生成式开放回答而非多选字母、非问答型协作任务、长期多轮代理、外部工具/检索、对抗代理、安全攻击、不同开源模型族，以及 GPT-4/Mixtral 上除 MedQA 外的数据集。PDF 没有提供这些边界上的证据。
- [OPEN_QUESTION] 正文先称“seven datasets”，又称“three medical and three non-medical datasets”，Figure 3 也写三类非医疗数据；Chess 是否被排除在 K-fold/某些结论之外及原因未说明。定位：PDF p.3–5，§3 与 Figure 3 caption。

## 6. 可抽取的 Operator 与真实可记录的 Failure（仅核源，不生成 Card）

### 可抽取的机制/Operator 内容

- [AUTHOR_FACT] **Agreement-intensity prompt operator**：在辩论开始前向代理 system prompt 加入目标同意比例 X；在 Multi-Persona 中施加给 devil。定位：PDF p.6–7，Figures 5–6。
- [AUTHOR_FACT] **答案共享/历史共享 operator**：把其他代理答案或全部先前历史追加给下一轮代理。定位：PDF p.2，SoM/ChatEval；p.20，SoM MAD suffix。
- [AUTHOR_FACT] **摘要压缩 operator**：每轮先由 summarizer 压缩讨论，再覆盖后续代理看到的历史。定位：PDF p.2，ChatEval；p.20，CE MAD/SoM MAD。
- [AUTHOR_FACT] **judge/early-stop operator**：judge 判断是否已有明确偏好；若有则提前结束，否则继续到下一轮，最后以 JSON/字母输出。定位：PDF p.2 Multi-Persona；p.20–21，`judge_system_message`、`UNIVERSAL MODE`、`FINAL MODE`。
- [AUTHOR_FACT] **independent sampling + aggregation operator**：Self-Consistency 对独立 reasoning paths 多数表决；ER 再把多个 student reasonings 交给聚合调用。定位：PDF p.2，Self-Consistency/ER；p.20，ER MAD。

### 真实可记录的 Failure

- [AUTHOR_FACT] **反驳代理破坏正确初答**：Multi-Persona 从第一轮到最后/最终答案的相对准确率下降，作者将其与 devil 强制反对联系起来。定位：PDF p.5–6，Figure 4。
- [AUTHOR_FACT] **协议对超参数/数据集敏感，跨数据集最优配置不稳定**：Figure 3 显示多种协议在新数据集上不保证超过单代理。定位：PDF p.5，Figure 3。
- [AUTHOR_FACT] **同一 agreement 操作不可普遍迁移**：ChatEval 几乎不响应，CIAR 的方向相反，GPT-3.5 的设置迁移到 Mixtral 失败。定位：PDF p.6–9，Figures 5–6、9。
- [AUTHOR_FACT] **提示词自身含算术校验错误**：SPP 示例最终式 `6 * (1 + 1) + 12 = 24` 是正确的，但示例中的“Expert/Math Expert”验证文字写成 `12 + 12 = 12`。这段错误被直接放入 agent prompt。定位：PDF p.21–22，Appendix A.6 `SPP ORIGINAL`/`SPP EXPERT`，短定位文本 “12 + 12 = 12”。
- [AUTHOR_FACT] 作者定义并记录 incorrectly parsed answer、messages removed due to prompt limit、bullied by other 等指标，但本 PDF 仅给指标定义，没有给这些失败的数值结果。定位：PDF p.19，Appendix A.3–A.4。
- [READER_INTERPRETATION] 因此“解析失败”“上下文截断”“被其他代理带偏”可作为待核验失败维度；除 Figure 4 所示答案退化外，不能从本 PDF 把它们写成已量化发生的 Failure。

## 7. 关键判断定位索引

| 判断 | PDF 页 | 章节/图表 | 短定位文本 |
|---|---:|---|---|
| MAD 是推理时上下文交互 | 2 | §2 | “in-context prompting” |
| agreement intensity 定义 | 6 | §3 | “agree ... X% of the time” |
| 七数据集与输入范围 | 3–5 | §3；Table 2 | “seven datasets” |
| 主基准最好值 | 5 | Table 2 | “Best performance achieved” |
| debate 可能降低表现 | 5–6 | Figure 4 | “leads to a decrease” |
| agreement 的数据集依赖 | 6–7 | Figures 5–6 | “CIAR follows a reverse pattern” |
| GPT-4/Mixtral 迁移 | 7–9 | Figures 8–9 | “does not extend well to Mixtral” |
| 成本/模型更新限制 | 9 | Limitations | “unforeseen model updates” |
| 主表与附录数值冲突 | 3, 5, 12, 17–18 | Figure 1；Table 2；Figure 10；Table 3 | `0.60` vs `0.76` |
| 解析/截断指标 | 19 | Appendix A.3–A.4 | “Incorrectly Parsed” / “Messages Removed” |
| 完整辩论与代理提示 | 20–23 | Appendix A.5–A.6 | `MP MAD`、`SPP` |
| SPP prompt 算术错误 | 21–22 | Appendix A.6 | “12 + 12 = 12” |

## 8. 逐页可视核对与解析冲突

- p.1：标题、Abstract、§1；双栏文本顺序正常。
- p.2：§2 各协议与脚注；解析文本与可视内容一致。
- p.3：Table 1、Figure 1、§3 开始；checkmark 与图例只能靠可视层确认，未见缺图。
- p.4：数据集列表与 Results；双栏续接正常。
- p.5：Table 2、Figure 2、K-fold/辩论效用；表格值经可视核对。
- p.6：Figures 3–4、agreement modulation；公式符号与百分比可见。
- p.7：Figures 5–6、debating behaviour/GPT-4 段；曲线与图注完整。
- p.8：Figures 7–8；雷达图和 GPT-4 基准完整。
- p.9：Figure 9、Conclusions、Limitations、Impact；双栏正常。
- p.10–11：References；无正文结果遗漏。
- p.12–15：Appendix A.1、Figures 10–16；所有数据集的 time/token/cost/accuracy 图均可见。
- p.16：Appendix A.2 导言；页面大部留白是原始排版，不是抽取缺失。
- p.17–18：Table 3 横向旋转跨两页；解析文本能读出行列内容，可视层确认主要数值。它与 Table 2/Figure 1/10 的不一致属于源文内部冲突。
- p.19：Appendix A.3–A.4 指标定义表；解析与可视一致。
- p.20：Appendix A.5 debate prompts；等宽小字可见，解析顺序正常。
- p.21–23：Appendix A.6 agent prompts；长 SPP 示例跨三页，视觉页序与解析文本一致；算术错误确实存在于可视 PDF。
- [AUTHOR_FACT] 未发现解析文本把正文页遗漏、重排到错误页或与可视 PDF 产生实质性文字冲突。
- [READER_INTERPRETATION] 图中单个散点的精确数值不能由文本抽取可靠恢复，因此本报告只引用正文/Table 2/Table 3 明示数字，不从散点位置臆造精确值。
- [OPEN_QUESTION] Table 3 的部分版面很密、p.17–18 横向旋转，但放大后仍确认核心冲突数字；其来源/版本差异只能由作者代码或勘误解释，本轮禁止联网，无法继续核验。

## 9. 本轮边界声明

本报告只回答统一核源问题，不生成 Card，不与其他读次合并，不评价 Candidate、novelty 或科研价值，也不把作者推测（如 CIAR 因 counter-intuitive 而受益于 disagreement）升级为已证实因果结论。
