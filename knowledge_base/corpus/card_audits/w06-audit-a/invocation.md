# W06 Card source audit A invocation

- Audit ID: `w06-audit-a`
- Start time: 2026-07-27T02:35:00+08:00
- Role: fresh independent source auditor, not a CRL Candidate Reviewer
- Output: `knowledge_base/corpus/card_audits/w06-audit-a/report.md`

## Exact request

Independently audit the twelve W06 Cards for P090–P093 (`paper/paper-p090.md`, `failure/failure-fixed-single-granularity-memory.md`, `operator/operator-entropy-routed-multi-granularity-retrieval.md`; `paper/paper-p091.md`, `failure/failure-cosine-cannot-separate-contradiction-from-duplicate.md`, `operator/operator-deterministic-sro-supersession-ledger.md`; `paper/paper-p092.md`, `failure/failure-answer-accuracy-without-conflict-recognition.md`, `operator/operator-support-evidence-whitebox-retrieval-metrics.md`; `paper/paper-p093.md`, `failure/failure-dense-retriever-surface-bias-collapse.md`, `operator/operator-paired-single-factor-bias-decomposition.md`) against the four official PDFs, their Evidence objects in `knowledge_base/corpus/evidence.json`, and the exact passages in `knowledge_base/knowledge.w06_next.sqlite`.

Check every AUTHOR_FACT and all numerical statements (AUROC 0.5926; 0.99→0.33 and 0.04→0.25 fabrication; CRS 0.2501; <10% foil rate; 250 queries per setting; entropy/router formulas' described roles). Check that every `[[evidence:...]]` token cites an Evidence whose quote actually supports the sentence. Check that CODEX_SYNTHESIS/HYPOTHESIS does not overstate: P090 pipeline-level gains as router-isolated; P091 single-embedder AUROC as universal; P092 judge-chain CRS absolute values; P093 pairwise preference as real top-k attack success, or dense-specific claims without a BM25 control. Return PASS or REVISE for each Card with the smallest exact correction. Do not evaluate a Candidate, do not run retrieval, do not modify any source asset.

## Allowed reads

- the twelve named Cards
- `knowledge_base/papers/P090_memgas.pdf`, `P091_memstrata.pdf`, `P092_memconflict.pdf`, `P093_dense_retriever_collapse.pdf`
- P090–P093 records in `knowledge_base/corpus/manifest.json` and `evidence.json`
- P090–P093 passages in `knowledge_base/knowledge.w06_next.sqlite`
- P090–P093 read-2 reports only if a source ambiguity remains
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
