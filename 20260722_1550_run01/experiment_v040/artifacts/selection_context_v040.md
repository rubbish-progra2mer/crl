# v040 Selection Context

## Final-version boundary

v040 is the user's final allowed version. If it does not produce Delivery, run01
must be paused with one durable resume point. No subagent may be created unless
a complete formal Review Packet is later frozen.

v039 ECDS is frozen `NO_GO_FOR_CONFIRMATION` at `4/8` gates. v040 does not
retune its model, likelihood, alignment, evidence withholding, controls, gates
or source selection.

## Reused exposed carrier

v026 CMCD on Terminal Wrench buckets 1--3 passed `7/8` gates. It failed because
its delta versus `single_support` was negative for Gemini
(`-0.004255910619258119`) even though Claude and GPT deltas were positive.
Bucket 0 remains absent, unacquired and unread.

All v026 Development outputs are exposed. Selecting a new computation after
that failure is optional stopping. No Development result can establish
generalization without untouched bucket 0.

## Three Card queries

Exactly three production Card searches ran and exited `0`:

1. failure:
   `support generator imbalance consensus aggregation negative group transfer`;
2. operator:
   `group balanced support aggregation source family equal weighting`;
3. paper:
   `group distribution robust domain generalization equal weighting ensemble`.

The Card store did not contain a direct prior for equal-support-family
aggregation. Relevant hits instead warned that aggregation needs matched
controls and that group mechanisms require an actual repeated group structure.

## Open prior and direct reading

Four open queries covered group-DRO theory, worst-group generalization,
equal/group weighting and multi-source shift. The main Codex downloaded Sagawa
et al., ICLR 2020, SHA-256
`7342848c5921ff5cedf2c27a0f84e38c221c085a9ce28befd9208f2bb0fe36d6`.
The first local extraction exited `1` only because GBK could not print a math
symbol; UTF-8 extraction then exited `0`, and physical pages 1--5 were read.

Group DRO optimizes worst empirical group risk and requires regularization for
worst-group generalization. v040 neither trains a group-DRO objective nor tunes
regularization; it only prevents a support generator with more successful
traces from receiving more inference mass.

## Prefreeze mechanism correction

An initial design proposed equal generator weight during both training and
inference. Main-Codex code review showed that every v026 training bundle leaves
only one allowed support generator per training query, so training reweighting
would be identically unchanged. Before freeze, that vacuous component was
removed. The selected computation changes only held-out aggregation, where two
support generator families can actually occur.

No v040 Development feature, aggregation output or metric was screened.
