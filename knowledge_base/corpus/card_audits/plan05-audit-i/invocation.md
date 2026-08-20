# PLAN_05 Card source audit I invocation

- Audit ID: `plan05-audit-i`
- Start time: 2026-07-20T07:42:00+08:00
- Role: fresh independent source auditor, not a CRL Candidate Reviewer
- Output: `knowledge_base/corpus/card_audits/plan05-audit-i/report.md`

## Exact request

Independently audit only `paper/paper-p084.md` and `failure/failure-semantically-related-toolkit-expansion.md` against P084's official PDF, the four P084 Evidence objects and their exact passages in `knowledge.plan05_84_scratch.sqlite`. Check every AUTHOR_FACT, all numerical/table statements, intervention controls, error-category wording, AST/execution boundary, generated-tool/equivalence-filter boundary, source_refs and Evidence hashes. Check that CODEX_SYNTHESIS/HYPOTHESIS does not overstate category-specific baseline increases, monotonic function-count causality, equal-token isolation, runtime malformed-argument exceptions, or a successful routing/filtering Operator. Return PASS or REVISE for each Card with the smallest exact correction. Do not evaluate a Candidate or implement, do not run retrieval, and do not modify any source asset.

## Allowed reads

- the two named P084 Cards
- `knowledge_base/papers/P084_function_calling_robustness.pdf`
- P084 records in `knowledge_base/corpus/manifest.json` and `evidence.json`
- P084 passages in `knowledge_base/knowledge.plan05_84_scratch.sqlite`
- P084 read-2 report only if a source ambiguity remains
- workspace governance/environment files needed to operate

## Forbidden reads

- all earlier Card audits and dispositions
- production calibration/blind queries, judgments, results, reports or revealed regressions
- other Cards/reads unless required only to confirm an ID collision
- Candidate, Commissioning or CRL research Reviewer assets
- saturation audits

## Provenance to complete

- End time: 2026-07-20T07:48:00+08:00
- Model/version: unavailable; auditor did not guess
- Procedural blinding: auditor reported reading only the allowed governance, two Cards, P084 PDF/manifest/Evidence/scratch passages and relevant skill instructions; a complete system-level trace remains unavailable
- Thread/task ID: `/root/plan05_p084_card_source_audit`
- Report SHA-256: `2553e5212da595f1454e1f6394a9dd725d0989238fbc92bdf459a3f9c6a5c136`
- Mechanical result: UTF-8 without BOM, LF-only; no source asset changed
