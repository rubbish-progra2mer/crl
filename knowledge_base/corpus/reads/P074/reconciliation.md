# P074 Reconciliation

- Disposition: `ACCEPTED_WITH_CONTRACT_RELATIVE_AND_NO_ROLLBACK_BOUNDARY`
- Read 1 SHA-256: `f6667f716caa222009b30b4d3cc89849b47350928e8efac338b345f1696ea244`
- Accepted read-2: `read_2_attempts/r2-20260720-p074-a1/`
- Final invocation SHA-256: `f7ae18654dcc77a05f2597f767d04d56776f5f8dff539f8806a2b7ac69a05b46`
- Read-2 report SHA-256: `23b63bc5c0419dff48ddf7793157363b0a7329848c40f2c40eb14ab038e4975f`
- Other attempts: none; no read-3 required.

## Provenance note

Post-completion edits to the invocation only corrected the future-dated snapshot field and filled reader/report metadata. The exact request and Frozen prompt bytes used by the independent reader are unchanged.

## Source reconciliation

- `AGREE`: ToolGate adds a real post-execution control point beyond a precondition check: a returned result changes typed trusted state only after `Q` and well-formedness pass. No-Q ablations are materially below the full method on both reported backbones.
- `NARROWED`: “verified” means relative to the provided contract. Roughly 25% of ToolBench tools fall back to `Q=True`, and ToolBench response shapes are LLM-assisted expected schemas rather than ground-truth specifications.
- `NARROWED`: the shown automatic contracts are mainly presence/type/explicit-length checks. Rich semantic predicates, `InitState`, `Update_t`, conflict handling, and extractor error rates are not sufficiently specified.
- `FAILURE_RETAINED`: structurally valid but false outputs can enter state; an incorrect or stale contract can create false trust; a postcondition cannot undo an external side effect that already happened.
- `FORMAL_BOUNDARY`: the theorem is conditional on sound contracts, sound updates, and valid initial invariants. The operational algorithm checks `P`, not the stronger pre-call weakest-precondition quantity used in the formal appendix.
- `EVALUATION_WARNING`: main results mix retrieval/reranking/search/contracts, omit variance and judge details, and report only three of six MCP-Universe domains. End-to-end runtime is not an isolated contract-check cost.

## Frozen source role

Contract-gated tool state-commit Operator + incomplete-contract false-verification Failure. It is not a transaction rollback, factual verifier, or complete external-side-effect safety mechanism.
