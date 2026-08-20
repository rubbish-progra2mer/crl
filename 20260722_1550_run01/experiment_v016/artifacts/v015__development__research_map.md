<!-- crl-v3-evidence-ids
["ev-p039-failure-core","ev-p039-aggregate-score-masking"]
-->
# Research Map v014

## Evidence-backed motivation

- `ev-p039-failure-core` establishes the target benchmark's distinct Tool-Skip, Result-Ignore, Output-Fabrication, and correct categories.
- `ev-p039-aggregate-score-masking` establishes why preserving diagnostic label identity matters instead of reporting final accuracy alone.

These formal Evidence records motivate the audit. They do not establish the newly observed order defect or RGP's empirical effect; those are bound to fixed target code, released trace bytes, raw judge outputs, and prospective experiment captures.

## Nearest source relationship

The exact target is ToolFailBench's released deterministic classifier and released trace/judge dataset. The paper already discloses broad exact-rule brittleness and uses two LLM judges to compensate. v014 therefore cannot claim discovery of answer-equivalence errors. Its narrower contribution is a byte-addressed test of one deterministic short-circuit: a satisfied official required-evidence contract can be overridden by a coarse fabrication proxy that never locates unsupported evidence.

## Failure

For a tool-required answer that:

- executed the expected tool;
- exactly contains all official required values;
- mentions at least two supported field names;
- quotes fewer than 30% of all leaves in a large tool return;

the released classifier returns `output_fabrication`. The return occurs without checking the required-answer contract and without identifying an unsupported answer value. This confounds concise selection of relevant evidence with invention of structured evidence.

## Intervention

Required-Grounding Precedence changes only the tool-required decision order:

1. preserve official expected-tool detection and `tool_skip`;
2. evaluate the unchanged official exact `answer_must_contain`/`match_mode` contract;
3. if satisfied, return `correct`;
4. otherwise run the unchanged official fabrication heuristic;
5. otherwise return `result_ignore`.

CTRL classification and every underlying predicate remain byte-for-byte equivalent in behavior to the released code.

## Changed-computation claim

v014 changes the evaluation computation from fabrication-first short-circuiting to required-grounding-first short-circuiting. It is not:

- a prompt modification;
- an LLM judge or learned evaluator;
- fuzzy matching, semantic similarity, or alias expansion;
- numeric/date normalization;
- threshold tuning;
- a relabeling based on the official majority ensemble;
- another BoR, RCED, TPPA, or retrieval experiment;
- fixture sanity or file-existence evidence.

## Main scientific risks

- All Development traces and judge labels were inspected during selection; only the generator-model partition provides untouched Confirmation.
- The two judges share the benchmark's base rubric and are not human gold. Unanimity reduces but does not eliminate correlated judge error.
- RGP may hide answers that contain required values and additional unsupported structured claims. Corrections/regressions and raw transition examples must therefore be reported, and a high regression rate kills the candidate.
- The Confirmation split changes generator models but uses the same two judge models and task set. It tests output-family transfer, not judge-family or task-family generalization.
- The selected computation cannot fix `result_ignore -> correct` surface variants and must not claim to.
- The target is a recent preprint and may be revised after the fixed bytes.
- A strong agreement improvement is a measurement correction, not a new tool-using agent algorithm.

## Candidate Promotion Audit Before Development

The source defect is directly observable and the changed computation is one auditable branch reordering. The nearest fair baseline is the exact released classifier on identical rows. The primary reference excludes the circular majority ensemble and uses only two-judge unanimity. The mechanism prediction is directional: RGP should mainly convert released `output_fabrication` labels to `correct`, and the conversion should be supported across models and domains rather than by one trace family.

The intervention has no tunable threshold. Development gates require exact baseline reproduction, structural invariance outside eligible tool-required rows, paired improvements, model/domain spread, and a correction-to-regression margin. Development exposure is explicit. On this basis, the main Codex authorizes a minimal implementation and one frozen Development experiment, but not Confirmation.

## Development contract

Development uses exactly the 40 files and hashes in `sources_v014/toolfailbench_development_manifest.json`. The experiment must:

- verify every input hash and size before parsing;
- join each trace to both judge rows by `(model_id, task_id)`;
- reproduce the released `classification` field with the fixed official code;
- exclude judge-disagreement rows from primary metrics while reporting their count;
- compute official and RGP predictions on every row;
- report paired accuracy and macro-F1 on unanimous rows;
- report corrections, regressions, transition matrices, per-model and per-domain deltas;
- bootstrap generator-model clusters with a frozen seed and resample count;
- freeze row-level predictions and a deterministic sample of correction/regression cases;
- independently recompute all metrics from row-level output.

## Development promotion gates

All gates are conjunctive:

1. **Input integrity:** all 40 manifest entries have exact path, byte count, and SHA-256; exactly 10 trace files and two judge files per generator model are used.
2. **Join integrity:** each trace file has 1,000 unique task IDs; both judge files cover the same 1,000 IDs; all joined model/task/domain values agree.
3. **Baseline identity:** the local fixed official classifier reproduces the released `classification` for every row carrying one of the classifier's six supported labels; any released external pipeline label such as `other_error` is counted, reported, and passed through unchanged rather than reinterpreted.
4. **Structural invariance:** RGP equals the released official label for every CTRL row, every released external-error row, and every row where the expected tool was not executed.
5. **Primary effect:** paired accuracy delta on unanimous-judge rows is at least `+0.01`.
6. **Cluster uncertainty:** a `20,000`-resample generator-model bootstrap with seed `20260723` gives a 95% percentile interval for paired accuracy delta with lower bound `> 0`.
7. **Correction margin:** corrections are at least twice regressions.
8. **Model spread:** at least `8/10` generator models have strictly positive accuracy delta.
9. **Domain spread:** at least `4/5` domains have strictly positive accuracy delta.
10. **Mechanism support:** at least 100 rows change from official `output_fabrication` to RGP `correct`, match unanimous `correct`, and span at least four domains.

No gate may be lowered, no predicate may be added, and no threshold may be tuned after execution. Development failure forbids Confirmation.

## Untouched Confirmation contract

After a positive main-Codex Promotion Audit, acquire only the 12 trace files and their 24 judge files named by the frozen partition from `SoHarshh/toolfailbench-traces@77ef18dadfc1ad96ce29c863f0913d990659432a`. Do not acquire or use ensemble files.

Apply the frozen implementation and metric procedure without any code, normalization, threshold, label, or sample-selection change.

Confirmation gates:

1. all acquired paths match the frozen Confirmation list and were absent from the Development manifest;
2. input, join, baseline-identity, and structural-invariance checks pass;
3. paired accuracy delta on unanimous rows is at least `+0.005`;
4. the 20,000-resample model-cluster bootstrap 95% lower bound is `> 0`;
5. corrections exceed regressions;
6. at least `9/12` generator models and at least `4/5` domains have positive accuracy delta;
7. at least 100 supported `official output_fabrication -> RGP correct -> unanimous correct` transitions occur across at least four domains.

The Development gates remain reported; Confirmation gates are not substituted for them.

## Review and decision boundary

Only after Confirmation passes may the main Codex freeze `review_v014/packet.md` with every listed implementation, Plan, source manifest, environment capture, raw Development and Confirmation row, raw stdout/stderr capture, summary, independent audit, and hash. Only then may three fresh direct leaf Reviewers be started. Reviewer labels, votes, scores, or file existence cannot replace the main Codex's final evidence adjudication.
