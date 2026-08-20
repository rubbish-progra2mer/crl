# Experiment Plan

```json
{
  "experiment_id": "v025",
  "candidate_sha256": "d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60",
  "evidence_packet_sha256": "87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f"
}
```

## Codex Plan

# v025 Frozen VIAF Execution-Correction Plan

Status: `FROZEN_BEFORE_EMPTY_PARENT_PREPARATION_AND_BUCKET1_ACQUISITION`.

This publish-once Plan carries v024's scientific identity unchanged and corrects only its pre-payload directory preparation. It authorizes creation of two empty parent directories, one acquisition of untouched bucket 1, one five-fold task-OOF Development fit and one independent replay audit. It does not authorize Confirmation without a positive written main-Codex Promotion Audit, and never authorizes Review, Decision, Delivery or a status transition. No subagent is permitted before a complete Review Packet is frozen.

## Frozen identity and lineage

- Candidate `d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60`; Evidence Packet `87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f`.
- Selection Context `10cb5ed5c9e67e8eef8c35f926b2cf51ce56c849e7616c97913d274a11fed282`; Problem `bd2d11c1f861ae98e43fee39aedda28de18a05456cdf69d536563cccdf4c9d1e`; Research Map `a775c4e8ac122a482e316699516b319decf4780f0997c2154c5b28f2f87bc034`; nearest-prior carryover `046f1f85659bfc4323f5c1831570e092341c93e3ac7cc78845a729b53ddda95b`; complete v024 prior `4c01037ddd330b41a84f80805239a64ce55774ee92b209a11e7595ba18ac61e5`.
- Program `e71a820adfe798b0732a07dbfe1e31286cad7eab43c229309a9522e34ea44ab6`; auditor `8eade0d127843da37545327622e7be7627592400ca696c05c63aa1a1dcd66c72`; config `e34c812e78d1476e6a283d89452f3f61b3cd7bb74859d11a29fa2202bacf9983`; test `1f334f43fb9222ef625f10732b9f17b072c5439cbfef76709ea28bf5b381a3fb`; Implementation Audit `e7b14242732c2d8c23119e50046d47d5d0fe283f8fc4603b42b7a46d9f88dca3`.
- Base `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`; acquire `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`; runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.
- v024 Plan / Result / attempts / main audit `30e6a7071686e036a7738b9af4d42b5f705949862b906740032799cd71c1f217` / `5a4dbd7636c6056e286efacf1292d22f2ce28e8bcd15d798e624dfeafa435d28` / `521e02d57e11075b5cc1cc1fe528a317ff1384dee9d6eca8adea3764f472db09` / `993cdab1120f8c51d8d47beba7c5cf19a7d6fd0fd817fb12aeb256b91e00dc4d`.
- Primary PDFs: Terminal Wrench `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`; Cheap Reward Hacking Detection `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`; Trajectory Guard `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`; TrajAD `3237bcd13e7f2926c3f3cd3891c661ea398f57f1cb347523c87a217a73278fec`; AgentRx `59680fd631934d6ad3046108a504195e8cd70066bdefbfb3561b7731f7d22923`; Strained Coherence `33a2ee601361ab3c538732133ff2a937c93f765f112451a9bf96899d9fce3271`.

All bytes are immutable copies in `experiment_v025/artifacts/`. The v025 program/auditor/config differ from v024 only in five version-identity strings; all scientific code, hyperparameters and tests are otherwise identical.

## Fixed Claim and computation

Only the frozen bounded Claim is allowed: on task-disjoint Terminal Wrench stripped actions, assigning separate shared-vocabulary coefficients to commands before versus at/after the first fixed label-free verifier-inspection batch improves reward-hack detection over all six controls. No causal, universal, reasoning-trace or first-ever novelty Claim is permitted.

The first batch containing a fixed inspection executable at a whitespace/shell-separator boundary and a fixed non-alphanumeric-delimited checker token is the anchor. No anchor means `before=all`, `from_anchor=empty`. Methods are `[x]`, `[c]`, `[c,o]`, `[x,c,c]`, `[x,h1,h2]`, `[x,am,an]`, and VIAF `[x,b,a]`. Each training fold alone fits one char-wb TF-IDF vocabulary (3–5 grams, min-df 2, max 30,000) and seven class-weighted liblinear logistic models, C=1, seed 12024.

Task SHA-256 byte 1 modulo four fixes bucket 1 Development and bucket 0 Confirmation. Commit-tree-only inspection established 71 and 81 task names. Their metadata, labels and trajectories remain unopened. Exposed buckets 2+3 cannot support v025 metrics.

## Exact empty-parent preparation

After Plan publication and before the unique runner call, create only:

- `D:\Desktop\crl\20260722_1550_run01\experiment_v025\captures`;
- `D:\Desktop\crl\20260722_1550_run01\experiment_v025\work`.

Then verify both are empty directories and these children are absent: `captures/dev_acquire_001`, `dev_acquire_output_001`, and `work/dev_acquire_001`. This is the only execution correction. Do not edit the frozen runner, add a retry, or create output/attempt child directories manually.

## One Development acquisition

Using shared Python 3.11.15, run frozen runner once, capture `captures/dev_acquire_001`, cwd frozen artifacts, outputs `dev_acquire_output_001/dataset.jsonl` and `manifest.json`, work root `work/dev_acquire_001`, payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\acquire.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\config.json --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v025\dev_acquire_output_001 --work-root D:\Desktop\crl\20260722_1550_run01\experiment_v025\work\dev_acquire_001
```

Preserve capture and any outputs regardless of exit. Exit 0 also requires fixed/checked-out commit `d8a29613235a0ef56a8b70b3142626a533da28c2`, bucket 1/modulus 4, exactly 71 predesignated tasks, Python 3.11.15, current config/dataset bindings and complete source hashes. Before fitting, Artifact-freeze `development_dataset.jsonl`, `development_manifest.json`, and `dev_acquire_001_execution/stdout/stderr`.

## One Development execution

After acquisition freezing, run once with capture `captures/dev_001`, cwd artifacts and output `dev_output_001`:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\development_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\development_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v025\dev_output_001
```

SHA-256 task byte 2 modulo five fixes folds. Every row is OOF once; other folds alone fit vocabulary/models. Seven full Development models are fit once solely for conditional Confirmation. Fixed cost is 42 local CPU logistic fits and 2,000 task-cluster bootstrap resamples, with no LLM call, paid API or GPU training. Preserve and Artifact-freeze raw predictions, source records, summary, model and three capture bytes before audit.

## One independent replay

Then run frozen auditor once, capture `captures/dev_audit_001`, report `dev_audit_output_001/report.json`:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\development_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\development_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\summary.json --source-records D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\source_records.jsonl --model D:\Desktop\crl\20260722_1550_run01\experiment_v025\artifacts\model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v025\dev_audit_output_001\report.json
```

Support requires exit 0, `AUDIT_OK`, all rows/tasks/source records, 35 fold-model replays, seven scores per row, exact bindings and maximum score/metric error `<=1e-12`. Freeze report and audit capture.

## Development evidence gates and main audit

Conjunctive evidence inputs are VIAF AUC `>=0.94`; TPR@5%FPR `>=0.75`; AUC delta over strongest comparator `>=0.005`; 2,000-task-bootstrap lower bound `>0`; strict superiority over every comparator; positive VIAF-minus-command-duplicated AUC among anchored rows; the same delta `>=-0.005` among unanchored rows; and complete integrity. Booleans do not authorize promotion.

The main Codex must personally inspect all raw rows and bounded sources, fold/task/model/source/anchor slices, candidate-only/comparator-only orderings, errors, bootstrap and concentration. Only a positive written audit attributing improvement beyond capacity, fixed time and checker-word presence may open bucket 0.

## Conditional untouched Confirmation

Only that written approval permits one bucket-0 acquisition (`confirmation_acquire_001`) with new immutable paths and artifact freezing before scoring. Frozen full-Development models then score each bucket-0 row once without fitting, row removal, comparator reselection or gate changes; one independent replay follows. Gates are AUC `>=0.93`, TPR@5%FPR `>=0.70`, delta versus frozen strongest `>0` with bootstrap lower `>=0`, strict superiority over all six, positive anchored delta, unanchored delta `>=-0.01`, zero task overlap and complete integrity. The main Codex must repeat the raw audit.

Only a positive written Confirmation Audit permits a complete Review Packet. Then—and not before—exactly three fresh `default`, `fork_turns=none`, direct leaf Reviewers may start simultaneously with `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN` in each request.

## Failure handling

Any nonzero acquisition/execution, missing output, audit mismatch, failed gate or negative main audit freezes v025 and advances the same Run. No same-version retry, predicate/weight/regularization/gate/task/Claim retuning, reduced comparators, post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is allowed. The Run remains ACTIVE unless user-paused or genuinely externally blocked.
