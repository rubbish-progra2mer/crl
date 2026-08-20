# v031 Development Promotion Audit

Decision: `NO_GO_FOR_CONFIRMATION`.

## Mechanical evidence

- Development runner exit `0`; duration `2241.9498179s`.
- Python `3.11.15`; PyTorch `2.12.0+cu130`; CUDA `13.0`; RTX 5060 Ti, capability `12.0`.
- 4,256 rows, 250 tasks and 444,000 task-command pairs.
- Independent audit runner exit `0`, `AUDIT_OK`; duration `2045.0522175999977s`.
- Pair-score, feature, OOF-prediction, summary/gate and frozen full-model maximum errors are all `0.0`.

## Gate decision

The Candidate passes `0/8` Development gates:

- AUC `0.8014552525024745 < 0.88`;
- TPR at 5% FPR `0.39967506092607635 < 0.55`;
- strongest comparator `task_concat`, AUC `0.864683659857255`;
- delta `-0.06322840735478052 < 0.0075`;
- bootstrap lower `-0.07888434856946733 <= 0`;
- not strictly better than any complete comparator set;
- all three generator deltas are negative;
- all five source deltas are negative.

## Scientific judgment

The raw audit rejects the hypothesized mechanism, not merely a numeric threshold. The Candidate is worse in every target-generator×fold cell. Its few high-margin corrections cluster around obvious/repeated exploit patterns, while it creates more threshold regressions than corrections. The lowest one percent of mutation relevance is almost exactly class-balanced.

The frozen physical-newline parser also turns heredoc body lines into pseudo-commands and labels bare output-producing `echo`/`printf` plus arrow-containing code as mutations. This undermines the intended interpretation of a mutation-specific relevance pool. Fixing segmentation, redefining roles, selecting another encoder, reducing sources or weakening gates would be a new computation and is forbidden within v031.

## Authorized next state

Bucket 0 remains absent and untouched. No Confirmation, Review Packet, Reviewer, Decision or Delivery is authorized. Freeze v031 as `NO_GO_FOR_CONFIRMATION` and continue the same Run at v032 with a scientifically distinct computation. Do not retune MGTR segmentation, roles, cross-encoder, controls, gates or Claim.

Run remains `ACTIVE`. System remains `DEVELOPMENT_NOT_COMMISSIONED`.
