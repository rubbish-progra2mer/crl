# P044 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P044/read_2_attempts/r2-20260719-p044-a1/invocation.md`
- 论文：*DEER: A Comprehensive and Reliable Benchmark for Deep-Research Expert Reports*
- PDF SHA-256：`bb262ad8999adb3feb46f3373db45815f31f16b714f02fe732c47625810cf42a`
- [AUTHOR_FACT] 已逐页读取全部 45 个物理页。

## 1. 改变的评测计算

- [AUTHOR_FACT] DEER 以 HLE 高难问题为种子，由领域专家重写成 50 个任务、13 个领域；5,842 条真实查询日志主要用于确定主题分布。预筛会排除“过难、无法由 LLM 评估”的候选。（物理页 3–5，Task construction）
- [AUTHOR_FACT] 评测 taxonomy 含 7 个维度、25 个子维度，由 80 份标准、20 个领域归纳；包括 101 个固定 rubric，并为每题加入领域专家撰写、交叉复核的 Expert Evaluation Guidance（EG）。（物理页 4–6，Evaluation taxonomy）
- [AUTHOR_FACT] 报告质量维度由 GPT-5.2 评判，信息验证由 GPT-5-mini 执行，估计成本每报告约 0.5–1 美元。（物理页 5–6，Evaluator setup）

## 2. 引用/主张流程的 I/O 边界

- [AUTHOR_FACT] 主张分为 A–F：A 显式引用，B/C 依赖同段/前文回溯，D recap，E 不需引用，F 来源未知；外部事实核验只直接处理 A–C。Evidence Coverage 定义为 |A,B,C|/全部 claims。（物理页 4–5 与方法附录；短定位：“A–F”“Evidence Coverage”）
- [READER_INTERPRETATION] F 会降低覆盖率，但不会进入外部支撑判定；因此“未引用且来源未知”的事实不能由 claim verification 直接判假。把该指标称为完整事实正确率会过度解释。
- [AUTHOR_FACT] 约 62.5% 主张有显式引用，语义回溯后 evidence coverage 约 91%；这支持回溯能找关联引用，不等于 91% 的主张均被正确支撑。（物理页 7–9，Citation analysis）

## 3. 验证规模与主要结果

- [AUTHOR_FACT] claim extraction 的人工金标仅来自 2 份报告、728 个 claims；claim verification 人评为 100 个 claims，其中 82 个 supported、仅 5 个 not-supported，另构造了对抗错误主张。两位专家 kappa 约 0.80。（物理页 8–10，Evaluator validation）
- [AUTHOR_FACT] 所选 verification 配置为 GPT-5-mini、batch 20、low effort、OpenAI embedding top-2；原始集 accuracy 约 77.01、F1 约 87.25，对抗集约 88.46/86.79，成本约每千主张 0.95 美元。（同上，验证表）
- [AUTHOR_FACT] rubric 人类相关验证只覆盖 45 份报告、15 题、每题 3 报告、2 位专家、共 90 ratings。固定细粒度 rubric 单独使用反而降低相关/可靠性，加入 EG 后 Pearson 约 .734、Spearman .707、pairwise agreement .840；LLM evaluator alpha 约 .55。（物理页 9–11）
- [READER_INTERPRETATION] EG 的正增益是可用 changed-evaluation 证据；但 tiny gold set、类别不平衡与较低 alpha 限制了“可靠自动裁判”强度。

## 4. 系统比较、预算与替代解释

- [AUTHOR_FACT] 主表比较 16 个模型/系统，覆盖 fast、thinking、search、deep research 等异质模式；OpenAI Deep Research overall 约 6.50，GPT-5.2 think+search mean 约 6.62。搜索通常提高信息维度，但可能降低报告质量；thinking 在无搜索时也常提高非信息维度。（物理页 6，表 2；物理页 11–13 分析）
- [READER_INTERPRETATION] 系统可用搜索、token、延迟与内部迭代不等，表 2 是产品/配置比较而非同预算架构消融；不能把 deep/search 的差异直接归因为某个机制。
- [AUTHOR_FACT] 800 份报告整体长度相关很弱（Pearson 约 -0.02、Spearman 约 0.10），每题也大多接近零。（物理页 12–13，Length analysis）
- [READER_INTERPRETATION] 数量指标的阶梯阈值和除数（如 information 15、citation 10、references 4）是设计选择；总体等权平均同样是规范性选择，排名需保留维度分解。

## 5. 限制、Operator 与 Failure

- [AUTHOR_FACT] 作者明示限制：LLM judge 仍可能偏置，当前只评文本报告，量化指标应与人类评审互补。（物理页 13–14，Limitations）
- [READER_INTERPRETATION] Operator 候选：固定 taxonomy + 题目专属 EG；claim 类型化、语义回溯、再对 A–C 做网页支撑核验。
- [READER_INTERPRETATION] Failure 候选：F 类主张逃逸直接核验；只看显式引用低估关联；固定 rubric 细化后反而降低与人评一致性；任务预筛排除“LLM 难评”造成选择偏差。
- [OPEN_QUESTION] 原文没有在独立、更大且类别平衡的 claim 金标集上验证 A–F 分类、回溯与外部支撑判定，也没有证明数量阈值/总体等权聚合对排名稳健。
- [READER_INTERPRETATION] 建议保留为细粒度评测/claim 回溯算子，同时显著标注 F 不直接验证、人工金标很小、任务选择偏差与系统预算异质性。

## 6. 可视核验

- [AUTHOR_FACT] 已核对物理页 6 表 2，主要总体分与模式标签和解析文本一致；未见实质冲突。
