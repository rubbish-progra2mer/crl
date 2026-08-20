# v148 假设组合

| 草案 | 判定 |
|---|---|
| 把重复意图编译为独立专用智能体 | `AGENT_SKILL_AND_PROCEDURAL_MEMORY_COLLISION`；独立调用仍是适用技能的路由与执行 |
| 编译优于检索式个性化 | `UNIDENTIFIED_WITHOUT_EQUIVALENT_RETRIEVAL_BASELINE`；目标实验只比较无记忆助手 |
| 任务模式生成智能体、行为模式进入共享风格 | `PREFERENCE_SCOPE_AND_APPLICABILITY_COLLISION`；是内容分区与触发域设计 |
| 两阶段触发降低语义相近技能的误路由 | `CASCADED_RETRIEVAL_AND_CLASSIFICATION_COLLISION`；且不同领域误触发率仍为 20% |
| 先离线质量门控再部署专用智能体 | `SKILL_VALIDATION_AND_REGRESSION_GATE_COLLISION`；候选批评、排序与小型评价没有独立算子 |
| 按复现频率、准确性风险和运行成本选择编译或检索 | 归约为缓存/专家路由的成本敏感选择，目标论文未测成本，当前证据不足以生成 Claim |

无假设达到最小可验证 Claim 或本地实验门槛。
