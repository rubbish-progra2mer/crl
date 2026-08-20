<!-- crl-v3-evidence-ids
["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Research Map

## Observed Failure and boundary

- [AUTHOR_FACT] ToolRet contains 7,615 tasks and 43,215 merged tools. [[evidence:ev-p085-large-corpus-scale]]
- [AUTHOR_FACT] In query-only evaluation, all reported retrievers have Completeness@10 below 35% and Recall@10 below 52%. [[evidence:ev-p085-retrieval-completeness-failure]]
- [AUTHOR_FACT] The merged benchmark has non-exhaustive labels because similar tools from another source dataset may also be valid. [[evidence:ev-p085-non-exhaustive-label]]
- [AUTHOR_FACT] The original paper separately defines `w/o inst.` as query-only and `w/ inst.` as query plus an instruction generated to bridge query intent and the target tools. The paper reports that 92.3% of reviewed instructions describe target-tool features and 89.2% comprehensively describe all target tools. This fact is bound to the P085 PDF and frozen source excerpts in `sources_v003/`; it is not inferred from retrieval scores.
- [CODEX_SYNTHESIS] A target-aware score is a legitimate conditional benchmark view, but it cannot by itself establish query-only open-world retrieval. A negative control that preserves instruction style while severing target identity can measure how much of the score is label-conditioned.

## Intervention stage

The intervention is at evaluation construction, after a query and qrels exist but before retrieval scoring. It reads the official query, target-aware instruction, source configuration, target IDs, and full corpus. It outputs four explicitly named query views and paired retrieval metrics. It does not alter the retriever or the ground-truth labels.

## Operator shortlist and source recheck

### Original two-view ToolRet evaluation

Baseline -> changed computation: query-only retrieval -> concatenate the target-aware instruction and query before retrieval. The P085 PDF directly defines both views. Its limitation for the present question is that it does not include a target-severed instruction negative control.

### Evidence audit before benchmark scoring

Baseline -> changed computation: treat benchmark inputs as self-describing -> inspect provenance and test a label-severing counterfactual before interpreting a score. This is an evaluation operator, not a policy improvement. It transfers only if the counterfactual preserves non-target style and source information.

### Query/document expansion

Baseline -> changed computation: enrich the query or document to improve retrieval. P087 and P089 are direct expansion priors. They are not the selected operator because this version does not propose deployable enrichment and must not present label-conditioned text as inference-time information.

## Competing method kernels

### Kernel A: local contrastive reranking among semantically close tools

Target Failure: related-tool distractors. Changed computation: rerank a dense top-k by local competitor residuals. Direct falsifier: an existing method already performs progressive hard-negative reranking or corpus-neighborhood correction with the same decision variable.

### Kernel B: clarification before retrieval

Target Failure: underspecified queries. Changed computation: ask one schema-derived discriminative question before selecting a tool. Direct falsifier: an existing structured-uncertainty method already selects tool-parameter questions using value of information.

### Kernel C: provenance-aware target-instruction negative control

Target Failure: interpreting label-conditioned target-aware scores as evidence about query-only retrieval. Changed computation: evaluate aligned, target-severed matched, generic, and query-only views under identical retrievers and corpus bytes. Direct falsifier: the matched view does not separate aligned from non-target instructions on source-disjoint confirmation, or the same audit is already reported for ToolRet.

## Natural-language disposition

Kernel A is killed for v003 because MagicSelector (arXiv:2607.17751v1, 2026-07-20) directly combines progressive reranking and hard-negative discrimination among similar tools; CSLS, MMR, COLT, and NNN also occupy its core computation. Kernel B is killed because SAGE-Agent (arXiv:2511.08798v2) already uses structured tool-parameter uncertainty and EVPI to decide which clarifying question to ask, while ToolDial already evaluates missing-information clarification. Kernel C is kept as a narrow evaluation implement. Its closest prior is the original ToolRet `w/ inst.` versus `w/o inst.` ablation; the proposed delta is only the source/length-matched target-severing negative control and provenance-explicit scorecard.

## Candidate Promotion Audit

### Before Development

The Target Failure is directly visible in the interpretation attached to NDCG@10, Recall@10, and Completeness@10: a score computed from target-conditioned input can be overextended to query-only open-world retrieval. The Candidate changes the evaluated input view, not the retriever. It compares an aligned target-aware instruction with a same-source, token-length-matched instruction whose labels do not overlap, plus query-only and generic controls. This can affect the Target Failure because the aligned-minus-mismatched difference directly estimates target-linked information unavailable to a query-only system. It is not a JSON-validity, execution, or formatting proxy. The closest existing computation is ToolRet's own two-view `w/ inst.`/`w/o inst.` evaluation; generic permutation and negative-control logic are borrowed and are not claimed as new.

### After Development, before Confirmation

Not yet written. This subsection will be appended only after reading the frozen Development output.

## Unique narrow Gap

ToolRet reports query-only and target-aware retrieval separately, but the reviewed paper does not report a same-source, length-matched wrong-target instruction control. The missing computation is a provenance-aware negative-control scorecard that quantifies the label-conditioned part of `w/ inst.` gains without claiming to improve a retriever.
