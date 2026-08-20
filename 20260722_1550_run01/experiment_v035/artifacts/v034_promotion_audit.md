# v034 Main-Codex Promotion Audit

Decision: `NO_GO_FOR_CONFIRMATION`.

This judgment was made after personally rereading the frozen Evidence Packet,
Plan, all Development outputs, both raw captures, the independent audit report,
all 315 pair rows, all 630 pointwise rows, source slices and representative
source histories/actions.

## Evidence integrity

- Development execution exit: `0`;
  SHA-256
  `7be16670fae2340c3d6daca2d65916d4ca360a9c8e0bd001e8db0ca5114943be`.
- Independent audit exit: `0`;
  SHA-256
  `c6cf853e6527329f60a8bc1e52ea01f858a638b26ba5793646dbf2b85f2a14b9`.
- Audit report:
  `AUDIT_OK`,
  SHA-256
  `bbf1c7ff5c57c8117d552456dde28f23b94a82c29ca9b7498b0eb107c48f649a`.
- Replayed rows/actions/prompts: `315/630/3780`.
- Prompt-hash mismatches: `0`.
- Pointwise and derived maximum numeric error: `0.0`.
- Raw Analysis:
  `d399676df25ff1161581380445d7b483a9d4dca213ae756f731722aa68fac6f2`.

The bytes are trustworthy enough to make the negative decision.

## Conjunctive gate audit

| Gate | Required | Observed | Result |
|---|---:|---:|---|
| Candidate accuracy | `>=0.60` | `0.682540` | PASS |
| Candidate-minus-strongest | `>=0.03` | `-0.017460` | FAIL |
| Bootstrap lower | `>0` | `-0.086094` | FAIL |
| Beat every comparator | strict | arguments `0.700000` | FAIL |
| Each source accuracy | `>=0.50` | min `0.590090` | PASS |
| All source deltas | `>=0` | GTA/BFCL negative | FAIL |
| Positive source deltas | `>=2` | `1` | FAIL |
| Action-swap integrity | exact | max error `0.0` | PASS |

Only `3/8` gates pass. Scripts report the same boundary, but this decision is
the main Codex's evidence judgment rather than an automatic gate action.

## Scientific judgment

The Candidate improves on the holistic prompt and helps ToolTalk, but its
proposed conjunctive bottleneck does not survive the complete control and
source-holdout test:

- the single `arguments` obligation is stronger overall;
- CCCB loses `0.059322` on GTA and `0.063063` on BFCL relative to that
  comparator;
- the bootstrap interval spans meaningful harm and benefit;
- raw regressions include missed login, currency-conversion, information
  already present and prerequisite-query cases that the extra obligations were
  intended to catch.

Therefore neither weakest-obligation aggregation nor the complete fixed CCCB
composition is identified. A ToolTalk-only result would be an exposed,
post-hoc subgroup Claim and is not admissible.

## Boundary

`prmbench_ToolSandbox.json` remains absent and unread. No Confirmation
acquisition or inference is authorized. No Reviewer or Review Packet is
authorized.

v034 is frozen. It may not retry or retune the five prompts, evidence
projections, empirical calibration, hard minimum, model size, controls, gates,
source subset or Claim. Any v035 candidate must use a scientifically different
computation rather than soften CCCB after seeing this result.

Run remains `ACTIVE`. System remains `DEVELOPMENT_NOT_COMMISSIONED`.
