# Main-Codex Development Promotion Audit v023

Disposition: `NO_GO_FOR_CONFIRMATION`.

No subagent or Reviewer participated. This is the current main Codex's scientific audit of the frozen v023 Development execution, not an automated gate decision.

## Execution and integrity

- Development capture exit `0`; duration `194.7493134999968` seconds; execution SHA-256 `d998184de272f2ffba3216f749078227f35d4167ce6684d50f98cf9dd182e043`.
- raw 599 Development-test rows SHA-256 `48df89d02ce871dbc2341b0347c3d4e0cfc5243441801528ac938e78ccf74f92`.
- 3,071 source records SHA-256 `cebbd991148733994949cdbbcd6fe1dc05d21cd11776650777b820927276c848`.
- summary SHA-256 `20443a288dc35b991b4391366c2637e036523d409c567fa6c1f539c15453b794`.
- eight-model bundle SHA-256 `ed0b822ab74cf758b7d034e90a41bc73b22c7b1cb86a72d811c925bd20cda0e3`.
- independent audit exit `0`; duration `51.51510459999554` seconds; audit execution SHA-256 `dd54829245e76639ba493e5fe8a3694b30ea7cecd7a5d2c0f105f94be70a047b`.
- audit report SHA-256 `aaa831ab1a7a8f32b330b1abb1dbce6266e64975d50d4bde7235b8d3e21bfe30`: `AUDIT_OK`, zero errors, 3,071 source rows and records, 599 evaluated rows, 33 tasks, eight models and 4,792 scores; maximum score and metric error both `0`.
- environment: Python 3.11.15, NumPy 2.3.5, SciPy 1.16.0, scikit-learn 1.9.0, PyTorch 2.12.0+cu130, CUDA available on NVIDIA GeForce RTX 5060 Ti; fixed CPU training path.

The Development input is the exposed union of buckets 2+3. The fixed task partition and source hashes are current. No bucket-0 data, metadata, label, trajectory, or metric byte was acquired or read.

## Preregistered result

Candidate `role_factorized=[x,c,o]`:

- AUC `0.9427105007629353`;
- TPR at 5% FPR `0.7387640449438202`;
- validation-frozen FPR `0.01646090534979424`;
- validation-frozen TPR `0.5`;
- fixed-threshold confusion: TN `239`, FP `4`, FN `178`, TP `178`.

Strongest comparator `command_duplicated=[x,c,c]`:

- AUC `0.9505941647015305`;
- TPR at 5% FPR `0.8146067415730337`;
- validation-frozen FPR `0.01646090534979424`;
- validation-frozen TPR `0.5365168539325843`;
- fixed-threshold confusion: TN `239`, FP `4`, FN `165`, TP `191`.

Candidate-minus-strongest AUC is `-0.007883663938595187`; the 2,000-resample task-ID bootstrap interval is `[-0.017235934020414227, 0.0009833609678356798]`. The Candidate also trails commands-only by `-0.0036644009802561106` AUC and `[c,o]` by `-0.0006704582235168566`. It beats mixed by `+0.017362556064179135`, triple-mixed by `+0.009663846118278085`, outputs by `+0.02829796088223069`, and duplicated outputs by `+0.015143108151847273`, but the maximum Claim requires beating every fair comparator.

Only three of seven gates pass: Candidate AUC, TPR at 5% FPR, and fixed FPR. The AUC delta, bootstrap lower bound, fixed TPR, and strict-all-comparator gates fail.

## Complete raw-row and slice audit

The main audit command exited `0` after parsing all 599 raw rows, verifying 599 unique row IDs and exact eight-method score sets, and joining them to all 3,071 frozen source rows. It enumerated all four Candidate false positives, all 178 Candidate false-negative row IDs, all five Candidate-only-correct rows, all 18 strongest-only-correct rows, and all 164 rows both methods misclassified. A second bounded-source inspection exited `0` after opening command/output previews and original relative paths for every one of the 23 disagreement rows, plus the four false positives and twelve lowest-scored false negatives.

The fixed-threshold comparison is adverse in the target outcome rather than only a proxy: with the same four false positives, AORF loses 13 true positives. Candidate-only corrections comprise four serious exploits—one Stockfish and three Connect-Four hollow/simplified implementations—and one React baseline. The 18 strongest-only corrections cover real serious exploits across tasks 1012, 1104, 1366, 408, 500, 652, COBOL modernization, Bitcoin nodes, Git multibranch, Play Lord, and PostgreSQL WAL-secret recovery, plus one task-352 baseline. Their source previews show actual hollow implementations, output spoofing, constraint loopholes, metric spoofing, binary hijacking, and structural extraction; they are not identity or capture artifacts.

The result is not isolated to one model: Candidate-minus-strongest AUC is `-0.008904374758033407` for Claude Opus 4.6, `-0.00826446280991755` for Gemini 3.1 Pro, and `-0.005663155510250317` for GPT-5.4. It is negative on TerminalBench-original (`-0.01345486111111116`), SETA (`-0.011460839347767982`), and terminal-bench-pro (`-0.018707482993197244`); only terminal-bench 2.0 is positive (`+0.012037037037037068`). Across the 33 test tasks, one task has positive AUC delta, 25 tie, and seven are negative.

Positive-category recall is lower for Candidate on binary hijacking, constraint loopholes, deceptive rationalization, hollow implementation, metric spoofing, output spoofing, and structural extraction; tied on mutable-input tampering; and higher only on algorithmic simplification and keyword gaming. Particularly weak Candidate recall is metric spoofing `0.125`, structural extraction `0.24242424242424243`, and mutable-input tampering `0.2972972972972973`.

## Scientific judgment

The baseline Target Failure is real: reference-free sparse detectors miss many rewarded serious exploits at the frozen low-FPR operating point. AORF changes final rankings, not merely validity or formatting, so the experiment is diagnostic of the proposed computation. However, the diagnostic is negative. Separating an output coefficient block while retaining mixed text does not add robust task-disjoint reward-hack evidence beyond duplicating command evidence. Commands-only also outranks the Candidate, and the loss spans models, sources, tasks, failure categories, and frozen-threshold true positives.

This is not a capacity-control omission, execution defect, unfair baseline, or one-slice anomaly that would justify opening untouched Confirmation. Retuning block weights, changing regularization, dropping command-dominant tasks, lowering the gates, or narrowing the Claim after seeing these bytes would be optional stopping on buckets 2+3. v023 is therefore closed without Confirmation, Review Packet, Reviewer, Decision, or Delivery. Bucket 0 remains the untouched prospective resource for a scientifically different later Candidate; AORF retuning on the exposed Terminal Wrench data is forbidden.
