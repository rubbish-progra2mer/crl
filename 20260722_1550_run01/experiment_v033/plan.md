# Experiment Plan

```json
{
  "experiment_id": "v033",
  "candidate_sha256": "2fd145cce11845463d765dababf8160e5a575502aa20ccee2e631368472824ce",
  "evidence_packet_sha256": "b6ec4b27d4e3c052a6b3072b69202bc128b09ec60cdc14b621e8798f7763d040"
}
```

## Codex Plan

# v033 Frozen Successful-Only Conditional Action Innovation Plan

Status: `FROZEN_BEFORE_DEVELOPMENT`.

This is the execution-only preparation repair of unexecuted v032. Scientific
computation, data, implementation, hyperparameters, seed, controls and gates
are unchanged. This Plan authorizes exactly one Development execution, one
independent full replay and a Main-Codex Promotion Audit. It cannot authorize
Confirmation, Review, Decision, Delivery or a system-state transition.

No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity

- Candidate
  `2fd145cce11845463d765dababf8160e5a575502aa20ccee2e631368472824ce`;
  Evidence Packet
  `b6ec4b27d4e3c052a6b3072b69202bc128b09ec60cdc14b621e8798f7763d040`.
- Selection Context
  `0fb8ec237b914e824f4b9a9ac1c1ec934ce312381817f84b7311a4fae71c9a4a`;
  Problem
  `bfb6853952cf6a5d1894a7d5807a15951c921bc76e533ba025ca881669784990`;
  Research Map
  `3d811279b5cc2c8e33c889df345df237a4ade0e9131497f7bfddcf82edc28d27`;
  Nearest Prior
  `13c6e299720f45e2784725bda00085aeef5bef456825c38a86990823d97d40ac`.
- Program
  `4875b8c7ecde6772fa25e8b86587fe6d59f210a5505763a8ebc38fb4f2a3cc39`;
  independent auditor
  `7a0055e44f84eae95d9a185d00b904f2a5439c1392f185bfeceb1f1cd39c9067`;
  tests
  `56fc6c5c89be3d8cda5c00bb3bd654d170d055e7ae7dd9efb92c4aba956d37c7`;
  config
  `7b5333e38a9ede666cf7fc2ae116e40b5c3e32e37df7d135dab5758e34875e13`.
- Base module
  `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`;
  acquisition
  `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`;
  runner
  `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`;
  Implementation Audit
  `a095ef104180ded576a921110dd9b6bf86f7a8e61eb95292c047b97db4e1eb38`.
- Artifact Manifest
  `34b0551ecf099d924450aebe0160419534aa324e67f7c7d29064fce4d1a00b08`.

The Artifact Manifest binds 33 files and 109,230,561 bytes. Independent rehash
found zero missing, mismatched or unlisted file. It binds three exposed
Development datasets and manifests plus v032 preparation-failure lineage. No
bucket-0 dataset, manifest or Confirmation output exists.

## Fixed computation and exact feature count

Each OOF bundle excludes one complete generator and one task fold. A
training-only shared char-wb TF-IDF plus 64-coordinate SVD produces normalized
task and action latents. An equal-task-weight ridge map fitted only on
successful training rows predicts normal action latent from task latent.

Candidate:

```text
[direct_action_tfidf, abs(action_latent - W_success(task_latent))]
```

Mandatory controls are direct action text, task/action concatenation, raw
task/action latent addition, identity innovation and equal-capacity all-row
conditional innovation.

The independent audit must recompute exactly:

```text
4,256 × (128 + 64 + 64 + 64) = 1,361,920 dense feature values
4,256 × 6 = 25,536 OOF method scores
```

No same-task support, role parser, reasoning trace, exploit category,
hyperparameter search, threshold search, LLM call or external inference tool is
permitted.

## One Development execution

Before execution, verify these paths are absent:

- `experiment_v033/captures`;
- `experiment_v033/dev_output_001`;
- `experiment_v033/dev_audit_output_001`.

Run `run_local_experiment.py` exactly once with:

- capture `experiment_v033/captures/dev_001`;
- cwd `experiment_v033/artifacts`;
- declared inputs: all 33 Manifest-listed files plus
  `artifact_manifest.json`;
- declared outputs: `dev_output_001/raw_predictions.jsonl`,
  `feature_rows.jsonl`, `summary.json`, `environment.json` and
  `model.joblib`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\candidate_v033.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\evidence_packet_v033.md --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket1_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket2_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket3_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket1_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket2_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket3_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v033\dev_output_001
```

Preserve capture and any output regardless of exit. Nonzero exit freezes v033
without same-version retry.

## One independent Development audit

Only after Development exit `0`, freeze its five outputs and the
`dev_001/{execution.json,stdout.bin,stderr.bin}` capture bytes.

Run the frozen auditor exactly once through the same runner:

- capture `experiment_v033/captures/dev_audit_001`;
- cwd `experiment_v033/artifacts`;
- declared inputs: all preexecution artifacts, all five Development outputs and
  all three Development capture files;
- declared output `experiment_v033/dev_audit_output_001/report.json`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\candidate_v033.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\evidence_packet_v033.md --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket1_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket2_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket3_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket1_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket2_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\development_bucket3_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v033\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v033\dev_output_001\raw_predictions.jsonl --feature-rows D:\Desktop\crl\20260722_1550_run01\experiment_v033\dev_output_001\feature_rows.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v033\dev_output_001\summary.json --model D:\Desktop\crl\20260722_1550_run01\experiment_v033\dev_output_001\model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v033\dev_audit_output_001\report.json
```

Support requires exit `0`, `AUDIT_OK`, 4,256 rows, 1,361,920 dense values,
25,536 OOF scores, zero identity mismatch and maximum OOF-score, feature,
summary and frozen-full-bundle error `<=1e-12`.

## Development decision boundary

All gates in `research_map_v033.md` are conjunctive:

- Candidate AUC `>=0.88`;
- TPR@5%FPR `>=0.55`;
- Candidate-minus-strongest AUC `>=0.005`;
- task-bootstrap lower bound `>0`;
- strict superiority to all five controls;
- all generator deltas nonnegative, at least two positive;
- at least four of five source deltas nonnegative;
- exact bytes, coverage, capture and audit integrity.

After a successful audit, the main Codex must personally read raw predictions
and feature rows, inspect corrections, regressions and every
generator/source/fold slice, and compare successful-only to all-row innovation.
Only a positive written Promotion Audit may open Confirmation.

## Conditional untouched Confirmation

Only after that positive Promotion Audit may frozen `acquire.py` run once for
bucket 0 with the frozen config and repository commit. The acquired dataset and
manifest must be frozen before reading. Frozen target-generator-excluded
Development bundles then score it once, and the frozen auditor independently
replays it once.

Only positive Development and Confirmation audits permit a complete formal
Review Packet. Only after that Packet is frozen may exactly three simultaneous
fresh `default`, `fork_turns=none`, direct leaf Reviewers start, with each exact
request containing `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Failure handling

Any nonzero execution, missing output, audit mismatch, failed gate or negative
main-Codex audit freezes v033 and advances the same Run to v034. No same-version
retry, feature/ridge/SVD/vocabulary/fold/control/gate retuning, reduced subset,
post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is
allowed.

Run remains `ACTIVE`. System remains `DEVELOPMENT_NOT_COMMISSIONED`.
