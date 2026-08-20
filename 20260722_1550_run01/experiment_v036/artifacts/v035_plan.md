# Experiment Plan

```json
{
  "experiment_id": "v035",
  "candidate_sha256": "0e6b148cc7ac87d997c4df0c89eb427c25107b455fc14271c98549adc8ecfd79",
  "evidence_packet_sha256": "c735d5a91e04518c48ba1e9867062a2cbe289626af68acbb29a4184e2dc698ff"
}
```

## Codex Plan

# v035 Frozen Symmetric Differential Evidence Judgment Plan

Status: `FROZEN_BEFORE_DEVELOPMENT`.

This Plan authorizes exactly one Development execution, one independent
model-replay audit and one main-Codex Promotion Audit. It cannot authorize
Confirmation, Review, Decision, Delivery or a system-state transition.

No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity

- Candidate
  `0e6b148cc7ac87d997c4df0c89eb427c25107b455fc14271c98549adc8ecfd79`;
  Evidence Packet
  `c735d5a91e04518c48ba1e9867062a2cbe289626af68acbb29a4184e2dc698ff`.
- Selection Context
  `ec3ea8a4eb17951bbee007648a58aaa8387e0faad9aa6055d02532155653dd56`;
  Problem
  `38e874aa95002ab5d2584129eac63a94ecda9282a220aa2ce114c24cb6d5a0de`;
  Research Map
  `c89b2510d85c931caf86cef4a55732bc7a06333e3edc39f1d61faa3a7d4e1a45`;
  Nearest Prior
  `417242fd378db2a188d288855a2d228365ccdc9a4203e6826b22a4c6688ac70e`.
- Program
  `f3a1fa0ac4b69daa4a629701f223ff595ffa430014c25755142cffd536e0ac64`;
  independent auditor
  `591a89bad636f5bfd8e86d487f9eaf014b0c604f9a838a03ea5f1fb19525f2a8`;
  tests
  `27fa74d6b278c57e872f0ba868084eebb3866a084eab4ad5df6aff2914eb0371`;
  config
  `f1ad651c0804422e534ba53fb87d2a6295f633f17659d730b38edc68e50e6d92`;
  Confirmation acquisition
  `a26821f7df2554490da04469d088abc9ebeeeadd1e4a0e941136062eaa3d6c14`.
- Main-Codex Implementation Audit
  `8863f2320eee2710dfc9e0a67e15cfe213967d0a8fdb3091b01df235a43c043b`;
  runner
  `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.
- Artifact Manifest
  `c0c180ee340eca25c17e3f091c459efc8925eb4751c6ffab88ade4ff9fe1fef0`.

The Artifact Manifest binds 34 records and 1,530,540,760 bytes: 27 artifact
files plus seven external frozen-model files. Independent rehash found zero
missing, mismatched or duplicate-name records.

It binds no ToolSandbox dataset, Confirmation output, Review report, Decision
or Delivery.

## Fixed computation

Development contains 315 pairs, 195 source/task clusters and exactly 2,520
prompts. The Candidate deterministically:

1. parses action mode, tool and recursive argument fields;
2. removes exactly shared canonical fields;
3. retains candidate-specific field or word/punctuation-token differences;
4. selects implicated contracts or an explicit system-message fallback;
5. scores `A`/`B` in both orders and averages aligned probabilities.

Mandatory controls are:

- order-symmetric complete actions (`full_pair`);
- independent complete-action `Yes`/`No` scoring (`full_pointwise`);
- order-symmetric differences without evidence (`delta_no_evidence`);
- original-order-only Candidate prompt (`delta_forward`).

No fitting, calibration, threshold search, source tuning, generation, external
API, tool execution or second model is permitted.

## One Development execution

Before execution, verify these paths are absent:

- `experiment_v035/captures`;
- `experiment_v035/dev_output_001`;
- `experiment_v035/dev_audit_output_001`.

Set:

```text
PYTHONDONTWRITEBYTECODE=1
PYTHONIOENCODING=utf-8
CUDA_VISIBLE_DEVICES=0
```

Run frozen `run_local_experiment.py` exactly once with:

- capture `experiment_v035/captures/dev_001`;
- cwd `experiment_v035/artifacts`;
- declared inputs: all 34 Artifact Manifest records, the Artifact Manifest and
  this frozen Plan;
- declared outputs:
  `dev_output_001/{raw_predictions.jsonl,summary.json,environment.json,frozen_state.json}`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\config.json --model-dir C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca --model-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\model_manifest.json --dataset gta=D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\prmbench_GTA.json --dataset bfcl=D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\prmbench_bfcl.json --dataset tooltalk=D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\prmbench_tooltalk.json --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v035\dev_output_001
```

Preserve capture and any output regardless of exit. A nonzero scientific
payload exit freezes v035 without same-version retry.

## One independent Development audit

Only after Development exit `0`, freeze all four outputs and
`dev_001/{execution.json,stdout.bin,stderr.bin}`.

Run the same capture runner exactly once with:

- capture `experiment_v035/captures/dev_audit_001`;
- cwd `experiment_v035/artifacts`;
- all frozen inputs plus the four Development outputs and three Development
  capture files;
- output `experiment_v035/dev_audit_output_001/report.json`.

Exact audit payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\audit.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\config.json --model-dir C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca --model-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\model_manifest.json --dataset gta=D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\prmbench_GTA.json --dataset bfcl=D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\prmbench_bfcl.json --dataset tooltalk=D:\Desktop\crl\20260722_1550_run01\experiment_v035\artifacts\prmbench_tooltalk.json --raw D:\Desktop\crl\20260722_1550_run01\experiment_v035\dev_output_001\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v035\dev_output_001\summary.json --report D:\Desktop\crl\20260722_1550_run01\experiment_v035\dev_audit_output_001\report.json
```

Any nonzero audit exit or numeric error above `1e-6` is a Development failure.
There is no same-version repair.

## Conjunctive Development gates

The main Codex may write a positive Promotion Audit only if:

1. SDEJ accuracy is at least `0.70`;
2. SDEJ exceeds the strongest mandatory control by at least `0.025`;
3. the source-cluster bootstrap 95% lower bound for that delta is greater than
   `0`;
4. SDEJ accuracy is at least `0.58` on each source;
5. source deltas are all nonnegative and positive on at least two sources;
6. SDEJ strictly exceeds `full_pair` and `full_pointwise`;
7. `delta_no_evidence` is strictly worse than SDEJ;
8. the independent audit exits `0` and reproduces all listed values.

All conditions are conjunctive. The main Codex must also inspect raw
corrections, regressions, order behavior and source concentration. Scripts do
not authorize promotion.

## Conditional untouched Confirmation

Only a positive Promotion Audit permits exactly one execution of frozen
`acquire_confirmation.py`. It must acquire the 130-row ToolSandbox file at
repository commit `b43164fbb2cd2963e1906a6fe62a86e7ce05973e`, record its
HTTP status, bytes and SHA, and never overwrite it.

The frozen program and Development state then run once on ToolSandbox,
followed by one independent audit. Confirmation gates are exactly those in
`candidate_v035.md`; failure freezes v035 and forbids Review.

Only a positive main-Codex Confirmation Audit permits a formal Review Packet.
Only after that Packet is fully frozen may the main Codex start exactly three
fresh direct-leaf Reviewers.

