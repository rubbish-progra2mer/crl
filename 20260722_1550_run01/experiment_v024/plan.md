# Experiment Plan

```json
{
  "experiment_id": "v024",
  "candidate_sha256": "d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60",
  "evidence_packet_sha256": "87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f"
}
```

## Codex Plan

# v024 Frozen VIAF Experiment Plan

Status: `FROZEN_BEFORE_BUCKET1_ACQUISITION`.

This publish-once plan authorizes one acquisition of predesignated untouched Development bucket 1, one five-fold task-OOF Development fit, and—only after successful artifact freezing—one independent replay audit. It does not authorize Confirmation: the current main Codex must personally read all Development evidence and write a positive Promotion Audit first. It never authorizes Review, Decision, Delivery or a status change. No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity

- Candidate `d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60`; Evidence Packet `87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f`.
- Selection Context `3784287c7f93eb42aa8bd776f2c3f9fdb93391336f509d6d6674d82604b28690`; Problem `bd2d11c1f861ae98e43fee39aedda28de18a05456cdf69d536563cccdf4c9d1e`; Research Map `a775c4e8ac122a482e316699516b319decf4780f0997c2154c5b28f2f87bc034`; nearest prior `4c01037ddd330b41a84f80805239a64ce55774ee92b209a11e7595ba18ac61e5`.
- Program `d47337fdf7cf9d6863c4efebb18abb9c7d80d72aec9a86df89cf28adbfd95437`; auditor `7b0ec0a85d15ca6127ecadbf57d48e96a559d672dc2fea88e9cbeb73e7988dc7`; config `3e588a5d2052814b7bb64bc2cfc2d71d8838ded02fe2ab35ab8877f0f1faddd9`; test `1f334f43fb9222ef625f10732b9f17b072c5439cbfef76709ea28bf5b381a3fb`; Implementation Audit `56fd37fbc5b851adb5510b8d2cd691d2a6042c04db19690f022ddbee57f94ab0`.
- Base module `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`; acquisition program `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`; capture runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.
- v023 Result / Promotion Audit / attempts `8fb3cf684631c3996dfa0d9664266d283231d483a9be48d84e695c2df7926723` / `ef9e892b449236ca4ec1f5b9b77c03f65d4716a0b33ec722a3b2f1a29ffd046d` / `0003061496894f74991406fedd65e0e0d42317a2fe7ec7e7b1d6e022ea221cc7`.
- PDFs: Terminal Wrench `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`; Cheap Reward Hacking Detection `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`; Trajectory Guard `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`; TrajAD `3237bcd13e7f2926c3f3cd3891c661ea398f57f1cb347523c87a217a73278fec`; AgentRx `59680fd631934d6ad3046108a504195e8cd70066bdefbfb3561b7731f7d22923`; Strained Coherence `33a2ee601361ab3c538732133ff2a937c93f765f112451a9bf96899d9fce3271`.

All listed bytes are immutable copies in `experiment_v024/artifacts/`; acquisition and scientific argv may reference only those copies.

## Claim, computation and isolation

Only the bounded frozen Claim is promotable: on fixed task-disjoint Terminal Wrench stripped actions, separate shared-vocabulary coefficients for commands before versus at/after the first fixed label-free verifier-inspection batch improve reward-hack detection over all six controls. No causal, universal, reasoning-trace or first-ever novelty Claim is authorized.

The first fixed inspection-executable plus non-alphanumeric-delimited checker-token batch is the anchor. With no anchor, `before=all` and `from_anchor=empty`. Methods are `[x]`, `[c]`, `[c,o]`, `[x,c,c]`, `[x,h1,h2]`, `[x,am,an]`, and Candidate `[x,b,a]`. Within every training fold, one char-wb TF-IDF vocabulary (3–5 grams, min-df 2, max 30,000) is fit on training-task mixed text only and transforms all blocks. Every method uses class-weighted liblinear logistic regression, C=1, seed 12024.

SHA-256 task byte 1 modulo four fixes bucket 1 as Development and bucket 0 as Confirmation. A commit-tree-only view established 71 and 81 task names respectively. Neither bucket's metadata, labels nor trajectories were opened at publication. Exposed buckets 2+3 may not support a v024 metric.

## One Development acquisition

Use `D:\Desktop\crl\crl_agent_v3\.venv\python.exe` (Python 3.11.15) and frozen runner once:

- capture `experiment_v024/captures/dev_acquire_001`;
- cwd `experiment_v024/artifacts`;
- output `experiment_v024/dev_acquire_output_001`;
- work root `experiment_v024/work/dev_acquire_001`;
- payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\acquire.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\config.json --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v024\dev_acquire_output_001 --work-root D:\Desktop\crl\20260722_1550_run01\experiment_v024\work\dev_acquire_001
```

Declared outputs are `dataset.jsonl` and `manifest.json`. Preserve capture and produced outputs regardless of exit. Exit 0 additionally requires repository/checked-out commit `d8a29613235a0ef56a8b70b3142626a533da28c2`, bucket 1/modulus 4, exactly the 71 tree-predesignated tasks, Python 3.11.15, current config/dataset bindings and complete source hashes. Before fitting, Artifact-freeze them as `development_dataset.jsonl`, `development_manifest.json`, `dev_acquire_001_execution.json`, `dev_acquire_001_stdout.bin`, and `dev_acquire_001_stderr.bin`.

## One Development fit

After acquisition freezing, run once with capture `captures/dev_001`, cwd frozen artifacts, output `dev_output_001`:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\development_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\development_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v024\dev_output_001
```

SHA-256 task byte 2 modulo five fixes folds. Every row is OOF once; the other four task folds alone fit vocabulary and seven models. Seven full-Development models are fit once only for conditional Confirmation. Total fixed cost is 42 local CPU logistic fits and 2,000 task-cluster bootstrap resamples, with no LLM calls, paid API or GPU training. Preserve and freeze `raw_predictions.jsonl`, `source_records.jsonl`, `summary.json`, `model.joblib`, `execution.json`, `stdout.bin`, and `stderr.bin` before audit.

## One independent replay

After Development freezing, run frozen `audit.py` once, captured as `captures/dev_audit_001`, cwd frozen artifacts, report `dev_audit_output_001/report.json`:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\development_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\development_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\summary.json --source-records D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\source_records.jsonl --model D:\Desktop\crl\20260722_1550_run01\experiment_v024\artifacts\model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v024\dev_audit_output_001\report.json
```

Audit support requires exit 0, `AUDIT_OK`, all rows/tasks/source records, 35 fold-model replays, seven scores per row, exact input/model/raw/fold/metric/gate bindings, and maximum errors `<=1e-12`. Freeze report and three audit capture bytes.

## Development evidence gates and main audit

All seven are conjunctive evidence inputs, not authorization: VIAF AUC `>=0.94`; TPR@5%FPR `>=0.75`; AUC delta over strongest comparator `>=0.005`; 2,000-task-bootstrap lower bound `>0`; strict AUC superiority over every comparator; positive VIAF-minus-command-duplicated AUC among anchored rows; the same delta `>=-0.005` among unanchored rows; plus complete byte integrity.

The main Codex must personally inspect all raw predictions and bounded source rows, fold/task/model/source/anchor slices, candidate-only/comparator-only orderings, false positives/negatives, bootstrap and concentration. Only a positive written Promotion Audit attributing improvement beyond capacity, fixed time and checker-word presence may open bucket 0.

## Conditional untouched Confirmation

Only that written approval authorizes one bucket-0 acquisition as `confirmation_acquire_001`, frozen before scoring. The full Development bundle then scores every bucket-0 row once without fitting, row removal, comparator reselection or gate changes; the frozen strongest Development comparator remains primary. One independent replay follows. Gates are VIAF AUC `>=0.93`, TPR@5%FPR `>=0.70`, delta versus frozen strongest `>0` with bootstrap lower `>=0`, strict superiority over all six, positive anchored delta, unanchored delta `>=-0.01`, zero task overlap and complete integrity. The main Codex must conduct the same raw audit.

Only a positive written Confirmation Audit permits a complete formal Review Packet. Then—and not before—exactly three fresh `default`, `fork_turns=none`, direct leaf Reviewers may start simultaneously with `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN` in each request.

## Failure handling

Any nonzero acquisition/execution, missing output, audit mismatch, failed gate, negative main-Codex audit, failed Confirmation, or negative Review/Decision freezes v024 and advances this same Run to v025. No same-version retry, predicate/weight/regularization/gate/task/Claim retuning, reduced comparator set, post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is allowed. The Run stays ACTIVE unless the user pauses or a genuine external blocker occurs.
