# P029 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p029-a1/invocation.md`；只核读 invocation、统一问题及指定的 42 页 PDF，未读取首读、Cards、其他报告或 blind query，未联网。
- [AUTHOR_FACT] 正文和全部附录逐页检查，重点核对 synthetic tasks、failure attribution、k 消融、人类验证和案例。
- [OPEN_QUESTION] 使用 PDF 文本层核读；表格与案例可连续提取，未逐页位图渲染，曲线仅按作者文字和轴表述理解。

## 2. 论文改变的计算/评估对象

- [AUTHOR_FACT] MemFail 不是新 memory architecture，而是把 agent memory 分解为 summarization、storage、retrieval、reasoning 阶段，并通过可观测中间状态定位失败（方法，物理页 3–6）。
- [AUTHOR_FACT] 数据含 Conditional Easy/Hard、Coexisting、Persona、Long-Hop 五类 synthetic memory tasks；评测四种 memory systems，并改变 retrieval `k∈{4,8,12,16,20}`（数据/实验，物理页 5–9）。
- [READER_INTERPRETATION] 核心 Operator 是 diagnostic attribution：比较原始事实、存储表示、检索结果和最终回答，判断信息在哪一阶段丢失；它是 Failure 知识的来源，不是 implement 本身。

## 3. 输入、输出与 judge 信息

- [AUTHOR_FACT] judge 能看到原始/全部 memory、retrieved memories 和模型答案，据此输出错误类别；同一个 GPT-5-mini 用作各系统 test-taker 与 grader（设置，物理页 8–10）。
- [AUTHOR_FACT] 数据由 GPT 系列模型生成，作者声称人工核验全部 dataset entries；另对 100 个样本做人工 judge 验证，answer correctness 约 98%，error-type agreement 约 98.4%（验证节/附录）。
- [READER_INTERPRETATION] judge 拥有部署时 agent 没有的全局证据，因此 attribution 可作离线诊断，不应转述为在线可观测 failure detector。

## 4. 结果与最强基线关系

- [AUTHOR_FACT] 不同架构在任务族上呈现明显不同 failure profile；提高 k 或更换模型不能一致消除错误，且没有单一系统在所有任务占优（主图/分析，物理页 9–13）。
- [AUTHOR_FACT] StructMem 在部分 causal/conditional 任务较强、在 coexisting 类较弱；Mem0 呈现不同取舍（主结果与案例）。
- [READER_INTERPRETATION] 结果支持“memory architecture 的错误并非统一 retrieval miss，且增加 retrieval 数量不是通用修复”；不能据此形成单一架构总排名。

## 5. 构造性边界与潜在偏差

- [AUTHOR_FACT] benchmark 是合成的、任务分布受控，主要研究显式 memory APIs；作者未覆盖参数化/隐式 memory（limitations，物理页 13–14）。
- [AUTHOR_FACT] 一个案例中，“watermelon seeds grow in stomach”之类的用户断言若未被忠实保存在 memory，会被归为 storage failure，即使 test model 以世界知识纠正了断言（案例/附录）。
- [READER_INTERPRETATION] 该 rubric 测的是对给定 user memory 的忠实保持，不是现实世界事实正确性或安全性；在部署准确性语境中，某些“失败”可能反而是合理纠错。
- [OPEN_QUESTION] test-taker 与 grader 同源模型可能共享判断偏差；人类验证规模不足以排除所有五类任务和所有系统上的细分偏差。
- [OPEN_QUESTION] 未报告端到端 latency、dollar cost 或真实长程对话分布上的外部效度。

## 6. 负向结果与可抽取资产

- [READER_INTERPRETATION] Failure 候选：`More retrieved memories do not monotonically repair memory reasoning`；`Flat and structured stores trade off different failure families`；`Faithful-memory evaluation can conflict with world-truth correction`。
- [READER_INTERPRETATION] Evaluation Operator 候选：`Stage-localized memory failure attribution using source/store/retrieval/answer views`。
- [READER_INTERPRETATION] 窄 Claim：在五个合成任务与四个显式 memory system 上，作者观察到 architecture-specific failure profiles，且 k 扩大和模型替换都不是统一解法。
- [READER_INTERPRETATION] 不支持：分类法覆盖真实部署全部 memory failure；failure labels 等同于最终回答错误原因的因果证明；忠实用户记忆总比世界知识纠错更好。

## 7. 独立二读建议

`ACCEPT_WITH_NARROWING`。该文最适合作为 Failure taxonomy 与评测机制来源，而不是成功方法来源；正式 Card 必须突出 synthetic、oracle-view judge 和“忠实性不等于事实正确性”的边界。本建议仅供主 Codex reconciliation。
