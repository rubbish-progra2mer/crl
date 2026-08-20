# Seed 支撑事实审计 v001

> ADVISORY_ONLY：仅陈列可核查的机械或显式事实；不判断新颖性、科学充分性或交付结论。

- Run：`20260815_1818_run11`
- 截止时间：`2026-08-15T11:25:37.967911Z`
- Seed：`seed_v001.md`；SHA-256：`7ce687f90953285c768e765de9e72ebb8c49e5d743fd88a84f31960232c0cd8a`
- Portfolio：`hypotheses_v001/portfolio.json`；SHA-256：`c7517187f950cb213d00dc6ed25737f7b1851e87f20594a14a15c4523836a9a9`
- Supporting attempts：`attempt-mutation-004`、`attempt-qwen-004`

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
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-mutation-004 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-mutation-004/execution.json`<br>`experiment_v001/attempts/attempt-mutation-004/spec.json`<br>`experiment_v001/attempts/attempt-mutation-004/metrics.json` |
| `warning` | `attempt_spec_parity_different` | supporting attempt attempt-qwen-004 的 Spec parity 维度 model_provider_revision 显式为 different。 | `experiment_v001/attempts/attempt-qwen-004/spec.json#/parity_dimensions/model_provider_revision` |
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-qwen-004 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-qwen-004/execution.json`<br>`experiment_v001/attempts/attempt-qwen-004/spec.json`<br>`experiment_v001/attempts/attempt-qwen-004/metrics.json` |
| `finding` | `independent_claim_validation_present` | 存在显式绑定为 independent_claim_validation 的有效 supporting attempt。 | `experiment_v001/attempts/attempt-qwen-004/spec.json` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 0 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-004/metrics.json#/records/0/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 1 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-004/metrics.json#/records/1/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 2 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-004/metrics.json#/records/2/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 3 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-qwen-004/metrics.json#/records/0/value` |
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
    "attempt-qwen-004"
  ],
  "prior_audits": [
    {
      "age_days": 0.04311299711805556,
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
      "age_days": 0.020699779872685186,
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
      "attempt_id": "attempt-mutation-004",
      "claim_ids": [
        "claim-mutation-discrimination"
      ],
      "execution_sha256": "9385d64776f9433a0e5a1a566b5b6ec83c9c736647eb7637e2b7261641553d51",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "b60265bcd2c3030c8f4021a6c38fed6d265060bfeea161c0f05530c592102644",
      "purpose": "mechanism_consistency",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-mutation-004/execution.json",
        "experiment_v001/attempts/attempt-mutation-004/spec.json",
        "experiment_v001/attempts/attempt-mutation-004/metrics.json"
      ],
      "spec_sha256": "1cc3b8cbd88a803fa508518ac12ea9ff29fd7a03ffd303095177453ac150b51a"
    },
    {
      "attempt_id": "attempt-qwen-004",
      "claim_ids": [
        "claim-one-shot-brittleness"
      ],
      "execution_sha256": "2d0d12838154fdf9d636fd133ba6d0e2d6805c2ff1eaf9b9ccead65daf101579",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "10cd9ca9f2fe5d3a74b7d8c3d34082727abd70e824c8ef6d18abbf45fa1f051c",
      "purpose": "independent_claim_validation",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-qwen-004/execution.json",
        "experiment_v001/attempts/attempt-qwen-004/spec.json",
        "experiment_v001/attempts/attempt-qwen-004/metrics.json"
      ],
      "spec_sha256": "97ece5b833a0a491ed549b2fedf478ef228b8237fcc1e98ff22c643b8ae2139e"
    }
  ]
}
```

## 机械权限边界

本材料不改变 Claim 或 hypothesis 状态，不改变三位 Reviewer、同字节哈希链或主研究者裁决权。
