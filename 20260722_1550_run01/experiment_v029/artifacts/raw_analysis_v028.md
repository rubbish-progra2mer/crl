# Main Codex Raw Analysis v028

## Byte and replay integrity

- Development runner exit `0`; duration `11.45576119999896s`.
- Execution SHA-256 `3e5feadddc6edf4c6b9fd231903bba1fc19bdc9c259a19c87535d95375a87b94`.
- Raw SHA-256 `2cb8d4502a0a8478e015f608a1ca71d00e467eea3712336c6d59743db347b604`.
- Summary SHA-256 `5b6d88370fc262f150acd4e12e46b6c1f66a3587a2be7db870ff1b936d0b3850`.
- Model SHA-256 `d04d1853500b599c929d0e33e36de58be8d86d1a080df7287153c4281d19379d`.
- Independent audit runner exit `0`; duration `10.55134580000231s`.
- Audit status `AUDIT_OK`; 3,363 cross-encoder pairs and 5,605 method scores replayed.
- Maximum field-score, method-score and metric errors are all `0.0`; audit report SHA-256 `3bc0ad342565e3bd8184998a7599d93d1b3918e845b14e23a37f9985e1beef5a`.

The main read-only traversal inspected all 200 unique queries, 1,121 menu tools, 3,363 field scores, five rankings per query, all fold assignments, gold membership, corrections/regressions and nearest ranked distractors. It found zero duplicate-tool, nonfinite-score, field/method-shape, ranking-permutation, SHA tie-break or metric-reconstruction errors.

Menu sizes were 2–8, mean 5.605: `{2:6, 3:2, 4:12, 5:67, 6:77, 7:30, 8:6}`. Fold row counts were `{0:34, 1:38, 2:39, 3:47, 4:42}`.

## Metrics

| Method | top-1 | MRR |
|---|---:|---:|
| full_cross_encoder | 0.920 | 0.9554166666666667 |
| pairwise_full | 0.920 | 0.9554166666666667 |
| equal_fields | 0.935 | 0.9629166666666668 |
| pointwise_fields | 0.935 | 0.9629166666666668 |
| menu_relative_field_contrast | 0.935 | 0.9629166666666668 |

The strongest frozen control is `pointwise_fields`. Candidate-minus-strongest top-1 and MRR are both exactly `0.0`; both 20,000-sample bootstrap intervals are `[0.0, 0.0]`.

More importantly, Candidate and `pointwise_fields` have identical top-1 correctness and reciprocal rank on all 200 rows. Candidate and `equal_fields` also have identical top-1 correctness and reciprocal rank on all 200 rows. Candidate changes full ranking order on 33 rows versus pointwise and 9 rows versus equal fields, but never changes the first-gold rank. Therefore the claimed menu-pair computation adds no measured task benefit over either mandatory field control.

Candidate corrected full-cross-encoder errors on `multiple_135`, `multiple_18`, `multiple_5`, and `multiple_52`, and regressed `multiple_175`. It retained 13 top-1 errors. The nearest wrong selections are operation-granularity confusions such as `football_league.ranking` over gold `sports_ranking`, `protein_function.mitochondria` over `cellbio.get_proteins`, and `openlibrary.books_search` over `library.search_books`; the mandatory pointwise field control makes the same top-1 choices on every one of these rows.

All five Candidate-minus-strongest fold MRR deltas are exactly `0.0`; positive folds are `0`.

## Gate reconstruction

Passed:

- Candidate-minus-full top-1 is exactly `+0.015`;
- corrections `4` exceed regressions `1`;
- all five fold MRR deltas are nonnegative.

Failed:

- Candidate top-1 `0.935 < 0.95`;
- Candidate does not strictly beat every control;
- Candidate-minus-strongest MRR bootstrap lower is `0`, not `>0`;
- positive folds `0 < 3`.

Result: `3/7` gates. No Confirmation byte may be acquired.

