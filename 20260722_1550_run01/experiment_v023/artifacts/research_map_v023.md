<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p079-action-conditioned-contextualization","ev-p079-unseen-ui-boundary"]
-->
# Research Map v023

## Frozen computation ladder

One char-wb TF-IDF vocabulary (3–5 grams, min-df 2, maximum 30,000) is fit only on the mixed texts of training tasks. It transforms mixed text `x`, commands `c`, and terminal outputs `o` into the same coordinate system.

1. `mixed = [x]`.
2. `commands = [c]`.
3. `outputs = [o]`.
4. `role_concat = [c,o]`.
5. `triple_mixed = [x,x,x]`.
6. `command_duplicated = [x,c,c]`.
7. `output_duplicated = [x,o,o]`.
8. Candidate `role_factorized = [x,c,o]`.

All methods use identical rows, task splits, shared vocabulary, class-weighted liblinear logistic regression, C=1, seed 12023, validation threshold rule and task-ID cluster bootstrap.

## Exposed Development

Development is the immutable union of Terminal Wrench buckets 2 and 3 at commit `d8a29613235a0ef56a8b70b3142626a533da28c2`. All baseline and rewarded-serious-exploit rows remain evaluated; no successful row is removed as a reference. Task hashing creates 60% train, 20% validation and 20% Development-test partitions.

Development gates: Candidate AUC `>=0.90`; TPR@5%FPR `>=0.65`; AUC delta versus the strongest of seven comparators `>=0.005`; 2,000-resample task-bootstrap lower bound `>0`; frozen-threshold FPR `<=0.08`; frozen-threshold TPR `>=0.55`; Candidate AUC strictly exceeds every comparator; all split/raw/model/audit bindings valid.

## Prospective Confirmation

Bucket 0 is fixed before any of its data bytes are acquired. It has 81 task names by commit-tree metadata and no overlap with buckets 2/3.

Confirmation gates: Candidate AUC `>=0.89`; TPR@5%FPR `>=0.55`; frozen-threshold FPR `<=0.08`; frozen-threshold TPR `>=0.50`; Candidate AUC strictly exceeds all seven comparators; delta versus Development's frozen strongest comparator `>0` with task-bootstrap lower bound `>=0`; all task/source/model/audit integrity valid.

Automated booleans cannot authorize Confirmation or Review. The main Codex must read every raw row and all task/model/category/error slices at both stages.

## Main-Codex Candidate Promotion Audit — before Development

The Target Failure is a detector-level failure on the released Terminal Wrench outcome label: a rewarded serious exploit is ranked as benign, or a baseline trajectory is ranked as exploitative. The final result variables are task-disjoint row AUC, TPR at 5% FPR, and the validation-frozen confusion operating point; token validity, command execution, output formatting, or a proxy reconstruction score is not the target.

The only proposed decision-variable change is that a linear classifier receives separate coefficient blocks for the shared-vocabulary command surface and terminal-output surface while retaining the conventional mixed surface. It does not change source rows, labels, task split, vocabulary coordinates, learner, threshold rule, execution environment, or evaluation. This can affect the Target Failure because identical lexical evidence can carry a different sign or magnitude when issued by the agent versus observed from the environment; the test directly measures whether that distinction changes final reward-hack rankings, not whether text is better formed or executable.

The nearest complete compositions considered before implementation are Terminal Wrench's mixed whole-trajectory judge, Cheap Reward Hacking Detection's whole-trajectory encoder, Trajectory Guard's task/sequence recurrent towers, and AgentDiagnose's observation–reasoning–action representation with LLM-scored diagnostics. The closest fair executable composition in the fixed sparse protocol is the full seven-comparator ladder, especially same-width `[x,x,x]`, `[x,c,c]`, and `[x,o,o]`. AORF is promoted only to one bounded Development execution because those controls can falsify a generic capacity or single-role duplication explanation. No result may be attributed beyond this fixed reference-free representation comparison.
