# Failure Mode Taxonomy — v001

## FM-v001-001：结构通过、语义失败的可信状态提交

- `failure_mode_id`: FM-v001-001
- `failure_statement`: 工具输出通过调用语法、结构模式或内部一致性检查后，仍可能在任务语义上错误，却被写入可信状态。
- `evidence_source`: EQ-001；P074 `ev-p074-missing-schema-true-postcondition`，P097 `ev-p097-feasibility-gap`，P096 `ev-p096-shared-misinterpretation`。
- `evidence_level`: A
- `affected_setting`: 直接工具执行（P074）及相邻的自然语言到优化模型验证（P097/P096）。
- `why_current_methods_fail`: 已直接观察到的原因包括缺少返回模式时后置条件退化为真、可执行性不检查遗漏语义、生成与验证共享同一误读。
- `existing_attempted_fixes`: 静态前/后置条件、求解器反馈、同模型自我批评、简化/敏感性行为检查。
- `why_fixes_are_insufficient`: 对无结构契约或完全遗漏的任务语义，静态/同源检查存在明确漏检；行为检查是否可泛化到工具轨迹仍未证实。
- `possible_causal_hypothesis`: 非同构的任务条件关系检查可降低共享误读；仅为假设，见 AS-v001-001/002。
- `possible_intervention_points`: 工具返回写入可信状态之前；状态声明从隔离层转为可信层时。
- `confidence`: 高（失败存在）；低—中（拟议干预有效）。
- `speculative_risk`: 因果修复高，失败事实低。
- `gap_matrix_eligibility`: YES；只允许“语义漏检”进入，不允许把具体方法有效性写成事实。
- `notes`: 最近工作碰撞可能把 h-v001-001 吸收，待 Prior Audit。

## FM-v001-002：置信或同模型反思与执行正确性错位

- `failure_mode_id`: FM-v001-002
- `failure_statement`: 工具执行轨迹可以在内部置信度和形式上相似，但真实执行正确性不同；没有外部反馈的同模型修订可能退化。
- `evidence_source`: EQ-002；P073、P013、P097。
- `evidence_level`: A
- `affected_setting`: 工具型语言智能体、不带外部反馈的一般推理、自然语言优化建模。
- `why_current_methods_fail`: 置信信号主要跟随文本/表示相似性；同模型验证继承原生成盲点。
- `existing_attempted_fixes`: 执行结果监督的置信校准、外部工具批评、行为扰动。
- `why_fixes_are_insufficient`: 执行监督不一定适用于新任务；统一外部验证超过预算；行为扰动的跨任务有效性未知。
- `possible_causal_hypothesis`: 验证预算应依据预期下游损失而非局部置信度；见 AS-v001-003。
- `possible_intervention_points`: 验证调度器、不可逆动作前检查。
- `confidence`: 高（错位存在）；低（传播风险代理更优）。
- `speculative_risk`: 方法因果解释高。
- `gap_matrix_eligibility`: YES；可要求强基线包含局部置信度、统一/随机验证。
- `notes`: 不得重新包装纯反思，LOCAL-PRUNE-001 仍生效。

## FM-v001-003：状态更新被识别但未真正支配后续行为

- `failure_mode_id`: FM-v001-003
- `failure_statement`: 智能体即使识别旧状态已失效，也可能没有在后续行为中应用更新；错误经验会被复制和放大。
- `evidence_source`: EQ-003；P030、P064。
- `evidence_level`: A（相邻设定）
- `affected_setting`: 长期/外部智能体记忆；迁移到在线工具状态尚未直接证实。
- `why_current_methods_fail`: 检索/识别与状态授权、策略应用是不同计算；线性历史会继续暴露污染内容。
- `existing_attempted_fixes`: 写时状态裁决、授权读出、记忆质量评估。
- `why_fixes_are_insufficient`: 对工具轨迹中的动态数据依赖、不可逆动作和局部恢复没有直接证据。
- `possible_causal_hypothesis`: 来源化隔离与后代失效可让更新真正控制行为；见 AS-v001-004/005。
- `possible_intervention_points`: 工具状态表示、冲突时恢复边界。
- `confidence`: 中（迁移相关性）；高（记忆设定中的原现象）。
- `speculative_risk`: 从记忆到工具轨迹的机制迁移较高。
- `gap_matrix_eligibility`: NO-DIRECT / ADJACENCY-ONLY；只能进入机制迁移审计与假设积压，不能直接构造本题 gap。
- `notes`: h-v001-003 必须先通过结构迁移与最近工作审计。

## FM-v001-004：汇总分数与单轮测量掩盖长程错误传播和恢复

- `failure_mode_id`: FM-v001-004
- `failure_statement`: 单一终局准确率可能把工具跳过、结果忽略和捏造混为一类；单轮诊断不能测量工具链、早期错误恢复或状态更新。
- `evidence_source`: EQ-005、EQ-006；P039、P066。
- `evidence_level`: A（两篇相关论文的互补直接证据）
- `affected_setting`: 工具调用基准与状态化多轮函数调用。
- `why_current_methods_fail`: 汇总指标不保留机制身份；单轮任务没有传播距离或恢复选择。
- `existing_attempted_fixes`: ToolFailBench 细粒度单轮分类；BFCL 多轮状态评价；P040 程序化终局检测。
- `why_fixes_are_insufficient`: 现有证据未展示同时具备自然化语义故障注入、传播路径、恢复动作和独立终局的评测。
- `possible_causal_hypothesis`: 将独立终局、故障提交率、传播距离、误验证与预算联合报告，能区分真正恢复与更多调用；这是测量设计假设，故障自然性见 AS-v001-007。
- `possible_intervention_points`: benchmark fault layer、trajectory logger、evaluation decomposition。
- `confidence`: 高（现有测量边界）；低—中（可构建无伪影注入层）。
- `speculative_risk`: “现有工作全部没有”未经系统最近工作审计，不能作为新颖性结论。
- `gap_matrix_eligibility`: YES-AS-MEASUREMENT-GAP；不等于方法贡献。
- `notes`: 必须把 tau-bench、BFCL、AppWorld 和 2026 后继纳入 Benchmark Prior 审计。

## 人工抽查

FM-v001-001 的失败陈述直接来自三处正文事实，不是从“论文没做某事”倒推；其拟议因果修复已明确降级并登记 AS-v001-001/002。FM-v001-003 因任务迁移仅作为相邻证据，不进入直接 gap。
