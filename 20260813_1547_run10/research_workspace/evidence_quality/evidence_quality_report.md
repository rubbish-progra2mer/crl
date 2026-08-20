# Evidence Quality Report — v001

本报告只分级已通过冻结知识库定位到论文正文的片段。当前 Run 没有 `route_failure_registry.json` 或本地 `paper_index.json`；历史准入检查依据为本 Run 的 `literature/route_pruning_log.json`，其中只阻断纯提示反思/统一重试作为方法种子，不阻断下列证据。共享知识库的 Card 排名不参与分级。

## EQ-001

- `evidence_id`: `ev-p074-missing-schema-true-postcondition`, `ev-p097-feasibility-gap`, `ev-p096-shared-misinterpretation`
- `paper_id`: P074, P097, P096
- `claim_or_failure_mode`: 结构/语法或生成器同源验证可以接受语义上错误但内部自洽的状态。
- `evidence_level`: A
- `grading_reason`: 三篇强相关论文直接报告不同实例：ToolGate 在缺少结构化返回模式时约四分之一工具使用 `Q=True`；ReLoop 报告可行性与真实建模正确性之间的巨大差距；VeriSimpl 报告生成与验证共享误读而共同接受错误模型。它们不是同一基准，但一致支持“可执行/内部一致不等于任务语义正确”。
- `linked_route_ids`: NONE
- `route_status_hint`: active-fresh-evidence
- `historical_admission_decision`: ADMIT；与 LOCAL-PRUNE-001/002 不冲突。
- `source_location`: P074 §3.2 p4；P097 §1 p2；P096 §1/失败分析 p8，均有精确 Passage 与哈希。
- `citation_context`: P074 是直接工具执行；P097/P096 是相邻的自然语言优化建模验证，后两者只能支撑一般验证失灵机制，不能单独证明工具智能体效果。
- `decision`: KEEP
- `allowed_next_use`: 可进入失败模式与 gap 候选；方法有效性仍需工具智能体直接实验。

## EQ-002

- `evidence_id`: `ev-p073-internal-confidence-misalignment`, `ev-p013-intrinsic-self-correction-degrades`, `ev-p097-feasibility-gap`
- `paper_id`: P073, P013, P097
- `claim_or_failure_mode`: 模型内部置信度或同模型自我批评不能可靠地区分执行正确与语义错误。
- `evidence_level`: A
- `grading_reason`: P073 在工具型智能体中直接显示相似形式的正确/错误执行得到相似不确定性；P013 在等预算、无外部反馈的自校正中报告退化；P097 直接说明自我批评继承生成错误。多源一致，但具体错误类型不同。
- `linked_route_ids`: LOCAL-PRUNE-001
- `route_status_hint`: baseline-only
- `historical_admission_decision`: ADMIT-AS-NEGATIVE-EVIDENCE；只能用于否定“纯反思/纯置信度足够”，不能把反思路线重新包装成候选。
- `source_location`: P073 §2.1 p3；P013 对应 Evidence；P097 §1 p2。
- `citation_context`: P073 最贴近工具执行；P013 为一般推理邻域；P097 为优化建模邻域。
- `decision`: KEEP
- `allowed_next_use`: 强基线设计与失败模式；不得推出传播风险代理一定更好。

## EQ-003

- `evidence_id`: `ev-p030-recognition-application-gap`, `ev-p064-experience-following-error`
- `paper_id`: P030, P064
- `claim_or_failure_mode`: 被识别为过时/错误的状态不一定停止支配后续行为，错误经验可被复制并放大。
- `evidence_level`: A（相邻设定）
- `grading_reason`: 两篇智能体记忆论文分别直接报告识别—应用差距与错误经验传播；现象本身有多源直接证据，但不是在线工具返回故障。
- `linked_route_ids`: NONE
- `route_status_hint`: adjacency-only
- `historical_admission_decision`: ADMIT-FOR-MECHANISM-TRANSFER-ONLY；不能直接宣称工具状态图方法有效。
- `source_location`: P030 §4.2 p7；P064 Introduction p2。
- `citation_context`: 外部/长期记忆与当前工具轨迹状态具有结构相似性，但迁移成立需要单独实验。
- `decision`: KEEP-AS-ADJACENCY
- `allowed_next_use`: 失败模式背景与 C 级机制假设；不能单独支撑方法 Claim。

## EQ-004

- `evidence_id`: `ev-p040-failure-core`
- `paper_id`: P040
- `claim_or_failure_mode`: 智能体会在环境终局不满足时自信宣称完成，且可用独立于自然语言的终局标注识别。
- `evidence_level`: B
- `grading_reason`: 单篇高度相关论文在 tau2-bench 与 AppWorld 多模型轨迹上直接报告；可追溯、评价依据独立，但当前为 2026 预印本且研究的是失败检测，不是注入的语义工具错误。
- `linked_route_ids`: NONE
- `route_status_hint`: active-fresh-evidence
- `historical_admission_decision`: ADMIT
- `source_location`: P040 Abstract p1；Methods p3 的程序化环境终局说明。
- `citation_context`: 支撑独立终局测量路径与假阳性完成现象。
- `decision`: KEEP
- `allowed_next_use`: 测量设计、终局标签与失败模式；不能证明特定恢复机制。

## EQ-005

- `evidence_id`: `ev-p039-aggregate-score-masking`, `ev-p039-failure-core`, Passage `P039:p0007:s0002`
- `paper_id`: P039
- `claim_or_failure_mode`: 汇总任务准确率会掩盖工具跳过、忽略结果、捏造等不同机制，而单轮诊断不覆盖工具链、早期错误恢复和状态更新。
- `evidence_level`: B
- `grading_reason`: 单篇直接报告并明确给出单轮边界；定位完整。它是 2026 预印本/研讨会版本，且没有测试语义错误返回的长程恢复。
- `linked_route_ids`: NONE
- `route_status_hint`: active-measurement-evidence
- `historical_admission_decision`: ADMIT
- `source_location`: P039 Abstract p1、§3.2 p3、Conclusion p7。
- `citation_context`: 仅支撑测量分解需求，不构成“没人做长程恢复”的新颖性证据。
- `decision`: KEEP
- `allowed_next_use`: 测量失败模式与实验指标设计。

## EQ-006

- `evidence_id`: `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- `paper_id`: P066
- `claim_or_failure_mode`: 强单轮函数调用表现不能建立状态化、多步、长程工具能力。
- `evidence_level`: B
- `grading_reason`: BFCL 论文直接报告并定义多轮状态评价；与目标任务边界高度相关，但不直接研究语义错误返回。
- `linked_route_ids`: NONE
- `route_status_hint`: active-benchmark-prior
- `historical_admission_decision`: ADMIT
- `source_location`: P066 Abstract p1、§3.3 p4。
- `citation_context`: 支撑必须使用多步/状态化评测。
- `decision`: KEEP
- `allowed_next_use`: benchmark prior 与任务边界；不得据此宣称验证或回滚有效。

## 人工抽查

- A 级抽查 EQ-001：原文直接陈述 `Q=True`、可行但错误、共享误读三类事实；“静态/同源验证会漏语义错误”是它们的最小共同结论，未扩张到方法有效性。
- 拒绝项抽查见 `weak_evidence_rejects.md` 的 WR-001：终局翻转定位发生在已知失败轨迹/训练语境，不能当作在线无真值验证器。
