# Main Codex Decision

```json
{
  "review_id": "v007",
  "packet_sha256": "21e585a0b252ea0b3e84e17d11515a1695557480564024c1b565e7cfee04322e",
  "reviewer_1_sha256": "96b3f55739ba1efe202d443c4597a68484e91cf9c7f42727108c9fdddcb78021",
  "reviewer_2_sha256": "97468daaef52562a7710fbfd22dc09e88226bc4911d29ca7fc3c8b1b89f199ca",
  "reviewer_3_sha256": "9c24ad824818309fe9dba4c960f7d277d90cbac51c32e2e0a416e1136d2099bf"
}
```

## Main Codex Decision Text

# v007 Main Codex Decision

## Disposition

`NO-GO FOR DELIVERY`. This is a scientific judgment by the Main Codex, not a vote, score, or automatic consequence of report labels. The fixed-byte experiment is real and reproducible, but the Candidate does not establish the proposed mechanism or a research implement worth delivering.

No `DELIVERY.md` may be created from v007. The Run remains `ACTIVE` and must advance to v008 with a different method kernel rather than another control-layer refinement of the same observation.

## Evidence Re-read By Main Codex

- Frozen Packet SHA-256: `21e585a0b252ea0b3e84e17d11515a1695557480564024c1b565e7cfee04322e`.
- Result SHA-256: `9d93edd2f99d16817adeb137b62b5beb93ee6744639252155c8f3d3c6e243c4e`.
- Reviewer 1 SHA-256: `96b3f55739ba1efe202d443c4597a68484e91cf9c7f42727108c9fdddcb78021`.
- Reviewer 2 SHA-256: `97468daaef52562a7710fbfd22dc09e88226bc4911d29ca7fc3c8b1b89f199ca`.
- Reviewer 3 SHA-256: `9c24ad824818309fe9dba4c960f7d277d90cbac51c32e2e0a416e1136d2099bf`.
- The Packet manifest contains 69 artifact and supplemental entries. The Main Codex re-read and hash-checked all listed bytes: 69/69 matched, the two raw files contained 12,000 rows each, all five JSONL datasets contained 44,745 rows in total, and the two NPY files loaded as finite `float32` arrays of shapes `(9436, 384)` and `(9309, 384)`.
- The Main Codex re-read all three complete raw Reviewer reports after all reports had returned and re-read the frozen P085 PDF. P085 physical pp. 5 and 7 already compare instruction-free and instruction-bearing retrieval, while physical pp. 19 and 21 show that query labels and target-tool descriptions are inputs to target-aware prompt generation and that TOOLRET-train uses the same strategy.
- The Main Codex independently downloaded Promptriever arXiv `2409.11136` from `https://arxiv.org/pdf/2409.11136` with exit code 0. The PDF SHA-256 is `8ed10aa540959344e2fdd596d54afd8b9e43083be6eea051456edac43b2f9671`, exactly matching Reviewer 1's source record. Physical p. 7 Table 6 and Q2 explicitly describe randomly pairing real instructions with other queries as `Swap Instructions`.

## What The Frozen Result Does Establish

For the exact two 1,000-row ranges, frozen corpora, official qrels, BM25 implementation, and pinned MiniLM outputs, aligned target-aware prompts score above the mean of the three deterministic length-approximated, label-disjoint wrong-target prompts. The aligned-minus-wrong-prompt effects are positive for both retrievers and all ten fixed row blocks in Development and Confirmation. The frozen rankings, metrics, donor identities, and captures are internally consistent.

The maximum defensible statement is a fixed-byte descriptive observation: target-aware ToolRet training prompts are associated with better official-qrel NDCG@10 than this particular wrong-prompt distribution. It is compatible with target-linked lexical signal in those generated prompts. It is not a causal estimate of target conditioning, a deployable improvement, or a new retrieval method.

## Fatal Scientific Grounds

1. The primary comparator does not identify the claimed mechanism. A wrong prompt changes semantic consistency with the recipient query, topic, irrelevant vocabulary, effective tokenizer length, and truncation as well as target access. It therefore bundles aligned information with active wrong-prompt interference.
2. The decomposition contradicts an interpretation of the large primary effect as practical gain. In Confirmation, BM25 aligned-minus-query-only is only `+0.007917`, with ten-block bootstrap interval `[-0.00554, 0.02455]`, while mean-wrong-minus-query-only is `-0.146810`. For MiniLM the corresponding values are `+0.029004` and `-0.168668`. Most of the registered aligned-minus-wrong effect is the wrong control making retrieval worse.
3. The aligned prompt is an oracle artifact generated with recipient labels and target-tool descriptions. It is unavailable to a query-only deployed retriever and can contain direct or paraphrased target information.
4. The novelty and lineage position is insufficient. P085 already reports instruction gains on ToolRet. Promptriever already uses random instruction swaps as a lexical-distribution control, while FollowIR, InF-IR, and Dual-View use stronger relevance-aware or semantically controlled counterfactuals. Three donors, approximate length matching, deterministic tie-breaking, and contiguous blocks are implementation details, not a new method contribution.
5. v007 changes no retriever, training objective, Agent decision, or end-to-end tool-use outcome. It is a static artifact audit. Its only delta from v006 is creating an output directory before `np.save`; execution repair cannot supply scientific novelty.
6. Confirmation is untouched at the selected row-byte level but not corpus-content independent, and the ten contiguous row blocks are not ten independent sources. This further limits external or inferential claims, although it does not invalidate the narrow fixed-byte observation.

## Reviewer Objection Adjudication

- Reviewer 1's prior-work collision is accepted. The Main Codex directly verified the decisive Promptriever Table 6 source and P085 source pages.
- Reviewer 2's estimand, oracle-input, truncation, and content-overlap objections are accepted as material. The absence of a query-aware, target-blind, same-composition control prevents causal attribution. The historical-byte completeness objection is also valid for any Delivery-wide interpretation, but the current v007 bytes alone are sufficient to decide no-go.
- Reviewer 3's practical-potential objection is accepted. The experiment measures a dataset construction property and does not implement a useful decision operator.
- Suggestions to add more controls are not adopted as a v007 rescue. They would require a new frozen version, and even a cleaner audit would remain too close to existing instructed-retrieval diagnostics unless it changes the method kernel and an outcome that matters.

## Unsupported Claims

v007 cannot support novelty of mismatched-instruction controls; causal target-conditioning benefit; general ToolRet or cross-domain generalization; independent-source replication; exhaustive relevance; deployable query-only benefit; improved retriever training; improved Agent routing or tool execution; or CCF-B-level method contribution.

## Next-Version Constraint

Freeze v007 without overwrite. v008 must start from a different evidence-backed failure and introduce a concrete changed computation with a direct final-outcome measurement and a fair strong comparator. It must not be another donor-matching, prompt-redaction, block-analysis, or claim-narrowing revision of v007.
