# Seed 支撑事实审计 v001

> ADVISORY_ONLY：仅陈列可核查的机械或显式事实；不判断新颖性、科学充分性或交付结论。

- Run：`20260815_1818_run11`
- 截止时间：`2026-08-15T13:04:15.654508Z`
- Seed：`seed_v001.md`；SHA-256：`aa8b557410002fa63d61f19bc18ac1cad8d75449148bf35ad29553585e8971c7`
- Portfolio：`hypotheses_v001/portfolio.json`；SHA-256：`b76b2f05c94ccc9c4fcc537841e6d4492c8d784c56193418cc0a357369b47af7`
- Supporting attempts：`attempt-mutation-007`、`attempt-qwen-007`

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
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-003 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-003` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-003 记录了来源降级。 | `hypotheses_v001/priors/prior-003/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-003 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-003/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-004 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-004` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-004 记录了来源降级。 | `hypotheses_v001/priors/prior-004/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-004 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-004/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-005 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-005` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-005 记录了来源降级。 | `hypotheses_v001/priors/prior-005/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-005 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-005/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-006 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-006` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-006 记录了来源降级。 | `hypotheses_v001/priors/prior-006/request.json` |
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-mutation-007 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-mutation-007/execution.json`<br>`experiment_v001/attempts/attempt-mutation-007/spec.json`<br>`experiment_v001/attempts/attempt-mutation-007/metrics.json` |
| `warning` | `attempt_spec_parity_different` | supporting attempt attempt-qwen-007 的 Spec parity 维度 model_provider_revision 显式为 different。 | `experiment_v001/attempts/attempt-qwen-007/spec.json#/parity_dimensions/model_provider_revision` |
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-qwen-007 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-qwen-007/execution.json`<br>`experiment_v001/attempts/attempt-qwen-007/spec.json`<br>`experiment_v001/attempts/attempt-qwen-007/metrics.json` |
| `finding` | `independent_claim_validation_present` | 存在显式绑定为 independent_claim_validation 的有效 supporting attempt。 | `experiment_v001/attempts/attempt-qwen-007/spec.json` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 0 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-007/metrics.json#/records/0/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 1 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-007/metrics.json#/records/1/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 2 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-007/metrics.json#/records/2/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 3 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-qwen-007/metrics.json#/records/0/value` |
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
    "attempt-qwen-007"
  ],
  "prior_audits": [
    {
      "age_days": 0.11160474013888888,
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
      "age_days": 0.08919152289351852,
      "audit_id": "prior-002",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T10:55:49.506930Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-002",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.05474041866898147,
      "audit_id": "prior-003",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T11:45:26.082335Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-003",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.03005015261574074,
      "audit_id": "prior-004",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T12:20:59.321322Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-004",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.004331645289351852,
      "audit_id": "prior-005",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T12:58:01.400355Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-005",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.0005367350462962963,
      "audit_id": "prior-006",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T13:03:29.280600Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-006",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    }
  ],
  "supporting_attempts": [
    {
      "attempt_id": "attempt-mutation-007",
      "claim_ids": [
        "claim-mutation-discrimination"
      ],
      "execution_sha256": "83d22699d11ec657567a24703a9e2b9685b355dac9d98e948ebf9a35e0b352b9",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "00c18842015ed5877874ed0a06aae503b87ad9f7de8d585af648bb51d308268b",
      "purpose": "mechanism_consistency",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-mutation-007/execution.json",
        "experiment_v001/attempts/attempt-mutation-007/spec.json",
        "experiment_v001/attempts/attempt-mutation-007/metrics.json"
      ],
      "spec_sha256": "859ebe2f6a038288fed90a151ae513e4b20a4cd7a9b41da7cf8b7d9a5cb4e738"
    },
    {
      "attempt_id": "attempt-qwen-007",
      "claim_ids": [
        "claim-one-shot-brittleness"
      ],
      "execution_sha256": "509edd3221b5f92df179648fd8ade17a63fb98d2df212389631dec8831de754f",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "2a0859ead2964ab646cb4fba3ead6b1a5a99608d7c6d2c72386de7f716b59896",
      "purpose": "independent_claim_validation",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-qwen-007/execution.json",
        "experiment_v001/attempts/attempt-qwen-007/spec.json",
        "experiment_v001/attempts/attempt-qwen-007/metrics.json"
      ],
      "spec_sha256": "57d92fcffc17e731e80b51de82058c400e994264b99f7cd527cb7202457ce74c"
    }
  ]
}
```

## 机械权限边界

本材料不改变 Claim 或 hypothesis 状态，不改变三位 Reviewer、同字节哈希链或主研究者裁决权。
