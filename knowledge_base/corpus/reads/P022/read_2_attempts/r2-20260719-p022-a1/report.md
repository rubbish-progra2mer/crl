# P022 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p022-a1/invocation.md`；只核读 invocation、统一问题和指定的 17 页 PDF，未读取任何首读/Card/其他报告，未联网。
- [AUTHOR_FACT] 正文与附录已逐页检查，重点核对方法、K/图密度消融、准确率、延迟与 token 表。
- [OPEN_QUESTION] 核读基于 PDF 文本层，未逐页位图渲染；未发现表格文本错位，但复杂示意图不存在完整视觉交叉核验。

## 2. 方法改变的计算

- [AUTHOR_FACT] MOC 让目标 agent 接收多跳祖先消息，不只接收直接前驱；消息按最短拓扑距离分组，并由远到近输入（方法节，物理页 3–5）。
- [AUTHOR_FACT] 为控制上下文，semantic-topological merging 先用 embedding 找相似消息对，再由 9B distiller 生成 5 个压缩候选并选择语义最接近者；实验主要使用 `K=2`、相似度阈值约 0.45（方法与设置，物理页 4–6）。
- [READER_INTERPRETATION] changed computation 是显式开放 higher-order communication path，并在进入目标 agent 前做语义合并；不是让程序理解科研关系，也不是全局图推理。

## 3. 输入、输出与干预时点

- [AUTHOR_FACT] 输入为固定 DAG 中祖先 agents 的自然语言消息及其拓扑距离；输出是供当前 target agent 推理的分组/合并上下文（物理页 3–5）。
- [AUTHOR_FACT] 干预发生在每个 agent 调用前的消息聚合阶段；实验采用 7-agent 随机 DAG，并考察不同图密度和模型（实验设置，物理页 6–7）。
- [READER_INTERPRETATION] 该算子改变的是协作信息可达性；其效果依赖祖先消息中确有互补证据，以及 distiller 不丢失关键差异。

## 4. 最强基线与结果

- [AUTHOR_FACT] 主要对照包括只用直接父节点消息的 Vanilla、拓扑/语义变体和其他 multi-agent 组织方式；在六个数据集与多种 backbone 上，MOC 报告总体提升，但多数为中小幅增益（Table 1–2，物理页 6–8）。
- [AUTHOR_FACT] `K=2` 整体最稳；`K=3` 在更稠密图中不一致并可能退化（消融，物理页 8–9）。
- [AUTHOR_FACT] SVAMP 在部分高密度设置出现轻微下降（主结果/密度分析，物理页 7–9）。
- [READER_INTERPRETATION] 结果支持“higher-order evidence 在固定 DAG 内有时可补足直接邻居信息”；不支持层数越多越好。

## 5. 成本与公平性

- [AUTHOR_FACT] 论文将目标 agents 的输入 token 报告为较 Vanilla 更少，但该口径不计 consolidation 调用；附录 Table 6 单列了 compression token（物理页 14–15）。
- [AUTHOR_FACT] 例如部分 `K=2` 设置约有 797,192 agent tokens，另需 336,087 compression tokens；`K=3` 的额外 compression token 可达约 870,624。图密度更高时压缩开销进一步上升（Table 6）。
- [AUTHOR_FACT] 延迟分解显示 distillation 占主导，约 80 秒/样本，而 embedding 约 0.25 秒（成本表，物理页 9–10）。
- [READER_INTERPRETATION] “agent 输入更短”不等于“系统总 token/延迟更低”；若把 consolidation 纳入，效率结论需重算。
- [OPEN_QUESTION] 原文没有对不同供应商模型给出统一货币成本，也未给出等 wall-clock 并行配置下的端到端比较。

## 6. 负向结果与边界

- [AUTHOR_FACT] 更深的祖先范围会增加待合并信息，K=3 并不稳定；高图密度下成本更明显（消融与附录）。
- [READER_INTERPRETATION] 可记录 Failure：扩大通信可达性若没有严格预算，会把信息收益转化为隐藏的 distillation 成本；过度合并还可能损失少数但关键的分歧消息。
- [OPEN_QUESTION] 未测试敌对/错误 ancestor 消息、长任务状态持续漂移，以及 distiller 与下游 agent 换模型后的稳健性。

## 7. 可抽取资产

- [READER_INTERPRETATION] Operator 候选：`Topology-aware higher-order message exposure with bounded semantic merging`。
- [READER_INTERPRETATION] Failure 候选：`Target-only token accounting hides consolidation cost`；`Deeper message closure can degrade under dense graphs`。
- [READER_INTERPRETATION] 窄 Claim：固定 7-agent DAG 和论文所测任务上，向 target 暴露合并后的多跳祖先消息可取得小幅但较一致的质量增益。
- [READER_INTERPRETATION] 不支持：MOC 系统级 token/延迟一定低于 Vanilla；更高 K 或更稠密通信普遍更强。

## 8. 独立二读建议

`ACCEPT_WITH_NARROWING`。保留 higher-order communication Operator 和成本型 Failure；正式记录必须将 agent-input token 与 compression/system token 分开。本建议仅供主 Codex reconciliation。
