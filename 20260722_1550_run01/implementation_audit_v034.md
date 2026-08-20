# v034 Main-Codex Implementation Audit

Status: `APPROVED_FOR_PREFREEZE_PACKET_CONSTRUCTION`.

This is a preexecution code and evidence-boundary audit by the current main
Codex. It is not a Development result, Promotion Audit, Confirmation, Review,
Decision or Delivery.

## Bytes inspected

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 35,859 | `a98b6f16b270fa4350bd1cf024bbf240f692d5658eb3be298117867e1d4a8ca4` |
| `audit.py` | 43,201 | `b43735617e0e09c0294f467b187bf4b2c8771c78d35d79e420ae40fd06e629c2` |
| `config.json` | 1,789 | `4efd0437ae4987176ec3edc83179e3c2478f6cf5059a89cfbcacc0b171ae237a` |
| `test_program.py` | 2,372 | `3940f8472b87d52a132d122b8cfdefd0c2fb14576c8aa19e64376a911c1fcfb9` |
| `acquire_confirmation.py` | 2,009 | `fda9a8f4e50042e43eed73b31c801c9bc495d4f53853a28e7769ff54289803f3` |

The Candidate SHA in config equals current `candidate_v034.md`:
`8f78b67bfa14e3f9cbbd94207143e2574c6898913f2045cbb38f1cdb1d750a09`.

## Label and data boundary

I traced the prompt-construction path from `load_rows` through
`build_evidence`, `evidence_sections` and `make_prompt`.

- Prompt evidence reads only `history`, `functions` and the pointwise action.
- BFCL-only `rationale`, `error type`, `possible_answer` and `model_name` never
  enter evidence or prompts.
- Chosen and rejected actions are scored pointwise with no alternative present
  in the prompt; labels enter only held-out pair evaluation and mandatory
  learned controls.
- GTA's embedded system tool description is used when `functions` is null.
  BFCL and ToolTalk use their separate tool metadata.
- A structured-call parser recognizes the three observed call containers;
  absent calls remain an explicit non-call rather than being fabricated.

The full structural scan over 315 exposed Development pairs exited `0` and
constructed exactly 630 pointwise actions and 3,780 prompts. It found 561
structured calls and 69 non-calls. Prompt lengths were 122 to 8,016 tokens
(median 903.5), with zero violations of the frozen 12,288-token cap and zero
action truncations.

## Computation and control audit

I traced each Candidate and control score from frozen logits:

- `Yes` and `No` identities are revalidated as single tokens 9454 and 2753;
- all six prompt kinds use the same fixed model, BF16 mode, native no-thinking
  chat template and next-token likelihood;
- leave-one-source-out empirical CDFs use both pointwise actions from only the
  other two sources and no labels;
- CCCB is exactly the minimum of five calibrated percentiles;
- the holistic, five single-obligation, raw-min, calibrated mean/product,
  majority, selected-single and fixed-C linear controls use the stated
  information boundaries;
- selected-single and linear controls are fitted only on the other two sources
  during Development;
- 195 fixed source/task clusters drive the 2,000-resample bootstrap;
- exact ties receive half credit and deterministic name ordering resolves
  comparator selection;
- full-Development calibration, selected-single and linear state are written
  before any possible Confirmation.

Action swapping is an algebraic invariance rather than an extra model call:
prompts are pointwise and contain no pair position, so swapping only negates
the stored pair margin. The auditor verifies prompt hashes and both pointwise
scores before checking the negation.

## Independent replay audit path

`audit.py` imports no code from `program.py`. It separately reparses every
source row, reconstructs all 3,780 prompts, reloads the frozen local model,
recomputes every next-token log probability, rebuilds calibration and learned
controls, repeats the cluster bootstrap, compares raw rows/state/summary, and
verifies environment plus runner capture hashes.

The duplicated mathematical definitions are visible frozen code, not a call to
the program or its summary. This gives a second executable path while keeping
the experiment small.

## Necessary regression

In the correct implementation cwd, the shared Python 3.11.15 interpreter ran:

```text
python -m unittest -v test_program.py
```

Exit code was `0`; all 5 tests passed. Separate strict AST parsing of all four
Python files exited `0`. Program and auditor `--help` invocations then both
exited `0`. The implementation tree contains zero `.pyc` files and zero
`__pycache__` directories.

## Model and environment feasibility

The acquired model manifest binds revision
`c1899de289a04d12100db370d81485cdf75e47ca`; its 1,503,300,328-byte weight
SHA is `f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b`.
A synthetic, non-benchmark smoke loaded the model in the shared environment on
the NVIDIA GeForce RTX 5060 Ti and produced finite `Yes`/`No` log probabilities
with exit code `0`.

The failed Qwen3-4B acquisition remains disclosed in
`selection_context_v034.md`. No 4B result, ToolSandbox byte, Development
metric, Review Packet or Delivery exists.

## Judgment

The implementation matches the narrow v034 Claim Contract and contains no
prompt tuning, generated rubric, tool execution, second model, hyperparameter
search or automatic Promotion authority. It is approved only for construction
of a current prefreeze Evidence Packet and one frozen Development execution.
