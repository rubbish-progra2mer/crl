# Candidate v036: SDEJ Execution-Only Correction

Scientific Candidate: Symmetric Differential Evidence Judgment (`SDEJ`).

## Unchanged computation

For each pair of proposed next actions:

1. parse mode, tool and recursively flattened argument paths;
2. remove exactly equal canonical fields;
3. retain candidate-specific fields, or deterministic
   word/punctuation-token differences for two text actions;
4. pair those differences with the frozen history and implicated contracts;
5. score bare next-token `A`/`B` probabilities in both orders with frozen
   Qwen3-0.6B and average aligned probabilities.

There is no fitting, source calibration, external retrieval, rollout,
execution or generated rationale.

Mandatory controls remain:

- `full_pair`;
- `full_pointwise`;
- `delta_no_evidence`;
- `delta_forward`.

## Sole v036 change

The model is loaded in float16 on CPU and moved to CUDA with `.to("cuda")`.
The unavailable `device_map`/`accelerate` path and deprecated `torch_dtype`
keyword are removed from both program and independent auditor. No shared
environment package is added.

## Development gates

All are conjunctive and unchanged:

1. SDEJ accuracy at least `0.70`;
2. delta over strongest mandatory control at least `0.025`;
3. source-cluster bootstrap 95% lower bound greater than `0`;
4. every source accuracy at least `0.58`;
5. all source deltas nonnegative and at least two positive;
6. SDEJ strictly exceeds `full_pair` and `full_pointwise`;
7. `delta_no_evidence` is strictly worse than SDEJ;
8. independent reproduction error at most `1e-6`.

## Conditional Confirmation

ToolSandbox remains the fixed 130-row untouched Confirmation. It may be
acquired only after all Development gates and a positive main-Codex Promotion
Audit. Confirmation requires:

1. SDEJ accuracy at least `0.60`;
2. strict superiority to `full_pair` and `full_pointwise`;
3. positive delta to the Development-frozen strongest control;
4. positive paired-bootstrap median delta;
5. independent reproduction within `1e-6`.

## Claim ceiling

The Claim ceiling is byte-for-byte the v035 scientific ceiling: this fixed
differential evidence projection improved this frozen small judge on these
pairwise tool-action splits against the listed controls. It is not general
judge superiority, formal correctness or downstream Agent success.

