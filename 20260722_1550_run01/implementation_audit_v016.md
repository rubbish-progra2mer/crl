# v016 Main-Codex Implementation Audit

## Audit boundary

v016 may correct only the one-character manifest SHA transcription error that closed v015 before scientific input parsing. No scientific code, data, partition, metric, threshold, or runtime behavior may change.

## v015 failure evidence

The sole v015 Confirmation capture exited `1` after `0.07323759999781032` seconds. Its execution SHA-256 is `9006ee15f97df9dc9836e0175d9c47f337aee5a1b98d6a3446c572d228de644d`; stderr SHA-256 is `fd2682b1e932e96245e9452afb4fce0c0d45b8753813c87f043ad146e9674125`.

The traceback terminated at `program.py:216` with `ValueError: Manifest does not match frozen config`. The expected and actual values were:

```text
expected: f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeb49a8011944
actual:   f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944
```

No trace/judge JSON was opened by the scientific program; no raw rows, summary, cases, or independent audit exist. v015 Result SHA-256 is `3e1ded11173fe49c1414afa002a14d47932b4a9a0f2c3cb3d4ba9e665ab2622c`.

## Current research bindings

| Artifact | SHA-256 |
|---|---|
| `selection_context_v016.md` | `b421c5520ec472f60b70d9733da3b609cd231070f789ec94a923812ce77f2d85` |
| `problem_v016.md` | `cbfe3395fc5037097c60ef93f0a78c4b3a63aded1359002562670268cee81809` |
| `research_map_v016.md` | `00f28a3ba880dd6af02b4c307a8740b7e744ee6b44e6a2a95026230cab3390a8` |
| `nearest_prior_v016.md` | `e22e9e5d7d34c01d2fa9d8c802727f06470039287910c3833c593610d37fdfb7` |
| `candidate_v016.md` | `31df88dfa09b6b5b214236f0a364bbaf7f3a417b96af1ce0aee5c9219f0de845` |
| `evidence_packet_v016.md` | `1bc9f9d937f7cafb1e63b449e255b1032baf5a18a59fec818da19561a3204526` |

The Evidence Packet is bound to the current Candidate, contains two formal Evidence entries, and both entries are current.

## Program byte identity

The main Codex compared complete file bytes:

| File | v015 SHA-256 | v016 SHA-256 | Equal |
|---|---|---|---|
| `audit.py` | `9551f79cc075f45f1b59be11bfca25e79e60d9d49372f5d36d2cc2ede40d99c2` | `9551f79cc075f45f1b59be11bfca25e79e60d9d49372f5d36d2cc2ede40d99c2` | true |
| `independent_audit.py` | `289965efc11d5882fe0b2f43db84960c6c1d22dda9a52b4c29474832f8b236cc` | `289965efc11d5882fe0b2f43db84960c6c1d22dda9a52b4c29474832f8b236cc` | true |
| `test_audit.py` | `db5d7e93c95cb13e0a0a4ced9ca1af92a864bcb26bc398ac2da81f56db02edd6` | `db5d7e93c95cb13e0a0a4ced9ca1af92a864bcb26bc398ac2da81f56db02edd6` | true |

The scientific-function AST comparison against v014 also returned `ALL_SCIENTIFIC_AST_IDENTICAL_TO_V014=true` with exit `0`.

## Config delta

`git diff --no-index` showed only four binding changes from v015:

1. candidate ID `v015` to `v016`;
2. manifest SHA corrected by inserting the missing `e`;
3. current v016 Candidate SHA;
4. current v016 Evidence Packet SHA.

The frozen scientific values are unchanged: phase, dataset revision, artifact prefix, file/row/model/domain cardinalities, labels, bootstrap configuration, case-sample limit, and every gate.

The current config is 1,551 bytes with SHA-256 `0c5cc494445d7eae922dabcbff0d2f9f45da34a46a17ee712955a468ef81d3b5`. A direct comparison now reports:

```text
CONFIG_EXPECTED=f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944
MANIFEST_ACTUAL=f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944
MATCH=True
```

## Necessary tests

Executed once from `D:\Desktop\crl\20260722_1550_run01\implementation_v016`:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe -B -m unittest -v test_audit.py
```

Exit code `0`; all seven tests passed. No Confirmation trace or judge JSON was imported. The implementation directory contained zero `__pycache__` directories and zero `.pyc` files.

## Scientific authority boundary

This audit authorizes only v016 Artifact freezing and one prospective Plan. It does not authorize execution before the Plan, same-version retry, Review, or Delivery. Automated gates remain measurements only.

## Disposition

`AUTHORIZED_TO_FREEZE_V016_ARTIFACTS_AND_WRITE_ONE_SHOT_CONFIRMATION_PLAN`
