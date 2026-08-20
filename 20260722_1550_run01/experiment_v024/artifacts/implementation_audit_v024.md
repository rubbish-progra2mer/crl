# Main Codex Implementation Audit v024

## Disposition

`APPROVED_FOR_FREEZE_AND_ONE_PREREGISTERED_DEVELOPMENT`

This is the main Codex's source-level judgment, not an automated scientific decision. Bucket 1 and bucket 0 data bytes remain unopened. No Development, Confirmation, Review, Decision or Delivery result exists for v024 at this point.

## Bytes reviewed

The main Codex read the complete current `program.py` (581 lines) and `audit.py` (479 lines), plus the complete configuration, test file, Candidate, Evidence Packet, Research Map and nearest-prior note. Current implementation bytes are:

- `program.py`: 23,422 bytes; SHA-256 `d47337fdf7cf9d6863c4efebb18abb9c7d80d72aec9a86df89cf28adbfd95437`.
- `audit.py`: 21,053 bytes; SHA-256 `7b0ec0a85d15ca6127ecadbf57d48e96a559d672dc2fea88e9cbeb73e7988dc7`.
- `config.json`: 1,200 bytes; SHA-256 `3e588a5d2052814b7bb64bc2cfc2d71d8838ded02fe2ab35ab8877f0f1faddd9`.
- `test_viaf.py`: 1,937 bytes; SHA-256 `1f334f43fb9222ef625f10732b9f17b072c5439cbfef76709ea28bf5b381a3fb`.
- `candidate_v024.md`: SHA-256 `d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60`.
- `evidence_packet_v024.md`: SHA-256 `87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f`.

The configuration's Candidate and Evidence Packet hashes exactly equal the current files. The Evidence Packet itself records the same current Candidate SHA. Its three cited Evidence records and their source/passages were reported current by the workspace API.

## Computation audit

- The fixed anchor predicate implements the exact executable and non-alphanumeric checker-token boundaries in `research_map_v024.md`; it neither reads nor derives from `target`.
- A single training-fold vocabulary is fit only on training-task mixed action text, then reused for every comparator and VIAF block. Held-out tasks never enter vocabulary or classifier fitting.
- Five folds are deterministic from the second SHA-256 byte of `task_id`; each Development row receives exactly one OOF score.
- All seven methods use the same classifier family and hyperparameters. `command_duplicated`, `fixed_halves`, `anchor_bag` and VIAF have the same three-block width, so additional coefficient capacity, generic chronology and checker-token presence have explicit controls.
- The strongest Development comparator is selected only from the six predeclared comparators. Confirmation, if later authorized, must reuse that frozen comparator and the full Development models without fitting or reselection.
- The task-cluster bootstrap resamples complete task groups. Anchor-present and anchor-absent deltas are recomputed separately.
- `audit.py` independently reconstructs partitions and matrices, reloads every frozen fold model, replays all row scores, recomputes metrics/bootstrap/strata/gates and verifies manifest, dataset, config, base module, model, raw-output and source-record hashes. A successful audit still does not authorize scientific promotion.
- Output directories are publish-once at the execution level. No retry, hyperparameter search, threshold search, task selection, or Confirmation-opening logic exists in the implementation.

## Pre-freeze checks

From `D:\Desktop\crl\20260722_1550_run01\implementation_v024`, using only `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`:

```text
python -m py_compile program.py audit.py test_viaf.py
exit 0

python -m pytest -q test_viaf.py
.... [100%]
4 passed in 2.16s
exit 0
```

The tests cover the fixed first anchor, no-anchor behavior including the prior `ls latest` false-positive boundary, the exact VIAF block composition/dimensions, and deterministic task-disjoint fold assignment. Generated `__pycache__` and `.pytest_cache` directories were deleted by exact validated paths; a recursive check returned `CACHE_LEFT=0`.

The final exposed-bucket unlabeled substrate command exited 0 after inspecting 3,071 action rows without using `target`, fitting a model or producing a method metric. The exact predicate found 1,760 anchored rows (57.31%), median first-anchor relative position `0.177521`, quartiles `[0.0769231, 0.375]`, and median 13 command batches. An earlier shell-escaping attempt exited 1 before any label/model/metric operation and is not evidence. The final counts, not the aborted broad intermediate count, are recorded in `selection_context_v024.md`.

The first Evidence Packet reporting snippet attempted to display a nonexistent `.entries` attribute after the workspace API had already atomically published the Packet, so that display process exited 1. The existing Packet was then read without rebuilding; current Candidate/Packet bindings matched exactly. No scientific byte was executed or frozen by that reporting error.

## Main Codex judgment

The implementation matches the bounded VIAF Claim and supplies the necessary same-capacity, fixed-time and position-free controls. I found no source-level defect that would invalidate one preregistered task-OOF Development. This approval is limited to freezing the listed bytes, publishing one immutable Experiment Plan, acquiring only tree-designated bucket 1, and executing exactly one Development plus one independent replay audit. Only a later written main-Codex Promotion Audit based on raw results may decide whether bucket 0 can be opened.
