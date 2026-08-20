# Seed 支撑事实审计 v001

> ADVISORY_ONLY：仅陈列可核查的机械或显式事实；不判断新颖性、科学充分性或交付结论。

- Run：`20260815_1818_run11`
- 截止时间：`2026-08-15T14:19:12.697278Z`
- Seed：`seed_v001.md`；SHA-256：`4e3c409c84046d55486355a240730f57060ee6d87aacafd14d8d335f46c9708c`
- Portfolio：`hypotheses_v001/portfolio.json`；SHA-256：`44cbca69d01bdbe9e0bec01cad1b1533d51aa6874e8bca5836ca70823026e9c3`
- Supporting attempts：`attempt-budget-control-008`

## 审计记录

| 类别 | 代码 | 事实 | 来源 |
|---|---|---|---|
| `finding` | `seed_snapshot` | 已读取当前 Seed 的精确字节身份。 | `seed_v001.md` |
| `finding` | `portfolio_snapshot` | 已读取 1 个 hypothesis 的当前 portfolio 身份。 | `hypotheses_v001/portfolio.json` |
| `finding` | `seed_hypothesis_reference_resolved` | Seed hypothesis 引用可解析：H001。 | `seed_v001.md`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `seed_claim_reference_resolved` | Seed Claim 引用可解析：claim-budget-matched-excess。 | `seed_v001.md`<br>`hypotheses_v001/falsification/plan-h001-v001.json` |
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
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-006 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-006/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-007 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-007` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-007 记录了来源降级。 | `hypotheses_v001/priors/prior-007/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-007 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-007/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-008 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-008` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-008 记录了来源降级。 | `hypotheses_v001/priors/prior-008/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-008 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-008/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-009 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-009` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-009 记录了来源降级。 | `hypotheses_v001/priors/prior-009/request.json` |
| `warning` | `attempt_spec_parity_different` | supporting attempt attempt-budget-control-008 的 Spec parity 维度 model_provider_revision 显式为 different。 | `experiment_v001/attempts/attempt-budget-control-008/spec.json#/parity_dimensions/model_provider_revision` |
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-budget-control-008 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-budget-control-008/execution.json`<br>`experiment_v001/attempts/attempt-budget-control-008/spec.json`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json` |
| `finding` | `independent_claim_validation_present` | 存在显式绑定为 independent_claim_validation 的有效 supporting attempt。 | `experiment_v001/attempts/attempt-budget-control-008/spec.json` |
| `missing` | `seed_metric_mapping_text_missing` | 数字映射 0 的 seed_text 不在 Seed 正文中。 | `seed_v001.md` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 1 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/2/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 2 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/0/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 3 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/3/value` |
| `warning` | `seed_numeric_literals_unmapped` | Seed 正文含未被成功显式映射的可见数字。 | `seed_v001.md` |

## 可追踪事实

```json
{
  "comparisons": [],
  "declared_claim_ids": [
    "claim-budget-matched-excess"
  ],
  "declared_hypothesis_ids": [
    "H001"
  ],
  "independent_claim_validation_attempt_ids": [
    "attempt-budget-control-008"
  ],
  "prior_audits": [
    {
      "age_days": 0.16365384627314813,
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
      "age_days": 0.1412406290277778,
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
      "age_days": 0.10678952480324075,
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
      "age_days": 0.08209925875,
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
      "age_days": 0.05638075142361111,
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
      "age_days": 0.05258584118055555,
      "audit_id": "prior-006",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T13:03:29.280600Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-006",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.0024915814351851853,
      "audit_id": "prior-007",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T14:15:37.424642Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-007",
      "queries": [
        "large language model metamorphic testing equal budget repeated calls tool output field perturbation paired reliability"
      ]
    },
    {
      "age_days": 0.0011253615393518519,
      "audit_id": "prior-008",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T14:17:35.466041Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-008",
      "queries": [
        "large language model metamorphic testing equal budget repeated calls tool output field perturbation paired reliability"
      ]
    },
    {
      "age_days": 0.0005121414236111111,
      "audit_id": "prior-009",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T14:18:28.448259Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-009",
      "queries": [
        "large language model metamorphic testing equal budget repeated calls tool output field perturbation paired reliability"
      ]
    }
  ],
  "supporting_attempts": [
    {
      "attempt_id": "attempt-budget-control-008",
      "claim_ids": [
        "claim-budget-matched-excess"
      ],
      "execution_sha256": "8d5310053883d750427eb129d19907e5c09d7a7093b2ffc98b393c75feb967df",
      "hypothesis_id": "H001",
      "metric_record_count": 4,
      "metrics_sha256": "957374383425a86e3f1e9b91b84af4de6aad1fa06fe1cb23c44016c5262e3a2b",
      "purpose": "independent_claim_validation",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-budget-control-008/execution.json",
        "experiment_v001/attempts/attempt-budget-control-008/spec.json",
        "experiment_v001/attempts/attempt-budget-control-008/metrics.json"
      ],
      "spec_sha256": "82b9110e4c2f144c3eddc40866663dec7ae0367d23a5d43861d687bd2c11c485"
    }
  ]
}
```

## 机械权限边界

本材料不改变 Claim 或 hypothesis 状态，不改变三位 Reviewer、同字节哈希链或主研究者裁决权。
