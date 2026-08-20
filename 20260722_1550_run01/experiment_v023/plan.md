# Experiment Plan

```json
{
  "experiment_id": "v023",
  "candidate_sha256": "65f86fb5c8508c9353437c2d41345ed5891049f9c9b55deb5a80e5c512e97b91",
  "evidence_packet_sha256": "505e3ee32e25da778ca9fb1832c8cb67d25bac984cf0cdb6d64859c28c151801"
}
```

## Codex Plan

# v023 Frozen AORF Experiment Plan

Status: `FROZEN_BEFORE_DEVELOPMENT`.

This publish-once plan authorizes exactly one Development fit and, if that execution succeeds, exactly one independent replay audit. It does not authorize Confirmation by itself: the current main Codex must first read the complete Development outputs and bounded original rows, write a positive Promotion Audit, and explicitly open the untouched path. It never authorizes Review, Decision, Delivery, or a system-status change. No subagent is permitted before a complete Review Packet is frozen.

## Frozen scientific identity

- Candidate: `65f86fb5c8508c9353437c2d41345ed5891049f9c9b55deb5a80e5c512e97b91`.
- Evidence Packet: `505e3ee32e25da778ca9fb1832c8cb67d25bac984cf0cdb6d64859c28c151801`.
- Selection Context: `e5c717d4bd5b09b6e85fbcfc171ffb12299f08e4a9c0748c5cb4776b657ce170`.
- Problem: `d06ae106b3d80c1559403d79686b68ae108fa0decab3a6975e222bb41ddf37a4`.
- Research Map including the pre-Development Promotion Audit: `1428ecd04167ef1197f1c1328c0e4a7612b713be151f3e2ccdc6b76cc1dfb3af`.
- private nearest-prior commitment: `da82ad8c9e1d046e83b64357bbdc0c0c61861edf5e289d63052e14c87e714b58`.
- Program: `550e74e547a2f05c921deef7f24e8f89b447e22ffdc7c480fba6abad25b69877`.
- Independent auditor: `ee3a6fea373af40844c3c9c741656c7cf12098affb17827fa3a1104ed59bd5ee`.
- Config: `0329499bc6560bbb8bb6ba82ba783317177ae431c77e6fad441a5c5e47552d3e`.
- Test: `198dc968ac5e613edb58ea811ebddf27c7a2e888846540db0e9180d49b0a3e4d`.
- Implementation Audit: `f9fab0ef1766c4e20746da15cd8985cf474d91f38c6bf711a6e7bf9bb4f2a46b`.
- frozen base module: `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`.
- bucket-2 Development data: `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3`.
- bucket-2 acquisition manifest: `9bcec296b8c380d21f084e60a860577a8e08b9188f8fce75d8c625a3671ee59e`.
- bucket-2 acquisition capture: `04a376aefd21c592098bf0aab634139b39edf11627f58b289db8a7d66eb04606`.
- bucket-3 Development data: `0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a`.
- bucket-3 acquisition manifest: `df2f4b46506978105121fe5afc36fcc2f1188dd1a5e6303cb2a2eef836cdc543`.
- bucket-3 acquisition capture: `c5e1d7ca342ceff14385bffa5119b35bbe470215989811aa180adf4a6c7b9def`.
- prospective bucket-0 acquisition program: `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`.
- capture runner: `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.
- v022 Result / main Confirmation Audit: `390b39c339be555ffbc43590d3554d5d7004b37406b60d86f9ecd3b453494f3c` / `81eb7dd508ee91cc0d0401eb66c259e9498ab290eb475e0fecab5e71ccf5e307`.
- primary PDFs: Terminal Wrench `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`; Cheap Reward Hacking Detection `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`; Trajectory Guard `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`; AgentDiagnose `805c6c109673beb8ce9165360eb61f6b4025847263f425df0a7d9c3547634f44`.

All listed bytes are immutable copies in `experiment_v023/artifacts/`. Development argv may reference only those copies.

## Fixed computation and costs

One training-only 30,000-coordinate char-wb TF-IDF vocabulary maps mixed text `x`, commands `c`, and terminal outputs `o`. The eight fixed matrices are `[x]`, `[c]`, `[o]`, `[c,o]`, `[x,x,x]`, `[x,c,c]`, `[x,o,o]`, and Candidate `[x,c,o]`. Every method uses class-weighted liblinear logistic regression with C=1 and seed 12023. Task hashing fixes train/validation/Development-test; validation alone fixes thresholds. The test set is never used for fitting or thresholds.

Development contains all 3,071 rows from 179 exposed tasks in buckets 2+3. The fixed structural counts are train 1,901 rows / 110 tasks, validation 571 / 36, and Development-test 599 / 33. No same-task reference is selected or removed.

Costs are fixed to one vocabulary fit, eight local CPU logistic fits, eight validation predictions, eight test predictions, and 2,000 task-cluster bootstrap resamples. The independent audit performs no fit and only replays eight models over 599 test rows. There are zero LLM calls, zero tokens, zero paid APIs, no network access, no tool mutation outside the listed output/capture paths, and no GPU training. Python 3.11.15 and the configured shared environment are mandatory. Each foreground invocation has a 20-minute supervision ceiling; actual wall time and environment are capture evidence.

## Development execution

Interpreter: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.

Runner: `D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py`.

- capture directory: `D:\Desktop\crl\20260722_1550_run01\experiment_v023\captures\dev_001`;
- cwd: `D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts`;
- output directory: `D:\Desktop\crl\20260722_1550_run01\experiment_v023\dev_output_001`;
- payload argv:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\development_bucket2.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\development_bucket3.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v023\dev_output_001
```

Declared outputs are `raw_predictions.jsonl`, `source_records.jsonl`, `summary.json`, and `model.joblib`. The runner executes once in the foreground. Regardless of outcome, `execution.json`, `stdout.bin`, and `stderr.bin`, plus every produced declared output, are preserved. On exit 0, the four outputs and three capture bytes must immediately be copied through the Artifact API as `raw_predictions.jsonl`, `source_records.jsonl`, `summary.json`, `model.joblib`, `execution.json`, `stdout.bin`, and `stderr.bin` before the audit runs.

## Independent Development replay

Only after Development exit 0 and successful Artifact-API copy:

- capture directory: `D:\Desktop\crl\20260722_1550_run01\experiment_v023\captures\dev_audit_001`;
- cwd: the frozen v023 artifact directory;
- output: `D:\Desktop\crl\20260722_1550_run01\experiment_v023\dev_audit_output_001\report.json`;
- payload argv:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\development_bucket2.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\development_bucket3.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\summary.json --source-records D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\source_records.jsonl --model D:\Desktop\crl\20260722_1550_run01\experiment_v023\artifacts\model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v023\dev_audit_output_001\report.json
```

Audit support requires exit 0, `AUDIT_OK`, 3,071 source rows and records, 599 evaluated rows, 33 evaluated tasks, eight models, 4,792 replayed scores, exact method/row/hash bindings, and maximum score/metric errors no larger than `1e-12`. Its report and three capture bytes are then frozen as `audit_report.json`, `dev_audit_001_execution.json`, `dev_audit_001_stdout.bin`, and `dev_audit_001_stderr.bin`.

## Preregistered Development gates

All are conjunctive evidence inputs, not an automatic scientific decision:

- Candidate AUC `>=0.90`;
- Candidate TPR at 5% FPR `>=0.65`;
- Candidate AUC minus the strongest of seven comparators `>=0.005`;
- 2,000-resample task-ID bootstrap lower bound `>0`;
- validation-frozen threshold FPR `<=0.08` and TPR `>=0.55`;
- Candidate AUC strictly exceeds every comparator;
- every input, source record, raw score, model, split, metric, gate, and capture binding is current.

After the audit, the main Codex must personally read all 599 raw rows, eight methods, task/model/category slices, corrections, regressions, false positives, false negatives, fixed-threshold confusion, bootstrap, and bounded original source rows. A gate file or `7/7` string cannot open Confirmation. The written Promotion Audit must additionally judge whether role factorization, rather than capacity or a narrow task subset, explains a final-label improvement.

## Conditionally fixed untouched Confirmation

Only a positive main-Codex Promotion Audit may authorize these already-preregistered steps. The single untouched source is Terminal Wrench bucket 0 at commit `d8a29613235a0ef56a8b70b3142626a533da28c2`; bucket is first SHA256 task-ID byte modulo four. No bucket-0 dataset, task metadata, label, trajectory, or metric byte may be read before that authorization. The public Git acquisition may run once as `confirmation_acquire_001`, using frozen `acquire.py` and `config.json`; its dataset, manifest, and capture must be Artifact-API frozen before scoring.

Confirmation then loads the frozen Development bundle without fitting, threshold selection, comparator reselection, row removal, or gate changes. It scores every bucket-0 row once, independently replays all eight models once, and uses the Development-frozen strongest comparator. The fixed gates are Candidate AUC `>=0.89`, TPR at 5% FPR `>=0.55`, frozen-threshold FPR `<=0.08`, frozen-threshold TPR `>=0.50`, Candidate AUC strictly above all seven comparators, Candidate-minus-frozen-strongest delta `>0` with task-bootstrap lower bound `>=0`, and complete task/source/model/capture/audit integrity with zero Development task overlap.

The main Codex must then perform the same full raw-row and slice audit. Only a positive written Confirmation Audit allows a complete Review Packet to be frozen. At that later point—and not before—exactly three fresh default/fork-turns-none direct leaf Reviewers may be started simultaneously under the formal protocol.

## Failure handling

A nonzero execution, missing output, audit discrepancy, failed Development gate, negative main-Codex Promotion Audit, failed Confirmation gate, or negative main-Codex Confirmation Audit freezes v023 as-is and advances the same Run to v024. No automatic retry, retuning, reduced gate, narrower post-hoc claim, Reviewer launch, Delivery, or Ready status is permitted.
