# Seed 支撑事实审计 v001

> ADVISORY_ONLY：仅陈列可核查的机械或显式事实；不判断新颖性、科学充分性或交付结论。

- Run：`20260815_1818_run11`
- 截止时间：`2026-08-15T11:14:56.429803Z`
- Seed：`seed_v001.md`；SHA-256：`1ee0ca3dc6cb71911365de3d84180485b45f209a2c362de013f2fb101a334d3c`
- Portfolio：`hypotheses_v001/portfolio.json`；SHA-256：`aecd2c672807953f394f47cfc3851ad71407703fa156ce2c302218d6fdfde8cc`
- Supporting attempts：`attempt-mutation-002`、`attempt-qwen-003`

## 审计记录

| 类别 | 代码 | 事实 | 来源 |
|---|---|---|---|
| `finding` | `seed_snapshot` | 已读取当前 Seed 的精确字节身份。 | `seed_v001.md` |
| `finding` | `portfolio_snapshot` | 已读取 1 个 hypothesis 的当前 portfolio 身份。 | `hypotheses_v001/portfolio.json` |
| `finding` | `seed_hypothesis_reference_resolved` | Seed hypothesis 引用可解析：H001。 | `seed_v001.md`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `seed_claim_reference_resolved` | Seed Claim 引用可解析：claim-mutation-discrimination。 | `seed_v001.md`<br>`hypotheses_v001/falsification/plan-h001-v001.json` |
| `finding` | `seed_claim_reference_resolved` | Seed Claim 引用可解析：claim-one-shot-brittleness。 | `seed_v001.md`<br>`hypotheses_v001/falsification/plan-h001-v001.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-001 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-001` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-001 记录了来源降级。 | `hypotheses_v001/priors/prior-001/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-001 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-001/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-002 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-002` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-002 记录了来源降级。 | `hypotheses_v001/priors/prior-002/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-002 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-002/request.json`<br>`hypotheses_v001/portfolio.json` |
| `warning` | `supporting_attempt_integrity_warning` | supporting attempt attempt-mutation-002 的闭合事实不可核验。 | `experiment_v001/attempts/attempt-mutation-002` |
| `warning` | `attempt_spec_parity_different` | supporting attempt attempt-qwen-003 的 Spec parity 维度 model_provider_revision 显式为 different。 | `experiment_v001/attempts/attempt-qwen-003/spec.json#/parity_dimensions/model_provider_revision` |
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-qwen-003 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-qwen-003/execution.json`<br>`experiment_v001/attempts/attempt-qwen-003/spec.json`<br>`experiment_v001/attempts/attempt-qwen-003/metrics.json` |
| `finding` | `independent_claim_validation_present` | 存在显式绑定为 independent_claim_validation 的有效 supporting attempt。 | `experiment_v001/attempts/attempt-qwen-003/spec.json` |
| `missing` | `seed_metric_mapping_source_missing` | 数字映射 0 的来源不是已核验 metrics/comparison 快照。 | `experiment_v001/attempts/attempt-mutation-002/metrics.json` |
| `missing` | `seed_metric_mapping_source_missing` | 数字映射 1 的来源不是已核验 metrics/comparison 快照。 | `experiment_v001/attempts/attempt-mutation-002/metrics.json` |
| `missing` | `seed_metric_mapping_source_missing` | 数字映射 2 的来源不是已核验 metrics/comparison 快照。 | `experiment_v001/attempts/attempt-mutation-002/metrics.json` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 3 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-qwen-003/metrics.json#/records/0/value` |
| `warning` | `seed_numeric_literals_unmapped` | Seed 正文含未被成功显式映射的可见数字。 | `seed_v001.md` |

## 可追踪事实

```json
{
  "comparisons": [],
  "declared_claim_ids": [
    "claim-mutation-discrimination",
    "claim-one-shot-brittleness"
  ],
  "declared_hypothesis_ids": [
    "H001"
  ],
  "independent_claim_validation_attempt_ids": [
    "attempt-qwen-003"
  ],
  "prior_audits": [
    {
      "age_days": 0.035687787534722216,
      "audit_id": "prior-001",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T10:23:33.004960Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-001",
      "queries": [
        "counterfactual tool output perturbation LLM agent tool result utilization causal sensitivity metamorphic testing"
      ]
    },
    {
      "age_days": 0.013274570289351851,
      "audit_id": "prior-002",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T10:55:49.506930Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-002",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    }
  ],
  "supporting_attempts": [
    {
      "attempt_id": "attempt-mutation-002",
      "integrity_errors": [
        "invalid supporting attempt attempt-mutation-002: implementation file 2 size does not match; implementation file 2 SHA-256 does not match"
      ],
      "sources": [
        "experiment_v001/attempts/attempt-mutation-002"
      ]
    },
    {
      "attempt_id": "attempt-qwen-003",
      "claim_ids": [
        "claim-one-shot-brittleness"
      ],
      "execution_sha256": "00adfb51e8333e3c81abc3a2e994d323ef446be0dba58b07253374d2981cf2cc",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "29276ab2cc799f88c0535bb2c7cde2bc7b33a2e6b5d9ec66cd61d77badccd50b",
      "purpose": "independent_claim_validation",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-qwen-003/execution.json",
        "experiment_v001/attempts/attempt-qwen-003/spec.json",
        "experiment_v001/attempts/attempt-qwen-003/metrics.json"
      ],
      "spec_sha256": "16658846523d500b2bd7cbc04939b0796efac54891e9da2a272d8248873f6676"
    }
  ]
}
```

## 机械权限边界

本材料不改变 Claim 或 hypothesis 状态，不改变三位 Reviewer、同字节哈希链或主研究者裁决权。
