# W06 Card source audit C invocation

- Audit ID: `w06-audit-c`
- Start time: 2026-07-27T02:35:00+08:00
- Role: fresh independent source auditor, not a CRL Candidate Reviewer
- Output: `knowledge_base/corpus/card_audits/w06-audit-c/report.md`

## Exact request

Independently audit the twelve W06 Cards for P098–P101 (`paper/paper-p098.md`, `failure/failure-objective-equivalence-passes-nonbinding-errors.md`, `operator/operator-labeled-probe-injection-dual-verifier.md`; `paper/paper-p099.md`, `failure/failure-llm-judge-misses-executable-spec-errors.md`, `operator/operator-four-bucket-executable-spec-testing.md`; `paper/paper-p100.md`, `failure/failure-fixed-shortlist-depth-masks-hard-query-zero.md`, `operator/operator-chance-corrected-depth-reward.md`; `paper/paper-p101.md`, `failure/failure-single-execution-denotation-false-positive.md`, `operator/operator-neighbor-distilled-test-suites.md`) against the four official PDFs, their Evidence objects in `knowledge_base/corpus/evidence.json`, and the exact passages in `knowledge_base/knowledge.w06_next.sqlite`.

Check every AUTHOR_FACT and all numerical statements (550/7347; -2.86/-4.00; 49 of 191 = 25.7%; 77→58/82→78/59→51; hard-bucket zeros and 16.7±4.3; K=80.7 and 1.04 bits; ESM 2.6%/8.1% and the abstract's 2.5% discrepancy; 61%-submission undervalued by 8%). Check that every `[[evidence:...]]` token cites an Evidence whose quote actually supports the sentence. Check that CODEX_SYNTHESIS/HYPOTHESIS does not overstate: P098 main-table wins over frontier models without the home-field/teacher-distillation confounds; P099 model rankings without the budget/latency confound, or 26% beyond the self-judge no-tool configuration; P100 downstream 93.1-vs-87.1 without the conditional-selection bias, or BoR metric attribution (belongs to reference [30]); P101 suite reliability without the one-sided-audit boundary and the adapted-metric loosening. Return PASS or REVISE for each Card with the smallest exact correction. Do not evaluate a Candidate, do not run retrieval, do not modify any source asset.

## Allowed reads

- the twelve named Cards
- `knowledge_base/papers/P098_constraint_injection.pdf`, `P099_verus_specgym.pdf`, `P100_tool_shortlist_size.pdf`, `P101_distilled_test_suites.pdf`
- P098–P101 records in `knowledge_base/corpus/manifest.json` and `evidence.json`
- P098–P101 passages in `knowledge_base/knowledge.w06_next.sqlite`
- P098–P101 read-2 reports only if a source ambiguity remains
- workspace governance/environment files needed to operate

## Forbidden reads

- all earlier Card audits and dispositions, including the other W06 audits
- production calibration/blind queries, judgments, results, reports or revealed regressions
- reconciliation files and read_1 files
- other Cards/reads unless required only to confirm an ID collision
- Candidate, Commissioning or CRL research Reviewer assets

## Provenance to complete

- End time:
- Model/version:
- Procedural blinding:
- Thread/task ID:
- Report SHA-256:
- Mechanical result:
