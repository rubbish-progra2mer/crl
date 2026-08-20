# P055 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_CONSTRAINT_SHIFT_NEGATIVE_ANCHOR`
- Read 1 SHA-256: `c23e953959b062e6c9b898cf5498fe5c967e70684632731f0d932a6f1e1c4766`
- Accepted read-2: `read_2_attempts/r2-20260720-p055-a1/`
- Read-2 invocation SHA-256: `12571fd0b66d941dc294d56466a713fb044a5eb316c547a98eb50d20dd8eec0d`
- Read-2 report SHA-256: `5479b3ec418626cef8cf351c4138448d8553eec79e27d1af8d360f0d2354f1d1`
- Other attempts: none; read-2 narrowed wording and measurement claims without a conflict requiring read-3.

## Source reconciliation

- `AGREE`: CoPE 把短约束分成 Initial、Goal、Action、State 四类，并比较 Planner 与多种 formalizer；主实验按域抽取 100 个代表性 pair，而非运行全部 10,000 个组合。
- `AGREE`: 约束通常引起明显性能下降，但表格存在个别上升单元，论文没有置信区间或显著性检验。因此只能记录为广泛的描述性下降趋势，不能写成普遍“稳定减半”的定律。
- `AGREE`: PDDL、PDDL3、SMT、LTL 路径使用不同 prompt、工具链、horizon 与调用预算；formalizer 最多接收三轮工具错误反馈并修订。跨形式主义结果不能被当成纯表示格式的受控比较。
- `AGREE`: plan correctness 对 faithfulness false positive 的检查只在合并抽样的 20 个样本中观察到 0 个；这不足以支持所有域、模型和 formalism 上假阳性“可忽略”。
- `RESOLVED_BY_SOURCE`: 正式 Failure 只表述为“短约束分布变化可击穿 planner/formalizer 的语义稳健性”；三轮错误修订属于测量预算与边界，不抽成 Operator，也不扩展成用户排除的环境反馈/执行恢复方向。
- `UNRESOLVED_NONBLOCKING`: 缺少 matched-budget formalism comparison、充分 faithfulness 估计和跨自然任务复现；这些限制普遍性，但不阻断其作为 constraint-shift negative anchor 准入。

## Frozen source role

P054 formalizer 路线的约束压力测试与负向知识来源。它提醒后续 CRL：外部 planner 或 formal solver 只能处理被正确形式化的约束；短而局部的约束变化仍可导致语义遗漏，且工具反馈预算和 evaluator false positive 必须与方法差异分开。

## PLAN_05 Card source audit E disposition

- Auditor task: `/root/plan05_card_source_audit_e`
- Raw report: `knowledge_base/corpus/card_audits/plan05-audit-e/report.md`
- Raw report SHA-256: `82e6b1f26842f02b00c03af621141791b513a82d930b2c3fa01a48086be5b1a2`
- Pre-revision constraint-shift Failure Card SHA-256: `45ebf8d2dc5597a994110169fa59c73578cc345f5781993466b593f658765db1`
- Post-revision constraint-shift Failure Card SHA-256: `c3f80b652ebe2234255041bfe1d6c1dea08511e3ab3aa74a4b55ab80b47c6b37`
- Disposition: `RESOLVED_BY_MAIN_CODEX_ONE_PASS`

处置：把 CoPE 下降限定为总体结果而非每个表格单元；把 revision 明确成“最多三次代码尝试/修订、错误消息如有、语法修复而非重新规划”；把 20-sample 检查明确为跨 datasets/methods 的 pooled sample；删除无当前 Evidence 支撑的 `horizon` 要求。保留 100 个 constraint–problem 手工代表配对边界。无 `REJECT` 项，不追加循环审计。
