<!-- crl-v3-evidence-ids
["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Research Map

## Evidence boundary

ToolRet evaluates thousands of queries over a large merged tool corpus. [[evidence:ev-p085-large-corpus-scale]] Its reported query-only retrieval remains incomplete at top 10. [[evidence:ev-p085-retrieval-completeness-failure]] Official qrels are non-exhaustive because merged datasets can contain valid unlabelled alternatives. [[evidence:ev-p085-non-exhaustive-label]] All v005 conclusions are therefore conditional on frozen official qrels.

## Observed failure that motivates the operator

v004's one-donor negative control passed aggregate Development and Confirmation checks but failed the universal Claim on one dense-retrieval source with effect `0.0`. That result establishes neither that aligned instructions are generally uninformative nor that the chosen donor is a stable counterfactual reference. It exposes single-donor selection as the next falsifiable weakness.

## Changed computation

For each query, rank eligible donors from the same source by absolute regex-token instruction-length difference and deterministic SHA-256 tie break. Retain the first three donors whose target labels do not overlap the recipient. Evaluate query-only, aligned, generic, and each of the three donor-conditioned views over identical full-corpus retrieval.

The primary query effect is:

`aligned NDCG@10 - mean(donor_1 NDCG@10, donor_2 NDCG@10, donor_3 NDCG@10)`.

Source effects average query effects. The primary aggregate weights source configs equally and bootstraps source effects. Donor-view standard deviation is a secondary stability diagnostic.

## Mandatory baselines

- P085 `query_only` versus `aligned_full` is the external closest composition.
- v004's single closest donor is the internal closest implementation.
- `generic_full` controls generic task wording.
- BM25 and fixed all-MiniLM-L6-v2 provide sparse and dense retrieval mechanisms.

## Falsifiers

- Either retriever's equal-source cluster-bootstrap lower bound is not above zero.
- Either retriever's median source effect is not above zero.
- Aligned instruction target-document lexical support does not exceed the mean of the three donor supports.
- Any recipient lacks three eligible donors, any donor overlaps target labels, any output cell is missing, or any official metric fails independent recomputation.
- Formal review finds the same ToolRet donor-ensemble audit already reported or judges the increment too weak for the claimed research contribution.

## Allowed interpretation

If all gates pass, v005 may conclude only that, averaged across the frozen untouched ToolRet source clusters, aligned target-aware instructions contain target-linked retrieval information beyond a small deterministic distribution of same-source, length-matched wrong-target instructions. Source-level neutral or negative effects must remain visible and no universal source claim is allowed.

## Candidate Promotion Audit

### Before Development

The Target Failure is an interpretation error visible in retrieval NDCG: a target-derived aligned instruction can be cited as evidence about query-only open-world retrieval even though the view contains label-side target information. The Candidate changes the evaluation decision variable from one arbitrary matched instruction to the arithmetic mean of three prospectively ordered same-source, label-disjoint controls. This directly tests target-conditioning specificity and exposes donor dispersion; it does not merely improve execution, formatting, or validity metadata. P085 is the closest external composition and frozen v004 is the closest runnable internal component combination.

### After Development, before Confirmation

The baseline phenomenon is present. Across the eight Development source configs, aligned-minus-query-only equal-source NDCG@10 is `0.07499738042272683` for BM25 and `0.07702642167089152` for MiniLM. Mean-donor-minus-query-only is instead `-0.10909366607383955` and `-0.09222867296169124`. Thus arbitrary same-style instruction text does not reproduce the aligned advantage.

The Candidate primary effect passes every frozen Development gate. BM25 equal-source aligned-minus-mean-donor effect is `0.18409104649656638`, bootstrap 95% interval `[0.10634469541050025, 0.25511671510647216]`, and median source effect `0.2380903076413946`. MiniLM values are `0.16925509463258276`, `[0.09017196289982367, 0.2582591410222212]`, and `0.13451055015721752`. Both retrievers are positive on all eight Development sources. The aligned-minus-mean-donor lexical-support signature is `0.17360030336989457`.

The Main Codex independently verified 31,200 unique raw cells, exact twelve-cell coverage per query, ten unique ranked IDs per cell, official qrel bindings, and metric recomputation with maximum absolute error `0.0`. All 7,800 donor pairs were independently reconstructed under the frozen ordering with zero mismatch and zero target overlap. Independent lexical-support reconstruction had maximum absolute error `3.885780586188048e-16`.

Development and Confirmation are isolated by source dataset config; the claim is about an equal-source average, so source config is the analysis and bootstrap cluster. Query rows within a source are not treated as independent generalization clusters. The implement does not improve a deployed retriever; its final research output is a provenance-corrected evaluation contrast, and that contrast changes the target interpretation rather than a proxy metric. The result belongs to the complete three-donor control bundle, not to any single donor or lexical/semantic subcomponent.

The frozen Development evidence is strong enough to justify the already budgeted untouched Confirmation. Confirmation remains unauthorized until this appended Audit is hashed and recorded in the Run ledger.
