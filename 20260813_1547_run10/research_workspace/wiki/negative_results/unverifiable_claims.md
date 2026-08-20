# 不可验证主张

## UC-v009-001

- `record_id`: UC-v009-001
- `source_artifact`: `workbench_v009/identifiability_probe_report.md`
- `failure_type`: unverifiable-hard-independence-claim
- `why_it_failed`: 没有必异根证据时，网页文档之间的独立生成关系不是可从当前观测唯一识别的事实，因此不能把 estimated lineage 输出称为硬证书。
- `lesson`: 谱系估计必须明确是概率或启发式，不得使用“证明独立”“安全证书”等过强措辞。
- `failure_class`: claim-overreach
- `triggering_artifact`: `workbench_v009/identifiability_probe_results.json`
- `blocked_actions`: 宣称普通网页上的分布无关根独立性与硬安全性。
- `allowed_next_actions`: 报告概率、置信集合和覆盖边界，或使用真正可审计的生成凭据。
- `anti_revival_rule`: 未改变可观察信息或统计假设时不得恢复硬证书表述。
- `source_action_decision_id`: CRL-v009-main-negative-decision
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13
