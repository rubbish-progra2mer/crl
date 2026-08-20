# v033 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

No v033 metric exists. This Packet binds an execution-only repair of v032.

## Preparation-failure lineage

- frozen v032 Plan:
  `5ef42ed12fb63dc317d373ee657faa8a96f8b395c83b9f7d3f7bf1ca5dfa9eb3`;
- v032 Result:
  `NO_GO_FOR_SAME_VERSION_RETRY_PREPARATION_FAILURE`;
- v032 Attempts Manifest:
  `127b924722029f1138d3251dd44bfbed3b95c157c1a2958f7d64f06c6522f688`;
- v032 Development executed: `false`;
- v032 Confirmation opened: `false`.

v033 changes no scientific field, computation, data, hyperparameter, control or
gate. It corrects version identity and replaces the frozen Plan's unresolved
explanatory count with `1,361,920`.

## Candidate and research identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v033.md` | 4,230 | `0fb8ec237b914e824f4b9a9ac1c1ec934ce312381817f84b7311a4fae71c9a4a` |
| `problem_v033.md` | 1,376 | `bfb6853952cf6a5d1894a7d5807a15951c921bc76e533ba025ca881669784990` |
| `research_map_v033.md` | 5,202 | `3d811279b5cc2c8e33c889df345df237a4ade0e9131497f7bfddcf82edc28d27` |
| `nearest_prior_v033.md` | 2,326 | `13c6e299720f45e2784725bda00085aeef5bef456825c38a86990823d97d40ac` |
| `candidate_v033.md` | 1,809 | `2fd145cce11845463d765dababf8160e5a575502aa20ccee2e631368472824ce` |
| `implementation_audit_v033.md` | 2,652 | `a095ef104180ded576a921110dd9b6bf86f7a8e61eb95292c047b97db4e1eb38` |

## Executable identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 29,813 | `4875b8c7ecde6772fa25e8b86587fe6d59f210a5505763a8ebc38fb4f2a3cc39` |
| `audit.py` | 26,874 | `7a0055e44f84eae95d9a185d00b904f2a5439c1392f185bfeceb1f1cd39c9067` |
| `config.json` | 2,198 | `7b5333e38a9ede666cf7fc2ae116e40b5c3e32e37df7d135dab5758e34875e13` |
| `test_program.py` | 1,845 | `56fc6c5c89be3d8cda5c00bb3bd654d170d055e7ae7dd9efb92c4aba956d37c7` |
| `base_v012.py` | 39,154 | `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d` |
| `acquire.py` | 12,438 | `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |

Program, auditor and test bytes are identical to v032. The config changes only
`experiment_id` and `candidate_sha256`.

## Development data

Repository commit:
`d8a29613235a0ef56a8b70b3142626a533da28c2`.

| File | Bytes | SHA-256 |
|---|---:|---|
| bucket-1 dataset | 28,801,199 | `d5daecba36e3e8f9c6bbe60c8e2b13e6206290d8ca7cddcf4a8cc27c2f82274f` |
| bucket-1 manifest | 312,237 | `aa20ea73e71b7a3b9a41d444c8a8b7997216f0b85e53fbc5cffb663e25b67932` |
| bucket-2 dataset | 38,050,057 | `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3` |
| bucket-2 manifest | 449,291 | `9bcec296b8c380d21f084e60a860577a8e08b9188f8fce75d8c625a3671ee59e` |
| bucket-3 dataset | 28,985,207 | `0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a` |
| bucket-3 manifest | 353,930 | `df2f4b46506978105121fe5afc36fcc2f1188dd1a5e6303cb2a2eef836cdc543` |

The structural boundary remains 4,256 unique rows, 250 tasks, three generators,
five sources and both classes in all nine double-holdout cells. Buckets 1-3 are
exposed Development. Bucket 0 remains absent and unread.

## Source and negative-lineage bytes

The v033 freeze must include the same PDFs and prior results bound by the v032
Packet:

- Task Shield `4a7775a5...f6edd69`;
- Trajectory Guard `ab6d2c66...18d34`;
- Terminal Wrench `140df68e...19e8a`;
- P040 false-success `ab1307fd...ba6a`;
- D²4FAD `c8f9aa62...231f7`;
- UniVAD `c20e3275...b55a9`;
- v022 Result `390b39c3...4f3c`;
- v026 Result `1e93bf3a...029f6`;
- v031 Result `881436f7...023a`;
- v031 Promotion Audit `dc51c1b6...b3d6`;
- v032 Result and Attempts Manifest.

The full digests are enumerated by the predevelopment Artifact Manifest.

## Frozen execution boundary

The changed computation and complete comparator ladder are exactly those in
`research_map_v033.md`. Development program and independent audit may each run
once from `experiment_v033/artifacts`. The exact dense-value count is:

```text
4,256 × (128 + 64 + 64 + 64) = 1,361,920
```

No Reviewer may be created before positive Development and untouched
Confirmation audits plus a complete frozen Review Packet.
