# P042 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P042/read_2_attempts/r2-20260719-p042-a1/invocation.md`
- 论文：*LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild*
- PDF SHA-256：`579b9728b76cfd242e9c94d9ff2985e196bbc72b5a741030e4f308ede04a4f69`
- [AUTHOR_FACT] 已读取 48 个物理页全文。

## 1. 改变的评测计算

- [AUTHOR_FACT] 论文构建 100 个专家策划、动态、多领域的深度研究任务和任务专属 checklist，累计策划工作量超过 1,500 小时。（物理页 3–5，Benchmark construction）
- [AUTHOR_FACT] DeepEval 将报告拆成六类协议：presentation 用 checklist；consistency 逐点寻找内部矛盾；coverage 按任务 checklist；depth 以与参考系统的两次换位 pairwise 比较；citation traceability 检查陈述到引用的关联；citation accuracy 则按 URL 聚合主张、抓取网页并沿 rubric tree 判断 E1 不可访问、E2 不相关、E3 无支撑。（物理页 5–8，Evaluation framework）
- [READER_INTERPRETATION] 真正改动是“按指标定制的评审程序”，不是一个统一 holistic judge；可复用部分是协议分解和可定位错误类型。

## 2. 输入、输出、基线与主结果

- [AUTHOR_FACT] 输入为系统生成的研究报告、任务及 checklist/网页；输出为六维分数和平均汇总。评审主模型为 Gemini 2.5 Pro 与 GPT-5，取两者平均。（物理页 7–9，Evaluator setup）
- [AUTHOR_FACT] 评测 17 个系统，并主动放宽各系统配置和输出长度（GPT-5 最高 128k），低质量/失败运行可重试；开源 DeerFlow+/Open Deep Research 使用 GPT-5 backbone。（物理页 8–9，Systems/configuration）
- [AUTHOR_FACT] 表 1 中 Open Deep Research 平均分约 73.6，为最高总体均值；GPT-5 约 72.7。多代理家族均值约 69.5，Web-agent 家族约 62.8，但不同维度领先者不同。（物理页 9，表 1）
- [AUTHOR_FACT] Depth 是相对 Open Deep Research 的胜率且排除 ties，不是绝对深度分；DeerFlow+、Gemini Deep Research 等在该相对指标上可超过参考。（物理页 9–10，Depth analysis）

## 3. 预算、judge/oracle 与泄漏风险

- [READER_INTERPRETATION] 各系统搜索次数、token、重试、并行度和专有内部预算不等，且部分“开源系统”共享 GPT-5 backbone；表 1 更接近端到端产品快照，不是同计算预算算法对照，不能把 multi-agent 家族均值差异直接解释为架构因果效应。
- [AUTHOR_FACT] citation error 的细分统计只在 market 与 wide-search 子集上做，不覆盖全部 100 题；多个领先系统仍有大量 E3 无支撑错误。（物理页 10–12，Citation error analysis）
- [READER_INTERPRETATION] 任务动态性降低静态答案泄漏，但 LLM judge、搜索网页快照和重试政策本身形成时间与模型依赖；排行榜需要版本化解释。

## 4. 人类对齐证据的边界

- [AUTHOR_FACT] 人类先独立判断，再看到两个 judge 结论及理由并选择偏好；论文报告“偏好 Gemini 或 GPT-5 任一方”的 union 比例，coverage/consistency 等可达约 98.3%/100%，不是盲态的人—模型逐项一致率。（物理页 11–13，Human evaluation）
- [AUTHOR_FACT] Depth 的人评仅 40 个经一致/不一致分层抽样案例；citation accuracy 约 200 对，union 偏好约 87.1%；consistency 在 128 个被指出问题上约 82% 被人接受，traceability 约 85.9%。（同上）
- [READER_INTERPRETATION] 这种“看过理由后的偏好”能评估理由说服力/可接受性，但会产生锚定，不能证明独立标注精度；union 指标还会天然高于单 judge。

## 5. 限制、Operator 与 Failure

- [READER_INTERPRETATION] Operator 候选：任务 checklist 驱动的 coverage/presentation；引用按 URL 分组后的可访问性—相关性—支撑性分级；pairwise depth 必须明确参考对象并换位。
- [READER_INTERPRETATION] Failure 候选：总体均值掩盖维度差异；引用存在却不支撑主张（E3）；同一模型 judge/系统或不等预算造成排名混杂；人类偏好 union 被误读为独立一致率。
- [OPEN_QUESTION] DeerFlow+ 同时改变 context manager、压缩、重试与行内引用验证，但没有覆盖所有组件的独立数值消融，无法归因单一机制。（物理页 14 以后，系统附录）
- [READER_INTERPRETATION] 建议保留为评测算子和失败类型证据；系统能力排名必须带“不等预算、LLM judge、动态快照”限定。

## 6. 可视核验

- [AUTHOR_FACT] 已核对物理页 9 表 1，列值与抽取文本一致；未发现可视表格与解析文本实质冲突。

