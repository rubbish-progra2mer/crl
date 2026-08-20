# v036 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

No v035 or v036 Development metric exists. v035 failed at model loading before
any prompt. ToolSandbox remains absent and unread. v036 binds the unchanged
scientific design plus one execution-only loader correction.

## v036 identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v036.md` | 1,150 | `edd501d7fff2813de1ea6cc7b4c0365e786a9660a84acb5cfe467fab146ba25e` |
| `problem_v036.md` | 609 | `e018e57ffbd5cd3dad698fa049e769591e4b5f7206987623b429528ec63c4c41` |
| `research_map_v036.md` | 764 | `88f69b56f936d1f755c970eba9416e2fd367e5f773eeadae6f11e62a8aa37221` |
| `nearest_prior_v036.md` | 740 | `c530102e453faec9ac6222a2096cacb41b872de238f2fde4743afe14b87e70d2` |
| `candidate_v036.md` | 2,339 | `de3eb8e0eac0a384d252cac64ba67ce8c6d7c4e2fc5f8c1c2dff81f9aa121840` |
| `implementation_audit_v036.md` | 2,460 | `b8a97aa2d835446682f79c537d602f2de8bdfe3e393cd95fd3a4414d4ea1e92b` |

## Executable identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 35,316 | `ac23300356663662e9529f0ec5feb8440447c51fdf1bd12d6e9927bc99f14aba` |
| `audit.py` | 37,441 | `710fdd75f683f41f81c5e402628ce04407889ec547d141d78252c065810f44e3` |
| `config.json` | 1,716 | `ce8ed62cdbc68753226aa07f9c417de60c75a47a115785d1444bc38366001c26` |
| `test_program.py` | 2,572 | `27fa74d6b278c57e872f0ba868084eebb3866a084eab4ad5df6aff2914eb0371` |
| `acquire_confirmation.py` | 2,009 | `61bac6cc9f5af4f93b07f19fb3bdf5dd46eec0fa3457f469b6ad4804e5b2df60` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |

The program and auditor differ from frozen v035 only in the exact
`dtype=float16` then `.to("cuda")` loader hunk. A synthetic no-data forward
pass exited `0` with finite CUDA logits.

## Unchanged scientific identity

Frozen v035 scientific bytes are incorporated:

- v035 Candidate:
  `0e6b148cc7ac87d997c4df0c89eb427c25107b455fc14271c98549adc8ecfd79`;
- v035 Problem:
  `38e874aa95002ab5d2584129eac63a94ecda9282a220aa2ce114c24cb6d5a0de`;
- v035 Research Map:
  `c89b2510d85c931caf86cef4a55732bc7a06333e3edc39f1d61faa3a7d4e1a45`;
- v035 Nearest Prior:
  `417242fd378db2a188d288855a2d228365ccdc9a4203e6826b22a4c6688ac70e`;
- v035 source/model Artifact Manifest:
  `c0c180ee340eca25c17e3f091c459efc8925eb4751c6ffab88ade4ff9fe1fef0`.

The v035 execution failure is bound by execution SHA
`8805f2a91a214c5dc2156909895ca11a5ede6447e63e7e036a23b05b3510e315`
and Result SHA
`ceb05197a873f1ddb1d06dff50d56c6f263cd6577caae74372dc322312c17dfc`.

## Data and model

Development remains exactly:

- GTA: 118 rows / 92 clusters,
  `dc4cfb906dd2b20ad9452b3afdca5346a4a6a3378e15667fd47fa1c21a54a23c`;
- BFCL: 111 rows / 52 clusters,
  `3c13646f14abaaeba619d5ba91d6cc64bcd4223472eea62ab91ca94f588f14a8`;
- ToolTalk: 86 rows / 51 clusters,
  `e5327446f854fae9d9ed5319bd5a418168626aa6327853d145e35cf87f2027a1`.

The frozen Qwen3-0.6B model revision remains
`c1899de289a04d12100db370d81485cdf75e47ca`, model manifest
`9518287b603d6bc25ef7cd3f98764db94a633f360faa68f57ee80ceb8cf72034`
and weight
`f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b`.

The structure remains 315 pairs, 195 clusters and 2,520 prompts. The prior
PDFs and collision boundary are identical to v035.

## Execution boundary

v036 permits exactly one Development capture and, only after exit `0`, one
independent replay audit. All eight Development gates are unchanged and
conjunctive. Main-Codex raw inspection and Promotion Audit remain mandatory.

No Reviewer may be created before positive Development, positive untouched
ToolSandbox Confirmation and a complete frozen formal Review Packet.

