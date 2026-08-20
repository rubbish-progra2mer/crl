# v015 Main-Codex Implementation Audit

## Audit boundary

The main Codex reviewed v015 as an execution-only continuation of v014 before any Confirmation scientific parsing or execution. v014 is immutable. v015 is permitted to change only manifest identity, frozen artifact mapping, input cardinalities, phase-specific gate values, and phase-neutral output labels.

The scientific candidate, partition, official predicates, judge reference, row construction, metrics, bootstrap seed/resamples, and all preregistered Confirmation thresholds must remain unchanged.

## Current research documents

| Artifact | SHA-256 |
|---|---|
| `selection_context_v015.md` | `ac4b79e8422a10f9ac101b2be03da1a4c71ecb9a103eec49a9c6571cbd39d3d9` |
| `problem_v015.md` | `8360f52ca27f2f6a90d1600166156e1d58e5e010a5a2ecd1844fdd5c2fc03630` |
| `research_map_v015.md` | `a914cf8dca63a1e13c5c68949dc09adf683838c2f8c616cff1daf2d7f9047840` |
| `nearest_prior_v015.md` | `b9990214ec1567a15708b361490fd388e077e9edbd6c6e64b56dae10f77a09d8` |
| `candidate_v015.md` | `97f3e2bd1cf9363c538b3b35f703313838e20d5c6ebe17850613d87fbdd1bae3` |
| `evidence_packet_v015.md` | `36f81572fa604082c2b92195000615581e2e7dc9c4be0bd7589678bebfc4adac` |

`ResearchWorkspace.read_evidence_packet()` reported `candidate_is_current=true`, two Evidence entries, and both entries current.

## Reviewed implementation bytes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `implementation_v015/audit.py` | 24,068 | `9551f79cc075f45f1b59be11bfca25e79e60d9d49372f5d36d2cc2ede40d99c2` |
| `implementation_v015/independent_audit.py` | 12,767 | `289965efc11d5882fe0b2f43db84960c6c1d22dda9a52b4c29474832f8b236cc` |
| `implementation_v015/config.json` | 1,550 | `f5655f9edc6b85fee9b09592c6eded4bc38f93c8d948d2e40d8ac6278509ef1d` |
| `implementation_v015/test_audit.py` | 2,650 | `db5d7e93c95cb13e0a0a4ced9ca1af92a864bcb26bc398ac2da81f56db02edd6` |

All three Python files parsed successfully through `ast.parse`. The implementation directory contained zero `__pycache__` directories and zero `.pyc` files after tests.

## Exact v014-to-v015 code delta

The main Codex read the complete `git diff --no-index` for both programs. The evaluator delta is limited to:

1. `manifest_path` receives the frozen `artifact_prefix` instead of embedding `input__`;
2. the manifest is bound by the phase-neutral `manifest_sha256` key;
3. expected files, traces, judges, ensembles, rows, models, domains, rows per trace, and judges per model come from the frozen `expected` object;
4. the gate table is the frozen Confirmation `gates` object;
5. the preregistered Confirmation correction gate is evaluated as `corrections > regressions`;
6. summary schema version is 2 and records `phase`.

The independent auditor delta is limited to the same Confirmation gate, the same frozen expected cardinalities, phase/manifest/cardinality checks, and phase-neutral descriptions. It still recomputes all primary metrics from row-level output.

No normalization, predicate, label mapping, judge selection, model selection, domain selection, row filter, transition definition, metric, bootstrap sample, random seed, or scientific threshold changed.

## Scientific-code identity audit

The main Codex parsed v014 and v015 with Python's AST and compared complete function AST dumps without location attributes. Command exit was `0`; every listed comparison was `identical=True`.

| Program/function | AST SHA-256 |
|---|---|
| evaluator `rgp_classify` | `eef632ebdf433e4e1be0c84b991562ea8c1a44e9987bc42a158176adeebf8d43` |
| evaluator `macro_f1` | `c70b7c1b8a231150383046dc62eeba5b054fd77e4d124d618eee7809937dbf2d` |
| evaluator `percentile` | `34fc9da9dc727cdba494af053c0988088e2ffc47aaafdf5bec5fe29417ad6ac8` |
| evaluator `grouped_accuracy` | `4f20fea6a3efde6fd5c1ba26acd8171c88853226b0f53d764dd7f9962950b297` |
| evaluator `cluster_bootstrap` | `1fc1cbe9b1d4ff6a46ac1214d309895c998ad640fcb756bdb66dd9bb846c536b` |
| evaluator `transition_counts` | `49c019953e8d8707859889831eb62784ee98af7d230e66eb25dfb00109b37400` |
| evaluator `per_group` | `e6ea2849f7481f531af4b2591a967a97936f530b1b56c45509c7b278bc32c665` |
| independent `macro_f1` | `2f3c6bd930ebf13a6a4152095ef7327085d313cd374c531fb76e62c66c471b62` |
| independent `percentile` | `774267c71b60b4f61b7790f99b14363ab0f6e06cad5f727bc1ca53d1779553f5` |
| independent `accuracy` | `62ba0cab8a653b8b75d219a9b28f6528eaebd38702e22cdff4b0207a2ce213de` |
| independent `per_group` | `ce1bd22d4f33dcdb11148d293376c04ac35cff24aa477b4a3e1b052d8f079311` |
| independent `bootstrap` | `a95cc622b6f1f6a9382dbaeb3c10a60e68bfba89f9391621ce2e94fa5276700f` |
| independent `maximum_numeric_error` | `feb7b3d79cc1fa95591f5eae03806e054250c0fa5435a8ecdbc8d7ba04d3cf1a` |

The aggregate result was `ALL_SCIENTIFIC_AST_IDENTICAL=true`.

## Frozen Confirmation contract audit

The current config binds:

- phase `confirmation`;
- manifest SHA-256 `f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeb49a8011944`;
- artifact prefix `input__`;
- 36 total files, 12 traces, 24 judge files, zero ensembles;
- 12,000 rows, 1,000 rows per trace, two judges per model, 12 models, five domains;
- 20,000 generator-model bootstrap resamples with seed `20260723`;
- accuracy delta at least `+0.005`, bootstrap lower bound above zero, corrections strictly above regressions, positive effect on at least nine models and four domains, and at least 100 supported transitions across four domains.

A metadata-only manifest audit exited `0`: 36 files, 342,075,457 bytes, 12 traces, 24 judges, zero ensembles, zero Development path overlap, and the fixed revision matched. A separate byte-only rehash of all 36 files exited `0`, processed all 342,075,457 bytes, and found zero SHA-256 or size errors. Neither command parsed or sampled scientific content.

## Necessary pre-Plan tests

Executed from `D:\Desktop\crl\20260722_1550_run01\implementation_v015` with the shared interpreter:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe -B -m unittest -v test_audit.py
```

Exit code: `0`. Seven tests ran and passed:

- CTRL remains unchanged;
- missing expected tool remains `tool_skip`;
- required grounding precedes the fabrication predicate;
- failed grounding plus fabrication remains `output_fabrication`;
- failed grounding without fabrication remains `result_ignore`;
- perfect macro-F1 is exact;
- artifact path mapping uses the frozen prefix.

No Confirmation trace or judge JSON was imported by these tests.

## Scientific authority boundary

The evaluator's gate booleans and the independent auditor's `audit_ok` are mechanical evidence only. They cannot authorize Review, decide the claim, or create Delivery. After a one-shot frozen Confirmation, the main Codex must read the complete outputs and bounded original cases before deciding whether a Review Packet is justified.

## Disposition

`AUTHORIZED_TO_FREEZE_V015_ARTIFACTS_AND_WRITE_ONE_SHOT_CONFIRMATION_PLAN`

This disposition does not authorize Confirmation execution until every Plan-listed byte is frozen and current. It does not authorize Reviewer creation.
