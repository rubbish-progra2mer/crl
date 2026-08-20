# 先行工作碰撞案例

## CC-v009-001

- `record_id`: CC-v009-001
- `source_artifact`: `research_workspace/subagents/v009_evidence_decision_prior.md`
- `failure_type`: method-family-occupied
- `why_it_failed`: 宽口径“候选答案触发反证义务、预期证据、竞争假设查询及查询/停止控制”已由 CoVe、CounterRefine、HCQR、EEP、FIRE 与 Argus 形成直接方法链；自然语言义务编译不再构成独立方法核。
- `lesson`: 后续不得把两阶段核验、答案条件化检索或真/假预期证据重新包装为新贡献。
- `failure_class`: nearest-prior-method-collision
- `triggering_artifact`: `research_workspace/subagents/v009_evidence_decision_prior.md`
- `blocked_actions`: 继续实现通用 claim-triggered falsification obligation compiler。
- `allowed_next_actions`: 只可将明确不同且有外部可判定语义的子算子作为其他方法的辅助模块；或转向正交问题。
- `anti_revival_rule`: 必须证明新的输入、计算和输出均不能由上述方法链组合复现，才允许重新审计。
- `source_action_decision_id`: CRL-v009-main-negative-decision
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13

## CC-v011-001

- `record_id`: CC-v011-001
- `source_artifact`: `research_workspace/subagents/v011_identity_binding_scout.md`
- `failure_type`: method-family-occupied-and-anti-revival
- `why_it_failed`: Entity Binding Failures 已覆盖实体解析前置、候选比较、门控、来源与澄清；PACT 和 IGAC 覆盖跨步参数来源、作用域证书与资源效果边界。来源根不可见时，来源折叠连接不可识别；可见时退化为经典带来源实体解析。
- `lesson`: 不得以“跨应用”或“非循环证书”换名复活 v009 的隐藏来源根。
- `failure_class`: nearest-prior-plus-identifiability
- `triggering_artifact`: `workbench_v011/v011_route_resolution.md`
- `blocked_actions`: 构建来源折叠的跨命名空间身份连接证书并把 AppWorld 扰动作为方法贡献。
- `allowed_next_actions`: 只有出现不依赖隐藏根且经典实体解析无法表达的新可观测对象时重审。
- `anti_revival_rule`: 必须同时越过 v009 根不可识别性、EntityBindingFailures、PACT、IGAC 与经典实体解析。
- `source_action_decision_id`: CRL-v011-main-identity-route-kill
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13

## CC-v011-002

- `record_id`: CC-v011-002
- `source_artifact`: `research_workspace/subagents/v011_authority_flow_scout.md`
- `failure_type`: strong-composite-baseline-absorption
- `why_it_failed`: PAuth、Progent、AIP/IBCT、FORGE/SEAgent 与经典能力安全可逐项重构任务切片、参数来源、权限只减不增、多跳沿袭和提交前检查。
- `lesson`: 把任务切片映射进衰减令牌并不改变授权计算。
- `failure_class`: nearest-prior-method-composition
- `triggering_artifact`: `workbench_v011/v011_route_resolution.md`
- `blocked_actions`: 实现目的绑定的多跳委派子图精化中间件。
- `allowed_next_actions`: 仅在发现最强复合基线结构上无法表达的系统性攻击族时重开。
- `anti_revival_rule`: 新目的字段、新令牌格式或 MCP/A2A 载体均不算新核。
- `source_action_decision_id`: CRL-v011-main-authority-route-kill
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13

## CC-v011-003

- `record_id`: CC-v011-003
- `source_artifact`: `research_workspace/subagents/v011_observability_scout.md`
- `failure_type`: exact-formal-reduction
- `why_it_failed`: 令 `f(h)=d_a(h)` 后，可能世界、ALLOW/DENY 标签、带成本只读查询和决策一致停止条件与函数求值决策树一一对应；噪声和状态依赖版本分别落入等价类判定与部分可观测强规划。
- `lesson`: 一行形式约化足以杀死只改变应用载体的主动查询方法。
- `failure_class`: cross-field-exact-computation-collision
- `triggering_artifact`: `workbench_v011/v011_route_resolution.md`
- `blocked_actions`: 实现决策条件化最小区分查询编译器。
- `allowed_next_actions`: 只有目标对象不再是可能世界上的决策函数时重开。
- `anti_revival_rule`: 从工具模式学习测试模型再接经典区分查询仍视为 v010 式组合。
- `source_action_decision_id`: CRL-v011-main-observability-route-kill
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13

## CC-v010-001

- `record_id`: CC-v010-001
- `source_artifact`: `workbench_v010/action_model_collision.md`
- `failure_type`: cross-field-computation-exact-plus-agent-runtime-composition
- `why_it_failed`: 工具语义足迹恢复等价于从部分轨迹学习 lifted action preconditions/effects/implicit arguments；该计算已被 STRIPS/STRIPS+ 动作模型学习占据，黑盒 API 的依赖/CRUD 图又由 RESTler/Morest 占据。下游可串行化已由 CoAgent/Atomix 等占据。
- `lesson`: 把动作模型称为工具足迹、再把它接入事务协议，不产生新方法核。
- `failure_class`: nearest-prior-cross-field-collision
- `triggering_artifact`: `hypotheses_v010/priors/v010-h001-action-model-lineage/candidates.json`
- `blocked_actions`: 实现反事实足迹编译器并将 AppWorld 足迹准确率作为方法贡献。
- `allowed_next_actions`: 转向不等价于前置条件/效果学习的正交问题；评测资产只能在独立方法核需要时使用。
- `anti_revival_rule`: 必须指出 action-model/API-dependency representation 无法表达的新对象与新计算，才允许重审。
- `source_action_decision_id`: CRL-v010-main-prior-collision
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13

## CC-v012-001

- `record_id`: CC-v012-001
- `source_artifact`: `workbench_v012/v012_async_future_collision.md`
- `failure_type`: method-level-counterfactual-replay-plus-speculation-composition
- `why_it_failed`: 未决 future 的成对完成、教师强制重放、调用等价比较与执行/等待门控，被 AttriGuard 的反事实观察替换、影子重放和调用存活门近乎精确吸收；PASTE、Speculative Actions、Speculative Interaction Agents 与成本感知提交屏障又覆盖了隔离、确认、取消和不可逆禁推测。
- `lesson`: 真实的显式依赖盲区不自动产生新解法；改变反事实干预变量并接入已有运行时仍是模块组合。
- `failure_class`: nearest-prior-exact-component-plus-runtime-composition
- `triggering_artifact`: `research_workspace/subagents/v012_async_future_scout.md`
- `blocked_actions`: 实现 paired future-completion replay barrier，或用 AsyncTool 端到端结果包装其新颖性。
- `allowed_next_actions`: 只可另行审计带覆盖风险的工具输出抽象商空间编译器，或转向正交问题。
- `anti_revival_rule`: 必须在不读真实 future/隐藏真值的条件下定义可审计结果类和未覆盖风险，并击败同预算 AsyncFC+AttriGuard-port 及安全推测强基线。
- `source_action_decision_id`: CRL-v012-main-async-future-route-kill
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13

## CC-v013-001

- `record_id`: CC-v013-001
- `source_artifact`: `research_workspace/subagents/v013_evidence_response_training_scout.md`
- `failure_type`: known-label-composition-plus-unknown-label-identifiability
- `why_it_failed`: 已知似然时，配对结果干预、后验/下一实验/停止标签和训练目标可由 v003、贝叶斯教学、Fisher-R1、HEP/EDIT、AttriGuard/CAR 与 POPPER/MDA 组合复现；未知似然时，相同可见输入可对应相反后验与动作。
- `lesson`: 科学证据不吸收是真问题，但把规范统计控制器的输出蒸馏进模型不是新方法；没有决定变量时训练不能识别正确标签。
- `failure_class`: strong-composite-baseline-plus-input-nonidentifiability
- `triggering_artifact`: `workbench_v013/v013_evidence_response_training_collision.md`
- `blocked_actions`: 实现 paired evidence-response 联合训练，或用科学基准端到端成功率包装 v003 路线。
- `allowed_next_actions`: 仅可另审具有独立覆盖保证或任意时有效保证的证据强度区间估计，并在覆盖不足时弃权。
- `anti_revival_rule`: 新结果标签、显式信念账本、过程奖励、更多重放样本或更换科学环境均不改变当前二难。
- `source_action_decision_id`: CRL-v013-main-evidence-response-route-kill
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13

## CC-v014-001

- `record_id`: CC-v014-001
- `source_artifact`: `research_workspace/subagents/v014_adaptive_verifier_feedback_scout.md`
- `failure_type`: exact-problem-reduction-plus-direct-agent-method-collision
- `why_it_failed`: 分布样本反馈归约为 Reusable Holdout/Thresholdout/Ladder，完整规范反馈归约为 CEGIS，有限代理反馈不能识别测试外意图；SEAL 已直接实现密封审计、单比特接受、保守回退和独立终局。
- `lesson`: 重复反馈成为预言机是真问题，但反馈预算和保护集外壳不是新的智能体端计算。
- `failure_class`: cross-field-exact-reduction-plus-nearest-prior-method-collision
- `triggering_artifact`: `workbench_v014/v014_adaptive_verifier_feedback_collision.md`
- `blocked_actions`: 实现 feedback-budget/public-private-holdout wrapper，或用 SpecBench/USACO 结果包装其新颖性。
- `allowed_next_actions`: 只有发现 Thresholdout/Ladder/CEGIS/SEAL 无法表达的新智能体状态—动作对象时另审。
- `anti_revival_rule`: 查询次数、返回精度、差分隐私噪声、公共/私有划分、主动购买反馈或新评测载体均不足以重开。
- `source_action_decision_id`: CRL-v014-main-adaptive-feedback-route-kill
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13

## CC-v015-001

- `record_id`: CC-v015-001
- `source_artifact`: `research_workspace/subagents/v015_nonmonotone_progress_scout.md`
- `failure_type`: exact-cross-field-computation-and-interface-collision
- `why_it_failed`: 读足迹、写变化、最小失效闭包、撤销旧通过、选择性重验和新鲜终局与动态依赖图、自调整计算、增量构建及 Ekstazi 安全回归测试选择逐字段同构；Agent 外层已有 Atomix/MemTX。
- `lesson`: 找到一个新基准盲点不等于产生新修复算子；验证进度节点仍是可失效的缓存计算节点。
- `failure_class`: cross-field-exact-method-collision
- `triggering_artifact`: `workbench_v015/v015_nonmonotone_progress_collision.md`
- `blocked_actions`: 实现 dependency-aware progress invalidation controller 并以 stale-progress 降低作为方法新颖性。
- `allowed_next_actions`: 可作为 PushBench/SkillSentry 的评价修补或复合系统组件，不可作为独立 CCF-B 方法核。
- `anti_revival_rule`: 更细足迹、风险排序、同快照终止或用 LLM 猜影响集合均不足以重开。
- `source_action_decision_id`: CRL-v015-main-nonmonotone-progress-route-kill
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13
