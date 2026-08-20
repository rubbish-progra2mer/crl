# Experiment Plan

```json
{
  "experiment_id": "v034",
  "candidate_sha256": "8f78b67bfa14e3f9cbbd94207143e2574c6898913f2045cbb38f1cdb1d750a09",
  "evidence_packet_sha256": "56d2c6e8b911056fafb6c23b856ccbd0992fc20e2205d709694729e2e4f89ead"
}
```

## Codex Plan

# v034 Frozen Contract-Calibrated Conjunctive Bottleneck Plan

Status: `FROZEN_BEFORE_DEVELOPMENT`.

This Plan authorizes exactly one Development execution, one independent
model-replay audit and one main-Codex Promotion Audit. It cannot authorize
Confirmation, Review, Decision, Delivery or a system-state transition.

No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity

- Candidate
  `8f78b67bfa14e3f9cbbd94207143e2574c6898913f2045cbb38f1cdb1d750a09`;
  Evidence Packet
  `56d2c6e8b911056fafb6c23b856ccbd0992fc20e2205d709694729e2e4f89ead`.
- Selection Context
  `c57d31212276a45eab39a4147b02a2aac3eaa5c312c7d864cb7a260222c3b540`;
  Problem
  `2e5114b4150b97ee3670a0ebc64ea23b19b5acf5d5ec851c489e2ed397a0bea3`;
  Research Map
  `3c8848067091ae3b47a96ab93c36ed6574f2712e790074bb8adaa5362ff2f3be`;
  Nearest Prior
  `5fc0f7c5aed338af1e6cafe18211dee40a0495860f1f08404e42b320302bd677`.
- Program
  `a98b6f16b270fa4350bd1cf024bbf240f692d5658eb3be298117867e1d4a8ca4`;
  independent auditor
  `b43735617e0e09c0294f467b187bf4b2c8771c78d35d79e420ae40fd06e629c2`;
  tests
  `3940f8472b87d52a132d122b8cfdefd0c2fb14576c8aa19e64376a911c1fcfb9`;
  config
  `4efd0437ae4987176ec3edc83179e3c2478f6cf5059a89cfbcacc0b171ae237a`;
  Confirmation acquisition
  `fda9a8f4e50042e43eed73b31c801c9bc495d4f53853a28e7769ff54289803f3`.
- Main-Codex Implementation Audit
  `b931acd775fbc051aa5fcef88336b8a44b54f3847bbea6a9a4a7c7d1589eed9a`;
  runner
  `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.
- Artifact Manifest
  `771a15c6f815f223d6945ccbf2cbbf5fffca8a2ebee3d51e82641cf7164a9acf`.

The Artifact Manifest binds 42 records and 1,537,183,940 bytes: 35 immutable
artifact files plus seven external frozen-model files. Independent rehash found
zero missing, mismatched, unlisted or listed-absent file.

It binds all three exposed Development datasets, every primary source and
Card, v033 negative lineage and exact Qwen3-0.6B bytes. It binds no ToolSandbox
dataset, Confirmation output, Review report, Decision or Delivery.

## Fixed computation

Development contains 315 pairs, 630 pointwise actions, 195 clusters and exactly
3,780 prompts. The frozen Qwen3-0.6B model evaluates five fixed obligation
views and one holistic view using next-token `Yes`/`No` log odds.

For each held-out source, other-source unlabeled empirical percentiles
calibrate the five obligations. Candidate:

```text
CCCB(action) = min_k F_k(log p(Yes_k) - log p(No_k))
```

Mandatory comparators are holistic, all five single obligations, raw minimum,
calibrated mean/product, pair majority, other-source-selected single
obligation and fixed-C supervised linear combination. No label-only metadata
enters a prompt.

No prompt search, obligation search, model-size search, generation, sampling,
fine-tuning, external API, tool execution or second model is permitted.

## One Development execution

Before execution, verify these paths are absent:

- `experiment_v034/captures`;
- `experiment_v034/dev_output_001`;
- `experiment_v034/dev_audit_output_001`.

Set:

```text
PYTHONDONTWRITEBYTECODE=1
PYTHONIOENCODING=utf-8
CUDA_VISIBLE_DEVICES=0
```

Run frozen `run_local_experiment.py` exactly once with:

- capture `experiment_v034/captures/dev_001`;
- cwd `experiment_v034/artifacts`;
- declared inputs: every Artifact Manifest record, the Artifact Manifest and
  this frozen Plan;
- declared outputs:
  `dev_output_001/{pointwise_scores.jsonl,raw_predictions.jsonl,summary.json,environment.json,frozen_state.json}`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\candidate_v034.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\evidence_packet_v034.md --model-dir C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca --model-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\model_manifest.json --dataset gta=D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\prmbench_GTA.json --dataset bfcl=D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\prmbench_bfcl.json --dataset tooltalk=D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\prmbench_tooltalk.json --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v034\dev_output_001
```

Preserve capture and any output regardless of exit. Nonzero exit freezes v034
without same-version retry.

## One independent Development audit

Only after Development exit `0`, freeze all five outputs and
`dev_001/{execution.json,stdout.bin,stderr.bin}`.

Run the frozen auditor exactly once through the same runner:

- capture `experiment_v034/captures/dev_audit_001`;
- cwd `experiment_v034/artifacts`;
- declared inputs: every preexecution record, Artifact Manifest, Plan, all five
  Development outputs and all three Development capture files;
- declared output `experiment_v034/dev_audit_output_001/report.json`.

Exact scientific payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\audit.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\candidate_v034.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\evidence_packet_v034.md --model-dir C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca --model-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\model_manifest.json --dataset gta=D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\prmbench_GTA.json --dataset bfcl=D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\prmbench_bfcl.json --dataset tooltalk=D:\Desktop\crl\20260722_1550_run01\experiment_v034\artifacts\prmbench_tooltalk.json --pointwise-scores D:\Desktop\crl\20260722_1550_run01\experiment_v034\dev_output_001\pointwise_scores.jsonl --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v034\dev_output_001\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v034\dev_output_001\summary.json --frozen-state D:\Desktop\crl\20260722_1550_run01\experiment_v034\dev_output_001\frozen_state.json --environment D:\Desktop\crl\20260722_1550_run01\experiment_v034\dev_output_001\environment.json --execution D:\Desktop\crl\20260722_1550_run01\experiment_v034\captures\dev_001\execution.json --stdout-capture D:\Desktop\crl\20260722_1550_run01\experiment_v034\captures\dev_001\stdout.bin --stderr-capture D:\Desktop\crl\20260722_1550_run01\experiment_v034\captures\dev_001\stderr.bin --report D:\Desktop\crl\20260722_1550_run01\experiment_v034\dev_audit_output_001\report.json
```

Support requires auditor exit `0`, `AUDIT_OK`, exactly 315 rows, 630 actions,
3,780 prompt evaluations, zero prompt-hash mismatch, maximum logit/derived
numeric error `<= 1e-6`, exact capture hashes and exact frozen environment.

## Development decision boundary

Every gate in `research_map_v034.md` is conjunctive:

- Candidate accuracy `>=0.60`;
- Candidate-minus-strongest accuracy `>=0.03`;
- cluster-bootstrap lower bound `>0`;
- strict superiority to all mandatory comparators;
- Candidate accuracy `>=0.50` on every Development source;
- all three source deltas nonnegative and at least two positive;
- exact pointwise action-swap invariance;
- current data/model/prompt/output/environment/capture/audit bytes.

After a successful audit, the main Codex must personally read raw pointwise and
pair rows, inspect every source, obligation and comparator, identify corrections
and regressions relative to the strongest control, verify calibration and
linear-control state, and write a Promotion Audit. Only a positive written
Promotion Audit may open ToolSandbox.

## Conditional untouched Confirmation

Only after positive Development gates and Promotion Audit may frozen
`acquire_confirmation.py` download `prmbench_ToolSandbox.json` at the fixed
repository commit. The acquired bytes and capture must be frozen before
reading. The full-Development calibration, selected-single, linear state and
strongest comparator then score Confirmation once, followed by one independent
replay audit.

Only positive Development and Confirmation audits permit a complete formal
Review Packet. Only after that Packet is frozen may exactly three simultaneous
fresh `default`, `fork_turns=none`, direct leaf Reviewers start, with every
exact request containing:

```text
REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN
```

## Failure handling

Any nonzero execution, missing output, audit mismatch, failed gate or negative
main-Codex audit freezes v034 and advances the same Run to v035. No same-version
retry, prompt/obligation/calibration/control/gate/model retuning, reduced
subset, post-hoc source Claim, early Reviewer, Delivery or Ready transition is
allowed.

Run remains `ACTIVE`. System remains `DEVELOPMENT_NOT_COMMISSIONED`.
