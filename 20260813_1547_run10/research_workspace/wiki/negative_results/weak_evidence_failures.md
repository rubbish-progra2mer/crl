# 弱证据失败

## WE-v009-001

- `record_id`: WE-v009-001
- `source_artifact`: `hypotheses_v009/priors/v009-h001-provenance-resilience/request.json`
- `failure_type`: degraded-prior-retrieval
- `why_it_failed`: 三次标准 Prior Audit 均受语义学者 429 限流，长复合 arXiv 查询包含大量泛化深度研究噪声，不能单独支持未碰撞结论。
- `lesson`: v009 的负裁决依赖一级来源逐篇核查与形式反例，而不是把降级检索当新颖性证明。
- `failure_class`: evidence-coverage-degradation
- `triggering_artifact`: `hypotheses_v009/priors/v009-h001-argus-lineage/request.json`
- `blocked_actions`: 以“标准审计未命中 exact”宣称新颖。
- `allowed_next_actions`: 使用固定一级来源、引文谱系与可执行反例。
- `anti_revival_rule`: 未补足高质量检索前，任何“未找到”只能记录为未解决。
- `source_action_decision_id`: CRL-v009-main-negative-decision
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13
