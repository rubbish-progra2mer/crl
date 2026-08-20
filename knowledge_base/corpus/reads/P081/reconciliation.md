# P081 Reconciliation

- Disposition: `ACCEPTED_AS_FIXED_BUDGET_BASELINE`
- Read 1 SHA-256: `127e3942e81715bebf10ba63616be44020a89ae89d70aaaa5fefa0aeb66e899a`
- Accepted read-2: `read_2_attempts/r2-20260720-p081-a1/`
- Read-2 invocation SHA-256: `67e5b306cdc0c647d08c425632d6183bfea9ca614b8814ae83f4e02259107b45`
- Read-2 report SHA-256: `7f47789b5bb61df6a8a36af6db1bca17584bcfaa3887d9fbe0c64d6b90f33105`
- Accepted read-3: `read_3_attempts/r3-20260720-p081-a1/`
- Read-3 invocation SHA-256: `1aa2c9ba177a330fe043e476fada7bfc6f653f87892d1db78d56f34d04239968`
- Read-3 report SHA-256: `a7272d808a48b051a353dbf11b61680662d0c448d66c7ecc683cd2d6665683f3`
- Other attempts: none.

## Source reconciliation

- `AGREE`: self-consistency independently samples reasoning paths from one model/prompt, extracts final answers and applies unweighted answer-frequency aggregation without training, verifier or inter-sample communication.
- `ROLE_NARROWED`: CRL admits it as a canonical compute baseline for search, debate, reflection and multi-Agent work, not as a complex new Agent Operator.
- `BUDGET_BOUNDARY`: headline gains compare forty paths with one greedy path. Same-candidate-count comparisons against sample-and-rank, beam and output-count-matched prompt ensembles support aggregation, but token, cache, FLOP and wall-clock remain unmatched.
- `ANSWER_SPACE_BOUNDARY`: the method assumes a fixed or normalizable answer space and task-specific parser. Open-text semantic equivalence, alias grouping and free-form implement aggregation are not solved.
- `GROUNDING_BOUNDARY`: majority agreement does not verify reasoning. The paper documents nonsensical and factually inaccurate paths and offers no guarantee against correlated wrong consensus.
- `RESOURCE_BOUNDARY`: several main models are unavailable proprietary systems and the reported TPU/API inference is substantial; five or ten paths are only a suggested cost compromise.

## Frozen source role

Baseline Operator and negative measurement rule: any interactive or multi-Agent gain using multiple generations must beat equal-candidate independent sampling before the interaction structure receives causal credit.
