# Main-Codex Implementation Audit v040

Status: `PREFREEZE_ACCEPTED_FOR_ONE_DEVELOPMENT_EXECUTION`.

The main Codex personally compared v040 against frozen v026 CMCD, inspected the
program and independent auditor, read the final config and verified the full
exposed input structure. No subagent was used.

## Exact scientific delta

`git diff --no-index` returned its normal difference exit code `1` and showed:

1. one new method name, `generator_balanced_consensus`;
2. one deterministic reducer that groups pair probabilities by support model,
   averages within group and equally averages group means;
3. one new score slot in program and auditor;
4. Candidate metric, bootstrap and generator-slice references changed from
   trace-mean CMCD to the new score;
5. experiment identity changed from v026 to v040.

The original `cross_model_consensus` remains unchanged and is included in
`COMPARATORS`. TF-IDF fitting, task/generator exclusion, pair generation,
absolute-deviation features, pair classifier, sample/class weights, folds,
bootstrap, all gates and Confirmation logic are unchanged.

An initial prefreeze proposal included training-time group weights. Direct code
inspection and an all-row structural scan proved every training query has only
one allowed support generator, making that component mathematically identical
to v026. It was removed before freeze. Every held-out row has two support
generator groups, and 3,820 of 4,072 have unequal group trace counts, so the
retained inference reduction is non-vacuous.

`config.json` changes only experiment identity, Candidate SHA and Evidence
Packet SHA. `base_v012.py` and the one-shot acquisition script are byte-identical
to v026. The capture runner differs from old v026 only by the already validated
`parents=True` capture-path correction used in v038/v039.

## Prefreeze verification

With shared Python 3.11.15 and `PYTHONDONTWRITEBYTECODE=1`:

- first unit run: `5/6`; one test expected the reference block rather than the
  absolute-difference block;
- the two expected constants were corrected before freeze;
- corrected run: `6/6`, exit `0`;
- a final explicit independent-auditor reducer test raised the total to `7/7`,
  exit `0`;
- seven Python files passed AST parsing, exit `0`;
- the all-row structural scan exited `0` over 4,256 source rows, 228 eligible
  tasks and 4,072 eligible rows;
- no v040 model fitting or metric was run;
- `.pyc` and bucket-0 file counts remain zero.

The first Group-DRO PDF extraction exited `1` only on console encoding; UTF-8
physical-page extraction exited `0`. Three Card queries all exited `0`.

## Executable hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 33,210 | `886dd6a113ae32828582dfa12f168ee33996cdaa1f49f8dc40b2655e0a2924d7` |
| `audit.py` | 32,114 | `d1ff0544ff1137a702696f92e0da9bd33d65320a2fdf405c1d04f165a7972a5d` |
| `base_v012.py` | 39,154 | `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d` |
| `config.json` | 2,189 | `492a07187e61469c37faf521ee8526bf2db13eeeef41c4a48aab3450c27d1b16` |
| `test_gbcd.py` | 8,485 | `f972cec6fc9d834a05b1b47e591510441e9c7fe1bf6069438a43bb73877df9fb` |
| `run_local_experiment.py` | 4,350 | `2a888a00cd9845f848fa2da8f572c105a55b5dbf7ca518dac8cd9988131abb37` |
| `acquire_confirmation.py` | 12,438 | `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836` |
| `freeze_artifacts.py` | 4,748 | `35c69758a5a4849b4989a32ceca13a019c3b015a0834397f7a851fd35ed4dc78` |

This audit authorizes one frozen v040 Development capture and, only after exit
`0`, one independent replay. It does not authorize bucket-0 acquisition,
Reviewer creation, Delivery or a system-state transition.
