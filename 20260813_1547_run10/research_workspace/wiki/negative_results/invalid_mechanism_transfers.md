# 无效机制迁移

## IMT-v009-001

- `record_id`: IMT-v009-001
- `source_artifact`: `workbench_v009/provenance_resilience_transfer_audit.md`
- `failure_type`: structural-transfer-with-unidentified-input
- `why_it_failed`: 数据库查询韧性在已知 lineage 上结构匹配，但自然语言网页中的独立证据根是潜变量；输入图无法从允许观测中可靠识别，因而 min-cut 的正确性不随迁移保留。
- `lesson`: 机制同构不仅要求图算法对应，还要求目标域输入对象可观测、可构造且不依赖隐藏真值。
- `failure_class`: invalid-mechanism-transfer
- `triggering_artifact`: `workbench_v009/identifiability_probe_report.md`
- `blocked_actions`: 把数据库 resilience 直接迁移为网页证据停止证书。
- `allowed_next_actions`: 寻找有显式 provenance 的工具系统，或使用有校准假设的概率模型并重做最近基线审计。
- `anti_revival_rule`: 若仍使用不可识别的普通网页来源根，迁移保持无效。
- `source_action_decision_id`: CRL-v009-main-negative-decision
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13
