# v013 Main-Codex Promotion Audit

## Frozen evidence boundary

- Experiment Plan SHA-256: `220B618A4810870F188EDA537F5876FF6905A173581323AB8E8BAE766E5BF24D`.
- Candidate SHA-256: `50AD937E5AA6DF51E76223EF002A675273902A59D71170082D05C222DB61FFF5`.
- Evidence Packet SHA-256: `1E8563B6ECCB27DACEF35F2C0B277B80C1742CE2EBC2AD83984053A59CB3C96E`.
- Development execution SHA-256: `E57BA013B6EDCBF46940EADF961DBDB7E3F8CB7AEF48E637000C75A4CD16AC17`.
- Development raw rows SHA-256: `64046FE59AE1706975830585D48896D689C31807D6139D153F7F18F91C598A68`.
- Development summary SHA-256: `A1FC5202DBC462A935181DDEC2A3B1746AF4D7985EDFECAFEB27AEBB4B7CBA7F`.
- Development split manifest SHA-256: `016B0D09C1FC0FB8B599B55C120D07AD6983E518922C3E75F93122ED92F2A107`.
- Independent audit execution SHA-256: `7A8917D7B5E1E20D9BDBB31A5EC2A0DA5FB4A4ED6851D9935C7F02ED511355A7`.
- Independent audit report SHA-256: `E7B71AB8E2370DF3D297214771F1A676E3BAFE1CCCA06C6600CBE01E2410233E`.

The exact machine value from `execution.json` is:

```text
a1fc5202dbc462a935181ddec2a3b1746af4d7985edfecafeb27aebb4b7cba7f
```

Development ran once under the shared Python 3.11.15 environment:

- exit code: `0`;
- duration: `668.1302038999984` seconds;
- stdout SHA-256: `5D6EFF7957CF37C6BF2D126746D1E2D6D08905C2834B21F5BD492AF94005FE09`;
- stderr bytes: `0`;
- all nine declared outputs exist and match the capture manifest.

The independent audit ran once:

- exit code: `0`;
- duration: `2.8199131000001216` seconds;
- stdout SHA-256: `D1CFA34A11C9AF09E330592538FB97800362AF799B24BA49B20A0F87D6D718EA`;
- stderr bytes: `0`;
- report bytes: `16,081`.

## Launch diagnostics

Before the successful captured execution, two non-scientific launch failures occurred:

1. A foreground shell call used a one-second outer timeout and returned shell exit `124`. It left no v013 process, capture directory, work directory, model, row, summary, or metric.
2. The first detached runner call found that `experiment_v013/captures/` had not yet been created and exited before launching `audit.py`, with `FileNotFoundError` at the runner's `capture_dir.mkdir()`. It left no capture or scientific output.

The exact parent directories were then created and the preregistered `dev_eval_001` command was launched unchanged. These are launcher defects, not additional scientific attempts; neither exposed a scientific result or changed a frozen input.

## Main-Codex direct raw-row audit

The main Codex read `raw_rows.jsonl` independently of both experiment programs and observed:

- 1,440 rows;
- 12 policy/seed groups;
- 120 rows and 120 unique query IDs in every group;
- every group query-ID set exactly equals the 120-ID Development test manifest;
- 280 train IDs and 120 test IDs, intersection `0`, union `400`;
- hit-consistency errors: `0`;
- depth-bound errors: `0`;
- only `N=370`;
- maximum stored target-reward error: `1.509903313490213e-14`;
- maximum stored chance-probability error: `5.551115123125783e-17`.

The independent report's 12 count errors are caused by a real metadata defect: `summary.json` records total parsed input count `400` in `query_count`, while each policy is correctly evaluated on the frozen 120-query test partition. The report compared each group against the mislabeled 400. The raw row bytes and split manifest establish that every required test query appears exactly once per group. This defect is preserved and disclosed; it is not repaired or rerun.

## Direct metrics

| Policy | Seed | Found | Mean K | Notebook statistic | Defined BoR |
|---|---:|---:|---:|---:|---:|
| BoR DQN | 42 | 0.9333333 | 11.6000 | 7.1659298 | 4.8957929 |
| BoR DQN | 123 | 0.9333333 | 10.1333 | 7.1779939 | 5.0908089 |
| BoR DQN | 456 | 0.9083333 | 7.4833 | 7.0726119 | 5.4889942 |
| F1 DQN | 42 | 0.8833333 | 5.0417 | 7.0054404 | 6.0185106 |
| F1 DQN | 123 | 0.8833333 | 6.3500 | 6.9177455 | 5.6856547 |
| F1 DQN | 456 | 0.9250000 | 10.6917 | 7.1596639 | 5.0004919 |
| FK1 | — | 0.6000000 | 1 | 5.1188289 | 7.7944159 |
| FK3 | — | 0.7833333 | 3 | 5.4413615 | 6.5941172 |
| FK5 | — | 0.8250000 | 5 | 5.1227990 | 5.9319194 |
| FK10 | — | 0.8500000 | 10 | 4.4280354 | 4.9749881 |
| FK20 | — | 0.8750000 | 20 | 3.6832717 | 4.0168083 |
| FK50 | — | 0.9083333 | 50 | 2.6228355 | 2.7488190 |

The notebook statistic selects BoR DQN in seeds 42 and 123 and F1 DQN in seed 456. Defined BoR selects FK1 in all three seeds. Twenty-one of the 27 strict reversals involve a learned policy; learned-policy reversals occur in all three seeds.

## Preregistered gate adjudication

| Gate | Evidence | Main-Codex judgment |
|---|---|---|
| 1. Row integrity | Direct raw audit: 12 × 120 unique test rows; zero hit/depth errors; train/test disjoint | PASS despite the separately disclosed summary-count metadata defect |
| 2. Stored reward identity | maximum error `1.5099e-14 <= 1e-12` | PASS |
| 3. Defined metric identity | official primitive maximum error `0.0` | PASS |
| 4. Official reproduction tolerances | fixed-K values exact; BoR-DQN mean found delta `0.022` passes, but mean K `9.7388889` differs from `7.4` by `2.3388889 > 1.0` | **FAIL** |
| 5. FK3/FK1 strict reversal | notebook `+0.3225326`; defined `-1.2002987` | PASS |
| 6. Learned-policy reversals in at least two seeds | seeds `42, 123, 456` | PASS |
| 7. Different maximizing policy | true for all three seeds | PASS |
| 8. Coupled-bootstrap support | notebook positive `0.86415 < 0.95`; defined negative `1.0` | **FAIL** |

Two conjunctive Development gates fail. The notebook-difference bootstrap 95% interval is `[-0.2279634, 0.9177074]`; the defined-difference interval is `[-1.3479233, -1.0230836]`.

## Scientific interpretation

The frozen Development rows strongly verify the algebraic non-equivalence and show numerous policy-order reversals. They do not satisfy the preregistered confirmation-opening contract:

- the learned BoR policy's mean depth is not reproduced within the fixed tolerance;
- the prospectively selected fixed-K notebook-order reversal lacks the required 0.95 bootstrap sign support.

Lowering the support threshold, choosing a different pair after seeing results, widening the reproduction tolerance, repairing metadata, or rerunning seeds would be post-result retuning. None is allowed.

## Promotion decision

`MAIN_CODEX_PROMOTION_AUTHORIZED: false`

- Untouched Confirmation remains unacquired and unread.
- No Review Packet is authorized.
- No Reviewer may be started.
- No Decision or Delivery is authorized.
- v013 freezes as a Development-screen candidate failure.
- The same Run must advance to a scientifically different v014.
- v014 must not retune the BoR audit, substitute another post-hoc policy pair, lower its bootstrap gate, or repair-and-rerun v013.
