# Weak Evidence Rejects — v001

## WR-001

- `evidence_id`: `ev-p027-operator-core`
- `paper_id`: P027
- `linked_route_ids`: NONE
- `reject_reason`: 只能证明在已知失败轨迹中，用终局翻转找到关键动作并构造训练偏好；不能支持在线、无终局真值的验证调度。
- `original_source`: P027 Methodology p3。
- `missing_requirement`: 测试时无真值定位与同预算工具验证证据。
- `suggested_followup`: 保留为强最近工作/离线 oracle 上界，不进入当前在线机制事实。
- `status`: C-ADJACENCY

## WR-002

- `evidence_id`: `ev-p025-grouped-step-influence`
- `paper_id`: P025
- `linked_route_ids`: NONE
- `reject_reason`: 该因果影响量作用于多智能体训练的下一步概率，不直接测量工具错误传播损失或验证价值。
- `original_source`: P025 §5.2 p6。
- `missing_requirement`: 在线工具轨迹、独立错误标签与验证调度结果。
- `suggested_followup`: 仅作为“屏蔽历史估计步骤影响”的机制邻居。
- `status`: C-ADJACENCY

## WR-003

- `evidence_id`: `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- `paper_id`: P037
- `linked_route_ids`: NONE
- `reject_reason`: milestone DAG 与 minefield 是评价结构，不是语义工具错误注入或恢复方法。
- `original_source`: P037 Introduction p5。
- `missing_requirement`: 工具返回故障模型与恢复动作效果。
- `suggested_followup`: 可用于独立轨迹评价设计，不进入方法空白。
- `status`: C-MEASUREMENT-ONLY

## WR-004

- `evidence_id`: `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`
- `paper_id`: P079
- `linked_route_ids`: NONE
- `reject_reason`: 训练阶段使用示范下一动作/真值动作选择观测，不能支持测试时无真值语义验证。
- `original_source`: P079 §3.2 p4。
- `missing_requirement`: 不访问真值动作的在线检测。
- `suggested_followup`: 作为特权信息上界或泄漏风险对照。
- `status`: C-ORACLE-BOUND

## WR-005

- `evidence_id`: NONE（模型推断）
- `paper_id`: NONE
- `linked_route_ids`: NONE
- `reject_reason`: “下游扇出×不可逆性必然是最优验证价值代理”当前没有直接论文证据。
- `original_source`: 主研究者假设 h-v001-002。
- `missing_requirement`: 真实/程序化故障标签上的排序关联与等预算干预结果。
- `suggested_followup`: 进入假设积压并由最小 killer experiment 反证。
- `status`: D-AS-FACT / C-AS-HYPOTHESIS
