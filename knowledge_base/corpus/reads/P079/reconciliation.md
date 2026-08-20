# P079 Reconciliation

- Disposition: `ACCEPTED_WITH_TEXT_AXTREE_AND_ORACLE_BOUNDARY`
- Read 1 SHA-256: `da88d2dd973cd2ca58695ac4b9446d1f5483a2b778175f9f891a392983e5c985`
- Accepted read-2: `read_2_attempts/r2-20260720-p079-a1/`
- Read-2 invocation SHA-256: `bbba8ed1656aad7decc9e69146a3908937c3f2975dc8a9051989ebadcfc825d4`
- Read-2 report SHA-256: `231b5ac4745723173c4aa0c8d31055c259bba2ca7a48efd5c78f84243393d0d9`
- Accepted read-3: `read_3_attempts/r3-20260720-p079-a1/`
- Read-3 invocation SHA-256: `3c870beade0b154fa3dd07e13bbc180ad3ab18e5ef93d12560bdbae9a617e079`
- Read-3 report SHA-256: `a0e76b05f1abb3627d86d76719cc22b5bb164e9d8cc10a2e1c489edb6e61d826`
- Other attempts: none.

## Source reconciliation

- `AGREE`: LCoW inserts a learned task/history-conditioned transform between raw accessibility-tree observation and the downstream decision model.
- `FUNCTION_NARROWED`: the contextualizer explicitly reasons about progress and the next action; it is an auxiliary planning/strategy conditioner as well as an observation transform. The gain cannot be assigned to neutral compression alone.
- `SCOPE_NARROWED`: only text/AXTree observations enter CRL. Screenshot, pixel, visual grounding and general GUI claims are excluded.
- `ORACLE_BOUNDARY`: training retains successful trajectories, rewards agreement with the demonstrated next action, and retries zero-score candidates with the ground-truth action as a hidden hint. This is training-time privileged action supervision, though no test action leakage is established by the source.
- `FIDELITY_BOUNDARY`: prompts request accurate IDs and structure, but the paper reports no element recall, omission, hallucination or faithfulness metric. A downstream Agent cannot recover an omitted element from the refined-only observation.
- `GENERALIZATION_BOUNDARY`: transfer to unseen decision LLMs and shared UI types is supported; truly unseen Filter-List affordances remain at zero for both tested Agents, and success-only trajectory collection leaves ten task types without seeds.
- `COST_AND_BASELINE_BOUNDARY`: every action adds a contextualizer call and training uses several strong proprietary teachers/judges. N/K, retry rate, token, latency and monetary cost are missing; raw/self-contextualization/BC and historical web-agent comparisons are not matched on total compute or teacher supervision.

## Frozen source role

Operator source for action-preserving, strategy-conditioned AXTree contextualization; Failure source for raw-observation overload, omitted unseen affordances and oracle/teacher confounding. It is not evidence for lossless generic context compression.
