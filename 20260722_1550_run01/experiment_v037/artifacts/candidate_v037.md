# Candidate v037: Evidence-Conditioned Differential Surprisal

## Frozen computation

For each action pair:

1. tokenize the two exact action serializations with frozen Qwen3-0.6B;
2. use deterministic token-ID `SequenceMatcher` opcodes to mark differential
   action-token positions: replacement/insertion/deletion tokens are marked;
   on the empty side of a pure insertion or deletion, the immediately following
   shared boundary token is marked, or the preceding token when the edit is at
   the end;
3. build a full-evidence assistant continuation context from the frozen
   interaction history and implicated contracts;
4. build a matched evidence-withheld context with the same system instruction
   and serialization boundary;
5. teacher-force each action under both contexts;
6. compute mean log likelihood over these differential action-token positions;
7. subtract evidence-withheld from full-evidence mean log likelihood for each
   action;
8. prefer the action with the larger evidence gain.

No A/B token, pair order, generation, fitting, source calibration, retrieval,
tool execution or threshold is used.

## Controls

- `full_diff_ll`: full-evidence mean likelihood over differential positions;
- `full_action_gain`: full-evidence minus withheld-evidence likelihood over all
  action tokens;
- `null_diff_ll`: withheld-evidence likelihood over differential positions;
- `full_action_ll`: full-evidence mean likelihood over all action tokens.

Ties score `0.5`. All controls use the same four teacher-forced sequences per
row and the same model bytes.

## Development gates

All conditions are conjunctive:

1. ECDS accuracy at least `0.65`;
2. ECDS exceeds the strongest mandatory control by at least `0.025`;
3. source-cluster bootstrap 95% lower delta bound greater than `0`;
4. every source accuracy at least `0.55`;
5. source deltas all nonnegative and positive on at least two sources;
6. ECDS strictly exceeds `full_diff_ll` and `full_action_gain`;
7. ECDS strictly exceeds `null_diff_ll`;
8. independent replay reproduces every token mask, log probability, metric and
   bootstrap value within `1e-6`.

## Conditional Confirmation

Only all Development gates plus a positive main-Codex Promotion Audit permit
acquiring the fixed 130-row ToolSandbox. Frozen code and Development-frozen
strongest control then run unchanged.

Confirmation requires:

1. ECDS accuracy at least `0.60`;
2. positive delta over the Development-frozen strongest control;
3. strict superiority to `full_diff_ll` and `full_action_gain`;
4. positive paired-bootstrap median delta;
5. independent replay within `1e-6`.

## Claim ceiling

At most: evidence-subtracted likelihood on aligned differential action
positions improved this frozen small model's pairwise next-action ranking on
these splits against the listed matched controls. No downstream Agent-success,
cost, safety or formal-correctness Claim is allowed.
