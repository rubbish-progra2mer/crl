<!-- crl-v3-evidence-ids
["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Research Map

ToolRet is a large-corpus retrieval setting with incomplete query-only retrieval and non-exhaustive merged labels. [[evidence:ev-p085-large-corpus-scale]] [[evidence:ev-p085-retrieval-completeness-failure]] [[evidence:ev-p085-non-exhaustive-label]] v006 tests the separate training artifact, where each row supplies a generated prompt plus positive and negative tool texts.

For each phase, hash each tool text to form a unique phase-wide corpus ID. Convert positive strings to qrels. Select three label-disjoint wrong prompts from the same 1,000-row phase by token-length difference and deterministic SHA tie break. Retrieve query-only, aligned prompt, three wrong-prompt, and generic views over the full phase corpus.

Primary query effect is aligned NDCG@10 minus mean wrong-prompt NDCG@10. Average within ten fixed 100-row blocks, then equally across blocks with a 20,000-replicate block bootstrap. Require both retrievers' lower bounds, block-effect medians, and lexical-support mechanism means above zero; require complete donor and raw-cell integrity.

The permitted conclusion is limited to target-linked information in generated training prompts on the two frozen row ranges. It is not evidence of deployable improvement, label exhaustiveness, causal effect, or all-row generalization.

## Candidate Promotion Audit

Before Development, the Target Failure was defined as interpreting target-aware generated prompt retrieval as query-only evidence. The three-donor operator changes the actual input control distribution, not execution metadata; P085 and v005 are the closest external and internal compositions.

After Development, the frozen 1,000 rows and 9,436-tool phase corpus produced 12,000 complete unique cells. Independent reconstruction found zero donor, ranking, qrel, or metric errors. BM25 equal-block effect is `0.17294899966329502`, median `0.16745071801763145`, bootstrap `[0.1575434082996223, 0.19102766900522142]`. MiniLM values are `0.20330747026568474`, `0.20031678887676024`, and `[0.19424093392342617, 0.21287438671633252]`. All ten blocks are positive for both; mechanism mean is `0.21661500690727706`.

The analysis cluster is the preregistered contiguous 100-row block, not individual rows. The implement changes the final provenance interpretation of training-prompt retrieval, not a deployable retriever score. The complete donor-control bundle receives attribution. Development passes and the Main Codex authorizes acquisition of the still-untouched row range `[207826,208826)`.

## Confirmation Audit

The untouched Confirmation acquisition returned the exact contiguous IDs `train_207826` through `train_208825`, 1,000 queries in ten fixed 100-row blocks, and a 9,309-document deduplicated phase corpus. The new Confirmation corpus embeddings were generated independently of Development. The captured evaluation exited `0` and produced all 12,000 expected cells.

The Main Codex independent audit verified 12,000 unique cell keys, 12,000 complete unique top-10 lists whose IDs belong to the frozen corpus, 3,000 deterministic label-disjoint donor pairs, zero target-overlap pairs, exact qrel metric recomputation, and exact ten-block/bootstrap reconstruction. Metric and summary maximum absolute errors were `0.0`; lexical-support maximum absolute error was `3.3306690738754696e-16`.

BM25 equal-block effect is `0.15472698575926586`, median `0.15881437019579883`, bootstrap `[0.13810078540627505, 0.17154230511897298]`. MiniLM values are `0.19767190048609523`, `0.1985772107226651`, and `[0.18139115743783601, 0.21385848024999743]`. Both retrievers are positive in all ten blocks. The independently recomputed lexical mechanism mean is `0.21566037397225948`.

The Confirmation gates pass only for the frozen Claim boundary: target-aware generated training prompts contain positive-tool-linked retrieval information beyond this deterministic three wrong-prompt control distribution on these two fixed ranges. This is not an end-to-end improvement, deployable retrieval claim, causal claim, exhaustive-label claim, or all-row generalization.

The frozen `candidate_v007.md` has one disclosed version-label defect in its final procedural sentence: it says a failure freezes `v006`; under the Run protocol a v007 failure would freeze `v007`. The computation, row ranges, thresholds, Claim Contract, and actual success path are unaffected. The executed Candidate bytes are not overwritten.
