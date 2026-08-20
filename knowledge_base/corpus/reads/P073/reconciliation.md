# P073 Reconciliation

- Disposition: `ACCEPTED_AS_SUPERVISED_OUTCOME_PROBE_WITH_TRANSFER_LIMITS`
- Read 1 SHA-256: `aa8ec7633e7fdc0029d8b6d32507d4fe38b4501ba8b70f683432edc736afaab2`
- Accepted read-2: `read_2_attempts/r2-20260720-p073-a1/`
- Final invocation SHA-256: `8c496194892295b8cb886dbb35763b403ae2208a489ad1d45607457d7d516375`
- Read-2 report SHA-256: `37623c6e0a55cc2987cf224a33831ebceca8a11cdc5bad9ae5a61f58e289346b`
- Other attempts: none; no read-3 required.

## Provenance note

Post-completion edits to the invocation only corrected the future-dated snapshot field and filled reader/report metadata. The exact request and Frozen prompt bytes used by the independent reader are unchanged.

## Source reconciliation

- `AGREE`: PROBECAL fits an MLP from accessible LLM representations to binary ground-truth execution success and uses it before generation for prompt allocation and after execution for trace-weighted answer aggregation.
- `NARROWED`: this is supervised in-domain outcome modeling, not oracle-free, zero-shot, online, or step-level uncertainty. It requires labeled calibration tasks, candidate execution, and hidden representations.
- `NARROWED`: tested tasks are program-aided MATH/TabMWP; no evidence establishes transfer to stateful Web/API Agent distributions or closed-source embeddings.
- `NEGATIVE_RETAINED`: temperature scaling adds little, verbal confidence can underperform, E.S.L./SORT variants can degrade, and prompt+trace combination is not uniformly best.
- `EVALUATION_WARNING`: baseline ECE uses an all-one confidence vector and is not a matched calibration estimator; candidate count/tool-execution budget is not fully recoverable and no variance/significance is reported.
- `OPEN_REPRODUCTION`: embedding layer/pooling, prompt sampling normalization, logits-versus-probabilities combination, and per-training-question trace budget remain unspecified.

## Frozen source role

Execution-supervised prompt/trace calibration Operator + internal-confidence-versus-execution-success Failure. Retrieval must surface the supervision, candidate-budget, distribution-shift, and hidden-embedding preconditions with the Operator.
