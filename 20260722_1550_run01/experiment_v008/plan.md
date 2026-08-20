# Experiment Plan

```json
{
  "experiment_id": "v008",
  "candidate_sha256": "3952ebd104e457c10b03ab43b2092695156c66d8c7dfbb628a53725bd13febea",
  "evidence_packet_sha256": "dc66e45036069b3ab310b3ee3e60b929e70a91de5f0994335d09886040882be9"
}
```

## Codex Plan

# v008 Typed Partial Parameter Alignment

## Frozen Before Results

Frozen at `2026-07-23T15:24:26.7053495+08:00`, before any v008 scientific execution or Confirmation acquisition.

- Candidate SHA-256: `3952ebd104e457c10b03ab43b2092695156c66d8c7dfbb628a53725bd13febea`.
- Evidence Packet SHA-256: `dc66e45036069b3ab310b3ee3e60b929e70a91de5f0994335d09886040882be9`; five Evidence entries, all PDF and passage bytes current.
- Program: `implementation_v008/evaluate.py`, SHA-256 `657b710318b850c11a02bc6ad7b836d19ae8dc348251cdb546043fa8171a6888`.
- Config: `implementation_v008/config.json`, SHA-256 `999db63c02c0b57e93f9cc6fe9efc47f11a7ff6e7058defd490cbac0a3323c2d`.
- Dense model: 11 files, 91,578,415 bytes, copied-manifest SHA-256 `4b198bddf01a386c84da55537d837090679fc8d04cb464c3de90b1312cab368b`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
- Cross-encoder: 6 files, 91,815,758 bytes, copied-manifest SHA-256 `c1690f252da82d084467a98fb08169c6e16a5b574928c8af72fd86774ee2dd2a`, revision `c5ee24cb16019beea0893ab7796b1df96625c6b8`.

The program, config, every model file, and all Development input files must be saved through `ResearchWorkspace.save_experiment_artifact()` before execution. Any later scientific-byte change requires v009.

## Data Acquisition And Sampling Contract

Development uses all 200 aligned IDs from:

- `BFCL_v3_multiple_tool_enrichment.json`, 582,498 bytes, SHA-256 `1be15f014a2d04af06fec2797e4e53f7a335ce46e6bdc2ec0ef3cabd6074a7b`, from `ibm-research/BFCL-FC-robustness@2ec93e790cf5fa3753d477a83cd596115387f1c5`.
- `BFCL_v3_multiple.json`, 316,583 bytes, SHA-256 `aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a`, from `ShishirPatil/gorilla@c15b2a151662cac9839c96d7dfb1493b5329c975`.
- `BFCL_v3_multiple_possible_answer.json`, 32,254 bytes, SHA-256 `244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047`, from the same BFCL commit.

There is no sampling or replacement. The expanded menu is evaluated; the original file verifies the unchanged question; answers are used only for metrics and one global Development tuple. `perturbed_question` and original-menu membership are not scored inputs.

Untouched Confirmation is fixed as `BFCL_v4_live_multiple.json` and `possible_answer/BFCL_v4_live_multiple.json` from `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`. Those bytes have not been downloaded or read. They may be acquired only after a successful Development capture and a Main Codex Promotion Audit. No replacement Confirmation source is allowed if overlap or coverage is unsuitable.

## Primary Metric And Mechanism Signature

Top-1 is one when the first ranked function belongs to the row's ground-truth function set. MRR uses the highest-ranked ground-truth function. Multi-gold rows therefore measure top-1 membership and best-gold MRR, not complete call-set recall.

Development selects one of 384 global tuples by top-1, MRR, lower fusion weight, lower type bonus, lower unmatched-required penalty, then lower null threshold. The relaxed comparator reuses that tuple. The primary delta is TPPA minus the identical cross-encoder. Paired item bootstrap uses 20,000 resamples and seed `20260723`.

The preregistered parameter-contrast subset contains rows where the highest-scoring gold function and strongest non-gold distractor are within `0.5` cross-encoder z units and have different required-parameter type multisets. Labels define this analysis subset only and never enter inference.

Development conditions are: top-1 delta at least `+0.02`; paired MRR-delta bootstrap lower bound above zero; corrections exceed regressions; and TPPA top-1 advantage is larger inside the nonempty contrast subset than outside. These mechanical conditions do not promote the Candidate automatically. The Main Codex must independently recompute the raw outputs, assess comparator fairness and target-failure coverage, and write the Promotion Audit.

## Closest Composition, Neutral Comparators, And Delta Ablation

All methods use the identical query, menu, and full-schema construction. Neutral methods are BM25, frozen MiniLM query-to-schema cosine, frozen cross-encoder, cross-encoder plus relaxed reusable matching, and cross-encoder plus TPPA. The relaxed matcher uses identical spans, edge features, selected tuple, and fusion weight; only one-use capacity is removed. This is the executable delta ablation, not a claimed reproduction of Meta-Tool or ToolDreamer.

No method receives gold names, original-menu membership, perturbed requests, generated hypothetical tools, or Confirmation labels at inference. Exact ties use function-name SHA-256 for every method.

## Development Capture And Artifact Bindings

Interpreter: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`. Cwd: `D:\Desktop\crl\20260722_1550_run01\implementation_v008`.

Scientific argv:

```text
evaluate.py --phase development --config config.json --expanded inputs/BFCL_v3_multiple_tool_enrichment.json --questions inputs/BFCL_v3_multiple.json --gold inputs/BFCL_v3_multiple_possible_answer.json --output-dir ../experiment_v008/work/dev_eval_001
```

The runner receives the program, config, all 17 model files, and all three Development files as declared inputs. Capture directory is `experiment_v008/captures/dev_eval_001/` and must not exist before execution. Declared outputs are `raw.jsonl`, `selected_params.json`, `query_hashes.json`, `summary.json`, and `environment.json` in `experiment_v008/work/dev_eval_001/`; none may exist before execution.

The capture's `execution.json`, `stdout.bin`, and `stderr.bin`, all five scientific outputs, program, config, 17 model files, and three inputs must be retained as Experiment Artifacts. Raw must contain complete queries, schemas, gold sets, spans, offsets, types, edge features, realized edge scores, threshold margins, assignments, scores, rankings, and tie order.

## Confirmation Capture Contract

If and only if the Main Codex Promotion Audit authorizes acquisition, the two pinned Confirmation files are copied into `implementation_v008/inputs/`, saved as Experiment Artifacts, and hashed before execution. The same frozen program/config/models run from the same cwd with:

```text
evaluate.py --phase confirmation --config config.json --expanded inputs/BFCL_v4_live_multiple.json --questions inputs/BFCL_v4_live_multiple.json --gold inputs/BFCL_v4_live_multiple_possible_answer.json --selected-params ../experiment_v008/work/dev_eval_001/selected_params.json --development-query-hashes ../experiment_v008/work/dev_eval_001/query_hashes.json --output-dir ../experiment_v008/work/confirmation_eval_001
```

Confirmation uses attempt `confirmation_eval_001`, a fresh capture directory, and the same five output names under its work directory. The Development tuple is loaded unchanged; the Confirmation branch performs no grid search. Query-hash overlap must be empty. Confirmation conditions are positive top-1 delta, positive MRR delta, nonnegative top-1 paired-bootstrap lower bound, and corrections greater than regressions. They still require a Main Codex raw audit before Review Packet authorization.

## Isolation And Analysis Unit

The paired resampling unit is one benchmark row/query; per-tool pairs are never treated as independent observations. Development contains 200 fixed P084 requests, not generated variants. Confirmation is repository-version and dataset-file separated and must be exact-query-hash disjoint. This isolation does not prove task-, template-, endpoint-, or open-world generalization.

## Cost And Bundle Attribution

The cross-encoder pair scores are identical for baseline and Candidate. Dense full-schema encoding supports the MiniLM baseline. TPPA additionally encodes extracted spans and required-parameter texts and solves small CPU assignments; relaxed reuses those features. There are no paid APIs, generated tokens, external inference tools, or retries. Real wall time, interpreter, packages, GPU, CUDA runtime, driver, model manifests, seeds, argv, and hashes are captured.

The primary comparison identifies the full TPPA addition to the cross-encoder. The relaxed comparison isolates capacity/null from reusable matching. It does not separately identify extraction, typing, embedding, fusion, or tuning effects.

## Leakage, Oracle, And Fixture Checks

- Confirmation bytes remain absent through Development and Promotion Audit.
- Gold is read only by evaluation, global Development selection, and analysis-subset construction; raw scoring functions receive no gold.
- Original-menu membership and P084 perturbed requests are unused.
- Model paths are local fixed snapshots; no remote model download is allowed during capture.
- This is a real 200-row Development evaluation, not a fixture or Run011-style sanity.

## Direct Falsification Conditions

A nonzero scientific execution, missing or nonrecomputable raw output, changed frozen byte, false Development condition, target-failure absence, unfair comparator, or bundle-only effect that cannot support the narrow Claim freezes v008 and advances the same Run to v009 without opening Confirmation. After promotion, any Confirmation query overlap, false Confirmation condition, nonrecomputable output, or material prior collision also freezes v008. Gates, file existence, and later Reviewer votes never substitute for Main Codex scientific judgment.
