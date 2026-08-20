# Experiment Plan

```json
{
  "experiment_id": "v036",
  "candidate_sha256": "de3eb8e0eac0a384d252cac64ba67ce8c6d7c4e2fc5f8c1c2dff81f9aa121840",
  "evidence_packet_sha256": "51d528370f7a81e6683db7f4af2da1507dd1e3b86c1ebe2fad3cc9a75a7f11f8"
}
```

## Codex Plan

# v036 Frozen SDEJ Execution-Only Correction Plan

Status: `FROZEN_BEFORE_DEVELOPMENT`.

This Plan authorizes one Development execution, one independent replay audit
and one main-Codex Promotion Audit. It cannot authorize Confirmation, Review,
Decision, Delivery or a system-state transition. No subagent is permitted.

## Frozen identity

- Candidate:
  `de3eb8e0eac0a384d252cac64ba67ce8c6d7c4e2fc5f8c1c2dff81f9aa121840`;
- Evidence Packet:
  `51d528370f7a81e6683db7f4af2da1507dd1e3b86c1ebe2fad3cc9a75a7f11f8`;
- Program:
  `ac23300356663662e9529f0ec5feb8440447c51fdf1bd12d6e9927bc99f14aba`;
- auditor:
  `710fdd75f683f41f81c5e402628ce04407889ec547d141d78252c065810f44e3`;
- config:
  `ce8ed62cdbc68753226aa07f9c417de60c75a47a115785d1444bc38366001c26`;
- Implementation Audit:
  `b8a97aa2d835446682f79c537d602f2de8bdfe3e393cd95fd3a4414d4ea1e92b`;
- runner:
  `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`;
- Artifact Manifest:
  `a95cb1382de55ac63640a517a64bfbf575b439a270b98352ee67fc2da883ec84`.

The Manifest binds 44 records and 1,530,572,938 bytes: 37 artifact files and
seven external frozen-model files. Independent rehash found zero missing,
mismatched or duplicate-name records. ToolSandbox is not bound or present.

## Scientific invariance

The exact SDEJ computation, 315 Development pairs, 195 clusters, 2,520 prompts,
four controls, bootstrap, gates and Claim ceiling are unchanged from v035.
v036 changes only the frozen model placement operation from unavailable
`device_map` loading to `dtype=float16` followed by `.to("cuda")` in both
program and auditor. The shared environment is unchanged.

## One Development execution

Before execution verify absent:

- `experiment_v036/captures`;
- `experiment_v036/dev_output_001`;
- `experiment_v036/dev_audit_output_001`.

Set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONIOENCODING=utf-8` and
`CUDA_VISIBLE_DEVICES=0`.

Use frozen `run_local_experiment.py` with capture
`experiment_v036/captures/dev_001`, cwd `experiment_v036/artifacts`, all 44
Manifest records plus the Manifest and this Plan as declared inputs, and these
declared outputs:

- `dev_output_001/raw_predictions.jsonl`;
- `dev_output_001/summary.json`;
- `dev_output_001/environment.json`;
- `dev_output_001/frozen_state.json`.

Exact payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\config.json --model-dir C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca --model-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\model_manifest.json --dataset gta=D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\prmbench_GTA.json --dataset bfcl=D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\prmbench_bfcl.json --dataset tooltalk=D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\prmbench_tooltalk.json --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v036\dev_output_001
```

A nonzero payload exit closes v036 without retry.

## One independent audit

Only after Development exit `0`, run one captured audit with all frozen
inputs, all four Development outputs and the three Development capture files.
Output is `dev_audit_output_001/report.json`.

Exact payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\audit.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\config.json --model-dir C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca --model-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\model_manifest.json --dataset gta=D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\prmbench_GTA.json --dataset bfcl=D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\prmbench_bfcl.json --dataset tooltalk=D:\Desktop\crl\20260722_1550_run01\experiment_v036\artifacts\prmbench_tooltalk.json --raw D:\Desktop\crl\20260722_1550_run01\experiment_v036\dev_output_001\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v036\dev_output_001\summary.json --report D:\Desktop\crl\20260722_1550_run01\experiment_v036\dev_audit_output_001\report.json
```

Audit exit must be `0` and maximum numeric error at most `1e-6`.

## Unchanged conjunctive gates

1. SDEJ accuracy at least `0.70`;
2. delta over strongest control at least `0.025`;
3. bootstrap lower 95% bound greater than `0`;
4. every source accuracy at least `0.58`;
5. no negative source delta and at least two positive sources;
6. strict superiority to `full_pair` and `full_pointwise`;
7. strict superiority to `delta_no_evidence`;
8. successful independent reproduction.

The main Codex must inspect raw corrections, regressions, order behavior and
source concentration before its Promotion Audit. Scripts cannot authorize
Confirmation.

Only a positive Promotion Audit permits the fixed 130-row untouched
ToolSandbox acquisition and one unchanged Confirmation plus audit. Only a
positive main-Codex Confirmation Audit permits a formal Review Packet.

