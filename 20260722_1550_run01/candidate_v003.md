<!-- crl-v3-evidence-ids
["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Candidate Implement

## One-sentence method kernel

Add a same-source, token-length-matched wrong-target instruction negative control to ToolRet evaluation so that target-conditioned instruction benefit is reported separately from query-only retrieval evidence.

## Failure/Evidence -> Operator -> Gap lineage

Large-corpus query-only tool retrieval remains incomplete on ToolRet. [[evidence:ev-p085-large-corpus-scale]] [[evidence:ev-p085-retrieval-completeness-failure]] The benchmark also has non-exhaustive labels, so all claims remain conditional on official qrels. [[evidence:ev-p085-non-exhaustive-label]] The original target-aware view deliberately gives retrievers an instruction generated around target-tool functionality. The selected operator is an evaluation negative control: preserve source/style/length while severing target identity. The Gap is the absence of that control in the original two-view comparison.

## Baseline computation

For each official query, retrieve from the full public tool corpus at the pinned revision with either (a) the user query alone or (b) the official aligned target-aware instruction concatenated with the query. Score NDCG@10, Recall@10, and Completeness@10 against unchanged official target IDs. The paper reports 43,215 tools, while current public metadata advertises 44,453 rows; acquisition must report the actual pinned row count and this drift rather than silently equating them.

## Changed computation

1. Keep the retriever, corpus, qrels, top-k, tokenization/model, and query fixed.
2. Within the same source config, choose the non-overlapping-label instruction with minimum absolute token-length difference; break ties by SHA-256 of `(query_id, candidate_id)`.
3. Evaluate `mismatched_full = matched_wrong_target_instruction + query`.
4. Also evaluate a fixed generic instruction plus query.
5. Report aligned-minus-mismatched paired effects by source config and equal-source aggregate.

Borrowed components are BM25, all-MiniLM-L6-v2, standard retrieval metrics, and negative-control logic. The only proposed delta is the deterministic source/length-matched target-severing view and its provenance-explicit report.

## Closest-composition difference

P085 already compares `query_only` and `aligned_full`. v003 adds `mismatched_full` and `generic_full`; it accesses labels only to construct an offline evaluation control and never presents this as deployable inference. All four views use identical corpus bytes and retriever budgets. The extra cost is two more query encodings/scorings per evaluated query plus deterministic matching.

## Minimal Claim Contract

The primary Claim is supported only if, on both Development and untouched source-disjoint Confirmation:

- `aligned_full - mismatched_full` NDCG@10 is positive for BM25 and all-MiniLM-L6-v2 in every included source config;
- the equal-source cluster-bootstrap 95% lower bound is above zero for both retrievers; and
- aligned instruction tokens show greater target-document lexical support than matched instruction tokens.

If supported, the allowed conclusion is: on these official ToolRet source clusters, the aligned target-aware view contains target-linked retrieval information beyond same-source instruction style and length, so its scores must not be cited as query-only open-world retrieval evidence.

The experiment cannot support claims that ToolRet is invalid, that query-only labels are exhaustive, that any deployable retriever improves, that target-aware evaluation has no legitimate use, or that end-to-end tool execution improves.

## Implement contract

- `implementation_v003/audit.py`: acquisition, matching, BM25, dense retrieval, metric, and bootstrap implementation.
- `implementation_v003/config.json`: pinned revisions, source configs, model identity, top-k, bootstrap seed/count, and exact view definitions.
- Entry points: `audit.py acquire --phase development`, `audit.py evaluate --phase development`, then only after Main Codex authorization the corresponding `confirmation` commands.
- Python: `D:/Desktop/crl/crl_agent_v3/.venv/python.exe`.
- CWD: `implementation_v003/`.

## Neutral comparators

- `query_only`: official query.
- `aligned_full`: official target-aware instruction plus query.
- `mismatched_full`: deterministic same-source wrong-target instruction plus query.
- `generic_full`: fixed instruction `Retrieve tools that satisfy the user's request.` plus query.
- `bm25`: local standard BM25 with fixed `k1=1.5`, `b=0.75`.
- `minilm`: cached `sentence-transformers/all-MiniLM-L6-v2`, normalized cosine similarity on CUDA.

## Experiment contract

Primary metric: NDCG@10 aligned-minus-mismatched, calculated per query and aggregated equally across source configs. Mechanism signature: target-document IDF-weighted lexical support of aligned instruction exceeds the matched instruction. Secondary metrics: Recall@10, Completeness@10, query-only and generic comparisons. Development uses four web source configs; Confirmation uses eight untouched code/customized source configs. No hyperparameter is selected from outcomes.

Artifacts include the implement, config, normalized public rows, acquisition manifest, exact split manifest, environment capture, retrieval outputs, summary, `execution.json`, `stdout.bin`, and `stderr.bin` for every attempt that affects the result.

## Confirmation isolation and analysis unit

Development configs: `apibank`, `restgpt-tmdb`, `rotbench`, `taskbench-daily`.

Untouched Confirmation configs: `craft-math-algebra`, `craft-tabmwp`, `gorilla-pytorch`, `gorilla-tensor`, `metatool`, `t-eval-dialog`, `t-eval-step`, `toolace`.

The isolation unit is source dataset config, not entity. The primary analysis unit is source config; query-level values are retained but not treated as independent evidence for the equal-source claim. Confirmation bytes are not acquired or read before Development promotion.

## Cost and bundle attribution

Both conditions use the same local models, corpus, top-k, and tool permissions. There are no LLM tokens, paid calls, or external execution tools. Acquisition uses public read-only HTTPS. Dense encoding uses one RTX 5060 Ti; BM25 uses CPU. The audit identifies the whole view-construction delta, not a semantic-versus-lexical subcomponent.

## Risks and kill conditions

- Kill if the aligned-minus-mismatched effect is not positive in every source config for both retrievers.
- Kill if either retriever's confirmation cluster-bootstrap lower bound is not above zero.
- Kill or reframe if matching fails for more than 1% of queries.
- Reframe if the result is driven only by exact tool names or one source family.
- Kill as research contribution if Reviewer 1 finds the same matched negative control already reported for ToolRet.
- Never convert a negative v003 result into a Run terminal state; freeze it and continue as v003.
