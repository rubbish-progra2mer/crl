# Candidate v039: ECDS Exact-Output Capture

## Frozen scientific identity

The complete ECDS computation remains byte-identical to v037/v038: same
program, independent auditor, 315 Development pairs, Qwen3-0.6B weights,
differential masks, contexts, controls, bootstrap, eight gates, untouched
ToolSandbox and claim ceiling.

Scientific ancestor SHA-256:
`85a6636225de3465641c185db4725781731fc3d1bc7cc4413c2df63507a4096e`.

## Exact capture correction

The runner executable is unchanged from v038. The frozen invocation lists four
file outputs:

1. `raw_predictions.jsonl`;
2. `summary.json`;
3. `environment.json`;
4. `frozen_state.json`.

The program still receives one new output directory and creates it exactly
once. The runner validates that each file is absent before execution and hashes
each file after execution. No v038 byte is reused as v039 output and no v038
path is overwritten.

Only experiment-version metadata, Candidate SHA, acquisition guard and freeze
paths may change. v039 permits one Development capture and, only after exit
`0`, one independent replay. The unchanged gates govern Confirmation.
