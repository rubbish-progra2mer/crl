<!-- crl-v3-evidence-ids
["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Candidate Implement

## Method kernel

Measure ToolRet training-prompt target conditioning against a deterministic three wrong-prompt distribution while retrieving from the complete phase-wide corpus.

## Evidence and gap

ToolRet operates at large corpus scale and its official labels are not exhaustive. [[evidence:ev-p085-large-corpus-scale]] [[evidence:ev-p085-retrieval-completeness-failure]] [[evidence:ev-p085-non-exhaustive-label]] P085 publishes target-aware prompts for training but no matched wrong-prompt distribution that separates target-linked prompt information from generic instruction form.

## Computation

- Pin `mangopy/ToolRet-Training-20w@fdf5a317455b1e60785de7ba587496aa6cc878e4`.
- Development rows are `[0,1000)`; untouched Confirmation rows are `[207826,208826)`.
- Deduplicate all phase positive/negative tool strings by SHA-256 into one phase corpus. Positive hashes are official row qrels; no per-query oracle menu is used.
- Assign ten contiguous 100-row `source_config` blocks for analysis. Select three non-self, label-disjoint donors from the full phase by minimum prompt token-length difference and SHA tie break.
- Evaluate `query_only`, `aligned_full`, three `mismatched_full_N` views, and `generic_full` using identical BM25 and fixed all-MiniLM-L6-v2 top-10 retrieval.
- Primary effect is aligned NDCG@10 minus the mean of three wrong-prompt NDCG values, aggregated equally over the ten blocks with seed `20260722`, 20,000-replicate block bootstrap.

## Claim Contract

For both retrievers in Development and untouched Confirmation: equal-block mean must be positive, bootstrap lower bound must exceed zero, median block effect must be positive, and aligned-minus-mean-donor lexical support must be positive. Every row must have three distinct label-disjoint donors; all `rows x 6 x 2` cells and top-10 rankings must be complete and official qrel metrics must independently recompute.

If supported, the only Claim is that target-aware prompts carry positive-tool-linked retrieval information beyond a three wrong-prompt control distribution on these two fixed ToolRet-training ranges. No universal, causal, deployable, benchmark-invalidity, or end-to-end claim is permitted.

Failure freezes v006 and continues the Run; success only permits a frozen Review Packet and three independent Reviewers.
