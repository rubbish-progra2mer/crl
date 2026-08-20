<!-- crl-v3-evidence-ids
["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Research Map

ToolRet is a large-corpus retrieval setting with incomplete query-only retrieval and non-exhaustive merged labels. [[evidence:ev-p085-large-corpus-scale]] [[evidence:ev-p085-retrieval-completeness-failure]] [[evidence:ev-p085-non-exhaustive-label]] v006 tests the separate training artifact, where each row supplies a generated prompt plus positive and negative tool texts.

For each phase, hash each tool text to form a unique phase-wide corpus ID. Convert positive strings to qrels. Select three label-disjoint wrong prompts from the same 1,000-row phase by token-length difference and deterministic SHA tie break. Retrieve query-only, aligned prompt, three wrong-prompt, and generic views over the full phase corpus.

Primary query effect is aligned NDCG@10 minus mean wrong-prompt NDCG@10. Average within ten fixed 100-row blocks, then equally across blocks with a 20,000-replicate block bootstrap. Require both retrievers' lower bounds, block-effect medians, and lexical-support mechanism means above zero; require complete donor and raw-cell integrity.

The permitted conclusion is limited to target-linked information in generated training prompts on the two frozen row ranges. It is not evidence of deployable improvement, label exhaustiveness, causal effect, or all-row generalization.
