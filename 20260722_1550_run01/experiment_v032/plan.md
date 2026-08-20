# Experiment Plan

```json
{
  "experiment_id": "v032",
  "candidate_sha256": "63fdd82c91a45ad6d162dcf5122ac3cc21bbdde84daa60fcba36264a310f34ec",
  "evidence_packet_sha256": "d867a5d8f8c42efcdd249a89816e6c0c93e8716f3c658211920842afabbfe1c5"
}
```

## Codex Plan

# v032 Frozen Successful-Only Conditional Action Innovation Plan

Status: `FROZEN_BEFORE_DEVELOPMENT`.

This publish-once Plan authorizes one Development execution, one independent
full replay and a Main-Codex Development Promotion Audit. Only a positive
written Promotion Audit may acquire untouched bucket 0. No script, score, gate
count or file existence may authorize Confirmation, Review, Decision, Delivery
or a system-state transition. No subagent is permitted before a complete formal
Review Packet is frozen.

## Frozen identity

- Candidate
  `63fdd82c91a45ad6d162dcf5122ac3cc21bbdde84daa60fcba36264a310f34ec`;
  Evidence Packet
  `d867a5d8f8c42efcdd249a89816e6c0c93e8716f3c658211920842afabbfe1c5`.
- Selection Context
  `628eb93c09bb75d2f8a11ced88c4f248e7bf88311a1d46d309ff9dea3356b36f`;
  Problem
  `7b21c0c30b0f7a857ea71b0129834d85ac4c9c22ce6caab4e7045c75bb8c887f`;
  Research Map
  `a2e0e85810b5b2ab3a80fd4924a49e065e9c563887a312f4ef281dc0a3988c62`;
  Nearest Prior
  `09278ad44261102d0ce962cac856666bec15c2a5db3b9e6dbd39fb8d96b5ac40`.
- Program
  `4875b8c7ecde6772fa25e8b86587fe6d59f210a5505763a8ebc38fb4f2a3cc39`;
  auditor
  `7a0055e44f84eae95d9a185d00b904f2a5439c1392f185bfeceb1f1cd39c9067`;
  tests
  `56fc6c5c89be3d8cda5c00bb3bd654d170d055e7ae7dd9efb92c4aba956d37c7`;
  config
  `ba2637c1338c721b97db5816ebfdaf424d4e09c11e38f5685dca5417987682b3`.
- Base module
  `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`;
  acquisition
  `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`;
  runner
  `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`;
  Implementation Audit
  `4fbbc4ac4118ca524cb67a24434010dbe239953908edde031c14dda65d2039df`.
- Artifact Manifest
  `b0896c58f6e277306f07eeb3170a5c61431d55341d33bb936c58ad84c68a9767`.

The Manifest binds exactly 30 preexecution files totaling 109,220,591 bytes.
Independent rehash found zero missing, unlisted or mismatched files. Exactly
three exposed Development datasets and their three source manifests are
present. No bucket-0 dataset, manifest or Confirmation-output byte is present.

## Fixed computation

For each held-out generator and task fold, a training-only shared char-wb
TF-IDF vocabulary and 64-coordinate randomized SVD map task descriptions and
full stripped action/terminal text to normalized latents. An equal-task-weight
ridge map learns task-to-action coordinates only from successful training rows.

The Candidate appends
`abs(action_latent - W_success(task_latent))` to the direct action-text
classifier. Mandatory controls are direct action text, task/action
concatenation, raw task/action latents, identity innovation and the
equal-capacity all-row conditional innovation.

Every representation, map, scaler and classifier excludes the complete target
generator and held-out task fold. There is no same-task support, role parser,
reasoning trace, exploit category, threshold search, hyperparameter search, LLM
call or external inference tool.

## One Development execution

Before execution, verify `captures`, `dev_output_001` and
`dev_audit_output_001` are absent.

Run frozen `run_local_experiment.py` exactly once:

- capture: `experiment_v032/captures/dev_001`;
- cwd: `experiment_v032/artifacts`;
- declared inputs: all 30 files listed by `artifact_manifest.json`, plus the
  Manifest itself;
- declared outputs under `experiment_v032/dev_output_001`:
  `raw_predictions.jsonl`, `feature_rows.jsonl`, `summary.json`,
  `environment.json` and `model.joblib`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\candidate_v032.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\evidence_packet_v032.md --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket1_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket2_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket3_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket1_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket2_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket3_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v032\dev_output_001
```

Preserve the capture and any outputs regardless of exit. A nonzero exit freezes
v032 as an execution failure without same-version retry.

## One independent Development audit

Only after Development exit `0`, freeze its five outputs and the three
Development capture files. Then run the frozen auditor exactly once through the
same runner:

- capture: `experiment_v032/captures/dev_audit_001`;
- cwd: `experiment_v032/artifacts`;
- declared inputs: all frozen preexecution artifacts, all five Development
  outputs and `dev_001/{execution.json,stdout.bin,stderr.bin}`;
- declared output:
  `experiment_v032/dev_audit_output_001/report.json`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\candidate_v032.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\evidence_packet_v032.md --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket1_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket2_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket3_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket1_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket2_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\development_bucket3_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v032\dev_output_001\raw_predictions.jsonl --feature-rows D:\Desktop\crl\20260722_1550_run01\experiment_v032\dev_output_001\feature_rows.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v032\dev_output_001\summary.json --model D:\Desktop\crl\20260722_1550_run01\experiment_v032\dev_output_001\model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v032\dev_audit_output_001\report.json
```

Support requires exit `0`, `AUDIT_OK`, 4,256 rows, 25,536 OOF scores and exact
recomputation of 1,362,? dense values as actually reported. Every identity
mismatch must be zero and maximum OOF-score, feature, summary and frozen
full-bundle error must be `<=1e-12`. The report's actual dense-value count, not
the explanatory estimate in this sentence, is authoritative.

## Development gates and Main-Codex audit

All gates are conjunctive:

- Candidate AUC `>=0.88`;
- TPR at empirical FPR `<=0.05` `>=0.55`;
- AUC delta `>=0.005` over the strongest mandatory comparator;
- task-bootstrap lower bound `>0`;
- strict AUC superiority over every control;
- all generator deltas nonnegative with at least two positive;
- at least four of five source deltas nonnegative;
- exact byte, coverage, capture and independent-audit integrity.

The main Codex must personally read all raw predictions and feature rows,
identify the strongest comparator, inspect corrections, regressions, generator,
source and task-fold cells, and compare successful-only versus all-row
innovation. Only a positive written `promotion_audit_v032.md` authorizes
Confirmation.

## Conditional untouched Confirmation

Only after a positive Promotion Audit may `acquire.py` run once with
`--phase confirmation`, frozen config and repository commit
`d8a29613235a0ef56a8b70b3142626a533da28c2`, producing bucket 0 in fresh work
and output directories. Dataset and manifest bytes must be frozen before any
reading.

The frozen target-generator-excluded bundles in `dev_output_001/model.joblib`
then score bucket 0 once; the frozen auditor must independently replay
Confirmation once. All Confirmation gates in `research_map_v032.md` and a
separate positive main-Codex raw Confirmation Audit are required before Review.

Only then may a complete neutral Review Packet be frozen and exactly three
simultaneous fresh `default`, `fork_turns=none`, direct leaf Reviewers start,
each exact request containing
`REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Failure handling

Any nonzero scientific/capture execution, missing output, integrity or audit
mismatch, failed gate, or negative Main-Codex audit freezes v032 and advances
the same Run to v033. No same-version retry, latent/ridge/vocabulary/fold/control
or gate retuning, reduced subset, post-hoc subgroup Claim, early Reviewer,
Delivery or Ready transition is allowed.

Run remains `ACTIVE`. System remains `DEVELOPMENT_NOT_COMMISSIONED`.
