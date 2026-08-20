# v160 失败归因

## 类型

`AGENT_MEMORY_BREAK_EVEN_ROUTING_CLOSED_BY_QUERY_AWARE_BUDGET_ROUTING_ADAPTIVE_MEMORY_AND_DEFERRED_CONSOLIDATION_PRIORS`

## 直接原因

- 目标论文已证明在其基准中，外部记忆相对完整历史的盈亏平衡高度依赖系统、骨干和内部流水线，不能靠轮数与消息长度的简单模型稳定预测；
- 已知会话长度下的切换只是成本核算，未知长度的二选一版本是经典在线切换；
- 加入查询难度、后端结构和答案质量后，BudgetMem、FluxMem 与 ShardMemo 已覆盖查询感知预算档、结构选择和成本感知门控；
- 避免逐轮高成本写入的自然修复又被 RecMem 的复现触发整合和 LightMem 的在线／离线解耦直接覆盖；
- 逐步质量—成本资源控制已有 RAG-on-a-Diet，不能靠把检索换名为“记忆调用”形成新差分。

## 非原因

- 不是否认目标论文的端到端服务成本测量或“记忆并非总是更便宜”的证据；
- 不是把 Hindsight 的未受控写入骨干或对话内样本相关性忽略；
- 不是因为缺少本机算力而跳过能改变新颖性判断的实验；
- 不是安全控制、科研反证、Prior collision 或 Run 终局。

## 决定

不注册实验或 Seed。保存服务成本账本和受控比较边界；Run 保持 `ACTIVE`，下一版离开记忆成本、预算路由与延迟整合方法族。
