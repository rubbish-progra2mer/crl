# v034 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

No v034 Development metric exists. ToolSandbox remains absent and unread. This
Packet binds the scientific identity, implementation, exposed Development
bytes, model identity, nearest-prior bytes and negative lineage before one
Development execution.

## Candidate and research identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v034.md` | 5,761 | `c57d31212276a45eab39a4147b02a2aac3eaa5c312c7d864cb7a260222c3b540` |
| `problem_v034.md` | 1,562 | `2e5114b4150b97ee3670a0ebc64ea23b19b5acf5d5ec851c489e2ed397a0bea3` |
| `research_map_v034.md` | 8,054 | `3c8848067091ae3b47a96ab93c36ed6574f2712e790074bb8adaa5362ff2f3be` |
| `nearest_prior_v034.md` | 3,339 | `5fc0f7c5aed338af1e6cafe18211dee40a0495860f1f08404e42b320302bd677` |
| `candidate_v034.md` | 2,328 | `8f78b67bfa14e3f9cbbd94207143e2574c6898913f2045cbb38f1cdb1d750a09` |
| `implementation_audit_v034.md` | 5,238 | `b931acd775fbc051aa5fcef88336b8a44b54f3847bbea6a9a4a7c7d1589eed9a` |

## Executable identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 35,859 | `a98b6f16b270fa4350bd1cf024bbf240f692d5658eb3be298117867e1d4a8ca4` |
| `audit.py` | 43,201 | `b43735617e0e09c0294f467b187bf4b2c8771c78d35d79e420ae40fd06e629c2` |
| `config.json` | 1,789 | `4efd0437ae4987176ec3edc83179e3c2478f6cf5059a89cfbcacc0b171ae237a` |
| `test_program.py` | 2,372 | `3940f8472b87d52a132d122b8cfdefd0c2fb14576c8aa19e64376a911c1fcfb9` |
| `acquire_confirmation.py` | 2,009 | `fda9a8f4e50042e43eed73b31c801c9bc495d4f53853a28e7769ff54289803f3` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |

`audit.py` imports no implementation module. It has a separate source-row,
prompt, model-replay, calibration, control, bootstrap, capture and output
comparison path.

## Development data

Repository:
`https://github.com/David-Li0406/ToolPRMBench`.
Commit: `b43164fbb2cd2963e1906a6fe62a86e7ce05973e`.

| Source | Rows | Bytes | SHA-256 |
|---|---:|---:|---|
| GTA | 118 | 410,147 | `dc4cfb906dd2b20ad9452b3afdca5346a4a6a3378e15667fd47fa1c21a54a23c` |
| BFCL | 111 | 3,019,158 | `3c13646f14abaaeba619d5ba91d6cc64bcd4223472eea62ab91ca94f588f14a8` |
| ToolTalk | 86 | 1,635,593 | `e5327446f854fae9d9ed5319bd5a418168626aa6327853d145e35cf87f2027a1` |

The acquisition manifest is 1,927 bytes, SHA-256
`4a30e583aa63ccdbab23124b478f99d6f727a5906ee4cffb34f29816569e3fa9`.
It records `confirmation_acquired: false` and names
`prmbench_ToolSandbox.json` as the conditional Confirmation.

The fixed structural boundary is 315 pairs, 630 pointwise actions, 195
source/task clusters and 3,780 model prompts. Development is exposed; its
selection and exploratory probes are disclosed.

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

These immutable local snapshot files are declared runner inputs and rehashed by
the capture. The model is loaded with `local_files_only=True`; no model network
access is allowed during Development.

The earlier incomplete 4B acquisition produced no model manifest or
scientific output and is not part of this frozen execution.

## Primary-source and Card evidence

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| ToolPRMBench paper | 1,883,463 | `f7ac155d9862f0def0b1f5c09e992dc7b626fdf90601a8cb2e8a9bcbd6712455` |
| Recursive Rubric Decomposition | 3,321,179 | `0d8220373db270500024e34575ce77129bad1a31842443838742d2cc8c22110c` |
| ToolRM v2 | 2,287,293 | `9679fe106dfc881cfdaf7e77cd6b38c871da2e503b4964f91f2fe0a8293f714f` |
| Tool-Verifier ACL Findings 2026 | 1,900,691 | `2ab5d9b8a426c138d1bfdd0b8d4af01feb2d7d1dfae989417862c19b05133945` |
| ToolGate | 3,395,441 | `7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d` |
| failure Card | 1,836 | `09789fcf448e4a770424b56e8e2f4dd4b532ed5b6895376f003a3074307382ee` |
| operator Card | 2,237 | `2c7c9cc0b1cebd4f661d4228842380b128ef736f54a96c503edbec6530c67156` |
| P074 Card | 1,800 | `7d8211b7000818dff559a643716b0275a8edacde6527559dd0d318c6a548d2a9` |

These sources establish the collision boundary: generic decomposition,
pairwise tool reward modeling, executable outcome verification and formal
pre/postcondition contracts are prior work. v034 has only the narrow empirical
composition Claim fixed in its Research Map.

## Negative lineage

v033 Result is 3,904 bytes, SHA-256
`bae8b43f2618ddbb2ee8ae5aa77de30320e558d0456b2ad34093024d0fe39956`.
Its Promotion Audit is 2,750 bytes, SHA-256
`67bc045a10c486aa5878296408bba6960c500b1352bc3a49d6b5becea7ed9409`.
They forbid further v033 representation, residual or gate retuning.

## Frozen execution boundary

Development may run exactly once over the three frozen datasets. It must write:

- `pointwise_scores.jsonl`;
- `raw_predictions.jsonl`;
- `summary.json`;
- `environment.json`;
- `frozen_state.json`.

The program must perform exactly 3,780 next-token prompt evaluations. The
independent auditor may then run exactly once, reload the same frozen model,
reconstruct all prompts from source bytes, replay every logit, recompute every
control and bootstrap, validate the runner capture, and write one `report.json`.

All gates in `research_map_v034.md` are conjunctive. Scripts can report them
but cannot authorize Confirmation. No Reviewer may be created before positive
Development and untouched Confirmation audits plus a complete formal Review
Packet.
