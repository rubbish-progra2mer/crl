# v013 Selection Context

## Recovery boundary

- Run: `20260722_1550_run01`
- System state: `DEVELOPMENT_NOT_COMMISSIONED`
- Run state: `ACTIVE`
- Previous durable result: `experiment_v012/result.md`
- Previous result SHA-256: `0E326207B582AB40E817872E05F6A3B61B523DE926CBC2B447B19DF889ED5843`
- v013 began with no Candidate, implementation, Experiment Plan, Development capture, Confirmation bytes, Review Packet, Reviewer report, Decision, or Delivery.
- v013 does not retune RCED, TPPA, residual features, prompt controls, or Development gates from a failed earlier version.

## Mandatory formal Card queries

The main Codex executed all three required entry queries before selecting v013:

- Failure: `multi step tool agent cascading error premature stop invalid state commit`
- Operator: `selective verification uncertainty stop gate tool execution trace`
- Paper: `function calling benchmark trajectory verification correction retrieval`

Relevant formal Cards included:

- `failure-tool-use-metrics-collapse-distinct-errors`
- `failure-fixed-search-depth-causes-under-and-over-search`
- `operator-gold-supervised-hindsight-search-depth`
- `paper-p039` (ToolFailBench)
- `paper-p080` (AutoSearch)

The formal evidence supports two premises only: aggregate task scores can mask distinct tool-use failures, and a fixed search depth can under-search some cases while over-searching others. It does not establish the v013 metric inconsistency or its empirical consequence.

## Four-view open-network audit

On 2026-07-23, the main Codex searched and directly inspected four distinct views:

1. **Exact target and formula view** — queries around `"How Many Tools Should an LLM Agent See"`, `"Bits-over-Random reward"`, and the exact formula terms `P_obs`, `P_rand`, `K`, and `N`; direct source: arXiv:2605.24660 and its official repository.
2. **Metric-definition view** — queries around `"Bits-over-Random aggregate audit P_obs P_rand"`; direct source: arXiv:2605.18857 and its official `bits-over-random` repository.
3. **Adjacent adaptive-depth view** — queries around adaptive K, dynamic tool selection, chance-corrected tool retrieval, AutoSearch, ToolRerank, and learned stopping; this view bounded the work away from claiming the first adaptive-K policy.
4. **Correction and critique view** — exact-title searches plus the target repository's Issues and Pull Requests. The GitHub API returned zero open or closed Issues and zero Pull Requests for both official repositories at inspection time. No public correction of the inconsistency was found. This is a bounded search result, not proof that no private or future critique exists.

## Fixed target bytes

| Source | Fixed identity | Local path | SHA-256 |
|---|---|---|---|
| How Many Tools Should an LLM Agent See? A Chance-Corrected Answer | arXiv:2605.24660 | `sources_v013/how_many_tools_2605.24660.pdf` | `4DB89BFAC79BC90DD5B532D04AC1012ED1691657A45379BBBB2312682847164C` |
| Official target repository | commit `9759eb9f0e7ed90ff289d34300acc15453f7851a` | `sources_v013/chance-corrected-tool-selection/` | clean Git checkout |
| Main downstream notebook | same commit | `sources_v013/chance-corrected-tool-selection/notebooks/01_tool_selection_downstream_validation.ipynb` | `61DA53127597D7A90A440A87FF2EFCEA77665454852D50552DF9BB2972A6FF81` |
| Preserved BM25 result rows | same commit | `sources_v013/chance-corrected-tool-selection/results/downstream_results_bm25.json` | `8872DB7F8528560419AB74AAE8D1F268C193AECE3E670CC11F96B15C336EFB93` |
| The 99% Success Paradox / Bits-over-Random | arXiv:2605.18857 | `sources_v013/bits_over_random_2605.18857.pdf` | `8587A2502CF4F5FA371A04EACA3EEC4D782AD52D0A12F346606EE2FFD4B3EC02` |
| Official metric repository | commit `746ef2466c24e0f810d2dde1b35db5c481949db6` | `sources_v013/bits-over-random/` | clean Git checkout |
| Official aggregate auditor | same commit | `sources_v013/bits-over-random/src/bor/audit.py` | `3DA2D063CCD78242686F54D3FDCD2E89A1E318BA20C6DAD4261F64552A8645C8` |
| Official metric primitives | same commit | `sources_v013/bits-over-random/src/bor/metrics.py` | `5D1E282B72B267314C8DA83B3FBA192D40FDD97A7FDB8D9D69943EAC34F6724D` |

The main Codex directly read both PDFs. Physical page 2 of arXiv:2605.24660 defines `BoR = log2(P_obs / P_rand)`. Physical page 5 turns the success-case ceiling into a per-query RL reward and assigns zero to failure. Physical pages 3–4 of arXiv:2605.18857 define observed success as an aggregate fraction and describe averaging query-level chance baselines before taking the logarithmic ratio.

## Verified source-code inconsistency

The target notebook implements:

```text
reward_i = -log2(K_i / N_i)  if hit_i else 0
reported_score = mean_i(reward_i)
```

For single-relevant-tool queries, the paper-defined aggregate metric is:

```text
defined_BoR = log2(mean_i(hit_i) / mean_i(K_i / N_i))
```

These are not algebraically equal. The official `bits-over-random` auditor at its fixed commit computes `p_obs` and `p_rand_mean` separately and then calls `bits_over_random(p_obs, p_rand_mean)`, matching the aggregate definition.

The target notebook's preserved fixed-K output already supplies an exact finite counterexample for `N=370`:

- `K=1`, found fraction `0.600`: notebook statistic `5.1188`, defined BoR `7.7944`.
- `K=3`, found fraction `0.78333`: notebook statistic `5.4414`, defined BoR `6.5941`.

Thus the notebook statistic ranks `K=3` above `K=1`, while the defined metric ranks `K=1` above `K=3`.

## Rejected routes

1. **Terminal-Wrench onset or hazard prediction** was rejected because Hide-and-Seek, FALAT, and ELPO occupy the nearest computation family.
2. **Multi-reference trajectory anomaly detection** was rejected because Trajectory Guard, TrajAD, and Praetor create direct or component-level collisions.
3. **ToolFailBench counterfactual tool-return validation** was rejected because EG-VAR directly covers execution-guided counterfactual validation, and the official public data do not include frozen author trajectories.
4. **BFCL top-k schema reranking** was rejected because MagicSelector, ReAttn, ToolRerank, hard-negative retrieval, and listwise reranking already occupy the nearest method family.
5. **A new adaptive-K policy** was rejected as the primary contribution because the target paper, AutoSearch, and related learned-stopping work already cover that claim family. v013 audits metric/reward consistency; it does not claim a new stopping policy.

## Development exposure and untouched boundary

- The main Codex read the target notebooks, preserved author outputs, and the fixed BFCL v3 simple file during selection. Development is therefore a disclosed replication/audit set, not untouched evidence.
- Development input is `sources_v013/bfcl_development/BFCL_v3_simple.json`, fixed from `ShishirPatil/gorilla@c15b2a151662cac9839c96d7dfb1493b5329c975`.
- Development input SHA-256: `FBC37B2AD252BF9AF985582E0E07B456173FE627D957491472EA9CEF5FB83158`.
- Prospective untouched Confirmation is `BFCL_v4_live_simple.json` at `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`.
- Only Confirmation Git-tree metadata was inspected. Confirmation file content has not been downloaded or read.
- Confirmation acquisition remains forbidden until Development passes every preregistered gate and the main Codex records a Promotion Audit.

## Selected computation

The selected v013 computation is a **Policy-Level BoR Consistency Audit**. It reproduces the target paper's fixed BFCL BM25 protocol, records per-query `hit`, `K`, and `N`, and evaluates the same frozen policy rows under both the notebook statistic and the paper-defined aggregate BoR. The material result is an auditable metric-identity and ordinal-consistency test, not a new model.
