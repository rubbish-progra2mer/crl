# Research Map

## Evidence-backed failures

P084 and the prior v009/v011 captures show that related-toolkit expansion produces operation-granularity errors that simple schema alignment and residual ranking did not repair. P041 WHEN2TOOL shows a distinct tool-overuse failure: binary necessity is linearly decodable, but unconditional steering has model-dependent override behavior.

## Exact nearest-prior map

| Proposed computation | Closest primary evidence | Collision |
| --- | --- | --- |
| Pairwise/listwise sibling-tool discrimination | `sources_v017/scalecall_2511.00074.pdf`, SHA-256 `3274AEF1DF3F74BDB15310EA3630A472EE5DB3EF1A9032AE509D3ABB68935546` | Directly applies listwise ranking to overlapping tool functionality. |
| Multi-aspect operation-granularity scoring | `sources_v017/multi_field_tool_retrieval_2602.05366.pdf`, SHA-256 `E0A6E0F53BCBE1DEA4C0C65B5D7A73DCC925F3814553F32596C43F4340233904` | Separately models functionality, input constraints, and output formats. |
| Rollout-derived discriminative tool/schema descriptions | `sources_v017/jtpro_2604.19821.pdf`, SHA-256 `EB565688A1EF0CC35A67BE24E5656EAEBF357138DC93CB9557FA0EC32CFBF1A5` | Co-optimizes instructions and tool schema/argument descriptions from rollout feedback. |
| Paired-outcome utility gate for tool steering | `sources_v017/to_call_or_not_2605.00737.pdf`, SHA-256 `676CA03AB9595FAE6784ED4995F985B0537E0E08AAC47D05F615E1C6C6747725` | Defines utility from ALWAYS TOOL versus NO TOOL, trains a hidden-state utility estimator, and controls calls with its score. |
| Cognition/action disagreement diagnosis | `sources_v017/model_adaptive_necessity_2605.14038.pdf`, SHA-256 `93002FD5EC9CFEDE5BAE3A8BF7FB458183DA116301E3FCDD746CE4F6188EA044` | Directly decomposes model-adaptive necessity cognition and execution and measures the knowing-doing transition. |

The fixed P041 source in the formal knowledge base is `knowledge_base/papers/P041_tool_call_necessity.pdf`, SHA-256 `A05F71B904209EA49CBC9CD13434255AAB4037F96640477810FB78A61B701BA0`.

## Mechanical source audit

The five v017 PDFs were downloaded successfully from official arXiv PDF endpoints. A read-only PyMuPDF traversal exited 0 over 114 pages and 414,463 extracted characters in total. Phrase-level readback located the claimed computations in the frozen bytes: `Latent Utility Estimator`, `ALWAYS TOOL`, `NO TOOL`, and `top-K`; `cognition`, `execution`, and `orthogonal`; multi-field functionality/input/output terms; listwise/overlapping terms; and JTPRO schema/rollout terms.

## Candidate Promotion Audit

No Candidate is promoted. Both plausible v017 computations collide with direct primary prior before any empirical screen. Proceeding would either relabel established methods or invite outcome-driven micro-variation.

## Next-version constraint

v018 must select a different failure/computation pair rather than another P084 reranker or hidden-state tool-necessity controller. A route may return to these topics only if its changed computation survives the direct priors frozen here and has a fresh, untouched Confirmation carrier.

