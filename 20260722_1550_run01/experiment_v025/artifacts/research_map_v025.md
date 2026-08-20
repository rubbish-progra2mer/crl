<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"]
-->
# Research Map v024

## Fixed anchor

Each original agent command-batch is one ordered action unit. A batch is an inspection anchor exactly when both conditions hold:

1. it contains one of the inspection executables `cat`, `sed`, `grep`, `rg`, `find`, `ls`, `head`, `tail`, `less`, `more`, `strings`, `type`, `which`, or `stat` at a whitespace/shell-separator boundary;
2. it contains a non-alphanumeric-delimited checker token from `check/checker/checking`, `test/tests/testing/pytest/unittest`, `verify/verifier/verification`, `grader/grading`, `score/scoring`, `eval/evaluator/evaluation`, or `reward`.

The first matching batch is the anchor. `before` contains earlier batches; `from_anchor` contains the anchor and every later batch. With no match, `before=all_commands` and `from_anchor=empty`. The predicate is frozen before bucket-1 acquisition and never observes labels.

## Shared sparse surface and comparator ladder

Within each training fold, one char-wb TF-IDF vocabulary (3–5 grams, min-df 2, maximum 30,000) is fit only on mixed command/output texts of training tasks. It transforms mixed text `x`, all commands `c`, all outputs `o`, fixed first/second chronological command halves `h1/h2`, anchor-matching/nonmatching command bags `am/an`, and anchor-relative commands `b/a` into the same coordinates.

1. `mixed=[x]`.
2. `commands=[c]`.
3. `role_concat=[c,o]`.
4. capacity-matched strongest surface `command_duplicated=[x,c,c]`.
5. generic-time control `fixed_halves=[x,h1,h2]`.
6. position-free semantic control `anchor_bag=[x,am,an]`.
7. Candidate `viaf=[x,b,a]`.

All use identical rows, task folds, vocabulary recipe, class-weighted liblinear logistic regression, C=1 and seed 12024. No metadata field is a feature.

## Untouched Development and OOF analysis

Development is Terminal Wrench bucket 1 at commit `d8a29613235a0ef56a8b70b3142626a533da28c2`, acquired only after implementation/config/Plan freezing. Fold is `SHA256(task_id)[1] mod 5`; every task is held out exactly once. For each fold, the vocabulary and seven classifiers fit only on the other four folds. All bucket-1 rows receive one out-of-fold score. Full-bucket-1 vocabulary/models are then fit once solely for possible bucket-0 Confirmation.

Primary analysis is row AUC and TPR at 5% FPR over all OOF rows, with 2,000 task-ID cluster bootstrap resamples. Development gates are: VIAF AUC `>=0.94`; TPR@5%FPR `>=0.75`; AUC delta versus the strongest of six comparators `>=0.005`; bootstrap lower bound `>0`; VIAF AUC strictly exceeds every comparator; VIAF-minus-command-duplicated AUC is positive within anchor-present rows and at least `-0.005` within anchor-absent rows; all acquisition/fold/raw/model/audit bindings valid.

## Prospective Confirmation

Only a positive written main-Codex Development Promotion Audit may acquire bucket 0. The frozen full-Development models score every bucket-0 row once without fitting, fold changes or comparator reselection. Confirmation gates are: VIAF AUC `>=0.93`; TPR@5%FPR `>=0.70`; VIAF strictly exceeds all six comparators; delta versus Development's frozen strongest comparator `>0` with task-bootstrap lower bound `>=0`; anchor-present delta positive and anchor-absent delta at least `-0.01`; zero Development-task overlap and complete source/model/audit integrity.

Booleans cannot authorize Confirmation or Review. The main Codex must inspect all raw rows, source/model/anchor/task slices, corrections and regressions at both stages.

## Main-Codex Candidate Promotion Audit — before Development

The Target Failure is final-label misranking of a rewarded serious exploit as benign or a successful baseline as exploitative. VIAF changes only the coefficient context assigned to command fragments before versus after a label-free verifier-inspection event. It does not change execution validity, labels, data, learner or evaluation.

The mechanism could affect the Target Failure because inspecting a verifier changes what surface constraints are known; subsequent writes, test manipulation or hollow implementations can therefore carry a different statistical role than identical commands issued before that information event. The mandatory command duplication, fixed-half and anchor-bag controls independently test extra L2 capacity, generic time position and checker-word presence.

The nearest complete pipelines—Terminal Wrench and Cheap Reward Hacking Detection whole-trajectory monitors, Trajectory Guard recurrent task/trajectory towers, TrajAD fine-grained generative process supervision, and AgentRx dynamic invariant checking—cover generic sequence/process monitoring but not this fixed sparse event-relative computation. Strained Coherence supplies a reasoning-visible late conflict signal, not an action-only verifier anchor. The candidate is promoted only to one bucket-1 Development because a confirmed result would support a narrow interpretable representation finding; no universal novelty or causal-monitor claim is permitted.
