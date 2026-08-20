# Experiment Plan

```json
{
  "experiment_id": "v013",
  "candidate_sha256": "50ad937e5aa6df51e76223ef002a675273902a59d71170082d05c222db61fff5",
  "evidence_packet_sha256": "1e8563b6eccb27dacef35f2c0b277b80c1742ce2ebc2ad83984053a59cb3c96e"
}
```

## Codex Plan

# v013 Policy-Level BoR Consistency Audit

## Frozen before Development

This one-shot Plan is frozen after candidate definition and main-Codex implementation audit, but before any v013 Development parser, BM25 ranking, DQN fitting, raw policy row, metric, or gate result has been executed. Selection exposure is disclosed: the target notebooks, their preserved outputs, and BFCL v3 simple bytes were read while identifying the inconsistency. Development is a reproduction/audit set; only the prospectively fixed BFCL v4 file can serve as untouched Confirmation.

- Selection Context SHA-256: `0D32EA2D3F55B5CCB05BBC0B7A03CFE04E30D3106F809A9B697D9FA20436D5F7`.
- Problem SHA-256: `1F5FC32FCF8632126173C57283E0A76D3567047BA248BC45FC8162976106875B`.
- Research Map SHA-256: `23C0E7D4E3E183A7F38563D9377C69B3712FB0FB309DF3A5A870C5FBA6F556F5`.
- Nearest Prior SHA-256: `20E62887DCC3C88622D4388E86F3B9DA1A9C1C70C34FA1E0572AFC779BF83CB3`.
- Candidate SHA-256: `50AD937E5AA6DF51E76223EF002A675273902A59D71170082D05C222DB61FFF5`.
- Evidence Packet SHA-256: `1E8563B6ECCB27DACEF35F2C0B277B80C1742CE2EBC2AD83984053A59CB3C96E`; its three formal Evidence entries and passages are current.
- Main-Codex implementation audit SHA-256: `06B701B044AE64FE3B2441D6041B779A287AD1443DA6496BFA3D72DE10CE27DA`.
- Evaluation/training program SHA-256: `EA92265ABF4B6D2FE8B6838F424B17E383F8361C0FC65658FE25FCC96B82F9E8`.
- Independent audit program SHA-256: `990A33893A98AF7C4996D89A754CB67861729840E729C8A424E382CA3E1212DE`.
- Formula test SHA-256: `9AE5104A273C9045C33B7E420B5DFA5444E7C289911C7CFAE1D78D6A6EC78CFD`.
- Config SHA-256: `6FB1FCDAD39AB7D3080900FC0EF1C47F998456ABB9A895D4961E1CB04BD8E7BA`.

The implementation checks recorded in `implementation_audit_v013.md` are code checks only. They do not constitute Development, Confirmation, research evidence, or Delivery.

## Fixed source identities

| Artifact | Fixed identity | SHA-256 |
|---|---|---|
| Target paper PDF | arXiv:2605.24660 | `4DB89BFAC79BC90DD5B532D04AC1012ED1691657A45379BBBB2312682847164C` |
| Target official repository | commit `9759eb9f0e7ed90ff289d34300acc15453f7851a` | clean checkout |
| Target main notebook | same commit | `61DA53127597D7A90A440A87FF2EFCEA77665454852D50552DF9BB2972A6FF81` |
| Target second notebook | same commit | `35C2CB2B624C0D364F196A3DB7493F0C7502AF120228410673A587460B2D85C3` |
| Target preserved BM25 result rows | same commit | `8872DB7F8528560419AB74AAE8D1F268C193AECE3E670CC11F96B15C336EFB93` |
| Original BoR paper PDF | arXiv:2605.18857 | `8587A2502CF4F5FA371A04EACA3EEC4D782AD52D0A12F346606EE2FFD4B3EC02` |
| Official BoR repository | commit `746ef2466c24e0f810d2dde1b35db5c481949db6` | clean checkout |
| Official aggregate auditor | same commit | `3DA2D063CCD78242686F54D3FDCD2E89A1E318BA20C6DAD4261F64552A8645C8` |
| Official metric primitives | same commit | `5D1E282B72B267314C8DA83B3FBA192D40FDD97A7FDB8D9D69943EAC34F6724D` |
| `rank-bm25` wheel | PyPI 0.2.2 | `7BD4A95571ADADFC271746FA146A4BCFD89C0CF731E49C3D1AD863290ADBE8AE` |

No source repository may be pulled, updated, or substituted after this Plan.

## Development input and split

Input:

```text
D:\Desktop\crl\20260722_1550_run01\sources_v013\bfcl_development\BFCL_v3_simple.json
```

- Source commit: `ShishirPatil/gorilla@c15b2a151662cac9839c96d7dfb1493b5329c975`.
- SHA-256: `FBC37B2AD252BF9AF985582E0E07B456173FE627D957491472EA9CEF5FB83158`.
- Expected nonempty lines: `400`.
- Registry and query extraction exactly follow the fixed target notebook.
- After BM25 ranking, shuffle once with Python seed `42`.
- Training is the first `floor(0.7 * 400) = 280` queries.
- Development test is the remaining `120` queries.
- Test rows are never used to fit DQN weights.

The parser freezes query IDs, gold ranks, train/test IDs, input SHA, and every input-line SHA.

## BM25 and policy protocol

The `rank-bm25==0.2.2` wheel is loaded directly from fixed bytes without installation. Corpus and query tokens are lowercase whitespace splits.

Policies:

- target BoR-reward DQN;
- F1-reward DQN;
- fixed `K ∈ {1, 3, 5, 10, 20, 50}`.

DQN protocol:

- architecture `7 → 64 → 64 → 2`, ReLU;
- one CPU model per policy and seed;
- seeds `42`, `123`, `456`;
- 15,000 episodes per model;
- replay capacity 20,000;
- batch size 64;
- Adam learning rate `0.001`;
- gamma `0.95`;
- intermediate step cost `0.005`;
- epsilon `0.5`, then `0.1` after 40% of episodes, then `0.03` after 70%;
- target network copied every 500 episodes;
- maximum depth `min(N, 100)`.

One unique raw row is saved per Development query/policy/seed. The target notebook's five evaluation repeats are deterministic duplicates; omitting those duplicates cannot change any mean or ordering.

## Frozen metrics

For every row:

```text
h_i = 1 if gold_rank_i <= K_i else 0
p_i = K_i / N_i
```

Target notebook statistic:

```text
S_notebook = mean_i[h_i * -log2(p_i)]
```

Paper-defined aggregate:

```text
S_defined = log2(mean_i[h_i] / mean_i[p_i])
```

The defined value is independently computed with the direct expression and the fixed official `bits_over_random` primitive. All policies use identical frozen query rows under both metrics.

Pairwise order is evaluated separately for each DQN seed, with deterministic fixed-K policies reused as the seed-matched controls. A strict reversal requires nonzero differences of opposite sign at tolerance `1e-12`.

## Reproduction tolerances

Against the preserved official BM25 notebook output:

- mean BoR-DQN found fraction within `0.03` of `0.903`;
- mean BoR-DQN K within `1.0` of `7.4`;
- mean F1-DQN found fraction within `0.03` of `0.889`;
- mean F1-DQN K within `1.0` of `6.4`;
- every fixed-K found fraction within `0.01` of its fixed official value:
  - K1 `0.600`;
  - K3 `0.7833333333333333`;
  - K5 `0.825`;
  - K10 `0.850`;
  - K20 `0.875`;
  - K50 `0.9083333333333333`.

These tolerances were fixed before execution because the official notebook did not pin PyTorch or `rank-bm25` runtime versions.

## Bootstrap

The preregistered comparison is `FK3 - FK1`.

- Unit: query ID.
- Resamples: `20,000`.
- Seed: `20260723`.
- Each resample applies the same sampled query indices to both policies.
- Report the observed difference, percentile 95% interval, probability positive, and probability negative under each metric.

No other pair can replace `FK3 - FK1` for a Development or Confirmation gate.

## Development promotion gates

Every gate is conjunctive:

1. Exactly one valid unique row per required query/policy/seed; `1 <= K <= N`; `hit == (gold_rank <= K)`; all metrics finite.
2. Maximum stored-reward error relative to `hit * -log2(K/N)` is `<= 1e-12`.
3. Direct defined BoR and the fixed official primitive differ by `<= 1e-12` for every group.
4. All official reproduction tolerances pass.
5. `FK3 - FK1` is strictly positive under `S_notebook` and strictly negative under `S_defined`.
6. At least two of three seeds have a strict reversal involving a learned policy and a fixed-K policy.
7. In at least one seed, the policy maximizing `S_notebook` differs from the policy maximizing `S_defined`.
8. The coupled bootstrap gives probability `>= 0.95` to positive `FK3 - FK1` under `S_notebook` and probability `>= 0.95` to negative `FK3 - FK1` under `S_defined`.

No field produced by either script authorizes promotion. After the independent audit, the main Codex must read raw rows, inspect all group summaries/reversals, verify source and model bindings, and write a Promotion Audit.

## Untouched Confirmation

Confirmation content has not been acquired or read. Only its Git-tree metadata was inspected.

After and only after all Development gates pass and the main Codex records positive promotion, acquire:

```text
repository: ShishirPatil/gorilla
commit: 6ea57973c7a6097fd7c5915698c54c17c5b1b6c8
path: berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_live_simple.json
```

Confirmation applies:

- the same parser and BM25 wheel;
- all six frozen Development DQN state dictionaries without refitting;
- the same fixed K set;
- the same metric equations;
- the same `FK3 - FK1` comparison;
- 20,000 coupled-query resamples with seed `20260723`.

Every Confirmation gate is conjunctive:

1. No Confirmation input-line SHA occurs in Development.
2. Row integrity and both metric-identity checks pass.
3. At least one strict policy-pair reversal occurs.
4. At least one seed has different maximizing policies under the two metrics.
5. `FK3 - FK1` strictly reverses and has at least `0.90` bootstrap support in both prospectively fixed directions.

No alternate file, benchmark, pair, seed, K set, model, or refit may replace a failed Confirmation.

## Captured Development attempts

Interpreter:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe
```

Capture runner:

```text
D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py
```

Environment:

- Python 3.11.15;
- PyTorch 2.12.0+cu130;
- shared environment only;
- DQN execution is CPU, matching the target notebook cell;
- GPU availability is captured but not used for DQN fitting.

### `dev_eval_001`

Cwd:

```text
D:\Desktop\crl\20260722_1550_run01\implementation_v013
```

Scientific argv:

```text
audit.py --phase development --input ..\sources_v013\bfcl_development\BFCL_v3_simple.json --rank-bm25-wheel ..\sources_v013\dependencies\rank_bm25-0.2.2-py3-none-any.whl --output-dir ..\experiment_v013\work\dev_eval_001 --episodes 15000 --bootstrap-resamples 20000 --bootstrap-seed 20260723
```

Capture directory:

```text
experiment_v013/captures/dev_eval_001/
```

Declared outputs:

- `work/dev_eval_001/raw_rows.jsonl`
- `work/dev_eval_001/summary.json`
- `work/dev_eval_001/split_manifest.json`
- `work/dev_eval_001/models/bor_dqn_seed42.pt`
- `work/dev_eval_001/models/bor_dqn_seed123.pt`
- `work/dev_eval_001/models/bor_dqn_seed456.pt`
- `work/dev_eval_001/models/f1_dqn_seed42.pt`
- `work/dev_eval_001/models/f1_dqn_seed123.pt`
- `work/dev_eval_001/models/f1_dqn_seed456.pt`

### `dev_audit_001`

Cwd:

```text
D:\Desktop\crl\20260722_1550_run01\implementation_v013
```

Scientific argv:

```text
independent_audit.py --rows ..\experiment_v013\work\dev_eval_001\raw_rows.jsonl --summary ..\experiment_v013\work\dev_eval_001\summary.json --official-bor-src ..\sources_v013\bits-over-random\src --output ..\experiment_v013\work\dev_audit_001\report.json --bootstrap-resamples 20000 --bootstrap-seed 20260723
```

Capture directory:

```text
experiment_v013/captures/dev_audit_001/
```

Declared output:

- `work/dev_audit_001/report.json`

Before `dev_eval_001`, the Plan-bound implementation, config, Candidate, Research Map, nearest prior, selection context, implementation audit, Evidence Packet, target PDFs/notebooks/results, official BoR source, fixed BM25 wheel, and Development input are saved as immutable Experiment Artifacts.

After each scientific attempt, its `execution.json`, `stdout.bin`, `stderr.bin`, and every declared output are saved as immutable Experiment Artifacts under attempt-specific names.

## Cost and stop rule

- Expected author runtime: approximately 184 seconds for six CPU DQNs.
- v013 Development wall-clock budget: 20 minutes for `dev_eval_001`, excluding the independent audit.
- Independent audit wall-clock budget: 5 minutes.
- No API key, model download, external service, or network access is allowed during either scientific attempt.
- There is one Development evaluation attempt and one independent audit attempt. A nonzero exit, missing declared output, changed frozen byte, gate failure, unfair comparison, or material nearest-prior collision closes v013 without Confirmation.
- Execution-only repair is allowed only if no scientific metric or claimed output was produced and the fault is a true program-execution defect; otherwise the candidate bytes freeze and the same Run advances to v014.

Only a fully passed untouched Confirmation may authorize a complete Review Packet and exactly three fresh direct leaf Reviewers. No Reviewer is permitted before that packet is frozen.
