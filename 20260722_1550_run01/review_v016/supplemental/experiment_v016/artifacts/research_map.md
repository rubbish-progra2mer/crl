<!-- crl-v3-evidence-ids
["ev-p039-failure-core","ev-p039-aggregate-score-masking"]
-->
# Research Map v016

## Evidence-backed motivation

- `ev-p039-failure-core` establishes ToolFailBench's distinct Tool-Skip, Result-Ignore, Output-Fabrication, and correct categories.
- `ev-p039-aggregate-score-masking` establishes why diagnostic label identity matters beyond final aggregate accuracy.

The formal Evidence records motivate the audit; the order defect and its measured effect are bound to fixed code, released traces, raw judge outputs, and prospective captures.

## Failure and intervention

The released tool-required classifier evaluates a coarse fabrication proxy before its own exact required-answer contract. A concise answer can include every required value while quoting fewer than 30% of a large return; the classifier can then emit `output_fabrication` without identifying unsupported answer evidence.

Required-Grounding Precedence preserves expected-tool detection, evaluates the unchanged required-answer contract first, returns `correct` when it is satisfied, and otherwise applies the unchanged fabrication predicate before `result_ignore`. CTRL logic and external pipeline labels remain unchanged.

## v014 Development evidence inherited without rerun

The fixed 10-model Development partition produced:

- 10,000 joined rows and 9,345 unanimous-reference rows;
- official accuracy `0.9295880149812734`;
- RGP accuracy `0.9462814339218834`;
- paired delta `+0.016693418940609953`;
- model-cluster bootstrap 95% `[+0.010464272171620851, +0.02313872522763792]`;
- 157 corrections and one regression;
- positive delta on 9/10 models and 5/5 domains;
- 157 supported mechanism transitions across all five domains;
- all ten Development gates passed;
- independent raw-row audit exit `0`, `audit_ok=true`, and maximum recorded metric error `0`.

The main Codex Promotion Audit authorized acquisition of the untouched Confirmation bytes. The single Development regression remains a real limitation: required values were present, but the answer also included unsupported structured claims.

## v016 changed-computation boundary

There is no new scientific computation in v016. v015 already made manifest identity, artifact prefix, expected file/row/model/domain counts, and phase gates explicit; v016 corrects only one missing `e` in the frozen manifest SHA. The RGP classifier, official predicates, row construction, metrics, and bootstrap must be byte-identical to v015 and AST-identical to v014.

The correction is not retuning, normalization, prompt modification, model selection, judge selection, data filtering, a fallback dataset, or a new research candidate. v015 produced no Confirmation row or metric before the correction was chosen.

## Fixed Confirmation contract

Inputs:

- dataset `SoHarshh/toolfailbench-traces`;
- revision `77ef18dadfc1ad96ce29c863f0913d990659432a`;
- manifest SHA-256 `f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944`;
- 12 trace files, 24 judge files, zero ensemble files, 36 total files;
- 12,000 rows before unanimity filtering;
- no path overlap with the 40-file Development manifest.

Procedure:

- verify every path, byte count, and SHA-256 before parsing;
- join each trace to both judges by model and task ID;
- reproduce every classifier-supported released label with the fixed official code;
- pass through disclosed external pipeline labels unchanged;
- compute official and RGP predictions on all rows;
- restrict primary agreement metrics to two-judge-unanimous rows;
- report all metrics, transitions, per-model/domain deltas, and bounded cases;
- use 20,000 generator-model-cluster resamples with seed `20260723`;
- independently recompute metrics and gates from frozen raw rows.

## Confirmation gates

All gates are conjunctive:

1. exact input cardinalities and hashes;
2. 12,000 unique joined rows with no join error;
3. exact supported-label baseline identity and no unexpected external label;
4. no change to CTRL, external-error, expected-tool-not-called, or required-contract-failed rows;
5. paired accuracy delta at least `+0.005`;
6. bootstrap 95% lower bound `> 0`;
7. corrections strictly exceed regressions;
8. positive delta on at least `9/12` models;
9. positive delta on at least `4/5` domains;
10. at least 100 supported OF-to-correct transitions across at least four domains.

The inherited Development evidence remains mandatory and is not replaced by these gates.

## Risks and claim ceiling

- The two judges share a rubric and are not human gold.
- The split changes generator models, not judge family or task family.
- RGP can hide extra unsupported structured claims when required values are also present; every Confirmation regression must be read.
- Macro-F1 improvement was negligible in Development, so the candidate cannot claim broad taxonomy improvement.
- General exact-match brittleness and semantic answer equivalence are established prior work.
- The surviving contribution is a narrow released-benchmark measurement correction, not an agent architecture or general evaluation theory.

## Review boundary

Only after a passing Confirmation and main-Codex audit may `review_v016/packet.md` be frozen with all listed v014 Development and v016 Confirmation bytes. Only then may three fresh direct leaf Reviewers start. Automated gates, voting, scores, and file existence cannot authorize Delivery.

