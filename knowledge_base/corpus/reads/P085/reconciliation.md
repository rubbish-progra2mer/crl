# P085 Reconciliation

- Disposition: `FAILURE_AND_BASELINE_ADMISSION_WITH_TRAINING_CONFLICT_EXCLUDED`
- Read 1 SHA-256: `eedc27c897701f72edbeed6c34af7422c95c6d0139a1bf3a50f970bea6fcfed2`
- Accepted read-2: `read_2_attempts/r2-20260720-p085-a1/`
- Read-2 invocation SHA-256: `5bc5e866d0fa5cc22dd4dbcca5f977c02b704de6d089b290ffbc6f72e29f9274`
- Read-2 report SHA-256: `2b028e01ab2c5b49d522134f5af040b3d4a8dac346e778d26dd011489c0bd1c6`
- Other attempts: none
- Read 3: not triggered. The unresolved hard-negative count/miner conflict is internal to the source and cannot be adjudicated by rereading the same bytes; the disputed detail is excluded from formal knowledge rather than guessed.

## Source reconciliation

- `AGREE`: TOOLRET contains 7,615 sampled retrieval tasks and 43,215 merged tools from 34 source datasets, divided into Web, Code and Customized domains.
- `DIRECT_FAILURE_EVIDENCE`: retrieval over the full heterogeneous corpus is materially harder than retrieval inside each source toolset. A tiny or oracle menu therefore cannot stand in for open-corpus tool retrieval.
- `LABEL_BOUNDARY`: target tools inherit source-dataset labels and are not an exhaustive relevance judgment over the merged corpus. Functionally usable unlabeled tools can be metric false negatives.
- `INSTRUCTION_BOUNDARY`: the target-aware instruction is generated from the query plus ground-truth target descriptions. It is a supervised diagnostic/training channel, not ordinary query-only open-world retrieval.
- `TRAINING_CONFLICT_EXCLUDED`: the PDF conflicts over whether hard negatives are mined by NV-Embed or the trained model and whether each instance contains five or ten negatives. CRL does not encode a fixed miner/count, a reproducible recipe, or a causal claim about that component.
- `BOUNDED_BASELINE_ROLE`: tool-specific query–tool training is retained only as a learned-retriever baseline family. It does not establish parameter correctness, output faithfulness or downstream semantic correctness.
- `DOWNSTREAM_BOUNDARY`: the ToolBench experiment shows a restricted association between retrieval changes and official pass rate; it does not decompose planning, tool choice, arguments, execution and answer synthesis, and the reported oracle condition is not a strict upper bound.
- `NO_SEMANTIC_SUCCESS_CLAIM`: improved NDCG/Recall/Completeness cannot by itself certify an executable or semantically correct tool call.

## Frozen source role

Direct Failure source for the oracle-menu assumption and a bounded strong-baseline source for learned tool retrieval. The formal knowledge excludes the source-internal hard-negative recipe conflict and does not promote retrieval metrics into end-to-end correctness.
