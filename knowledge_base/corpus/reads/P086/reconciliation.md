# P086 Reconciliation

- Disposition: `DIRECT_OPERATOR_ADMISSION_WITH_SCHEMA_BOUNDARY`
- Read 1 SHA-256: `ca823ab9ee20d90d2ee9fae16cce0c70723eb852906cd218538dea8458849240`
- Accepted read-2: `read_2_attempts/r2-20260720-p086-a1/`
- Read-2 invocation SHA-256: `70032cacb05154222c21fd1ded4eac0cb765554795cea81b163a41a9dea95f62`
- Read-2 report SHA-256: `5190fd73d0dbd52847db8f5500a482a3b7e725e2eb12accc7a24abf018895c2f`
- Other attempts: none
- Read 3: not triggered; the independent reads agree on the computation, benchmark and direct-prior role, while the remaining limitations narrow rather than reverse the source role.

## Source reconciliation

- `AGREE`: Meta-Tool first generates a missing-tool description and required-parameter descriptions, then retrieves before invocation.
- `EXACT_CHANGED_COMPUTATION`: candidate scoring combines tool-description similarity with the mean, over hypothesized required parameters, of each parameter's maximum description similarity to any required candidate parameter.
- `DIRECT_PRIOR`: this is a direct prior for required-parameter-description-aware retrieval, not post-call output validation. Later parameter/schema routing ideas must compare against it or explain a concrete incompatibility.
- `MATCHING_BOUNDARY`: parameter matching is independent max-pooling. It has no one-to-one assignment, reuse penalty, cardinality penalty or proof that all candidate constraints are covered.
- `SCHEMA_BOUNDARY`: the method embeds natural-language descriptions of required parameters. It does not compute over full JSON Schema structure, names/types/enums/defaults, optional/nested relations, concrete user-value binding or cross-parameter constraints.
- `GENERATION_BOUNDARY`: performance depends jointly on function-missing detection, LLM-generated meta-tool descriptions and retrieval; the reported results do not isolate every component under every model/task condition.
- `DISTRIBUTION_BOUNDARY`: train and test dialogues do not overlap, but they are sampled from nearly identical distributions and similar tools may occur across splits. Cross-registry and time-shift transfer are unproven.
- `END_TO_END_BOUNDARY`: the chain ends at exact-match function-call construction. It does not validate real API availability, runtime constraints, returned content, final answer correctness, safety, latency or tool-version drift.

## Frozen source role

Operator source and mandatory closest-composition comparator for hypothesize–retrieve–invoke with required-parameter-description matching. It is not evidence that full typed-schema reasoning or downstream semantic correctness has been solved.
