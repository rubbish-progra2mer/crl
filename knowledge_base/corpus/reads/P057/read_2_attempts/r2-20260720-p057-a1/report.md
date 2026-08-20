# P057 独立二读报告

## Provenance

- Attempt：`r2-20260720-p057-a1`
- Invocation：`knowledge_base/corpus/reads/P057/read_2_attempts/r2-20260720-p057-a1/invocation.md`
- 论文：Hu, Lu, Clune, *Automated Design of Agentic Systems*，ICLR 2025，arXiv:2408.08435。
- PDF：`knowledge_base/staging/plan05_sat_a1/P057_adas.pdf`
- PDF SHA-256：`32eb1c1a6888e35fae0f618e33c58698b54d9c49bc063fef91ee591719fca376`（实测与 invocation 匹配）。
- Prompt SHA-256：`ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`（实测与 invocation 匹配）。
- 物理页数：34；已按物理页 1–34 顺序完整读取。
- 线程 provenance：`reused independent reader thread due platform thread cap`。本线程此前未接触 P057，但线程本身并非全新，因此不声称 fresh thread。
- Canonical task/thread：`/root/plan05_card_source_audit_e`。
- Actual model/version：`unknown`（当前上下文不可观察精确模型版本）。
- 隔离：`procedural_blinding`，不是技术 file allowlist。

## 1. 方法改变了哪一步计算

- [AUTHOR_FACT] ADAS 被形式化为“search algorithm 在 agentic-system search space 中优化 evaluation function”。Meta Agent Search 选择代码作为表示空间，由 meta agent 生成整个 agent 的 Python `forward` 函数，而不是只优化单条 prompt。定位：物理 p3–p4，§2、Fig. 2；短定位 `agents defined by code`、`programming ever better ones in code`。
- [AUTHOR_FACT] 外层搜索循环为：可选地用 COT/Self-Refine 等基线初始化 archive；meta agent 读取 archive 后提出设计说明并生成代码；做两轮 novelty/correctness self-reflection；在目标域 validation data 上评估；仅当运行报错时最多进行五轮错误驱动修复；把 agent 与评估指标加入 archive，继续迭代。定位：p4–p5，§3；p21–p23 prompts；p33，Algorithm 1。
- [READER_INTERPRETATION] 真正 changed computation 是“以验证集分数为目标、以累计 archive 为上下文的外层代码搜索”。论文发现的 peer review、divide-and-conquer、feedback ensemble 等是搜索结果，不应与 Meta Agent Search 本身混成同一个 Operator。
- [READER_INTERPRETATION] “Turing complete 因而可发现任意 agentic system”只说明表示能力上限，不证明有限 prompt、有限迭代和当前基础框架能有效到达任意设计。定位：p2–p4；p11 明示从零编程所有组件在实践中低效。

## 2. 输入、输出、信息边界与干预时点

- [AUTHOR_FACT] meta agent 的主输入包含目标域简述、少于 100 行的 framework code、输出格式/常见错误提示，以及随迭代更新的 discovered-agent archive；主输出为设计 reasoning、名字和完整 `forward()` Python 代码。定位：p4，§3；p21–p24，Appendix B/C。
- [AUTHOR_FACT] archive 保存先前 agent 与 evaluation metrics，并在后续迭代进入 meta-agent prompt。评估函数使用 validation performance；论文没有让 meta agent 读取成功/失败执行日志，除非候选代码发生 runtime error。定位：p3–p5；p21 主 prompt；p23 runtime-error prompt；p11 `simply evaluate... numerical performance results`。
- [AUTHOR_FACT] 干预发生在部署/回答任务之前的 agent-design 外循环；被发现的 agent 在执行时接收 `taskInfo`，再按生成的 workflow 调用 FM 模块或工具。定位：p4 framework/`forward`；p23–p25 Code 1/2。
- [AUTHOR_FACT] ARC 中 agent 被要求生成转换代码，并获得两个工具：在示例 grids 上测试代码、把代码应用到 test grid 得到输出；accuracy 是预测输出与 reference 的 exact match。定位：p6，§4.1；p25–p26，Appendix D。
- [READER_INTERPRETATION] ARC 的示例执行反馈是题内 demonstrations 上的可用工具反馈，不等同于直接读取 test answer；但它令 ARC agent 的信息/工具边界明显不同于纯文本 QA，转移结论不能忽略这种差异。
- [OPEN_QUESTION] 论文未精确列出 archive 中传给 meta agent 的每个字段、是否包含完整历史代码/全部 validation 分数，以及 archive 超长时是否截断；无法从原文核定上下文增长和信息压缩策略。

## 3. 最强基线与最近组合基线

- [AUTHOR_FACT] 手工 agent 基线为 COT、COT-SC、Self-Refine、LLM-Debate、Quality-Diversity；reasoning/problem-solving 另加 Step-back Abstraction 与 Role Assignment。论文把“state-of-the-art”限定为代表重要设计模式，不是声称其数值仍为开放世界最强。定位：p6，§4.1 Baselines；p30，Appendix F。
- [AUTHOR_FACT] 唯一直接实验的自动设计基线是 OPRO prompt optimization。定位：p7，§4.2 Baselines/Table 1。
- [READER_INTERPRETATION] 最近的单组件自动基线是 OPRO；最近的 archive/diversity 机制对照是 Quality-Diversity，但后者在实验中是回答生成/ensemble 基线，不是同等代码级 agent-design search。
- [AUTHOR_FACT] 论文 Related Work 明确列出 GPTSwarm、DSPy、Trace、AgentOptimizer、AutoFlow、Agent Symbolic Learning 等更接近 workflow/tool/多组件自动优化的方法，但没有进行数值比较。定位：p9–p10，§5 `Existing Attempts to ADAS`。
- [READER_INTERPRETATION] 因而“胜过最近组合基线”的证据不足；当前强结论只能是优于作者实现的手工基线与 OPRO，而不能扩写成优于当时所有自动 workflow/agent 优化系统。

## 4. 公平性、模型、预算、oracle 与泄漏边界

### 4.1 公平性与计算成本

- [AUTHOR_FACT] 搜索 meta agent 使用 `gpt-4o-2024-05-13`（正文简称 GPT-4）；候选 agent 与基线执行使用 `gpt-3.5-turbo-0125`。ARC 搜索 25 iterations，其他四域各 30 iterations。定位：p6–p7；p26、p29。
- [AUTHOR_FACT] 作者称所有 baseline 均在同一 framework 中实现。各 baseline 本身调用预算不同：COT-SC 采样 5 个答案，Self-Refine 最多 5 次 refinement，LLM-Debate 两轮，Quality-Diversity 三轮。定位：p6；p30。
- [AUTHOR_FACT] 一个 ARC 搜索+评估 run 约 500 USD，一个 reasoning/problem-solving 域约 300 USD，主要成本来自大量 GPT-3.5 evaluation calls。定位：p34，Appendix J。
- [READER_INTERPRETATION] “同一 framework/执行模型”不等于 matched budget。发现过程额外使用 GPT-4o、25/30 轮候选搜索、两轮设计反思和错误修复；最终 discovered agents 也可能比基线调用更多 FM。例如 ARC 最佳 agent 有 5 个初始候选、逐候选 human/expert feedback、最多 3 次 refinement 与最终 ensemble。定位：p27–p28，Code 3。论文未按 token、FM calls、latency 或美元成本匹配或归一化，因此性能差不能纯归因于 architecture。
- [OPEN_QUESTION] OPRO 的优化迭代、token/API 预算与 Meta Agent Search 是否匹配，原文没有给出足以复算的预算表。
- [OPEN_QUESTION] 表中置信区间主要反映题目/采样层面的不确定性；没有看到对完整 search run 使用多个随机种子重复并报告 search-level variance。一次 search 找到的 best agent 可能带来选择方差。

### 4.2 validation/test 与选择泄漏

- [AUTHOR_FACT] ARC 使用 20-question validation set 搜索、60-question held-out test set测试；作者称“evaluate all discovered agents on the held-out test set”。定位：p6，§4.1 Setup。
- [AUTHOR_FACT] 跨模型 ARC transfer 明确选择“with the best test accuracy evaluated with GPT-3.5”的 top 3 agents，再转到 Claude-Haiku、GPT-4、Claude-Sonnet。定位：p8，§4.3。
- [READER_INTERPRETATION] 这形成 test-informed source selection：ARC test set 不再只是一次性最终评估，因为它被用于筛选 transfer 的 top-3 source architectures。该步骤不能表述为完全无 test selection 的 held-out transfer。
- [OPEN_QUESTION] MGSM 的 top-3 transfer agents究竟按 validation 还是 MGSM test performance 选择，正文只写 `top 3 agents from MGSM`，未明确。
- [AUTHOR_FACT] 各域 meta prompt 含一个示例问题，但答案标注为 `[Not Given]`；ARC prompt 含 demonstrations，这是 ARC 题目定义的一部分。定位：p26–p30。
- [OPEN_QUESTION] 论文没有实证排除基础模型对 ARC/MGSM/MMLU/GPQA/DROP 测试题或已有 agent 论文代码的预训练污染；代码空间搜索 prompt 还主动允许从 academic literature 获得 inspiration。定位：p21。
- [READER_INTERPRETATION] p29–p30 的 GPQA 示例说明存在内部文本不一致：题干 lifetimes 为 `10^-9`/`10^-8`，解释改成 `10^-9`/`10^-11`；标注答案为 `10^-7 eV`，解释末尾却写 `10^-4 eV`。这些答案/解释标为 `[Not provided]`，所以不能直接断言泄漏给 meta agent，但它是论文 prompt-documentation 的真实质量缺口。

## 5. 结果、负结果与 transfer 边界

- [AUTHOR_FACT] 独立按域搜索时，Table 1 报告 DROP 79.4 F1、MGSM 53.4%、MMLU 69.6%、GPQA 34.6%；相对最佳手工基线，DROP 与 MGSM 的绝对提升分别为 13.6 与 14.4。定位：p7，Table 1。
- [READER_INTERPRETATION] MMLU/GPQA 的领先幅度较小且 95% CI 与强对照重叠；论文表注也把 median 落入最佳 treatment 95% CI 的条目共同加粗。因此不能把四域都描述成同等强度的显著优势。
- [AUTHOR_FACT] MGSM top agents 迁移到 GSM8K/GSM-Hard 时，最佳 transferred agent 为 69.5/31.2，对应作者所报相对手工基线的 25.9/13.2 个百分点提升。定位：p8，Table 2；p20，Table 4。
- [AUTHOR_FACT] 非数学 transfer 并非逐 agent、逐域都优于手工基线：Table 5 中三名 math agents 的 Science 中位数 28.6/28.7/29.9，低于 Self-Refine 31.6；MMLU 中 62.4 和 64.8 也低于多个手工基线，仅 67.0 的 agent 中位数领先。定位：p20，Table 5。
- [READER_INTERPRETATION] 因此“agents ... still outperform baselines”只能解释为 top-3 集合中存在在目标域领先的 architecture，不能解释为每个 transferred agent 都一致领先；Science 最多是 CI 意义上的“match”，不是中位数胜出。
- [AUTHOR_FACT] ARC 跨模型 Table 3 也不是每个 transferred agent 都领先：Structured Feedback agent 在 Claude-Haiku 为 5.0，低于 Self-Refine 6.3；在 Claude-Sonnet 为 38.7，低于 Self-Refine 39.3。top-3 集合中的最佳 agent 在每个目标模型上领先。定位：p9，Table 3。
- [READER_INTERPRETATION] 若在每个目标模型/域事后选择 top-3 中表现最好的不同 architecture，会引入 target-side oracle selection；论文没有给出预先固定单一 transferable agent 的统一比较。
- [AUTHOR_FACT] 空 archive 初始化仍超过表中手工基线，但初始化并非总有益：Math 中 empty initialization 为 67.5，显著高于 seeded search 的 53.4；其他三域 seeded 更好。定位：p33–p34，Appendix I/Table 6。
- [READER_INTERPRETATION] 这是重要负结果：human-designed seeds 会改变搜索轨迹并可能限制探索，archive 并非单调有益；也说明单次有限迭代搜索对初始化敏感。

## 6. 作者明示限制与未测试边界

- [AUTHOR_FACT] 当前只评估 single-step QA，未测试需要与复杂环境多步交互的真实应用。定位：p11，§6 `More complex domains`。
- [AUTHOR_FACT] 当前只优化 performance，未联合优化 cost、latency、robustness 或 safety。定位：p10，`Multi-objective ADAS`。
- [AUTHOR_FACT] 当前 evaluation 只给 numerical performance，既昂贵又遗漏执行日志中的成功/失败信息；也未解决主观任务无 ground truth 的评价。定位：p11，`More Intelligent Evaluation Functions`。
- [AUTHOR_FACT] 当前每次搜索只针对一个域，未搜索显式多域 generalist agent。定位：p11，同一段末尾。
- [AUTHOR_FACT] 当前搜索算法较简单，主要追求 interesting new designs；更完整 exploration/exploitation、quality-diversity/open-ended search 留待未来。定位：p11，`Novelty search algorithms`。
- [AUTHOR_FACT] 当前框架未实证搜索 RAG、search engine、不同 FM 选择或多模态工具；这些被列为未来 seed/building blocks。定位：p11，`Seeding ADAS...`。
- [AUTHOR_FACT] 生成代码有破坏风险；作者报告用容器隔离、人工检查与警告缓解。定位：p10，§6 Safety Considerations。
- [READER_INTERPRETATION] “跨不相似域 generalize”仍限于共享 FM API/`taskInfo` 框架下的单步 benchmark；不等于 transfer 到交互式、具身、长期记忆或真实工具环境。

## 7. 可抽取的 Operator 候选

- [READER_INTERPRETATION] **Code-space meta-agent search**：把 agentic workflow 表示为可执行 `forward()` 代码，让 meta FM直接提出并实现下一架构。证据：p3–p4，§2–3；p23–p25 framework。
- [READER_INTERPRETATION] **Archive-conditioned stepping-stone search**：把先前代码/设计和 performance 放入 growing archive，作为后续 proposal 的上下文，而非只保留单一 incumbent。证据：p2 Fig. 1；p4–p5；p21 main prompt；p33 Algorithm 1。
- [READER_INTERPRETATION] **Separated proposal repair**：固定两轮 novelty/implementation reflection；runtime error 时最多五轮 debug/re-evaluate。应与基于性能的搜索更新分开记录，因为当前 agent 不因低分获得逐例语义反馈。证据：p4–p5；p22–p23；p33。
- [READER_INTERPRETATION] **Architecture transfer without re-search** 可作为 evaluation facet，而非独立 method Operator：把 MGSM/ARC top architectures直接换域或换基础 FM执行。证据：p8–p9、p20。

## 8. 可记录的 Failure 候选

- [AUTHOR_FACT] **Scalar-evaluation information loss/cost**：作者明确说只用 numerical performance 昂贵且漏掉运行日志中的 failure/success modes。定位：p11。
- [AUTHOR_FACT] **Initialization can constrain search**：Math empty archive 67.5 高于 seeded 53.4。定位：p34，Table 6。
- [AUTHOR_FACT] **Transfer is not universal per architecture**：Table 3/5 存在 transferred agents 低于手工基线的单元。定位：p9、p20。
- [AUTHOR_FACT] **Knowledge-limited domains show smaller gains**：Science/Multi-task 改善较小；作者把原因解释为基础 FM 知识不足，但该原因本身是 hypothesis。定位：p7 Results and Analysis。
- [READER_INTERPRETATION] **Unmatched-compute confound**：最终 accuracy 同时混合了 workflow 设计与更多 FM calls/token/ensemble/refinement；当前表格不能分离两者。证据边界：p27–p28 Code 3；p30 baseline calls；p34 costs。
- [READER_INTERPRETATION] **Test-informed transfer selection**：ARC 使用 source test accuracy 选择 top-3 transfer architectures。定位：p6、p8。
- [READER_INTERPRETATION] **Reachability gap**：代码空间理论上通用，但当前 <100 行 framework、单一 FM API、有限迭代与单域 scalar validation 未证明可搜索到任意 tool/memory/workflow。定位：p4、p10–p11。
- [READER_INTERPRETATION] **Prompt-documentation inconsistency**：GPQA 示例的 lifetime、答案与解释互相矛盾；因 `[Not provided]` 标记，当前只可记录为文档质量 Failure，不可写成训练/评估标签泄漏事实。定位：p29–p30。
- [AUTHOR_FACT] **附录代码/域标签不一致**：最佳 ARC agent 的 Code 3 第 60 行写成用已实例化的 `refinement_module(...)` 构造 Final Decision Module，而框架构造器是 `FM_Module(...)`；p31 又把 GPQA 称为 Reading Comprehension domain，并在 Code 4 使用未在框架定义的大小写形式 `FM_module`。定位：p24 framework signature；p28 Code 3；p31 Appendix G/Code 4。
- [READER_INTERPRETATION] 若按附录文字逐字执行，Code 3 第 60 行的参数与 `FM_Module.__call__` 签名不匹配，Code 4 的大小写也可能触发未定义名称；因此附录示例代码不能单独视为已验证的可运行 artifact。未读取仓库代码，不能判断开源实现是否已修正。

## 9. 解析文本与可视 PDF

- [AUTHOR_FACT] PyMuPDF 对全部 34 页均抽取到非空文本；图像对象出现在 p2、p3、p5、p26。表 1–6、Algorithm 1、Code 1–6、图注和正文数值均可定位。
- [READER_INTERPRETATION] 双栏抽取在少数页会交错，但本文所有数值判断均回到对应表格行/图注/相邻正文交叉核对，而非依赖交错段落。
- [OPEN_QUESTION] 在“只允许写 report.md、不得生成临时页图”的约束下，本线程没有获得可用的逐页 raster 视觉通道，因此不能声称完成像素级图表核验。当前未发现 parsed text 与 PDF 内嵌文字/图注的实质冲突；涉及 Fig. 3 曲线形状的细粒度判断未作主张。

## 10. 总体二读结论

- [READER_INTERPRETATION] P057 对“meta-agent 在代码空间搜索完整 agent workflow，并用 growing archive 累积 stepping stones”提供了清楚、可执行、可定位的 changed computation。
- [READER_INTERPRETATION] 结果支持“在作者实现、模型和预算下，搜索所得 agent 的准确率/F1 高于所测手工基线与 OPRO”；不支持无条件的“architecture 本身普遍更优”，因为搜索成本和执行调用数未匹配、最近自动 workflow 基线未实验比较、transfer 使用 top-set/可能 target-side 选择，且实证域仍是单步 benchmark。
- [READER_INTERPRETATION] 最值得下游保留的边界是：archive/validation feedback 属于外层设计搜索；runtime-error repair 不是低分样本的语义反馈；跨域/跨模型优势按“top set 中存在赢家”解释；Table 6 的 Math initialization reversal 和 Table 3/5 的负 transfer 单元不能被总体叙述抹去。

## 11. 可观察访问轨迹

1. 复核精确规则文件：工作区根 `AGENTS.md`、`crl_agent_v3/AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`；`paper-ingestion-and-evidence-builder/SKILL.md` 及其直接要求的 `rules.md`、`output_schema.md`、`checklists.md`。
2. 只读任务输入：本 attempt `invocation.md`、`knowledge_base/templates/second_read_prompt.md`、invocation 指定 `P057_adas.pdf`。
3. 对 prompt/PDF 执行 SHA-256，均匹配冻结值；用受支持 `.venv` 的 PyMuPDF 读取 PDF metadata/TOC、物理页 1–34 全文，并逐页统计文本字符数和图像对象数。
4. 未枚举工作区；未读取 read_1、Cards、其他报告、Corpus Report、saturation/retrieval/blind 文件或其他论文读稿；未联网、未调用外部 API。
5. 写入仅通过 `apply_patch` 新建本 attempt 的 `report.md`；未修改其他文件。
