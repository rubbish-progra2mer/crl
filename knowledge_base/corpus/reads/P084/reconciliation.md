# P084 Reconciliation

- Disposition: `FAILURE_ONLY_ADMISSION`
- Read 1 SHA-256: `bd4f9db038b1badfffaf3db5f23b7b53b974dab8dcd6296520292160b9e5942f`
- Accepted read-2: `read_2_attempts/r2-20260720-p084-a1/`
- Read-2 invocation SHA-256: `639368bac3b69d62519631238cb0487fcad95e0831b8d35f9379ff42572da27c`
- Read-2 report SHA-256: `418ba8ff3262230c58847d78d0a9a87b3202860a5442bfb9d424e9e42c5bb684`
- Other attempts: none
- Read 3: not triggered; the two reads agree on the intervention, result and boundary, and the source affects one narrow Failure rather than multiple Operators.

## Source reconciliation

- `AGREE`: the comparison holds the original BFCL request, evaluated model and AST framework fixed while expanding the visible toolkit from mean 2.7 to 5.6 with about three semantically related but intended-to-be-distinct functions per case.
- `DIRECT_NEGATIVE_EVIDENCE`: all nine tested models have lower displayed AST accuracy under expanded toolkit; expansion-condition failures include wrong function, wrong number of functions and wrong parameter assignment.
- `CLAIM_NARROWED`: the source proves those error types occur within the expansion failures, not the category-specific increase from baseline, because baseline error-type distributions and paired transitions are not reported.
- `ARGUMENT_BOUNDARY`: wrong parameter assignment and parameter hallucination are supported; runtime invalid-argument exceptions are not, because the paper executes only BFCL AST phase one.
- `CONTROL_BOUNDARY`: added tool definitions increase prompt length, while decoding settings, seeds, repeat counts, tool ordering and exact per-case added-tool counts are not reported. The result is not an equal-token causal isolation.
- `DATA_BOUNDARY`: one 200-example single-turn BFCL subset is expanded with LLM-generated related requests/tools and a 0.8 cosine signature filter; the filter is not formal functional-equivalence proof.
- `NO_OPERATOR_ADMISSION`: the similarity filter is offline benchmark cleaning, not an online router. The paper establishes a Failure and evaluation requirement, not a successful filtering Operator.
- `TABLE_WARNING`: the printed Claude-3.5-Haiku relative percentages conflict with the displayed absolute scores; CRL records only the unambiguous displayed-score direction/range and error categories.

## Frozen source role

Direct negative evidence that semantically related toolkit expansion can destabilize function-call construction under a fixed request/model comparison. The source is consumed by one Paper Card and one Failure Card; no positive routing/filtering Operator is extracted.
