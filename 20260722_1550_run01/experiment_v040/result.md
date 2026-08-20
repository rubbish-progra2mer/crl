# v040 Result

Disposition: `NO_GO_FOR_CONFIRMATION`.

v040 executed the frozen Support-Family Equalized Consensus (SFEC) Development
plan exactly once and independently replayed every frozen output. Both capture
runners and both scientific processes exited `0`; Development took
`1402.1020888999992` seconds and audit took `416.8721399999995` seconds.
Audit status is `AUDIT_OK`, with nine bundles and 24,432 scores replayed and
maximum score and metric error exactly `0.0`.

SFEC passes only `3/8` conjunctive gates:

- SFEC AUC: `0.8811531141534616`;
- original trace-mean CMCD AUC: `0.8832616787559023`;
- delta: `-0.002108564602440688`;
- task-bootstrap 95% interval:
  `[-0.003549491444661765, -0.00048764947907491976]`;
- generator deltas: Claude `-0.0012563211125158347`, Gemini
  `+0.0017222207513699628`, GPT `-0.002996778401454403`.

The method therefore fails the required positive delta, bootstrap,
every-comparator, all-generator-nonnegative and two-positive-generator gates.
Its absolute AUC, TPR@5%FPR and eligible-fraction passes do not override those
failures.

Frozen evidence identities:

- Candidate:
  `aa82bbe9988b7e1824a49a7e4d080c46a3d9e38b833e6d2c396b006f717cc51c`;
- Evidence Packet:
  `287c5628537281805cdb093f785c0002cd13c2880a85ad66bf3b4ed1c8962aa9`;
- Plan:
  `4f7d6b035b401f359ebb8a09e863d230ddadc35d0f4b69c3b1fda1715136d8de`;
- Artifact Manifest:
  `7fed84bdf490775299dc0e26c9e4c8e8080c17e2da58455d58de7c9365b0ea12`;
- Development execution:
  `92b79cfeef21fbc2da0c6c97cfedc42f975d658ea42515b18caec83be308c504`;
- raw predictions:
  `a6b2e48581f1f1e437f11f937009f1845b123f9dd02eabdb70475a7755d6379d`;
- summary:
  `ce6ebe99857ef6c757f14515aec027a45aaa4aec215af778ff1b516b4d5aff31`;
- audit execution:
  `308f06c65cc3e8944d8eda03ea2bc133de333bba02c5dab815b6c097978de952`;
- audit report:
  `e4392c92e3184bd5e5d688dad46fce43580f116223b0d5846dd9d447e98e650c`;
- Main-Codex Promotion Audit:
  `51cc36ba6ef135c563f3c26802fc4dc31849f5c7ca99e9e92eb5c1c739df8ddb`;
- Attempts Manifest:
  `a602c75b19534679d80c5d997f355760e160bbd149879931eb10999f58ac244b`.

Terminal Wrench bucket 0 remains absent and unread. No Confirmation, Review
Packet, Reviewer or Delivery was created. The failed Candidate is frozen
without post-hoc retuning.

Because v040 is the user's explicit cutoff, run01 is paused after this result
with one resume point: the user must explicitly authorize continuation beyond
v040. System status remains `DEVELOPMENT_NOT_COMMISSIONED`.
