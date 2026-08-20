# v040 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

No v040 Development metric exists. Terminal Wrench bucket 0 remains absent,
unacquired and unread. This Packet binds one final Development computation; it
is not a Review Packet or Delivery evidence.

## Candidate identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v040.md` | 2,748 | `8e4fa8b6facd870af9a4f22d74d357b948c537ea8c6a06b71f67a6c971af2ebc` |
| `problem_v040.md` | 724 | `854545bbf8580a2cec4f361eeb2e9664587ffc72b754b4bca0064ad6b006d765` |
| `research_map_v040.md` | 1,201 | `9fc60e7f032c113ff27b04f64d88058be598b02d038ae6bcb636dbab7d9d5080` |
| `nearest_prior_v040.md` | 1,793 | `58e6cd55ebfaa56bdc9657ae1f5f68e602187d9371241d65c4173ae104091174` |
| `candidate_v040.md` | 2,520 | `aa82bbe9988b7e1824a49a7e4d080c46a3d9e38b833e6d2c396b006f717cc51c` |

## Scientific executable identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 33,210 | `886dd6a113ae32828582dfa12f168ee33996cdaa1f49f8dc40b2655e0a2924d7` |
| `audit.py` | 32,114 | `d1ff0544ff1137a702696f92e0da9bd33d65320a2fdf405c1d04f165a7972a5d` |
| `base_v012.py` | 39,154 | `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d` |
| `test_gbcd.py` | 8,485 | `f972cec6fc9d834a05b1b47e591510441e9c7fe1bf6069438a43bb73877df9fb` |
| `run_local_experiment.py` | 4,350 | `2a888a00cd9845f848fa2da8f572c105a55b5dbf7ca518dac8cd9988131abb37` |
| `acquire_confirmation.py` | 12,438 | `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836` |
| `freeze_artifacts.py` | 4,748 | `35c69758a5a4849b4989a32ceca13a019c3b015a0834397f7a851fd35ed4dc78` |

## Exposed Development carrier

The exact v026 exposed inputs are reused:

| Bucket | Dataset SHA-256 | Manifest SHA-256 |
|---:|---|---|
| 1 | `d5daecba36e3e8f9c6bbe60c8e2b13e6206290d8ca7cddcf4a8cc27c2f82274f` | `aa20ea73e71b7a3b9a41d444c8a8b7997216f0b85e53fbc5cffb663e25b67932` |
| 2 | `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3` | `9bcec296b8c380d21f084e60a860577a8e08b9188f8fce75d8c625a3671ee59e` |
| 3 | `0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a` | `df2f4b46506978105121fe5afc36fcc2f1188dd1a5e6303cb2a2eef836cdc543` |

The carrier contains 4,256 source rows. Prospective eligibility leaves 228 of
250 tasks and 4,072 evaluated rows. Three task folds and complete
target-generator exclusion remain unchanged.

## Changed computation and matched controls

The v026 pair classifier, vocabulary, query/support/absolute-deviation features,
class weighting, C and seed are unchanged. v040 groups held-out pair scores by
support generator, averages within group, then equally averages group means.

The all-row structural scan exited `0`:

- every one of 4,072 held-out rows has exactly two support generator groups;
- 3,820 held-out rows have unequal group trace counts, so the computation is
  non-vacuous;
- every training query has exactly one support generator group, which is why a
  proposed training-reweighting component was removed before freeze.

Original trace-mean CMCD, single support, no-absolute-deviation, triple-query and
direct are mandatory controls. All eight v026 Development gates remain
unchanged and conjunctive.

## Prior and negative-result boundary

- v026 Candidate:
  `b43922594122236b08fcdd94836a5731a8d1cc91c49e7a0a918b51a225bc5f61`;
- v026 raw:
  `ee4a8c5961def6500b8f82105821c104347a337589f1ef0a067fa3ae961a87b8`;
- v026 summary:
  `a14aab0834aea724daa6daa29d658b5f6c0544b6b9fb61257adf8ee43cfb000c`.

Group-DRO PDF:
`7342848c5921ff5cedf2c27a0f84e38c221c085a9ce28befd9208f2bb0fe36d6`.
Group DRO changes the training objective and regularization; v040 does neither.
Generic hierarchical means are prior art.

## Prefreeze verification and boundary

- three formal Card queries: all exit `0`;
- first Group-DRO text extraction: exit `1` from GBK output encoding only;
- UTF-8 extraction and physical-page 1--5 reading: exit `0`;
- first unit-test run: `5/6`, one incorrect expected constant;
- corrected unit-test run: `6/6`, exit `0`;
- final program-plus-independent-auditor unit-test run: `7/7`, exit `0`;
- seven-file AST and all-row structural scan: exit `0`;
- `.pyc` count: zero;
- bucket-0 file count: zero.

No v040 score was screened. Exactly one frozen Development capture and one
independent audit are permitted. Only all gates plus positive Promotion Audit
allows one-shot bucket-0 acquisition. No Reviewer may start before positive
Confirmation and a complete frozen Review Packet.
