# Experiment Plan

```json
{
  "experiment_id": "v031",
  "candidate_sha256": "fdbbf978279d8a7fbfaea35ab9949054a8f671126ef2e641c9180b24f5948bd0",
  "evidence_packet_sha256": "86a06e5e0432decdc6dfbd28e2c501449f8b02662f2402dca96872dd4e5ebfa3"
}
```

## Codex Plan

# v031 Frozen MGTR Plan

Status: `FROZEN_BEFORE_DEVELOPMENT`.

This publish-once Plan authorizes one Development execution, one independent full replay and the Main Codex Development Promotion Audit. Only a positive written Promotion Audit may acquire untouched bucket 0. No gate count, script or file existence may authorize Confirmation, Review, Decision, Delivery or a system-state transition. No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity

- Candidate `fdbbf978279d8a7fbfaea35ab9949054a8f671126ef2e641c9180b24f5948bd0`; Evidence Packet `86a06e5e0432decdc6dfbd28e2c501449f8b02662f2402dca96872dd4e5ebfa3`.
- Selection Context `cf6bbeccc45e31f90a5c07aa407bd6031cc3e5078538d67f7167725b2520c1dd`; Problem `7b67e73f005012af73e6fd9e1bd585755650855deb876ea752ab87783226d565`; Research Map `6d9bdb9d39b93649d3879f33f9b24e881ec2f816abe1cf733f70996691f52670`; Nearest Prior `78022d4ed5c53a7f9d03caf76dfbef81a2d25477f69aa6f3780f9a4afc5a8671`.
- Program `2bd01db3af6b9e448df4cebbbd53d7e1bcf811f2bd588577954deaebecb18300`; auditor `b5e923337bf698f8d7a66a5519e757bf42aa245dd08c5effe7e8da1c7dddb3c5`; tests `13d3b8f9e28b633d0506d2e616652a05d66209f06225f004233d60a4d95cb347`; config `e98e37614cec3ce86bce8fd70f0634678e93b58f29c94734299d591d832dff55`.
- Base parser `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`; conditional acquisition `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`; runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`; Implementation Audit `575d0d5645e42ce0a3c0cbade22b776f448a1db1eb9facdcb2616032e1baa665`.
- Artifact Manifest `e3fba3cb822cde4405221c839149ef40dc111f57a6aa464af809d2312c98d60a`.

The Artifact Manifest binds exactly 31 preexecution files totaling 191,272,292 bytes. Independent rehash found zero missing, unlisted or mismatched files. It contains exactly three exposed Development datasets, three corresponding acquisition manifests and six cross-encoder files. No bucket-0 or Confirmation-output byte is present.

## Fixed computation

MGTR splits every stripped trajectory into command segments, assigns each segment one frozen label-free operation role, scores each `(task description, command segment)` pair with frozen `cross-encoder/ms-marco-MiniLM-L-6-v2`, and pools fraction/minimum/mean/maximum/population-standard-deviation separately for mutation, verification, read and other roles.

The Candidate appends those 20 features to direct action/terminal character TF-IDF. Mandatory controls are direct text, task/action concatenation, direct text plus four role fractions, direct text plus global relevance, and direct text plus equal-capacity chronological relevance. Every method uses the same balanced logistic regression and the same double holdout: its scoring bundle excludes the complete target generator and the held-out task fold.

Development contains 4,256 unique rows, 250 tasks and 444,000 task-command pairs. There is no threshold search, model acquisition, retry, category input, successful-trajectory reference, cross-model support or per-slice tuning.

## One Development execution

Before execution, verify `captures`, `dev_output_001` and `dev_audit_output_001` are absent. Create only the empty `captures` directory.

Run frozen `run_local_experiment.py` exactly once:

- capture: `experiment_v031/captures/dev_001`;
- cwd: `experiment_v031/artifacts`;
- declared inputs: all 31 files listed by Artifact Manifest plus `artifact_manifest.json`;
- declared outputs: `pair_scores.jsonl`, `feature_rows.jsonl`, `raw_predictions.jsonl`, `summary.json`, `model.joblib` and `environment.json` under `experiment_v031/dev_output_001`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket1_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket2_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket3_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket1_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket2_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket3_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\base_v012.py --model-dir D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\model_cross --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v031\dev_output_001
```

Preserve capture and any outputs regardless of exit. A nonzero exit freezes v031 as an execution failure without same-version retry.

## One independent Development audit

Only after Development exit `0`, freeze its six outputs and capture bytes. Create the previously absent empty `dev_audit_output_001` directory, then run the frozen auditor exactly once through the same runner:

- capture: `experiment_v031/captures/dev_audit_001`;
- cwd: `experiment_v031/artifacts`;
- declared inputs: all frozen preexecution artifacts, all six Development outputs and the Development capture bytes;
- declared output: `experiment_v031/dev_audit_output_001/report.json`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\audit.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket1_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket2_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket3_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket1_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket2_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\development_bucket3_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\base_v012.py --model-dir D:\Desktop\crl\20260722_1550_run01\experiment_v031\artifacts\model_cross --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v031\dev_output_001 --report D:\Desktop\crl\20260722_1550_run01\experiment_v031\dev_audit_output_001\report.json
```

Support requires exit `0`, `AUDIT_OK`, 4,256 rows, 444,000 pairs and maximum errors no greater than `1e-6` for cross scores, `1e-12` for dense features, `1e-10` for OOF/frozen-model predictions and `1e-12` for metrics/gates.

## Development gates and Main-Codex audit

All gates in `research_map_v031.md` are conjunctive: exact bytes and coverage; Candidate AUC `>=0.88`; TPR at empirical FPR `<=0.05` `>=0.55`; AUC delta `>=0.0075` over the strongest mandatory comparator; task-bootstrap lower bound `>0`; strict AUC superiority over every control; all generator slices nonnegative with at least two positive; at least four of five source slices nonnegative; exact independent audit.

The Main Codex must personally read the raw predictions and pair/feature rows; identify the strongest comparator; inspect corrections, regressions, low-relevance mutations, role ablations and generator/source slices; and judge whether any gain is stable operation-role concentration rather than exposed-data tailoring, output length, a single generator/source or a direct text effect. Only a positive written `promotion_audit_v031.md` authorizes Confirmation.

## Conditional untouched Confirmation

Only after that positive Promotion Audit may frozen `acquire.py` run once with `--phase confirmation`, the frozen config, repository commit `d8a29613235a0ef56a8b70b3142626a533da28c2`, output `experiment_v031/confirmation_acquire_output_001` and a fresh `experiment_v031/work/confirmation_acquire_001`. Bucket 0 dataset and manifest bytes must be frozen before reading.

The frozen full target-generator bundles in `dev_output_001/model.joblib` then score bucket 0 exactly once with `program.py --phase confirmation`; the auditor replays it exactly once. Confirmation requires the conjunctive Research Map gates and a separate Main-Codex raw Confirmation Audit.

Only positive Development and Confirmation audits permit a complete formal Review Packet. Only after that Packet is frozen may exactly three simultaneous fresh `default`, `fork_turns=none`, direct leaf Reviewers start, each request containing `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Failure handling

Any nonzero scientific/capture execution, missing output, integrity/audit mismatch, failed gate or negative Main-Codex audit freezes v031 and advances the same Run to v032. No same-version retry, feature/role/model/control/gate/Claim retuning, reduced subset, post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is allowed. Run remains `ACTIVE`; system remains `DEVELOPMENT_NOT_COMMISSIONED`.
