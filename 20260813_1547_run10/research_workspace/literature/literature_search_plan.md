# Literature Search Plan

- `target_problem_ref`: `research_workspace/target_problem_card.md#TP-v001-01`
- `selected_sources`: 冻结 CRL 共享知识库的 purpose-aware retrieval；Run-local Prior Audit；arXiv、OpenReview、ACL Anthology、会议正式论文页等论文一级来源；Semantic Scholar/Crossref 仅用于引文与元数据扩展。
- `routing_rationale`: 先用知识库的 Failure/Operator/Paper/Passage 路线建立有原文定位的已知问题和算子，再用最近三年的一级来源补最近工作；关键候选沿前向/后向引文展开，不能以标题或摘要直接支持方法主张。
- `historical_failures_consulted`: 本 Run 尚无 `route_failure_registry.json`；未读取其他 Run。
- `blocked_route_ids`: NONE
- `monitored_route_ids`: NONE
- `pruned_query_families`: 显式异常码检测、网络重试、纯单轮事实核查、具身视觉恢复、纯提示反思。
- `blocked_seed_families`: 将“多调用几次工具”本身包装为方法；使用候选独占的真值、隐藏状态或工具权限；仅做提示模板变化。
- `route_pruning_policy_ref`: `research_workspace/literature/route_pruning_log.json`
- `avoid_repeat_failure_rules`: 每个查询和命中保存到本 Run；被强基线或最近工作吸收的路线记录组件级理由；摘要仅用于粗筛，核心判断必须回到可定位正文或论文原文。

## Query Families

1. `failure`: 表面成功但语义错误的工具结果、陈旧/不完整观测、长程状态漂移与错误放大。
2. `operator`: 选择性验证、回滚、重规划、轨迹一致性检查、因果/反事实信用分配、预算化诊断。
3. `prior`: 工具增强大语言模型智能体的执行验证、工具错误恢复、长程可靠性、自校正与过程监督。
4. `measurement`: 可控工具故障注入、独立终局判定、多步工具基准、成本—成功率曲线。
5. `semantic adjacency`: 规划中的部分可观测性、软件工作流补偿事务、故障定位；只提取可迁移计算机制，不直接当作同题新颖性证据。

## 双层漏斗

- 第一层：组合关键词、语义近邻、目标会议、近三年筛选和引文元数据，目标召回至少 100 条候选元数据；仅在本 Run 保存轻量索引，不写回共享知识库。
- 第二层：按问题贴合度、组件相似度、正式发表场所、引文邻接和可获得全文精选 20—30 篇；任何构造候选或淘汰路线的核心依据必须核对正文、Run-local Evidence 或原始 PDF。

## Exclusion Rules

- 排除候选方法获得额外真值、隐藏状态、额外工具或不可比预算的实验。
- 排除只研究显式工具异常、只评单轮问答或只报告自评置信度的论文作为直接最近工作。
- 相邻领域论文只提供机制词汇，不能单独支撑本题空白或有效性。

## Expected Failure Modes

- “语义工具错误”术语不统一，关键词召回可能碎片化。
- 许多工作只给摘要或网页描述，无法支持组件级碰撞判断。
- 最近工作可能已把选择性验证、反思或回滚作为完整方法，需要优先做最近工作审计。
- 工具基准常无受控语义故障注入，测量论文可能来自可靠性/软件工程邻域。

## Recall Quality Audit

| 项目 | 当前状态 | 防线 |
|---|---|---|
| 被排除 Top-5 论文与理由 | 待第一层检索后填写 | 在进入方法核前补齐题名、来源、排除理由及是否需回查 |
| 预计元数据召回概率 | 初始估计 0.70—0.85，待真实命中校准 | 五类信号交叉检索；术语同义扩展；引文前后向展开 |
| 核心基准先验 | tau-bench、BFCL、ToolBench/相关后继不得因术语差异被漏掉 | 设置 benchmark 专门查询；核心主张前核对其任务、工具错误模型和评价标签 |
| 最近工作 | 2023—2026 为主，经典先验不限年份 | arXiv/OpenReview/正式会议页交叉核对发布日期与版本 |

## 人工确认

主研究者确认来源优先级与种子查询未越过 `non_goals.md`；允许开始抓取和检索。
