# 基准死路

## BD-v009-001

- `record_id`: BD-v009-001
- `source_artifact`: `research_workspace/subagents/v009_drnoise_impl_probe.md`
- `failure_type`: official-assets-unavailable
- `why_it_failed`: 截至 2026-08-13 未定位到 DRNOISE 官方代码、100 题数据、评分器或数据/代码许可证；论文 TeX 源包不含这些资产。
- `lesson`: Run-local 合成只能称 DRNOISE-inspired 机制探针，不能声称 DRNOISE 复现或外部有效性。
- `failure_class`: benchmark-asset-dead-end
- `triggering_artifact`: `research_workspace/subagents/v009_drnoise_impl_probe.md`
- `blocked_actions`: 把合成任务报告为官方 DRNOISE 结果；使用来源不明镜像。
- `allowed_next_actions`: 等待官方资产；寻找许可清晰且带独立终局的自然基准；正交转向。
- `anti_revival_rule`: 未固定官方资产与许可证前不得恢复“DRNOISE 复现”表述。
- `source_action_decision_id`: CRL-v009-main-negative-decision
- `baseline_delta_audit_path`: null
- `last_updated`: 2026-08-13
