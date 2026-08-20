# P089 Reconciliation

- Disposition: `DIRECT_OPERATOR_ADMISSION_WITH_GOLD_COUNT_AND_COST_BOUNDARY`
- Read 1 SHA-256: `20e98f16fd43e8ec8fb911132c50613b83af68be7a7589e9b7191b6b950ed840`
- Accepted read-2: `read_2_attempts/r2-20260720-p089-a1/`
- Read-2 invocation SHA-256: `249ee791c175b2248e38515d087112001a320dc7b146e80c4f3f2648661d2f85`
- Read-2 report SHA-256: `9bd35909edb72fa30adf7c3962d2e115c8c96c3ca86efe6ae2cd7aea5a37925d`
- Other attempts: none
- Read 3: not triggered; the independent reads agree on the query-expansion computation and direct-prior role, while the remaining issues are explicit supervision, reproducibility and evaluation boundaries.

## Source reconciliation

- `AGREE`: ToolDreamer generates one or more textual hypothetical tools from a query, retrieves separately for each representation and fuses the lists with reciprocal-rank fusion.
- `TRAINING_OPERATOR`: training aligns hypothetical and gold tools with embedding similarity plus Hungarian assignment, then applies InfoNCE to TND or query-plus-TND anchors and real tools.
- `DIRECT_PRIOR`: this is a direct collision for query-side latent-tool descriptions, multi-hypothesis retrieval and list fusion. Renaming them intents, sketches or plans does not change the computation.
- `GOLD_COUNT_BOUNDARY`: training generation is told the exact number of gold tools, while inference must choose the number itself. This makes the alignment matrix square and introduces a train–test supervision difference.
- `ALIGNMENT_BOUNDARY`: Hungarian assignment forces one-to-one matches without rejection even when a hypothetical tool has no valid correspondence. It is a noisy proxy, not verified tool equivalence.
- `BEST_VARIANT_BOUNDARY`: the strongest reported QTND representation includes the original question; results do not support the stronger claim that hypothetical metadata alone always improves every metric.
- `FUSION_BOUNDARY`: RRF is deterministic only given fixed ranked lists. The upstream LLM generation remains unspecified with respect to seeds/decoding, and the PDF omits enough RRF detail for exact reproduction.
- `COST_BOUNDARY`: the method adds LLM generation latency and may require a paid GPT generator; the reported cost and single-example latency are not a production distribution. CRL treats the open generator as a separate comparator and requests user approval before any paid reproduction.
- `END_TO_END_BOUNDARY`: experiments stop at retrieval metrics. They do not establish correct tool selection by an Agent, argument correctness, execution success or final task accuracy.

## Frozen source role

Operator source and mandatory closest-composition prior for hypothetical-tool query expansion, learned hypothetical-to-real alignment and multi-list fusion. It is not evidence that the generated tools are executable or that retrieval gains transfer to end-to-end semantic correctness.
