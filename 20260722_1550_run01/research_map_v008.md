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

ToolDreamer uses Hungarian one-to-one matching between LLM-generated hypothetical tools and gold tools, but its square matrix always returns a match and the authors call the alignment a potentially imperfect proxy. [[evidence:ev-p089-forced-alignment-proxy]] v008 therefore cannot claim novelty from the Hungarian algorithm or one-to-one matching alone; the material delta must be typed query-value-to-required-parameter partial matching with null assignments, no hypothetical-tool generator, no gold tool count, and no training labels at inference.

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
