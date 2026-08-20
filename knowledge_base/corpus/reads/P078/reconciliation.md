# P078 Reconciliation

- Disposition: `ACCEPTED_WITH_TEXT_CODE_TOOL_BOUNDARY`
- Read 1 SHA-256: `97fba8d5fe34dff7c7376a01eb35137063efd2ab7bac16872119314499612fa7`
- Accepted read-2: `read_2_attempts/r2-20260720-p078-a1/`
- Read-2 invocation SHA-256: `74b2305fc7118c08d04ad22e7723d31874630a4ef234fce63cd4498802172841`
- Read-2 report SHA-256: `bffee997e3d84cdc841f5f65bca0530e7ee6494caae31674643e49ae36ce3cca`
- Accepted read-3: `read_3_attempts/r3-20260720-p078-a1/`
- Read-3 invocation SHA-256: `a08e0ca4fae5117dc005997c75da1fd2a8d958129f73d934125340a368195aee`
- Read-3 report SHA-256: `4c1de7fcf8e9b22053ebe4a6dbd0c5ff4e08a0f72441a74333e16e5968abfc16`
- Other attempts: none.

## Source reconciliation

- `AGREE`: the changed computation is an offline create → execute-filter → abstract → replay-validate → deduplicate tool library followed by online multi-view retrieval and executable reuse.
- `SCOPE_NARROWED`: only the text/code-function mechanism and TabMWP/MATH evidence enter CRL. ImagePatch, visual encoding, VQA gains and multimodal generality remain outside scope.
- `EVIDENCE_NARROWED`: replaying the same source problem after abstraction demonstrates instance preservation, not unseen-input correctness, contract completeness, safe termination or cross-domain transfer.
- `RESOLVED_BY_SOURCE`: abstraction and three retrieval views contribute in the authors' setup, but component ablations are concentrated in VQA; they cannot be promoted to a universal text-task causal claim.
- `BASELINE_BOUNDARY`: BM25 is slightly stronger on TabMWP, while CRAFT receives generated function-name/docstring expansion. CREATOR's checking/correction loop is removed even though CRAFT retains expensive offline filtering. No equal-total-token/API/cost superiority is established.
- `COST_AND_ORACLE_BOUNDARY`: GPT-4 constructs and adjudicates the library using known source answers; reported creation cost is about USD 2,500 and detailed call/token/latency amortization is absent. CRL does not execute this paid process.
- `FAILURE_RETAINED`: provided functions include narrow assumptions and at least one unbounded equality-based loop. Low cyclomatic complexity and source-example success are not reliability guarantees.

## Frozen source role

Operator source for validated specialized tool creation and multi-view retrieval; Failure source for generic/unvalidated tool libraries, weak generalization checks and unmatched offline construction cost. It does not establish a generally safe or universally superior tool-management system.
