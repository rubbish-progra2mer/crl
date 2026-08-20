# v036 Raw Analysis

## Capture and reproduction

Development exited `0` after `210.43340929999977` seconds. Independent model
replay exited `0` after `210.7018065000011` seconds and reproduced:

- 315 rows;
- 2,520 prompts;
- 19,570 numeric values;
- 10,580 exact values;
- zero mismatches;
- maximum numeric error `0.0`.

The captured environment is Python 3.11.15, PyTorch 2.12.0+cu130, CUDA 13.0,
Transformers 5.14.1 and NVIDIA GeForce RTX 5060 Ti, capability 12.0.

## Metrics

| Method | Accuracy |
|---|---:|
| SDEJ | 0.507937 |
| full pair | 0.519048 |
| full pointwise | 0.561905 |
| difference without evidence | 0.674603 |
| forward-only difference | 1.000000 |

The preregistered strongest control is `delta_forward`, so the formal
Candidate delta is `-0.492063`. Its source-cluster bootstrap interval is
`[-0.553799, -0.426512]`, median `-0.492536`.

SDEJ source accuracies are:

- BFCL `0.536036`;
- GTA `0.521186`;
- ToolTalk `0.453488`.

All three source deltas against the strongest control are negative.

## Position behavior

The forward-only value is not scientific success. The benchmark stores the
preferred action in the first slot for every row, and the frozen small judge
selected displayed option A:

- on `315/315` forward SDEJ prompts;
- on `313/315` reverse SDEJ prompts.

Thus `delta_forward=1.0` is a position shortcut. It is retained because it was
preregistered, but it cannot be interpreted as action discrimination.

Bidirectional aggregation cancels two nearly identical A-position
preferences. Candidate order consistency is only `2/315 = 0.006349`.
Forward A-probability median is `0.743168`; reverse A-probability median is
`0.737158`. SDEJ margin median is exactly `0`, with 10th/90th percentiles
`-0.029533` and `0.033462`.

This is direct evidence that Qwen3-0.6B did not use the localized content
reliably under the frozen prompt.

## Paired behavior

Against full pointwise, SDEJ records 62 corrections, 81 regressions and 172
ties. Against evidence-free differences it records 26 corrections, 79
regressions and 210 ties. Against full pair it records 55 corrections, 56
regressions and 204 ties.

Representative full-pointwise regressions read directly from source and raw
bytes include:

- BFCL row 1: `cp` destination `archives` versus a renamed destination;
- BFCL row 2: `cat test_report.docx` versus a `find` call;
- BFCL row 8: logarithm precision 2 versus 10;
- BFCL row 13: navigation to the returned shop versus a text-only response;
- BFCL row 15: funding the account versus repeating symbol lookup.

Evidence-free differences also beat SDEJ on repeated frozen date contrasts
such as 2026 versus 2024 flight dates. Adding history/contracts did not
identify the intended action; it often moved the bidirectional average to the
wrong side of zero.

## Gate audit

| Gate | Result |
|---|---|
| candidate accuracy >= 0.70 | FAIL |
| delta >= 0.025 | FAIL |
| bootstrap lower > 0 | FAIL |
| every source accuracy >= 0.58 | FAIL |
| all source deltas nonnegative and >=2 positive | FAIL |
| strictly beat full pair and pointwise | FAIL |
| strictly beat evidence-free difference | FAIL |
| independent reproduction | PASS |

Result: `1/8`.

The Candidate is falsified on exposed Development. No threshold or prompt
adjustment is permitted within v036.

