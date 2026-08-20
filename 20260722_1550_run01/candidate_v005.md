<!-- crl-v3-evidence-ids
["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Candidate Implement

## One-sentence method kernel

Replace ToolRet's single matched wrong-target instruction control with a three-donor, same-source, label-disjoint, closest-length control distribution and report aligned target-aware retrieval advantage at the source-cluster level.

## Failure/Evidence -> Operator -> Gap lineage

ToolRet's large-corpus query-only task remains incomplete under official qrels. [[evidence:ev-p085-large-corpus-scale]] [[evidence:ev-p085-retrieval-completeness-failure]] Those qrels are non-exhaustive, so scores remain benchmark-conditional. [[evidence:ev-p085-non-exhaustive-label]] v004 added one target-severed donor but failed a universal per-source Claim when MiniLM was neutral on one source. The selected operator is a minimal donor ensemble that measures rather than hides control-selection variability. The Gap is the absence of a donor-distribution reference for interpreting P085's target-aware instruction scores.

## Baseline and closest composition

The external baseline is P085's official `query_only` versus `aligned_full` comparison over the full public corpus. The internal closest implementation is frozen v004: one same-source, target-disjoint donor selected by minimum token-length difference and SHA-256 tie break. v005 changes only donor multiplicity, aggregation, source split, and the Claim boundary required by that change.

## Changed computation

1. For each official query, sort all eligible same-source, label-disjoint donors by absolute regex-token instruction-length difference and SHA-256 of `(recipient_id, donor_id)`.
2. Retain the first three donors; preserve each donor ID, source, target IDs, token-length difference, and overlap count.
3. Retrieve six views: `query_only`, `aligned_full`, `mismatched_full_1`, `mismatched_full_2`, `mismatched_full_3`, and `generic_full`.
4. Define the primary per-query effect as aligned NDCG@10 minus the arithmetic mean of the three mismatched NDCG@10 values.
5. Average per query within each source, then equally across sources; form a source-cluster bootstrap interval with seed `20260722` and 20,000 replicates.
6. Report the median source effect, number and identity of non-positive sources, mean donor-view NDCG standard deviation, and aligned lexical support minus mean donor lexical support.

## Minimal Claim Contract

Development may open Confirmation only if, for both BM25 and MiniLM:

- the equal-source mean primary effect is positive and its source-cluster bootstrap 95% lower bound is above zero;
- the median source effect is above zero;
- the aligned-minus-mean-donor lexical-support signature is positive; and
- every query has exactly three eligible donors with zero target overlap and every required raw cell passes independent integrity and qrel-metric recomputation.

The same conditions must pass on untouched Confirmation. No condition requires every source effect to be positive. All non-positive sources must be disclosed by name and value.

If supported, the allowed conclusion is: averaged across these frozen source clusters, ToolRet's aligned target-aware instruction view contains target-linked retrieval information beyond a deterministic three-donor same-source/length-matched control distribution, so it must not be described as query-only open-world retrieval evidence.

## Phase isolation

Development uses eight previously untouched configs (2,600 advertised rows): `apigen`, `craft-vqa`, `gorilla-huggingface`, `reversechain`, `toolalpaca`, `toolbench-sam`, `tooleyes`, `toollens`.

Confirmation uses the other fifteen previously untouched configs (2,764 advertised rows): `appbench`, `autotools-food`, `autotools-music`, `autotools-weather`, `gpt4tools`, `gta`, `mnms`, `restgpt-spotify`, `taskbench-huggingface`, `taskbench-multimedia`, `tool-be-honest`, `toolbench`, `toolemu`, `toolink`, `ultratool`.

Confirmation query bytes cannot be acquired or read before Main Codex Promotion Audit. The already touched fixed corpus and embeddings are reused identically in both phases and are not outcome partitions.

## Cost and fairness

All six views use identical corpus bytes, qrels, retriever settings, top-k 10, local permissions, and model revision. Relative to v004, each query adds two BM25 scorings and two dense query encodings; no corpus encoding is repeated. There are no LLM tokens, paid calls, tuning, or tool execution.

## Limits and kill conditions

- The implement is an evaluation audit, not a deployable retriever improvement.
- Three donors are a fixed minimal sensitivity sample, not an optimal or exhaustive counterfactual distribution.
- No universal per-source, causal, benchmark-invalidity, label-exhaustiveness, or end-to-end Agent claim is allowed.
- Kill if either Confirmation bootstrap lower bound or median source effect is non-positive, the mechanism signature is non-positive, donor coverage/overlap fails, or formal review finds an exact collision or insufficient research contribution.
- A failed v005 remains frozen and the same Run continues to v006; it never terminates the Run by itself.
