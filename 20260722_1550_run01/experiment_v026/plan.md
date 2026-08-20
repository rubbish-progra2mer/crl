# Experiment Plan

```json
{
  "experiment_id": "v026",
  "candidate_sha256": "b43922594122236b08fcdd94836a5731a8d1cc91c49e7a0a918b51a225bc5f61",
  "evidence_packet_sha256": "0ad0e89d9dc7a690d4c4b586d10e37504df23c4a2e9d1a4541a1794dd9c1b3f8"
}
```

## Codex Plan

# v026 Frozen CMCD Plan

Status: `FROZEN_BEFORE_DEVELOPMENT_EXECUTION`.

This publish-once Plan authorizes exactly one Development fit on the already exposed immutable union of Terminal Wrench buckets 1–3, one independent frozen-model replay, and the main Codex's raw Promotion Audit. Only a positive written Promotion Audit may open untouched bucket 0 for one acquisition, one frozen Confirmation score and one independent replay. It never lets a script, gate count or file existence authorize Confirmation, Review, Decision, Delivery or a system-state transition. No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity and evidence

- Candidate `b43922594122236b08fcdd94836a5731a8d1cc91c49e7a0a918b51a225bc5f61`; Evidence Packet `0ad0e89d9dc7a690d4c4b586d10e37504df23c4a2e9d1a4541a1794dd9c1b3f8`.
- Selection Context `dd1103b1f6bcf1036fcfcb07846519ccea75143445ad9b9a3e9a09f9acc705d8`; Problem `684374ba6b5dc74070429275a0e9dba7cab8067f957f4ac1c555e777fe386785`; Research Map `932c5a7e37565b2f060df4f141e2c4db4660342f275a34ee58b0456066378f23`; nearest prior `ef6bdfbdde465a052e188e18a90b9dcc3da97e4fff08703d1d6d29070a607963`.
- Program `d709235915e1406fa65c38b567773bc1fa43e3aad6be71e66bdd1b845053d2e1`; independent auditor `1676eecf7886b8a76047da8c50458b9855749bbede297fddebee90a9c9e83f3f`; config `9b784ed930a5514fe57a40c484519ca6d32c09ef45e9f0a091c35af2d84dd0c9`; tests `f7accf7ea298e99765e4d87c594bff479d71b1e6c07269184d2ad3efc4fae9fc`; Implementation Audit `09d14ee91e2ec83f4e3bec8793bac78b6bf05c48616d7c977e6ca5551e2e8e13`.
- Shared base `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`; acquisition program `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`; execution capture runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.
- Development bucket 1 dataset/manifest `d5daecba36e3e8f9c6bbe60c8e2b13e6206290d8ca7cddcf4a8cc27c2f82274f` / `aa20ea73e71b7a3b9a41d444c8a8b7997216f0b85e53fbc5cffb663e25b67932`; bucket 2 `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3` / `9bcec296b8c380d21f084e60a860577a8e08b9188f8fce75d8c625a3671ee59e`; exposed bucket 3 `0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a` / `df2f4b46506978105121fe5afc36fcc2f1188dd1a5e6303cb2a2eef836cdc543`.
- The bucket-3 manifest truthfully retains its v022 `phase=confirmation`; config freezes original acquisition phases as Development, Development and Confirmation respectively. All three are now exposed and may only be v026 Development. Bucket 0 has not been acquired, read or listed at row/task/label/trajectory level.
- Primary prior PDFs are frozen: Terminal Wrench `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`, Cheap Reward Hacking Detection `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`, Trajectory Guard `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`, D²4FAD `c8f9aa621915f8e1ecb3945155eb5bf06580f74214f3d9d88be520154a5231f7`, UniVAD `c20e32751c4f7b6332606a810ec07be854af0afb4c9202619a5822936d5b55a9`, LOTTERY `1bc52603140c3afee187346364aaa160f90c1e0678a36c10c3618e370b055096`.

All named bytes are immutable API copies under `experiment_v026/artifacts/`. v021, v022 and v025 Result/audit lineage is also frozen there. The source audit and six focused tests passed before this Plan, but those checks are not experimental evidence.

## Fixed computation and claim boundary

The eligible Development population is fixed prospectively to tasks having at least one successful baseline from all three frozen generator families. The pre-score structural check found 228/250 tasks, 4,072/4,256 rows and 22 exclusions. No row may be removed after scores exist.

For target generator `m` and task fold `f=SHA256(task_id)[1] mod 3`, training queries exclude fold `f` and generator `m`; their successful same-task supports exclude both query and target generators. Held-out rows have generator `m` and fold `f`, and their supports are all successful same-task rows from the other two generators. A training-only char-wb TF-IDF vocabulary uses 3–5 grams, min-df 2 and max 20,000. Class-weighted liblinear logistic regression uses C=1, max-iter 2,000 and seed 12026. Pair weights total one per query and pair class weights derive from query-class counts.

Methods are `direct=[q]`, capacity control `triple_query=[q,q,q]`, no-deviation control `consensus_no_abs=[q,r,r]` mean-aggregated over all supports, aggregation control `single_support=[q,r,abs(q-r)]` using the lexicographically first support with the frozen Candidate pair model, and Candidate `cross_model_consensus=[q,r,abs(q-r)]` mean-aggregated over all supports. No vocabulary, support selector, pair weighting, C, fold, eligibility rule, comparator, gate or Claim may change.

The maximum conditional Claim remains the Candidate document's fixed Terminal Wrench representation-and-transfer statement. No generic few-shot anomaly, support weighting, unseen-model universality, online monitor, causal verification, cross-benchmark or first-ever claim is permitted.

## Exact Development execution

After Plan publication, create only the empty parent `D:\Desktop\crl\20260722_1550_run01\experiment_v026\captures`. Verify `captures/dev_001`, `dev_output_001`, `captures/dev_audit_001` and `dev_audit_output_001` are absent. Then invoke the frozen runner exactly once from the frozen-artifact cwd. The payload is:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\candidate_v026.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\evidence_packet_v026.md --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket1_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket2_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket3_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket1_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket2_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket3_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v026\dev_output_001
```

The runner capture is `captures/dev_001`; declared outputs are `model.joblib`, `raw_predictions.jsonl`, `source_records.jsonl` and `summary.json`. Fixed cost is 12 training-only vectorizers, 48 local CPU logistic fits and 2,000 task-cluster bootstrap resamples, with no LLM call, paid API or GPU training. Preserve all bytes regardless of exit. On exit 0, API-freeze the four outputs and the three runner capture files before audit.

## One independent Development replay

Run the frozen auditor exactly once through the same runner, capture `captures/dev_audit_001`, report `dev_audit_output_001/report.json`, using the frozen Development outputs copied into `artifacts/`:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\candidate_v026.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\evidence_packet_v026.md --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket1_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket2_dataset.jsonl --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket3_dataset.jsonl --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket1_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket2_manifest.json --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\development_bucket3_manifest.json --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\summary.json --source-records D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\source_records.jsonl --model D:\Desktop\crl\20260722_1550_run01\experiment_v026\artifacts\model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v026\dev_audit_output_001\report.json
```

Support requires exit 0, `AUDIT_OK`, exact bindings, 4,072 evaluated rows, nine OOF bundles, all five scores per row and maximum score/metric error `<=1e-12`. Freeze report and capture before interpretation.

## Development gates and main Promotion Audit

Conjunctive evidence gates are Candidate AUC `>=0.88`; TPR at empirical 5% row FPR `>=0.55`; Candidate-minus-strongest-comparator AUC `>=0.005`; 2,000-task-bootstrap lower bound `>0`; strict AUC superiority over all four controls; Candidate-minus-strongest AUC nonnegative for all three held-out generators and positive for at least two; eligible-task fraction `>=0.90`; complete integrity.

The main Codex must personally join every raw row to frozen source/support bytes and inspect task, fold, target generator, source dataset, support count, class, corrections/regressions and concentration. It must determine whether any gain belongs to the absolute-deviation/multi-support delta rather than capacity, reference presence, task identity or one generator/source. Only a positive natural-language `promotion_audit_v026.md` may open bucket 0. Gate booleans cannot authorize it.

## Conditional untouched Confirmation

Only after a positive Promotion Audit, run one bucket-0 acquisition with frozen `acquire.py`, config and runner, capture `captures/confirmation_acquire_001`, output `confirmation_acquire_output_001`, and work root `work/confirmation_acquire_001`. Freeze dataset, manifest and capture before scoring. The manifest must bind commit `d8a29613235a0ef56a8b70b3142626a533da28c2`, bucket 0/modulus 4, current config SHA and complete source hashes.

Then run `program.py --phase confirmation` exactly once with the same Candidate/Evidence/config/base, the frozen bucket-0 dataset/manifest, `--model artifacts/model.joblib`, and new `confirmation_output_001`. No fitting, support reselection, comparator reselection or gate change is allowed. Freeze raw/source/summary and capture. Run `audit.py` once on those frozen bytes, using the same frozen Development model, and freeze its report/capture.

Confirmation gates are Candidate AUC `>=0.86`; TPR@5%FPR `>=0.50`; strict superiority over all four controls; AUC delta versus the frozen Development strongest comparator `>0` with task-bootstrap lower bound `>=0`; per-generator deltas all nonnegative and at least two positive; eligible-task fraction `>=0.90`; zero Development task overlap; complete integrity. The main Codex must repeat the raw audit. Only its positive written Confirmation Audit permits a complete formal Review Packet.

After the Packet is fully frozen—and not before—exactly three simultaneous fresh `default`, `fork_turns=none`, direct leaf Reviewers may be started, each request containing `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Failure handling

Any nonzero execution, missing output, audit mismatch, failed conjunctive gate or negative main audit freezes v026 as a negative attempt and advances this same Run to v027. No same-version retry, CMCD retuning, reduced comparator set, altered eligibility, weaker gate, post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is allowed. The Run remains `ACTIVE` unless the user pauses or a genuine external blocker occurs; the product remains `DEVELOPMENT_NOT_COMMISSIONED`.
