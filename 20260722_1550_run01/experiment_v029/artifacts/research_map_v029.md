<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p087-structured-query-independent-expansion","ev-p087-fields-not-universally-beneficial"]
-->
# Research Map v029

## Failure and intervention

P084 shows that adding related functions to fixed requests causes wrong-function and parameter-side errors. P087 shows that documentation fields are not uniformly beneficial. v029 tests whether a tool’s relevance should require complementary support from both its operation description and argument contract rather than treating a high score from either component as sufficient.

## Fixed counterfactual computation

For every query/tool pair, the same pinned cross-encoder scores four deterministic texts:

1. `full`: split tool name, source operation description and recursively serialized parameter schema;
2. `without_operation`: split tool name plus parameter schema;
3. `without_arguments`: split tool name plus operation description;
4. `name_only`: split tool name.

Define `operation_drop = full - without_operation` and `argument_drop = full - without_arguments`. Candidate `dual_necessity` is:

`full + min(operation_drop, argument_drop)`.

There is no learned coefficient, standardization, fitting, generated text, query decomposition, TPPA span, assignment, hierarchy or threshold. The `name_only` score is retained for integrity and interaction diagnostics but does not enter Candidate ranking.

## Mandatory controls

- `full_schema`: unchanged full score;
- `operation_schema`: `without_arguments`;
- `argument_schema`: `without_operation`;
- `additive_support`: `full + 0.5 * (operation_drop + argument_drop)`;
- `max_support`: `full + max(operation_drop, argument_drop)`.

Strict superiority over every control is required. This isolates the smaller-drop conjunction from extra model calls, deletion itself, single-field evidence, ordinary averaging or best-field selection.

## Development and Confirmation

Development uses the fully exposed 200-query P084/BFCL v3 expanded-toolkit files. Query folds `SHA256(query_id)[1] mod 5` are evaluation slices only; nothing is fit. The strongest comparator is frozen by top-1, then MRR, then lexicographically greatest name.

All Development gates are conjunctive: Candidate top-1 at least `0.95`; Candidate-minus-full top-1 at least `+0.015`; strict top-1 superiority over all five controls; Candidate-minus-strongest MRR bootstrap lower `>0`; corrections exceed regressions versus full; all five fold MRR deltas are nonnegative and at least three positive; complete identity/ranking/audit integrity.

Only a positive main-Codex Promotion Audit may acquire BFCL v4 live-multiple from commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`. Confirmation uses the identical formula with no fitting or comparator reselection and requires Candidate top-1 and MRR above the frozen strongest control, top-1 bootstrap lower `>=0`, corrections exceeding regressions, strict top-1 superiority over all controls, exact normalized-query-hash disjointness and complete integrity.

## Claim ceiling

The maximum possible Claim is a fixed-protocol result for complementary operation/argument deletion support on two pinned BFCL compact related-tool menu datasets. It excludes argument correctness, complete call-set recall, execution, Agent success, causal semantics, generic retrieval superiority and first-ever novelty.

