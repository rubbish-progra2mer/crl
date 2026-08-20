# v035 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

No v035 Development metric exists. ToolSandbox remains absent and unread. This
Packet binds the scientific identity, implementation, exposed Development
bytes, frozen model and primary-source boundary before one Development
execution.

## Candidate and research identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v035.md` | 4,002 | `ec3ea8a4eb17951bbee007648a58aaa8387e0faad9aa6055d02532155653dd56` |
| `problem_v035.md` | 1,323 | `38e874aa95002ab5d2584129eac63a94ecda9282a220aa2ce114c24cb6d5a0de` |
| `research_map_v035.md` | 2,546 | `c89b2510d85c931caf86cef4a55732bc7a06333e3edc39f1d61faa3a7d4e1a45` |
| `nearest_prior_v035.md` | 2,567 | `417242fd378db2a188d288855a2d228365ccdc9a4203e6826b22a4c6688ac70e` |
| `candidate_v035.md` | 3,802 | `0e6b148cc7ac87d997c4df0c89eb427c25107b455fc14271c98549adc8ecfd79` |
| `implementation_audit_v035.md` | 4,699 | `8863f2320eee2710dfc9e0a67e15cfe213967d0a8fdb3091b01df235a43c043b` |

## Executable identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 35,344 | `f3a1fa0ac4b69daa4a629701f223ff595ffa430014c25755142cffd536e0ac64` |
| `audit.py` | 37,469 | `591a89bad636f5bfd8e86d487f9eaf014b0c604f9a838a03ea5f1fb19525f2a8` |
| `config.json` | 1,716 | `f1ad651c0804422e534ba53fb87d2a6295f633f17659d730b38edc68e50e6d92` |
| `test_program.py` | 2,572 | `27fa74d6b278c57e872f0ba868084eebb3866a084eab4ad5df6aff2914eb0371` |
| `acquire_confirmation.py` | 2,009 | `a26821f7df2554490da04469d088abc9ebeeeadd1e4a0e941136062eaa3d6c14` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |

`audit.py` imports no implementation module. It separately reloads the same
frozen inputs and model, rebuilds all 2,520 prompts, replays probabilities and
recomputes raw rows, controls, metrics and bootstrap values.

## Development data

Repository:
`https://github.com/David-Li0406/ToolPRMBench`.
Commit: `b43164fbb2cd2963e1906a6fe62a86e7ce05973e`.

| Source | Rows | Clusters | Bytes | SHA-256 |
|---|---:|---:|---:|---|
| GTA | 118 | 92 | 410,147 | `dc4cfb906dd2b20ad9452b3afdca5346a4a6a3378e15667fd47fa1c21a54a23c` |
| BFCL | 111 | 52 | 3,019,158 | `3c13646f14abaaeba619d5ba91d6cc64bcd4223472eea62ab91ca94f588f14a8` |
| ToolTalk | 86 | 51 | 1,635,593 | `e5327446f854fae9d9ed5319bd5a418168626aa6327853d145e35cf87f2027a1` |

The frozen structure is 315 pairs, 195 source/task clusters and exactly 2,520
model prompts. Development is exposed by v034, and v035 optional stopping is
explicitly disclosed.

The source manifest is 2,106 bytes, SHA-256
`280fc539e321517e3b5f0fa7a3d9882100f412c92daff22c92d9709cfaedde62`.
`config.json` names `prmbench_ToolSandbox.json` as the conditional 130-row
Confirmation and records `acquired: false`.

## Frozen model

Model ID: `Qwen/Qwen3-0.6B`.
Revision: `c1899de289a04d12100db370d81485cdf75e47ca`.
Model manifest: 2,499 bytes, SHA-256
`9518287b603d6bc25ef7cd3f98764db94a633f360faa68f57ee80ceb8cf72034`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `config.json` | 726 | `660db3b73d788119c04535e48cf9be5f55bc3100841a718637ae695b442f27dd` |
| `generation_config.json` | 239 | `2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2` |
| `merges.txt` | 1,671,853 | `8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5` |
| `model.safetensors` | 1,503,300,328 | `f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b` |
| `tokenizer.json` | 11,422,654 | `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4` |
| `tokenizer_config.json` | 9,732 | `d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101` |
| `vocab.json` | 2,776,833 | `ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910` |

All seven immutable snapshot files are declared capture inputs and rehashed by
both program and auditor. Model loading is local-only.

## Primary-source evidence

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| ToolPRMBench | 1,883,463 | `f7ac155d9862f0def0b1f5c09e992dc7b626fdf90601a8cb2e8a9bcbd6712455` |
| ToolRM v2 | 2,287,293 | `9679fe106dfc881cfdaf7e77cd6b38c871da2e503b4964f91f2fe0a8293f714f` |
| PRePair | 848,130 | `8735b209a569f7b6d06b90b3c3dc970013ae0bbc23849032fe7ec6ff417549b9` |
| Pairwise or Pointwise | 484,742 | `1257158555afd20ec4c52e9ae37d26ee70c4448b6070f64a54592b8021d7412e` |
| SCOPE | 663,078 | `7211f2e58739ff480279d3cbeddc8877c6bf41f0f023ed1b04d4bc727f936a08` |

These sources prohibit broad claims for pairwise tool reward modeling,
pointwise-before-pairwise reasoning, order-swapped probability aggregation,
confidence selection or general bias mitigation. Only the fixed
field-difference evidence projection remains testable.

## Frozen execution boundary

Development may run exactly once. It must write:

- `raw_predictions.jsonl`;
- `summary.json`;
- `environment.json`;
- `frozen_state.json`.

The independent auditor may then run exactly once, rebuild all 2,520 prompts
and write one `report.json`. The main Codex must inspect raw corrections,
regressions, every gate and source behavior before deciding whether
Confirmation may be acquired.

No Reviewer may be created before positive Development, positive untouched
Confirmation and a complete frozen formal Review Packet.
