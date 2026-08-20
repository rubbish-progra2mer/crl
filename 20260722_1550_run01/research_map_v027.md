<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p087-structured-query-independent-expansion","ev-p087-fields-not-universally-beneficial"]
-->
# Research Map v027

## Failure and intervention

P084 fixes the requests while expanding a mean 2.7-tool menu to 5.6 with related functions, and reports wrong-function and argument-side failures. v027 intervenes only at function ranking. The hypothesis is that a monolithic query/full-schema score can conflate operation intent with argument compatibility; a menu-relative learner can instead estimate which frozen field-score differences distinguish the gold operation from its actual local distractors.

## Fixed computation

For each query/tool pair, the pinned `cross-encoder/ms-marco-MiniLM-L6-v2@c5ee24cb16019beea0893ab7796b1df96625c6b8` produces three scores:

1. `full`: split function name, description and recursively serialized parameter schema;
2. `operation`: split namespace/function-name tokens plus function description;
3. `arguments`: deterministic recursive paths, names, types, descriptions, enums, required/optional/default markers for all schema nodes.

No generated text, dense model, TPPA span extractor, type bonus, assignment, null threshold or per-query rule is used. Query fold is `SHA256(query_id)[1] mod 5`. A training-only standardizer is fit on candidate-tool feature rows from other folds. The Candidate creates both orientations of every gold/non-gold pair in a training menu, weights each menu's pairs to total one, and fits zero-intercept L2 logistic regression with C=1 and seed 12027. A tool's scalar rank score is the learned linear score of its standardized three-field vector. Every Development query is ranked once by an OOF model; one full Development model is frozen only for conditional Confirmation.

## Controls

- `full_cross_encoder`: unchanged primary baseline;
- `equal_fields`: arithmetic mean of standardized full/operation/argument scores, isolating factorization without learned weights;
- `pointwise_fields`: same standardized three fields and learner, but independent gold/non-gold candidate labels with one total weight per menu;
- `pairwise_full`: the Candidate pairwise objective using only the full-schema score, isolating menu-pair training without field factorization;
- Candidate `menu_relative_field_contrast`: pairwise three-field differences.

No claim may come from pairwise logistic regression, schema serialization, cross-encoders or field splitting alone. The only supported delta would be their fixed composition against all four controls.

## Development gates

Top-1 is correct when the first-ranked function belongs to the ground-truth function-name set; MRR uses the first gold name. Multi-gold rows do not establish full call-set recall. The strongest comparator is selected prospectively by Development OOF top-1, then MRR, then lexicographically greatest method name.

All Development gates are conjunctive: Candidate top-1 at least `0.95`; Candidate-minus-frozen full-cross-encoder top-1 at least `+0.015`; Candidate strictly exceeds every control in top-1; Candidate-minus-strongest MRR task-row bootstrap lower bound `>0`; Candidate produces more baseline-error corrections than regressions; all five folds have nonnegative Candidate-minus-strongest MRR and at least three are positive; every query/tool/field/model/input/output/capture/audit binding is current. Mechanical booleans cannot authorize Confirmation.

## Conditional Confirmation

Only a positive main-Codex Promotion Audit may acquire pinned BFCL v4 live-multiple queries and possible answers. Exact normalized-query hashes must be disjoint from Development. The full Development standardizer/models and frozen strongest comparator then score every Confirmation menu without fitting, rule change or comparator reselection.

Confirmation requires Candidate top-1 and MRR strictly above the frozen strongest comparator, paired top-1 bootstrap lower bound `>=0`, more corrections than regressions, strict top-1 superiority over every control, query-hash disjointness and complete integrity. A positive main Confirmation Audit is required before Review.

## Prior collision and claim ceiling

ToolRerank trains a cross-encoder on hard negatives, then changes candidate truncation by seen/unseen status and groups APIs by tool hierarchy for concentration/diversity. TOOL-DE performs query-independent generated document expansion and shows that fields are not uniformly helpful. Meta-Tool matches hypothetical required-parameter descriptions. Generic pointwise/pairwise reranking is established. None permits novelty claims for those pieces. The maximum contribution is a fixed-protocol result for deterministic real-schema field scores learned through local menu-pair differences on two pinned BFCL versions.
