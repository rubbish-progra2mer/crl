# Main-Codex Promotion Audit v040

Decision: `NO_GO_FOR_CONFIRMATION`.

The one frozen Development execution is valid and complete:

- child and capture runner exit code: `0`;
- duration: `1402.1020888999992` seconds;
- stderr: `0` bytes;
- 4,256 source rows, 228 eligible tasks and 4,072 OOF rows;
- Python `3.11.15` from the shared product environment;
- frozen Candidate and Evidence Packet hashes match the Plan.

The independent frozen replay also exits `0` and reports `AUDIT_OK`. It replays
all nine model bundles and 24,432 method scores. Maximum score error and maximum
metric error are both exactly `0.0`.

The Candidate nevertheless passes only three of eight conjunctive Development
gates. The decisive evidence is:

1. SFEC AUC is `0.8811531141534616`, while the strongest comparator is the
   mandatory original trace-mean CMCD at `0.8832616787559023`;
2. Candidate-minus-CMCD AUC is `-0.002108564602440688`, below the required
   `+0.005`;
3. the task-bootstrap 95% interval is
   `[-0.003549491444661765, -0.00048764947907491976]`, wholly below zero;
4. SFEC does not strictly beat every comparator;
5. generator-slice AUC deltas are `-0.0012563211125158347` for
   Claude Opus 4.6, `+0.0017222207513699628` for Gemini 3.1 Pro and
   `-0.002996778401454403` for GPT-5.4;
6. only one of three generator slices is positive, rather than at least two,
   and the all-nonnegative rule fails.

The absolute AUC, TPR@5%FPR and eligible-task-fraction gates pass, but they
cannot override the five failures above. A read-only row-level inspection
independently covers all 4,072 raw rows: SFEC is above CMCD on 1,884 rows,
below it on 2,032 and exactly equal on 156. Every held-out row has two support
families. Thus the equalized reduction is non-vacuous, but it does not improve
the preregistered discrimination objective.

The main Codex rejects lowering gates, removing CMCD, selecting only the Gemini
slice, changing support-family weights after exposure, or treating a mean
row-score shift as a substitute for task-level AUC. Those would be post-hoc
retuning of a failed final candidate.

Terminal Wrench bucket 0 remains absent and unread. No Confirmation, Review
Packet, Reviewer or Delivery is authorized. v040 is frozen as a negative
result. Per the user's explicit cutoff, run01 must now pause with one resume
point rather than advance automatically to v041.

System status remains `DEVELOPMENT_NOT_COMMISSIONED`.
