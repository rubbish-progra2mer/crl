# Main-Codex Raw Analysis v039

The main Codex personally read the primary summary, environment, first and last
raw rows, aggregate raw-row diagnostics, execution captures and independent
audit report. No subagent was used.

One initial read-only aggregation command exited `1` with `NameError` because
its tie-count comprehension referenced the wrong local variable. It wrote
nothing and did not run the model. One corrected read-only aggregation exited
`0`.

## Captured identity

- primary runner / child exit: `0 / 0`;
- primary duration: `98.67002579999826` seconds;
- primary execution:
  `590d26683be6fe5fc9bff3a21096296cd7e72c779f1253e365110e594a6f1ce0`;
- raw predictions:
  `73986d3bdd8449952abd9410aa962b0edf39a2b8a908498108f31e58b7ffe389`;
- summary:
  `0372704c4efd1508edb1e166a3c2075ece646327743b3ffe2d0de91fd9b59564`;
- environment:
  `743d5b062ba7b17c1a3ac62cff6eb7a25be145ddb5bdf0a16fe54432e3086ef8`;
- frozen state:
  `d1a04fb303a1ed4b88941e18268de42dd09a7219a97ce70706e12a44fe166970`.

v039 raw predictions are byte-identical to the disclosed v038 raw predictions;
the summary differs only because its experiment ID is v039.

## Metrics

Overall accuracy:

| Method | Accuracy |
|---|---:|
| ECDS | 0.5396825396825397 |
| full action gain | 0.4984126984126984 |
| null differential likelihood | 0.4666666666666667 |
| full action likelihood | 0.4444444444444444 |
| full differential likelihood | 0.4126984126984127 |

The strongest control is `full_action_gain`. Candidate delta is
`0.041269841269841234`. Source-cluster bootstrap delta is
`[-0.0033444816053511683, 0.04147683233453692, 0.08911048748186917]`
for lower 95%, median and upper 95%.

Source ECDS accuracy / strongest-control delta:

- BFCL: `0.43243243243243246 / -0.04504504504504503`;
- GTA: `0.7033898305084746 / +0.10169491525423735`;
- ToolTalk: `0.45348837209302323 / +0.06976744186046507`.

Against the strongest control, ECDS has 34 corrections and 21 regressions.
There are no method ties. Differential positions range 1--2,596, median 26.
Sequence lengths range 84--7,968, median 256. Truncated sequence count is zero.
ECDS margin quartiles are approximately `-0.99615`, `0.10289`, `0.97712`.

The gain is source-dependent: GTA carries the strongest benefit while BFCL is
both below chance-like ranking and worse than the strongest control. This
cannot be repaired by narrowing the claim after seeing Development.

## Independent replay and environment

- audit runner / child exit: `0 / 0`;
- audit duration: `98.47787719999906` seconds;
- audit execution:
  `f4685b2e5df4eebb7e760b53d2d22ed78ad1b07f6b98db610bc77e26343261ec`;
- report:
  `5f593b7f32a7bb7cb958f3c26a70edcf0a7cfa66282f975ee272bdfb12f83da4`;
- 315 rows / 1,260 sequences recomputed;
- 12,008 numeric and 10,408 exact values checked;
- mismatches `0`, maximum numeric error `0.0`.

Environment capture confirms Python 3.11.15, NumPy 2.3.5, PyTorch
2.12.0+cu130, CUDA runtime 13.0, Transformers 5.14.1 and NVIDIA GeForce RTX
5060 Ti capability 12.0. `PYTHONDONTWRITEBYTECODE=1`.

## Gate evaluation

| Gate | Result |
|---|---|
| accuracy at least 0.65 | FAIL |
| delta at least 0.025 | PASS |
| bootstrap lower bound greater than 0 | FAIL |
| every source accuracy at least 0.55 | FAIL |
| all source deltas nonnegative, at least two positive | FAIL |
| beat full differential and full action gain | PASS |
| beat null differential likelihood | PASS |
| independent replay within 1e-6 | PASS |

Total: `4/8`. This is a scientific no-go, not an execution or audit ambiguity.
