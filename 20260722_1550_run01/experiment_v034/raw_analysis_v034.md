# v034 Main-Codex Raw Analysis

Status: `DEVELOPMENT_NEGATIVE`.

This analysis was written only after Development exit `0` and independent
`AUDIT_OK`. It is based on direct reading of the frozen summary, all 315 raw
pair rows, all 630 pointwise rows, the source bytes and both captures.

## Integrity first

- Development execution:
  `7be16670fae2340c3d6daca2d65916d4ca360a9c8e0bd001e8db0ca5114943be`,
  exit `0`, duration `1391.8097116999998s`.
- Independent audit execution:
  `c6cf853e6527329f60a8bc1e52ea01f858a638b26ba5793646dbf2b85f2a14b9`,
  exit `0`, duration `1160.6648085000052s`.
- Audit report:
  `bbf1c7ff5c57c8117d552456dde28f23b94a82c29ca9b7498b0eb107c48f649a`,
  status `AUDIT_OK`.
- The auditor checked 28,163 derived numeric values and 965 exact values.
  Pointwise and derived maximum errors are both `0.0`; prompt-hash mismatches
  are `0`.
- Rows/actions/prompts are exactly `315/630/3780`; environment is Python
  3.11.15, PyTorch 2.12.0+cu130, CUDA 13.0 and RTX 5060 Ti.

The four scikit-learn messages in each stderr capture are deprecation warnings
for the frozen explicit L2 parameter. They did not change exit, outputs or
independent replay.

## Overall result

| Method | Accuracy |
|---|---:|
| `arguments` | 0.700000 |
| CCCB | 0.682540 |
| `calibrated_product` | 0.647619 |
| `raw_min` | 0.642857 |
| `linear_ensemble` | 0.638095 |
| `calibrated_mean` | 0.631746 |
| `pair_majority` | 0.623810 |
| `progress` | 0.617460 |
| `mode` | 0.600000 |
| `grounding` | 0.592063 |
| `selected_single` | 0.585714 |
| `tool` | 0.558730 |
| `holistic` | 0.544444 |

The strongest mandatory comparator is the individual `arguments` obligation.
CCCB-minus-arguments is `-0.0174603`, not the required `+0.03`. The
task-cluster bootstrap is
`[-0.0860941, 0.0458934]`, with median `-0.0183486`; its lower bound is not
positive.

Only `3/8` gates pass:

- pass: Candidate accuracy `>=0.60`;
- pass: every source Candidate accuracy `>=0.50`;
- pass: exact pointwise action-swap invariance;
- fail: required overall delta;
- fail: positive bootstrap lower bound;
- fail: strict superiority to every comparator;
- fail: all source deltas nonnegative;
- fail: at least two positive source deltas.

## Source boundary

| Source | CCCB | Arguments | Delta |
|---|---:|---:|---:|
| GTA | 0.796610 | 0.855932 | -0.059322 |
| BFCL | 0.590090 | 0.653153 | -0.063063 |
| ToolTalk | 0.645349 | 0.546512 | +0.098837 |

The mechanism helps ToolTalk but regresses on both GTA and BFCL. ToolTalk was
one of the three exposed Development sources; a ToolTalk-only Claim selected
after observing this table is prohibited post-hoc narrowing and cannot justify
Confirmation.

## Pairwise crossover

Against `arguments`, CCCB is more correct on 46 rows and less correct on 49
rows. Accounting for half-credit ties, the net is `-5.5` correct-pair
equivalents:

- GTA: 2 corrections, 11 regressions/tie-regressions, net `-7.0`;
- BFCL: 20 corrections, 26 regressions, net `-7.0`;
- ToolTalk: 24 corrections, 14 regressions, net `+8.5`.

CCCB has 10 exact pair ties versus 7 for `arguments`. The result is not an
artifact of one tie: removing half-credit arithmetic cannot reverse both
negative source slices or the failed overall delta.

## Bottleneck behavior

The chosen action's minimum percentile is attached to:

- arguments: 95 rows;
- mode: 83;
- progress: 63;
- tool: 52;
- grounding: 33.

The rejected action's minimum is:

- arguments: 126 rows;
- mode: 74;
- tool: 51;
- progress: 49;
- grounding: 23.

Thus the hard minimum is not merely reproducing the strong argument checker.
It frequently lets a noisier mode/progress/tool/grounding score dominate. That
is the proposed computation, and on GTA/BFCL the extra bottlenecks destroy more
correct distinctions than they add.

## Direct case reading

I reread source histories and both actions for representative corrections and
regressions.

Corrections show the intended benefit:

- `bfcl:0000`: both calls use the same tweet tool and schema-valid parameters,
  but the rejected content introduces newlines not present in the tool result;
  CCCB recovers the exact grounding/format distinction that `arguments` misses.
- `bfcl:0016`: after trading activity, the user asks for the most recent
  support ticket; CCCB prefers `get_ticket` over the rejected
  `get_user_tickets` call.
- `gta:0071`: OCR already provides all menu prices; CCCB prefers a Calculator
  call for `(10+20+8+36)*2` over asking the user to provide information again.
- `tooltalk:0014`: the user asks to delete all past reminders; CCCB correctly
  prefers listing reminders before prematurely deleting one arbitrary ID.

Regressions directly falsify the weakest-obligation story:

- `bfcl:0011`: the history supplies the recipient ID but the agent must log in
  before messaging. CCCB incorrectly prefers the premature `send_message`
  action over the chosen `message_login`; its chosen bottleneck is grounding
  and rejected bottleneck is progress.
- `bfcl:0030`: the user specifies a 20,000 RMB budget; CCCB incorrectly prefers
  setting `20000.0` directly over the required RMB-to-USD conversion.
- `gta:0018`: after describing the product image, the correct next step is to
  inspect the menu image; CCCB instead favors asking the user for an image that
  is already available.
- `tooltalk:0030`: modifying a birthday event and notifying invitees requires
  first querying the calendar; CCCB incorrectly prefers immediately sending an
  email.

These are not marginal lexical disagreements. They include exactly the
precondition, ordering, already-provided-evidence and progress failures CCCB
was designed to protect. The fixed 0.6B obligation scores are not reliable
enough for a hard conjunction.

## Judgment

The Candidate is above chance and materially better than the holistic 0.6B
prompt, but the predeclared attribution is not identified. A single argument
obligation is stronger overall, the Candidate regresses on two sources, and the
confidence interval includes substantial harm.

No prompt, obligation, calibration, aggregation, model-size or source-specific
retuning is allowed in v034. ToolSandbox remains absent and unread. v034 must
close as `NO_GO_FOR_CONFIRMATION`.
