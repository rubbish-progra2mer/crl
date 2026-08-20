# v032 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

This Packet contains no scientific result. It binds the exact Candidate,
problem, prior-work boundary, implementation, audit path, data and source bytes
that may enter the one-shot Development Plan.

## Candidate and research identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v032.md` | 3,790 | `628eb93c09bb75d2f8a11ced88c4f248e7bf88311a1d46d309ff9dea3356b36f` |
| `problem_v032.md` | 1,377 | `7b21c0c30b0f7a857ea71b0129834d85ac4c9c22ce6caab4e7045c75bb8c887f` |
| `research_map_v032.md` | 5,203 | `a2e0e85810b5b2ab3a80fd4924a49e065e9c563887a312f4ef281dc0a3988c62` |
| `nearest_prior_v032.md` | 2,327 | `09278ad44261102d0ce962cac856666bec15c2a5db3b9e6dbd39fb8d96b5ac40` |
| `candidate_v032.md` | 1,809 | `63fdd82c91a45ad6d162dcf5122ac3cc21bbdde84daa60fcba36264a310f34ec` |
| `implementation_audit_v032.md` | 4,111 | `4fbbc4ac4118ca524cb67a24434010dbe239953908edde031c14dda65d2039df` |

The config binds the Candidate SHA exactly.

## Executable implementation

| File | Bytes | SHA-256 |
|---|---:|---|
| `implementation_v032/program.py` | 29,813 | `4875b8c7ecde6772fa25e8b86587fe6d59f210a5505763a8ebc38fb4f2a3cc39` |
| `implementation_v032/audit.py` | 26,874 | `7a0055e44f84eae95d9a185d00b904f2a5439c1392f185bfeceb1f1cd39c9067` |
| `implementation_v032/config.json` | 2,198 | `ba2637c1338c721b97db5816ebfdaf424d4e09c11e38f5685dca5417987682b3` |
| `implementation_v032/test_program.py` | 1,845 | `56fc6c5c89be3d8cda5c00bb3bd654d170d055e7ae7dd9efb92c4aba956d37c7` |
| `base_v012.py` | 39,154 | `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d` |
| `acquire.py` | 12,438 | `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |

`audit.py` does not import `program.py`. It independently refits and replays the
complete Development computation and frozen full-bundle predictions.

## Development data

Repository: `https://github.com/few-sh/terminal-wrench.git`

Commit: `d8a29613235a0ef56a8b70b3142626a533da28c2`

| Bucket/file | Bytes | SHA-256 |
|---|---:|---|
| `development_bucket1_dataset.jsonl` | 28,801,199 | `d5daecba36e3e8f9c6bbe60c8e2b13e6206290d8ca7cddcf4a8cc27c2f82274f` |
| `development_bucket1_manifest.json` | 312,237 | `aa20ea73e71b7a3b9a41d444c8a8b7997216f0b85e53fbc5cffb663e25b67932` |
| `development_bucket2_dataset.jsonl` | 38,050,057 | `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3` |
| `development_bucket2_manifest.json` | 449,291 | `9bcec296b8c380d21f084e60a860577a8e08b9188f8fce75d8c625a3671ee59e` |
| `development_bucket3_dataset.jsonl` | 28,985,207 | `0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a` |
| `development_bucket3_manifest.json` | 353,930 | `df2f4b46506978105121fe5afc36fcc2f1188dd1a5e6303cb2a2eef836cdc543` |

Structural preflight exited `0`: 4,256 unique rows, 250 tasks, 1,794
successful rows, 2,462 serious-exploit rows, three generators, five sources and
both classes in every one of the nine generator×task-fold held-out cells.

Buckets 1-3 are already exposed Development. Bucket 0 is absent and unread.

## Original-source bytes

| File | Bytes | SHA-256 |
|---|---:|---|
| `task_shield_2412.16682.pdf` | 1,446,420 | `4a7775a5695b32325b1616d62ae8141d4d95f7c3f2e244462616da8d4f6edd69` |
| `trajectory_guard_2601.00516.pdf` | 334,806 | `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34` |
| `terminal_wrench_2604.17596.pdf` | 248,630 | `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a` |

## Frozen nearest-method and negative-lineage bytes

| File | Bytes | SHA-256 |
|---|---:|---|
| `P040_false_success.pdf` | 498,129 | `ab1307fdaaf97841bd09296bca225b736e8e9a712002ac123b1fab663f35ba6a` |
| `d24fad_2603.01713.pdf` | 3,562,892 | `c8f9aa621915f8e1ecb3945155eb5bf06580f74214f3d9d88be520154a5231f7` |
| `univad_2412.03342.pdf` | 6,001,964 | `c20e32751c4f7b6332606a810ec07be854af0afb4c9202619a5822936d5b55a9` |
| `v022_result.md` | 15,199 | `390b39c339be555ffbc43590d3554d5d7004b37406b60d86f9ecd3b453494f3c` |
| `v026_result.md` | 13,427 | `1e93bf3a5980f3851ed2f8180b9d33984cdbfe4b323b0794c7cb8e8652e029f6` |
| `v031_result.md` | 4,090 | `881436f7aa1a99979f9fb08e1386cc21f3bffa5a5ca5da9c5c1d27ab2dee023a` |
| `v031_promotion_audit.md` | 2,143 | `dc51c1b692be0bf8c74f54630fc6cc2611886bebc2deecbaf0d265cc4367b3d6` |

These bytes expose earlier results and are included to make optional stopping
and the prohibited same-task/support/role routes auditable. They are not extra
Development rows.

## Frozen changed computation and controls

The Candidate is the direct action-text classifier augmented by the absolute
latent innovation from an equal-task-weight task-to-action ridge map fitted
only on successful training rows.

Mandatory controls are direct action text, task/action concatenation, raw
latent addition, identity innovation and the equal-capacity all-row conditional
innovation. Candidate attribution is forbidden unless it strictly beats the
all-row map and every other control.

All hyperparameters, double-holdout bundles, metrics, 2,000-task bootstrap,
generator/source slice requirements and Development/Confirmation gates are
fixed in `research_map_v032.md` and `config.json`.

## Execution boundary

The Development program and independent audit must each run exactly once
through the frozen runner from
`D:\Desktop\crl\20260722_1550_run01\experiment_v032\artifacts`.

No v032 metric existed when this Packet was written. No Reviewer may be created
before a successful untouched Confirmation and a complete neutral Review Packet
are frozen.
