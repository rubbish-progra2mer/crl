# Main-Codex Implementation Audit v037

Status: `PREFREEZE_ACCEPTED_FOR_ONE_DEVELOPMENT_EXECUTION`.

The main Codex personally inspected `program.py`, `audit.py`, the configuration,
all 315 exposed Development rows and the frozen model manifest. No subagent was
used.

## Prefreeze defect and correction

The first all-row token-alignment scan exited `0` and found seven pure
insertion/deletion pairs whose shorter side had zero non-shared tokens. The
unfrozen implementation would therefore have stopped before model execution.

Before any freeze or Development execution, the computation was corrected once:
each non-equal `SequenceMatcher` opcode marks its replacement/insertion/deletion
tokens; the empty side of a pure insertion/deletion marks the immediately
following shared boundary token, or the preceding token for an end edit. The
Candidate, Research Map, nearest-prior boundary, selection context and config
Candidate hash were updated together.

The post-correction all-row static build exited `0`:

- 315 rows and 1,260 teacher-forced sequences;
- every differential mask nonempty and in bounds;
- minimum/maximum differential positions per sequence: 1 / 2,596;
- maximum sequence length: 7,968, below the 12,288 cap;
- zero full-context truncations;
- 166 deterministic batches, maximum batch size 8.

## Executable review

`program.py`:

- validates exact Development data and external model bytes;
- selects only contracts implicated by the two actions;
- constructs full and fixed evidence-withheld contexts;
- scores the exact action tokens with teacher forcing;
- reports ECDS and four mandatory matched controls;
- freezes the Development-selected strongest control and summary hash;
- contains no generation, fitting, threshold tuning, source calibration,
  Confirmation access or automatic promotion.

`audit.py` is a separate executable byte stream. It independently rebuilds all
rows, differential masks, contexts, batches, log probabilities, raw metrics,
source-cluster bootstrap values and summaries, then compares every exact and
numeric value to the primary output at tolerance `1e-6`.

## Verification

With `PYTHONDONTWRITEBYTECODE=1` and the shared Python 3.11.15 interpreter:

- six unit tests passed, exit `0`;
- AST parsing of all six Python files passed, exit `0`;
- the all-row static build passed, exit `0`;
- no `__pycache__` or `.pyc` remained;
- ToolSandbox file count remained zero.

One no-data synthetic Qwen check intentionally compared a padded batch against
separate unpadded forwards and exited `1`: the maximum mean-log-probability
difference was `0.0051479339599609375`, exceeding an incorrectly strict
`1e-6` assertion across different batch shapes. It used no ToolPRMBench row and
produced no scientific metric.

One bounded follow-up separated indexing from numerical batch-shape effects. It
exited `0`: a deterministic fake model verified target positions, while the same
padded Qwen batch produced maximum error `0.0` between full logits and
`logits_to_keep` logits. The exact model device was `cuda:0`, dtype
`torch.float16`. No code change followed this check.

## Executable hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 27,605 | `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17` |
| `audit.py` | 29,749 | `abfcb551889d3e0051feee788be45192b80bbfd4bc344159ddc97e62d2dcb0a6` |
| `config.json` | 1,674 | `bbd7c007b95ef83ec0eeb663f7c88ec28f42b174d1af1041e891aa22f8eb7273` |
| `test_program.py` | 2,969 | `f98af7ecd9424b5c60b3372e528a96bfd6a7d6941b150c84cc10970c11d29d45` |
| `acquire_confirmation.py` | 2,009 | `df2e008db3b96e56555434055d013fd2b3343e95454dd1a2a51127ce88287f69` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |
| `freeze_artifacts.py` | 5,016 | `1135861cef2bab9f8c861d2d5d9b09fb34e51687cd1ed745c69b9a5a6d137e58` |

This audit authorizes exactly one frozen v037 Development capture and, only
after a successful primary execution, one independent replay audit. It does not
authorize Confirmation, Review, Delivery or a system-state transition.
