# Main Codex Raw Analysis v029

## Mechanical integrity

- Development runner exit `0`; duration `10.970545399999537s`.
- Development execution SHA-256 `3075e5bef184403d6b3d14097ef98abfdbf3e7defb7d208e14003b37fea2d2f5`.
- Raw SHA-256 `f69c56403fcce9e417c565d92ba6f1e1063c77d257b34e4e0820193f9b8b3a6a`; summary SHA-256 `2b0622cfaa3b892f6df6f7ce938d7fb5279d8ab22cc29e44ba7160ce3af05c86`.
- Independent audit exit `0`, `AUDIT_OK`, duration `11.30999249999877s`.
- The audit independently replayed 4,484 view scores and 6,726 method scores; maximum view, method and metric errors were all `0.0`.
- Audit report SHA-256 `336ff99c91ecff3ce925c7739bd9b8a116165daaab4edac06eaf73fda4083af1`.

The main traversal inspected all 200 unique queries, 1,121 tools, four view scores and six method scores per tool, every deletion drop, ranking, fold, correction/regression, menu size and nearest top distractor. It found zero identity, nonfinite, formula, permutation, tie-break or metric errors.

## Metrics

| Method | top-1 | MRR |
|---|---:|---:|
| full_schema | 0.920 | 0.9554166666666667 |
| operation_schema | 0.880 | 0.9279166666666667 |
| argument_schema | 0.900 | 0.9426666666666668 |
| additive_support | 0.900 | 0.9455833333333333 |
| max_support | 0.890 | 0.9370833333333333 |
| dual_necessity | 0.905 | 0.9428333333333333 |

The strongest comparator is the unchanged full schema. DCN is `-0.015` top-1 and `-0.012583333333333334` MRR below it. The MRR bootstrap interval is `[-0.02791875, 0.0013333333333333333]`; the top-1 interval is `[-0.04, 0.01]`.

DCN corrects only `multiple_135` and `multiple_68` relative to full, while regressing `multiple_119`, `multiple_38`, `multiple_58`, `multiple_72`, and `multiple_79`. It leaves 19 top-1 errors.

Of 1,121 tools, only 424 have both deletion drops positive; 697 have at least one negative drop. The smaller-drop conjunction therefore penalizes many otherwise correct full-schema rankings. It does not isolate useful complementary necessity in this frozen representation.

Fold MRR deltas versus full are positive only in folds 0 and 3 and negative in folds 1, 2 and 4.

## Gate reconstruction

Every prospective gate failed:

- Candidate top-1 `0.905 < 0.95`;
- Candidate-minus-full top-1 `-0.015 < +0.015`;
- Candidate does not strictly beat every control;
- MRR bootstrap lower is negative;
- corrections `2` do not exceed regressions `5`;
- three of five fold deltas are negative;
- positive folds `2 < 3`.

Result: `0/7`. Confirmation is forbidden.

