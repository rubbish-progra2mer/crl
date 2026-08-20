<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p086-required-parameter-score","ev-p086-near-identical-distribution","ev-p089-forced-alignment-proxy"]
-->
# Research Map

## Failure And Intervention Point

P084 holds 200 original BFCL requests fixed while increasing the mean visible menu from 2.7 to 5.6 with semantically related but intended-function-different tools. All nine tested calling models lose AST accuracy, with objective errors spanning wrong function, wrong function count, wrong parameter assignment, and parameter hallucination. [[evidence:ev-p084-expanded-toolkit-controlled-setting]] [[evidence:ev-p084-related-toolkit-error-types]]

The intervention point is retrieval-time function selection before any call is generated. The desired computation must distinguish tools that share topical descriptions but require different observable argument structures.

## Mandatory Card Queries Executed

- Failure query: `semantically related toolkit expansion wrong function parameter assignment`.
- Operator query: `one-to-one typed parameter alignment tool retrieval function schema`.
- Paper query: `Meta-Tool required parameter matching expanded toolkit robustness`.

These queries returned P084 as the direct failure source, P086 Meta-Tool as the closest parameter-description component, P089 ToolDreamer as the nearest bipartite-alignment warning, and P087 document expansion as the closest representation-side alternative.

## Nearest Prior Boundaries

Meta-Tool compares a generated desired-tool description and desired required-parameter descriptions with real schemas. Its parameter score independently takes the best real required parameter for each desired parameter and averages those maxima. [[evidence:ev-p086-required-parameter-score]] It does not prevent reuse of one real parameter, encode observable argument values or types, or allow an explicit unmatched decision. Its own benchmark has near-identical train/test distribution and similar tools across splits. [[evidence:ev-p086-near-identical-distribution]]

ToolDreamer uses Hungarian one-to-one matching between LLM-generated hypothetical tools and gold tools, but its square matrix always returns a match and the authors call the alignment a potentially imperfect proxy. [[evidence:ev-p089-forced-alignment-proxy]] v009 therefore cannot claim novelty from the Hungarian algorithm or one-to-one matching alone; the material delta must be typed query-value-to-required-parameter partial matching with null assignments, no hypothetical-tool generator, no gold tool count, and no training labels at inference.

## Alternative Kernels Considered

- More v007 prompt controls were excluded by `decision_v007.md`: they would refine a known static audit rather than change a useful computation.
- A RefineBench stop/select gate was excluded before Candidate formation because the public dataset contains questions and checklists but no frozen multi-turn model outputs; a real experiment would require a new generative model and LLM Judge, while synthetic revision pairs would not be acceptable evidence.
- A contract-gated state-commit experiment was excluded because the available source documents do not provide a real downstream false-commit benchmark; injected fixtures would only prove the validator's definition.
- Full schema text expansion was excluded because P087 is a direct prior and generation would add an unfrozen LLM source.

## Selected Kernel

`Typed Partial Parameter Alignment` (TPPA) extracts observable value-bearing spans from the query without an LLM, assigns a coarse value type, embeds each span and each required parameter description, and solves a maximum-weight partial bipartite assignment. Each span and parameter can be used at most once; dummy null nodes permit rejection. Edge weights combine semantic similarity, type compatibility, and exact enum support. The normalized assignment score is fused with an otherwise unchanged frozen cross-encoder query-to-tool score.

The nearest fair comparator is the exact cross-encoder score without TPPA. Additional comparators are frozen MiniLM query-to-full-schema cosine, BM25 over the same full schema, and a relaxed parameter matcher that uses the same extracted spans, edge scores, Development-selected tuple, and fusion weight but independently takes each span's best parameter, allowing reuse. Candidate attribution is the difference between cross-encoder+TPPA and the identical cross-encoder baseline.

## Candidate Promotion Audit Before Development

The Target Failure appears directly as top-1 selection of a non-gold related function in the expanded menu. TPPA changes the function ranking decision by adding a capacity-constrained typed correspondence between user-provided values and required schema fields; it does not merely repair JSON validity, execution, formatting, or evaluation labels.

The expected signature is concentrated on examples where the highest-scoring gold function and strongest non-gold distractor differ by at most `0.5` within-menu cross-encoder z units and have different required-parameter type multisets. Gold labels define this evaluation subset only; TPPA inference never receives them. TPPA must improve top-1 membership in the ground-truth function set without using gold calls, original-menu membership, perturbed-request generators, or confirmation labels.

## Development And Confirmation Contract

Development may tune only a small frozen grid of fusion weight, type bonus, null threshold, and unmatched-required penalty on the 200 P084 items. The selected tuple is fixed by highest top-1 accuracy, then MRR, then lower fusion weight, type bonus, unmatched-required penalty, and null threshold in that order. The relaxed comparator reuses this exact tuple and is not tuned separately. No per-item adaptation is allowed.

Development opens Confirmation only if TPPA beats the frozen cross-encoder by at least 2 percentage points in top-1 accuracy, has positive paired bootstrap lower bound for MRR difference, produces more cross-encoder-error corrections than newly introduced errors, and the TPPA-specific advantage is larger on the preregistered parameter-contrast subset than outside it.

After promotion, Confirmation acquires only the pinned BFCL v4 live-multiple question and gold files. Exact query hashes must be disjoint from Development; otherwise the version fails without replacement data. The Development-selected tuple is applied unchanged. Confirmation requires positive top-1 and MRR differences versus cross-encoder, a nonnegative paired-bootstrap lower bound for top-1 difference, and more corrections than regressions. All rankings, extracted spans, edge matrices, assignments, scores, and ties must be frozen.

The maximum possible Claim is limited to improved top-1 membership in the ground-truth function set on these two pinned BFCL menu datasets. Multi-gold rows do not establish complete call-set recall. No parameter-value correctness, execution, stateful competence, end-to-end task success, or general open-world claim is permitted.

## v009 Execution-Only Revision

v008 froze and attempted the same scientific design but produced no metric. Its single Development capture exited 1 because one observed BFCL tool stored a required-name list at `properties.required` and nested one required parameter schema under another property; the frozen parser assumed every `properties` value was an object. v009 changes only strict expansion of that observed embedded-required layout. Data, models, span rules, edge computation, assignment, grid, tie order, metrics, gates, cost comparison, and untouched Confirmation source are unchanged.

## Candidate Promotion Audit After Development

The cross-encoder baseline exhibits the target final-outcome failure on 14 of 200 rows. Development and the fixed Confirmation source are dataset-version separated and must be exact-query-hash disjoint, but that design cannot support task-, template-, endpoint-, or open-world generalization. The paired analysis unit is one request row; tool candidates and edges inside a row are not independent observations.

The independently recomputed Development result is cross-encoder top-1 `0.930` and MRR `0.9591667` versus TPPA top-1 `0.935` and MRR `0.9625`. TPPA corrects one baseline error and introduces no regression, giving top-1 `+0.005` and MRR `+0.0033333`. The paired MRR bootstrap interval is `[0.0, 0.0091667]`. The preregistered 13-row parameter-contrast subset contains that one correction and has `+0.0769231`, while the outside subset has `0.0`. These values fail the frozen `+0.02` top-1 condition and the strictly positive MRR-bootstrap-lower condition.

The unique proposed capacity/null delta is not identified in the final outcome. TPPA and the relaxed reusable matcher differ on 173 tool assignments, 79 rows contain an alignment-score difference, and 21 rows have a different complete ranking, but all 200 rows have the same top-1. Both methods finish at exactly `0.935` top-1 and `0.9625` MRR. The lone corrected row, `multiple_5`, is corrected by both and includes overlapping date/entity/number spans. Its gain can support only the shared extraction/type/embedding/fusion bundle, not the capacity-one partial assignment proposed as the material method difference.

The Main Codex therefore does not authorize Confirmation. This is not a script-automatic decision: the independent audit verified 200 raw rows, 1,121 tools, 7,120 edge cells, 1,815 assignments, all 384 grid rows, all rankings, both bootstrap intervals, and the contrast subset with zero numerical discrepancy. v009 freezes as a Development-screen candidate failure; Confirmation remains unopened, no Review Packet is authorized, and the same Run must move to a scientifically different v010.
