# v037 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

No v037 Development metric exists. ToolSandbox remains absent, unacquired and
unread. This Packet binds one scientifically distinct computation for one
Development execution; it is not a Review Packet or Delivery evidence.

## Candidate identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v037.md` | 2,714 | `3ebdc264d28d9ce0707dc4ddcd84d4b70b4b2ed3388eb1fd60b082ad445ce3cc` |
| `problem_v037.md` | 649 | `91caa02089085acb80c0d68c0769ea5a390006ac9346dd2dbc5e65cecaafb472` |
| `research_map_v037.md` | 1,820 | `c88f1a4ce3ce09c4192c39992660def86581c73d012724723c6977667e656b1a` |
| `nearest_prior_v037.md` | 1,420 | `388a9d24451e2dced71f4f847b94925cd51ee0b4fc96deb215f6e7f22ea3d947` |
| `candidate_v037.md` | 2,915 | `85a6636225de3465641c185db4725781731fc3d1bc7cc4413c2df63507a4096e` |
| `implementation_audit_v037.md` | 4,110 | `d4538e1b1830511911a026a75b271e68b4129f8c38552b2c61a9a0eb362b6784` |

## Executable identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 27,605 | `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17` |
| `audit.py` | 29,749 | `abfcb551889d3e0051feee788be45192b80bbfd4bc344159ddc97e62d2dcb0a6` |
| `config.json` | 1,674 | `bbd7c007b95ef83ec0eeb663f7c88ec28f42b174d1af1041e891aa22f8eb7273` |
| `test_program.py` | 2,969 | `f98af7ecd9424b5c60b3372e528a96bfd6a7d6941b150c84cc10970c11d29d45` |
| `acquire_confirmation.py` | 2,009 | `df2e008db3b96e56555434055d013fd2b3343e95454dd1a2a51127ce88287f69` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |
| `freeze_artifacts.py` | 5,016 | `1135861cef2bab9f8c861d2d5d9b09fb34e51687cd1ed745c69b9a5a6d137e58` |

## Frozen computation and controls

Evidence-Conditioned Differential Surprisal teacher-forces each action under
full history plus implicated contracts and under a fixed evidence-withheld
context. Deterministic token-ID alignment defines differential positions;
pure insertion/deletion uses the adjacent shared boundary token on the empty
side. ECDS compares the full-minus-withheld likelihood gain of chosen versus
rejected.

Mandatory controls use the same four sequences per row:

1. full-evidence differential-position likelihood;
2. full-minus-withheld evidence gain over every action token;
3. withheld-evidence differential-position likelihood;
4. full-evidence full-action likelihood.

There is no A/B verdict token, pair-position prompt, generation, fitting,
retrieval, execution, source calibration or tuned threshold.

## Development carrier

| Source | Rows | Clusters | SHA-256 |
|---|---:|---:|---|
| GTA | 118 | 92 | `dc4cfb906dd2b20ad9452b3afdca5346a4a6a3378e15667fd47fa1c21a54a23c` |
| BFCL | 111 | 52 | `3c13646f14abaaeba619d5ba91d6cc64bcd4223472eea62ab91ca94f588f14a8` |
| ToolTalk | 86 | 51 | `e5327446f854fae9d9ed5319bd5a418168626aa6327853d145e35cf87f2027a1` |

Total: 315 rows, 195 source-qualified clusters and 1,260 teacher-forced
sequences. These sources were exposed in v034--v036; choosing v037 is optional
stopping and cannot establish generalization without untouched Confirmation.

## Model and environment boundary

- Qwen3-0.6B revision:
  `c1899de289a04d12100db370d81485cdf75e47ca`;
- model manifest:
  `9518287b603d6bc25ef7cd3f98764db94a633f360faa68f57ee80ceb8cf72034`;
- model weight:
  `f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b`;
- shared interpreter: Python 3.11.15;
- frozen execution dtype/device: float16 / CUDA.

No environment package was installed or changed for v037.

## Prior-work bytes

| Source | Bytes | SHA-256 |
|---|---:|---|
| Toolformer | 657,966 | `6d7483d94653008e40c2058a1c22441c92e3713dae278b6361e8efc447c99522` |
| ToolPRMBench | 1,883,463 | `f7ac155d9862f0def0b1f5c09e992dc7b626fdf90601a8cb2e8a9bcbd6712455` |
| ToolRM | 2,287,293 | `9679fe106dfc881cfdaf7e77cd6b38c871da2e503b4964f91f2fe0a8293f714f` |
| Prior source manifest | 808 | `d1c01b550e61dd34e7be8eb25115325fa8ea0bc89fd44ce382b687017f7ea1a1` |

The main Codex directly read Toolformer physical pages 2--4. Likelihood scoring,
differential tokens and counterfactual subtraction are not individually novel.

## Gates and claim ceiling

All eight Candidate Development gates are conjunctive. The strongest control
is selected deterministically from Development and frozen in state. Only all
gates plus a positive main-Codex Promotion Audit permits acquiring the fixed
130-row ToolSandbox.

At most, a pass may claim improved pairwise next-action ranking for this frozen
small model on the exact splits against the listed controls. No Agent success,
utility, cost, safety or formal-correctness claim is permitted.

## Prefreeze verification and execution boundary

- the initial all-row scan disclosed seven empty-side insertion/deletion cases;
- the computation and documents were corrected before freeze;
- the corrected all-row static build exited `0`;
- six unit tests and six-file AST parsing exited `0`;
- one no-data cross-batch-shape numerical smoke exited `1`;
- one bounded same-batch indexing check exited `0` with maximum error `0.0`;
- ToolSandbox file count and `.pyc` count were both zero.

After Artifact Manifest creation, v037 permits exactly one Development capture
and, only if it exits `0`, exactly one independent replay audit. Confirmation,
Reviewer creation and Delivery remain forbidden until their scientific gates
are actually satisfied.
