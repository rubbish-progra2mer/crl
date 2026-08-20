# Main Codex Raw Analysis v026

The independent replay returned `AUDIT_OK` with zero score and metric error. I then joined the complete frozen raw output to all three frozen datasets, source records and acquisition manifests in one read-only analysis. The analysis exited 0.

## Integrity

- 4,256 source rows were unique; the prospective eligibility rule produced 4,072 raw rows and 4,072 source records across 228 tasks.
- Raw row IDs and source-record row IDs were identical subsets of the datasets. Task, generator, target, source dataset, source path and source SHA matched for every evaluated row.
- All 4,256 dataset source paths and SHAs matched the union of 4,980 immutable manifest source-file records; join errors were zero.
- The frozen independent auditor replayed 9 OOF bundles and 20,360 method scores with maximum score error 0 and maximum metric/gate/structural error 0.

## Overall and fixed controls

Candidate CMCD achieved AUC `0.8832616788` and TPR@5%FPR `0.6340118745`. The four controls were:

- `direct`: AUC `0.8570308085`, TPR `0.5050890585`;
- `triple_query`: AUC `0.8651839909`, TPR `0.5178117048`;
- `consensus_no_abs`: AUC `0.8655845737`, TPR `0.5636132316`;
- strongest `single_support`: AUC `0.8732057902`, TPR `0.5843935539`.

Candidate-minus-strongest AUC was `+0.0100558886`; the 2,000-task-bootstrap interval was `[0.0033534428, 0.0171627105]`. Candidate strictly exceeded every control. At separately selected empirical 5% FPR thresholds, Candidate and strongest both had TN/FP `1629/85`; Candidate had FN/TP `863/1495` versus `980/1378`. Candidate alone classified 172 rows correctly and strongest alone 55.

Within-task exploit-versus-baseline orderings were: both correct 18,078; Candidate-only correct 803; strongest-only correct 336; neither 1,513, across 20,730 pairs. Among tasks with both classes, Candidate-minus-strongest task AUC signs were 77 positive, 107 tied and 41 negative; three tasks had one class only.

## Generalization slices

All three held-out task folds were positive: fold deltas `+0.0100027`, `+0.0066077` and `+0.0135161`. The required held-out-generator slices were not all nonnegative:

- Claude Opus 4.6: `+0.0112634324`;
- Gemini 3.1 Pro: `-0.0042559106`;
- GPT-5.4: `+0.0128789825`.

At generator-by-fold resolution, Gemini fold 0 was slightly positive (`+0.0016949`) but folds 1 and 2 were negative (`-0.0076933`, `-0.0088819`). Claude and GPT were positive in all six corresponding fold cells. This is not a single-fold accident, and the preregistered `all_generator_slices_nonnegative` gate is false.

Source-dataset deltas were positive for OpenThoughts-TB-dev (`+0.0446105`), TerminalBench-original (`+0.0068597`), seta_2026_01_29 (`+0.0127361`) and terminal-bench-pro (`+0.0022936`), but negative for terminal-bench__2.0 (`-0.0330063`). Diagnostic support-count bins were also heterogeneous: count 2 `-0.0123810`, counts 3–4 `+0.0157355`, counts 5–7 `-0.0004848`, counts 8+ `+0.0065785`. These post-result slices cannot be used to narrow the Claim.

Every held-out query used exactly the two other generator families as its support-model set; support counts ranged 2–21 with median 4. The negative Gemini result therefore cannot be explained by a missing support family under the frozen eligibility rule.

## Gate fact

Seven of eight mechanical gates were true. The sole false gate was the prospectively conjunctive `all_generator_slices_nonnegative`. Gate count is not a vote: one failed conjunctive gate is sufficient to close Confirmation. Bucket 0 remains untouched, and no Review Packet or Reviewer is allowed for v026.
