# P068 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_AUDIT_THEN_SCORE_AND_COST_DEPENDENCE`
- Read 1 SHA-256: `3035a3b88849b023953a175a01398c5424ba1e6b8f6b0297daa5d11a13c14471`
- Accepted read-2: `read_2_attempts/r2-20260720-p068-a1/`
- Read-2 invocation SHA-256: `cac41421d2f66a28b77ed1a18f56dba13e152bb59318d5b21a233fdb60345083`
- Read-2 report SHA-256: `3242e4d3668a7763d08ab40a45be336dd06298b1f09ab9582578272b2db6031d`
- Other attempts: none; no read-3 required.

## Source reconciliation

- `AGREE`: challenger 提交 evidence-backed disagreement，auditor 可修订 versioned benchmark，再评分。
- `AGREE`: hidden micro-golds 的人工 accuracy 经审计显著变化，支持 one-shot gold brittleness。
- `NARROWED`: rationale evolution 只在 label disagreement 触发；同标签但理由错误不保证更新。
- `CONFOUND_RETAINED`: full method token/API 成本明显更高，且 GPT-4.1/GPT-5 同族参与 benchmark construction 和 scoring，不能把总分纯归因于审计逻辑。

## Frozen source role

Evidence-audit-before-score Operator + brittle-gold Failure；未来必须同时报告近成本对照和 label revision trace。
