<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p084-generated-tool-single-dataset-boundary","ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Candidate Implement: Thin-Anchored Related-Tool Residual

## One-sentence method kernel

Fit a linear residual on frozen cross-encoder CLS differences between gold and P084-added related tools, then analytically cap that residual so it cannot reverse any positive frozen margin on a correctly ranked original thin menu.

## Failure/Evidence → Operator → Gap lineage

P084 holds the request fixed while adding semantically related, intended-function-different tools and observes function/parameter failures. [[evidence:ev-p084-expanded-toolkit-controlled-setting]] [[evidence:ev-p084-related-toolkit-error-types]] Its single generated dataset limits transfer. [[evidence:ev-p084-generated-tool-single-dataset-boundary]] ToolRet shows that large-corpus complete-set recovery is a separate bottleneck and that merged labels may omit valid alternatives. [[evidence:ev-p085-large-corpus-scale]] [[evidence:ev-p085-retrieval-completeness-failure]] [[evidence:ev-p085-non-exhaustive-label]]

Generic hard-negative adaptation is already crowded. The narrow v011 gap is not learning from related negatives; it is preserving proven thin-menu ordering while applying that learned residual to expanded menus.

## Baseline computation

Serialize every tool in a fixed field order: function name, function description, and sorted parameter records containing name, required flag, type, description, and enum. The pinned `cross-encoder/ms-marco-MiniLM-L6-v2` scores each query/schema pair once. Stable ties use the SHA-256 of the function name. The baseline receives no gold, thin/added membership, perturbed request, or labels at inference.

## Changed computation

For each Development training fold:

1. Keep the cross-encoder weights frozen and retain its raw logit `s(q,t)` and final-layer CLS vector `h(q,t)`.
2. For every gold tool and every added related non-gold tool in the training rows, form base margin `m=s(q,g)-s(q,n)` and vector difference `d=h(q,g)-h(q,n)`.
3. Fit one vector `w` by minimizing mean `log(1+exp(-(m+d·w))) + 0.5*||w||²`, with fixed L2 `1.0`.
4. For every training row whose frozen cross-encoder ranks a gold tool first in the original thin menu, enumerate positive gold-versus-thin-negative margins. Compute the largest `alpha` in `[0,1]` such that every affected margin after adding `alpha*w` retains at least `0.01` of its original positive value.
5. Rank held-out rows by `s(q,t)+alpha*h(q,t)·w`.

Grouped five-fold assignment is `int(query_sha256[:16],16) mod 5`, so duplicate query bytes never cross train/held-out. After OOF evaluation, fit one full-Development `w` and `alpha` for possible untouched Confirmation.

## Closest-composition difference

The executable closest-composition is `unanchored_related_adapter`. It uses the identical model logits, CLS vectors, related-negative pairs, objective, L2, optimizer, folds, tie rule, and inference score, but fixes `alpha=1`. The Candidate's only proposed delta is the analytic thin-menu margin cap. The frozen cross-encoder is the no-adaptation baseline.

## Minimal Claim Contract

Development can support only: on the already-touched P084 200-row expanded-menu dataset, grouped OOF thin-anchored residual ranking improves top-1 and MRR over the frozen cross-encoder, and the anchor reduces regressions versus the same unanchored residual while retaining most of its corrections.

If an untouched BFCL v4 live-multiple Confirmation also passes, the maximum Claim remains a local two-dataset function-ranking result for the fixed model and training source. It does not establish open-corpus retrieval, complete multi-tool recall, argument correctness, execution success, end-to-end Agent success, task/template/endpoint generalization, or novelty of hard-negative learning.

## Implement contract

- Program: `implementation_v011/evaluate.py`, SHA-256 `38d0320e37a960cbaaf64e20b27eb95d8f6f5704f459ca333742f0bb0b983874`.
- Config: `implementation_v011/config.json`, SHA-256 `2df83a3f7a5e804dc2d3f2a503db50e50062a495ebd5cb1d24fd869a984c6ab7`.
- Cross-encoder: six files, 91,815,758 bytes, revision `c5ee24cb16019beea0893ab7796b1df96625c6b8`; the deterministic local manifest digest recorded before results is `66c543f61785f1c65bf9420f2dadef19a4c520dce8de38f4d4a988a685996341`.
- Interpreter: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.
- Cwd: `D:\Desktop\crl\20260722_1550_run01\implementation_v011`.

Development argv:

```text
evaluate.py --phase development --config config.json --expanded inputs/BFCL_v3_multiple_tool_enrichment.json --questions inputs/BFCL_v3_multiple.json --gold inputs/BFCL_v3_multiple_possible_answer.json --output-dir ../experiment_v011/work/dev_eval_001
```

## Neutral comparators

- `cross_encoder`: the pinned frozen query/schema scorer.
- `unanchored_related_adapter`: the same learned residual with `alpha=1`.
- `thin_anchor_adapter`: the Candidate with analytically capped `alpha`.

All three score the same visible menu with the same frozen encoder. Candidate and unanchored adapter have identical training pairs and optimizer cost.

## Experiment contract

Development uses all 200 aligned P084/BFCL v3 rows. Input SHA-256 values are:

- expanded: `1be15f014a2d04af06fec2797e4e53f7a335ce46e6bdc2ec0ef3cabd6074a7b`;
- questions: `aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a`;
- gold: `244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047`.

Primary metrics are top-1 ground-truth membership and best-gold MRR on grouped OOF predictions. Paired item bootstrap uses 20,000 resamples and seed `20260723`.

Development direct conditions:

- Candidate minus frozen cross-encoder top-1 at least `+0.02`;
- paired MRR-delta bootstrap 95% lower bound above `0`;
- Candidate corrections exceed regressions;
- Candidate regressions are strictly fewer than unanchored-adapter regressions;
- Candidate retains at least three quarters of unanchored-adapter corrections.

These conditions do not automatically promote the Candidate. Main Codex must independently recompute raw bytes and complete the Promotion Audit.

Capture directory is `experiment_v011/captures/dev_eval_001/`. Declared outputs under `experiment_v011/work/dev_eval_001/` are `raw.jsonl`, `selected_params.json`, `query_hashes.json`, `summary.json`, and `environment.json`. Program, config, all six model files, three Development inputs, `execution.json`, `stdout.bin`, `stderr.bin`, and all five outputs must be saved as Experiment Artifacts.

## Confirmation isolation and analysis unit

Untouched Confirmation is fixed to `BFCL_v4_live_multiple.json` and `possible_answer/BFCL_v4_live_multiple.json` from `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`. Those bytes may be acquired only after Development passes and Main Codex writes the Promotion Audit. The frozen full-Development adapter must be loaded unchanged; no Confirmation fitting or parameter choice is allowed.

The paired analysis unit is one benchmark row/query. Duplicate query hashes are grouped in Development folds. Confirmation must be exact-query-hash disjoint, but this does not prove task-, template-, endpoint-, or entity-disjoint generalization.

## Cost and bundle attribution

The baseline and both adapters share one cross-encoder pass per query/tool pair. Each adapter adds one 384-dimensional dot product per tool. Adapter fitting is deterministic CPU L-BFGS over the same frozen features; no model-weight training, paid API, generated tokens, external tool call, retry, or additional inference model is used. Wall time, packages, GPU, CUDA runtime, driver, model manifest, argv, and input hashes must be captured.

Any total gain of the learned bundle must be separated from the anchor delta by the unanchored comparator. If only both learned variants improve equally, the anchor Claim fails.

## Risks and kill conditions

- P084 Development is already outcome-exposed; OOF is not untouched evidence.
- P084 added tools are generated and may contain style shortcuts.
- A linear residual may learn dataset artifacts or fail to generalize.
- The analytic cap protects only observed positive thin-menu training margins; it provides no test-time guarantee.
- Any nonzero execution, missing/recomputably incomplete raw output, baseline mismatch, false preregistered condition, unfair comparator, direct prior collision, or inability to attribute a regression reduction to the anchor freezes v011 and advances the same Run without Confirmation.
- After promotion, query overlap, changed adapter bytes, false Confirmation condition, or failed raw audit freezes v011.
