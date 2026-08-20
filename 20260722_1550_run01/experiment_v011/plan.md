# Experiment Plan

```json
{
  "experiment_id": "v011",
  "candidate_sha256": "acf6a6fab1f66622907bbf7c338bd388b8c871609bb151c718f06fb52476eb20",
  "evidence_packet_sha256": "212c7513d99878567d9339e9c1596e6ab726511efed436f15bd52719856bc1c7"
}
```

## Codex Plan

# v011 Thin-Anchored Related-Tool Residual

## Frozen before results

This plan fixes v011 before any scientific scoring or metric output. The P084 Development rows and prior v009 outcomes are already known and are disclosed in `selection_context_v011.md`. The v011 computation, grouped folds, optimizer, anchor rule, metrics, gates, implementation, config, model, and inputs are now immutable. The fixed BFCL v4 live-multiple Confirmation bytes remain unacquired and unread.

- Candidate SHA-256: `acf6a6fab1f66622907bbf7c338bd388b8c871609bb151c718f06fb52476eb20`.
- Evidence Packet SHA-256: `212c7513d99878567d9339e9c1596e6ab726511efed436f15bd52719856bc1c7`; six Evidence entries are current.
- Program SHA-256: `38d0320e37a960cbaaf64e20b27eb95d8f6f5704f459ca333742f0bb0b983874`.
- Config SHA-256: `2df83a3f7a5e804dc2d3f2a503db50e50062a495ebd5cb1d24fd869a984c6ab7`.
- Cross-encoder: six files, 91,815,758 bytes, local manifest digest `66c543f61785f1c65bf9420f2dadef19a4c520dce8de38f4d4a988a685996341`, revision `c5ee24cb16019beea0893ab7796b1df96625c6b8`.

## Data acquisition and sampling contract

Development uses all 200 aligned rows from:

- `BFCL_v3_multiple_tool_enrichment.json`, SHA-256 `1be15f014a2d04af06fec2797e4e53f7a335ce46e6bdc2ec0ef3cabd6074a7b`, from `ibm-research/BFCL-FC-robustness@2ec93e790cf5fa3753d477a83cd596115387f1c5`;
- `BFCL_v3_multiple.json`, SHA-256 `aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a`;
- `BFCL_v3_multiple_possible_answer.json`, SHA-256 `244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047`.

The latter two files are from `ShishirPatil/gorilla@c15b2a151662cac9839c96d7dfb1493b5329c975`. There is no row sampling. Duplicate query bytes are assigned to the same one of five folds by `int(query_sha256[:16],16) mod 5`.

Untouched Confirmation is fixed as `BFCL_v4_live_multiple.json` and `possible_answer/BFCL_v4_live_multiple.json` from `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`. It may be acquired only after all Development conditions pass and Main Codex completes the Promotion Audit. No replacement source is allowed.

## Primary metric and mechanism signature

Top-1 is one when the first ranked function belongs to the row's ground-truth function set. MRR uses the highest-ranked ground-truth function. Multi-gold rows do not measure complete call-set recall.

The Candidate is evaluated only from held-out OOF predictions. Paired bootstrap resamples benchmark rows 20,000 times with seed `20260723`.

Development conditions are:

- Candidate minus frozen cross-encoder top-1 at least `+0.02`;
- Candidate MRR-delta bootstrap lower bound above `0`;
- Candidate corrections exceed regressions;
- Candidate regressions are strictly fewer than unanchored-adapter regressions;
- Candidate corrections are at least three quarters of unanchored-adapter corrections.

The mechanism signature is regression reduction versus the identical unanchored residual while retaining most corrections. Passing booleans never substitute for Main Codex recomputation and judgment.

## Closest-composition, neutral comparators and delta ablation

- `cross_encoder`: frozen local model without v011 learning.
- `unanchored_related_adapter`: same frozen CLS vectors, gold-versus-added-related pairs, pairwise logistic objective, L2, optimizer, folds, and score, with residual scale exactly 1.
- `thin_anchor_adapter`: same residual multiplied by the largest scale in `[0,1]` that retains 1% of every positive frozen gold-versus-thin-negative margin on correctly ranked thin training menus.

The only delta between the last two methods is the scale cap. No method receives gold or thin/added membership at held-out or Confirmation inference.

## Same-model/data/tool-budget controls

All methods use the same query, serialized schema, visible menu, frozen cross-encoder pass, and stable tie rule. Both learned variants use the same training pairs and optimizer. Each adds one 384-dimensional dot product per tool. There are no paid APIs, generated tokens, model-weight updates, external inference tools, or retries.

## Capture and Artifact bindings

Interpreter: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.

Cwd: `D:\Desktop\crl\20260722_1550_run01\implementation_v011`.

Scientific argv:

```text
evaluate.py --phase development --config config.json --expanded inputs/BFCL_v3_multiple_tool_enrichment.json --questions inputs/BFCL_v3_multiple.json --gold inputs/BFCL_v3_multiple_possible_answer.json --output-dir ../experiment_v011/work/dev_eval_001
```

The capture runner must receive program, config, six model files, and three input files as declared inputs. The fresh capture directory is `experiment_v011/captures/dev_eval_001/`. Declared outputs under `experiment_v011/work/dev_eval_001/` are `raw.jsonl`, `selected_params.json`, `query_hashes.json`, `summary.json`, and `environment.json`.

Before execution, program, config, all model files, and all input files must be saved with `ResearchWorkspace.save_experiment_artifact()`. After execution, `execution.json`, `stdout.bin`, `stderr.bin`, and all five outputs must also be saved. Raw must include every query, gold set, thin/related membership used only for training provenance, complete tool schema, frozen logit, full CLS vector, all three rankings, and both learned scores.

## Confirmation isolation and cluster-aware analysis

P084 Development is already outcome-exposed from v009. Grouped OOF prevents a query or exact duplicate query from fitting its own residual but does not make Development untouched. The paired resampling unit is one row/query. P084 rows share one LLM generation pipeline, so 200 rows are not 200 independent generation mechanisms.

Confirmation must have zero exact query-hash overlap and uses the full-Development frozen adapter unchanged. This provides file/repository-version and exact-query isolation only; it does not prove task-, template-, endpoint-, or entity-disjoint generalization.

## Cost and bundle-level attribution

Capture real wall time, Python, NumPy, SciPy, PyTorch, Transformers, CUDA runtime, GPU capability, driver, model manifest, argv, and all input/config hashes. Total learned-bundle gain is Candidate versus frozen cross-encoder. Anchor attribution requires Candidate versus unanchored adapter; if the anchor does not reduce regressions, no anchor Claim is allowed.

## Leakage, oracle and fixture checks

- Gold labels construct training pairs and metrics only; held-out scoring functions receive frozen query/tool features and a training-fold vector.
- Thin/added membership constructs Development training/anchor pairs only and is not an inference feature.
- Exact duplicate queries remain in one fold.
- Confirmation files remain absent until Promotion Audit authorization.
- Local model loading uses fixed bytes only.
- Schema parsing over all 1,121 Development tools and a synthetic anchor invariant were checked before freeze; those are implementation checks, not research evidence.
- This is not a fixture, Pilot, or old Run011 artifact.

## Direct falsification conditions

Any nonzero scientific execution, missing declared output, unrecomputable raw bytes, changed frozen byte, baseline mismatch, false Development condition, unfair comparator, absence of anchor-specific regression reduction, or material direct-prior collision freezes v011 and advances this Run without Confirmation. After promotion, query overlap, parameter change, false Confirmation condition, or failed raw audit also freezes v011. Reviewer reports and gates cannot replace Main Codex judgment.
