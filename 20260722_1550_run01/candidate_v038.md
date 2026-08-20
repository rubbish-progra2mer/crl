# Candidate v038: ECDS Execution-Capture Correction

## Frozen scientific identity

The complete v037 Evidence-Conditioned Differential Surprisal computation is
unchanged:

- same program and independent auditor bytes;
- same 315 exposed Development rows and 195 clusters;
- same Qwen3-0.6B revision and float16 CUDA execution;
- same deterministic differential masks and four teacher-forced sequences per
  row;
- same four controls, source-cluster bootstrap and eight conjunctive gates;
- same absent, untouched 130-row ToolSandbox Confirmation;
- same claim ceiling.

The scientific Candidate ancestor SHA-256 is
`85a6636225de3465641c185db4725781731fc3d1bc7cc4413c2df63507a4096e`.

## Exact execution correction

The capture runner changes one call:

```text
- capture_dir.mkdir()
+ capture_dir.mkdir(parents=True)
```

This creates the missing `captures` parent and leaf in one operation before the
subprocess starts. It does not change subprocess argv, cwd, inputs, outputs,
environment, stdout/stderr capture or execution metadata.

Only experiment-version guards, Candidate-document SHA and freeze paths may
change for v038 bookkeeping. No retry or overwrite of v037 is permitted.

## Decision boundary

v038 permits one frozen Development capture and, only if it exits `0`, one
independent replay. The unchanged v037 Development and Confirmation gates govern
promotion. A runtime failure closes v038. A scientific gate failure leaves
ToolSandbox absent and advances the same Run without Reviewer creation.
