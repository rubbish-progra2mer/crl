# W06 Card source audit B invocation

- Audit ID: `w06-audit-b`
- Start time: 2026-07-27T02:35:00+08:00
- Role: fresh independent source auditor, not a CRL Candidate Reviewer
- Output: `knowledge_base/corpus/card_audits/w06-audit-b/report.md`

## Exact request

Independently audit the twelve W06 Cards for P094–P097 (`paper/paper-p094.md`, `failure/failure-selective-forgetting-collapses-with-context-length.md`, `operator/operator-incremental-injection-benchmark-reconstruction.md`; `paper/paper-p095.md`, `failure/failure-llm-freshness-judgment-prior-override-and-drift.md`, `operator/operator-extract-then-deterministic-max-assembly.md`; `paper/paper-p096.md`, `failure/failure-generator-aligned-verification-passes-shared-misreads.md`, `operator/operator-solver-simplification-query-verification.md`; `paper/paper-p097.md`, `failure/failure-solver-feasibility-near-zero-information-proxy.md`, `operator/operator-behavioral-perturbation-existence-test.md`) against the four official PDFs, their Evidence objects in `knowledge_base/corpus/evidence.json`, and the exact passages in `knowledge_base/knowledge.w06_next.sqlite`.

Check every AUTHOR_FACT and all numerical statements (80.0→14.0; serial-number guardrail wording; +10.8pp and 75%→61% drift; 91.5%/23-34%; 91.1% vs 0.5% and the verbatim "solver feedback catches syntax errors, not missing constraints"; perturbation factors and thresholds). Check that every `[[evidence:...]]` token cites an Evidence whose quote actually supports the sentence. Check that CODEX_SYNTHESIS/HYPOTHESIS does not overstate: P094 main-table cross-row rankings as same-backbone/same-chunk conclusions; P095 pipeline-level +10.8pp as resolver-isolated or as transferable without explicit total-order version markers; P096 gains without the best-of-K compute confound, or A.2/A.3 case transcripts as mechanism evidence; P097 ReLoop gains without the retry-budget confound and cited-baseline caveat. Return PASS or REVISE for each Card with the smallest exact correction. Do not evaluate a Candidate, do not run retrieval, do not modify any source asset.

## Allowed reads

- the twelve named Cards
- `knowledge_base/papers/P094_memoryagentbench.pdf`, `P095_deterministic_freshness.pdf`, `P096_verisimpl.pdf`, `P097_reloop.pdf`
- P094–P097 records in `knowledge_base/corpus/manifest.json` and `evidence.json`
- P094–P097 passages in `knowledge_base/knowledge.w06_next.sqlite`
- P094–P097 read-2 reports only if a source ambiguity remains
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
