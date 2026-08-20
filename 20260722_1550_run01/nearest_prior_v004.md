# Main Codex Nearest Prior Record

## Frozen before review

This record was written before Development execution. Its final pre-review SHA and the source snapshot SHAs will be committed in `review_v004/packet.md` after all scientific bytes are frozen.

## Search views

- Changed computation: retrieval evaluation with a target-derived instruction versus a target-severed matched instruction.
- Key component: label-conditioned query enrichment, negative controls, within-source instruction permutation, and provenance-aware score interpretation.
- Full pipeline: official query/targets -> target-aware instruction -> query view -> full-corpus retriever -> qrel metrics -> scientific interpretation.
- Component combination and runnable baseline: original ToolRet `w/ inst.`/`w/o inst.` evaluation, BM25, all-MiniLM-L6-v2, and deterministic matched wrong-target instruction selection.

## Exact searches

- 2026-07-22, arXiv API, `all:"tool retrieval"`, 100 results sorted by submitted date. This found MagicSelector 2607.17751v1, PCTD 2607.15696v1, Multi-Field Tool Retrieval 2602.05366v1, ToolDreamer 2510.19791v2, Tool-DE 2510.22670v1, Re-Invoke 2408.01875v2, COLT 2405.16089v2, and other tool-retrieval pipelines.
- 2026-07-22, arXiv API, `all:"clarifying question" AND all:"tool"`; this found SAGE-Agent 2511.08798v2 and ToolDial 2503.00564v1.
- 2026-07-22, arXiv API, `all:"target-aware" AND all:"tool retrieval"`; no result was returned. This is only a search outcome, not proof of novelty.
- 2026-07-22, arXiv API, `all:"label leakage" AND all:"retrieval"`; no directly relevant tool-retrieval audit was returned. This is only a search outcome.
- 2026-07-22, formal knowledge-base Card searches for target-aware label-side evaluation failure, counterfactual evaluation audit operators, and ToolRet source lineage. Exact command outputs remain available in the main task transcript; the frozen scientific source record uses the P085 PDF and public dataset revision metadata.

## Component collisions

- Generic negative controls and permutation tests are established evaluation techniques. v004 does not claim invention of permutation importance or causal identification from arbitrary permutations.
- P085 explicitly generates instructions to bridge query intent and target-tool functionality. The target-conditioned nature of the input is not a new discovery.
- P087 and P089 enrich document or query representations to improve retrieval. v004 does not claim a retrieval method and does not use their generated text.

## Composition collisions

The closest composition is P085's `w/ inst.` versus `w/o inst.` experiment on the same ToolRet corpus and metrics. The remaining delta is a matched wrong-target instruction view that preserves source-specific instruction style and nearly matches token length while excluding label overlap, plus an explicit provenance scorecard. No reviewed source was found that reports this exact control on ToolRet.

## Full-pipeline collisions

No open source found in the searches above combines the official ToolRet aligned target-aware view, a same-source/length matched target-severed view, two retrieval families, source-disjoint confirmation, and source-cluster analysis. This remains an incomplete open-world search, not a proof that no such audit exists.

## Comparator roles and relative differences

- `query_only`: original user query; deployment-relevant baseline.
- `aligned_full`: original target-aware instruction plus query; original P085 conditional view.
- `mismatched_full`: another query's instruction from the same source config, selected by closest token length with no target-ID overlap, plus the original query; unique proposed negative control.
- `generic_full`: fixed non-target instruction plus original query; formatting and generic-task control.
- BM25 and all-MiniLM-L6-v2: neutral sparse and dense retrievers over identical corpus bytes.

## Closest-composition conclusion

P085 is the mandatory closest composition and must be reported first. The experiment can support only a narrow interpretation audit: whether aligned target-aware input carries target-linked retrieval advantage beyond a matched non-target instruction on the selected source clusters. It cannot establish a new retrieval algorithm, benchmark invalidity, end-to-end Agent benefit, or general label leakage outside this construction.
