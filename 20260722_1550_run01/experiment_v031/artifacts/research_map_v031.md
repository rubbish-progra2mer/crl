# Research Map v031

## Evidence and nearest boundary

- Terminal Wrench establishes a diverse real command-line reward-hack corpus and a stripped action/terminal condition where LLM-judge AUC falls to `0.9168`.
- Cheap Reward Hacking Detection trains global trajectory encoders and reports that action-only detection is materially weaker than reasoning-aware detection.
- Trajectory Guard directly combines task-trajectory alignment with sequence reconstruction on other anomaly datasets.
- P040 grounds the broader distinction between an agent's claimed success and environment terminal truth.

MGTR does not claim any of those ideas. Its testable delta is deterministic operation-role pooling of a frozen task-command relevance score.

## Frozen representation

1. Extract the task description between the fixed `Task Description:` and `Current terminal state:` delimiters.
2. Split the emitted command surface at `&&`, `||`, semicolon and physical newline boundaries.
3. Assign each segment one label-free role using the frozen v012 parser:
   - `mutation`: write, delete, permission, package, service or network;
   - `verify`;
   - `read`;
   - `other`.
4. Score every `(task description, command segment)` pair with the frozen local `cross-encoder/ms-marco-MiniLM-L-6-v2` bytes.
5. For each role, emit five fixed statistics: segment fraction, minimum, mean, maximum and population standard deviation. Empty roles emit five zeros.

The Candidate appends these 20 dense features to the same 20,000-dimensional character TF-IDF action representation used by the direct baseline, standardizes dense columns on training rows only and fits the same balanced logistic regression.

## Mandatory controls

- `direct_action`: action/terminal TF-IDF only;
- `task_concat`: TF-IDF over fixed task description plus action/terminal text;
- `structural_counts`: direct TF-IDF plus the four role fractions, without cross-encoder scores;
- `global_relevance`: direct TF-IDF plus count, minimum, mean, maximum and standard deviation over all command relevance scores;
- `chronological_relevance`: direct TF-IDF plus the same five statistics in four equal chronological command bins, matching the Candidate's dense-feature count without operation roles.

All methods use identical rows, OOF bundles, generator exclusions, classifier, class weights, C and seed.

## Development gates

All gates are conjunctive:

1. exact SHA binding for three datasets, three acquisition manifests, base parser and six model files;
2. 4,256 unique rows from 250 tasks; every row receives exactly one OOF score;
3. no task or target-generator row enters its scoring bundle's training set;
4. Candidate AUC at least `0.88`;
5. Candidate TPR at empirical FPR `<=0.05` at least `0.55`;
6. Candidate AUC exceeds the strongest mandatory control by at least `0.0075`;
7. a 2,000-resample task-cluster bootstrap 95% lower bound for that AUC delta is above zero;
8. Candidate strictly beats every mandatory control in AUC;
9. Candidate-minus-strongest AUC is nonnegative for all three generator slices and positive for at least two;
10. Candidate-minus-strongest AUC is nonnegative for at least four of the five source-dataset slices;
11. an independent source-to-score auditor reproduces all pair scores within `1e-6`, dense features within `1e-12`, OOF scores within `1e-10`, and metrics/gates within `1e-12`.

The Main Codex must inspect raw rows, low-relevance mutations, corrections, regressions, generator/source slices and role ablations. Scripts cannot authorize Confirmation.

## Conditional Confirmation

Only after a positive written Development Promotion Audit may the frozen acquisition script fetch bucket 0. Its task IDs must be disjoint from Development.

The frozen full target-generator bundles then score Confirmation once. Required gates are:

- exact input/model/task-disjoint integrity;
- Candidate AUC at least `0.86`;
- Candidate TPR at 5% FPR at least `0.50`;
- positive AUC delta over the frozen Development strongest comparator;
- task-bootstrap lower bound at least zero;
- strict AUC superiority over every control;
- all generator slices nonnegative and at least two positive;
- at least four of five source slices nonnegative;
- exact independent audit.

## Maximum Claim

If and only if Development, untouched Confirmation, three independent Reviewers and the Main-Codex Decision all pass:

> On the fixed Terminal Wrench stripped command/terminal protocol, pooling frozen task-command relevance by deterministic operation role improves serious reward-hack detection under held-out-task and held-out-generator evaluation relative to direct text, task concatenation, structural, global-relevance and equal-capacity chronological controls.

No first-ever, causal, exploit-localization, online-prevention, hidden-intent, human-gold or cross-benchmark claim is allowed.
